"""Runner: non-deadlock escort-closure line (escort Oro clinic -> archive)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from escort_validation_second_run import run, REPORT_DIR  # noqa: E402

STEPS = [
    # 0. Commit protect-witness stance up front (present-safe wording, keywords
    #    不要清洗 / 事故证词 / 停止校准; no absent-NPC name to avoid coherence bail).
    ("我反对清洗证人记忆。事故证词必须保留下来，不要擦除塔基工人的记忆，应当停止校准流程。",
     "(commit protect_witness_memory stance)"),

    # 1. Walk to the clinic (Oro, the cosigning authority, is here).
    ("goto", "mnemonic_clinic"),

    # 2. Ask Oro about the legal limit — keyword-free discussion that seeds a ledger
    #    fact on the cosign/injunction track.
    ("对奥罗医师说：旧章程要求记忆清洗必须经过档案署见证和可撤回听证。在档案署禁令联签之前，"
     "继续校准是不是违规？",
     "(seed ledger via discussion)"),

    # 3. SLICE-2 FRICTION #1 (short dest 档案署) + #2 (third-party 梅档案官) + ESCORT.
    #    Addressed to co-located Oro; short destination; third-party witness name.
    ("对奥罗医师说：跟我去档案署，当着梅档案官的面把档案署联签办了。",
     "(escort Oro -> archive_stack; friction #1 short-dest + #2 third-party)"),

    # 4. On arrival (archive_stack): face-to-face cosign with Oro present.
    ("对奥罗医师说：我们现在就在档案署，请你为档案署禁令联签，确认白舱可等待可撤回听证，给档案署联签。",
     "(face-to-face: clinician_cosign_obtained)"),

    # 5. Face-to-face file the injunction with Mae, cosigner on-site.
    ("对梅档案官说：奥罗医师已在场并已联签，请你援引旧章程，提交档案署禁令，要求可撤回听证。",
     "(face-to-face: archive_injunction_filed)"),

    # 6. #4 FOLLOW-UP routing: keyword-free substantive follow-up on a ledgered var.
    ("对梅档案官说：那现在到哪一步了？请你继续把这件事办下去。",
     "(#4 keyword-free follow-up routing)"),

    # 7. Let any offscreen process mature.
    ("/wait", ""),
    ("/wait", ""),
    ("/wait", ""),
    ("/world", ""),

    # 8. Terminal closure attempt: with injunction leverage, ask Oro to halt purge.
    #    (Oro is at archive_stack now too, escorted there.)
    ("对奥罗医师说：档案署禁令已经提交，证词必须保留。请暂停记忆清洗，关闭白舱，停止擦除证人记忆。",
     "(terminal: memory_purge_halted)"),
    ("/world", ""),
]

if __name__ == "__main__":
    rc = run(STEPS, REPORT_DIR / "run.log", "out.txt")
    print(f"main run rc={rc}")
    raise SystemExit(rc)
