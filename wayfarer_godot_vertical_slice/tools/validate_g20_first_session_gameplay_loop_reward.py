#!/usr/bin/env python3
"""Validate the G-20 first-session gameplay-loop and reward pass."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from opening_village_island_validator_common import (
    PROJECT_ROOT,
    REPO_ROOT,
    load_json,
    print_result,
    require_text,
    repo_path,
    validate_phase_contract,
)


SOURCE_JSON = PROJECT_ROOT / "data" / "quests" / "g20_first_session_gameplay_loop_reward_v1.json"
G19_GUIDANCE_SOURCE = PROJECT_ROOT / "data" / "ux" / "g19_player_guidance_map_journal_interaction_v1.json"
RUNTIME_LAYOUT_SOURCE = PROJECT_ROOT / "data" / "world_layout" / "g19s_newport_runtime_reconstruction_v1.json"
BLOCKOUT_SOURCE = REPO_ROOT / "docs" / "design" / "NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.json"
FIRST_LIGHT_QUEST_GD = PROJECT_ROOT / "scripts" / "quests" / "FirstLightQuest.gd"
MAIN_GD = PROJECT_ROOT / "scenes" / "Main.gd"
HUD_GD = PROJECT_ROOT / "scenes" / "ui" / "HUD.gd"
CAPTURE_GD = PROJECT_ROOT / "tools" / "capture_g20_first_session_gameplay_loop_screenshots.gd"
CAPTURE_PS1 = PROJECT_ROOT / "tools" / "capture_g20_first_session_gameplay_loop_screenshots.ps1"
SCREENSHOT_DIR = PROJECT_ROOT / "artifacts" / "review" / "g20_first_session_gameplay_loop"
SCREENSHOT_MANIFEST = SCREENSHOT_DIR / "g20_first_session_screenshot_manifest.json"
TRACE_JSON = SCREENSHOT_DIR / "g20_first_session_trace.json"
PLAYTEST_LOG = SCREENSHOT_DIR / "g20_first_session_playtest_log.md"
PHASE_REPORT = REPO_ROOT / "docs" / "reports" / "G20_FIRST_SESSION_GAMEPLAY_LOOP_REWARD_PASS.md"
COUNCIL_REPORT = REPO_ROOT / "docs" / "reports" / "G20_FIRST_SESSION_GAMEPLAY_AGENT_COUNCIL_REPORT.md"

REQUIRED_VIEWPOINTS = {
    "arrival_goal",
    "counting_house_first_talk",
    "wharf_investigation_reward",
    "tavern_whisper_social_hook",
    "choice_branch_next_lead",
    "island_exit_reward_hook",
    "old_road_explore",
    "hidden_landing_discovery",
    "return_report_choice",
    "final_reward_next_hook",
    "debug_disabled_first_session",
}

REQUIRED_BEATS = {
    "arrive",
    "orient",
    "talk",
    "investigate",
    "tavern_whisper",
    "choose",
    "explore",
    "discover",
    "return_report",
    "continue",
}

REQUIRED_REWARDS = [
    "Reward: Resolve +5 for following the tavern whisper",
    "Named contact: Edrin Vale",
    "Access: old road island lead",
    "Reward: Resolve +8 for proving the island clue",
    "Named contact: Annelise Crow",
]


def rel(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def project_path(raw_path: str) -> Path:
    normalized = raw_path.replace("\\", "/")
    if normalized.startswith("res://"):
        return PROJECT_ROOT / normalized.removeprefix("res://")
    if normalized.startswith("wayfarer_godot_vertical_slice/"):
        return REPO_ROOT / normalized
    return repo_path(normalized)


def require_path(path: Path, failures: list[str], label: str) -> None:
    if not path.exists():
        failures.append(f"missing {label}: {rel(path)}")


def main() -> int:
    failures: list[str] = []
    validate_phase_contract("G-20", failures)
    for path, label in [
        (SOURCE_JSON, "G-20 first-session source"),
        (G19_GUIDANCE_SOURCE, "G-19 guidance source dependency"),
        (RUNTIME_LAYOUT_SOURCE, "G-19S runtime layout dependency"),
        (BLOCKOUT_SOURCE, "G-19R blockout dependency"),
        (CAPTURE_GD, "G-20 capture script"),
        (CAPTURE_PS1, "G-20 capture wrapper"),
        (SCREENSHOT_MANIFEST, "G-20 screenshot manifest"),
        (TRACE_JSON, "G-20 first-session trace"),
        (PLAYTEST_LOG, "G-20 playtest log"),
        (PHASE_REPORT, "G-20 phase report"),
        (COUNCIL_REPORT, "G-20 council report"),
    ]:
        require_path(path, failures, label)

    source = load_json(SOURCE_JSON, failures)
    manifest = load_json(SCREENSHOT_MANIFEST, failures)
    trace = load_json(TRACE_JSON, failures)

    require_text(
        FIRST_LIGHT_QUEST_GD,
        [
            "G20_FIRST_SESSION_GAMEPLAY_LOOP_REWARD_PASS",
            "debug_first_session_gameplay_loop_reward_contract",
            "first_20_30_minutes_playable",
            "player_receives_feedback_and_reward",
            "player_has_reason_to_continue",
            "no_dead_objective_states",
            "QUEST_REWARD_LABEL",
            "ISLAND_EVIDENCE_REWARD_LABEL",
            "first_time_player_reason_to_continue",
        ],
        failures,
    )
    require_text(
        MAIN_GD,
        [
            "first_session_gameplay_loop_reward_contract",
            "source_loop",
            "first_20_30_minutes_playable",
            "reward_feedback_visible",
            "quest_geography_loop",
            "implementation_readiness_score",
        ],
        failures,
    )
    require_text(
        HUD_GD,
        [
            "G20_FIRST_SESSION_LOOP_REWARD_PASS",
            "first_session_reward_loop_contract",
            "reward_feedback_visible",
            "latest_reward",
            "has_reward_feedback",
        ],
        failures,
    )
    require_text(
        CAPTURE_GD,
        [
            "g20_first_session_screenshot_manifest.json",
            "g20_first_session_trace.json",
            "g20_first_session_playtest_log.md",
            "first_session_gameplay_loop_reward_contract",
            "debug_disabled_first_session",
        ]
        + sorted(REQUIRED_VIEWPOINTS),
        failures,
    )
    require_text(CAPTURE_PS1, ["capture_g20_first_session_gameplay_loop_screenshots.gd", "g20_first_session_gameplay_loop"], failures)
    require_text(
        PLAYTEST_LOG,
        [
            "G-20 First-Session Gameplay Loop Playtest Log",
            "Playthrough result: PASS",
            "Reward Resolve total: 13",
            "Reason to continue",
        ],
        failures,
    )
    phase_report_text = require_text(
        PHASE_REPORT,
        [
            "G-20 First-Session Gameplay Loop and Reward Pass",
            "first 20-30 minutes",
            "reward cadence",
            "reason to continue",
            "COUNCIL_PASS_READY_FOR_PR",
            "Next phase: G-21 Opening Island Performance, Browser Build, and Regression Hardening",
        ],
        failures,
    )
    council_report_text = require_text(
        COUNCIL_REPORT,
        [
            "COUNCIL_PASS_READY_FOR_PR",
            "World-class Game Designer",
            "Narrative/Quest Designer",
            "First-Session Gameplay Result",
            "Human review required: no",
        ],
        failures,
    )
    forbidden = ["NEEDS_HUMAN_REVIEW", "READY_FOR_HUMAN_VISUAL_REVIEW", "AWAITING_CHRIS_REVIEW", "TECHNICAL_PASS_ONLY"]
    for token in forbidden:
        if token in phase_report_text or token in council_report_text:
            failures.append(f"G-20 reports must not contain deprecated status: {token}")

    if isinstance(source, dict):
        validate_source(source, failures)
    if isinstance(manifest, dict):
        validate_manifest(manifest, failures)
    if isinstance(trace, dict):
        validate_final_contract(trace, failures, "trace")
    return print_result("G-20 first-session gameplay loop reward", failures)


def validate_source(data: dict[str, Any], failures: list[str]) -> None:
    if data.get("schema_id") != "wayfarer.g20.first_session_gameplay_loop_reward.v1":
        failures.append("G-20 source schema_id mismatch")
    if data.get("phase") != "G-20":
        failures.append("G-20 source phase mismatch")
    duration = data.get("first_session_duration_target_minutes", {})
    if not isinstance(duration, dict) or int(duration.get("minimum", 0)) < 20 or int(duration.get("maximum", 0)) > 30:
        failures.append("G-20 duration target must stay within first 20-30 minutes")
    beats = data.get("player_experience_arc", [])
    if not isinstance(beats, list) or len(beats) < 10:
        failures.append("G-20 source must define at least ten first-session beats")
        beats = []
    beat_ids = {str(item.get("beat_id", "")) for item in beats if isinstance(item, dict)}
    for beat_id in REQUIRED_BEATS:
        if beat_id not in beat_ids:
            failures.append(f"G-20 source missing beat: {beat_id}")
    cadence = data.get("reward_cadence", [])
    if not isinstance(cadence, list) or len(cadence) < 6:
        failures.append("G-20 source must define reward cadence")
    serialized = json.dumps(data, sort_keys=True)
    for token in [
        "Newport Harbor",
        "Counting House",
        "Tavern/Inn",
        "Third Toast",
        "old road",
        "hidden landing",
        "Governor's men",
        "pre-Revolution",
    ]:
        if token not in serialized:
            failures.append(f"G-20 source missing token: {token}")
    for reward in REQUIRED_REWARDS:
        if reward not in serialized:
            failures.append(f"G-20 source missing reward: {reward}")
    acceptance = data.get("acceptance", {})
    for flag in [
        "first_session_playable",
        "first_20_30_minutes_playable",
        "player_receives_feedback_and_reward",
        "player_has_reason_to_continue",
        "no_dead_objective_states",
        "arrive_orient_talk_investigate_explore_discover_return_report_reward_continue",
        "quest_geography_uses_newport_and_island",
        "source_layout_not_bypassed",
        "npc_movement_policy_blocks_static_sprite_glide",
    ]:
        if not isinstance(acceptance, dict) or acceptance.get(flag) is not True:
            failures.append(f"G-20 acceptance missing true flag: {flag}")
    for score_key in [
        "gameplay_hook_score",
        "reward_cadence_score",
        "world_cohesion_score",
        "player_orientation_score",
        "quest_geography_integration_score",
        "implementation_readiness_score",
    ]:
        if not isinstance(acceptance, dict) or float(acceptance.get(score_key, 0.0)) < 8.5:
            failures.append(f"G-20 source {score_key} must be at least 8.5")


def validate_manifest(data: dict[str, Any], failures: list[str]) -> None:
    if data.get("schema_id") != "wayfarer.g20.first_session_screenshot_manifest.v1":
        failures.append("G-20 screenshot manifest schema mismatch")
    if data.get("phase") != "G-20" or data.get("status") != "PASS":
        failures.append("G-20 screenshot manifest must be PASS for G-20")
    if data.get("debug_overlays_disabled") is not True:
        failures.append("G-20 manifest must prove debug overlays disabled")
    if data.get("hud_visible_for_reward_proof") is not True:
        failures.append("G-20 manifest must prove HUD-visible reward guidance")
    final_contract = data.get("first_session_contract_final", {})
    if not isinstance(final_contract, dict):
        failures.append("G-20 manifest missing final first-session contract")
    else:
        validate_final_contract(final_contract, failures, "manifest final contract")
    screenshots = data.get("screenshots", [])
    if not isinstance(screenshots, list) or len(screenshots) < len(REQUIRED_VIEWPOINTS):
        failures.append("G-20 manifest must include all canonical first-session screenshots")
        screenshots = []
    seen = set()
    reward_visible_count = 0
    for shot in screenshots:
        if not isinstance(shot, dict):
            failures.append("G-20 screenshot entry must be an object")
            continue
        viewpoint_id = str(shot.get("viewpoint_id", ""))
        seen.add(viewpoint_id)
        if shot.get("status") != "PASS":
            failures.append(f"G-20 screenshot {viewpoint_id} must be PASS")
        path = project_path(str(shot.get("path", "")))
        if not str(shot.get("path", "")).strip() or not path.exists():
            failures.append(f"G-20 screenshot file missing: {shot.get('path', '')}")
        dimensions = shot.get("dimensions", {})
        if not isinstance(dimensions, dict) or int(dimensions.get("w", 0)) < 1200 or int(dimensions.get("h", 0)) < 800:
            failures.append(f"G-20 screenshot {viewpoint_id} dimensions too small")
        png = shot.get("png_verification", {})
        if not isinstance(png, dict) or png.get("status") != "PASS":
            failures.append(f"G-20 screenshot {viewpoint_id} missing PNG PASS verification")
        reward_contract = shot.get("reward_loop_contract", {})
        if isinstance(reward_contract, dict) and reward_contract.get("reward_feedback_visible") is True:
            reward_visible_count += 1
        first_session_contract = shot.get("first_session_contract", {})
        if isinstance(first_session_contract, dict) and first_session_contract.get("phase") != "G-20":
            failures.append(f"G-20 screenshot {viewpoint_id} first-session contract phase mismatch")
    for viewpoint_id in sorted(REQUIRED_VIEWPOINTS - seen):
        failures.append(f"G-20 manifest missing required view: {viewpoint_id}")
    if reward_visible_count < 2:
        failures.append("G-20 screenshots must show reward feedback in at least two beats")


def validate_final_contract(data: dict[str, Any], failures: list[str], label: str) -> None:
    if data.get("phase") != "G-20":
        failures.append(f"G-20 {label} phase mismatch")
    if data.get("status") != "PASS":
        failures.append(f"G-20 {label} status must be PASS")
    minutes = int(data.get("playable_minutes_estimate", 0))
    if minutes < 20 or minutes > 30:
        failures.append(f"G-20 {label} playable_minutes_estimate must be 20-30")
    for flag in [
        "first_session_playable",
        "first_20_30_minutes_playable",
        "arrive",
        "orient",
        "talk",
        "investigate",
        "explore",
        "discover",
        "return_report",
        "reward_progression",
        "unlock_next_hook",
        "player_receives_feedback_and_reward",
        "player_has_reason_to_continue",
        "no_dead_objective_states",
    ]:
        if data.get(flag) is not True:
            failures.append(f"G-20 {label} must prove {flag}")
    if int(data.get("reward_resolve", 0)) < 13:
        failures.append(f"G-20 {label} must prove at least 13 Resolve reward")
    rewards = [str(item) for item in data.get("reward_log", [])]
    for reward in REQUIRED_REWARDS:
        if reward not in rewards:
            failures.append(f"G-20 {label} missing reward: {reward}")
    if len(data.get("loop_beats", [])) < 10:
        failures.append(f"G-20 {label} must include at least ten loop beats")
    if len(data.get("playthrough_trace", [])) < 12:
        failures.append(f"G-20 {label} must include a full playthrough trace")
    if "harbor arrival" not in str(data.get("quest_geography_loop", "")):
        failures.append(f"G-20 {label} must describe the harbor-to-island-to-return quest geography")
    if "Governor" not in str(data.get("first_time_player_reason_to_continue", "")):
        failures.append(f"G-20 {label} must include a strong reason-to-continue hook")
    for score_key in [
        "gameplay_hook_score",
        "reward_cadence_score",
        "world_cohesion_score",
        "player_orientation_score",
        "quest_geography_integration_score",
        "implementation_readiness_score",
    ]:
        if float(data.get(score_key, 0.0)) < 8.5:
            failures.append(f"G-20 {label} {score_key} must be at least 8.5")


if __name__ == "__main__":
    sys.exit(main())
