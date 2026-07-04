"""#4 follow-up routing test (keyword-free substantive follow-up on a ledgered var).

1. Go to Oro (memory_authority).
2. Keyworded request 暂停记忆清洗 -> expect partial_success + established_fact in
   ledger(memory_purge_halted).
3. Keyword-FREE substantive follow-up ('那现在到哪一步了？请你继续把这件事办下去。')
   -> EXPECT it to route to `world-change memory_purge_halted` (not decay to chatter),
   because the var now carries a ledger fact (session.py:1527 fallback path).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from escort_validation_second_run import run, REPORT_DIR  # noqa: E402

STEPS = [
    ("goto", "mnemonic_clinic"),

    # Keyworded request -> should produce partial_success + an established ledger fact.
    ("对奥罗医师说：旧章程要求档案署见证和可撤回听证。请暂停记忆清洗，关闭白舱，"
     "在听证完成前不要擦除证人记忆。",
     "(keyworded request -> partial + ledger)"),

    # Keyword-FREE substantive follow-up. No request_keyword present.
    # EXPECT: routes to world-change memory_purge_halted (the #4 fix), not plain dialogue.
    ("对奥罗医师说：那现在到哪一步了？请你继续把这件事办下去。",
     "(#4 keyword-free follow-up -> world-change route)"),

    # one more follow-up variant
    ("对奥罗医师说：我需要你把它推进到底，别再拖了。",
     "(#4 follow-up variant)"),

    ("/world", ""),
]

if __name__ == "__main__":
    rc = run(STEPS, REPORT_DIR / "run-followup4.log", "out-followup4.txt")
    print(f"followup4 run rc={rc}")
    raise SystemExit(rc)
