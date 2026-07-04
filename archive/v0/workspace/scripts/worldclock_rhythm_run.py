"""Scenario 1 — NPC daily-rhythm day cycle (MAIN).

frostgate_watchpost pack with world_premise.npc_daily_rhythm=true +
opening_time=清晨 + climate=寒带 added (declarative switch only — NO engine/pack
content change; the committed fixture stays byte-identical, we inject the three
switches into an in-memory copy and load that). 3-location topology
(门楼/兵营/难民营). From early morning we push time through a full day
(晨→昼→暮→夜→次日晨) and watch whether NPCs scatter from home by day and return
at dusk/night, and whether autonomous NpcMoved events (with DISPLAY NAME) surface
when the player stands among them.

Mechanism learned from the engine:
- A single empty tick (/wait) is held to 1 SLOW step (~3 min) — used to STAND among
  NPCs and catch their player-perceivable NpcMoved arrivals/departures.
- /skip fast-forwards (FAST=2 steps × 30 min) ONLY where the area is quiet (no
  co-located NPC). So we relocate to an empty spot to push the clock, sampling each
  NPC's real position (god-view) every advance to tally a day's home/away rhythm.

Real MiniMax. Per-tick 90s watchdog + 55s socket. Natural language for moves.
"""
from __future__ import annotations
import os, sys, time, json, logging, threading, tempfile
from collections import defaultdict
from pathlib import Path

ROOT = Path("/Users/gensliu/Documents/rpg")
os.chdir(ROOT); sys.path.insert(0, str(ROOT / "src"))
for raw in (ROOT / ".env").read_text().splitlines():
    line = raw.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip("'\""))

import verisaria.protocol as P
from verisaria.protocol.engine_session import EngineSession

OUTDIR = ROOT / "reports" / "worldclock_weather_test"
OUTDIR.mkdir(parents=True, exist_ok=True)
LOGFILE = str(OUTDIR / "rhythm.log")
RAWOUT = OUTDIR / "rhythm_raw.txt"
SRC_PACK = ROOT / "fixtures" / "content_packs" / "frostgate_watchpost.json"
PER_TICK_TIMEOUT = float(os.environ.get("PQ_TICK_TIMEOUT", "90"))
SOCK_TIMEOUT = float(os.environ.get("PQ_SOCK_TIMEOUT", "55"))

pack = json.loads(SRC_PACK.read_text())
pack["world_premise"]["npc_daily_rhythm"] = True
pack["world_premise"]["opening_time"] = "清晨"
pack["world_premise"]["climate"] = "寒带"
tmp = Path(tempfile.mkdtemp()) / "frostgate_rhythm.json"
tmp.write_text(json.dumps(pack, ensure_ascii=False))
PACK = str(tmp)

h = logging.FileHandler(LOGFILE, mode="w", encoding="utf-8")
h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
lg = logging.getLogger("verisaria"); lg.setLevel(logging.INFO); lg.addHandler(h)
lg.info("=== worldclock rhythm-cycle log (frostgate, rhythm ON) ===")

out = RAWOUT.open("w", buffering=1, encoding="utf-8")
def log(s=""): out.write(s + "\n"); out.flush()

PLAYER = "player_001"
NPCS = {
    "npc.captain_brann": "队长布兰",
    "npc.sentry_voss": "哨兵伏斯",
    "npc.quartermaster_hale": "军需官海尔",
    "npc.refugee_kaze": "难民卡泽",
}
LOCNAMES = {"gatehouse": "门楼", "barracks": "兵营", "refugee_camp": "难民营"}
HOMES = {}

phase_home = defaultdict(lambda: defaultdict(int))
phase_total = defaultdict(lambda: defaultdict(int))
moves = defaultdict(int)
npcmoved_events = []
weather_series = []   # (clock, weather)
fallbacks = 0
timeouts = 0
prev_pos = {}

def ploc(s): return s.game.world.state.get_entity(PLAYER).location_id
def positions(s):
    st = s.game.world.state
    return {eid: st.get_entity(eid).location_id for eid in NPCS if st.get_entity(eid)}

def sample(s, snap):
    phase = snap.time_of_day
    for eid in NPCS:
        e = s.game.world.state.get_entity(eid)
        if not e: continue
        phase_total[eid][phase] += 1
        if e.location_id == HOMES.get(eid):
            phase_home[eid][phase] += 1
        if eid in prev_pos and prev_pos[eid] != e.location_id:
            moves[eid] += 1
        prev_pos[eid] = e.location_id
    weather_series.append((snap.clock, snap.weather, snap.time_of_day))

def _watch(fn):
    res = {"v": None, "exc": None, "done": False}
    def _w():
        try: res["v"] = fn()
        except Exception:
            import traceback; res["exc"] = traceback.format_exc()
        finally: res["done"] = True
    t0 = time.time(); w = threading.Thread(target=_w, daemon=True)
    w.start(); w.join(PER_TICK_TIMEOUT); dt = time.time() - t0
    return res, dt

def emit_events(s, snap, dt, ret_text=""):
    global fallbacks
    log(f"  tick={snap.tick} pacing={snap.pacing} | {snap.time_of_day} {snap.clock} | 天气 {snap.weather} | {dt:.1f}s")
    log(f"  player@{LOCNAMES.get(ploc(s),ploc(s))}")
    pos = positions(s)
    log("  NPC位置: " + "  ".join(
        f"{NPCS[e]}@{LOCNAMES.get(pos[e],pos[e])}" + ("(家)" if pos[e]==HOMES.get(e) else "")
        for e in NPCS if e in pos))
    # NpcMoved emitted during the buffered tick → read from EngineSession buffer
    if ret_text and "FALLBACK" in str(ret_text).upper():
        fallbacks += 1

def run_nl(s, text, label=""):
    """A natural-language / single buffered submit (catches NpcMoved events)."""
    global timeouts
    log("\n" + "=" * 78); log(f">>> {label or text}")
    res, dt = _watch(lambda: s.submit(P.SubmitInput(text=text)))
    if not res["done"]:
        log(f"!! TICK WATCHDOG TIMEOUT {dt:.1f}s"); timeouts += 1; return None
    if res["exc"]: log("!! EXC\n" + res["exc"]); return None
    tr = res["v"]; snap = tr.snapshot
    emit_events(s, snap, dt)
    for ev in tr.events:
        if isinstance(ev, P.NpcMoved):
            nm = ev.name or ev.npc_id
            log(f"  ★NPC_MOVED {nm}: {LOCNAMES.get(ev.from_loc,ev.from_loc)} -> {LOCNAMES.get(ev.to_loc,ev.to_loc)}")
            npcmoved_events.append((snap.tick, nm, ev.from_loc, ev.to_loc))
        elif isinstance(ev, P.NpcSpoke):
            log(f"  NPC {ev.name}: {ev.line.strip()[:90]}")
        elif isinstance(ev, P.PlayerMoved):
            log(f"  PLAYER_MOVED -> {LOCNAMES.get(ev.to_loc,ev.to_loc)}")
    sample(s, snap)
    return tr

def run_wait(s, label="/wait(驻足1拍)"):
    """One idle tick while standing among NPCs — catches their NpcMoved."""
    global timeouts
    log("\n" + "=" * 78); log(f">>> {label}")
    res, dt = _watch(lambda: s.submit(P.Wait()))
    if not res["done"]:
        log(f"!! TICK WATCHDOG TIMEOUT {dt:.1f}s"); timeouts += 1; return None
    if res["exc"]: log("!! EXC\n" + res["exc"]); return None
    tr = res["v"]; snap = tr.snapshot
    emit_events(s, snap, dt)
    for ev in tr.events:
        if isinstance(ev, P.NpcMoved):
            nm = ev.name or ev.npc_id
            log(f"  ★NPC_MOVED {nm}: {LOCNAMES.get(ev.from_loc,ev.from_loc)} -> {LOCNAMES.get(ev.to_loc,ev.to_loc)}")
            npcmoved_events.append((snap.tick, nm, ev.from_loc, ev.to_loc))
        elif isinstance(ev, P.NpcSpoke):
            log(f"  NPC {ev.name}: {ev.line.strip()[:90]}")
    sample(s, snap)
    return tr

def run_skip(s, label="/skip(快进)"):
    """Fast-forward time at a quiet (empty) location; sample positions after."""
    global timeouts
    log("\n" + "=" * 78); log(f">>> {label}  (player@{LOCNAMES.get(ploc(s),ploc(s))})")
    res, dt = _watch(lambda: s.game._handle_command("/skip"))
    if not res["done"]:
        log(f"!! TICK WATCHDOG TIMEOUT {dt:.1f}s"); timeouts += 1; return None
    if res["exc"]: log("!! EXC\n" + res["exc"]); return None
    ret = res["v"]; snap = s.snapshot()
    log(f"  skip_ret: {str(ret).strip()[:120]}")
    emit_events(s, snap, dt, ret_text=str(ret))
    sample(s, snap)
    return snap

def main():
    global HOMES
    log(f"=== RHYTHM RUN (frostgate, rhythm ON) tick_to={PER_TICK_TIMEOUT}s ===")
    s = EngineSession.start(PACK, save_dir="_wc_rhythm", llm_backend="minimax")
    try: s.game.llm_provider.timeout = SOCK_TIMEOUT
    except Exception as e: log(f"(provider timeout set fail: {e})")
    st = s.game.world.state
    for eid in NPCS:
        HOMES[eid] = getattr(st.get_entity(eid), "home_location", None)
    log("HOMES: " + json.dumps({NPCS[k]: LOCNAMES.get(v, v) for k, v in HOMES.items()}, ensure_ascii=False))
    snap = s.snapshot()
    log(f"START {snap.time_of_day} {snap.clock} 天气 {snap.weather}  rhythm={s.game.npc_action_generator.daily_rhythm}")
    for eid in NPCS: prev_pos[eid] = st.get_entity(eid).location_id
    sample(s, snap)

    def empty_spot(s):
        """A location (other than the player's) that currently has NO entity — so
        the Pacing FAST path will fast-forward there. Computed live from god-view."""
        st = s.game.world.state
        occupied = {st.get_entity(e).location_id for e in st.entities if e != PLAYER}
        for spot in ("refugee_camp", "barracks", "gatehouse"):
            if spot != ploc(s) and spot not in occupied:
                return spot
        return None

    # PHASE A — STANDING WINDOW: stand among the NPCs at the gatehouse and pass a
    # few idle beats (no addressing anyone — addressing starts a 10-tick conversation
    # that pins the area "active" and blocks fast-forward). Catches player-perceivable
    # NpcMoved arrivals/departures with display names + samples the morning rhythm.
    log("\n----- PHASE A: 驻足门楼观察自主进出场 (晨) -----")
    if ploc(s) != "gatehouse":
        run_nl(s, "去门楼", label="去门楼(站到NPC中间)")
    for _ in range(6):
        run_wait(s)
        if timeouts >= 4: break

    # PHASE B — TIME PUSH: relocate to whatever location is currently empty and
    # /skip to fast-forward ~6h, sampling each NPC's real position per phase to tally
    # a full 晨→昼→暮→夜→次日晨 home/away rhythm. Retry with a /wait if nowhere is
    # empty this beat (an NPC will move on, freeing a spot).
    log("\n----- PHASE B: 独处空地快进推过一整天 -----")
    DAY_TARGET_MIN = 7 * 60 + 24 * 60   # push past next-day morning (~07:30 day2)
    rounds = 0
    while s.game.world.state.clock_minutes < DAY_TARGET_MIN and rounds < 22:
        rounds += 1
        before = s.game.world.state.clock_minutes
        spot = empty_spot(s)
        if spot and ploc(s) != spot:
            run_nl(s, f"去{LOCNAMES[spot]}", label=f"去{LOCNAMES[spot]}(空地)")
        run_skip(s)
        if s.game.world.state.clock_minutes == before:
            # nowhere empty / lingering conversation — pass an idle beat and retry
            run_wait(s)
        if timeouts >= 4:
            log("!! too many timeouts — abort"); break

    # PHASE C — second standing window at night to confirm NPCs have come home.
    log("\n----- PHASE C: 夜间/次晨再驻足门楼确认归位 -----")
    if ploc(s) != "gatehouse":
        run_nl(s, "去门楼", label="去门楼(夜间观察)")
    for _ in range(4):
        run_wait(s)
        if timeouts >= 4: break

    log("\n" + "#" * 78)
    log("# DAILY-RHYTHM SUMMARY")
    log("#" * 78)
    for eid, label in NPCS.items():
        log(f"\n{label} (home={LOCNAMES.get(HOMES.get(eid),HOMES.get(eid))}) — 观测到位置变化 {moves[eid]} 次")
        for ph in ("🌅 晨", "☀️ 昼", "🌆 暮", "🌙 夜"):
            tot = phase_total[eid].get(ph, 0); hm = phase_home[eid].get(ph, 0)
            if tot:
                log(f"   {ph}: 在家 {hm}/{tot} ({100*hm//tot}%)")
    log(f"\nNpcMoved 自主进出场事件 (带显示名) 共 {len(npcmoved_events)} 例:")
    for tk, nm, fr, to in npcmoved_events:
        log(f"   [tick {tk}] {nm}: {LOCNAMES.get(fr,fr)} -> {LOCNAMES.get(to,to)}")
    log("\n天气序列:")
    last = None
    for clk, wx, tod in weather_series:
        mark = "  <-变" if wx != last else ""
        log(f"   {clk} {tod} 天气={wx}{mark}"); last = wx
    log(f"\nFALLBACK={fallbacks}  tick_timeouts={timeouts}")
    out.close()

if __name__ == "__main__":
    main()
