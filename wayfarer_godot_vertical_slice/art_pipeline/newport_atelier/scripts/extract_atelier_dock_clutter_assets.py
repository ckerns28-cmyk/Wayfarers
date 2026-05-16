#!/usr/bin/env python3
"""Extract G-4.19A AI-assisted Newport atelier dock clutter sprites.

This follows the locked G-4.18D atelier cargo production pattern:
saved prompt/source, local chroma extraction, transparent sprites, atlas,
contact sheet, manifest, provenance report, Godot placement, and validation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[3]
PIPELINE_ROOT = PROJECT_ROOT / "art_pipeline" / "newport_atelier"
SOURCE_PATH = PIPELINE_ROOT / "source_generated" / "g419a_atelier_dock_clutter_sheet_imagegen.png"
PROMPT_PATH = PIPELINE_ROOT / "source_generated" / "g419a_atelier_dock_clutter_prompt.txt"
GENERATED_ROOT = PIPELINE_ROOT / "generated"
ATLAS_PATH = PIPELINE_ROOT / "atlases" / "newport_atelier_dock_clutter_v1.png"
CONTACT_PATH = PIPELINE_ROOT / "contact_sheets" / "newport_atelier_dock_clutter_contact_sheet.png"
MANIFEST_PATH = PIPELINE_ROOT / "manifests" / "newport_atelier_dock_clutter_manifest.json"
REPORT_PATH = PIPELINE_ROOT / "reports" / "G419A_NEWPORT_DOCK_CLUTTER_ATELIER_PACK.md"
QA_REPORT_PATH = PIPELINE_ROOT / "reports" / "newport_atelier_dock_clutter_extraction_qa.json"
ART_BIBLE_PATH = PROJECT_ROOT / "docs" / "NEWPORT_ART_BIBLE.md"
G418D_STANDARD_REPORT_PATH = PIPELINE_ROOT / "reports" / "G418D_ATELIER_CARGO_STANDARD.md"

MIN_CROP_PADDING = 6

ASSETS = {
    "atelier_dock_bollards_01": {
        "asset_type": "bollard_pair_prop",
        "crop": [38, 112, 385, 470],
        "source_identity": "top_left_weathered_bollard_pair",
        "pivot": {"x": 0.5, "y": 0.94},
        "recommended_game_scale": 0.19,
        "notes": "Weathered paired wharf bollards with iron caps, rope turns, wet-dark bases, and readable salt-worn wood grain.",
    },
    "atelier_mooring_hardware_01": {
        "asset_type": "rope_post_mooring_hardware_cluster",
        "crop": [400, 140, 760, 490],
        "source_identity": "top_second_rope_post_cleats_and_ringbolts",
        "pivot": {"x": 0.5, "y": 0.93},
        "recommended_game_scale": 0.19,
        "notes": "Compact mooring post cluster with cleats, ring bolts, planked footing, frayed rope, and blackened forged iron.",
    },
    "atelier_fishing_net_bundle_01": {
        "asset_type": "fishing_net_bundle_prop",
        "crop": [752, 120, 1133, 490],
        "source_identity": "top_third_folded_fishing_net_bundle",
        "pivot": {"x": 0.5, "y": 0.92},
        "recommended_game_scale": 0.20,
        "notes": "Folded dockside fishing net with cork floats, lead weights, knotted mesh, and harbor grime.",
    },
    "atelier_sacks_fish_baskets_01": {
        "asset_type": "sacks_and_fish_baskets_cluster",
        "crop": [1125, 120, 1530, 490],
        "source_identity": "top_right_burlap_sacks_and_woven_fish_baskets",
        "pivot": {"x": 0.5, "y": 0.93},
        "recommended_game_scale": 0.19,
        "notes": "Market-edge sacks and fish baskets with woven fiber detail, fish-market staining, and muted coastal grime.",
    },
    "atelier_anchor_rope_01": {
        "asset_type": "anchor_and_rope_prop",
        "crop": [35, 520, 360, 900],
        "source_identity": "bottom_left_small_iron_anchor_with_rope",
        "pivot": {"x": 0.5, "y": 0.94},
        "recommended_game_scale": 0.18,
        "notes": "Pitted iron anchor with bevel highlights, rope knot, and readable hook silhouette for wharf edges.",
    },
    "atelier_dock_repair_planks_01": {
        "asset_type": "stacked_planks_dock_repair_boards",
        "crop": [370, 560, 800, 900],
        "source_identity": "bottom_second_stacked_dock_repair_planks",
        "pivot": {"x": 0.5, "y": 0.93},
        "recommended_game_scale": 0.20,
        "notes": "Stacked repair boards and planks with saw marks, pegs, cracked ends, nail holes, and strong dock-work utility.",
    },
    "atelier_dock_lantern_01": {
        "asset_type": "dock_lantern_prop",
        "crop": [780, 520, 1080, 915],
        "source_identity": "bottom_third_compact_dock_lantern",
        "pivot": {"x": 0.5, "y": 0.95},
        "recommended_game_scale": 0.17,
        "notes": "Compact dock lantern with aged brass/iron frame, glass glint, soot, and planked base.",
    },
    "atelier_shoreline_debris_01": {
        "asset_type": "shoreline_debris_cluster",
        "crop": [1070, 560, 1534, 920],
        "source_identity": "bottom_right_driftwood_shells_seaweed_debris",
        "pivot": {"x": 0.5, "y": 0.90},
        "recommended_game_scale": 0.19,
        "notes": "Shoreline debris cluster with driftwood, shells, seaweed, broken crate slats, and low visual profile.",
    },
}


def rel(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _is_key_magenta(r: int, g: int, b: int, a: int) -> bool:
    if a <= 0:
        return False
    return r > 170 and b > 170 and g < 150 and abs(r - b) < 120


def _is_magenta_halo(r: int, g: int, b: int, a: int) -> bool:
    if a <= 0:
        return False
    return r >= 120 and b >= 120 and g <= 115 and abs(r - b) <= 80 and min(r, b) - g >= 38


def key_to_alpha(image: Image.Image) -> Image.Image:
    """Remove the #ff00ff chroma key and purple matte contamination."""
    image = image.convert("RGBA")
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            if _is_magenta_halo(r, g, b, a):
                pixels[x, y] = (r, g, b, 0)
                continue
            if max(r, b) < 175 and r > g + 20 and b > g + 20 and abs(r - b) < 88:
                shade = max(6, min(48, g + 14, (r + b + g) // 5))
                pixels[x, y] = (shade, shade, shade, a)
                continue
            magenta_dominant = r > g + 45 and b > g + 45 and abs(r - b) < 92
            saturated_key = r > 170 and b > 170 and g < 150 and abs(r - b) < 120
            if magenta_dominant or saturated_key:
                pixels[x, y] = (r, g, b, 0)
                continue
            if r > 120 and b > 120 and g < 145 and abs(r - b) < 110:
                neutral = max(g, min(r, b) - 38)
                pixels[x, y] = (neutral, neutral, neutral, a)
    return image


def trim_alpha(image: Image.Image, padding: int = 8) -> Image.Image:
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        return image
    x0, y0, x1, y1 = bbox
    return image.crop(
        (
            max(0, x0 - padding),
            max(0, y0 - padding),
            min(image.width, x1 + padding),
            min(image.height, y1 + padding),
        )
    )


def alpha_metrics(image: Image.Image) -> dict:
    image = image.convert("RGBA")
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        return {
            "size": {"w": image.width, "h": image.height},
            "alpha_bbox": None,
            "alpha_pixels": 0,
            "opaque_pixels": 0,
            "magenta_pixels_remaining": 0,
            "magenta_halo_pixels": 0,
            "crop_padding": {"left": 0, "top": 0, "right": 0, "bottom": 0},
            "cutoff_edges": ["empty_alpha"],
            "readable": False,
        }

    pixels = image.load()
    alpha_pixels = 0
    opaque_pixels = 0
    magenta_pixels = 0
    halo_pixels = 0
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            if a <= 0:
                continue
            alpha_pixels += 1
            if a >= 220:
                opaque_pixels += 1
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
        "opaque_pixels": opaque_pixels,
        "magenta_pixels_remaining": magenta_pixels,
        "magenta_halo_pixels": halo_pixels,
        "crop_padding": padding,
        "cutoff_edges": [side for side, value in padding.items() if value < MIN_CROP_PADDING],
        "readable": alpha_pixels >= 1200 and bbox_w >= 48 and bbox_h >= 40,
    }


def write_assets(alpha_sheet: Image.Image) -> dict[str, dict]:
    GENERATED_ROOT.mkdir(parents=True, exist_ok=True)
    output: dict[str, dict] = {}
    for asset_id, config in ASSETS.items():
        crop = config["crop"]
        piece = alpha_sheet.crop(tuple(crop))
        piece = trim_alpha(piece, padding=8)
        path = GENERATED_ROOT / f"{asset_id}.png"
        piece.save(path)
        output[asset_id] = {
            "path": path,
            "atlas_region": {"x": crop[0], "y": crop[1], "w": crop[2] - crop[0], "h": crop[3] - crop[1]},
            "sprite_size": {"w": piece.width, "h": piece.height},
        }
    return output


def write_atlas(alpha_sheet: Image.Image) -> None:
    ATLAS_PATH.parent.mkdir(parents=True, exist_ok=True)
    alpha_sheet.save(ATLAS_PATH)


def manifest_entry(asset_id: str, output: dict[str, dict]) -> dict:
    config = ASSETS[asset_id]
    path = output[asset_id]["path"]
    qa = output[asset_id]["qa"]
    return {
        "asset_id": asset_id,
        "asset_type": config["asset_type"],
        "source_identity": config["source_identity"],
        "path": rel(path),
        "atlas": rel(ATLAS_PATH),
        "atlas_region": output[asset_id]["atlas_region"],
        "sprite_size": output[asset_id]["sprite_size"],
        "pivot": config["pivot"],
        "grounding": {
            "pivot_y": config["pivot"]["y"],
            "expected_contact": "bottom-shadow pixels sit inside transparent sprite bounds; draw destination bottom is the world grounding line",
        },
        "recommended_game_scale": config["recommended_game_scale"],
        "source_type": "ai_assisted_image_generation_with_local_chroma_extraction",
        "created_by": "Codex built-in image generation tool plus local transparent extraction",
        "generation_prompt": rel(PROMPT_PATH),
        "source_image": rel(SOURCE_PATH),
        "extraction_script": rel(SCRIPT_PATH),
        "input_sources": [
            {
                "type": "ai_generated_source_image",
                "path": rel(SOURCE_PATH),
                "source_pixels_used": True,
                "commercial_status": "green_origin_candidate_pending_license_review",
            },
            {
                "type": "project_prompt",
                "path": rel(PROMPT_PATH),
                "source_pixels_used": False,
                "commercial_status": "green_origin_candidate",
            },
            {
                "type": "project_style_rules",
                "path": rel(ART_BIBLE_PATH),
                "source_pixels_used": False,
                "commercial_status": "documentation_only",
            },
            {
                "type": "locked_atelier_standard",
                "path": rel(G418D_STANDARD_REPORT_PATH),
                "source_pixels_used": False,
                "commercial_status": "documentation_only",
            },
        ],
        "license": "AI-assisted original generated sprite candidate for Wayfarer; no web image, marketplace pack, ripped sheet, or copied game sprite was provided as source input. Final-commercial promotion still requires project policy approval for AI-generated artwork.",
        "ownership": "project-owned-candidate",
        "provenance_status": "ai_assisted_green_origin_candidate_pending_license_review",
        "origin_classification": "green_origin_candidate_pending_license_review",
        "commercial_use_status": "green_origin_candidate_pending_license_review",
        "review_eligible": True,
        "normal_review_eligible": True,
        "lab_only": False,
        "final_commercial_candidate": False,
        "final_commercial_eligible": False,
        "source_pixels_from_yellow_uncertain_assets": False,
        "source_pixels_from_third_party_material": False,
        "web_scraped_source_pixels": False,
        "ai_generated": True,
        "human_selected": True,
        "chroma_key_removed": True,
        "extraction_qa": qa,
        "sha256": sha256(path),
        "notes": config["notes"],
    }


def write_manifest(output: dict[str, dict]) -> dict:
    manifest = {
        "schema_id": "wayfarer.newport_atelier.dock_clutter_manifest.v1",
        "phase": "G-4.19A",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "visual_standard": "First city rollout pack built from the accepted G-4.18D 10/10 Newport atelier cargo prop standard.",
        "source_policy": "AI-assisted original art is allowed here only with recorded prompt/source image/extraction script and no yellow building pixels, third-party sprites, marketplace packs, or web-scraped images as source inputs.",
        "atlas": rel(ATLAS_PATH),
        "source_image": rel(SOURCE_PATH),
        "generation_prompt": rel(PROMPT_PATH),
        "generated_asset_root": rel(GENERATED_ROOT),
        "contact_sheet": rel(CONTACT_PATH),
        "provenance_report": rel(REPORT_PATH),
        "validation_report": rel(QA_REPORT_PATH),
        "pipeline_status": "ai_assisted_green_origin_candidate_pending_final_license_policy_approval",
        "base_pipeline_standard": "G-4.18D Newport atelier cargo pipeline lock",
        "future_pack_pattern": "10/10 source sheet -> saved prompt/source -> extraction script -> transparent sprites -> atlas/contact sheet -> manifest/provenance report -> Godot placement -> validation",
        "rollout_pack_role": "first_city_rollout_pack_after_g418d_atelier_standard",
        "placement_policy": "Controlled wharf proof placement only; no over-scatter; prioritize believable clusters around docks, cargo, market/harbor edges, and service paths while preserving navigation.",
        "deprecated_visual_targets": [
            "G-4.18B weak deterministic/procedural cargo proof",
            "G-4.18D.2 deferred rope/crate/barrel capability cluster",
        ],
        "assets": [manifest_entry(asset_id, output) for asset_id in ASSETS],
    }
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def collect_qa(output: dict[str, dict]) -> dict:
    qa: dict[str, dict] = {}
    for asset_id, details in output.items():
        image = Image.open(details["path"]).convert("RGBA")
        metrics = alpha_metrics(image)
        metrics["source_identity"] = ASSETS[asset_id]["source_identity"]
        metrics["manifest_identity_match"] = Path(details["path"]).stem == asset_id
        metrics["status"] = "PASS"
        failures: list[str] = []
        if metrics["magenta_pixels_remaining"] != 0:
            failures.append("magenta_background_remaining")
        if metrics["magenta_halo_pixels"] != 0:
            failures.append("magenta_halo_pixels")
        if metrics["cutoff_edges"]:
            failures.append("insufficient_crop_padding")
        if not metrics["readable"]:
            failures.append("sprite_not_visually_readable")
        if not metrics["manifest_identity_match"]:
            failures.append("manifest_identity_mismatch")
        if failures:
            metrics["status"] = "FAIL"
            metrics["failures"] = failures
        qa[asset_id] = metrics
    return qa


def write_qa_report(qa: dict[str, dict]) -> None:
    QA_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    status = "PASS" if all(details.get("status") == "PASS" for details in qa.values()) else "FAIL"
    QA_REPORT_PATH.write_text(
        json.dumps(
            {
                "schema_id": "wayfarer.newport_atelier.extraction_qa.v1",
                "phase": "G-4.19A",
                "pack": "newport_dock_clutter",
                "status": status,
                "checks": [
                    "source image and prompt exist",
                    "transparent sprites have no magenta background",
                    "transparent sprites have no magenta halo on alpha edges",
                    "sprites retain clean transparent crop padding",
                    "sprites are not cut off at object edges",
                    "sprites remain visually readable by alpha footprint",
                    "source sheet object identity maps to manifest asset ids",
                ],
                "assets": qa,
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def validate_pipeline(manifest: dict, qa: dict[str, dict]) -> list[str]:
    failures: list[str] = []
    for path in [SOURCE_PATH, PROMPT_PATH, ATLAS_PATH, CONTACT_PATH, MANIFEST_PATH, REPORT_PATH, QA_REPORT_PATH]:
        if not path.exists():
            failures.append(f"missing artifact: {rel(path)}")
    expected_ids = set(ASSETS.keys())
    manifest_ids = {asset.get("asset_id") for asset in manifest.get("assets", [])}
    if manifest_ids != expected_ids:
        failures.append(f"manifest asset ids mismatch: {sorted(manifest_ids)} != {sorted(expected_ids)}")
    if set(qa.keys()) != expected_ids:
        failures.append(f"qa asset ids mismatch: {sorted(qa.keys())} != {sorted(expected_ids)}")
    for asset_id, details in qa.items():
        if details.get("status") != "PASS":
            failures.append(f"{asset_id} extraction QA failed: {details.get('failures', [])}")
    for asset in manifest.get("assets", []):
        if asset.get("provenance_status") != "ai_assisted_green_origin_candidate_pending_license_review":
            failures.append(f"{asset.get('asset_id', 'unknown')} provenance status is not pending AI-assisted green-origin")
        if asset.get("commercial_use_status") != "green_origin_candidate_pending_license_review":
            failures.append(f"{asset.get('asset_id', 'unknown')} commercial status is not pending license review")
        if asset.get("final_commercial_candidate") is not False or asset.get("final_commercial_eligible") is not False:
            failures.append(f"{asset.get('asset_id', 'unknown')} is incorrectly final-commercial promoted")
    return failures


def label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fill: str = "#efe0ad") -> None:
    draw.text(xy, text, fill=fill, font=ImageFont.load_default())


def write_contact_sheet(output: dict[str, dict]) -> None:
    CONTACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    sheet = Image.new("RGB", (1600, 1120), "#20261e")
    draw = ImageDraw.Draw(sheet)
    label(draw, (24, 18), "G-4.19A Newport Dock Clutter Atelier Pack")
    label(draw, (24, 40), "First city rollout pack from G-4.18D: AI-assisted green-origin candidates, extracted sprites, controlled wharf placement.")
    positions = {
        "atelier_dock_bollards_01": (40, 92, 330, 300),
        "atelier_mooring_hardware_01": (420, 98, 330, 300),
        "atelier_fishing_net_bundle_01": (800, 98, 330, 300),
        "atelier_sacks_fish_baskets_01": (1180, 98, 330, 300),
        "atelier_anchor_rope_01": (40, 580, 330, 300),
        "atelier_dock_repair_planks_01": (420, 580, 330, 300),
        "atelier_dock_lantern_01": (800, 580, 330, 300),
        "atelier_shoreline_debris_01": (1180, 580, 330, 300),
    }
    for asset_id, (x, y, max_w, max_h) in positions.items():
        piece = Image.open(output[asset_id]["path"]).convert("RGBA")
        scale = min(max_w / piece.width, max_h / piece.height, 1.0)
        thumb = piece.resize((max(1, int(piece.width * scale)), max(1, int(piece.height * scale))), Image.Resampling.LANCZOS)
        card = Image.new("RGBA", (max_w, max_h), (39, 46, 36, 255))
        card.alpha_composite(thumb, ((max_w - thumb.width) // 2, (max_h - thumb.height) // 2))
        sheet.paste(card.convert("RGB"), (x, y))
        draw.rectangle((x, y, x + max_w, y + max_h), outline="#5e6a54", width=1)
        label(draw, (x + 10, y + max_h + 10), asset_id, "#efe0ad")
        label(draw, (x + 10, y + max_h + 28), ASSETS[asset_id]["asset_type"], "#c8d2ac")
    label(draw, (24, 1078), "Placement uses a controlled subset around dock edges, cargo frontage, harbor market edges, and service paths; no over-scatter.", "#c8d2ac")
    sheet.save(CONTACT_PATH)


def write_report(manifest: dict) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    asset_lines = "\n".join(
        f"- `{asset['asset_id']}`: `{asset['asset_type']}`, `{asset['commercial_use_status']}`"
        for asset in manifest["assets"]
    )
    REPORT_PATH.write_text(
        f"""# G-4.19A Newport Dock Clutter Atelier Pack

## Result

G-4.19A is the first Newport city rollout pack built from the G-4.18D atelier
cargo standard. It keeps the locked production pattern intact and extends the
wharf proof with authored-looking dock clutter instead of procedural filler.

## Source Chain

- Source image: `{rel(SOURCE_PATH)}`
- Prompt record: `{rel(PROMPT_PATH)}`
- Extraction script: `{rel(SCRIPT_PATH)}`
- Output atlas: `{rel(ATLAS_PATH)}`
- Manifest: `{rel(MANIFEST_PATH)}`
- Contact sheet: `{rel(CONTACT_PATH)}`
- Extraction QA report: `{rel(QA_REPORT_PATH)}`
- Base standard: `{rel(G418D_STANDARD_REPORT_PATH)}`

No yellow Newport building pixels, third-party sprite sheets, marketplace
assets, web images, or ripped game art were supplied as source inputs.

## Classification

These assets are `ai_assisted_green_origin_candidate_pending_license_review`.
They are review-eligible as original AI-assisted candidates, but final
commercial promotion remains blocked until the project approves its final
license policy for generated artwork.

## Generated Assets

{asset_lines}

## Placement QA

The in-game proof uses a controlled subset only. The placements are clustered
around docks, cargo frontage, market/harbor edges, and service paths. The pack
does not attempt city-wide scatter in this pass.

Validation criteria for placement:

1. Scale remains consistent with G-4.18D cargo sprites.
2. Destination bottoms match placement `ground_y`.
3. Pivots stay near the lower center of each prop.
4. Props are drawn from transparent atlas regions with no magenta halo.
5. Props do not block navigation or hide critical walkable path reads.
6. Low shoreline debris stays visually subordinate to cargo and buildings.

## Reusable Production Pattern

10/10 source sheet -> saved prompt/source -> extraction script -> transparent
sprites -> atlas/contact sheet -> manifest/provenance report -> Godot placement
-> validation.
""",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validate-only", action="store_true", help="validate existing generated outputs without rewriting sprites")
    args = parser.parse_args()

    if args.validate_only:
        if not MANIFEST_PATH.exists():
            raise FileNotFoundError(MANIFEST_PATH)
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        output = {asset_id: {"path": GENERATED_ROOT / f"{asset_id}.png"} for asset_id in ASSETS}
        qa = collect_qa(output)
        write_qa_report(qa)
        failures = validate_pipeline(manifest, qa)
        if failures:
            for failure in failures:
                print(f"FAIL: {failure}")
            raise SystemExit(1)
        print("PASS: existing atelier dock clutter extraction outputs validated")
        return

    source = Image.open(SOURCE_PATH).convert("RGBA")
    alpha_sheet = key_to_alpha(source)
    write_atlas(alpha_sheet)
    output = write_assets(alpha_sheet)
    qa = collect_qa(output)
    for asset_id, details in output.items():
        details["qa"] = qa[asset_id]
    manifest = write_manifest(output)
    write_qa_report(qa)
    write_contact_sheet(output)
    write_report(manifest)
    failures = validate_pipeline(manifest, qa)
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        raise SystemExit(1)
    print(f"Wrote atelier dock clutter atlas: {rel(ATLAS_PATH)}")
    print(f"Wrote {len(output)} atelier dock clutter sprites to {rel(GENERATED_ROOT)}")


if __name__ == "__main__":
    main()
