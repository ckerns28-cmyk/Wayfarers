#!/usr/bin/env python3
"""Validate the internal SV-1/G-14 village proof gate.

This must fail until every Starter Village phase is complete and PASS, but it
must not treat G-14 as a human-review stopping point. The next formal human
review milestone is OVI-1.
"""

from __future__ import annotations

import sys

from starter_village_validator_common import REPO_ROOT, LEDGER_JSON, REQUIRED_PHASES, load_json, phase_map, print_result, require_text


G14_PACKAGE_MD = REPO_ROOT / "docs" / "reports" / "G14_INTERNAL_STARTER_VILLAGE_PROOF_GATE.md"
G14_PACKAGE_JSON = REPO_ROOT / "docs" / "reports" / "G14_INTERNAL_STARTER_VILLAGE_PROOF_GATE.json"


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
        else:
            for key in ["package_markdown", "package_json", "screenshot_manifest", "browser_review_zip", "next_phase"]:
                if not str(package.get(key, "")).strip():
                    failures.append(f"SV-1 internal package missing {key}")
            if package.get("next_phase") != "G-15 Opening Island Masterplan + World Topology":
                failures.append("SV-1 internal package must continue to G-15")
    require_text(
        G14_PACKAGE_MD,
        [
            "G-14 Internal Starter Village Proof Gate",
            "Human review required: no",
            "Reason: G-14 is now an internal checkpoint inside the larger OVI-1 autonomous",
            "Next phase: G-15 Opening Island Masterplan + World Topology",
            "COUNCIL_PASS_READY_FOR_PR",
        ],
        failures,
    )
    package_json = load_json(G14_PACKAGE_JSON, failures)
    if isinstance(package_json, dict):
        if package_json.get("status") != "PASS":
            failures.append("G-14 package JSON status must be PASS")
        if package_json.get("human_review_required") is not False:
            failures.append("G-14 package JSON human_review_required must be false")
        if package_json.get("agent_council_verdict") != "COUNCIL_PASS_READY_FOR_PR":
            failures.append("G-14 package JSON council verdict must be COUNCIL_PASS_READY_FOR_PR")
    return print_result("SV-1 internal gate", failures)


if __name__ == "__main__":
    sys.exit(main())
