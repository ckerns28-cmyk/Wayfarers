#!/usr/bin/env python3
"""Validate OVI-2 Newport origin immersion and city-planning gate."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from opening_village_island_validator_common import (
    PROJECT_ROOT,
    REPO_ROOT,
    load_json,
    print_result,
    repo_path,
    require_text,
    validate_phase_contract,
)


BLUEPRINT = PROJECT_ROOT / "scripts" / "NewportTownBlueprint.gd"
MAIN_GD = PROJECT_ROOT / "scenes" / "Main.gd"
MAP_LAYER = PROJECT_ROOT / "scenes" / "map" / "MapLayer.gd"
SOURCE_JSON = PROJECT_ROOT / "data" / "world_layout" / "ovi2_newport_origin_immersion_city_plan_v1.json"
CAPTURE_GD = PROJECT_ROOT / "tools" / "capture_ovi2_runtime_screenshots.gd"
CAPTURE_PS1 = PROJECT_ROOT / "tools" / "capture_ovi2_runtime_screenshots.ps1"
SCREENSHOT_DIR = PROJECT_ROOT / "artifacts" / "review" / "ovi2_newport_origin_immersion"
SCREENSHOT_MANIFEST = SCREENSHOT_DIR / "ovi2_newport_origin_immersion_screenshot_manifest.json"
REPORT_MD = REPO_ROOT / "docs" / "reports" / "OVI2_NEWPORT_ORIGIN_IMMERSION_CITY_PLANNING_GATE.md"
COUNCIL_REPORT_MD = REPO_ROOT / "docs" / "reports" / "OVI2_NEWPORT_ORIGIN_IMMERSION_AGENT_COUNCIL_REPORT.md"

REQUIRED_SCREENSHOTS = [
    "ovi2_01_player_spawn_first_impression_hud.png",
    "ovi2_02_player_spawn_first_impression_no_hud.png",
    "ovi2_03_harborfront_avenue.png",
    "ovi2_04_tavern_inn_district.png",
    "ovi2_05_counting_house_civic_district.png",
    "ovi2_06_shopfront_commercial_street.png",
    "ovi2_07_wharf_dock_service_district.png",
    "ovi2_08_wide_town_composition.png",
    "ovi2_09_movement_route_through_town.png",
    "ovi2_10_before_after_reference_current_failure.png",
]

REQUIRED_CRITERIA = [
    "no_visible_debug_overlays_in_production_screenshots",
    "No oversized translucent road/region rectangles dominating the play area",
    "road_avenue_continuity",
    "building_to_street_frontage_alignment",
    "building_spacing_gap_sanity",
    "prop_density_in_large_negative_spaces",
    "no_huge_undecorated_rectangles_in_core_starting_view",
    "tavern_inn_integrated_into_main_town_structure",
    "civic_counting_house_district_integrated_into_road_plan",
    "harbor_wharf_identity_visible_in_harborfront_screenshots",
    "NPCs placed only on believable walkable/station surfaces",
    "player_movement_lanes_preserved",
    "z_order_and_occlusion_preserved",
    "representative_human_review_angles_captured",
]

FORBIDDEN_ACTIVE_TOKENS = [
    "_draw_newport_commercial_street(Rect2(260, 542, 1525, 326)",
    "_draw_newport_commercial_street(Rect2(220, 774, 1590, 272)",
    "_draw_newport_commercial_street(Rect2(260, 285, 1440, 150)",
    "_draw_newport_commercial_street(Rect2(958, 325, 204, 550)",
    "_draw_newport_commercial_street(Rect2(422, 335, 177, 535)",
    "_draw_newport_commercial_street(Rect2(1478, 360, 164, 530)",
    "draw_rect(Rect2(70, 170, 1468, 574)",
]


def main() -> int:
    failures: list[str] = []

    source = load_json(SOURCE_JSON, failures)
    if isinstance(source, dict):
        _validate_source_json(source, failures)

    blueprint = require_text(
        BLUEPRINT,
        [
            "OVI2_NEWPORT_ORIGIN_IMMERSION_PASS",
            "OVI2_NEWPORT_ORIGIN_IMMERSION_SOURCE_PATH",
            "ovi2_newport_origin_immersion_contract",
            "not_outward_gameplay_expansion",
            "No oversized translucent road/region rectangles",
            "representative_human_review_angles_captured",
        ],
        failures,
    )
    require_text(
        MAIN_GD,
        [
            "ovi2_newport_origin_immersion_contract",
            "NEWPORT_TOWN.ovi2_newport_origin_immersion_contract",
        ],
        failures,
    )
    map_layer = require_text(
        MAP_LAYER,
        [
            "_draw_ovi2_origin_ground_foundation",
            "_draw_ovi2_source_truth_lots",
            "_draw_ovi2_harborfront_avenue_segments",
            "_draw_ovi2_civic_counting_house_terrace",
            "_draw_ovi2_rear_service_lane_network",
            "_draw_ovi2_wharf_work_apron",
            "_draw_ovi2_route_curbs_and_edges",
            "_draw_ovi2_origin_district_props",
            "no_oversized_translucent_road_rectangles",
            "ovi2_tavern_inn_centerpiece_warm_entry",
            "ovi2_counting_house_notice_board_first_objective_anchor",
            "ovi2_west_wharf_manifest_cargo_stack",
        ],
        failures,
    )
    for token in FORBIDDEN_ACTIVE_TOKENS:
        if token in map_layer:
            failures.append(f"OVI-2 forbidden old slab renderer token still active: {token}")

    require_text(
        CAPTURE_GD,
        [
            "wayfarer.ovi2.newport_origin_immersion_screenshot_manifest.v1",
            "ovi2_01_player_spawn_first_impression_hud.png",
            "ovi2_10_before_after_reference_current_failure.png",
            "representative_human_review_angles",
            "not_outward_gameplay_expansion",
        ],
        failures,
    )
    require_text(
        CAPTURE_PS1,
        [
            "capture_ovi2_runtime_screenshots.gd",
            "1600x1000",
            "windows",
        ],
        failures,
    )

    _validate_screenshot_manifest(failures)
    _validate_reports(failures)
    validate_phase_contract("OVI-2", failures)

    if "origin-to-field gameplay loop" in blueprint:
        failures.append("OVI-2 implementation must not steer into an origin-to-field gameplay loop")

    return print_result("OVI-2 Newport origin immersion", failures)


def _validate_source_json(source: dict[str, Any], failures: list[str]) -> None:
    if source.get("schema_id") != "wayfarer.ovi2.newport_origin_immersion_city_plan.v1":
        failures.append("OVI-2 source schema_id mismatch")
    if source.get("phase_id") != "OVI-2":
        failures.append("OVI-2 source phase_id mismatch")
    if source.get("baseline_commit") != "e36949f3fa824ebee178f048a59f8f1778483c2f":
        failures.append("OVI-2 source baseline commit mismatch")
    scope = source.get("scope_ruling", {})
    if not isinstance(scope, dict) or scope.get("not_outward_gameplay_expansion") is not True:
        failures.append("OVI-2 source must explicitly block outward gameplay expansion")
    if not isinstance(scope, dict) or scope.get("no_combat") is not True:
        failures.append("OVI-2 source must explicitly block combat scope")
    scores = source.get("target_scores", {})
    if not isinstance(scores, dict) or float(scores.get("visual_art_direction", 0.0)) < 8.5:
        failures.append("OVI-2 source must preserve the 8.5 visual/art target")
    diagnosis = source.get("forensic_diagnosis", {})
    if not isinstance(diagnosis, dict):
        failures.append("OVI-2 source missing forensic_diagnosis object")
    else:
        for key in [
            "why_current_screen_reads_artificial",
            "giant_slab_flat_plane_source",
            "rectangle_classification",
            "building_integration_failure",
            "design_rule_fix",
        ]:
            if not str(diagnosis.get(key, "")).strip():
                failures.append(f"OVI-2 forensic diagnosis missing {key}")
        if "not debug overlays" not in str(diagnosis.get("rectangle_classification", "")).lower():
            failures.append("OVI-2 diagnosis must classify rectangles as not debug overlays")
    criteria = source.get("measurable_design_rules", [])
    if not isinstance(criteria, list):
        failures.append("OVI-2 source measurable_design_rules must be a list")
    else:
        for criterion in REQUIRED_CRITERIA:
            if criterion not in criteria:
                failures.append(f"OVI-2 source missing measurable criterion: {criterion}")
    screenshots = source.get("screenshot_package", [])
    if not isinstance(screenshots, list):
        failures.append("OVI-2 source screenshot_package must be a list")
    else:
        filenames = {str(item.get("filename", "")) for item in screenshots if isinstance(item, dict)}
        for filename in REQUIRED_SCREENSHOTS:
            if filename not in filenames:
                failures.append(f"OVI-2 source missing screenshot requirement: {filename}")
    baseline = repo_path(str(source.get("baseline_reference", "")))
    if not baseline.exists():
        failures.append(f"OVI-2 baseline reference screenshot missing: {baseline}")


def _validate_screenshot_manifest(failures: list[str]) -> None:
    manifest = load_json(SCREENSHOT_MANIFEST, failures)
    if not isinstance(manifest, dict):
        return
    if manifest.get("schema_id") != "wayfarer.ovi2.newport_origin_immersion_screenshot_manifest.v1":
        failures.append("OVI-2 screenshot manifest schema_id mismatch")
    if manifest.get("phase") != "OVI-2":
        failures.append("OVI-2 screenshot manifest phase mismatch")
    if manifest.get("status") != "PASS":
        failures.append("OVI-2 screenshot manifest must be PASS")
    if manifest.get("debug_overlays_disabled") is not True:
        failures.append("OVI-2 screenshot manifest must record debug overlays disabled")
    if manifest.get("representative_human_review_angles") is not True:
        failures.append("OVI-2 screenshot manifest must record representative human review angles")
    if manifest.get("not_outward_gameplay_expansion") is not True:
        failures.append("OVI-2 screenshot manifest must record not outward gameplay expansion")
    shots = manifest.get("screenshots", [])
    if not isinstance(shots, list):
        failures.append("OVI-2 screenshot manifest screenshots must be a list")
        return
    if len(shots) < len(REQUIRED_SCREENSHOTS):
        failures.append("OVI-2 screenshot manifest missing required screenshot count")
    by_filename = {str(shot.get("filename", "")): shot for shot in shots if isinstance(shot, dict)}
    for filename in REQUIRED_SCREENSHOTS:
        shot = by_filename.get(filename)
        if not isinstance(shot, dict):
            failures.append(f"OVI-2 screenshot missing from manifest: {filename}")
            continue
        if shot.get("status") != "PASS":
            failures.append(f"OVI-2 screenshot not PASS: {filename}")
        raw_path = str(shot.get("path", ""))
        path = repo_path(raw_path)
        if not path.exists():
            failures.append(f"OVI-2 screenshot path missing: {raw_path}")
            continue
        width, height = _png_size(path, failures)
        if width < 1200 or height < 800:
            failures.append(f"OVI-2 screenshot too small: {filename} {width}x{height}")
    if by_filename.get("ovi2_01_player_spawn_first_impression_hud.png", {}).get("hide_hud") is not False:
        failures.append("OVI-2 first spawn HUD screenshot must keep HUD visible")
    if by_filename.get("ovi2_02_player_spawn_first_impression_no_hud.png", {}).get("hide_hud") is not True:
        failures.append("OVI-2 no-HUD spawn screenshot must hide HUD")


def _validate_reports(failures: list[str]) -> None:
    report_text = require_text(
        REPORT_MD,
        [
            "OVI-2 Newport Origin Village Immersion & City-Planning Gate",
            "Human Screenshot Failure Summary",
            "Forensic Diagnosis",
            "not debug overlays",
            "not outward gameplay expansion",
            "Screenshot Artifact Paths",
            "Validation Table",
            "Agent Council Verdict",
        ],
        failures,
    )
    council_text = require_text(
        COUNCIL_REPORT_MD,
        [
            "Scrum Master",
            "Game Director",
            "World Designer",
            "City Planner",
            "Art Director",
            "Gameplay Designer",
            "Narrative Designer",
            "UX Designer",
            "Godot Engineer",
            "QA Lead",
            "Release Manager",
            "COUNCIL_PASS_READY_FOR_PR",
        ],
        failures,
    )
    for filename in REQUIRED_SCREENSHOTS:
        if filename not in report_text:
            failures.append(f"OVI-2 report missing screenshot path token: {filename}")
    if "COUNCIL_CONDITIONAL_PASS_WITH_LIMITATIONS" in council_text or "COUNCIL_FAIL_REQUIRES_REVISION" in council_text:
        failures.append("OVI-2 final council report must not include a weaker final verdict when ledger row is PASS")


def _png_size(path: Path, failures: list[str]) -> tuple[int, int]:
    try:
        header = path.read_bytes()[:24]
    except OSError as exc:
        failures.append(f"could not read PNG {path}: {exc}")
        return 0, 0
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        failures.append(f"not a PNG file: {path}")
        return 0, 0
    return int.from_bytes(header[16:20], "big"), int.from_bytes(header[20:24], "big")


if __name__ == "__main__":
    sys.exit(main())
