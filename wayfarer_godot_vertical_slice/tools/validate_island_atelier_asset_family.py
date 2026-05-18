#!/usr/bin/env python3
"""Validate the G-16A island atelier asset family contract."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from opening_village_island_validator_common import PROJECT_ROOT, REPO_ROOT, load_json, print_result, require_text, repo_path, validate_phase_contract


ASSET_JSON = PROJECT_ROOT / "data" / "world_layout" / "island_atelier_asset_family_v1.json"
TOPOLOGY_JSON = PROJECT_ROOT / "data" / "world_layout" / "opening_island_world_topology_v1.json"
SCREENSHOT_MANIFEST = PROJECT_ROOT / "artifacts" / "review" / "g16a_runtime_screenshots" / "g16a_runtime_screenshot_manifest.json"
G16A_REPORT = REPO_ROOT / "docs" / "reports" / "G16A_ISLAND_ATELIER_ASSET_FAMILY_PASS.md"
G16A_REPORT_JSON = REPO_ROOT / "docs" / "reports" / "G16A_ISLAND_ATELIER_ASSET_FAMILY_PASS.json"
BLUEPRINT_GD = PROJECT_ROOT / "scripts" / "NewportTownBlueprint.gd"
MAIN_GD = PROJECT_ROOT / "scenes" / "Main.gd"
MAP_LAYER_GD = PROJECT_ROOT / "scenes" / "map" / "MapLayer.gd"
CAPTURE_GD = PROJECT_ROOT / "tools" / "capture_g16a_runtime_screenshots.gd"
CAPTURE_PS1 = PROJECT_ROOT / "tools" / "capture_g16a_runtime_screenshots.ps1"
ATELIER_MANIFEST_DIR = PROJECT_ROOT / "art_pipeline" / "newport_atelier" / "manifests"

REQUIRED_ASSET_IDS = [
    "atelier_terrain_dirt_path_border_01",
    "atelier_terrain_broken_grassy_shoulder_01",
    "atelier_path_dirt_worn_section_01",
    "atelier_path_loose_paving_fragments_01",
    "atelier_shore_shell_pebble_cluster_01",
    "atelier_shore_wet_rocks_sand_01",
    "atelier_shore_driftwood_log_cluster_01",
    "atelier_shore_harbor_debris_slats_rope_01",
    "atelier_shore_eelgrass_reeds_cluster_01",
    "atelier_wayfinding_pier_lantern_stand_01",
    "atelier_wayfinding_harbor_road_marker_01",
    "atelier_wayfinding_multi_arrow_signpost_01",
    "atelier_wayfinding_bollard_lantern_01",
    "atelier_wayfinding_coastal_waystone_01",
    "atelier_civic_anchor_plaque_01",
    "atelier_civic_dock_rules_board_01",
    "atelier_g418e_service_fence_gate_01",
    "atelier_g418e_service_utility_barrels_01",
    "atelier_g418e_service_alley_crates_01",
    "atelier_g418e_service_firewood_barrow_01",
    "atelier_g418e_service_repair_sawhorse_01",
    "atelier_g418e_service_stone_edge_01",
    "atelier_g418e_harbor_bollard_pair_01",
    "atelier_g418e_harbor_rope_coil_large_01",
    "atelier_g418e_harbor_cargo_stack_01",
    "atelier_g418e_harbor_fishing_crate_net_stack_01",
    "atelier_g418e_harbor_service_post_lantern_01",
    "atelier_g418e_harbor_fish_baskets_tub_01",
]

REQUIRED_FAMILY_IDS = [
    "coastal_rocks_shore_debris_cove_objects",
    "trail_edge_clutter_wooded_props",
    "old_road_path_fragments",
    "lantern_posts_signposts_wayfinding",
    "quest_clue_props_civic_harbor_memory",
    "farm_service_props_fences_small_carts_crates",
    "cove_objects_harbor_work_props",
]

REQUIRED_SCREENSHOTS = [
    "g16a_01_island_asset_family_wide.png",
    "g16a_02_trail_edge_clutter.png",
    "g16a_03_cove_coastal_assets.png",
    "g16a_04_farm_service_props.png",
    "g16a_05_quest_clue_asset_provenance.png",
    "g16a_06_debug_overlays_disabled.png",
]


def project_path(raw_path: str) -> Path:
    normalized = raw_path.replace("\\", "/")
    if normalized.startswith("res://"):
        return PROJECT_ROOT / normalized.removeprefix("res://")
    if normalized.startswith("art_pipeline/"):
        return PROJECT_ROOT / normalized
    return repo_path(normalized)


def main() -> int:
    failures: list[str] = []
    validate_phase_contract("G-16A", failures)
    source = load_json(ASSET_JSON, failures)
    topology = load_json(TOPOLOGY_JSON, failures)
    report_json = load_json(G16A_REPORT_JSON, failures)
    manifest = load_json(SCREENSHOT_MANIFEST, failures)
    require_text(
        G16A_REPORT,
        [
            "G-16A Island Atelier Asset Family Pass",
            "No placeholders",
            "Atelier compliance PASS",
            "COUNCIL_PASS_READY_FOR_PR",
            "Next phase: G-17 Island NPC / Encounter / Ambient Life Foundation",
        ],
        failures,
    )
    require_text(
        BLUEPRINT_GD,
        [
            "G16A_ISLAND_ATELIER_ASSET_FAMILY_PASS",
            "opening_island_atelier_asset_family_contract",
            "opening_island_atelier_asset_family_assets",
            "atelier_wayfinding_pier_lantern_stand_01",
            "atelier_g418e_harbor_fishing_crate_net_stack_01",
        ],
        failures,
    )
    require_text(MAIN_GD, ["opening_island_atelier_asset_family_contract"], failures)
    require_text(
        MAP_LAYER_GD,
        [
            "_draw_g16a_island_atelier_asset_family",
            "g16a_trail_edge_clutter_pasture_lane",
            "g16a_cove_objects_harbor_work_read",
            "g16a_farm_service_props_worked_edge",
            "g16a_signposts_old_road_choice_without_debug_ui",
        ],
        failures,
    )
    require_text(CAPTURE_GD, REQUIRED_SCREENSHOTS, failures)
    require_text(CAPTURE_PS1, ["capture_g16a_runtime_screenshots.gd"], failures)
    if isinstance(source, dict):
        validate_source(source, failures)
    if isinstance(topology, dict):
        implementation = topology.get("g16a_atelier_asset_family_implementation", {})
        if not isinstance(implementation, dict) or implementation.get("status") != "PASS":
            failures.append("topology missing PASS g16a_atelier_asset_family_implementation")
    if isinstance(report_json, dict):
        validate_report_json(report_json, failures)
    if isinstance(manifest, dict):
        validate_manifest(manifest, failures)
    if isinstance(source, dict):
        validate_atelier_manifests(source, failures)
    return print_result("island atelier asset family", failures)


def validate_source(data: dict, failures: list[str]) -> None:
    if data.get("schema_id") != "wayfarer.g16a.island_atelier_asset_family.v1":
        failures.append("G-16A source schema mismatch")
    if data.get("phase") != "G-16A":
        failures.append("G-16A source phase mismatch")
    if data.get("poi_source") != "wayfarer_godot_vertical_slice/data/world_layout/island_poi_landmarks_v1.json":
        failures.append("G-16A POI source mismatch")
    required_assets = set(str(item) for item in data.get("required_asset_ids", []))
    for asset_id in REQUIRED_ASSET_IDS:
        if asset_id not in required_assets:
            failures.append(f"G-16A required_asset_ids missing {asset_id}")
    family_ids = set()
    covered_assets = set()
    for raw_family in data.get("asset_families", []):
        if not isinstance(raw_family, dict):
            failures.append("G-16A asset_families rows must be objects")
            continue
        family_id = str(raw_family.get("family_id", "")).strip()
        family_ids.add(family_id)
        for key in ["manifest", "contact_sheet", "source_image", "generation_prompt", "provenance_report", "validation_report"]:
            raw_path = str(raw_family.get(key, "")).strip()
            if not raw_path:
                failures.append(f"G-16A family {family_id} missing {key}")
                continue
            if not project_path(raw_path).exists():
                failures.append(f"G-16A family {family_id} missing {key} path: {raw_path}")
        covered_assets.update(str(asset_id) for asset_id in raw_family.get("asset_ids", []))
        if not str(raw_family.get("island_role", "")).strip():
            failures.append(f"G-16A family {family_id} missing island_role")
    for family_id in REQUIRED_FAMILY_IDS:
        if family_id not in family_ids:
            failures.append(f"G-16A missing asset family: {family_id}")
    for asset_id in REQUIRED_ASSET_IDS:
        if asset_id not in covered_assets:
            failures.append(f"G-16A asset not covered by a family: {asset_id}")
    acceptance = data.get("acceptance", {})
    for flag in [
        "island_assets_feel_cohesive_with_Newport",
        "assets_reinforce_island_fantasy",
        "manifest_provenance_source_proof_exists",
        "no_placeholders",
        "no_untracked_sprites",
        "no_crude_markers",
        "no_yellow_red_unknown_assets_promoted",
        "route_probes_remain_clear",
    ]:
        if not isinstance(acceptance, dict) or acceptance.get(flag) is not True:
            failures.append(f"G-16A acceptance missing true flag: {flag}")
    if not isinstance(acceptance, dict) or acceptance.get("atelier_compliance") != "PASS":
        failures.append("G-16A acceptance must record atelier_compliance PASS")
    if float(acceptance.get("art_direction_score", 0.0)) < 8.5:
        failures.append("G-16A art_direction_score must be at least 8.5")
    if float(acceptance.get("world_layout_score", 0.0)) < 8.5:
        failures.append("G-16A world_layout_score must be at least 8.5")
    screenshots = set(str(item) for item in data.get("required_screenshots", []))
    for filename in REQUIRED_SCREENSHOTS:
        if filename not in screenshots:
            failures.append(f"G-16A source missing required screenshot: {filename}")


def validate_report_json(data: dict, failures: list[str]) -> None:
    if data.get("status") != "PASS":
        failures.append("G-16A report JSON status must be PASS")
    if data.get("screenshot_manifest") != "wayfarer_godot_vertical_slice/artifacts/review/g16a_runtime_screenshots/g16a_runtime_screenshot_manifest.json":
        failures.append("G-16A report JSON screenshot manifest mismatch")
    if data.get("provenance_atelier_result") != "PASS":
        failures.append("G-16A report JSON provenance_atelier_result must be PASS")
    if float(data.get("art_direction_score", 0.0)) < 8.5:
        failures.append("G-16A report JSON art_direction_score must be at least 8.5")
    acceptance = data.get("acceptance", {})
    if not isinstance(acceptance, dict) or acceptance.get("atelier_compliance") != "PASS":
        failures.append("G-16A report JSON acceptance must record atelier compliance PASS")


def validate_manifest(manifest: dict, failures: list[str]) -> None:
    if manifest.get("phase") != "G-16A":
        failures.append("G-16A screenshot manifest phase mismatch")
    if manifest.get("status") != "PASS":
        failures.append("G-16A screenshot manifest status must be PASS")
    if manifest.get("no_hud_capture") is not True:
        failures.append("G-16A screenshot manifest must record no_hud_capture=true")
    if manifest.get("debug_overlays_disabled") is not True:
        failures.append("G-16A screenshot manifest must record debug_overlays_disabled=true")
    filenames = {
        str(item.get("filename", ""))
        for item in manifest.get("screenshots", [])
        if isinstance(item, dict)
    }
    for filename in REQUIRED_SCREENSHOTS:
        if filename not in filenames:
            failures.append(f"G-16A screenshot manifest missing {filename}")
    contract = manifest.get("opening_island_atelier_asset_family_contract", {})
    if not isinstance(contract, dict) or contract.get("phase") != "G-16A":
        failures.append("G-16A screenshot manifest missing atelier asset family contract")
    elif int(contract.get("asset_count", 0)) < len(REQUIRED_ASSET_IDS):
        failures.append("G-16A runtime contract asset_count is too low")
    for item in manifest.get("screenshots", []):
        if isinstance(item, dict) and item.get("status") != "PASS":
            failures.append(f"G-16A screenshot did not PASS: {item.get('filename', '<unknown>')}")


def validate_atelier_manifests(source: dict, failures: list[str]) -> None:
    asset_index: dict[str, dict] = {}
    manifest_paths = []
    for raw_family in source.get("asset_families", []):
        if isinstance(raw_family, dict):
            raw_path = str(raw_family.get("manifest", "")).strip()
            if raw_path:
                manifest_paths.append(project_path(raw_path))
    if not manifest_paths:
        failures.append("no G-16A Newport atelier family manifests listed")
        return
    for path in manifest_paths:
        if not path.exists():
            failures.append(f"missing G-16A family manifest: {path}")
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"invalid atelier manifest {path.name}: {exc}")
            continue
        for asset in data.get("assets", []):
            if isinstance(asset, dict):
                asset_id = str(asset.get("asset_id", "")).strip()
                if asset_id:
                    asset_index[asset_id] = asset
    for asset_id in REQUIRED_ASSET_IDS:
        asset = asset_index.get(asset_id)
        if not isinstance(asset, dict):
            failures.append(f"required G-16A asset missing from Newport atelier manifests: {asset_id}")
            continue
        validate_asset_provenance(asset_id, asset, failures)


def validate_asset_provenance(asset_id: str, asset: dict, failures: list[str]) -> None:
    if asset.get("review_eligible") is not True:
        failures.append(f"{asset_id} must be review_eligible")
    if asset.get("normal_review_eligible") is not True:
        failures.append(f"{asset_id} must be normal_review_eligible")
    for flag in [
        "lab_only",
        "source_pixels_from_yellow_uncertain_assets",
        "source_pixels_from_third_party_material",
        "web_scraped_source_pixels",
    ]:
        if asset.get(flag) is not False:
            failures.append(f"{asset_id} must have {flag}=false")
    rating = float(asset.get("visual_quality_rating", asset.get("visual_quality_gate", 0.0)))
    gate = float(asset.get("visual_quality_gate", 0.0))
    if rating < 8.5 or gate < 8.5:
        failures.append(f"{asset_id} must meet 8.5 atelier visual gate")
    for key in ["path", "atlas", "source_image", "generation_prompt", "extraction_script"]:
        raw_path = str(asset.get(key, "")).strip()
        if not raw_path:
            failures.append(f"{asset_id} missing provenance field {key}")
            continue
        if not project_path(raw_path).exists():
            failures.append(f"{asset_id} missing provenance path {key}: {raw_path}")


if __name__ == "__main__":
    sys.exit(main())
