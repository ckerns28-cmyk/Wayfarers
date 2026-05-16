#!/usr/bin/env python3
"""Generate G-4.18B green-origin Newport proof assets.

The generator is deliberately small and deterministic. It reads only
hand-authored local JSON parameters plus this script, then draws original
Pillow bitmaps. It does not open or sample the yellow Newport building sprites,
the older G-4.17/G-4.18 hero atlas, marketplace assets, web images, or any
third-party art.
"""

from __future__ import annotations

import hashlib
import json
import random
from collections import OrderedDict
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[3]
PIPELINE_ROOT = PROJECT_ROOT / "art_pipeline" / "newport_green_origin"
STYLE_TOKENS_PATH = PIPELINE_ROOT / "source_authored" / "newport_green_origin_style_tokens.json"
GENERATED_ROOT = PIPELINE_ROOT / "generated"
ATLAS_PATH = PIPELINE_ROOT / "atlases" / "newport_green_origin_dock_factory_v1.png"
CONTACT_SHEET_PATH = PIPELINE_ROOT / "contact_sheets" / "green_origin_asset_contact_sheet.png"
PALETTE_SHEET_PATH = PIPELINE_ROOT / "contact_sheets" / "green_origin_palette_shadow_sheet.png"
COMPARISON_PATH = PIPELINE_ROOT / "contact_sheets" / "green_origin_dock_before_after_comparison.png"
MANIFEST_PATH = PIPELINE_ROOT / "manifests" / "green_origin_asset_manifest.json"
REPORT_PATH = PIPELINE_ROOT / "reports" / "G418B_GREEN_ORIGIN_ASSET_FACTORY.md"
ART_BIBLE_PATH = PROJECT_ROOT / "docs" / "NEWPORT_ART_BIBLE.md"

REGIONS: "OrderedDict[str, tuple[int, int, int, int]]" = OrderedDict(
    [
        ("green_dock_plank_strip", (0, 0, 320, 72)),
        ("green_dock_plank_patch", (0, 84, 180, 72)),
        ("green_dock_edge_shadow", (0, 168, 320, 42)),
        ("green_pier_post_pair", (336, 0, 112, 92)),
        ("green_rope_coil_small", (336, 104, 80, 56)),
        ("green_plank_contact_shadow", (336, 172, 144, 36)),
    ]
)

ASSET_TYPES = {
    "green_dock_plank_strip": "dock_plank_tile",
    "green_dock_plank_patch": "dock_plank_tile",
    "green_dock_edge_shadow": "contact_shadow_tile",
    "green_pier_post_pair": "dock_post_prop",
    "green_rope_coil_small": "rope_prop",
    "green_plank_contact_shadow": "contact_shadow_tile",
}


def rel(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def rgba(hex_color: str, alpha: int = 255) -> tuple[int, int, int, int]:
    value = hex_color.strip("#")
    return (int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16), alpha)


def seeded(asset_id: str, salt: int = 0) -> random.Random:
    seed = 418200 + salt
    for index, char in enumerate(asset_id):
        seed += (index + 1) * ord(char)
    return random.Random(seed)


def jitter(hex_color: str, rng: random.Random, amount: int = 8, alpha: int = 255) -> tuple[int, int, int, int]:
    r, g, b, _ = rgba(hex_color)
    return (
        max(0, min(255, r + rng.randint(-amount, amount))),
        max(0, min(255, g + rng.randint(-amount, amount))),
        max(0, min(255, b + rng.randint(-amount, amount))),
        alpha,
    )


def load_tokens() -> dict:
    return json.loads(STYLE_TOKENS_PATH.read_text(encoding="utf-8"))


def draw_soft_shadow(size: tuple[int, int], inset: int, alpha: int) -> Image.Image:
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((inset, size[1] // 3, size[0] - inset, size[1] - 2), fill=(8, 9, 7, alpha))
    return image.filter(ImageFilter.GaussianBlur(radius=5))


def draw_planks(asset_id: str, size: tuple[int, int], tokens: dict, patch: bool = False) -> Image.Image:
    rng = seeded(asset_id)
    palette = tokens["palettes"]
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    image.alpha_composite(draw_soft_shadow(size, 10, 80), (0, 6))

    board_h = 11 if not patch else 13
    y = 9
    row = 0
    while y < size[1] - 8:
        x = 4 - (row % 2) * 22
        while x < size[0] - 2:
            length = rng.randint(52, 92) if not patch else rng.randint(38, 70)
            x0 = x + rng.randint(-2, 2)
            y0 = y + rng.randint(-1, 1)
            x1 = min(size[0] - 4, x0 + length)
            y1 = min(size[1] - 7, y0 + board_h + rng.randint(-1, 1))
            fill = jitter(rng.choice(palette["dock_wood"]), rng, 7, 242)
            outline = jitter(rng.choice(palette["dock_shadow"]), rng, 4, 210)
            draw.rounded_rectangle((x0, y0, x1, y1), radius=2, fill=fill, outline=outline, width=1)
            draw.line((x0 + 3, y0 + 2, x1 - 4, y0 + 1), fill=jitter(rng.choice(palette["dock_highlight"]), rng, 5, 92), width=1)
            draw.line((x0 + 4, y1 - 2, x1 - 5, y1 - 2), fill=jitter(rng.choice(palette["dock_shadow"]), rng, 4, 105), width=1)
            for _ in range(3):
                px = rng.randint(max(0, int(x0 + 6)), max(int(x0 + 7), int(x1 - 6)))
                py = rng.randint(max(0, int(y0 + 3)), max(int(y0 + 4), int(y1 - 3)))
                draw.point((px, py), fill=jitter("#1c1812", rng, 3, 170))
            x += length + rng.randint(2, 6)
        y += board_h + 2
        row += 1

    for x in range(8, size[0], 37):
        draw.line((x, 12, x + rng.choice([-2, -1, 0, 1]), size[1] - 12), fill=jitter(palette["dock_shadow"][1], rng, 4, 42), width=1)
    return image


def draw_edge_shadow(asset_id: str, size: tuple[int, int], tokens: dict) -> Image.Image:
    rng = seeded(asset_id)
    palette = tokens["palettes"]
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    for y in range(size[1]):
        alpha = max(0, 110 - y * 3)
        color = jitter(rng.choice(palette["harbor_contact"]), rng, 4, alpha)
        draw.line((0, y, size[0], y + rng.choice([-1, 0, 1])), fill=color, width=1)
    for x in range(0, size[0], 19):
        y = rng.randint(6, size[1] - 8)
        draw.ellipse((x, y, x + rng.randint(12, 28), y + rng.randint(2, 5)), fill=jitter(palette["oxidized_green"][rng.randrange(3)], rng, 7, 54))
    return image.filter(ImageFilter.GaussianBlur(radius=0.35))


def draw_post_pair(asset_id: str, size: tuple[int, int], tokens: dict) -> Image.Image:
    rng = seeded(asset_id)
    palette = tokens["palettes"]
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    image.alpha_composite(draw_soft_shadow(size, 6, 90), (0, 15))
    for cx in (32, 76):
        draw.ellipse((cx - 13, 46, cx + 15, 82), fill=jitter("#12130f", rng, 5, 86))
        fill = jitter(rng.choice(palette["dock_wood"]), rng, 8, 245)
        outline = jitter("#15120d", rng, 4, 230)
        draw.rounded_rectangle((cx - 9, 11, cx + 9, 67), radius=5, fill=fill, outline=outline, width=1)
        draw.ellipse((cx - 9, 5, cx + 9, 19), fill=jitter(rng.choice(palette["dock_highlight"]), rng, 8, 230), outline=outline, width=1)
        draw.line((cx - 5, 18, cx - 5, 62), fill=jitter(rng.choice(palette["dock_highlight"]), rng, 5, 80), width=1)
        draw.line((cx + 6, 20, cx + 5, 64), fill=jitter(rng.choice(palette["dock_shadow"]), rng, 4, 120), width=2)
    return image


def draw_rope(asset_id: str, size: tuple[int, int], tokens: dict) -> Image.Image:
    rng = seeded(asset_id)
    palette = tokens["palettes"]
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    image.alpha_composite(draw_soft_shadow(size, 10, 72), (0, 8))
    bbox = (18, 12, 58, 42)
    for inset in (0, 5, 10):
        color = jitter(rng.choice(palette["rope"]), rng, 7, 230)
        outline = jitter("#18140e", rng, 3, 180)
        rect = (bbox[0] + inset, bbox[1] + inset // 2, bbox[2] - inset, bbox[3] - inset // 2)
        draw.ellipse(rect, outline=outline, width=3)
        draw.arc(rect, 18, 344, fill=color, width=3)
    draw.line((54, 27, 72, 25), fill=jitter(rng.choice(palette["rope"]), rng, 8, 224), width=3)
    for x in range(24, 58, 7):
        draw.line((x, 15, x + 5, 40), fill=jitter("#d0bd8a", rng, 6, 62), width=1)
    return image


def make_piece(asset_id: str, size: tuple[int, int], tokens: dict) -> Image.Image:
    if asset_id == "green_dock_plank_strip":
        return draw_planks(asset_id, size, tokens)
    if asset_id == "green_dock_plank_patch":
        return draw_planks(asset_id, size, tokens, patch=True)
    if asset_id == "green_dock_edge_shadow":
        return draw_edge_shadow(asset_id, size, tokens)
    if asset_id == "green_pier_post_pair":
        return draw_post_pair(asset_id, size, tokens)
    if asset_id == "green_rope_coil_small":
        return draw_rope(asset_id, size, tokens)
    if asset_id == "green_plank_contact_shadow":
        return draw_soft_shadow(size, 8, 96)
    raise KeyError(asset_id)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_assets(tokens: dict) -> dict[str, Path]:
    GENERATED_ROOT.mkdir(parents=True, exist_ok=True)
    ATLAS_PATH.parent.mkdir(parents=True, exist_ok=True)
    atlas = Image.new("RGBA", (512, 256), (0, 0, 0, 0))
    paths: dict[str, Path] = {}
    for asset_id, region in REGIONS.items():
        x, y, width, height = region
        piece = make_piece(asset_id, (width, height), tokens)
        piece_path = GENERATED_ROOT / f"{asset_id}.png"
        piece.save(piece_path)
        paths[asset_id] = piece_path
        atlas.alpha_composite(piece, (x, y))
    atlas.save(ATLAS_PATH)
    return paths


def manifest_entry(asset_id: str, region: tuple[int, int, int, int], paths: dict[str, Path]) -> dict:
    return {
        "asset_id": asset_id,
        "asset_type": ASSET_TYPES[asset_id],
        "path": rel(paths[asset_id]),
        "atlas": rel(ATLAS_PATH),
        "atlas_region": {"x": region[0], "y": region[1], "w": region[2], "h": region[3]},
        "source_type": "deterministic_python_pillow",
        "created_by": "Wayfarer project local deterministic generator",
        "generation_script": rel(SCRIPT_PATH),
        "input_sources": [
            {
                "type": "project_script",
                "path": rel(SCRIPT_PATH),
                "source_pixels_used": False,
                "commercial_status": "green_origin_candidate"
            },
            {
                "type": "project_authored_parameters",
                "path": rel(STYLE_TOKENS_PATH),
                "source_pixels_used": False,
                "commercial_status": "green_origin_candidate"
            },
            {
                "type": "project_style_rules",
                "path": rel(ART_BIBLE_PATH),
                "source_pixels_used": False,
                "commercial_status": "documentation_only"
            }
        ],
        "license": "Wayfarer project-owned deterministic generated bitmap; no third-party, marketplace, web-scraped, ripped, or yellow-source pixels; commercial project use allowed.",
        "ownership": "project-owned",
        "commercial_use_status": "green_origin_candidate",
        "provenance_status": "green_origin_candidate",
        "origin_classification": "green_origin_candidate",
        "visual_quality_status": "visual_failed_g418b_proof",
        "review_eligible": False,
        "normal_review_eligible": False,
        "lab_only": True,
        "final_commercial_candidate": False,
        "final_commercial_eligible": False,
        "lab_access_mode": "F6 or --show-green-origin-lab",
        "source_pixels_from_yellow_uncertain_assets": False,
        "source_pixels_from_third_party_material": False,
        "web_scraped_source_pixels": False,
        "ai_generated": False,
        "deterministic_generated": True,
        "sha256": sha256(paths[asset_id]),
        "visual_review_notes": "G-4.18C quarantine: source-safe proof asset reads too small, noisy, sticker-like, or off-scale in the player-facing scene. Preserve for provenance/lab inspection only.",
        "notes": "Original Pillow mark-making from authored palettes and geometry rules. Yellow Newport building sprites were not opened, sampled, cropped, traced, or copied. G-4.18C quarantine: preserved as provenance proof, hidden from normal review until redesigned."
    }


def write_manifest(paths: dict[str, Path]) -> dict:
    assets = [manifest_entry(asset_id, region, paths) for asset_id, region in REGIONS.items()]
    manifest = {
        "schema_id": "wayfarer.newport_green_origin.asset_manifest.v1",
        "phase": "G-4.18B",
        "generated_at": "2026-05-15T00:00:00Z",
        "atlas": rel(ATLAS_PATH),
        "generated_asset_root": rel(GENERATED_ROOT),
        "contact_sheets": [rel(CONTACT_SHEET_PATH), rel(PALETTE_SHEET_PATH), rel(COMPARISON_PATH)],
        "origin_taxonomy": [
            "temporary_review_yellow",
            "green_origin_candidate",
            "final_commercial_green",
            "red_unsafe"
        ],
        "source_policy": "Green-origin assets may use only project scripts, authored parameters, and documented project-owned sources. Yellow/uncertain sprites are visual reference only and cannot be source pixels. G-4.18C adds visual gating: provenance green + visual failed = lab-only, not normal review or final-commercial candidate.",
        "quarantine_phase": "G-4.18C",
        "visual_quality_gate": "G-4.18C correction: green-origin provenance is necessary but not sufficient. This proof family is legally useful but visually failed and is lab-only.",
        "lab_access_mode": "F6 or --show-green-origin-lab",
        "assets": assets
    }
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fill: str = "#efe0ad") -> None:
    draw.text(xy, text, fill=fill, font=ImageFont.load_default())


def write_contact_sheets(paths: dict[str, Path], tokens: dict) -> None:
    CONTACT_SHEET_PATH.parent.mkdir(parents=True, exist_ok=True)
    sheet = Image.new("RGB", (1120, 720), "#20261e")
    draw = ImageDraw.Draw(sheet)
    label(draw, (24, 18), "G-4.18B green-origin dock asset family")
    label(draw, (24, 38), "All pieces are deterministic Pillow output from project-authored parameters; no yellow sprite pixels.")
    x, y = 24, 76
    for index, (asset_id, path) in enumerate(paths.items()):
        piece = Image.open(path).convert("RGBA")
        preview = Image.new("RGBA", (320, 118), (42, 48, 38, 255))
        scale = min(300 / piece.width, 84 / piece.height, 1.4)
        thumb = piece.resize((max(1, int(piece.width * scale)), max(1, int(piece.height * scale))), Image.Resampling.NEAREST)
        preview.alpha_composite(thumb, ((320 - thumb.width) // 2, 14 + (84 - thumb.height) // 2))
        sheet.paste(preview.convert("RGB"), (x, y))
        draw.rectangle((x, y, x + 320, y + 118), outline="#5e6a54", width=1)
        label(draw, (x + 10, y + 96), asset_id)
        x += 350
        if (index + 1) % 3 == 0:
            x = 24
            y += 164
    sheet.save(CONTACT_SHEET_PATH)

    palette_sheet = Image.new("RGB", (900, 520), "#20261e")
    pdraw = ImageDraw.Draw(palette_sheet)
    label(pdraw, (24, 18), "Green-origin authored palette and contact-shadow proof")
    row_y = 62
    for name, colors in tokens["palettes"].items():
        label(pdraw, (24, row_y + 8), name, "#d8cfad")
        x0 = 190
        for color in colors:
            pdraw.rectangle((x0, row_y, x0 + 42, row_y + 32), fill=color, outline="#10120f")
            label(pdraw, (x0, row_y + 38), color, "#bfc8a8")
            x0 += 74
        row_y += 64
    shadow = Image.open(paths["green_plank_contact_shadow"]).convert("RGBA").resize((288, 72), Image.Resampling.BILINEAR)
    palette_sheet.paste(Image.new("RGB", (320, 96), "#30372b"), (520, 382))
    palette_sheet.paste(shadow.convert("RGB"), (536, 394), shadow)
    label(pdraw, (520, 482), "generated contact shadow tile")
    palette_sheet.save(PALETTE_SHEET_PATH)

    before_after = Image.new("RGB", (1040, 430), "#20261e")
    bdraw = ImageDraw.Draw(before_after)
    label(bdraw, (24, 18), "Dock proof comparison: procedural sketch surface to green-origin generated strip")
    bdraw.rectangle((48, 86, 478, 318), fill="#4d3d2b", outline="#10120f")
    for yy in range(102, 304, 28):
        bdraw.line((60, yy, 466, yy + 3), fill="#7c6240", width=3)
    for xx in range(72, 458, 54):
        bdraw.line((xx, 96, xx + 6, 308), fill="#2f261c", width=1)
    label(bdraw, (76, 334), "before: procedural MapLayer-style plank marks", "#d8cfad")
    after = Image.open(paths["green_dock_plank_strip"]).convert("RGBA").resize((430, 116), Image.Resampling.NEAREST)
    before_after.paste(Image.new("RGB", (430, 232), "#30372b"), (560, 86))
    before_after.paste(after.convert("RGB"), (560, 146), after)
    label(bdraw, (588, 334), "after: green-origin generated atlas tile", "#d8cfad")
    label(bdraw, (48, 374), "No yellow building pixels are used in either side; the right side is the shipped G-4.18B proof asset.", "#bfc8a8")
    before_after.save(COMPARISON_PATH)


def write_report(manifest: dict) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    asset_lines = "\n".join(
        f"- `{asset['asset_id']}`: `{asset['asset_type']}`, `{asset['commercial_use_status']}`, visual `{asset['visual_quality_status']}`, lab-only `{str(asset['lab_only']).lower()}`"
        for asset in manifest["assets"]
    )
    REPORT_PATH.write_text(
        f"""# G-4.18B Green-Origin Newport Art Factory

## Result

G-4.18B creates the first green-origin Newport art factory under
`art_pipeline/newport_green_origin/`. The proof family is a small dock-plank,
dock-edge, post, rope, and contact-shadow set generated by deterministic
Python/Pillow drawing from hand-authored project parameters.

## Source Chain

- Generator: `{rel(SCRIPT_PATH)}`
- Authored tokens: `{rel(STYLE_TOKENS_PATH)}`
- Output atlas: `{rel(ATLAS_PATH)}`
- Manifest: `{rel(MANIFEST_PATH)}`
- Contact sheet: `{rel(CONTACT_SHEET_PATH)}`
- Palette/contact-shadow sheet: `{rel(PALETTE_SHEET_PATH)}`
- Before/after comparison: `{rel(COMPARISON_PATH)}`

No yellow Newport building sprite, G-4.17/G-4.18 hero atlas, marketplace asset,
web image, ripped sheet, or mystery PNG is opened, sampled, cropped, copied, or
used as source pixels.

## Classification

The current yellow Newport building sprites remain temporary review art only.
The G-4.17/G-4.18 crop-derived hero atlas remains temporary_review_yellow. This
G-4.18B dock proof family remains classified as `green_origin_candidate` for
provenance, but G-4.18C marks it `visual_failed_g418b_proof`,
`normal_review_eligible=false`, `lab_only=true`, and
`final_commercial_candidate=false`. Final art promotion can happen only after
both provenance approval and visual direction approval.

## Generated Assets

{asset_lines}

## Godot Proof Area

`MapLayer.gd` loads the green-origin atlas but draws the G-4.18B proof only in
Green-Origin Lab mode (`F6` or `--show-green-origin-lab`). Yellow buildings
remain in the prototype as temporary review art; they are not source pixels for
the green-origin dock assets.

## Validation Expectations

- `validate_green_origin_assets.py` must pass.
- `validate_newport_asset_provenance.py` must keep yellow assets out of final
  commercial classification.
- The Godot vertical slice validator must see the G-4.18B green-origin atlas API.
- Browser screenshots should include the full harbor, a green-origin dock
  close-up, the contact sheet, and a provenance/debug proof.
""",
        encoding="utf-8",
    )


def main() -> None:
    tokens = load_tokens()
    paths = write_assets(tokens)
    manifest = write_manifest(paths)
    write_contact_sheets(paths, tokens)
    write_report(manifest)
    print(f"Wrote {len(paths)} green-origin assets to {rel(GENERATED_ROOT)}")
    print(f"Wrote atlas: {rel(ATLAS_PATH)}")
    print(f"Wrote manifest: {rel(MANIFEST_PATH)}")


if __name__ == "__main__":
    main()
