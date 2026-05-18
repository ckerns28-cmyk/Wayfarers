#!/usr/bin/env python3
"""Validate the G-8 character motion foundation.

This validator is expected to fail until G-8 replaces static-frame drift with
grounded motion proof.
"""

from __future__ import annotations

import sys

from starter_village_validator_common import CHARACTER_MANIFEST, print_result, require_text


def main() -> int:
    failures: list[str] = []
    manifest_text = require_text(
        CHARACTER_MANIFEST,
        [
            "idle_down",
            "idle_up",
            "idle_left",
            "idle_right",
            "walk_down",
            "walk_up",
            "walk_left",
            "walk_right",
            "foot_anchor",
        ],
        failures,
    )
    if "repeats accepted down-facing source art" in manifest_text:
        failures.append("G-8 not complete: manifest still repeats static directional art for walk contracts")
    if "pause_behavior" not in manifest_text or "movement_speed" not in manifest_text:
        failures.append("G-8 not complete: movement speed and pause behavior contract not recorded in character manifest")
    return print_result("character motion foundation", failures)


if __name__ == "__main__":
    sys.exit(main())
