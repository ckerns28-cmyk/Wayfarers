#!/usr/bin/env python3
"""Validate current runtime atelier asset consistency for Starter Village work."""

from __future__ import annotations

import subprocess
import sys

from starter_village_validator_common import CHARACTER_MANIFEST, MAP_LAYER, PROJECT_ROOT, print_result, require_text


def main() -> int:
    failures: list[str] = []
    require_text(
        CHARACTER_MANIFEST,
        [
            "newport_atelier_characters_g422r",
            "player_wayfarer_atelier_g422r",
            "newport_npc_atelier_g422r_v1.png",
            "normal_review_eligible",
        ],
        failures,
    )
    require_text(
        MAP_LAYER,
        [
            "NEWPORT_ATELIER_CHARACTER_VERSION",
            "NEWPORT_ATELIER_CHARACTER_ATLAS_PATH",
            "G422R_SUPPRESS_PRIMITIVE_WORLD_PROPS",
            "G422R_HIDE_NORMAL_PLAY_LAYOUT_GUIDES",
        ],
        failures,
    )
    validator = PROJECT_ROOT / "tools" / "validate_g422r_runtime_asset_consistency.py"
    if not validator.exists():
        failures.append("missing G-4.22R runtime asset consistency validator")
    else:
        result = subprocess.run(
            [sys.executable, str(validator)],
            cwd=str(PROJECT_ROOT.parent),
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            output = " ".join((result.stdout + "\n" + result.stderr).split())
            failures.append("G-4.22R runtime asset consistency validator failed: " + output)

    return print_result("runtime atelier asset consistency", failures)


if __name__ == "__main__":
    sys.exit(main())
