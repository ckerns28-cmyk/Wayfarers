#!/usr/bin/env python3
"""Validate the SV-1 autonomous execution ledger structure."""

from __future__ import annotations

import sys

from starter_village_validator_common import (
    ALLOWED_LEDGER_STATUSES,
    DEPRECATED_STATUSES,
    G7_COUNCIL_REPORT,
    G7_REPORT,
    LEDGER_JSON,
    LEDGER_MD,
    ROADMAP_JSON,
    REQUIRED_PHASES,
    load_json,
    phase_map,
    print_result,
    repo_path,
    require_path,
    require_text,
)


def validate_phase_row(phase_id: str, row: dict, failures: list[str]) -> None:
    status = str(row.get("current_status", "")).strip()
    if status not in ALLOWED_LEDGER_STATUSES:
        failures.append(f"{phase_id} invalid current_status: {status}")
    for key in ["phase_name", "branch", "implementing_prs", "commits", "current_status", "reason_for_status", "next_required_action"]:
        if key not in row or not str(row.get(key, "")).strip():
            failures.append(f"{phase_id} missing {key}")
    if phase_id == "G-7":
        if status != "PASS":
            failures.append("G-7 must be PASS after masterplan lock")
        if row.get("agent_council_verdict") != "COUNCIL_PASS_READY_FOR_PR":
            failures.append("G-7 council verdict must be COUNCIL_PASS_READY_FOR_PR")
        for raw_path in row.get("screenshot_paths", []):
            if not repo_path(str(raw_path)).exists():
                failures.append(f"G-7 missing screenshot evidence: {raw_path}")
        for required in [G7_REPORT, G7_COUNCIL_REPORT]:
            if not required.exists():
                failures.append(f"G-7 missing evidence file: {required}")


def main() -> int:
    failures: list[str] = []
    ledger = load_json(LEDGER_JSON, failures)

    require_text(
        LEDGER_MD,
        [
            "SV-1 STARTER VILLAGE PLAYABLE OBSESSION GATE",
            "PR #461 result: already merged",
            "Autonomous merge-governance result",
            "Street, Lot, and Ground Cohesion Reconstruction",
        ],
        failures,
    )
    require_path(ROADMAP_JSON, failures, "roadmap json")
    require_path(G7_REPORT, failures, "G-7 report")
    require_path(G7_COUNCIL_REPORT, failures, "G-7 council report")

    if isinstance(ledger, dict):
        if ledger.get("schema_id") != "wayfarer.sv1.autonomous_execution_ledger.v1":
            failures.append("ledger schema_id mismatch")
        if ledger.get("milestone_id") != "SV-1":
            failures.append("ledger milestone_id must be SV-1")
        governance = ledger.get("autonomous_merge_governance")
        if not isinstance(governance, dict) or governance.get("per_pr_chris_approval_removed_as_recurring_blocker") is not True:
            failures.append("ledger must record recurring per-PR merge approval blocker removal")
        merged = ledger.get("pr_461_merge_result")
        if not isinstance(merged, dict) or merged.get("state") != "MERGED" or merged.get("contained_in_main") is not True:
            failures.append("ledger must record PR #461 as merged and contained in main")
        by_phase = phase_map(ledger, failures)
        for phase_id in REQUIRED_PHASES:
            row = by_phase.get(phase_id)
            if isinstance(row, dict):
                if str(row.get("current_status", "")) in DEPRECATED_STATUSES:
                    failures.append(f"{phase_id} uses deprecated current_status")
                if str(row.get("agent_council_verdict", "")) in DEPRECATED_STATUSES:
                    failures.append(f"{phase_id} uses deprecated council verdict")
                validate_phase_row(phase_id, row, failures)

    return print_result("starter village execution ledger", failures, [f"Rows audited: {len(REQUIRED_PHASES)}"])


if __name__ == "__main__":
    sys.exit(main())
