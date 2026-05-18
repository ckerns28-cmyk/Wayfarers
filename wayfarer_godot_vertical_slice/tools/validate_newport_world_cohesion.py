#!/usr/bin/env python3
"""Validate the Newport world-cohesion masterplan and runtime references."""

from __future__ import annotations

import sys

from starter_village_validator_common import (
    BLUEPRINT,
    G7A_COUNCIL_REPORT,
    G7A_REPORT,
    G7A_SCREENSHOT_MANIFEST,
    G7B_COUNCIL_REPORT,
    G7B_REPORT,
    G7B_SCREENSHOT_MANIFEST,
    G7_COUNCIL_REPORT,
    G7_REPORT,
    LEDGER_JSON,
    MAP_LAYER,
    ROADMAP_JSON,
    ROADMAP_MD,
    load_json,
    phase_map,
    print_result,
    repo_path,
    require_text,
)


def main() -> int:
    failures: list[str] = []
    roadmap = load_json(ROADMAP_JSON, failures)
    ledger = load_json(LEDGER_JSON, failures)
    blueprint = require_text(
        BLUEPRINT,
        [
            "starter_district_plan",
            "district_identity",
            "street_grammar",
            "waterfront_avenue_parallel_to_harbor",
            "back_street_behind_waterfront_road",
            "walking_loop_specs",
            "interaction_anchors",
            "tavern_inn_entrance",
            "town_hall_entrance",
            "dock_worker_west",
            "STARTER_VILLAGE_G7A_STREET_LOT_GROUND_COHESION_PASS",
            "street_lot_ground_cohesion_reconstruction_pass",
            "g7a_runtime_cohesion_contract",
            "STARTER_VILLAGE_G7B_HARBOR_COMMERCIAL_SPINE_PASS",
            "harbor_commercial_spine_cohesion_pass",
            "g7b_harbor_commercial_spine_contract",
        ],
        failures,
    )
    map_layer = require_text(
        MAP_LAYER,
        [
            "STARTER_VILLAGE_G7A_COHESION_PASS",
            "G7A_TOWN_COHESION_PHASE_SCORE",
            "_draw_g7a_cohesive_ground_foundation",
            "_draw_g7a_lot_foundation_overlays",
            "_draw_g7a_continuous_street_base",
            "_draw_g7a_route_curbs_and_material_transitions",
            "g7a_tavern_lot_foundation",
            "g7a_counting_house_civic_lot_foundation",
            "g7a_west_wharf_lot_foundation",
            "STARTER_VILLAGE_G7B_HARBOR_SPINE_PASS",
            "NEWPORT_G7B_HARBOR_WORK_ZONE_PLACEMENTS",
            "_draw_g7b_functional_wharf_work_zones",
            "_draw_g7b_harbor_commercial_spine_dressing",
            "g7b_west_fish_offload_zone_net_crates",
            "g7b_central_manifest_cargo_waiting_for_counting_house",
            "g7b_market_transfer_goods_linked_to_wharf",
        ],
        failures,
    )
    require_text(
        G7_REPORT,
        [
            "Locked Town Grammar",
            "Player Arrival Route",
            "District Purpose And Building Reasons",
            "Opening Quest Beat Map",
            "NPC Work/Life Route Contract",
            "G-7A Repair Instructions",
        ],
        failures,
    )
    require_text(
        G7_COUNCIL_REPORT,
        [
            "COUNCIL_PASS_READY_FOR_PR",
            "World/Layout Designer",
            "runtime screenshot remains",
            "known failing baseline",
        ],
        failures,
    )
    require_text(ROADMAP_MD, ["town cohesion is approximately 2/10", "G-7A"], failures)

    if isinstance(roadmap, dict):
        baseline = roadmap.get("baseline")
        if not isinstance(baseline, dict):
            failures.append("roadmap baseline must be an object")
        else:
            if float(baseline.get("town_cohesion_score", 0.0)) != 2.0:
                failures.append("baseline town cohesion must preserve Chris's 2/10 signal")
            for raw_path in baseline.get("evidence", []):
                if not repo_path(str(raw_path)).exists():
                    failures.append(f"baseline screenshot evidence missing: {raw_path}")
        phases = {str(row.get("phase_id", "")): row for row in roadmap.get("phases", []) if isinstance(row, dict)}
        g7a = phases.get("G-7A", {})
        if "town_cohesion_at_least_7_5" not in str(g7a):
            failures.append("G-7A acceptance must require town cohesion at least 7.5")
        g14 = phases.get("G-14", {})
        if "town_cohesion_score_at_least_8_5" not in str(g14):
            failures.append("G-14 acceptance must require town cohesion at least 8.5")
        if phases.get("G-7A", {}).get("status") == "PASS":
            g7b_status = phases.get("G-7B", {}).get("status")
            if g7b_status not in {"PENDING", "PASS"}:
                failures.append("G-7B roadmap status must remain PENDING until proof exists, then become PASS")

    for token in ["harbor_loop", "market_loop", "civic_residential_loop"]:
        if token not in blueprint:
            failures.append(f"blueprint missing walking loop token: {token}")
    for token in [
        "g7a_continuous_harborfront_avenue_binds_the_wide_view",
        "g7a_back_street_and_service_lane_read_as_connected_routes",
        "g7a_uphill_connectors_join_harbor_commerce_to_civic_residential_blocks",
        "g7a_lot_foundations_ground_every_major_visible_building",
        "g7a_dock_to_road_transition_replaces_random_green_empty_blocks",
        "g7a_no_debug_like_road_planning_artifacts_in_normal_play",
    ]:
        if token not in blueprint:
            failures.append(f"blueprint missing G-7A street grammar token: {token}")
    for token in [
        "g7b_fish_offload_manifest_chandlery_market_work_zones",
        "g7b_commercial_avenue_goods_visibly_flow_to_wharf",
        "g7b_counting_house_route_reads_as_harbor_commerce",
        "g7b_dock_objects_group_by_function_without_blocking_navigation",
    ]:
        if token not in blueprint:
            failures.append(f"blueprint missing G-7B harbor/commercial token: {token}")
    if "draw_circle(pos, 4, Color(\"#2f251b\"))" in map_layer and "if not G422R_SUPPRESS_PRIMITIVE_WORLD_PROPS" not in map_layer:
        failures.append("primitive marker draw calls must stay behind suppression guards")

    if isinstance(ledger, dict):
        ledger_phases = phase_map(ledger, failures)
        if ledger_phases.get("G-7A", {}).get("current_status") == "PASS":
            require_text(
                G7A_REPORT,
                [
                    "G-7A Street, Lot, and Ground Cohesion Reconstruction",
                    "Roads lead somewhere",
                    "Town cohesion score",
                    "G-7B next",
                ],
                failures,
            )
            require_text(
                G7A_COUNCIL_REPORT,
                [
                    "COUNCIL_PASS_READY_FOR_PR",
                    "World/Layout Designer",
                    "Art Director",
                    "runtime screenshots",
                    "town cohesion score: 7.6",
                ],
                failures,
            )
            manifest = load_json(G7A_SCREENSHOT_MANIFEST, failures)
            if isinstance(manifest, dict):
                if manifest.get("status") != "PASS":
                    failures.append("G-7A screenshot manifest must be PASS")
                screenshots = manifest.get("screenshots")
                if not isinstance(screenshots, list) or len(screenshots) < 15:
                    failures.append("G-7A screenshot manifest must include the 15 recurring proof views")
                else:
                    for shot in screenshots:
                        if not isinstance(shot, dict):
                            failures.append("G-7A screenshot manifest row must be an object")
                            continue
                        if shot.get("status") != "PASS":
                            failures.append(f"G-7A screenshot failed: {shot.get('filename')}")
                        raw_path = str(shot.get("path", ""))
                        if raw_path and not repo_path(raw_path).exists():
                            failures.append(f"G-7A screenshot path missing: {raw_path}")
        if ledger_phases.get("G-7B", {}).get("current_status") == "PASS":
            require_text(
                G7B_REPORT,
                [
                    "G-7B Harbor, Wharf, and Commercial Spine Cohesion",
                    "working waterfront",
                    "commercial avenue connected to harbor labor",
                    "G-7C next",
                ],
                failures,
            )
            require_text(
                G7B_COUNCIL_REPORT,
                [
                    "COUNCIL_PASS_READY_FOR_PR",
                    "World/Layout Designer",
                    "runtime screenshots",
                    "harbor/world score: 8.5",
                ],
                failures,
            )
            manifest = load_json(G7B_SCREENSHOT_MANIFEST, failures)
            if isinstance(manifest, dict):
                if manifest.get("status") != "PASS":
                    failures.append("G-7B screenshot manifest must be PASS")
                screenshots = manifest.get("screenshots")
                if not isinstance(screenshots, list) or len(screenshots) < 15:
                    failures.append("G-7B screenshot manifest must include the 15 recurring proof views")
                else:
                    for shot in screenshots:
                        if not isinstance(shot, dict):
                            failures.append("G-7B screenshot manifest row must be an object")
                            continue
                        if shot.get("status") != "PASS":
                            failures.append(f"G-7B screenshot failed: {shot.get('filename')}")
                        raw_path = str(shot.get("path", ""))
                        if raw_path and not repo_path(raw_path).exists():
                            failures.append(f"G-7B screenshot path missing: {raw_path}")

    return print_result(
        "newport world cohesion",
        failures,
        ["G-7A/G-7B cohesion contracts are runtime-backed when the ledger marks those phases PASS."],
    )


if __name__ == "__main__":
    sys.exit(main())
