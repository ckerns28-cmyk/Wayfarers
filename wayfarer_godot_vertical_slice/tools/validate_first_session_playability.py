#!/usr/bin/env python3
"""Validate G-12 first-session playability evidence."""

from __future__ import annotations

import sys

from starter_village_validator_common import (
    G12_COUNCIL_REPORT,
    G12_REPORT,
    G12_SCREENSHOT_MANIFEST,
    LEDGER_JSON,
    MAIN_GD,
    PLAYER_GD,
    load_json,
    phase_map,
    print_result,
    repo_path,
    require_text,
)


REQUIRED_SCREENSHOTS = [
    "g12_01_wide_newport_normal_gameplay_view.png",
    "g12_02_player_arrival_at_harbor.png",
    "g12_03_player_on_route_to_counting_house.png",
    "g12_04_player_near_tavern_inn.png",
    "g12_05_player_on_commercial_avenue.png",
    "g12_06_player_at_dock_wharf_work_area.png",
    "g12_07_living_town_rhythm_without_prompt_clutter.png",
    "g12_08_npc_idle_and_readability_proof.png",
    "g12_09_player_interacting_with_counting_house_clerk.png",
    "g12_10_player_interacting_at_tavern_rumor_location.png",
    "g12_11_quest_prompt_journal_objective_proof.png",
    "g12_12_signs_markers_interaction_ux_proof.png",
    "g12_13_y_sort_layering_near_buildings_props.png",
    "g12_14_debug_overlays_disabled.png",
    "g12_15_contact_sheet_provenance_proof.png",
]

REQUIRED_PLAYTEST_FLAGS = [
    "within_10_seconds_goal_clear",
    "within_60_seconds_route_readable",
    "within_3_minutes_objective_advances",
    "within_10_minutes_rumor_and_roles",
    "within_15_20_minutes_loop_complete",
    "no_dead_objective_state",
    "reward_or_progression_exists",
    "optional_secret_exists",
    "debug_overlays_disabled_proof",
]


def main() -> int:
    failures: list[str] = []
    ledger = load_json(LEDGER_JSON, failures)
    require_text(
        MAIN_GD,
        [
            "starter_village_first_session_readability_contract",
            "set_starter_village_ambient_barks_enabled",
            "_starter_village_player_focus_blocks_barks",
            "_suppress_player_prompt_for",
            "ambient_barks_suppressed_when_focused",
        ],
        failures,
    )
    require_text(
        PLAYER_GD,
        [
            "set_prompt_suppressed",
            "_prompt_suppressed",
            "prompt_suppression_available",
        ],
        failures,
    )

    manifest = load_json(G12_SCREENSHOT_MANIFEST, failures)
    if isinstance(manifest, dict):
        validate_manifest(manifest, failures)

    if isinstance(ledger, dict):
        phases = phase_map(ledger, failures)
        for phase_id in ["G-9A", "G-10", "G-10A", "G-10B", "G-11", "G-11A"]:
            status = str(phases.get(phase_id, {}).get("current_status", ""))
            if status != "PASS":
                failures.append(f"first-session prerequisite not complete: {phase_id} is {status or 'missing'}")
        if phases.get("G-12", {}).get("current_status") == "PASS":
            row = phases.get("G-12", {})
            if row.get("agent_council_verdict") != "COUNCIL_PASS_READY_FOR_PR":
                failures.append("G-12 council verdict must be COUNCIL_PASS_READY_FOR_PR")
            for key in ["screenshot_paths", "validation_commands", "validation_results"]:
                if not row.get(key):
                    failures.append(f"G-12 ledger missing {key}")
            require_text(
                G12_REPORT,
                [
                    "G-12 First-Session Fun, Pacing, and Readability Pass",
                    "Game Studio playtest method",
                    "within 10 seconds",
                    "within 15-20 minutes",
                    "prompt/dialogue/bark overlap",
                    "COUNCIL_PASS_READY_FOR_PR",
                ],
                failures,
            )
            if G12_COUNCIL_REPORT.exists():
                require_text(
                    G12_COUNCIL_REPORT,
                    [
                        "G-12 First-Session Result",
                        "COUNCIL_PASS_READY_FOR_PR",
                        "runtime screenshots inspected",
                        "prompt/dialogue/bark overlap",
                    ],
                    failures,
                )

    return print_result("first-session playability", failures)


def validate_manifest(manifest: dict, failures: list[str]) -> None:
    if manifest.get("schema_id") != "wayfarer.g12.runtime_screenshot_manifest.v1":
        failures.append("G-12 screenshot manifest schema mismatch")
    if manifest.get("phase") != "G-12":
        failures.append("G-12 screenshot manifest phase mismatch")
    if manifest.get("status") != "PASS":
        failures.append("G-12 screenshot manifest must be PASS")
    if "Screenshots override written PASS claims" not in str(manifest.get("screenshot_contradiction_policy", "")):
        failures.append("G-12 manifest must record screenshot contradiction policy")
    screenshots = manifest.get("screenshots")
    if not isinstance(screenshots, list) or len(screenshots) < 15:
        failures.append("G-12 screenshot manifest must include the full 15-view proof set")
        screenshots = []
    filenames = {str(shot.get("filename", "")) for shot in screenshots if isinstance(shot, dict)}
    for required in REQUIRED_SCREENSHOTS:
        if required not in filenames:
            failures.append(f"G-12 screenshot proof missing {required}")
    for shot in screenshots:
        if not isinstance(shot, dict):
            failures.append("G-12 screenshot row must be an object")
            continue
        if shot.get("status") != "PASS":
            failures.append(f"G-12 screenshot row not PASS: {shot.get('filename', '')}")
        raw_path = str(shot.get("path", ""))
        if raw_path and not repo_path(raw_path).exists():
            failures.append(f"G-12 screenshot path missing: {raw_path}")
        if shot.get("dialogue_visible") and shot.get("prompt_visible"):
            failures.append(f"G-12 dialogue/prompt overlap remains in {shot.get('filename', '')}")
        if (shot.get("dialogue_visible") or shot.get("prompt_visible")) and int(shot.get("ambient_bark_visible_count", 0)) > 0:
            failures.append(f"G-12 focused screenshot has ambient bark clutter: {shot.get('filename', '')}")
        safety = shot.get("camera_focus_safety")
        if not isinstance(safety, dict) or safety.get("status") != "PASS":
            failures.append(f"G-12 camera focus safety failed for {shot.get('filename', '')}")
    playtest = manifest.get("first_session_playtest")
    if not isinstance(playtest, dict):
        failures.append("G-12 manifest missing first_session_playtest contract")
        return
    if playtest.get("status") != "PASS":
        failures.append("G-12 first_session_playtest status must be PASS")
    for flag in REQUIRED_PLAYTEST_FLAGS:
        if playtest.get(flag) is not True:
            failures.append(f"G-12 first_session_playtest missing true flag: {flag}")
    for forbidden in ["prompt_dialogue_overlap", "focused_bark_overlap", "camera_focus_safety_fail"]:
        if playtest.get(forbidden) is not False:
            failures.append(f"G-12 first_session_playtest must keep {forbidden}=false")
    if float(playtest.get("first_session_score", 0.0)) < 8.5:
        failures.append("G-12 first_session_score must be at least 8.5")
    if float(playtest.get("readability_score", 0.0)) < 8.5:
        failures.append("G-12 readability_score must be at least 8.5")


if __name__ == "__main__":
    sys.exit(main())
