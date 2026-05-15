#!/usr/bin/env python3
"""Generate a Newport world atlas derived from the building sprite language."""

from __future__ import annotations

import json
import random
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageOps


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[3]
PIPELINE_ROOT = PROJECT_ROOT / "art_pipeline" / "newport"
STYLE_JSON_PATH = PIPELINE_ROOT / "manifests" / "newport_building_style_values.json"
ATLAS_PATH = PIPELINE_ROOT / "atlases" / "newport_hero_street_atlas_v1.png"
MANIFEST_PATH = PIPELINE_ROOT / "manifests" / "newport_hero_street_assets.json"
CONTACT_PATH = PIPELINE_ROOT / "generated_contact_sheets" / "newport_hero_street_atlas_contact_sheet.png"
BUILDING_ROOT = PROJECT_ROOT / "assets" / "sprites" / "buildings" / "isolated"
PROP_ATLAS_PATH = PIPELINE_ROOT / "source_refs" / "hearthvale_props_atlas_v1_transparent.png"
PROP_MANIFEST_PATH = PIPELINE_ROOT / "source_refs" / "hearthvale_props_atlas_v1.manifest.json"

REGIONS = {
    "commercial_cobble_long_a": [0, 0, 320, 96],
    "curb_sidewalk_stoop_strip": [0, 96, 320, 72],
    "building_contact_shadow_strip": [0, 168, 320, 48],
    "dirt_wear_transition": [0, 216, 320, 64],
    "grass_edge_north": [0, 280, 320, 64],
    "dock_market_transition": [0, 344, 320, 96],
    "dock_pier_vertical": [0, 448, 96, 224],
    "crate_barrel_table_cluster": [336, 0, 184, 136],
    "fence_sign_market_cluster": [536, 0, 184, 136],
    "small_crate_barrel_cluster": [336, 152, 160, 112],
    "market_sign_cluster": [536, 152, 160, 112],
    "wharf_crate_pile_cluster": [336, 288, 220, 146],
    "chandlery_base_cluster": [536, 288, 220, 146],
}

SOURCE_CROPS = {
    "dockside_wharf": {
        "file": "newport_dockside_storehouse_isolated.png",
        "box": [58, 284, 364, 382],
        "usage": "front-facing dock planks, post spacing, ladder shadows, water contact",
    },
    "boathouse_wharf": {
        "file": "newport_wharf_boathouse_large_isolated.png",
        "box": [66, 270, 476, 350],
        "usage": "wharf board rhythm, pier posts, crates, stone-to-dock scale",
    },
    "boathouse_crates": {
        "file": "newport_wharf_boathouse_large_isolated.png",
        "box": [313, 252, 472, 346],
        "usage": "crate/barrel outline density and stack proportions",
    },
    "chandlery_base": {
        "file": "newport_chandlery_outfitter_front_isolated.png",
        "box": [46, 255, 404, 366],
        "usage": "shop-base prop density, rope curves, barrel color, brass highlights",
    },
    "mercantile_base": {
        "file": "mercantile_shop_isolated.png",
        "box": [54, 294, 344, 418],
        "usage": "stoop/awning shadow, crate scale, door-adjacent prop scale",
    },
    "counting_house_base": {
        "file": "newport_counting_house_civic_exchange_isolated.png",
        "box": [78, 244, 380, 333],
        "usage": "stone step scale, muted gray siding, base shadow language",
    },
    "tavern_base": {
        "file": "inn_tavern_v1_isolated.png",
        "box": [38, 332, 428, 430],
        "usage": "porch plank highlights, railing thickness, dark base contact",
    },
}

PROP_CROPS = {
    "barrel_large": [28, 37, 99, 146],
    "barrel_open": [202, 53, 281, 151],
    "crate_single": [473, 77, 553, 151],
    "crate_pair": [573, 55, 692, 157],
    "crate_stack": [711, 28, 859, 157],
    "sacks": [1014, 54, 1143, 153],
    "basket": [1153, 86, 1223, 157],
    "market_table": [25, 207, 171, 288],
    "bench": [187, 216, 302, 288],
    "signpost": [564, 176, 661, 347],
    "hanging_ship_sign": [687, 200, 814, 345],
    "notice_board": [840, 188, 986, 346],
    "street_lamp": [1014, 172, 1084, 486],
    "lantern_post": [1114, 190, 1206, 408],
    "well": [41, 303, 190, 507],
    "fence_plain": [377, 368, 541, 466],
    "fence_gate": [724, 369, 927, 471],
    "fence_low": [556, 370, 711, 467],
    "dock_long": [230, 513, 453, 634],
    "dock_square": [497, 513, 671, 634],
    "rope_coil": [1104, 558, 1190, 617],
    "fish_table": [39, 653, 262, 772],
    "basket_table": [299, 640, 436, 770],
    "apple_basket": [465, 665, 561, 768],
    "green_basket": [590, 671, 672, 769],
    "vegetable_crate": [695, 665, 829, 768],
    "woodpile": [845, 663, 974, 765],
    "water_trough": [1003, 681, 1225, 772],
    "stone_patch_a": [101, 922, 190, 968],
    "stone_patch_b": [221, 922, 293, 989],
    "stone_patch_c": [321, 924, 404, 987],
    "water_edge_stone": [29, 1126, 138, 1220],
    "post_with_gull": [735, 1126, 791, 1221],
    "black_lantern": [896, 1123, 945, 1221],
    "black_lamp": [817, 1128, 868, 1221],
}


def rel(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def rgba(hex_color: str, alpha: int = 255) -> tuple[int, int, int, int]:
    value = hex_color.strip("#")
    return (int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16), alpha)


def load_style_palette() -> dict[str, list[str]]:
    fallback = {
        "dark": ["#1b1711", "#241f18", "#302719", "#353025"],
        "shadow": ["#3d3528", "#4b4434", "#514432", "#263328"],
        "mid": ["#5f594c", "#756d5a", "#806b4d", "#6f5b41", "#5b7251"],
        "highlight": ["#c7ad72", "#d5c28c", "#b9aa80", "#e0c58b"],
    }
    if not STYLE_JSON_PATH.exists():
        return fallback
    data = json.loads(STYLE_JSON_PATH.read_text(encoding="utf-8"))
    return {
        "dark": [item["hex"] for item in data.get("outline_dark_edge_samples", [])[:5]] or fallback["dark"],
        "shadow": [item["hex"] for item in data.get("common_shadow_colors", [])[:6]] or fallback["shadow"],
        "mid": [item["hex"] for item in data.get("midtone_material_colors", [])[:7]] or fallback["mid"],
        "highlight": [item["hex"] for item in data.get("highlight_colors", [])[:5]] or fallback["highlight"],
    }


def region_box(region_id: str) -> tuple[int, int, int, int]:
    x, y, w, h = REGIONS[region_id]
    return (x, y, x + w, y + h)


def crop_source(crop_id: str) -> Image.Image:
    crop = SOURCE_CROPS[crop_id]
    return Image.open(BUILDING_ROOT / crop["file"]).convert("RGBA").crop(tuple(crop["box"]))


def crop_prop(crop_id: str) -> Image.Image:
    return Image.open(PROP_ATLAS_PATH).convert("RGBA").crop(tuple(PROP_CROPS[crop_id]))


def fit_crop(crop_id: str, size: tuple[int, int], opacity: int = 255, contrast: float = 1.0) -> Image.Image:
    image = ImageOps.fit(crop_source(crop_id), size, method=Image.Resampling.LANCZOS)
    if contrast != 1.0:
        image = ImageEnhance.Contrast(image).enhance(contrast)
    if opacity < 255:
        alpha = image.getchannel("A").point(lambda value: value * opacity // 255)
        image.putalpha(alpha)
    return image


def fit_prop(crop_id: str, size: tuple[int, int], opacity: int = 255, contrast: float = 1.0) -> Image.Image:
    image = ImageOps.contain(crop_prop(crop_id), size, method=Image.Resampling.LANCZOS)
    if contrast != 1.0:
        image = ImageEnhance.Contrast(image).enhance(contrast)
    if opacity < 255:
        alpha = image.getchannel("A").point(lambda value: value * opacity // 255)
        image.putalpha(alpha)
    return image


def paste_prop(tile: Image.Image, draw: ImageDraw.ImageDraw, crop_id: str, xy: tuple[int, int], size: tuple[int, int], opacity: int = 255) -> None:
    prop = fit_prop(crop_id, size, opacity=opacity, contrast=1.05)
    tile.alpha_composite(prop, xy)


def stamp_source_texture(base: Image.Image, crop_id: str, opacity: int, contrast: float = 0.8) -> None:
    texture = fit_crop(crop_id, base.size, opacity=opacity, contrast=contrast)
    base.alpha_composite(texture)


def draw_line_noise(draw: ImageDraw.ImageDraw, bounds: tuple[int, int, int, int], seed: int, colors: list[str], count: int) -> None:
    rng = random.Random(seed)
    x0, y0, x1, y1 = bounds
    for _ in range(count):
        x = rng.randint(x0 + 2, x1 - 10)
        y = rng.randint(y0 + 2, y1 - 4)
        length = rng.randint(6, 32)
        color = rgba(rng.choice(colors), rng.randint(36, 100))
        draw.line((x, y, min(x1 - 2, x + length), y + rng.choice([-1, 0, 0, 1])), fill=color, width=1)


def draw_stone_paver_tile(tile: Image.Image, palette: dict[str, list[str]]) -> None:
    draw = ImageDraw.Draw(tile)
    rng = random.Random(417171)
    w, h = tile.size
    draw.rectangle((0, 0, w, h), fill=rgba("#5b5548"))
    stamp_source_texture(tile, "counting_house_base", 38, 0.7)
    tile.alpha_composite(fit_prop("stone_patch_a", (140, 58), opacity=78, contrast=0.9), (18, 18))
    tile.alpha_composite(fit_prop("stone_patch_b", (120, 56), opacity=70, contrast=0.9), (176, 24))
    y = 5
    row = 0
    while y < h - 4:
        block_h = rng.randint(10, 16)
        x = -rng.randint(10, 34) + (row % 2) * rng.randint(8, 18)
        while x < w:
            block_w = rng.randint(22, 52)
            skew = rng.randint(-3, 3)
            x2 = x + block_w
            y2 = min(h - 3, y + block_h)
            fill = rng.choice(["#625b4d", "#6d6655", "#716852", "#514c40", "#77705d"])
            polygon = [(x, y + 1), (x2, y + skew), (x2 - 2, y2), (x + 1, y2 - skew)]
            draw.polygon(polygon, fill=rgba(fill, rng.randint(210, 245)))
            draw.line((x + 1, y + 1, x2 - 3, y + skew), fill=rgba(rng.choice(palette["highlight"]), 70), width=1)
            draw.line((x + 1, y2 - 1, x2 - 2, y2), fill=rgba(rng.choice(palette["dark"]), 120), width=1)
            draw.line((x, y + 2, x + 1, y2 - 2), fill=rgba("#19140e", 88), width=1)
            chip_min = max(0, x + 4)
            chip_max = min(w - 2, x2 - 4)
            if rng.random() < 0.38 and chip_min <= chip_max:
                cx = rng.randint(chip_min, chip_max)
                cy = rng.randint(y + 3, max(y + 3, y2 - 3))
                draw.line((cx, cy, cx + rng.randint(4, 13), cy + rng.choice([-1, 0, 1])), fill=rgba("#211b14", 100), width=1)
            x += block_w - rng.randint(1, 5)
        y += block_h - rng.randint(0, 3)
        row += 1
    draw_line_noise(draw, (0, 0, w, h), 417172, palette["dark"] + palette["highlight"], 90)
    draw.rectangle((0, 0, w - 1, h - 1), outline=rgba("#18130e", 135), width=2)


def draw_sidewalk_tile(tile: Image.Image, palette: dict[str, list[str]]) -> None:
    draw = ImageDraw.Draw(tile)
    w, h = tile.size
    draw.rectangle((0, 0, w, h), fill=rgba("#696151"))
    stamp_source_texture(tile, "tavern_base", 18, 0.78)
    draw.rectangle((0, 0, w, 9), fill=rgba("#b9aa80", 105))
    draw.rectangle((0, 9, w, 14), fill=rgba("#2a2218", 145))
    draw.rectangle((0, h - 12, w, h), fill=rgba("#252017", 165))
    for x in range(-28, w + 18, 54):
        draw.line((x, 16, x - 10, h - 14), fill=rgba("#1d1811", 92), width=1)
        draw.line((x + 2, 17, x + 28, 16), fill=rgba(rng_choice(palette["highlight"], x), 62), width=1)
    for y in range(24, h - 16, 15):
        draw.line((6, y, w - 10, y - 1), fill=rgba("#201a13", 70), width=1)
    for x in [36, 132, 228]:
        draw.rectangle((x, 0, x + 48, 22), fill=rgba("#8b7658", 245))
        draw.rectangle((x, 0, x + 48, 22), outline=rgba("#22180f", 190), width=2)
        draw.line((x + 6, 5, x + 41, 3), fill=rgba("#d3b879", 90), width=1)
        draw.line((x + 5, 17, x + 42, 16), fill=rgba("#2a1e14", 95), width=1)
    draw_line_noise(draw, (0, 14, w, h - 12), 417173, palette["dark"] + palette["highlight"], 46)


def draw_shadow_tile(tile: Image.Image) -> None:
    draw = ImageDraw.Draw(tile)
    w, h = tile.size
    for y in range(h):
        alpha = max(0, int(150 * (1.0 - y / max(1, h))))
        draw.line((0, y, w, y), fill=rgba("#15110c", alpha), width=1)
    for x in range(18, w - 18, 38):
        draw.ellipse((x, h - 19, x + 36, h - 5), fill=rgba("#0c0906", 65))
        draw.rectangle((x + 8, h - 18, x + 28, h - 13), fill=rgba("#514432", 70))


def draw_dirt_tile(tile: Image.Image, palette: dict[str, list[str]]) -> None:
    draw = ImageDraw.Draw(tile)
    rng = random.Random(417174)
    w, h = tile.size
    draw.rectangle((0, 0, w, h), fill=rgba("#745f42"))
    for _ in range(120):
        x = rng.randint(0, w - 6)
        y = rng.randint(2, h - 5)
        length = rng.randint(5, 36)
        color = rng.choice(["#3a2c1d", "#5d4931", "#94764e", "#b18c5a", "#211811"])
        draw.rectangle((x, y, min(w - 1, x + length), y + rng.randint(1, 4)), fill=rgba(color, rng.randint(70, 160)))
    for _ in range(36):
        x = rng.randint(4, w - 8)
        y = rng.randint(4, h - 8)
        draw.ellipse((x, y, x + 3, y + 2), fill=rgba(rng.choice(palette["dark"]), 120))
    draw.line((0, 3, w, 1), fill=rgba("#d5c28c", 72), width=1)
    draw.line((0, h - 5, w, h - 8), fill=rgba("#1c140d", 135), width=2)


def draw_grass_tile(tile: Image.Image, palette: dict[str, list[str]]) -> None:
    draw = ImageDraw.Draw(tile)
    rng = random.Random(417175)
    w, h = tile.size
    draw.rectangle((0, 0, w, h), fill=rgba("#526b4a"))
    for _ in range(140):
        x = rng.randint(0, w - 8)
        y = rng.randint(1, h - 5)
        color = rng.choice(["#2c4530", "#3e5b3c", "#6f875a", "#82945c", "#253d2b"])
        draw.line((x, y, min(w - 1, x + rng.randint(4, 20)), y + rng.choice([-2, -1, 0, 1])), fill=rgba(color, rng.randint(55, 145)), width=1)
    draw.line((0, h - 9, w, h - 6), fill=rgba("#263f2a", 155), width=2)
    draw.line((0, h - 3, w, h - 2), fill=rgba("#b9aa80", 72), width=1)


def draw_dock_tile(tile: Image.Image, palette: dict[str, list[str]]) -> None:
	draw = ImageDraw.Draw(tile)
	rng = random.Random(417177)
	w, h = tile.size
	draw.rectangle((0, 0, w, h), fill=rgba("#5a4228"))
	tile.alpha_composite(fit_crop("dockside_wharf", (w, h), opacity=28, contrast=0.82))
	tile.alpha_composite(fit_crop("boathouse_wharf", (w, h), opacity=24, contrast=0.88))
	y = 0
	row = 0
	while y < h:
		board_h = rng.randint(10, 15)
		base = rng.choice(["#60472c", "#6a5030", "#715636", "#563d25", "#775a37"])
		draw.rectangle((0, y, w, min(h, y + board_h)), fill=rgba(base, rng.randint(218, 248)))
		draw.line((0, y, w, y - 1), fill=rgba("#d2ae72", 66), width=1)
		draw.line((0, min(h - 1, y + board_h), w, min(h - 1, y + board_h)), fill=rgba("#160f09", 128), width=1)
		x = -rng.randint(6, 42) + (row % 2) * 18
		while x < w:
			seam_x = x + rng.randint(28, 62)
			draw.line((seam_x, y + 2, seam_x - rng.randint(-2, 3), min(h - 2, y + board_h - 2)), fill=rgba("#1b120a", 104), width=1)
			if rng.random() < 0.42:
				draw.point((seam_x - 4, y + rng.randint(3, max(3, board_h - 3))), fill=rgba("#100b07", 150))
				draw.point((seam_x + 5, y + rng.randint(3, max(3, board_h - 3))), fill=rgba("#c39a5a", 80))
			x += rng.randint(46, 74)
		y += board_h
		row += 1
	for x in range(30, w, 78):
		draw.rectangle((x - 3, 8, x + 4, h - 10), fill=rgba("#372313", 106))
		draw.line((x - 2, 10, x + 3, h - 12), fill=rgba("#c59f61", 42), width=1)
	for _ in range(48):
		x = rng.randint(2, w - 10)
		y = rng.randint(5, h - 8)
		draw.line((x, y, min(w - 2, x + rng.randint(6, 28)), y + rng.choice([-1, 0, 1])), fill=rgba(rng.choice(["#24180d", "#c8a160", "#8a6840"]), rng.randint(42, 94)), width=1)
	draw.rectangle((0, 0, w, 5), fill=rgba("#1b120a", 154))
	draw.line((0, 5, w, 3), fill=rgba("#d7b978", 78), width=1)
	draw.rectangle((0, h - 12, w, h), fill=rgba("#24170d", 176))
	draw.rectangle((0, 0, w - 1, h - 1), outline=rgba("#130e09", 170), width=2)


def draw_vertical_pier_tile(tile: Image.Image, palette: dict[str, list[str]]) -> None:
	draw = ImageDraw.Draw(tile)
	w, h = tile.size
	rng = random.Random(417178)
	draw.rectangle((0, 0, w, h), fill=rgba("#553c24"))
	tile.alpha_composite(fit_prop("dock_square", (96, 82), opacity=42, contrast=0.9), (0, 5))
	for x in range(5, w - 2, 15):
		fill = rng.choice(["#725533", "#65492b", "#7b5d38", "#563c24"])
		draw.rectangle((x, 0, min(w - 1, x + 11), h), fill=rgba(fill, 236))
		draw.line((x + 2, 5, x + 8, h - 6), fill=rgba("#d2ad72", 56), width=1)
		draw.line((x + 11, 0, x + 11, h), fill=rgba("#150e08", 132), width=1)
		for y in range(22, h, 52):
			draw.point((x + 3, y), fill=rgba("#100b07", 150))
	for y in range(26, h, 56):
		draw.rectangle((0, y, w, y + 9), fill=rgba("#2b1b0f", 164))
		draw.line((0, y + 1, w, y), fill=rgba("#cba766", 58), width=1)
	draw.rectangle((0, 0, w - 1, h - 1), outline=rgba("#120c08", 170), width=2)


def rng_choice(values: list[str], seed: int) -> str:
    return random.Random(seed).choice(values)


def draw_contact_shadow(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], alpha: int = 90) -> None:
    x0, y0, x1, y1 = box
    draw.ellipse((x0, y1 - 22, x1, y1 - 2), fill=rgba("#0c0906", alpha))


def draw_newport_crate(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, color: str) -> None:
    draw.rectangle((x + 2, y + 3, x + w + 2, y + h + 3), fill=rgba("#0d0905", 92))
    draw.rectangle((x, y, x + w, y + h), fill=rgba(color))
    draw.rectangle((x, y, x + w, y + h), outline=rgba("#1b120a"), width=2)
    draw.line((x + 4, y + 5, x + w - 4, y + h - 5), fill=rgba("#2c1a0e", 185), width=2)
    draw.line((x + 4, y + h - 6, x + w - 5, y + 4), fill=rgba("#c69151", 120), width=1)
    for yy in [y + 6, y + h - 7]:
        draw.line((x + 4, yy, x + w - 5, yy - 1), fill=rgba("#d2a165", 100), width=1)
    draw.line((x + w - 2, y + 2, x + w - 2, y + h - 2), fill=rgba("#0e0905", 120), width=1)


def draw_newport_barrel(draw: ImageDraw.ImageDraw, x: int, y: int, scale: float = 1.0) -> None:
    rx = int(9 * scale)
    ry = int(15 * scale)
    draw.ellipse((x - rx + 2, y - ry + 3, x + rx + 2, y + ry + 3), fill=rgba("#0a0704", 75))
    draw.ellipse((x - rx, y - ry, x + rx, y + ry), fill=rgba("#7f5530"), outline=rgba("#1b120a"), width=2)
    draw.rectangle((x - rx + 1, y - int(5 * scale), x + rx - 1, y - int(2 * scale)), fill=rgba("#2a1c10"))
    draw.rectangle((x - rx + 1, y + int(5 * scale), x + rx - 1, y + int(8 * scale)), fill=rgba("#2a1c10"))
    draw.arc((x - rx + 2, y - ry + 2, x + rx - 2, y + ry - 2), 85, 275, fill=rgba("#c49a5c"), width=1)
    draw.line((x - 2, y - ry + 4, x - 4, y + ry - 5), fill=rgba("#2a1c10", 130), width=1)


def draw_rope_coil(draw: ImageDraw.ImageDraw, x: int, y: int, r: int) -> None:
    draw.ellipse((x - r + 4, y - r + 5, x + r + 4, y + r + 5), outline=rgba("#0d0905", 82), width=3)
    for inset in [0, 6, 11]:
        draw.arc((x - r + inset, y - r + inset, x + r - inset, y + r - inset), 5, 352, fill=rgba("#cdb774"), width=2)
    draw.arc((x - r + 3, y - r + 4, x + r - 3, y + r - 3), 40, 210, fill=rgba("#6f5935"), width=1)


def draw_market_table(draw: ImageDraw.ImageDraw, x: int, y: int, w: int) -> None:
    draw.rectangle((x + 4, y + 18, x + w + 4, y + 24), fill=rgba("#0d0905", 85))
    draw.rectangle((x, y, x + w, y + 21), fill=rgba("#7c5935"))
    draw.rectangle((x, y, x + w, y + 21), outline=rgba("#1b120a"), width=2)
    for line_y in [y + 5, y + 11, y + 17]:
        draw.line((x + 4, line_y, x + w - 4, line_y - 1), fill=rgba("#2c1a0e", 120), width=1)
    for i, color in enumerate(["#d9c37a", "#a95e45", "#d9c37a", "#b08246", "#d9c37a", "#c39b58"]):
        cx = x + 18 + i * 13
        draw.ellipse((cx - 5, y + 7, cx + 5, y + 17), fill=rgba(color), outline=rgba("#1b120a", 130))
    draw.rectangle((x + 8, y + 22, x + 13, y + 49), fill=rgba("#3a2716"))
    draw.rectangle((x + w - 13, y + 22, x + w - 8, y + 49), fill=rgba("#3a2716"))


def draw_prop_cluster(tile: Image.Image, variant: str) -> None:
    draw = ImageDraw.Draw(tile)
    w, h = tile.size
    draw_contact_shadow(draw, (8, 32, w - 8, h - 4), 82)
    if variant == "market":
        paste_prop(tile, draw, "fish_table", (4, 18), (112, 62))
        paste_prop(tile, draw, "basket_table", (76, 38), (82, 72))
        paste_prop(tile, draw, "barrel_open", (128, 48), (40, 54))
        paste_prop(tile, draw, "rope_coil", (116, 83), (46, 26))
    elif variant == "fence":
        paste_prop(tile, draw, "fence_gate", (0, 45), (118, 62))
        paste_prop(tile, draw, "hanging_ship_sign", (80, 6), (74, 86))
        paste_prop(tile, draw, "crate_single", (128, 78), (44, 42))
    elif variant == "crates":
        paste_prop(tile, draw, "crate_stack", (0, 10), (82, 72))
        paste_prop(tile, draw, "barrel_large", (70, 28), (52, 70))
        paste_prop(tile, draw, "sacks", (106, 22), (48, 48))
        paste_prop(tile, draw, "rope_coil", (96, 84), (48, 28))
    elif variant == "wharf":
        draw.rectangle((6, h - 42, w - 8, h - 24), fill=rgba("#0d0905", 58))
        for x in range(10, w - 18, 34):
            draw.line((x, h - 38, x + 22, h - 40), fill=rgba("#d0aa69", 44), width=1)
            draw.line((x, h - 29, x + 24, h - 31), fill=rgba("#171008", 82), width=1)
        paste_prop(tile, draw, "crate_stack", (8, 18), (92, 76))
        paste_prop(tile, draw, "woodpile", (84, 38), (82, 66))
        paste_prop(tile, draw, "barrel_large", (156, 44), (50, 70))
        paste_prop(tile, draw, "rope_coil", (170, 94), (44, 26))
    elif variant == "chandlery":
        draw.rectangle((8, h - 40, w - 8, h - 22), fill=rgba("#0d0905", 58))
        for x in range(12, w - 18, 38):
            draw.line((x, h - 36, x + 26, h - 37), fill=rgba("#d0aa69", 40), width=1)
            draw.line((x, h - 28, x + 28, h - 29), fill=rgba("#171008", 76), width=1)
        paste_prop(tile, draw, "notice_board", (6, 8), (76, 78))
        paste_prop(tile, draw, "vegetable_crate", (78, 36), (70, 54))
        paste_prop(tile, draw, "barrel_large", (150, 42), (50, 72))
        paste_prop(tile, draw, "black_lantern", (190, 58), (28, 56))


def draw_atlas() -> None:
    palette = load_style_palette()
    atlas = Image.new("RGBA", (768, 768), (0, 0, 0, 0))
    tile_drawers = {
        "commercial_cobble_long_a": lambda tile: draw_stone_paver_tile(tile, palette),
        "curb_sidewalk_stoop_strip": lambda tile: draw_sidewalk_tile(tile, palette),
        "building_contact_shadow_strip": draw_shadow_tile,
        "dirt_wear_transition": lambda tile: draw_dirt_tile(tile, palette),
        "grass_edge_north": lambda tile: draw_grass_tile(tile, palette),
        "dock_market_transition": lambda tile: draw_dock_tile(tile, palette),
        "dock_pier_vertical": lambda tile: draw_vertical_pier_tile(tile, palette),
    }
    prop_variants = {
        "crate_barrel_table_cluster": "market",
        "fence_sign_market_cluster": "fence",
        "small_crate_barrel_cluster": "crates",
        "market_sign_cluster": "fence",
        "wharf_crate_pile_cluster": "wharf",
        "chandlery_base_cluster": "chandlery",
    }
    for asset_id, region in REGIONS.items():
        tile = Image.new("RGBA", (region[2], region[3]), (0, 0, 0, 0))
        if asset_id in tile_drawers:
            tile_drawers[asset_id](tile)
        else:
            draw_prop_cluster(tile, prop_variants[asset_id])
        atlas.alpha_composite(tile, (region[0], region[1]))
    ATLAS_PATH.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(ATLAS_PATH)


def material_sources_for(asset_id: str) -> list[dict[str, object]]:
    mapping = {
        "commercial_cobble_long_a": ["counting_house_base", "tavern_base"],
        "curb_sidewalk_stoop_strip": ["tavern_base", "mercantile_base", "counting_house_base"],
        "building_contact_shadow_strip": ["counting_house_base", "chandlery_base"],
        "dirt_wear_transition": ["mercantile_base"],
        "grass_edge_north": ["tavern_base"],
        "dock_market_transition": ["dockside_wharf", "boathouse_wharf"],
        "dock_pier_vertical": ["dockside_wharf", "boathouse_wharf"],
        "crate_barrel_table_cluster": ["chandlery_base", "mercantile_base"],
        "fence_sign_market_cluster": ["tavern_base"],
        "small_crate_barrel_cluster": ["boathouse_crates"],
        "market_sign_cluster": ["tavern_base"],
        "wharf_crate_pile_cluster": ["boathouse_crates", "dockside_wharf"],
        "chandlery_base_cluster": ["chandlery_base"],
    }
    sources = []
    for crop_id in mapping[asset_id]:
        crop = SOURCE_CROPS[crop_id]
        sources.append(
            {
                "source_crop_id": crop_id,
                "file": f"assets/sprites/buildings/isolated/{crop['file']}",
                "crop": crop["box"],
                "usage": crop["usage"],
            }
        )
    return sources


def prop_sources_for(asset_id: str) -> list[dict[str, object]]:
    mapping = {
        "commercial_cobble_long_a": ["stone_patch_a", "stone_patch_b"],
        "dock_market_transition": ["dock_long", "dock_square"],
        "dock_pier_vertical": ["dock_square"],
        "crate_barrel_table_cluster": ["fish_table", "basket_table", "barrel_open", "rope_coil"],
        "fence_sign_market_cluster": ["fence_gate", "hanging_ship_sign", "crate_single"],
        "small_crate_barrel_cluster": ["crate_stack", "barrel_large", "sacks", "rope_coil"],
        "market_sign_cluster": ["fence_gate", "hanging_ship_sign", "crate_single"],
        "wharf_crate_pile_cluster": ["crate_stack", "woodpile", "barrel_large", "rope_coil"],
        "chandlery_base_cluster": ["notice_board", "vegetable_crate", "barrel_large", "black_lantern"],
    }
    sources = []
    for crop_id in mapping.get(asset_id, []):
        sources.append(
            {
                "source_crop_id": crop_id,
                "file": rel(PROP_ATLAS_PATH),
                "original_file": "wayfarer_v7_github_ready/worker/assets/wayfarer/props/hearthvale_props_atlas_v1_transparent.png",
                "crop": PROP_CROPS[crop_id],
                "usage": "prior project project-owned prop sprite incorporated as Newport source reference",
            }
        )
    return sources


def write_manifest() -> None:
    category = {
        "commercial_cobble_long_a": "commercial street/cobble",
        "curb_sidewalk_stoop_strip": "curb/sidewalk/stoop",
        "building_contact_shadow_strip": "building contact-shadow/base",
        "dirt_wear_transition": "dirt/wear transition",
        "grass_edge_north": "grass edge",
        "dock_market_transition": "dock/market transition",
        "dock_pier_vertical": "dock/pier transition",
        "crate_barrel_table_cluster": "crate/barrel/table prop cluster",
        "fence_sign_market_cluster": "fence/sign/market object cluster",
        "small_crate_barrel_cluster": "crate/barrel prop cluster",
        "market_sign_cluster": "fence/sign/market object cluster",
        "wharf_crate_pile_cluster": "crate/barrel/rope wharf cluster",
        "chandlery_base_cluster": "shop-base prop cluster",
    }
    assets = []
    for asset_id, region in REGIONS.items():
        is_prop = "cluster" in asset_id
        source = {
            "type": "project_owned_derived_bitmap",
            "created_by": "art_pipeline/newport/scripts/generate_hero_street_atlas.py",
            "ownership": "project-owned",
            "license": "Wayfarer project asset; no external scraped art",
            "material_sources": material_sources_for(asset_id),
            "prior_project_prop_sources": prop_sources_for(asset_id),
            "source_manifest": rel(PROP_MANIFEST_PATH) if PROP_MANIFEST_PATH.exists() else "",
            "notes": "Generated from in-repository Newport building sprite material crops, project-owned prior prop sprite crops, and deterministic mark-making; no web or third-party art inputs.",
        }
        assets.append(
            {
                "asset_id": asset_id,
                "material_category": category[asset_id],
                "source_file": rel(ATLAS_PATH),
                "source": source,
                "atlas_region": {"x": region[0], "y": region[1], "w": region[2], "h": region[3]},
                "intended_scale": "1 atlas pixel maps to approximately 1 world pixel; source crop scale is anchored to Newport doors, stoops, barrels, and wharf posts.",
                "collision_behavior": "none; decorative/grounding only" if not is_prop else "decorative blocker only if a future collision rect is authored separately",
                "y_sort_behavior": "drawn on map layer below buildings; props are seated in front-of-building or wharf bands but remain non-interactive",
                "contact_shadow_required": True,
                "visual_cohesion_status": "g417_review_candidate",
                "placeholder": False,
                "final": False,
                "review_eligible": True,
                "review_notes": "Derived from the building sprite material standard: dark outlines, dense internal texture, muted Newport palette, contact shadows, and door/window scale references.",
            }
        )

    manifest = {
        "schema_id": "wayfarer.newport.asset_manifest.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "atlas": rel(ATLAS_PATH),
        "assets": assets,
        "source_policy": "Building sprites define the visual standard; atlas assets must name the project-owned source crops they derive from.",
        "review_gate": "Assets with placeholder=false and review_eligible=true must satisfy NEWPORT_ART_BIBLE.md.",
    }
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def make_contact_sheet() -> None:
    atlas = Image.open(ATLAS_PATH).convert("RGBA")
    sheet = Image.new("RGBA", (1120, 760), rgba("#20261e"))
    sheet.alpha_composite(atlas, (20, 20))
    draw = ImageDraw.Draw(sheet)
    draw.rectangle((20, 20, 788, 788), outline=rgba("#f1e0ad"), width=2)
    for index, (asset_id, region) in enumerate(REGIONS.items()):
        x, y, w, h = region
        ox, oy = 20 + x, 20 + y
        draw.rectangle((ox, oy, ox + w, oy + h), outline=rgba("#f1e0ad", 150), width=1)
        label_y = 32 + index * 50
        draw.text((820, label_y), f"{asset_id}: {region}", fill=rgba("#f1e0ad"))
    CONTACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    sheet.convert("RGB").save(CONTACT_PATH)


def main() -> None:
    draw_atlas()
    write_manifest()
    make_contact_sheet()
    print(f"Wrote {rel(ATLAS_PATH)}")
    print(f"Wrote {rel(MANIFEST_PATH)}")
    print(f"Wrote {rel(CONTACT_PATH)}")


if __name__ == "__main__":
    main()
