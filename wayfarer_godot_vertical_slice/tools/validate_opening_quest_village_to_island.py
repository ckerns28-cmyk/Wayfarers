#!/usr/bin/env python3
"""Validate the G-18 village-to-island opening quest contract."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from opening_village_island_validator_common import PROJECT_ROOT, REPO_ROOT, load_json, print_result, require_text, repo_path, validate_phase_contract


SOURCE_JSON = PROJECT_ROOT / "data" / "quests" / "whispers_before_dawn_village_to_island_v1.json"
FIRST_LIGHT_QUEST_JSON = PROJECT_ROOT / "data" / "quests" / "first_light_whispers_before_dawn.json"
FIRST_LIGHT_QUEST_GD = PROJECT_ROOT / "scripts" / "quests" / "FirstLightQuest.gd"
MAIN_GD = PROJECT_ROOT / "scenes" / "Main.gd"
CAPTURE_GD = PROJECT_ROOT / "tools" / "capture_g18_quest_playthrough.gd"
CAPTURE_PS1 = PROJECT_ROOT / "tools" / "capture_g18_quest_playthrough.ps1"
SCREENSHOT_MANIFEST = PROJECT_ROOT / "artifacts" / "review" / "g18_runtime_screenshots" / "g18_runtime_screenshot_manifest.json"
QUEST_PROOF_DIR = PROJECT_ROOT / "artifacts" / "review" / "g18_quest_playthrough"
QUEST_TRACE = QUEST_PROOF_DIR / "quest_playthrough_state_trace.json"
QUEST_SCREENSHOT_MANIFEST = QUEST_PROOF_DIR / "quest_playthrough_screenshot_manifest.json"
QUEST_LOG = QUEST_PROOF_DIR / "quest_playthrough_log.md"
G18_REPORT = REPO_ROOT / "docs" / "reports" / "G18_OPENING_QUEST_VILLAGE_TO_ISLAND.md"
G18_REPORT_JSON = REPO_ROOT / "docs" / "reports" / "G18_OPENING_QUEST_VILLAGE_TO_ISLAND.json"
G18_COUNCIL_REPORT = REPO_ROOT / "docs" / "reports" / "G18_OPENING_QUEST_AGENT_COUNCIL_REPORT.md"

REQUIRED_OBJECTIVES = [
    "make_landfall",
    "report_to_counting_house",
    "investigate_missing_line",
    "follow_tavern_whisper",
    "choose_next_lead",
    "lantern_at_wharf",
    "secure_contact",
    "follow_island_lead",
    "travel_to_island_clue_site",
    "discover_physical_evidence",
    "return_or_report_choice",
    "hook_to_continue",
]

REQUIRED_STEPS = [
    "arrival",
    "first_objective",
    "counting_house_clerk",
    "missing_manifest_or_harbor_ledger",
    "tavern_whisper",
    "npc_rumor_interaction",
    "island_lead",
    "travel_to_island",
    "island_clue_discovery",
    "optional_clue_or_branch",
    "return_report_or_next_hook",
    "reward_progression_update",
    "reason_to_continue",
]

REQUIRED_SCREENSHOTS = [
    "g18_01_arrival_first_objective.png",
    "g18_02_counting_house_missing_manifest.png",
    "g18_03_harbor_ledger_dockworker.png",
    "g18_04_tavern_third_toast_whisper.png",
    "g18_05_wharf_lantern_rumor.png",
    "g18_06_edrin_dawn_hook_to_island.png",
    "g18_07_village_exit_island_lead.png",
    "g18_08_old_road_coded_whisper.png",
    "g18_09_signal_optional_clue.png",
    "g18_10_hidden_landing_physical_evidence.png",
    "g18_11_return_contact_report_choice.png",
    "g18_12_return_to_town_reward_next_hook.png",
]

REQUIRED_ISLAND_FLAGS = [
    "island_lead_active",
    "coded_whisper_confirmed",
    "optional_signal_cache_clue",
    "island_physical_evidence_found",
    "return_report_choice",
    "reason_to_continue_after_island",
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
    validate_phase_contract("G-18", failures)
    source = load_json(SOURCE_JSON, failures)
    quest_data = load_json(FIRST_LIGHT_QUEST_JSON, failures)
    manifest = load_json(SCREENSHOT_MANIFEST, failures)
    trace = load_json(QUEST_TRACE, failures)
    quest_screenshot_manifest = load_json(QUEST_SCREENSHOT_MANIFEST, failures)
    report_json = load_json(G18_REPORT_JSON, failures)
    require_text(
        FIRST_LIGHT_QUEST_GD,
        [
            "G18_OPENING_QUEST_VILLAGE_TO_ISLAND_PASS",
            "debug_village_to_island_playthrough_contract",
            "follow_island_lead",
            "travel_to_island_clue_site",
            "discover_physical_evidence",
            "return_or_report_choice",
            "isla_brooke_farmhand",
            "elias_ward_suspicious_courier",
            "mara_oren_coast_patrol",
            "tomas_reed_dock_runner",
            "annelise_crow_rumor_contact",
            "ISLAND_EVIDENCE_REWARD_LABEL",
            "reason_to_continue_after_island",
        ],
        failures,
    )
    require_text(
        MAIN_GD,
        [
            "opening_village_to_island_quest_contract",
            "village_to_island_quest_contract",
            "debug_apply_first_light_quest_events",
        ],
        failures,
    )
    require_text(CAPTURE_GD, REQUIRED_SCREENSHOTS + ["quest_playthrough_state_trace.json", "quest_playthrough_log.md"], failures)
    require_text(CAPTURE_PS1, ["capture_g18_quest_playthrough.gd"], failures)
    require_text(
        G18_REPORT,
        [
            "G-18 Opening Quest Extension: From Whispers to the Island",
            "Whispers Before Dawn",
            "Human review required: no",
            "village-to-island quest chain",
            "COUNCIL_PASS_READY_FOR_PR",
            "Next phase: G-18A Multi-Path Rumor and Choice Foundation",
        ],
        failures,
    )
    require_text(
        G18_COUNCIL_REPORT,
        [
            "COUNCIL_PASS_READY_FOR_PR",
            "Quest Designer",
            "Narrative Designer",
            "Opening Quest Extension",
            "G-18",
        ],
        failures,
    )
    require_text(
        QUEST_LOG,
        [
            "G-18 Quest Playthrough Log",
            "Whispers Before Dawn",
            "reward_progression_update",
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
    if isinstance(quest_screenshot_manifest, dict):
        validate_quest_screenshot_manifest(quest_screenshot_manifest, failures)
    if isinstance(report_json, dict):
        validate_report_json(report_json, failures)
    return print_result("opening quest village to island", failures)


def validate_source(data: dict[str, Any], failures: list[str]) -> None:
    if data.get("schema_id") != "wayfarer.quest.whispers_before_dawn_village_to_island.v1":
        failures.append("G-18 source schema mismatch")
    if data.get("phase") != "G-18":
        failures.append("G-18 source phase mismatch")
    for path_key in ["runtime_contract", "main_contract", "screenshot_manifest"]:
        if not str(data.get(path_key, "")).strip():
            failures.append(f"G-18 source missing {path_key}")
    required_steps = set(str(item) for item in data.get("required_steps", []))
    for step in REQUIRED_STEPS:
        if step not in required_steps:
            failures.append(f"G-18 source missing required step: {step}")
    if len(data.get("village_paths", [])) < 3:
        failures.append("G-18 source must define at least three village paths")
    if len(data.get("island_path", [])) < 5:
        failures.append("G-18 source must define five island path beats")
    serialized = json.dumps(data, sort_keys=True)
    for token in [
        "counting_house_path",
        "tavern_rumor_path",
        "dockworker_harbor_path",
        "isla_brooke_farmhand",
        "tomas_reed_dock_runner",
        "Annelise Crow",
        "pre-Revolutionary",
    ]:
        if token not in serialized:
            failures.append(f"G-18 source missing token: {token}")
    acceptance = data.get("acceptance", {})
    for flag in [
        "quest_playable_end_to_end",
        "player_knows_next_objective",
        "quest_state_updates_correctly",
        "dialogue_supports_story",
        "island_exploration_has_purpose",
        "at_least_two_ways_to_gather_the_lead",
        "optional_clue_changes_or_enriches_journal",
        "reward_or_progression_beat",
        "meaningful_return_to_town",
    ]:
        if not isinstance(acceptance, dict) or acceptance.get(flag) is not True:
            failures.append(f"G-18 acceptance missing true flag: {flag}")
    for score_key in ["quest_gameplay_score", "narrative_hook_score", "ux_readability_score"]:
        if not isinstance(acceptance, dict) or float(acceptance.get(score_key, 0.0)) < 8.5:
            failures.append(f"G-18 acceptance {score_key} must be at least 8.5")


def validate_quest_data(data: dict[str, Any], failures: list[str]) -> None:
    if "G-18" not in [str(item) for item in data.get("phase_extensions", [])]:
        failures.append("first_light quest data must include G-18 phase extension")
    objectives = {
        str(item.get("id", ""))
        for item in data.get("objectives", [])
        if isinstance(item, dict)
    }
    for objective_id in REQUIRED_OBJECTIVES:
        if objective_id not in objectives:
            failures.append(f"first_light quest data missing objective: {objective_id}")
    extension = data.get("opening_island_extension", {})
    if not isinstance(extension, dict):
        failures.append("first_light quest data missing opening_island_extension")
        return
    if extension.get("phase") != "G-18":
        failures.append("opening_island_extension phase must be G-18")
    for beat in [
        "arrival_in_Newport",
        "counting_house_missing_manifest",
        "tavern_rumor",
        "coded_whisper",
        "island_lead",
        "travel_to_island_clue_site",
        "discover_physical_evidence",
        "return_or_report_choice",
        "reason_to_continue_hook",
    ]:
        if beat not in [str(item) for item in extension.get("quest_beats", [])]:
            failures.append(f"opening_island_extension missing beat: {beat}")
    acceptance = extension.get("acceptance", {})
    if not isinstance(acceptance, dict) or acceptance.get("village_to_island_quest_chain") is not True:
        failures.append("opening_island_extension must assert village_to_island_quest_chain")
    if not isinstance(acceptance, dict) or float(acceptance.get("quest_gameplay_score", 0.0)) < 8.5:
        failures.append("opening_island_extension quest_gameplay_score must be at least 8.5")


def validate_manifest(manifest: dict[str, Any], failures: list[str]) -> None:
    if manifest.get("schema_id") != "wayfarer.g18.runtime_screenshot_manifest.v1":
        failures.append("G-18 screenshot manifest schema mismatch")
    if manifest.get("phase") != "G-18":
        failures.append("G-18 screenshot manifest phase mismatch")
    if manifest.get("status") != "PASS":
        failures.append("G-18 screenshot manifest status must be PASS")
    if manifest.get("debug_overlays_disabled") is not True:
        failures.append("G-18 screenshot manifest must record debug_overlays_disabled=true")
    if manifest.get("hud_visible_for_journal_proof") is not True:
        failures.append("G-18 screenshot manifest must record HUD/journal proof")
    filenames = {
        str(item.get("filename", ""))
        for item in manifest.get("screenshots", [])
        if isinstance(item, dict)
    }
    for filename in REQUIRED_SCREENSHOTS:
        if filename not in filenames:
            failures.append(f"G-18 screenshot manifest missing {filename}")
    for item in manifest.get("screenshots", []):
        if not isinstance(item, dict):
            continue
        if item.get("status") != "PASS":
            failures.append(f"G-18 screenshot did not PASS: {item.get('filename', '<unknown>')}")
        raw_path = str(item.get("path", ""))
        if raw_path and not project_path(raw_path).exists():
            failures.append(f"G-18 screenshot path missing: {raw_path}")
        png = item.get("png_verification", {})
        if not isinstance(png, dict) or png.get("status") != "PASS":
            failures.append(f"G-18 screenshot PNG verification failed: {item.get('filename', '<unknown>')}")
    result = manifest.get("playthrough_result", {})
    if not isinstance(result, dict) or result.get("status") != "PASS":
        failures.append("G-18 screenshot manifest playthrough_result must PASS")
    else:
        for key in [
            "island_lead_active",
            "coded_whisper_confirmed",
            "optional_clue_or_branch",
            "island_physical_evidence_found",
            "return_or_report_choice",
            "reason_to_continue",
            "reward_or_progression",
            "contract_end_to_end_pass",
        ]:
            if result.get(key) is not True:
                failures.append(f"G-18 playthrough_result missing true flag: {key}")
        for score_key in ["quest_gameplay_score", "narrative_hook_score", "ux_readability_score"]:
            if float(result.get(score_key, 0.0)) < 8.5:
                failures.append(f"G-18 playthrough_result {score_key} must be at least 8.5")
    validate_final_contract(manifest.get("quest_contract_final", {}), failures, "screenshot manifest final quest contract")
    validate_g18_contract(manifest.get("opening_village_to_island_contract_final", {}), failures, "screenshot manifest G-18 contract")


def validate_trace(trace: dict[str, Any], failures: list[str]) -> None:
    if trace.get("schema_id") != "wayfarer.g18.quest_playthrough_state_trace.v1":
        failures.append("G-18 quest trace schema mismatch")
    if trace.get("status") != "PASS":
        failures.append("G-18 quest trace status must be PASS")
    steps = trace.get("steps", [])
    if not isinstance(steps, list) or len(steps) < 12:
        failures.append("G-18 quest trace must include at least 12 steps")
        steps = []
    seen_steps = {str(step.get("step_id", "")) for step in steps if isinstance(step, dict)}
    for step in REQUIRED_STEPS:
        if step == "reason_to_continue":
            continue
        if step not in seen_steps:
            failures.append(f"G-18 quest trace missing step: {step}")
    for step in steps:
        if not isinstance(step, dict):
            continue
        if not str(step.get("current_objective_id", "")).strip():
            failures.append(f"G-18 trace step missing current objective: {step.get('step_id', '<unknown>')}")
        screenshot = str(step.get("screenshot", ""))
        if screenshot and not project_path(screenshot).exists():
            failures.append(f"G-18 trace screenshot path missing: {screenshot}")
    validate_final_contract(trace.get("final_quest_contract", {}), failures, "quest trace final contract")
    validate_g18_contract(trace.get("opening_village_to_island_contract", {}), failures, "quest trace G-18 contract")
    result = trace.get("playthrough_result", {})
    if not isinstance(result, dict) or result.get("status") != "PASS":
        failures.append("G-18 quest trace playthrough_result must PASS")


def validate_quest_screenshot_manifest(data: dict[str, Any], failures: list[str]) -> None:
    if data.get("schema_id") != "wayfarer.g18.quest_playthrough_screenshot_manifest.v1":
        failures.append("G-18 quest screenshot manifest schema mismatch")
    if data.get("phase") != "G-18":
        failures.append("G-18 quest screenshot manifest phase mismatch")
    if data.get("status") != "PASS":
        failures.append("G-18 quest screenshot manifest status must be PASS")
    filenames = {
        str(item.get("filename", ""))
        for item in data.get("screenshots", [])
        if isinstance(item, dict)
    }
    for filename in REQUIRED_SCREENSHOTS:
        if filename not in filenames:
            failures.append(f"G-18 quest screenshot manifest missing {filename}")


def validate_final_contract(contract: Any, failures: list[str], label: str) -> None:
    if not isinstance(contract, dict):
        failures.append(f"G-18 missing {label}")
        return
    flags = contract.get("flags", {})
    completed = contract.get("completed_objectives", [])
    rewards = contract.get("reward_log", [])
    for flag in REQUIRED_ISLAND_FLAGS:
        if not isinstance(flags, dict) or flags.get(flag) is not True:
            failures.append(f"G-18 {label} missing flag: {flag}")
    for objective_id in ["follow_island_lead", "travel_to_island_clue_site", "discover_physical_evidence", "return_or_report_choice"]:
        if objective_id not in completed:
            failures.append(f"G-18 {label} missing completed objective: {objective_id}")
    if contract.get("current_objective_id") != "hook_to_continue":
        failures.append(f"G-18 {label} must end on hook_to_continue")
    if not isinstance(rewards, list) or len(rewards) < 4:
        failures.append(f"G-18 {label} must include village and island reward/contact progression")
    if int(contract.get("reward_resolve", 0)) < 13:
        failures.append(f"G-18 {label} reward_resolve must be at least 13")


def validate_g18_contract(contract: Any, failures: list[str], label: str) -> None:
    if not isinstance(contract, dict):
        failures.append(f"G-18 missing {label}")
        return
    if contract.get("phase") != "G-18":
        failures.append(f"G-18 {label} phase mismatch")
    for key in [
        "counting_house_missing_manifest",
        "tavern_rumor",
        "coded_whisper",
        "island_lead",
        "travel_to_island_clue_site",
        "discover_physical_evidence",
        "optional_clue_or_branch",
        "return_or_report_choice",
        "reward_progression_update",
        "reason_to_continue",
        "village_to_island_chain_playable_end_to_end",
        "dialogue_supports_story",
        "island_exploration_has_purpose",
    ]:
        if contract.get(key) is not True:
            failures.append(f"G-18 {label} missing true contract flag: {key}")
    trace = contract.get("playthrough_trace", [])
    seen_steps = {str(step.get("step_id", "")) for step in trace if isinstance(step, dict)}
    for step in REQUIRED_STEPS:
        if step == "reason_to_continue":
            continue
        if step not in seen_steps:
            failures.append(f"G-18 {label} missing playthrough step: {step}")
    for score_key in ["quest_gameplay_score", "narrative_hook_score", "ux_readability_score"]:
        if float(contract.get(score_key, 0.0)) < 8.5:
            failures.append(f"G-18 {label} {score_key} must be at least 8.5")


def validate_report_json(data: dict[str, Any], failures: list[str]) -> None:
    if data.get("status") != "PASS":
        failures.append("G-18 report JSON status must be PASS")
    if data.get("human_review_required") is not False:
        failures.append("G-18 report JSON must record human_review_required=false")
    if data.get("agent_council_verdict") != "COUNCIL_PASS_READY_FOR_PR":
        failures.append("G-18 report JSON council verdict mismatch")
    for path_key in ["screenshot_manifest", "quest_playthrough_log", "quest_state_trace", "quest_screenshot_manifest"]:
        raw_path = str(data.get(path_key, ""))
        if not raw_path:
            failures.append(f"G-18 report JSON missing {path_key}")
        elif not project_path(raw_path).exists():
            failures.append(f"G-18 report JSON path missing for {path_key}: {raw_path}")
    for score_key in ["quest_gameplay_score", "narrative_hook_score", "ux_readability_score", "technical_stability_score"]:
        if float(data.get(score_key, 0.0)) < 8.5:
            failures.append(f"G-18 report JSON {score_key} must be at least 8.5")
    if data.get("provenance_atelier_result") != "PASS":
        failures.append("G-18 report JSON provenance_atelier_result must be PASS")
    if data.get("north_star_result") != "PASS":
        failures.append("G-18 report JSON north_star_result must be PASS")


if __name__ == "__main__":
    sys.exit(main())
