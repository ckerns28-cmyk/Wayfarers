#!/usr/bin/env python3
"""Validate G-8A/G-11 NPC population and route readiness."""

from __future__ import annotations

import sys

from starter_village_validator_common import (
    ATELIER_NPC_GD,
    ATELIER_NPC_TSCN,
    BLUEPRINT,
    G7_REPORT,
    G8A_COUNCIL_REPORT,
    G8A_REPORT,
    G8A_SCREENSHOT_MANIFEST,
    LEDGER_JSON,
    MAIN_GD,
    MAP_LAYER,
    load_json,
    phase_map,
    print_result,
    repo_path,
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
    map_layer = require_text(
        MAP_LAYER,
        [
            "NEWPORT_ATELIER_CHARACTER_MATERIALS",
            "STARTER_VILLAGE_G8A_LIVING_NPC_POPULATION_PASS",
            "G8A_RUNTIME_NPC_NODES_ENABLED := true",
            "stationary_work_pose_until_dedicated_walk_sheets",
        ],
        failures,
    )
    main_source = require_text(
        MAIN_GD,
        [
            "ATELIER_TOWN_NPC_SCENE",
            "_place_starter_village_npcs",
            "configure_population",
            "starter_village_npc_specs",
        ],
        failures,
    )
    ledger = load_json(LEDGER_JSON, failures)
    blueprint = require_text(
        BLUEPRINT,
        [
            "g7b_harbor_commercial_spine_contract",
            "g7b_fish_offload_to_market_transfer",
            "g7b_manifest_cargo_to_counting_house",
            "g7b_chandlery_rope_service_to_storehouse",
            "STARTER_VILLAGE_G8A_LIVING_NPC_POPULATION_PASS",
            "starter_village_npc_specs",
            "g8a_living_npc_population_contract",
            "stationary_work_pose_until_dedicated_walk_sheets",
        ],
        failures,
    )
    atelier_npc_source = require_text(
        ATELIER_NPC_GD,
        [
            "G8A_LIVING_NPC_POPULATION_PASS",
            "NPC_ROUTE_WALKING_ENABLED := false",
            "starter_village_npc",
            "npc_population_contract",
            "motion_foundation_contract",
            "GroundShadow",
            "AnimatedSprite2D",
        ],
        failures,
    )
    require_text(ATELIER_NPC_TSCN, ["AtelierTownNpc", "GroundShadow", "AnimatedSprite2D", "InteractionArea"], failures)
    required_roles = [
        "tavern_keeper",
        "dockworker",
        "counting_house_clerk",
        "merchant_shopkeeper",
        "rumor_carrier",
        "suspicious_patron",
    ]
    required_names = [
        "Edrin Vale",
        "Bess Armitage",
        "Mara Pike",
        "Honor Finch",
        "Nora Vale",
        "Silas Crowe",
    ]
    required_purposes = [
        "g8a_tavern_keeper_station_supports_rumor_hub",
        "g8a_west_dockworker_station_supports_harbor_labor",
        "g8a_counting_house_clerk_station_supports_first_objective",
        "g8a_merchant_shopkeeper_station_supports_commercial_spine",
        "g8a_rumor_carrier_station_supports_civic_to_tavern_whisper",
        "g8a_suspicious_patron_station_supports_secret_path",
    ]
    for token in required_roles + required_names:
        if token not in blueprint:
            failures.append(f"G-8A blueprint missing NPC identity token: {token}")
    for token in required_roles + required_purposes:
        if token not in map_layer:
            failures.append(f"G-8A map layer missing NPC placement token: {token}")
    if "world.add_child(npc)" not in main_source:
        failures.append("G-8A runtime NPC nodes must be instantiated into the world")
    if "draw_circle" in atelier_npc_source or "func _draw()" in atelier_npc_source:
        failures.append("G-8A AtelierTownNpc must not use primitive placeholder drawing")
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
            require_text(
                G8A_REPORT,
                [
                    "G-8A Living NPC Population Pass",
                    "stationary_work_pose_until_dedicated_walk_sheets",
                    "Bess Armitage",
                    "Mara Pike",
                    "Honor Finch",
                    "Nora Vale",
                    "Silas Crowe",
                    "No static portrait-like NPC may drift",
                ],
                failures,
            )
            require_text(
                G8A_COUNCIL_REPORT,
                [
                    "COUNCIL_PASS_READY_FOR_PR",
                    "Animation/NPC Behavior Director",
                    "Living NPC Population Result",
                    "NPC population score: 8.5",
                    "stationary work-pose policy",
                ],
                failures,
            )
            manifest = load_json(G8A_SCREENSHOT_MANIFEST, failures)
            if isinstance(manifest, dict):
                screenshots = manifest.get("screenshots")
                if manifest.get("status") != "PASS":
                    failures.append("G-8A screenshot manifest must be PASS")
                if manifest.get("phase") != "G-8A":
                    failures.append("G-8A screenshot manifest phase mismatch")
                if int(manifest.get("npc_population_count", 0)) < 6:
                    failures.append("G-8A screenshot manifest must record at least six NPC contracts")
                if not isinstance(screenshots, list) or len(screenshots) < 15:
                    failures.append("G-8A screenshot manifest must include 15 proof views")
                else:
                    for shot in screenshots:
                        if isinstance(shot, dict):
                            raw_path = str(shot.get("path", ""))
                            if raw_path and not repo_path(raw_path).exists():
                                failures.append(f"G-8A screenshot path missing: {raw_path}")
    if "No static portrait-like NPC may drift across the map" not in g7:
        failures.append("G-7 report must preserve the no-static-drift NPC rule")
    return print_result("npc population and routes", failures)


if __name__ == "__main__":
    sys.exit(main())
