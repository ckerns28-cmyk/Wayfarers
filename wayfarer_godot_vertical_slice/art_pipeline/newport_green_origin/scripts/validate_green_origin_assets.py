#!/usr/bin/env python3
"""Validate the G-4.18B green-origin Newport asset manifest."""

from __future__ import annotations

import json
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[3]
PIPELINE_ROOT = PROJECT_ROOT / "art_pipeline" / "newport_green_origin"
MANIFEST_PATH = PIPELINE_ROOT / "manifests" / "green_origin_asset_manifest.json"
REPORT_PATH = PIPELINE_ROOT / "reports" / "G418B_GREEN_ORIGIN_ASSET_FACTORY.md"
FORBIDDEN_INPUT_FRAGMENTS = [
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
REQUIRED_ASSET_FIELDS = [
    "asset_id",
    "asset_type",
    "source_type",
    "created_by",
    "generation_script",
    "input_sources",
    "license",
    "ownership",
    "commercial_use_status",
    "review_eligible",
    "final_commercial_candidate",
    "notes",
]


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
    full_path = PROJECT_ROOT / rel_path
    if full_path.exists():
        pass_check(f"path exists: {rel_path}")
    else:
        fail(f"path missing: {rel_path}", failures)


def validate_manifest(manifest: dict, failures: list[str]) -> None:
    if manifest.get("schema_id") != "wayfarer.newport_green_origin.asset_manifest.v1":
        fail("green-origin manifest schema_id must be wayfarer.newport_green_origin.asset_manifest.v1", failures)
    else:
        pass_check("green-origin manifest schema id")

    taxonomy = manifest.get("origin_taxonomy", [])
    for required in ["temporary_review_yellow", "green_origin_candidate", "final_commercial_green", "red_unsafe"]:
        if required not in taxonomy:
            fail(f"origin taxonomy missing {required}", failures)
    if not failures:
        pass_check("origin taxonomy present")

    path_exists(str(manifest.get("atlas", "")), failures)
    path_exists(str(manifest.get("generated_asset_root", "")), failures)
    for contact_sheet in manifest.get("contact_sheets", []):
        path_exists(str(contact_sheet), failures)

    assets = manifest.get("assets", [])
    if not isinstance(assets, list) or len(assets) < 4:
        fail("green-origin manifest must contain at least 4 assets", failures)
        return
    pass_check(f"green-origin asset entries: {len(assets)}")

    seen: set[str] = set()
    for asset in assets:
        if not isinstance(asset, dict):
            fail("green-origin asset entry is not an object", failures)
            continue
        asset_id = str(asset.get("asset_id", ""))
        if not asset_id:
            fail("green-origin asset missing asset_id", failures)
            continue
        if asset_id in seen:
            fail(f"duplicate green-origin asset id: {asset_id}", failures)
        seen.add(asset_id)
        for field in REQUIRED_ASSET_FIELDS:
            if field not in asset:
                fail(f"{asset_id} missing field {field}", failures)
        path_exists(str(asset.get("path", "")), failures)
        path_exists(str(asset.get("generation_script", "")), failures)
        if asset.get("ownership") != "project-owned":
            fail(f"{asset_id} ownership must be project-owned", failures)
        if asset.get("source_type") != "deterministic_python_pillow":
            fail(f"{asset_id} source_type must be deterministic_python_pillow", failures)
        status = str(asset.get("commercial_use_status", ""))
        if status not in {"green_origin_candidate", "final_commercial_green"}:
            fail(f"{asset_id} commercial_use_status must be green_origin_candidate or final_commercial_green", failures)
        if asset.get("final_commercial_candidate") is True and status not in {"green_origin_candidate", "final_commercial_green"}:
            fail(f"{asset_id} final_commercial_candidate requires green status", failures)
        if asset.get("review_eligible") is not True:
            fail(f"{asset_id} must be review_eligible", failures)
        if asset.get("source_pixels_from_yellow_uncertain_assets") is not False:
            fail(f"{asset_id} uses yellow/uncertain source pixels", failures)
        if asset.get("source_pixels_from_third_party_material") is not False:
            fail(f"{asset_id} uses third-party source pixels", failures)
        if asset.get("web_scraped_source_pixels") is not False:
            fail(f"{asset_id} uses web-scraped source pixels", failures)

        for raw_source in asset.get("input_sources", []):
            if not isinstance(raw_source, dict):
                fail(f"{asset_id} input source is not object", failures)
                continue
            source_text = json.dumps(raw_source, sort_keys=True).lower()
            for forbidden in FORBIDDEN_INPUT_FRAGMENTS:
                if forbidden.lower() in source_text:
                    fail(f"{asset_id} forbidden input source reference: {forbidden}", failures)
            if raw_source.get("source_pixels_used") is not False:
                fail(f"{asset_id} input source must not use source pixels: {raw_source.get('path', 'unknown')}", failures)
            if "path" in raw_source:
                path_exists(str(raw_source["path"]), failures)

    if REPORT_PATH.exists():
        report = REPORT_PATH.read_text(encoding="utf-8")
        for required_text in ["green_origin_candidate", "No yellow Newport building sprite", "Godot Proof Area"]:
            if required_text not in report:
                fail(f"green-origin report missing text: {required_text}", failures)
        pass_check("green-origin report present")
    else:
        fail(f"missing green-origin report: {REPORT_PATH}", failures)


def main() -> int:
    failures: list[str] = []
    manifest = load_json(MANIFEST_PATH, failures)
    if manifest:
        validate_manifest(manifest, failures)
    if failures:
        print(f"Green-origin validation: FAIL ({len(failures)} issue(s))")
        return 1
    print("Green-origin validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
