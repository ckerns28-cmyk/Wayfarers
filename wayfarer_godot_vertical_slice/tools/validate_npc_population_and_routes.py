#!/usr/bin/env python3
"""Validate G-8A/G-11 NPC population and route readiness."""

from __future__ import annotations

import sys

from starter_village_validator_common import (
    BLUEPRINT,
    G7_REPORT,
    LEDGER_JSON,
    MAP_LAYER,
    load_json,
    phase_map,
    print_result,
    require_text,
)


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
    ledger = load_json(LEDGER_JSON, failures)
    blueprint = require_text(
        BLUEPRINT,
        [
            "g7b_harbor_commercial_spine_contract",
            "g7b_fish_offload_to_market_transfer",
            "g7b_manifest_cargo_to_counting_house",
            "g7b_chandlery_rope_service_to_storehouse",
        ],
        failures,
    )
    if isinstance(ledger, dict):
        phases = phase_map(ledger, failures)
        if phases.get("G-7B", {}).get("current_status") == "PASS":
            for token in [
                "g7b_west_fish_offload_zone_net_crates",
                "g7b_central_manifest_cargo_waiting_for_counting_house",
                "g7b_market_transfer_goods_linked_to_wharf",
                "g7b_east_storehouse_barrel_row_work_queue",
            ]:
                if token not in map_layer:
                    failures.append(f"G-7B harbor/commercial route proof missing {token}")
            if "work_zones" not in blueprint or "commercial_flow" not in blueprint:
                failures.append("G-7B harbor/commercial contract must preserve work zones and commercial flow")
        if phases.get("G-8A", {}).get("current_status") == "PASS" or phases.get("G-11", {}).get("current_status") == "PASS":
            for token in ["tavern_keeper", "rumor_carrier", "suspicious_patron", "merchant_shopkeeper"]:
                if token not in map_layer:
                    failures.append(f"G-8A not complete: runtime NPC population missing {token}")
    if "No static portrait-like NPC may drift across the map" not in g7:
        failures.append("G-7 report must preserve the no-static-drift NPC rule")
    return print_result("npc population and routes", failures)


if __name__ == "__main__":
    sys.exit(main())
