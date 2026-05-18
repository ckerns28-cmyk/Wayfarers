#!/usr/bin/env python3
"""Validate the G-6 production cutover planning package.

G-6 is a release-safety planning phase. It defines route ownership, rollback,
QA gates, and cutover criteria while proving that the JavaScript Worker remains
the production route.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[1]
REPO_ROOT = PROJECT_ROOT.parent

REPORT_MD = REPO_ROOT / "docs" / "reports" / "G6_PRODUCTION_CUTOVER_PLANNING.md"
REPORT_JSON = REPO_ROOT / "docs" / "reports" / "G6_PRODUCTION_CUTOVER_PLANNING.json"
COUNCIL_REPORT = REPO_ROOT / "docs" / "reports" / "G6_PRODUCTION_CUTOVER_AGENT_COUNCIL_REPORT.md"
ROADMAP = REPO_ROOT / "docs" / "WAYFARER_GODOT_ROADMAP.md"
WEB_DELIVERY = PROJECT_ROOT / "WEB_DELIVERY.md"
TECH_DEBT = REPO_ROOT / "docs" / "TECH_DEBT_REGISTER.md"
REGRESSION = REPO_ROOT / "docs" / "REGRESSION_TEST_CHECKLIST.md"
PR_CHECKLIST = REPO_ROOT / "docs" / "checklists" / "WAYFARER_PR_REVIEW_CHECKLIST.md"
ROOT_WRANGLER = REPO_ROOT / "wrangler.toml"
WORKER_WRANGLER = REPO_ROOT / "wayfarer_v7_github_ready" / "worker" / "wrangler.toml"

EXPECTED_WORKER_MAIN = 'main = "wayfarer_v7_github_ready/worker/src/index.js"'
EXPECTED_WORKER_ASSETS = 'directory = "./wayfarer_v7_github_ready/worker/assets"'

REQUIRED_DECISION_IDS = {
    "keep_js_worker_production_route",
    "parallel_godot_itch_review_route",
    "parallel_godot_pages_preview_route",
    "replace_worker_with_godot_route",
    "hybrid_worker_router_godot_client",
}

REQUIRED_QA_GATE_IDS = {
    "preflight_branch_remote",
    "production_route_protection",
    "g5_parity_evidence",
    "save_compatibility_round_trip",
    "godot_web_export_served",
    "runtime_visual_qa",
    "performance_browser_matrix",
    "rollback_rehearsal",
    "release_authority",
}

REQUIRED_REPORT_SECTIONS = [
    "## Status",
    "## Why G-6 Exists",
    "## Source Evidence",
    "## Hosting Decision Matrix",
    "## Hard Cutover Preconditions",
    "## QA Gates",
    "## Cutover Runbook",
    "## Rollback Plan",
    "## Route Protection",
    "## Known Caveats",
    "## Blockers To Actual Cutover",
    "## Recommendation",
]

REQUIRED_COUNCIL_SECTIONS = [
    "## Roadmap Execution Result",
    "## Production Route Audit",
    "## Hosting Decision Audit",
    "## Rollback Readiness Audit",
    "## QA Gate Audit",
    "## Scrum Master Review",
    "## Game Designer Review",
    "## Art Director Review",
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


def repo_path(raw_path: str) -> Path:
    normalized = raw_path.replace("\\", "/")
    if normalized.startswith("res://"):
        return PROJECT_ROOT / normalized.removeprefix("res://")
    return REPO_ROOT / normalized


def require_existing_path(raw_path: str, label: str, failures: list[str]) -> None:
    path = repo_path(raw_path)
    if not path.exists():
        failures.append(f"missing {label}: {raw_path}")


def require_text(path: Path, tokens: list[str], failures: list[str]) -> str:
    if fail_missing(path, failures):
        return ""
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        if token not in text:
            failures.append(f"{rel(path)} missing token: {token}")
    return text


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


def require_non_empty_list(data: dict[str, Any], key: str, failures: list[str]) -> list[Any]:
    value = data.get(key)
    if not isinstance(value, list) or not value:
        failures.append(f"{key} must be a non-empty list")
        return []
    return value


def validate_source_evidence(data: dict[str, Any], failures: list[str]) -> None:
    evidence = data.get("source_evidence")
    if not isinstance(evidence, dict) or not evidence:
        failures.append("source_evidence must be a non-empty object")
        return
    for label, raw_path in evidence.items():
        if not str(raw_path).strip():
            failures.append(f"source_evidence.{label} is empty")
            continue
        require_existing_path(str(raw_path), f"source evidence {label}", failures)


def validate_current_routes(data: dict[str, Any], failures: list[str]) -> None:
    routes = data.get("current_routes")
    if not isinstance(routes, dict):
        failures.append("current_routes must be an object")
        return
    production = routes.get("production_route")
    godot_review = routes.get("godot_review_route")
    if not isinstance(production, dict):
        failures.append("current_routes.production_route must be an object")
    else:
        if production.get("main") != "wayfarer_v7_github_ready/worker/src/index.js":
            failures.append("production route main must remain the JavaScript Worker")
        if production.get("status") != "ACTIVE_PRODUCTION_REFERENCE":
            failures.append("production route status must be ACTIVE_PRODUCTION_REFERENCE")
    if not isinstance(godot_review, dict):
        failures.append("current_routes.godot_review_route must be an object")
    else:
        if godot_review.get("status") != "PARALLEL_REVIEW_ONLY":
            failures.append("Godot review route status must be PARALLEL_REVIEW_ONLY")


def validate_decision_matrix(data: dict[str, Any], failures: list[str]) -> None:
    rows = require_non_empty_list(data, "decision_matrix", failures)
    by_id = {str(row.get("decision_id", "")): row for row in rows if isinstance(row, dict)}
    for required_id in sorted(REQUIRED_DECISION_IDS):
        if required_id not in by_id:
            failures.append(f"missing decision matrix row: {required_id}")
    for decision_id, row in by_id.items():
        for key in ["option", "status", "reason", "risk", "guardrail"]:
            if not str(row.get(key, "")).strip():
                failures.append(f"{decision_id} missing {key}")
    replace = by_id.get("replace_worker_with_godot_route")
    if isinstance(replace, dict) and replace.get("status") != "NOT_AUTHORIZED":
        failures.append("replace_worker_with_godot_route must be NOT_AUTHORIZED in G-6")


def validate_qa_gates(data: dict[str, Any], failures: list[str]) -> None:
    rows = require_non_empty_list(data, "qa_gates", failures)
    by_id = {str(row.get("gate_id", "")): row for row in rows if isinstance(row, dict)}
    for required_id in sorted(REQUIRED_QA_GATE_IDS):
        if required_id not in by_id:
            failures.append(f"missing QA gate: {required_id}")
    for gate_id, row in by_id.items():
        for key in ["name", "required_evidence"]:
            if not str(row.get(key, "")).strip():
                failures.append(f"{gate_id} missing {key}")
        if row.get("blocking") is not True:
            failures.append(f"{gate_id} must be blocking")


def validate_runbook(data: dict[str, Any], key: str, minimum_steps: int, failures: list[str]) -> None:
    rows = require_non_empty_list(data, key, failures)
    if len(rows) < minimum_steps:
        failures.append(f"{key} must include at least {minimum_steps} steps")
    expected_step = 1
    for row in rows:
        if not isinstance(row, dict):
            failures.append(f"{key} contains non-object row")
            continue
        if row.get("step") != expected_step:
            failures.append(f"{key} step sequence expected {expected_step}")
        expected_step += 1
        for field in ["name", "action"]:
            if not str(row.get(field, "")).strip():
                failures.append(f"{key} step {row.get('step')} missing {field}")


def validate_json(data: dict[str, Any], failures: list[str]) -> None:
    expected_values = {
        "schema_id": "wayfarer.g6.production_cutover_plan.v1",
        "phase_id": "G-6",
        "phase_name": "Production Cutover Planning",
        "agent_council_verdict": "COUNCIL_PASS_READY_FOR_PR",
        "next_recommended_roadmap_phase": "NO_NEXT_PHASE_DEFINED_IN_ROADMAP",
    }
    for key, expected in expected_values.items():
        if data.get(key) != expected:
            failures.append(f"{key} must be {expected}")

    bool_requirements = {
        "planning_only": True,
        "production_route_change": False,
        "worker_route_remains_production": True,
        "cutover_authorized_now": False,
    }
    for key, expected in bool_requirements.items():
        if data.get(key) is not expected:
            failures.append(f"{key} must be {expected}")

    validate_source_evidence(data, failures)
    validate_current_routes(data, failures)
    validate_decision_matrix(data, failures)
    validate_qa_gates(data, failures)
    validate_runbook(data, "cutover_runbook", 7, failures)
    validate_runbook(data, "rollback_runbook", 4, failures)

    hard_preconditions = require_non_empty_list(data, "hard_cutover_preconditions", failures)
    if len(hard_preconditions) < 8:
        failures.append("hard_cutover_preconditions must include at least 8 requirements")

    route_files = [str(item) for item in data.get("route_files_that_must_not_change_in_g6", [])]
    for required_path in ["wrangler.toml", "wayfarer_v7_github_ready/worker/wrangler.toml"]:
        if required_path not in route_files:
            failures.append(f"route_files_that_must_not_change_in_g6 missing {required_path}")

    blockers = " ".join(str(item).lower() for item in data.get("blockers_to_actual_cutover", []))
    for token in ["save", "parity", "rollback", "g-5"]:
        if token not in blockers:
            failures.append(f"blockers_to_actual_cutover missing concept: {token}")


def validate_wrangler_route(failures: list[str]) -> None:
    text = require_text(ROOT_WRANGLER, [EXPECTED_WORKER_MAIN, EXPECTED_WORKER_ASSETS], failures)
    if "wayfarer_godot_vertical_slice" in text:
        failures.append("root wrangler.toml must not point at the Godot slice in G-6")
    require_text(
        WORKER_WRANGLER,
        ['main = "src/index.js"', 'directory = "./assets"', 'binding = "ASSETS"'],
        failures,
    )


def main() -> int:
    failures: list[str] = []
    data = load_json(REPORT_JSON, failures)

    require_text(REPORT_MD, REQUIRED_REPORT_SECTIONS + ["COUNCIL_PASS_READY_FOR_PR"], failures)
    require_text(COUNCIL_REPORT, REQUIRED_COUNCIL_SECTIONS + ["COUNCIL_PASS_READY_FOR_PR"], failures)
    require_text(ROADMAP, ["Current G-6 result", "Production Cutover Planning"], failures)
    require_text(WEB_DELIVERY, ["G-6 Production Cutover Planning", "wayfarer_v7_github_ready/worker/src/index.js"], failures)
    require_text(TECH_DEBT, ["Production cutover is blocked until G-5 parity evidence exists"], failures)
    require_text(REGRESSION, ["G-6 Production Cutover Planning", "Production route protection"], failures)
    require_text(PR_CHECKLIST, ["G-6 production cutover validator"], failures)
    validate_wrangler_route(failures)

    if isinstance(data, dict):
        validate_json(data, failures)

    if failures:
        print("FAIL: G-6 production cutover planning")
        for failure in failures:
            print(" - " + failure)
        return 1

    print("PASS: G-6 production cutover planning")
    print(f"Report: {rel(REPORT_MD)}")
    print(f"Plan: {rel(REPORT_JSON)}")
    print("Decision rows:", len(REQUIRED_DECISION_IDS))
    print("QA gates:", len(REQUIRED_QA_GATE_IDS))
    print("Production route: JavaScript Worker remains active")
    return 0


if __name__ == "__main__":
    sys.exit(main())
