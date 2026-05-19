#!/usr/bin/env python3
"""Validate G-19 player guidance, map/journal, and interaction polish."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from opening_village_island_validator_common import print_result


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[1]
REPO_ROOT = PROJECT_ROOT.parent

GUIDANCE_SOURCE = PROJECT_ROOT / "data" / "ux" / "g19_player_guidance_map_journal_interaction_v1.json"
RUNTIME_LAYOUT_SOURCE = PROJECT_ROOT / "data" / "world_layout" / "g19s_newport_runtime_reconstruction_v1.json"
HUD_GD = PROJECT_ROOT / "scenes" / "ui" / "HUD.gd"
HUD_TSCN = PROJECT_ROOT / "scenes" / "ui" / "HUD.tscn"
MAIN_GD = PROJECT_ROOT / "scenes" / "Main.gd"
FIRST_LIGHT_QUEST_GD = PROJECT_ROOT / "scripts" / "quests" / "FirstLightQuest.gd"
CAPTURE_GD = PROJECT_ROOT / "tools" / "capture_g19_player_guidance_screenshots.gd"
CAPTURE_PS1 = PROJECT_ROOT / "tools" / "capture_g19_player_guidance_screenshots.ps1"
SCREENSHOT_DIR = PROJECT_ROOT / "artifacts" / "review" / "g19_player_guidance_screenshots"
SCREENSHOT_MANIFEST = SCREENSHOT_DIR / "g19_player_guidance_screenshot_manifest.json"
PHASE_REPORT = REPO_ROOT / "docs" / "reports" / "G19_PLAYER_GUIDANCE_MAP_JOURNAL_INTERACTION_POLISH.md"
COUNCIL_REPORT = REPO_ROOT / "docs" / "reports" / "G19_PLAYER_GUIDANCE_AGENT_COUNCIL_REPORT.md"

REQUIRED_VIEWPOINTS = {
    "arrival_journal_route",
    "counting_house_route_prompt",
    "counting_house_journal_update",
    "wharf_lantern_guidance",
    "tavern_whisper_route",
    "commercial_branch_guidance",
    "rear_service_lane_secret",
    "island_exit_guidance",
    "journal_reward_return_route",
    "debug_disabled_guidance_view",
}


def rel(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def load_json(path: Path, failures: list[str]) -> dict[str, Any]:
    if not path.exists():
        failures.append(f"missing required json: {rel(path)}")
        return {}
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        failures.append(f"invalid json {rel(path)}: {exc}")
        return {}
    if not isinstance(parsed, dict):
        failures.append(f"{rel(path)} root must be an object")
        return {}
    return parsed


def require_path(path: Path, failures: list[str], label: str) -> None:
    if not path.exists():
        failures.append(f"missing {label}: {rel(path)}")


def require_text(path: Path, tokens: list[str], failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing required text file: {rel(path)}")
        return ""
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        if token not in text:
            failures.append(f"{rel(path)} missing token: {token}")
    return text


def validate_g19_player_guidance(failures: list[str]) -> None:
    for path, label in [
        (GUIDANCE_SOURCE, "G-19 guidance source"),
        (RUNTIME_LAYOUT_SOURCE, "G-19S runtime layout source"),
        (CAPTURE_GD, "G-19 capture script"),
        (CAPTURE_PS1, "G-19 capture wrapper"),
        (SCREENSHOT_MANIFEST, "G-19 screenshot manifest"),
        (PHASE_REPORT, "G-19 phase report"),
        (COUNCIL_REPORT, "G-19 council report"),
    ]:
        require_path(path, failures, label)

    guidance = load_json(GUIDANCE_SOURCE, failures)
    if guidance:
        if guidance.get("schema_id") != "wayfarer.g19.player_guidance_map_journal_interaction.v1":
            failures.append("G-19 guidance source schema_id mismatch")
        if guidance.get("phase") != "G-19":
            failures.append("G-19 guidance source phase mismatch")
        if guidance.get("source_runtime_layout") != "wayfarer_godot_vertical_slice/data/world_layout/g19s_newport_runtime_reconstruction_v1.json":
            failures.append("G-19 guidance must derive from the G-19S runtime layout source")
        if len(guidance.get("objective_route_hints", [])) < 5:
            failures.append("G-19 guidance source must define at least five objective route hints")
        if len(guidance.get("location_bands", [])) < 6:
            failures.append("G-19 guidance source must define location bands")
        quality_bar = guidance.get("quality_bar", {})
        if not isinstance(quality_bar, dict) or float(quality_bar.get("g19_assigned_score", 0.0)) < 8.5:
            failures.append("G-19 guidance source must score at least 8.5")

    require_text(
        HUD_GD,
        [
            "G19_PLAYER_GUIDANCE_POLISH_PASS",
            "QuestRoute",
            "player_guidance_contract",
            "set_player_world_position",
            "Route: harborfront road -> Counting House clerk",
            "East Road - Island Exit",
            "no_debug_looking_prompts",
        ],
        failures,
    )
    require_text(HUD_TSCN, ["QuestRoute", "Route: harborfront road -> Counting House clerk"], failures)
    require_text(
        MAIN_GD,
        [
            "player_guidance_polish_contract",
            "set_player_world_position",
            "source_runtime_layout",
            "player_knows_where_to_go",
        ],
        failures,
    )
    require_text(
        FIRST_LIGHT_QUEST_GD,
        [
            "Follow the harborfront road to Edrin Vale at the Counting House.",
            "wharf apron, merchant row, or civic notice board",
            "east guidepost beyond Newport toward the island road",
        ],
        failures,
    )
    phase_report_text = require_text(
        PHASE_REPORT,
        [
            "G-19 Player Guidance, Map, Journal, and Interaction Polish",
            "No debug-looking prompts",
            "ux_readability_score",
            "G-19S runtime layout",
        ],
        failures,
    )
    council_report_text = require_text(
        COUNCIL_REPORT,
        [
            "COUNCIL_PASS_READY_FOR_PR",
            "UX Designer",
            "World/Layout Designer",
            "Player Guidance Result",
        ],
        failures,
    )
    if "NEEDS_HUMAN_REVIEW" in phase_report_text + council_report_text:
        failures.append("G-19 reports must not use deprecated human-review statuses")

    manifest = load_json(SCREENSHOT_MANIFEST, failures)
    if manifest:
        if manifest.get("schema_id") != "wayfarer.g19.player_guidance_screenshot_manifest.v1":
            failures.append("G-19 screenshot manifest schema_id mismatch")
        if manifest.get("phase") != "G-19":
            failures.append("G-19 screenshot manifest phase mismatch")
        if manifest.get("status") != "PASS":
            failures.append("G-19 screenshot manifest must be PASS")
        if manifest.get("debug_overlays_disabled") is not True:
            failures.append("G-19 screenshot manifest must prove debug overlays disabled")
        if manifest.get("hud_visible_for_guidance_proof") is not True:
            failures.append("G-19 screenshot manifest must prove HUD-visible guidance")
        final_contract = manifest.get("g19_player_guidance_contract_final", {})
        if not isinstance(final_contract, dict):
            failures.append("G-19 manifest missing final player guidance contract")
        else:
            if final_contract.get("phase") != "G-19":
                failures.append("G-19 final contract phase mismatch")
            for key in [
                "quest_available",
                "journal_visible",
                "route_hint_visible",
                "location_names_or_subtle_guidance",
                "quest_markers_signage_are_diegetic",
                "no_debug_looking_prompts",
                "no_oversized_labels_blocking_world",
                "player_knows_where_to_go",
            ]:
                if final_contract.get(key) is not True:
                    failures.append(f"G-19 final contract must prove {key}")
            if float(final_contract.get("ux_readability_score", 0.0)) < 8.5:
                failures.append("G-19 final UX readability score must be at least 8.5")
        screenshots = manifest.get("screenshots", [])
        if not isinstance(screenshots, list) or len(screenshots) < len(REQUIRED_VIEWPOINTS):
            failures.append("G-19 manifest must include all canonical guidance screenshots")
            screenshots = []
        seen = set()
        for shot in screenshots:
            if not isinstance(shot, dict):
                failures.append("G-19 screenshot entry must be an object")
                continue
            viewpoint_id = str(shot.get("viewpoint_id", ""))
            seen.add(viewpoint_id)
            if shot.get("status") != "PASS":
                failures.append(f"G-19 screenshot {viewpoint_id} must be PASS")
            raw_path = str(shot.get("path", "")).replace("res://", "")
            screenshot_path = PROJECT_ROOT / raw_path
            if not raw_path or not screenshot_path.exists():
                failures.append(f"G-19 screenshot file missing: {shot.get('path', '')}")
            if "Press E" in str(shot.get("prompt_text", "")):
                failures.append(f"G-19 screenshot {viewpoint_id} contains debug-like Press E prompt copy")
            guidance_contract = shot.get("player_guidance_contract", {})
            if isinstance(guidance_contract, dict) and guidance_contract.get("phase") != "G-19":
                failures.append(f"G-19 screenshot {viewpoint_id} guidance contract phase mismatch")
        missing_views = REQUIRED_VIEWPOINTS - seen
        for viewpoint_id in sorted(missing_views):
            failures.append(f"G-19 screenshot manifest missing required view: {viewpoint_id}")


def main() -> int:
    failures: list[str] = []
    validate_g19_player_guidance(failures)
    return print_result("G-19 player guidance map journal interaction", failures)


if __name__ == "__main__":
    sys.exit(main())
