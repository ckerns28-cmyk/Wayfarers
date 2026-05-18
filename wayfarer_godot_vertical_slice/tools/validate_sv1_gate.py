#!/usr/bin/env python3
"""Validate the internal SV-1/G-14 village proof gate.

This must fail until every Starter Village phase is complete and PASS, but it
must not treat G-14 as a human-review stopping point. The next formal human
review milestone is OVI-1.
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
        g14_policy = ledger.get("g14_policy")
        if not isinstance(g14_policy, dict) or g14_policy.get("human_review_required") is not False:
            failures.append("SV-1 internal gate must record human_review_required=false")
        package = ledger.get("g14_internal_review_package") or ledger.get("sv1_review_package")
        if not isinstance(package, dict):
            failures.append("SV-1 internal gate not complete: g14_internal_review_package is missing")
        elif package.get("human_review_required") is not False:
            failures.append("SV-1 internal package must record human_review_required=false")
    return print_result("SV-1 internal gate", failures)


if __name__ == "__main__":
    sys.exit(main())
