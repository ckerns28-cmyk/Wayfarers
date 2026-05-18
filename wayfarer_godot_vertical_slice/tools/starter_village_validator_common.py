#!/usr/bin/env python3
"""Shared helpers for Starter Village validators."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[1]
REPO_ROOT = PROJECT_ROOT.parent

ROADMAP_MD = REPO_ROOT / "docs" / "roadmaps" / "STARTER_VILLAGE_PLAYABLE_OBSESSION_ROADMAP.md"
ROADMAP_JSON = REPO_ROOT / "docs" / "roadmaps" / "STARTER_VILLAGE_PLAYABLE_OBSESSION_ROADMAP.json"
LEDGER_MD = REPO_ROOT / "docs" / "reports" / "STARTER_VILLAGE_AUTONOMOUS_EXECUTION_LEDGER.md"
LEDGER_JSON = REPO_ROOT / "docs" / "reports" / "STARTER_VILLAGE_AUTONOMOUS_EXECUTION_LEDGER.json"
G7_REPORT = REPO_ROOT / "docs" / "reports" / "G7_NEWPORT_LIVING_ORIGIN_VILLAGE_MASTERPLAN_LOCK.md"
G7_COUNCIL_REPORT = REPO_ROOT / "docs" / "reports" / "G7_NEWPORT_LIVING_ORIGIN_VILLAGE_MASTERPLAN_AGENT_COUNCIL_REPORT.md"
G7A_REPORT = REPO_ROOT / "docs" / "reports" / "G7A_STREET_LOT_GROUND_COHESION_RECONSTRUCTION.md"
G7A_COUNCIL_REPORT = REPO_ROOT / "docs" / "reports" / "G7A_STREET_LOT_GROUND_COHESION_AGENT_COUNCIL_REPORT.md"
G7A_SCREENSHOT_MANIFEST = PROJECT_ROOT / "artifacts" / "review" / "g7a_runtime_screenshots" / "g7a_runtime_screenshot_manifest.json"
G7B_REPORT = REPO_ROOT / "docs" / "reports" / "G7B_HARBOR_WHARF_COMMERCIAL_SPINE_COHESION.md"
G7B_COUNCIL_REPORT = REPO_ROOT / "docs" / "reports" / "G7B_HARBOR_WHARF_COMMERCIAL_SPINE_AGENT_COUNCIL_REPORT.md"
G7B_SCREENSHOT_MANIFEST = PROJECT_ROOT / "artifacts" / "review" / "g7b_runtime_screenshots" / "g7b_runtime_screenshot_manifest.json"
G7C_REPORT = REPO_ROOT / "docs" / "reports" / "G7C_LANDMARK_DISTRICT_IDENTITY_PASS.md"
G7C_COUNCIL_REPORT = REPO_ROOT / "docs" / "reports" / "G7C_LANDMARK_DISTRICT_IDENTITY_AGENT_COUNCIL_REPORT.md"
G7C_SCREENSHOT_MANIFEST = PROJECT_ROOT / "artifacts" / "review" / "g7c_runtime_screenshots" / "g7c_runtime_screenshot_manifest.json"
G8_REPORT = REPO_ROOT / "docs" / "reports" / "G8_ATELIER_CHARACTER_AND_NPC_MOVEMENT_FOUNDATION.md"
G8_COUNCIL_REPORT = REPO_ROOT / "docs" / "reports" / "G8_ATELIER_CHARACTER_AND_NPC_MOVEMENT_AGENT_COUNCIL_REPORT.md"
G8_SCREENSHOT_MANIFEST = PROJECT_ROOT / "artifacts" / "review" / "g8_runtime_screenshots" / "g8_runtime_screenshot_manifest.json"
G8A_REPORT = REPO_ROOT / "docs" / "reports" / "G8A_LIVING_NPC_POPULATION_PASS.md"
G8A_COUNCIL_REPORT = REPO_ROOT / "docs" / "reports" / "G8A_LIVING_NPC_POPULATION_AGENT_COUNCIL_REPORT.md"
G8A_SCREENSHOT_MANIFEST = PROJECT_ROOT / "artifacts" / "review" / "g8a_runtime_screenshots" / "g8a_runtime_screenshot_manifest.json"
G9_REPORT = REPO_ROOT / "docs" / "reports" / "G9_INTERACTION_UX_DIEGETIC_PROMPT_PASS.md"
G9_COUNCIL_REPORT = REPO_ROOT / "docs" / "reports" / "G9_INTERACTION_UX_AGENT_COUNCIL_REPORT.md"
G9_SCREENSHOT_MANIFEST = PROJECT_ROOT / "artifacts" / "review" / "g9_runtime_screenshots" / "g9_runtime_screenshot_manifest.json"
G9A_REPORT = REPO_ROOT / "docs" / "reports" / "G9A_JOURNAL_OBJECTIVE_QUEST_STATE_FOUNDATION.md"
G9A_COUNCIL_REPORT = REPO_ROOT / "docs" / "reports" / "G9A_JOURNAL_OBJECTIVE_AGENT_COUNCIL_REPORT.md"
G9A_SCREENSHOT_MANIFEST = PROJECT_ROOT / "artifacts" / "review" / "g9a_runtime_screenshots" / "g9a_runtime_screenshot_manifest.json"
G10_REPORT = REPO_ROOT / "docs" / "reports" / "G10_OPENING_QUEST_ARC_FIRST_LIGHT_WHISPERS_BEFORE_DAWN.md"
G10_COUNCIL_REPORT = REPO_ROOT / "docs" / "reports" / "G10_OPENING_QUEST_ARC_AGENT_COUNCIL_REPORT.md"
G10_SCREENSHOT_MANIFEST = PROJECT_ROOT / "artifacts" / "review" / "g10_runtime_screenshots" / "g10_runtime_screenshot_manifest.json"
G10A_REPORT = REPO_ROOT / "docs" / "reports" / "G10A_TAVERN_WHISPER_SYSTEM.md"
G10A_COUNCIL_REPORT = REPO_ROOT / "docs" / "reports" / "G10A_TAVERN_WHISPER_AGENT_COUNCIL_REPORT.md"
G10A_SCREENSHOT_MANIFEST = PROJECT_ROOT / "artifacts" / "review" / "g10a_runtime_screenshots" / "g10a_runtime_screenshot_manifest.json"
G10B_REPORT = REPO_ROOT / "docs" / "reports" / "G10B_MULTI_PATH_STARTER_CHOICE_FOUNDATION.md"
G10B_COUNCIL_REPORT = REPO_ROOT / "docs" / "reports" / "G10B_MULTI_PATH_STARTER_CHOICE_AGENT_COUNCIL_REPORT.md"
G10B_SCREENSHOT_MANIFEST = PROJECT_ROOT / "artifacts" / "review" / "g10b_runtime_screenshots" / "g10b_runtime_screenshot_manifest.json"
G11_REPORT = REPO_ROOT / "docs" / "reports" / "G11_LIVING_TOWN_RHYTHM_PASS.md"
G11_COUNCIL_REPORT = REPO_ROOT / "docs" / "reports" / "G11_LIVING_TOWN_RHYTHM_AGENT_COUNCIL_REPORT.md"
G11_SCREENSHOT_MANIFEST = PROJECT_ROOT / "artifacts" / "review" / "g11_runtime_screenshots" / "g11_runtime_screenshot_manifest.json"
G11A_REPORT = REPO_ROOT / "docs" / "reports" / "G11A_AUDIO_ATMOSPHERE_PLACEHOLDER_FREE_FOUNDATION.md"
G11A_COUNCIL_REPORT = REPO_ROOT / "docs" / "reports" / "G11A_AUDIO_ATMOSPHERE_AGENT_COUNCIL_REPORT.md"
G11A_AUDIO_HOOKS_JSON = PROJECT_ROOT / "data" / "audio" / "starter_village_atmosphere_hooks.json"
G11A_AUDIO_HOOKS_GD = PROJECT_ROOT / "scripts" / "audio" / "StarterVillageAudioHooks.gd"
G12_REPORT = REPO_ROOT / "docs" / "reports" / "G12_FIRST_SESSION_FUN_PACING_READABILITY_PASS.md"
G12_COUNCIL_REPORT = REPO_ROOT / "docs" / "reports" / "G12_FIRST_SESSION_AGENT_COUNCIL_REPORT.md"
G12_SCREENSHOT_MANIFEST = PROJECT_ROOT / "artifacts" / "review" / "g12_runtime_screenshots" / "g12_runtime_screenshot_manifest.json"
SV0_REPORT = REPO_ROOT / "docs" / "reports" / "SV0_FREE_TOOLING_INTAKE_PRODUCTION_STACK_LOCK.md"
SV0_REPORT_JSON = REPO_ROOT / "docs" / "reports" / "SV0_FREE_TOOLING_INTAKE_PRODUCTION_STACK_LOCK.json"
SV0_TOOLING_ROADMAP = REPO_ROOT / "docs" / "roadmaps" / "STARTER_VILLAGE_TOOLING_STACK.md"
SV0_VALIDATOR = PROJECT_ROOT / "tools" / "validate_sv0_tooling_stack.py"
SV0_WORLD_LAYOUT = PROJECT_ROOT / "data" / "world_layout" / "starter_village_world_layout_v1.json"
SV0_VISUAL_QA = PROJECT_ROOT / "data" / "visual_qa" / "starter_village_visual_regression_manifest_v1.json"
SV0_MOVEMENT_PROOF = PROJECT_ROOT / "data" / "movement_proof" / "starter_village_movement_proof_manifest_v1.json"
SV0_GROUND_STACK = PROJECT_ROOT / "data" / "ground_materials" / "starter_village_ground_material_stack_v1.json"
G7A_SV0_LAYOUT_REPAIR_REPORT = REPO_ROOT / "docs" / "reports" / "G7A_SV0_TOOL_BACKED_LAYOUT_REPAIR.md"
G7A_SV0_LAYOUT_USAGE_VALIDATOR = PROJECT_ROOT / "tools" / "validate_starter_village_layout_source_usage.py"
QUEST_STATE_GD = PROJECT_ROOT / "scripts" / "QuestState.gd"
FIRST_LIGHT_QUEST_GD = PROJECT_ROOT / "scripts" / "quests" / "FirstLightQuest.gd"
FIRST_LIGHT_QUEST_JSON = PROJECT_ROOT / "data" / "quests" / "first_light_whispers_before_dawn.json"
FIRST_LIGHT_CHOICE_ROUTER_GD = PROJECT_ROOT / "scripts" / "quests" / "FirstLightChoiceRouter.gd"
FIRST_LIGHT_MULTI_PATH_JSON = PROJECT_ROOT / "data" / "quests" / "first_light_multi_path_choices.json"
TAVERN_WHISPER_GD = PROJECT_ROOT / "scripts" / "dialogue" / "TavernWhisperSystem.gd"
TAVERN_WHISPER_JSON = PROJECT_ROOT / "data" / "dialogue" / "tavern_whispers.json"
VISUAL_ORDER_VALIDATOR = PROJECT_ROOT / "tools" / "validate_newport_visual_ordering.py"
BLUEPRINT = PROJECT_ROOT / "scripts" / "NewportTownBlueprint.gd"
BUILDING_CATALOG_GD = PROJECT_ROOT / "scripts" / "BuildingCatalog.gd"
MAIN_GD = PROJECT_ROOT / "scenes" / "Main.gd"
MAP_LAYER = PROJECT_ROOT / "scenes" / "map" / "MapLayer.gd"
HUD_SCENE = PROJECT_ROOT / "scenes" / "ui" / "HUD.tscn"
HUD_GD = PROJECT_ROOT / "scenes" / "ui" / "HUD.gd"
BUILDING_GD = PROJECT_ROOT / "scenes" / "buildings" / "Building.gd"
CHARACTER_MANIFEST = PROJECT_ROOT / "art_pipeline" / "player_identity" / "manifests" / "newport_atelier_characters_g422r_manifest.json"
PLAYER_GD = PROJECT_ROOT / "scenes" / "player" / "Player.gd"
PLAYER_TSCN = PROJECT_ROOT / "scenes" / "player" / "Player.tscn"
EDRIN_GD = PROJECT_ROOT / "scenes" / "npc" / "EdrinVale.gd"
EDRIN_TSCN = PROJECT_ROOT / "scenes" / "npc" / "EdrinVale.tscn"
ATELIER_NPC_GD = PROJECT_ROOT / "scenes" / "npc" / "AtelierTownNpc.gd"
ATELIER_NPC_TSCN = PROJECT_ROOT / "scenes" / "npc" / "AtelierTownNpc.tscn"

REQUIRED_PHASES = [
    "SV-0",
    "G-7",
    "G-7A",
    "G-7B",
    "G-7C",
    "G-8",
    "G-8A",
    "G-9",
    "G-9A",
    "G-10",
    "G-10A",
    "G-10B",
    "G-11",
    "G-11A",
    "G-12",
    "G-13",
    "G-14",
]

ALLOWED_LEDGER_STATUSES = {
    "PASS",
    "IN_PROGRESS",
    "PENDING",
    "FAIL_NEEDS_CODE_FIX",
    "BLOCKED_REQUIRES_HUMAN_ESCALATION",
}

DEPRECATED_STATUSES = {
    "NEEDS_HUMAN_REVIEW",
    "READY_FOR_HUMAN_VISUAL_REVIEW",
    "AWAITING_CHRIS_REVIEW",
    "VISUAL_REVIEW_REQUIRED",
    "TECHNICAL_PASS_ONLY",
}


def rel(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def repo_path(raw_path: str) -> Path:
    normalized = raw_path.replace("\\", "/")
    if normalized.startswith("res://"):
        return PROJECT_ROOT / normalized.removeprefix("res://")
    return REPO_ROOT / normalized


def load_json(path: Path, failures: list[str]) -> dict[str, Any] | None:
    if not path.exists():
        failures.append(f"missing required json: {rel(path)}")
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        failures.append(f"invalid json {rel(path)}: {exc}")
        return None
    if not isinstance(data, dict):
        failures.append(f"{rel(path)} root must be an object")
        return None
    return data


def require_path(path: Path, failures: list[str], label: str = "required path") -> None:
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


def phase_map(data: dict[str, Any], failures: list[str]) -> dict[str, dict[str, Any]]:
    rows = data.get("phases")
    if not isinstance(rows, list):
        failures.append("phases must be a list")
        return {}
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict):
            failures.append("phase row must be an object")
            continue
        phase_id = str(row.get("phase_id", "")).strip()
        if not phase_id:
            failures.append("phase row missing phase_id")
            continue
        result[phase_id] = row
    for phase_id in REQUIRED_PHASES:
        if phase_id not in result:
            failures.append(f"missing phase row: {phase_id}")
    return result


def list_value(row: dict[str, Any], key: str, failures: list[str], phase_id: str) -> list[Any]:
    value = row.get(key)
    if not isinstance(value, list) or not value:
        failures.append(f"{phase_id} missing non-empty {key}")
        return []
    return value


def print_result(name: str, failures: list[str], details: list[str] | None = None) -> int:
    if failures:
        print(f"FAIL: {name}")
        for failure in failures:
            print(" - " + failure)
        return 1
    print(f"PASS: {name}")
    for detail in details or []:
        print(detail)
    return 0
