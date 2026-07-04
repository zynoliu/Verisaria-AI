"""Anti-cheat clean session — emberfall_kiln_assize.

Fresh session, no evidence / no escort. Player walks straight to 征瓷使严 and
bluffs: claims 真因已明 + 证人已陈情. branding_stayed must NOT flip (its only
prereq = kiln_fault_disclosed==true && digger_testimony_given==true, both False).
Capture the failure reason.
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
LOGF = OUTDIR / "closeloop_anticheat.log"
TRANS = OUTDIR / "closeloop_anticheat_transcript.md"
VARS = ["kiln_fault_disclosed", "digger_testimony_given", "branding_stayed"]

fh = logging.FileHandler(LOGF, mode="w", encoding="utf-8")
fh.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s"))
for nm in ("verisaria", "verisaria.channel_c", "verisaria.relationship"):
    lg = logging.getLogger(nm); lg.setLevel(logging.INFO); lg.addHandler(fh)
class Ring(logging.Handler):
    def __init__(self): super().__init__(); self.buf = []
    def emit(self, rec): self.buf.append(self.format(rec))
ring = Ring(); ring.setFormatter(logging.Formatter("%(name)s %(message)s"))
for nm in ("verisaria.channel_c",): logging.getLogger(nm).addHandler(ring)

tf = TRANS.open("w", buffering=1, encoding="utf-8")
def w(s=""): tf.write(s + "\n"); tf.flush()

G = {}
def make_session():
    g = GameSession(PACK, save_dir="_anticheat_saves", llm_backend="minimax")
    g._progress_sink = lambda m: None
    G['g'] = g
    return g
def wd():
    return "\n".join(f"    {v} = {G['g'].get_world_var(v)}" for v in VARS)

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
    "对征瓷使严说：使君，窑变真因已经查实清楚了——是窑监私运龙骨土致窑拱缺骨而裂，掘泥户的女工证人也已经当面陈情备案了。我请你停止行烙、不要封掘场，改判缓赔议偿。",
    "对征瓷使严说：使君，我以勘瓷之名担保，真因已明、证人已陈情，事情就是这样，请你立刻叫停烙刑、免去充债。",
    "@@QUIT",
]

def main():
    es = EngineSession(make_session())
    w("# 反作弊 clean session transcript — emberfall_kiln_assize\n")
    w(f"包: {PACK}\n伪造: 无取证/无护送，直接对严谎称真因已明、证人已陈情。")
    w(f"\n开局世界状态:\n{wd()}")
    tick = 0
    for action in SEQ:
        if action == "@@QUIT": break
        tick += 1; ring.buf.clear()
        t0 = time.time(); r = do_tick(es, action); dt = time.time() - t0
        w("\n" + "=" * 70); w(f"## 拍 {tick}\n> {action}")
        if r.get('timeout'): w("\n[TIMEOUT]"); continue
        if r.get('err'): w("\n[ERR]\n" + r['err']); continue
        res = r['r']
        for ev in res.events:
            if isinstance(ev, P.NpcSpoke): w(f"\n**{ev.name}**: {ev.line}")
        if res.text and res.text.strip(): w(f"\n_引擎返回_: {res.text.strip()}")
        w(f"\n_世界状态_:\n{wd()}")
        marks = [ln for ln in ring.buf if ("world-change" in ln or "→" in ln)]
        if marks:
            w("\n_channel-c_:")
            for ln in marks: w(f"    | {ln}")
        w(f"\n_(tick {dt:.1f}s)_")
    w(f"\n\n## 终局\n{wd()}")
    tf.close()

if __name__ == "__main__":
    main()
