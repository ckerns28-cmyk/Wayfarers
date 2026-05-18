#!/usr/bin/env python3
"""Validate the G-15B island terrain/route cohesion contract."""

from __future__ import annotations

import sys

from opening_village_island_validator_common import PROJECT_ROOT, REPO_ROOT, load_json, print_result, require_text, validate_phase_contract


COHESION_JSON = PROJECT_ROOT / "data" / "world_layout" / "island_world_cohesion_v1.json"
TOPOLOGY_JSON = PROJECT_ROOT / "data" / "world_layout" / "opening_island_world_topology_v1.json"
SCREENSHOT_MANIFEST = PROJECT_ROOT / "artifacts" / "review" / "g15b_runtime_screenshots" / "g15b_runtime_screenshot_manifest.json"
G15B_REPORT = REPO_ROOT / "docs" / "reports" / "G15B_ISLAND_TERRAIN_GROUND_ROUTE_COHESION.md"
G15B_REPORT_JSON = REPO_ROOT / "docs" / "reports" / "G15B_ISLAND_TERRAIN_GROUND_ROUTE_COHESION.json"
BLUEPRINT_GD = PROJECT_ROOT / "scripts" / "NewportTownBlueprint.gd"
MAIN_GD = PROJECT_ROOT / "scenes" / "Main.gd"
MAP_LAYER_GD = PROJECT_ROOT / "scenes" / "map" / "MapLayer.gd"
CAPTURE_GD = PROJECT_ROOT / "tools" / "capture_g15b_runtime_screenshots.gd"
CAPTURE_PS1 = PROJECT_ROOT / "tools" / "capture_g15b_runtime_screenshots.ps1"

REQUIRED_SCREENSHOTS = [
    "g15b_01_island_wide_cohesion.png",
    "g15b_02_main_trail_ground_transition.png",
    "g15b_03_coastline_route_cohesion.png",
    "g15b_04_route_loop_return_path.png",
    "g15b_05_debug_overlays_disabled.png",
]


def main() -> int:
    failures: list[str] = []
    validate_phase_contract("G-15B", failures)
    cohesion = load_json(COHESION_JSON, failures)
    topology = load_json(TOPOLOGY_JSON, failures)
    report_json = load_json(G15B_REPORT_JSON, failures)
    manifest = load_json(SCREENSHOT_MANIFEST, failures)
    require_text(
        G15B_REPORT,
        [
            "G-15B Island Terrain, Ground, and Route Cohesion",
            "No patchwork terrain",
            "Routes lead somewhere",
            "COUNCIL_PASS_READY_FOR_PR",
            "Next phase: G-16 Island Landmark and Point-of-Interest Pass",
        ],
        failures,
    )
    require_text(
        BLUEPRINT_GD,
        [
            "G15B_ISLAND_WORLD_COHESION_PASS",
            "opening_island_world_cohesion_contract",
            "opening_island_world_cohesion_route_rects",
            "g15b_cove_edge_path",
            "g15b_return_lane",
        ],
        failures,
    )
    require_text(MAIN_GD, ["opening_island_world_cohesion_contract"], failures)
    require_text(
        MAP_LAYER_GD,
        [
            "_draw_g15b_island_world_ground",
            "_draw_g15b_island_world_routes",
            "_draw_g15b_island_world_props",
            "_draw_g15b_island_shoreline_water",
            "g15b_coastline_shoreline_treatment",
        ],
        failures,
    )
    require_text(CAPTURE_GD, REQUIRED_SCREENSHOTS, failures)
    require_text(CAPTURE_PS1, ["capture_g15b_runtime_screenshots.gd"], failures)
    if isinstance(cohesion, dict):
        validate_cohesion_json(cohesion, failures)
    if isinstance(topology, dict):
        implementation = topology.get("g15b_world_cohesion_implementation", {})
        if not isinstance(implementation, dict) or implementation.get("status") != "PASS":
            failures.append("topology missing PASS g15b_world_cohesion_implementation")
    if isinstance(report_json, dict):
        if report_json.get("status") != "PASS":
            failures.append("G-15B report JSON status must be PASS")
        if float(report_json.get("world_layout_score", 0.0)) < 8.5:
            failures.append("G-15B world_layout_score must be at least 8.5")
        if report_json.get("screenshot_manifest") != "wayfarer_godot_vertical_slice/artifacts/review/g15b_runtime_screenshots/g15b_runtime_screenshot_manifest.json":
            failures.append("G-15B report JSON screenshot manifest mismatch")
    if isinstance(manifest, dict):
        validate_manifest(manifest, failures)
    return print_result("island world cohesion", failures)


def validate_cohesion_json(data: dict, failures: list[str]) -> None:
    if data.get("schema_id") != "wayfarer.g15b.island_world_cohesion.v1":
        failures.append("G-15B cohesion schema mismatch")
    if data.get("phase") != "G-15B":
        failures.append("G-15B cohesion phase mismatch")
    if data.get("topology_source") != "wayfarer_godot_vertical_slice/data/world_layout/opening_island_world_topology_v1.json":
        failures.append("G-15B topology source mismatch")
    if data.get("transition_source") != "wayfarer_godot_vertical_slice/data/world_layout/village_to_island_transition_v1.json":
        failures.append("G-15B transition source mismatch")
    zones = data.get("terrain_zones", [])
    if not isinstance(zones, list) or len(zones) < 6:
        failures.append("G-15B must define at least six terrain zones")
    if len(data.get("route_rects", [])) < 7:
        failures.append("G-15B must define at least seven route rects")
    samples = {
        str(sample.get("id", ""))
        for sample in data.get("walkable_samples", [])
        if isinstance(sample, dict)
    }
    for sample_id in ["pasture_crossing", "wooded_switchback", "signal_rise_route", "cove_edge_path", "return_lane"]:
        if sample_id not in samples:
            failures.append(f"G-15B missing walkable sample: {sample_id}")
    blocked = data.get("blocked_space_samples", [])
    if not isinstance(blocked, list) or len(blocked) < 3:
        failures.append("G-15B must define at least three blocked-space samples")
    loop = data.get("route_loop", [])
    if not isinstance(loop, list) or "newport_east_gate" not in loop or "return_lane" not in loop:
        failures.append("G-15B route_loop must connect Newport and return_lane")
    acceptance = data.get("acceptance", {})
    for flag in [
        "wide_screenshots_read_as_cohesive_island",
        "gameplay_zoom_reads_cleanly",
        "routes_lead_somewhere",
        "no_patchwork_terrain",
        "clear_walkable_space",
        "clear_blocked_space",
        "route_loops",
        "coastline_shoreline_treatment",
    ]:
        if not isinstance(acceptance, dict) or acceptance.get(flag) is not True:
            failures.append(f"G-15B acceptance missing true flag: {flag}")
    if float(acceptance.get("terrain_world_cohesion_score", 0.0)) < 8.5:
        failures.append("G-15B terrain_world_cohesion_score must be at least 8.5")


def validate_manifest(manifest: dict, failures: list[str]) -> None:
    if manifest.get("phase") != "G-15B":
        failures.append("G-15B screenshot manifest phase mismatch")
    if manifest.get("status") != "PASS":
        failures.append("G-15B screenshot manifest status must be PASS")
    if manifest.get("no_hud_capture") is not True:
        failures.append("G-15B screenshot manifest must record no_hud_capture=true")
    if manifest.get("debug_overlays_disabled") is not True:
        failures.append("G-15B screenshot manifest must record debug_overlays_disabled=true")
    filenames = {
        str(item.get("filename", ""))
        for item in manifest.get("screenshots", [])
        if isinstance(item, dict)
    }
    for filename in REQUIRED_SCREENSHOTS:
        if filename not in filenames:
            failures.append(f"G-15B screenshot manifest missing {filename}")
    cohesion_contract = manifest.get("opening_island_world_cohesion_contract", {})
    if not isinstance(cohesion_contract, dict) or cohesion_contract.get("phase") != "G-15B":
        failures.append("G-15B screenshot manifest missing cohesion contract")
    for item in manifest.get("screenshots", []):
        if isinstance(item, dict) and item.get("status") != "PASS":
            failures.append(f"G-15B screenshot did not PASS: {item.get('filename', '<unknown>')}")


if __name__ == "__main__":
    sys.exit(main())
