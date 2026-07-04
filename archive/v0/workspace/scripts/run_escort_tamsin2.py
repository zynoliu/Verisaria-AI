"""Final clean escort-MOVED attempt: Tamsin (willing) -> 低温档案署 (resolver-safe name).

Uses 低温档案署 (full location name) which the destination resolver handles and which
did NOT get flagged as a generic ambiguity in earlier runs. Tamsin already showed
willingness ('你先跟我下廊道'); pairing willingness with a resolvable destination is
the cleanest shot at `escort ... success ⟳MOVED`.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from escort_validation_second_run import run, REPORT_DIR  # noqa: E402

STEPS = [
    ("goto", "valley_platform"),
    ("对信使塔姆辛说：低谷家庭需要那份事故证词才能拿到热能通行证，你最清楚。我需要你陪我跑一趟。",
     "(rapport)"),
    ("对信使塔姆辛说：跟我去低温档案署，我陪你一起走，把证词交给档案官封存，事成低谷就能拿通行证。",
     "(ESCORT: Tamsin -> 低温档案署, success ⟳MOVED expected)"),
    ("对信使塔姆辛说：我们一起去低温档案署，现在就走，你带路。",
     "(ESCORT retry)"),
    ("/world", ""),
]

if __name__ == "__main__":
    rc = run(STEPS, REPORT_DIR / "run-tamsin2.log", "out-tamsin2.txt")
    print(f"tamsin2 run rc={rc}")
    raise SystemExit(rc)
