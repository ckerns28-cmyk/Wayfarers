#!/usr/bin/env python3
"""Fail the pre-G-5 gate when visible runtime sprites are not atelier-traceable."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from PIL import Image


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[1]
REPO_ROOT = PROJECT_ROOT.parent

MANIFEST_PATH = PROJECT_ROOT / "art_pipeline" / "player_identity" / "manifests" / "newport_atelier_characters_g422r_manifest.json"
REGISTRY_PATH = PROJECT_ROOT / "art_pipeline" / "newport" / "manifests" / "newport_visual_production_registry.json"
PLAYER_GD = PROJECT_ROOT / "scenes" / "player" / "Player.gd"
EDRIN_GD = PROJECT_ROOT / "scenes" / "npc" / "EdrinVale.gd"
EDRIN_TSCN = PROJECT_ROOT / "scenes" / "npc" / "EdrinVale.tscn"
ATELIER_NPC_GD = PROJECT_ROOT / "scenes" / "npc" / "AtelierTownNpc.gd"
ATELIER_NPC_TSCN = PROJECT_ROOT / "scenes" / "npc" / "AtelierTownNpc.tscn"
MAP_LAYER_GD = PROJECT_ROOT / "scenes" / "map" / "MapLayer.gd"
BLUEPRINT_GD = PROJECT_ROOT / "scripts" / "NewportTownBlueprint.gd"
SCREENSHOT_MANIFEST = PROJECT_ROOT / "artifacts" / "review" / "g422r_runtime_screenshots" / "g422r_runtime_screenshot_manifest.json"

PLAYER_ATLAS = PROJECT_ROOT / "art_pipeline" / "player_identity" / "atlases" / "player_wayfarer_atelier_g422r_v1.png"
NPC_ATLAS = PROJECT_ROOT / "art_pipeline" / "player_identity" / "atlases" / "newport_npc_atelier_g422r_v1.png"
CONTACT_SHEET = PROJECT_ROOT / "art_pipeline" / "player_identity" / "contact_sheets" / "newport_atelier_characters_g422r_contact_sheet.png"
SOURCE_IMAGE = PROJECT_ROOT / "art_pipeline" / "player_identity" / "source_generated" / "g422r_atelier_characters_source_imagegen.png"
SOURCE_PROMPT = PROJECT_ROOT / "art_pipeline" / "player_identity" / "source_generated" / "g422r_atelier_characters_prompt.txt"
SIGN_CONTACT = PROJECT_ROOT / "art_pipeline" / "newport_atelier" / "contact_sheets" / "newport_atelier_sign_shop_markers_contact_sheet.png"
WAYFINDING_CONTACT = PROJECT_ROOT / "art_pipeline" / "newport_atelier" / "contact_sheets" / "newport_atelier_lamps_wayfinding_contact_sheet.png"

REQUIRED_SCREENSHOT_TARGETS = {
    "wide_newport_normal_gameplay_view",
    "player_near_tavern_inn_district",
    "player_near_commercial_avenue",
    "player_at_harbor_dock_edge",
    "player_near_npcs",
    "player_near_props_signs_markers",
    "player_near_layered_y_sort_objects",
    "gameplay_zoom_readability_proof",
    "debug_overlays_disabled_proof",
    "player_npc_contact_sheet_proof",
    "marker_sign_world_object_contact_sheet_proof",
    "wider_town_cohesion_no_placeholder_mix",
}


def rel(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def load_json(path: Path, failures: list[str]) -> Any:
    if not path.exists():
        failures.append(f"missing {rel(path)}")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        failures.append(f"invalid json {rel(path)}: {exc}")
        return None


def require_path(path: Path, failures: list[str]) -> None:
    if not path.exists():
        failures.append(f"missing {rel(path)}")


def require_image(path: Path, failures: list[str], min_nontransparent_pixels: int = 500) -> None:
    require_path(path, failures)
    if not path.exists():
        return
    try:
        image = Image.open(path).convert("RGBA")
    except OSError as exc:
        failures.append(f"could not open image {rel(path)}: {exc}")
        return
    alpha = image.getchannel("A")
    if alpha.getbbox() is None:
        failures.append(f"image has no visible alpha content: {rel(path)}")
        return
    opaque_count = sum(1 for value in alpha.getdata() if value > 16)
    if opaque_count < min_nontransparent_pixels:
        failures.append(f"image visible content too small: {rel(path)} opaque_pixels={opaque_count}")


def validate_manifest(failures: list[str]) -> None:
    manifest = load_json(MANIFEST_PATH, failures)
    if not isinstance(manifest, dict):
        return
    if manifest.get("schema_id") != "wayfarer.player_identity.g422r.character_manifest.v2":
        failures.append("G-4.22R character manifest schema mismatch")
    if manifest.get("phase") != "G-4.22R":
        failures.append("G-4.22R character manifest phase mismatch")
    if manifest.get("family_id") != "newport_atelier_characters_g422r":
        failures.append("G-4.22R character manifest family mismatch")
    provenance = manifest.get("provenance_assertions", {})
    if not isinstance(provenance, dict):
        failures.append("G-4.22R provenance assertions missing")
    else:
        for key in ["source_pixels_from_yellow_uncertain_assets", "source_pixels_from_third_party_material", "web_scraped_source_pixels", "placeholder"]:
            if provenance.get(key) is not False:
                failures.append(f"G-4.22R manifest must mark {key}=false")
        if provenance.get("normal_review_eligible") is not True:
            failures.append("G-4.22R manifest must mark normal_review_eligible=true")
    runtime_assets = manifest.get("runtime_assets", {})
    if not isinstance(runtime_assets, dict):
        failures.append("G-4.22R runtime assets must be recorded")
    else:
        if "player_wayfarer_atelier_g422r_v1.png" not in str(runtime_assets.get("player_atlas", "")):
            failures.append("G-4.22R manifest missing player runtime atlas")
        if "newport_npc_atelier_g422r_v1.png" not in str(runtime_assets.get("npc_atlas", "")):
            failures.append("G-4.22R manifest missing NPC runtime atlas")
    if len(manifest.get("npcs", [])) < 3:
        failures.append("G-4.22R manifest must include at least three approved NPC variants")


def validate_registry(failures: list[str]) -> None:
    registry = load_json(REGISTRY_PATH, failures)
    if not isinstance(registry, dict):
        return
    if registry.get("phase") != "G-4.22R":
        failures.append("visual production registry must record the G-4.22R runtime consistency repair")
    entries = registry.get("asset_entries", [])
    if not isinstance(entries, list):
        failures.append("visual production registry asset_entries must be a list")
        return
    by_id = {str(entry.get("asset_id", "")): entry for entry in entries if isinstance(entry, dict)}
    for asset_id in ["player_wayfarer_atelier_g422r", "newport_npc_atelier_g422r"]:
        entry = by_id.get(asset_id)
        if not isinstance(entry, dict):
            failures.append(f"missing registry entry: {asset_id}")
            continue
        usage = entry.get("current_usage", {})
        if not isinstance(usage, dict) or usage.get("normal_review") is not True:
            failures.append(f"{asset_id} must be normal-review active")
        if "green_origin_candidate" not in str(entry.get("source_provenance_status", "")):
            failures.append(f"{asset_id} provenance must be green-origin candidate pending license review")
        if entry.get("rebuild_status") != "APPROVED_TEMPORARY":
            failures.append(f"{asset_id} rebuild_status must be APPROVED_TEMPORARY")
    old_player = by_id.get("player_wayfarer_foundation_g419")
    if isinstance(old_player, dict):
        usage = old_player.get("current_usage", {})
        if isinstance(usage, dict) and usage.get("normal_review") is True:
            failures.append("G-4.19 player foundation must not remain active normal review after G-4.22R")


def validate_runtime_references(failures: list[str]) -> None:
    for path in [PLAYER_GD, EDRIN_GD, EDRIN_TSCN, ATELIER_NPC_GD, ATELIER_NPC_TSCN, MAP_LAYER_GD, BLUEPRINT_GD]:
        require_path(path, failures)
    player_source = PLAYER_GD.read_text(encoding="utf-8") if PLAYER_GD.exists() else ""
    edrin_source = EDRIN_GD.read_text(encoding="utf-8") if EDRIN_GD.exists() else ""
    edrin_scene = EDRIN_TSCN.read_text(encoding="utf-8") if EDRIN_TSCN.exists() else ""
    atelier_npc_source = ATELIER_NPC_GD.read_text(encoding="utf-8") if ATELIER_NPC_GD.exists() else ""
    atelier_npc_scene = ATELIER_NPC_TSCN.read_text(encoding="utf-8") if ATELIER_NPC_TSCN.exists() else ""
    map_source = MAP_LAYER_GD.read_text(encoding="utf-8") if MAP_LAYER_GD.exists() else ""
    blueprint_source = BLUEPRINT_GD.read_text(encoding="utf-8") if BLUEPRINT_GD.exists() else ""

    if "player_wayfarer_atelier_g422r_v1.png" not in player_source:
        failures.append("Player.gd must use the G-4.22R atelier player atlas")
    if "player_wayfarer_foundation_g419_v1.png" in player_source:
        failures.append("Player.gd still references the superseded G-4.19 player atlas")
    if "newport_npc_atelier_g422r_v1.png" not in edrin_source:
        failures.append("EdrinVale.gd must use the G-4.22R NPC atlas")
    if 'node name="Visual" type="AnimatedSprite2D"' not in edrin_scene:
        failures.append("EdrinVale.tscn must have an AnimatedSprite2D visual child after G-8")
    if 'node name="GroundShadow" type="Polygon2D"' not in edrin_scene:
        failures.append("EdrinVale.tscn must include a grounded shadow treatment after G-8")
    for forbidden in ["func _draw()", "draw_circle", "draw_rect", "draw_line"]:
        if forbidden in edrin_source:
            failures.append(f"EdrinVale.gd still contains primitive placeholder drawing: {forbidden}")
        if forbidden in atelier_npc_source:
            failures.append(f"AtelierTownNpc.gd contains primitive placeholder drawing: {forbidden}")
    if "newport_npc_atelier_g422r_v1.png" not in atelier_npc_source:
        failures.append("AtelierTownNpc.gd must use the G-4.22R NPC atlas")
    if "npc_population_contract" not in atelier_npc_source or "stationary_work_pose_until_dedicated_walk_sheets" not in atelier_npc_source:
        failures.append("AtelierTownNpc.gd must expose the G-8A population/no-glide contract")
    if 'node name="Visual" type="AnimatedSprite2D"' not in atelier_npc_scene:
        failures.append("AtelierTownNpc.tscn must have an AnimatedSprite2D visual child")
    if 'node name="GroundShadow" type="Polygon2D"' not in atelier_npc_scene:
        failures.append("AtelierTownNpc.tscn must include a grounded shadow treatment")
    if "npc_placeholder" in blueprint_source:
        failures.append("NewportTownBlueprint.gd must not expose npc_placeholder anchors in normal play")
    if "npc_atelier" not in blueprint_source:
        failures.append("NewportTownBlueprint.gd must expose npc_atelier anchors")
    for token in ["starter_village_npc_specs", "tavern_keeper", "dockworker", "counting_house_clerk", "merchant_shopkeeper", "rumor_carrier", "suspicious_patron"]:
        if token not in blueprint_source:
            failures.append(f"NewportTownBlueprint.gd missing G-8A NPC token: {token}")
    if "_draw_newport_npc_placeholder" in map_source:
        failures.append("MapLayer.gd must not keep the NPC placeholder draw path")
    g410_start = map_source.find("func _draw_g410_props")
    g423a_start = map_source.find("func _draw_g423a_city_ground_washes")
    if g410_start >= 0 and g423a_start > g410_start:
        g410_props = map_source[g410_start:g423a_start]
        if "_draw_sign_post" in g410_props:
            failures.append("_draw_g410_props must not draw primitive sign posts in normal play")
        if "_draw_newport_npc_placeholder" in g410_props:
            failures.append("_draw_g410_props must not draw primitive NPC placeholders in normal play")
    else:
        failures.append("could not isolate _draw_g410_props for normal-play primitive scan")
    for token in ["NEWPORT_ATELIER_CHARACTER_PLACEMENTS", "newport_atelier_character_materials", "newport_atelier_character_placements"]:
        if token not in map_source:
            failures.append(f"MapLayer.gd missing character audit token: {token}")
    for token in [
        "G422R_SUPPRESS_PRIMITIVE_WORLD_PROPS",
        "G422R_HIDE_NORMAL_PLAY_LAYOUT_GUIDES",
        "G422R_HIDDEN_NORMAL_PLAY_MARKER_ASSETS",
        "g422r_hidden_normal_play_marker_assets",
        "_is_g422r_hidden_normal_play_marker",
    ]:
        if token not in map_source:
            failures.append(f"MapLayer.gd missing hidden-marker gate token: {token}")
    for asset_id in [
        "atelier_sign_tavern_inn_placeholder_01",
        "atelier_sign_painted_shop_plaque_01",
        "atelier_g418e_tavern_hanging_inn_sign_01",
        "atelier_g418e_commercial_mercantile_sign_01",
        "atelier_g418e_commercial_fishmonger_sign_01",
    ]:
        if asset_id not in map_source:
            failures.append(f"MapLayer.gd hidden normal-play list missing low-bar marker/sign asset: {asset_id}")
    for func_name in ["func _draw_g415_lane_connections", "func _draw_g423a_lot_threshold_overlays"]:
        start = map_source.find(func_name)
        if start < 0:
            failures.append(f"MapLayer.gd missing {func_name}")
            continue
        end = map_source.find("\nfunc ", start + 1)
        body = map_source[start:] if end < 0 else map_source[start:end]
        if "G422R_HIDE_NORMAL_PLAY_LAYOUT_GUIDES" not in body:
            failures.append(f"{func_name} must hide layout-guide overlays in normal G-4.22R play")
    for func_name in ["func _draw_g420b_town_identity_accents", "func _draw_g418e_hero_asset_family_accents"]:
        start = map_source.find(func_name)
        if start < 0:
            failures.append(f"MapLayer.gd missing {func_name}")
            continue
        end = map_source.find("\nfunc ", start + 1)
        body = map_source[start:] if end < 0 else map_source[start:end]
        if "_is_g422r_hidden_normal_play_marker" not in body:
            failures.append(f"{func_name} must skip hidden normal-play marker assets")


def validate_artifacts(failures: list[str]) -> None:
    for path in [PLAYER_ATLAS, NPC_ATLAS, CONTACT_SHEET, SOURCE_IMAGE, SOURCE_PROMPT, SIGN_CONTACT, WAYFINDING_CONTACT]:
        require_path(path, failures)
    require_image(PLAYER_ATLAS, failures)
    require_image(NPC_ATLAS, failures)
    require_image(CONTACT_SHEET, failures)
    require_image(SOURCE_IMAGE, failures)


def validate_screenshots(failures: list[str]) -> None:
    manifest = load_json(SCREENSHOT_MANIFEST, failures)
    if not isinstance(manifest, dict):
        return
    if manifest.get("status") != "PASS":
        failures.append("G-4.22R screenshot manifest status must be PASS")
    screenshots = manifest.get("screenshots", [])
    if not isinstance(screenshots, list):
        failures.append("G-4.22R screenshots must be a list")
        return
    targets = {str(item.get("target", "")) for item in screenshots if isinstance(item, dict)}
    missing = sorted(REQUIRED_SCREENSHOT_TARGETS - targets)
    if missing:
        failures.append("G-4.22R screenshot manifest missing targets: " + ", ".join(missing))
    for item in screenshots:
        if not isinstance(item, dict):
            continue
        if item.get("status") != "PASS":
            failures.append(f"screenshot target failed: {item.get('target')}")
        path_text = str(item.get("absolute_path", "")) or str(item.get("path", ""))
        if path_text:
            path = Path(path_text) if Path(path_text).is_absolute() else PROJECT_ROOT / path_text.replace("res://", "")
            require_path(path, failures)


def main() -> int:
    failures: list[str] = []
    validate_manifest(failures)
    validate_registry(failures)
    validate_runtime_references(failures)
    validate_artifacts(failures)
    validate_screenshots(failures)
    if failures:
        print("FAIL: G-4.22R runtime asset consistency")
        for failure in failures:
            print(" - " + failure)
        return 1
    print("PASS: G-4.22R runtime asset consistency")
    print(f"Manifest: {rel(MANIFEST_PATH)}")
    print(f"Screenshots: {rel(SCREENSHOT_MANIFEST)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
