#!/usr/bin/env python3
"""Validate G-11 living town rhythm without allowing static NPC glide."""

from __future__ import annotations

import sys
from typing import Any

from starter_village_validator_common import (
    ATELIER_NPC_GD,
    BLUEPRINT,
    EDRIN_GD,
    G11_COUNCIL_REPORT,
    G11_REPORT,
    G11_SCREENSHOT_MANIFEST,
    LEDGER_JSON,
    MAIN_GD,
    load_json,
    phase_map,
    print_result,
    repo_path,
    require_text,
)


REQUIRED_RHYTHMS = [
    "dock_work_bell",
    "tavern_whisper_pulse",
    "market_street_trade",
    "counting_house_watch",
    "rear_gate_suspicion",
]

REQUIRED_BEHAVIORS = [
    "ambient_barks",
    "dock_work_behavior",
    "tavern_social_behavior",
    "merchant_street_behavior",
    "civic_notice_behavior",
    "rear_service_lane_behavior",
    "idle_pauses",
    "facing_changes",
]

REQUIRED_NPCS = [
    "edrin_vale_counting_house_clerk",
    "bess_armitage_tavern_keeper",
    "mara_pike_dockworker",
    "honor_finch_merchant_shopkeeper",
    "nora_vale_rumor_carrier",
    "silas_crowe_suspicious_patron",
    "jonah_reed_dock_courier",
]


def _validate_actor_contract(actor: dict[str, Any], failures: list[str]) -> None:
    npc_id = str(actor.get("npc_id", ""))
    if not npc_id:
        failures.append("G-11 actor contract missing npc_id")
    if actor.get("route_walking_enabled") is not False:
        failures.append(f"G-11 actor {npc_id} must keep route_walking_enabled=false")
    if float(actor.get("movement_speed", 0.0)) != 0.0:
        failures.append(f"G-11 actor {npc_id} must keep movement_speed=0.0 until walk sheets exist")
    if actor.get("no_static_sprite_translation") is not True:
        failures.append(f"G-11 actor {npc_id} must declare no_static_sprite_translation")
    if int(actor.get("stage_count", 0)) < 3:
        failures.append(f"G-11 actor {npc_id} needs at least three rhythm stages")
    if int(actor.get("ambient_bark_count", 0)) < 1:
        failures.append(f"G-11 actor {npc_id} needs ambient bark proof")
    if not str(actor.get("rhythm_id", "")):
        failures.append(f"G-11 actor {npc_id} missing rhythm_id")
    if not actor.get("ground_shadow_visible", False):
        failures.append(f"G-11 actor {npc_id} missing ground shadow proof")


def _validate_manifest(failures: list[str]) -> None:
    manifest = load_json(G11_SCREENSHOT_MANIFEST, failures)
    if not isinstance(manifest, dict):
        return
    if manifest.get("status") != "PASS":
        failures.append("G-11 screenshot manifest must be PASS")
    if manifest.get("phase") != "G-11":
        failures.append("G-11 screenshot manifest phase mismatch")
    if manifest.get("schema_id") != "wayfarer.g11.runtime_screenshot_manifest.v1":
        failures.append("G-11 screenshot manifest schema mismatch")
    screenshots = manifest.get("screenshots")
    if not isinstance(screenshots, list) or len(screenshots) < 15:
        failures.append("G-11 screenshot manifest must include the 15 recurring proof views")
    else:
        for shot in screenshots:
            if not isinstance(shot, dict):
                failures.append("G-11 screenshot row must be an object")
                continue
            raw_path = str(shot.get("path", ""))
            if raw_path and not repo_path(raw_path).exists():
                failures.append(f"G-11 screenshot path missing: {raw_path}")
            snapshot = shot.get("town_rhythm_snapshot")
            if not isinstance(snapshot, dict):
                failures.append(f"G-11 screenshot missing rhythm snapshot: {shot.get('filename')}")
    proof_sequence = manifest.get("town_rhythm_motion_proof_sequence")
    if not isinstance(proof_sequence, list) or len(proof_sequence) < 5:
        failures.append("G-11 manifest must include at least five timestamped rhythm proof snapshots")
    final_contract = manifest.get("town_rhythm_contract_final")
    if not isinstance(final_contract, dict):
        failures.append("G-11 manifest missing final town rhythm contract")
        return
    if final_contract.get("position_drift_detected") is not False:
        failures.append("G-11 town rhythm must not drift NPC positions")
    if int(final_contract.get("moving_actor_count", 0)) != 0:
        failures.append("G-11 must not enable moving actors with one-frame NPC sprites")
    if int(final_contract.get("actor_count", 0)) < 6:
        failures.append("G-11 must include at least six rhythm actors")
    if int(final_contract.get("runtime_rhythm_count", 0)) < 4:
        failures.append("G-11 must include multiple district rhythms")
    if int(final_contract.get("runtime_ambient_bark_count", 0)) < 8:
        failures.append("G-11 needs enough ambient bark lines to show town-life rhythm")
    for actor in final_contract.get("actors", []):
        if isinstance(actor, dict):
            _validate_actor_contract(actor, failures)


def main() -> int:
    failures: list[str] = []
    ledger = load_json(LEDGER_JSON, failures)
    blueprint = require_text(
        BLUEPRINT,
        [
            "STARTER_VILLAGE_G11_LIVING_TOWN_RHYTHM_PASS",
            "STARTER_VILLAGE_G11_NPC_RHYTHM_POLICY",
            "starter_village_town_rhythm_specs",
            "starter_village_town_rhythm_contract",
            "starter_village_town_rhythm_spec_for_npc",
            "no_static_sprite_translation",
            "G-10B ground-material patchwork remains in G-11/G-12 review",
        ]
        + REQUIRED_RHYTHMS
        + REQUIRED_BEHAVIORS
        + REQUIRED_NPCS,
        failures,
    )
    main_source = require_text(
        MAIN_GD,
        [
            "_configure_starter_village_town_rhythm",
            "starter_village_town_rhythm_contract",
            "debug_apply_starter_village_town_rhythm_tick",
            "debug_apply_starter_village_town_rhythm_ticks",
            "_starter_village_town_rhythm_drift_detected",
            "configure_rhythm",
            "apply_town_rhythm_tick",
        ],
        failures,
    )
    for path, label in [(ATELIER_NPC_GD, "AtelierTownNpc"), (EDRIN_GD, "EdrinVale")]:
        source = require_text(
            path,
            [
                "G11_LIVING_TOWN_RHYTHM_PASS",
                "NPC_TOWN_RHYTHM_POLICY",
                "NPC_ROUTE_WALKING_ENABLED := false",
                "NPC_MOVEMENT_SPEED := 0.0",
                "configure_rhythm",
                "apply_town_rhythm_tick",
                "set_town_rhythm_bark_visible",
                "town_rhythm_contract",
                "AmbientBarkLabel",
                "no_static_sprite_translation",
            ],
            failures,
        )
        for forbidden in ["global_position +=", "position +=", "move_and_slide", "move_and_collide", "velocity ="]:
            if forbidden in source:
                failures.append(f"G-11 {label} must not translate static NPC sprites via {forbidden}")
    if "NPC_ROUTE_WALKING_ENABLED := true" in blueprint + main_source:
        failures.append("G-11 must not re-enable NPC route walking until dedicated walk sheets exist")

    if isinstance(ledger, dict):
        phases = phase_map(ledger, failures)
        if phases.get("G-11", {}).get("current_status") == "PASS":
            require_text(
                G11_REPORT,
                [
                    "G-11 Living Town Rhythm Pass",
                    "stationary_no_glide_rhythm_until_dedicated_walk_sheets",
                    "dock_work_bell",
                    "tavern_whisper_pulse",
                    "market_street_trade",
                    "counting_house_watch",
                    "rear_gate_suspicion",
                    "No static NPC sprite translates",
                    "Ground/material patchwork remains a G-12 review risk",
                ],
                failures,
            )
            require_text(
                G11_COUNCIL_REPORT,
                [
                    "COUNCIL_PASS_READY_FOR_PR",
                    "Animation/NPC Behavior Director",
                    "G-11 Living Town Rhythm Result",
                    "NPC rhythm score: 8.5",
                    "position drift: none",
                ],
                failures,
            )
            _validate_manifest(failures)

    return print_result("living town rhythm", failures)


if __name__ == "__main__":
    sys.exit(main())
