#!/usr/bin/env python3
"""Validate the SV-1 Starter Village roadmap package."""

from __future__ import annotations

import sys

from starter_village_validator_common import (
    DEPRECATED_STATUSES,
    G7_COUNCIL_REPORT,
    G7_REPORT,
    LEDGER_JSON,
    LEDGER_MD,
    ROADMAP_JSON,
    ROADMAP_MD,
    REQUIRED_PHASES,
    load_json,
    phase_map,
    print_result,
    require_path,
    require_text,
)


def main() -> int:
    failures: list[str] = []
    roadmap = load_json(ROADMAP_JSON, failures)

    require_text(
        ROADMAP_MD,
        [
            "SV-1 INTERNAL STARTER VILLAGE PROOF GATE",
            "OVI-1 Opening Village + Island Production Playable Gate",
            "Street, Lot, and Ground Cohesion Reconstruction",
            "Opening Quest Arc: First Light / Whispers Before Dawn",
            "Autonomous Production Loop",
            "Recurring Screenshot Set",
            "COUNCIL_PASS_READY_FOR_PR",
            "BLOCKED_REQUIRES_HUMAN_ESCALATION",
        ],
        failures,
    )
    require_path(LEDGER_MD, failures, "ledger markdown")
    require_path(LEDGER_JSON, failures, "ledger json")
    require_path(G7_REPORT, failures, "G-7 report")
    require_path(G7_COUNCIL_REPORT, failures, "G-7 council report")

    if isinstance(roadmap, dict):
        if roadmap.get("schema_id") != "wayfarer.sv1.starter_village_playable_obsession_roadmap.v1":
            failures.append("roadmap schema_id mismatch")
        if roadmap.get("milestone_id") != "SV-1":
            failures.append("roadmap milestone_id must be SV-1")
        if roadmap.get("next_human_review_milestone") != "OVI-1 Opening Village + Island Production Playable Gate":
            failures.append("roadmap must point human review to OVI-1")
        if roadmap.get("autonomous_merge_authorized_until") != "OVI-1":
            failures.append("roadmap must authorize ordinary autonomous merge until OVI-1")
        g14_policy = roadmap.get("g14_policy")
        if not isinstance(g14_policy, dict) or g14_policy.get("human_review_required") is not False:
            failures.append("roadmap must record G-14 as internal with human_review_required=false")
        elif "G-15 Opening Island Masterplan + World Topology" not in str(g14_policy.get("next_phase", "")):
            failures.append("roadmap G-14 policy must continue to G-15")
        merge_policy = roadmap.get("merge_policy")
        if not isinstance(merge_policy, dict) or merge_policy.get("ordinary_autonomous_prs_may_merge") is not True:
            failures.append("merge_policy must authorize ordinary autonomous PR merges before OVI-1")
        else:
            required_conditions = " ".join(str(item) for item in merge_policy.get("required_conditions", []))
            for token in ["remote_checks_green", "pr_mergeable", "agent_council_verdict_COUNCIL_PASS_READY_FOR_PR"]:
                if token not in required_conditions:
                    failures.append(f"merge_policy missing required condition: {token}")
        roles = set(str(item) for item in roadmap.get("required_council_roles", []))
        for role in [
            "Scrum Master",
            "Game Designer",
            "World/Layout Designer",
            "Art Director",
            "Animation/NPC Behavior Director",
            "Narrative Designer",
            "UX Designer",
            "Game Programmer",
            "QA Analyst",
            "Build/Release Engineer",
        ]:
            if role not in roles:
                failures.append(f"missing council role: {role}")
        screenshot_set = roadmap.get("recurring_screenshot_set")
        if not isinstance(screenshot_set, list) or len(screenshot_set) < 15:
            failures.append("recurring_screenshot_set must include at least 15 proof items")
        by_phase = phase_map(roadmap, failures)
        for phase_id in REQUIRED_PHASES:
            row = by_phase.get(phase_id, {})
            for key in ["title", "purpose", "objectives", "acceptance", "primary_validators", "status"]:
                if key not in row:
                    failures.append(f"{phase_id} missing {key}")
        if by_phase.get("G-7", {}).get("status") != "PASS":
            failures.append("G-7 roadmap status must be PASS after masterplan lock")
        if by_phase.get("G-14", {}).get("title") != "SV-1 Internal Starter Village Proof Gate":
            failures.append("G-14 must be the internal SV-1 proof gate")
        if "Human review required: no" not in str(by_phase.get("G-14", {})):
            failures.append("G-14 must record Human review required: no")
        serialized = str(roadmap)
        for deprecated in DEPRECATED_STATUSES:
            if deprecated in serialized:
                failures.append(f"roadmap contains deprecated status: {deprecated}")

    return print_result("starter village roadmap", failures, [f"Phases audited: {len(REQUIRED_PHASES)}"])


if __name__ == "__main__":
    sys.exit(main())
