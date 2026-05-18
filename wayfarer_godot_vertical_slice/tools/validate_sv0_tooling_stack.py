#!/usr/bin/env python3
"""Validate the SV-0 free tooling stack lock."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[1]
REPO_ROOT = PROJECT_ROOT.parent

REPORT_MD = REPO_ROOT / "docs" / "reports" / "SV0_FREE_TOOLING_INTAKE_PRODUCTION_STACK_LOCK.md"
REPORT_JSON = REPO_ROOT / "docs" / "reports" / "SV0_FREE_TOOLING_INTAKE_PRODUCTION_STACK_LOCK.json"
ACQUISITION_MD = REPO_ROOT / "docs" / "reports" / "SV0_TOOL_ACQUISITION_MANIFEST.md"
ACQUISITION_JSON = REPO_ROOT / "docs" / "reports" / "SV0_TOOL_ACQUISITION_MANIFEST.json"
TOOLING_ROADMAP_MD = REPO_ROOT / "docs" / "roadmaps" / "STARTER_VILLAGE_TOOLING_STACK.md"
SV1_ROADMAP_MD = REPO_ROOT / "docs" / "roadmaps" / "STARTER_VILLAGE_PLAYABLE_OBSESSION_ROADMAP.md"
SV1_ROADMAP_JSON = REPO_ROOT / "docs" / "roadmaps" / "STARTER_VILLAGE_PLAYABLE_OBSESSION_ROADMAP.json"
SV1_LEDGER_MD = REPO_ROOT / "docs" / "reports" / "STARTER_VILLAGE_AUTONOMOUS_EXECUTION_LEDGER.md"
SV1_LEDGER_JSON = REPO_ROOT / "docs" / "reports" / "STARTER_VILLAGE_AUTONOMOUS_EXECUTION_LEDGER.json"
AGENTS_MD = REPO_ROOT / "AGENTS.md"
PR_CHECKLIST = REPO_ROOT / "docs" / "checklists" / "WAYFARER_PR_REVIEW_CHECKLIST.md"
REGRESSION_CHECKLIST = REPO_ROOT / "docs" / "REGRESSION_TEST_CHECKLIST.md"
COUNCIL_TOOL = REPO_ROOT / "tools" / "wayfarer_agent_council.py"

WORLD_LAYOUT = PROJECT_ROOT / "data" / "world_layout" / "starter_village_world_layout_v1.json"
VISUAL_QA = PROJECT_ROOT / "data" / "visual_qa" / "starter_village_visual_regression_manifest_v1.json"
MOVEMENT_PROOF = PROJECT_ROOT / "data" / "movement_proof" / "starter_village_movement_proof_manifest_v1.json"
GROUND_STACK = PROJECT_ROOT / "data" / "ground_materials" / "starter_village_ground_material_stack_v1.json"

ALLOWED_DECISIONS = {"ADOPT_NOW", "SPIKE_ONLY", "DEFER", "REJECT", "ALREADY_COVERED"}
REQUIRED_CATEGORY_IDS = {str(index) for index in range(1, 10)}
REQUIRED_TOOL_FIELDS = [
    "tool_name",
    "purpose",
    "license",
    "cost_free_status",
    "godot_version_compatibility",
    "web_review_build_risk",
    "ci_automation_compatibility",
    "installation_path",
    "rollback_path",
    "helps_sv1",
    "provenance_safety",
]


def rel(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def load_json(path: Path, failures: list[str]) -> dict[str, Any] | None:
    if not path.exists():
        failures.append(f"missing json: {rel(path)}")
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


def require_text(path: Path, tokens: list[str], failures: list[str]) -> None:
    if not path.exists():
        failures.append(f"missing text file: {rel(path)}")
        return
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        if token not in text:
            failures.append(f"{rel(path)} missing token: {token}")


def require_path(path: Path, failures: list[str], label: str) -> None:
    if not path.exists():
        failures.append(f"missing {label}: {rel(path)}")


def check_nonempty(value: Any, path: str, failures: list[str]) -> None:
    if value is None or value == "" or value == [] or value == {}:
        failures.append(f"missing non-empty value: {path}")


def check_tool(tool: dict[str, Any], path: str, failures: list[str], adopted: bool) -> None:
    fields = REQUIRED_TOOL_FIELDS if adopted else [
        "tool_name",
        "decision",
        "license",
        "cost_free_status",
        "godot_version_compatibility",
        "web_review_build_risk",
        "ci_automation_compatibility",
        "installation_path",
        "rollback_path",
        "helps_sv1",
        "provenance_safety",
    ]
    for field in fields:
        check_nonempty(tool.get(field), f"{path}.{field}", failures)
    if not adopted:
        decision = str(tool.get("decision", ""))
        if decision not in ALLOWED_DECISIONS:
            failures.append(f"{path}.decision invalid: {decision}")
    if adopted and "addons/" in str(tool.get("installation_path", "")).replace("\\", "/"):
        addon_path = REPO_ROOT / str(tool["installation_path"]).replace("\\", "/")
        proof = str(tool.get("validation_proof", "")).strip()
        if not addon_path.exists() and not proof:
            failures.append(f"{path} adopted Godot addon must exist or carry validation proof")


def list_ids(items: Any, key: str = "id") -> set[str]:
    if not isinstance(items, list):
        return set()
    return {str(item.get(key, "")) for item in items if isinstance(item, dict)}


def validate_report(data: dict[str, Any], failures: list[str]) -> None:
    if data.get("schema_id") != "wayfarer.sv0.free_tooling_stack_lock.v1":
        failures.append("SV-0 report schema_id mismatch")
    if data.get("phase_id") != "SV-0":
        failures.append("SV-0 report phase_id must be SV-0")
    if data.get("cost_policy") != "free_only_no_paid_dependencies":
        failures.append("SV-0 cost policy must be free only")
    safety = data.get("safety_policy")
    if not isinstance(safety, dict):
        failures.append("safety_policy must be an object")
    else:
        for key in [
            "do_not_delete_old_files_or_photos",
            "do_not_move_external_drive_contents",
            "do_not_reformat_drives",
            "do_not_overwrite_non_wayfarer_folders",
        ]:
            if safety.get(key) is not True:
                failures.append(f"safety_policy.{key} must be true")
    outcomes = data.get("required_outcomes")
    if not isinstance(outcomes, dict):
        failures.append("required_outcomes must be an object")
    else:
        for key, value in outcomes.items():
            if value is not True:
                failures.append(f"required outcome is not locked: {key}")

    categories = data.get("tool_categories")
    if not isinstance(categories, list):
        failures.append("tool_categories must be a list")
        return
    seen_ids: set[str] = set()
    decisions: dict[str, str] = {}
    for index, category in enumerate(categories):
        if not isinstance(category, dict):
            failures.append(f"tool_categories[{index}] must be an object")
            continue
        category_id = str(category.get("category_id", ""))
        seen_ids.add(category_id)
        decision = str(category.get("decision", ""))
        decisions[category_id] = decision
        if decision not in ALLOWED_DECISIONS:
            failures.append(f"category {category_id} invalid decision: {decision}")
        check_nonempty(category.get("category_name"), f"category {category_id}.category_name", failures)
        selected = category.get("selected_tool")
        if not isinstance(selected, dict):
            failures.append(f"category {category_id} missing selected_tool")
        else:
            check_tool(selected, f"category {category_id}.selected_tool", failures, adopted=decision == "ADOPT_NOW")
            if decision == "ADOPT_NOW":
                install_path = str(selected.get("installation_path", ""))
                if install_path.startswith("wayfarer_godot_vertical_slice/"):
                    require_path(REPO_ROOT / install_path, failures, f"adopted tool path for category {category_id}")
        alternatives = category.get("evaluated_tools", [])
        if not isinstance(alternatives, list):
            failures.append(f"category {category_id} evaluated_tools must be a list")
        else:
            for alt_index, alternative in enumerate(alternatives):
                if not isinstance(alternative, dict):
                    failures.append(f"category {category_id} evaluated_tools[{alt_index}] must be an object")
                    continue
                check_tool(alternative, f"category {category_id}.evaluated_tools[{alt_index}]", failures, adopted=False)

    missing = REQUIRED_CATEGORY_IDS - seen_ids
    if missing:
        failures.append("missing tool categories: " + ", ".join(sorted(missing)))
    for category_id, expected in {
        "1": "ADOPT_NOW",
        "2": "ADOPT_NOW",
        "3": "ADOPT_NOW",
        "4": "ADOPT_NOW",
        "5": "ADOPT_NOW",
        "6": "ADOPT_NOW",
        "7": "ADOPT_NOW",
        "8": "ADOPT_NOW",
        "9": "ADOPT_NOW",
    }.items():
        if decisions.get(category_id) != expected:
            failures.append(f"category {category_id} must be {expected}")
    serialized = json.dumps(data)
    for forbidden in ["NEEDS_HUMAN_REVIEW", "READY_FOR_HUMAN_VISUAL_REVIEW", "AWAITING_CHRIS_REVIEW", "VISUAL_REVIEW_REQUIRED", "TECHNICAL_PASS_ONLY"]:
        if forbidden in serialized:
            failures.append(f"SV-0 report contains deprecated status: {forbidden}")
    policy = data.get("phase_gate_policy")
    if not isinstance(policy, dict):
        failures.append("phase_gate_policy must be an object")
    else:
        for key in [
            "all_future_sv_phases_must_reference_sv0_stack",
            "screenshot_evidence_can_override_written_pass",
            "movement_phases_require_motion_proof",
            "new_unvalidated_one_off_systems_are_failures",
        ]:
            if policy.get(key) is not True:
                failures.append(f"phase_gate_policy.{key} must be true")


def validate_world_layout(data: dict[str, Any], failures: list[str]) -> None:
    if data.get("schema_id") != "wayfarer.starter_village.world_layout.v1":
        failures.append("world layout schema_id mismatch")
    for key, minimum in {
        "districts": 7,
        "roads": 5,
        "alleys": 2,
        "dock_paths": 3,
        "lots": 12,
        "building_anchors": 3,
        "npc_routes": 7,
        "interaction_zones": 4,
        "quest_beat_locations": 6,
        "camera_viewpoints": 9,
    }.items():
        value = data.get(key)
        if not isinstance(value, list) or len(value) < minimum:
            failures.append(f"world layout {key} must contain at least {minimum} rows")
    camera_ids = list_ids(data.get("camera_viewpoints"))
    for required in ["wide_town", "arrival_harbor", "tavern", "commercial_avenue", "harbor_wharf", "npc_movement", "quest_interaction", "debug_disabled"]:
        if required not in camera_ids:
            failures.append(f"world layout missing camera viewpoint: {required}")
    npc_routes = data.get("npc_routes", [])
    if isinstance(npc_routes, list):
        for route in npc_routes:
            if isinstance(route, dict) and not route.get("movement_policy"):
                failures.append(f"npc route missing movement_policy: {route.get('npc_id')}")


def validate_visual_qa(data: dict[str, Any], failures: list[str]) -> None:
    if data.get("schema_id") != "wayfarer.starter_village.visual_regression_manifest.v1":
        failures.append("visual QA schema_id mismatch")
    views = data.get("minimum_required_views")
    if not isinstance(views, list) or len(views) < 15:
        failures.append("visual QA manifest must include at least 15 recurring views")
    checks = set(str(item) for item in data.get("automatic_warning_checks", []))
    for required in ["image_not_blank", "debug_overlay_absent_in_normal_views", "large_layout_pixel_change_requires_council_note"]:
        if required not in checks:
            failures.append(f"visual QA missing warning check: {required}")
    fail_conditions = set(str(item) for item in data.get("council_fail_conditions", []))
    for required in ["screenshot_contradicts_written_pass", "building_overlap_or_clipped_building_visible", "npc_static_sprite_glide"]:
        if required not in fail_conditions:
            failures.append(f"visual QA missing council fail condition: {required}")
    if "warning" not in str(data.get("diff_status", "")).lower():
        failures.append("visual diff status must be warning-oriented, not final art authority")


def validate_movement_proof(data: dict[str, Any], failures: list[str]) -> None:
    if data.get("schema_id") != "wayfarer.starter_village.movement_proof_manifest.v1":
        failures.append("movement proof schema_id mismatch")
    phases = set(str(item) for item in data.get("required_for_phases", []))
    for phase_id in ["G-8", "G-8A", "G-11", "G-12", "G-14"]:
        if phase_id not in phases:
            failures.append(f"movement proof missing required phase: {phase_id}")
    sequences = list_ids(data.get("required_sequences"))
    for required in ["player_directional_walk", "npc_idle_station", "npc_route_walk_when_enabled", "interaction_prompt_priority"]:
        if required not in sequences:
            failures.append(f"movement proof missing sequence: {required}")
    metadata = set(str(item) for item in data.get("minimum_capture_metadata", []))
    for required in ["timestamp_msec", "position", "facing_direction", "animation_state", "screenshot_path"]:
        if required not in metadata:
            failures.append(f"movement proof missing metadata: {required}")


def validate_ground_stack(data: dict[str, Any], failures: list[str]) -> None:
    if data.get("schema_id") != "wayfarer.starter_village.ground_material_stack.v1":
        failures.append("ground material stack schema_id mismatch")
    families = list_ids(data.get("material_families"))
    for required in [
        "harbor_dock_plank",
        "wharf_cobble_apron",
        "waterfront_road",
        "uphill_road",
        "frontage_lot_stone",
        "service_yard_gravel",
        "residential_grass_edge",
        "water_edge",
    ]:
        if required not in families:
            failures.append(f"ground material missing family: {required}")
    rules = " ".join(str(item) for item in data.get("cohesion_rules", []))
    for token in ["No large translucent road rectangles", "Every building base", "Props cannot be used"]:
        if token not in rules:
            failures.append(f"ground material rules missing token: {token}")


def main() -> int:
    failures: list[str] = []

    for path, label in [
        (REPORT_MD, "SV-0 markdown report"),
        (REPORT_JSON, "SV-0 json report"),
        (ACQUISITION_MD, "SV-0 tool acquisition markdown manifest"),
        (ACQUISITION_JSON, "SV-0 tool acquisition json manifest"),
        (TOOLING_ROADMAP_MD, "Starter Village tooling roadmap"),
        (WORLD_LAYOUT, "world layout source"),
        (VISUAL_QA, "visual QA manifest"),
        (MOVEMENT_PROOF, "movement proof manifest"),
        (GROUND_STACK, "ground material stack"),
        (SV1_ROADMAP_MD, "Starter Village roadmap markdown"),
        (SV1_ROADMAP_JSON, "Starter Village roadmap json"),
        (SV1_LEDGER_MD, "Starter Village ledger markdown"),
        (SV1_LEDGER_JSON, "Starter Village ledger json"),
        (AGENTS_MD, "AGENTS.md"),
        (PR_CHECKLIST, "PR checklist"),
        (REGRESSION_CHECKLIST, "regression checklist"),
        (COUNCIL_TOOL, "Agent Council tool"),
    ]:
        require_path(path, failures, label)

    require_text(REPORT_MD, ["SV-0", "ADOPT_NOW", "COUNCIL_PASS_READY_FOR_PR", "screenshots can override reports", "SV-0 Tool Acquisition Manifest"], failures)
    require_text(ACQUISITION_MD, ["No paid tools", "No Google/browser credentials", "Deferred Or Spike-Only Tools"], failures)
    require_text(TOOLING_ROADMAP_MD, ["Locked Stack", "Runtime movement proof", "External Tool Policy", "Tool Acquisition Manifest"], failures)
    require_text(AGENTS_MD, ["SV-0", "locked SV-0 tooling stack", "movement proof", "SV-0 Tool Acquisition Manifest"], failures)
    require_text(PR_CHECKLIST, ["SV-0 tooling stack", "movement proof", "SV-0 tool acquisition manifest"], failures)
    require_text(REGRESSION_CHECKLIST, ["SV-0", "visual regression", "validate_sv0_tool_acquisition_manifest.py"], failures)
    require_text(COUNCIL_TOOL, ["validate_sv0_tooling_stack.py", "validate_sv0_tool_acquisition_manifest.py", "SV-0 Tooling Stack"], failures)
    require_text(SV1_ROADMAP_MD, ["SV-0", "Starter Village Tooling Stack"], failures)
    require_text(SV1_LEDGER_MD, ["SV-0", "Free Tooling Intake Production Stack Lock"], failures)

    report = load_json(REPORT_JSON, failures)
    world = load_json(WORLD_LAYOUT, failures)
    visual = load_json(VISUAL_QA, failures)
    movement = load_json(MOVEMENT_PROOF, failures)
    ground = load_json(GROUND_STACK, failures)
    if isinstance(report, dict):
        validate_report(report, failures)
    if isinstance(world, dict):
        validate_world_layout(world, failures)
    if isinstance(visual, dict):
        validate_visual_qa(visual, failures)
    if isinstance(movement, dict):
        validate_movement_proof(movement, failures)
    if isinstance(ground, dict):
        validate_ground_stack(ground, failures)

    if failures:
        print("FAIL: SV-0 tooling stack")
        for failure in failures:
            print(" - " + failure)
        return 1
    print("PASS: SV-0 tooling stack")
    print("Categories audited: 9")
    print(f"World layout source: {rel(WORLD_LAYOUT)}")
    print(f"Visual QA manifest: {rel(VISUAL_QA)}")
    print(f"Movement proof manifest: {rel(MOVEMENT_PROOF)}")
    print(f"Ground material stack: {rel(GROUND_STACK)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
