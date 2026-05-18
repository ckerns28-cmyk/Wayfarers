#!/usr/bin/env python3
"""Validate Starter Village interaction UX readiness."""

from __future__ import annotations

import sys

from starter_village_validator_common import (
    BLUEPRINT,
    G7C_COUNCIL_REPORT,
    G7C_REPORT,
    G7C_SCREENSHOT_MANIFEST,
    HUD_SCENE,
    LEDGER_JSON,
    MAP_LAYER,
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
        ],
        failures,
    )
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
        if phases.get("G-9", {}).get("current_status") == "PASS" or phases.get("G-9A", {}).get("current_status") == "PASS":
            hud = require_text(HUD_SCENE, ["First Light", "counting house"], failures)
            for required in ["Journal", "Objective updated", "Whisper", "Rumor"]:
                if required not in hud:
                    failures.append(f"G-9/G-9A not complete: HUD or UX surface missing {required}")
    if "g7c_tavern_inn_warm_entry_landmark" not in map_layer or "g7c_landmark_identity_contract" not in blueprint:
        failures.append("G-7C landmark identity contract must be runtime-backed")
    return print_result("interaction ux", failures)


if __name__ == "__main__":
    sys.exit(main())
