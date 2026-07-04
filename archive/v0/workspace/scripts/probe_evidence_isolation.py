"""Clean isolation probe — emberfall_kiln_assize evidence vars.

Goal: nail whether the author-declared zero-prerequisite evidence vars
(charcoal_ledger_obtained / digger_witness_recorded) actually FLIP True
under clean operation, with driver pollution removed:
  - SINGLE-adjacency moves only (one connection per step), /look to confirm
  - never mention an absent NPC when speaking to a present one

Geography (start assize_hall):
  Lou @ tally_house  : assize_hall→guild_loft(adj)→tally_house
  Miao @ clay_pits   : assize_hall→dragon_kiln(near)→clay_pits
  Kuo @ guild_loft(adj)

Short run, flush every tick, watchdog ~90s.
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
LOGF = OUTDIR / "probe.log"
TRANS = OUTDIR / "probe_transcript.md"

KUO = "npc.warden_kuo"
LOU = "npc.factor_lou"
MIAO = "npc.digger_miao"
PLAYER = "player_001"
WATCH = [KUO, LOU, MIAO]
VARS = ["charcoal_ledger_obtained", "digger_witness_recorded",
        "kiln_fault_disclosed", "digger_testimony_given"]

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
FALLBACK_COUNT = {"n": 0}
def make_session():
    g = GameSession(PACK, save_dir="_probe_saves", llm_backend="minimax")
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
    return "\n".join(f"    {v} = {g.get_world_var(v)}" for v in VARS)

def rel_dump():
    g = GSESS['g']
    out = []
    for nid in WATCH:
        r = g.get_relationship(nid, PLAYER)
        if r is None:
            out.append(f"    {nid}: (未评估)"); continue
        d = getattr(r, "dimensions", None) or getattr(r, "scores", None) or r
        try:
            out.append(f"    {nid}: susp={d.get('suspicion')} trust={d.get('trust')} "
                       f"resp={d.get('respect')} fam={d.get('familiarity')}")
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

MARK_KEYS = ("world-change", "appraises player", "escort", "MOVED", "⟳MOVED",
             "FLIP", "⟳FLIP", "sufficiency backstop", "new_prerequisite",
             "dynamic prerequisite", "process", "ledger", "partial", "FALLBACK",
             "fallback", "insufficient", "充分", "coherence", "NOT registered")

# Single-hop sequence. Each move is ONE adjacency; /look confirms arrival.
SEQUENCE = [
    ("/look", "orient"),

    # ===== ① 物证 isolation: assize_hall → guild_loft → tally_house, 找娄 =====
    ("我穿过侧廊登上窑监阁。", "移动 assize_hall→guild_loft"),
    ("/look", "confirm guild_loft"),
    ("我过账桥前往商会账房。", "移动 guild_loft→tally_house"),
    ("/look", "confirm tally_house"),
    # 先给台阶
    ("对账房娄说：娄账房，我不写你的名字，出了事我一人担着，不会让账房惹祸上身。",
     "①给娄台阶"),
    # 祈使 + request_keywords「把账册交给勘瓷」「官炭私运账」
    ("对账房娄说：娄账房，请你把那本官炭私运账交给勘瓷。把账册交给勘瓷，我这就接过来。",
     "①★要炭账(charcoal_ledger_obtained)"),

    # ===== ① 人证 isolation: tally_house → clay_pits → 找苗 =====
    # tally_house→clay_pits(near) 是单跳相邻
    ("我沿辙印走向赭泥掘场。", "移动 tally_house→clay_pits"),
    ("/look", "confirm clay_pits"),
    # 先安抚/保障
    ("对掘泥女工苗说：苗，别怕，有我在，你只要到场我就护着你，不会让窑卫动你。",
     "①安抚苗"),
    # 祈使 + keywords「记录苗的证词」「说出骡车出城」
    ("对掘泥女工苗说：我请你说出那夜骡车出城的经过，我记录苗的证词、留下你的目击口供。",
     "①★录苗证词(digger_witness_recorded)"),

    ("@@FLUSH", ""),  # checkpoint: write report after core ① before risking ②③
]

# ===== ② 杠杆 A vs B：clay_pits → dragon_kiln → guild_loft，压窑监阔 =====
PHASE2 = [
    ("我沿料道上到龙脊窑膛。", "移动 clay_pits→dragon_kiln"),
    ("/look", "confirm dragon_kiln"),
    ("我由监道上到窑监阁。", "移动 dragon_kiln→guild_loft"),
    ("/look", "confirm guild_loft"),
    # A: 无证据纯软话/质问（基线，句中不提别人）
    ("对窑监阔说：阔监，跟我说句实话，这窑变到底是不是掘泥户的赭泥之过？",
     "A·无证据·质问阔(基线)"),
    # B: 明说手上已有炭账/证词 + 体面台阶
    ("对窑监阔说：阔监，我手上已有那本炭账、也录得了目击证词，窑拱缺骨之事已能核对。"
     "我请你当众承认私运龙骨土、查实窑变真因——你肯认了，我替你留个体面台阶、不深究你个人。",
     "B·有证据·压阔(kiln_fault_disclosed)"),
]

# ===== ③ 护送 isolation（可选）: guild_loft → ... → clay_pits 对苗祈使护送 =====
PHASE3 = [
    ("我由监道下到龙脊窑膛。", "移动 guild_loft→dragon_kiln"),
    ("/look", "confirm dragon_kiln"),
    ("我沿料道下到赭泥掘场。", "移动 dragon_kiln→clay_pits"),
    ("/look", "confirm clay_pits"),
    ("对掘泥女工苗说：苗，现在跟我去山祠后坛当面陈情备案，我护着你，我们这就走。",
     "③护送苗(digger_testimony_given ⟳MOVED)"),
]

def run_phase(es, seq, tick0):
    tick = tick0
    for action, tag in seq:
        if action == "@@FLUSH":
            w("\n=== CHECKPOINT (核心①跑完) ===")
            continue
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
        for nid in (KUO,):
            lev = LEV.get(nid)
            if lev is None: continue
            if lev:
                w(f"\n_{nid}·筹码块[非空]_:")
                for f in lev: w(f"    + {f}")
            else:
                w(f"\n_{nid}·筹码块[空]_")
        marks = [ln for ln in ring.buf if any(k in ln for k in MARK_KEYS)]
        for ln in marks:
            if "FALLBACK" in ln or "fallback" in ln:
                FALLBACK_COUNT["n"] += 1
        if marks:
            w("\n_关键日志_:")
            for ln in marks: w(f"    | {ln}")
        w(f"\n_(tick {dt:.1f}s)_")
        tf.flush()
    return tick

def main():
    es = EngineSession(make_session())
    s0 = es.snapshot()
    w("# 取证 isolation probe — emberfall_kiln_assize（真机 MiniMax）\n")
    w(f"包: {PACK}")
    w(f"开局在场: {present_str(s0)}")
    w(f"\n开局世界状态:\n{world_dump()}")
    tf.flush()

    tick = run_phase(es, SEQUENCE, 0)
    tick = run_phase(es, PHASE2, tick)
    tick = run_phase(es, PHASE3, tick)

    w(f"\n\n## 终局世界状态\n{world_dump()}")
    w(f"\n## 终局关系\n{rel_dump()}")
    w(f"\n## FALLBACK 计数: {FALLBACK_COUNT['n']}")
    w(f"\n## 总拍数: {tick}")
    tf.close()

if __name__ == "__main__":
    main()
