"""P2c escort closed-loop · THIRD run, FINAL ordered driver.

Correct ordering (the dynamic eyewitness prereq only spawns once the warden REFUSES
an open-sluice request):
  1. 去院子找安雅
  2. escort Anya to gatehouse, retry until Anya@gatehouse (⟳MOVED) using imperative
     "带你过去" phrasing that parses as escort (proven in second_run).
  3. ask warden to open sluice  → warden refuses, engine may emerge dynamic prereq
     anya_eyewitness_testimony_given.
  4. have Anya testify in person to the warden (both co-located) → that prereq ⟳FLIP.
  5. ask warden again → sluice_opened ⟳FLIP.
Every tick watchdog-protected. If the warden wanders off (he sometimes moves to yard),
re-summon him by going to him / calling him before the open-sluice ask.
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
PLAYER, ANYA, KANG = "player_001", "npc.miller_anya", "npc.warden_kang"
OUTDIR = ROOT / "reports" / "escort_moved_validation_third_run"
OUTDIR.mkdir(parents=True, exist_ok=True)
LOGFILE = str(OUTDIR / os.environ.get("ESC_LOG", "run.log"))
RAWOUT = OUTDIR / os.environ.get("ESC_RAW", "main_raw.txt")
PER_TICK_TIMEOUT = float(os.environ.get("ESC_TICK_TIMEOUT", "90"))
SOCK_TIMEOUT = float(os.environ.get("ESC_SOCK_TIMEOUT", "55"))

h = logging.FileHandler(LOGFILE, mode="w", encoding="utf-8")
h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
lg = logging.getLogger("verisaria"); lg.setLevel(logging.INFO); lg.addHandler(h)
lg.info("=== escort_moved THIRD final-ordered run log ===")
out = RAWOUT.open("w", buffering=1, encoding="utf-8")
def log(s=""): out.write(s + "\n"); out.flush()
def loc(s, eid):
    e = s.world.state.get_entity(eid); return e.location_id if e else None
def present(s):
    st = s.world.state; p = st.get_entity(PLAYER); l = p.location_id if p else ""
    return [eid for eid, e in st.entities.items() if eid != PLAYER and e.location_id == l]
def wv(s): return dict(s.world.state.world_vars)

def run(s, action):
    st = s.world.state
    log("\n" + "=" * 78); log(f">>> {action!r}")
    log(f"pre:  tick={st.tick} player@{loc(s,PLAYER)} present={present(s)} "
        f"anya@{loc(s,ANYA)} kang@{loc(s,KANG)} world={wv(s)}")
    events = []; s._event_sink = events.append
    res = {"n": None, "exc": None, "done": False}
    def _w():
        try: res["n"] = s.run_tick(action)
        except Exception:
            import traceback; res["exc"] = traceback.format_exc()
        finally: res["done"] = True
    t0 = time.time(); th = threading.Thread(target=_w, daemon=True); th.start()
    th.join(PER_TICK_TIMEOUT); dt = time.time() - t0
    if not res["done"]:
        log(f"!! TICK WATCHDOG TIMEOUT {dt:.1f}s (>{PER_TICK_TIMEOUT}s) — ABANDON, continue.")
        lg.warning("TICK WATCHDOG TIMEOUT action=%r %.1fs", action, dt)
        s._event_sink = None; return True
    s._event_sink = None
    if res["exc"]: log("!! EXCEPTION\n" + res["exc"])
    st = s.world.state
    log(f"post: tick={st.tick} player@{loc(s,PLAYER)} anya@{loc(s,ANYA)} "
        f"kang@{loc(s,KANG)} world={wv(s)} elapsed={dt:.1f}s")
    for e in events:
        if isinstance(e, P.NpcSpoke):       log(f"  NPC {e.name}: {e.line}")
        elif isinstance(e, P.NpcMoved):     log(f"  NPC_MOVED {e.npc_id}: {e.from_loc} -> {e.to_loc}")
        elif isinstance(e, P.PlayerMoved):  log(f"  PLAYER_MOVED: {e.from_loc} -> {e.to_loc}")
        elif isinstance(e, P.Narration) and e.text.strip():  log(f"  NARR: {e.text.strip()}")
        elif isinstance(e, P.Notice) and e.text.strip():     log(f"  NOTICE: {e.text.strip()}")
        elif isinstance(e, P.ClarificationNeeded):           log(f"  CLARIFY: {e.question}")
    if res.get("n") and res["n"].strip(): log(f"  NARRATIVE: {res['n'].strip()}")
    return False

# Imperative escort phrasings (parse as escort, proven in second_run pattern).
ESCORT = [
    "对安雅说：跟我去闸房，把你亲眼见过的上游塌方当面讲给闸官老康听，我现在就带你过去。",
    "我带安雅去闸房，让她当面把上游塌方的事讲给闸官老康。",
    "对安雅说：安雅，我现在就带你去闸房见老康，你跟我走。",
]
def testimony_var(s):
    return s.world.state.world_vars.get("anya_eyewitness_testimony_given")

def ensure_kang_here(s):
    """If the warden wandered off, go to wherever he is so we're co-located."""
    if loc(s, KANG) != loc(s, PLAYER):
        target = loc(s, KANG)
        run(s, "去闸房" if target == "gatehouse" else "去院子")

def main():
    log(f"=== THIRD final-ordered: per_tick={PER_TICK_TIMEOUT}s sock={SOCK_TIMEOUT}s ===")
    s = GameSession(PACK, save_dir="_playtest_saves_escort3c", llm_backend="minimax")
    s._progress_sink = lambda m: None
    try: s.llm_provider.timeout = SOCK_TIMEOUT
    except Exception as e: log(f"(set timeout failed: {e})")
    log(f"start player@{loc(s,PLAYER)} anya@{loc(s,ANYA)} kang@{loc(s,KANG)}")

    run(s, "去院子找安雅")

    # escort retry until ⟳MOVED
    for i in range(6):
        if loc(s, ANYA) == "gatehouse": break
        log(f"\n--- ESCORT ATTEMPT {i+1} ---")
        run(s, ESCORT[i % len(ESCORT)])
    if loc(s, ANYA) != "gatehouse":
        log("!! ESCORT never landed ⟳MOVED; STOP."); log("\n=== FINAL ===")
        log(f"world={wv(s)} player@{loc(s,PLAYER)} anya@{loc(s,ANYA)} kang@{loc(s,KANG)}")
        out.close(); return
    log("*** ⟳MOVED confirmed: Anya@gatehouse ***")

    # Drive the warden-gate loop: ask -> (refuse / maybe spawn prereq) -> testify -> ask ...
    for rnd in range(4):
        if s.world.state.world_vars.get("sluice_opened"):
            break
        ensure_kang_here(s)
        log(f"\n--- OPEN-SLUICE ASK round {rnd+1} ---")
        run(s, "对闸官老康说：请你现在就开闸放水。")
        if s.world.state.world_vars.get("sluice_opened"):
            log("*** sluice_opened ⟳FLIP=True ***"); break
        # If a testimony prereq exists (or warden wants eyewitness), have Anya testify.
        log(f"\n--- ANYA TESTIFIES round {rnd+1} (prereq var now: "
            f"{testimony_var(s)}) ---")
        ensure_kang_here(s)
        if loc(s, ANYA) != loc(s, KANG):
            run(s, ESCORT[0])  # re-escort if she drifted
        run(s, "对安雅说：安雅，现在就当着闸官老康的面，把你亲眼见的上游塌方亲口作证给他——"
               "你当时在渠口，看见整面山皮塌进河里、水头一下就断了，把这经过讲清楚。")
        if testimony_var(s):
            log("*** anya_eyewitness_testimony_given ⟳FLIP=True ***")

    log("\n=== FINAL ===")
    log(f"world={wv(s)}")
    log(f"player@{loc(s,PLAYER)} anya@{loc(s,ANYA)} kang@{loc(s,KANG)}")
    out.close()

if __name__ == "__main__":
    main()
