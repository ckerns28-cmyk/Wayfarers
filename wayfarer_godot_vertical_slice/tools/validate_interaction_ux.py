#!/usr/bin/env python3
"""Validate Starter Village interaction UX readiness."""

from __future__ import annotations

import sys

from starter_village_validator_common import HUD_SCENE, print_result, require_text


def main() -> int:
    failures: list[str] = []
    hud = require_text(HUD_SCENE, ["First Light", "counting house"], failures)
    for required in ["Journal", "Objective updated", "Whisper", "Rumor"]:
        if required not in hud:
            failures.append(f"G-9/G-9A not complete: HUD or UX surface missing {required}")
    return print_result("interaction ux", failures)


if __name__ == "__main__":
    sys.exit(main())
