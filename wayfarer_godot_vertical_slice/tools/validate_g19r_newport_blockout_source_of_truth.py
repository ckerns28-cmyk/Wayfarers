#!/usr/bin/env python3
"""Validate the G-19R Newport scale/street blockout source of truth."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from opening_village_island_validator_common import PROJECT_ROOT, REPO_ROOT, load_json, print_result, require_path, require_text, validate_phase_contract


DESIGN_MD = REPO_ROOT / "docs" / "design" / "NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.md"
DESIGN_JSON = REPO_ROOT / "docs" / "design" / "NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.json"
REPORT_MD = REPO_ROOT / "docs" / "reports" / "G19R_NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.md"
COUNCIL_REPORT = REPO_ROOT / "docs" / "reports" / "G19R_NEWPORT_SCALE_STREET_BLOCKOUT_AGENT_COUNCIL_REPORT.md"
ROADMAP_MD = REPO_ROOT / "docs" / "roadmaps" / "OPENING_VILLAGE_ISLAND_PRODUCTION_ROADMAP.md"
LEDGER_MD = REPO_ROOT / "docs" / "reports" / "OPENING_VILLAGE_ISLAND_AUTONOMOUS_EXECUTION_LEDGER.md"
ARTIFACT_DIR = PROJECT_ROOT / "artifacts" / "planning" / "g19r_newport_blockout"

REQUIRED_ARTIFACTS = {
    "blockout_svg": ARTIFACT_DIR / "g19r_newport_measured_blockout.svg",
    "blockout_png": ARTIFACT_DIR / "g19r_newport_measured_blockout.png",
    "scale_metrics": ARTIFACT_DIR / "g19r_newport_scale_metrics.json",
    "district_plan": ARTIFACT_DIR / "g19r_newport_district_plan.json",
    "street_hierarchy": ARTIFACT_DIR / "g19r_newport_street_hierarchy.json",
    "lot_plan": ARTIFACT_DIR / "g19r_newport_lot_plan.json",
    "npc_route_plan": ARTIFACT_DIR / "g19r_newport_npc_route_plan.json",
    "quest_beat_locations": ARTIFACT_DIR / "g19r_newport_quest_beat_locations.json",
    "camera_viewpoints": ARTIFACT_DIR / "g19r_newport_camera_viewpoints.json",
    "blockout_manifest": ARTIFACT_DIR / "g19r_newport_blockout_manifest.json",
}

REQUIRED_DISTRICTS = {
    "harbor_wharf",
    "counting_house_clerk",
    "tavern_inn_rumor_hub",
    "commercial_avenue",
    "rear_service_lane",
    "residential_edge",
    "village_to_island_exit",
}

REQUIRED_STREETS = {
    "harborfront_road",
    "main_commercial_avenue",
    "rear_service_street",
    "dock_paths",
    "hidden_rumor_cutthrough",
    "village_to_island_road",
}

REQUIRED_LOTS = {
    "lot_tavern_inn_centerpiece",
    "lot_counting_house_clerk",
    "lot_mercantile_shop",
    "lot_chandlery_outfitter",
    "lot_market_shed",
    "lot_west_dock_warehouse",
    "lot_central_boathouse_landing",
    "lot_cooperage_service",
    "lot_boarding_house",
    "lot_dockworker_rowhouse",
    "lot_clerk_lodging",
    "lot_civic_notice_board",
    "lot_village_exit_guidepost",
}

REQUIRED_QUEST_BEATS = {
    "arrival_harbor_beat",
    "first_objective_beat",
    "counting_house_missing_manifest_beat",
    "dock_clue_beat",
    "tavern_whisper_beat",
    "two_npc_rumor_beat",
    "island_lead_beat",
    "village_exit_beat",
    "optional_hidden_clue_beat",
    "return_report_beat",
}

REQUIRED_VIEWPOINTS = {
    "wide_town_cohesion_view",
    "arrival_harbor_view",
    "counting_house_route_view",
    "tavern_landmark_view",
    "commercial_avenue_view",
    "harbor_work_view",
    "rear_service_lane_view",
    "npc_route_proof_view",
    "village_exit_to_island_view",
    "quest_interaction_view",
    "debug_disabled_view",
}


def main() -> int:
    failures: list[str] = []
    validate_phase_contract("G-19R", failures)
    for label, path in REQUIRED_ARTIFACTS.items():
        require_path(path, failures, f"G-19R {label}")
    require_text(
        DESIGN_MD,
        [
            "Newport Scale + Street Blockout Source Of Truth",
            "Figma/FigJam was not used",
            "Scale Derivation",
            "Major runtime layout edits",
            "G-19S Newport Blockout-To-Godot Runtime Reconstruction",
        ],
        failures,
    )
    require_text(
        REPORT_MD,
        [
            "G-19R Newport Scale + Street Blockout Source Of Truth",
            "Figma/FigJam used: no",
            "Current 3-tile road audit",
            "Agent Council verdict: `COUNCIL_PASS_READY_FOR_PR`",
        ],
        failures,
    )
    require_text(
        COUNCIL_REPORT,
        [
            "G-19R Newport Scale + Street Blockout Source of Truth",
            "COUNCIL_PASS_READY_FOR_PR",
            "Did Codex use design-production thinking instead of code-only implementation?",
            "Is there a source of truth future phases must follow?",
        ],
        failures,
    )
    require_text(
        ROADMAP_MD,
        [
            "G-19R | Newport Scale + Street Blockout Source of Truth",
            "G-19S | Newport Blockout-To-Godot Runtime Reconstruction",
            "G-19R corrective acceptance",
        ],
        failures,
    )
    require_text(LEDGER_MD, ["G-19R Source-Of-Truth Gate", "G-19S | Newport Blockout-To-Godot Runtime Reconstruction"], failures)

    source = load_json(DESIGN_JSON, failures)
    metrics = load_json(REQUIRED_ARTIFACTS["scale_metrics"], failures)
    district_plan = load_json(REQUIRED_ARTIFACTS["district_plan"], failures)
    street_plan = load_json(REQUIRED_ARTIFACTS["street_hierarchy"], failures)
    lot_plan = load_json(REQUIRED_ARTIFACTS["lot_plan"], failures)
    npc_plan = load_json(REQUIRED_ARTIFACTS["npc_route_plan"], failures)
    quest_plan = load_json(REQUIRED_ARTIFACTS["quest_beat_locations"], failures)
    camera_plan = load_json(REQUIRED_ARTIFACTS["camera_viewpoints"], failures)
    manifest = load_json(REQUIRED_ARTIFACTS["blockout_manifest"], failures)

    if isinstance(source, dict):
        validate_source(source, failures)
    if isinstance(metrics, dict):
        validate_scale_metrics(metrics, failures)
    if isinstance(district_plan, dict):
        validate_required_ids(district_plan.get("districts"), REQUIRED_DISTRICTS, "district", failures)
    if isinstance(street_plan, dict):
        validate_streets(street_plan, failures)
    if isinstance(lot_plan, dict):
        validate_lots(lot_plan, failures)
    if isinstance(npc_plan, dict):
        validate_npcs(npc_plan, failures)
    if isinstance(quest_plan, dict):
        validate_required_ids(quest_plan.get("quest_beats"), REQUIRED_QUEST_BEATS, "quest beat", failures)
    if isinstance(camera_plan, dict):
        validate_required_ids(camera_plan.get("camera_viewpoints"), REQUIRED_VIEWPOINTS, "camera viewpoint", failures)
    if isinstance(manifest, dict):
        validate_manifest(manifest, failures)
    validate_not_only_code_changes(failures)

    return print_result("G-19R Newport blockout source of truth", failures)


def validate_source(data: dict[str, Any], failures: list[str]) -> None:
    if data.get("schema_id") != "wayfarer.g19r.newport_scale_street_blockout_source_of_truth.v1":
        failures.append("source-of-truth schema_id mismatch")
    if data.get("phase") != "G-19R":
        failures.append("source-of-truth phase must be G-19R")
    if data.get("status") != "PASS":
        failures.append("source-of-truth status must be PASS")
    if data.get("figma_figjam", {}).get("used") is not False:
        failures.append("G-19R must document Figma/FigJam usage or fallback; expected local fallback used=false")
    if len(data.get("browser_research_sources", [])) < 4:
        failures.append("G-19R must document browser/design-production research sources")
    governance = data.get("future_placement_governance", {})
    if not isinstance(governance, dict) or governance.get("major_layout_files_guarded") in (None, []):
        failures.append("future placement governance is missing guarded layout files")
    if "validate_newport_layout_source_alignment.py" not in str(governance):
        failures.append("future placement governance must reference validate_newport_layout_source_alignment.py")
    scores = data.get("acceptance_scores", {})
    for key in [
        "blockout_layout_plan_score",
        "world_cohesion_plan_score",
        "player_orientation_plan_score",
        "quest_geography_integration_score",
        "implementation_readiness_score",
    ]:
        if float(scores.get(key, 0.0)) < 8.5:
            failures.append(f"G-19R score below 8.5: {key}")
    validate_required_ids(data.get("districts"), REQUIRED_DISTRICTS, "source district", failures)
    validate_required_ids(data.get("streets"), REQUIRED_STREETS, "source street", failures)
    validate_required_ids(data.get("lots"), REQUIRED_LOTS, "source lot", failures)
    validate_required_ids(data.get("quest_beats"), REQUIRED_QUEST_BEATS, "source quest beat", failures)
    validate_required_ids(data.get("camera_viewpoints"), REQUIRED_VIEWPOINTS, "source camera viewpoint", failures)


def validate_scale_metrics(data: dict[str, Any], failures: list[str]) -> None:
    if data.get("schema_id") != "wayfarer.g19r.newport.scale_metrics.v1":
        failures.append("scale metrics schema mismatch")
    player = data.get("player_derived_scale", {})
    for key in [
        "player_visual_width_world_units",
        "player_visual_height_world_units",
        "player_collision_body_width_world_units",
        "player_collision_body_height_world_units",
        "camera_viewport_assumption_px",
        "gameplay_zoom_assumption",
        "pixels_per_character_width",
        "world_units_per_character_width",
    ]:
        if key not in player:
            failures.append(f"player-derived scale missing {key}")
    character_width = float(player.get("world_units_per_character_width", 0.0))
    if character_width <= 0:
        failures.append("world_units_per_character_width must be positive")
    targets = data.get("street_width_targets", {})
    for key in [
        "main_commercial_harbor_street",
        "secondary_street",
        "rear_service_lane",
        "alley_service_cutthrough",
        "wharf_working_apron",
        "npc_route_clearance",
        "interaction_clearance",
        "minimum_readable_landmark_spacing",
    ]:
        item = targets.get(key, {})
        if not isinstance(item, dict) or float(item.get("width_world_units", 0.0)) <= 0:
            failures.append(f"street/clearance target missing measured width: {key}")
    main = targets.get("main_commercial_harbor_street", {})
    main_chars = float(main.get("selected_character_widths", 0.0))
    if not (10.0 <= main_chars <= 15.0):
        failures.append("main commercial/harbor street width must be measured at 10-15 character widths")
    audit = data.get("current_runtime_scale_audit", {})
    if float(audit.get("current_primary_road_three_tiles_character_widths", 99.0)) >= 10.0:
        failures.append("current road audit should record existing three-tile roads as below target")


def validate_required_ids(items: Any, required: set[str], label: str, failures: list[str]) -> None:
    if not isinstance(items, list):
        failures.append(f"{label} list missing")
        return
    seen = {str(item.get("id", "")) for item in items if isinstance(item, dict)}
    for required_id in sorted(required):
        if required_id not in seen:
            failures.append(f"missing {label}: {required_id}")


def validate_streets(data: dict[str, Any], failures: list[str]) -> None:
    streets = data.get("streets")
    validate_required_ids(streets, REQUIRED_STREETS, "street", failures)
    if not isinstance(streets, list):
        return
    by_id = {item.get("id"): item for item in streets if isinstance(item, dict)}
    main = by_id.get("main_commercial_avenue", {})
    if float(main.get("width_character_units", 0.0)) < 10.0:
        failures.append("main_commercial_avenue width must be at least 10 character units")
    for street in streets:
        if not isinstance(street, dict):
            continue
        for key in [
            "start_point",
            "end_point",
            "width_character_units",
            "width_world_units",
            "districts_connected",
            "player_purpose",
            "npc_route_usage",
            "quest_usage",
            "ground_type",
            "landmark_sightline",
            "camera_readability_note",
        ]:
            if street.get(key) in (None, "", [], {}):
                failures.append(f"street {street.get('id', '<unknown>')} missing {key}")
    counting_route = by_id.get("central_upland_counting_house_connector", {})
    if "counting_house_clerk" not in counting_route.get("districts_connected", []):
        failures.append("counting house route is missing or does not connect counting_house_clerk")
    exit_route = by_id.get("village_to_island_road", {})
    if "village_to_island_exit" not in exit_route.get("districts_connected", []):
        failures.append("village-to-island exit route is missing")


def validate_lots(data: dict[str, Any], failures: list[str]) -> None:
    lots = data.get("lots")
    validate_required_ids(lots, REQUIRED_LOTS, "lot", failures)
    if not isinstance(lots, list):
        return
    for lot in lots:
        if not isinstance(lot, dict):
            continue
        for key in [
            "district",
            "building_role",
            "frontage_street",
            "entry_orientation",
            "lot_size",
            "building_footprint_target",
            "setback_world_units",
            "npc_use",
            "quest_use",
            "sightline_purpose",
        ]:
            if lot.get(key) in (None, "", [], {}):
                failures.append(f"lot {lot.get('id', '<unknown>')} missing {key}")


def validate_npcs(data: dict[str, Any], failures: list[str]) -> None:
    routes = data.get("npc_routes")
    if not isinstance(routes, list) or len(routes) < 5:
        failures.append("NPC route plan must define at least five roles")
        return
    text = json.dumps(routes)
    for role in ["dockworker", "counting house clerk", "tavern patron", "merchant", "courier"]:
        if role not in text:
            failures.append(f"NPC route plan missing role: {role}")
    for route in routes:
        if not isinstance(route, dict):
            continue
        if "stationed_until_dedicated_walk_animation" not in str(route.get("movement_state", "")):
            failures.append(f"NPC route must keep static sprites stationed until animation proof: {route.get('id', '<unknown>')}")
        if "No static sprite" not in str(route.get("animation_movement_requirements", "")) and "Do not glide" not in str(route.get("animation_movement_requirements", "")):
            failures.append(f"NPC route missing no-glide policy: {route.get('id', '<unknown>')}")


def validate_manifest(data: dict[str, Any], failures: list[str]) -> None:
    if data.get("schema_id") != "wayfarer.g19r.newport.blockout_manifest.v1":
        failures.append("blockout manifest schema mismatch")
    if data.get("status") != "PASS":
        failures.append("blockout manifest status must be PASS")
    if data.get("primary_change_type") != "design_source_of_truth":
        failures.append("blockout manifest must mark primary_change_type=design_source_of_truth")
    if data.get("godot_runtime_placement_changed") is not False:
        failures.append("G-19R must not claim runtime Godot placement changes")
    if data.get("future_placement_governance_present") is not True:
        failures.append("blockout manifest missing future placement governance")
    artifact_paths = {str(item.get("path", "")) for item in data.get("artifacts", []) if isinstance(item, dict)}
    for path in REQUIRED_ARTIFACTS.values():
        if str(path.relative_to(REPO_ROOT).as_posix()) not in artifact_paths and path.name != "g19r_newport_blockout_manifest.json":
            failures.append(f"blockout manifest missing artifact: {path.name}")


def validate_not_only_code_changes(failures: list[str]) -> None:
    changed: set[str] = set()
    for args in [
        ["git", "diff", "--name-only", "origin/main...HEAD"],
        ["git", "diff", "--name-only"],
        ["git", "diff", "--name-only", "--cached"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    ]:
        result = subprocess.run(args, cwd=REPO_ROOT, text=True, capture_output=True, check=False)
        if result.returncode == 0:
            changed.update(line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip())
    if not changed:
        return
    source_or_artifact = [
        path
        for path in changed
        if path.startswith("docs/design/")
        or path.startswith("docs/reports/G19R_")
        or path.startswith("docs/roadmaps/")
        or path.startswith("wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/")
    ]
    code_only_suffixes = (".py", ".gd", ".tscn", ".uid", ".cs")
    if changed and not source_or_artifact and all(path.endswith(code_only_suffixes) for path in changed):
        failures.append("G-19R cannot pass with only code changes; design/source artifacts are required")


if __name__ == "__main__":
    sys.exit(main())
