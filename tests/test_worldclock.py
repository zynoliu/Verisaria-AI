"""World clock — variable in-world time keyed off the pacing verdict (not tick×const),
plus time-of-day derivation. Pure functions; see docs/design/worldclock-and-weather.md."""
from __future__ import annotations

import pytest

from verisaria.engine import worldclock as wc
from verisaria.engine.schemas import PacingSpeed


def test_minutes_per_step_scales_with_pacing_density():
    # a charged beat (conversation/combat) is short; a quiet fast-forward step is long
    assert wc.minutes_for_step(PacingSpeed.PAUSE) < wc.minutes_for_step(PacingSpeed.SLOW)
    assert wc.minutes_for_step(PacingSpeed.SLOW) < wc.minutes_for_step(PacingSpeed.FORCE)
    assert wc.minutes_for_step(PacingSpeed.FORCE) < wc.minutes_for_step(PacingSpeed.FAST)
    # an unknown/None speed falls back to the SLOW (ordinary-beat) weight
    assert wc.minutes_for_step(None) == wc.minutes_for_step(PacingSpeed.SLOW)


def test_variable_flow_a_conversation_is_minutes_a_skip_is_hours():
    # 1 SLOW step ≈ a few minutes; a quiet fast-forward (FAST, 2 steps) ≈ ~an hour
    convo = wc.minutes_for_step(PacingSpeed.SLOW)
    skip = wc.minutes_for_step(PacingSpeed.FAST) * 2
    assert convo <= 5
    assert skip >= 45              # the whole point: a tick's scale isn't fixed


@pytest.mark.parametrize("minutes,phase,glyph", [
    (6 * 60, "晨", "🌅"),
    (12 * 60, "昼", "☀️"),
    (18 * 60, "暮", "🌆"),
    (22 * 60, "夜", "🌙"),
    (2 * 60, "夜", "🌙"),          # after midnight is still 夜
])
def test_time_of_day_phases(minutes, phase, glyph):
    label = wc.time_of_day(minutes)
    assert label.phase == phase and label.glyph == glyph


def test_time_of_day_wraps_past_one_day():
    # day 2, 06:30 → still 晨, and the hour resets
    minutes = 1440 + 6 * 60 + 30
    label = wc.time_of_day(minutes)
    assert label.phase == "晨" and label.hour == 6


def test_clock_label_shows_day_and_hhmm():
    assert wc.clock_label(6 * 60 + 30) == "第1天 06:30"
    assert wc.clock_label(1440 + 18 * 60 + 5) == "第2天 18:05"


def test_parse_opening_time_accepts_hhmm_and_named_phases():
    assert wc.parse_opening_time("18:30") == 18 * 60 + 30
    assert wc.parse_opening_time("06:00") == 6 * 60
    # a named phase maps to a representative hour
    assert wc.time_of_day(wc.parse_opening_time("黄昏")).phase == "暮"
    assert wc.time_of_day(wc.parse_opening_time("清晨")).phase == "晨"
    # unknown / missing → default opening (08:00)
    assert wc.parse_opening_time(None) == wc.DEFAULT_OPENING_MINUTES == 8 * 60
    assert wc.parse_opening_time("nonsense") == wc.DEFAULT_OPENING_MINUTES


# -- wired into the engine --

def test_tick_advance_moves_clock_by_minutes():
    from verisaria.engine.world import WorldCore, WorldState
    w = WorldCore(initial_state=WorldState())
    start = w.state.clock_minutes
    w.tick_advance(7)
    assert w.state.tick == 1 and w.state.clock_minutes == start + 7
    w.tick_advance()  # default = an ordinary SLOW beat, not a fixed constant
    assert w.state.clock_minutes == start + 7 + wc.minutes_for_step(None)


def test_session_wait_advances_world_clock(tmp_path):
    from verisaria.runtime.session import GameSession
    g = GameSession("fixtures/content_packs/frostgate_watchpost.json",
                    save_dir=str(tmp_path), llm_backend="fake")
    before = g.world.state.clock_minutes
    g.run_tick("")  # the player waits one beat → in-world time moves on
    assert g.world.state.clock_minutes > before


def test_pack_opening_time_sets_starting_clock(tmp_path, monkeypatch):
    # a pack that opens at dusk starts the clock there rather than the 08:00 default
    from verisaria.runtime.session import GameSession
    from verisaria.engine.campaign_loader import CampaignLoader
    real = CampaignLoader.load_or_fallback  # bound classmethod

    def _wrapped(path):
        pack, state, validation = real(path)
        pack.world_premise.opening_time = "黄昏"
        return pack, state, validation

    monkeypatch.setattr(CampaignLoader, "load_or_fallback", staticmethod(_wrapped))
    g = GameSession("fixtures/content_packs/frostgate_watchpost.json",
                    save_dir=str(tmp_path), llm_backend="fake")
    assert wc.time_of_day(g.world.state.clock_minutes).phase == "暮"
