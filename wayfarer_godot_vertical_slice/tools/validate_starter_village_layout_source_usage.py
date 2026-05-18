#!/usr/bin/env python3
"""Validate that Newport runtime placement follows the locked SV-0 layout source.

This validator targets the screenshot failures that generic PASS reports missed:
clipped/cropped buildings, overlapping row houses, mismatched scale beside the
commercial block, and the false stable/service-yard read behind the tavern.
"""

from __future__ import annotations

import re
import sys
from typing import Any

from starter_village_validator_common import (
    BLUEPRINT,
    BUILDING_CATALOG_GD,
    G7A_SV0_LAYOUT_REPAIR_REPORT,
    MAP_LAYER,
    SV0_WORLD_LAYOUT,
    load_json,
    print_result,
    rel,
    require_text,
)


MIN_FRONTAGE_GAPS = {
    "waterfront_avenue_main": 120,
    "central_counting_connector": 180,
    "residential_backstreet": 180,
    "rear_service_lane": 145,
    "wharf_boardwalk_west": 110,
    "wharf_boardwalk_center": 110,
    "wharf_boardwalk_east": 110,
}


def _extract_starter_ids(blueprint: str, failures: list[str]) -> list[str]:
    match = re.search(r"const\s+STARTER_HARBOR_BUILDING_IDS\s*:=\s*\[(.*?)\]", blueprint, re.S)
    if not match:
        failures.append("NewportTownBlueprint.gd missing STARTER_HARBOR_BUILDING_IDS array")
        return []
    ids = re.findall(r'"([^"]+)"', match.group(1))
    if not ids:
        failures.append("STARTER_HARBOR_BUILDING_IDS did not contain any string building ids")
    return ids


def _lot_anchor(lot: dict[str, Any]) -> tuple[float, float]:
    anchor = lot.get("anchor")
    if not isinstance(anchor, dict):
        return (0.0, 0.0)
    return (float(anchor.get("x", 0.0)), float(anchor.get("y", 0.0)))


def _validate_lot_source(layout: dict[str, Any], active_ids: list[str], failures: list[str]) -> dict[str, dict[str, Any]]:
    lots = layout.get("lots")
    if not isinstance(lots, list) or not lots:
        failures.append("world layout source must contain non-empty lots")
        return {}
    by_building: dict[str, dict[str, Any]] = {}
    for lot in lots:
        if not isinstance(lot, dict):
            failures.append("world layout lot rows must be objects")
            continue
        building_id = str(lot.get("building_id", "")).strip()
        if not building_id:
            failures.append("world layout lot row missing building_id")
            continue
        if building_id in by_building:
            failures.append(f"duplicate lot assignment for {building_id}")
        by_building[building_id] = lot
        x, y = _lot_anchor(lot)
        if x <= 0.0 or y <= 0.0:
            failures.append(f"{building_id} lot anchor must be positive")
        if x < 80.0 or x > 1530.0:
            failures.append(f"{building_id} lot anchor x={x:.0f} risks screen-edge cutoff")
        if y < 120.0 or y > 800.0:
            failures.append(f"{building_id} lot anchor y={y:.0f} is outside the playable town bands")

    missing = [building_id for building_id in active_ids if building_id not in by_building]
    for building_id in missing:
        failures.append(f"active starter building missing authoritative lot assignment: {building_id}")

    for frontage, min_gap in MIN_FRONTAGE_GAPS.items():
        group = [
            (str(lot.get("building_id", "")), _lot_anchor(lot)[0])
            for lot in lots
            if isinstance(lot, dict) and lot.get("frontage") == frontage
        ]
        group.sort(key=lambda item: item[1])
        for (left_id, left_x), (right_id, right_x) in zip(group, group[1:]):
            gap = right_x - left_x
            if gap < float(min_gap):
                failures.append(
                    f"{frontage} anchors too close: {left_id} to {right_id} gap {gap:.0f}px < {min_gap}px"
                )

    expected_anchor_caps = {
        "b_printer_rowhouse": 1525,
        "b_dockworker_rowhouse": 1320,
        "b_boarding_house": 1160,
    }
    for building_id, max_x in expected_anchor_caps.items():
        lot = by_building.get(building_id)
        if lot:
            x, _ = _lot_anchor(lot)
            if x > float(max_x):
                failures.append(f"{building_id} anchor x={x:.0f} exceeds camera-safe cap {max_x}")

    cooperage = by_building.get("b_cooperage_shed", {})
    if cooperage:
        x, y = _lot_anchor(cooperage)
        if cooperage.get("district") != "harbor_waterfront" or y < 680.0 or x < 1000.0:
            failures.append("b_cooperage_shed must be a wharf-side work lot, not a tavern-back stable lot")

    return by_building


def _require_tokens(text: str, tokens: list[str], file_label: str, failures: list[str]) -> None:
    for token in tokens:
        if token not in text:
            failures.append(f"{file_label} missing token: {token}")


def _reject_tokens(text: str, tokens: list[str], file_label: str, failures: list[str]) -> None:
    for token in tokens:
        if token in text:
            failures.append(f"{file_label} still contains rejected token: {token}")


def main() -> int:
    failures: list[str] = []
    layout = load_json(SV0_WORLD_LAYOUT, failures)
    blueprint = require_text(
        BLUEPRINT,
        [
            "STARTER_VILLAGE_LAYOUT_SOURCE_PATH",
            "STARTER_VILLAGE_G7A_TOOL_BACKED_LAYOUT_REPAIR_PASS",
            "starter_village_runtime_lot_assignments",
            "_runtime_lot_foot_tile",
            "res://data/world_layout/starter_village_world_layout_v1.json",
        ],
        failures,
    )
    map_layer = require_text(
        MAP_LAYER,
        [
            "g7a_west_residential_lot_foundation",
            "Rect2(204, 178, 230, 126)",
            "g7a_cooperage_service_lot_foundation",
            "Rect2(1084, 626, 210, 96)",
            "g7a_backstreet_service_lot_foundation",
            "Rect2(1086, 350, 330, 126)",
            "cooperage_wharf_repair_sawhorse",
            "east_rear_service_connector_fence_gate",
        ],
        failures,
    )
    catalog = require_text(
        BUILDING_CATALOG_GD,
        [
            "G-7A-SV0 scale repair",
            '"b_mercantile"',
            "142.0",
        ],
        failures,
    )
    require_text(
        G7A_SV0_LAYOUT_REPAIR_REPORT,
        [
            "G-7A-SV0 Tool-Backed Layout Repair",
            "Screenshot Failures Addressed",
            "Validator Catches",
            "false stable",
            "overlap",
            "cutoff",
        ],
        failures,
    )

    _reject_tokens(
        map_layer,
        [
            "tavern_rear_stable_service_yard",
            "west_service_yard_repair_sawhorse",
            "Rect2(146, 410, 232, 124)",
            "Rect2(1378, 414, 176, 126)",
            "Vector2(1450, 474)",
        ],
        rel(MAP_LAYER),
        failures,
    )
    _reject_tokens(
        blueprint,
        [
            'Vector2(1472.0, 416.0)',
            'Vector2(1299.0, 408.0)',
            'Vector2(264.0, 476.0)',
            'parcel_cooperage_yard", "support", 462.0',
        ],
        rel(BLUEPRINT),
        failures,
    )

    active_ids = _extract_starter_ids(blueprint, failures)
    if isinstance(layout, dict):
        if layout.get("authoring_mode") != "godot_native_repo_local_json":
            failures.append("world layout authoring_mode must remain godot_native_repo_local_json")
        planning_order = layout.get("planning_order")
        if not isinstance(planning_order, list) or "props_last" not in planning_order:
            failures.append("world layout planning_order must include props_last")
        for key in [
            "districts",
            "roads",
            "alleys",
            "dock_paths",
            "lots",
            "npc_routes",
            "interaction_zones",
            "quest_beat_locations",
            "camera_viewpoints",
        ]:
            value = layout.get(key)
            if not isinstance(value, list) or not value:
                failures.append(f"world layout source missing non-empty {key}")
        lot_by_building = _validate_lot_source(layout, active_ids, failures)
        for building_id in active_ids:
            _require_tokens(
                blueprint,
                [
                    f'"{building_id}": _runtime_lot(',
                    f'_runtime_lot_foot_tile("{building_id}"',
                ],
                rel(BLUEPRINT),
                failures,
            )
        expected_layout_rule_tokens = [
            'Vector2(1522.0, 596.0)',
            'Vector2(1160.0, 430.0)',
            'Vector2(1320.0, 430.0)',
            'Vector2(1165.0, 705.0)',
            'parcel_cooperage_wharf',
            'not a fake stable yard behind the tavern',
        ]
        _require_tokens(blueprint, expected_layout_rule_tokens, rel(BLUEPRINT), failures)

        # The screenshot complaints were about visible composition, so assert the
        # source data now makes the visual intent inspectable instead of implicit.
        if "b_mercantile" in lot_by_building and "b_clerk_townhouse" in lot_by_building:
            mercantile_x, _ = _lot_anchor(lot_by_building["b_mercantile"])
            clerk_x, _ = _lot_anchor(lot_by_building["b_clerk_townhouse"])
            if mercantile_x - clerk_x < 160.0:
                failures.append("b_mercantile must have a full-size shop lot beside the clerk rowhouse")
        if "b_market_shed" in lot_by_building and "b_printer_rowhouse" in lot_by_building:
            market_x, _ = _lot_anchor(lot_by_building["b_market_shed"])
            printer_x, _ = _lot_anchor(lot_by_building["b_printer_rowhouse"])
            if printer_x - market_x < 120.0:
                failures.append("b_printer_rowhouse must not overlap the market shed block")

    if '"b_mercantile":' not in catalog or "G-7A-SV0 scale repair" not in catalog:
        failures.append("BuildingCatalog must document the mercantile scale repair")

    details = [
        "layout source: " + rel(SV0_WORLD_LAYOUT),
        "active starter buildings checked: " + str(len(active_ids)),
        "screenshot-failure gates: false stable, clipped rowhouse, overlap spacing, mercantile scale",
    ]
    return print_result("starter village layout source usage", failures, details)


if __name__ == "__main__":
    sys.exit(main())
