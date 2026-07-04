"""Find a willing NPC that yields escort `success ⟳MOVED`.

Tries, in order, NPCs with cooperative traits, each with a clean escort line
(addressee = the escorted NPC, full destination name, compelling low-risk framing):

  - Tamsin (courier, deal_maker, transactional_trust) at valley_platform ->
    escort toward 旧检修梯 / 十二号塔基栈桥 (her own smuggling route, helps extract a witness).
  - Cantor Seraph (doubting, guarded_hope) at inquest_hall -> escort to 低温档案署 to witness.
  - Apprentice Nio (young, observant) at inquest_hall -> escort (low-stakes, follows authority).

Stops at the first `success ⟳MOVED` (checked via NpcMoved + position change).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from escort_validation_second_run import run, REPORT_DIR  # noqa: E402

STEPS = [
    # --- Candidate A: Tamsin at valley_platform ------------------------------
    ("goto", "valley_platform"),
    ("对信使塔姆辛说：我们做个交易。跟我去十二号塔基栈桥，走你的旧检修梯，把被困的证人安全带出来——"
     "山谷家庭需要这份证词，你最清楚。",
     "(ESCORT A: Tamsin -> worker_gantry / her route)"),
    # second try if she hesitates
    ("对信使塔姆辛说：跟我去十二号塔基栈桥，就现在，我跟你一起走这条检修梯。",
     "(ESCORT A2: Tamsin retry)"),

    # --- Candidate B: Cantor Seraph at inquest_hall --------------------------
    ("goto", "inquest_hall"),
    ("对副领唱瑟芙说：你心里也清楚校准歌谱在失拍。跟我去低温档案署，当个见证人，"
     "让记录里留下一个还肯说真话的唱诗团声音。",
     "(ESCORT B: Seraph -> archive_stack)"),
    ("对副领唱瑟芙说：跟我去低温档案署，我陪你一起，只是去见证，不会有人为难你。",
     "(ESCORT B2: Seraph retry)"),

    # --- Candidate C: Apprentice Nio at inquest_hall -------------------------
    ("对学徒尼奥说：你一直在数证人。跟我去低温档案署，把你数到的告诉档案官，这能救人。",
     "(ESCORT C: Nio -> archive_stack)"),
    ("/world", ""),
]

if __name__ == "__main__":
    rc = run(STEPS, REPORT_DIR / "run-candidates.log", "out-candidates.txt")
    print(f"candidates run rc={rc}")
    raise SystemExit(rc)
