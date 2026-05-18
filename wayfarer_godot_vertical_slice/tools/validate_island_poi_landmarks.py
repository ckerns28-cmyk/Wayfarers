#!/usr/bin/env python3
"""Validate the G-16 island POI/landmark contract."""

from __future__ import annotations

import sys

from opening_village_island_validator_common import print_result, validate_phase_contract


def main() -> int:
    failures: list[str] = []
    validate_phase_contract("G-16", failures)
    return print_result("island poi landmarks", failures)


if __name__ == "__main__":
    sys.exit(main())
