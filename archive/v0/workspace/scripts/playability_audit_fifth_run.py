"""Playability audit — fifth run. Interactive free-play REPL over a fifo-style
file, so the human-driving agent can react tick-by-tick.

Reads actions one-per-line from CMD_FILE; appends raw transcript to RAW.
Special lines: '/look', '/world', '/skip', '/wait' pass through; '__QUIT__' ends.

Per tick logs: player input, present NPCs, world vars (changed), stances,
NPC dialogue (raw lines), narration/notices/clarify, snapshot (tick/clock/weather),
and a RELATIONSHIP snapshot (trust/suspicion/respect + descriptor phrase) for each
present NPC, plus any deltas emitted this tick.
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

PACK = "fixtures/content_packs/skyglass_memory_inquest.json"
PLAYER = "player_001"
OUTDIR = ROOT / "reports" / "playability_audit_fifth_run"
OUTDIR.mkdir(parents=True, exist_ok=True)
CMD_FILE = OUTDIR / "cmds.txt"
RAW = OUTDIR / "transcript.md"
LOGFILE = OUTDIR / "run.log"
STATUS = OUTDIR / "status.txt"

h = logging.FileHandler(LOGFILE, mode="w", encoding="utf-8")
h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
lg = logging.getLogger("verisaria"); lg.setLevel(logging.INFO); lg.addHandler(h)
lg.info("=== fifth run ===")

out = RAW.open("w", buffering=1, encoding="utf-8")
def log(s=""):
    out.write(s + "\n"); out.flush()


def present_npcs(s):
    st = s.world.state
    p = st.get_entity(PLAYER)
    loc = p.location_id if p else ""
    return {eid: ent.name for eid, ent in st.entities.items()
            if eid != PLAYER and ent.location_id == loc}


def rel_line(s, eid, name):
    snap = s.get_relationship(eid, PLAYER)
    if not snap or not snap.dimensions:
        return f"    REL {name}: (none)"
    parts = []
    for dim in ("trust", "suspicion", "respect", "affection"):
        if dim in snap.dimensions:
            val = snap.dimensions[dim]
            try:
                d = P.relationship_descriptor(dim, val)
                ph = f" [{d.phrase}]" if d.phrase else ""
            except Exception:
                ph = ""
            parts.append(f"{dim}={val:+.3f}{ph}")
    return f"    REL {name}: " + "  ".join(parts)


def snapshot(s):
    st = s.world.state
    bits = [f"tick={st.tick}"]
    clk = getattr(st, "clock", None) or getattr(st, "world_clock", None)
    for attr in ("clock", "time_of_day", "weather", "climate"):
        v = getattr(st, attr, None)
        if v is not None and not callable(v):
            bits.append(f"{attr}={v}")
    return " ".join(bits)


def do(s, action):
    st = s.world.state
    p = st.get_entity(PLAYER)
    loc = p.location_id if p else "?"
    pres = present_npcs(s)
    pre_world = dict(st.world_vars)
    log("\n" + "=" * 78)
    log(f">>> {action}")
    log(f"pre:  {snapshot(s)} loc={loc} present={list(pres.values())}")
    events = []
    s._event_sink = events.append
    t0 = time.time()
    narrative = None
    try:
        narrative = s.run_tick(action)
    except Exception:
        import traceback
        log("!! EXCEPTION\n" + traceback.format_exc())
    finally:
        s._event_sink = None
    dt = time.time() - t0
    st = s.world.state
    p2 = st.get_entity(PLAYER)
    loc2 = p2.location_id if p2 else "?"
    post_world = dict(st.world_vars)
    log(f"post: {snapshot(s)} loc={loc2} elapsed={dt:.1f}s")
    # world var changes
    changed = {k: post_world[k] for k in post_world if pre_world.get(k) != post_world.get(k)}
    if changed:
        log(f"  WORLD-CHANGED: {changed}")
    truthy = {k: v for k, v in post_world.items() if v is True}
    if truthy:
        log(f"  WORLD-TRUE: {sorted(truthy)}")
    try:
        stances = sorted(s.agenda_service.get_confirmed_stance_topics())
        if stances:
            log(f"  STANCES: {stances}")
    except Exception:
        pass
    for e in events:
        if isinstance(e, P.NpcSpoke):
            log(f"  NPC {e.name}: {e.line}")
        elif isinstance(e, P.Narration) and e.text.strip():
            log(f"  NARR: {e.text.strip()}")
        elif isinstance(e, P.Notice) and e.text.strip():
            log(f"  NOTICE: {e.text.strip()}")
        elif isinstance(e, P.ClarificationNeeded):
            log(f"  CLARIFY: {e.question} opts={e.options}")
        elif isinstance(e, P.RelationshipShifted):
            d = e.descriptor
            log(f"  REL-SHIFT {e.name}: {d.label} {e.delta:+.3f} -> {d.value:+.3f} [{d.phrase}]")
        elif isinstance(e, P.WorldVarChanged):
            log(f"  WORLDVAR: {e.label} ({e.var_id}) = {e.value}")
        elif isinstance(e, P.StanceConfirmed):
            log(f"  STANCE-CONFIRMED: {e.label} ({e.topic_id})")
        elif isinstance(e, P.NpcMoved):
            log(f"  NPC-MOVED: {e.name or e.npc_id} {e.from_loc} -> {e.to_loc}")
    if narrative and narrative.strip():
        log(f"  NARRATIVE: {narrative.strip()}")
    # relationship snapshot for present NPCs (post-tick)
    pres2 = present_npcs(s)
    for eid, name in pres2.items():
        log(rel_line(s, eid, name))
    out.flush()


def main():
    log("=== FIFTH RUN — skyglass_memory_inquest — free play (valley/orchid/broadcast lines) ===")
    s = GameSession(PACK, save_dir="_playtest_saves_5", llm_backend="minimax")
    s._progress_sink = lambda m: None
    st = s.world.state
    p = st.get_entity(PLAYER)
    log(f"start loc={p.location_id}")
    log("entities:")
    for eid, ent in st.entities.items():
        if eid != PLAYER:
            log(f"  {ent.name} ({eid}) @ {ent.location_id}")
    # opening drives
    try:
        ag = getattr(s.agenda_service, "player_agenda", None) or getattr(s.agenda_service, "_player_agenda", None)
        drives = getattr(ag, "current_drives", None) if ag else None
        if drives:
            log(f"drives: {[getattr(d,'label',d) for d in drives]}")
    except Exception as e:
        log(f"drives: (err {e})")

    CMD_FILE.write_text("", encoding="utf-8")
    STATUS.write_text("READY\n", encoding="utf-8")
    seen = 0
    idle = 0
    while True:
        lines = CMD_FILE.read_text(encoding="utf-8").splitlines()
        if len(lines) > seen:
            for action in lines[seen:]:
                action = action.strip()
                seen += 1
                if not action:
                    continue
                if action == "__QUIT__":
                    log("\n=== QUIT ===")
                    log(f"final world={dict(s.world.state.world_vars)}")
                    out.close()
                    STATUS.write_text("DONE\n", encoding="utf-8")
                    return
                STATUS.write_text(f"BUSY tick {seen}: {action}\n", encoding="utf-8")
                do(s, action)
                STATUS.write_text(f"READY (done {seen})\n", encoding="utf-8")
            idle = 0
        else:
            idle += 1
            time.sleep(1.0)
            if idle > 1800:  # 30 min idle -> bail
                log("\n=== IDLE TIMEOUT ===")
                out.close()
                STATUS.write_text("IDLE_TIMEOUT\n", encoding="utf-8")
                return


if __name__ == "__main__":
    main()
