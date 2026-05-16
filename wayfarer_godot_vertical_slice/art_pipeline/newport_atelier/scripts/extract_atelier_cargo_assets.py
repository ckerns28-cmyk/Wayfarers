#!/usr/bin/env python3
"""Extract G-4.18D AI-assisted Newport atelier cargo sprites.

This script keeps the accepted generated sheet as the source of record, removes
the flat chroma-key background, crops the four reviewed assets, and writes a
manifest/contact sheet so the style can be repeated without losing provenance.
"""

from __future__ import annotations

import hashlib
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[3]
PIPELINE_ROOT = PROJECT_ROOT / "art_pipeline" / "newport_atelier"
SOURCE_PATH = PIPELINE_ROOT / "source_generated" / "g418d_atelier_cargo_sheet_imagegen.png"
PROMPT_PATH = PIPELINE_ROOT / "source_generated" / "g418d_atelier_cargo_prompt.txt"
GENERATED_ROOT = PIPELINE_ROOT / "generated"
ATLAS_PATH = PIPELINE_ROOT / "atlases" / "newport_atelier_cargo_v1.png"
CONTACT_PATH = PIPELINE_ROOT / "contact_sheets" / "newport_atelier_cargo_contact_sheet.png"
MANIFEST_PATH = PIPELINE_ROOT / "manifests" / "newport_atelier_cargo_manifest.json"
REPORT_PATH = PIPELINE_ROOT / "reports" / "G418D_ATELIER_CARGO_STANDARD.md"
QA_REPORT_PATH = PIPELINE_ROOT / "reports" / "newport_atelier_cargo_extraction_qa.json"
ART_BIBLE_PATH = PROJECT_ROOT / "docs" / "NEWPORT_ART_BIBLE.md"

MIN_CROP_PADDING = 6

ASSETS = {
    "atelier_newport_crate_01": {
        "asset_type": "crate_prop",
        "crop": [80, 36, 655, 522],
        "source_identity": "upper_left_wooden_shipping_crate",
        "pivot": {"x": 0.5, "y": 0.94},
        "recommended_game_scale": 0.20,
        "notes": "Hero-quality salt-worn 1700s Newport shipping crate: planks, brace work, iron plates, nail heads, and contact shadow.",
    },
    "atelier_newport_barrel_01": {
        "asset_type": "barrel_prop",
        "crop": [900, 38, 1328, 526],
        "source_identity": "upper_right_coopered_barrel",
        "pivot": {"x": 0.5, "y": 0.94},
        "recommended_game_scale": 0.18,
        "notes": "Hero-quality coopered barrel with iron hoops, stave curvature, rim detail, and weathered highlights.",
    },
    "atelier_newport_rope_coil_01": {
        "asset_type": "rope_prop",
        "crop": [76, 574, 686, 948],
        "source_identity": "lower_left_rope_coil",
        "pivot": {"x": 0.5, "y": 0.90},
        "recommended_game_scale": 0.18,
        "notes": "Hero-quality rope coil with braided fiber structure, inner depth, frayed tail, and grounding shadow.",
    },
    "atelier_wharf_cargo_cluster_01": {
        "asset_type": "crate_barrel_rope_prop_cluster",
        "crop": [710, 548, 1468, 1020],
        "source_identity": "lower_right_composed_cargo_cluster",
        "pivot": {"x": 0.5, "y": 0.94},
        "recommended_game_scale": 0.25,
        "notes": "Composed wharf cargo cluster showing the target sprite density for city-wide prop dressing.",
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
            if max(r, b) < 175 and r > g + 20 and b > g + 20 and abs(r - b) < 88:
                shade = max(6, min(48, g + 14, (r + b + g) // 5))
                pixels[x, y] = (shade, min(58, shade + 6), shade, a)
                continue
            magenta_dominant = r > g + 45 and b > g + 45 and abs(r - b) < 92
            saturated_key = r > 170 and b > 170 and g < 150 and abs(r - b) < 120
            # The generated sheet uses a saturated magenta key, and the contact
            # shadows are purple because they were blended over that key. Remove
            # both; neutral shadows are handled by map placement/contact art.
            if magenta_dominant or saturated_key:
                pixels[x, y] = (r, g, b, 0)
                continue
            # Despill faint magenta fringes without changing wood/rope values.
            if r > 120 and b > 120 and g < 145 and abs(r - b) < 110:
                neutral = max(g, min(r, b) - 38)
                pixels[x, y] = (min(r, neutral + 42), neutral, min(b, neutral + 42), a)
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
    cutoff_edges = [side for side, value in padding.items() if value < MIN_CROP_PADDING]
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
        "cutoff_edges": cutoff_edges,
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
        "schema_id": "wayfarer.newport_atelier.cargo_manifest.v1",
        "phase": "G-4.18D",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "visual_standard": "Accepted 10/10 cargo prop style target for city-wide Newport sprite rollout.",
        "source_policy": "AI-assisted original art is allowed here only with recorded prompt/source image/extraction script and no yellow building pixels, third-party sprites, marketplace packs, or web-scraped images as source inputs.",
        "atlas": rel(ATLAS_PATH),
        "source_image": rel(SOURCE_PATH),
        "generation_prompt": rel(PROMPT_PATH),
        "generated_asset_root": rel(GENERATED_ROOT),
        "contact_sheet": rel(CONTACT_PATH),
        "provenance_report": rel(REPORT_PATH),
        "validation_report": rel(QA_REPORT_PATH),
        "pipeline_status": "locked_pending_final_license_policy_approval",
        "deprecated_visual_targets": [
            "G-4.18B weak deterministic/procedural cargo proof",
            "G-4.18D.2 deferred rope/crate/barrel capability cluster",
        ],
        "future_pack_pattern": "10/10 source sheet -> saved prompt/source -> extraction script -> transparent sprites -> atlas/contact sheet -> manifest/provenance report -> Godot placement -> validation",
        "recommended_rollout_order": [
            "dock clutter expansion",
            "terrain edge dressing",
            "signs/lamps/posts",
            "market goods/carts",
            "shopfront props",
            "NPC/player standards",
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
                "phase": "G-4.18D",
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
    sheet = Image.new("RGB", (1500, 980), "#20261e")
    draw = ImageDraw.Draw(sheet)
    label(draw, (24, 18), "G-4.18D Newport Atelier Cargo Standard")
    label(draw, (24, 40), "Accepted 10/10 AI-assisted green-origin candidate style: dense hand-painted sprite detail, 1700s harbor materials, documented prompt/source.")
    positions = {
        "atelier_newport_crate_01": (50, 90, 520, 400),
        "atelier_newport_barrel_01": (670, 80, 330, 420),
        "atelier_newport_rope_coil_01": (52, 560, 560, 310),
        "atelier_wharf_cargo_cluster_01": (700, 540, 720, 370),
    }
    for asset_id, (x, y, max_w, max_h) in positions.items():
        piece = Image.open(output[asset_id]["path"]).convert("RGBA")
        scale = min(max_w / piece.width, max_h / piece.height, 1.0)
        thumb = piece.resize((max(1, int(piece.width * scale)), max(1, int(piece.height * scale))), Image.Resampling.LANCZOS)
        card = Image.new("RGBA", (max_w, max_h), (39, 46, 36, 255))
        card.alpha_composite(thumb, ((max_w - thumb.width) // 2, (max_h - thumb.height) // 2))
        sheet.paste(card.convert("RGB"), (x, y))
        draw.rectangle((x, y, x + max_w, y + max_h), outline="#5e6a54", width=1)
        label(draw, (x + 12, y + max_h + 10), asset_id, "#efe0ad")
        label(draw, (x + 12, y + max_h + 28), ASSETS[asset_id]["asset_type"], "#c8d2ac")
    label(draw, (24, 944), "This sheet is the prop quality baseline for the full city rollout; the prior deterministic cargo proof is no longer the art target.", "#c8d2ac")
    sheet.save(CONTACT_PATH)


def write_report(manifest: dict) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    asset_lines = "\n".join(
        f"- `{asset['asset_id']}`: `{asset['asset_type']}`, `{asset['commercial_use_status']}`"
        for asset in manifest["assets"]
    )
    REPORT_PATH.write_text(
        f"""# G-4.18D Newport Atelier Cargo Standard

## Result

This pass establishes the accepted 10/10 cargo prop quality target for the
Newport city-wide sprite rollout. The source sheet is an AI-assisted original
generation selected for art direction quality, then locally extracted into
transparent game sprites and a review atlas.

## Source Chain

- Source image: `{rel(SOURCE_PATH)}`
- Prompt record: `{rel(PROMPT_PATH)}`
- Extraction script: `{rel(SCRIPT_PATH)}`
- Output atlas: `{rel(ATLAS_PATH)}`
- Manifest: `{rel(MANIFEST_PATH)}`
- Contact sheet: `{rel(CONTACT_PATH)}`
- Extraction QA report: `{rel(QA_REPORT_PATH)}`

No yellow Newport building pixels, third-party sprite sheets, marketplace
assets, web images, or ripped game art were supplied as source inputs.

## Classification

These assets are `green_origin_candidate_pending_license_review`: they are
review-eligible and legally documented as original AI-assisted candidates, but
final-commercial promotion still requires project policy approval for generated
art. They are now the visual target for the city-wide sprite buildout.

The weak deterministic/procedural cargo cluster and the deferred G-4.18D.2
capability proof are deprecated as visual targets. They remain useful as
provenance/process evidence only.

## Generated Assets

{asset_lines}

## City-Wide Standard

Every future Newport prop, terrain object, UI-world item, character accessory,
dock detail, sign, cart, market good, and building-adjacent dressing sprite
should be judged against this density: believable material construction, crisp
3/4 RPG read, dark painterly contours, muted 1700s Newport palette, salt-worn
surface storytelling, and contact grounding.

Reusable production pattern:

1. 10/10 source sheet.
2. Saved prompt/source artifact.
3. Local extraction script.
4. Transparent sprites with clean bounds and no magenta fringe.
5. Atlas, contact sheet, manifest, provenance report, and QA report.
6. Godot placement using manifest-style IDs, scale, and pivot/grounding data.
7. Automated validation before rollout.

Recommended rollout after this lock: dock clutter expansion, terrain edge
dressing, signs/lamps/posts, market goods/carts, shopfront props, then
NPC/player standards.
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
        print("PASS: existing atelier cargo extraction outputs validated")
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
    print(f"Wrote atelier cargo atlas: {rel(ATLAS_PATH)}")
    print(f"Wrote {len(output)} atelier cargo sprites to {rel(GENERATED_ROOT)}")


if __name__ == "__main__":
    main()
