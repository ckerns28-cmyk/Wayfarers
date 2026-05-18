#!/usr/bin/env python3
"""Validate the final OVI-1 Opening Village + Island production-playable gate."""

from __future__ import annotations

import sys

from opening_village_island_validator_common import (
    REQUIRED_PHASES,
    LEDGER_JSON,
    load_json,
    phase_map,
    print_result,
    validate_common_ledger_contract,
    validate_common_roadmap_contract,
    validate_final_ovi1_artifacts,
)


def main() -> int:
    failures: list[str] = []
    validate_common_roadmap_contract(failures)
    validate_common_ledger_contract(failures)
    ledger = load_json(LEDGER_JSON, failures)
    if isinstance(ledger, dict):
        by_phase = phase_map(ledger, failures)
        for phase_id in REQUIRED_PHASES:
            status = str(by_phase.get(phase_id, {}).get("current_status", ""))
            if status != "PASS":
                failures.append(f"OVI-1 gate not complete: {phase_id} is {status or 'missing'}")
        package = ledger.get("ovi1_review_package")
        if not isinstance(package, dict):
            failures.append("OVI-1 gate not complete: ovi1_review_package is missing")
        else:
            for key in [
                "current_main_commit",
                "clean_worktree_proof",
                "no_open_pr_proof",
                "screenshot_manifest",
                "motion_proof_path",
                "quest_playthrough_path",
                "browser_review_zip_path",
                "agent_council_final_verdict",
            ]:
                if not str(package.get(key, "")).strip():
                    failures.append(f"OVI-1 review package missing {key}")
    validate_final_ovi1_artifacts(failures)
    return print_result("OVI-1 gate", failures)


if __name__ == "__main__":
    sys.exit(main())
