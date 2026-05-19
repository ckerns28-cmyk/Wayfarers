#!/usr/bin/env python3
"""Validate the G-19/G-20 first-session guidance and gameplay-loop contracts."""

from __future__ import annotations

import sys

from opening_village_island_validator_common import print_result, validate_phase_contract
from validate_g19_player_guidance_map_journal_interaction import validate_g19_player_guidance


def main() -> int:
    failures: list[str] = []
    validate_phase_contract("G-19", failures)
    validate_g19_player_guidance(failures)
    validate_phase_contract("G-20", failures)
    return print_result("first-session gameplay loop", failures)


if __name__ == "__main__":
    sys.exit(main())
