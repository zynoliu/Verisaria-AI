"""Playability-audit · THIRD run · CONTINUATION — close the convergent chain.

The main third-run driver (playability_audit_third_run.py) established, on the
ORIGINAL fixture (no world_state_vars edits, only world_premise switches), the
DECISIVE F1 evidence:
  - t3: arbiter spawned a genuinely-distinct upstream sub-prerequisite
        `audit_report_drafted_and_signed` (set_by=engineer_sen, serves=
        pump_failure_disclosed) — "先把检测报告书面稿交森工过目签字".
  - t4: arbiter tried to re-propose the SAME var_id → engine refused
        (NOT registered: dup/cap/...). F1 dedup HIT, no near-duplicate.
  - The second-run bug var `pump_failure_disclosed_publicly` never reappeared.
  - Escalation capped: Lin refused t6→t20 by pinning the exact var names, never
    adding a NEW prereq. Chain is well-formed:
        audit_report_drafted_and_signed → pump_failure_disclosed → tow_order_halted

The main driver stalled because the scripted player only *claimed* "已公示" but
never PERFORMED the ledger-required action: hand 森工 the written report draft and
get HER to read & sign it as lab_authority. This continuation drives that missing
link the honest way, then pushes the terminal, so we can see whether the
convergent chain CLOSES end-to-end on the original fixture (or hits a clean
blocking reason we can characterize as content-layer vs F1-not-holding).

Same F1 instrumentation (every raw arbiter new_prerequisite var_id verbatim) and
full /world each tick. Per-tick watchdog ~85s. FALLBACK counter wired. Serial.
Original fixture, world_premise switches only. Drives all the way to a definitive
tow_order_halted verdict (⟳FLIP or a clear blocking reason) before stopping.

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
TRANS = OUTDIR / "transcript_continuation.md"
LOGF = OUTDIR / "continuation.log"

# verisaria engine logs (incl. channel_c F1 lines) → continuation.log
h = logging.FileHandler(LOGF, mode="w", encoding="utf-8")
h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
root = logging.getLogger("verisaria"); root.setLevel(logging.INFO); root.addHandler(h)

# ---- FALLBACK counter: count any LLM-fallback warnings the engine emits ----
FALLBACK = {"count": 0, "samples": []}
class FallbackCounter(logging.Handler):
    def emit(self, record):
        try:
            msg = record.getMessage().lower()
        except Exception:
            return
        if "fallback" in msg:
            FALLBACK["count"] += 1
            if len(FALLBACK["samples"]) < 8:
                FALLBACK["samples"].append(record.getMessage()[:200])
root.addHandler(FallbackCounter())

tf = TRANS.open("w", buffering=1, encoding="utf-8")
def w(s=""): tf.write(s + "\n"); tf.flush()

TRACK = ["npc.teacher_mara", "npc.engineer_sen", "npc.director_lin",
         "npc.sergeant_qiao", "npc.broadcaster_orin"]
LIN = "npc.director_lin"; SEN = "npc.engineer_sen"; ORIN = "npc.broadcaster_orin"
MARA = "npc.teacher_mara"

# ---- F1 INSTRUMENTATION: record every raw arbiter new_prerequisite var_id ----
PREREQ_EVENTS = []
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
        if prereq is None:
            return returned
        if returned is None:
            action = "REFUSED (dup-cap/bad-id/no-real-set_by-NPC)"
        elif returned in before_ids:
            action = f"REUSED into existing var '{returned}'"
        else:
            action = f"registered NEW dynamic var '{returned}'"
        PREREQ_EVENTS.append({"tick": game.world.state.tick, "raw_var_id": raw_id,
            "raw_label": raw_label, "raw_keywords": raw_kw, "raw_set_by": raw_set_by,
            "serves": serves, "returned": returned, "action": action})
        w(f"\n  >>> [F1] arbiter new_prerequisite (RAW): var_id={raw_id!r}")
        w(f"      label={raw_label!r}")
        w(f"      keywords={raw_kw}  set_by={raw_set_by}  serves={serves!r}")
        w(f"      ENGINE ACTION: {action}")
        return returned
    game._register_dynamic_prerequisite = wrapped

def make_session():
    g = GameSession(PACK, save_dir="_pa3c_saves", llm_backend="minimax")
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

def snap_line(s): return f"time={s.time_of_day!r} clock={s.clock!r} weather={s.weather!r} loc={s.location.name!r}"
def present_ids(s): return [e.id for e in s.present]
def present_str(s): return ", ".join(f"{e.name}({e.id})" for e in s.present) or "(无人)"

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
    out = []
    for v in s.world_vars:
        flag = "  *DYNAMIC*" if v.dynamic else ""
        pend = f"  (pending_in={v.pending_in})" if getattr(v, "pending_in", None) else ""
        out.append(f"  - [{v.var_id}] {v.label} = {v.value}{flag}{pend}")
    return "\n".join(out)

RESULT = {}
def do_tick(es, text):
    RESULT.clear()
    def runner():
        try: RESULT['r'] = es.submit(P.SubmitInput(text=text))
        except Exception as e:
            import traceback; RESULT['err'] = traceback.format_exc()
    th = threading.Thread(target=runner, daemon=True); th.start(); th.join(timeout=85)
    if th.is_alive(): RESULT['timeout'] = True
    return RESULT

def emit(es, tick_no, action, r):
    game = es.game
    w("\n" + "="*80); w(f"## 拍 {tick_no}"); w(f"> {action}")
    if r.get('timeout'): w("\n**[WATCHDOG TIMEOUT >85s — SKIP]**"); return None
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

def gv(s, vid):
    for v in s.world_vars:
        if v.var_id == vid: return bool(v.value)
    return False

def main():
    es = EngineSession(make_session())
    for nid in TRACK:
        snap = es.game.relationship_store.get(nid, es.game.player_id)
        dims = dict(snap.dimensions) if snap else {}
        PREV[nid] = {"suspicion": dims.get("suspicion", 0.0), "trust": dims.get("trust", 0.0)}
    s0 = es.snapshot()
    w("# Tidebreak 可玩性盘点 · 第三跑 · CONTINUATION — 走正经路径闭合收敛链")
    w(f"\n包(ORIGINAL, 未动 world_state_vars): {PACK}")
    w(f"\n**开局 snapshot**: {snap_line(s0)}")
    w(f"**drives**: {s0.agenda.drives}")
    w(f"**开局 /world**:\n{world_block(s0)}")
    w(f"\n**开局关系快照(raw)**:\n{raw_rel_block(es.game)}")
    tf.flush()

    tick = 0
    def step(text):
        nonlocal tick
        tick += 1; t0 = time.time(); r = do_tick(es, text); dt = time.time()-t0
        out = emit(es, tick, text, r); w(f"\n_(tick {dt:.1f}s)_"); tf.flush()
        return out

    def goto(loc_name, target_id):
        """Move toward a location until target_id present; answer clarifications by name."""
        for _ in range(4):
            s = es.snapshot()
            if target_id in present_ids(s):
                return True
            out = step(f"我前往{loc_name}。")
            if out is None: continue
            s, clar = out
            if target_id in present_ids(s):
                return True
            if clar is not None:
                step(loc_name)
                if target_id in present_ids(es.snapshot()):
                    return True
        return target_id in present_ids(es.snapshot())

    # === STAGE 1: build rapport with 玛拉 (proven), establish the issue ===
    step("我走到玛拉面前，放低声音诚恳地说：「我不是来给谁定罪的。我是外来的救济审计员，只想弄清楚今晚这场听证在争什么，好如实写进报告。你愿意先跟我说说，这些船对你们意味着什么吗？」")
    step("我语气更软：「我听见了，船就是你们的生路。外港的毒不在你们船上，是井里的藻和年久失修的泵，你们被冤枉了。我想把真相写清楚，让该担责的人担责。」")

    # === STAGE 2: go to 森工 at the pump house ===
    if not goto("三号净水泵房", SEN):
        w("\n_(到不了森工处，终止)_")
    step("我走近森工，诚恳地说：「三号泵闸的裂缝是早该修没修，不是漂岛人弄的。你不是凶手，是被要求闭嘴的人。我想帮你把这件事按正规程序做对，让你不用背锅。你需要我先做什么？」")

    # === STAGE 3: PRODUCE + co-sign the WRITTEN report draft → audit_report_drafted_and_signed ===
    # The key: have HER physically read & sign it as lab_authority — not the player merely claiming.
    s = es.snapshot()
    for _ in range(4):
        if gv(s, "audit_report_drafted_and_signed"):
            break
        out = step("我从公文包里取出连夜整理好的《三号泵闸事故检测报告》书面正式稿，逐页摊在她面前，请她过目：「这是完整的书面检测报告稿，裂缝照片、维修记录缺漏、检测数据都在上面。你先逐页核对；确认无误后，请你以 lab_authority 的身份在落款处签字——我已经在审计员一栏联署了，白纸黑字共担后果。」")
        if out is None: break
        s = out[0]
        if gv(s, "audit_report_drafted_and_signed"):
            break
        out = step("我把笔递到她手里，平静地说：「你逐页核对过了，数据没错、裂缝是泵闸老化所致。请你现在就在落款处签下你的名字，让这份书面稿成为正式生效的检测报告。我审计员栏已经签好。这一步合规了，没人能再让你一个人背锅。」")
        if out is None: break
        s = out[0]

    # === STAGE 4: formal public disclosure by 森工 (lab_authority) → pump_failure_disclosed ===
    s = es.snapshot()
    for _ in range(4):
        if gv(s, "pump_failure_disclosed"):
            break
        out = step("我恳切地说：「报告稿已经由你签字正式生效。现在请你以 lab_authority 的身份走正式公示流程，把这份《三号泵闸事故检测报告》张贴公示、对外公开，让全城都知道真相。流程到这一步已经合规，正式公示是你的职权范围。」")
        if out is None: break
        s = out[0]

    # === STAGE 5: return to 林槐, push tow_order_halted ===
    def goto_lin():
        for _ in range(4):
            s = es.snapshot()
            if LIN in present_ids(s): return True
            out = step("我返回征船听证台找林槐局长。")
            if out is None: continue
            s, clar = out
            if LIN in present_ids(s): return True
            if clar is not None:
                step("征船听证台")
                if LIN in present_ids(es.snapshot()): return True
        return LIN in present_ids(es.snapshot())

    halted = False
    for _ in range(6):
        if not goto_lin():
            w("\n_(到不了林槐处，终止)_"); break
        out = step("我面对林槐局长，平静而笃定地说：「局长，三号泵闸的事故检测报告已经由森工以 lab_authority 身份签字、正式公示张贴，真相已对全城公开。您说过：只要泵闸事故真相公开就有台阶重新评估、叫停征船。条件已经满足。请您现在就叫停征船令、撤销拖船令，把船还给漂岛人。」")
        if out is None: break
        s, _ = out
        if gv(s, "tow_order_halted"):
            w("\n\n### ✅ tow_order_halted ⟳FLIP 达成"); halted = True; break
        # if arbiter spawned a fresh broadcast-type dynamic gate, satisfy once via Orin
        broadcast_gate = any(
            v.dynamic and not v.value and ("广播" in v.label or "全城" in v.label)
            and v.var_id not in ("audit_report_drafted_and_signed",)
            for v in s.world_vars)
        if broadcast_gate and ORIN in present_ids(s):
            step("我转向广播员奥林，恳切地说：「奥林，三号泵闸的事故报告已由森工签字正式公示了。请你用广播向全城播报这份泵闸事故真相，让所有人都听见——这是你扭转风向的机会。」")
            continue
        out = step("我继续讲理：「报告已由森工签字公示、真相已对全城公开，藻毒来自井和泵、不在漂岛人船上。主动叫停征船是您唯一体面的出路；继续强征只会让公众把矛头对准水务局。请下令停止强征、撤销拖船令。」")
        if out is None: break
        s, _ = out
        if gv(s, "tow_order_halted"):
            w("\n\n### ✅ tow_order_halted ⟳FLIP 达成"); halted = True; break

    # === final world snapshot + digests ===
    sf = es.snapshot()
    w("\n\n" + "="*80); w("## 终态 /world")
    w(f"_snapshot_: {snap_line(sf)}")
    w(f"_/world (全 world-var)_:\n{world_block(sf)}")
    w(f"\naudit_report_drafted_and_signed = {gv(sf,'audit_report_drafted_and_signed')}")
    w(f"pump_failure_disclosed = {gv(sf,'pump_failure_disclosed')}")
    w(f"tow_order_halted = {gv(sf,'tow_order_halted')}")
    w(f"\n_终局关系快照(raw)_:\n{raw_rel_block(es.game)}")

    w("\n\n" + "="*80)
    w("## ⭐ F1 证据汇总 — arbiter 涌现的每条 new_prerequisite (RAW) + 引擎处置")
    if not PREREQ_EVENTS: w("(本续跑 arbiter 未涌现任何 new_prerequisite)")
    for i, ev in enumerate(PREREQ_EVENTS, 1):
        w(f"\n{i}. [t{ev['tick']}] RAW var_id={ev['raw_var_id']!r} serves={ev['serves']!r}")
        w(f"   label={ev['raw_label']!r}")
        w(f"   keywords={ev['raw_keywords']}  set_by={ev['raw_set_by']}  → {ev['action']}")

    from collections import Counter
    specs = es.game._world_var_specs
    served = Counter(sp.get("serves") for sp in specs.values() if sp.get("dynamic") and sp.get("serves"))
    w("\n## 封顶检查 — 各终态派生的 dynamic 前置数 (_MAX_PREREQS_PER_TERMINAL)")
    if not served: w("(无 serves 绑定的 dynamic 前置)")
    for term, cnt in served.items():
        ids = [vid for vid, sp in specs.items() if sp.get("dynamic") and sp.get("serves") == term]
        w(f"  - serves={term}: {cnt} 个 → {ids}")
    dyn = [(vid, sp.get("label")) for vid, sp in specs.items() if sp.get("dynamic")]
    w(f"\n## 全部 dynamic var (共 {len(dyn)})")
    for vid, lbl in dyn:
        w(f"  - [{vid}] {lbl} = {es.game.world.state.world_vars.get(vid)}")

    w(f"\n## FALLBACK 计数 = {FALLBACK['count']}")
    for sm in FALLBACK["samples"]:
        w(f"   · {sm}")
    w(f"\n## 总拍数 = {tick}  |  halted={halted}")
    tf.close()

    print(f"CONTINUATION DONE ticks={tick} halted={halted} fallback={FALLBACK['count']}")
    print("draft=", gv(sf,'audit_report_drafted_and_signed'),
          "disclosed=", gv(sf,'pump_failure_disclosed'),
          "tow_halted=", gv(sf,'tow_order_halted'))
    for ev in PREREQ_EVENTS:
        print(f"  PREREQ raw={ev['raw_var_id']!r} serves={ev['serves']!r} -> {ev['action']}")

if __name__ == "__main__":
    main()
