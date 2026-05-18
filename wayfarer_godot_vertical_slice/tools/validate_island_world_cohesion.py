#!/usr/bin/env python3
"""Validate the G-15B island terrain/route cohesion contract."""

from __future__ import annotations

import sys

from opening_village_island_validator_common import print_result, validate_phase_contract


def main() -> int:
    failures: list[str] = []
    validate_phase_contract("G-15B", failures)
    return print_result("island world cohesion", failures)


if __name__ == "__main__":
    sys.exit(main())
