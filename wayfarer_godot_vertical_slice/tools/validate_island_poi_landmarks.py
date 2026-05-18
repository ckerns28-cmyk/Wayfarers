#!/usr/bin/env python3
"""Validate the G-16 island POI/landmark contract."""

from __future__ import annotations

import sys

from opening_village_island_validator_common import PROJECT_ROOT, REPO_ROOT, load_json, print_result, require_text, validate_phase_contract


POI_JSON = PROJECT_ROOT / "data" / "world_layout" / "island_poi_landmarks_v1.json"
TOPOLOGY_JSON = PROJECT_ROOT / "data" / "world_layout" / "opening_island_world_topology_v1.json"
SCREENSHOT_MANIFEST = PROJECT_ROOT / "artifacts" / "review" / "g16_runtime_screenshots" / "g16_runtime_screenshot_manifest.json"
G16_REPORT = REPO_ROOT / "docs" / "reports" / "G16_ISLAND_LANDMARK_POI_PASS.md"
G16_REPORT_JSON = REPO_ROOT / "docs" / "reports" / "G16_ISLAND_LANDMARK_POI_PASS.json"
BLUEPRINT_GD = PROJECT_ROOT / "scripts" / "NewportTownBlueprint.gd"
MAIN_GD = PROJECT_ROOT / "scenes" / "Main.gd"
MAP_LAYER_GD = PROJECT_ROOT / "scenes" / "map" / "MapLayer.gd"
CAPTURE_GD = PROJECT_ROOT / "tools" / "capture_g16_runtime_screenshots.gd"
CAPTURE_PS1 = PROJECT_ROOT / "tools" / "capture_g16_runtime_screenshots.ps1"

REQUIRED_POIS = [
    "signal_overlook",
    "old_road_marker",
    "cove_hidden_landing",
    "wooded_grove_path",
    "farm_service_outbuilding",
    "quest_clue_site",
    "optional_secret_cache",
    "return_landmark",
]

REQUIRED_SCREENSHOTS = [
    "g16_01_signal_overlook_landmark.png",
    "g16_02_old_road_marker_and_grove.png",
    "g16_03_cove_hidden_landing.png",
    "g16_04_farm_service_edge_settlement.png",
    "g16_05_quest_clue_optional_secret.png",
    "g16_06_return_landmark_debug_disabled.png",
]


def main() -> int:
    failures: list[str] = []
    validate_phase_contract("G-16", failures)
    poi = load_json(POI_JSON, failures)
    topology = load_json(TOPOLOGY_JSON, failures)
    report_json = load_json(G16_REPORT_JSON, failures)
    manifest = load_json(SCREENSHOT_MANIFEST, failures)
    require_text(
        G16_REPORT,
        [
            "G-16 Island Landmark and Point-of-Interest Pass",
            "Optional secret location",
            "Return landmark",
            "COUNCIL_PASS_READY_FOR_PR",
            "Next phase: G-16A Island Atelier Asset Family Pass",
        ],
        failures,
    )
    require_text(
        BLUEPRINT_GD,
        [
            "G16_ISLAND_POI_LANDMARKS_PASS",
            "opening_island_poi_landmarks_contract",
            "opening_island_poi_landmark_specs",
            "optional_secret_cache",
            "return_landmark",
        ],
        failures,
    )
    require_text(MAIN_GD, ["opening_island_poi_landmarks_contract"], failures)
    require_text(
        MAP_LAYER_GD,
        [
            "_draw_g16_island_poi_landmarks",
            "g16_signal_overlook_lantern_destination",
            "g16_cove_hidden_landing_wharf_remnant",
            "g16_quest_clue_site_physical_evidence",
            "g16_optional_secret_cache_off_route_discovery",
        ],
        failures,
    )
    require_text(CAPTURE_GD, REQUIRED_SCREENSHOTS, failures)
    require_text(CAPTURE_PS1, ["capture_g16_runtime_screenshots.gd"], failures)
    if isinstance(poi, dict):
        validate_poi_json(poi, failures)
    if isinstance(topology, dict):
        implementation = topology.get("g16_poi_landmarks_implementation", {})
        if not isinstance(implementation, dict) or implementation.get("status") != "PASS":
            failures.append("topology missing PASS g16_poi_landmarks_implementation")
    if isinstance(report_json, dict):
        if report_json.get("status") != "PASS":
            failures.append("G-16 report JSON status must be PASS")
        if float(report_json.get("art_world_score", 0.0)) < 8.5:
            failures.append("G-16 art_world_score must be at least 8.5")
        if report_json.get("screenshot_manifest") != "wayfarer_godot_vertical_slice/artifacts/review/g16_runtime_screenshots/g16_runtime_screenshot_manifest.json":
            failures.append("G-16 report JSON screenshot manifest mismatch")
    if isinstance(manifest, dict):
        validate_manifest(manifest, failures)
    return print_result("island poi landmarks", failures)


def validate_poi_json(data: dict, failures: list[str]) -> None:
    if data.get("schema_id") != "wayfarer.g16.island_poi_landmarks.v1":
        failures.append("G-16 POI schema mismatch")
    if data.get("phase") != "G-16":
        failures.append("G-16 POI phase mismatch")
    required = set(str(item) for item in data.get("required_poi_ids", []))
    for poi_id in REQUIRED_POIS:
        if poi_id not in required:
            failures.append(f"G-16 required_poi_ids missing {poi_id}")
    points = {
        str(point.get("id", "")): point
        for point in data.get("points_of_interest", [])
        if isinstance(point, dict)
    }
    for poi_id in REQUIRED_POIS:
        point = points.get(poi_id)
        if not isinstance(point, dict):
            failures.append(f"G-16 missing point_of_interest: {poi_id}")
            continue
        if point.get("recognizable_destination") is not True:
            failures.append(f"G-16 POI must be recognizable: {poi_id}")
        if not str(point.get("exploration_purpose", "")).strip():
            failures.append(f"G-16 POI missing exploration purpose: {poi_id}")
        if not str(point.get("quest_purpose", "")).strip():
            failures.append(f"G-16 POI missing quest purpose: {poi_id}")
    if points.get("optional_secret_cache", {}).get("optional_discovery") is not True:
        failures.append("G-16 optional_secret_cache must be marked optional_discovery=true")
    acceptance = data.get("acceptance", {})
    for flag in [
        "player_can_name_or_recognize_destinations",
        "each_poi_supports_exploration_or_quest_purpose",
        "pois_are_not_random_props",
        "at_least_one_optional_discovery_exists",
        "return_landmark_visible_from_multiple_routes",
    ]:
        if not isinstance(acceptance, dict) or acceptance.get(flag) is not True:
            failures.append(f"G-16 acceptance missing true flag: {flag}")
    if float(acceptance.get("art_world_score", 0.0)) < 8.5:
        failures.append("G-16 art_world_score must be at least 8.5")


def validate_manifest(manifest: dict, failures: list[str]) -> None:
    if manifest.get("phase") != "G-16":
        failures.append("G-16 screenshot manifest phase mismatch")
    if manifest.get("status") != "PASS":
        failures.append("G-16 screenshot manifest status must be PASS")
    if manifest.get("no_hud_capture") is not True:
        failures.append("G-16 screenshot manifest must record no_hud_capture=true")
    if manifest.get("debug_overlays_disabled") is not True:
        failures.append("G-16 screenshot manifest must record debug_overlays_disabled=true")
    filenames = {
        str(item.get("filename", ""))
        for item in manifest.get("screenshots", [])
        if isinstance(item, dict)
    }
    for filename in REQUIRED_SCREENSHOTS:
        if filename not in filenames:
            failures.append(f"G-16 screenshot manifest missing {filename}")
    contract = manifest.get("opening_island_poi_landmarks_contract", {})
    if not isinstance(contract, dict) or contract.get("phase") != "G-16":
        failures.append("G-16 screenshot manifest missing POI contract")
    for item in manifest.get("screenshots", []):
        if isinstance(item, dict) and item.get("status") != "PASS":
            failures.append(f"G-16 screenshot did not PASS: {item.get('filename', '<unknown>')}")


if __name__ == "__main__":
    sys.exit(main())
