#!/usr/bin/env python3
"""Validate G-4.18E Newport hero asset family artifacts and runtime wiring."""

from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[3]
ATELIER_ROOT = PROJECT_ROOT / "art_pipeline" / "newport_atelier"
WAVE_MANIFEST_PATH = ATELIER_ROOT / "manifests" / "newport_atelier_g418e_hero_asset_family_manifest.json"
REGIONS_PATH = ATELIER_ROOT / "manifests" / "newport_atelier_g418e_hero_asset_family_regions.json"
WAVE_REPORT_PATH = ATELIER_ROOT / "reports" / "G418E_GREEN_ORIGIN_HERO_ASSET_FAMILY.md"
VISUAL_REGISTRY_PATH = PROJECT_ROOT / "art_pipeline" / "newport" / "manifests" / "newport_visual_production_registry.json"
MAP_LAYER_PATH = PROJECT_ROOT / "scenes" / "map" / "MapLayer.gd"

PHASE = "G-4.18E"
FAMILY_ID = "newport_harbor_commercial_tavern_district_asset_family"
PROVENANCE_STATUS = "ai_assisted_green_origin_candidate_pending_license_review"
COMMERCIAL_STATUS = "green_origin_candidate_pending_license_review"
EXPECTED_PACK_IDS = {
    "tavern_inn_district",
    "commercial_avenue",
    "harbor_dock_edge",
    "rear_service_connector",
}
EXPECTED_MATERIAL_CONSTS = {
    "NEWPORT_G418E_TAVERN_INN_MATERIALS",
    "NEWPORT_G418E_COMMERCIAL_AVENUE_MATERIALS",
    "NEWPORT_G418E_HARBOR_DOCK_EDGE_MATERIALS",
    "NEWPORT_G418E_REAR_SERVICE_CONNECTOR_MATERIALS",
}
EXPECTED_PLACEMENT_CONSTS = {
    "NEWPORT_G418E_TAVERN_INN_PLACEMENTS",
    "NEWPORT_G418E_COMMERCIAL_AVENUE_PLACEMENTS",
    "NEWPORT_G418E_HARBOR_DOCK_EDGE_PLACEMENTS",
    "NEWPORT_G418E_REAR_SERVICE_CONNECTOR_PLACEMENTS",
}
REQUIRED_ARTIFACT_FIELDS = {
    "manifest",
    "source_image",
    "generation_prompt",
    "extraction_script",
    "atlas",
    "contact_sheet",
    "validation_report",
    "provenance_report",
}


def rel(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)
    print(f"FAIL: {message}")


def pass_check(message: str) -> None:
    print(f"PASS: {message}")


def load_json(path: Path, failures: list[str]) -> dict:
    if not path.exists():
        fail(f"missing JSON: {rel(path)}", failures)
        return {}
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON {rel(path)}: {exc}", failures)
        return {}
    if not isinstance(parsed, dict):
        fail(f"JSON root is not object: {rel(path)}", failures)
        return {}
    pass_check(f"loaded {rel(path)}")
    return parsed


def path_exists(rel_path: str, failures: list[str], require_import: bool = False) -> None:
    if not rel_path:
        fail("empty artifact path", failures)
        return
    path = PROJECT_ROOT / rel_path
    if path.exists():
        pass_check(f"path exists: {rel_path}")
    else:
        fail(f"path missing: {rel_path}", failures)
    if require_import and path.suffix.lower() == ".png":
        import_path = Path(str(path) + ".import")
        if import_path.exists():
            pass_check(f"Godot import exists: {rel_path}.import")
        else:
            fail(f"missing Godot import: {rel_path}.import", failures)


def _is_key_magenta(pixel: tuple[int, int, int, int]) -> bool:
    r, g, b, a = pixel
    return a > 0 and r > 170 and b > 170 and g < 150 and abs(r - b) < 120


def _is_magenta_halo(pixel: tuple[int, int, int, int]) -> bool:
    r, g, b, a = pixel
    return a > 0 and r >= 120 and b >= 120 and g <= 115 and abs(r - b) <= 80 and min(r, b) - g >= 38


def image_alpha_metrics(path: Path) -> dict:
    image = Image.open(path).convert("RGBA")
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        return {
            "alpha_pixels": 0,
            "magenta_pixels_remaining": 0,
            "magenta_halo_pixels": 0,
            "cutoff_edges": ["empty_alpha"],
            "readable": False,
        }
    pixels = image.load()
    magenta_pixels = 0
    halo_pixels = 0
    alpha_pixels = 0
    for y in range(image.height):
        for x in range(image.width):
            pixel = pixels[x, y]
            if pixel[3] <= 0:
                continue
            alpha_pixels += 1
            if _is_key_magenta(pixel):
                magenta_pixels += 1
            if _is_magenta_halo(pixel):
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
        "alpha_pixels": alpha_pixels,
        "magenta_pixels_remaining": magenta_pixels,
        "magenta_halo_pixels": halo_pixels,
        "cutoff_edges": [side for side, value in padding.items() if value < 6],
        "readable": alpha_pixels >= 1200 and bbox_w >= 48 and bbox_h >= 40,
    }


def extract_const_strings(source: str, const_name: str) -> list[str]:
    match = re.search(r"const\s+" + re.escape(const_name) + r"\s*:=\s*\[(.*?)\]", source, re.DOTALL)
    if not match:
        return []
    return re.findall(r'"([^"]+)"', match.group(1))


def extract_placement_ids(source: str, const_name: str) -> list[str]:
    match = re.search(r"const\s+" + re.escape(const_name) + r"\s*:=\s*\[(.*?)\]\n", source, re.DOTALL)
    if not match:
        return []
    return re.findall(r'"asset_id":\s*"([^"]+)"', match.group(1))


def validate_wave_manifest(wave: dict, failures: list[str]) -> tuple[set[str], set[str]]:
    if wave.get("schema_id") != "wayfarer.newport_atelier.g418e.hero_asset_family.v1":
        fail("G-4.18E wave schema mismatch", failures)
    if wave.get("phase") != PHASE:
        fail("G-4.18E wave phase mismatch", failures)
    if wave.get("family_id") != FAMILY_ID:
        fail("G-4.18E family_id mismatch", failures)
    if float(wave.get("visual_quality_gate", 0.0)) < 8.5:
        fail("G-4.18E visual quality gate below 8.5", failures)
    if "no random prop scatter" not in str(wave.get("placement_policy", "")).lower():
        fail("G-4.18E wave placement policy must forbid random prop scatter", failures)
    if "third-party" not in str(wave.get("source_policy", "")).lower():
        fail("G-4.18E source policy must mention third-party exclusions", failures)

    packs = wave.get("packs", [])
    if not isinstance(packs, list):
        fail("G-4.18E packs must be a list", failures)
        packs = []
    pack_ids = {str(pack.get("pack_id", "")) for pack in packs if isinstance(pack, dict)}
    if pack_ids != EXPECTED_PACK_IDS:
        fail(f"G-4.18E pack ids mismatch: {sorted(pack_ids)}", failures)
    else:
        pass_check("G-4.18E pack ids complete")

    assets = wave.get("assets", [])
    if not isinstance(assets, list):
        fail("G-4.18E assets must be a list", failures)
        assets = []
    if len(assets) != 32:
        fail(f"G-4.18E wave must contain 32 assets, found {len(assets)}", failures)
    else:
        pass_check("G-4.18E wave asset count 32")
    wave_asset_ids = {str(asset.get("asset_id", "")) for asset in assets if isinstance(asset, dict)}
    placed_asset_ids = {str(asset.get("asset_id", "")) for asset in assets if isinstance(asset, dict) and asset.get("used_in_g418e_playable_hero_slice") is True}
    return wave_asset_ids, placed_asset_ids


def validate_pack(pack: dict, wave_asset_ids: set[str], failures: list[str]) -> None:
    pack_id = str(pack.get("pack_id", ""))
    for path_key in ["manifest", "source_image", "generation_prompt", "atlas", "contact_sheet", "validation_report", "provenance_report"]:
        rel_path = str(pack.get(path_key, ""))
        path_exists(rel_path, failures, require_import=path_key in {"source_image", "atlas", "contact_sheet"})

    manifest_path = PROJECT_ROOT / str(pack.get("manifest", ""))
    manifest = load_json(manifest_path, failures)
    if not manifest:
        return
    if manifest.get("phase") != PHASE:
        fail(f"{pack_id} manifest phase mismatch", failures)
    if manifest.get("family_id") != FAMILY_ID:
        fail(f"{pack_id} manifest family_id mismatch", failures)
    if manifest.get("pack_id") != pack_id:
        fail(f"{pack_id} manifest pack id mismatch", failures)
    if "third-party" not in str(manifest.get("source_policy", "")).lower():
        fail(f"{pack_id} manifest source policy must mention third-party exclusions", failures)

    qa = load_json(PROJECT_ROOT / str(pack.get("validation_report", "")), failures)
    if qa.get("schema_id") != "wayfarer.newport_atelier.g418e.extraction_qa.v1":
        fail(f"{pack_id} QA schema mismatch", failures)
    if qa.get("phase") != PHASE:
        fail(f"{pack_id} QA phase mismatch", failures)
    if qa.get("status") != "PASS":
        fail(f"{pack_id} QA must be PASS", failures)

    assets = manifest.get("assets", [])
    if not isinstance(assets, list) or len(assets) != 8:
        fail(f"{pack_id} manifest must contain exactly 8 assets", failures)
        return
    for asset in assets:
        if not isinstance(asset, dict):
            fail(f"{pack_id} asset entry is not an object", failures)
            continue
        asset_id = str(asset.get("asset_id", ""))
        if asset_id not in wave_asset_ids:
            fail(f"{asset_id} missing from G-4.18E wave manifest", failures)
        for field in [
            "asset_id",
            "asset_type",
            "source_identity",
            "family_id",
            "path",
            "atlas",
            "atlas_region",
            "sprite_size",
            "generation_prompt",
            "source_image",
            "extraction_script",
            "input_sources",
            "provenance_status",
            "origin_classification",
            "commercial_use_status",
            "visual_quality_rating",
            "extraction_qa",
            "sha256",
        ]:
            if field not in asset:
                fail(f"{asset_id} missing field {field}", failures)
        if asset.get("family_id") != FAMILY_ID:
            fail(f"{asset_id} family_id mismatch", failures)
        if asset.get("provenance_status") != PROVENANCE_STATUS:
            fail(f"{asset_id} provenance status mismatch", failures)
        if asset.get("origin_classification") != COMMERCIAL_STATUS or asset.get("commercial_use_status") != COMMERCIAL_STATUS:
            fail(f"{asset_id} commercial classification mismatch", failures)
        if asset.get("final_commercial_candidate") is not False or asset.get("final_commercial_eligible") is not False:
            fail(f"{asset_id} incorrectly final-commercial promoted", failures)
        if asset.get("source_pixels_from_yellow_uncertain_assets") is not False:
            fail(f"{asset_id} has yellow/uncertain source pixels", failures)
        if asset.get("source_pixels_from_third_party_material") is not False or asset.get("web_scraped_source_pixels") is not False:
            fail(f"{asset_id} has unsafe external source pixels", failures)
        if float(asset.get("visual_quality_rating", 0.0)) < 8.5:
            fail(f"{asset_id} visual rating below 8.5", failures)
        for source in asset.get("input_sources", []):
            if isinstance(source, dict) and source.get("source_pixels_used") is True:
                if source.get("commercial_status") != COMMERCIAL_STATUS:
                    fail(f"{asset_id} source-pixel input is not G-4.18E green-origin candidate status", failures)
        asset_path = PROJECT_ROOT / str(asset.get("path", ""))
        path_exists(str(asset.get("path", "")), failures, require_import=True)
        metrics = image_alpha_metrics(asset_path)
        if metrics["magenta_pixels_remaining"] != 0:
            fail(f"{asset_id} has magenta pixels remaining", failures)
        if metrics["magenta_halo_pixels"] != 0:
            fail(f"{asset_id} has magenta halo pixels", failures)
        if metrics["cutoff_edges"]:
            fail(f"{asset_id} has cutoff/crop edge risk: {metrics['cutoff_edges']}", failures)
        if metrics["readable"] is not True:
            fail(f"{asset_id} alpha footprint is not readable", failures)
        asset_qa = asset.get("extraction_qa", {})
        if not isinstance(asset_qa, dict) or asset_qa.get("status") != "PASS":
            fail(f"{asset_id} embedded extraction QA is not PASS", failures)


def validate_registry_and_map(wave_asset_ids: set[str], placed_asset_ids: set[str], failures: list[str]) -> None:
    registry = load_json(VISUAL_REGISTRY_PATH, failures)
    entries = registry.get("asset_entries", []) if registry else []
    registry_by_id = {str(entry.get("asset_id", "")): entry for entry in entries if isinstance(entry, dict)}
    for asset_id in wave_asset_ids:
        entry = registry_by_id.get(asset_id)
        if not entry:
            fail(f"{asset_id} missing from Newport visual production registry", failures)
            continue
        if entry.get("source_provenance_status") != PROVENANCE_STATUS:
            fail(f"{asset_id} registry provenance mismatch", failures)
        usage = entry.get("current_usage", {})
        if not isinstance(usage, dict):
            fail(f"{asset_id} registry current_usage must be object", failures)
            continue
        if usage.get("lab_only") is not False or usage.get("normal_review") is not True:
            fail(f"{asset_id} registry review usage flags incorrect", failures)
        if asset_id in placed_asset_ids and usage.get("used_in_g418e_playable_hero_slice") is not True:
            fail(f"{asset_id} registry missing placed hero-slice flag", failures)
        artifacts = entry.get("atelier_artifacts", {})
        if not isinstance(artifacts, dict):
            fail(f"{asset_id} registry atelier_artifacts must be object", failures)
            continue
        for field in REQUIRED_ARTIFACT_FIELDS:
            if field not in artifacts:
                fail(f"{asset_id} registry missing artifact {field}", failures)
            else:
                path_exists(str(artifacts[field]), failures, require_import=str(artifacts[field]).endswith(".png"))

    map_source = MAP_LAYER_PATH.read_text(encoding="utf-8")
    if 'NEWPORT_G418E_HERO_ASSET_FAMILY_VERSION := "G-4.18E"' not in map_source:
        fail("MapLayer missing G-4.18E version constant", failures)
    material_ids: set[str] = set()
    for const_name in EXPECTED_MATERIAL_CONSTS:
        ids = extract_const_strings(map_source, const_name)
        if not ids:
            fail(f"MapLayer missing material const {const_name}", failures)
        material_ids.update(ids)
    if material_ids != wave_asset_ids:
        fail(f"MapLayer G-4.18E material ids mismatch: missing {sorted(wave_asset_ids - material_ids)} extra {sorted(material_ids - wave_asset_ids)}", failures)
    else:
        pass_check("MapLayer G-4.18E materials match wave manifest")

    placement_ids: set[str] = set()
    for const_name in EXPECTED_PLACEMENT_CONSTS:
        ids = extract_placement_ids(map_source, const_name)
        if not ids:
            fail(f"MapLayer missing placement const {const_name}", failures)
        placement_ids.update(ids)
    if placement_ids != placed_asset_ids:
        fail(f"MapLayer G-4.18E placement ids mismatch: missing {sorted(placed_asset_ids - placement_ids)} extra {sorted(placement_ids - placed_asset_ids)}", failures)
    else:
        pass_check("MapLayer G-4.18E placements match playable hero-slice manifest flags")

    if "atelier_g418e_tavern_twin_stack_chimney_detail_01" in placement_ids:
        fail("Tavern chimney detail candidate must not be placed without roof integration", failures)


def main() -> int:
    failures: list[str] = []
    wave = load_json(WAVE_MANIFEST_PATH, failures)
    regions = load_json(REGIONS_PATH, failures)
    if not regions:
        fail("G-4.18E regions JSON missing", failures)
    if WAVE_REPORT_PATH.exists():
        report = WAVE_REPORT_PATH.read_text(encoding="utf-8")
        for required in ["not random prop scatter", "No asset is final-commercial promoted", "runtime", "Agent Council"]:
            if required not in report:
                fail(f"G-4.18E report missing text: {required}", failures)
    else:
        fail(f"missing G-4.18E wave report: {rel(WAVE_REPORT_PATH)}", failures)
    if not wave:
        print("G-4.18E hero asset family validation: FAIL")
        return 1

    wave_asset_ids, placed_asset_ids = validate_wave_manifest(wave, failures)
    for raw_pack in wave.get("packs", []):
        if isinstance(raw_pack, dict):
            validate_pack(raw_pack, wave_asset_ids, failures)
        else:
            fail("G-4.18E pack entry is not an object", failures)
    validate_registry_and_map(wave_asset_ids, placed_asset_ids, failures)

    if failures:
        print(f"G-4.18E hero asset family validation: FAIL ({len(failures)} issue(s))")
        return 1
    print("G-4.18E hero asset family validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
