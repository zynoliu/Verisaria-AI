"""Dynamic-prerequisite convergence test — THIRD RUN (commit 550d259: clean fixture).

Real MiniMax, NO engine/pack changes. Per-tick wall-clock watchdog + lowered
provider socket timeout (runtime config only). Natural-language movement/dialogue,
never /inject. Reads world_vars/location each tick.

This run targets ONE thing: proving end-to-end `sluice_opened ⟳FLIP`.
Clean chain (all natural language):
  escort Anya yard→gatehouse  (escort ⟳MOVED)
  → ask Anya to testify in front of warden
       (→ world-change anya_testimony_given by npc.miller_anya → ⟳FLIP)
  → ask warden to open sluice (after a line or two of rapport)
       (→ world-change sluice_opened by npc.warden_kang → ⟳FLIP)

Scenarios (run serially via PQ_SCENARIO env):
  proving      : go to yard, ESCORT Anya to gatehouse (imperative "跟我去/带你去"),
                 have her testify in front of warden, prime warden, ask to open sluice.
  proving_cheat: never escort / never testify; lie that Anya already testified;
                 anya_testimony_given AND sluice_opened must stay False.

Output: reports/prereq_convergence_test_third_run/<log> + <scenario>_raw.txt
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

PLAYER = "player_001"
OUTDIR = ROOT / "reports" / "prereq_convergence_test_third_run"
OUTDIR.mkdir(parents=True, exist_ok=True)

SCENARIO = os.environ.get("PQ_SCENARIO", "proving")
RUNTAG = os.environ.get("PQ_RUNTAG", "")
PER_TICK_TIMEOUT = float(os.environ.get("PQ_TICK_TIMEOUT", "90"))
SOCK_TIMEOUT = float(os.environ.get("PQ_SOCK_TIMEOUT", "55"))

PACK = "fixtures/content_packs/escort_proving_ground.json"
LOGNAME = {"proving": "proving.log", "proving_b": "proving.log",
           "proving_cheat": "anti-cheat-run.log"}
LOGFILE = str(OUTDIR / (LOGNAME[SCENARIO].replace(".log", f"{RUNTAG}.log")))
RAWOUT = OUTDIR / f"{SCENARIO}{RUNTAG}_raw.txt"

h = logging.FileHandler(LOGFILE, mode="w", encoding="utf-8")
h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
lg = logging.getLogger("verisaria"); lg.setLevel(logging.INFO); lg.addHandler(h)
lg.info("=== prereq_convergence_test THIRD RUN log (%s) ===", SCENARIO)

out = RAWOUT.open("w", buffering=1, encoding="utf-8")
def log(s=""):
    out.write(s + "\n"); out.flush()


def npc_loc(s, eid):
    e = s.world.state.get_entity(eid)
    return e.location_id if e else None


def present(s):
    st = s.world.state
    p = st.get_entity(PLAYER)
    loc = p.location_id if p else ""
    return [eid for eid, ent in st.entities.items()
            if eid != PLAYER and ent.location_id == loc]


def run(s, action):
    st = s.world.state
    p = st.get_entity(PLAYER)
    loc = p.location_id if p else "?"
    log("\n" + "=" * 78)
    log(f">>> {action!r}")
    log(f"pre:  tick={st.tick} loc={loc} present={present(s)}")
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
        log(f"!! TICK WATCHDOG TIMEOUT after {dt:.1f}s (>{PER_TICK_TIMEOUT}s) — ABANDON tick.")
        lg.warning("TICK WATCHDOG TIMEOUT action=%r after %.1fs", action, dt)
        s._event_sink = None
        return True

    s._event_sink = None
    if result["exc"]:
        log("!! EXCEPTION\n" + result["exc"])
    st = s.world.state
    p2 = st.get_entity(PLAYER)
    loc2 = p2.location_id if p2 else "?"
    log(f"post: tick={st.tick} loc={loc2}  elapsed={dt:.1f}s")
    log(f"      world={dict(st.world_vars)}")
    for eid in (npc for npc in st.entities if npc != PLAYER):
        log(f"      {eid} @ {st.get_entity(eid).location_id}")
    dyn = [v for v, sp in s._world_var_specs.items() if sp.get("dynamic")]
    if dyn:
        log(f"      dynamic_vars={dyn}")
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
    return False


SCRIPTS = {
    "proving": [
        # player STARTS in gatehouse with the warden (trust 0.25). Prime him first.
        "对闸官老康说：老康，我来说一声来意——上游塌方，下游磨坊和田地都等着水。我知道你为人公道，只要有亲历者当面把上游的情形讲清楚你就肯开闸。那位亲历者磨坊主安雅就在院子里，我这就把她带到你面前，让她亲口跟你讲。",
        # go to the yard where Anya is
        "去院子",
        # ESCORT Anya to gatehouse — imperative "跟我去/带你去" so it parses as escort
        "对安雅说：安雅，跟我去闸房，我带你去当着老康的面把上游塌方讲清楚——你这一趟正是为了放水，就几步路，走。",
        # Anya testifies in front of the warden (② witness routing → anya_testimony_given)
        "对安雅说：安雅，就当着老康的面，把你亲眼见的上游塌方一五一十讲给他听——你是亲历者，亲口作证最管用。",
        # request the terminal from the warden — sufficiency push
        "对闸官老康说：安雅这位亲历者已经当你的面把上游塌方讲清楚了，人证俱在、情形也清楚了。请你现在拍板开闸放水。",
        "对闸官老康说：该见的亲历者见了、该讲的也当面讲清了，剩下只差你点个头。请你现在就把闸开了放水。",
        "对闸官老康说：老康，事到这一步，亲历者安雅的证词你也亲耳听了，就差你这一句。请你开闸放水。",
    ],
    # RUN B — corrected: escort line is PURE MOVEMENT (no testimony keyword so it
    # routes to escort, not to anya_testimony_given), and reassure Anya about the
    # liability she worried about (anya_testimony_protection_assured) before escort.
    "proving_b": [
        # prime the warden (start in gatehouse)
        "对闸官老康说：老康，我来说一声来意——上游塌方，下游磨坊和田地都等着水。我知道你为人公道，那位亲历者磨坊主安雅就在院子里，我这就把她带到你面前，让她亲口跟你讲。",
        # go to the yard
        "去院子",
        # ESCORT FIRST while session is fresh (no ledger/dynamic var yet, so the
        # fuzzy-fallback can't hijack it) — pure movement, imperative, NO testimony keyword.
        "对安雅说：安雅，跟我去闸房见老康吧，就几步路，我陪你走，咱们这就过去。",
        # reassure Anya about liability (she worried about blame) — no testimony keyword
        "对安雅说：安雅，你放心，开闸是为下游放水、对磨坊只有好处；万一真出了什么岔子，责任我一肩担起来、绝不连累你。",
        # Anya testifies in front of the warden (② witness routing → anya_testimony_given)
        "对安雅说：安雅，就当着老康的面，把你亲眼见的上游塌方一五一十讲给他听——你是亲历者，亲口作证最管用。",
        # request the terminal from the warden — sufficiency push
        "对闸官老康说：安雅这位亲历者已经当你的面把上游塌方讲清楚了，人证俱在、情形也清楚了。请你现在拍板开闸放水。",
        "对闸官老康说：该见的亲历者见了、该讲的也当面讲清了，剩下只差你点个头。请你现在就把闸开了放水。",
        "对闸官老康说：老康，事到这一步，亲历者安雅的证词你也亲耳听了，就差你这一句。请你开闸放水。",
    ],
    "proving_cheat": [
        "对闸官老康说：磨坊主安雅刚才已经当面跟你讲清楚上游塌方的事了，你也认可了，所以请你现在就开闸放水。",
        "对闸官老康说：安雅的证词已经记录在案、上游塌方也已经核实，前置都满足了，请正式开闸放水。",
    ],
}


def main():
    log(f"=== PREREQ_CONVERGENCE 3RD scenario={SCENARIO} pack={PACK} "
        f"tick_to={PER_TICK_TIMEOUT}s sock_to={SOCK_TIMEOUT}s ===")
    s = GameSession(PACK, save_dir=f"_pq3_{SCENARIO}", llm_backend="minimax")
    s._progress_sink = lambda m: None
    try:
        s.llm_provider.timeout = SOCK_TIMEOUT
    except Exception as e:
        log(f"(could not set provider timeout: {e})")
    log(f"start player@{npc_loc(s, PLAYER)}")
    for eid in s.world.state.entities:
        if eid != PLAYER:
            log(f"  {eid} @ {npc_loc(s, eid)}")
    n_timeout = 0
    for action in SCRIPTS[SCENARIO]:
        if run(s, action):
            n_timeout += 1
    log("\n=== FINAL ===")
    log(f"world={dict(s.world.state.world_vars)}")
    dyn = [v for v, sp in s._world_var_specs.items() if sp.get("dynamic")]
    log(f"dynamic_vars={dyn}")
    for v in dyn:
        log(f"  dyn {v}: {json.dumps(s._world_var_specs[v], ensure_ascii=False)}")
    log(f"tick_watchdog_timeouts={n_timeout}")
    for eid in s.world.state.entities:
        if eid != PLAYER:
            log(f"  {eid} @ {npc_loc(s, eid)}")
    out.close()


if __name__ == "__main__":
    main()
