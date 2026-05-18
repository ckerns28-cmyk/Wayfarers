#!/usr/bin/env python3
"""Validate G-8A/G-11 NPC population and route readiness."""

from __future__ import annotations

import sys

from starter_village_validator_common import G7_REPORT, MAP_LAYER, print_result, require_text


def main() -> int:
    failures: list[str] = []
    g7 = require_text(
        G7_REPORT,
        [
            "Tavern Keeper or Inn Servant",
            "Dockworker",
            "Clerk / Edrin Vale",
            "Merchant / Shopkeeper",
            "Rumor Carrier / Suspicious Patron",
        ],
        failures,
    )
    map_layer = require_text(MAP_LAYER, ["NEWPORT_ATELIER_CHARACTER_MATERIALS"], failures)
    for token in ["tavern_keeper", "rumor_carrier", "suspicious_patron", "merchant_shopkeeper"]:
        if token not in map_layer:
            failures.append(f"G-8A not complete: runtime NPC population missing {token}")
    if "No static portrait-like NPC may drift across the map" not in g7:
        failures.append("G-7 report must preserve the no-static-drift NPC rule")
    return print_result("npc population and routes", failures)


if __name__ == "__main__":
    sys.exit(main())
