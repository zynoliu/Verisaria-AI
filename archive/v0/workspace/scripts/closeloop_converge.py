"""Convergence retry — try hardest to flip at least ONE var to success and,
if possible, break the prereq cycle the main run hit. Single-hop moves only.

Strategy: go straight to clay_pits (assize_hall -> dragon_kiln -> clay_pits),
hit 苗 with the EXACT injected-prereq keywords (我担保/我陪你走/不是窑卫的人/
当面作证/陪护人) to satisfy escort_trust_witnessed_by_miao, then push escort +
witness. Watch for any → success and ⟳MOVED.
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
LOGF = OUTDIR / "closeloop_converge.log"
TRANS = OUTDIR / "closeloop_converge_transcript.md"
VARS = ["digger_witness_recorded", "digger_testimony_given",
        "kiln_fault_disclosed", "charcoal_ledger_obtained",
        "shrine_appeal_consecrated", "branding_stayed"]

fh = logging.FileHandler(LOGF, mode="w", encoding="utf-8")
fh.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s"))
for nm in ("verisaria", "verisaria.channel_c"):
    lg = logging.getLogger(nm); lg.setLevel(logging.INFO); lg.addHandler(fh)
class Ring(logging.Handler):
    def __init__(self): super().__init__(); self.buf = []
    def emit(self, rec): self.buf.append(self.format(rec))
ring = Ring(); ring.setFormatter(logging.Formatter("%(name)s %(message)s"))
logging.getLogger("verisaria.channel_c").addHandler(ring)
logging.getLogger("verisaria").addHandler(ring)

tf = TRANS.open("w", buffering=1, encoding="utf-8")
def w(s=""): tf.write(s + "\n"); tf.flush()
G = {}
def make_session():
    g = GameSession(PACK, save_dir="_converge_saves", llm_backend="minimax")
    g._progress_sink = lambda m: None
    G['g'] = g; return g
def wd(): return "\n".join(f"    {v} = {G['g'].get_world_var(v)}" for v in VARS)

RESULT = {}
def do_tick(es, text):
    RESULT.clear()
    def runner():
        try: RESULT['r'] = es.submit(P.SubmitInput(text=text))
        except Exception:
            import traceback; RESULT['err'] = traceback.format_exc()
    th = threading.Thread(target=runner, daemon=True); th.start(); th.join(timeout=90)
    if th.is_alive(): RESULT['timeout'] = True
    return RESULT

SEQ = [
    "我走进龙脊窑膛。",
    "我下到赭泥掘场。",
    # hit injected escort_trust_witnessed_by_miao keywords head-on:
    "对掘泥女工苗说：苗，我当面跟你担保——我不是窑卫的人、不是商会的爪牙，我陪你走、我替你当面作证、做你的陪护人。你信我，我现在就护你出去。",
    # then escort imperative:
    "对掘泥女工苗说：苗，跟我走，现在就跟我经旧矿道去山祠后坛当面陈情备案，我护着你。",
    # also try to record witness on the way:
    "对掘泥女工苗说：苗，路上你把那夜骡车出城、龙骨土被运走的经过说出来，我替你记录证词、留一份目击口供。",
    "@@QUIT",
]
MK = ("world-change","→","escort","MOVED","⟳","success","prerequisite","backstop")
def main():
    es = EngineSession(make_session())
    w("# 收敛重试 transcript — emberfall_kiln_assize\n")
    w(f"包: {PACK}\n目标: 单跳移动+直击注入前置关键词，看能否把任一 var 推到 success / ⟳MOVED。")
    w(f"\n开局世界状态:\n{wd()}")
    tick = 0
    for action in SEQ:
        if action == "@@QUIT": break
        tick += 1; ring.buf.clear()
        t0 = time.time(); r = do_tick(es, action); dt = time.time()-t0
        w("\n"+"="*70); w(f"## 拍 {tick}\n> {action}")
        if r.get('timeout'): w("\n[TIMEOUT]"); continue
        if r.get('err'): w("\n[ERR]\n"+r['err']); continue
        res = r['r']
        for ev in res.events:
            if isinstance(ev, P.NpcSpoke): w(f"\n**{ev.name}**: {ev.line}")
            elif isinstance(ev, P.WorldVarChanged): w(f"\n_WORLD变化_: {ev.label} = {ev.value}")
        if res.text and res.text.strip(): w(f"\n_引擎返回_: {res.text.strip()}")
        w(f"\n_世界状态_:\n{wd()}")
        marks = [ln for ln in ring.buf if any(k in ln for k in MK)]
        if marks:
            w("\n_关键日志_:")
            for ln in marks: w(f"    | {ln}")
        w(f"\n_(tick {dt:.1f}s)_")
    w(f"\n\n## 终局\n{wd()}")
    tf.close()
if __name__ == "__main__":
    main()
