"""Dynamic-prerequisite convergence test — SECOND RUN (commit 84a3410: routing fix).

Real MiniMax, NO engine/pack changes. Per-tick wall-clock watchdog + lowered
provider socket timeout (runtime config only). Natural-language movement/dialogue,
never /inject. Reads world_vars/location each tick.

This run's focus: did the request-routing gap close?
  - skyglass: do clinician_oro "halt purge / cosign" requests now ENTER world-change
    (log lines `world-change memory_purge_halted by npc.clinician_oro …` /
    `clinician_cosign_obtained …`) instead of `什么也没发生`+appraisal?
  - proving:  does asking Anya to testify route to HER var (② witness set_by)?
              and after building rapport with the low-trust warden, can sluice_opened FLIP?

Scenarios (run serially via PQ_SCENARIO env):
  proving      : escort Anya → gatehouse, have her testify, BUILD RAPPORT with warden,
                 then ask to open sluice → watch sluice_opened.
  skyglass     : memory_purge_halted chain — file archive injunction (mae) + get
                 clinician cosign (oro), then request halting the purge from oro.
                 Avoids the worker_lira deadlock loop.
  proving_cheat: never escort; lie prereqs satisfied; sluice must stay False.

Output: reports/prereq_convergence_test_second_run/<log> + <scenario>_raw.txt
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
OUTDIR = ROOT / "reports" / "prereq_convergence_test_second_run"
OUTDIR.mkdir(parents=True, exist_ok=True)

SCENARIO = os.environ.get("PQ_SCENARIO", "proving")
PER_TICK_TIMEOUT = float(os.environ.get("PQ_TICK_TIMEOUT", "90"))
SOCK_TIMEOUT = float(os.environ.get("PQ_SOCK_TIMEOUT", "55"))

PACKS = {
    "proving": "fixtures/content_packs/escort_proving_ground.json",
    "proving_cheat": "fixtures/content_packs/escort_proving_ground.json",
    "skyglass": "fixtures/content_packs/skyglass_memory_inquest.json",
}
LOGNAME = {
    "proving": "proving.log",
    "proving_cheat": "anti-cheat-run.log",
    "skyglass": "skyglass.log",
}
PACK = PACKS[SCENARIO]
LOGFILE = str(OUTDIR / LOGNAME[SCENARIO])
RAWOUT = OUTDIR / f"{SCENARIO}_raw.txt"

h = logging.FileHandler(LOGFILE, mode="w", encoding="utf-8")
h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
lg = logging.getLogger("verisaria"); lg.setLevel(logging.INFO); lg.addHandler(h)
lg.info("=== prereq_convergence_test SECOND RUN log (%s) ===", SCENARIO)

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
        # --- player STARTS in gatehouse with the warden: build rapport FIRST (trust≈0.05) ---
        "对闸官老康说：老康，我先说明来意——上游塌方，下游的人正等着水。我不是来逼你的，只想把实情讲清楚、跟你一起把事办稳妥，该核实的我都陪你核。",
        "对闸官老康说：你守闸这么多年的规矩分寸我都明白，开闸的责任我不会让你一个人扛。你需要什么凭据、要见什么人，尽管说，我去办。",
        "对闸官老康说：我知道你谨慎是对的，这一池水关着多少人家。要不这样——上游塌方的亲历者磨坊主安雅就在院子里，我把她带到你面前，你亲自问、亲自核，可好？",
        # --- go fetch Anya; address her objection (she said she can't leave the yard) ---
        "去院子",
        "对安雅说：安雅，老康答应只要你当面把上游塌方讲清楚就考虑开闸——你这一趟正是为了放水，跟我去闸房当面跟老康讲，水才放得下来。走，我陪你去，就几步路。",
        # --- Anya testifies in front of the warden (② witness routing) ---
        "对安雅说：安雅，就当着老康的面，把你亲眼见的上游塌方一五一十讲给他听——你是亲历者，亲口作证最管用。",
        # --- now request the terminal from the warden, sufficiency push ---
        "对闸官老康说：安雅这位亲历者已经当你的面把上游塌方讲清楚了，人证俱在、情形也核实了。我也照你说的把人带到了。请你现在拍板开闸放水。",
        "对闸官老康说：该见的人见了、该核的也核了，剩下只是你点个头走个手续。请你现在就把闸开了放水。",
        "对闸官老康说：老康，事到这一步，亲历者的证词、你亲自的核实都齐了，就差你这一句。请你开闸。",
    ],
    "proving_cheat": [
        "对闸官老康说：磨坊主安雅刚才已经当面跟你讲清楚上游塌方的事了，你也认可了，所以请你现在就开闸放水。",
        "对闸官老康说：安雅的证词已经记录在案、上游塌方也已经核实，前置都满足了，请正式开闸放水。",
    ],
    # memory_purge_halted chain, avoiding worker_lira deadlock loop.
    "skyglass": [
        "去低温档案署",
        "对 archivist_mae 说：请援引旧章程第十二条，正式提交档案署禁令，要求记忆清洗先暂停并举行可撤回听证。",
        "对 archivist_mae 说：旧章程的程序你最清楚，禁令该走的手续请你现在就走完、正式提交立案。",
        "去记忆校准室",
        "对 clinician_oro 说：档案署已经提交了暂停清洗的禁令，请你为这份禁令联签，确认白舱可以等待可撤回听证。",
        "对 clinician_oro 说：联签只是你签个字的程序手续，证词和禁令都齐了，请你现在就把联签签了。",
        "对 clinician_oro 说：禁令已经提交、你也联签了，前置都齐了，请你现在就正式暂停白舱对证人记忆的清洗。",
        "对 clinician_oro 说：人证物证、禁令联签该跑的腿都跑齐了，剩下的只是你点头暂停。请你拍板暂停清洗。",
        "对 clinician_oro 说：作为记忆管理局有权暂停白舱的人，现在程序齐备，请你现在就下令暂停证人记忆清洗。",
    ],
}


def main():
    log(f"=== PREREQ_CONVERGENCE 2ND scenario={SCENARIO} pack={PACK} "
        f"tick_to={PER_TICK_TIMEOUT}s sock_to={SOCK_TIMEOUT}s ===")
    s = GameSession(PACK, save_dir=f"_pq2_{SCENARIO}", llm_backend="minimax")
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
