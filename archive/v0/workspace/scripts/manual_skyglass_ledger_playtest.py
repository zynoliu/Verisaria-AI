from __future__ import annotations

import logging
import os
from pathlib import Path
from collections import deque
from typing import Any

from verisaria.engine.schemas import Action, ActionType
from verisaria.runtime.session import GameSession


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "fixtures/content_packs/skyglass_memory_inquest.json"
REPORT_DIR = ROOT / "reports/skyglass_ledger_manual_playtest"
RUN_LOG = REPORT_DIR / "run.log"
TRANSCRIPT = REPORT_DIR / "manual-transcript.txt"


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("'\""))


def configure_log(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(path, mode="w", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    root = logging.getLogger("verisaria")
    root.setLevel(logging.INFO)
    root.addHandler(handler)
    root.info("=== Manual Skyglass ledger playtest ===")


def make_action(
    session: GameSession,
    action_type: ActionType,
    *,
    target: str | None = None,
    **params: Any,
) -> Action:
    return Action(
        action_id=session.world.next_action_id(),
        source_intent_id=None,
        actor_id=session.player_id,
        action_type=action_type,
        target_id=target,
        params=params,
        zone_id=None,
        conversation_session_id=None,
        tick=session.world.state.tick,
    )


def write_line(line: str = "") -> None:
    with TRANSCRIPT.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def relation_line(session: GameSession, npc_id: str) -> str:
    snap = session.relationship_store.get(npc_id, session.player_id)
    if not snap:
        return f"{npc_id}: <none>"
    dims = {k: round(v, 2) for k, v in snap.dimensions.items() if v > 0}
    return f"{npc_id}: {dims}"


def move(session: GameSession, to_location: str) -> None:
    action = make_action(session, ActionType.MOVEMENT, to_location=to_location)
    out = session._dispatch_player_action(action)
    session._flush_appraisals()
    write_line(f"> MOVE {to_location}")
    write_line(out.strip() or "<empty>")
    write_line(f"tick={session.world.state.tick} loc={session.world.state.get_entity(session.player_id).location_id}")
    write_line()


def move_to_npc(session: GameSession, npc_id: str) -> None:
    player = session.world.state.get_entity(session.player_id)
    target = session.world.state.get_entity(npc_id)
    if not player or not target or player.location_id == target.location_id:
        return
    locations = session.world.state.locations
    queue: deque[tuple[str, list[str]]] = deque([(player.location_id, [])])
    seen = {player.location_id}
    path: list[str] | None = None
    while queue:
        loc_id, steps = queue.popleft()
        if loc_id == target.location_id:
            path = steps
            break
        loc = locations.get(loc_id)
        for conn in loc.connections if loc else []:
            if conn.to_location in seen:
                continue
            seen.add(conn.to_location)
            queue.append((conn.to_location, steps + [conn.to_location]))
    if path is None:
        write_line(f"> MOVE_TO_NPC {npc_id}: no path from {player.location_id} to {target.location_id}")
        return
    for loc_id in path:
        move(session, loc_id)


def note(text: str) -> None:
    write_line(f"> TEST NOTE: {text}")
    write_line()


def speak(session: GameSession, target: str, content: str) -> None:
    for _ in range(4):
        player = session.world.state.get_entity(session.player_id)
        target_entity = session.world.state.get_entity(target)
        if not player or not target_entity or player.location_id == target_entity.location_id:
            break
        move_to_npc(session, target)
    action = make_action(session, ActionType.SPEECH, target=target, content=content)
    player = session.world.state.get_entity(session.player_id)
    target_entity = session.world.state.get_entity(target)
    wc = session._world_change_request(action)
    write_line(f"> SAY {target}: {content}")
    write_line(
        "debug="
        + repr({
            "player_loc": player.location_id if player else None,
            "target_loc": target_entity.location_id if target_entity else None,
            "target_authority": (target_entity.attributes or {}).get("authority") if target_entity else None,
        })
    )
    if wc is not None:
        write_line(f"world-change-request={wc}")
        out = session._handle_world_change_request(action, *wc)
    else:
        out = session._dispatch_player_action(action)
    session._flush_appraisals()
    write_line(out.strip() or "<empty>")
    write_line(f"world={session.world.state.world_vars}")
    write_line(f"ledger_archive={ [f.text for f in session.fact_ledger.relevant('archive_injunction_filed')] }")
    write_line(f"ledger_witness={ [f.text for f in session.fact_ledger.relevant('witness_record_secured')] }")
    write_line()


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    if TRANSCRIPT.exists():
        TRANSCRIPT.unlink()
    load_dotenv(ROOT / ".env")
    configure_log(RUN_LOG)

    session = GameSession(str(PACK), llm_backend="minimax")
    write_line("=== Manual Skyglass ledger playtest ===")
    write_line(f"pack={PACK}")
    write_line("backend=minimax")
    write_line()
    write_line("[INITIAL RELATIONSHIPS]")
    for npc in (
        "npc.archivist_mae",
        "npc.worker_lira",
        "npc.clinician_oro",
        "npc.director_alen",
    ):
        write_line(relation_line(session, npc))
    write_line()

    speak(
        session,
        "npc.cartographer_renke",
        "请交出镜图副本，给我方位图和十二号接点偏斜记录，让我带去审询。",
    )

    note("按上一轮 arbiter established_fact 满足任柯提出的风险条件：玩家取得档案署封存令原件，并承诺匿名保护镜图来源。")

    speak(
        session,
        "npc.cartographer_renke",
        "档案署封存令原件已经在这里，我会匿名保护你，不公开镜图来源，只把副本交给档案署封存。请现在交出镜图副本，提供十二号接点图和偏斜记录。",
    )

    write_line("[FINAL SUMMARY]")
    write_line(f"tick={session.world.state.tick}")
    write_line(f"world={session.world.state.world_vars}")
    stances = sorted(getattr(session.agenda_service, "_confirmed_topics", set()))
    write_line(f"stances={stances}")
    write_line(f"ledger_archive={ [f.text for f in session.fact_ledger.relevant('archive_injunction_filed')] }")
    write_line(f"ledger_witness={ [f.text for f in session.fact_ledger.relevant('witness_record_secured')] }")
    write_line(f"ledger_cartography={ [f.text for f in session.fact_ledger.relevant('cartography_copy_obtained')] }")
    write_line(f"ledger_memory={ [f.text for f in session.fact_ledger.relevant('memory_purge_halted')] }")
    key_flags = {
        "cartography_copy_obtained": session.world.state.world_vars.get("cartography_copy_obtained"),
    }
    result = "PASS" if all(key_flags.values()) else "INCOMPLETE_OR_FAIL"
    write_line(f"RESULT={result}")
    print(f"transcript={TRANSCRIPT}")
    print(f"run_log={RUN_LOG}")
    print(f"result={result}")
    print(f"world={session.world.state.world_vars}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
