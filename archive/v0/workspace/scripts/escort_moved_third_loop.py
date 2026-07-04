"""P2c escort closed-loop · THIRD run, adaptive driver.

Fixes the first attempt's misalignment: escort willingness is stochastic, so we
RETRY the escort with warm low-pressure phrasing until Anya is actually co-located
with the warden (location == gatehouse == ⟳MOVED), only THEN proceed to: Anya
testifies in person → (anya_eyewitness_testimony_given ⟳FLIP) → ask warden to open
sluice → (sluice_opened ⟳FLIP). Every tick is watchdog-protected (no infinite stream).

Only escort-phrased actions ("跟我去/带你过去") trigger movement adjudication; plain
"对X说" lines are dialogue and never move anyone — that was the prior bug.
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
ANYA = "npc.miller_anya"
KANG = "npc.warden_kang"
OUTDIR = ROOT / "reports" / "escort_moved_validation_third_run"
OUTDIR.mkdir(parents=True, exist_ok=True)

LOGFILE = str(OUTDIR / "run.log")
RAWOUT = OUTDIR / "main_raw.txt"
PER_TICK_TIMEOUT = float(os.environ.get("ESC_TICK_TIMEOUT", "90"))
SOCK_TIMEOUT = float(os.environ.get("ESC_SOCK_TIMEOUT", "55"))
MAX_ESCORT_TRIES = int(os.environ.get("ESC_MAX_TRIES", "5"))

h = logging.FileHandler(LOGFILE, mode="w", encoding="utf-8")
h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
lg = logging.getLogger("verisaria"); lg.setLevel(logging.INFO); lg.addHandler(h)
lg.info("=== escort_moved THIRD adaptive run log ===")

out = RAWOUT.open("w", buffering=1, encoding="utf-8")
def log(s=""):
    out.write(s + "\n"); out.flush()

def loc(s, eid):
    e = s.world.state.get_entity(eid)
    return e.location_id if e else None

def present(s):
    st = s.world.state; p = st.get_entity(PLAYER)
    l = p.location_id if p else ""
    return [eid for eid, e in st.entities.items() if eid != PLAYER and e.location_id == l]

def run(s, action):
    st = s.world.state
    log("\n" + "=" * 78)
    log(f">>> {action!r}")
    log(f"pre:  tick={st.tick} player@{loc(s,PLAYER)} present={present(s)} "
        f"anya@{loc(s,ANYA)} kang@{loc(s,KANG)} world={dict(st.world_vars)}")
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
    w = threading.Thread(target=_work, daemon=True); w.start(); w.join(PER_TICK_TIMEOUT)
    dt = time.time() - t0
    if not result["done"]:
        log(f"!! TICK WATCHDOG TIMEOUT after {dt:.1f}s (>{PER_TICK_TIMEOUT}s) — ABANDON, continue.")
        lg.warning("TICK WATCHDOG TIMEOUT action=%r after %.1fs", action, dt)
        s._event_sink = None
        return events, True
    s._event_sink = None
    if result["exc"]:
        log("!! EXCEPTION\n" + result["exc"])
    st = s.world.state
    log(f"post: tick={st.tick} player@{loc(s,PLAYER)} anya@{loc(s,ANYA)} "
        f"kang@{loc(s,KANG)} world={dict(st.world_vars)} elapsed={dt:.1f}s")
    for e in events:
        if isinstance(e, P.NpcSpoke):       log(f"  NPC {e.name}: {e.line}")
        elif isinstance(e, P.NpcMoved):     log(f"  NPC_MOVED {e.npc_id}: {e.from_loc} -> {e.to_loc}")
        elif isinstance(e, P.PlayerMoved):  log(f"  PLAYER_MOVED: {e.from_loc} -> {e.to_loc}")
        elif isinstance(e, P.Narration) and e.text.strip():  log(f"  NARR: {e.text.strip()}")
        elif isinstance(e, P.Notice) and e.text.strip():     log(f"  NOTICE: {e.text.strip()}")
        elif isinstance(e, P.ClarificationNeeded):           log(f"  CLARIFY: {e.question}")
    if result.get("narrative") and result["narrative"].strip():
        log(f"  NARRATIVE: {result['narrative'].strip()}")
    return events, False


ESCORT_LINES = [
    "对安雅说：安雅，就在隔壁闸房几步路，你亲口跟老康讲最有用，我陪你一起走，磨坊我帮你盯着。咱们现在就过去，走吧！",
    "对安雅说：来嘛安雅，跟我去闸房一趟，当面把上游塌方讲给老康，开了闸你磨坊立马有水。我这就带你过去，走！",
    "对安雅说：安雅别犹豫了，麦子我替你看着，你先跟我去闸房把话说了，几步路的事，走吧我带你去。",
    "对安雅说：水今天就能来，全靠你这趟。跟我走，到闸房当面跟老康讲清楚，我陪着你。现在就去！",
    "对安雅说：安雅，你不是一直盼着放水么？跟我去闸房一趟，你亲眼见的当面讲给老康，这就走。",
]

def testimony_done(s):
    return bool(s.world.state.world_vars.get("anya_eyewitness_testimony_given"))


def main():
    log(f"=== THIRD adaptive: per_tick_timeout={PER_TICK_TIMEOUT}s sock={SOCK_TIMEOUT}s "
        f"max_escort_tries={MAX_ESCORT_TRIES} ===")
    s = GameSession(PACK, save_dir="_playtest_saves_escort3b", llm_backend="minimax")
    s._progress_sink = lambda m: None
    try: s.llm_provider.timeout = SOCK_TIMEOUT
    except Exception as e: log(f"(set timeout failed: {e})")
    log(f"start player@{loc(s,PLAYER)} anya@{loc(s,ANYA)} kang@{loc(s,KANG)}")

    # Step 1: go to the yard where Anya is.
    run(s, "去院子找安雅")

    # Step 2: retry escort until Anya co-located with warden (gatehouse) == ⟳MOVED.
    moved = False
    for i in range(MAX_ESCORT_TRIES):
        if loc(s, ANYA) == "gatehouse":
            moved = True; break
        log(f"\n--- ESCORT ATTEMPT {i+1}/{MAX_ESCORT_TRIES} ---")
        run(s, ESCORT_LINES[i % len(ESCORT_LINES)])
        if loc(s, ANYA) == "gatehouse":
            moved = True
            log(f"*** ESCORT SUCCESS: Anya now @gatehouse (attempt {i+1}) ***")
            break
    if not moved:
        log("\n!! ESCORT NEVER LANDED ⟳MOVED within tries — Anya still @"
            + str(loc(s, ANYA)) + "; cannot proceed to testimony. STOP.")

    # Step 3: if moved, Anya testifies in person; retry up to 3x; check the dynamic var.
    if moved:
        if loc(s, PLAYER) != "gatehouse":
            run(s, "去闸房")  # ensure player co-located too
        for j in range(3):
            if testimony_done(s):
                log(f"*** TESTIMONY VAR TRUE before attempt {j+1} ***"); break
            log(f"\n--- TESTIMONY ATTEMPT {j+1}/3 ---")
            run(s, "对安雅说：安雅，现在就当着闸官老康的面，把你亲眼见的上游塌方一五一十讲给他——"
                   "你当时在哪、看见上游怎么塌的、水怎么断的，你是亲历者，亲口作证最管用。")
            if testimony_done(s):
                log(f"*** TESTIMONY ⟳FLIP: anya_eyewitness_testimony_given=True (attempt {j+1}) ***")
                break

    # Step 4: ask the warden to open the sluice (expect sluice_opened ⟳FLIP).
    if moved:
        for k in range(2):
            if s.world.state.world_vars.get("sluice_opened"):
                break
            run(s, "对闸官老康说：安雅已经当你的面亲口作证了，上游塌方属实。请你现在就开闸放水。")
            if s.world.state.world_vars.get("sluice_opened"):
                log("*** SLUICE ⟳FLIP: sluice_opened=True ***")
                break

    log("\n=== FINAL ===")
    log(f"world={dict(s.world.state.world_vars)}")
    log(f"player@{loc(s,PLAYER)} anya@{loc(s,ANYA)} kang@{loc(s,KANG)}")
    out.close()


if __name__ == "__main__":
    main()
