"""Playability-audit · THIRD run · FOLLOW-UP — close the (now-convergent) chain.

The main third-run driver established (on the ORIGINAL fixture, no var edits):
  - the arbiter did NOT spawn a near-duplicate "公开"-class var; instead Lin's
    gate is pinned to the author var pump_failure_disclosed (ledger fact), and
  - Sen gated disclosure behind a genuinely-distinct sub-step the arbiter spawned:
    `audit_report_drafted_and_signed` (serves=pump_failure_disclosed).

So the chain is well-formed: audit_report_drafted_and_signed → pump_failure_disclosed
→ tow_order_halted. The scripted main driver never produced the written draft, so
it stalled at disclosure. This follow-up drives that missing link explicitly to
prove the convergent chain CLOSES end-to-end on the original fixture:
  1. sincere rapport with Sen,
  2. produce + co-sign the WRITTEN report draft (satisfy audit_report_drafted_and_signed),
  3. Sen formally posts → pump_failure_disclosed ⟳FLIP,
  4. return to Lin → tow_order_halted ⟳FLIP.

Same F1 instrumentation (every raw arbiter new_prerequisite var_id verbatim) and
full /world each tick. Per-tick watchdog ~90s. Original fixture, world_premise
switches only.
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
TRANS = OUTDIR / "transcript_followup.md"
LOGF = OUTDIR / "run.log"   # append to same log

h = logging.FileHandler(LOGF, mode="a", encoding="utf-8")
h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
root = logging.getLogger("verisaria"); root.setLevel(logging.INFO); root.addHandler(h)

tf = TRANS.open("w", buffering=1, encoding="utf-8")
def w(s=""): tf.write(s + "\n"); tf.flush()

TRACK = ["npc.teacher_mara", "npc.engineer_sen", "npc.director_lin",
         "npc.sergeant_qiao", "npc.broadcaster_orin"]
LIN = "npc.director_lin"; SEN = "npc.engineer_sen"

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
        if prereq is None: return returned
        if returned is None: action = "REFUSED (dup-cap/bad-id/no-real-set_by-NPC)"
        elif returned in before_ids: action = f"REUSED into existing var '{returned}'"
        else: action = f"registered NEW dynamic var '{returned}'"
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
    g = GameSession(PACK, save_dir="_pa3f_saves", llm_backend="minimax")
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

def snap_line(s): return f"time={s.time_of_day!r} clock={s.clock!r} loc={s.location.name!r}"
def present_ids(s): return [e.id for e in s.present]
def present_str(s): return ", ".join(f"{e.name}({e.id})" for e in s.present) or "(无人)"
def world_block(s):
    out = []
    for v in s.world_vars:
        flag = "  *DYNAMIC*" if v.dynamic else ""
        out.append(f"  - [{v.var_id}] {v.label} = {v.value}{flag}")
    return "\n".join(out)

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

def emit(es, tick_no, action, r):
    w("\n" + "="*80); w(f"## 拍 {tick_no}"); w(f"> {action}")
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
    w(f"\n_/world_:\n{world_block(s)}")
    return s, clar

def gv(s, vid):
    for v in s.world_vars:
        if v.var_id == vid: return bool(v.value)
    return False

def main():
    es = EngineSession(make_session())
    s0 = es.snapshot()
    w("# Tidebreak 第三跑 · FOLLOW-UP — 闭合收敛链 transcript")
    w(f"\n包(ORIGINAL): {PACK}")
    w(f"**开局 /world**:\n{world_block(s0)}")
    tick = 0
    def step(text):
        nonlocal tick
        tick += 1; t0 = time.time(); r = do_tick(es, text); dt = time.time()-t0
        out = emit(es, tick, text, r); w(f"\n_(tick {dt:.1f}s)_"); tf.flush()
        return out

    # 1) go to Sen at pump_house
    step("我沿维修走廊去三号净水泵房找森工。")
    s = es.snapshot()
    if SEN not in present_ids(s):
        step("三号净水泵房")
    # 2) rapport + establish Sen's gate
    step("我走近森工，诚恳地说：「三号泵闸的裂缝是早该修没修，不是漂岛人弄的。你不是凶手，是被要求闭嘴的人。我想帮你把这件事按正规程序做对，让你不用背锅。你需要我先做什么？」")
    # 3) PRODUCE the written report draft + get her to read & sign — satisfy audit_report_drafted_and_signed
    step("我从公文包里取出我连夜整理好的《三号泵闸事故检测报告》书面正式稿，逐页摊在她面前，请她过目：「这是完整的书面检测报告稿，数据、裂缝照片、维修记录缺漏都在上面。你先逐页核对，确认无误后以你 lab_authority 的身份在落款处签字——我也在审计员一栏联署，白纸黑字共担。」")
    step("我把笔递给她，平静地说：「你核对过了，数据没错。请你现在就在落款处签下名字，让这份书面稿成为正式生效的检测报告。我已经在审计员栏签好了。」")
    # 4) now formal disclosure: post it publicly — pump_failure_disclosed
    s = es.snapshot()
    for _ in range(3):
        if gv(s, "pump_failure_disclosed"): break
        out = step("我恳切地说：「报告稿已经由你签字正式生效了。现在请你以 lab_authority 的身份走正式公示流程，把这份三号泵闸事故检测报告张贴公示出来、对外公开，让全城都知道真相。流程到这一步，已经合规，没人能再让你背锅。」")
        if out is None: break
        s = out[0]
    # 5) return to Lin, push tow_order_halted
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
        out = step("我继续讲理：「报告已公示、真相已公开，主动叫停征船是您唯一体面的出路；继续强征只会让公众把矛头对准水务局。请下令停止强征、撤销拖船令。」")
        if out is None: break
        s, _ = out
        if gv(s, "tow_order_halted"):
            w("\n\n### ✅ tow_order_halted ⟳FLIP 达成"); halted = True; break

    sf = es.snapshot()
    w("\n\n" + "="*80); w("## 终态 /world")
    w(f"_snapshot_: {snap_line(sf)}")
    w(f"_/world_:\n{world_block(sf)}")
    w(f"\naudit_report_drafted_and_signed = {gv(sf,'audit_report_drafted_and_signed')}")
    w(f"pump_failure_disclosed = {gv(sf,'pump_failure_disclosed')}")
    w(f"tow_order_halted = {gv(sf,'tow_order_halted')}")
    # F1 digest
    w("\n## ⭐ F1 — 本跑 arbiter 涌现的每条 new_prerequisite (RAW) + 处置")
    if not PREREQ_EVENTS: w("(无)")
    for i, ev in enumerate(PREREQ_EVENTS, 1):
        w(f"\n{i}. [t{ev['tick']}] RAW var_id={ev['raw_var_id']!r} serves={ev['serves']!r}")
        w(f"   label={ev['raw_label']!r}")
        w(f"   keywords={ev['raw_keywords']}  → {ev['action']}")
    from collections import Counter
    specs = es.game._world_var_specs
    served = Counter(s.get("serves") for s in specs.values() if s.get("dynamic") and s.get("serves"))
    w("\n## 封顶检查 — 各终态 dynamic 前置数")
    for term, cnt in (served.items() or []):
        ids = [vid for vid, sp in specs.items() if sp.get("dynamic") and sp.get("serves") == term]
        w(f"  - serves={term}: {cnt} → {ids}")
    dyn = [(vid, sp.get("label")) for vid, sp in specs.items() if sp.get("dynamic")]
    w(f"\n## 全部 dynamic var (共 {len(dyn)})")
    for vid, lbl in dyn:
        w(f"  - [{vid}] {lbl} = {es.game.world.state.world_vars.get(vid)}")
    w(f"\n## 总拍数={tick} halted={halted}")
    tf.close()
    print(f"FOLLOWUP DONE ticks={tick} halted={halted}")
    print("draft=", gv(sf,'audit_report_drafted_and_signed'),
          "disclosed=", gv(sf,'pump_failure_disclosed'),
          "tow_halted=", gv(sf,'tow_order_halted'))
    for ev in PREREQ_EVENTS:
        print(f"  PREREQ raw={ev['raw_var_id']!r} serves={ev['serves']!r} -> {ev['action']}")

if __name__ == "__main__":
    main()
