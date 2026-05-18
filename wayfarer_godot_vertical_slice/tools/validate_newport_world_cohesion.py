#!/usr/bin/env python3
"""Validate the Newport world-cohesion masterplan and runtime references."""

from __future__ import annotations

import sys

from starter_village_validator_common import (
    BLUEPRINT,
    G7_COUNCIL_REPORT,
    G7_REPORT,
    ROADMAP_JSON,
    ROADMAP_MD,
    load_json,
    print_result,
    repo_path,
    require_text,
)


def main() -> int:
    failures: list[str] = []
    roadmap = load_json(ROADMAP_JSON, failures)
    blueprint = require_text(
        BLUEPRINT,
        [
            "starter_district_plan",
            "district_identity",
            "street_grammar",
            "waterfront_avenue_parallel_to_harbor",
            "back_street_behind_waterfront_road",
            "walking_loop_specs",
            "interaction_anchors",
            "tavern_inn_entrance",
            "town_hall_entrance",
            "dock_worker_west",
        ],
        failures,
    )
    require_text(
        G7_REPORT,
        [
            "Locked Town Grammar",
            "Player Arrival Route",
            "District Purpose And Building Reasons",
            "Opening Quest Beat Map",
            "NPC Work/Life Route Contract",
            "G-7A Repair Instructions",
        ],
        failures,
    )
    require_text(
        G7_COUNCIL_REPORT,
        [
            "COUNCIL_PASS_READY_FOR_PR",
            "World/Layout Designer",
            "runtime screenshot remains",
            "known failing baseline",
        ],
        failures,
    )
    require_text(ROADMAP_MD, ["town cohesion is approximately 2/10", "G-7A"], failures)

    if isinstance(roadmap, dict):
        baseline = roadmap.get("baseline")
        if not isinstance(baseline, dict):
            failures.append("roadmap baseline must be an object")
        else:
            if float(baseline.get("town_cohesion_score", 0.0)) != 2.0:
                failures.append("baseline town cohesion must preserve Chris's 2/10 signal")
            for raw_path in baseline.get("evidence", []):
                if not repo_path(str(raw_path)).exists():
                    failures.append(f"baseline screenshot evidence missing: {raw_path}")
        phases = {str(row.get("phase_id", "")): row for row in roadmap.get("phases", []) if isinstance(row, dict)}
        g7a = phases.get("G-7A", {})
        if "town_cohesion_at_least_7_5" not in str(g7a):
            failures.append("G-7A acceptance must require town cohesion at least 7.5")
        g14 = phases.get("G-14", {})
        if "town_cohesion_score_at_least_8_5" not in str(g14):
            failures.append("G-14 acceptance must require town cohesion at least 8.5")

    for token in ["harbor_loop", "market_loop", "civic_residential_loop"]:
        if token not in blueprint:
            failures.append(f"blueprint missing walking loop token: {token}")

    return print_result(
        "newport world cohesion masterplan",
        failures,
        ["Current runtime cohesion baseline remains failing; G-7A must repair it."],
    )


if __name__ == "__main__":
    sys.exit(main())
