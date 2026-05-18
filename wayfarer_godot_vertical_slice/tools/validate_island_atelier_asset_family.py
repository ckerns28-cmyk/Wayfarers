#!/usr/bin/env python3
"""Validate the G-16A island atelier asset family contract."""

from __future__ import annotations

import sys

from opening_village_island_validator_common import print_result, validate_phase_contract


def main() -> int:
    failures: list[str] = []
    validate_phase_contract("G-16A", failures)
    return print_result("island atelier asset family", failures)


if __name__ == "__main__":
    sys.exit(main())
