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
AUDIT_PATH = PIPELINE_ROOT / "reports" / "G417_G418_ASSET_PROVENANCE_AUDIT.md"


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)
    print(f"FAIL: {message}")


def pass_check(message: str) -> None:
    print(f"PASS: {message}")


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
    if "Visual Cohesion" in gate and "Asset Provenance" in gate:
        pass_check("permanent visual/provenance gate recorded")
    else:
        fail("source_policy must include both Visual Cohesion and Asset Provenance gates", failures)

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
        "provenance_status",
        "placeholder",
        "final",
        "review_eligible",
        "license_ownership_status",
        "source_pixels_from_prior_wayfarer_assets",
        "source_pixels_from_project_owned_wayfarer_assets",
        "source_pixels_from_third_party_material",
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
        if asset.get("provenance_status") != "passed":
            fail(f"{asset_id} provenance_status must be passed", failures)
        if asset.get("placeholder") is not False:
            fail(f"{asset_id} must not be placeholder in review manifest", failures)
        if asset.get("review_eligible") is not True:
            fail(f"{asset_id} must be review_eligible", failures)
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
        if "no third-party" not in str(source.get("license", "")).lower():
            fail(f"{asset_id} license text must forbid third-party pixels", failures)
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
        pass_check("all review-facing assets pass provenance gate")


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

    if failures:
        print(f"Newport provenance validation: FAIL ({len(failures)} issue(s))")
        return 1
    print("Newport provenance validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
