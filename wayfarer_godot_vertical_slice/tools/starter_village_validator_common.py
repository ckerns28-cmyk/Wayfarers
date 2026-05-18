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
BLUEPRINT = PROJECT_ROOT / "scripts" / "NewportTownBlueprint.gd"
MAP_LAYER = PROJECT_ROOT / "scenes" / "map" / "MapLayer.gd"
HUD_SCENE = PROJECT_ROOT / "scenes" / "ui" / "HUD.tscn"
CHARACTER_MANIFEST = PROJECT_ROOT / "art_pipeline" / "player_identity" / "manifests" / "newport_atelier_characters_g422r_manifest.json"

REQUIRED_PHASES = [
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
