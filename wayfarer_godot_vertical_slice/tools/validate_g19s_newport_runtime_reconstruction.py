#!/usr/bin/env python3
"""Validate the G-19S Newport blockout-to-Godot runtime reconstruction."""

from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Any

from opening_village_island_validator_common import PROJECT_ROOT, REPO_ROOT, load_json, print_result, require_path, require_text, validate_phase_contract


SOURCE_JSON = REPO_ROOT / "docs" / "design" / "NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.json"
ARTIFACT_DIR = PROJECT_ROOT / "artifacts" / "planning" / "g19r_newport_blockout"
STREET_PLAN = ARTIFACT_DIR / "g19r_newport_street_hierarchy.json"
LOT_PLAN = ARTIFACT_DIR / "g19r_newport_lot_plan.json"
NPC_ROUTE_PLAN = ARTIFACT_DIR / "g19r_newport_npc_route_plan.json"
CAMERA_PLAN = ARTIFACT_DIR / "g19r_newport_camera_viewpoints.json"
RUNTIME_SOURCE = PROJECT_ROOT / "data" / "world_layout" / "g19s_newport_runtime_reconstruction_v1.json"
BLUEPRINT = PROJECT_ROOT / "scripts" / "NewportTownBlueprint.gd"
MAP_LAYER = PROJECT_ROOT / "scenes" / "map" / "MapLayer.gd"
MAIN = PROJECT_ROOT / "scenes" / "Main.gd"
REPORT_MD = REPO_ROOT / "docs" / "reports" / "G19S_NEWPORT_BLOCKOUT_TO_GODOT_RUNTIME_RECONSTRUCTION.md"
COUNCIL_REPORT = REPO_ROOT / "docs" / "reports" / "G19S_NEWPORT_BLOCKOUT_TO_GODOT_AGENT_COUNCIL_REPORT.md"
SCREENSHOT_DIR = PROJECT_ROOT / "artifacts" / "review" / "g19s_runtime_screenshots"
SCREENSHOT_MANIFEST = SCREENSHOT_DIR / "g19s_runtime_screenshot_manifest.json"

REQUIRED_STREETS = {
    "main_commercial_avenue",
    "harborfront_road",
    "rear_service_street",
    "central_upland_counting_house_connector",
    "west_tavern_connector",
    "east_market_connector",
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
}

REQUIRED_NPCS = {
    "mara_pike_dockworker",
    "jonah_reed_dock_courier",
    "edrin_vale_counting_house_clerk",
    "bess_armitage_tavern_keeper",
    "honor_finch_merchant_shopkeeper",
    "silas_crowe_suspicious_patron",
}

REQUIRED_SCREENSHOTS = {
    "g19s_01_wide_town_cohesion_view.png",
    "g19s_02_arrival_harbor_view.png",
    "g19s_03_counting_house_route_view.png",
    "g19s_04_tavern_landmark_view.png",
    "g19s_05_commercial_avenue_view.png",
    "g19s_06_harbor_work_view.png",
    "g19s_07_rear_service_lane_view.png",
    "g19s_08_npc_route_proof_view.png",
    "g19s_09_village_exit_to_island_view.png",
    "g19s_10_quest_interaction_view.png",
    "g19s_11_debug_disabled_view.png",
}


def main() -> int:
    failures: list[str] = []
    validate_phase_contract("G-19S", failures)
    for path, label in [
        (SOURCE_JSON, "G-19R source-of-truth JSON"),
        (STREET_PLAN, "G-19R street hierarchy"),
        (LOT_PLAN, "G-19R lot plan"),
        (NPC_ROUTE_PLAN, "G-19R NPC route plan"),
        (CAMERA_PLAN, "G-19R camera viewpoint plan"),
        (RUNTIME_SOURCE, "G-19S runtime reconstruction source"),
        (BLUEPRINT, "Newport runtime blueprint"),
        (MAP_LAYER, "Newport map layer"),
        (MAIN, "Main runtime contract"),
        (REPORT_MD, "G-19S runtime reconstruction report"),
        (COUNCIL_REPORT, "G-19S Agent Council report"),
        (SCREENSHOT_MANIFEST, "G-19S runtime screenshot manifest"),
    ]:
        require_path(path, failures, label)

    require_text(
        BLUEPRINT,
        [
            "G19S_NEWPORT_RUNTIME_RECONSTRUCTION_PASS",
            "g19s_newport_runtime_layout_source_path",
            "g19s_runtime_reconstruction_contract",
            "runtime_layout_matches_G19R_source_of_truth",
            "no_new_layout_invented_in_Godot",
        ],
        failures,
    )
    require_text(
        MAP_LAYER,
        [
            "_draw_g19s_source_truth_street_plan",
            "_draw_g19s_source_truth_lots",
            "_draw_g19s_source_truth_wharf_water",
            "_draw_g19s_source_truth_props",
        ],
        failures,
    )
    require_text(MAIN, ["g19s_runtime_reconstruction_contract"], failures)
    require_text(
        REPORT_MD,
        [
            "G-19S Newport Blockout-To-Godot Runtime Reconstruction",
            "runtime_layout_matches_G19R_source_of_truth",
            "no_new_layout_invented_in_Godot",
            "canonical G-19R camera viewpoints",
            "Agent Council verdict: `COUNCIL_PASS_READY_FOR_PR`",
        ],
        failures,
    )
    require_text(
        COUNCIL_REPORT,
        [
            "G-19S Newport Blockout-To-Godot Runtime Reconstruction",
            "COUNCIL_PASS_READY_FOR_PR",
            "Does the runtime match the approved G-19R source of truth?",
            "Would this impress a first-time player?",
        ],
        failures,
    )

    source = load_json(SOURCE_JSON, failures)
    street_plan = load_json(STREET_PLAN, failures)
    lot_plan = load_json(LOT_PLAN, failures)
    npc_plan = load_json(NPC_ROUTE_PLAN, failures)
    camera_plan = load_json(CAMERA_PLAN, failures)
    runtime = load_json(RUNTIME_SOURCE, failures)
    screenshot_manifest = load_json(SCREENSHOT_MANIFEST, failures) if SCREENSHOT_MANIFEST.exists() else None

    if isinstance(runtime, dict):
        validate_runtime_source(runtime, source or {}, street_plan or {}, lot_plan or {}, npc_plan or {}, camera_plan or {}, failures)
    if isinstance(screenshot_manifest, dict):
        validate_screenshot_manifest(screenshot_manifest, failures)
    return print_result("G-19S Newport runtime reconstruction", failures)


def validate_runtime_source(
    runtime: dict[str, Any],
    source: dict[str, Any],
    street_plan: dict[str, Any],
    lot_plan: dict[str, Any],
    npc_plan: dict[str, Any],
    camera_plan: dict[str, Any],
    failures: list[str],
) -> None:
    if runtime.get("schema_id") != "wayfarer.g19s.newport.runtime_reconstruction.v1":
        failures.append("G-19S runtime source schema_id mismatch")
    if runtime.get("phase") != "G-19S":
        failures.append("G-19S runtime source phase must be G-19S")
    if runtime.get("source_of_truth") != "docs/design/NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.json":
        failures.append("G-19S runtime source must reference the G-19R source of truth")
    reconstruction = runtime.get("runtime_reconstruction", {})
    if not isinstance(reconstruction, dict):
        failures.append("G-19S runtime_reconstruction object missing")
        reconstruction = {}
    if reconstruction.get("no_new_layout_invented_in_godot") is not True:
        failures.append("G-19S must record no_new_layout_invented_in_godot=true")
    if reconstruction.get("major_runtime_layout_derives_from_g19r") is not True:
        failures.append("G-19S must record major_runtime_layout_derives_from_g19r=true")
    if _point(reconstruction.get("player_spawn")) != (430.0, 920.0):
        failures.append("G-19S player spawn must match G-19R arrival harbor")
    if _point(reconstruction.get("edrin_spawn")) != (1080.0, 555.0):
        failures.append("G-19S Edrin/counting clerk spawn must match G-19R counting house route")
    if float(reconstruction.get("water_edge_y", 0.0)) != 1120.0:
        failures.append("G-19S water_edge_y must preserve the G-19R harbor boundary")

    source_streets = _source_street_map(source, street_plan)
    runtime_streets = {str(item.get("id", "")): item for item in runtime.get("street_tile_rects", []) if isinstance(item, dict)}
    for street_id in sorted(REQUIRED_STREETS):
        item = runtime_streets.get(street_id)
        if not item:
            failures.append(f"G-19S runtime source missing street: {street_id}")
            continue
        source_item = source_streets.get(street_id, {})
        source_chars = float(source_item.get("width_character_units", 0.0))
        runtime_chars = float(item.get("width_character_units", 0.0))
        if source_chars and abs(runtime_chars - source_chars) > 0.11:
            failures.append(f"{street_id} width_character_units does not match G-19R source: runtime={runtime_chars} source={source_chars}")
        if _rect_area(item.get("source_world_rect")) <= 0:
            failures.append(f"{street_id} missing measured source_world_rect")
        if _rect_area(item.get("runtime_tile_rect")) <= 0:
            failures.append(f"{street_id} missing runtime_tile_rect")
    if float(runtime_streets.get("main_commercial_avenue", {}).get("width_character_units", 0.0)) < 10.0:
        failures.append("G-19S main commercial avenue regressed below 10 character widths")
    if float(runtime_streets.get("harborfront_road", {}).get("width_character_units", 0.0)) < 8.0:
        failures.append("G-19S harborfront road regressed below wharf scale")

    source_lots = _source_lot_map(lot_plan)
    runtime_lots = runtime.get("building_runtime_lots", [])
    if not isinstance(runtime_lots, list):
        failures.append("building_runtime_lots must be a list")
        runtime_lots = []
    seen_lot_ids = set()
    for item in runtime_lots:
        if not isinstance(item, dict):
            continue
        lot_id = str(item.get("g19r_lot_id", ""))
        seen_lot_ids.add(lot_id)
        position = _point(item.get("runtime_position"))
        lot_rect = _rect(source_lots.get(lot_id, {}).get("lot_size"))
        if lot_rect and not _point_inside_rect(position, lot_rect, margin=64.0):
            failures.append(f"{item.get('building_id')} runtime position {position} is not on/near G-19R lot {lot_id}")
    for lot_id in sorted(REQUIRED_LOTS):
        if lot_id not in seen_lot_ids:
            failures.append(f"G-19S runtime source missing core lot mapping: {lot_id}")

    route_points = _route_pause_points(npc_plan)
    runtime_npcs = runtime.get("npc_runtime_stations", [])
    if not isinstance(runtime_npcs, list):
        failures.append("npc_runtime_stations must be a list")
        runtime_npcs = []
    seen_npcs = set()
    for item in runtime_npcs:
        if not isinstance(item, dict):
            continue
        npc_id = str(item.get("npc_id", ""))
        seen_npcs.add(npc_id)
        route_id = str(item.get("g19r_route_id", ""))
        position = _point(item.get("runtime_position"))
        if "stationed_until_dedicated_walk_animation" not in str(item.get("movement_state", "")):
            failures.append(f"{npc_id} must remain stationed until dedicated walk animation is ready")
        if route_id in route_points and not any(_distance(position, point) <= 72.0 for point in route_points[route_id]):
            failures.append(f"{npc_id} runtime station is not near a G-19R route pause point for {route_id}")
    for npc_id in sorted(REQUIRED_NPCS):
        if npc_id not in seen_npcs:
            failures.append(f"G-19S runtime source missing NPC station: {npc_id}")

    camera_views = camera_plan.get("camera_viewpoints", [])
    if not isinstance(camera_views, list) or len(camera_views) < 11:
        failures.append("G-19R camera viewpoint source must contain the canonical 11 views for G-19S")
    if runtime.get("camera_viewpoints_source") != "wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_camera_viewpoints.json":
        failures.append("G-19S runtime source camera_viewpoints_source mismatch")


def validate_screenshot_manifest(manifest: dict[str, Any], failures: list[str]) -> None:
    if manifest.get("schema_id") != "wayfarer.g19s.runtime_screenshot_manifest.v1":
        failures.append("G-19S screenshot manifest schema mismatch")
    if manifest.get("phase") != "G-19S":
        failures.append("G-19S screenshot manifest phase mismatch")
    if manifest.get("status") != "PASS":
        failures.append("G-19S screenshot manifest status must be PASS")
    contract = manifest.get("g19s_runtime_reconstruction_contract", {})
    if not isinstance(contract, dict) or contract.get("runtime_layout_matches_G19R_source_of_truth") is not True:
        failures.append("G-19S screenshot manifest missing runtime layout contract proof")
    screenshots = manifest.get("screenshots", [])
    if not isinstance(screenshots, list):
        failures.append("G-19S screenshots must be a list")
        screenshots = []
    filenames = {str(item.get("filename", "")) for item in screenshots if isinstance(item, dict)}
    for filename in sorted(REQUIRED_SCREENSHOTS):
        if filename not in filenames:
            failures.append(f"G-19S screenshot manifest missing {filename}")
    for item in screenshots:
        if not isinstance(item, dict):
            continue
        if item.get("status") != "PASS":
            failures.append(f"{item.get('filename')} screenshot status is not PASS")
        png = item.get("png_verification", {})
        if not isinstance(png, dict) or png.get("status") != "PASS":
            failures.append(f"{item.get('filename')} PNG verification did not pass")
        path = Path(str(item.get("absolute_path", "")))
        if not path.exists():
            failures.append(f"{item.get('filename')} missing PNG on disk: {path}")


def _source_street_map(source: dict[str, Any], street_plan: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for container in [source.get("streets"), street_plan.get("streets")]:
        if not isinstance(container, list):
            continue
        for item in container:
            if isinstance(item, dict):
                result[str(item.get("id", ""))] = item
    return result


def _source_lot_map(lot_plan: dict[str, Any]) -> dict[str, dict[str, Any]]:
    lots = lot_plan.get("lots", [])
    if not isinstance(lots, list):
        return {}
    return {str(item.get("id", "")): item for item in lots if isinstance(item, dict)}


def _route_pause_points(npc_plan: dict[str, Any]) -> dict[str, list[tuple[float, float]]]:
    result: dict[str, list[tuple[float, float]]] = {}
    routes = npc_plan.get("npc_routes", [])
    if not isinstance(routes, list):
        return result
    for item in routes:
        if not isinstance(item, dict):
            continue
        route_id = str(item.get("id", ""))
        points: list[tuple[float, float]] = []
        for key in ["home_station", "work_destination"]:
            point = _point(item.get(key))
            if point != (0.0, 0.0):
                points.append(point)
        pauses = item.get("pause_points", [])
        if isinstance(pauses, list):
            for pause in pauses:
                points.append(_point(pause))
        result[route_id] = points
    return result


def _rect(raw: Any) -> tuple[float, float, float, float] | None:
    if not isinstance(raw, dict):
        return None
    values = []
    for key in ["x", "y", "w", "h"]:
        try:
            values.append(float(raw.get(key, 0.0)))
        except (TypeError, ValueError):
            return None
    if values[2] <= 0 or values[3] <= 0:
        return None
    return (values[0], values[1], values[2], values[3])


def _rect_area(raw: Any) -> float:
    rect = _rect(raw)
    if rect is None:
        return 0.0
    return rect[2] * rect[3]


def _point(raw: Any) -> tuple[float, float]:
    if isinstance(raw, dict):
        try:
            return (float(raw.get("x", 0.0)), float(raw.get("y", 0.0)))
        except (TypeError, ValueError):
            return (0.0, 0.0)
    return (0.0, 0.0)


def _point_inside_rect(point: tuple[float, float], rect: tuple[float, float, float, float], margin: float = 0.0) -> bool:
    x, y = point
    rx, ry, rw, rh = rect
    return rx - margin <= x <= rx + rw + margin and ry - margin <= y <= ry + rh + margin


def _distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


if __name__ == "__main__":
    sys.exit(main())
