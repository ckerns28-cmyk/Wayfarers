#!/usr/bin/env python3
"""Validate Newport asset manifest and provenance gates."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[3]
PIPELINE_ROOT = PROJECT_ROOT / "art_pipeline" / "newport"
MANIFEST_PATH = PIPELINE_ROOT / "manifests" / "newport_asset_manifest.json"
LEGACY_MANIFEST_PATH = PIPELINE_ROOT / "manifests" / "newport_hero_street_assets.json"
BUILDING_PROVENANCE_PATH = PIPELINE_ROOT / "manifests" / "newport_building_sprite_provenance.json"
VISUAL_REGISTRY_PATH = PIPELINE_ROOT / "manifests" / "newport_visual_production_registry.json"
AUDIT_PATH = PIPELINE_ROOT / "reports" / "G417_G418_ASSET_PROVENANCE_AUDIT.md"
BUILDING_AUDIT_PATH = PIPELINE_ROOT / "reports" / "G418A_BUILDING_SPRITE_PROVENANCE_AUDIT.md"
VISUAL_PRODUCTION_AUDIT_PATH = PIPELINE_ROOT / "reports" / "G419B_NEWPORT_VISUAL_PRODUCTION_AUDIT.md"
GREEN_ORIGIN_ROOT = PROJECT_ROOT / "art_pipeline" / "newport_green_origin"
GREEN_ORIGIN_MANIFEST_PATH = GREEN_ORIGIN_ROOT / "manifests" / "green_origin_asset_manifest.json"
GREEN_ORIGIN_BAKEOFF_MANIFEST_PATH = GREEN_ORIGIN_ROOT / "manifests" / "green_origin_method_bakeoff_manifest.json"
GREEN_ORIGIN_REPORT_PATH = GREEN_ORIGIN_ROOT / "reports" / "G418B_GREEN_ORIGIN_ASSET_FACTORY.md"
GREEN_ORIGIN_BAKEOFF_REPORT_PATH = GREEN_ORIGIN_ROOT / "reports" / "G418D_GREEN_ORIGIN_METHOD_BAKEOFF.md"
GREEN_ORIGIN_CAPABILITY_REPORT_PATH = GREEN_ORIGIN_ROOT / "reports" / "G418D2_ART_PRODUCTION_CAPABILITY_GATE.md"
ATELIER_ROOT = PROJECT_ROOT / "art_pipeline" / "newport_atelier"
ATELIER_MANIFEST_PATH = ATELIER_ROOT / "manifests" / "newport_atelier_cargo_manifest.json"
ATELIER_QA_REPORT_PATH = ATELIER_ROOT / "reports" / "newport_atelier_cargo_extraction_qa.json"
ATELIER_STANDARD_REPORT_PATH = ATELIER_ROOT / "reports" / "G418D_ATELIER_CARGO_STANDARD.md"
ATELIER_DOCK_CLUTTER_MANIFEST_PATH = ATELIER_ROOT / "manifests" / "newport_atelier_dock_clutter_manifest.json"
ATELIER_DOCK_CLUTTER_QA_REPORT_PATH = ATELIER_ROOT / "reports" / "newport_atelier_dock_clutter_extraction_qa.json"
ATELIER_DOCK_CLUTTER_REPORT_PATH = ATELIER_ROOT / "reports" / "G419A_NEWPORT_DOCK_CLUTTER_ATELIER_PACK.md"
ATELIER_G420A_WAVE_MANIFEST_PATH = ATELIER_ROOT / "manifests" / "newport_atelier_environmental_believability_manifest.json"
ATELIER_G420A_WAVE_REPORT_PATH = ATELIER_ROOT / "reports" / "G420A_NEWPORT_ENVIRONMENTAL_BELIEVABILITY_ATELIER_WAVE.md"
ATELIER_G420B_WAVE_MANIFEST_PATH = ATELIER_ROOT / "manifests" / "newport_atelier_town_identity_manifest.json"
ATELIER_G420B_WAVE_REPORT_PATH = ATELIER_ROOT / "reports" / "G420B_NEWPORT_TOWN_IDENTITY_ATELIER_WAVE.md"
ATELIER_G421A_WAVE_MANIFEST_PATH = ATELIER_ROOT / "manifests" / "newport_atelier_core_building_rebuild_wave_1_manifest.json"
ATELIER_G421A_WAVE_REPORT_PATH = ATELIER_ROOT / "reports" / "G421A_NEWPORT_CORE_BUILDING_ATELIER_REBUILD_WAVE_1.md"
ATELIER_G418E_WAVE_MANIFEST_PATH = ATELIER_ROOT / "manifests" / "newport_atelier_g418e_hero_asset_family_manifest.json"
ATELIER_G418E_WAVE_REPORT_PATH = ATELIER_ROOT / "reports" / "G418E_GREEN_ORIGIN_HERO_ASSET_FAMILY.md"
BUILDING_CATALOG_PATH = PROJECT_ROOT / "scripts" / "BuildingCatalog.gd"
TOWN_BLUEPRINT_PATH = PROJECT_ROOT / "scripts" / "NewportTownBlueprint.gd"
MAP_LAYER_PATH = PROJECT_ROOT / "scenes" / "map" / "MapLayer.gd"
ISOLATED_BUILDING_DIR = PROJECT_ROOT / "assets" / "sprites" / "buildings" / "isolated"
ORIGIN_TAXONOMY = {"temporary_review_yellow", "green_origin_candidate", "final_commercial_green", "red_unsafe"}
VISUAL_REGISTRY_STATUS_TAXONOMY = {
    "APPROVED_FINAL",
    "APPROVED_TEMPORARY",
    "NEEDS_REWORK",
    "REBUILD_REQUIRED",
    "REBUILD_REQUIRED_CENTERPIECE",
    "DEPRECATED_DO_NOT_USE",
    "PROVENANCE_UNKNOWN",
}
FINAL_PROVENANCE_STATUSES = {"final_commercial_green", "approved_final_project_owned"}
ATELIER_REQUIRED_ARTIFACT_FIELDS = [
    "manifest",
    "source_image",
    "generation_prompt",
    "extraction_script",
    "atlas",
    "contact_sheet",
    "validation_report",
    "provenance_report",
]
ATELIER_G420A_PACK_IDS = {
    "terrain_edge_dressing",
    "cobble_path_transition",
    "shoreline_harbor_edge",
    "building_grounding_service",
}
ATELIER_G420B_PACK_IDS = {
    "sign_shop_markers",
    "lamps_wayfinding",
    "civic_market_identity",
    "shopfront_support_accents",
}
ATELIER_G421A_PACK_IDS = {"core_building_rebuild_wave_1"}
ATELIER_G418E_PACK_IDS = {
    "tavern_inn_district",
    "commercial_avenue",
    "harbor_dock_edge",
    "rear_service_connector",
}
G421A_REQUIRED_BUILDING_ASSETS = {
    "atelier_newport_tavern_inn_hero_01",
    "atelier_newport_mercantile_store_01",
    "atelier_newport_wharf_warehouse_01",
    "atelier_newport_harbor_cottage_gabled_01",
    "atelier_newport_harbor_cottage_dormer_01",
    "atelier_newport_cooperage_workshop_01",
}
G421A_BUILDING_ID_TO_ASSET = {
    "b_inn_tavern": "atelier_newport_tavern_inn_hero_01",
    "b_mercantile": "atelier_newport_mercantile_store_01",
    "b_dock_warehouse": "atelier_newport_wharf_warehouse_01",
    "b_res_small": "atelier_newport_harbor_cottage_gabled_01",
    "b_boarding_house": "atelier_newport_harbor_cottage_dormer_01",
    "b_cooperage_shed": "atelier_newport_cooperage_workshop_01",
}
G421A_TAVERN_ASSET_ID = "atelier_newport_tavern_inn_hero_01"
GREEN_ORIGIN_FORBIDDEN_INPUTS = [
    "assets/sprites/buildings/isolated",
    "assets/buildings",
    "art_pipeline/newport/atlases/newport_hero_street_atlas_v1.png",
    "art_pipeline/newport/generated_assets",
    "art_pipeline/newport/source_refs",
    "hearthvale",
    "yellow",
    "uncertain",
    "marketplace",
    "web-scraped",
    "ripped",
]


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)
    print(f"FAIL: {message}")


def pass_check(message: str) -> None:
    print(f"PASS: {message}")


def warn(message: str) -> None:
    print(f"WARN: {message}")


def load_json(path: Path, failures: list[str]) -> dict:
    if not path.exists():
        fail(f"missing JSON file: {path}", failures)
        return {}
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON {path}: {exc}", failures)
        return {}
    if not isinstance(parsed, dict):
        fail(f"JSON root is not object: {path}", failures)
        return {}
    pass_check(f"loaded {path.relative_to(PROJECT_ROOT)}")
    return parsed


def read_text(path: Path, failures: list[str]) -> str:
    if not path.exists():
        fail(f"missing text file: {path}", failures)
        return ""
    return path.read_text(encoding="utf-8")


def path_exists(rel_path: str, failures: list[str]) -> None:
    if not rel_path:
        fail("empty manifest path", failures)
        return
    full_path = PROJECT_ROOT / rel_path
    if full_path.exists():
        pass_check(f"path exists: {rel_path}")
    else:
        fail(f"path missing: {rel_path}", failures)


def _is_key_magenta(r: int, g: int, b: int, a: int) -> bool:
    return a > 0 and r > 170 and b > 170 and g < 150 and abs(r - b) < 120


def _is_magenta_halo(r: int, g: int, b: int, a: int) -> bool:
    return a > 0 and r >= 120 and b >= 120 and g <= 115 and abs(r - b) <= 80 and min(r, b) - g >= 38


def image_alpha_metrics(path: Path) -> dict:
    image = Image.open(path).convert("RGBA")
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        return {
            "size": {"w": image.width, "h": image.height},
            "alpha_bbox": None,
            "alpha_pixels": 0,
            "magenta_pixels_remaining": 0,
            "magenta_halo_pixels": 0,
            "crop_padding": {"left": 0, "top": 0, "right": 0, "bottom": 0},
            "cutoff_edges": ["empty_alpha"],
            "readable": False,
        }

    pixels = image.load()
    alpha_pixels = 0
    magenta_pixels = 0
    halo_pixels = 0
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            if a <= 0:
                continue
            alpha_pixels += 1
            if _is_key_magenta(r, g, b, a):
                magenta_pixels += 1
            if not _is_magenta_halo(r, g, b, a):
                continue
            near_transparent = False
            for ny in range(max(0, y - 1), min(image.height, y + 2)):
                for nx in range(max(0, x - 1), min(image.width, x + 2)):
                    if nx == x and ny == y:
                        continue
                    if pixels[nx, ny][3] <= 8:
                        near_transparent = True
                        break
                if near_transparent:
                    break
            if near_transparent:
                halo_pixels += 1

    padding = {
        "left": bbox[0],
        "top": bbox[1],
        "right": image.width - bbox[2],
        "bottom": image.height - bbox[3],
    }
    bbox_w = bbox[2] - bbox[0]
    bbox_h = bbox[3] - bbox[1]
    return {
        "size": {"w": image.width, "h": image.height},
        "alpha_bbox": {"x": bbox[0], "y": bbox[1], "w": bbox_w, "h": bbox_h},
        "alpha_pixels": alpha_pixels,
        "magenta_pixels_remaining": magenta_pixels,
        "magenta_halo_pixels": halo_pixels,
        "crop_padding": padding,
        "cutoff_edges": [side for side, value in padding.items() if value < 6],
        "readable": alpha_pixels >= 1200 and bbox_w >= 48 and bbox_h >= 40,
    }


def validate_manifest(manifest: dict, failures: list[str]) -> None:
    if manifest.get("schema_id") != "wayfarer.newport.asset_manifest.v2":
        fail("manifest schema_id must be wayfarer.newport.asset_manifest.v2", failures)
    else:
        pass_check("manifest schema id")

    gate = str(manifest.get("source_policy", ""))
    if "Temporary yellow review art" in gate and "green-origin assets" in gate:
        pass_check("permanent yellow/green provenance gate recorded")
    else:
        fail("source_policy must include the G-4.18B yellow/prototype vs green/final gate", failures)
    if "Green-origin is necessary but not sufficient" not in str(manifest.get("visual_quality_gate", "")):
        fail("manifest must include the G-4.18C visual quality gate", failures)

    path_exists(str(manifest.get("atlas", "")), failures)
    path_exists(str(manifest.get("generated_asset_root", "")), failures)

    assets = manifest.get("assets", [])
    if not isinstance(assets, list) or len(assets) < 12:
        fail("manifest must contain at least 12 Newport generated assets", failures)
        return
    pass_check(f"asset count: {len(assets)}")

    seen: set[str] = set()
    required_fields = [
        "asset_id",
        "material_category",
        "source_file",
        "generated_piece_file",
        "source",
        "atlas_region",
        "intended_scale",
        "collision_behavior",
        "y_sort_behavior",
        "contact_shadow_required",
        "visual_cohesion_status",
        "visual_quality_status",
        "provenance_status",
        "placeholder",
        "final",
        "review_eligible",
        "normal_review_eligible",
        "lab_only",
        "license_ownership_status",
        "source_pixels_from_prior_wayfarer_assets",
        "source_pixels_from_project_owned_wayfarer_assets",
        "source_pixels_from_third_party_material",
        "origin_classification",
        "commercial_use_status",
        "final_commercial_candidate",
        "final_commercial_eligible",
        "source_pixels_from_yellow_uncertain_assets",
    ]
    for asset in assets:
        if not isinstance(asset, dict):
            fail("asset entry is not an object", failures)
            continue
        asset_id = str(asset.get("asset_id", ""))
        if not asset_id:
            fail("asset missing asset_id", failures)
            continue
        if asset_id in seen:
            fail(f"duplicate asset id: {asset_id}", failures)
        seen.add(asset_id)
        for field in required_fields:
            if field not in asset:
                fail(f"{asset_id} missing field {field}", failures)
        if asset.get("visual_cohesion_status") != "g418_review_candidate":
            fail(f"{asset_id} visual_cohesion_status must be g418_review_candidate", failures)
        if asset.get("visual_quality_status") != "temporary_review_visual_accepted":
            fail(f"{asset_id} visual_quality_status must be temporary_review_visual_accepted", failures)
        if asset.get("provenance_status") != "temporary_review_yellow":
            fail(f"{asset_id} provenance_status must be temporary_review_yellow after G-4.18A", failures)
        if asset.get("origin_classification") != "temporary_review_yellow":
            fail(f"{asset_id} origin_classification must be temporary_review_yellow", failures)
        if asset.get("commercial_use_status") != "temporary_review_yellow":
            fail(f"{asset_id} commercial_use_status must be temporary_review_yellow", failures)
        if asset.get("final_commercial_candidate") is not False:
            fail(f"{asset_id} must not be a final commercial candidate while yellow-source derived", failures)
        if asset.get("source_pixels_from_yellow_uncertain_assets") is not True:
            fail(f"{asset_id} must declare yellow/uncertain source influence", failures)
        if asset.get("placeholder") is not False:
            fail(f"{asset_id} must not be placeholder in review manifest", failures)
        if asset.get("review_eligible") is not True:
            fail(f"{asset_id} must be review_eligible", failures)
        if asset.get("normal_review_eligible") is not True:
            fail(f"{asset_id} must be normal_review_eligible as temporary yellow baseline", failures)
        if asset.get("lab_only") is not False:
            fail(f"{asset_id} must not be lab_only in the normal temporary-yellow baseline", failures)
        if asset.get("final_commercial_eligible") is not False:
            fail(f"{asset_id} final_commercial_eligible must be false while yellow-source derived", failures)
        if asset.get("source_pixels_from_prior_wayfarer_assets") not in [True, False]:
            fail(f"{asset_id} must explicitly declare whether project-owned Wayfarer source pixels were copied", failures)
        if asset.get("source_pixels_from_project_owned_wayfarer_assets") not in [True, False]:
            fail(f"{asset_id} must explicitly declare project-owned Wayfarer source pixel use", failures)
        if asset.get("source_pixels_from_third_party_material") is not False:
            fail(f"{asset_id} copied third-party source pixels", failures)
        path_exists(str(asset.get("source_file", "")), failures)
        path_exists(str(asset.get("generated_piece_file", "")), failures)

        source = asset.get("source", {})
        if not isinstance(source, dict):
            fail(f"{asset_id} source must be an object", failures)
            continue
        if source.get("ownership") != "project-owned":
            fail(f"{asset_id} source ownership must be project-owned", failures)
        if source.get("type") != "deterministic_generated_bitmap":
            fail(f"{asset_id} source type must be deterministic_generated_bitmap", failures)
        if source.get("prior_project_prop_sources") != []:
            fail(f"{asset_id} prior_project_prop_sources must be empty for G-4.18 review", failures)
        if source.get("source_pixels_from_prior_wayfarer_assets") not in [True, False]:
            fail(f"{asset_id} source must explicitly declare project-owned Wayfarer source pixel use", failures)
        if source.get("source_pixels_from_project_owned_wayfarer_assets") not in [True, False]:
            fail(f"{asset_id} source must explicitly declare project-owned Wayfarer source pixel use", failures)
        if source.get("source_pixels_from_third_party_material") is not False:
            fail(f"{asset_id} source copied third-party pixels", failures)
        if source.get("source_pixels_from_yellow_uncertain_assets") is not True:
            fail(f"{asset_id} source must declare yellow/uncertain Newport source influence", failures)
        if source.get("green_origin_candidate") is True:
            fail(f"{asset_id} cannot be green_origin_candidate because it uses yellow-source influence", failures)
        if "no third-party" not in str(source.get("license", "")).lower():
            fail(f"{asset_id} license text must forbid third-party pixels", failures)
        license_text = str(source.get("license", "")).lower()
        if "temporary review" not in license_text and "temporary yellow review" not in license_text:
            fail(f"{asset_id} license text must mark yellow-source assets as temporary review only", failures)
        path_exists(str(source.get("exact_source_path", "")), failures)

        material_sources = source.get("material_sources", [])
        if not isinstance(material_sources, list):
            fail(f"{asset_id} material_sources must be a list", failures)
            continue
        if source.get("source_pixels_from_project_owned_wayfarer_assets") is True and len(material_sources) == 0:
            fail(f"{asset_id} declares project-owned source pixels but has no material_sources", failures)
        for crop in material_sources:
            if not isinstance(crop, dict):
                fail(f"{asset_id} material source is not an object", failures)
                continue
            if "project-owned" not in str(crop.get("ownership", "")):
                fail(f"{asset_id} crop {crop.get('source_crop_id', 'unknown')} ownership must be project-owned", failures)
            if crop.get("third_party_pixels") is not False:
                fail(f"{asset_id} crop {crop.get('source_crop_id', 'unknown')} has third_party_pixels not false", failures)
            file_path = str(crop.get("file", ""))
            if not file_path.startswith("assets/sprites/buildings/isolated/"):
                fail(f"{asset_id} crop {crop.get('source_crop_id', 'unknown')} must come from isolated Newport building sprites", failures)
            path_exists(file_path, failures)

    if not failures:
        pass_check("all G-4.17/G-4.18 review-facing assets are quarantined as temporary yellow")


def _extract_quoted_list(source: str, const_name: str) -> list[str]:
    marker = f"const {const_name} := ["
    start = source.find(marker)
    if start < 0:
        return []
    start = source.find("[", start)
    end = source.find("]", start)
    if end < 0:
        return []
    block = source[start:end]
    return [part.split('"', 2)[1] for part in block.splitlines() if '"' in part]


def _extract_building_sprite_ids(source: str) -> dict[str, str]:
    mapping: dict[str, str] = {}
    current_building_id = ""
    for line in source.splitlines():
        stripped = line.strip()
        if stripped.startswith('"b_') and stripped.endswith(":"):
            current_building_id = stripped.strip('":')
            continue
        if current_building_id and "return _definition(building_id," in stripped:
            parts = stripped.split('"')
            if len(parts) >= 4:
                mapping[current_building_id] = parts[3]
            current_building_id = ""
    return mapping


def validate_building_sprite_provenance(failures: list[str]) -> None:
    manifest = load_json(BUILDING_PROVENANCE_PATH, failures)
    if not manifest:
        return
    if manifest.get("schema_id") != "wayfarer.newport.building_sprite_provenance.v1":
        fail("building provenance manifest schema_id must be wayfarer.newport.building_sprite_provenance.v1", failures)
    else:
        pass_check("building provenance manifest schema id")

    assets = manifest.get("assets", [])
    if not isinstance(assets, list):
        fail("building provenance manifest assets must be a list", failures)
        return
    by_id = {str(asset.get("asset_id", "")): asset for asset in assets if isinstance(asset, dict)}
    by_filename = {str(asset.get("filename", "")): asset for asset in assets if isinstance(asset, dict)}
    pass_check(f"building provenance entries: {len(by_id)}")

    required_fields = [
        "asset_id",
        "filename",
        "source_type",
        "created_by",
        "source_tool",
        "source_prompt_or_script_path",
        "source_commit",
        "license",
        "ownership",
        "third_party_reference_used",
        "reverse_search_status",
        "commercial_use_status",
        "review_eligible",
        "provenance_status",
        "origin_classification",
        "visual_quality_status",
        "normal_review_eligible",
        "lab_only",
        "provenance_classification",
        "final_commercial_candidate",
        "final_commercial_eligible",
        "source_pixel_policy",
        "notes",
    ]
    for asset_id, asset in by_id.items():
        for field in required_fields:
            if field not in asset:
                fail(f"{asset_id} missing building provenance field {field}", failures)
        status = str(asset.get("commercial_use_status", "")).lower()
        classification = str(asset.get("provenance_classification", "")).lower()
        if status not in {"green", "yellow", "red", "unknown"}:
            fail(f"{asset_id} commercial_use_status must be green, yellow, red, or unknown", failures)
        if classification and classification not in ORIGIN_TAXONOMY:
            fail(f"{asset_id} provenance_classification must use the G-4.18B taxonomy", failures)
        if status in {"red", "unknown"} and asset.get("review_eligible") is True:
            fail(f"{asset_id} is {status} but still review_eligible", failures)
        if status == "yellow":
            warn(f"{asset_id} is temporary review art only; not final/commercial eligible")
            if asset.get("provenance_status") != "temporary_review_yellow":
                fail(f"{asset_id} yellow status must set provenance_status=temporary_review_yellow", failures)
            if asset.get("origin_classification") != "temporary_review_yellow":
                fail(f"{asset_id} yellow status must set origin_classification=temporary_review_yellow", failures)
            if asset.get("visual_quality_status") not in {"temporary_review_visual_accepted", "visual_review_pending"}:
                fail(f"{asset_id} yellow status must record visual_quality_status", failures)
            if asset.get("lab_only") is not False:
                fail(f"{asset_id} yellow building sprites must not be lab_only", failures)
            if asset.get("active_normal_review") is True and asset.get("review_eligible") is True and asset.get("normal_review_eligible") is not True:
                fail(f"{asset_id} active yellow baseline sprite must set normal_review_eligible=true", failures)
            if asset.get("final_commercial_eligible") is not False:
                fail(f"{asset_id} yellow status must set final_commercial_eligible=false", failures)
            if classification != "temporary_review_yellow":
                fail(f"{asset_id} yellow status must set provenance_classification=temporary_review_yellow", failures)
            if asset.get("final_commercial_candidate") is not False:
                fail(f"{asset_id} yellow status must set final_commercial_candidate=false", failures)
            if "cannot be used as source pixels" not in str(asset.get("source_pixel_policy", "")).lower():
                fail(f"{asset_id} source_pixel_policy must block yellow pixels from green final art", failures)
        filename = str(asset.get("filename", ""))
        if filename.endswith(".png") and not filename.startswith("assets/buildings/"):
            path_exists(str(asset.get("path", f"assets/sprites/buildings/isolated/{filename}")), failures)

    isolated_files = sorted(path.name for path in ISOLATED_BUILDING_DIR.glob("*.png"))
    for filename in isolated_files:
        if filename not in by_filename:
            fail(f"isolated building sprite lacks provenance entry: {filename}", failures)
    if isolated_files:
        pass_check(f"isolated building sprites inventoried: {len(isolated_files)}")

    catalog = read_text(BUILDING_CATALOG_PATH, failures)
    blueprint = read_text(TOWN_BLUEPRINT_PATH, failures)
    active_building_ids = _extract_quoted_list(blueprint, "STARTER_HARBOR_BUILDING_IDS")
    building_to_sprite = _extract_building_sprite_ids(catalog)
    missing_active: list[str] = []
    for building_id in active_building_ids:
        sprite_id = building_to_sprite.get(building_id, "")
        if not sprite_id or sprite_id not in by_id:
            missing_active.append(f"{building_id}:{sprite_id or 'unknown'}")
            continue
        entry = by_id[sprite_id]
        if entry.get("active_normal_review") is not True:
            fail(f"active building sprite is not marked active_normal_review: {building_id}:{sprite_id}", failures)
        if entry.get("final_commercial_eligible") is not False:
            fail(f"active building sprite must not bypass final commercial review: {building_id}:{sprite_id}", failures)
    if missing_active:
        fail("active normal-review building sprites missing provenance: " + ", ".join(missing_active), failures)
    else:
        pass_check(f"active normal-review building sprites have provenance: {len(active_building_ids)}")

    if BUILDING_AUDIT_PATH.exists():
        audit = BUILDING_AUDIT_PATH.read_text(encoding="utf-8")
        for required_text in [
            "Building Sprite Provenance Gate",
            "newport_chandlery_outfitter_front_isolated.png",
            "Reverse Search",
            "Replacement Queue",
        ]:
            if required_text not in audit:
                fail(f"building audit report missing section/text: {required_text}", failures)
        pass_check("building provenance audit report present")
    else:
        fail(f"missing building provenance audit report: {BUILDING_AUDIT_PATH}", failures)


def validate_green_origin_asset_manifest(failures: list[str]) -> None:
    manifest = load_json(GREEN_ORIGIN_MANIFEST_PATH, failures)
    if not manifest:
        return
    if manifest.get("schema_id") != "wayfarer.newport_green_origin.asset_manifest.v1":
        fail("green-origin manifest schema_id must be wayfarer.newport_green_origin.asset_manifest.v1", failures)
    else:
        pass_check("green-origin manifest schema id")
    if "green-origin provenance is necessary but not sufficient" not in str(manifest.get("visual_quality_gate", "")).lower():
        fail("green-origin manifest missing G-4.18C visual quality gate", failures)
    taxonomy = manifest.get("origin_taxonomy", [])
    for required in sorted(ORIGIN_TAXONOMY):
        if required not in taxonomy:
            fail(f"green-origin manifest taxonomy missing {required}", failures)
    path_exists(str(manifest.get("atlas", "")), failures)
    path_exists(str(manifest.get("generated_asset_root", "")), failures)
    for contact_sheet in manifest.get("contact_sheets", []):
        path_exists(str(contact_sheet), failures)

    assets = manifest.get("assets", [])
    if not isinstance(assets, list):
        fail("green-origin manifest assets must be a list", failures)
        return
    if len(assets) < 4:
        fail("green-origin manifest must contain a small proof asset family", failures)
    else:
        pass_check(f"green-origin asset entries: {len(assets)}")

    required_fields = [
        "asset_id",
        "asset_type",
        "source_type",
        "created_by",
        "generation_script",
        "input_sources",
        "license",
        "ownership",
        "commercial_use_status",
        "provenance_status",
        "origin_classification",
        "visual_quality_status",
        "review_eligible",
        "normal_review_eligible",
        "lab_only",
        "final_commercial_candidate",
        "final_commercial_eligible",
        "notes",
    ]
    for asset in assets:
        if not isinstance(asset, dict):
            fail("green-origin asset entry is not an object", failures)
            continue
        asset_id = str(asset.get("asset_id", ""))
        for field in required_fields:
            if field not in asset:
                fail(f"{asset_id or 'unknown'} missing green-origin field {field}", failures)
        path_exists(str(asset.get("path", "")), failures)
        path_exists(str(asset.get("generation_script", "")), failures)
        if asset.get("ownership") != "project-owned":
            fail(f"{asset_id} ownership must be project-owned", failures)
        status = str(asset.get("commercial_use_status", ""))
        if status not in {"green_origin_candidate", "final_commercial_green"}:
            fail(f"{asset_id} commercial_use_status must be green_origin_candidate or final_commercial_green", failures)
        if asset.get("provenance_status") != "green_origin_candidate":
            fail(f"{asset_id} provenance_status must stay green_origin_candidate", failures)
        if asset.get("origin_classification") != "green_origin_candidate":
            fail(f"{asset_id} origin_classification must stay green_origin_candidate", failures)
        if asset.get("visual_quality_status") != "visual_failed_g418b_proof":
            fail(f"{asset_id} visual_quality_status must be visual_failed_g418b_proof", failures)
        if asset.get("review_eligible") is not False:
            fail(f"{asset_id} review_eligible must be false after visual quarantine", failures)
        if asset.get("normal_review_eligible") is not False:
            fail(f"{asset_id} normal_review_eligible must be false after visual quarantine", failures)
        if asset.get("lab_only") is not True:
            fail(f"{asset_id} lab_only must be true after visual quarantine", failures)
        if asset.get("final_commercial_candidate") is not False:
            fail(f"{asset_id} final_commercial_candidate must be false while visual failed", failures)
        if asset.get("final_commercial_eligible") is not False:
            fail(f"{asset_id} final_commercial_eligible must be false while visual failed", failures)
        if asset.get("source_pixels_from_yellow_uncertain_assets") is not False:
            fail(f"{asset_id} uses yellow/uncertain source pixels", failures)
        if asset.get("source_pixels_from_third_party_material") is not False:
            fail(f"{asset_id} uses third-party source pixels", failures)
        if asset.get("web_scraped_source_pixels") is not False:
            fail(f"{asset_id} uses web-scraped source pixels", failures)
        for raw_source in asset.get("input_sources", []):
            if not isinstance(raw_source, dict):
                fail(f"{asset_id} input source is not an object", failures)
                continue
            source_text = json.dumps(raw_source, sort_keys=True).lower()
            for forbidden in GREEN_ORIGIN_FORBIDDEN_INPUTS:
                if forbidden.lower() in source_text:
                    fail(f"{asset_id} forbidden green-origin input source: {forbidden}", failures)
            if raw_source.get("source_pixels_used") is not False:
                fail(f"{asset_id} green-origin input source uses source pixels", failures)
            if "path" in raw_source:
                path_exists(str(raw_source["path"]), failures)

    if GREEN_ORIGIN_REPORT_PATH.exists():
        report = GREEN_ORIGIN_REPORT_PATH.read_text(encoding="utf-8")
        for required_text in ["green_origin_candidate", "No yellow Newport building sprite", "Godot Proof Area"]:
            if required_text not in report:
                fail(f"green-origin report missing text: {required_text}", failures)
        pass_check("green-origin report present")
    else:
        fail(f"missing green-origin report: {GREEN_ORIGIN_REPORT_PATH}", failures)


def validate_green_origin_bakeoff_manifest(failures: list[str]) -> None:
    manifest = load_json(GREEN_ORIGIN_BAKEOFF_MANIFEST_PATH, failures)
    if not manifest:
        return
    if manifest.get("schema_id") != "wayfarer.newport_green_origin.method_bakeoff.v1":
        fail("green-origin bakeoff manifest schema_id must be wayfarer.newport_green_origin.method_bakeoff.v1", failures)
    else:
        pass_check("green-origin bakeoff manifest schema id")
    if manifest.get("phase") != "G-4.18D.2":
        fail("green-origin bakeoff manifest phase must be G-4.18D.2", failures)
    if manifest.get("recommended_method_for_g418e") is not None:
        fail("green-origin bakeoff/capability manifest must not recommend a promotion method in G-4.18D.2", failures)
    if "No G-4.18D, G-4.18D.1, or G-4.18D.2 experimental/capability asset is normal-review eligible" not in str(manifest.get("normal_review_policy", "")):
        fail("green-origin bakeoff manifest must explicitly block normal review", failures)
    gate_text = str(manifest.get("visual_quality_gate", ""))
    if "8.5" not in gate_text or "7.5" not in gate_text:
        fail("green-origin bakeoff manifest must declare the 8.5 bakeoff and 7.5 capability visual PASS gates", failures)
    for contact_sheet in manifest.get("contact_sheets", []):
        path_exists(str(contact_sheet), failures)

    candidates = manifest.get("candidates", [])
    if not isinstance(candidates, list) or len(candidates) != 6:
        fail("green-origin bakeoff must retain the 5 corrected G-4.18D candidates plus M01B", failures)
        return
    pass_check("green-origin retained bakeoff candidate entries: 6")

    pass_count = 0
    recommendations = {str(candidate.get("recommendation", "")) for candidate in candidates if isinstance(candidate, dict)}
    if "PASS" in recommendations:
        fail("green-origin retained bakeoff must not keep any PASS recommendation below the 8.5 visual gate", failures)
    for required in ["DEFER", "FAIL"]:
        if required not in recommendations:
            fail(f"green-origin bakeoff recommendations missing {required}", failures)
    for candidate in candidates:
        if not isinstance(candidate, dict):
            fail("green-origin bakeoff candidate is not an object", failures)
            continue
        candidate_id = str(candidate.get("candidate_id", "unknown"))
        for field in [
            "candidate_id",
            "method_name",
            "sample_path",
            "phase",
            "provenance_status",
            "origin_classification",
            "commercial_use_status",
            "visual_quality_status",
            "visual_rating",
            "visual_pass_gate",
            "review_eligible",
            "normal_review_eligible",
            "lab_only",
            "final_commercial_candidate",
            "final_commercial_eligible",
            "recommendation",
            "input_sources",
            "source_pixels_from_yellow_uncertain_assets",
            "source_pixels_from_third_party_material",
            "web_scraped_source_pixels",
        ]:
            if field not in candidate:
                fail(f"{candidate_id} missing bakeoff field {field}", failures)
        path_exists(str(candidate.get("sample_path", "")), failures)
        if candidate.get("phase") != "G-4.18D.1":
            fail(f"{candidate_id} retained bakeoff phase must remain G-4.18D.1", failures)
        if candidate.get("provenance_status") != "green_origin_candidate":
            fail(f"{candidate_id} bakeoff provenance_status must be green_origin_candidate", failures)
        if candidate.get("origin_classification") != "green_origin_candidate":
            fail(f"{candidate_id} bakeoff origin_classification must be green_origin_candidate", failures)
        if candidate.get("commercial_use_status") != "green_origin_candidate":
            fail(f"{candidate_id} bakeoff commercial_use_status must be green_origin_candidate", failures)
        if candidate.get("review_eligible") is not False:
            fail(f"{candidate_id} bakeoff review_eligible must be false", failures)
        if candidate.get("normal_review_eligible") is not False:
            fail(f"{candidate_id} bakeoff normal_review_eligible must be false", failures)
        if candidate.get("lab_only") is not True:
            fail(f"{candidate_id} bakeoff lab_only must be true", failures)
        if candidate.get("final_commercial_eligible") is not False:
            fail(f"{candidate_id} bakeoff final_commercial_eligible must be false", failures)
        if candidate.get("source_pixels_from_yellow_uncertain_assets") is not False:
            fail(f"{candidate_id} bakeoff uses yellow/uncertain source pixels", failures)
        if candidate.get("source_pixels_from_third_party_material") is not False:
            fail(f"{candidate_id} bakeoff uses third-party source pixels", failures)
        if candidate.get("web_scraped_source_pixels") is not False:
            fail(f"{candidate_id} bakeoff uses web-scraped source pixels", failures)
        visual_rating = float(candidate.get("visual_rating", 0.0))
        visual_gate = float(candidate.get("visual_pass_gate", 0.0))
        if visual_gate < 8.5:
            fail(f"{candidate_id} bakeoff visual_pass_gate must be at least 8.5", failures)
        if visual_rating < 8.5 and candidate.get("recommendation") == "PASS":
            fail(f"{candidate_id} bakeoff cannot be PASS below the 8.5 visual gate", failures)
        if visual_rating < 8.5 and candidate.get("final_commercial_candidate") is not False:
            fail(f"{candidate_id} bakeoff cannot be final_commercial_candidate below the 8.5 visual gate", failures)
        recommendation = str(candidate.get("recommendation", ""))
        if recommendation == "PASS":
            pass_count += 1
        elif recommendation == "DEFER":
            if "defer" not in str(candidate.get("visual_quality_status", "")):
                fail(f"{candidate_id} DEFER candidate must record defer visual status", failures)
        elif recommendation == "FAIL":
            if "fail" not in str(candidate.get("visual_quality_status", "")):
                fail(f"{candidate_id} FAIL candidate must record visual failure", failures)
        else:
            fail(f"{candidate_id} bakeoff recommendation must be PASS, DEFER, or FAIL", failures)
        for raw_source in candidate.get("input_sources", []):
            if not isinstance(raw_source, dict):
                fail(f"{candidate_id} bakeoff input source is not object", failures)
                continue
            source_text = json.dumps(raw_source, sort_keys=True).lower()
            for forbidden in GREEN_ORIGIN_FORBIDDEN_INPUTS:
                if forbidden.lower() in source_text:
                    fail(f"{candidate_id} forbidden bakeoff input source: {forbidden}", failures)
            source_uses_pixels = raw_source.get("source_pixels_used")
            source_path = str(raw_source.get("path", ""))
            if source_uses_pixels is not False:
                allowed_m01b_substrate = (
                    candidate_id == "method_01b_manual_paintover_proof"
                    and source_uses_pixels is True
                    and source_path.endswith("method_01_generated_base_pixel_cleanup.png")
                )
                if not allowed_m01b_substrate:
                    fail(f"{candidate_id} bakeoff input source uses source pixels: {source_path or 'unknown'}", failures)
            if "path" in raw_source:
                path_exists(str(raw_source["path"]), failures)
    if pass_count != 0:
        fail("green-origin retained bakeoff must have zero PASS recommendations in G-4.18D.2", failures)

    capability = manifest.get("art_production_capability_gate", {})
    if not isinstance(capability, dict) or not capability:
        fail("green-origin manifest must include one G-4.18D.2 art_production_capability_gate object", failures)
    else:
        asset_id = str(capability.get("asset_id", "unknown"))
        required_capability_fields = [
            "phase",
            "asset_id",
            "sample_path",
            "rough_base_path",
            "prepared_path",
            "isolated_proof_path",
            "before_after_path",
            "in_world_comparison_path",
            "source_file",
            "provenance_status",
            "origin_classification",
            "commercial_use_status",
            "visual_quality_status",
            "visual_rating",
            "visual_pass_gate",
            "capability_verdict",
            "review_eligible",
            "normal_review_eligible",
            "lab_only",
            "final_commercial_candidate",
            "final_commercial_eligible",
            "input_sources",
            "source_pixels_from_yellow_uncertain_assets",
            "source_pixels_from_third_party_material",
            "web_scraped_source_pixels",
            "ownership",
            "license",
            "sha256",
            "capability_answer",
        ]
        for field in required_capability_fields:
            if field not in capability:
                fail(f"{asset_id} missing capability field {field}", failures)
        if capability.get("phase") != "G-4.18D.2":
            fail(f"{asset_id} capability phase must be G-4.18D.2", failures)
        for path_field in ["sample_path", "rough_base_path", "prepared_path", "isolated_proof_path", "before_after_path", "in_world_comparison_path", "source_file"]:
            path_exists(str(capability.get(path_field, "")), failures)
        if capability.get("provenance_status") != "green_origin_candidate":
            fail(f"{asset_id} capability provenance_status must be green_origin_candidate", failures)
        if capability.get("origin_classification") != "green_origin_candidate":
            fail(f"{asset_id} capability origin_classification must be green_origin_candidate", failures)
        if capability.get("commercial_use_status") != "green_origin_candidate":
            fail(f"{asset_id} capability commercial_use_status must be green_origin_candidate", failures)
        if capability.get("review_eligible") is not False:
            fail(f"{asset_id} capability review_eligible must be false", failures)
        if capability.get("normal_review_eligible") is not False:
            fail(f"{asset_id} capability normal_review_eligible must be false", failures)
        if capability.get("lab_only") is not True:
            fail(f"{asset_id} capability lab_only must be true", failures)
        if capability.get("final_commercial_eligible") is not False:
            fail(f"{asset_id} capability final_commercial_eligible must be false", failures)
        if capability.get("source_pixels_from_yellow_uncertain_assets") is not False:
            fail(f"{asset_id} capability uses yellow/uncertain source pixels", failures)
        if capability.get("source_pixels_from_third_party_material") is not False:
            fail(f"{asset_id} capability uses third-party source pixels", failures)
        if capability.get("web_scraped_source_pixels") is not False:
            fail(f"{asset_id} capability uses web-scraped source pixels", failures)
        visual_rating = float(capability.get("visual_rating", 0.0))
        visual_gate = float(capability.get("visual_pass_gate", 0.0))
        verdict = str(capability.get("capability_verdict", ""))
        if visual_gate < 7.5:
            fail(f"{asset_id} capability visual_pass_gate must be at least 7.5", failures)
        if visual_rating < 7.5 and verdict == "PASS":
            fail(f"{asset_id} capability cannot PASS below the 7.5 visual gate", failures)
        if visual_rating < 7.5 and capability.get("final_commercial_candidate") is not False:
            fail(f"{asset_id} capability cannot be final_commercial_candidate below the 7.5 visual gate", failures)
        if verdict == "DEFER" and "defer" not in str(capability.get("visual_quality_status", "")):
            fail(f"{asset_id} DEFER capability must record defer visual status", failures)
        if verdict not in ["PASS", "DEFER", "FAIL"]:
            fail(f"{asset_id} capability_verdict must be PASS, DEFER, or FAIL", failures)
        for raw_source in capability.get("input_sources", []):
            if not isinstance(raw_source, dict):
                fail(f"{asset_id} capability input source is not object", failures)
                continue
            source_text = json.dumps(raw_source, sort_keys=True).lower()
            for forbidden in GREEN_ORIGIN_FORBIDDEN_INPUTS:
                if forbidden.lower() in source_text:
                    fail(f"{asset_id} forbidden capability input source: {forbidden}", failures)
            if raw_source.get("source_pixels_used") is not False:
                fail(f"{asset_id} capability input source uses source pixels", failures)
            if "path" in raw_source:
                path_exists(str(raw_source["path"]), failures)

    if GREEN_ORIGIN_BAKEOFF_REPORT_PATH.exists():
        report = GREEN_ORIGIN_BAKEOFF_REPORT_PATH.read_text(encoding="utf-8")
        for required_text in [
            "North Star Relevance",
            "G-4.18D produced no accepted visual candidate",
            "M01 is downgraded",
        ]:
            if required_text not in report:
                fail(f"green-origin bakeoff report missing text: {required_text}", failures)
        pass_check("green-origin bakeoff report present")
    else:
        fail(f"missing green-origin bakeoff report: {GREEN_ORIGIN_BAKEOFF_REPORT_PATH}", failures)

    if GREEN_ORIGIN_CAPABILITY_REPORT_PATH.exists():
        report = GREEN_ORIGIN_CAPABILITY_REPORT_PATH.read_text(encoding="utf-8")
        for required_text in [
            "G-4.18D.2 produced one green-origin rope coil",
            "Was the failure due to tool access?",
            "Was the failure due to art-direction execution?",
            "Was the failure due to Codex not being able to perform finished-art production?",
            "DEFER",
        ]:
            if required_text not in report:
                fail(f"green-origin capability report missing text: {required_text}", failures)
        pass_check("green-origin capability report present")
    else:
        fail(f"missing green-origin capability report: {GREEN_ORIGIN_CAPABILITY_REPORT_PATH}", failures)


def validate_atelier_cargo_manifest(failures: list[str]) -> None:
    manifest = load_json(ATELIER_MANIFEST_PATH, failures)
    if not manifest:
        return
    if manifest.get("schema_id") != "wayfarer.newport_atelier.cargo_manifest.v1":
        fail("atelier cargo manifest schema_id must be wayfarer.newport_atelier.cargo_manifest.v1", failures)
    else:
        pass_check("atelier cargo manifest schema id")
    if manifest.get("phase") != "G-4.18D":
        fail("atelier cargo manifest phase must be G-4.18D", failures)
    if "10/10" not in str(manifest.get("visual_standard", "")):
        fail("atelier cargo manifest must record the 10/10 visual standard", failures)
    if manifest.get("pipeline_status") != "locked_pending_final_license_policy_approval":
        fail("atelier cargo pipeline_status must preserve pending license approval", failures)
    if "AI-assisted" not in str(manifest.get("source_policy", "")):
        fail("atelier cargo source_policy must explicitly describe AI-assisted source handling", failures)
    if "10/10 source sheet" not in str(manifest.get("future_pack_pattern", "")):
        fail("atelier cargo future_pack_pattern must document the reusable pack structure", failures)

    for field in [
        "atlas",
        "source_image",
        "generation_prompt",
        "generated_asset_root",
        "contact_sheet",
        "provenance_report",
        "validation_report",
    ]:
        path_exists(str(manifest.get(field, "")), failures)
    path_exists(str(manifest.get("generated_asset_root", "")), failures)

    deprecated_targets = json.dumps(manifest.get("deprecated_visual_targets", [])).lower()
    if "deterministic" not in deprecated_targets and "procedural" not in deprecated_targets:
        fail("atelier cargo manifest must deprecate the weak deterministic/procedural cargo target", failures)
    rollout = manifest.get("recommended_rollout_order", [])
    for expected in [
        "dock clutter expansion",
        "terrain edge dressing",
        "signs/lamps/posts",
        "market goods/carts",
        "shopfront props",
        "NPC/player standards",
    ]:
        if expected not in rollout:
            fail(f"atelier cargo rollout order missing {expected}", failures)

    qa_report = load_json(ATELIER_QA_REPORT_PATH, failures)
    if qa_report:
        if qa_report.get("schema_id") != "wayfarer.newport_atelier.extraction_qa.v1":
            fail("atelier cargo QA report schema mismatch", failures)
        if qa_report.get("status") != "PASS":
            fail("atelier cargo QA report must be PASS", failures)
        for required_check in [
            "transparent sprites have no magenta background",
            "transparent sprites have no magenta halo on alpha edges",
            "sprites retain clean transparent crop padding",
            "sprites are not cut off at object edges",
            "source sheet object identity maps to manifest asset ids",
        ]:
            if required_check not in qa_report.get("checks", []):
                fail(f"atelier cargo QA report missing check: {required_check}", failures)

    assets = manifest.get("assets", [])
    if not isinstance(assets, list):
        fail("atelier cargo manifest assets must be a list", failures)
        return
    expected_ids = {
        "atelier_newport_crate_01",
        "atelier_newport_barrel_01",
        "atelier_newport_rope_coil_01",
        "atelier_wharf_cargo_cluster_01",
    }
    seen_ids: set[str] = set()
    required_fields = [
        "asset_id",
        "asset_type",
        "source_identity",
        "path",
        "atlas",
        "atlas_region",
        "sprite_size",
        "pivot",
        "grounding",
        "recommended_game_scale",
        "source_type",
        "created_by",
        "generation_prompt",
        "source_image",
        "extraction_script",
        "input_sources",
        "license",
        "ownership",
        "provenance_status",
        "origin_classification",
        "commercial_use_status",
        "review_eligible",
        "normal_review_eligible",
        "lab_only",
        "final_commercial_candidate",
        "final_commercial_eligible",
        "source_pixels_from_yellow_uncertain_assets",
        "source_pixels_from_third_party_material",
        "web_scraped_source_pixels",
        "ai_generated",
        "human_selected",
        "chroma_key_removed",
        "extraction_qa",
        "sha256",
        "notes",
    ]
    for asset in assets:
        if not isinstance(asset, dict):
            fail("atelier cargo asset entry is not an object", failures)
            continue
        asset_id = str(asset.get("asset_id", ""))
        seen_ids.add(asset_id)
        for field in required_fields:
            if field not in asset:
                fail(f"{asset_id or 'unknown'} missing atelier cargo field {field}", failures)
        if asset_id not in expected_ids:
            fail(f"unexpected atelier cargo asset id: {asset_id}", failures)
        if asset.get("source_type") != "ai_assisted_image_generation_with_local_chroma_extraction":
            fail(f"{asset_id} source_type must be AI-assisted image generation plus local extraction", failures)
        if asset.get("provenance_status") != "ai_assisted_green_origin_candidate_pending_license_review":
            fail(f"{asset_id} provenance_status must remain AI-assisted pending license review", failures)
        if asset.get("origin_classification") != "green_origin_candidate_pending_license_review":
            fail(f"{asset_id} origin_classification must remain green_origin_candidate_pending_license_review", failures)
        if asset.get("commercial_use_status") != "green_origin_candidate_pending_license_review":
            fail(f"{asset_id} commercial_use_status must remain pending license review", failures)
        if asset.get("review_eligible") is not True:
            fail(f"{asset_id} must be review_eligible", failures)
        if asset.get("normal_review_eligible") is not True:
            fail(f"{asset_id} must be normal_review_eligible for this visual lock", failures)
        if asset.get("lab_only") is not False:
            fail(f"{asset_id} must not be lab_only after the cargo standard lock", failures)
        if asset.get("final_commercial_candidate") is not False:
            fail(f"{asset_id} must not be marked final_commercial_candidate", failures)
        if asset.get("final_commercial_eligible") is not False:
            fail(f"{asset_id} must not be marked final_commercial_eligible", failures)
        for bool_field in ["source_pixels_from_yellow_uncertain_assets", "source_pixels_from_third_party_material", "web_scraped_source_pixels"]:
            if asset.get(bool_field) is not False:
                fail(f"{asset_id} must set {bool_field}=false", failures)
        if asset.get("ai_generated") is not True or asset.get("human_selected") is not True:
            fail(f"{asset_id} must declare ai_generated and human_selected", failures)
        if asset.get("chroma_key_removed") is not True:
            fail(f"{asset_id} must declare chroma_key_removed", failures)
        asset_rel_path = str(asset.get("path", ""))
        path_exists(asset_rel_path, failures)
        asset_path = PROJECT_ROOT / asset_rel_path
        if asset_path.exists():
            metrics = image_alpha_metrics(asset_path)
            qa = asset.get("extraction_qa", {})
            if metrics.get("magenta_pixels_remaining") != 0:
                fail(f"{asset_id} has magenta background pixels remaining", failures)
            if metrics.get("magenta_halo_pixels") != 0:
                fail(f"{asset_id} has magenta halo pixels", failures)
            if metrics.get("cutoff_edges"):
                fail(f"{asset_id} crop padding/cutoff failed: {metrics.get('cutoff_edges')}", failures)
            if metrics.get("readable") is not True:
                fail(f"{asset_id} alpha footprint is not visually readable", failures)
            for metric_key in ["magenta_pixels_remaining", "magenta_halo_pixels", "cutoff_edges", "readable"]:
                if qa.get(metric_key) != metrics.get(metric_key):
                    fail(f"{asset_id} manifest QA metric {metric_key} does not match image inspection", failures)
        for path_field in ["generation_prompt", "source_image", "extraction_script", "atlas"]:
            path_exists(str(asset.get(path_field, "")), failures)
        if str(asset.get("atlas", "")) != str(manifest.get("atlas", "")):
            fail(f"{asset_id} atlas path does not match manifest atlas", failures)
        if str(asset.get("source_image", "")) != str(manifest.get("source_image", "")):
            fail(f"{asset_id} source image path does not match manifest source image", failures)
        if str(asset.get("generation_prompt", "")) != str(manifest.get("generation_prompt", "")):
            fail(f"{asset_id} prompt path does not match manifest prompt", failures)
        for raw_source in asset.get("input_sources", []):
            if not isinstance(raw_source, dict):
                fail(f"{asset_id} input source is not an object", failures)
                continue
            if str(raw_source.get("commercial_status", "")) not in {"green_origin_candidate_pending_license_review", "green_origin_candidate", "documentation_only"}:
                fail(f"{asset_id} input source has unsupported commercial status", failures)
            if "path" in raw_source:
                path_exists(str(raw_source["path"]), failures)
    if seen_ids != expected_ids:
        fail(f"atelier cargo manifest asset ids mismatch: {sorted(seen_ids)}", failures)
    else:
        pass_check("atelier cargo manifest contains crate, barrel, rope, and cluster")

    if ATELIER_STANDARD_REPORT_PATH.exists():
        report = ATELIER_STANDARD_REPORT_PATH.read_text(encoding="utf-8")
        for required_text in [
            "accepted 10/10 cargo prop quality target",
            "green_origin_candidate_pending_license_review",
            "deprecated as visual targets",
            "Reusable production pattern",
            "Recommended rollout",
        ]:
            if required_text not in report:
                fail(f"atelier cargo report missing text: {required_text}", failures)
        pass_check("atelier cargo standard report present")
    else:
        fail(f"missing atelier cargo standard report: {ATELIER_STANDARD_REPORT_PATH}", failures)


def validate_atelier_dock_clutter_manifest(failures: list[str]) -> None:
    manifest = load_json(ATELIER_DOCK_CLUTTER_MANIFEST_PATH, failures)
    if not manifest:
        return
    if manifest.get("schema_id") != "wayfarer.newport_atelier.dock_clutter_manifest.v1":
        fail("atelier dock clutter manifest schema_id must be wayfarer.newport_atelier.dock_clutter_manifest.v1", failures)
    else:
        pass_check("atelier dock clutter manifest schema id")
    if manifest.get("phase") != "G-4.19A":
        fail("atelier dock clutter manifest phase must be G-4.19A", failures)
    if "G-4.18D" not in str(manifest.get("visual_standard", "")) or "10/10" not in str(manifest.get("visual_standard", "")):
        fail("atelier dock clutter manifest must record the G-4.18D 10/10 visual standard", failures)
    if manifest.get("pipeline_status") != "ai_assisted_green_origin_candidate_pending_final_license_policy_approval":
        fail("atelier dock clutter pipeline_status must preserve pending license approval", failures)
    if manifest.get("rollout_pack_role") != "first_city_rollout_pack_after_g418d_atelier_standard":
        fail("atelier dock clutter manifest must identify G-4.19A as the first city rollout pack", failures)
    if "no over-scatter" not in str(manifest.get("placement_policy", "")):
        fail("atelier dock clutter placement_policy must forbid over-scatter", failures)
    if "AI-assisted" not in str(manifest.get("source_policy", "")):
        fail("atelier dock clutter source_policy must explicitly describe AI-assisted source handling", failures)
    if "10/10 source sheet" not in str(manifest.get("future_pack_pattern", "")):
        fail("atelier dock clutter future_pack_pattern must preserve the reusable pack structure", failures)

    for field in [
        "atlas",
        "source_image",
        "generation_prompt",
        "generated_asset_root",
        "contact_sheet",
        "provenance_report",
        "validation_report",
    ]:
        path_exists(str(manifest.get(field, "")), failures)
    path_exists(str(manifest.get("generated_asset_root", "")), failures)

    qa_report = load_json(ATELIER_DOCK_CLUTTER_QA_REPORT_PATH, failures)
    if qa_report:
        if qa_report.get("schema_id") != "wayfarer.newport_atelier.extraction_qa.v1":
            fail("atelier dock clutter QA report schema mismatch", failures)
        if qa_report.get("phase") != "G-4.19A":
            fail("atelier dock clutter QA report phase must be G-4.19A", failures)
        if qa_report.get("status") != "PASS":
            fail("atelier dock clutter QA report must be PASS", failures)
        for required_check in [
            "transparent sprites have no magenta background",
            "transparent sprites have no magenta halo on alpha edges",
            "sprites retain clean transparent crop padding",
            "sprites are not cut off at object edges",
            "source sheet object identity maps to manifest asset ids",
        ]:
            if required_check not in qa_report.get("checks", []):
                fail(f"atelier dock clutter QA report missing check: {required_check}", failures)

    assets = manifest.get("assets", [])
    if not isinstance(assets, list):
        fail("atelier dock clutter manifest assets must be a list", failures)
        return
    expected_ids = {
        "atelier_dock_bollards_01",
        "atelier_mooring_hardware_01",
        "atelier_fishing_net_bundle_01",
        "atelier_sacks_fish_baskets_01",
        "atelier_anchor_rope_01",
        "atelier_dock_repair_planks_01",
        "atelier_dock_lantern_01",
        "atelier_shoreline_debris_01",
    }
    if len(assets) != len(expected_ids):
        fail("atelier dock clutter manifest must contain exactly eight assets", failures)
    seen_ids: set[str] = set()
    required_fields = [
        "asset_id",
        "asset_type",
        "source_identity",
        "path",
        "atlas",
        "atlas_region",
        "sprite_size",
        "pivot",
        "grounding",
        "recommended_game_scale",
        "source_type",
        "created_by",
        "generation_prompt",
        "source_image",
        "extraction_script",
        "input_sources",
        "license",
        "ownership",
        "provenance_status",
        "origin_classification",
        "commercial_use_status",
        "review_eligible",
        "normal_review_eligible",
        "lab_only",
        "final_commercial_candidate",
        "final_commercial_eligible",
        "source_pixels_from_yellow_uncertain_assets",
        "source_pixels_from_third_party_material",
        "web_scraped_source_pixels",
        "ai_generated",
        "human_selected",
        "chroma_key_removed",
        "extraction_qa",
        "sha256",
        "notes",
    ]
    for asset in assets:
        if not isinstance(asset, dict):
            fail("atelier dock clutter asset entry is not an object", failures)
            continue
        asset_id = str(asset.get("asset_id", ""))
        seen_ids.add(asset_id)
        for field in required_fields:
            if field not in asset:
                fail(f"{asset_id or 'unknown'} missing atelier dock clutter field {field}", failures)
        if asset_id not in expected_ids:
            fail(f"unexpected atelier dock clutter asset id: {asset_id}", failures)
        if asset.get("source_type") != "ai_assisted_image_generation_with_local_chroma_extraction":
            fail(f"{asset_id} source_type must be AI-assisted image generation plus local extraction", failures)
        if asset.get("provenance_status") != "ai_assisted_green_origin_candidate_pending_license_review":
            fail(f"{asset_id} provenance_status must remain AI-assisted pending license review", failures)
        if asset.get("origin_classification") != "green_origin_candidate_pending_license_review":
            fail(f"{asset_id} origin_classification must remain green_origin_candidate_pending_license_review", failures)
        if asset.get("commercial_use_status") != "green_origin_candidate_pending_license_review":
            fail(f"{asset_id} commercial_use_status must remain pending license review", failures)
        if asset.get("review_eligible") is not True:
            fail(f"{asset_id} must be review_eligible", failures)
        if asset.get("normal_review_eligible") is not True:
            fail(f"{asset_id} must be normal_review_eligible for this visual rollout pack", failures)
        if asset.get("lab_only") is not False:
            fail(f"{asset_id} must not be lab_only after G-4.19A placement", failures)
        if asset.get("final_commercial_candidate") is not False:
            fail(f"{asset_id} must not be marked final_commercial_candidate", failures)
        if asset.get("final_commercial_eligible") is not False:
            fail(f"{asset_id} must not be marked final_commercial_eligible", failures)
        for bool_field in ["source_pixels_from_yellow_uncertain_assets", "source_pixels_from_third_party_material", "web_scraped_source_pixels"]:
            if asset.get(bool_field) is not False:
                fail(f"{asset_id} must set {bool_field}=false", failures)
        if asset.get("ai_generated") is not True or asset.get("human_selected") is not True:
            fail(f"{asset_id} must declare ai_generated and human_selected", failures)
        if asset.get("chroma_key_removed") is not True:
            fail(f"{asset_id} must declare chroma_key_removed", failures)
        asset_rel_path = str(asset.get("path", ""))
        path_exists(asset_rel_path, failures)
        asset_path = PROJECT_ROOT / asset_rel_path
        if asset_path.exists():
            metrics = image_alpha_metrics(asset_path)
            qa = asset.get("extraction_qa", {})
            if metrics.get("magenta_pixels_remaining") != 0:
                fail(f"{asset_id} has magenta background pixels remaining", failures)
            if metrics.get("magenta_halo_pixels") != 0:
                fail(f"{asset_id} has magenta halo pixels", failures)
            if metrics.get("cutoff_edges"):
                fail(f"{asset_id} crop padding/cutoff failed: {metrics.get('cutoff_edges')}", failures)
            if metrics.get("readable") is not True:
                fail(f"{asset_id} alpha footprint is not visually readable", failures)
            for metric_key in ["magenta_pixels_remaining", "magenta_halo_pixels", "cutoff_edges", "readable"]:
                if qa.get(metric_key) != metrics.get(metric_key):
                    fail(f"{asset_id} manifest QA metric {metric_key} does not match image inspection", failures)
        for path_field in ["generation_prompt", "source_image", "extraction_script", "atlas"]:
            path_exists(str(asset.get(path_field, "")), failures)
        if str(asset.get("atlas", "")) != str(manifest.get("atlas", "")):
            fail(f"{asset_id} atlas path does not match manifest atlas", failures)
        if str(asset.get("source_image", "")) != str(manifest.get("source_image", "")):
            fail(f"{asset_id} source image path does not match manifest source image", failures)
        if str(asset.get("generation_prompt", "")) != str(manifest.get("generation_prompt", "")):
            fail(f"{asset_id} prompt path does not match manifest prompt", failures)
        for raw_source in asset.get("input_sources", []):
            if not isinstance(raw_source, dict):
                fail(f"{asset_id} input source is not an object", failures)
                continue
            if str(raw_source.get("commercial_status", "")) not in {"green_origin_candidate_pending_license_review", "green_origin_candidate", "documentation_only"}:
                fail(f"{asset_id} input source has unsupported commercial status", failures)
            if "path" in raw_source:
                path_exists(str(raw_source["path"]), failures)
    if seen_ids != expected_ids:
        fail(f"atelier dock clutter manifest asset ids mismatch: {sorted(seen_ids)}", failures)
    else:
        pass_check("atelier dock clutter manifest contains all eight dock clutter assets")

    if ATELIER_DOCK_CLUTTER_REPORT_PATH.exists():
        report = ATELIER_DOCK_CLUTTER_REPORT_PATH.read_text(encoding="utf-8")
        for required_text in [
            "first Newport city rollout pack",
            "G-4.18D atelier",
            "ai_assisted_green_origin_candidate_pending_license_review",
            "controlled subset",
            "Reusable Production Pattern",
        ]:
            if required_text not in report:
                fail(f"atelier dock clutter report missing text: {required_text}", failures)
        pass_check("atelier dock clutter report present")
    else:
        fail(f"missing atelier dock clutter report: {ATELIER_DOCK_CLUTTER_REPORT_PATH}", failures)


def validate_g420a_environmental_believability_wave(failures: list[str]) -> None:
    wave = load_json(ATELIER_G420A_WAVE_MANIFEST_PATH, failures)
    if not wave:
        return
    if wave.get("schema_id") != "wayfarer.newport_atelier.g420a.environmental_believability_wave.v1":
        fail("G-4.20A environmental wave manifest schema mismatch", failures)
    else:
        pass_check("G-4.20A environmental wave manifest schema id")
    if wave.get("phase") != "G-4.20A":
        fail("G-4.20A environmental wave manifest phase must be G-4.20A", failures)
    if wave.get("wave_id") != "wave_1_environmental_believability":
        fail("G-4.20A environmental wave must identify wave_1_environmental_believability", failures)
    if float(wave.get("visual_quality_gate", 0.0)) < 8.5:
        fail("G-4.20A environmental wave must preserve the 8.5 visual gate", failures)
    if "no over-scatter" not in str(wave.get("placement_policy", "")):
        fail("G-4.20A environmental wave placement policy must forbid over-scatter", failures)
    if "REBUILD_REQUIRED_CENTERPIECE" not in str(wave.get("tavern_inn_lock", "")):
        fail("G-4.20A environmental wave must preserve Tavern/Inn centerpiece lock", failures)

    packs = wave.get("packs", [])
    if not isinstance(packs, list):
        fail("G-4.20A environmental wave packs must be a list", failures)
        return
    pack_ids = {str(pack.get("pack_id", "")) for pack in packs if isinstance(pack, dict)}
    if pack_ids != ATELIER_G420A_PACK_IDS:
        fail(f"G-4.20A environmental wave pack ids mismatch: {sorted(pack_ids)}", failures)
    if len(packs) < 3 or len(packs) > 5:
        fail("G-4.20A environmental wave must contain 3-5 themed atelier sheets", failures)

    wave_assets = wave.get("assets", [])
    if not isinstance(wave_assets, list) or len(wave_assets) != 32:
        fail("G-4.20A environmental wave must contain exactly 32 registered extracted assets", failures)
    else:
        pass_check("G-4.20A environmental wave asset count: 32")

    required_pack_fields = [
        "manifest",
        "source_image",
        "generation_prompt",
        "atlas",
        "contact_sheet",
        "validation_report",
        "provenance_report",
        "asset_ids",
    ]
    required_asset_fields = [
        "asset_id",
        "asset_type",
        "source_identity",
        "category",
        "path",
        "atlas",
        "atlas_region",
        "sprite_size",
        "pivot",
        "grounding",
        "recommended_game_scale",
        "visual_quality_rating",
        "visual_quality_gate",
        "visual_quality_status",
        "source_type",
        "created_by",
        "generation_prompt",
        "source_image",
        "extraction_script",
        "input_sources",
        "license",
        "ownership",
        "provenance_status",
        "origin_classification",
        "commercial_use_status",
        "review_eligible",
        "normal_review_eligible",
        "lab_only",
        "final_commercial_candidate",
        "final_commercial_eligible",
        "source_pixels_from_yellow_uncertain_assets",
        "source_pixels_from_third_party_material",
        "web_scraped_source_pixels",
        "ai_generated",
        "human_selected",
        "chroma_key_removed",
        "extraction_qa",
        "gameplay_role",
        "sha256",
        "notes",
    ]
    seen_asset_ids: set[str] = set()
    for raw_pack in packs:
        if not isinstance(raw_pack, dict):
            fail("G-4.20A environmental wave pack entry is not an object", failures)
            continue
        pack_id = str(raw_pack.get("pack_id", ""))
        for field in required_pack_fields:
            if field not in raw_pack:
                fail(f"{pack_id} missing wave pack field {field}", failures)
            else:
                value = raw_pack.get(field)
                if field != "asset_ids":
                    path_exists(str(value), failures)
        manifest = load_json(PROJECT_ROOT / str(raw_pack.get("manifest", "")), failures)
        qa_report = load_json(PROJECT_ROOT / str(raw_pack.get("validation_report", "")), failures)
        if not manifest:
            continue
        if manifest.get("phase") != "G-4.20A":
            fail(f"{pack_id} manifest phase must be G-4.20A", failures)
        if manifest.get("pack_id") != pack_id:
            fail(f"{pack_id} manifest pack_id mismatch", failures)
        if "8.5/10" not in str(manifest.get("visual_standard", "")):
            fail(f"{pack_id} manifest must record the 8.5/10 visual gate", failures)
        for field in [
            "atlas",
            "source_image",
            "generation_prompt",
            "generated_asset_root",
            "contact_sheet",
            "provenance_report",
            "validation_report",
        ]:
            path_exists(str(manifest.get(field, "")), failures)
        if qa_report:
            if qa_report.get("schema_id") != "wayfarer.newport_atelier.extraction_qa.v1":
                fail(f"{pack_id} QA report schema mismatch", failures)
            if qa_report.get("phase") != "G-4.20A":
                fail(f"{pack_id} QA report phase must be G-4.20A", failures)
            if qa_report.get("status") != "PASS":
                fail(f"{pack_id} QA report must be PASS", failures)
            for required_check in [
                "transparent sprites have no magenta background",
                "transparent sprites have no magenta halo on alpha edges",
                "sprites retain clean transparent crop padding",
                "sprites are not cut off at object edges",
                "source sheet object identity maps to manifest asset ids",
                "visual quality rating meets or exceeds 8.5/10",
            ]:
                if required_check not in qa_report.get("checks", []):
                    fail(f"{pack_id} QA report missing check: {required_check}", failures)
        assets = manifest.get("assets", [])
        if not isinstance(assets, list) or len(assets) != 8:
            fail(f"{pack_id} manifest must contain exactly eight assets", failures)
            continue
        for asset in assets:
            if not isinstance(asset, dict):
                fail(f"{pack_id} asset entry is not an object", failures)
                continue
            asset_id = str(asset.get("asset_id", ""))
            if asset_id in seen_asset_ids:
                fail(f"duplicate G-4.20A environmental asset id: {asset_id}", failures)
            seen_asset_ids.add(asset_id)
            for field in required_asset_fields:
                if field not in asset:
                    fail(f"{asset_id or 'unknown'} missing G-4.20A asset field {field}", failures)
            if asset.get("source_type") != "ai_assisted_image_generation_with_local_chroma_extraction":
                fail(f"{asset_id} source_type must be AI-assisted image generation plus local extraction", failures)
            if asset.get("provenance_status") != "ai_assisted_green_origin_candidate_pending_license_review":
                fail(f"{asset_id} provenance status must remain pending AI-assisted green-origin", failures)
            if asset.get("origin_classification") != "green_origin_candidate_pending_license_review":
                fail(f"{asset_id} origin classification must remain pending license review", failures)
            if asset.get("commercial_use_status") != "green_origin_candidate_pending_license_review":
                fail(f"{asset_id} commercial use status must remain pending license review", failures)
            if asset.get("review_eligible") is not True or asset.get("normal_review_eligible") is not True:
                fail(f"{asset_id} must be review-eligible for the G-4.20A wave", failures)
            if asset.get("lab_only") is not False:
                fail(f"{asset_id} must not be lab-only after G-4.20A acceptance", failures)
            if asset.get("final_commercial_candidate") is not False or asset.get("final_commercial_eligible") is not False:
                fail(f"{asset_id} must not be final-commercial promoted", failures)
            for bool_field in ["source_pixels_from_yellow_uncertain_assets", "source_pixels_from_third_party_material", "web_scraped_source_pixels"]:
                if asset.get(bool_field) is not False:
                    fail(f"{asset_id} must set {bool_field}=false", failures)
            if float(asset.get("visual_quality_rating", 0.0)) < 8.5:
                fail(f"{asset_id} visual quality rating is below 8.5", failures)
            asset_rel_path = str(asset.get("path", ""))
            path_exists(asset_rel_path, failures)
            asset_path = PROJECT_ROOT / asset_rel_path
            if asset_path.exists():
                metrics = image_alpha_metrics(asset_path)
                qa = asset.get("extraction_qa", {})
                if metrics.get("magenta_pixels_remaining") != 0:
                    fail(f"{asset_id} has magenta background pixels remaining", failures)
                if metrics.get("magenta_halo_pixels") != 0:
                    fail(f"{asset_id} has magenta halo pixels", failures)
                if metrics.get("cutoff_edges"):
                    fail(f"{asset_id} crop padding/cutoff failed: {metrics.get('cutoff_edges')}", failures)
                if metrics.get("readable") is not True:
                    fail(f"{asset_id} alpha footprint is not visually readable", failures)
                for metric_key in ["magenta_pixels_remaining", "magenta_halo_pixels", "cutoff_edges", "readable"]:
                    if qa.get(metric_key) != metrics.get(metric_key):
                        fail(f"{asset_id} manifest QA metric {metric_key} does not match image inspection", failures)
            for path_field in ["generation_prompt", "source_image", "extraction_script", "atlas"]:
                path_exists(str(asset.get(path_field, "")), failures)
            for raw_source in asset.get("input_sources", []):
                if not isinstance(raw_source, dict):
                    fail(f"{asset_id} input source is not an object", failures)
                    continue
                if str(raw_source.get("commercial_status", "")) not in {"green_origin_candidate_pending_license_review", "green_origin_candidate", "documentation_only"}:
                    fail(f"{asset_id} input source has unsupported commercial status", failures)
                if "path" in raw_source:
                    path_exists(str(raw_source["path"]), failures)

    if len(seen_asset_ids) == 32:
        pass_check("G-4.20A environmental wave contains 32 unique assets")
    else:
        fail(f"G-4.20A environmental wave unique asset count mismatch: {len(seen_asset_ids)}", failures)

    if ATELIER_G420A_WAVE_REPORT_PATH.exists():
        report = ATELIER_G420A_WAVE_REPORT_PATH.read_text(encoding="utf-8")
        for required_text in [
            "first mass atelier production wave",
            "environmental believability",
            "Tavern/Inn remains",
            "REBUILD_REQUIRED_CENTERPIECE",
            "blocked from final commercial promotion",
        ]:
            if required_text not in report:
                fail(f"G-4.20A environmental wave report missing text: {required_text}", failures)
        pass_check("G-4.20A environmental wave report present")
    else:
        fail(f"missing G-4.20A environmental wave report: {ATELIER_G420A_WAVE_REPORT_PATH}", failures)


def validate_g420b_town_identity_wave(failures: list[str]) -> None:
    wave = load_json(ATELIER_G420B_WAVE_MANIFEST_PATH, failures)
    if not wave:
        return
    if wave.get("schema_id") != "wayfarer.newport_atelier.g420b.town_identity_wave.v1":
        fail("G-4.20B town identity wave manifest schema mismatch", failures)
    else:
        pass_check("G-4.20B town identity wave manifest schema id")
    if wave.get("phase") != "G-4.20B":
        fail("G-4.20B town identity wave manifest phase must be G-4.20B", failures)
    if wave.get("wave_id") != "wave_2_town_identity":
        fail("G-4.20B town identity wave must identify wave_2_town_identity", failures)
    if float(wave.get("visual_quality_gate", 0.0)) < 8.5:
        fail("G-4.20B town identity wave must preserve the 8.5 visual gate", failures)
    placement_policy = str(wave.get("placement_policy", ""))
    if "no over-decoration" not in placement_policy or "no navigation blocking" not in placement_policy:
        fail("G-4.20B town identity wave placement policy must forbid over-decoration and navigation blocking", failures)
    if "REBUILD_REQUIRED_CENTERPIECE" not in str(wave.get("tavern_inn_lock", "")):
        fail("G-4.20B town identity wave must preserve Tavern/Inn centerpiece lock", failures)

    packs = wave.get("packs", [])
    if not isinstance(packs, list):
        fail("G-4.20B town identity wave packs must be a list", failures)
        return
    pack_ids = {str(pack.get("pack_id", "")) for pack in packs if isinstance(pack, dict)}
    if pack_ids != ATELIER_G420B_PACK_IDS:
        fail(f"G-4.20B town identity wave pack ids mismatch: {sorted(pack_ids)}", failures)
    if len(packs) < 3 or len(packs) > 5:
        fail("G-4.20B town identity wave must contain 3-5 themed atelier sheets", failures)

    wave_assets = wave.get("assets", [])
    if not isinstance(wave_assets, list) or len(wave_assets) != 32:
        fail("G-4.20B town identity wave must contain exactly 32 registered extracted assets", failures)
    else:
        pass_check("G-4.20B town identity wave asset count: 32")

    required_pack_fields = [
        "manifest",
        "source_image",
        "generation_prompt",
        "atlas",
        "contact_sheet",
        "validation_report",
        "provenance_report",
        "asset_ids",
    ]
    required_asset_fields = [
        "asset_id",
        "asset_type",
        "source_identity",
        "category",
        "path",
        "atlas",
        "atlas_region",
        "sprite_size",
        "pivot",
        "grounding",
        "recommended_game_scale",
        "visual_quality_rating",
        "visual_quality_gate",
        "source_type",
        "generation_prompt",
        "source_image",
        "extraction_script",
        "input_sources",
        "provenance_status",
        "origin_classification",
        "commercial_use_status",
        "review_eligible",
        "normal_review_eligible",
        "lab_only",
        "final_commercial_candidate",
        "final_commercial_eligible",
        "source_pixels_from_yellow_uncertain_assets",
        "source_pixels_from_third_party_material",
        "web_scraped_source_pixels",
        "extraction_qa",
        "gameplay_role",
        "sha256",
        "notes",
    ]
    seen_asset_ids: set[str] = set()
    for raw_pack in packs:
        if not isinstance(raw_pack, dict):
            fail("G-4.20B town identity wave pack entry is not an object", failures)
            continue
        pack_id = str(raw_pack.get("pack_id", ""))
        for field in required_pack_fields:
            if field not in raw_pack:
                fail(f"{pack_id} missing wave pack field {field}", failures)
            elif field != "asset_ids":
                path_exists(str(raw_pack.get(field, "")), failures)
        manifest = load_json(PROJECT_ROOT / str(raw_pack.get("manifest", "")), failures)
        qa_report = load_json(PROJECT_ROOT / str(raw_pack.get("validation_report", "")), failures)
        if not manifest:
            continue
        if manifest.get("phase") != "G-4.20B":
            fail(f"{pack_id} manifest phase must be G-4.20B", failures)
        if manifest.get("pack_id") != pack_id:
            fail(f"{pack_id} manifest pack_id mismatch", failures)
        if "8.5/10" not in str(manifest.get("visual_standard", "")):
            fail(f"{pack_id} manifest must record the 8.5/10 visual gate", failures)
        if "REBUILD_REQUIRED_CENTERPIECE" not in str(manifest.get("tavern_inn_lock", "")):
            fail(f"{pack_id} must preserve the Tavern/Inn centerpiece lock", failures)
        for field in [
            "atlas",
            "source_image",
            "generation_prompt",
            "generated_asset_root",
            "contact_sheet",
            "provenance_report",
            "validation_report",
        ]:
            path_exists(str(manifest.get(field, "")), failures)
        if qa_report:
            if qa_report.get("schema_id") != "wayfarer.newport_atelier.extraction_qa.v1":
                fail(f"{pack_id} QA report schema mismatch", failures)
            if qa_report.get("phase") != "G-4.20B":
                fail(f"{pack_id} QA report phase must be G-4.20B", failures)
            if qa_report.get("status") != "PASS":
                fail(f"{pack_id} QA report must be PASS", failures)
            for required_check in [
                "transparent sprites have no magenta background",
                "transparent sprites have no magenta halo on alpha edges",
                "sprites retain clean transparent crop padding",
                "sprites are not cut off at object edges",
                "source sheet object identity maps to manifest asset ids",
                "visual quality rating meets or exceeds 8.5/10",
                "temporary Tavern/Inn sign candidate is not placed as a final building patch",
            ]:
                if required_check not in qa_report.get("checks", []):
                    fail(f"{pack_id} QA report missing check: {required_check}", failures)
        assets = manifest.get("assets", [])
        if not isinstance(assets, list) or len(assets) != 8:
            fail(f"{pack_id} manifest must contain exactly eight assets", failures)
            continue
        for asset in assets:
            if not isinstance(asset, dict):
                fail(f"{pack_id} asset entry is not an object", failures)
                continue
            asset_id = str(asset.get("asset_id", ""))
            if asset_id in seen_asset_ids:
                fail(f"duplicate G-4.20B town identity asset id: {asset_id}", failures)
            seen_asset_ids.add(asset_id)
            for field in required_asset_fields:
                if field not in asset:
                    fail(f"{asset_id or 'unknown'} missing G-4.20B asset field {field}", failures)
            if asset.get("source_type") != "ai_assisted_image_generation_with_local_chroma_extraction":
                fail(f"{asset_id} source_type must be AI-assisted image generation plus local extraction", failures)
            if asset.get("provenance_status") != "ai_assisted_green_origin_candidate_pending_license_review":
                fail(f"{asset_id} provenance status must remain pending AI-assisted green-origin", failures)
            if asset.get("origin_classification") != "green_origin_candidate_pending_license_review":
                fail(f"{asset_id} origin classification must remain pending license review", failures)
            if asset.get("commercial_use_status") != "green_origin_candidate_pending_license_review":
                fail(f"{asset_id} commercial use status must remain pending license review", failures)
            if asset.get("review_eligible") is not True or asset.get("normal_review_eligible") is not True:
                fail(f"{asset_id} must be review-eligible for the G-4.20B wave", failures)
            if asset.get("lab_only") is not False:
                fail(f"{asset_id} must not be lab-only after G-4.20B acceptance", failures)
            if asset.get("final_commercial_candidate") is not False or asset.get("final_commercial_eligible") is not False:
                fail(f"{asset_id} must not be final-commercial promoted", failures)
            for bool_field in ["source_pixels_from_yellow_uncertain_assets", "source_pixels_from_third_party_material", "web_scraped_source_pixels"]:
                if asset.get(bool_field) is not False:
                    fail(f"{asset_id} must set {bool_field}=false", failures)
            if float(asset.get("visual_quality_rating", 0.0)) < 8.5:
                fail(f"{asset_id} visual quality rating is below 8.5", failures)
            asset_rel_path = str(asset.get("path", ""))
            path_exists(asset_rel_path, failures)
            asset_path = PROJECT_ROOT / asset_rel_path
            if asset_path.exists():
                metrics = image_alpha_metrics(asset_path)
                qa = asset.get("extraction_qa", {})
                if metrics.get("magenta_pixels_remaining") != 0:
                    fail(f"{asset_id} has magenta background pixels remaining", failures)
                if metrics.get("magenta_halo_pixels") != 0:
                    fail(f"{asset_id} has magenta halo pixels", failures)
                if metrics.get("cutoff_edges"):
                    fail(f"{asset_id} crop padding/cutoff failed: {metrics.get('cutoff_edges')}", failures)
                if metrics.get("readable") is not True:
                    fail(f"{asset_id} alpha footprint is not visually readable", failures)
                for metric_key in ["magenta_pixels_remaining", "magenta_halo_pixels", "cutoff_edges", "readable"]:
                    if qa.get(metric_key) != metrics.get(metric_key):
                        fail(f"{asset_id} manifest QA metric {metric_key} does not match image inspection", failures)
            for path_field in ["generation_prompt", "source_image", "extraction_script", "atlas"]:
                path_exists(str(asset.get(path_field, "")), failures)

    if len(seen_asset_ids) == 32:
        pass_check("G-4.20B town identity wave contains 32 unique assets")
    else:
        fail(f"G-4.20B town identity wave unique asset count mismatch: {len(seen_asset_ids)}", failures)

    if ATELIER_G420B_WAVE_REPORT_PATH.exists():
        report = ATELIER_G420B_WAVE_REPORT_PATH.read_text(encoding="utf-8")
        for required_text in [
            "Town Identity atelier wave",
            "signage",
            "wayfinding",
            "Tavern/Inn remains",
            "REBUILD_REQUIRED_CENTERPIECE",
            "blocked from final commercial promotion",
        ]:
            if required_text not in report:
                fail(f"G-4.20B town identity wave report missing text: {required_text}", failures)
        pass_check("G-4.20B town identity wave report present")
    else:
        fail(f"missing G-4.20B town identity wave report: {ATELIER_G420B_WAVE_REPORT_PATH}", failures)


def validate_g421a_core_building_rebuild_wave(failures: list[str]) -> None:
    wave = load_json(ATELIER_G421A_WAVE_MANIFEST_PATH, failures)
    if not wave:
        return
    if wave.get("schema_id") != "wayfarer.newport_atelier.g421a.core_building_rebuild_wave_1.v1":
        fail("G-4.21A core building rebuild wave manifest schema mismatch", failures)
    else:
        pass_check("G-4.21A core building rebuild wave manifest schema id")
    if wave.get("phase") != "G-4.21A":
        fail("G-4.21A core building rebuild wave manifest phase must be G-4.21A", failures)
    if wave.get("wave_id") != "wave_4_building_rebuild_or_enhancement":
        fail("G-4.21A core building rebuild wave must identify wave_4_building_rebuild_or_enhancement", failures)
    if float(wave.get("visual_quality_gate", 0.0)) < 8.5:
        fail("G-4.21A core building rebuild wave must preserve the 8.5 visual gate", failures)
    placement_policy = str(wave.get("placement_policy", "")).lower()
    for required_text in ["controlled proof subset", "do not over-place", "block navigation", "old unverified buildings"]:
        if required_text not in placement_policy:
            fail(f"G-4.21A placement policy missing: {required_text}", failures)
    tavern_direction = str(wave.get("tavern_inn_hero_direction", ""))
    for required_text in ["brick construction", "front/back", "twin-stack", "Hotel Viking", "without direct copy", "hero asset"]:
        if required_text not in tavern_direction:
            fail(f"G-4.21A Tavern/Inn direction missing: {required_text}", failures)

    packs = wave.get("packs", [])
    if not isinstance(packs, list):
        fail("G-4.21A core building rebuild wave packs must be a list", failures)
        return
    pack_ids = {str(pack.get("pack_id", "")) for pack in packs if isinstance(pack, dict)}
    if pack_ids != ATELIER_G421A_PACK_IDS:
        fail(f"G-4.21A core building rebuild wave pack ids mismatch: {sorted(pack_ids)}", failures)
    if len(packs) != 1:
        fail("G-4.21A core building rebuild wave must contain exactly one Wave 1 pack", failures)

    wave_assets = wave.get("assets", [])
    if not isinstance(wave_assets, list) or len(wave_assets) != 6:
        fail("G-4.21A core building rebuild wave must contain exactly six registered building assets", failures)
    else:
        pass_check("G-4.21A core building rebuild wave asset count: 6")
    wave_asset_ids = {str(asset.get("asset_id", "")) for asset in wave_assets if isinstance(asset, dict)}
    if wave_asset_ids != G421A_REQUIRED_BUILDING_ASSETS:
        fail(f"G-4.21A core building rebuild wave asset ids mismatch: {sorted(wave_asset_ids)}", failures)

    required_pack_fields = [
        "manifest",
        "source_image",
        "generation_prompt",
        "atlas",
        "contact_sheet",
        "validation_report",
        "provenance_report",
        "asset_ids",
    ]
    required_asset_fields = [
        "asset_id",
        "asset_type",
        "source_identity",
        "category",
        "path",
        "atlas",
        "atlas_region",
        "sprite_size",
        "building_id",
        "display_name",
        "replaces_asset_id",
        "pivot",
        "grounding",
        "recommended_game_scale",
        "building_draw_width",
        "visual_quality_rating",
        "visual_quality_gate",
        "visual_quality_status",
        "source_type",
        "created_by",
        "generation_prompt",
        "source_image",
        "extraction_script",
        "input_sources",
        "license",
        "ownership",
        "provenance_status",
        "origin_classification",
        "commercial_use_status",
        "review_eligible",
        "normal_review_eligible",
        "lab_only",
        "final_commercial_candidate",
        "final_commercial_eligible",
        "source_pixels_from_yellow_uncertain_assets",
        "source_pixels_from_third_party_material",
        "web_scraped_source_pixels",
        "ai_generated",
        "human_selected",
        "chroma_key_removed",
        "extraction_qa",
        "building_qa",
        "gameplay_role",
        "controlled_proof_placement",
        "sha256",
        "notes",
    ]
    seen_asset_ids: set[str] = set()
    for raw_pack in packs:
        if not isinstance(raw_pack, dict):
            fail("G-4.21A core building rebuild wave pack entry is not an object", failures)
            continue
        pack_id = str(raw_pack.get("pack_id", ""))
        for field in required_pack_fields:
            if field not in raw_pack:
                fail(f"{pack_id} missing wave pack field {field}", failures)
            elif field != "asset_ids":
                path_exists(str(raw_pack.get(field, "")), failures)
        if set(raw_pack.get("asset_ids", [])) != G421A_REQUIRED_BUILDING_ASSETS:
            fail(f"{pack_id} asset_ids must match the required G-4.21A building set", failures)
        pack_manifest = load_json(PROJECT_ROOT / str(raw_pack.get("manifest", "")), failures)
        qa_report = load_json(PROJECT_ROOT / str(raw_pack.get("validation_report", "")), failures)
        if not pack_manifest:
            continue
        if pack_manifest.get("schema_id") != "wayfarer.newport_atelier.g421a.core_building_rebuild_wave_1.manifest.v1":
            fail(f"{pack_id} manifest schema mismatch", failures)
        if pack_manifest.get("phase") != "G-4.21A":
            fail(f"{pack_id} manifest phase must be G-4.21A", failures)
        if pack_manifest.get("pack_id") != pack_id:
            fail(f"{pack_id} manifest pack_id mismatch", failures)
        for field in [
            "atlas",
            "source_image",
            "generation_prompt",
            "generated_asset_root",
            "contact_sheet",
            "provenance_report",
            "validation_report",
        ]:
            path_exists(str(pack_manifest.get(field, "")), failures)
        if "brick construction" not in str(pack_manifest.get("tavern_inn_hero_direction", "")):
            fail(f"{pack_id} manifest must record Tavern/Inn brick hero direction", failures)
        if qa_report:
            if qa_report.get("schema_id") != "wayfarer.newport_atelier.extraction_qa.v1":
                fail(f"{pack_id} QA report schema mismatch", failures)
            if qa_report.get("phase") != "G-4.21A":
                fail(f"{pack_id} QA report phase must be G-4.21A", failures)
            if qa_report.get("status") != "PASS":
                fail(f"{pack_id} QA report must be PASS", failures)
            for required_check in [
                "transparent sprites have no magenta background",
                "transparent sprites have no magenta halo on alpha edges",
                "sprites retain clean transparent crop padding",
                "sprites are not cut off at object edges",
                "building transparent bounds metadata is recorded",
                "base/foundation grounding is visible and usable",
                "entrance is readable",
                "pivot/base anchor is sensible",
                "building does not visually float",
                "chimneys and rooflines are not cut off",
                "Tavern/Inn QA confirms brick construction",
                "Tavern/Inn QA confirms two sets of large twin-stack chimneys",
                "Tavern/Inn QA confirms front/back bridged chimney-pair arrangement",
                "Tavern/Inn QA confirms centerpiece hero landmark status",
                "Tavern/Inn QA confirms Hotel Viking inspiration without direct copy",
            ]:
                if required_check not in qa_report.get("checks", []):
                    fail(f"{pack_id} QA report missing check: {required_check}", failures)
        assets = pack_manifest.get("assets", [])
        if not isinstance(assets, list) or len(assets) != 6:
            fail(f"{pack_id} manifest must contain exactly six building assets", failures)
            continue
        for asset in assets:
            if not isinstance(asset, dict):
                fail(f"{pack_id} asset entry is not an object", failures)
                continue
            asset_id = str(asset.get("asset_id", ""))
            if asset_id in seen_asset_ids:
                fail(f"duplicate G-4.21A core building asset id: {asset_id}", failures)
            seen_asset_ids.add(asset_id)
            for field in required_asset_fields:
                if field not in asset:
                    fail(f"{asset_id or 'unknown'} missing G-4.21A asset field {field}", failures)
            if asset_id not in G421A_REQUIRED_BUILDING_ASSETS:
                fail(f"unexpected G-4.21A core building asset id: {asset_id}", failures)
            if G421A_BUILDING_ID_TO_ASSET.get(str(asset.get("building_id", ""))) != asset_id:
                fail(f"{asset_id} building_id does not match required proof placement", failures)
            if asset.get("source_type") != "codex_assisted_original_building_sheet_with_local_chroma_extraction":
                fail(f"{asset_id} source_type must be Codex-assisted original sheet plus local chroma extraction", failures)
            if asset.get("provenance_status") != "ai_assisted_green_origin_candidate_pending_license_review":
                fail(f"{asset_id} provenance status must remain pending AI-assisted green-origin", failures)
            if asset.get("origin_classification") != "green_origin_candidate_pending_license_review":
                fail(f"{asset_id} origin classification must remain pending license review", failures)
            if asset.get("commercial_use_status") != "green_origin_candidate_pending_license_review":
                fail(f"{asset_id} commercial use status must remain pending license review", failures)
            if asset.get("review_eligible") is not True or asset.get("normal_review_eligible") is not True:
                fail(f"{asset_id} must be review-eligible for the G-4.21A wave", failures)
            if asset.get("lab_only") is not False:
                fail(f"{asset_id} must not be lab-only after G-4.21A proof placement", failures)
            if asset.get("final_commercial_candidate") is not False or asset.get("final_commercial_eligible") is not False:
                fail(f"{asset_id} must not be final-commercial promoted", failures)
            for bool_field in ["source_pixels_from_yellow_uncertain_assets", "source_pixels_from_third_party_material", "web_scraped_source_pixels"]:
                if asset.get(bool_field) is not False:
                    fail(f"{asset_id} must set {bool_field}=false", failures)
            if asset.get("ai_generated") is not True or asset.get("human_selected") is not True:
                fail(f"{asset_id} must declare ai_generated and human_selected", failures)
            if asset.get("chroma_key_removed") is not True:
                fail(f"{asset_id} must declare chroma_key_removed", failures)
            if float(asset.get("visual_quality_rating", 0.0)) < 8.5:
                fail(f"{asset_id} visual quality rating is below 8.5", failures)
            placement = asset.get("controlled_proof_placement", {})
            if not isinstance(placement, dict) or placement.get("placed") is not True:
                fail(f"{asset_id} controlled proof placement must be recorded", failures)
            asset_rel_path = str(asset.get("path", ""))
            path_exists(asset_rel_path, failures)
            asset_path = PROJECT_ROOT / asset_rel_path
            if asset_path.exists():
                metrics = image_alpha_metrics(asset_path)
                qa = asset.get("extraction_qa", {})
                if metrics.get("magenta_pixels_remaining") != 0:
                    fail(f"{asset_id} has magenta background pixels remaining", failures)
                if metrics.get("magenta_halo_pixels") != 0:
                    fail(f"{asset_id} has magenta halo pixels", failures)
                if metrics.get("cutoff_edges"):
                    fail(f"{asset_id} crop padding/cutoff failed: {metrics.get('cutoff_edges')}", failures)
                if metrics.get("readable") is not True:
                    fail(f"{asset_id} alpha footprint is not visually readable", failures)
                for metric_key in ["magenta_pixels_remaining", "magenta_halo_pixels", "cutoff_edges", "readable"]:
                    if qa.get(metric_key) != metrics.get(metric_key):
                        fail(f"{asset_id} manifest QA metric {metric_key} does not match image inspection", failures)
                if "alpha_bbox" not in qa or qa.get("alpha_bbox") != metrics.get("alpha_bbox"):
                    fail(f"{asset_id} missing or mismatched transparent bounds metadata", failures)
            for path_field in ["generation_prompt", "source_image", "extraction_script", "atlas"]:
                path_exists(str(asset.get(path_field, "")), failures)
            if str(asset.get("atlas", "")) != str(pack_manifest.get("atlas", "")):
                fail(f"{asset_id} atlas path does not match pack manifest atlas", failures)
            pack_source_images = pack_manifest.get("source_images", {})
            expected_source = ""
            if isinstance(pack_source_images, dict):
                expected_source = str(pack_source_images.get(asset_id, ""))
            if expected_source and str(asset.get("source_image", "")) != expected_source:
                fail(f"{asset_id} source image path does not match pack manifest source_images entry", failures)
            elif not expected_source and str(asset.get("source_image", "")) != str(pack_manifest.get("source_image", "")):
                fail(f"{asset_id} source image path does not match pack manifest source image", failures)
            if str(asset.get("generation_prompt", "")) != str(pack_manifest.get("generation_prompt", "")):
                fail(f"{asset_id} prompt path does not match pack manifest prompt", failures)
            for raw_source in asset.get("input_sources", []):
                if not isinstance(raw_source, dict):
                    fail(f"{asset_id} input source is not an object", failures)
                    continue
                if str(raw_source.get("commercial_status", "")) not in {"green_origin_candidate_pending_license_review", "green_origin_candidate", "documentation_only"}:
                    fail(f"{asset_id} input source has unsupported commercial status", failures)
                if "path" in raw_source:
                    path_exists(str(raw_source["path"]), failures)
            if asset_id == G421A_TAVERN_ASSET_ID:
                qa = asset.get("building_qa", {})
                if not isinstance(qa, dict):
                    fail("G-4.21A Tavern/Inn building_qa must be an object", failures)
                    qa = {}
                for required_key in [
                    "brick_construction",
                    "two_sets_large_twin_stack_chimneys",
                    "front_back_bridged_chimney_pairs",
                    "hero_centerpiece",
                    "hotel_viking_inspired_not_direct_copy",
                    "clear_entrance",
                    "strong_foundation_grounding",
                    "visually_outranks_ordinary_buildings",
                ]:
                    if qa.get(required_key) is not True:
                        fail(f"G-4.21A Tavern/Inn QA must confirm {required_key}", failures)

    if seen_asset_ids == G421A_REQUIRED_BUILDING_ASSETS:
        pass_check("G-4.21A core building rebuild wave contains all six required building assets")
    else:
        fail(f"G-4.21A core building rebuild wave unique asset ids mismatch: {sorted(seen_asset_ids)}", failures)

    catalog = read_text(BUILDING_CATALOG_PATH, failures)
    building_to_sprite = _extract_building_sprite_ids(catalog)
    for building_id, asset_id in G421A_BUILDING_ID_TO_ASSET.items():
        if building_to_sprite.get(building_id) != asset_id:
            fail(f"BuildingCatalog does not wire {building_id} to {asset_id}", failures)

    if ATELIER_G421A_WAVE_REPORT_PATH.exists():
        report = ATELIER_G421A_WAVE_REPORT_PATH.read_text(encoding="utf-8")
        for required_text in [
            "core building atelier rebuild",
            "coherent starting-town architectural set",
            "Tavern/Inn is the required hero asset",
            "brick construction",
            "two front/back bridged twin-stack chimney sets",
            "Hotel Viking-inspired",
            "Old/unverified buildings are not automatically final",
        ]:
            if required_text not in report:
                fail(f"G-4.21A core building wave report missing text: {required_text}", failures)
        pass_check("G-4.21A core building rebuild wave report present")
    else:
        fail(f"missing G-4.21A core building wave report: {ATELIER_G421A_WAVE_REPORT_PATH}", failures)


def validate_g418e_hero_asset_family(failures: list[str]) -> None:
    wave = load_json(ATELIER_G418E_WAVE_MANIFEST_PATH, failures)
    if not wave:
        return
    if wave.get("schema_id") != "wayfarer.newport_atelier.g418e.hero_asset_family.v1":
        fail("G-4.18E hero asset family schema mismatch", failures)
    if wave.get("phase") != "G-4.18E":
        fail("G-4.18E hero asset family phase mismatch", failures)
    if wave.get("family_id") != "newport_harbor_commercial_tavern_district_asset_family":
        fail("G-4.18E family id mismatch", failures)
    if float(wave.get("visual_quality_gate", 0.0)) < 8.5:
        fail("G-4.18E visual gate must be at least 8.5", failures)
    if "no random prop scatter" not in str(wave.get("placement_policy", "")).lower():
        fail("G-4.18E placement policy must forbid random prop scatter", failures)
    packs = wave.get("packs", [])
    if not isinstance(packs, list):
        fail("G-4.18E packs must be a list", failures)
        packs = []
    pack_ids = {str(pack.get("pack_id", "")) for pack in packs if isinstance(pack, dict)}
    if pack_ids != ATELIER_G418E_PACK_IDS:
        fail(f"G-4.18E pack ids mismatch: {sorted(pack_ids)}", failures)
    else:
        pass_check("G-4.18E hero asset family pack ids")
    wave_assets = wave.get("assets", [])
    if not isinstance(wave_assets, list) or len(wave_assets) != 32:
        fail("G-4.18E hero asset family must contain exactly 32 assets", failures)
    wave_asset_ids = {str(asset.get("asset_id", "")) for asset in wave_assets if isinstance(asset, dict)}
    placed_asset_ids = {
        str(asset.get("asset_id", ""))
        for asset in wave_assets
        if isinstance(asset, dict) and asset.get("used_in_g418e_playable_hero_slice") is True
    }

    for raw_pack in packs:
        if not isinstance(raw_pack, dict):
            fail("G-4.18E pack entry is not an object", failures)
            continue
        pack = raw_pack
        pack_id = str(pack.get("pack_id", ""))
        for path_key in ["manifest", "source_image", "generation_prompt", "atlas", "contact_sheet", "validation_report", "provenance_report"]:
            rel_path = str(pack.get(path_key, ""))
            path_exists(rel_path, failures)
            if rel_path.endswith(".png"):
                path_exists(rel_path + ".import", failures)
        pack_manifest = load_json(PROJECT_ROOT / str(pack.get("manifest", "")), failures)
        qa_report = load_json(PROJECT_ROOT / str(pack.get("validation_report", "")), failures)
        if pack_manifest.get("schema_id") != f"wayfarer.newport_atelier.g418e.{pack_id}.manifest.v1":
            fail(f"G-4.18E {pack_id} manifest schema mismatch", failures)
        if pack_manifest.get("phase") != "G-4.18E":
            fail(f"G-4.18E {pack_id} manifest phase mismatch", failures)
        if pack_manifest.get("family_id") != "newport_harbor_commercial_tavern_district_asset_family":
            fail(f"G-4.18E {pack_id} manifest family mismatch", failures)
        if qa_report.get("schema_id") != "wayfarer.newport_atelier.g418e.extraction_qa.v1":
            fail(f"G-4.18E {pack_id} QA schema mismatch", failures)
        if qa_report.get("phase") != "G-4.18E":
            fail(f"G-4.18E {pack_id} QA phase mismatch", failures)
        if qa_report.get("status") != "PASS":
            fail(f"G-4.18E {pack_id} QA must pass", failures)
        assets = pack_manifest.get("assets", [])
        if not isinstance(assets, list) or len(assets) != 8:
            fail(f"G-4.18E {pack_id} manifest must contain 8 assets", failures)
            continue
        for raw_asset in assets:
            if not isinstance(raw_asset, dict):
                fail(f"G-4.18E {pack_id} asset entry is not an object", failures)
                continue
            asset = raw_asset
            asset_id = str(asset.get("asset_id", "unknown"))
            if asset_id not in wave_asset_ids:
                fail(f"{asset_id} missing from G-4.18E wave manifest", failures)
            for key in ["asset_id", "asset_type", "source_identity", "family_id", "path", "atlas", "atlas_region", "sprite_size", "generation_prompt", "source_image", "extraction_script", "input_sources", "provenance_status", "origin_classification", "commercial_use_status", "visual_quality_rating", "extraction_qa", "sha256"]:
                if key not in asset:
                    fail(f"{asset_id} missing G-4.18E field {key}", failures)
            if asset.get("provenance_status") != "ai_assisted_green_origin_candidate_pending_license_review":
                fail(f"{asset_id} G-4.18E provenance status mismatch", failures)
            if asset.get("origin_classification") != "green_origin_candidate_pending_license_review":
                fail(f"{asset_id} G-4.18E origin classification mismatch", failures)
            if asset.get("commercial_use_status") != "green_origin_candidate_pending_license_review":
                fail(f"{asset_id} G-4.18E commercial status mismatch", failures)
            if asset.get("final_commercial_candidate") is not False or asset.get("final_commercial_eligible") is not False:
                fail(f"{asset_id} incorrectly final-commercial promoted", failures)
            if asset.get("source_pixels_from_yellow_uncertain_assets") is not False:
                fail(f"{asset_id} uses yellow/uncertain source pixels", failures)
            if asset.get("source_pixels_from_third_party_material") is not False or asset.get("web_scraped_source_pixels") is not False:
                fail(f"{asset_id} uses unsafe external source pixels", failures)
            if float(asset.get("visual_quality_rating", 0.0)) < 8.5:
                fail(f"{asset_id} G-4.18E visual rating below 8.5", failures)
            path_exists(str(asset.get("path", "")), failures)
            path_exists(str(asset.get("path", "")) + ".import", failures)
            metrics = image_alpha_metrics(PROJECT_ROOT / str(asset.get("path", "")))
            if metrics.get("magenta_pixels_remaining") != 0:
                fail(f"{asset_id} has magenta pixels remaining", failures)
            if metrics.get("magenta_halo_pixels") != 0:
                fail(f"{asset_id} has magenta halo pixels", failures)
            if metrics.get("cutoff_edges"):
                fail(f"{asset_id} has crop/cutoff risk: {metrics.get('cutoff_edges')}", failures)
            if metrics.get("readable") is not True:
                fail(f"{asset_id} is not readable by alpha metrics", failures)
            qa = asset.get("extraction_qa", {})
            if not isinstance(qa, dict) or qa.get("status") != "PASS":
                fail(f"{asset_id} embedded G-4.18E extraction QA must pass", failures)

    map_layer = read_text(MAP_LAYER_PATH, failures)
    material_ids: set[str] = set()
    for const_name in [
        "NEWPORT_G418E_TAVERN_INN_MATERIALS",
        "NEWPORT_G418E_COMMERCIAL_AVENUE_MATERIALS",
        "NEWPORT_G418E_HARBOR_DOCK_EDGE_MATERIALS",
        "NEWPORT_G418E_REAR_SERVICE_CONNECTOR_MATERIALS",
    ]:
        material_ids.update(_extract_quoted_list(map_layer, const_name))
    if material_ids != wave_asset_ids:
        fail(f"G-4.18E MapLayer material ids mismatch: missing {sorted(wave_asset_ids - material_ids)} extra {sorted(material_ids - wave_asset_ids)}", failures)
    else:
        pass_check("G-4.18E MapLayer material ids")
    placed_in_map = {
        asset_id
        for asset_id in wave_asset_ids
        if map_layer.find('"asset_id": "' + asset_id + '"') >= 0
    }
    if placed_in_map != placed_asset_ids:
        fail(f"G-4.18E MapLayer placed ids mismatch: missing {sorted(placed_asset_ids - placed_in_map)} extra {sorted(placed_in_map - placed_asset_ids)}", failures)
    if "atelier_g418e_tavern_twin_stack_chimney_detail_01" in placed_in_map:
        fail("G-4.18E chimney detail must not be placed without roof integration", failures)
    if ATELIER_G418E_WAVE_REPORT_PATH.exists():
        report = ATELIER_G418E_WAVE_REPORT_PATH.read_text(encoding="utf-8")
        for required_text in ["not random prop scatter", "No asset is final-commercial promoted", "Agent Council"]:
            if required_text not in report:
                fail(f"G-4.18E report missing text: {required_text}", failures)
    else:
        fail(f"missing G-4.18E report: {ATELIER_G418E_WAVE_REPORT_PATH}", failures)


def validate_visual_production_registry(failures: list[str]) -> None:
    registry = load_json(VISUAL_REGISTRY_PATH, failures)
    if not registry:
        return
    if registry.get("schema_id") != "wayfarer.newport.visual_production_registry.v1":
        fail("visual production registry schema_id must be wayfarer.newport.visual_production_registry.v1", failures)
    else:
        pass_check("visual production registry schema id")
    registry_phase = str(registry.get("phase", ""))
    if registry_phase not in {"G-4.21A", "G-4.18E", "G-4.19"}:
        fail("visual production registry phase must be G-4.21A, G-4.18E, or G-4.19", failures)
    if "starting town/village" not in str(registry.get("north_star", "")):
        fail("visual production registry must restore the Newport starting town/village North Star", failures)
    registry_policy = str(registry.get("policy", ""))
    if registry_phase == "G-4.18E":
        for required_text in [
            "G-4.18E",
            "Newport Harbor Commercial + Tavern District",
            "AI-assisted green-origin candidates pending final generated-art license policy approval",
            "not final-commercial promoted",
        ]:
            if required_text not in registry_policy:
                fail(f"visual production registry G-4.18E policy missing: {required_text}", failures)
    elif registry_phase == "G-4.19":
        for required_text in [
            "G-4.19",
            "Player Visual Identity Foundation",
            "not final-commercial promoted",
            "old drawn player placeholder is deprecated",
        ]:
            if required_text not in registry_policy:
                fail(f"visual production registry G-4.19 policy missing: {required_text}", failures)
    else:
        if "core building atelier rebuild" not in registry_policy or "Tavern/Inn is the required hero centerpiece asset" not in registry_policy:
            fail("visual production registry must record the G-4.21A core building atelier rebuild policy", failures)
        for required_text in ["brick construction", "two front/back bridged twin-stack chimney sets", "Hotel Viking-inspired", "coherent starting-town architectural set"]:
            if required_text not in registry_policy:
                fail(f"visual production registry G-4.21A policy missing: {required_text}", failures)

    statuses = registry.get("status_taxonomy", [])
    if not isinstance(statuses, list):
        fail("visual production registry status_taxonomy must be a list", failures)
        statuses = []
    for status in sorted(VISUAL_REGISTRY_STATUS_TAXONOMY):
        if status not in statuses:
            fail(f"visual production registry status taxonomy missing {status}", failures)

    waves = registry.get("production_wave_plan", [])
    if not isinstance(waves, list):
        fail("visual production registry production_wave_plan must be a list", failures)
        waves = []
    expected_waves = [
        "wave_1_environmental_believability",
        "wave_2_town_identity",
        "wave_3_economy_life",
        "wave_4_building_rebuild_or_enhancement",
        "wave_5_character_npc_standard",
    ]
    wave_by_id = {str(wave.get("wave_id", "")): wave for wave in waves if isinstance(wave, dict)}
    for wave_id in expected_waves:
        if wave_id not in wave_by_id:
            fail(f"visual production registry missing production wave: {wave_id}", failures)
            continue
        wave = wave_by_id[wave_id]
        if wave.get("atelier_required") is not True:
            fail(f"{wave_id} must require the atelier pipeline", failures)
        scope = wave.get("scope", [])
        if not isinstance(scope, list) or len(scope) < 3:
            fail(f"{wave_id} must include a production scope list", failures)
    pass_check(f"visual production waves recorded: {len(wave_by_id)}")

    entries = registry.get("asset_entries", [])
    if not isinstance(entries, list):
        fail("visual production registry asset_entries must be a list", failures)
        return
    if len(entries) < 60:
        fail("visual production registry must classify the major Newport visual set", failures)
    else:
        pass_check(f"visual production registry entries: {len(entries)}")

    required_entry_fields = [
        "asset_id",
        "name",
        "category",
        "path",
        "source_provenance_status",
        "current_usage",
        "visual_quality_status",
        "gameplay_role",
        "rebuild_status",
        "notes",
    ]
    by_id: dict[str, dict] = {}
    for raw_entry in entries:
        if not isinstance(raw_entry, dict):
            fail("visual production registry entry is not an object", failures)
            continue
        asset_id = str(raw_entry.get("asset_id", ""))
        if not asset_id:
            fail("visual production registry entry missing asset_id", failures)
            continue
        if asset_id in by_id:
            fail(f"duplicate visual production registry asset id: {asset_id}", failures)
        by_id[asset_id] = raw_entry
        for field in required_entry_fields:
            if field not in raw_entry:
                fail(f"{asset_id} missing visual registry field {field}", failures)
        for status_field in ["visual_quality_status", "rebuild_status"]:
            status = str(raw_entry.get(status_field, ""))
            if status not in VISUAL_REGISTRY_STATUS_TAXONOMY:
                fail(f"{asset_id} has unsupported {status_field}: {status}", failures)
        rel_path = str(raw_entry.get("path", ""))
        path_exists(rel_path, failures)
        if not str(raw_entry.get("category", "")):
            fail(f"{asset_id} missing visual registry category", failures)
        if not str(raw_entry.get("source_provenance_status", "")):
            fail(f"{asset_id} missing source/provenance status", failures)
        usage = raw_entry.get("current_usage", {})
        if not isinstance(usage, dict):
            fail(f"{asset_id} current_usage must be an object", failures)
            usage = {}
        for usage_field in ["normal_review", "lab_only", "runtime_target"]:
            if usage_field not in usage:
                fail(f"{asset_id} current_usage missing {usage_field}", failures)

        provenance = str(raw_entry.get("source_provenance_status", ""))
        if raw_entry.get("visual_quality_status") == "APPROVED_FINAL" or raw_entry.get("rebuild_status") == "APPROVED_FINAL":
            if provenance not in FINAL_PROVENANCE_STATUSES:
                fail(f"{asset_id} is marked final without final provenance", failures)

        deprecated = bool(raw_entry.get("deprecated_visual_target", False)) or raw_entry.get("rebuild_status") == "DEPRECATED_DO_NOT_USE"
        if deprecated:
            if usage.get("normal_review") is True or usage.get("final_path") is True:
                fail(f"{asset_id} is deprecated but still marked for normal/final usage", failures)

        if asset_id.startswith("atelier_"):
            artifacts = raw_entry.get("atelier_artifacts", {})
            if not isinstance(artifacts, dict):
                fail(f"{asset_id} atelier_artifacts must be an object", failures)
                artifacts = {}
            for artifact_field in ATELIER_REQUIRED_ARTIFACT_FIELDS:
                if artifact_field not in artifacts:
                    fail(f"{asset_id} missing atelier artifact {artifact_field}", failures)
                else:
                    path_exists(str(artifacts.get(artifact_field, "")), failures)

        if asset_id == "player_wayfarer_foundation_g419":
            artifacts = raw_entry.get("player_identity_artifacts", {})
            if not isinstance(artifacts, dict):
                fail("player_wayfarer_foundation_g419 player_identity_artifacts must be an object", failures)
                artifacts = {}
            for artifact_field in [
                "manifest",
                "style_tokens",
                "brief",
                "generation_script",
                "validation_script",
                "atlas",
                "contact_sheet",
                "validation_report",
            ]:
                if artifact_field not in artifacts:
                    fail(f"player_wayfarer_foundation_g419 missing player identity artifact {artifact_field}", failures)
                else:
                    path_exists(str(artifacts.get(artifact_field, "")), failures)
            detail = raw_entry.get("provenance_detail", {})
            if not isinstance(detail, dict):
                fail("player_wayfarer_foundation_g419 provenance_detail must be an object", failures)
                detail = {}
            if detail.get("project_owned_deterministic_source") is not True:
                fail("player_wayfarer_foundation_g419 must declare project-owned deterministic source", failures)
            for provenance_key in [
                "source_pixels_from_yellow_uncertain_assets",
                "source_pixels_from_third_party_material",
                "web_scraped_source_pixels",
                "final_commercial_promoted",
            ]:
                if detail.get(provenance_key) is not False:
                    fail(f"player_wayfarer_foundation_g419 provenance must mark {provenance_key}=false", failures)

        if raw_entry.get("category") == "BUILDING" and usage.get("normal_review") is True:
            audit = raw_entry.get("building_audit", {})
            if not isinstance(audit, dict):
                fail(f"{asset_id} active building entry missing building_audit object", failures)
            else:
                for audit_field in [
                    "provenance_confidence",
                    "atelier_consistency",
                    "scale_perspective_fit",
                    "grounding_quality",
                    "town_role",
                ]:
                    if audit_field not in audit:
                        fail(f"{asset_id} building audit missing {audit_field}", failures)

    catalog = read_text(BUILDING_CATALOG_PATH, failures)
    blueprint = read_text(TOWN_BLUEPRINT_PATH, failures)
    map_layer = read_text(MAP_LAYER_PATH, failures)
    active_building_ids = _extract_quoted_list(blueprint, "STARTER_HARBOR_BUILDING_IDS")
    building_to_sprite = _extract_building_sprite_ids(catalog)
    for building_id in active_building_ids:
        sprite_id = building_to_sprite.get(building_id, "")
        if not sprite_id:
            fail(f"active building has no sprite id for visual registry cross-check: {building_id}", failures)
            continue
        if sprite_id not in by_id:
            fail(f"active building sprite missing from visual production registry: {building_id}:{sprite_id}", failures)
            continue
        entry = by_id[sprite_id]
        deprecated = bool(entry.get("deprecated_visual_target", False)) or entry.get("rebuild_status") == "DEPRECATED_DO_NOT_USE"
        if deprecated:
            fail(f"active building sprite is deprecated in visual production registry: {building_id}:{sprite_id}", failures)
        usage = entry.get("current_usage", {})
        if not isinstance(usage, dict) or usage.get("normal_review") is not True:
            fail(f"active building sprite must be normal-review in visual production registry: {building_id}:{sprite_id}", failures)

    for const_name in [
        "NEWPORT_HERO_ATLAS_MATERIALS",
        "NEWPORT_GREEN_ORIGIN_MATERIALS",
        "NEWPORT_ATELIER_CARGO_MATERIALS",
        "NEWPORT_ATELIER_DOCK_CLUTTER_MATERIALS",
        "NEWPORT_ATELIER_TERRAIN_EDGE_MATERIALS",
        "NEWPORT_ATELIER_COBBLE_PATH_MATERIALS",
        "NEWPORT_ATELIER_SHORELINE_MATERIALS",
        "NEWPORT_ATELIER_BUILDING_GROUNDING_MATERIALS",
        "NEWPORT_ATELIER_SIGN_SHOP_MARKER_MATERIALS",
        "NEWPORT_ATELIER_LAMPS_WAYFINDING_MATERIALS",
        "NEWPORT_ATELIER_CIVIC_MARKET_MATERIALS",
        "NEWPORT_ATELIER_SHOPFRONT_SUPPORT_MATERIALS",
        "NEWPORT_G418E_TAVERN_INN_MATERIALS",
        "NEWPORT_G418E_COMMERCIAL_AVENUE_MATERIALS",
        "NEWPORT_G418E_HARBOR_DOCK_EDGE_MATERIALS",
        "NEWPORT_G418E_REAR_SERVICE_CONNECTOR_MATERIALS",
    ]:
        for asset_id in _extract_quoted_list(map_layer, const_name):
            if asset_id not in by_id:
                fail(f"MapLayer material missing from visual production registry: {const_name}:{asset_id}", failures)

    for asset_id, entry in by_id.items():
        deprecated = bool(entry.get("deprecated_visual_target", False)) or entry.get("rebuild_status") == "DEPRECATED_DO_NOT_USE"
        if not deprecated:
            continue
        usage = entry.get("current_usage", {})
        rel_path = str(entry.get("path", ""))
        referenced_in_map_layer = asset_id in map_layer or (rel_path and rel_path in map_layer)
        if referenced_in_map_layer and not (isinstance(usage, dict) and usage.get("lab_only") is True and usage.get("normal_review") is False):
            fail(f"MapLayer references deprecated visual target outside lab-only scope: {asset_id}", failures)

    tavern = by_id.get(G421A_TAVERN_ASSET_ID, {})
    if not tavern:
        fail("G-4.21A Tavern/Inn hero asset missing from visual production registry", failures)
    if tavern.get("centerpiece_hero_rebuild_asset") is not True:
        fail("G-4.21A Tavern/Inn must be marked as centerpiece_hero_rebuild_asset", failures)
    if tavern.get("category") != "BUILDING":
        fail("G-4.21A Tavern/Inn must be registered as BUILDING", failures)
    if tavern.get("rebuild_status") != "APPROVED_TEMPORARY":
        fail("G-4.21A Tavern/Inn rebuild status must be APPROVED_TEMPORARY pending final policy", failures)
    tavern_usage = tavern.get("current_usage", {}) if isinstance(tavern, dict) else {}
    if not isinstance(tavern_usage, dict) or tavern_usage.get("normal_review") is not True:
        fail("G-4.21A Tavern/Inn hero asset must be active for normal review", failures)
    tavern_qa = tavern.get("building_qa", {}) if isinstance(tavern, dict) else {}
    if not isinstance(tavern_qa, dict):
        fail("G-4.21A Tavern/Inn registry entry must include building_qa", failures)
        tavern_qa = {}
    for required_key in [
        "brick_construction",
        "two_sets_large_twin_stack_chimneys",
        "front_back_bridged_chimney_pairs",
        "hero_centerpiece",
        "hotel_viking_inspired_not_direct_copy",
        "clear_entrance",
    ]:
        if tavern_qa.get(required_key) is not True:
            fail(f"G-4.21A Tavern/Inn registry QA missing {required_key}", failures)
    old_tavern = by_id.get("inn_tavern_v1", {})
    if isinstance(old_tavern, dict) and old_tavern:
        old_usage = old_tavern.get("current_usage", {})
        if old_tavern.get("rebuild_status") != "DEPRECATED_DO_NOT_USE":
            fail("old inn_tavern_v1 must be deprecated after G-4.21A replacement", failures)
        if isinstance(old_usage, dict) and old_usage.get("normal_review") is True:
            fail("old inn_tavern_v1 must not remain normal-review after G-4.21A replacement", failures)

    player_foundation = by_id.get("player_wayfarer_foundation_g419", {})
    if not player_foundation:
        fail("G-4.19 player visual identity foundation missing from visual production registry", failures)
    elif isinstance(player_foundation, dict):
        usage = player_foundation.get("current_usage", {})
        if not isinstance(usage, dict) or usage.get("normal_review") is not True:
            fail("G-4.19 player visual identity foundation must be active for normal review", failures)
        if player_foundation.get("rebuild_status") != "APPROVED_TEMPORARY":
            fail("G-4.19 player visual identity foundation must be approved temporary")
        if player_foundation.get("visual_quality_status") != "APPROVED_TEMPORARY":
            fail("G-4.19 player visual identity foundation visual status must be approved temporary")

    player_placeholder = by_id.get("player_placeholder_drawn", {})
    if isinstance(player_placeholder, dict) and player_placeholder:
        placeholder_usage = player_placeholder.get("current_usage", {})
        if player_placeholder.get("rebuild_status") != "DEPRECATED_DO_NOT_USE":
            fail("drawn player placeholder must be deprecated after G-4.19")
        if isinstance(placeholder_usage, dict) and placeholder_usage.get("normal_review") is True:
            fail("drawn player placeholder must not remain normal-review after G-4.19")

    if VISUAL_PRODUCTION_AUDIT_PATH.exists():
        report = VISUAL_PRODUCTION_AUDIT_PATH.read_text(encoding="utf-8")
        for required_text in [
            "North Star",
            "REBUILD_REQUIRED_CENTERPIECE",
            "Wave 1 - Environmental believability",
            "Wave 5 - Character/NPC standard",
            "No current Newport visual asset is promoted to `APPROVED_FINAL`",
        ]:
            if required_text not in report:
                fail(f"G-4.19B visual production audit missing text: {required_text}", failures)
        pass_check("G-4.19B visual production audit report present")
    else:
        fail(f"missing visual production audit report: {VISUAL_PRODUCTION_AUDIT_PATH}", failures)


def main() -> int:
    failures: list[str] = []
    manifest = load_json(MANIFEST_PATH, failures)
    legacy_manifest = load_json(LEGACY_MANIFEST_PATH, failures)
    if manifest and legacy_manifest and manifest.get("assets") == legacy_manifest.get("assets"):
        pass_check("legacy hero manifest mirrors canonical manifest assets")
    elif manifest and legacy_manifest:
        fail("legacy hero manifest must mirror canonical manifest assets", failures)

    if AUDIT_PATH.exists():
        audit = AUDIT_PATH.read_text(encoding="utf-8")
        if "No asset enters the player-facing review build unless it passes both Newport Visual Cohesion and Asset Provenance gates." in audit:
            pass_check("provenance audit includes permanent gate")
        else:
            fail("provenance audit missing permanent gate", failures)
    else:
        fail(f"missing audit report: {AUDIT_PATH}", failures)

    if manifest:
        validate_manifest(manifest, failures)
    validate_building_sprite_provenance(failures)
    validate_green_origin_asset_manifest(failures)
    validate_green_origin_bakeoff_manifest(failures)
    validate_atelier_cargo_manifest(failures)
    validate_atelier_dock_clutter_manifest(failures)
    validate_g420a_environmental_believability_wave(failures)
    validate_g420b_town_identity_wave(failures)
    validate_g421a_core_building_rebuild_wave(failures)
    validate_g418e_hero_asset_family(failures)
    validate_visual_production_registry(failures)

    if failures:
        print(f"Newport provenance validation: FAIL ({len(failures)} issue(s))")
        return 1
    print("Newport provenance validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
