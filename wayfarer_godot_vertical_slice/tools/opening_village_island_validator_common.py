#!/usr/bin/env python3
"""Shared helpers for Opening Village + Island validators."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[1]
REPO_ROOT = PROJECT_ROOT.parent

ROADMAP_MD = REPO_ROOT / "docs" / "roadmaps" / "OPENING_VILLAGE_ISLAND_PRODUCTION_ROADMAP.md"
ROADMAP_JSON = REPO_ROOT / "docs" / "roadmaps" / "OPENING_VILLAGE_ISLAND_PRODUCTION_ROADMAP.json"
LEDGER_MD = REPO_ROOT / "docs" / "reports" / "OPENING_VILLAGE_ISLAND_AUTONOMOUS_EXECUTION_LEDGER.md"
LEDGER_JSON = REPO_ROOT / "docs" / "reports" / "OPENING_VILLAGE_ISLAND_AUTONOMOUS_EXECUTION_LEDGER.json"
STARTER_ROADMAP_MD = REPO_ROOT / "docs" / "roadmaps" / "STARTER_VILLAGE_PLAYABLE_OBSESSION_ROADMAP.md"
STARTER_ROADMAP_JSON = REPO_ROOT / "docs" / "roadmaps" / "STARTER_VILLAGE_PLAYABLE_OBSESSION_ROADMAP.json"
STARTER_LEDGER_MD = REPO_ROOT / "docs" / "reports" / "STARTER_VILLAGE_AUTONOMOUS_EXECUTION_LEDGER.md"
STARTER_LEDGER_JSON = REPO_ROOT / "docs" / "reports" / "STARTER_VILLAGE_AUTONOMOUS_EXECUTION_LEDGER.json"
AGENTS_MD = REPO_ROOT / "AGENTS.md"
GODOT_ROADMAP_MD = REPO_ROOT / "docs" / "WAYFARER_GODOT_ROADMAP.md"
PROTOCOL_MD = REPO_ROOT / "docs" / "PRE_G5_AUTONOMOUS_PRODUCTION_PROTOCOL.md"
PR_CHECKLIST_MD = REPO_ROOT / "docs" / "checklists" / "WAYFARER_PR_REVIEW_CHECKLIST.md"
REGRESSION_CHECKLIST_MD = REPO_ROOT / "docs" / "REGRESSION_TEST_CHECKLIST.md"
COUNCIL_TOOL = REPO_ROOT / "tools" / "wayfarer_agent_council.py"
COUNCIL_TEMPLATE = REPO_ROOT / "docs" / "templates" / "WAYFARER_COUNCIL_REPORT_TEMPLATE.md"

OVI1_SCREENSHOT_DIR = PROJECT_ROOT / "artifacts" / "review" / "g22_ovi1_review_screenshots"
OVI1_SCREENSHOT_MANIFEST = OVI1_SCREENSHOT_DIR / "g22_ovi1_screenshot_manifest.json"
OVI1_MOTION_PROOF_DIR = PROJECT_ROOT / "artifacts" / "review" / "g22_ovi1_motion_proof"
OVI1_QUEST_PLAYTHROUGH_DIR = PROJECT_ROOT / "artifacts" / "review" / "g22_ovi1_quest_playthrough"

OVI1_REVIEW_PACKAGE_MD = REPO_ROOT / "docs" / "reports" / "G22_OVI1_OPENING_VILLAGE_ISLAND_REVIEW_PACKAGE.md"
OVI1_REVIEW_PACKAGE_JSON = REPO_ROOT / "docs" / "reports" / "G22_OVI1_OPENING_VILLAGE_ISLAND_REVIEW_PACKAGE.json"
OVI1_COUNCIL_REPORT = REPO_ROOT / "docs" / "reports" / "G22_OVI1_AGENT_COUNCIL_REPORT.md"
OVI1_REVIEW_INDEX_MD = REPO_ROOT / "docs" / "reports" / "OVI1_REVIEW_INDEX.md"
OVI1_REVIEW_INDEX_JSON = REPO_ROOT / "docs" / "reports" / "OVI1_REVIEW_INDEX.json"

REQUIRED_PHASES = [
    "G-14",
    "G-15",
    "G-15A",
    "G-15B",
    "G-16",
    "G-16A",
    "G-17",
    "G-18",
    "G-18A",
    "G-19R",
    "G-19S",
    "G-19",
    "G-20",
    "G-21",
    "G-22",
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

REQUIRED_COUNCIL_ROLES = [
    "Scrum Master",
    "World-class Game Designer",
    "Game Programmer",
    "Art Director",
    "World/Layout Designer",
    "Narrative Designer",
    "Quest Designer",
    "Animation/NPC Behavior Director",
    "UX Designer",
    "QA Analyst",
    "Build/Release Engineer",
]

REQUIRED_OVI1_SCREENSHOTS = [
    "01_village_wide_cohesion.png",
    "02_player_arrival_harbor.png",
    "03_counting_house_route.png",
    "04_tavern_rumor_hub.png",
    "05_commercial_avenue.png",
    "06_harbor_wharf_work_area.png",
    "07_village_exit_to_island.png",
    "08_island_entry_transition.png",
    "09_island_main_trail.png",
    "10_island_landmark_signal_or_overlook.png",
    "11_island_cove_or_hidden_landing.png",
    "12_island_optional_discovery.png",
    "13_npc_village_movement.png",
    "14_npc_island_movement.png",
    "15_quest_journal_village_step.png",
    "16_quest_journal_island_step.png",
    "17_return_to_town_or_next_hook.png",
    "18_interaction_ux_proof.png",
    "19_ysort_layering_proof.png",
    "20_debug_overlays_disabled.png",
    "21_browser_review_identity_proof.png",
    "22_contact_sheet_player_npc_world_assets.png",
]

PHASE_VALIDATORS = {
    "G-14": "validate_opening_village_island_roadmap.py",
    "G-15": "validate_island_world_topology.py",
    "G-15A": "validate_village_to_island_transition.py",
    "G-15B": "validate_island_world_cohesion.py",
    "G-16": "validate_island_poi_landmarks.py",
    "G-16A": "validate_island_atelier_asset_family.py",
    "G-17": "validate_island_npc_encounter_foundation.py",
    "G-18": "validate_opening_quest_village_to_island.py",
    "G-18A": "validate_multipath_rumor_choice_foundation.py",
    "G-19R": "validate_g19r_newport_blockout_source_of_truth.py",
    "G-19S": "validate_newport_layout_source_alignment.py",
    "G-19": "validate_first_session_gameplay_loop.py",
    "G-20": "validate_first_session_gameplay_loop.py",
    "G-21": "validate_ovi1_gate.py",
    "G-22": "validate_ovi1_gate.py",
}

PHASE_REQUIRED_TOKENS = {
    "G-14": [
        "Internal Starter Village Proof Gate",
        "Human review required: no",
        "Next phase: G-15 Opening Island Masterplan + World Topology",
        "Tavern whisper hook",
    ],
    "G-15": ["Opening Island Masterplan + World Topology", "danger/safety gradient", "quest destination"],
    "G-15A": ["Village-to-Island Transition Pass", "Clear town exit", "First sense of mystery"],
    "G-15B": ["Island Terrain, Ground, and Route Cohesion", "No patchwork terrain", "route loops"],
    "G-16": ["Island Landmark and Point-of-Interest Pass", "Optional secret location", "Return landmark"],
    "G-16A": ["Island Atelier Asset Family Pass", "No placeholders", "Atelier compliance PASS"],
    "G-17": ["Island NPC / Encounter / Ambient Life Foundation", "grounded movement", "NPC/ambient score"],
    "G-18": ["Whispers Before Dawn", "village-to-island quest chain", "return or report choice"],
    "G-18A": ["Multi-Path Rumor and Choice Foundation", "Counting house path", "Dockworker/harbor path"],
    "G-19R": ["Newport Scale + Street Blockout Source of Truth", "measured_town_blockout_exists", "future_phases_block_ad_hoc_layout_edits"],
    "G-19S": ["Newport Blockout-To-Godot Runtime Reconstruction", "runtime_layout_matches_G19R_source_of_truth", "no_new_layout_invented_in_Godot"],
    "G-19": ["Player Guidance, Map, Journal, and Interaction Polish", "No debug-looking prompts"],
    "G-20": ["First-Session Gameplay Loop and Reward Pass", "first 20-30 minutes", "reason to continue"],
    "G-21": ["Opening Island Performance, Browser Build, and Regression Hardening", "Browser/review artifact"],
    "G-22": ["OVI-1 Opening Village + Island Production Playable Gate", "North Star alignment PASS"],
}

PASS_ROW_REQUIRED_FIELDS = [
    "branch",
    "commits",
    "implementing_prs",
    "merge_status",
    "files_changed",
    "validation_commands",
    "validation_results",
    "agent_council_report_path",
    "agent_council_verdict",
    "design_score",
    "world_layout_score",
    "art_direction_score",
    "ux_readability_score",
    "technical_stability_score",
    "provenance_atelier_result",
    "north_star_result",
    "next_required_action",
]


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


def list_text(row: dict[str, Any], key: str) -> str:
    value = row.get(key)
    if isinstance(value, list):
        return " ".join(str(item) for item in value)
    return str(value or "")


def validate_common_roadmap_contract(failures: list[str]) -> dict[str, Any] | None:
    roadmap = load_json(ROADMAP_JSON, failures)
    require_text(
        ROADMAP_MD,
        [
            "OVI-1 Opening Village + Island Production Playable Gate",
            "G-14 Internal Starter Village Proof Gate",
            "Human review required: no",
            "G-15 Opening Island Masterplan + World Topology",
            "G-22 OVI-1 Opening Village + Island Production Playable Gate",
            "COUNCIL_PASS_READY_FOR_PR",
            "COUNCIL_FAIL_NEEDS_CODE_FIX",
            "BLOCKED_REQUIRES_HUMAN_ESCALATION",
        ],
        failures,
    )
    for path, label in [
        (LEDGER_MD, "OVI ledger markdown"),
        (LEDGER_JSON, "OVI ledger json"),
        (STARTER_ROADMAP_MD, "Starter Village roadmap markdown"),
        (STARTER_LEDGER_MD, "Starter Village ledger markdown"),
        (AGENTS_MD, "AGENTS.md"),
        (GODOT_ROADMAP_MD, "Godot roadmap"),
        (PROTOCOL_MD, "autonomous protocol"),
        (PR_CHECKLIST_MD, "PR checklist"),
        (REGRESSION_CHECKLIST_MD, "regression checklist"),
        (COUNCIL_TOOL, "Agent Council tool"),
        (COUNCIL_TEMPLATE, "Agent Council template"),
    ]:
        require_path(path, failures, label)

    if not isinstance(roadmap, dict):
        return None
    if roadmap.get("schema_id") != "wayfarer.ovi1.opening_village_island_production_roadmap.v1":
        failures.append("OVI roadmap schema_id mismatch")
    if roadmap.get("milestone_id") != "OVI-1":
        failures.append("OVI roadmap milestone_id must be OVI-1")
    if roadmap.get("next_human_review_milestone") != "OVI-1 Opening Village + Island Production Playable Gate":
        failures.append("OVI roadmap next_human_review_milestone mismatch")
    if roadmap.get("autonomous_merge_authorized_until") != "OVI-1":
        failures.append("OVI roadmap must authorize ordinary autonomous merges until OVI-1")
    roles = set(str(item) for item in roadmap.get("required_council_roles", []))
    for role in REQUIRED_COUNCIL_ROLES:
        if role not in roles:
            failures.append(f"OVI roadmap missing council role: {role}")
    phase_rows = phase_map(roadmap, failures)
    for phase_id, token_list in PHASE_REQUIRED_TOKENS.items():
        row = phase_rows.get(phase_id, {})
        serialized = " ".join([str(row.get("title", "")), str(row.get("purpose", "")), list_text(row, "objectives"), list_text(row, "acceptance")])
        for token in token_list:
            if token not in serialized:
                failures.append(f"{phase_id} roadmap contract missing token: {token}")
        validator = PHASE_VALIDATORS.get(phase_id)
        validators = list_text(row, "primary_validators")
        if validator and validator not in validators:
            failures.append(f"{phase_id} roadmap missing primary validator: {validator}")
    serialized = json.dumps(roadmap, sort_keys=True)
    for deprecated in DEPRECATED_STATUSES:
        if deprecated in serialized:
            failures.append(f"OVI roadmap contains deprecated status: {deprecated}")
    return roadmap


def validate_common_ledger_contract(failures: list[str]) -> dict[str, Any] | None:
    ledger = load_json(LEDGER_JSON, failures)
    require_text(
        LEDGER_MD,
        [
            "OVI-1 Opening Village + Island Production Playable Gate",
            "G-14 is now an internal checkpoint",
            "Human review required: no",
            "G-15 Opening Island Masterplan + World Topology",
            "COUNCIL_PASS_READY_FOR_PR",
        ],
        failures,
    )
    if not isinstance(ledger, dict):
        return None
    if ledger.get("schema_id") != "wayfarer.ovi1.autonomous_execution_ledger.v1":
        failures.append("OVI ledger schema_id mismatch")
    if ledger.get("milestone_id") != "OVI-1":
        failures.append("OVI ledger milestone_id must be OVI-1")
    if ledger.get("human_review_required_before_ovi1") is not False:
        failures.append("OVI ledger must record human_review_required_before_ovi1=false")
    if ledger.get("next_true_human_review_milestone") != "OVI-1 Opening Village + Island Production Playable Gate":
        failures.append("OVI ledger next true milestone mismatch")
    phase_rows = phase_map(ledger, failures)
    for phase_id in REQUIRED_PHASES:
        row = phase_rows.get(phase_id, {})
        status = str(row.get("current_status", "")).strip()
        if status not in ALLOWED_LEDGER_STATUSES:
            failures.append(f"{phase_id} invalid current_status: {status}")
        for key in ["phase_name", "branch", "implementing_prs", "commits", "current_status", "reason_for_status", "next_required_action"]:
            if key not in row or not str(row.get(key, "")).strip():
                failures.append(f"{phase_id} ledger missing {key}")
        if str(row.get("agent_council_verdict", "")) in DEPRECATED_STATUSES:
            failures.append(f"{phase_id} uses deprecated council verdict")
        if status == "PASS":
            validate_pass_row(phase_id, row, failures)
    serialized = json.dumps(ledger, sort_keys=True)
    for deprecated in DEPRECATED_STATUSES:
        if deprecated in serialized:
            failures.append(f"OVI ledger contains deprecated status: {deprecated}")
    return ledger


def validate_pass_row(phase_id: str, row: dict[str, Any], failures: list[str]) -> None:
    for key in PASS_ROW_REQUIRED_FIELDS:
        value = row.get(key)
        if value in (None, "", [], {}):
            failures.append(f"{phase_id} PASS row missing {key}")
    if row.get("agent_council_verdict") != "COUNCIL_PASS_READY_FOR_PR":
        failures.append(f"{phase_id} PASS row must have council verdict COUNCIL_PASS_READY_FOR_PR")
    if phase_id in {"G-14", "G-15", "G-15A", "G-15B", "G-16", "G-16A", "G-17", "G-18", "G-18A", "G-19", "G-20", "G-21", "G-22"}:
        if not row.get("screenshot_paths"):
            failures.append(f"{phase_id} PASS row missing screenshot_paths")
    if phase_id in {"G-14", "G-17", "G-22"} and not row.get("motion_proof_paths"):
        failures.append(f"{phase_id} PASS row missing motion_proof_paths")
    if phase_id in {"G-14", "G-18", "G-18A", "G-20", "G-22"} and not row.get("quest_proof_paths"):
        failures.append(f"{phase_id} PASS row missing quest_proof_paths")


def validate_phase_contract(phase_id: str, failures: list[str]) -> None:
    roadmap = validate_common_roadmap_contract(failures)
    ledger = validate_common_ledger_contract(failures)
    if isinstance(roadmap, dict):
        row = phase_map(roadmap, failures).get(phase_id, {})
        if not row:
            failures.append(f"{phase_id} missing from OVI roadmap")
        validator = PHASE_VALIDATORS.get(phase_id)
        if validator and validator not in list_text(row, "primary_validators"):
            failures.append(f"{phase_id} missing validator {validator}")
        for token in PHASE_REQUIRED_TOKENS.get(phase_id, []):
            serialized = " ".join([str(row.get("title", "")), str(row.get("purpose", "")), list_text(row, "objectives"), list_text(row, "acceptance")])
            if token not in serialized:
                failures.append(f"{phase_id} missing roadmap token: {token}")
    if isinstance(ledger, dict):
        row = phase_map(ledger, failures).get(phase_id, {})
        if not row:
            failures.append(f"{phase_id} missing from OVI ledger")
        elif str(row.get("current_status", "")) == "PASS":
            validate_pass_row(phase_id, row, failures)


def validate_final_ovi1_artifacts(failures: list[str]) -> None:
    for path, label in [
        (OVI1_REVIEW_PACKAGE_MD, "OVI-1 review package markdown"),
        (OVI1_REVIEW_PACKAGE_JSON, "OVI-1 review package json"),
        (OVI1_COUNCIL_REPORT, "OVI-1 Agent Council report"),
        (OVI1_REVIEW_INDEX_MD, "OVI-1 review index markdown"),
        (OVI1_REVIEW_INDEX_JSON, "OVI-1 review index json"),
        (OVI1_SCREENSHOT_DIR, "OVI-1 screenshot directory"),
        (OVI1_SCREENSHOT_MANIFEST, "OVI-1 screenshot manifest"),
        (OVI1_MOTION_PROOF_DIR, "OVI-1 motion proof directory"),
        (OVI1_QUEST_PLAYTHROUGH_DIR, "OVI-1 quest playthrough directory"),
    ]:
        require_path(path, failures, label)
    manifest = load_json(OVI1_SCREENSHOT_MANIFEST, failures) if OVI1_SCREENSHOT_MANIFEST.exists() else None
    if isinstance(manifest, dict):
        filenames = {
            str(item.get("filename", ""))
            for item in manifest.get("screenshots", [])
            if isinstance(item, dict)
        }
        for filename in REQUIRED_OVI1_SCREENSHOTS:
            if filename not in filenames:
                failures.append(f"OVI-1 screenshot manifest missing {filename}")


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
