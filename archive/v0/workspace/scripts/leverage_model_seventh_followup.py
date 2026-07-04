"""Seventh run · follow-up — get the B-segment appraisal Δ that the main run lost.

Finding from the main run: once a var Mae controls carries a ledger fact, the
Channel-C router's `fallback` branch (session.py:1753) routes ANY non-question
speech to Mae into world-change — so the relationship APPRAISER never fires for
B-segment soft-talk, and we get no Δ to compare against A.

Fix for the methodology: phrase the sincere/concession line as a QUESTION. The
router's question gate (session.py:1761-1762) suppresses the fuzzy/fallback
routes, so a sincere question FALLS THROUGH to ordinary speech → the appraiser
fires. Leverage is per-NPC, so it is present regardless of phrasing.

So we compare, with the SAME question-phrased sincere line:
  A' (no leverage): sincere question to Mae BEFORE any ledger fact  → appraiser, leverage empty
  build leverage:   one keyword imperative (writes ledger on archive_injunction_filed)
  B' (leverage):    SAME sincere question to Mae AFTER the ledger fact → appraiser, leverage non-empty
Δ(A') vs Δ(B') with identical wording = the clean leverage-model judgment.
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
OUTDIR = ROOT / "reports" / "playability_audit_seventh_run"
OUTDIR.mkdir(parents=True, exist_ok=True)
LOGF = OUTDIR / "run_followup.log"
TRANS = OUTDIR / "transcript_followup.md"
MAE = "npc.archivist_mae"

fh = logging.FileHandler(LOGF, mode="w", encoding="utf-8")
fh.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s"))
for nm in ("verisaria", "verisaria.channel_c", "verisaria.relationship"):
    lg = logging.getLogger(nm); lg.setLevel(logging.INFO); lg.addHandler(fh)

class Ring(logging.Handler):
    def __init__(self): super().__init__(); self.buf = []
    def emit(self, rec): self.buf.append(self.format(rec))
ring = Ring(); ring.setFormatter(logging.Formatter("%(name)s %(levelname)s %(message)s"))
for nm in ("verisaria.channel_c", "verisaria", "verisaria.relationship"):
    logging.getLogger(nm).addHandler(ring)

tf = TRANS.open("w", buffering=1, encoding="utf-8")
def w(s=""): tf.write(s + "\n"); tf.flush()

LEV = {}
def make_session():
    g = GameSession(PACK, save_dir="_seventh_fu_saves", llm_backend="minimax")
    g._progress_sink = lambda m: None
    orig = g._player_leverage_over
    def wrapped(observer_id):
        facts = orig(observer_id); LEV[observer_id] = list(facts); return facts
    g._player_leverage_over = wrapped
    return g

def present_str(s):
    return ", ".join(f"{e.name}({e.id})" for e in s.present) or "(无人)"

RESULT = {}
def do_tick(es, text):
    RESULT.clear()
    def runner():
        try: RESULT['r'] = es.submit(P.SubmitInput(text=text))
        except Exception:
            import traceback; RESULT['err'] = traceback.format_exc()
    th = threading.Thread(target=runner, daemon=True); th.start()
    th.join(timeout=90)
    if th.is_alive(): RESULT['timeout'] = True
    return RESULT

# Same sincere/concession line, phrased as a QUESTION so it falls through to the
# appraiser instead of routing to Channel-C.
SINCERE_Q = ("对梅档案官说：梅档案官，我只想保住真相、不会让你受牵连，"
             "你能不能信我一回、把我当成站在同一边的人？")

SEQ = [
    ("我去低温档案署找梅档案官。", "移动", "—"),
    # A' — sincere question, NO leverage yet (ledger empty)
    (SINCERE_Q, "真诚·问句(同句)", "A'(无筹码)"),
    (SINCERE_Q, "真诚·问句(同句)", "A'(无筹码)"),
    # build leverage: keyword imperative → ledger fact on archive_injunction_filed
    ("对梅档案官说：梅档案官，我请你立刻援引旧章程、提交禁令，申请一场可撤回听证，暂停今晚的清洗流程。",
     "祈使·建筹码(取证)", "建筹码"),
    # B' — SAME sincere question, leverage now present
    (SINCERE_Q, "真诚·问句(同句)", "B'(有筹码)"),
    (SINCERE_Q, "真诚·问句(同句)", "B'(有筹码)"),
    ("@@QUIT", "", ""),
]

def main():
    es = EngineSession(make_session())
    s0 = es.snapshot()
    w("# 第七跑 · 跟进 — A'/B' 同句(问句)对照 transcript\n")
    w(f"包: {PACK}（无注入）")
    w(f"对照 NPC: 梅档案官 ({MAE}), archive_authority")
    w(f"\n同一句(问句式真诚/给台阶): {SINCERE_Q}")
    w("\n说明：问句不进 Channel-C → appraiser 必触发；A' 时 ledger 空(筹码块空)，B' 时 ledger 有事实(筹码块非空)。")
    w(f"\n开局在场: {present_str(s0)}")
    tf.flush()

    tick = 0
    for action, tag, seg in SEQ:
        if action == "@@QUIT":
            w("\n=== QUIT ==="); break
        tick += 1
        ring.buf.clear(); LEV.clear()
        t0 = time.time(); r = do_tick(es, action); dt = time.time() - t0
        w("\n" + "=" * 80)
        w(f"## 拍 {tick} — [段{seg}] [{tag}]")
        w(f"> {action}")
        if r.get('timeout'): w("\n**[WATCHDOG TIMEOUT >90s]**"); tf.flush(); continue
        if r.get('err'): w("\n**[EXCEPTION]**\n```\n"+r['err']+"\n```"); tf.flush(); continue
        res = r['r']; s = res.snapshot
        w(f"\n_在场_: {present_str(s)}")
        for ev in res.events:
            if isinstance(ev, P.NpcSpoke): w(f"\n**{ev.name}**: {ev.line}")
            elif isinstance(ev, P.WorldVarChanged): w(f"\n_WORLD变化_: {ev.label} = {ev.value}")
        if res.text and res.text.strip(): w(f"\n_引擎返回_: {res.text.strip()}")
        mae_lev = LEV.get(MAE)
        if mae_lev is None: w("\n_梅·筹码块_: (本拍未对梅触发 appraisal)")
        elif mae_lev:
            w("\n_梅·筹码块 [非空·有筹码]_:")
            for f in mae_lev: w(f"    + {f}")
        else: w("\n_梅·筹码块 [空·无筹码]_: （空口而谈）")
        appr = [ln for ln in ring.buf if "appraises player" in ln]
        cc = [ln for ln in ring.buf if ("world-change" in ln or "什么也没发生" in ln or "ledger" in ln)]
        w("\n_appraisal Δ→_:")
        if appr:
            for ln in appr: w(f"    | {ln}")
        else: w("    | (本拍无 appraisal 行)")
        if cc:
            w("\n_channel-c 标记_:")
            for ln in cc: w(f"    | {ln}")
        w(f"\n_(tick {dt:.1f}s)_")
        tf.flush()
    tf.close()

if __name__ == "__main__":
    main()
