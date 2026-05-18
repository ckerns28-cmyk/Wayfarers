#!/usr/bin/env python3
"""Validate Newport visual order and screenshot-review hard gates."""

from __future__ import annotations

import sys

from starter_village_validator_common import (
    BLUEPRINT,
    G10A_COUNCIL_REPORT,
    G10A_REPORT,
    G10A_SCREENSHOT_MANIFEST,
    LEDGER_JSON,
    MAP_LAYER,
    load_json,
    phase_map,
    print_result,
    repo_path,
    require_text,
)


def main() -> int:
    failures: list[str] = []
    ledger = load_json(LEDGER_JSON, failures)
    blueprint = require_text(
        BLUEPRINT,
        [
            "STARTER_VILLAGE_VISUAL_ORDER_REVIEW_SCORE",
            "starter_village_visual_order_review_contract",
            "starter_village_route_order_specs",
            "central_civic_connector_between_commercial_blocks",
            "west_upland_gap_between_tavern_and_clerk",
            "Council must fail",
            "route corridors run beneath tavern",
            "proof screenshot exists but road order is wrong",
        ],
        failures,
    )
    map_layer = require_text(
        MAP_LAYER,
        [
            "_draw_g7a_authored_visual_order_streets",
            "starter_village_route_order_specs",
            "Vector2(820, 430)",
            "Vector2(1260, 426)",
            "Vector2(1458, 500)",
        ],
        failures,
    )
    require_text(
        repo_path("wayfarer_godot_vertical_slice/tools/validate_vertical_slice.gd"),
        [
            "_validate_starter_village_visual_order_review",
            "_validate_route_segment_clear_of_building_bodies",
            "route_corridor_does_not_run_under_building_body",
            "_rect_overlap_area",
        ],
        failures,
    )

    if '{"center": Vector2(704, 500)' in map_layer:
        failures.append("old broad central route under the counting house must not remain in normal street drawing")
    if '{"center": Vector2(1156, 514)' in map_layer:
        failures.append("old broad east route under the shop/market block must not remain in normal street drawing")
    if "Rect2(361, 300, 50, 238)" in blueprint:
        failures.append("west route segment must not run under the uphill cottage visual body")

    if isinstance(ledger, dict):
        phases = phase_map(ledger, failures)
        if phases.get("G-10A", {}).get("current_status") == "PASS":
            require_text(
                G10A_REPORT,
                [
                    "Visual Order QA Repair",
                    "route/building order",
                    "Council must fail",
                    "tavern-to-clerk street gap",
                ],
                failures,
            )
            if G10A_COUNCIL_REPORT.exists():
                require_text(
                    G10A_COUNCIL_REPORT,
                    [
                        "Visual Order QA Repair",
                        "route corridors",
                        "COUNCIL_PASS_READY_FOR_PR",
                    ],
                    failures,
                )
            manifest = load_json(G10A_SCREENSHOT_MANIFEST, failures)
            if isinstance(manifest, dict):
                screenshots = manifest.get("screenshots")
                if manifest.get("status") != "PASS":
                    failures.append("G-10A screenshot manifest must be PASS before visual order can pass")
                if not isinstance(screenshots, list) or len(screenshots) < 15:
                    failures.append("G-10A visual order requires the full 15-screenshot proof set")
                else:
                    filenames = {str(shot.get("filename", "")) for shot in screenshots if isinstance(shot, dict)}
                    for required in [
                        "g10a_01_wide_newport_normal_gameplay_view.png",
                        "g10a_04_player_near_tavern_inn.png",
                        "g10a_13_y_sort_layering_near_buildings_props.png",
                        "g10a_14_debug_overlays_disabled.png",
                    ]:
                        if required not in filenames:
                            failures.append(f"G-10A visual order proof missing {required}")
                    for shot in screenshots:
                        if not isinstance(shot, dict):
                            continue
                        raw_path = str(shot.get("path", ""))
                        if raw_path and not repo_path(raw_path).exists():
                            failures.append(f"G-10A screenshot path missing: {raw_path}")

    return print_result("newport visual ordering", failures)


if __name__ == "__main__":
    sys.exit(main())
