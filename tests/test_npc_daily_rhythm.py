"""Slice 3 — opt-in daily rhythm: time of day biases NPC home/away movement.
By day NPCs leave home to mill about; by dusk/night they head home and settle.
OFF by default → P1.8 home anchoring is byte-identical. See
docs/design/worldclock-and-weather.md."""
from __future__ import annotations

from verisaria.engine.world import WorldState, EntityState, LocationState, Connection
from verisaria.engine import npc_runtime as NR
from verisaria.engine.npc_runtime import NPCActionGenerator
from verisaria.engine.schemas import ActionType

PACK = "fixtures/content_packs/frostgate_watchpost.json"
DAY = 12 * 60     # 12:00 → 昼
NIGHT = 22 * 60   # 22:00 → 夜


# -- pure schedule helpers --

def test_multiplier_pulls_home_at_night_disperses_by_day():
    assert NR.schedule_move_multiplier("夜", away_from_home=True) > 1.0   # hurry home
    assert NR.schedule_move_multiplier("夜", away_from_home=False) < 1.0  # settle in
    assert NR.schedule_move_multiplier("昼", away_from_home=False) > 1.0  # leave home
    assert NR.schedule_move_multiplier("昼", away_from_home=True) == 1.0  # mill about


def test_prefers_home_only_at_dusk_and_night():
    assert NR.prefers_home_now("夜") and NR.prefers_home_now("暮")
    assert not NR.prefers_home_now("昼") and not NR.prefers_home_now("晨")


# -- movement direction (deterministic) --

def _world(clock_minutes, npc_loc="post", home="home"):
    w = WorldState(clock_minutes=clock_minutes)
    w.locations["post"] = LocationState(location_id="post", connections=[
        Connection(to_location="home"), Connection(to_location="market")])
    w.locations["home"] = LocationState(location_id="home",
                                        connections=[Connection(to_location="post")])
    w.locations["market"] = LocationState(location_id="market",
                                          connections=[Connection(to_location="post")])
    npc = EntityState(entity_id="npc.x", entity_type="npc",
                      location_id=npc_loc, home_location=home)
    w.entities["npc.x"] = npc
    return w, npc


def _dest(gen, world, npc):
    return gen._make_movement("a", "npc.x", npc, world, tick=0).params["to_location"]


def test_rhythm_on_heads_home_at_night():
    gen = NPCActionGenerator(seed=1)
    gen.daily_rhythm = True
    world, npc = _world(NIGHT)
    assert _dest(gen, world, npc) == "home"   # away + dusk/night → straight home


def test_rhythm_on_does_not_force_home_by_day():
    # by day the home-pull is off, so an away NPC wanders (sometimes to a non-home exit)
    world, npc = _world(DAY)
    seen = set()
    for seed in range(40):
        gen = NPCActionGenerator(seed=seed)
        gen.daily_rhythm = True
        seen.add(_dest(gen, world, npc))
    assert "market" in seen   # not yanked home — proves the day branch wanders


def test_rhythm_off_preserves_p18_home_anchor_even_by_day():
    gen = NPCActionGenerator(seed=1)  # daily_rhythm defaults False
    world, npc = _world(DAY)
    assert gen.daily_rhythm is False
    assert _dest(gen, world, npc) == "home"  # P1.8: away + home reachable → home


def test_no_home_means_no_rhythm_effect():
    # an NPC without a home is unaffected by the rhythm (the multiplier is gated on home)
    gen = NPCActionGenerator(seed=1)
    gen.daily_rhythm = True
    world, npc = _world(NIGHT, home=None)
    # with no home, _make_movement just picks a random connection (never crashes)
    assert _dest(gen, world, npc) in {"home", "market"}


# -- stationed: a key NPC holds its post (slice 3c) --

def test_stationed_npc_never_autonomously_moves_even_under_rhythm(tmp_path):
    # a stationed at-home NPC, by day (×2.5 leave), must still never wander off
    gen = NPCActionGenerator(seed=1)
    gen.daily_rhythm = True
    world, npc = _world(DAY, npc_loc="home")  # at its post
    npc.stationed = True
    for seed in range(60):
        gen2 = NPCActionGenerator(seed=seed)
        gen2.daily_rhythm = True
        act = gen2._generate_for_npc("npc.x", npc, world, tick=0, in_conversation=False)
        assert act.action_type != ActionType.MOVEMENT  # holds post; talks/looks/waits only


def test_non_stationed_default_unchanged(tmp_path):
    # default stationed=False → the rhythm still disperses by day (proves the gate
    # is the only difference)
    world, npc = _world(DAY, npc_loc="home")
    assert getattr(npc, "stationed", False) is False
    moved = False
    for seed in range(60):
        gen = NPCActionGenerator(seed=seed)
        gen.daily_rhythm = True
        act = gen._generate_for_npc("npc.x", npc, world, tick=0, in_conversation=False)
        if act.action_type == ActionType.MOVEMENT:
            moved = True
            break
    assert moved  # a non-stationed at-home NPC does leave sometimes by day


def test_loader_reads_stationed_flag(tmp_path):
    from verisaria.engine.campaign_loader import CampaignLoader
    from verisaria.engine.world import WorldState
    pack, state, _ = CampaignLoader.load_or_fallback(PACK)
    # frostgate declares no stationed NPCs → all default False
    assert all(not getattr(e, "stationed", False)
               for e in state.entities.values() if e.entity_type == "npc")


# -- pack opt-in wiring --

def test_pack_defaults_to_rhythm_off(tmp_path):
    from verisaria.runtime.session import GameSession
    g = GameSession("fixtures/content_packs/frostgate_watchpost.json",
                    save_dir=str(tmp_path), llm_backend="fake")
    assert g.npc_action_generator.daily_rhythm is False  # no pack flag → unchanged behaviour


def test_pack_can_opt_into_rhythm(tmp_path, monkeypatch):
    from verisaria.runtime.session import GameSession
    from verisaria.engine.campaign_loader import CampaignLoader
    real = CampaignLoader.load_or_fallback

    def _wrapped(path):
        pack, state, validation = real(path)
        pack.world_premise.npc_daily_rhythm = True
        return pack, state, validation

    monkeypatch.setattr(CampaignLoader, "load_or_fallback", staticmethod(_wrapped))
    g = GameSession("fixtures/content_packs/frostgate_watchpost.json",
                    save_dir=str(tmp_path), llm_backend="fake")
    assert g.npc_action_generator.daily_rhythm is True
