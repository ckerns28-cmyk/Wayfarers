#!/usr/bin/env python3
"""Validate the OVI-1 autonomous execution ledger."""

from __future__ import annotations

import sys

from opening_village_island_validator_common import (
    REQUIRED_PHASES,
    print_result,
    validate_common_ledger_contract,
)


def main() -> int:
    failures: list[str] = []
    validate_common_ledger_contract(failures)
    return print_result("opening village island execution ledger", failures, [f"Rows audited: {len(REQUIRED_PHASES)}"])


if __name__ == "__main__":
    sys.exit(main())
