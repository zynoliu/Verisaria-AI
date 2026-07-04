"""Sixth-run playability driver (real MiniMax) — pressured-party sincerity probe.

Focus: skyglass_memory_inquest. Move to the orchid house, talk sincerely /
offer face-saving to greenhouse_sura (a guarded, pressured party), and capture
the appraisal log line `<npc> appraises player: Δ{...} → {...}` PER TICK so we
can tell apart (a) LLM now gives a delta vs (b) delta eaten by store decay.

Reads actions one-per-line from a QUEUE file (tail). Flushes transcript each
tick. Per-tick watchdog ~90s. Only world_premise is injected (no world_state_vars).
"""
from __future__ import annotations
import os, sys, time, logging, threading
from pathlib import Path

ROOT = Path("/Users/gensliu/Documents/rpg")
os.chdir(ROOT); sys.path.insert(0, str(ROOT / "src"))
for raw in (ROOT / ".env").read_text().splitlines():
    line = raw.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip("'\""))

import verisaria.protocol as P
from verisaria.runtime.session import GameSession
from verisaria.protocol.engine_session import EngineSession

PACK = "fixtures/content_packs/skyglass_memory_inquest.json"
OUTDIR = ROOT / "reports" / "playability_audit_sixth_run"
OUTDIR.mkdir(parents=True, exist_ok=True)
QUEUE = OUTDIR / "queue.txt"
TRANS = OUTDIR / "transcript.md"
LOGF = OUTDIR / "run.log"

# --- file log on parent 'verisaria' (catches verisaria.relationship etc.) ---
h = logging.FileHandler(LOGF, mode="w", encoding="utf-8")
h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
lg = logging.getLogger("verisaria"); lg.setLevel(logging.INFO); lg.addHandler(h)

# --- in-memory capture of appraisal lines, drained per tick ---
class CaptureHandler(logging.Handler):
    def __init__(self):
        super().__init__(); self.buf = []
    def emit(self, record):
        msg = record.getMessage()
        if "appraises player" in msg:
            self.buf.append(msg)
cap = CaptureHandler(); cap.setLevel(logging.INFO)
logging.getLogger("verisaria.relationship").addHandler(cap)

QUEUE.write_text("", encoding="utf-8")
tf = TRANS.open("w", buffering=1, encoding="utf-8")
def w(s=""): tf.write(s + "\n"); tf.flush()


def make_session():
    g = GameSession(PACK, save_dir="_pa6_saves", llm_backend="minimax")
    g._progress_sink = lambda m: None
    prem = getattr(g.pack, "world_premise", None)
    if prem is not None:
        try:
            prem.npc_daily_rhythm = True
        except Exception as e:
            w(f"<!-- premise inject failed: {e} -->")
    return g


def snap_line(s):
    return f"time={s.time_of_day!r} clock={s.clock!r} weather={s.weather!r} loc={s.location.name!r}"

def present_str(s):
    return ", ".join(f"{e.name}({e.id})" for e in s.present) or "(无人)"

def rel_str(s):
    if not s.relationships: return "(无)"
    out = []
    for r in s.relationships:
        d = "/".join(f"{x.label}:{x.value:.3f}" if hasattr(x,'value') else str(x) for x in r.descriptors)
        out.append(f"{r.name}[{d}]")
    return "; ".join(out)

RESULT = {}
def do_tick(es, text):
    RESULT.clear()
    def runner():
        try:
            RESULT['r'] = es.submit(P.SubmitInput(text=text))
        except Exception as e:
            import traceback
            RESULT['err'] = traceback.format_exc()
    th = threading.Thread(target=runner, daemon=True); th.start()
    th.join(timeout=90)
    if th.is_alive():
        RESULT['timeout'] = True
    return RESULT

def emit(tick_no, action, kind, r):
    w("\n" + "="*80)
    w(f"## 拍 {tick_no} — 玩家输入 [{kind}]")
    w(f"> {action}")
    if r.get('timeout'):
        w("\n**[WATCHDOG TIMEOUT >90s — tick skipped]**")
        return None
    if r.get('err'):
        w("\n**[EXCEPTION]**\n```\n" + r['err'] + "\n```")
        return None
    res = r['r']
    s = res.snapshot
    w(f"\n_snapshot_: {snap_line(s)}")
    w(f"_在场_: {present_str(s)}")
    for ev in res.events:
        if isinstance(ev, P.NpcSpoke):
            w(f"\n**{ev.name}**: {ev.line}")
        elif isinstance(ev, P.Narration) and ev.text.strip():
            w(f"\n_叙述_: {ev.text.strip()}")
        elif isinstance(ev, P.Notice) and ev.text.strip():
            w(f"\n_提示_: {ev.text.strip()}")
        elif isinstance(ev, P.NpcMoved):
            w(f"\n_移动_: {ev.name or ev.npc_id}  {ev.from_loc} -> {ev.to_loc}")
        elif isinstance(ev, P.ClarificationNeeded):
            w(f"\n_澄清_: {ev.question} opts={getattr(ev,'options',None)}")
        elif isinstance(ev, P.RelationshipShifted):
            d = ev.descriptor; lbl = getattr(d, 'label', d)
            w(f"\n_关系移动_: {ev.name} {lbl} (Δ{ev.delta:+.3f})")
    if res.text and res.text.strip():
        w(f"\n_引擎返回_: {res.text.strip()}")
    # drain captured appraisal lines for THIS tick
    if cap.buf:
        w(f"\n**[APPRAISAL Δ→]**")
        for ln in cap.buf:
            w(f"  - `{ln}`")
        cap.buf.clear()
    else:
        w(f"\n**[APPRAISAL Δ→]** (无 appraisal 日志行)")
    w(f"\n_关系_: {rel_str(s)}")
    return s

def main():
    es = EngineSession(make_session())
    s0 = es.snapshot()
    w(f"# Skyglass 第六跑 transcript — 被施压当事人真诚松动 probe")
    w(f"\n包: {PACK}")
    w(f"world_premise 注入: npc_daily_rhythm=True (内存副本; 未动 world_state_vars)")
    w(f"\n**开局 snapshot**: {snap_line(s0)}")
    w(f"**开局在场**: {present_str(s0)}")
    cap.buf.clear()
    tf.flush()

    tick_no = 0; pos = 0; idle = 0
    while True:
        lines = QUEUE.read_text(encoding="utf-8").splitlines()
        if pos < len(lines):
            idle = 0
            raw = lines[pos]; pos += 1
            if raw.strip() == "@@QUIT":
                w("\n\n=== QUIT ==="); break
            if not raw.strip():
                continue
            # optional "kind|||text" annotation
            if "|||" in raw:
                kind, action = raw.split("|||", 1)
            else:
                kind, action = "?", raw
            tick_no += 1
            cap.buf.clear()
            t0 = time.time()
            r = do_tick(es, action)
            dt = time.time() - t0
            emit(tick_no, action.strip(), kind.strip(), r)
            w(f"\n_(tick {dt:.1f}s)_")
            tf.flush()
        else:
            idle += 1
            time.sleep(1.5)
            if idle > 400:
                w("\n\n=== IDLE TIMEOUT ==="); break
    tf.close()

if __name__ == "__main__":
    main()
