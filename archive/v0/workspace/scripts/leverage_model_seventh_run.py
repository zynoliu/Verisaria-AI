"""Seventh run — leverage model: backed words move a wary principal.

Two-segment A/B contrast on ONE principal (梅档案官 / npc.archivist_mae, who
holds archive_authority → controls archive_injunction_filed & witness_record_secured).

  A 纯软话（无筹码）: at archive_stack, sincere / give-an-out talk to Mae for
      3 rounds while the ledger is empty → leverage block MUST be empty.
  B 有筹码: first land ONE keyword-hitting imperative on Mae to write a ledger
      fact onto a var she controls (archive_injunction_filed) → leverage non-empty;
      THEN repeat the same sincere / concession talk → does suspicion fall / trust rise?

Per tick: dump leverage block (monkeypatched, = exactly what appraiser receives),
relationship snapshot for Mae, the appraisal log line (Δ → ), and Channel-C markers.
Flush per tick. ~12-14 ticks.
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
LOGF = OUTDIR / "run.log"
TRANS = OUTDIR / "transcript.md"
MAE = "npc.archivist_mae"

fh = logging.FileHandler(LOGF, mode="w", encoding="utf-8")
fh.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s"))
for nm in ("verisaria", "verisaria.channel_c", "verisaria.relationship"):
    lg = logging.getLogger(nm); lg.setLevel(logging.INFO); lg.addHandler(fh)

class Ring(logging.Handler):
    def __init__(self): super().__init__(); self.buf = []
    def emit(self, rec): self.buf.append(self.format(rec))
ring = Ring(); ring.setFormatter(logging.Formatter("%(name)s %(levelname)s %(message)s"))
logging.getLogger("verisaria.channel_c").addHandler(ring)
logging.getLogger("verisaria").addHandler(ring)
logging.getLogger("verisaria.relationship").addHandler(ring)

tf = TRANS.open("w", buffering=1, encoding="utf-8")
def w(s=""): tf.write(s + "\n"); tf.flush()

# Capture the leverage block the appraiser actually receives for Mae.
LEV = {}  # observer_id -> last leverage list

def make_session():
    g = GameSession(PACK, save_dir="_seventh_saves", llm_backend="minimax")
    g._progress_sink = lambda m: None
    orig = g._player_leverage_over
    def wrapped(observer_id):
        facts = orig(observer_id)
        LEV[observer_id] = list(facts)
        return facts
    g._player_leverage_over = wrapped
    return g

def present_str(s):
    return ", ".join(f"{e.name}({e.id})" for e in s.present) or "(无人)"

def rel_snap(es):
    sess = es._session if hasattr(es, "_session") else None
    return None

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

# (action, phrasing-type tag, segment)
SEQ = [
    ("我去低温档案署找梅档案官。", "移动", "—"),
    # ===== A 纯软话（无筹码）=====
    ("对梅档案官说：梅档案官，我不是来找你麻烦的，我知道你也想保住这些证词，我们其实站在一边。", "真诚/示善意", "A"),
    ("对梅档案官说：梅档案官，你放心，我不会把这事算到你头上，你的署里不会因为我受牵连。", "给台阶/卸威胁", "A"),
    ("对梅档案官说：梅档案官，我向你保证，我只想要真相被保住，不会动你一根头发，你可以信我。", "真诚/给台阶", "A"),
    # ===== 建立筹码：祈使+命中 archive_injunction_filed 关键词 =====
    ("对梅档案官说：梅档案官，我请你立刻援引旧章程、提交禁令，申请一场可撤回听证，暂停今晚的清洗流程。", "祈使·建筹码(取证)", "建筹码"),
    # ===== B 有筹码（同样的软话）=====
    ("对梅档案官说：梅档案官，我不是来找你麻烦的，我知道你也想保住这些证词，我们其实站在一边。", "真诚/示善意(同A)", "B"),
    ("对梅档案官说：梅档案官，你放心，我不会把这事算到你头上，你的署里不会因为我受牵连。", "给台阶/卸威胁(同A)", "B"),
    ("对梅档案官说：梅档案官，我向你保证，我只想要真相被保住，不会动你一根头发，你可以信我。", "真诚/给台阶(同A)", "B"),
    ("@@QUIT", "", ""),
]

def main():
    es = EngineSession(make_session())
    s0 = es.snapshot()
    w("# 第七跑 · 杠杆模型 A/B 对照 transcript\n")
    w(f"包: {PACK}")
    w("注入: 无（默认 world_premise，未动 world_state_vars）")
    w(f"对照 NPC: 梅档案官 ({MAE}) — authority=archive_authority，掌管 "
      "archive_injunction_filed / witness_record_secured")
    w(f"\n开局在场: {present_str(s0)}")
    w("\n说明：每拍打印 appraiser 实收的「筹码块」(空=无筹码 / 非空=有筹码) + Mae 关系 Δ→ 行。")
    tf.flush()

    tick = 0
    for action, tag, seg in SEQ:
        if action == "@@QUIT":
            w("\n=== QUIT ==="); break
        tick += 1
        ring.buf.clear()
        LEV.clear()
        t0 = time.time()
        r = do_tick(es, action)
        dt = time.time() - t0
        w("\n" + "=" * 80)
        w(f"## 拍 {tick} — [段{seg}] [{tag}]")
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
        # leverage block the appraiser saw for Mae
        mae_lev = LEV.get(MAE)
        if mae_lev is None:
            w("\n_梅·筹码块_: (本拍未对梅触发 appraisal)")
        elif mae_lev:
            w(f"\n_梅·筹码块 [非空·有筹码]_:")
            for f in mae_lev: w(f"    + {f}")
        else:
            w("\n_梅·筹码块 [空·无筹码]_: （空口而谈）")
        # appraisal Δ lines + channel-c markers
        appr = [ln for ln in ring.buf if "appraises player" in ln]
        cc = [ln for ln in ring.buf if ("world-change" in ln or "什么也没发生" in ln
              or "new_prerequisite" in ln or "ledger" in ln)]
        w("\n_appraisal Δ→_:")
        if appr:
            for ln in appr: w(f"    | {ln}")
        else:
            w("    | (本拍无 appraisal 行)")
        if cc:
            w("\n_channel-c 标记_:")
            for ln in cc: w(f"    | {ln}")
        w(f"\n_(tick {dt:.1f}s)_")
        tf.flush()
    tf.close()

if __name__ == "__main__":
    main()
