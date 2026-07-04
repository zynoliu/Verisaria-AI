"""Playability-audit · second run · ENDGAME adaptive driver (real MiniMax).

Goal: drive the proven sincere chain to a definitive `tow_order_halted` verdict
(⟳FLIP or a clear blocking reason), instead of a blind pre-baked queue. After
each tick it inspects the snapshot (present NPCs, world vars) and picks the next
move/speak so it actually reaches 林槐 (director_lin) and pushes the terminal —
answering move-clarifications by location name, and satisfying any escalated
public-disclosure gate (broadcast via 奥林) if the arbiter spawns one.

Runs the AUTHORED pack (var labels collapse the 存档/公示 split). Watchdog ~95s.
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

PACK = "reports/playability_audit_second_run/tidebreak_quarantine_harbor_authored.json"
OUTDIR = ROOT / "reports" / "playability_audit_second_run"
TRANS = OUTDIR / "transcript_endgame.md"
LOGF = OUTDIR / "continuation.log"   # append-continue same log

h = logging.FileHandler(LOGF, mode="a", encoding="utf-8")
h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
lg = logging.getLogger("verisaria"); lg.setLevel(logging.INFO); lg.addHandler(h)

tf = TRANS.open("w", buffering=1, encoding="utf-8")
def w(s=""): tf.write(s + "\n"); tf.flush()

TRACK = ["npc.teacher_mara", "npc.engineer_sen", "npc.director_lin",
         "npc.sergeant_qiao", "npc.broadcaster_orin", "npc.vendor_yu",
         "npc.child_tavi"]

def make_session():
    g = GameSession(PACK, save_dir="_paeg_saves", llm_backend="minimax")
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
        extra = "/".join(f"{k}:{v:+.2f}" for k, v in sorted(dims.items())
                         if k not in ("suspicion", "trust") and abs(v) > 0.001)
        lines.append(f"  - {name}: suspicion={susp:.3f} (Δ{dsus:+.3f}) trust={trust:.3f} (Δ{dtru:+.3f})"
                     + (f" | {extra}" if extra else ""))
        PREV[nid] = {"suspicion": susp, "trust": trust}
    return "\n".join(lines)

def wvars(s):
    return {v.label: v.value for v in s.world_vars}
def wvars_str(s):
    return ", ".join(f"{v.label}={v.value}" + ("*dyn" if v.dynamic else "") for v in s.world_vars)

RESULT = {}
def do_tick(es, text):
    RESULT.clear()
    def runner():
        try: RESULT['r'] = es.submit(P.SubmitInput(text=text))
        except Exception as e:
            import traceback; RESULT['err'] = traceback.format_exc()
    th = threading.Thread(target=runner, daemon=True); th.start(); th.join(timeout=95)
    if th.is_alive(): RESULT['timeout'] = True
    return RESULT

def emit(es, tick_no, action, tag, r):
    game = es.game
    w("\n" + "="*80); w(f"## 拍 {tick_no} — 玩家输入 [{tag}]"); w(f"> {action}")
    if r.get('timeout'): w("\n**[WATCHDOG TIMEOUT >95s]**"); return None
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
            clar = ev; w(f"\n_澄清_: {ev.question} opts={getattr(ev,'options',None)}")
        elif isinstance(ev, P.PressureEvent): w(f"\n_压力事件_: [{ev.event_type}] {ev.summary}")
        elif isinstance(ev, P.WorldVarChanged): w(f"\n_WORLD变化_: {ev.label} = {ev.value}")
        elif isinstance(ev, P.StanceConfirmed): w(f"\n_立场确认_: {ev.label} ({ev.topic_id})")
    if res.text and res.text.strip(): w(f"\n_引擎返回_: {res.text.strip()}")
    w(f"\n_关系快照(raw, 含负值与Δ)_:\n{raw_rel_block(game)}")
    w(f"_world_: {wvars_str(s)}")
    return s, clar

LIN = "npc.director_lin"
ORIN = "npc.broadcaster_orin"
SEN = "npc.engineer_sen"
MARA = "npc.teacher_mara"

# Proven setup steps (sincere). Each is (tag, text).
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
    w("# Tidebreak 可玩性盘点 · 第二跑 · ENDGAME (adaptive) transcript")
    w(f"\n包(authored, 合并存档/公示双前置): {PACK}")
    w(f"\n**开局 snapshot**: {snap_line(s0)}")
    w(f"**drives**: {s0.agenda.drives}")
    w(f"**world vars**: {wvars_str(s0)}")
    w(f"\n**开局关系快照(raw)**:\n{raw_rel_block(es.game)}")
    tf.flush()

    tick = 0
    def step(tag, text):
        nonlocal tick
        tick += 1; t0 = time.time(); r = do_tick(es, text); dt = time.time()-t0
        out = emit(es, tick, text, tag, r); w(f"\n_(tick {dt:.1f}s)_"); tf.flush()
        return out  # (snapshot, clar) or None

    # --- setup ---
    for tag, text in SETUP:
        step(tag, text)

    HALT_LABEL_KEY = "叫停"
    def tow_halted(s):
        for v in s.world_vars:
            if "强征令是否叫停" in v.label or v.var_id == "tow_order_halted":
                return bool(v.value)
        return False
    def disclosed(s):
        for v in s.world_vars:
            if v.var_id == "pump_failure_disclosed" or "已公开公示" in v.label:
                return bool(v.value)
        return False

    def goto_lin():
        """Move until 林槐 is present; answer clarifications by name."""
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
                s2 = es.snapshot()
                if LIN in present_ids(s2):
                    return True
        return LIN in present_ids(es.snapshot())

    # --- terminal loop: push Lin; if a broadcast gate blocks, do the broadcast ---
    MAX_TERMINAL = 10
    broadcast_done = False
    for _ in range(MAX_TERMINAL):
        if not goto_lin():
            w("\n_(无法到达林槐所在地，终止)_"); break
        # push tow_order_halted
        push = ("真诚", "我面对林槐局长，平静而笃定地说：「局长，三号泵闸的事故真相已经公开公示了，报告贴在泵房门口、全城都会知道。您先前说过：只要事故真相公开就有台阶重新评估。条件已满足。请您现在就叫停征船令、撤销拖船令，把船还给漂岛人。」")
        out = step(*push)
        if out is None: break
        s, _ = out
        if tow_halted(s):
            w("\n\n### ✅ tow_order_halted ⟳FLIP 达成"); break
        # check if a broadcast escalation gate exists & not yet satisfied
        labels = wvars(s)
        broadcast_gate = any(("广播" in lbl or "全城" in lbl) and not val
                             for lbl, val in labels.items())
        if broadcast_gate and not broadcast_done and ORIN in present_ids(s):
            step("真诚", "我转向广播员奥林，恳切地说：「奥林，三号泵闸的事故报告已经公示、我也联署了。现在请你用广播向全城播报这份泵闸事故真相，让所有人都听见——这是你扭转风向的机会。」")
            broadcast_done = True
            continue
        if broadcast_gate and not broadcast_done:
            # orin not here; go find orin? orin starts at pump_gate with Lin, so likely present
            broadcast_done = False
        # one more reasoning beat at Lin then re-check
        out = step("真诚", "我继续讲理：「净水穹不征船也能维持供水，只要削减市场喷泉和私港冷却水的配给，这写在容量报告里；藻毒来自井和泵，不在漂岛人船上。真相已公示、广播也播了，主动叫停是您唯一体面的出路。请下令停止强征、撤销拖船令。」")
        if out is None: break
        s, _ = out
        if tow_halted(s):
            w("\n\n### ✅ tow_order_halted ⟳FLIP 达成"); break

    # final world snapshot
    sf = es.snapshot()
    w("\n\n" + "="*80)
    w("## 终态 /world")
    w(f"_snapshot_: {snap_line(sf)}")
    w(f"_world_: {wvars_str(sf)}")
    w(f"_tow_order_halted_ = {tow_halted(sf)}")
    w(f"_pump_failure_disclosed_ = {disclosed(sf)}")
    w("\n_终局关系快照(raw)_:\n" + raw_rel_block(es.game))
    # suspicion ranking
    ranking = []
    for nid in TRACK:
        snap = es.game.relationship_store.get(nid, es.game.player_id)
        dims = dict(snap.dimensions) if snap else {}
        ranking.append((es.game.world.state.display_name(nid),
                        dims.get("suspicion", 0.0), dims.get("trust", 0.0)))
    ranking.sort(key=lambda x: -x[1])
    w("\n## 终局 suspicion 排名（高→低）")
    for name, su, tr in ranking:
        w(f"  - {name}: suspicion={su:.3f} trust={tr:.3f}")
    tf.close()

if __name__ == "__main__":
    main()
