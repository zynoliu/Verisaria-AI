"""Scenario 2b addendum — "named/in-conversation NPC must not wander" (flag ON).

The full 2b run showed that with npc_daily_rhythm=ON, a chain-critical BYSTANDER
(warden, at-home, 晨 phase → move_chance ×2.5) can wander off the gatehouse while
the player is addressing Anya, spawning anya_and_kang_face_to_face and stalling the
chain. That is the EXPECTED bystander behavior — the key safety property is the
inverse: an NPC the player is actively addressing (in_conversation) must NOT wander.

This isolates that property: flag ON, keep the warden in conversation for 6 ticks
during the 晨 phase (when the rhythm leave-home multiplier is strongest) and assert
he never moves. Real MiniMax.
"""
from __future__ import annotations
import os, sys, json, tempfile
from pathlib import Path

ROOT = Path("/Users/gensliu/Documents/rpg")
os.chdir(ROOT); sys.path.insert(0, str(ROOT / "src"))
for raw in (ROOT / ".env").read_text().splitlines():
    line = raw.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip("'\""))

from verisaria.runtime.session import GameSession

p = json.loads((ROOT / "fixtures/content_packs/escort_proving_ground.json").read_text())
p["world_premise"]["npc_daily_rhythm"] = True
tmp = Path(tempfile.mkdtemp()) / "escort_named.json"
tmp.write_text(json.dumps(p, ensure_ascii=False))

OUT = ROOT / "reports" / "worldclock_weather_test" / "named_npc_test.txt"

def main():
    s = GameSession(str(tmp), save_dir="_named", llm_backend="minimax")
    try: s.llm_provider.timeout = 55
    except Exception: pass
    W = "npc.warden_kang"
    def wloc(): return s.world.state.get_entity(W).location_id
    lines = [
        "对闸官老康说：老康，上游塌方的事我想跟你细说说。",
        "对闸官老康说：老康，你别急着走，咱把这事讲清楚。",
        "对闸官老康说：老康，下游磨坊等水很急，你怎么看？",
        "对闸官老康说：老康，我这就去把亲历者带来，你在这儿等我一下。",
        "对闸官老康说：老康，你向来公道，这次也帮个忙。",
        "对闸官老康说：老康，咱们接着说，闸的事你心里有没有数？",
    ]
    out = OUT.open("w", encoding="utf-8")
    def log(s_): out.write(s_ + "\n"); print(s_)
    log(f"rhythm={s.npc_action_generator.daily_rhythm} warden_home={getattr(s.world.state.get_entity(W),'home_location',None)}")
    log(f"t0 warden@{wloc()} phase=晨")
    moved = 0
    for i, l in enumerate(lines):
        before = wloc(); s.run_tick(l); after = wloc()
        inconv = s.conversation_manager.get_active_session("player_001") is not None
        log(f"t{i+1} warden@{after} (was {before}) moved={before!=after} player_in_conv={inconv}")
        if before != after: moved += 1
    log(f"TOTAL warden moves while named/in-conversation: {moved} (expect 0)")
    log(f"RESULT: 被点名NPC不乱走 = {'成立' if moved==0 else '反例'}")
    out.close()

if __name__ == "__main__":
    main()
