#!/usr/bin/env python3
"""Validate the pre-G-5 roadmap execution ledger.

The ledger gate exists because a later council pass is not enough when runtime
screenshots contradict the visible player-facing result. G-5 readiness fails if
any required row is missing, unproven, or not backed by phase evidence.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[1]
REPO_ROOT = PROJECT_ROOT.parent
LEDGER_JSON = REPO_ROOT / "docs" / "reports" / "PRE_G5_ROADMAP_EXECUTION_LEDGER.json"
LEDGER_MD = REPO_ROOT / "docs" / "reports" / "PRE_G5_ROADMAP_EXECUTION_LEDGER.md"
G422R_VALIDATOR = PROJECT_ROOT / "tools" / "validate_g422r_runtime_asset_consistency.py"

REQUIRED_PHASES = [
    "G-4.23B",
    "G-4.18E",
    "G-4.19",
    "G-4.20",
    "G-4.21",
    "G-4.22",
    "G-4.22R",
]

ALLOWED_STATUSES = {
    "PASS",
    "FAIL_NEEDS_CODE_FIX",
    "UNPROVEN_NEEDS_EVIDENCE_OR_REPAIR",
    "BLOCKED_REQUIRES_HUMAN_ESCALATION",
}


def rel(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def repo_path(value: str) -> Path:
    normalized = value.replace("\\", "/")
    if normalized.startswith("res://"):
        return PROJECT_ROOT / normalized.removeprefix("res://")
    return REPO_ROOT / normalized


def load_ledger(failures: list[str]) -> dict[str, Any] | None:
    for path in [LEDGER_JSON, LEDGER_MD]:
        if not path.exists():
            failures.append(f"missing ledger file: {rel(path)}")
    if not LEDGER_JSON.exists():
        return None
    try:
        data = json.loads(LEDGER_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        failures.append(f"invalid ledger json: {exc}")
        return None
    if not isinstance(data, dict):
        failures.append("ledger json root must be an object")
        return None
    return data


def list_field(row: dict[str, Any], name: str, failures: list[str]) -> list[str]:
    value = row.get(name)
    if not isinstance(value, list) or not value:
        failures.append(f"{row.get('phase_id', '<unknown>')} missing non-empty {name}")
        return []
    result = [str(item) for item in value if str(item).strip()]
    if not result:
        failures.append(f"{row.get('phase_id', '<unknown>')} has empty {name}")
    return result


def require_existing_paths(phase_id: str, paths: list[str], label: str, failures: list[str]) -> None:
    for raw_path in paths:
        path = repo_path(raw_path)
        if not path.exists():
            failures.append(f"{phase_id} missing {label}: {raw_path}")


def validate_row(row: dict[str, Any], failures: list[str]) -> None:
    phase_id = str(row.get("phase_id", "")).strip()
    if not phase_id:
        failures.append("ledger row missing phase_id")
        return

    status = str(row.get("current_status", "")).strip()
    if status not in ALLOWED_STATUSES:
        failures.append(f"{phase_id} has invalid status: {status}")
    elif status != "PASS":
        failures.append(f"{phase_id} is not PASS: {status}")

    for required_text in [
        "phase_name",
        "roadmap_source",
        "expected_outcome",
        "branch",
        "agent_council_report_path",
        "agent_council_verdict",
        "art_direction_result",
        "world_layout_result",
        "gameplay_readability_result",
        "technical_stability_result",
        "provenance_result",
        "north_star_result",
        "reason_for_status",
        "next_required_action",
    ]:
        if not str(row.get(required_text, "")).strip():
            failures.append(f"{phase_id} missing {required_text}")

    implementing_prs = list_field(row, "implementing_prs", failures)
    commits = list_field(row, "commits", failures)
    list_field(row, "files_changed", failures)
    validation_commands = list_field(row, "validation_commands", failures)

    if phase_id != "G-4.22R" and any("pending" in item.lower() for item in implementing_prs):
        failures.append(f"{phase_id} must not use pending PR evidence")
    if phase_id != "G-4.22R" and any("working-tree" in item.lower() for item in commits):
        failures.append(f"{phase_id} must use committed merge evidence")
    if phase_id == "G-4.22R" and not any("pending_current_remediation_pr" in item for item in implementing_prs):
        # After PR creation this may become a numeric PR; both are valid for this branch.
        if not any(item.startswith("#") for item in implementing_prs):
            failures.append("G-4.22R must record the remediation PR or pending remediation PR marker")

    council_report = str(row.get("agent_council_report_path", "")).strip()
    if council_report:
        council_path = repo_path(council_report)
        if phase_id != "G-4.22R" and not council_path.exists():
            failures.append(f"{phase_id} missing council report: {council_report}")

    if row.get("agent_council_verdict") != "COUNCIL_PASS_READY_FOR_PR":
        failures.append(f"{phase_id} council verdict is not COUNCIL_PASS_READY_FOR_PR")

    if bool(row.get("visual_player_facing")):
        screenshots = list_field(row, "screenshot_paths", failures)
        require_existing_paths(phase_id, screenshots, "screenshot evidence", failures)
        if "screenshot" not in " ".join(validation_commands).lower():
            failures.append(f"{phase_id} lacks screenshot validation command evidence")

    if bool(row.get("asset_player_npc_world_phase")):
        provenance = str(row.get("provenance_result", "")).upper()
        if "PASS" not in provenance:
            failures.append(f"{phase_id} asset/player/NPC/world phase lacks provenance PASS")


def run_g422r_runtime_validator(failures: list[str]) -> None:
    if not G422R_VALIDATOR.exists():
        failures.append(f"missing runtime asset consistency validator: {rel(G422R_VALIDATOR)}")
        return
    result = subprocess.run(
        [sys.executable, str(G422R_VALIDATOR)],
        cwd=str(REPO_ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        output = (result.stdout + "\n" + result.stderr).strip()
        failures.append("G-4.22R runtime asset consistency validator failed: " + " ".join(output.split()))


def main() -> int:
    failures: list[str] = []
    ledger = load_ledger(failures)
    if isinstance(ledger, dict):
        if ledger.get("schema_id") != "wayfarer.pre_g5.roadmap_execution_ledger.v1":
            failures.append("ledger schema_id mismatch")
        phases = ledger.get("phases")
        if not isinstance(phases, list):
            failures.append("ledger phases must be a list")
        else:
            by_phase = {str(row.get("phase_id", "")): row for row in phases if isinstance(row, dict)}
            for phase_id in REQUIRED_PHASES:
                if phase_id not in by_phase:
                    failures.append(f"missing required pre-G-5 phase row: {phase_id}")
            for phase_id in REQUIRED_PHASES:
                row = by_phase.get(phase_id)
                if isinstance(row, dict):
                    validate_row(row, failures)
            extra_nonpass = [
                str(row.get("phase_id", "<unknown>"))
                for row in phases
                if isinstance(row, dict) and str(row.get("current_status", "")) != "PASS"
            ]
            if extra_nonpass:
                failures.append("ledger contains non-PASS phase rows: " + ", ".join(extra_nonpass))

    run_g422r_runtime_validator(failures)

    if failures:
        print("FAIL: pre-G-5 roadmap execution ledger")
        for failure in failures:
            print(" - " + failure)
        return 1

    print("PASS: pre-G-5 roadmap execution ledger")
    print(f"Ledger: {rel(LEDGER_JSON)}")
    print("Rows audited:", len(REQUIRED_PHASES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
