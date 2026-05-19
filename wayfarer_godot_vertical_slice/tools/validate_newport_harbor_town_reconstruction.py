#!/usr/bin/env python3
"""Validate the G-19R Newport harbor town reconstruction guardrail.

This is a corrective validator for the "cart before the horse" failure: art was
ready, but the city structure was not locked. It checks that Newport is now
authored from district, road, wharf, lot, and camera-composition requirements
before later guidance or prop polish can claim success.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

from opening_village_island_validator_common import (
    LEDGER_JSON,
    PROJECT_ROOT,
    REPO_ROOT,
    ROADMAP_JSON,
    load_json,
    print_result,
    require_text,
)


SOURCE_JSON = PROJECT_ROOT / "data" / "world_layout" / "newport_harbor_town_reconstruction_v1.json"
BLUEPRINT_GD = PROJECT_ROOT / "scripts" / "NewportTownBlueprint.gd"
MAP_LAYER_GD = PROJECT_ROOT / "scenes" / "map" / "MapLayer.gd"
MAIN_GD = PROJECT_ROOT / "scenes" / "Main.gd"
CAPTURE_GD = PROJECT_ROOT / "tools" / "capture_g19r_runtime_screenshots.gd"
CAPTURE_PS1 = PROJECT_ROOT / "tools" / "capture_g19r_runtime_screenshots.ps1"
ROADMAP_MD = REPO_ROOT / "docs" / "roadmaps" / "OPENING_VILLAGE_ISLAND_PRODUCTION_ROADMAP.md"
LEDGER_MD = REPO_ROOT / "docs" / "reports" / "OPENING_VILLAGE_ISLAND_AUTONOMOUS_EXECUTION_LEDGER.md"
G19_REPORT_JSON = REPO_ROOT / "docs" / "reports" / "G19_PLAYER_GUIDANCE_JOURNAL_INTERACTION_POLISH.json"

REQUIRED_PLANNING_ORDER = [
    "landform_and_water_edge",
    "primary_harborfront_avenue",
    "uphill_civic_route",
    "rear_service_lane",
    "wharf_apron_and_work_docks",
    "district_lots_and_frontages",
    "building_anchors",
    "npc_stations",
    "quest_route_readability",
    "functional_props_last",
    "fresh_wide_screenshot_review",
]

REQUIRED_ROUTE_WIDTHS = {
    "waterfront_avenue_main": (360, 300),
    "civic_uphill_route": (190, 160),
    "rear_service_lane": (180, 140),
    "west_tavern_climb": (150, 120),
    "market_exit_to_island": (180, 150),
    "wharf_work_apron": (340, 280),
}

REQUIRED_DISTRICTS = {
    "upper_residential_terrace",
    "civic_green_counting_house",
    "rear_service_lane",
    "waterfront_avenue_lots",
    "working_wharf_apron",
    "east_gate_settlement_edge",
}

REQUIRED_ROUTE_SPINES = {
    "waterfront_avenue_main",
    "civic_uphill_route",
    "rear_service_lane",
    "west_tavern_climb",
    "market_exit_to_island",
    "wharf_work_apron",
}

REQUIRED_BUILDINGS = {
    "b_inn_tavern",
    "b_clerk_townhouse",
    "b_mercantile",
    "b_counting_house",
    "b_chandlery_front",
    "b_shop_house",
    "b_market_shed",
    "b_printer_rowhouse",
    "b_custom_house",
    "b_res_small",
    "b_large_residence",
    "b_boarding_house",
    "b_dockworker_rowhouse",
    "b_cooperage_shed",
    "b_dock_warehouse",
    "b_wharf_boathouse",
    "b_dock_storehouse",
}

REQUIRED_DOCK_NPC_STATIONS = {
    "mara_pike_dockworker": {
        "position": (390.0, 812.0),
        "standing_surface": "west_pier_landing",
        "blocked_rects": {"b_dock_warehouse": (378.0, 624.0, 216.0, 146.0)},
    },
    "jonah_reed_dock_courier": {
        "position": (1196.0, 812.0),
        "standing_surface": "east_storehouse_landing",
        "blocked_rects": {"b_dock_storehouse": (1219.0, 636.0, 208.0, 128.0)},
    },
}

DOCK_NPC_FRONT_DECK_MIN_Y = 790.0


def _rows_by_id(data: dict[str, Any], key: str) -> dict[str, dict[str, Any]]:
    rows = data.get(key, [])
    if not isinstance(rows, list):
        return {}
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        if isinstance(row, dict):
            row_id = str(row.get("id", "")).strip()
            if row_id:
                result[row_id] = row
    return result


def _rect(row: dict[str, Any], key: str = "rect") -> dict[str, Any]:
    value = row.get(key, {})
    return value if isinstance(value, dict) else {}


def _validate_source(data: dict[str, Any], failures: list[str]) -> None:
    if data.get("schema_id") != "wayfarer.newport.harbor_town_reconstruction.v1":
        failures.append("G-19R reconstruction source schema mismatch")
    if data.get("phase") != "G-19R":
        failures.append("G-19R reconstruction source phase mismatch")
    if data.get("authoring_mode") != "composition_first_godot_native_json":
        failures.append("G-19R authoring_mode must be composition_first_godot_native_json")

    method_reset = data.get("method_reset", {})
    if not isinstance(method_reset, dict) or method_reset.get("preserve_assets") is not True:
        failures.append("G-19R must explicitly preserve existing building/drawing assets")
    if isinstance(method_reset, dict) and method_reset.get("engine_change_required") is not False:
        failures.append("G-19R must record that the engine/language is not the root problem")
    if "layered procedural repair" not in str(method_reset.get("reject_method", "")):
        failures.append("G-19R must reject layered procedural repair as the acceptance method")

    planning_order = data.get("planning_order", [])
    if planning_order != REQUIRED_PLANNING_ORDER:
        failures.append("G-19R planning_order must lock city structure before props and screenshots")

    structure = data.get("city_structure_requirements", {})
    if not isinstance(structure, dict):
        failures.append("G-19R missing city_structure_requirements")
    else:
        for flag in [
            "road_hierarchy_required",
            "street_widths_authored_before_props",
            "districts_authored_before_lots",
            "walkable_negative_space_required",
            "camera_readability_required",
        ]:
            if structure.get(flag) is not True:
                failures.append(f"G-19R city_structure_requirements missing true flag: {flag}")
        widths = structure.get("road_widths_px", {})
        if not isinstance(widths, dict):
            failures.append("G-19R road_widths_px must be an object")
        else:
            for route_id, (target, minimum) in REQUIRED_ROUTE_WIDTHS.items():
                spec = widths.get(route_id, {})
                if not isinstance(spec, dict):
                    failures.append(f"G-19R missing road width spec: {route_id}")
                    continue
                if int(spec.get("target", 0)) != target or int(spec.get("minimum", 0)) != minimum:
                    failures.append(f"G-19R bad road width for {route_id}: expected target {target}, minimum {minimum}")
                if not str(spec.get("reason", "")).strip():
                    failures.append(f"G-19R road width spec missing reason: {route_id}")
        block_spacing = structure.get("block_spacing_px", {})
        if not isinstance(block_spacing, dict) or int(block_spacing.get("commercial_frontage_gap_min", 0)) < 120:
            failures.append("G-19R commercial_frontage_gap_min must be at least 120 px")
        review_questions = structure.get("review_questions", [])
        if not isinstance(review_questions, list) or len(review_questions) < 6:
            failures.append("G-19R must include city-structure review questions")
        if "10-15 characters shoulder to shoulder" not in json.dumps(structure):
            failures.append("G-19R must require 10-15 character shoulder-to-shoulder avenue and wharf scale")

    districts = _rows_by_id(data, "district_bands")
    for district_id in REQUIRED_DISTRICTS:
        if district_id not in districts:
            failures.append(f"G-19R missing district band: {district_id}")
    for district_id, row in districts.items():
        rect = _rect(row)
        if float(rect.get("w", 0)) <= 0 or float(rect.get("h", 0)) <= 0:
            failures.append(f"G-19R district has invalid rect: {district_id}")
        if not str(row.get("purpose", "")).strip():
            failures.append(f"G-19R district missing purpose: {district_id}")

    routes = _rows_by_id(data, "route_spines")
    for route_id in REQUIRED_ROUTE_SPINES:
        if route_id not in routes:
            failures.append(f"G-19R missing route spine: {route_id}")
    for route_id, row in routes.items():
        rect = _rect(row)
        polyline = row.get("polyline", [])
        if float(rect.get("w", 0)) <= 0 and not isinstance(polyline, list):
            failures.append(f"G-19R route spine has no rect or polyline: {route_id}")
        if route_id in REQUIRED_ROUTE_WIDTHS and isinstance(polyline, list):
            _, minimum = REQUIRED_ROUTE_WIDTHS[route_id]
            if int(row.get("width", 0)) < minimum and float(rect.get("h", 0)) < minimum:
                failures.append(f"G-19R route spine too narrow: {route_id}")

    lots = data.get("lots", [])
    if not isinstance(lots, list) or len(lots) < len(REQUIRED_BUILDINGS):
        failures.append("G-19R must define lots for every required Newport building")
    else:
        building_ids = {str(row.get("building_id", "")) for row in lots if isinstance(row, dict)}
        for building_id in REQUIRED_BUILDINGS:
            if building_id not in building_ids:
                failures.append(f"G-19R missing lot for building: {building_id}")
        for row in lots:
            if not isinstance(row, dict):
                continue
            if not str(row.get("frontage", "")).strip():
                failures.append(f"G-19R lot missing frontage: {row.get('id')}")
            if not str(row.get("role", "")).strip():
                failures.append(f"G-19R lot missing role: {row.get('id')}")

    props = data.get("functional_props", [])
    if not isinstance(props, list) or len(props) < 6:
        failures.append("G-19R must include restrained functional props after city structure")
    else:
        for row in props:
            if not isinstance(row, dict):
                continue
            if not str(row.get("purpose", "")).strip():
                failures.append(f"G-19R functional prop missing purpose: {row.get('id')}")
            if "debug" in str(row.get("purpose", "")).lower():
                failures.append(f"G-19R functional prop purpose looks debug-like: {row.get('id')}")

    stations = _rows_by_id(data, "npc_station_guardrails")
    for npc_id, requirement in REQUIRED_DOCK_NPC_STATIONS.items():
        row = stations.get(npc_id)
        if not row:
            failures.append(f"G-19R missing NPC station guardrail: {npc_id}")
            continue
        pos = row.get("position", {})
        if not isinstance(pos, dict):
            failures.append(f"G-19R NPC station guardrail has invalid position: {npc_id}")
            continue
        actual = (float(pos.get("x", 0.0)), float(pos.get("y", 0.0)))
        expected = requirement["position"]
        if actual != expected:
            failures.append(f"G-19R NPC station guardrail mismatch for {npc_id}: expected {expected}, found {actual}")
        if row.get("standing_surface") != requirement["standing_surface"]:
            failures.append(f"G-19R NPC station has wrong standing surface for {npc_id}: {row.get('standing_surface')}")
        if actual[1] < DOCK_NPC_FRONT_DECK_MIN_Y:
            failures.append(f"G-19R NPC station is too far up the building body/roof band: {npc_id}")
        for building_id, rect in requirement["blocked_rects"].items():
            if _point_in_rect(actual, rect):
                failures.append(f"G-19R NPC station overlaps {building_id} body/roof band: {npc_id}")
        blocked = row.get("must_not_overlap_building_body", [])
        if not isinstance(blocked, list) or not set(requirement["blocked_rects"]).issubset({str(item) for item in blocked}):
            failures.append(f"G-19R NPC station guardrail missing blocked building body list: {npc_id}")

    acceptance = data.get("acceptance", {})
    if not isinstance(acceptance, dict):
        failures.append("G-19R missing acceptance object")
    else:
        for flag in [
            "preserves_atelier_assets",
            "requires_runtime_override_from_source",
            "requires_validator_guardrail",
            "requires_no_false_pass_report",
        ]:
            if acceptance.get(flag) is not True:
                failures.append(f"G-19R acceptance missing true flag: {flag}")
        if float(acceptance.get("target_town_cohesion_score", 0.0)) < 8.5:
            failures.append("G-19R target_town_cohesion_score must be at least 8.5")


def _validate_no_false_g19_pass(failures: list[str]) -> None:
    if not G19_REPORT_JSON.exists():
        return
    try:
        data = json.loads(G19_REPORT_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        failures.append(f"G-19 report JSON exists but is invalid: {exc}")
        return
    if isinstance(data, dict) and data.get("status") == "PASS":
        failures.append("G-19 report JSON claims PASS while G-19R reconstruction is active")


def _point_in_rect(point: tuple[float, float], rect: tuple[float, float, float, float]) -> bool:
    x, y = point
    rect_x, rect_y, rect_w, rect_h = rect
    return rect_x <= x <= rect_x + rect_w and rect_y <= y <= rect_y + rect_h


def _extract_vector_after_id(source: str, npc_id: str) -> tuple[float, float] | None:
    match = re.search(
        rf'"{re.escape(npc_id)}"[\s\S]{{0,600}}?Vector2\(\s*([0-9.]+)\s*,\s*([0-9.]+)\s*\)',
        source,
    )
    if not match:
        return None
    return (float(match.group(1)), float(match.group(2)))


def _validate_runtime_dock_npc_positions(blueprint_source: str, map_layer_source: str, failures: list[str]) -> None:
    for npc_id, requirement in REQUIRED_DOCK_NPC_STATIONS.items():
        expected = requirement["position"]
        for label, source in [("blueprint", blueprint_source), ("map layer", map_layer_source)]:
            actual = _extract_vector_after_id(source, npc_id)
            if actual is None:
                failures.append(f"G-19R {label} missing runtime station for {npc_id}")
                continue
            if actual != expected:
                failures.append(f"G-19R {label} runtime station mismatch for {npc_id}: expected {expected}, found {actual}")
            if actual[1] < DOCK_NPC_FRONT_DECK_MIN_Y:
                failures.append(f"G-19R {label} runtime station still sits in roof/body band for {npc_id}")
            for building_id, rect in requirement["blocked_rects"].items():
                if _point_in_rect(actual, rect):
                    failures.append(f"G-19R {label} runtime station overlaps {building_id}: {npc_id}")


def main() -> int:
    failures: list[str] = []
    source = load_json(SOURCE_JSON, failures)
    load_json(ROADMAP_JSON, failures)
    load_json(LEDGER_JSON, failures)
    blueprint_source = require_text(
        BLUEPRINT_GD,
        [
            "G19S_NEWPORT_RUNTIME_RECONSTRUCTION_PASS",
            "G19S_NEWPORT_RUNTIME_LAYOUT_SOURCE_PATH",
            "g19s_runtime_reconstruction_contract",
            "Vector2(390.0, 812.0)",
            "Vector2(1196.0, 812.0)",
        ],
        failures,
    )
    require_text(
        MAIN_GD,
        [
            "starter_village_first_session_readability_contract",
            "player_guidance_polish_contract",
            "first_session_gameplay_loop_reward_contract",
            "g19s_runtime_reconstruction_contract",
            "_set_debug_overlay(false)",
            "BUILD_INFO.DEBUG_OVERLAY_TOGGLE_ENABLED",
        ],
        failures,
    )
    map_layer_source = require_text(
        MAP_LAYER_GD,
        [
            "_draw_g19s_source_truth_street_plan",
            "_draw_g19s_source_truth_lots",
            "_draw_g19s_source_truth_wharf_water",
            "_draw_g19s_source_truth_props",
            "g19r_roof_station_repair_west_dockworker_on_landing_lip",
            "g19r_roof_station_repair_east_dockworker_on_front_landing",
            "Vector2(390, 812)",
            "Vector2(1196, 812)",
        ],
        failures,
    )
    require_text(
        CAPTURE_GD,
        [
            "g19r_01_village_wide_city_structure.png",
            "g19r_02_harborfront_avenue_width.png",
            "g19r_03_counting_house_civic_climb.png",
            "g19r_04_wharf_work_apron.png",
            "g19r_05_east_gate_settlement_edge.png",
            "hud_hidden_for_world_structure_review",
        ],
        failures,
    )
    require_text(CAPTURE_PS1, ["capture_g19r_runtime_screenshots.gd"], failures)
    require_text(
        ROADMAP_MD,
        [
            "G-19R",
            "road hierarchy",
            "waterfront avenue target 360 px",
            "Props are last",
            "Screenshot contradiction fails the phase",
        ],
        failures,
    )
    require_text(
        LEDGER_MD,
        [
            "G-19R",
            "Chris screenshot critique fails the current G-19 direction",
            "district structure",
            "avenue widths",
        ],
        failures,
    )
    if isinstance(source, dict):
        _validate_source(source, failures)
    _validate_no_false_g19_pass(failures)
    _validate_runtime_dock_npc_positions(blueprint_source, map_layer_source, failures)
    return print_result("newport harbor town reconstruction", failures)


if __name__ == "__main__":
    sys.exit(main())
