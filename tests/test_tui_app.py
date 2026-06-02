"""TUI app smoke test: input → worker-threaded tick streams events → status advances.
Driven via asyncio.run (no pytest-asyncio dependency)."""
from __future__ import annotations

import asyncio

from textual.widgets import Input

from verisaria.protocol.engine_session import EngineSession
from verisaria.frontends.tui.app import VerisariaApp
from verisaria import protocol as P
from verisaria.engine.schemas import ParsedIntent, ActionType, CommitmentLevel

PACK = "fixtures/content_packs/frostgate_watchpost.json"


def test_tui_submit_streams_events_and_advances_tick(tmp_path):
    es = EngineSession.start(PACK, save_dir=str(tmp_path), llm_backend="fake")
    es.game.intent_parser.parse = lambda raw_text, **kw: ParsedIntent(
        intent_id="i", source="natural_language", raw_text=raw_text,
        intent_type=ActionType.SPEECH, actor_id="player_001",
        target_id="npc.captain_brann", content="你好，队长。", modifiers={},
        commitment=CommitmentLevel.COMMITTED, confidence=0.9,
        performed_content=raw_text, timestamp=0,
    )
    app = VerisariaApp(es)
    seen: list = []
    snaps: list = []  # snapshots the app refreshed its panels with

    async def scenario():
        async with app.run_test() as pilot:
            on_ev, refresh = app._on_event, app._refresh_panels
            app._on_event = lambda ev: (seen.append(ev), on_ev(ev))
            app._refresh_panels = lambda s: (snaps.append(s), refresh(s))
            app.query_one("#input", Input).value = "对队长布兰说：你好。"
            await pilot.press("enter")
            await app.workers.wait_for_complete()
            await pilot.pause()
            assert app._busy is False  # input re-enabled after the tick

    asyncio.run(scenario())

    assert any(isinstance(e, P.PlayerSpoke) for e in seen)
    assert any(isinstance(e, P.TickAdvanced) for e in seen)
    # the app refreshed its sidebar panels with a post-tick snapshot carrying the
    # world var + the co-located NPCs (what render_nearby / render_world draw).
    last = snaps[-1]
    assert any(w.var_id == "refugees_admitted" for w in last.world_vars)
    assert any(e.name in ("captain_brann", "sentry_voss") for e in last.present)
