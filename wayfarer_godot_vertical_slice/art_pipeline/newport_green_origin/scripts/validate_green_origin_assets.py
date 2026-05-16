#!/usr/bin/env python3
"""Validate the G-4.18B-G-4.18D.3 green-origin Newport asset manifests."""

from __future__ import annotations

import json
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[3]
PIPELINE_ROOT = PROJECT_ROOT / "art_pipeline" / "newport_green_origin"
MANIFEST_PATH = PIPELINE_ROOT / "manifests" / "green_origin_asset_manifest.json"
BAKEOFF_MANIFEST_PATH = PIPELINE_ROOT / "manifests" / "green_origin_method_bakeoff_manifest.json"
REPORT_PATH = PIPELINE_ROOT / "reports" / "G418B_GREEN_ORIGIN_ASSET_FACTORY.md"
BAKEOFF_REPORT_PATH = PIPELINE_ROOT / "reports" / "G418D_GREEN_ORIGIN_METHOD_BAKEOFF.md"
CAPABILITY_REPORT_PATH = PIPELINE_ROOT / "reports" / "G418D2_ART_PRODUCTION_CAPABILITY_GATE.md"
PIXEL_ATELIER_REPORT_PATH = PIPELINE_ROOT / "reports" / "G418D3_PIXEL_BY_PIXEL_SPRITE_ATELIER.md"
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
REQUIRED_BAKEOFF_FIELDS = [
    "candidate_id",
    "method_name",
    "asset_family",
    "sample_path",
    "sample_type",
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
    "lab_access_mode",
    "recommendation",
    "production_scalability_notes",
    "risk_notes",
    "input_sources",
    "source_pixels_from_yellow_uncertain_assets",
    "source_pixels_from_third_party_material",
    "web_scraped_source_pixels",
    "ownership",
    "license",
    "sha256",
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
    if "green-origin provenance is necessary but not sufficient" not in str(manifest.get("visual_quality_gate", "")).lower():
        fail("green-origin manifest must record the G-4.18C visual quality gate", failures)

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
        if asset.get("provenance_status") != "green_origin_candidate":
            fail(f"{asset_id} provenance_status must remain green_origin_candidate", failures)
        if asset.get("origin_classification") != "green_origin_candidate":
            fail(f"{asset_id} origin_classification must remain green_origin_candidate", failures)
        if asset.get("visual_quality_status") != "visual_failed_g418b_proof":
            fail(f"{asset_id} must be visually quarantined as visual_failed_g418b_proof", failures)
        if asset.get("review_eligible") is not False:
            fail(f"{asset_id} must be blocked from normal review after G-4.18C", failures)
        if asset.get("normal_review_eligible") is not False:
            fail(f"{asset_id} normal_review_eligible must be false after G-4.18C", failures)
        if asset.get("lab_only") is not True:
            fail(f"{asset_id} lab_only must be true after G-4.18C", failures)
        if asset.get("final_commercial_candidate") is not False:
            fail(f"{asset_id} final_commercial_candidate must be false while visually failed", failures)
        if asset.get("final_commercial_eligible") is not False:
            fail(f"{asset_id} final_commercial_eligible must be false while visually failed", failures)
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


def validate_bakeoff_manifest(manifest: dict, failures: list[str]) -> None:
    if manifest.get("schema_id") != "wayfarer.newport_green_origin.method_bakeoff.v1":
        fail("bakeoff manifest schema_id must be wayfarer.newport_green_origin.method_bakeoff.v1", failures)
    else:
        pass_check("G-4.18D bakeoff/capability manifest schema id")
    if manifest.get("phase") != "G-4.18D.3":
        fail("bakeoff manifest phase must be G-4.18D.3", failures)
    if "G-4.18D.3" not in str(manifest.get("normal_review_policy", "")):
        fail("bakeoff manifest must block G-4.18D.3 candidates from normal review", failures)
    if manifest.get("recommended_method_for_g418e") is not None:
        fail("G-4.18D.2 manifest must not recommend a promotion method", failures)
    gate_text = str(manifest.get("visual_quality_gate", ""))
    if "8.5" not in gate_text or "7.5" not in gate_text or "G-4.18D.3" not in gate_text:
        fail("G-4.18D.3 manifest must declare the 8.5 bakeoff and 7.5 capability visual gates", failures)

    for contact_sheet in manifest.get("contact_sheets", []):
        path_exists(str(contact_sheet), failures)

    candidates = manifest.get("candidates", [])
    if not isinstance(candidates, list) or len(candidates) != 6:
        fail("G-4.18D.2 manifest must retain 5 corrected methods plus M01B", failures)
        return
    pass_check("G-4.18D.2 retained bakeoff candidate count: 6")

    recommendations = {str(candidate.get("recommendation", "")) for candidate in candidates if isinstance(candidate, dict)}
    for required in {"DEFER", "FAIL"}:
        if required not in recommendations:
            fail(f"bakeoff recommendations missing {required}", failures)
    if "PASS" in recommendations:
        fail("G-4.18D.2 must not keep any bakeoff PASS recommendation below the 8.5 visual gate", failures)

    pass_count = 0
    for candidate in candidates:
        if not isinstance(candidate, dict):
            fail("bakeoff candidate entry is not an object", failures)
            continue
        candidate_id = str(candidate.get("candidate_id", "unknown"))
        for field in REQUIRED_BAKEOFF_FIELDS:
            if field not in candidate:
                fail(f"{candidate_id} missing bakeoff field {field}", failures)
        path_exists(str(candidate.get("sample_path", "")), failures)
        if candidate.get("phase") != "G-4.18D.1":
            fail(f"{candidate_id} retained bakeoff phase must remain G-4.18D.1", failures)
        if candidate.get("provenance_status") != "green_origin_candidate":
            fail(f"{candidate_id} provenance_status must be green_origin_candidate", failures)
        if candidate.get("origin_classification") != "green_origin_candidate":
            fail(f"{candidate_id} origin_classification must be green_origin_candidate", failures)
        if candidate.get("commercial_use_status") != "green_origin_candidate":
            fail(f"{candidate_id} commercial_use_status must be green_origin_candidate", failures)
        if candidate.get("review_eligible") is not False:
            fail(f"{candidate_id} review_eligible must be false for lab-only bakeoff", failures)
        if candidate.get("normal_review_eligible") is not False:
            fail(f"{candidate_id} normal_review_eligible must be false for lab-only bakeoff", failures)
        if candidate.get("lab_only") is not True:
            fail(f"{candidate_id} lab_only must be true for bakeoff candidates", failures)
        if candidate.get("final_commercial_eligible") is not False:
            fail(f"{candidate_id} final_commercial_eligible must be false before later screenshot acceptance", failures)
        visual_rating = float(candidate.get("visual_rating", 0.0))
        visual_gate = float(candidate.get("visual_pass_gate", 0.0))
        if visual_gate < 8.5:
            fail(f"{candidate_id} visual_pass_gate must be at least 8.5", failures)
        if visual_rating < 8.5 and candidate.get("recommendation") == "PASS":
            fail(f"{candidate_id} cannot be PASS below the 8.5 visual gate", failures)
        if visual_rating < 8.5 and candidate.get("final_commercial_candidate") is not False:
            fail(f"{candidate_id} cannot be final_commercial_candidate below the 8.5 visual gate", failures)
        if candidate.get("source_pixels_from_yellow_uncertain_assets") is not False:
            fail(f"{candidate_id} uses yellow/uncertain source pixels", failures)
        if candidate.get("source_pixels_from_third_party_material") is not False:
            fail(f"{candidate_id} uses third-party source pixels", failures)
        if candidate.get("web_scraped_source_pixels") is not False:
            fail(f"{candidate_id} uses web-scraped source pixels", failures)
        recommendation = str(candidate.get("recommendation", ""))
        if recommendation == "PASS":
            pass_count += 1
            if visual_rating < 8.5:
                fail(f"{candidate_id} PASS candidate must meet the 8.5 visual gate", failures)
        elif recommendation == "DEFER":
            if "defer" not in str(candidate.get("visual_quality_status", "")):
                fail(f"{candidate_id} DEFER candidate must record defer visual status", failures)
        elif recommendation == "FAIL":
            if "fail" not in str(candidate.get("visual_quality_status", "")):
                fail(f"{candidate_id} FAIL candidate must record visual failure", failures)
        else:
            fail(f"{candidate_id} recommendation must be PASS, DEFER, or FAIL", failures)

        for raw_source in candidate.get("input_sources", []):
            if not isinstance(raw_source, dict):
                fail(f"{candidate_id} input source is not object", failures)
                continue
            source_text = json.dumps(raw_source, sort_keys=True).lower()
            for forbidden in FORBIDDEN_INPUT_FRAGMENTS:
                if forbidden.lower() in source_text:
                    fail(f"{candidate_id} forbidden input source reference: {forbidden}", failures)
            source_uses_pixels = raw_source.get("source_pixels_used")
            source_path = str(raw_source.get("path", ""))
            if source_uses_pixels is not False:
                allowed_m01b_substrate = (
                    candidate_id == "method_01b_manual_paintover_proof"
                    and source_uses_pixels is True
                    and source_path.endswith("method_01_generated_base_pixel_cleanup.png")
                )
                if not allowed_m01b_substrate:
                    fail(f"{candidate_id} input source must not use source pixels: {source_path or 'unknown'}", failures)
            if "path" in raw_source:
                path_exists(str(raw_source["path"]), failures)

    if pass_count != 0:
        fail("G-4.18D.2 retained bakeoff must identify zero PASS candidates", failures)

    capability = manifest.get("art_production_capability_gate", {})
    if not isinstance(capability, dict) or not capability:
        fail("G-4.18D.2 manifest must include one art_production_capability_gate object", failures)
    else:
        required_capability_fields = [
            "phase",
            "asset_id",
            "asset_name",
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
        asset_id = str(capability.get("asset_id", "unknown"))
        for field in required_capability_fields:
            if field not in capability:
                fail(f"{asset_id} missing capability field {field}", failures)
        if capability.get("phase") != "G-4.18D.2":
            fail(f"{asset_id} phase must be G-4.18D.2", failures)
        for path_field in ["sample_path", "rough_base_path", "prepared_path", "isolated_proof_path", "before_after_path", "in_world_comparison_path", "source_file"]:
            path_exists(str(capability.get(path_field, "")), failures)
        if capability.get("provenance_status") != "green_origin_candidate":
            fail(f"{asset_id} provenance_status must be green_origin_candidate", failures)
        if capability.get("origin_classification") != "green_origin_candidate":
            fail(f"{asset_id} origin_classification must be green_origin_candidate", failures)
        if capability.get("commercial_use_status") != "green_origin_candidate":
            fail(f"{asset_id} commercial_use_status must be green_origin_candidate", failures)
        if capability.get("review_eligible") is not False:
            fail(f"{asset_id} review_eligible must be false for the capability gate", failures)
        if capability.get("normal_review_eligible") is not False:
            fail(f"{asset_id} normal_review_eligible must be false for the capability gate", failures)
        if capability.get("lab_only") is not True:
            fail(f"{asset_id} lab_only must be true for the capability gate", failures)
        if capability.get("final_commercial_eligible") is not False:
            fail(f"{asset_id} final_commercial_eligible must be false", failures)
        if capability.get("source_pixels_from_yellow_uncertain_assets") is not False:
            fail(f"{asset_id} uses yellow/uncertain source pixels", failures)
        if capability.get("source_pixels_from_third_party_material") is not False:
            fail(f"{asset_id} uses third-party source pixels", failures)
        if capability.get("web_scraped_source_pixels") is not False:
            fail(f"{asset_id} uses web-scraped source pixels", failures)
        visual_rating = float(capability.get("visual_rating", 0.0))
        visual_gate = float(capability.get("visual_pass_gate", 0.0))
        verdict = str(capability.get("capability_verdict", ""))
        if visual_gate < 7.5:
            fail(f"{asset_id} visual_pass_gate must be at least 7.5", failures)
        if visual_rating < 7.5 and verdict == "PASS":
            fail(f"{asset_id} cannot PASS below the 7.5 visual gate", failures)
        if visual_rating < 7.5 and capability.get("final_commercial_candidate") is not False:
            fail(f"{asset_id} cannot be final_commercial_candidate below the 7.5 visual gate", failures)
        if verdict == "DEFER" and "defer" not in str(capability.get("visual_quality_status", "")):
            fail(f"{asset_id} DEFER verdict must record defer visual status", failures)
        if verdict not in ["PASS", "DEFER", "FAIL"]:
            fail(f"{asset_id} capability_verdict must be PASS, DEFER, or FAIL", failures)
        for raw_source in capability.get("input_sources", []):
            if not isinstance(raw_source, dict):
                fail(f"{asset_id} capability input source is not object", failures)
                continue
            source_text = json.dumps(raw_source, sort_keys=True).lower()
            for forbidden in FORBIDDEN_INPUT_FRAGMENTS:
                if forbidden.lower() in source_text:
                    fail(f"{asset_id} forbidden capability input source reference: {forbidden}", failures)
            if raw_source.get("source_pixels_used") is not False:
                fail(f"{asset_id} capability input source must not use source pixels", failures)
            if "path" in raw_source:
                path_exists(str(raw_source["path"]), failures)

    atelier = manifest.get("pixel_sprite_atelier_proof", {})
    if not isinstance(atelier, dict) or not atelier:
        fail("G-4.18D.3 manifest must include one pixel_sprite_atelier_proof object", failures)
    else:
        required_atelier_fields = [
            "phase",
            "asset_id",
            "asset_name",
            "sample_path",
            "pass_01_blockout_path",
            "pass_02_material_detail_path",
            "pass_03_polish_shadow_grounding_path",
            "krita_projection_path",
            "sprite_sheet_path",
            "isolated_1x_path",
            "grid_8x_path",
            "before_after_path",
            "palette_sheet_path",
            "in_world_comparison_path",
            "standard_comparison_path",
            "atelier_board_path",
            "source_file",
            "required_layers",
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
        asset_id = str(atelier.get("asset_id", "unknown"))
        for field in required_atelier_fields:
            if field not in atelier:
                fail(f"{asset_id} missing pixel atelier field {field}", failures)
        if atelier.get("phase") != "G-4.18D.3":
            fail(f"{asset_id} phase must be G-4.18D.3", failures)
        for path_field in [
            "sample_path",
            "pass_01_blockout_path",
            "pass_02_material_detail_path",
            "pass_03_polish_shadow_grounding_path",
            "krita_projection_path",
            "sprite_sheet_path",
            "isolated_1x_path",
            "grid_8x_path",
            "before_after_path",
            "palette_sheet_path",
            "in_world_comparison_path",
            "standard_comparison_path",
            "atelier_board_path",
            "source_file",
        ]:
            path_exists(str(atelier.get(path_field, "")), failures)
        for required_layer in [
            "silhouette_blockout",
            "dark_outline",
            "wood_base",
            "rope_base",
            "barrel_base",
            "metal_bands",
            "highlights",
            "chips_scratches",
            "grime",
            "cast_shadow",
            "contact_shadow",
        ]:
            if required_layer not in atelier.get("required_layers", []):
                fail(f"{asset_id} missing required layer {required_layer}", failures)
        if atelier.get("provenance_status") != "green_origin_candidate":
            fail(f"{asset_id} provenance_status must be green_origin_candidate", failures)
        if atelier.get("origin_classification") != "green_origin_candidate":
            fail(f"{asset_id} origin_classification must be green_origin_candidate", failures)
        if atelier.get("commercial_use_status") != "green_origin_candidate":
            fail(f"{asset_id} commercial_use_status must be green_origin_candidate", failures)
        if atelier.get("review_eligible") is not False:
            fail(f"{asset_id} review_eligible must remain false before human promotion", failures)
        if atelier.get("normal_review_eligible") is not False:
            fail(f"{asset_id} normal_review_eligible must remain false before human promotion", failures)
        if atelier.get("lab_only") is not True:
            fail(f"{asset_id} lab_only must be true while staged for review", failures)
        if atelier.get("final_commercial_eligible") is not False:
            fail(f"{asset_id} final_commercial_eligible must be false before human promotion", failures)
        if atelier.get("source_pixels_from_yellow_uncertain_assets") is not False:
            fail(f"{asset_id} uses yellow/uncertain source pixels", failures)
        if atelier.get("source_pixels_from_third_party_material") is not False:
            fail(f"{asset_id} uses third-party source pixels", failures)
        if atelier.get("web_scraped_source_pixels") is not False:
            fail(f"{asset_id} uses web-scraped source pixels", failures)
        visual_rating = float(atelier.get("visual_rating", 0.0))
        visual_gate = float(atelier.get("visual_pass_gate", 0.0))
        verdict = str(atelier.get("capability_verdict", ""))
        if visual_gate < 7.5:
            fail(f"{asset_id} visual_pass_gate must be at least 7.5", failures)
        if verdict == "PASS":
            if visual_rating < 7.5:
                fail(f"{asset_id} PASS must meet the 7.5 visual gate", failures)
            if atelier.get("final_commercial_candidate") is not True:
                fail(f"{asset_id} PASS should be recorded as a future commercial candidate", failures)
        elif verdict in ["DEFER", "FAIL"]:
            if visual_rating >= 7.5:
                fail(f"{asset_id} non-PASS should stay below the 7.5 visual gate", failures)
            if atelier.get("final_commercial_candidate") is not False:
                fail(f"{asset_id} non-PASS cannot be final_commercial_candidate", failures)
        else:
            fail(f"{asset_id} capability_verdict must be PASS, DEFER, or FAIL", failures)
        for raw_source in atelier.get("input_sources", []):
            if not isinstance(raw_source, dict):
                fail(f"{asset_id} pixel atelier input source is not object", failures)
                continue
            source_text = json.dumps(raw_source, sort_keys=True).lower()
            for forbidden in FORBIDDEN_INPUT_FRAGMENTS:
                if forbidden.lower() in source_text:
                    fail(f"{asset_id} forbidden pixel atelier input source: {forbidden}", failures)
            if raw_source.get("source_pixels_used") is not False:
                fail(f"{asset_id} pixel atelier input source must not use source pixels", failures)
            if "path" in raw_source:
                path_exists(str(raw_source["path"]), failures)

    if BAKEOFF_REPORT_PATH.exists():
        report = BAKEOFF_REPORT_PATH.read_text(encoding="utf-8")
        for required_text in [
            "North Star Relevance",
            "G-4.18D produced no accepted visual candidate",
            "M01 is downgraded",
        ]:
            if required_text not in report:
                fail(f"bakeoff report missing text: {required_text}", failures)
        pass_check("G-4.18D bakeoff report present")
    else:
        fail(f"missing G-4.18D bakeoff report: {BAKEOFF_REPORT_PATH}", failures)

    if CAPABILITY_REPORT_PATH.exists():
        report = CAPABILITY_REPORT_PATH.read_text(encoding="utf-8")
        for required_text in [
            "G-4.18D.2 produced one green-origin rope coil",
            "Was the failure due to tool access?",
            "Was the failure due to art-direction execution?",
            "Was the failure due to Codex not being able to perform finished-art production?",
            "DEFER",
        ]:
            if required_text not in report:
                fail(f"G-4.18D.2 capability report missing text: {required_text}", failures)
        pass_check("G-4.18D.2 capability report present")
    else:
        fail(f"missing G-4.18D.2 capability report: {CAPABILITY_REPORT_PATH}", failures)

    if PIXEL_ATELIER_REPORT_PATH.exists():
        report = PIXEL_ATELIER_REPORT_PATH.read_text(encoding="utf-8")
        for required_text in [
            "G-4.18D.3 produced one green-origin",
            "Pixel-Layer Source",
            "Krita CLI",
            "GIMP",
            "DEFER",
            "chandlery-standard comparison",
        ]:
            if required_text not in report:
                fail(f"G-4.18D.3 pixel atelier report missing text: {required_text}", failures)
        pass_check("G-4.18D.3 pixel atelier report present")
    else:
        fail(f"missing G-4.18D.3 pixel atelier report: {PIXEL_ATELIER_REPORT_PATH}", failures)


def main() -> int:
    failures: list[str] = []
    manifest = load_json(MANIFEST_PATH, failures)
    if manifest:
        validate_manifest(manifest, failures)
    bakeoff_manifest = load_json(BAKEOFF_MANIFEST_PATH, failures)
    if bakeoff_manifest:
        validate_bakeoff_manifest(bakeoff_manifest, failures)
    if failures:
        print(f"Green-origin validation: FAIL ({len(failures)} issue(s))")
        return 1
    print("Green-origin validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
