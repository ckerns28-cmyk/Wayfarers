#!/usr/bin/env python3
"""Validate the G-19/G-20 first-session guidance and gameplay-loop contracts."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from opening_village_island_validator_common import PROJECT_ROOT, REPO_ROOT, load_json, print_result, require_text, repo_path, validate_phase_contract


G19_SOURCE_JSON = PROJECT_ROOT / "data" / "ui" / "opening_first_session_guidance_v1.json"
G19_DIRECTOR_GD = PROJECT_ROOT / "scripts" / "ui" / "OpeningGuidanceDirector.gd"
HUD_GD = PROJECT_ROOT / "scenes" / "ui" / "HUD.gd"
MAIN_GD = PROJECT_ROOT / "scenes" / "Main.gd"
MAP_LAYER_GD = PROJECT_ROOT / "scenes" / "map" / "MapLayer.gd"
CAPTURE_GD = PROJECT_ROOT / "tools" / "capture_g19_runtime_screenshots.gd"
CAPTURE_PS1 = PROJECT_ROOT / "tools" / "capture_g19_runtime_screenshots.ps1"
SCREENSHOT_MANIFEST = PROJECT_ROOT / "artifacts" / "review" / "g19_runtime_screenshots" / "g19_runtime_screenshot_manifest.json"
G19_REPORT = REPO_ROOT / "docs" / "reports" / "G19_PLAYER_GUIDANCE_JOURNAL_INTERACTION_POLISH.md"
G19_REPORT_JSON = REPO_ROOT / "docs" / "reports" / "G19_PLAYER_GUIDANCE_JOURNAL_INTERACTION_POLISH.json"
G19_COUNCIL_REPORT = REPO_ROOT / "docs" / "reports" / "G19_PLAYER_GUIDANCE_AGENT_COUNCIL_REPORT.md"

REQUIRED_G19_SCREENSHOTS = [
    "g19_01_arrival_dynamic_location.png",
    "g19_02_counting_house_guidance.png",
    "g19_03_tavern_rumor_clean_journal.png",
    "g19_04_village_exit_east_gate.png",
    "g19_05_old_road_signal_guidance.png",
    "g19_06_hidden_landing_return_lane.png",
    "g19_07_chris_screenshot_repair_composition.png",
]

REQUIRED_ZONES = [
    "newport_harbor",
    "counting_house_row",
    "third_toast_tavern",
    "working_wharf",
    "east_gate",
    "old_road",
    "signal_rise",
    "hidden_landing",
    "return_lane",
]

BANNED_COPY = ["DEBUG", "Press E", "Hook updated:", "Objective updated:", "Objective complete:"]


def project_path(raw_path: str) -> Path:
    normalized = raw_path.replace("\\", "/")
    if normalized.startswith("res://"):
        return PROJECT_ROOT / normalized.removeprefix("res://")
    if normalized.startswith("wayfarer_godot_vertical_slice/"):
        return REPO_ROOT / normalized
    return repo_path(normalized)


def main() -> int:
    failures: list[str] = []
    validate_phase_contract("G-19", failures)
    validate_phase_contract("G-20", failures)
    source = load_json(G19_SOURCE_JSON, failures)
    manifest = load_json(SCREENSHOT_MANIFEST, failures)
    report_json = load_json(G19_REPORT_JSON, failures)
    require_text(
        G19_DIRECTOR_GD,
        [
            "G19_PLAYER_GUIDANCE_PASS",
            "opening_first_session_guidance_v1.json",
            "guidance_for",
            "build_quest_region",
            "sanitize_feedback",
            "Objective updated:",
            "Hook updated:",
            "Dawn warning:",
            "guidance_contract",
        ],
        failures,
    )
    require_text(
        HUD_GD,
        [
            "OPENING_GUIDANCE_DIRECTOR",
            "set_player_world_position",
            "opening_player_guidance_contract",
            "Next:",
            "Area:",
            "sanitized_feedback",
            "no_debug_looking_prompts",
        ],
        failures,
    )
    require_text(
        MAIN_GD,
        [
            "opening_player_guidance_contract",
            "_update_player_guidance_hud",
            "set_player_world_position",
        ],
        failures,
    )
    require_text(
        MAP_LAYER_GD,
        [
            "G19_PLAYER_GUIDANCE_SCREEN_COMPOSITION_PASS",
            "_draw_g19_player_guidance_screen_composition_ground",
            "_draw_g19_player_guidance_screen_composition_routes",
            "_draw_g19_player_guidance_screen_composition_props",
            "g19_east_gate_road_shoulder_not_random_green",
            "g19_old_road_choice_guidance_no_crude_marker",
        ],
        failures,
    )
    require_text(CAPTURE_GD, REQUIRED_G19_SCREENSHOTS + ["chris_screenshot_repair_composition", "BANNED_HUD_COPY"], failures)
    require_text(CAPTURE_PS1, ["capture_g19_runtime_screenshots.gd"], failures)
    require_text(
        G19_REPORT,
        [
            "G-19 Player Guidance, Map, Journal, and Interaction Polish",
            "Human review required: no",
            "Chris screenshot repair",
            "No debug-looking prompts",
            "COUNCIL_PASS_READY_FOR_PR",
            "Next phase: G-20 First-Session Gameplay Loop and Reward Pass",
        ],
        failures,
    )
    if G19_COUNCIL_REPORT.exists():
        require_text(
            G19_COUNCIL_REPORT,
            [
                "COUNCIL_PASS_READY_FOR_PR",
                "UX Designer",
                "World/Layout Designer",
                "G-19",
            ],
            failures,
        )
    if isinstance(source, dict):
        validate_g19_source(source, failures)
    if isinstance(manifest, dict):
        validate_g19_manifest(manifest, failures)
    if isinstance(report_json, dict):
        validate_g19_report_json(report_json, failures)
    return print_result("first-session gameplay loop", failures)


def validate_g19_source(data: dict[str, Any], failures: list[str]) -> None:
    if data.get("schema_id") != "wayfarer.ui.opening_first_session_guidance.v1":
        failures.append("G-19 guidance source schema mismatch")
    if data.get("phase") != "G-19":
        failures.append("G-19 guidance source phase mismatch")
    zones = data.get("zones", [])
    if not isinstance(zones, list) or len(zones) < len(REQUIRED_ZONES):
        failures.append("G-19 guidance source missing required zones")
    else:
        zone_ids = {str(item.get("id", "")) for item in zones if isinstance(item, dict)}
        for zone_id in REQUIRED_ZONES:
            if zone_id not in zone_ids:
                failures.append(f"G-19 guidance source missing zone: {zone_id}")
    objectives = data.get("objective_guidance", [])
    if not isinstance(objectives, list) or len(objectives) < 10:
        failures.append("G-19 guidance source must include objective guidance across village and island beats")
    serialized = json.dumps(data, sort_keys=True)
    for token in ["Newport Harbor", "Counting House Row", "Third Toast Tavern", "East Gate", "Old Road", "Hidden Landing"]:
        if token not in serialized:
            failures.append(f"G-19 guidance source missing display token: {token}")
    acceptance = data.get("acceptance", {})
    for key in [
        "clean_objective_display",
        "journal_updates",
        "interaction_prompts_are_compact",
        "location_names_or_subtle_guidance",
        "quest_markers_signage_do_not_look_crude",
        "first_session_route_readability",
        "no_debug_looking_prompts",
        "screenshot_contradiction_fails_phase",
    ]:
        if not isinstance(acceptance, dict) or acceptance.get(key) is not True:
            failures.append(f"G-19 guidance acceptance missing true flag: {key}")
    for score_key in ["ux_readability_score", "world_screen_composition_score"]:
        if not isinstance(acceptance, dict) or float(acceptance.get(score_key, 0.0)) < 8.5:
            failures.append(f"G-19 guidance {score_key} must be at least 8.5")


def validate_g19_manifest(data: dict[str, Any], failures: list[str]) -> None:
    if data.get("schema_id") != "wayfarer.g19.runtime_screenshot_manifest.v1":
        failures.append("G-19 screenshot manifest schema mismatch")
    if data.get("phase") != "G-19" or data.get("status") != "PASS":
        failures.append("G-19 screenshot manifest must be PASS")
    if data.get("debug_overlays_disabled") is not True:
        failures.append("G-19 screenshot manifest must prove debug overlays disabled")
    screenshots = data.get("screenshots", [])
    if not isinstance(screenshots, list) or len(screenshots) < len(REQUIRED_G19_SCREENSHOTS):
        failures.append("G-19 screenshot manifest missing proof screenshots")
        return
    filenames = {str(item.get("filename", "")) for item in screenshots if isinstance(item, dict)}
    for filename in REQUIRED_G19_SCREENSHOTS:
        if filename not in filenames:
            failures.append(f"G-19 screenshot manifest missing {filename}")
    location_labels: set[str] = set()
    for shot in screenshots:
        if not isinstance(shot, dict):
            failures.append("G-19 screenshot row must be an object")
            continue
        if shot.get("status") != "PASS":
            failures.append(f"G-19 screenshot did not pass: {shot.get('filename')}")
        raw_path = str(shot.get("path", ""))
        if raw_path and not project_path(raw_path).exists():
            failures.append(f"G-19 screenshot path missing: {raw_path}")
        png = shot.get("png_verification", {})
        if not isinstance(png, dict) or png.get("status") != "PASS":
            failures.append(f"G-19 PNG verification failed: {shot.get('filename')}")
        copy = shot.get("hud_copy", {})
        serialized_copy = json.dumps(copy, sort_keys=True) if isinstance(copy, dict) else str(copy)
        for banned in BANNED_COPY:
            if banned in serialized_copy:
                failures.append(f"G-19 screenshot HUD copy contains banned token {banned}: {shot.get('filename')}")
        if isinstance(copy, dict):
            location_labels.add(str(copy.get("zone", "")))
            if "Next:" not in str(copy.get("quest_region", "")) or "Area:" not in str(copy.get("quest_region", "")):
                failures.append(f"G-19 screenshot HUD region missing Next/Area guidance: {shot.get('filename')}")
        contract = shot.get("opening_player_guidance_contract", {})
        if isinstance(contract, dict):
            for key in ["dynamic_location_names", "clean_objective_display", "sanitized_feedback", "no_debug_looking_prompts", "first_session_route_readability", "village_to_island_screen_composition_repair"]:
                if contract.get(key) is not True:
                    failures.append(f"G-19 screenshot contract missing {key}: {shot.get('filename')}")
        else:
            failures.append(f"G-19 screenshot missing opening_player_guidance_contract: {shot.get('filename')}")
    if len(location_labels - {""}) < 5:
        failures.append("G-19 screenshot proof must show at least five authored location labels")
    if location_labels == {"Newport Harbor"}:
        failures.append("G-19 screenshot proof still uses static Newport Harbor location only")
    result = data.get("playthrough_result", {})
    if not isinstance(result, dict) or result.get("status") != "PASS":
        failures.append("G-19 playthrough result must PASS")
    elif float(result.get("ux_readability_score", 0.0)) < 8.5 or float(result.get("world_screen_composition_score", 0.0)) < 8.5:
        failures.append("G-19 playthrough result scores must be at least 8.5")


def validate_g19_report_json(data: dict[str, Any], failures: list[str]) -> None:
    if data.get("schema_id") != "wayfarer.g19.player_guidance_report.v1":
        failures.append("G-19 report schema mismatch")
    if data.get("phase_id") != "G-19" or data.get("status") != "PASS":
        failures.append("G-19 report must be PASS")
    if data.get("human_review_required") is not False:
        failures.append("G-19 report must say human_review_required=false")
    if data.get("agent_council_verdict") != "COUNCIL_PASS_READY_FOR_PR":
        failures.append("G-19 report council verdict must be COUNCIL_PASS_READY_FOR_PR")
    raw_manifest = str(data.get("screenshot_manifest", ""))
    if not raw_manifest:
        failures.append("G-19 report missing screenshot_manifest")
    elif not project_path(raw_manifest).exists():
        failures.append(f"G-19 report screenshot_manifest path missing: {raw_manifest}")
    acceptance = data.get("acceptance", {})
    for flag in [
        "clean_objective_display",
        "journal_updates",
        "interaction_prompts_are_compact",
        "location_names_or_subtle_guidance",
        "quest_markers_signage_do_not_look_crude",
        "first_session_route_readability",
        "no_debug_looking_prompts",
        "chris_screenshot_repair",
    ]:
        if not isinstance(acceptance, dict) or acceptance.get(flag) is not True:
            failures.append(f"G-19 report acceptance missing {flag}")
    for score_key in ["ux_readability_score", "world_screen_composition_score", "technical_stability_score"]:
        if float(data.get(score_key, 0.0)) < 8.5:
            failures.append(f"G-19 report {score_key} must be at least 8.5")
    if data.get("provenance_atelier_result") != "PASS":
        failures.append("G-19 report provenance_atelier_result must be PASS")
    if data.get("north_star_result") != "PASS":
        failures.append("G-19 report north_star_result must be PASS")


if __name__ == "__main__":
    sys.exit(main())
