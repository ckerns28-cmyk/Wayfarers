#!/usr/bin/env python3
"""Validate Starter Village interaction UX readiness."""

from __future__ import annotations

import sys

from starter_village_validator_common import (
    ATELIER_NPC_GD,
    BLUEPRINT,
    BUILDING_GD,
    EDRIN_GD,
    G7C_COUNCIL_REPORT,
    G7C_REPORT,
    G7C_SCREENSHOT_MANIFEST,
    G9_COUNCIL_REPORT,
    G9_REPORT,
    G9_SCREENSHOT_MANIFEST,
    HUD_GD,
    HUD_SCENE,
    LEDGER_JSON,
    MAP_LAYER,
    PLAYER_GD,
    PLAYER_TSCN,
    load_json,
    phase_map,
    print_result,
    repo_path,
    require_text,
)


def main() -> int:
    failures: list[str] = []
    ledger = load_json(LEDGER_JSON, failures)
    map_layer = require_text(
        MAP_LAYER,
        [
            "NEWPORT_G7C_LANDMARK_IDENTITY_PLACEMENTS",
            "g7c_tavern_inn_warm_entry_landmark",
            "g7c_counting_house_civic_notice_board_landmark",
            "g7c_commercial_shop_row_colored_awning_identity",
            "g7c_rear_service_lane_gate_identity",
        ],
        failures,
    )
    blueprint = require_text(
        BLUEPRINT,
        [
            "g7c_landmark_identity_contract",
            "Tavern/Inn centerpiece",
            "Counting House civic notice anchor",
            "small civic notice-board location",
            "STARTER_VILLAGE_G9_INTERACTION_UX_PASS",
            "g9_interaction_ux_contract",
            "compact_diegetic_action_name_no_debug_marker",
        ],
        failures,
    )
    player_source = require_text(
        PLAYER_GD,
        [
            "G9_INTERACTION_UX_PASS",
            "PROMPT_MAX_WIDTH",
            "PROMPT_FONT_SIZE",
            "prompt_ux_contract",
            "compact_diegetic_action_name_no_debug_marker",
        ],
        failures,
    )
    player_scene = require_text(PLAYER_TSCN, ["PromptLabel", "font_size = 12", "offset_left = -80.0", "offset_right = 80.0"], failures)
    hud_source = require_text(
        HUD_GD,
        [
            "G9_INTERACTION_UX_PASS",
            "G9_OBJECTIVE_LINE",
            "G9_OBJECTIVE_UPDATE_COPY",
            "G9_RUMOR_GUIDANCE_COPY",
            "interaction_ux_contract",
            "Counting House",
            "tavern whisper",
        ],
        failures,
    )
    hud_scene = require_text(HUD_SCENE, ["First Light", "Counting House", "tavern whisper"], failures)
    edrin_source = require_text(EDRIN_GD, ["get_prompt_text", "Talk -", "prompt_ux_contract"], failures)
    atelier_npc_source = require_text(ATELIER_NPC_GD, ["get_prompt_text", "Talk -", "prompt_ux_contract"], failures)
    if 'prompt_label.text = "Press E' in player_source:
        failures.append("G-9 player prompt code must not display Press E copy in normal in-world prompts")
    if "Press E" in hud_source or "Press E" in hud_scene:
        failures.append("G-9 HUD/objective copy must not use debug-like Press E instruction text")
    if "E: Enter - " not in require_text(BUILDING_GD, ["prompt_ux_contract"], failures):
        failures.append("G-9 building prompts must use compact E: Enter - form")
    if isinstance(ledger, dict):
        phases = phase_map(ledger, failures)
        if phases.get("G-7C", {}).get("current_status") == "PASS":
            require_text(G7C_REPORT, ["G-7C Landmark and District Identity Pass", "Tavern/Inn centerpiece", "G-8 next"], failures)
            require_text(G7C_COUNCIL_REPORT, ["COUNCIL_PASS_READY_FOR_PR", "UX Designer", "runtime screenshots"], failures)
            manifest = load_json(G7C_SCREENSHOT_MANIFEST, failures)
            if isinstance(manifest, dict):
                screenshots = manifest.get("screenshots")
                if manifest.get("status") != "PASS":
                    failures.append("G-7C screenshot manifest must be PASS")
                if not isinstance(screenshots, list) or len(screenshots) < 15:
                    failures.append("G-7C screenshot manifest must include 15 proof views")
                else:
                    for shot in screenshots:
                        if isinstance(shot, dict):
                            raw_path = str(shot.get("path", ""))
                            if raw_path and not repo_path(raw_path).exists():
                                failures.append(f"G-7C screenshot path missing: {raw_path}")
        if phases.get("G-9", {}).get("current_status") == "PASS":
            require_text(
                G9_REPORT,
                [
                    "G-9 Interaction UX and Diegetic Prompt Pass",
                    "compact_diegetic_action_name_no_debug_marker",
                    "E: Enter - Harbor Mercantile",
                    "E: Talk - Edrin Vale",
                    "Objective updated",
                    "Rumor:",
                ],
                failures,
            )
            require_text(
                G9_COUNCIL_REPORT,
                [
                    "COUNCIL_PASS_READY_FOR_PR",
                    "UX Designer",
                    "Interaction UX Result",
                    "UX/readability score",
                    "runtime screenshots",
                ],
                failures,
            )
            manifest = load_json(G9_SCREENSHOT_MANIFEST, failures)
            if isinstance(manifest, dict):
                screenshots = manifest.get("screenshots")
                if manifest.get("status") != "PASS":
                    failures.append("G-9 screenshot manifest must be PASS")
                if manifest.get("phase") != "G-9":
                    failures.append("G-9 screenshot manifest phase mismatch")
                if not isinstance(screenshots, list) or len(screenshots) < 15:
                    failures.append("G-9 screenshot manifest must include 15 proof views")
                else:
                    for shot in screenshots:
                        if isinstance(shot, dict):
                            raw_path = str(shot.get("path", ""))
                            if raw_path and not repo_path(raw_path).exists():
                                failures.append(f"G-9 screenshot path missing: {raw_path}")
        if phases.get("G-9A", {}).get("current_status") == "PASS":
            for required in ["Journal", "Objective updated", "Whisper", "Rumor"]:
                if required not in hud_source and required not in hud_scene:
                    failures.append(f"G-9A not complete: HUD or UX surface missing {required}")
    if "g7c_tavern_inn_warm_entry_landmark" not in map_layer or "g7c_landmark_identity_contract" not in blueprint:
        failures.append("G-7C landmark identity contract must be runtime-backed")
    return print_result("interaction ux", failures)


if __name__ == "__main__":
    sys.exit(main())
