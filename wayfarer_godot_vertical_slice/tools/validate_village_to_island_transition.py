#!/usr/bin/env python3
"""Validate the G-15A village-to-island transition contract."""

from __future__ import annotations

import sys

from opening_village_island_validator_common import PROJECT_ROOT, REPO_ROOT, load_json, print_result, require_text, validate_phase_contract


TRANSITION_JSON = PROJECT_ROOT / "data" / "world_layout" / "village_to_island_transition_v1.json"
TOPOLOGY_JSON = PROJECT_ROOT / "data" / "world_layout" / "opening_island_world_topology_v1.json"
SCREENSHOT_MANIFEST = PROJECT_ROOT / "artifacts" / "review" / "g15a_runtime_screenshots" / "g15a_runtime_screenshot_manifest.json"
G15A_REPORT = REPO_ROOT / "docs" / "reports" / "G15A_VILLAGE_TO_ISLAND_TRANSITION_PASS.md"
G15A_REPORT_JSON = REPO_ROOT / "docs" / "reports" / "G15A_VILLAGE_TO_ISLAND_TRANSITION_PASS.json"
BLUEPRINT_GD = PROJECT_ROOT / "scripts" / "NewportTownBlueprint.gd"
MAIN_GD = PROJECT_ROOT / "scenes" / "Main.gd"
MAP_LAYER_GD = PROJECT_ROOT / "scenes" / "map" / "MapLayer.gd"
CAPTURE_GD = PROJECT_ROOT / "tools" / "capture_g15a_runtime_screenshots.gd"
CAPTURE_PS1 = PROJECT_ROOT / "tools" / "capture_g15a_runtime_screenshots.ps1"

REQUIRED_SCREENSHOTS = [
    "g15a_01_village_exit_to_island.png",
    "g15a_02_island_entry_transition.png",
    "g15a_03_first_mystery_beyond_town.png",
    "g15a_04_debug_overlays_disabled.png",
]


def main() -> int:
    failures: list[str] = []
    validate_phase_contract("G-15A", failures)
    transition = load_json(TRANSITION_JSON, failures)
    topology = load_json(TOPOLOGY_JSON, failures)
    report_json = load_json(G15A_REPORT_JSON, failures)
    manifest = load_json(SCREENSHOT_MANIFEST, failures)
    require_text(
        G15A_REPORT,
        [
            "G-15A Village-to-Island Transition Pass",
            "Clear town exit",
            "First sense of mystery",
            "COUNCIL_PASS_READY_FOR_PR",
            "Next phase: G-15B Island Terrain, Ground, and Route Cohesion",
        ],
        failures,
    )
    require_text(
        BLUEPRINT_GD,
        [
            "G15A_VILLAGE_TO_ISLAND_TRANSITION_PASS",
            "opening_island_transition_contract",
            "opening_island_transition_route_rects",
            "village_exit_to_island",
            "first_mystery_beyond_town",
        ],
        failures,
    )
    require_text(MAIN_GD, ["opening_island_transition_contract"], failures)
    require_text(
        MAP_LAYER_GD,
        [
            "_draw_g15a_transition_ground",
            "_draw_g15a_transition_streets",
            "_draw_g15a_transition_props",
            "atelier_wayfinding_coastal_waystone_01",
            "g15a_fence_break_threshold",
        ],
        failures,
    )
    require_text(CAPTURE_GD, REQUIRED_SCREENSHOTS, failures)
    require_text(CAPTURE_PS1, ["capture_g15a_runtime_screenshots.gd"], failures)
    if isinstance(transition, dict):
        validate_transition_json(transition, failures)
    if isinstance(topology, dict):
        implementation = topology.get("g15a_transition_implementation", {})
        if not isinstance(implementation, dict) or implementation.get("status") != "PASS":
            failures.append("topology missing PASS g15a_transition_implementation")
    if isinstance(report_json, dict):
        if report_json.get("status") != "PASS":
            failures.append("G-15A report JSON status must be PASS")
        if float(report_json.get("world_layout_score", 0.0)) < 8.5:
            failures.append("G-15A world_layout_score must be at least 8.5")
        if report_json.get("screenshot_manifest") != "wayfarer_godot_vertical_slice/artifacts/review/g15a_runtime_screenshots/g15a_runtime_screenshot_manifest.json":
            failures.append("G-15A report JSON screenshot manifest mismatch")
    if isinstance(manifest, dict):
        validate_manifest(manifest, failures)
    return print_result("village to island transition", failures)


def validate_transition_json(data: dict, failures: list[str]) -> None:
    if data.get("schema_id") != "wayfarer.g15a.village_to_island_transition.v1":
        failures.append("G-15A transition schema mismatch")
    if data.get("phase") != "G-15A":
        failures.append("G-15A transition phase mismatch")
    if data.get("topology_source") != "wayfarer_godot_vertical_slice/data/world_layout/opening_island_world_topology_v1.json":
        failures.append("G-15A transition topology source mismatch")
    world_size = data.get("world_size", {})
    if not isinstance(world_size, dict) or int(world_size.get("w", 0)) < 2400 or int(world_size.get("h", 0)) < 1600:
        failures.append("G-15A transition world_size must be at least 2400x1600")
    route = data.get("transition_route", {})
    if not isinstance(route, dict):
        failures.append("G-15A transition missing transition_route")
        return
    if len(route.get("route_rects", [])) < 5:
        failures.append("G-15A transition must define at least five route rects")
    samples = {
        str(sample.get("id", ""))
        for sample in route.get("walkable_samples", [])
        if isinstance(sample, dict)
    }
    for sample_id in ["village_exit_to_island", "island_entry_transition", "first_mystery_beyond_town"]:
        if sample_id not in samples:
            failures.append(f"G-15A transition missing walkable sample: {sample_id}")
    acceptance = data.get("acceptance", {})
    for flag in [
        "player_knows_where_to_go_next",
        "transition_feels_natural",
        "world_opens_without_confusion",
        "no_invisible_wall_or_random_edge_feeling",
    ]:
        if not isinstance(acceptance, dict) or acceptance.get(flag) is not True:
            failures.append(f"G-15A acceptance missing true flag: {flag}")
    if float(acceptance.get("world_layout_score", 0.0)) < 8.5:
        failures.append("G-15A acceptance world_layout_score must be at least 8.5")


def validate_manifest(manifest: dict, failures: list[str]) -> None:
    if manifest.get("phase") != "G-15A":
        failures.append("G-15A screenshot manifest phase mismatch")
    if manifest.get("status") != "PASS":
        failures.append("G-15A screenshot manifest status must be PASS")
    if manifest.get("no_hud_capture") is not True:
        failures.append("G-15A screenshot manifest must record no_hud_capture=true")
    if manifest.get("debug_overlays_disabled") is not True:
        failures.append("G-15A screenshot manifest must record debug_overlays_disabled=true")
    filenames = {
        str(item.get("filename", ""))
        for item in manifest.get("screenshots", [])
        if isinstance(item, dict)
    }
    for filename in REQUIRED_SCREENSHOTS:
        if filename not in filenames:
            failures.append(f"G-15A screenshot manifest missing {filename}")
    transition_contract = manifest.get("opening_island_transition_contract", {})
    if not isinstance(transition_contract, dict) or transition_contract.get("phase") != "G-15A":
        failures.append("G-15A screenshot manifest missing transition contract")
    for item in manifest.get("screenshots", []):
        if isinstance(item, dict) and item.get("status") != "PASS":
            failures.append(f"G-15A screenshot did not PASS: {item.get('filename', '<unknown>')}")


if __name__ == "__main__":
    sys.exit(main())
