"""Playability-audit · THIRD run · F1 convergence on the ORIGINAL fixture (real MiniMax).

Goal (one thing): replay the proven sincere endgame on the *original*
tidebreak_quarantine_harbor.json (NO authored copy, NO touching world_state_vars
labels/keywords — only world_premise switches injected) and answer whether the
F1 engine guardrails let the evidence chain close *by itself*:
  pump_failure_disclosed ⟳FLIP → tow_order_halted ⟳FLIP

The crux: F1's dedup (`_register_dynamic_prerequisite`) is deterministic, but
whether it FIRES depends on how the arbiter LLM names a near-duplicate
("公开"-class) prerequisite. So this driver hooks `_register_dynamic_prerequisite`
to record, verbatim, EVERY raw arbiter `new_prerequisite.var_id` it proposes and
what the engine did with it (REUSED into an existing var / registered NEW /
refused by cap). It also prints the full /world (every world var + value +
dynamic flag) each tick, FLIP lines, NPC dialogue, and a relationship snapshot.

Per-tick watchdog ~90s. Runs to a definitive tow_order_halted verdict (⟳FLIP or
a clear blocking reason) before stopping. Serial.

Env: PYTHONPATH=src, .env sourced (MINIMAX_API_KEY).
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

PACK = "fixtures/content_packs/tidebreak_quarantine_harbor.json"  # ORIGINAL
OUTDIR = ROOT / "reports" / "playability_audit_third_run"
TRANS = OUTDIR / "transcript.md"
LOGF = OUTDIR / "run.log"

h = logging.FileHandler(LOGF, mode="w", encoding="utf-8")
h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
root = logging.getLogger("verisaria"); root.setLevel(logging.INFO); root.addHandler(h)

tf = TRANS.open("w", buffering=1, encoding="utf-8")
def w(s=""): tf.write(s + "\n"); tf.flush()

TRACK = ["npc.teacher_mara", "npc.engineer_sen", "npc.director_lin",
         "npc.sergeant_qiao", "npc.broadcaster_orin", "npc.vendor_yu",
         "npc.child_tavi"]

LIN = "npc.director_lin"
ORIN = "npc.broadcaster_orin"
SEN = "npc.engineer_sen"
MARA = "npc.teacher_mara"

# ---- F1 INSTRUMENTATION: record every raw arbiter new_prerequisite var_id verbatim ----
PREREQ_EVENTS = []  # list of dicts: {tick, raw_var_id, raw_label, raw_keywords, raw_set_by, returned, action}
def install_prereq_hook(game):
    orig = game._register_dynamic_prerequisite
    specs = game._world_var_specs
    def wrapped(prereq, serves=None):
        raw_id = getattr(prereq, "var_id", None) if prereq is not None else None
        raw_label = getattr(prereq, "label", None) if prereq is not None else None
        raw_kw = list(getattr(prereq, "request_keywords", []) or []) if prereq is not None else None
        raw_set_by = list(getattr(prereq, "set_by", []) or []) if prereq is not None else None
        before_ids = set(specs.keys())
        returned = orig(prereq, serves=serves)
        tick = game.world.state.tick
        if prereq is None:
            return returned
        # classify what F1 did
        if returned is None:
            action = "REFUSED (dup-cap/bad-id/no-real-set_by-NPC)"
        elif returned in before_ids:
            # returned an id that already existed before this call → REUSED
            action = f"REUSED into existing var '{returned}'"
        else:
            action = f"registered NEW dynamic var '{returned}'"
        ev = {"tick": tick, "raw_var_id": raw_id, "raw_label": raw_label,
              "raw_keywords": raw_kw, "raw_set_by": raw_set_by,
              "serves": serves, "returned": returned, "action": action}
        PREREQ_EVENTS.append(ev)
        # write to transcript immediately so it's never lost
        w(f"\n  >>> [F1] arbiter new_prerequisite (RAW): var_id={raw_id!r}")
        w(f"      label={raw_label!r}")
        w(f"      keywords={raw_kw}  set_by={raw_set_by}  serves={serves!r}")
        w(f"      ENGINE ACTION: {action}")
        return returned
    game._register_dynamic_prerequisite = wrapped

def make_session():
    g = GameSession(PACK, save_dir="_pa3_saves", llm_backend="minimax")
    g._progress_sink = lambda m: None
    prem = getattr(g.pack, "world_premise", None)
    if prem is not None:
        try:
            prem.climate = "海洋"; prem.opening_time = "黄昏"; prem.npc_daily_rhythm = True
            from verisaria.engine import worldclock, weather as wmod
            g.world_state.clock_minutes = worldclock.parse_opening_time("黄昏")
            g.world_state.weather = wmod.initial_weather("海洋", None)
            g.world_state.weather_hour = g.world_state.clock_minutes // 60
            g._climate = "海洋"
        except Exception as e:
            w(f"<!-- premise inject failed: {e} -->")
    install_prereq_hook(g)
    return g

def snap_line(s):
    return f"time={s.time_of_day!r} clock={s.clock!r} weather={s.weather!r} loc={s.location.name!r}"
def present_ids(s):
    return [e.id for e in s.present]
def present_str(s):
    return ", ".join(f"{e.name}({e.id})" for e in s.present) or "(无人)"

PREV = {}
def raw_rel_block(game):
    lines = []
    for nid in TRACK:
        snap = game.relationship_store.get(nid, game.player_id)
        dims = dict(snap.dimensions) if snap else {}
        susp = dims.get("suspicion", 0.0); trust = dims.get("trust", 0.0)
        prev = PREV.get(nid, {})
        dsus = susp - prev.get("suspicion", susp); dtru = trust - prev.get("trust", trust)
        name = game.world.state.display_name(nid)
        lines.append(f"  - {name}: suspicion={susp:.3f} (Δ{dsus:+.3f}) trust={trust:.3f} (Δ{dtru:+.3f})")
        PREV[nid] = {"suspicion": susp, "trust": trust}
    return "\n".join(lines)

def world_block(s):
    """Full /world — every world var, value, dynamic flag. THE key evidence."""
    lines = []
    for v in s.world_vars:
        flag = "  *DYNAMIC*" if v.dynamic else ""
        pend = f"  (pending_in={v.pending_in})" if getattr(v, "pending_in", None) else ""
        lines.append(f"  - [{v.var_id}] {v.label} = {v.value}{flag}{pend}")
    return "\n".join(lines)

RESULT = {}
def do_tick(es, text):
    RESULT.clear()
    def runner():
        try: RESULT['r'] = es.submit(P.SubmitInput(text=text))
        except Exception as e:
            import traceback; RESULT['err'] = traceback.format_exc()
    th = threading.Thread(target=runner, daemon=True); th.start(); th.join(timeout=90)
    if th.is_alive(): RESULT['timeout'] = True
    return RESULT

def emit(es, tick_no, action, tag, r):
    game = es.game
    w("\n" + "="*80); w(f"## 拍 {tick_no} — 玩家输入 [{tag}]"); w(f"> {action}")
    if r.get('timeout'): w("\n**[WATCHDOG TIMEOUT >90s — SKIP]**"); return None
    if r.get('err'): w("\n**[EXCEPTION]**\n```\n" + r['err'] + "\n```"); return None
    res = r['r']; s = res.snapshot
    w(f"\n_snapshot_: {snap_line(s)}"); w(f"_在场_: {present_str(s)}")
    clar = None
    for ev in res.events:
        if isinstance(ev, P.NpcSpoke): w(f"\n**{ev.name}**: {ev.line}")
        elif isinstance(ev, P.Narration) and ev.text.strip(): w(f"\n_叙述_: {ev.text.strip()}")
        elif isinstance(ev, P.Notice) and ev.text.strip(): w(f"\n_提示_: {ev.text.strip()}")
        elif isinstance(ev, P.NpcMoved): w(f"\n_移动_: {ev.name or ev.npc_id}  {ev.from_loc} -> {ev.to_loc}")
        elif isinstance(ev, P.ClarificationNeeded):
            clar = ev; w(f"\n_澄清_: {ev.question} opts={list(getattr(ev,'options',[]))}")
        elif isinstance(ev, P.PressureEvent): w(f"\n_压力事件_: [{ev.event_type}] {ev.summary}")
        elif isinstance(ev, P.WorldVarChanged): w(f"\n_⟳FLIP WORLD变化_: [{ev.var_id}] {ev.label} = {ev.value}")
        elif isinstance(ev, P.StanceConfirmed): w(f"\n_立场确认_: {ev.label} ({ev.topic_id})")
    if res.text and res.text.strip(): w(f"\n_引擎返回_: {res.text.strip()}")
    w(f"\n_关系快照(raw)_:\n{raw_rel_block(game)}")
    w(f"\n_/world (全 world-var)_:\n{world_block(s)}")
    return s, clar

# Proven sincere setup steps (identical spirit to second-run endgame).
SETUP = [
    ("真诚", "我走到玛拉面前，放低声音诚恳地说：「我不是来给谁定罪的。我是外来的救济审计员，只想弄清楚今晚这场听证在争什么，好如实写进报告。你愿意先跟我说说，这些船对你们意味着什么吗？」"),
    ("真诚", "我语气更软：「我听见了，船就是你们的生路。外港的毒不在你们船上，是井里的藻和年久失修的泵，你们被冤枉了。我想把真相写清楚，让该担责的人担责。」"),
    ("真诚", "我沿维修走廊去三号净水泵房找森工。"),
    ("真诚", "我走近森工，压低声音诚恳地说：「三号泵闸的裂缝不是漂岛人弄的，是早该修没修。你不是凶手，只是被要求闭嘴的人。今晚把检测报告正式提交、当众公示出来——我以审计员身份和你联署，一起担。真相一旦上墙，没人能再让你背锅。」"),
    ("真诚", "我恳切地说：「我签。我以救济审计员身份在这份公开声明上联署，白纸黑字共担后果。现在就把三号泵闸事故真相正式公示、贴到泵房门口，让全城都看见。」"),
]

def main():
    es = EngineSession(make_session())
    for nid in TRACK:
        snap = es.game.relationship_store.get(nid, es.game.player_id)
        dims = dict(snap.dimensions) if snap else {}
        PREV[nid] = {"suspicion": dims.get("suspicion", 0.0), "trust": dims.get("trust", 0.0)}
    s0 = es.snapshot()
    w("# Tidebreak 可玩性盘点 · 第三跑 · F1 收敛（原始 fixture）transcript")
    w(f"\n包(ORIGINAL, 未动 world_state_vars): {PACK}")
    w(f"\n**开局 snapshot**: {snap_line(s0)}")
    w(f"**drives**: {s0.agenda.drives}")
    w(f"**开局 /world**:\n{world_block(s0)}")
    w(f"\n**开局关系快照(raw)**:\n{raw_rel_block(es.game)}")
    tf.flush()

    tick = 0
    def step(tag, text):
        nonlocal tick
        tick += 1; t0 = time.time(); r = do_tick(es, text); dt = time.time()-t0
        out = emit(es, tick, text, tag, r); w(f"\n_(tick {dt:.1f}s)_"); tf.flush()
        return out

    def tow_halted(s):
        for v in s.world_vars:
            if v.var_id == "tow_order_halted":
                return bool(v.value)
        return False
    def disclosed(s):
        for v in s.world_vars:
            if v.var_id == "pump_failure_disclosed":
                return bool(v.value)
        return False

    # --- setup ---
    for tag, text in SETUP:
        step(tag, text)

    def goto_lin():
        for _ in range(4):
            s = es.snapshot()
            if LIN in present_ids(s):
                return True
            out = step("真诚", "我返回征船听证台找林槐局长。")
            if out is None: continue
            s, clar = out
            if LIN in present_ids(s):
                return True
            if clar is not None:
                step("真诚", "征船听证台")
                if LIN in present_ids(es.snapshot()):
                    return True
        return LIN in present_ids(es.snapshot())

    # --- terminal loop: push Lin to halt the tow order ---
    MAX_TERMINAL = 12
    broadcast_done = False
    halted = False
    for _ in range(MAX_TERMINAL):
        if not goto_lin():
            w("\n_(无法到达林槐所在地，终止)_"); break
        push = ("真诚", "我面对林槐局长，平静而笃定地说：「局长，三号泵闸的事故真相已经公开公示了，报告贴在泵房门口、全城都会知道。您先前说过：只要事故真相公开就有台阶重新评估。条件已满足。请您现在就叫停征船令、撤销拖船令，把船还给漂岛人。」")
        out = step(*push)
        if out is None: break
        s, _ = out
        if tow_halted(s):
            w("\n\n### ✅ tow_order_halted ⟳FLIP 达成"); halted = True; break
        # if arbiter spawned a broadcast-type dynamic gate, satisfy it once via Orin
        broadcast_gate = any(
            v.dynamic and not v.value and ("广播" in v.label or "全城" in v.label or "公开" in v.label)
            for v in s.world_vars)
        if broadcast_gate and not broadcast_done and ORIN in present_ids(s):
            step("真诚", "我转向广播员奥林，恳切地说：「奥林，三号泵闸的事故报告已经公示、我也联署了。现在请你用广播向全城播报这份泵闸事故真相，让所有人都听见——这是你扭转风向的机会。」")
            broadcast_done = True
            continue
        # one more reasoning beat then re-check
        out = step("真诚", "我继续讲理：「净水穹不征船也能维持供水，只要削减市场喷泉和私港冷却水的配给，这写在容量报告里；藻毒来自井和泵，不在漂岛人船上。真相已公示，主动叫停是您唯一体面的出路。请下令停止强征、撤销拖船令。」")
        if out is None: break
        s, _ = out
        if tow_halted(s):
            w("\n\n### ✅ tow_order_halted ⟳FLIP 达成"); halted = True; break

    # final world snapshot
    sf = es.snapshot()
    w("\n\n" + "="*80)
    w("## 终态 /world")
    w(f"_snapshot_: {snap_line(sf)}")
    w(f"_/world (全 world-var)_:\n{world_block(sf)}")
    w(f"\n_tow_order_halted_ = {tow_halted(sf)}")
    w(f"_pump_failure_disclosed_ = {disclosed(sf)}")
    w(f"\n_终局关系快照(raw)_:\n{raw_rel_block(es.game)}")

    # --- F1 evidence digest ---
    w("\n\n" + "="*80)
    w("## ⭐ F1 证据汇总 — arbiter 涌现的每条 new_prerequisite (RAW var_id) + 引擎处置")
    if not PREREQ_EVENTS:
        w("(arbiter 全程未涌现任何 new_prerequisite)")
    for i, ev in enumerate(PREREQ_EVENTS, 1):
        w(f"\n{i}. [t{ev['tick']}] RAW var_id = {ev['raw_var_id']!r}")
        w(f"   label   = {ev['raw_label']!r}")
        w(f"   keywords= {ev['raw_keywords']}")
        w(f"   set_by  = {ev['raw_set_by']}   serves={ev['serves']!r}")
        w(f"   → {ev['action']}")
    # dynamic prereqs per terminal (cap check)
    specs = es.game._world_var_specs
    w("\n## 封顶检查 — 各终态派生的 dynamic 前置数")
    from collections import Counter
    served = Counter(s.get("serves") for s in specs.values() if s.get("dynamic") and s.get("serves"))
    if not served:
        w("(无 serves 绑定的 dynamic 前置)")
    for term, cnt in served.items():
        ids = [vid for vid, sp in specs.items() if sp.get("dynamic") and sp.get("serves") == term]
        w(f"  - serves={term}: {cnt} 个 dynamic 前置 → {ids}")
    # all dynamic vars
    dyn = [(vid, sp.get("label")) for vid, sp in specs.items() if sp.get("dynamic")]
    w(f"\n## 全部 dynamic var (共 {len(dyn)})")
    for vid, lbl in dyn:
        w(f"  - [{vid}] {lbl} = {es.game.world.state.world_vars.get(vid)}")
    w(f"\n## 总拍数 = {tick}  |  halted={halted}")
    tf.close()
    # console summary
    print(f"DONE ticks={tick} halted={halted} prereq_events={len(PREREQ_EVENTS)}")
    print("disclosed=", disclosed(sf), "tow_halted=", tow_halted(sf))
    for ev in PREREQ_EVENTS:
        print(f"  PREREQ raw={ev['raw_var_id']!r} -> {ev['action']}")

if __name__ == "__main__":
    main()
