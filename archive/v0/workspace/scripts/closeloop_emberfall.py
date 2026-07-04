"""Closeloop run — emberfall_kiln_assize grand-integration pack, main line.

Real MiniMax, no engine/pack edits. Segmented short run (~18-22 ticks),
flush transcript + world snapshot every tick.

Main line (design table ①②③⑤, ④ interleaved):
  ① evidence: charcoal ledger (factor 娄 @ tally_house) + digger witness (苗 @ clay_pits)
  ② leverage: A(no evidence) vs B(with evidence) on warden 阔 @ guild_loft → kiln_fault_disclosed
  ③ escort: 苗 from clay_pits via old_drift → digger_testimony_given (⟳MOVED)
  ④ offline process: shrine appeal @ kiln_shrine → shrine_appeal_consecrated (matures)
  ⑤ multi-step finale: assessor 严 @ assize_hall → branding_stayed ⟳FLIP

Per tick: /world dump, relationship snapshot (suspicion/trust) for key NPCs,
leverage block the appraiser received (for 阔/严), appraisal Δ lines, and
channel-c markers (world-change / appraises / escort / MOVED / FLIP /
sufficiency backstop / new_prerequisite / process / FALLBACK).
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

PACK = "fixtures/content_packs/emberfall_kiln_assize.json"
OUTDIR = ROOT / "reports" / "grand_integration_pack"
OUTDIR.mkdir(parents=True, exist_ok=True)
LOGF = OUTDIR / "closeloop.log"
TRANS = OUTDIR / "closeloop_transcript.md"

KUO = "npc.warden_kuo"      # ② leverage target
YAN = "npc.assessor_yan"    # ⑤ finale authority
MIAO = "npc.digger_miao"
PLAYER = "player_001"
WATCH = [KUO, YAN, MIAO, "npc.factor_lou", "npc.priest_ji"]
VARS = ["charcoal_ledger_obtained", "digger_witness_recorded", "kiln_fault_disclosed",
        "digger_testimony_given", "shrine_appeal_consecrated", "branding_stayed"]

fh = logging.FileHandler(LOGF, mode="w", encoding="utf-8")
fh.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s"))
for nm in ("verisaria", "verisaria.channel_c", "verisaria.relationship"):
    lg = logging.getLogger(nm); lg.setLevel(logging.INFO); lg.addHandler(fh)

class Ring(logging.Handler):
    def __init__(self): super().__init__(); self.buf = []
    def emit(self, rec): self.buf.append(self.format(rec))
ring = Ring(); ring.setFormatter(logging.Formatter("%(name)s %(levelname)s %(message)s"))
for nm in ("verisaria", "verisaria.channel_c", "verisaria.relationship"):
    logging.getLogger(nm).addHandler(ring)

tf = TRANS.open("w", buffering=1, encoding="utf-8")
def w(s=""): tf.write(s + "\n"); tf.flush()

LEV = {}
GSESS = {}
def make_session():
    g = GameSession(PACK, save_dir="_closeloop_saves", llm_backend="minimax")
    g._progress_sink = lambda m: None
    orig = g._player_leverage_over
    def wrapped(observer_id):
        facts = orig(observer_id)
        LEV[observer_id] = list(facts)
        return facts
    g._player_leverage_over = wrapped
    GSESS['g'] = g
    return g

def present_str(s):
    return ", ".join(f"{e.name}({e.id})" for e in s.present) or "(无人)"

def world_dump():
    g = GSESS['g']
    out = []
    for v in VARS:
        out.append(f"    {v} = {g.get_world_var(v)}")
    return "\n".join(out)

def rel_dump():
    g = GSESS['g']
    out = []
    for nid in WATCH:
        r = g.get_relationship(nid, PLAYER)
        if r is None:
            out.append(f"    {nid}: (未评估)")
        else:
            d = getattr(r, "dimensions", None) or getattr(r, "scores", None) or r
            try:
                susp = d.get("suspicion"); trust = d.get("trust")
                resp = d.get("respect"); fam = d.get("familiarity")
                out.append(f"    {nid}: susp={susp} trust={trust} resp={resp} fam={fam}")
            except Exception:
                out.append(f"    {nid}: {d}")
    return "\n".join(out)

RESULT = {}
def do_tick(es, text, budget=90):
    RESULT.clear()
    def runner():
        try: RESULT['r'] = es.submit(P.SubmitInput(text=text))
        except Exception:
            import traceback; RESULT['err'] = traceback.format_exc()
    th = threading.Thread(target=runner, daemon=True); th.start()
    th.join(timeout=budget)
    if th.is_alive(): RESULT['timeout'] = True
    return RESULT

MARK_KEYS = ("world-change", "什么也没发生", "appraises player", "escort",
             "MOVED", "⟳MOVED", "FLIP", "⟳FLIP", "sufficiency backstop",
             "new_prerequisite", "process", "ledger", "partial", "FALLBACK",
             "fallback", "insufficient", "充分")

def main():
    es = EngineSession(make_session())
    s0 = es.snapshot()
    w("# 闭环段 transcript — emberfall_kiln_assize（真机 MiniMax）\n")
    w(f"包: {PACK}")
    w("注入: 无（包自带 climate=干旱 / opening_time=暮 / npc_daily_rhythm）")
    w(f"开局在场: {present_str(s0)}")
    w(f"\n开局世界状态:\n{world_dump()}")
    tf.flush()

    # action sequence: (text, segment-tag)
    SEQ = list(SEQUENCE)
    tick = 0
    for action, tag in SEQ:
        if action == "@@QUIT":
            w("\n=== QUIT ==="); break
        tick += 1
        ring.buf.clear(); LEV.clear()
        t0 = time.time()
        r = do_tick(es, action)
        dt = time.time() - t0
        w("\n" + "=" * 80)
        w(f"## 拍 {tick} — [{tag}]")
        w(f"> {action}")
        if r.get('timeout'):
            w("\n**[WATCHDOG TIMEOUT >90s — skipped]**"); tf.flush(); continue
        if r.get('err'):
            w("\n**[EXCEPTION]**\n```\n" + r['err'] + "\n```"); tf.flush(); continue
        res = r['r']; s = res.snapshot
        w(f"\n_在场_: {present_str(s)}")
        for ev in res.events:
            if isinstance(ev, P.NpcSpoke):
                w(f"\n**{ev.name}**: {ev.line}")
            elif isinstance(ev, P.WorldVarChanged):
                w(f"\n_WORLD变化(event)_: {ev.label} = {ev.value}")
            elif isinstance(ev, P.StanceConfirmed):
                w(f"\n_立场确认_: {ev.label}")
        if res.text and res.text.strip():
            w(f"\n_引擎返回_: {res.text.strip()}")
        w(f"\n_世界状态_:\n{world_dump()}")
        w(f"\n_关系(susp/trust)_:\n{rel_dump()}")
        for nid in (KUO, YAN):
            lev = LEV.get(nid)
            if lev is None:
                continue
            if lev:
                w(f"\n_{nid}·筹码块[非空]_:")
                for f in lev: w(f"    + {f}")
            else:
                w(f"\n_{nid}·筹码块[空]_")
        marks = [ln for ln in ring.buf if any(k in ln for k in MARK_KEYS)]
        if marks:
            w("\n_关键日志_:")
            for ln in marks: w(f"    | {ln}")
        w(f"\n_(tick {dt:.1f}s)_")
        tf.flush()
    w(f"\n\n## 终局世界状态\n{world_dump()}")
    w(f"\n## 终局关系\n{rel_dump()}")
    tf.close()


# ====== sequence imported from a sibling list so we can edit phases ======
from closeloop_seq import SEQUENCE  # noqa: E402

if __name__ == "__main__":
    main()
