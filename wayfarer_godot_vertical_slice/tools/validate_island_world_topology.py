#!/usr/bin/env python3
"""Validate the G-15 island masterplan/topology contract."""

from __future__ import annotations

import sys

from opening_village_island_validator_common import PROJECT_ROOT, REPO_ROOT, load_json, print_result, require_text, validate_phase_contract


TOPOLOGY_JSON = PROJECT_ROOT / "data" / "world_layout" / "opening_island_world_topology_v1.json"
VIEWPOINT_MANIFEST_JSON = (
    PROJECT_ROOT
    / "data"
    / "visual_qa"
    / "g15_topology_screenshot_viewpoint_manifest.json"
)
G15_REPORT = REPO_ROOT / "docs" / "reports" / "G15_OPENING_ISLAND_MASTERPLAN_WORLD_TOPOLOGY.md"
G15_REPORT_JSON = REPO_ROOT / "docs" / "reports" / "G15_OPENING_ISLAND_MASTERPLAN_WORLD_TOPOLOGY.json"

REQUIRED_STRUCTURE = [
    "safe_village_core",
    "harbor_edge",
    "outskirts",
    "farms_pastures_service_lands",
    "wooded_paths",
    "rocky_coast_cove",
    "old_road_signal_point_ruin_lookout",
    "quest_destination",
    "optional_secret",
    "return_path",
]

REQUIRED_ZONES = [
    "newport_east_gate",
    "outskirt_lane",
    "pasture_crossing",
    "wooded_switchback",
    "signal_rise",
    "old_road_marker",
    "cove_descent",
    "hidden_landing",
    "quest_clue_site",
    "optional_secret_cache",
    "return_lane",
]

REQUIRED_ROUTES = [
    "village_to_signal_route",
    "signal_to_clue_route",
    "cove_loop_route",
    "return_to_newport_route",
]

REQUIRED_VIEWPOINTS = [
    "07_village_exit_to_island",
    "08_island_entry_transition",
    "09_island_main_trail",
    "10_island_landmark_signal_or_overlook",
    "11_island_cove_or_hidden_landing",
    "12_island_optional_discovery",
    "17_return_to_town_or_next_hook",
]


def main() -> int:
    failures: list[str] = []
    validate_phase_contract("G-15", failures)
    topology = load_json(TOPOLOGY_JSON, failures)
    require_text(
        G15_REPORT,
        [
            "G-15 Opening Island Masterplan + World Topology",
            "Authoritative source",
            "Screenshot viewpoint manifest",
            "No patchwork terrain",
            "COUNCIL_PASS_READY_FOR_PR",
            "Next phase: G-15A Village-to-Island Transition Pass",
        ],
        failures,
    )
    report_json = load_json(G15_REPORT_JSON, failures)
    if isinstance(report_json, dict):
        if report_json.get("status") != "PASS":
            failures.append("G-15 report JSON status must be PASS")
        if report_json.get("topology_source") != "wayfarer_godot_vertical_slice/data/world_layout/opening_island_world_topology_v1.json":
            failures.append("G-15 report JSON topology source mismatch")
        if (
            report_json.get("screenshot_viewpoint_manifest")
            != "wayfarer_godot_vertical_slice/data/visual_qa/g15_topology_screenshot_viewpoint_manifest.json"
        ):
            failures.append("G-15 report JSON screenshot viewpoint manifest mismatch")
        if float(report_json.get("world_layout_score", 0.0)) < 8.5:
            failures.append("G-15 world_layout_score must be at least 8.5")
    viewpoint_manifest = load_json(VIEWPOINT_MANIFEST_JSON, failures)
    if isinstance(topology, dict):
        validate_topology(topology, failures)
        if isinstance(viewpoint_manifest, dict):
            validate_viewpoint_manifest(topology, viewpoint_manifest, failures)
    return print_result("island world topology", failures)


def _ids(rows: object) -> set[str]:
    if not isinstance(rows, list):
        return set()
    return {str(row.get("id", "")) for row in rows if isinstance(row, dict)}


def validate_topology(topology: dict, failures: list[str]) -> None:
    if topology.get("schema_id") != "wayfarer.opening_island.world_topology.v1":
        failures.append("opening island topology schema mismatch")
    if topology.get("phase") != "G-15":
        failures.append("opening island topology phase must be G-15")
    structure_ids = _ids(topology.get("structure"))
    for required in REQUIRED_STRUCTURE:
        if required not in structure_ids:
            failures.append(f"topology missing structure node: {required}")
    zone_ids = _ids(topology.get("zones"))
    for required in REQUIRED_ZONES:
        if required not in zone_ids:
            failures.append(f"topology missing zone: {required}")
    route_ids = _ids(topology.get("primary_routes"))
    for required in REQUIRED_ROUTES:
        if required not in route_ids:
            failures.append(f"topology missing primary route: {required}")
    viewpoint_ids = _ids(topology.get("screenshot_viewpoints"))
    for required in REQUIRED_VIEWPOINTS:
        if required not in viewpoint_ids:
            failures.append(f"topology missing screenshot viewpoint: {required}")
    if len(topology.get("exploration_loops", [])) < 2:
        failures.append("topology must define at least two exploration loops")
    if len(topology.get("landmarks", [])) < 4:
        failures.append("topology must define at least four landmarks")
    if len(topology.get("quest_beats", [])) < 6:
        failures.append("topology must define at least six quest beats")
    terrain_rules = " ".join(str(item) for item in topology.get("terrain_rules", []))
    for token in ["No patchwork terrain", "lead somewhere", "Blocked space"]:
        if token not in terrain_rules:
            failures.append(f"terrain rules missing token: {token}")
    acceptance = topology.get("g15_acceptance")
    if not isinstance(acceptance, dict):
        failures.append("topology missing g15_acceptance")
        return
    for flag in [
        "island_reads_as_one_authored_place",
        "player_understands_how_to_leave_town_and_explore",
        "routes_loop_naturally",
        "no_patchwork_terrain",
        "no_meaningless_empty_sprawl",
    ]:
        if acceptance.get(flag) is not True:
            failures.append(f"g15_acceptance missing true flag: {flag}")
    if float(acceptance.get("world_layout_score", 0.0)) < 8.5:
        failures.append("g15_acceptance world_layout_score must be at least 8.5")


def validate_viewpoint_manifest(topology: dict, manifest: dict, failures: list[str]) -> None:
    if manifest.get("schema_id") != "wayfarer.g15.topology_screenshot_viewpoint_manifest.v1":
        failures.append("G-15 screenshot viewpoint manifest schema mismatch")
    if manifest.get("phase") != "G-15":
        failures.append("G-15 screenshot viewpoint manifest phase must be G-15")
    if manifest.get("screenshots_required_now") is not False:
        failures.append("G-15 screenshot viewpoint manifest must record screenshots_required_now=false")
    topology_viewpoints = _ids(topology.get("screenshot_viewpoints"))
    manifest_viewpoints = _ids(manifest.get("planned_viewpoints"))
    for required in REQUIRED_VIEWPOINTS:
        if required not in manifest_viewpoints:
            failures.append(f"G-15 screenshot viewpoint manifest missing viewpoint: {required}")
    if topology_viewpoints != manifest_viewpoints:
        failures.append("G-15 screenshot viewpoint manifest must match topology screenshot_viewpoints")
    final_filenames = " ".join(
        str(row.get("target_final_screenshot", ""))
        for row in manifest.get("planned_viewpoints", [])
        if isinstance(row, dict)
    )
    for filename in [
        "07_village_exit_to_island.png",
        "08_island_entry_transition.png",
        "09_island_main_trail.png",
        "10_island_landmark_signal_or_overlook.png",
        "11_island_cove_or_hidden_landing.png",
        "12_island_optional_discovery.png",
        "17_return_to_town_or_next_hook.png",
    ]:
        if filename not in final_filenames:
            failures.append(f"G-15 screenshot viewpoint manifest missing final target: {filename}")


if __name__ == "__main__":
    sys.exit(main())
