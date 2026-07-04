"""Read-only probe: capture the rendered escort prompt (to confirm traits are
fed) and the arbiter's reason for the escort willingness call. Does NOT modify
engine/pack code — only wraps methods at runtime to record their I/O."""
from __future__ import annotations
import os, sys
from pathlib import Path

ROOT = Path("/Users/gensliu/Documents/rpg")
os.chdir(ROOT); sys.path.insert(0, str(ROOT / "src"))
for raw in (ROOT / ".env").read_text().splitlines():
    line = raw.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip("'\""))

from verisaria.runtime.session import GameSession
from verisaria.engine import arbiter as arb_mod

PACK = "fixtures/content_packs/escort_proving_ground.json"
PLAYER = "player_001"
OUT = ROOT / "reports" / "escort_moved_validation_second_run" / "arbiter_probe.txt"

captured = {}

_orig_prompt = arb_mod.LLMArbiter._build_escort_prompt
def _patched_prompt(self, context):
    p = _orig_prompt(self, context)
    captured["prompt"] = p
    captured["traits"] = list(context.target_traits)
    return p
arb_mod.LLMArbiter._build_escort_prompt = _patched_prompt

_orig_arb = arb_mod.LLMArbiter.arbitrate
def _patched_arb(self, action, world):
    out = _orig_arb(self, action, world)
    if getattr(world, "escort_request", None) or captured.get("prompt"):
        captured["outcome"] = out.arbiter_output.outcome
        captured["reason"] = out.arbiter_output.reason
        captured["confidence"] = out.arbiter_output.confidence
    return out
arb_mod.LLMArbiter.arbitrate = _patched_arb

s = GameSession(PACK, save_dir="_playtest_saves_escort_probe", llm_backend="minimax")
s._progress_sink = lambda m: None
s.run_tick("去院子找安雅")
captured.clear()
s.run_tick("对安雅说：跟我去闸房，把你亲眼见过的上游塌方当面讲给闸官老康听，我现在就带你过去。")

lines = []
lines.append("=== TRAITS FED TO JUDGE ===")
lines.append(repr(captured.get("traits")))
lines.append("\n=== RENDERED ESCORT PROMPT ===")
lines.append(captured.get("prompt", "(none)"))
lines.append("\n=== ARBITER OUTPUT ===")
lines.append(f"outcome  = {captured.get('outcome')}")
lines.append(f"reason   = {captured.get('reason')}")
lines.append(f"confidence = {captured.get('confidence')}")
anya = s.world.state.get_entity("npc.miller_anya")
lines.append(f"\nanya.location_id = {anya.location_id}  (moved? {anya.location_id=='gatehouse'})")
OUT.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
