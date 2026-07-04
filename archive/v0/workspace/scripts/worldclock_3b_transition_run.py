"""slice 3b · 第二跑 (part 2) — capture the ambient TIME/WEATHER transition Narration.

The main run (worldclock_3b_immersion_run.py) proved the NPC catches the snow/night
in dialogue, but in frostgate's 3-loc topology every location has a resident NPC, so
the FAST /skip path ("周围并不安全" gate) never fired and the clock never crossed a
time-of-day boundary — so no time/weather transition line surfaced.

This focused run opens at 黄昏 (暮, 18:00) — only ~2h to the 夜 boundary (20:00) — and
turns on npc_daily_rhythm so NPCs disperse and transiently free a location for the
FAST /skip. We loop: relocate to whatever's currently empty (god-view) → /skip → fall
back to a /wait if nothing's empty this beat — until the clock crosses 暮→夜 (and we
keep going to try to catch a weather change too), collecting every Narration VERBATIM.
This reuses the proven phase-B logic from scripts/worldclock_rhythm_run.py.

Declarative world_premise switches only (climate/opening_weather/opening_time/
npc_daily_rhythm). NO engine/other-pack change. Real MiniMax, 90s/55s watchdogs.
"""
from __future__ import annotations
import os, sys, time, json, logging, threading, tempfile
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

OUTDIR = ROOT / "reports" / "worldclock_weather_test_second_run"
OUTDIR.mkdir(parents=True, exist_ok=True)
RAWOUT = OUTDIR / "transition_raw.txt"
SRC_PACK = ROOT / "fixtures" / "content_packs" / "frostgate_watchpost.json"
PER_TICK_TIMEOUT = float(os.environ.get("PQ_TICK_TIMEOUT", "90"))
SOCK_TIMEOUT = float(os.environ.get("PQ_SOCK_TIMEOUT", "55"))

pack = json.loads(SRC_PACK.read_text())
pack["world_premise"]["climate"] = "寒带"
pack["world_premise"]["opening_weather"] = "雪"
pack["world_premise"]["opening_time"] = "19:30"         # 暮, ~30min to 夜(20:00)
pack["world_premise"]["npc_daily_rhythm"] = True         # disperse NPCs → free a loc
tmp = Path(tempfile.mkdtemp()) / "frostgate_3b_tr.json"
tmp.write_text(json.dumps(pack, ensure_ascii=False))
PACK = str(tmp)

h = logging.FileHandler(str(OUTDIR / "transition.log"), mode="w", encoding="utf-8")
h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
lg = logging.getLogger("verisaria"); lg.setLevel(logging.INFO); lg.addHandler(h)

out = RAWOUT.open("w", buffering=1, encoding="utf-8")
def log(s=""): out.write(s + "\n"); out.flush()

PLAYER = "player_001"
LOCNAMES = {"gatehouse": "门楼", "barracks": "兵营", "refugee_camp": "难民营"}
transition_narr = []   # (tick, text) — only the time/weather ambient lines
all_narr = []
timeouts = 0
fallbacks = 0

def ploc(s): return s.game.world.state.get_entity(PLAYER).location_id

TIME_WX_MARKERS = ("天色", "天黑", "夜幕", "入夜", "天亮", "天蒙蒙", "日头",
                   "到了白天", "天气变了", "向晚")

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

def note_narr(tick, text):
    text = text.strip()
    all_narr.append((tick, text))
    is_tw = any(m in text for m in TIME_WX_MARKERS)
    tag = "  ⏱☁ TIME/WX TRANSITION" if is_tw else "  ☁ narration"
    log(f"{tag}: {text}")
    if is_tw:
        transition_narr.append((tick, text))

def empty_spot(s):
    st = s.game.world.state
    occupied = {st.get_entity(e).location_id for e in st.entities if e != PLAYER}
    for spot in ("refugee_camp", "barracks", "gatehouse"):
        if spot != ploc(s) and spot not in occupied:
            return spot
    return None

def run_nl(s, text, label=""):
    global timeouts
    log("\n" + "=" * 70); log(f">>> {label or text}")
    res, dt = _watch(lambda: s.submit(P.SubmitInput(text=text)))
    if not res["done"]:
        log(f"!! TIMEOUT {dt:.1f}s"); timeouts += 1; return None
    if res["exc"]: log("!! EXC\n" + res["exc"]); return None
    tr = res["v"]; snap = tr.snapshot
    log(f"  {snap.time_of_day} {snap.clock} 天气 {snap.weather} | player@{LOCNAMES.get(ploc(s),ploc(s))} | {dt:.1f}s")
    for ev in tr.events:
        if isinstance(ev, P.Narration): note_narr(snap.tick, ev.text)
        elif isinstance(ev, P.NpcMoved):
            log(f"  ★NPC_MOVED {ev.name or ev.npc_id}: {LOCNAMES.get(ev.from_loc,ev.from_loc)} -> {LOCNAMES.get(ev.to_loc,ev.to_loc)}")
    return tr

def run_wait(s):
    global timeouts
    log("\n" + "=" * 70); log(">>> /wait")
    res, dt = _watch(lambda: s.submit(P.Wait()))
    if not res["done"]:
        log(f"!! TIMEOUT {dt:.1f}s"); timeouts += 1; return None
    if res["exc"]: log("!! EXC\n" + res["exc"]); return None
    tr = res["v"]; snap = tr.snapshot
    log(f"  {snap.time_of_day} {snap.clock} 天气 {snap.weather} | player@{LOCNAMES.get(ploc(s),ploc(s))} | {dt:.1f}s")
    for ev in tr.events:
        if isinstance(ev, P.Narration): note_narr(snap.tick, ev.text)
        elif isinstance(ev, P.NpcMoved):
            log(f"  ★NPC_MOVED {ev.name or ev.npc_id}: {LOCNAMES.get(ev.from_loc,ev.from_loc)} -> {LOCNAMES.get(ev.to_loc,ev.to_loc)}")
    return tr

def run_skip(s):
    global timeouts
    phase_b = s.snapshot().time_of_day; wx_b = s.snapshot().weather
    log("\n" + "=" * 70); log(f">>> /skip (player@{LOCNAMES.get(ploc(s),ploc(s))})")
    s._buffer.clear()
    res, dt = _watch(lambda: s.game._handle_command("/skip"))
    if not res["done"]:
        log(f"!! TIMEOUT {dt:.1f}s"); timeouts += 1; return None
    if res["exc"]: log("!! EXC\n" + res["exc"]); return None
    ret = res["v"]; snap = s.snapshot()
    evs = list(s._buffer); s._buffer.clear()
    log(f"  skip_ret: {str(ret).strip()[:90]}")
    log(f"  {snap.time_of_day} {snap.clock} 天气 {snap.weather} | "
        f"phase {phase_b}->{snap.time_of_day} wx {wx_b}->{snap.weather} | {dt:.1f}s")
    for ev in evs:
        if isinstance(ev, P.Narration): note_narr(snap.tick, ev.text)
        elif isinstance(ev, P.NpcMoved):
            log(f"  ★NPC_MOVED {ev.name or ev.npc_id}: {LOCNAMES.get(ev.from_loc,ev.from_loc)} -> {LOCNAMES.get(ev.to_loc,ev.to_loc)}")
    return snap

def main():
    log(f"=== 3b TRANSITION RUN (frostgate 寒带/雪/黄昏, rhythm ON) ===")
    s = EngineSession.start(PACK, save_dir="_wc_3b_tr", llm_backend="minimax")
    try: s.game.llm_provider.timeout = SOCK_TIMEOUT
    except Exception as e: log(f"(provider timeout set fail: {e})")
    snap = s.snapshot()
    log(f"START {snap.time_of_day} {snap.clock} 天气 {snap.weather} "
        f"(clock_minutes={s.game.world.state.clock_minutes}, rhythm={s.game.npc_action_generator.daily_rhythm})")

    start_phase = snap.time_of_day
    start_wx = s.game.world.state.weather
    rounds = 0
    crossed_phase = False
    crossed_wx = False
    # IMPORTANT: the ambient time/weather transition Narration is emitted by
    # run_tick (→ _emit_environment_transition), which is the /wait (Wait) and
    # natural-input path — NOT /skip's _handle_skip fast-forward loop. So we cross
    # the boundary with Wait() from an EMPTY spot (alone+quiet → pacing goes FAST,
    # so a single Wait can jump ~1h and cross 暮→夜), capturing the line. We relocate
    # to whatever's empty each round (rhythm ON disperses NPCs, freeing a loc).
    while rounds < 40 and not (crossed_phase and crossed_wx):
        rounds += 1
        spot = empty_spot(s)
        if spot and ploc(s) != spot:
            run_nl(s, f"我走到{LOCNAMES[spot]}。", label=f"去{LOCNAMES[spot]}(空地)")
        # one idle beat — when alone+quiet this fast-forwards and may cross a boundary
        run_wait(s)
        cur_phase = s.snapshot().time_of_day
        cur_wx = s.game.world.state.weather
        if cur_phase != start_phase: crossed_phase = True
        if cur_wx != start_wx: crossed_wx = True
        if s.game.world.state.clock_minutes >= 30 * 60:  # safety: ~day2 06:00
            break
        if timeouts >= 4:
            log("!! too many timeouts — abort"); break

    log("\n" + "#" * 70); log("# SUMMARY")
    log(f"start: {start_phase}/{start_wx}  ->  end: {s.snapshot().time_of_day}/{s.game.world.state.weather}")
    log(f"crossed_phase={crossed_phase}  crossed_weather={crossed_wx}")
    log(f"\n⏱☁ TIME/WEATHER TRANSITION Narration (共 {len(transition_narr)} 条):")
    for tk, tx in transition_narr:
        log(f"   [t{tk}] {tx}")
    log(f"\n所有 Narration (共 {len(all_narr)} 条，含NPC动作):")
    for tk, tx in all_narr:
        log(f"   [t{tk}] {tx}")
    log(f"\nFALLBACK={fallbacks}  tick_timeouts={timeouts}")
    out.close()
    print(f"DONE transitions={len(transition_narr)} crossed_phase={crossed_phase} "
          f"crossed_wx={crossed_wx} timeouts={timeouts}")

if __name__ == "__main__":
    main()
