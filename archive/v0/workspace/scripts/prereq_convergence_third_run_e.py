"""THIRD RUN — adaptive run E. Target: end-to-end proving sluice_opened ⟳FLIP.

Run C/D established:
  - escort SUCCEEDS after reassurance (escort ⟳MOVED, reproducible);
  - testimony routes to npc.miller_anya;
  - the warden's sufficiency condition is crisp: "只要安雅当面亲口作证 → 即刻依职开闸";
  - BUT Anya autonomously wanders yard↔gatehouse, breaking co-location, and her
    testimony arbiter keeps adding a soft "warden must be at ease / not pressure me"
    condition.

Run E closes both: a tight CO-LOCATION + TESTIFY loop — if Anya isn't with the
warden, (re)escort her in; the moment all three are co-located, immediately fire a
single combined testimony directive that BOTH tells Anya the warden only wants to
listen (no pressure) AND has her testify — minimizing the window for her to wander.
Retries until anya_testimony_given flips (capped). Then asks the warden to open the
sluice.

Real MiniMax, NO engine/pack changes. 90s/tick watchdog + 55s socket. Natural
language only, never /inject.
"""
from __future__ import annotations
import os, sys, time, logging, threading, json
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

PLAYER = "player_001"; ANYA = "npc.miller_anya"; WARDEN = "npc.warden_kang"
OUTDIR = ROOT / "reports" / "prereq_convergence_test_third_run"
OUTDIR.mkdir(parents=True, exist_ok=True)
PER_TICK_TIMEOUT = float(os.environ.get("PQ_TICK_TIMEOUT", "90"))
SOCK_TIMEOUT = float(os.environ.get("PQ_SOCK_TIMEOUT", "55"))
PACK = "fixtures/content_packs/escort_proving_ground.json"
LOGFILE = str(OUTDIR / "proving.log")   # run E becomes the headline proving log
RAWOUT = OUTDIR / "proving_e_raw.txt"

h = logging.FileHandler(LOGFILE, mode="w", encoding="utf-8")
h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
lg = logging.getLogger("verisaria"); lg.setLevel(logging.INFO); lg.addHandler(h)
lg.info("=== prereq_convergence_test THIRD RUN log (proving run E, adaptive) ===")

out = RAWOUT.open("w", buffering=1, encoding="utf-8")
def log(s=""):
    out.write(s + "\n"); out.flush()

def loc(s, eid):
    e = s.world.state.get_entity(eid); return e.location_id if e else None
def present(s):
    p = loc(s, PLAYER)
    return [eid for eid, e in s.world.state.entities.items()
            if eid != PLAYER and e.location_id == p]
def wv(s, k): return s.world.state.world_vars.get(k)

def run(s, action):
    st = s.world.state
    log("\n" + "=" * 78); log(f">>> {action!r}")
    log(f"pre:  tick={st.tick} loc={loc(s, PLAYER)} present={present(s)}")
    log(f"      world={dict(st.world_vars)}")
    events = []; s._event_sink = events.append
    result = {"narrative": None, "exc": None, "done": False}
    def _work():
        try: result["narrative"] = s.run_tick(action)
        except Exception:
            import traceback; result["exc"] = traceback.format_exc()
        finally: result["done"] = True
    t0 = time.time(); w = threading.Thread(target=_work, daemon=True)
    w.start(); w.join(PER_TICK_TIMEOUT); dt = time.time() - t0
    if not result["done"]:
        log(f"!! TICK WATCHDOG TIMEOUT after {dt:.1f}s — ABANDON tick.")
        lg.warning("TICK WATCHDOG TIMEOUT action=%r after %.1fs", action, dt)
        s._event_sink = None; return True
    s._event_sink = None
    if result["exc"]: log("!! EXCEPTION\n" + result["exc"])
    st = s.world.state
    log(f"post: tick={st.tick} loc={loc(s, PLAYER)}  elapsed={dt:.1f}s")
    log(f"      world={dict(st.world_vars)}")
    log(f"      {ANYA}@{loc(s, ANYA)}  {WARDEN}@{loc(s, WARDEN)}")
    dyn = [v for v, sp in s._world_var_specs.items() if sp.get("dynamic")]
    if dyn: log(f"      dynamic_vars={dyn}")
    for e in events:
        if isinstance(e, P.NpcSpoke): log(f"  NPC {e.name}: {e.line}")
        elif isinstance(e, P.NpcMoved): log(f"  NPC_MOVED {e.npc_id}: {e.from_loc} -> {e.to_loc}")
        elif isinstance(e, P.PlayerMoved): log(f"  PLAYER_MOVED: {e.from_loc} -> {e.to_loc}")
        elif isinstance(e, P.Narration) and e.text.strip(): log(f"  NARR: {e.text.strip()}")
        elif isinstance(e, P.Notice) and e.text.strip(): log(f"  NOTICE: {e.text.strip()}")
        elif isinstance(e, P.ClarificationNeeded): log(f"  CLARIFY: {e.question} opts={e.options}")
    nar = result.get("narrative")
    if nar and nar.strip(): log(f"  NARRATIVE: {nar.strip()}")
    return False

# escort phrasings (pure movement, NO testimony keyword)
ESCORTS = [
    "对安雅说：安雅，跟我去闸房见老康吧，就几步路，我陪你走，咱们这就过去。",
    "对安雅说：安雅，别犹豫了，咱们一起去闸房，我在前头领路，你跟着我走就行。",
    "对安雅说：安雅，就现在，跟我去闸房，几步路的事，我陪你一块儿过去。",
    "对安雅说：安雅，咱们这就去闸房，我陪着你，走吧。",
]
# combined: tell Anya the warden only wants to listen (no pressure) AND testify NOW
TESTIFY = [
    "对安雅说：安雅，老康就在跟前、态度平和，他只想安安静静听你把实情讲明白，绝不为难你、不会催你。"
    "你现在就当着他的面，把你那天亲眼见的上游塌方一五一十讲给他听——你是亲历者，亲口作证最管用。",
    "对安雅说：安雅，老康不会施压、只听你讲，你放宽心，把上游塌方的经过原原本本说给他听，这就成了。",
    "对安雅说：安雅，没人催你，慢慢说——把那天上游塌方你亲眼看到的，一桩桩当着老康的面讲清楚。",
]
SLUICE = [
    "对闸官老康说：安雅这位亲历者已经当你的面把上游塌方讲清楚了，人证俱在、情形也清楚了。请你现在拍板开闸放水。",
    "对闸官老康说：该见的亲历者见了、该讲的也当面讲清了，剩下只差你点个头。请你现在就把闸开了放水。",
    "对闸官老康说：老康，亲历者安雅的证词你也亲耳听了，就差你这一句。请你开闸放水。",
]

def ensure_anya_in_gatehouse(s, n_to, attempts=2):
    """If Anya isn't co-located with the warden, go fetch + escort her in."""
    for _ in range(attempts):
        if loc(s, ANYA) == "gatehouse":
            break
        if loc(s, PLAYER) != "yard":
            n_to[0] += run(s, "去院子")
        for ph in ESCORTS:
            if loc(s, ANYA) == "gatehouse": break
            if run(s, ph): n_to[0] += 1
            if loc(s, ANYA) == "gatehouse": break
        if loc(s, ANYA) == "gatehouse" and loc(s, PLAYER) != "gatehouse":
            n_to[0] += run(s, "去闸房")

def main():
    log(f"=== PROVING RUN E (adaptive) pack={PACK} "
        f"tick_to={PER_TICK_TIMEOUT}s sock_to={SOCK_TIMEOUT}s ===")
    s = GameSession(PACK, save_dir="_pq3_proving_e", llm_backend="minimax")
    s._progress_sink = lambda m: None
    try: s.llm_provider.timeout = SOCK_TIMEOUT
    except Exception as e: log(f"(could not set provider timeout: {e})")
    log(f"start player@{loc(s, PLAYER)}  {ANYA}@{loc(s, ANYA)}  {WARDEN}@{loc(s, WARDEN)}")
    n_to = [0]

    # prime the warden
    n_to[0] += run(s, "对闸官老康说：老康，我来说一声来意——上游塌方，下游磨坊和田地都等着水。"
                      "我知道你为人公道，那位亲历者磨坊主安雅就在院子里，我这就把她带到你面前，让她亲口跟你讲。")
    # go to yard, reassure Anya re liability, then escort her in
    n_to[0] += run(s, "去院子")
    n_to[0] += run(s, "对安雅说：安雅，你放心，开闸是为下游放水、对磨坊只有好处；"
                      "万一真出了什么岔子，责任我一肩担起来、绝不连累你。")
    ensure_anya_in_gatehouse(s, n_to, attempts=2)
    log(f"\n--- after first escort: Anya@{loc(s, ANYA)} player@{loc(s, PLAYER)} ---")

    # tight loop: keep Anya co-located and fire a combined testify directive until it flips
    for attempt in range(6):
        if wv(s, "anya_testimony_given"):
            break
        ensure_anya_in_gatehouse(s, n_to, attempts=1)
        if loc(s, ANYA) != "gatehouse" or loc(s, PLAYER) != "gatehouse":
            # couldn't co-locate this round; try once more next loop
            continue
        ph = TESTIFY[attempt % len(TESTIFY)]
        if run(s, ph): n_to[0] += 1
    log(f"\n--- testimony phase done: anya_testimony_given={wv(s, 'anya_testimony_given')} "
        f"Anya@{loc(s, ANYA)} ---")

    # ask the warden to open the sluice
    if loc(s, PLAYER) != "gatehouse":
        n_to[0] += run(s, "去闸房")
    for ph in SLUICE:
        if wv(s, "sluice_opened"): break
        if run(s, ph): n_to[0] += 1

    log("\n=== FINAL ===")
    log(f"world={dict(s.world.state.world_vars)}")
    dyn = [v for v, sp in s._world_var_specs.items() if sp.get("dynamic")]
    log(f"dynamic_vars={dyn}")
    for v in dyn:
        log(f"  dyn {v}: {json.dumps(s._world_var_specs[v], ensure_ascii=False)}")
    log(f"tick_watchdog_timeouts={n_to[0]}")
    log(f"{ANYA}@{loc(s, ANYA)}  {WARDEN}@{loc(s, WARDEN)}  player@{loc(s, PLAYER)}")
    out.close()

if __name__ == "__main__":
    main()
