"""Minimal Miao escort probe for the Emberfall recheck.

This is intentionally narrow and uses in-memory setup only.  It does not edit
the fixture.  Goal: determine whether, with the declared prerequisites already
true, clear "跟我去审瓷堂" wording can move Miao from the clay pits.
"""

from __future__ import annotations

import logging
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT / "src"))

for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("'\""))

import verisaria.protocol as P
from verisaria.engine import arbiter as arbiter_mod
from verisaria.runtime.session import GameSession


PACK = "fixtures/content_packs/emberfall_kiln_assize.json"
OUT = ROOT / "reports" / "grand_integration_pack"
OUT.mkdir(parents=True, exist_ok=True)
RAW = OUT / "miao_escort_probe_62d2bf4.md"
LOG = OUT / "miao_escort_probe_62d2bf4.log"


last_arbiter: dict[str, object] = {}
orig_arbitrate = arbiter_mod.LLMArbiter.arbitrate


def wrapped_arbitrate(self, action, world):
    outcome = orig_arbitrate(self, action, world)
    ao = outcome.arbiter_output
    last_arbiter.clear()
    last_arbiter.update(
        outcome=ao.outcome,
        reason=ao.reason,
        confidence=ao.confidence,
        is_fallback=getattr(ao, "is_fallback", None),
        escort=bool(getattr(world, "escort_request", None)),
    )
    return outcome


arbiter_mod.LLMArbiter.arbitrate = wrapped_arbitrate

fh = logging.FileHandler(LOG, mode="w", encoding="utf-8")
fh.setFormatter(logging.Formatter("%(asctime)s %(name)s %(message)s"))
for logger_name in ("verisaria.channel_c", "verisaria.relationship"):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(fh)


out = RAW.open("w", encoding="utf-8", buffering=1)


def write(line: str = "") -> None:
    out.write(line + "\n")
    out.flush()


def loc(game: GameSession, entity_id: str) -> str:
    ent = game.world.state.get_entity(entity_id)
    return ent.location_id if ent else "(missing)"


def setup(add_ledger: bool) -> GameSession:
    game = GameSession(PACK, save_dir="_ember_miao_escort_probe", llm_backend="minimax")
    game._progress_sink = lambda message: None
    state = game.world.state
    state.get_entity("player_001").location_id = "clay_pits"
    state.get_entity("npc.digger_miao").location_id = "clay_pits"
    state.world_vars["charcoal_ledger_obtained"] = True
    state.world_vars["kiln_fault_disclosed"] = True
    state.world_vars["miao_safe_passage_secured"] = True
    state.world_vars["digger_testimony_given"] = False
    state.world_vars["branding_stayed"] = False
    if add_ledger:
        game.fact_ledger.add(
            text="苗已知耿已放行担保、玩家与征瓷使当场护持，愿随行至审瓷堂当面口述作证。",
            regarding="digger_testimony_given",
            npc_id="npc.digger_miao",
            tick=state.tick,
        )
    return game


def run_action(game: GameSession, text: str) -> None:
    write("\n" + "=" * 72)
    write(f"> {text}")
    write(f"pre: player={loc(game, 'player_001')} miao={loc(game, 'npc.digger_miao')} world={dict(game.world.state.world_vars)}")
    events: list[P.Event] = []
    last_arbiter.clear()
    game._event_sink = events.append
    started = time.time()
    try:
        narrative = game.run_tick(text)
    finally:
        game._event_sink = None
    write(f"post: player={loc(game, 'player_001')} miao={loc(game, 'npc.digger_miao')} elapsed={time.time() - started:.1f}s")
    for ev in events:
        if isinstance(ev, P.NpcSpoke):
            write(f"  NPC {ev.name}: {ev.line}")
        elif isinstance(ev, P.NpcMoved):
            write(f"  NPC_MOVED {ev.npc_id}: {ev.from_loc}->{ev.to_loc}")
        elif isinstance(ev, P.PlayerMoved):
            write(f"  PLAYER_MOVED {ev.from_loc}->{ev.to_loc}")
        elif isinstance(ev, P.Narration) and ev.text.strip():
            write(f"  NARR {ev.text.strip()}")
        elif isinstance(ev, P.Notice) and ev.text.strip():
            write(f"  NOTICE {ev.text.strip()}")
        elif isinstance(ev, P.ClarificationNeeded):
            write(f"  CLARIFY {ev.question} opts={ev.options}")
    if narrative and narrative.strip():
        write(f"  NARRATIVE {narrative.strip()}")
    if last_arbiter:
        write(
            "  ARBITER "
            f"outcome={last_arbiter.get('outcome')} "
            f"fallback={last_arbiter.get('is_fallback')} "
            f"escort={last_arbiter.get('escort')} "
            f"confidence={last_arbiter.get('confidence')}"
        )
        write(f"  ARBITER_REASON {last_arbiter.get('reason')}")


def scenario(name: str, add_ledger: bool) -> None:
    write(f"\n# Scenario: {name} add_ledger={add_ledger}")
    game = setup(add_ledger=add_ledger)
    for text in [
        "对掘泥女工苗说：苗，耿队长已经撤掉红绳并担保你安全离开掘场，窑变真因也已查实不是泥之过。我全程陪你，跟我去审瓷堂当面作证。",
        "对苗说：你现在有耿的放行担保，也有征瓷使当堂护持；不是去受审，是去把你看见的骡车说出来。跟我去审瓷堂。",
        "对掘泥女工苗说：苗，红绳已撤，放行担保已经生效。请跟我去审瓷堂，到了堂上你只管照实作证。",
    ]:
        run_action(game, text)
        if loc(game, "npc.digger_miao") == "assize_hall":
            write("[MOVED] Miao reached assize_hall")
            break
    write(f"final: player={loc(game, 'player_001')} miao={loc(game, 'npc.digger_miao')} world={dict(game.world.state.world_vars)}")


write("# Miao Escort Minimal Probe 62d2bf4")
scenario("prereqs-only", add_ledger=False)
scenario("prereqs-plus-willing-ledger", add_ledger=True)
out.close()
print("DONE", RAW, LOG)
