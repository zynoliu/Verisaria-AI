"""Channel-C observability: each world-change adjudication traces the arbiter
verdict, any established fact, and whether the flag flipped — so the fact ledger
is visible on real runs (CLI/TUI --log). Logger only; never a player-facing event."""
from __future__ import annotations

import logging
from types import SimpleNamespace

from verisaria.runtime.session import GameSession
from verisaria.engine.validator import ValidatedOutcome
from verisaria.engine.schemas import ArbiterOutput

PACK = "fixtures/content_packs/frostgate_watchpost.json"
VAR = "refugees_admitted"
AUTH = "npc.captain_brann"


def _capture_channel_c(tmp_path, outcome: str, fact: str | None):
    records: list[str] = []

    class _H(logging.Handler):
        def emit(self, r): records.append(r.getMessage())

    logger = logging.getLogger("verisaria.channel_c")
    h = _H(); logger.addHandler(h); logger.setLevel(logging.INFO)
    try:
        g = GameSession(PACK, save_dir=str(tmp_path), llm_backend="fake")
        ao = ArbiterOutput(arbiter_id="t", source_action_id="a", outcome=outcome,  # type: ignore[arg-type]
                           reason="测试理由", confidence=0.5, established_fact=fact)
        g.arbiter.arbitrate = lambda action, world: ValidatedOutcome(
            accepted=True, arbiter_output=ao,
            accepted_state_changes=[], rejected_state_changes=[])
        g._handle_world_change_request(
            SimpleNamespace(params={"content": "请开城门"}, raw_text="请开城门"), VAR, AUTH)
    finally:
        logger.removeHandler(h)
    return records


def test_channel_c_logs_verdict_and_established_fact(tmp_path):
    msgs = _capture_channel_c(tmp_path, "partial_success", "守军愿松口，条件是先安置老弱")
    joined = "\n".join(msgs)
    assert "world-change" in joined and VAR in joined and "partial_success" in joined
    assert "守军愿松口，条件是先安置老弱" in joined        # the established fact is traced
    assert "ledger" in joined                              # current ledger snapshot logged


def test_channel_c_logs_no_flip_marker_on_partial(tmp_path):
    msgs = _capture_channel_c(tmp_path, "partial_success", "条件未满足")
    assert not any("⟳FLIP" in m for m in msgs)             # partial_success never flips
