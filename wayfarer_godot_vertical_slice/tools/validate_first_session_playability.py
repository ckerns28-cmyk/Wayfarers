#!/usr/bin/env python3
"""Validate first-session playability evidence."""

from __future__ import annotations

import sys

from starter_village_validator_common import LEDGER_JSON, load_json, phase_map, print_result


def main() -> int:
    failures: list[str] = []
    ledger = load_json(LEDGER_JSON, failures)
    if isinstance(ledger, dict):
        by_phase = phase_map(ledger, failures)
        for phase_id in ["G-9A", "G-10", "G-10A", "G-10B", "G-11", "G-12"]:
            status = str(by_phase.get(phase_id, {}).get("current_status", ""))
            if status != "PASS":
                failures.append(f"first-session playability not complete: {phase_id} is {status or 'missing'}")
    return print_result("first-session playability", failures)


if __name__ == "__main__":
    sys.exit(main())
