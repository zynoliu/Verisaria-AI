"""Focused run: produce escort `success ⟳MOVED` then on-site closure.

Build rapport with a willing co-located NPC, then escort. We try the courier
Tamsin (deal_maker, union_authority) at valley_platform escorted toward the
archive route is too far; instead we use Mae (archive_authority) who is mobile
and shares the legal goal, OR Oro after trust-building. This script:
  1. go to clinic, build common cause with Oro across a couple turns,
  2. issue a strong, reassuring escort to 低温档案署 (full name, legal framing),
  3. if MOVED, file injunction + cosign on-site -> closure.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from escort_validation_second_run import run, REPORT_DIR  # noqa: E402

STEPS = [
    ("goto", "mnemonic_clinic"),

    # Build common cause — agree on the legal violation, lower defensiveness.
    ("对奥罗医师说：我不是来追究你的。旧章程白纸黑字写着，没有档案署联签就清洗是违规的，"
     "真出事审计第一个查的是你。我们利益一致，我来替你把程序补齐。",
     "(rapport 1)"),
    ("对奥罗医师说：梅档案官就在低温档案署等着，只要你当面在场，联签和禁令一次就能办完，"
     "白舱可以合法等可撤回听证，没人会怪你。",
     "(rapport 2: set up the offer)"),

    # Strong escort — full destination name, reassurance, legality, companionship.
    ("对奥罗医师说：跟我去低温档案署，我陪你一起走，当面把联签办了。这是合法听证，几分钟就回来。",
     "(ESCORT attempt: success ⟳MOVED expected)"),

    # If moved: on-site cosign with Oro, file injunction with Mae.
    ("对奥罗医师说：我们已经在低温档案署了，请你现在为档案署禁令联签，确认白舱可等待可撤回听证，给档案署联签。",
     "(on-site: clinician_cosign_obtained)"),
    ("对梅档案官说：奥罗医师已在场联签，请你援引旧章程，提交档案署禁令，要求可撤回听证。",
     "(on-site: archive_injunction_filed)"),

    # #4 keyword-free follow-up on the (now ledgered) injunction var.
    ("对梅档案官说：那现在到哪一步了？请你继续把这件事办下去。",
     "(#4 keyword-free follow-up)"),

    ("/wait", ""), ("/wait", ""), ("/wait", ""),
    ("/world", ""),

    # Terminal: with injunction, ask Oro to halt the purge.
    ("对奥罗医师说：档案署禁令已经提交，证词必须保留。请暂停记忆清洗，关闭白舱，停止擦除证人记忆。",
     "(terminal: memory_purge_halted)"),
    ("/world", ""),
]

if __name__ == "__main__":
    rc = run(STEPS, REPORT_DIR / "run-moved.log", "out-moved.txt")
    print(f"moved run rc={rc}")
    raise SystemExit(rc)
