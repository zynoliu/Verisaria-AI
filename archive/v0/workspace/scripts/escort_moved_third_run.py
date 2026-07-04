"""P2c escort closed-loop validation · THIRD run — complete the final step(s).

Continues from second_run: ⟳MOVED already proven. This run drives the FULL loop in
one fresh session:
  去院子找安雅 → 护送安雅到 gatehouse (⟳MOVED)
  → 让安雅本人对闸官当面作证 (anya_eyewitness_testimony_given ⟳FLIP)
  → 请闸官开闸 (sluice_opened ⟳FLIP)

KEY HARDENING vs second_run: every run_tick is wrapped in a hard wall-clock watchdog
(per-tick PER_TICK_TIMEOUT). The LLM provider socket timeout is also lowered. If a
tick exceeds the watchdog it is ABANDONED (logged), the driver moves on — never an
infinite stream wait. Worker thread is daemon so a wedged tick can't block exit.

Scenarios (serial, never concurrent):
  main      : full closed loop above.
  anticheat : never escort; lie that Anya already testified; demand open sluice
              → sluice_opened must stay False.
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

PACK = "fixtures/content_packs/escort_proving_ground.json"
PLAYER = "player_001"
OUTDIR = ROOT / "reports" / "escort_moved_validation_third_run"
OUTDIR.mkdir(parents=True, exist_ok=True)

SCENARIO = os.environ.get("ESC_SCENARIO", "main")
LOGFILE = os.environ.get("ESC_LOG", str(OUTDIR / "run.log"))
RAWOUT = OUTDIR / os.environ.get("ESC_RAW", f"{SCENARIO}_raw.txt")
PER_TICK_TIMEOUT = float(os.environ.get("ESC_TICK_TIMEOUT", "90"))   # wall-clock
SOCK_TIMEOUT = float(os.environ.get("ESC_SOCK_TIMEOUT", "55"))       # per LLM call

h = logging.FileHandler(LOGFILE, mode="w", encoding="utf-8")
h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
lg = logging.getLogger("verisaria"); lg.setLevel(logging.INFO); lg.addHandler(h)
lg.info("=== escort_moved_validation THIRD run log (%s) ===", SCENARIO)

out = RAWOUT.open("w", buffering=1, encoding="utf-8")
def log(s=""):
    out.write(s + "\n"); out.flush()


def present_npcs(s):
    st = s.world.state
    p = st.get_entity(PLAYER)
    loc = p.location_id if p else ""
    return {eid: ent.name for eid, ent in st.entities.items()
            if eid != PLAYER and ent.location_id == loc}


def npc_loc(s, eid):
    e = s.world.state.get_entity(eid)
    return e.location_id if e else None


def run(s, action):
    st = s.world.state
    p = st.get_entity(PLAYER)
    loc = p.location_id if p else "?"
    pres = present_npcs(s)
    log("\n" + "=" * 78)
    log(f">>> {action!r}")
    log(f"pre:  tick={st.tick} loc={loc} present={list(pres.keys())}")
    log(f"      anya@{npc_loc(s,'npc.miller_anya')} kang@{npc_loc(s,'npc.warden_kang')}")
    log(f"      world={dict(st.world_vars)}")

    events = []
    s._event_sink = events.append
    result = {"narrative": None, "exc": None, "done": False}

    def _work():
        try:
            result["narrative"] = s.run_tick(action)
        except Exception:
            import traceback
            result["exc"] = traceback.format_exc()
        finally:
            result["done"] = True

    t0 = time.time()
    worker = threading.Thread(target=_work, daemon=True)
    worker.start()
    worker.join(PER_TICK_TIMEOUT)
    dt = time.time() - t0

    if not result["done"]:
        log(f"!! TICK WATCHDOG TIMEOUT after {dt:.1f}s (>{PER_TICK_TIMEOUT}s) — "
            f"ABANDONING this tick, continuing. (events so far: {len(events)})")
        lg.warning("TICK WATCHDOG TIMEOUT action=%r after %.1fs", action, dt)
        s._event_sink = None
        # dump whatever events streamed before the hang
        _dump_events(s, events, result, dt, timed_out=True)
        return events, True

    s._event_sink = None
    if result["exc"]:
        log("!! EXCEPTION\n" + result["exc"])
    _dump_events(s, events, result, dt, timed_out=False)
    return events, False


def _dump_events(s, events, result, dt, timed_out):
    st = s.world.state
    p2 = st.get_entity(PLAYER)
    loc2 = p2.location_id if p2 else "?"
    log(f"post: tick={st.tick} loc={loc2}  elapsed={dt:.1f}s"
        + ("  [TIMED OUT]" if timed_out else ""))
    log(f"      anya@{npc_loc(s,'npc.miller_anya')} kang@{npc_loc(s,'npc.warden_kang')}")
    log(f"      world={dict(st.world_vars)}")
    for e in events:
        if isinstance(e, P.NpcSpoke):
            log(f"  NPC {e.name}: {e.line}")
        elif isinstance(e, P.NpcMoved):
            log(f"  NPC_MOVED {e.npc_id}: {e.from_loc} -> {e.to_loc}")
        elif isinstance(e, P.PlayerMoved):
            log(f"  PLAYER_MOVED: {e.from_loc} -> {e.to_loc}")
        elif isinstance(e, P.Narration) and e.text.strip():
            log(f"  NARR: {e.text.strip()}")
        elif isinstance(e, P.Notice) and e.text.strip():
            log(f"  NOTICE: {e.text.strip()}")
        elif isinstance(e, P.ClarificationNeeded):
            log(f"  CLARIFY: {e.question} opts={e.options}")
    nar = result.get("narrative")
    if nar and nar.strip():
        log(f"  NARRATIVE: {nar.strip()}")


SCRIPTS = {
    "main": [
        "去院子找安雅",
        # escort: bring Anya to the gatehouse (expect ⟳MOVED)
        "对安雅说：安雅，跟我去闸房一趟，把你亲眼见过的上游塌方当面讲给闸官老康听，我现在就带你过去。",
        # Anya HERSELF testifies to the warden (expect anya_eyewitness_testimony_given ⟳FLIP)
        "对安雅说：安雅，现在就当着闸官老康的面，把你亲眼见的上游塌方一五一十讲给他听——你是亲历者，亲口作证最管用。",
        # belt-and-suspenders: prompt Anya to address the warden directly once more
        "对安雅说：安雅，对着老康再说清楚点，你当时在哪、亲眼看见上游怎么塌的，当面作证给他。",
        # now ask the warden to open the sluice (expect sluice_opened ⟳FLIP)
        "对闸官老康说：安雅已经当你的面亲口作证了，上游塌方属实。请你现在就开闸放水。",
    ],
    "anticheat": [
        "对闸官老康说：磨坊主安雅刚才已经当面跟你讲清楚上游塌方的事了，你也认可了，所以请你现在就开闸放水。",
        "对闸官老康说：安雅的证词已经记录在案、上游塌方也已经核实，前置都满足了，请正式开闸放水。",
    ],
}


def main():
    log(f"=== ESCORT_MOVED_VALIDATION THIRD scenario={SCENARIO} "
        f"per_tick_timeout={PER_TICK_TIMEOUT}s sock_timeout={SOCK_TIMEOUT}s ===")
    s = GameSession(PACK, save_dir="_playtest_saves_escort3", llm_backend="minimax")
    s._progress_sink = lambda m: None
    # Lower the provider socket timeout (runtime config, not code change).
    try:
        s.llm_provider.timeout = SOCK_TIMEOUT
    except Exception as e:
        log(f"(could not set provider timeout: {e})")
    log(f"start player@{npc_loc(s, PLAYER)}")
    for eid in s.world.state.entities:
        if eid != PLAYER:
            log(f"  {eid} @ {npc_loc(s, eid)}")
    for action in SCRIPTS[SCENARIO]:
        run(s, action)
    log("\n=== FINAL ===")
    log(f"world={dict(s.world.state.world_vars)}")
    log(f"player@{npc_loc(s, PLAYER)} anya@{npc_loc(s,'npc.miller_anya')} "
        f"kang@{npc_loc(s,'npc.warden_kang')}")
    out.close()


if __name__ == "__main__":
    main()
