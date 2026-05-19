#!/usr/bin/env python3
"""Validate the G-18A multi-path rumor/choice foundation contract."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from opening_village_island_validator_common import PROJECT_ROOT, REPO_ROOT, load_json, print_result, require_text, repo_path, validate_phase_contract


SOURCE_JSON = PROJECT_ROOT / "data" / "quests" / "whispers_before_dawn_multipath_rumor_choice_v1.json"
FIRST_LIGHT_QUEST_JSON = PROJECT_ROOT / "data" / "quests" / "first_light_whispers_before_dawn.json"
FIRST_LIGHT_QUEST_GD = PROJECT_ROOT / "scripts" / "quests" / "FirstLightQuest.gd"
MAIN_GD = PROJECT_ROOT / "scenes" / "Main.gd"
CAPTURE_GD = PROJECT_ROOT / "tools" / "capture_g18a_multipath_choice_proof.gd"
CAPTURE_PS1 = PROJECT_ROOT / "tools" / "capture_g18a_multipath_choice_proof.ps1"
SCREENSHOT_MANIFEST = PROJECT_ROOT / "artifacts" / "review" / "g18a_runtime_screenshots" / "g18a_runtime_screenshot_manifest.json"
BRANCH_PROOF_DIR = PROJECT_ROOT / "artifacts" / "review" / "g18a_quest_branch_proof"
BRANCH_TRACE = BRANCH_PROOF_DIR / "multipath_branch_trace.json"
BRANCH_SCREENSHOT_MANIFEST = BRANCH_PROOF_DIR / "multipath_branch_screenshot_manifest.json"
BRANCH_LOG = BRANCH_PROOF_DIR / "multipath_branch_log.md"
G18A_REPORT = REPO_ROOT / "docs" / "reports" / "G18A_MULTIPATH_RUMOR_CHOICE_FOUNDATION.md"
G18A_REPORT_JSON = REPO_ROOT / "docs" / "reports" / "G18A_MULTIPATH_RUMOR_CHOICE_FOUNDATION.json"
G18A_COUNCIL_REPORT = REPO_ROOT / "docs" / "reports" / "G18A_MULTIPATH_RUMOR_CHOICE_AGENT_COUNCIL_REPORT.md"

REQUIRED_PATHS = [
    "counting_house_path",
    "tavern_rumor_path",
    "dockworker_harbor_path",
    "optional_island_clue_path",
]

REQUIRED_FLAGS = [
    "island_route_choice",
    "optional_clue_enriched_journal",
    "return_report_route_choice",
]

REQUIRED_SCREENSHOTS = [
    "g18a_01_counting_house_path.png",
    "g18a_02_tavern_rumor_path.png",
    "g18a_03_dockworker_harbor_path.png",
    "g18a_04_optional_island_clue_path.png",
    "g18a_05_return_report_choice.png",
    "g18a_06_branch_contract_journal.png",
]


def project_path(raw_path: str) -> Path:
    normalized = raw_path.replace("\\", "/")
    if normalized.startswith("res://"):
        return PROJECT_ROOT / normalized.removeprefix("res://")
    if normalized.startswith("wayfarer_godot_vertical_slice/"):
        return REPO_ROOT / normalized
    return repo_path(normalized)


def main() -> int:
    failures: list[str] = []
    validate_phase_contract("G-18A", failures)
    source = load_json(SOURCE_JSON, failures)
    quest_data = load_json(FIRST_LIGHT_QUEST_JSON, failures)
    manifest = load_json(SCREENSHOT_MANIFEST, failures)
    trace = load_json(BRANCH_TRACE, failures)
    branch_screenshot_manifest = load_json(BRANCH_SCREENSHOT_MANIFEST, failures)
    report_json = load_json(G18A_REPORT_JSON, failures)
    require_text(
        FIRST_LIGHT_QUEST_GD,
        [
            "G18A_MULTIPATH_RUMOR_CHOICE_PASS",
            "debug_village_to_island_multipath_choice_contract",
            "_simulate_island_branch",
            "counting_house_path",
            "tavern_rumor_path",
            "dockworker_harbor_path",
            "optional_island_clue_path",
            "optional_clue_enriched_journal",
            "return_report_route_choice",
            "island_route_choice",
        ],
        failures,
    )
    require_text(
        MAIN_GD,
        [
            "opening_village_to_island_multipath_choice_contract",
            "village_to_island_multipath_choice_contract",
            "debug_apply_first_light_quest_events",
        ],
        failures,
    )
    require_text(CAPTURE_GD, REQUIRED_SCREENSHOTS + ["multipath_branch_trace.json", "multipath_branch_log.md"], failures)
    require_text(CAPTURE_PS1, ["capture_g18a_multipath_choice_proof.gd"], failures)
    require_text(
        G18A_REPORT,
        [
            "G-18A Multi-Path Rumor and Choice Foundation",
            "Human review required: no",
            "counting-house",
            "tavern",
            "dockworker",
            "optional island clue",
            "COUNCIL_PASS_READY_FOR_PR",
            "Next phase: G-19 Player Guidance, Map, Journal, and Interaction Polish",
        ],
        failures,
    )
    if G18A_COUNCIL_REPORT.exists():
        require_text(
            G18A_COUNCIL_REPORT,
            [
                "COUNCIL_PASS_READY_FOR_PR",
                "Quest Designer",
                "Narrative Designer",
                "Multi-Path Rumor and Choice Foundation",
                "G-18A",
            ],
            failures,
        )
    require_text(
        BRANCH_LOG,
        [
            "G-18A Multi-Path Branch Log",
            "Whispers Before Dawn",
            "Player agency exists: true",
            "No broken branches: true",
            "Playthrough result: PASS",
        ],
        failures,
    )
    if isinstance(source, dict):
        validate_source(source, failures)
    if isinstance(quest_data, dict):
        validate_quest_data(quest_data, failures)
    if isinstance(manifest, dict):
        validate_manifest(manifest, failures)
    if isinstance(trace, dict):
        validate_trace(trace, failures)
    if isinstance(branch_screenshot_manifest, dict):
        validate_branch_screenshot_manifest(branch_screenshot_manifest, failures)
    if isinstance(report_json, dict):
        validate_report_json(report_json, failures)
    return print_result("multipath rumor choice foundation", failures)


def validate_source(data: dict[str, Any], failures: list[str]) -> None:
    if data.get("schema_id") != "wayfarer.quest.whispers_before_dawn_multipath_rumor_choice.v1":
        failures.append("G-18A source schema mismatch")
    if data.get("phase") != "G-18A":
        failures.append("G-18A source phase mismatch")
    for key in ["runtime_contract", "main_contract", "screenshot_manifest", "branch_trace"]:
        if not str(data.get(key, "")).strip():
            failures.append(f"G-18A source missing {key}")
    path_rows = data.get("required_paths", [])
    if not isinstance(path_rows, list) or len(path_rows) < 4:
        failures.append("G-18A source must define four required paths")
    else:
        path_ids = {str(item.get("id", "")) for item in path_rows if isinstance(item, dict)}
        for path_id in REQUIRED_PATHS:
            if path_id not in path_ids:
                failures.append(f"G-18A source missing path: {path_id}")
    serialized = json.dumps(data, sort_keys=True)
    for token in ["Edrin Vale", "Bess Armitage", "Mara Pike", "Mara Oren", "Annelise Crow", "pre-Revolutionary"]:
        if token not in serialized:
            failures.append(f"G-18A source missing token: {token}")
    for flag in REQUIRED_FLAGS:
        if flag not in serialized:
            failures.append(f"G-18A source missing choice-effect flag: {flag}")
    minimums = data.get("minimums", {})
    if not isinstance(minimums, dict) or int(minimums.get("minimum_advancement_npcs", 0)) < 2:
        failures.append("G-18A minimum advancement NPC count must be at least 2")
    if not isinstance(minimums, dict) or int(minimums.get("minimum_distinct_route_choices", 0)) < 3:
        failures.append("G-18A minimum distinct route choice count must be at least 3")
    acceptance = data.get("acceptance", {})
    for flag in [
        "player_agency_exists",
        "quest_state_supports_branching",
        "two_npcs_can_advance_main_thread",
        "optional_discovery_enriches_journal",
        "choice_changes_dialogue_route_or_next_objective_text",
        "no_broken_branches",
        "no_unclear_progression",
    ]:
        if not isinstance(acceptance, dict) or acceptance.get(flag) is not True:
            failures.append(f"G-18A acceptance missing true flag: {flag}")
    for score_key in ["design_score", "quest_narrative_score", "ux_readability_score"]:
        if not isinstance(acceptance, dict) or float(acceptance.get(score_key, 0.0)) < 8.5:
            failures.append(f"G-18A acceptance {score_key} must be at least 8.5")


def validate_quest_data(data: dict[str, Any], failures: list[str]) -> None:
    if "G-18A" not in [str(item) for item in data.get("phase_extensions", [])]:
        failures.append("first_light quest data must include G-18A phase extension")
    extension = data.get("opening_island_multipath_choice_extension", {})
    if not isinstance(extension, dict):
        failures.append("first_light quest data missing opening_island_multipath_choice_extension")
        return
    if extension.get("phase") != "G-18A":
        failures.append("opening_island_multipath_choice_extension phase must be G-18A")
    for path_id in REQUIRED_PATHS:
        if path_id not in [str(item) for item in extension.get("required_paths", [])]:
            failures.append(f"opening_island_multipath_choice_extension missing path: {path_id}")
    for effect in REQUIRED_FLAGS:
        if effect not in [str(item) for item in extension.get("choice_effects", [])]:
            failures.append(f"opening_island_multipath_choice_extension missing choice effect: {effect}")
    acceptance = extension.get("acceptance", {})
    for flag in ["player_agency_exists", "quest_state_supports_branching", "no_broken_branches", "no_unclear_progression"]:
        if not isinstance(acceptance, dict) or acceptance.get(flag) is not True:
            failures.append(f"opening_island_multipath_choice_extension missing acceptance flag: {flag}")


def validate_manifest(data: dict[str, Any], failures: list[str]) -> None:
    if data.get("schema_id") != "wayfarer.g18a.runtime_screenshot_manifest.v1":
        failures.append("G-18A screenshot manifest schema mismatch")
    if data.get("phase") != "G-18A" or data.get("status") != "PASS":
        failures.append("G-18A screenshot manifest must be PASS for G-18A")
    if data.get("debug_overlays_disabled") is not True:
        failures.append("G-18A screenshot manifest must prove debug overlays disabled")
    screenshots = data.get("screenshots", [])
    if not isinstance(screenshots, list) or len(screenshots) < len(REQUIRED_SCREENSHOTS):
        failures.append("G-18A screenshot manifest missing proof screenshots")
    else:
        filenames = {str(item.get("filename", "")) for item in screenshots if isinstance(item, dict)}
        for filename in REQUIRED_SCREENSHOTS:
            if filename not in filenames:
                failures.append(f"G-18A screenshot manifest missing {filename}")
        for shot in screenshots:
            if not isinstance(shot, dict):
                failures.append("G-18A screenshot row must be an object")
                continue
            if shot.get("status") != "PASS":
                failures.append(f"G-18A screenshot did not pass: {shot.get('filename')}")
            raw_path = str(shot.get("path", ""))
            if raw_path and not project_path(raw_path).exists():
                failures.append(f"G-18A screenshot path missing: {raw_path}")
    result = data.get("playthrough_result", {})
    if isinstance(result, dict):
        for flag in [
            "player_agency_exists",
            "quest_state_supports_branching",
            "two_npcs_can_advance_main_thread",
            "optional_discovery_enriches_journal",
            "choice_changes_dialogue_route_or_next_objective_text",
            "no_broken_branches",
        ]:
            if result.get(flag) is not True:
                failures.append(f"G-18A playthrough result missing true flag: {flag}")
    else:
        failures.append("G-18A manifest missing playthrough_result")


def validate_trace(data: dict[str, Any], failures: list[str]) -> None:
    if data.get("schema_id") != "wayfarer.g18a.multipath_branch_trace.v1":
        failures.append("G-18A branch trace schema mismatch")
    if data.get("phase") != "G-18A" or data.get("status") != "PASS":
        failures.append("G-18A branch trace must be PASS for G-18A")
    steps = data.get("steps", [])
    if not isinstance(steps, list) or len(steps) < len(REQUIRED_SCREENSHOTS):
        failures.append("G-18A branch trace missing steps")
    else:
        seen = {str(step.get("step_id", "")) for step in steps if isinstance(step, dict)}
        for step_id in ["counting_house_path", "tavern_rumor_path", "dockworker_harbor_path", "optional_island_clue_path", "return_report_choice", "branch_contract_journal"]:
            if step_id not in seen:
                failures.append(f"G-18A branch trace missing step: {step_id}")
    contract = data.get("branch_contract", {})
    if not isinstance(contract, dict):
        failures.append("G-18A branch trace missing branch_contract")
        return
    if contract.get("phase") != "G-18A":
        failures.append("G-18A branch contract phase mismatch")
    for flag in [
        "player_agency_exists",
        "quest_state_supports_branching",
        "two_npcs_can_advance_main_thread",
        "optional_discovery_enriches_journal",
        "choice_changes_dialogue_route_or_next_objective_text",
        "no_broken_branches",
    ]:
        if contract.get(flag) is not True:
            failures.append(f"G-18A branch contract missing true flag: {flag}")
    if int(contract.get("advancement_source_count", 0)) < 2:
        failures.append("G-18A branch contract must prove at least two advancement NPCs")
    if len(contract.get("distinct_route_choices", [])) < 3:
        failures.append("G-18A branch contract must prove at least three distinct route choices")
    branch_results = contract.get("branch_results", {})
    if not isinstance(branch_results, dict):
        failures.append("G-18A branch_results must be an object")
        return
    for path_id in REQUIRED_PATHS:
        branch = branch_results.get(path_id)
        if not isinstance(branch, dict):
            failures.append(f"G-18A missing branch result: {path_id}")
            continue
        if branch.get("branch_playable") is not True:
            failures.append(f"G-18A branch not playable: {path_id}")
        flags = branch.get("flags", {})
        if not isinstance(flags, dict) or not str(flags.get("island_route_choice", "")).strip():
            failures.append(f"G-18A branch missing island_route_choice: {path_id}")
    optional_branch = branch_results.get("optional_island_clue_path", {})
    if isinstance(optional_branch, dict):
        optional_flags = optional_branch.get("flags", {})
        if not isinstance(optional_flags, dict) or optional_flags.get("optional_clue_enriched_journal") is not True:
            failures.append("G-18A optional branch must set optional_clue_enriched_journal")


def validate_branch_screenshot_manifest(data: dict[str, Any], failures: list[str]) -> None:
    if data.get("schema_id") != "wayfarer.g18a.multipath_branch_screenshot_manifest.v1":
        failures.append("G-18A branch screenshot manifest schema mismatch")
    if data.get("phase") != "G-18A" or data.get("status") != "PASS":
        failures.append("G-18A branch screenshot manifest must be PASS")
    screenshots = data.get("screenshots", [])
    if not isinstance(screenshots, list) or len(screenshots) < len(REQUIRED_SCREENSHOTS):
        failures.append("G-18A branch screenshot manifest missing screenshot rows")


def validate_report_json(data: dict[str, Any], failures: list[str]) -> None:
    if data.get("schema_id") != "wayfarer.g18a.multipath_rumor_choice_report.v1":
        failures.append("G-18A report schema mismatch")
    if data.get("phase_id") != "G-18A" or data.get("status") != "PASS":
        failures.append("G-18A report must be PASS")
    if data.get("human_review_required") is not False:
        failures.append("G-18A report must say human_review_required=false")
    if data.get("agent_council_verdict") != "COUNCIL_PASS_READY_FOR_PR":
        failures.append("G-18A report council verdict must be COUNCIL_PASS_READY_FOR_PR")
    acceptance = data.get("acceptance", {})
    for flag in [
        "player_agency_exists",
        "quest_state_supports_branching",
        "two_npcs_can_advance_main_thread",
        "optional_discovery_enriches_journal",
        "choice_changes_dialogue_route_or_next_objective_text",
        "no_broken_branches",
        "no_unclear_progression",
    ]:
        if not isinstance(acceptance, dict) or acceptance.get(flag) is not True:
            failures.append(f"G-18A report acceptance missing {flag}")
    for score_key in ["design_score", "quest_narrative_score", "ux_readability_score", "technical_stability_score"]:
        if float(data.get(score_key, 0.0)) < 8.5:
            failures.append(f"G-18A report {score_key} must be at least 8.5")


if __name__ == "__main__":
    sys.exit(main())
