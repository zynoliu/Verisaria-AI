"""Interactive playability-audit driver (real MiniMax).

Runs a persistent GameSession via the clean EngineSession interface. Reads
player actions one-per-line from a QUEUE file (tailing it); for each new line it
executes one tick and appends a rich record (player input + NPC dialogue raw +
narration + snapshot time/weather/clock + present NPCs + relationships + world
vars + NpcMoved) to a TRANSCRIPT file. A control line "@@QUIT" stops it.

The driving agent appends actions to the queue and reads the transcript to
decide the next move — i.e. plays like a curious, adversarial human, not a
pre-written script. No engine/pack edits; live-world switches are injected on an
in-memory copy of world_premise only.

Env: PYTHONPATH=src, .env sourced (MINIMAX_API_KEY). Per-tick watchdog ~90s.
"""
from __future__ import annotations
import os, sys, time, logging, json, threading
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

PACK = os.environ.get("PA_PACK", "fixtures/content_packs/tidebreak_quarantine_harbor.json")
OUTDIR = ROOT / "reports" / "playability_audit"
OUTDIR.mkdir(parents=True, exist_ok=True)
QUEUE = OUTDIR / os.environ.get("PA_QUEUE", "queue.txt")
TRANS = OUTDIR / os.environ.get("PA_TRANS", "transcript.md")
LOGF = OUTDIR / os.environ.get("PA_LOG", "run.log")

h = logging.FileHandler(LOGF, mode="w", encoding="utf-8")
h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
lg = logging.getLogger("verisaria"); lg.setLevel(logging.INFO); lg.addHandler(h)

QUEUE.write_text("", encoding="utf-8")
tf = TRANS.open("w", buffering=1, encoding="utf-8")
def w(s=""): tf.write(s + "\n"); tf.flush()

# --- live-world switches: inject onto in-memory premise copy ONLY ---
def make_session():
    g = GameSession(PACK, save_dir="_pa_saves", llm_backend="minimax")
    g._progress_sink = lambda m: None
    prem = getattr(g.pack, "world_premise", None)
    if prem is not None:
        # humid coastal noir -> ocean climate, dusk opening, living NPC rhythm
        try:
            prem.climate = "海洋"
            prem.opening_time = "黄昏"
            prem.npc_daily_rhythm = True
            # re-apply opening clock/weather now that premise changed
            from verisaria.engine import worldclock, weather as wmod
            g.world_state.clock_minutes = worldclock.parse_opening_time("黄昏")
            g.world_state.weather = wmod.initial_weather("海洋", None)
            g.world_state.weather_hour = g.world_state.clock_minutes // 60
            g._climate = "海洋"
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
        d = "/".join(f"{x.label}:{x.value:.2f}" if hasattr(x,'value') else str(x) for x in r.descriptors)
        out.append(f"{r.name}[{d}]")
    return "; ".join(out)

def wvars_str(s):
    return ", ".join(f"{v.label}={v.value}" + (f"(pend{v.pending_in})" if v.pending_in else "") + ("*dyn" if v.dynamic else "") for v in s.world_vars)

def stances_str(s):
    return ", ".join(s.agenda.confirmed_stances) or "(无)"

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

def emit(tick_no, action, r):
    w("\n" + "="*80)
    w(f"## 拍 {tick_no} — 玩家输入")
    w(f"> {action}")
    if r.get('timeout'):
        w("\n**[WATCHDOG TIMEOUT >90s — tick skipped in report]**")
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
        elif isinstance(ev, P.PressureEvent):
            w(f"\n_压力事件_: [{ev.event_type}] {ev.summary}")
        elif isinstance(ev, P.RelationshipShifted):
            d = ev.descriptor
            lbl = getattr(d, 'label', d)
            w(f"\n_关系移动_: {ev.name} {lbl} (Δ{ev.delta:+.2f})")
        elif isinstance(ev, P.WorldVarChanged):
            w(f"\n_WORLD变化_: {ev.label} = {ev.value}")
        elif isinstance(ev, P.StanceConfirmed):
            w(f"\n_立场确认_: {ev.label} ({ev.topic_id})")
    if res.text and res.text.strip():
        w(f"\n_引擎返回_: {res.text.strip()}")
    w(f"\n_关系_: {rel_str(s)}")
    w(f"_立场_: {stances_str(s)}")
    w(f"_world_: {wvars_str(s)}")
    return s

def main():
    es = EngineSession(make_session())
    s0 = es.snapshot()
    w(f"# Tidebreak 可玩性盘点 transcript")
    w(f"\n包: {PACK}")
    w(f"world_premise 注入: climate=海洋 opening_time=黄昏 npc_daily_rhythm=True (内存副本)")
    prem = es.game.pack.world_premise
    w(f"\n**central_tension**: {prem.central_tension}")
    w(f"\n**开局 snapshot**: {snap_line(s0)}")
    w(f"**开局在场**: {present_str(s0)}")
    w(f"**开局位置描述**: {s0.location.description}")
    w(f"**drives**: {s0.agenda.drives}")
    w(f"**world vars**: {wvars_str(s0)}")
    # entity map
    st = es.game.world.state
    w(f"\n**全实体位置**:")
    for eid, e in st.entities.items():
        if eid != es.game.player_id:
            w(f"  - {e.name} ({eid}) @ {e.location_id}")
    tf.flush()

    tick_no = 0
    pos = 0
    idle = 0
    while True:
        lines = QUEUE.read_text(encoding="utf-8").splitlines()
        if pos < len(lines):
            idle = 0
            action = lines[pos]; pos += 1
            if action.strip() == "@@QUIT":
                w("\n\n=== QUIT ===")
                break
            if not action.strip():
                continue
            tick_no += 1
            t0 = time.time()
            r = do_tick(es, action)
            dt = time.time() - t0
            emit(tick_no, action, r)
            w(f"\n_(tick {dt:.1f}s)_")
            tf.flush()
        else:
            idle += 1
            time.sleep(1.5)
            if idle > 600:  # 15 min no input -> stop
                w("\n\n=== IDLE TIMEOUT ===")
                break
    tf.close()

if __name__ == "__main__":
    main()
