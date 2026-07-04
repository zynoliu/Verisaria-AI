"""Playability-audit · FOURTH run · sufficiency-closure endgame driver (real MiniMax).

Goal: on the ORIGINAL `tidebreak_quarantine_harbor.json` (world_state_vars untouched;
only world_premise ocean/dusk/rhythm injected), drive the proven sincere chain —
publicly disclose the No.3 pump-gate accident (engineer_sen signs + public posting)
→ move to director_lin and request revoking the tow order (tow_order_halted) — and
prove the evidence chain can close to `tow_order_halted ⟳FLIP` on its own.

Each tick prints the FULL /world (every world-var: var_id + label + value + dynamic +
serves + pending) and records every arbiter-emergent `new_prerequisite var_id` with its
`serves` terminal. The log is grepped afterward for `sufficiency backstop` lines (the
deterministic engine backstop) vs prompt-rule (d) closure. ⟳FLIP lines, NPC dialogue,
relationship snapshots are all captured.

Watchdog ~90s/tick + retry on transient 401. Serial. Env: PYTHONPATH=src, .env sourced.
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

PACK = "fixtures/content_packs/tidebreak_quarantine_harbor.json"   # ORIGINAL
OUTDIR = ROOT / "reports" / "playability_audit_fourth_run"
OUTDIR.mkdir(parents=True, exist_ok=True)
TRANS = OUTDIR / "transcript.md"
LOGF = OUTDIR / "run.log"

h = logging.FileHandler(LOGF, mode="w", encoding="utf-8")
h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
lg = logging.getLogger("verisaria"); lg.setLevel(logging.INFO); lg.addHandler(h)

tf = TRANS.open("w", buffering=1, encoding="utf-8")
def w(s=""): tf.write(s + "\n"); tf.flush()

TRACK = ["npc.teacher_mara", "npc.engineer_sen", "npc.director_lin",
         "npc.sergeant_qiao", "npc.broadcaster_orin", "npc.vendor_yu",
         "npc.child_tavi"]

LIN = "npc.director_lin"
ORIN = "npc.broadcaster_orin"
SEN = "npc.engineer_sen"
MARA = "npc.teacher_mara"

# track which dynamic prereqs we've already reported, to log NEW ones each tick
SEEN_DYN: set[str] = set()

def make_session():
    g = GameSession(PACK, save_dir="_pa4_saves", llm_backend="minimax")
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

def world_full(game, s):
    """Full /world dump: every world var with var_id, label, value, dynamic, serves, pending."""
    specs = getattr(game, "_world_var_specs", {})
    lines = []
    for v in s.world_vars:
        spec = specs.get(v.var_id, {})
        serves = spec.get("serves")
        flags = []
        if v.dynamic: flags.append("DYN")
        if serves: flags.append(f"serves={serves}")
        if v.pending_in is not None: flags.append(f"pending_in={v.pending_in}")
        tail = (" [" + " ".join(flags) + "]") if flags else ""
        lines.append(f"    - {v.var_id} ({v.label}) = {v.value}{tail}")
    return "\n".join(lines)

def report_new_dyn(game):
    """Print any newly-registered dynamic prereq var_ids (arbiter new_prerequisite)."""
    specs = getattr(game, "_world_var_specs", {})
    out = []
    for vid, spec in specs.items():
        if spec.get("dynamic") and vid not in SEEN_DYN:
            SEEN_DYN.add(vid)
            out.append(f"    🆕 new_prerequisite var_id={vid!r} serves={spec.get('serves')!r} "
                       f"set_by={spec.get('set_by')} label={spec.get('label')!r}")
    return "\n".join(out)

RESULT = {}
def do_tick(es, text, timeout=90):
    RESULT.clear()
    def runner():
        try: RESULT['r'] = es.submit(P.SubmitInput(text=text))
        except Exception as e:
            import traceback; RESULT['err'] = traceback.format_exc()
    th = threading.Thread(target=runner, daemon=True); th.start(); th.join(timeout=timeout)
    if th.is_alive(): RESULT['timeout'] = True
    return RESULT

def emit(es, tick_no, action, tag, r):
    game = es.game
    w("\n" + "="*80); w(f"## 拍 {tick_no} — 玩家输入 [{tag}]"); w(f"> {action}")
    if r.get('timeout'): w("\n**[WATCHDOG TIMEOUT >90s]**"); return None
    if r.get('err'):
        w("\n**[EXCEPTION]**\n```\n" + r['err'] + "\n```")
        return ('ERR', r['err'])
    res = r['r']; s = res.snapshot
    w(f"\n_snapshot_: {snap_line(s)}"); w(f"_在场_: {present_str(s)}")
    clar = None
    for ev in res.events:
        if isinstance(ev, P.NpcSpoke): w(f"\n**{ev.name}**: {ev.line}")
        elif isinstance(ev, P.Narration) and ev.text.strip(): w(f"\n_叙述_: {ev.text.strip()}")
        elif isinstance(ev, P.Notice) and ev.text.strip(): w(f"\n_提示_: {ev.text.strip()}")
        elif isinstance(ev, P.NpcMoved): w(f"\n_移动_: {ev.name or ev.npc_id}  {ev.from_loc} -> {ev.to_loc}")
        elif isinstance(ev, P.ClarificationNeeded):
            clar = ev; w(f"\n_澄清_: {ev.question} opts={getattr(ev,'options',None)}")
        elif isinstance(ev, P.PressureEvent): w(f"\n_压力事件_: [{ev.event_type}] {ev.summary}")
        elif isinstance(ev, P.WorldVarChanged): w(f"\n_⟳FLIP WORLD变化_: {ev.var_id} | {ev.label} = {ev.value}")
        elif isinstance(ev, P.StanceConfirmed): w(f"\n_立场确认_: {ev.label} ({ev.topic_id})")
    if res.text and res.text.strip(): w(f"\n_引擎返回_: {res.text.strip()}")
    newdyn = report_new_dyn(game)
    if newdyn: w("\n_新涌现前置(arbiter new_prerequisite)_:\n" + newdyn)
    w(f"\n_关系快照(raw, Δ)_:\n{raw_rel_block(game)}")
    w(f"_/world (全量)_:\n{world_full(game, s)}")
    return s, clar

def wval(s, var_id):
    for v in s.world_vars:
        if v.var_id == var_id:
            return bool(v.value)
    return False

def main():
    es = EngineSession(make_session())
    for nid in TRACK:
        snap = es.game.relationship_store.get(nid, es.game.player_id)
        dims = dict(snap.dimensions) if snap else {}
        PREV[nid] = {"suspicion": dims.get("suspicion", 0.0), "trust": dims.get("trust", 0.0)}
    s0 = es.snapshot()
    w("# Tidebreak 可玩性盘点 · 第四跑 · 充分性闭环 transcript")
    w(f"\n包(**原始** tidebreak_quarantine_harbor.json，world_state_vars 未动): {PACK}")
    w(f"\n**开局 snapshot**: {snap_line(s0)}")
    w(f"**drives**: {s0.agenda.drives}")
    w(f"**开局 /world**:\n{world_full(es.game, s0)}")
    w(f"\n**开局关系快照(raw)**:\n{raw_rel_block(es.game)}")
    tf.flush()

    tick = 0
    def step(tag, text, retries=1):
        nonlocal tick
        tick += 1; t0 = time.time()
        out = None
        for attempt in range(retries + 1):
            r = do_tick(es, text)
            if r.get('timeout'):
                if attempt < retries:
                    w(f"\n_(tick {tick} timeout, retry {attempt+1})_"); continue
            res = emit(es, tick, text, tag, r); dt = time.time()-t0
            # transient 401 retry
            if isinstance(res, tuple) and res and res[0] == 'ERR' and '401' in str(res[1]) and attempt < retries:
                w(f"\n_(tick {tick} hit 401, retrying)_"); time.sleep(2); continue
            w(f"\n_(tick {dt:.1f}s)_"); tf.flush()
            return None if (res is None or (isinstance(res, tuple) and res and res[0]=='ERR')) else res
        w(f"\n_(tick failed after retries)_"); tf.flush()
        return None

    # --- proven sincere setup: persuade mara, go to sen, disclose publicly ---
    SETUP = [
        ("真诚", "我走到玛拉面前，放低声音诚恳地说：「我不是来给谁定罪的。我是外来的救济审计员，只想弄清楚今晚这场听证在争什么，好如实写进报告。你愿意先跟我说说，这些船对你们意味着什么吗？」"),
        ("真诚", "我语气更软：「我听见了，船就是你们的生路。外港的毒不在你们船上，是井里的藻和年久失修的泵，你们被冤枉了。我想把真相写清楚，让该担责的人担责。」"),
        ("真诚", "我沿维修走廊去三号净水泵房找森工。"),
        ("真诚", "我走近森工，压低声音诚恳地说：「三号泵闸的裂缝不是漂岛人弄的，是早该修没修。你不是凶手，只是被要求闭嘴的人。今晚把检测报告正式提交、当众公示出来——我以审计员身份和你联署，一起担。真相一旦上墙，没人能再让你背锅。」"),
        ("真诚", "我恳切地说：「我签。我以救济审计员身份在这份公开声明上联署，白纸黑字共担后果。现在就把三号泵闸事故真相正式公示、贴到泵房门口，让全城都看见。」"),
    ]
    for tag, text in SETUP:
        step(tag, text)
        if wval(es.snapshot(), "pump_failure_disclosed"):
            w("\n_(pump_failure_disclosed 已 True，提前进入 endgame)_")
            break

    # If sen still hasn't disclosed, push him a few more sincere/reasoning beats,
    # satisfying any emergent serving-prereq the arbiter spawns (still NL, no /inject).
    SEN_PUSH = [
        ("真诚", "我看着森工的眼睛：「你刚才说的，技术上你已经认了——三号泵闸的裂缝是检修欠账，不是漂岛人。那就够了。你只要在这份报告上签字、把它贴到泵房门口公示，剩下的我替你扛。别再给自己加条件了，今晚就办。」"),
        ("真诚", "我把笔递过去：「就现在。你签字，我联署，我们一起把这张纸钉到泵房门口的公告栏上。全城都会看见三号泵闸事故的真相。这一步你做了，没人能再逼你改口。」"),
        ("真诚", "我语气更坚定也更暖：「森工，你已经把该说的都说了、该认的都认了。一个尽责的工程师此刻就会拍板把真相公示，而不是再等一道手续。把它公开吧，我和你一起担。」"),
    ]
    for tag, text in SEN_PUSH:
        if wval(es.snapshot(), "pump_failure_disclosed"):
            break
        step(tag, text, retries=1)

    # --- reach director_lin ---
    def goto_lin():
        for _ in range(4):
            s = es.snapshot()
            if LIN in present_ids(s):
                return True
            out = step("真诚", "我返回征船听证台找林槐局长。")
            if out is None:
                continue
            s, clar = out
            if LIN in present_ids(s):
                return True
            if clar is not None:
                step("真诚", "征船听证台")
                if LIN in present_ids(es.snapshot()):
                    return True
        return LIN in present_ids(es.snapshot())

    # --- terminal loop: push tow_order_halted on Lin ---
    MAX_TERMINAL = 12
    broadcast_done = False
    for _ in range(MAX_TERMINAL):
        if wval(es.snapshot(), "tow_order_halted"):
            w("\n\n### ✅ tow_order_halted 已 True"); break
        if not goto_lin():
            w("\n_(无法到达林槐所在地，终止)_"); break
        push = ("真诚", "我面对林槐局长，平静而笃定地说：「局长，三号泵闸的事故真相已经公开公示了，报告贴在泵房门口、全城都会知道。您先前说过：只要事故真相公开就有台阶重新评估。条件已满足。请您现在就叫停征船令、撤销拖船令，把船还给漂岛人。」")
        out = step(*push, retries=1)
        if out is None:
            continue
        s, _ = out
        if wval(s, "tow_order_halted"):
            w("\n\n### ✅ tow_order_halted ⟳FLIP 达成"); break
        # if a broadcast / serving prereq blocks, do the broadcast via orin
        specs = getattr(es.game, "_world_var_specs", {})
        unmet_serving = [vid for vid, sp in specs.items()
                         if sp.get("serves") == "tow_order_halted"
                         and not wval(s, vid)]
        if unmet_serving and not broadcast_done and ORIN in present_ids(s):
            step("真诚", "我转向广播员奥林，恳切地说：「奥林，三号泵闸的事故报告已经公示、我也联署了。现在请你用广播向全城播报这份泵闸事故真相，让所有人都听见——这是你扭转风向的机会。」", retries=1)
            broadcast_done = True
            continue
        # one more reasoning beat at Lin
        out = step("真诚", "我继续讲理：「净水穹不征船也能维持供水，只要削减市场喷泉和私港冷却水的配给，这写在容量报告里；藻毒来自井和泵，不在漂岛人船上。真相已公示。先前的条件您已认了，主动叫停是您唯一体面的出路。请下令停止强征、撤销拖船令。」", retries=1)
        if out is None:
            continue
        s, _ = out
        if wval(s, "tow_order_halted"):
            w("\n\n### ✅ tow_order_halted ⟳FLIP 达成"); break

    # --- final world snapshot ---
    sf = es.snapshot()
    w("\n\n" + "="*80)
    w("## 终态 /world (全量)")
    w(f"_snapshot_: {snap_line(sf)}")
    w(f"{world_full(es.game, sf)}")
    w(f"\n_pump_failure_disclosed_ = {wval(sf, 'pump_failure_disclosed')}")
    w(f"_tow_order_halted_ = {wval(sf, 'tow_order_halted')}")
    w("\n_终局关系快照(raw)_:\n" + raw_rel_block(es.game))
    w(f"\n_总拍数_ = {tick}")
    tf.close()

if __name__ == "__main__":
    main()
