#!/usr/bin/env python3
"""Validate the final SV-1 gate.

This must fail until every Starter Village phase is complete and PASS.
"""

from __future__ import annotations

import sys

from starter_village_validator_common import LEDGER_JSON, REQUIRED_PHASES, load_json, phase_map, print_result


def main() -> int:
    failures: list[str] = []
    ledger = load_json(LEDGER_JSON, failures)
    if isinstance(ledger, dict):
        by_phase = phase_map(ledger, failures)
        for phase_id in REQUIRED_PHASES:
            status = str(by_phase.get(phase_id, {}).get("current_status", ""))
            if status != "PASS":
                failures.append(f"SV-1 gate not complete: {phase_id} is {status or 'missing'}")
        sv1_package = ledger.get("sv1_review_package")
        if not isinstance(sv1_package, dict):
            failures.append("SV-1 gate not complete: sv1_review_package is missing")
    return print_result("SV-1 gate", failures)


if __name__ == "__main__":
    sys.exit(main())
