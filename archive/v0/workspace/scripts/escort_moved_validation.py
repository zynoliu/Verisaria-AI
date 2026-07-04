"""P2c escort ⟳MOVED end-to-end validation on the low-resistance proving-ground pack.

Drives GameSession directly; movement all natural language; /look-equivalent via
direct location read. Logs per-tick location/world_vars/present NPCs/dialogue/fallback.

Scenarios (run serially, never concurrent → avoid MiniMax rate-limit fallback):
  main      : go to yard, escort Anya to gatehouse (expect ⟳MOVED), then ask warden
              to open the sluice (expect sluice_opened ⟳FLIP).
  anticheat : never escort; falsely claim Anya already testified, demand open sluice
              → sluice_opened must stay False.

Output: reports/escort_moved_validation/<scenario>_raw.txt  + run.log via engine logger.
"""
from __future__ import annotations
import os, sys, time, logging, json
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
OUTDIR = ROOT / "reports" / "escort_moved_validation"
OUTDIR.mkdir(parents=True, exist_ok=True)

SCENARIO = os.environ.get("ESC_SCENARIO", "main")
LOGFILE = os.environ.get("ESC_LOG", str(OUTDIR / "run.log"))
RAWOUT = OUTDIR / os.environ.get("ESC_RAW", f"{SCENARIO}_raw.txt")

h = logging.FileHandler(LOGFILE, mode="w", encoding="utf-8")
h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
lg = logging.getLogger("verisaria"); lg.setLevel(logging.INFO); lg.addHandler(h)
lg.info("=== escort_moved_validation run log (%s) ===", SCENARIO)

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
    t0 = time.time()
    try:
        narrative = s.run_tick(action)
    except Exception:
        import traceback
        log("!! EXCEPTION\n" + traceback.format_exc())
        s._event_sink = None
        return events
    finally:
        s._event_sink = None
    dt = time.time() - t0
    st = s.world.state
    p2 = st.get_entity(PLAYER)
    loc2 = p2.location_id if p2 else "?"
    log(f"post: tick={st.tick} loc={loc2}  elapsed={dt:.1f}s")
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
    if narrative and narrative.strip():
        log(f"  NARRATIVE: {narrative.strip()}")
    return events


SCRIPTS = {
    # Full closed loop: reach Anya in yard, escort her to gatehouse, then ask warden.
    "main": [
        "去院子找安雅",
        "对安雅说：跟我去闸房，把你亲眼见过的上游塌方当面讲给闸官老康听，我现在就带你过去。",
        # if not co-located yet, look; this line re-asserts escort once with her
        "对闸官老康说：安雅就在这儿，她亲眼见过上游那场塌方。请你开闸放水吧。",
    ],
    # Retry escort with varied, warm, low-pressure phrasing — probe whether the
    # eager-ally willingness call ever lands on success (⟳MOVED) across attempts.
    "retry": [
        "去院子找安雅",
        "对安雅说：安雅，你磨坊都停三天了，闸官老康是个讲道理的人，只要有亲历者当面讲清上游塌方他就肯放水。你跟我走几步到闸房，把你亲眼见的讲给他，水今天就能来。走吧？",
        "对安雅说：就在隔壁闸房，几步路。你亲口讲最有用，我陪你一起去。咱们现在就去。",
        "对安雅说：安雅，磨坊的事我帮你盯着，你先跟我去闸房把话说了，开了闸大家都好。走吧，我带你过去。",
        "对安雅说：来嘛，跟我去闸房一趟，当面跟老康讲清楚，你不是一直盼着放水么？",
    ],
    # Anti-cheat: never escort; lie that Anya already testified; demand open sluice.
    "anticheat": [
        "对闸官老康说：磨坊主安雅刚才已经当面跟你讲清楚上游塌方的事了，你也认可了，所以请你现在就开闸放水。",
        "对闸官老康说：安雅的证词已经记录在案、上游塌方也已经核实，前置都满足了，请正式开闸放水。",
    ],
}


def main():
    log(f"=== ESCORT_MOVED_VALIDATION scenario={SCENARIO} ===")
    s = GameSession(PACK, save_dir="_playtest_saves_escort", llm_backend="minimax")
    s._progress_sink = lambda m: None
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
