#!/usr/bin/env python3
"""Validate the G-8 character motion foundation.

This validator is expected to fail until G-8 replaces static-frame drift with
grounded motion proof.
"""

from __future__ import annotations

import sys

from starter_village_validator_common import (
    CHARACTER_MANIFEST,
    EDRIN_GD,
    EDRIN_TSCN,
    G8_COUNCIL_REPORT,
    G8_REPORT,
    G8_SCREENSHOT_MANIFEST,
    LEDGER_JSON,
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
    manifest_text = require_text(
        CHARACTER_MANIFEST,
        [
            "motion_foundation_phase",
            "G-8",
            "idle_down",
            "idle_up",
            "idle_left",
            "idle_right",
            "walk_down",
            "walk_up",
            "walk_left",
            "walk_right",
            "foot_anchor",
            "movement_speed_synced_to_animation",
            "stationary_until_walk_sheet",
        ],
        failures,
    )
    player_source = require_text(
        PLAYER_GD,
        [
            "G8_CHARACTER_MOTION_FOUNDATION_PASS",
            "PLAYER_FOOT_ANCHOR",
            "PLAYER_GROUND_SHADOW_SIZE",
            "PLAYER_MOTION_STATE_NAMES",
            "character_motion_contract",
            "PLAYER_WALK_ANIMATION_FPS",
        ],
        failures,
    )
    player_scene = require_text(PLAYER_TSCN, ["GroundShadow", "AnimatedSprite2D"], failures)
    edrin_source = require_text(
        EDRIN_GD,
        [
            "G8_CHARACTER_MOTION_FOUNDATION_PASS",
            "NPC_ROUTE_WALKING_ENABLED := false",
            "NPC_STATIONARY_UNTIL_WALK_SHEET := true",
            "NPC_MOTION_STATE_NAMES",
            "set_review_motion_state",
            "motion_foundation_contract",
            "stationary_idle_until_dedicated_walk_sheet_no_static_drift",
        ],
        failures,
    )
    edrin_scene = require_text(EDRIN_TSCN, ["GroundShadow", "AnimatedSprite2D"], failures)
    if "repeats accepted down-facing source art" in manifest_text:
        failures.append("G-8 not complete: manifest still repeats static directional art for walk contracts")
    if "pause_behavior" not in manifest_text or "movement_speed" not in manifest_text:
        failures.append("G-8 not complete: movement speed and pause behavior contract not recorded in character manifest")
    if "draw_circle" in edrin_source or "func _draw()" in edrin_source:
        failures.append("G-8 NPC grounding must not reintroduce primitive placeholder drawing in EdrinVale.gd")
    if "position = Vector2(0, -37.12)" not in player_scene or "position = Vector2(0, -37.12)" not in edrin_scene:
        failures.append("G-8 foot-anchor visual offsets must be applied to player and Edrin scenes")
    if "speed := 185.0" not in player_source:
        failures.append("G-8 player movement speed must remain synced to the documented animation cadence")
    ledger = load_json(LEDGER_JSON, failures)
    if isinstance(ledger, dict):
        phases = phase_map(ledger, failures)
        if phases.get("G-8", {}).get("current_status") == "PASS":
            require_text(G8_REPORT, ["G-8 Atelier Character and NPC Movement Foundation", "No static portrait-like NPC may drift", "G-8A next"], failures)
            require_text(G8_COUNCIL_REPORT, ["COUNCIL_PASS_READY_FOR_PR", "Animation/NPC Behavior Director", "runtime screenshots", "NPC motion/grounding score: 8.5"], failures)
            manifest = load_json(G8_SCREENSHOT_MANIFEST, failures)
            if isinstance(manifest, dict):
                screenshots = manifest.get("screenshots")
                if manifest.get("status") != "PASS":
                    failures.append("G-8 screenshot manifest must be PASS")
                if not isinstance(screenshots, list) or len(screenshots) < 15:
                    failures.append("G-8 screenshot manifest must include 15 proof views")
                else:
                    for shot in screenshots:
                        if isinstance(shot, dict):
                            raw_path = str(shot.get("path", ""))
                            if raw_path and not repo_path(raw_path).exists():
                                failures.append(f"G-8 screenshot path missing: {raw_path}")
    return print_result("character motion foundation", failures)


if __name__ == "__main__":
    sys.exit(main())
