#!/usr/bin/env python3
"""Validate Newport asset manifest and provenance gates."""

from __future__ import annotations

import json
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[3]
PIPELINE_ROOT = PROJECT_ROOT / "art_pipeline" / "newport"
MANIFEST_PATH = PIPELINE_ROOT / "manifests" / "newport_asset_manifest.json"
LEGACY_MANIFEST_PATH = PIPELINE_ROOT / "manifests" / "newport_hero_street_assets.json"
BUILDING_PROVENANCE_PATH = PIPELINE_ROOT / "manifests" / "newport_building_sprite_provenance.json"
AUDIT_PATH = PIPELINE_ROOT / "reports" / "G417_G418_ASSET_PROVENANCE_AUDIT.md"
BUILDING_AUDIT_PATH = PIPELINE_ROOT / "reports" / "G418A_BUILDING_SPRITE_PROVENANCE_AUDIT.md"
GREEN_ORIGIN_ROOT = PROJECT_ROOT / "art_pipeline" / "newport_green_origin"
GREEN_ORIGIN_MANIFEST_PATH = GREEN_ORIGIN_ROOT / "manifests" / "green_origin_asset_manifest.json"
GREEN_ORIGIN_BAKEOFF_MANIFEST_PATH = GREEN_ORIGIN_ROOT / "manifests" / "green_origin_method_bakeoff_manifest.json"
GREEN_ORIGIN_REPORT_PATH = GREEN_ORIGIN_ROOT / "reports" / "G418B_GREEN_ORIGIN_ASSET_FACTORY.md"
GREEN_ORIGIN_BAKEOFF_REPORT_PATH = GREEN_ORIGIN_ROOT / "reports" / "G418D_GREEN_ORIGIN_METHOD_BAKEOFF.md"
GREEN_ORIGIN_CAPABILITY_REPORT_PATH = GREEN_ORIGIN_ROOT / "reports" / "G418D2_ART_PRODUCTION_CAPABILITY_GATE.md"
BUILDING_CATALOG_PATH = PROJECT_ROOT / "scripts" / "BuildingCatalog.gd"
TOWN_BLUEPRINT_PATH = PROJECT_ROOT / "scripts" / "NewportTownBlueprint.gd"
ISOLATED_BUILDING_DIR = PROJECT_ROOT / "assets" / "sprites" / "buildings" / "isolated"
ORIGIN_TAXONOMY = {"temporary_review_yellow", "green_origin_candidate", "final_commercial_green", "red_unsafe"}
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

    if failures:
        print(f"Newport provenance validation: FAIL ({len(failures)} issue(s))")
        return 1
    print("Newport provenance validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
