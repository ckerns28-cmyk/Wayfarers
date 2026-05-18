#!/usr/bin/env python3
"""Validate the G-5 migration architecture package.

G-5 is planning-only. This validator fails empty or hand-wavy architecture
claims by requiring a machine-readable system inventory, migration sequence,
source evidence, and explicit production-route safety policy.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[1]
REPO_ROOT = PROJECT_ROOT.parent

REPORT_MD = REPO_ROOT / "docs" / "reports" / "G5_MIGRATION_ARCHITECTURE.md"
REPORT_JSON = REPO_ROOT / "docs" / "reports" / "G5_MIGRATION_ARCHITECTURE.json"
COUNCIL_REPORT = REPO_ROOT / "docs" / "reports" / "G5_MIGRATION_ARCHITECTURE_AGENT_COUNCIL_REPORT.md"
ROADMAP = REPO_ROOT / "docs" / "WAYFARER_GODOT_ROADMAP.md"
TECH_DEBT = REPO_ROOT / "docs" / "TECH_DEBT_REGISTER.md"
REGRESSION = REPO_ROOT / "docs" / "REGRESSION_TEST_CHECKLIST.md"
PR_CHECKLIST = REPO_ROOT / "docs" / "checklists" / "WAYFARER_PR_REVIEW_CHECKLIST.md"

REQUIRED_SYSTEM_IDS = {
    "movement_camera_zone",
    "interaction_dialogue_quest",
    "inventory_equipment_economy",
    "combat_enemy_loot_progression",
    "save_load_persistence",
    "world_objects_dungeons_persistence",
    "ui_hud_chronicle_feedback",
    "deployment_qa_multiplayer_boundary",
}

REQUIRED_SEQUENCE_IDS = {
    "G-5.1",
    "G-5.2",
    "G-5.3",
    "G-5.4",
    "G-5.5",
    "G-5.6",
    "G-5.7",
    "G-5.8",
    "G-5.9",
}

REQUIRED_MARKDOWN_SECTIONS = [
    "## Status",
    "## Why G-5 Exists",
    "## Source Evidence",
    "## Non-Negotiable Rules",
    "## Target Godot Boundaries",
    "## Migration System Inventory",
    "## Migration Sequence",
    "## Save Compatibility Policy",
    "## Multiplayer Boundary Policy",
    "## QA Gates For Future Migration PRs",
    "## Recommendation",
]

REQUIRED_COUNCIL_SECTIONS = [
    "## Roadmap Execution Result",
    "## Migration Architecture Audit",
    "## Scrum Master Review",
    "## Game Designer Review",
    "## Game Programmer Review",
    "## QA Review",
    "## Release Manager Decision",
]


def rel(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def fail_missing(path: Path, failures: list[str]) -> bool:
    if path.exists():
        return False
    failures.append(f"missing required path: {rel(path)}")
    return True


def load_json(path: Path, failures: list[str]) -> dict[str, Any] | None:
    if fail_missing(path, failures):
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


def require_text(path: Path, tokens: list[str], failures: list[str]) -> str:
    if fail_missing(path, failures):
        return ""
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        if token not in text:
            failures.append(f"{rel(path)} missing token: {token}")
    return text


def repo_path(raw_path: str) -> Path:
    normalized = raw_path.replace("\\", "/")
    if normalized.startswith("res://"):
        return PROJECT_ROOT / normalized.removeprefix("res://")
    return REPO_ROOT / normalized


def require_existing_path(raw_path: str, label: str, failures: list[str]) -> None:
    path = repo_path(raw_path)
    if not path.exists():
        failures.append(f"missing {label}: {raw_path}")


def require_non_empty_string(row: dict[str, Any], key: str, system_id: str, failures: list[str]) -> None:
    if not str(row.get(key, "")).strip():
        failures.append(f"{system_id} missing {key}")


def require_non_empty_list(row: dict[str, Any], key: str, system_id: str, failures: list[str]) -> list[str]:
    value = row.get(key)
    if not isinstance(value, list) or not value:
        failures.append(f"{system_id} missing non-empty {key}")
        return []
    values = [str(item) for item in value if str(item).strip()]
    if not values:
        failures.append(f"{system_id} has empty {key}")
    return values


def validate_system(row: dict[str, Any], failures: list[str]) -> None:
    system_id = str(row.get("system_id", "")).strip()
    if not system_id:
        failures.append("migration system row missing system_id")
        return
    if system_id not in REQUIRED_SYSTEM_IDS:
        failures.append(f"unexpected migration system id: {system_id}")

    if row.get("status") != "PLANNED_CONTRACT_ONLY":
        failures.append(f"{system_id} must be PLANNED_CONTRACT_ONLY")

    for key in [
        "current_javascript_evidence",
        "current_godot_surface",
        "migration_owner_module",
        "data_contract",
        "migration_order",
        "risk",
    ]:
        require_non_empty_string(row, key, system_id, failures)

    if str(row.get("migration_order", "")).strip() not in REQUIRED_SEQUENCE_IDS:
        failures.append(f"{system_id} migration_order must reference a G-5 sequence id")

    for source in require_non_empty_list(row, "source_files", system_id, failures):
        require_existing_path(source, f"{system_id} source file", failures)
    for godot_path in require_non_empty_list(row, "current_godot_files", system_id, failures):
        require_existing_path(godot_path, f"{system_id} current Godot file", failures)
    require_non_empty_list(row, "validation_gates", system_id, failures)


def validate_json(data: dict[str, Any], failures: list[str]) -> None:
    if data.get("schema_id") != "wayfarer.g5.migration_architecture.v1":
        failures.append("schema_id mismatch")
    if data.get("phase_id") != "G-5":
        failures.append("phase_id must be G-5")
    if data.get("planning_only") is not True:
        failures.append("G-5 must be marked planning_only=true")
    if data.get("production_route_change") is not False:
        failures.append("G-5 must not change the production route")
    if data.get("worker_route_remains_reference") is not True:
        failures.append("Worker route must remain reference")
    if data.get("g6_cutover_required_before_replacing_worker") is not True:
        failures.append("G-6 cutover must be required before replacing Worker")
    if data.get("agent_council_verdict") != "COUNCIL_PASS_READY_FOR_PR":
        failures.append("agent_council_verdict must be COUNCIL_PASS_READY_FOR_PR")
    if data.get("next_recommended_roadmap_phase") != "G-6 Production Cutover Planning":
        failures.append("next recommended phase must be G-6 Production Cutover Planning")

    evidence = data.get("source_evidence")
    if not isinstance(evidence, dict) or not evidence:
        failures.append("source_evidence must be a non-empty object")
    else:
        for label, raw_path in evidence.items():
            if not str(raw_path).strip():
                failures.append(f"source_evidence.{label} is empty")
                continue
            require_existing_path(str(raw_path), f"source evidence {label}", failures)

    systems = data.get("migration_systems")
    if not isinstance(systems, list):
        failures.append("migration_systems must be a list")
    else:
        by_id = {str(row.get("system_id", "")): row for row in systems if isinstance(row, dict)}
        for required_id in sorted(REQUIRED_SYSTEM_IDS):
            if required_id not in by_id:
                failures.append(f"missing migration system: {required_id}")
        for row in systems:
            if isinstance(row, dict):
                validate_system(row, failures)
            else:
                failures.append("migration_systems contains a non-object row")

    sequence = data.get("migration_sequence")
    if not isinstance(sequence, list):
        failures.append("migration_sequence must be a list")
    else:
        by_sequence = {str(row.get("sequence_id", "")): row for row in sequence if isinstance(row, dict)}
        for required_id in sorted(REQUIRED_SEQUENCE_IDS):
            if required_id not in by_sequence:
                failures.append(f"missing migration sequence: {required_id}")
        for sequence_id, row in by_sequence.items():
            for key in ["name", "objective", "entry_gate", "exit_gate"]:
                if not str(row.get(key, "")).strip():
                    failures.append(f"{sequence_id} missing {key}")

    boundaries = data.get("target_godot_boundaries")
    if not isinstance(boundaries, list) or len(boundaries) < 8:
        failures.append("target_godot_boundaries must include at least 8 service boundaries")

    principles = data.get("architecture_principles")
    if not isinstance(principles, list) or len(principles) < 5:
        failures.append("architecture_principles must include at least 5 rules")
    else:
        joined = " ".join(str(item) for item in principles).lower()
        for token in ["do not port", "worker", "save", "screenshot", "server-authoritative"]:
            if token not in joined:
                failures.append(f"architecture_principles missing concept: {token}")


def main() -> int:
    failures: list[str] = []
    data = load_json(REPORT_JSON, failures)
    require_text(REPORT_MD, REQUIRED_MARKDOWN_SECTIONS, failures)
    require_text(COUNCIL_REPORT, REQUIRED_COUNCIL_SECTIONS + ["COUNCIL_PASS_READY_FOR_PR"], failures)
    require_text(ROADMAP, ["Current G-5 result", "G-6 Production Cutover Planning"], failures)
    require_text(TECH_DEBT, ["Godot migration contract suite", "Save compatibility bridge"], failures)
    require_text(REGRESSION, ["G-5 Migration Architecture", "Golden Worker save fixtures"], failures)
    require_text(PR_CHECKLIST, ["G-5 migration architecture validator"], failures)
    if isinstance(data, dict):
        validate_json(data, failures)

    if failures:
        print("FAIL: G-5 migration architecture")
        for failure in failures:
            print(" - " + failure)
        return 1

    print("PASS: G-5 migration architecture")
    print(f"Report: {rel(REPORT_MD)}")
    print(f"Inventory: {rel(REPORT_JSON)}")
    print("Systems audited:", len(REQUIRED_SYSTEM_IDS))
    print("Migration sequences:", len(REQUIRED_SEQUENCE_IDS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
