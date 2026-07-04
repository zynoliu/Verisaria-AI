"""Final focused attempt at escort success ⟳MOVED with the most willing NPC (Tamsin).

Tamsin: courier_union, deal_maker, transactional_trust, loyal_to_valley, smuggler.
She runs the secret maintenance ladder (union_secret_route) — escorting her toward
the gantry/ladder to extract a witness is squarely in-character and helps the witness
chain. We build a concrete transactional offer first, then escort with a destination
phrased to avoid the location-name-as-ambiguity friction (use 旧检修梯 / transit_ladder).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from escort_validation_second_run import run, REPORT_DIR  # noqa: E402

STEPS = [
    ("goto", "valley_platform"),

    # Build transactional rapport — offer something concrete for the valley.
    ("对信使塔姆辛说：我能在听证厅替低谷家庭争取热能通行证，但我需要你帮个忙——你最熟那条旧检修梯。",
     "(rapport: offer a deal)"),

    # Escort toward the ladder (adjacent to valley_platform). Use the location id to
    # dodge the location-name-as-ambiguity friction.
    ("对信使塔姆辛说：跟我去 transit_ladder，就走你那条旧检修梯，我们一起把证人接出来，"
     "事成我保证低谷拿到通行证。",
     "(ESCORT: Tamsin -> transit_ladder, success ⟳MOVED expected)"),

    # Retry with full place-name framing if needed.
    ("对信使塔姆辛说：跟我去旧检修梯，现在就走，我跟你一起。",
     "(ESCORT retry)"),

    ("/world", ""),
]

if __name__ == "__main__":
    rc = run(STEPS, REPORT_DIR / "run-tamsin.log", "out-tamsin.txt")
    print(f"tamsin run rc={rc}")
    raise SystemExit(rc)
