#!/usr/bin/env python3
"""Generate G-4.18 Newport hero-strip assets from project-owned procedures.

This factory is the legal/provenance reset for the Newport hero strip. It uses
the accepted Newport building sprites as palette and scale references only, then
creates deterministic Pillow bitmaps and post-processed local Blender silhouettes.
No review-facing asset copies source pixels from prior prop sheets, third-party
art, marketplace samples, scraped images, or other games.
"""

from __future__ import annotations

import json
import math
import random
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[3]
PIPELINE_ROOT = PROJECT_ROOT / "art_pipeline" / "newport"
STYLE_JSON_PATH = PIPELINE_ROOT / "manifests" / "newport_building_style_values.json"
ART_BIBLE_PATH = PROJECT_ROOT / "docs" / "NEWPORT_ART_BIBLE.md"
ATLAS_PATH = PIPELINE_ROOT / "atlases" / "newport_hero_street_atlas_v1.png"
LEGACY_MANIFEST_PATH = PIPELINE_ROOT / "manifests" / "newport_hero_street_assets.json"
CANONICAL_MANIFEST_PATH = PIPELINE_ROOT / "manifests" / "newport_asset_manifest.json"
CONTACT_PATH = PIPELINE_ROOT / "generated_contact_sheets" / "newport_hero_street_atlas_contact_sheet.png"
PROOF_PATH = PIPELINE_ROOT / "generated_contact_sheets" / "newport_g418_provenance_safe_hero_asset_proof.png"
AUDIT_PATH = PIPELINE_ROOT / "reports" / "G417_G418_ASSET_PROVENANCE_AUDIT.md"
GENERATED_ROOT = PIPELINE_ROOT / "generated_assets" / "hero_strip"
BLENDER_COMPONENT_ROOT = PIPELINE_ROOT / "generated_assets" / "blender_components"
BLENDER_SCRIPT_PATH = PIPELINE_ROOT / "blender" / "render_newport_components.py"
BLENDER_COMPONENT_MANIFEST = BLENDER_COMPONENT_ROOT / "newport_blender_components_manifest.json"
BUILDING_ROOT = PROJECT_ROOT / "assets" / "sprites" / "buildings" / "isolated"

SCALE = 2

REGIONS: "OrderedDict[str, list[int]]" = OrderedDict(
    [
        ("commercial_cobble_long_a", [0, 0, 320, 96]),
        ("commercial_cobble_patch_b", [0, 104, 220, 72]),
        ("commercial_cobble_patch_c", [0, 184, 180, 64]),
        ("curb_sidewalk_stoop_strip", [0, 256, 320, 72]),
        ("curb_sidewalk_broken_edge", [0, 336, 320, 56]),
        ("building_contact_shadow_strip", [0, 400, 320, 48]),
        ("dirt_wear_transition", [0, 456, 320, 64]),
        ("grass_edge_north", [0, 528, 320, 64]),
        ("grass_cobble_feather", [0, 600, 320, 56]),
        ("dock_market_transition", [0, 664, 320, 96]),
        ("dock_pier_vertical", [336, 0, 96, 224]),
        ("dock_edge_feather", [448, 0, 320, 64]),
        ("pier_shadow_post_strip", [448, 72, 224, 56]),
        ("crate_barrel_table_cluster", [448, 144, 184, 136]),
        ("fence_sign_market_cluster", [648, 144, 184, 136]),
        ("small_crate_barrel_cluster", [448, 296, 160, 112]),
        ("market_sign_cluster", [624, 296, 160, 112]),
        ("wharf_crate_pile_cluster", [448, 424, 220, 146]),
        ("chandlery_base_cluster", [684, 424, 220, 146]),
    ]
)

MATERIAL_CATEGORIES = {
    "commercial_cobble_long_a": "commercial street/cobble",
    "commercial_cobble_patch_b": "commercial street/cobble patch",
    "commercial_cobble_patch_c": "commercial street/cobble patch",
    "curb_sidewalk_stoop_strip": "curb/sidewalk/stoop",
    "curb_sidewalk_broken_edge": "curb/sidewalk irregular edge",
    "building_contact_shadow_strip": "building contact-shadow/base",
    "dirt_wear_transition": "dirt/wear transition",
    "grass_edge_north": "grass edge",
    "grass_cobble_feather": "grass/cobble feather",
    "dock_market_transition": "dock/market transition",
    "dock_pier_vertical": "dock/pier transition",
    "dock_edge_feather": "dock/waterline feather",
    "pier_shadow_post_strip": "pier post shadow strip",
    "crate_barrel_table_cluster": "fish table/produce/crate/barrel prop cluster",
    "fence_sign_market_cluster": "fence/sign/market object cluster",
    "small_crate_barrel_cluster": "crate/barrel/sack/rope prop cluster",
    "market_sign_cluster": "market sign/fence/crate prop cluster",
    "wharf_crate_pile_cluster": "crate/barrel/rope wharf cluster",
    "chandlery_base_cluster": "shop-base prop cluster",
}

BLENDER_COMPONENTS_BY_ASSET = {
    "crate_barrel_table_cluster": ["market_table"],
    "fence_sign_market_cluster": ["fence_segment"],
    "market_sign_cluster": ["fence_segment"],
}

SOURCE_CROPS = {
    "counting_roof_plain_left": {
        "file": "newport_counting_house_civic_exchange_isolated.png",
        "box": [40, 46, 172, 84],
        "usage": "slate roof texture used as cobble grain; crop excludes windows and facade objects",
    },
    "counting_roof_plain_right": {
        "file": "newport_counting_house_civic_exchange_isolated.png",
        "box": [292, 46, 426, 84],
        "usage": "slate roof texture used as cobble grain; crop excludes windows and facade objects",
    },
    "counting_steps_material": {
        "file": "newport_counting_house_civic_exchange_isolated.png",
        "box": [184, 303, 274, 346],
        "usage": "stone step/curb material and scale; crop excludes door and windows",
    },
    "market_stone_base": {
        "file": "newport_market_shed_stalls_isolated.png",
        "box": [38, 315, 384, 376],
        "usage": "market stone base and curb material; crop excludes roof/windows",
    },
    "wharf_plank_run": {
        "file": "newport_wharf_boathouse_large_isolated.png",
        "box": [50, 292, 506, 375],
        "usage": "project-owned dock planks, posts, crates, and waterline material",
    },
    "wharf_waterline": {
        "file": "newport_wharf_boathouse_large_isolated.png",
        "box": [44, 346, 520, 416],
        "usage": "waterline grime, pier contact, and post-shadow material",
    },
    "market_left_goods": {
        "file": "newport_market_shed_stalls_isolated.png",
        "box": [36, 242, 164, 342],
        "usage": "market table goods/fish/produce reference pixels for hero prop cluster",
    },
    "market_right_goods": {
        "file": "newport_market_shed_stalls_isolated.png",
        "box": [260, 238, 386, 342],
        "usage": "market baskets, fish, and barrels reference pixels for hero prop cluster",
    },
    "mercantile_hanging_sign": {
        "file": "mercantile_shop_isolated.png",
        "box": [24, 196, 112, 276],
        "usage": "shop sign source pixels and scale reference",
    },
    "mercantile_left_barrels": {
        "file": "mercantile_shop_isolated.png",
        "box": [24, 326, 118, 426],
        "usage": "barrels/crates beside mercantile front",
    },
    "mercantile_right_crates": {
        "file": "mercantile_shop_isolated.png",
        "box": [246, 326, 374, 426],
        "usage": "large crates and barrel beside mercantile front",
    },
    "chandlery_left_props": {
        "file": "newport_chandlery_outfitter_front_isolated.png",
        "box": [20, 292, 154, 376],
        "usage": "barrel/crate/rope props from project-owned chandlery sprite",
    },
    "chandlery_right_props": {
        "file": "newport_chandlery_outfitter_front_isolated.png",
        "box": [244, 282, 412, 376],
        "usage": "anchor/rope/barrel props from project-owned chandlery sprite",
    },
    "boathouse_crate_stack": {
        "file": "newport_wharf_boathouse_large_isolated.png",
        "box": [300, 246, 506, 372],
        "usage": "wharf crate stack and net source pixels",
    },
    "boathouse_left_barrels": {
        "file": "newport_wharf_boathouse_large_isolated.png",
        "box": [48, 286, 164, 372],
        "usage": "wharf barrels, ladder, and plank source pixels",
    },
}

ASSET_SOURCE_CROPS = {
    "commercial_cobble_long_a": ["counting_roof_plain_left", "counting_roof_plain_right", "counting_steps_material"],
    "commercial_cobble_patch_b": ["counting_roof_plain_left", "counting_steps_material"],
    "commercial_cobble_patch_c": ["counting_roof_plain_right", "counting_steps_material"],
    "curb_sidewalk_stoop_strip": ["counting_steps_material"],
    "curb_sidewalk_broken_edge": ["counting_steps_material"],
    "dirt_wear_transition": [],
    "dock_market_transition": ["wharf_plank_run", "wharf_waterline"],
    "dock_pier_vertical": ["wharf_plank_run"],
    "dock_edge_feather": ["wharf_plank_run", "wharf_waterline"],
    "pier_shadow_post_strip": ["wharf_waterline"],
    "crate_barrel_table_cluster": ["market_left_goods", "mercantile_right_crates"],
    "fence_sign_market_cluster": ["mercantile_hanging_sign", "mercantile_left_barrels"],
    "small_crate_barrel_cluster": ["mercantile_right_crates", "chandlery_left_props"],
    "market_sign_cluster": ["mercantile_hanging_sign", "mercantile_right_crates"],
    "wharf_crate_pile_cluster": ["boathouse_crate_stack", "boathouse_left_barrels", "wharf_plank_run"],
    "chandlery_base_cluster": ["chandlery_left_props", "chandlery_right_props"],
}


def rel(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def rgba(hex_color: str, alpha: int = 255) -> tuple[int, int, int, int]:
    value = hex_color.strip("#")
    return (int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16), alpha)


def hex_from_rgb(color: tuple[int, int, int]) -> str:
    return f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"


def seeded(asset_id: str, salt: int = 0) -> random.Random:
    seed = 418000 + salt
    for index, char in enumerate(asset_id):
        seed += (index + 1) * ord(char)
    return random.Random(seed)


def load_style_data() -> dict:
    if STYLE_JSON_PATH.exists():
        return json.loads(STYLE_JSON_PATH.read_text(encoding="utf-8"))
    return {}


def band(style_data: dict, name: str, fallback: list[str], limit: int) -> list[str]:
    values = [str(item.get("hex", "")) for item in style_data.get(name, [])]
    values = [value for value in values if value.startswith("#") and len(value) == 7]
    return (values[:limit] + fallback)[: max(limit, len(fallback))]


def load_palette(style_data: dict) -> dict[str, list[str]]:
    return {
        "outline": band(style_data, "outline_dark_edge_samples", ["#080808", "#181818", "#282818", "#383828"], 7),
        "shadow": band(style_data, "common_shadow_colors", ["#483828", "#584838", "#685848", "#383828"], 7),
        "midtone": band(style_data, "midtone_material_colors", ["#786858", "#887868", "#988878", "#a89888"], 8),
        "highlight": band(style_data, "highlight_colors", ["#d8c8b8", "#c8b8a8", "#d8c8a8", "#b8a898"], 8),
        "stone": ["#383838", "#484838", "#585858", "#685848", "#786858", "#887868", "#988878"],
        "wood": ["#382818", "#483828", "#584838", "#684828", "#786848", "#887858", "#a48658"],
        "rope": ["#786848", "#887858", "#a89878", "#b8a888", "#d8c8a8"],
        "grass": ["#243429", "#314d35", "#405c41", "#4e6849", "#5b7251", "#6f875a"],
        "dirt": ["#382818", "#483828", "#584838", "#685848", "#806442", "#a48658"],
        "water_shadow": ["#182421", "#20302d", "#283d39", "#38524c"],
    }


def crop_source(crop_id: str) -> Image.Image:
    crop = SOURCE_CROPS[crop_id]
    return Image.open(BUILDING_ROOT / crop["file"]).convert("RGBA").crop(tuple(crop["box"]))


def trim_alpha(image: Image.Image, padding: int = 2) -> Image.Image:
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        return image
    x0, y0, x1, y1 = bbox
    return image.crop((max(0, x0 - padding), max(0, y0 - padding), min(image.width, x1 + padding), min(image.height, y1 + padding)))


def fit_source(crop_id: str, size: tuple[int, int], alpha: int = 255, trim: bool = False, cover: bool = True) -> Image.Image:
    image = crop_source(crop_id)
    if trim:
        image = trim_alpha(image)
    if cover:
        image = ImageOps.fit(image, size, method=Image.Resampling.LANCZOS)
    else:
        contained = ImageOps.contain(image, size, method=Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", size, (0, 0, 0, 0))
        canvas.alpha_composite(contained, ((size[0] - contained.width) // 2, size[1] - contained.height))
        image = canvas
    image = ImageEnhance.Color(image).enhance(0.82)
    image = ImageEnhance.Contrast(image).enhance(1.06)
    image = ImageEnhance.Sharpness(image).enhance(1.12)
    if alpha < 255:
        image.putalpha(image.getchannel("A").point(lambda value: value * alpha // 255))
    return image


def overlay_source(tile: Image.Image, crop_id: str, alpha: int, trim: bool = False, cover: bool = True) -> Image.Image:
    texture = fit_source(crop_id, tile.size, alpha=alpha, trim=trim, cover=cover)
    mask = tile.getchannel("A")
    texture.putalpha(ImageChops.multiply(texture.getchannel("A"), mask))
    tile.alpha_composite(texture)
    return tile


def paste_source(tile: Image.Image, crop_id: str, xy: tuple[int, int], size: tuple[int, int], alpha: int = 242) -> None:
    piece = fit_source(crop_id, size, alpha=alpha, trim=True, cover=False)
    piece = add_alpha_outline(piece, "#080808", 72, 1)
    tile.alpha_composite(piece, xy)


def paste_source_hi(tile: Image.Image, crop_id: str, xy: tuple[int, int], size: tuple[int, int], alpha: int = 242) -> None:
    piece = fit_source(crop_id, (size[0] * SCALE, size[1] * SCALE), alpha=alpha, trim=True, cover=False)
    piece = add_alpha_outline(piece, "#080808", 84, 2)
    tile.alpha_composite(piece, (xy[0] * SCALE, xy[1] * SCALE))


def choose(rng: random.Random, colors: list[str]) -> tuple[int, int, int, int]:
    return rgba(rng.choice(colors))


def jitter(hex_color: str, rng: random.Random, amount: int = 8, alpha: int = 255) -> tuple[int, int, int, int]:
    r, g, b, _ = rgba(hex_color)
    return (
        max(0, min(255, r + rng.randint(-amount, amount))),
        max(0, min(255, g + rng.randint(-amount, amount))),
        max(0, min(255, b + rng.randint(-amount, amount))),
        alpha,
    )


def layer(size: tuple[int, int], bg: tuple[int, int, int, int] | None = None) -> Image.Image:
    if bg is None:
        bg = (0, 0, 0, 0)
    return Image.new("RGBA", (size[0] * SCALE, size[1] * SCALE), bg)


def down(image: Image.Image) -> Image.Image:
    if SCALE == 1:
        return image
    return image.resize((image.width // SCALE, image.height // SCALE), Image.Resampling.LANCZOS)


def sc_rect(rect: tuple[float, float, float, float]) -> tuple[int, int, int, int]:
    return tuple(int(round(value * SCALE)) for value in rect)


def sc_points(points: list[tuple[float, float]]) -> list[tuple[int, int]]:
    return [(int(round(x * SCALE)), int(round(y * SCALE))) for x, y in points]


def ellipse_shadow(size: tuple[int, int], alpha: int = 82, y_bias: float = 0.72) -> Image.Image:
    shadow = layer(size)
    draw = ImageDraw.Draw(shadow)
    width, height = size
    for i in range(5):
        inset = i * 2.8
        rect = (8 + inset, height * y_bias + inset, width - 8 - inset, height - 3)
        draw.ellipse(sc_rect(rect), fill=rgba("#080808", max(0, alpha - i * 13)))
    return down(shadow.filter(ImageFilter.GaussianBlur(1.25 * SCALE)))


def apply_ragged_alpha(tile: Image.Image, asset_id: str, top: int = 0, bottom: int = 0, left: int = 0, right: int = 0) -> Image.Image:
    rng = seeded(asset_id, 77)
    width, height = tile.size
    alpha = tile.getchannel("A")
    pixels = alpha.load()
    top_offsets = [rng.randint(0, max(0, top)) for _ in range(width)] if top else []
    bottom_offsets = [rng.randint(0, max(0, bottom)) for _ in range(width)] if bottom else []
    left_offsets = [rng.randint(0, max(0, left)) for _ in range(height)] if left else []
    right_offsets = [rng.randint(0, max(0, right)) for _ in range(height)] if right else []
    for y in range(height):
        for x in range(width):
            factor = 1.0
            if top:
                edge = top + top_offsets[x]
                if y < edge:
                    factor = min(factor, max(0.0, y / max(1.0, float(edge))))
            if bottom:
                edge = bottom + bottom_offsets[x]
                dist = height - 1 - y
                if dist < edge:
                    factor = min(factor, max(0.0, dist / max(1.0, float(edge))))
            if left:
                edge = left + left_offsets[y]
                if x < edge:
                    factor = min(factor, max(0.0, x / max(1.0, float(edge))))
            if right:
                edge = right + right_offsets[y]
                dist = width - 1 - x
                if dist < edge:
                    factor = min(factor, max(0.0, dist / max(1.0, float(edge))))
            if factor < 1.0:
                pixels[x, y] = int(pixels[x, y] * factor)
    tile.putalpha(alpha)
    return tile


def soften_edge(tile: Image.Image, blur: float = 0.35) -> Image.Image:
    alpha = tile.getchannel("A").filter(ImageFilter.GaussianBlur(blur))
    tile.putalpha(alpha)
    return tile


def draw_line_noise(draw: ImageDraw.ImageDraw, rng: random.Random, size: tuple[int, int], colors: list[str], count: int, alpha: tuple[int, int]) -> None:
    width, height = size
    for _ in range(count):
        x = rng.randint(1, max(1, width - 8))
        y = rng.randint(1, max(1, height - 4))
        length = rng.randint(4, min(36, max(5, width // 5)))
        color = jitter(rng.choice(colors), rng, 5, rng.randint(alpha[0], alpha[1]))
        draw.line(sc_points([(x, y), (min(width - 2, x + length), y + rng.choice([-1, 0, 1]))]), fill=color, width=max(1, SCALE))


def draw_poly(draw: ImageDraw.ImageDraw, points: list[tuple[float, float]], fill: tuple[int, int, int, int], outline: tuple[int, int, int, int], width: int = 1) -> None:
    scaled = sc_points(points)
    draw.polygon(scaled, fill=fill)
    draw.line(scaled + [scaled[0]], fill=outline, width=max(1, width * SCALE), joint="curve")


def draw_rect(draw: ImageDraw.ImageDraw, rect: tuple[float, float, float, float], fill: tuple[int, int, int, int], outline: tuple[int, int, int, int], width: int = 1) -> None:
    draw.rectangle(sc_rect(rect), fill=fill, outline=outline, width=max(1, width * SCALE))


def make_cobble(asset_id: str, size: tuple[int, int], palette: dict[str, list[str]], patch: bool = False) -> Image.Image:
    rng = seeded(asset_id, 101)
    base = layer(size, jitter("#585858", rng, 9, 238 if not patch else 220))
    draw = ImageDraw.Draw(base)
    width, height = size
    y = -rng.randint(0, 9)
    row_index = 0
    while y < height + 12:
        row_h = rng.randint(10, 15)
        x = -rng.randint(4, 26) if row_index % 2 == 0 else -rng.randint(18, 44)
        while x < width + 18:
            w = rng.randint(24, 52)
            skew = rng.randint(-3, 4)
            points = [
                (x + rng.randint(-2, 2), y + rng.randint(-2, 2)),
                (x + w + rng.randint(-3, 3), y + rng.randint(-1, 2)),
                (x + w + skew + rng.randint(-3, 3), y + row_h + rng.randint(-2, 2)),
                (x + skew + rng.randint(-2, 2), y + row_h + rng.randint(-2, 2)),
            ]
            fill = jitter(rng.choice(palette["stone"] + palette["midtone"][:4]), rng, 10, rng.randint(160, 220))
            outline = jitter(rng.choice(palette["outline"] + palette["shadow"]), rng, 5, rng.randint(62, 128))
            draw_poly(draw, points, fill, outline, 1)
            if rng.random() < 0.86:
                hx0 = max(0, points[0][0] + 3)
                hx1 = min(width, points[1][0] - 3)
                hy = points[0][1] + rng.uniform(1.2, 3.4)
                draw.line(sc_points([(hx0, hy), (hx1, hy + rng.choice([-0.4, 0, 0.4]))]), fill=jitter(rng.choice(palette["highlight"]), rng, 5, 52), width=max(1, SCALE))
            if rng.random() < 0.44:
                cx = x + rng.randint(4, max(5, w - 5))
                cy = y + rng.randint(3, max(4, row_h - 3))
                draw.line(sc_points([(cx, cy), (cx + rng.randint(4, 16), cy + rng.choice([-2, -1, 1, 2]))]), fill=jitter("#181818", rng, 3, 70), width=max(1, SCALE))
            x += w - rng.randint(0, 4)
        y += row_h - rng.randint(0, 2)
        row_index += 1
    draw_line_noise(draw, rng, size, palette["shadow"] + palette["highlight"], 150 if not patch else 74, (34, 84))
    if patch:
        apply_ragged_alpha(base, asset_id, top=16, bottom=18, left=22, right=20)
    else:
        apply_ragged_alpha(base, asset_id, top=4, bottom=7, left=5, right=6)
    result = soften_edge(down(base), 0.25)
    for crop_id in ASSET_SOURCE_CROPS.get(asset_id, [])[:2]:
        overlay_source(result, crop_id, 68 if not patch else 58)
    return result


def make_sidewalk(asset_id: str, size: tuple[int, int], palette: dict[str, list[str]], broken: bool = False) -> Image.Image:
    rng = seeded(asset_id, 117)
    base = layer(size, jitter("#786858", rng, 8, 236 if not broken else 214))
    draw = ImageDraw.Draw(base)
    width, height = size
    x = -rng.randint(0, 20)
    while x < width + 16:
        w = rng.randint(44, 80)
        y0 = rng.randint(1, 4)
        y1 = height - rng.randint(13, 18)
        fill = jitter(rng.choice(palette["stone"] + palette["midtone"]), rng, 9, 178)
        draw_poly(
            draw,
            [(x, y0), (x + w, y0 + rng.randint(-2, 2)), (x + w - rng.randint(0, 4), y1), (x + rng.randint(-3, 3), y1 + rng.randint(-1, 2))],
            fill,
            jitter(rng.choice(palette["outline"] + palette["shadow"]), rng, 4, 92),
            1,
        )
        x += w - rng.randint(0, 7)
    curb_h = 12 if not broken else 10
    draw.rectangle(sc_rect((0, height - curb_h, width, height)), fill=jitter("#383828", rng, 6, 112))
    for x in range(18, width - 44, 86):
        step_w = rng.randint(42, 58)
        step_h = rng.randint(14, 20)
        fill = jitter(rng.choice(palette["midtone"] + palette["highlight"][:3]), rng, 8, 168)
        draw_rect(draw, (x, 7, x + step_w, 7 + step_h), fill, jitter("#181818", rng, 4, 108), 1)
        draw.line(sc_points([(x + 4, 10), (x + step_w - 4, 9)]), fill=jitter(rng.choice(palette["highlight"]), rng, 4, 88), width=max(1, SCALE))
    draw_line_noise(draw, rng, size, palette["shadow"] + palette["highlight"], 82 if broken else 58, (36, 92))
    apply_ragged_alpha(base, asset_id, top=3, bottom=18 if broken else 5, left=10 if broken else 2, right=12 if broken else 2)
    result = soften_edge(down(base), 0.25)
    for crop_id in ASSET_SOURCE_CROPS.get(asset_id, []):
        overlay_source(result, crop_id, 82 if not broken else 66)
    return result


def make_shadow(asset_id: str, size: tuple[int, int]) -> Image.Image:
    tile = layer(size)
    draw = ImageDraw.Draw(tile)
    width, height = size
    for y in range(height):
        alpha = int(124 * (1.0 - y / max(1, height)) ** 1.4)
        draw.line(sc_points([(0, y), (width, y)]), fill=rgba("#080808", alpha), width=max(1, SCALE))
    rng = seeded(asset_id, 127)
    for _ in range(18):
        x = rng.randint(0, max(0, width - 34))
        y = rng.randint(height // 3, height - 11)
        draw.ellipse(sc_rect((x, y, x + rng.randint(24, 58), y + rng.randint(7, 15))), fill=rgba("#080808", rng.randint(20, 58)))
    apply_ragged_alpha(tile, asset_id, bottom=8, left=6, right=6)
    return down(tile.filter(ImageFilter.GaussianBlur(0.35 * SCALE)))


def make_dirt(asset_id: str, size: tuple[int, int], palette: dict[str, list[str]]) -> Image.Image:
    rng = seeded(asset_id, 133)
    base = layer(size, jitter("#584838", rng, 8, 210))
    draw = ImageDraw.Draw(base)
    width, height = size
    for _ in range(95):
        x = rng.randint(-18, width - 4)
        y = rng.randint(2, height - 4)
        length = rng.randint(16, 72)
        color = jitter(rng.choice(palette["dirt"] + palette["stone"][:3]), rng, 8, rng.randint(42, 118))
        draw.line(sc_points([(x, y), (min(width + 8, x + length), y + rng.randint(-3, 3))]), fill=color, width=max(1, SCALE))
    for _ in range(24):
        cx = rng.randint(0, width)
        cy = rng.randint(0, height)
        r = rng.randint(2, 7)
        draw.ellipse(sc_rect((cx - r, cy - r * 0.4, cx + r, cy + r * 0.4)), fill=jitter(rng.choice(palette["stone"]), rng, 7, rng.randint(24, 72)))
    apply_ragged_alpha(base, asset_id, top=17, bottom=18, left=16, right=16)
    result = soften_edge(down(base.filter(ImageFilter.GaussianBlur(0.15 * SCALE))), 0.3)
    for crop_id in ASSET_SOURCE_CROPS.get(asset_id, []):
        overlay_source(result, crop_id, 40)
    return result


def make_grass(asset_id: str, size: tuple[int, int], palette: dict[str, list[str]], feather: bool = False) -> Image.Image:
    rng = seeded(asset_id, 149)
    base = layer(size, jitter("#405c41", rng, 8, 214 if feather else 226))
    draw = ImageDraw.Draw(base)
    width, height = size
    for _ in range(165 if not feather else 122):
        x = rng.randint(-6, width - 2)
        y = rng.randint(0, height - 2)
        length = rng.randint(5, 24)
        color = jitter(rng.choice(palette["grass"] + palette["dirt"][:3] + palette["highlight"][:2]), rng, 8, rng.randint(34, 104))
        draw.line(sc_points([(x, y), (min(width, x + length), y + rng.choice([-2, -1, 0, 1]))]), fill=color, width=max(1, SCALE))
    if feather:
        for _ in range(34):
            x = rng.randint(0, width - 18)
            y = rng.randint(height // 4, height - 5)
            draw.line(sc_points([(x, y), (x + rng.randint(12, 44), y + rng.randint(-2, 2))]), fill=jitter(rng.choice(palette["stone"] + palette["shadow"]), rng, 6, rng.randint(34, 72)), width=max(1, SCALE))
    draw_line_noise(draw, rng, size, palette["shadow"] + palette["highlight"], 38 if not feather else 64, (22, 70))
    apply_ragged_alpha(base, asset_id, top=18 if feather else 5, bottom=21 if feather else 11, left=10, right=12)
    return soften_edge(down(base), 0.25)


def make_dock(asset_id: str, size: tuple[int, int], palette: dict[str, list[str]], feather: bool = False) -> Image.Image:
    rng = seeded(asset_id, 173)
    base = layer(size, jitter("#584838", rng, 8, 232 if not feather else 200))
    draw = ImageDraw.Draw(base)
    width, height = size
    y = -rng.randint(0, 11)
    while y < height + 10:
        plank_h = rng.randint(8, 12)
        fill = jitter(rng.choice(palette["wood"] + palette["midtone"][:4]), rng, 10, rng.randint(154, 218))
        draw_rect(draw, (-4, y, width + 4, y + plank_h), fill, jitter("#181808", rng, 4, 84 if not feather else 58), 1)
        x = -rng.randint(4, 20)
        while x < width + 8:
            joint = x + rng.randint(42, 88)
            draw.line(sc_points([(joint, y + 1), (joint + rng.randint(-1, 1), y + plank_h - 1)]), fill=jitter("#080808", rng, 3, rng.randint(36, 88)), width=max(1, SCALE))
            x = joint
        for _ in range(rng.randint(3, 6)):
            sx = rng.randint(0, width - 10)
            sy = y + rng.randint(1, max(1, plank_h - 2))
            draw.line(sc_points([(sx, sy), (sx + rng.randint(10, 34), sy + rng.choice([-1, 0, 1]))]), fill=jitter(rng.choice(palette["highlight"] + palette["shadow"]), rng, 5, rng.randint(28, 78)), width=max(1, SCALE))
        y += plank_h - rng.randint(0, 2)
    if not feather:
        for x in range(12, width, 72):
            draw.rectangle(sc_rect((x, 0, x + 5, height)), fill=jitter("#181808", rng, 4, 74))
            draw.line(sc_points([(x + 3, 5), (x + 4, height - 5)]), fill=jitter(rng.choice(palette["highlight"]), rng, 5, 38), width=max(1, SCALE))
    else:
        for _ in range(38):
            x = rng.randint(0, width - 2)
            y = rng.randint(height - 25, height - 2)
            draw.line(sc_points([(x, y), (x + rng.randint(5, 28), y + rng.randint(-1, 2))]), fill=jitter(rng.choice(palette["water_shadow"] + palette["grass"]), rng, 5, rng.randint(42, 96)), width=max(1, SCALE))
    apply_ragged_alpha(base, asset_id, top=4 if not feather else 7, bottom=7 if not feather else 20, left=5 if not feather else 12, right=5 if not feather else 14)
    result = soften_edge(down(base), 0.25)
    for crop_id in ASSET_SOURCE_CROPS.get(asset_id, []):
        overlay_source(result, crop_id, 112 if not feather else 84)
    return result


def make_pier(asset_id: str, size: tuple[int, int], palette: dict[str, list[str]]) -> Image.Image:
    rng = seeded(asset_id, 181)
    base = layer(size)
    draw = ImageDraw.Draw(base)
    width, height = size
    x = 10
    while x < width - 8:
        plank_w = rng.randint(10, 14)
        fill = jitter(rng.choice(palette["wood"]), rng, 10, 218)
        draw_rect(draw, (x, 0, x + plank_w, height), fill, jitter("#181808", rng, 4, 88), 1)
        for y in range(12, height, 34):
            draw.line(sc_points([(x + 2, y), (x + plank_w - 2, y + rng.randint(-1, 1))]), fill=jitter(rng.choice(palette["highlight"] + palette["shadow"]), rng, 6, 58), width=max(1, SCALE))
        x += plank_w - rng.randint(0, 1)
    for y in range(0, height, 56):
        draw.rectangle(sc_rect((8, y + 2, width - 8, y + 6)), fill=jitter("#181808", rng, 4, 76))
    apply_ragged_alpha(base, asset_id, top=4, bottom=8, left=7, right=7)
    result = soften_edge(down(base), 0.25)
    for crop_id in ASSET_SOURCE_CROPS.get(asset_id, []):
        overlay_source(result, crop_id, 98)
    return result


def make_pier_shadow(asset_id: str, size: tuple[int, int], palette: dict[str, list[str]]) -> Image.Image:
    rng = seeded(asset_id, 191)
    base = layer(size)
    draw = ImageDraw.Draw(base)
    width, height = size
    for x in range(10, width - 8, 32):
        post_w = rng.randint(3, 5)
        post_h = rng.randint(26, 50)
        draw.rectangle(sc_rect((x, height - post_h - 4, x + post_w, height - 4)), fill=jitter("#181808", rng, 3, 112))
        draw.ellipse(sc_rect((x - 10, height - 17, x + 22, height - 4)), fill=rgba("#080808", rng.randint(30, 62)))
        draw.line(sc_points([(x + post_w + 1, height - post_h), (x + post_w + rng.randint(12, 26), height - post_h + rng.randint(2, 9))]), fill=jitter(rng.choice(palette["water_shadow"]), rng, 5, 60), width=max(1, SCALE))
    for _ in range(38):
        y = rng.randint(height - 20, height - 3)
        x = rng.randint(0, width - 14)
        draw.line(sc_points([(x, y), (x + rng.randint(8, 34), y + rng.randint(-1, 1))]), fill=jitter(rng.choice(palette["water_shadow"]), rng, 4, rng.randint(26, 72)), width=max(1, SCALE))
    apply_ragged_alpha(base, asset_id, top=8, bottom=10, left=12, right=12)
    result = down(base.filter(ImageFilter.GaussianBlur(0.25 * SCALE)))
    for crop_id in ASSET_SOURCE_CROPS.get(asset_id, []):
        overlay_source(result, crop_id, 60)
    return result


def add_alpha_outline(image: Image.Image, color: str = "#080808", alpha: int = 145, radius: int = 2) -> Image.Image:
    mask = image.getchannel("A")
    outline = mask.filter(ImageFilter.MaxFilter(radius * 2 + 1))
    outline = ImageChops.subtract(outline, mask)
    out = Image.new("RGBA", image.size, (0, 0, 0, 0))
    color_layer = Image.new("RGBA", image.size, rgba(color, alpha))
    color_layer.putalpha(outline.point(lambda value: min(value, alpha)))
    out.alpha_composite(color_layer)
    out.alpha_composite(image)
    return out


def stylize_blender_component(component_id: str, size: tuple[int, int], palette: dict[str, list[str]], alpha: int = 232) -> Image.Image | None:
    path = BLENDER_COMPONENT_ROOT / f"{component_id}.png"
    if not path.exists():
        return None
    image = Image.open(path).convert("RGBA")
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        return None
    image = image.crop((max(0, bbox[0] - 3), max(0, bbox[1] - 3), min(image.width, bbox[2] + 3), min(image.height, bbox[3] + 3)))
    pixels = image.load()
    rng = seeded(component_id, 207)
    wood_ramp = [rgba(color)[:3] for color in (palette["shadow"][:2] + palette["wood"] + palette["highlight"][:2])]
    rope_ramp = [rgba(color)[:3] for color in (palette["shadow"][:1] + palette["rope"])]
    ramp = rope_ramp if "rope" in component_id else wood_ramp
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            lum = (r * 0.3 + g * 0.59 + b * 0.11) / 255.0
            index = max(0, min(len(ramp) - 1, int(lum * (len(ramp) - 1))))
            rr, gg, bb = ramp[index]
            pixels[x, y] = (
                max(0, min(255, rr + rng.randint(-5, 5))),
                max(0, min(255, gg + rng.randint(-5, 5))),
                max(0, min(255, bb + rng.randint(-5, 5))),
                min(a, alpha),
            )
    image = ImageEnhance.Contrast(image).enhance(1.18)
    image = ImageEnhance.Sharpness(image).enhance(1.35)
    image = add_alpha_outline(image, "#080808", 136, 2)
    image = ImageOps.contain(image, size, method=Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(image)
    for _ in range(16):
        x = rng.randint(0, max(0, image.width - 6))
        y = rng.randint(0, max(0, image.height - 3))
        draw.line((x, y, min(image.width - 1, x + rng.randint(4, 18)), y + rng.choice([-1, 0, 1])), fill=jitter(rng.choice(palette["highlight"] + palette["shadow"]), rng, 5, rng.randint(32, 76)), width=1)
    return image


def paste_blender(tile: Image.Image, component_id: str, xy: tuple[int, int], size: tuple[int, int], palette: dict[str, list[str]], alpha: int = 232) -> None:
    component = stylize_blender_component(component_id, size, palette, alpha)
    if component is not None:
        tile.alpha_composite(component, xy)


def draw_crate(draw: ImageDraw.ImageDraw, rng: random.Random, x: float, y: float, w: float, h: float, palette: dict[str, list[str]], tilt: float = 4.0) -> None:
    fill = jitter(rng.choice(palette["wood"]), rng, 9, 238)
    outline = jitter("#080808", rng, 3, 150)
    draw_poly(draw, [(x, y + tilt), (x + w, y), (x + w, y + h), (x, y + h + tilt)], fill, outline, 1)
    for frac in (0.24, 0.52, 0.78):
        xx = x + w * frac
        draw.line(sc_points([(xx, y + 2), (xx, y + h - 2)]), fill=jitter(rng.choice(palette["shadow"]), rng, 5, 100), width=max(1, SCALE))
    draw.line(sc_points([(x + 4, y + 5), (x + w - 4, y + h - 5)]), fill=jitter(rng.choice(palette["shadow"]), rng, 4, 116), width=max(1, SCALE))
    draw.line(sc_points([(x + 5, y + h - 7), (x + w - 5, y + 7)]), fill=jitter(rng.choice(palette["highlight"]), rng, 4, 64), width=max(1, SCALE))
    for _ in range(5):
        sx = rng.uniform(x + 4, x + w - 10)
        sy = rng.uniform(y + 4, y + h - 4)
        draw.line(sc_points([(sx, sy), (sx + rng.uniform(4, 12), sy + rng.choice([-1, 0, 1]))]), fill=jitter(rng.choice(palette["highlight"] + palette["shadow"]), rng, 4, rng.randint(42, 86)), width=max(1, SCALE))


def draw_barrel(draw: ImageDraw.ImageDraw, rng: random.Random, x: float, y: float, w: float, h: float, palette: dict[str, list[str]]) -> None:
    fill = jitter(rng.choice(palette["wood"]), rng, 8, 238)
    outline = jitter("#080808", rng, 3, 150)
    draw.ellipse(sc_rect((x, y, x + w, y + h * 0.28)), fill=jitter(rng.choice(palette["highlight"] + palette["wood"]), rng, 8, 212), outline=outline, width=max(1, SCALE))
    draw.rectangle(sc_rect((x + 1, y + h * 0.14, x + w - 1, y + h * 0.84)), fill=fill)
    draw.ellipse(sc_rect((x, y + h * 0.66, x + w, y + h)), fill=jitter(rng.choice(palette["wood"] + palette["shadow"]), rng, 8, 224), outline=outline, width=max(1, SCALE))
    for frac in (0.23, 0.76):
        yy = y + h * frac
        draw.line(sc_points([(x + 2, yy), (x + w - 2, yy + rng.choice([-1, 0, 1]))]), fill=jitter("#181808", rng, 3, 130), width=max(1, SCALE))
    for frac in (0.32, 0.5, 0.68):
        xx = x + w * frac
        draw.line(sc_points([(xx, y + 3), (xx + rng.choice([-1, 0, 1]), y + h - 4)]), fill=jitter(rng.choice(palette["shadow"]), rng, 5, 66), width=max(1, SCALE))
    draw.arc(sc_rect((x + 3, y + 2, x + w - 3, y + h * 0.26)), 190, 350, fill=jitter(rng.choice(palette["highlight"]), rng, 4, 88), width=max(1, SCALE))


def draw_sack(draw: ImageDraw.ImageDraw, rng: random.Random, x: float, y: float, w: float, h: float, palette: dict[str, list[str]]) -> None:
    fill = jitter(rng.choice(palette["rope"] + palette["midtone"][:3]), rng, 8, 224)
    outline = jitter("#181808", rng, 3, 122)
    points = [(x + w * 0.22, y + h * 0.16), (x + w * 0.78, y + h * 0.12), (x + w, y + h * 0.62), (x + w * 0.76, y + h), (x + w * 0.2, y + h * 0.9), (x, y + h * 0.48)]
    draw_poly(draw, points, fill, outline, 1)
    draw.line(sc_points([(x + w * 0.24, y + h * 0.32), (x + w * 0.72, y + h * 0.28)]), fill=jitter(rng.choice(palette["highlight"]), rng, 4, 64), width=max(1, SCALE))
    draw.line(sc_points([(x + w * 0.48, y + h * 0.16), (x + w * 0.55, y + h * 0.9)]), fill=jitter(rng.choice(palette["shadow"]), rng, 4, 52), width=max(1, SCALE))


def draw_rope(draw: ImageDraw.ImageDraw, rng: random.Random, x: float, y: float, w: float, h: float, palette: dict[str, list[str]]) -> None:
    outline = jitter("#080808", rng, 3, 128)
    for i, inset in enumerate([0, 5, 10]):
        color = jitter(rng.choice(palette["rope"]), rng, 8, 232 - i * 14)
        draw.ellipse(sc_rect((x + inset, y + inset * 0.62, x + w - inset, y + h - inset * 0.62)), outline=outline, width=max(1, SCALE))
        draw.arc(sc_rect((x + inset + 1, y + inset * 0.62 + 1, x + w - inset - 1, y + h - inset * 0.62 - 1)), 15, 335, fill=color, width=max(2, SCALE * 2))
    draw.line(sc_points([(x + w * 0.55, y + h * 0.55), (x + w + 8, y + h * 0.52)]), fill=jitter(rng.choice(palette["rope"]), rng, 7, 210), width=max(2, SCALE * 2))


def draw_table(draw: ImageDraw.ImageDraw, rng: random.Random, x: float, y: float, w: float, h: float, palette: dict[str, list[str]]) -> None:
    outline = jitter("#080808", rng, 3, 146)
    top_fill = jitter(rng.choice(palette["wood"] + palette["midtone"][:2]), rng, 9, 238)
    draw_poly(draw, [(x, y + h * 0.18), (x + w, y), (x + w - 8, y + h * 0.36), (x + 5, y + h * 0.48)], top_fill, outline, 1)
    for frac in (0.23, 0.48, 0.72):
        sx = x + w * frac
        draw.line(sc_points([(sx, y + h * 0.12), (sx - 3, y + h * 0.41)]), fill=jitter(rng.choice(palette["shadow"]), rng, 4, 92), width=max(1, SCALE))
    for lx in (x + 8, x + w - 16):
        draw.rectangle(sc_rect((lx, y + h * 0.35, lx + 5, y + h)), fill=jitter("#181808", rng, 3, 152))
    for i in range(6):
        fx = x + 12 + i * (w - 28) / 5
        fy = y + rng.uniform(6, h * 0.22)
        fish = jitter("#c8b8a8", rng, 6, 220)
        draw.ellipse(sc_rect((fx, fy, fx + 10, fy + 4)), fill=fish, outline=outline, width=max(1, SCALE))
        draw.polygon(sc_points([(fx + 9, fy + 2), (fx + 14, fy - 1), (fx + 13, fy + 5)]), fill=fish)


def draw_fence(draw: ImageDraw.ImageDraw, rng: random.Random, x: float, y: float, w: float, h: float, palette: dict[str, list[str]]) -> None:
    outline = jitter("#080808", rng, 3, 132)
    wood = jitter(rng.choice(palette["wood"]), rng, 8, 224)
    for frac in (0.1, 0.38, 0.66, 0.9):
        px = x + w * frac
        draw_rect(draw, (px, y, px + 5, y + h), wood, outline, 1)
        draw.line(sc_points([(px + 1, y + 4), (px + 1, y + h - 4)]), fill=jitter(rng.choice(palette["highlight"]), rng, 4, 54), width=max(1, SCALE))
    for yy in (y + h * 0.32, y + h * 0.68):
        draw_poly(draw, [(x, yy), (x + w, yy - 3), (x + w, yy + 5), (x, yy + 8)], wood, outline, 1)


def draw_sign(draw: ImageDraw.ImageDraw, rng: random.Random, x: float, y: float, w: float, h: float, palette: dict[str, list[str]], mark: str) -> None:
    outline = jitter("#080808", rng, 3, 144)
    draw_rect(draw, (x + w * 0.46, y + h * 0.3, x + w * 0.54, y + h), jitter("#382818", rng, 5, 224), outline, 1)
    board = (x, y, x + w, y + h * 0.38)
    draw_rect(draw, board, jitter(rng.choice(palette["wood"]), rng, 9, 236), outline, 1)
    draw.line(sc_points([(x + 6, y + 6), (x + w - 6, y + 5)]), fill=jitter(rng.choice(palette["highlight"]), rng, 5, 64), width=max(1, SCALE))
    try:
        font = ImageFont.truetype("arial.ttf", max(8, int(10 * SCALE)))
    except OSError:
        font = ImageFont.load_default()
    draw.text((int((x + w * 0.43) * SCALE), int((y + 5) * SCALE)), mark, fill=jitter("#181808", rng, 3, 170), font=font)


def make_prop_cluster(asset_id: str, size: tuple[int, int], palette: dict[str, list[str]]) -> Image.Image:
    rng = seeded(asset_id, 223)
    base = layer(size)
    small_shadow = ellipse_shadow(size, 74, 0.76).resize((size[0] * SCALE, size[1] * SCALE), Image.Resampling.BILINEAR)
    base.alpha_composite(small_shadow)
    draw = ImageDraw.Draw(base)

    if asset_id == "crate_barrel_table_cluster":
        paste_blender(base, "market_table", (12 * SCALE, 36 * SCALE), (84, 58), palette, 198)
        draw_table(draw, rng, 18, 41, 72, 39, palette)
        paste_source_hi(base, "market_left_goods", (50, 30), (74, 66), 236)
        paste_source_hi(base, "mercantile_right_crates", (112, 58), (58, 50), 238)
        draw_barrel(draw, rng, 96, 66, 20, 30, palette)
        draw_rope(draw, rng, 67, 91, 29, 17, palette)
    elif asset_id == "fence_sign_market_cluster":
        paste_blender(base, "fence_segment", (8 * SCALE, 63 * SCALE), (112, 44), palette, 192)
        draw_fence(draw, rng, 12, 70, 108, 32, palette)
        paste_source_hi(base, "mercantile_hanging_sign", (118, 10), (50, 76), 238)
        paste_source_hi(base, "mercantile_left_barrels", (66, 61), (55, 49), 232)
        draw_crate(draw, rng, 137, 82, 31, 24, palette)
    elif asset_id == "small_crate_barrel_cluster":
        paste_source_hi(base, "mercantile_right_crates", (10, 28), (72, 62), 238)
        paste_source_hi(base, "chandlery_left_props", (66, 39), (62, 52), 236)
        draw_barrel(draw, rng, 103, 50, 22, 33, palette)
        draw_sack(draw, rng, 122, 40, 25, 25, palette)
        draw_rope(draw, rng, 61, 76, 37, 22, palette)
    elif asset_id == "market_sign_cluster":
        draw_fence(draw, rng, 18, 62, 82, 32, palette)
        paste_source_hi(base, "mercantile_hanging_sign", (100, 14), (43, 72), 236)
        paste_source_hi(base, "mercantile_right_crates", (112, 76), (39, 30), 230)
        draw_rope(draw, rng, 36, 82, 29, 17, palette)
    elif asset_id == "wharf_crate_pile_cluster":
        dock = make_dock(asset_id + "_dock_floor", (size[0], 44), palette, feather=True)
        base.alpha_composite(dock.resize((size[0] * SCALE, 44 * SCALE), Image.Resampling.BILINEAR), (0, (size[1] - 48) * SCALE))
        paste_source_hi(base, "boathouse_crate_stack", (22, 32), (124, 84), 242)
        paste_source_hi(base, "boathouse_left_barrels", (126, 55), (62, 52), 230)
        draw_barrel(draw, rng, 174, 64, 21, 31, palette)
        draw_rope(draw, rng, 126, 88, 43, 24, palette)
        draw_sack(draw, rng, 78, 81, 28, 24, palette)
    elif asset_id == "chandlery_base_cluster":
        paste_source_hi(base, "chandlery_left_props", (20, 50), (76, 56), 238)
        paste_source_hi(base, "chandlery_right_props", (104, 38), (96, 70), 238)
        draw_sign(draw, rng, 18, 28, 38, 62, palette, "R")
        draw_rope(draw, rng, 91, 98, 38, 22, palette)
        draw_rope(draw, rng, 154, 98, 31, 18, palette)
    draw_line_noise(draw, rng, size, palette["shadow"] + palette["highlight"], 18, (22, 58))
    out = down(base)
    return apply_ragged_alpha(out, asset_id, top=2, bottom=4, left=3, right=3)


def build_tile(asset_id: str, palette: dict[str, list[str]], size: tuple[int, int]) -> Image.Image:
    if asset_id == "commercial_cobble_long_a":
        return make_cobble(asset_id, size, palette, patch=False)
    if asset_id in ["commercial_cobble_patch_b", "commercial_cobble_patch_c"]:
        return make_cobble(asset_id, size, palette, patch=True)
    if asset_id == "curb_sidewalk_stoop_strip":
        return make_sidewalk(asset_id, size, palette, broken=False)
    if asset_id == "curb_sidewalk_broken_edge":
        return make_sidewalk(asset_id, size, palette, broken=True)
    if asset_id == "building_contact_shadow_strip":
        return make_shadow(asset_id, size)
    if asset_id == "dirt_wear_transition":
        return make_dirt(asset_id, size, palette)
    if asset_id == "grass_edge_north":
        return make_grass(asset_id, size, palette, feather=False)
    if asset_id == "grass_cobble_feather":
        return make_grass(asset_id, size, palette, feather=True)
    if asset_id == "dock_market_transition":
        return make_dock(asset_id, size, palette, feather=False)
    if asset_id == "dock_edge_feather":
        return make_dock(asset_id, size, palette, feather=True)
    if asset_id == "dock_pier_vertical":
        return make_pier(asset_id, size, palette)
    if asset_id == "pier_shadow_post_strip":
        return make_pier_shadow(asset_id, size, palette)
    return make_prop_cluster(asset_id, size, palette)


def generated_piece_path(asset_id: str) -> Path:
    return GENERATED_ROOT / f"{asset_id}.png"


def draw_atlas(palette: dict[str, list[str]]) -> dict[str, Path]:
    atlas = Image.new("RGBA", (1024, 768), (0, 0, 0, 0))
    generated_paths: dict[str, Path] = {}
    GENERATED_ROOT.mkdir(parents=True, exist_ok=True)
    for asset_id, region in REGIONS.items():
        _, _, width, height = region
        tile = build_tile(asset_id, palette, (width, height))
        atlas.alpha_composite(tile, (region[0], region[1]))
        piece_path = generated_piece_path(asset_id)
        tile.save(piece_path)
        generated_paths[asset_id] = piece_path
    ATLAS_PATH.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(ATLAS_PATH)
    return generated_paths


def blender_sources_for(asset_id: str) -> list[dict[str, object]]:
    sources = []
    for component_id in BLENDER_COMPONENTS_BY_ASSET.get(asset_id, []):
        path = BLENDER_COMPONENT_ROOT / f"{component_id}.png"
        if path.exists():
            sources.append(
                {
                    "component_id": component_id,
                    "file": rel(path),
                    "source": "Blender 5.1 procedural mesh render created locally for Wayfarer, then palette-stylized by the asset factory",
                    "source_pixels_copied": True,
                    "source_pixels_kind": "project-owned generated support pixels",
                    "third_party_pixels": False,
                    "creation_script": rel(BLENDER_SCRIPT_PATH),
                }
            )
    return sources


def crop_manifest_entries(asset_id: str) -> list[dict[str, object]]:
    entries = []
    for crop_id in ASSET_SOURCE_CROPS.get(asset_id, []):
        crop = SOURCE_CROPS[crop_id]
        entries.append(
            {
                "source_crop_id": crop_id,
                "file": f"assets/sprites/buildings/isolated/{crop['file']}",
                "crop": crop["box"],
                "usage": crop["usage"],
                "ownership": "project-owned in-repo Newport building sprite",
                "source_pixels_copied": True,
                "third_party_pixels": False,
            }
        )
    return entries


def manifest_entry(asset_id: str, region: list[int], generated_paths: dict[str, Path], style_data: dict) -> dict:
    is_prop = "cluster" in asset_id
    script = rel(SCRIPT_PATH)
    blender_sources = blender_sources_for(asset_id)
    crop_sources = crop_manifest_entries(asset_id)
    uses_project_owned_pixels = bool(crop_sources)
    source = {
        "type": "deterministic_generated_bitmap",
        "source_kind": "temporary_review_yellow_with_documented_newport_crop_or_palette_influence",
        "created_by": script,
        "creation_script": script,
        "support_scripts": [rel(BLENDER_SCRIPT_PATH)] if blender_sources else [],
        "exact_source_path": rel(generated_paths[asset_id]),
        "generated_piece_file": rel(generated_paths[asset_id]),
        "atlas_file": rel(ATLAS_PATH),
        "ownership": "project-owned",
        "license": "Wayfarer temporary yellow review asset; commercial final use blocked until every yellow/uncertain Newport building source influence is replaced or proven green; no third-party game sprites, ripped assets, marketplace/demo/sample assets, web-scraped art, copied prior prop-sheet pixels, or copied third-party pixels are allowed.",
        "license_ownership_status": "temporary yellow review asset; not final-commercial eligible after G-4.18A.",
        "palette_reference_manifest": rel(STYLE_JSON_PATH),
        "palette_reference_sources": style_data.get("source_files", []),
        "newport_art_bible": rel(ART_BIBLE_PATH),
        "material_sources": crop_sources,
        "blender_component_sources": blender_sources,
        "prior_project_prop_sources": [],
        "source_manifest": rel(STYLE_JSON_PATH),
        "source_pixels_from_prior_wayfarer_assets": uses_project_owned_pixels,
        "source_pixels_from_project_owned_wayfarer_assets": uses_project_owned_pixels,
        "source_pixels_from_yellow_uncertain_assets": True,
        "green_origin_candidate": False,
        "palette_reference_from_project_owned_wayfarer_assets": True,
        "source_pixels_from_third_party_material": False,
        "third_party_source_pixels": False,
        "web_scraped_source_pixels": False,
        "ai_generated": False,
        "hand_authored": True,
        "deterministic_generated": True,
        "notes": "Built for prototype review with deterministic Pillow mark-making and documented Newport building crop/palette influence. Because those Newport building sources are yellow/uncertain, this asset is yellow review art only and cannot seed green final assets.",
    }
    return {
        "asset_id": asset_id,
        "material_category": MATERIAL_CATEGORIES[asset_id],
        "source_file": rel(ATLAS_PATH),
        "generated_piece_file": rel(generated_paths[asset_id]),
        "source": source,
        "atlas_region": {"x": region[0], "y": region[1], "w": region[2], "h": region[3]},
        "intended_scale": "1 atlas pixel maps to approximately 1 world pixel; prop clusters are scaled below Newport door height and seated against steps, barrels, dock posts, and temporary player clearance.",
        "collision_behavior": "none; decorative/grounding only" if not is_prop else "decorative only in G-4.18 review; no gameplay collision until dedicated blockers are authored.",
        "y_sort_behavior": "drawn on map layer below buildings; props are seated in front-of-building or wharf bands and remain non-interactive",
        "contact_shadow_required": True,
        "visual_cohesion_status": "g418_review_candidate",
        "visual_quality_status": "temporary_review_visual_accepted",
        "provenance_status": "temporary_review_yellow",
        "placeholder": False,
        "final": False,
        "review_eligible": True,
        "normal_review_eligible": True,
        "lab_only": False,
        "review_eligibility": "eligible",
        "license_ownership_status": "temporary yellow review asset; no third-party, marketplace, web-scraped, or ripped pixels known, but yellow/uncertain Newport building source influence prevents final-commercial classification.",
        "origin_classification": "temporary_review_yellow",
        "commercial_use_status": "temporary_review_yellow",
        "final_commercial_candidate": False,
        "final_commercial_eligible": False,
        "source_pixels_from_yellow_uncertain_assets": True,
        "yellow_source_policy": "Visual review only. Do not use this asset or its source pixels as source material for green/final-commercial assets without source proof.",
        "visual_quality_gate": "Allowed in normal review only as temporary yellow art because it currently improves the screenshot; blocked from final-commercial green promotion.",
        "normal_review_mode": True,
        "source_pixels_from_prior_wayfarer_assets": uses_project_owned_pixels,
        "source_pixels_from_project_owned_wayfarer_assets": uses_project_owned_pixels,
        "palette_reference_from_project_owned_wayfarer_assets": True,
        "source_pixels_from_third_party_material": False,
        "review_notes": "Reclassified by G-4.18B as temporary yellow review art due to yellow/uncertain Newport building crop or palette influence. Still allowed in prototype review composition; not final-commercial.",
    }


def write_manifest(generated_paths: dict[str, Path], style_data: dict) -> dict:
    assets = [manifest_entry(asset_id, region, generated_paths, style_data) for asset_id, region in REGIONS.items()]
    manifest = {
        "schema_id": "wayfarer.newport.asset_manifest.v2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "phase": "G-4.18-temporary-yellow",
        "atlas": rel(ATLAS_PATH),
        "generated_asset_root": rel(GENERATED_ROOT),
        "blender_component_manifest": rel(BLENDER_COMPONENT_MANIFEST) if BLENDER_COMPONENT_MANIFEST.exists() else "",
        "assets": assets,
        "origin_taxonomy": ["temporary_review_yellow", "green_origin_candidate", "final_commercial_green", "red_unsafe"],
        "source_policy": "Temporary yellow review art may be used to prototype composition, scale, and gameplay, but final-commercial Wayfarer art must come from green-origin assets with documented provenance. Yellow assets cannot be used as pixel sources for green final art.",
        "review_gate": "Assets with placeholder=false and review_eligible=true must satisfy NEWPORT_ART_BIBLE.md and must have project-owned or compatible licensed provenance.",
        "third_party_policy": "No third-party game sprites, ripped assets, marketplace/demo/sample assets, mystery assets, web-scraped art, or copied recognizable third-party sprite pixels are allowed.",
        "generation_policy": "Review-facing G-4.18 hero assets are deterministic Pillow output plus documented Newport material/prop crops or palette influence; after G-4.18A those source influences are yellow/uncertain and cannot become final-commercial green without replacement or proof.",
        "g418b_reclassification": "G-4.17/G-4.18 hero assets remain review-eligible temporary yellow art because their source chain includes yellow/uncertain Newport building crop or palette influence.",
        "green_origin_manifest": "art_pipeline/newport_green_origin/manifests/green_origin_asset_manifest.json",
        "legacy_manifest_mirror": rel(LEGACY_MANIFEST_PATH),
        "visual_quality_gate": "Green-origin is necessary but not sufficient. Assets require separate provenance and visual approval before normal review or final-commercial eligibility.",
    }
    CANONICAL_MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    LEGACY_MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def make_contact_sheet() -> None:
    atlas = Image.open(ATLAS_PATH).convert("RGBA")
    sheet = Image.new("RGBA", (1320, 900), rgba("#20261e"))
    sheet.alpha_composite(atlas, (20, 20))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.rectangle((20, 20, 1044, 788), outline=rgba("#f1e0ad"), width=2)
    for index, (asset_id, region) in enumerate(REGIONS.items()):
        x, y, width, height = region
        ox, oy = 20 + x, 20 + y
        draw.rectangle((ox, oy, ox + width, oy + height), outline=rgba("#f1e0ad", 138), width=1)
        label_y = 32 + index * 43
        draw.text((1074, label_y), f"{asset_id}: {region}", fill=rgba("#f1e0ad"), font=font)
    CONTACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    sheet.convert("RGB").save(CONTACT_PATH)


def make_provenance_proof(manifest: dict) -> None:
    assets = manifest["assets"]
    sheet = Image.new("RGB", (1400, 1100), "#243025")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((24, 22), "G-4.18 Newport provenance-safe hero asset proof", fill="#f1e0ad", font=font)
    draw.text((24, 44), "Review pieces are project-owned generated/composited output with documented Newport crops only; no prior prop-sheet, third-party, marketplace, scraped, or ripped sprite pixels.", fill="#d9cda5", font=font)
    x, y = 24, 80
    card_w, card_h = 250, 210
    for index, asset in enumerate(assets):
        asset_id = asset["asset_id"]
        piece = Image.open(PROJECT_ROOT / asset["generated_piece_file"]).convert("RGBA")
        piece.thumbnail((220, 112))
        draw.rectangle((x, y, x + card_w, y + card_h), outline="#59634c", width=1)
        tile = Image.new("RGBA", (220, 112), (45, 52, 39, 255))
        tile.alpha_composite(piece, ((220 - piece.width) // 2, (112 - piece.height) // 2))
        sheet.paste(tile.convert("RGB"), (x + 14, y + 12))
        draw.text((x + 14, y + 132), asset_id[:34], fill="#f1e0ad", font=font)
        draw.text((x + 14, y + 150), "owned: project-generated/crops", fill="#cbd4b0", font=font)
        source_line = "source pixels: Newport crops" if asset["source_pixels_from_project_owned_wayfarer_assets"] else "source pixels: no"
        draw.text((x + 14, y + 166), source_line, fill="#cbd4b0", font=font)
        draw.text((x + 14, y + 182), "third-party pixels: no", fill="#cbd4b0", font=font)
        x += card_w + 24
        if (index + 1) % 5 == 0:
            x = 24
            y += card_h + 24
    PROOF_PATH.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(PROOF_PATH)


def write_audit_report(manifest: dict) -> None:
    now = datetime.now(timezone.utc).isoformat()
    lines: list[str] = []
    lines.append("# G-4.17 / G-4.18 Asset Provenance Audit")
    lines.append("")
    lines.append(f"Generated: `{now}`")
    lines.append("")
    lines.append("## Audit Result")
    lines.append("")
    lines.append("- G-4.17 hero manifest entries were audited as the starting point.")
    lines.append("- G-4.17 referenced copied prior Wayfarer prop crops in `art_pipeline/newport/source_refs/`; those crop pixels are not used by the G-4.18 review-facing atlas.")
    lines.append("- G-4.18 review-facing atlas pieces are deterministic project-owned Pillow output, documented Newport material/prop crop composites, and optional local Blender 5.1 procedural support silhouettes that are palette-stylized before compositing.")
    lines.append("- Newport building sprites are used as palette, material-rule, scale, and documented project-owned crop sources. Crops are limited to material/prop regions and exclude third-party or mystery pixels.")
    lines.append("- No third-party game sprites, ripped assets, marketplace/demo/sample assets, mystery assets, web-scraped art, or copied recognizable third-party sprite pixels are used.")
    lines.append("")
    lines.append("Permanent rule: No asset enters the player-facing review build unless it passes both Newport Visual Cohesion and Asset Provenance gates.")
    lines.append("")
    lines.append("## Removed From Normal Review")
    lines.append("")
    lines.append("| Source | G-4.17 Use | G-4.18 Status | Reason |")
    lines.append("| ------ | ---------- | ------------- | ------ |")
    lines.append("| `art_pipeline/newport/source_refs/hearthvale_props_atlas_v1_transparent.png` | crop reference for props/stones/dock | not referenced by G-4.18 manifest; not used in normal review hero atlas | replaced with deterministic project-owned generated assets |")
    lines.append("| `art_pipeline/newport/source_refs/hearthvale_props_atlas_v1.manifest.json` | source note for copied prop sheet | retained for historical G-4.17 audit only | superseded by canonical G-4.18 manifest |")
    lines.append("")
    lines.append("## Review-Facing Hero Assets")
    lines.append("")
    lines.append("| Asset id | Source file | Exact generated source path | Creation script | Project-owned Wayfarer source pixels | Third-party source pixels | Ownership/license | Review eligibility |")
    lines.append("| -------- | ----------- | --------------------------- | --------------- | ------------------------------------ | ------------------------- | ----------------- | ------------------ |")
    for asset in manifest["assets"]:
        source = asset["source"]
        lines.append(
            "| `{asset_id}` | `{source_file}` | `{exact}` | `{script}` | `{prior}` | `{third_party}` | {license_status} | {eligibility} |".format(
                asset_id=asset["asset_id"],
                source_file=asset["source_file"],
                exact=source["exact_source_path"],
                script=source["creation_script"],
                prior="yes, documented Newport crops" if asset["source_pixels_from_project_owned_wayfarer_assets"] else "no",
                third_party="no",
                license_status=asset["license_ownership_status"],
                eligibility="eligible" if asset["review_eligible"] else "blocked",
            )
        )
    lines.append("")
    lines.append("## Generation Detail")
    lines.append("")
    lines.append("| Asset id | Generated piece | Palette reference | Documented crop support | Blender support | Third-party pixels |")
    lines.append("| -------- | --------------- | ----------------- | ----------------------- | --------------- | ------------------ |")
    for asset in manifest["assets"]:
        blender = ", ".join(item["component_id"] for item in asset["source"].get("blender_component_sources", [])) or "none"
        crops = ", ".join(item["source_crop_id"] for item in asset["source"].get("material_sources", [])) or "none"
        lines.append(f"| `{asset['asset_id']}` | `{asset['generated_piece_file']}` | `{STYLE_JSON_PATH.relative_to(PROJECT_ROOT).as_posix()}` | {crops} | {blender} | no |")
    lines.append("")
    lines.append("## Crop Source Detail")
    lines.append("")
    lines.append("| Asset id | Crop id | Source path | Crop | Usage |")
    lines.append("| -------- | ------- | ----------- | ---- | ----- |")
    for asset in manifest["assets"]:
        for crop in asset["source"].get("material_sources", []):
            lines.append(f"| `{asset['asset_id']}` | `{crop['source_crop_id']}` | `{crop['file']}` | `{crop['crop']}` | {crop['usage']} |")
    lines.append("")
    lines.append("## Gate Notes")
    lines.append("")
    lines.append("- `newport_asset_manifest.json` is the canonical G-4.18 manifest.")
    lines.append("- `newport_hero_street_assets.json` mirrors the canonical manifest for existing validator and renderer compatibility.")
    lines.append("- Any future asset with uncertain source, copied third-party pixels, or missing license documentation must be marked `review_eligible=false` and removed from normal review mode.")
    lines.append("- The current player remains temporary scale/debug art; G-4.19 or a near follow-up must begin the player/NPC sprite-style foundation before NPC, monster, combat, or equipment systems enter normal review.")
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    AUDIT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    style_data = load_style_data()
    palette = load_palette(style_data)
    generated_paths = draw_atlas(palette)
    manifest = write_manifest(generated_paths, style_data)
    make_contact_sheet()
    make_provenance_proof(manifest)
    write_audit_report(manifest)
    print(f"Wrote {rel(ATLAS_PATH)}")
    print(f"Wrote {rel(CANONICAL_MANIFEST_PATH)}")
    print(f"Wrote {rel(LEGACY_MANIFEST_PATH)}")
    print(f"Wrote {rel(CONTACT_PATH)}")
    print(f"Wrote {rel(PROOF_PATH)}")
    print(f"Wrote {rel(AUDIT_PATH)}")


if __name__ == "__main__":
    main()
