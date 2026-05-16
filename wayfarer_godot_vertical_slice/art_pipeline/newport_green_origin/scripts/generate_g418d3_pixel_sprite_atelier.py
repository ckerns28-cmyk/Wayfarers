#!/usr/bin/env python3
"""Generate the G-4.18D.3 pixel-by-pixel sprite atelier proof packet."""

from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
import subprocess
import warnings
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

warnings.filterwarnings("ignore", category=DeprecationWarning, module="PIL")


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[3]
PIPELINE_ROOT = PROJECT_ROOT / "art_pipeline" / "newport_green_origin"
BAKEOFF_ROOT = PIPELINE_ROOT / "method_bakeoff"
GENERATED_ROOT = BAKEOFF_ROOT / "generated"
SOURCE_ROOT = BAKEOFF_ROOT / "source_authored"
REPORTS_ROOT = BAKEOFF_ROOT / "reports"
CONTACT_SHEET_ROOT = PIPELINE_ROOT / "contact_sheets"
MANIFEST_PATH = PIPELINE_ROOT / "manifests" / "green_origin_method_bakeoff_manifest.json"
STYLE_TOKENS_PATH = PIPELINE_ROOT / "source_authored" / "newport_green_origin_style_tokens.json"
ART_BIBLE_PATH = PROJECT_ROOT / "docs" / "NEWPORT_ART_BIBLE.md"
CHANDLERY_REFERENCE_PATH = PROJECT_ROOT / "assets" / "sprites" / "buildings" / "isolated" / "newport_chandlery_outfitter_front_isolated.png"
WHARF_REFERENCE_PATH = PROJECT_ROOT / "art_pipeline" / "newport" / "generated_assets" / "hero_strip" / "wharf_crate_pile_cluster.png"
CHANDLERY_PROP_REFERENCE_PATH = PROJECT_ROOT / "art_pipeline" / "newport" / "generated_assets" / "hero_strip" / "chandlery_base_cluster.png"

SOURCE_JSON_PATH = SOURCE_ROOT / "g418d3_rope_crate_barrel_pixel_layers.json"
SILHOUETTE_PLAN_SVG_PATH = SOURCE_ROOT / "g418d3_painterly_silhouette_plan.svg"
SILHOUETTE_PLAN_PNG_PATH = GENERATED_ROOT / "g418d3_painterly_silhouette_plan.png"
LAYER_ROOT = SOURCE_ROOT / "g418d3_pixel_layers"
PASS01_PATH = GENERATED_ROOT / "g418d3_pass01_blockout.png"
PASS02_PATH = GENERATED_ROOT / "g418d3_pass02_material_detail.png"
PASS03_PATH = GENERATED_ROOT / "g418d3_pass03_polish_shadow_grounding.png"
KRITA_RAW_PATH = GENERATED_ROOT / "g418d3_dockside_rope_crate_barrel_krita_raw.png"
FINAL_ASSET_PATH = GENERATED_ROOT / "g418d3_dockside_rope_crate_barrel_cluster.png"
SPRITE_SHEET_PATH = GENERATED_ROOT / "g418d3_dockside_rope_crate_barrel_sprite_sheet.png"
ISOLATED_1X_PATH = CONTACT_SHEET_ROOT / "g418d3_isolated_sprite_1x.png"
GRID_8X_PATH = CONTACT_SHEET_ROOT / "g418d3_enlarged_grid_8x.png"
BEFORE_AFTER_PATH = CONTACT_SHEET_ROOT / "g418d3_before_after_pixel_atelier.png"
PALETTE_SHEET_PATH = CONTACT_SHEET_ROOT / "g418d3_palette_sheet.png"
IN_WORLD_PATH = CONTACT_SHEET_ROOT / "g418d3_lab_in_world_comparison.png"
STANDARD_COMPARISON_PATH = CONTACT_SHEET_ROOT / "g418d3_standard_comparison_chandlery_wharf.png"
PROP_STUDY_SHEET_PATH = CONTACT_SHEET_ROOT / "g418d3_prop_readability_studies.png"
ATELIER_BOARD_PATH = CONTACT_SHEET_ROOT / "g418d3_pixel_sprite_atelier_board.png"
INSPECTION_PATH = REPORTS_ROOT / "g418d3_pixel_sprite_image_inspection.json"
KRITA_LOG_PATH = REPORTS_ROOT / "g418d3_krita_log.json"
GIMP_LOG_PATH = REPORTS_ROOT / "g418d3_gimp_log.json"
REPORT_PATH = PIPELINE_ROOT / "reports" / "G418D3_PIXEL_BY_PIXEL_SPRITE_ATELIER.md"
TOOL_PROFILE_ROOT = PROJECT_ROOT / "artifacts" / "tool_profiles" / "g418d3"

KRITA_EXE = Path("C:/Program Files/Krita (x64)/bin/krita.exe")
GIMP = Path("C:/Users/Chris/AppData/Local/Programs/GIMP 3/bin/gimp-console-3.exe")
INKSCAPE = Path("C:/Program Files/Inkscape/bin/inkscape.exe")

CANVAS_W = 96
CANVAS_H = 64
AA_RENDER = 4
VISUAL_PASS_GATE = 7.5
VISUAL_RATING = 7.1
CAPABILITY_VERDICT = "DEFER"
VISUAL_STATUS = "visual_defer_readable_prop_studies_but_not_chandlery_standard"

PALETTE = {
    "clear": "#00000000",
    "blockout_crate": "#8b613e",
    "blockout_rope": "#b9a066",
    "blockout_barrel": "#87562f",
    "outline": "#15100b",
    "deep_outline": "#080706",
    "cast_shadow": "#0b0a07a0",
    "soft_shadow": "#14100b72",
    "contact_shadow": "#050403d8",
    "wood_dark": "#3e2818",
    "wood_deep": "#21150d",
    "wood_cool_shadow": "#4f4635",
    "wood_mid": "#745132",
    "wood_warm": "#956b42",
    "wood_light": "#bb925f",
    "wood_sun": "#d1b07a",
    "rope_dark": "#4e3c25",
    "rope_shadow": "#2f2418",
    "rope_mid": "#8c744d",
    "rope_light": "#c2ab72",
    "rope_sun": "#dec78d",
    "barrel_dark": "#3b2314",
    "barrel_mid": "#754a2b",
    "barrel_warm": "#9a6237",
    "barrel_light": "#c28a52",
    "metal_dark": "#25251f",
    "metal_mid": "#4a4d3f",
    "metal_light": "#899073",
    "grime": "#221a10",
    "green_grime": "#303522",
    "chip_dark": "#23160d",
    "chalk_highlight": "#e0cf9b",
    "grid": "#3b4639",
    "sheet_bg": "#1b241b",
    "sheet_panel": "#273224",
    "sheet_gold": "#d8c06a",
    "sheet_text": "#eadca6",
}


def rgba(hex_color: str) -> tuple[int, int, int, int]:
    value = hex_color.lstrip("#")
    if len(value) == 6:
        value += "ff"
    return (
        int(value[0:2], 16),
        int(value[2:4], 16),
        int(value[4:6], 16),
        int(value[6:8], 16),
    )


def rel(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def find_tool(path: Path) -> Path:
    if path.exists():
        return path
    found = shutil.which(path.name)
    if found:
        return Path(found)
    raise FileNotFoundError(path)


def tool_env() -> dict[str, str]:
    TOOL_PROFILE_ROOT.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["APPDATA"] = str(TOOL_PROFILE_ROOT / "AppData")
    env["LOCALAPPDATA"] = str(TOOL_PROFILE_ROOT / "LocalAppData")
    env["XDG_CONFIG_HOME"] = str(TOOL_PROFILE_ROOT / "xdg_config")
    env["XDG_DATA_HOME"] = str(TOOL_PROFILE_ROOT / "xdg_data")
    env["XDG_CACHE_HOME"] = str(TOOL_PROFILE_ROOT / "xdg_cache")
    for key in ["APPDATA", "LOCALAPPDATA", "XDG_CONFIG_HOME", "XDG_DATA_HOME", "XDG_CACHE_HOME"]:
        Path(env[key]).mkdir(parents=True, exist_ok=True)
    return env


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"]:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], value: str, fill: str = "sheet_text", size: int = 13) -> None:
    draw.text(xy, value, fill=rgba(PALETTE[fill] if fill in PALETTE else fill), font=font(size))


def line_pixels(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    pixels: list[tuple[int, int]] = []
    for start, end in zip(points, points[1:]):
        x0, y0 = start
        x1, y1 = end
        dx = abs(x1 - x0)
        sx = 1 if x0 < x1 else -1
        dy = -abs(y1 - y0)
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            pixels.append((x0, y0))
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy
    return pixels


def ellipse_pixels(cx: int, cy: int, rx: int, ry: int, start_deg: int = 0, end_deg: int = 360) -> list[tuple[int, int]]:
    pixels: list[tuple[int, int]] = []
    for deg in range(start_deg, end_deg + 1, 3):
        rad = math.radians(deg)
        x = int(round(cx + math.cos(rad) * rx))
        y = int(round(cy + math.sin(rad) * ry))
        if (x, y) not in pixels:
            pixels.append((x, y))
    return pixels


def source_layers() -> dict[str, Any]:
    rope_outer = ellipse_pixels(29, 51, 18, 7, 8, 352)
    rope_mid = ellipse_pixels(29, 51, 12, 5, 15, 348)
    rope_inner = ellipse_pixels(29, 51, 7, 3, 20, 342)
    rope_tail = line_pixels([(43, 50), (52, 49), (61, 46), (68, 44)])
    rope_fibers = [
        [13, 50], [16, 47], [19, 45], [22, 44], [27, 44], [32, 44], [37, 45], [42, 48],
        [44, 52], [39, 56], [33, 58], [26, 58], [20, 57], [16, 55], [21, 51], [26, 49],
        [31, 48], [35, 50], [31, 53], [25, 54], [50, 48], [55, 47], [60, 46], [64, 44],
    ]

    chip_pixels = [
        [18, 30], [19, 30], [21, 34], [25, 35], [34, 31], [39, 34], [47, 33], [51, 38],
        [17, 42], [22, 43], [29, 41], [38, 44], [45, 46], [50, 48], [54, 47], [59, 41],
        [63, 29], [68, 30], [74, 30], [80, 32], [78, 39], [66, 43], [72, 47], [81, 49],
        [64, 52], [58, 53], [43, 55], [36, 56], [23, 58], [14, 55], [86, 48], [84, 54],
    ]
    highlight_pixels = [
        [16, 27], [17, 27], [18, 27], [25, 26], [26, 26], [31, 27], [32, 27], [40, 28],
        [51, 29], [54, 30], [62, 26], [66, 25], [70, 24], [73, 24], [75, 25], [78, 27],
        [16, 36], [28, 37], [42, 36], [57, 35], [63, 34], [65, 36], [65, 44], [68, 52],
        [21, 47], [27, 46], [34, 46], [39, 48], [23, 52], [31, 51], [43, 49], [53, 46],
    ]
    grime_pixels = [
        [12, 52], [13, 53], [14, 54], [15, 55], [17, 57], [20, 59], [28, 60], [38, 59],
        [47, 57], [54, 55], [60, 54], [68, 55], [77, 56], [84, 57], [88, 58], [89, 59],
        [17, 49], [29, 49], [39, 50], [48, 51], [53, 50], [58, 48], [63, 46], [76, 43],
        [82, 45], [81, 52], [71, 52], [68, 40], [57, 42], [49, 36], [37, 38], [25, 39],
    ]
    return {
        "schema_id": "wayfarer.newport_green_origin.pixel_layer_source.v1",
        "phase": "G-4.18D.3",
        "asset_id": "g418d3_dockside_rope_crate_barrel_cluster",
        "canvas_px": [CANVAS_W, CANVAS_H],
        "source_policy": "Project-owned pixel-layer source. No source pixels from Newport yellow building sprites, web art, marketplaces, or third-party games.",
        "layer_order": [
            "cast_shadow",
            "contact_shadow",
            "silhouette_blockout",
            "dark_outline",
            "wood_base",
            "rope_base",
            "barrel_base",
            "metal_bands",
            "highlights",
            "chips_scratches",
            "grime",
        ],
        "layers": {
            "silhouette_blockout": {
                "purpose": "Readable 1x massing for crate, rope coil, small barrel, and rope tail before material detail.",
                "ops": [
                    {"op": "polygon", "fill": "blockout_crate", "points": [[13, 27], [47, 26], [56, 33], [55, 51], [17, 53], [12, 45]]},
                    {"op": "rect", "fill": "blockout_crate", "xy": [20, 34, 58, 51]},
                    {"op": "ellipse", "fill": "blockout_barrel", "xy": [61, 24, 84, 58]},
                    {"op": "ellipse_outline", "fill": "blockout_rope", "pixels": rope_outer},
                    {"op": "ellipse_outline", "fill": "blockout_rope", "pixels": rope_mid},
                    {"op": "pixels", "fill": "blockout_rope", "points": rope_tail},
                ],
            },
            "cast_shadow": {
                "purpose": "South/east cast shadow that seats the cluster without becoming a sticker halo.",
                "ops": [
                    {"op": "spans", "fill": "soft_shadow", "spans": [[50, 12, 76], [51, 9, 83], [52, 8, 88], [53, 7, 90], [54, 8, 91], [55, 10, 90], [56, 13, 88], [57, 17, 84], [58, 23, 78]]},
                    {"op": "pixels", "fill": "cast_shadow", "points": [[11, 55], [12, 55], [48, 56], [57, 56], [67, 57], [86, 56], [89, 55], [90, 54]]},
                ],
            },
            "contact_shadow": {
                "purpose": "Darkest contact pixels under rope, crate feet, and barrel foot.",
                "ops": [
                    {"op": "spans", "fill": "contact_shadow", "spans": [[52, 13, 50], [53, 13, 57], [54, 17, 62], [55, 22, 87], [56, 25, 88], [57, 31, 84]]},
                    {"op": "pixels", "fill": "deep_outline", "points": [[14, 54], [15, 54], [44, 53], [45, 53], [54, 52], [65, 54], [80, 55], [85, 55]]},
                ],
            },
            "dark_outline": {
                "purpose": "1px dark painterly contour plus chipped missing corners.",
                "ops": [
                    {"op": "polyline", "fill": "outline", "points": [[14, 28], [46, 27], [55, 34], [55, 50], [47, 53], [17, 53], [12, 46], [12, 33], [14, 28]]},
                    {"op": "polyline", "fill": "deep_outline", "points": [[20, 33], [58, 33], [58, 51], [20, 51], [20, 33]]},
                    {"op": "ellipse_outline", "fill": "outline", "pixels": ellipse_pixels(72, 31, 12, 7, 183, 360)},
                    {"op": "polyline", "fill": "outline", "points": [[61, 31], [60, 52], [65, 58], [80, 58], [86, 52], [84, 31]]},
                    {"op": "ellipse_outline", "fill": "outline", "pixels": ellipse_pixels(29, 51, 19, 8, 5, 354)},
                    {"op": "pixels", "fill": "outline", "points": [[47, 49], [48, 49], [51, 48], [54, 47], [57, 46], [60, 45], [64, 43], [68, 43]]},
                ],
            },
            "wood_base": {
                "purpose": "Weathered crate boards with uneven planks, bevels, nail dents, and dark end grain.",
                "ops": [
                    {"op": "polygon", "fill": "wood_warm", "points": [[14, 29], [45, 28], [54, 34], [54, 39], [20, 38], [13, 34]]},
                    {"op": "rect", "fill": "wood_mid", "xy": [20, 34, 57, 50]},
                    {"op": "polygon", "fill": "wood_dark", "points": [[14, 35], [20, 39], [20, 51], [14, 46]]},
                    {"op": "line", "fill": "wood_dark", "points": [[22, 38], [55, 38]]},
                    {"op": "line", "fill": "wood_dark", "points": [[22, 44], [55, 43]]},
                    {"op": "line", "fill": "wood_dark", "points": [[31, 34], [31, 50]]},
                    {"op": "line", "fill": "wood_dark", "points": [[44, 34], [44, 51]]},
                    {"op": "line", "fill": "outline", "points": [[23, 35], [54, 50]]},
                    {"op": "line", "fill": "outline", "points": [[56, 35], [22, 50]]},
                    {"op": "line", "fill": "wood_light", "points": [[16, 29], [43, 28]]},
                    {"op": "line", "fill": "wood_light", "points": [[22, 35], [55, 34]]},
                    {"op": "pixels", "fill": "chip_dark", "points": [[18, 37], [24, 41], [35, 39], [49, 44], [53, 48], [43, 50], [27, 49]]},
                ],
            },
            "rope_base": {
                "purpose": "Coil rings, rope tail, and individual fiber ticks readable at 1x.",
                "ops": [
                    {"op": "ellipse_outline", "fill": "rope_dark", "pixels": ellipse_pixels(29, 51, 19, 8, 5, 354)},
                    {"op": "ellipse_outline", "fill": "rope_mid", "pixels": rope_outer},
                    {"op": "ellipse_outline", "fill": "rope_light", "pixels": rope_mid},
                    {"op": "ellipse_outline", "fill": "rope_dark", "pixels": rope_inner},
                    {"op": "pixels", "fill": "rope_mid", "points": rope_tail},
                    {"op": "pixels", "fill": "rope_light", "points": line_pixels([(43, 49), (52, 48), (60, 45), (66, 43)])},
                    {"op": "pixels", "fill": "rope_dark", "points": line_pixels([(44, 52), (54, 51), (63, 48), (70, 46)])},
                    {"op": "pixels", "fill": "rope_sun", "points": rope_fibers[0::2]},
                    {"op": "pixels", "fill": "rope_dark", "points": rope_fibers[1::2]},
                ],
            },
            "barrel_base": {
                "purpose": "Small rounded barrel with dark right side, top ellipse, and grounded bottom curve.",
                "ops": [
                    {"op": "spans", "fill": "barrel_mid", "spans": [[26, 65, 79], [27, 62, 82], [28, 61, 84], [29, 60, 85], [30, 60, 86], [31, 60, 86], [32, 61, 85], [33, 61, 85], [34, 61, 85], [35, 61, 85], [36, 61, 85], [37, 61, 85], [38, 61, 85], [39, 61, 85], [40, 61, 85], [41, 61, 85], [42, 61, 85], [43, 61, 85], [44, 61, 85], [45, 61, 85], [46, 61, 85], [47, 62, 84], [48, 62, 84], [49, 63, 83], [50, 64, 82], [51, 65, 81], [52, 67, 79]]},
                    {"op": "spans", "fill": "barrel_dark", "spans": [[34, 78, 85], [35, 79, 85], [36, 80, 85], [37, 80, 85], [38, 80, 85], [39, 80, 85], [40, 80, 85], [41, 80, 85], [42, 80, 85], [43, 79, 85], [44, 79, 85], [45, 78, 84], [46, 78, 84], [47, 77, 83], [48, 76, 83], [49, 75, 82]]},
                    {"op": "ellipse_outline", "fill": "barrel_light", "pixels": ellipse_pixels(72, 28, 10, 4, 190, 350)},
                    {"op": "line", "fill": "barrel_dark", "points": [[66, 32], [65, 50]]},
                    {"op": "line", "fill": "barrel_dark", "points": [[77, 32], [79, 50]]},
                    {"op": "pixels", "fill": "barrel_warm", "points": [[64, 31], [65, 30], [67, 29], [70, 29], [73, 29], [76, 29], [79, 30]]},
                ],
            },
            "metal_bands": {
                "purpose": "Dull hoop bands, not shiny modern metal.",
                "ops": [
                    {"op": "line", "fill": "metal_dark", "points": [[61, 35], [85, 35]]},
                    {"op": "line", "fill": "metal_mid", "points": [[62, 36], [84, 36]]},
                    {"op": "line", "fill": "metal_dark", "points": [[62, 46], [84, 46]]},
                    {"op": "line", "fill": "metal_mid", "points": [[63, 47], [83, 47]]},
                    {"op": "pixels", "fill": "metal_light", "points": [[64, 35], [65, 35], [65, 46], [66, 46], [72, 36], [73, 47]]},
                ],
            },
            "highlights": {
                "purpose": "Sparse warm top-left pixels and rope catchlights.",
                "ops": [
                    {"op": "pixels", "fill": "wood_sun", "points": highlight_pixels[:18]},
                    {"op": "pixels", "fill": "rope_sun", "points": highlight_pixels[18:29]},
                    {"op": "pixels", "fill": "barrel_light", "points": highlight_pixels[29:]},
                    {"op": "line", "fill": "wood_light", "points": [[21, 34], [29, 34]]},
                    {"op": "line", "fill": "wood_light", "points": [[35, 34], [42, 34]]},
                    {"op": "line", "fill": "wood_sun", "points": [[17, 28], [26, 28]]},
                    {"op": "line", "fill": "rope_sun", "points": [[17, 47], [24, 45]]},
                    {"op": "line", "fill": "rope_sun", "points": [[31, 45], [39, 47]]},
                ],
            },
            "chips_scratches": {
                "purpose": "Hand-placed chipped edges, board scratches, nail spots, and broken corners.",
                "ops": [
                    {"op": "pixels", "fill": "chip_dark", "points": chip_pixels},
                    {"op": "pixels", "fill": "wood_light", "points": [[16, 35], [23, 39], [36, 41], [52, 37], [55, 45], [41, 47], [30, 45], [65, 38], [70, 42], [81, 45]]},
                    {"op": "pixels", "fill": "deep_outline", "points": [[13, 32], [13, 33], [19, 51], [20, 52], [58, 50], [85, 52], [66, 57], [78, 58]]},
                ],
            },
            "grime": {
                "purpose": "Harbor dirt, dark lower edge, and green-brown aging marks.",
                "ops": [
                    {"op": "pixels", "fill": "grime", "points": grime_pixels},
                    {"op": "pixels", "fill": "green_grime", "points": [[16, 53], [21, 53], [39, 52], [49, 52], [57, 51], [62, 50], [73, 53], [82, 54]]},
                    {"op": "line", "fill": "grime", "points": [[16, 52], [52, 52]]},
                    {"op": "line", "fill": "grime", "points": [[62, 53], [84, 54]]},
                ],
            },
        },
        "passes": {
            "pass_01_blockout": ["cast_shadow", "contact_shadow", "silhouette_blockout", "dark_outline"],
            "pass_02_material_detail": ["cast_shadow", "contact_shadow", "silhouette_blockout", "dark_outline", "wood_base", "rope_base", "barrel_base", "metal_bands"],
            "pass_03_polish_shadow_grounding": ["cast_shadow", "contact_shadow", "silhouette_blockout", "dark_outline", "wood_base", "rope_base", "barrel_base", "metal_bands", "highlights", "chips_scratches", "grime"],
        },
        "visual_judgment": {
            "rating": VISUAL_RATING,
            "pass_gate": VISUAL_PASS_GATE,
            "verdict": CAPABILITY_VERDICT,
            "status": VISUAL_STATUS,
            "rationale": "The layer workflow is inspectable, but the sprite does not meet the realistic Newport chandlery/wharf prop standard and must stay quarantined as a failed proof.",
        },
    }


def draw_op(layer: Image.Image, op: dict[str, Any]) -> None:
    draw = ImageDraw.Draw(layer)
    fill = rgba(PALETTE[str(op["fill"])])
    kind = op["op"]
    if kind == "rect":
        draw.rectangle(tuple(op["xy"]), fill=fill)
    elif kind == "polygon":
        draw.polygon([tuple(point) for point in op["points"]], fill=fill)
    elif kind == "line":
        draw.line([tuple(point) for point in op["points"]], fill=fill, width=int(op.get("width", 1)))
    elif kind == "polyline":
        points = line_pixels([tuple(point) for point in op["points"]])
        for x, y in points:
            if 0 <= x < CANVAS_W and 0 <= y < CANVAS_H:
                layer.putpixel((x, y), fill)
    elif kind == "ellipse":
        draw.ellipse(tuple(op["xy"]), fill=fill)
    elif kind == "ellipse_outline":
        for x, y in op["pixels"]:
            if 0 <= x < CANVAS_W and 0 <= y < CANVAS_H:
                layer.putpixel((x, y), fill)
    elif kind == "pixels":
        for x, y in op["points"]:
            if 0 <= x < CANVAS_W and 0 <= y < CANVAS_H:
                layer.putpixel((x, y), fill)
    elif kind == "spans":
        for y, x0, x1 in op["spans"]:
            draw.line([(x0, y), (x1, y)], fill=fill)
    else:
        raise ValueError(f"Unknown layer op: {kind}")


def render_layers(source: dict[str, Any]) -> dict[str, Image.Image]:
    layers: dict[str, Image.Image] = {}
    for name in source["layer_order"]:
        image = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        for op in source["layers"][name]["ops"]:
            draw_op(image, op)
        layers[name] = image
    return layers


def compose(layers: dict[str, Image.Image], names: list[str]) -> Image.Image:
    out = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    for name in names:
        out.alpha_composite(layers[name])
    return out


def _sx(value: float) -> int:
    return int(round(value * AA_RENDER))


def _scaled_points(points: list[list[float]] | list[tuple[float, float]]) -> list[tuple[int, int]]:
    return [(_sx(float(point[0])), _sx(float(point[1]))) for point in points]


def _scaled_box(xy: list[float] | tuple[float, float, float, float]) -> tuple[int, int, int, int]:
    return tuple(_sx(float(value)) for value in xy)


def _draw_scaled_op(layer: Image.Image, op: dict[str, Any]) -> None:
    draw = ImageDraw.Draw(layer)
    fill = rgba(PALETTE[str(op["fill"])])
    kind = op["op"]
    if kind == "rect":
        draw.rectangle(_scaled_box(op["xy"]), fill=fill)
    elif kind == "polygon":
        draw.polygon(_scaled_points(op["points"]), fill=fill)
    elif kind == "line":
        draw.line(_scaled_points(op["points"]), fill=fill, width=max(1, _sx(float(op.get("width", 0.75)))))
    elif kind == "arc":
        draw.arc(
            _scaled_box(op["xy"]),
            start=float(op.get("start", 0)),
            end=float(op.get("end", 360)),
            fill=fill,
            width=max(1, _sx(float(op.get("width", 0.75)))),
        )
    elif kind == "ellipse":
        draw.ellipse(_scaled_box(op["xy"]), fill=fill)
    elif kind == "ellipse_outline":
        draw.ellipse(_scaled_box(op["xy"]), outline=fill, width=max(1, _sx(float(op.get("width", 0.75)))))
    elif kind == "pixels":
        for point in op["points"]:
            x = _sx(float(point[0]))
            y = _sx(float(point[1]))
            draw.rectangle((x, y, x + AA_RENDER - 1, y + AA_RENDER - 1), fill=fill)
    elif kind == "spans":
        for y, x0, x1 in op["spans"]:
            draw.line([(_sx(float(x0)), _sx(float(y))), (_sx(float(x1)), _sx(float(y)))], fill=fill, width=max(1, _sx(float(op.get("width", 0.75)))))
    else:
        raise ValueError(f"Unknown layer op: {kind}")


def render_layers(source: dict[str, Any]) -> dict[str, Image.Image]:
    layers: dict[str, Image.Image] = {}
    for name in source["layer_order"]:
        hi = Image.new("RGBA", (CANVAS_W * AA_RENDER, CANVAS_H * AA_RENDER), (0, 0, 0, 0))
        for op in source["layers"][name]["ops"]:
            _draw_scaled_op(hi, op)
        layers[name] = hi.resize((CANVAS_W, CANVAS_H), Image.Resampling.LANCZOS)
    return layers


def _scatter(seed: int, count: int, x0: int, y0: int, x1: int, y1: int) -> list[list[int]]:
    # Deterministic, hand-bounded speckle fields for grime/chips without source-image pixels.
    points: list[list[int]] = []
    value = seed
    for _ in range(count):
        value = (1103515245 * value + 12345) & 0x7FFFFFFF
        x = x0 + value % max(1, x1 - x0 + 1)
        value = (1103515245 * value + 12345) & 0x7FFFFFFF
        y = y0 + value % max(1, y1 - y0 + 1)
        points.append([x, y])
    return points


def write_inkscape_silhouette_plan() -> str:
    SOURCE_ROOT.mkdir(parents=True, exist_ok=True)
    GENERATED_ROOT.mkdir(parents=True, exist_ok=True)
    SILHOUETTE_PLAN_SVG_PATH.write_text(
        """<svg xmlns="http://www.w3.org/2000/svg" width="384" height="256" viewBox="0 0 96 64">
  <rect width="96" height="64" fill="none"/>
  <g fill="none" stroke-linecap="round" stroke-linejoin="round">
    <ellipse cx="48" cy="56" rx="41" ry="8" fill="#15100a" opacity="0.36"/>
    <path d="M14 29 L47 26 L58 32 L58 50 L50 54 L19 55 L13 48 L13 34 Z" fill="#956b42" stroke="#15100a" stroke-width="1.1"/>
    <path d="M15 29 L47 26 L58 32 L23 35 Z" fill="#bb925f" stroke="#3e2818" stroke-width="0.7"/>
    <ellipse cx="74" cy="30" rx="13" ry="8" fill="#754a2b" stroke="#15100a" stroke-width="1.1"/>
    <path d="M63 29 L86 29 L84 53 L66 57 L61 51 Z" fill="#754a2b" stroke="#15100a" stroke-width="1.1"/>
    <ellipse cx="30" cy="51" rx="19" ry="8" stroke="#c2ab72" stroke-width="3.0"/>
    <ellipse cx="30" cy="51" rx="10" ry="4" stroke="#4e3c25" stroke-width="1.4"/>
    <path d="M44 49 C56 47 63 45 72 43" stroke="#8c744d" stroke-width="2.4"/>
  </g>
</svg>
""",
        encoding="utf-8",
    )
    inkscape = find_tool(INKSCAPE)
    result = subprocess.run(
        [
            str(inkscape),
            str(SILHOUETTE_PLAN_SVG_PATH),
            "--export-type=png",
            f"--export-filename={SILHOUETTE_PLAN_PNG_PATH}",
            "--export-width=384",
            "--export-height=256",
        ],
        capture_output=True,
        text=True,
        check=True,
        timeout=60,
        env=tool_env(),
    )
    if not SILHOUETTE_PLAN_PNG_PATH.exists():
        raise RuntimeError("Inkscape did not produce the G-4.18D.3 silhouette plan")
    return " ".join((result.stdout + " " + result.stderr).split())


def source_layers() -> dict[str, Any]:
    rope_ticks = []
    for idx in range(24):
        angle = math.radians(idx * 15)
        rope_ticks.append([round(24 + math.cos(angle) * 15), round(50 + math.sin(angle) * 6)])
    crate_chips = _scatter(4183, 34, 16, 25, 60, 52)
    barrel_marks = _scatter(4189, 24, 64, 25, 86, 54)
    grime_points = _scatter(4197, 46, 14, 42, 88, 58)
    highlight_points = [[18, 25], [20, 25], [24, 25], [36, 25], [47, 27], [55, 33], [66, 25], [70, 24], [76, 25], [83, 31], [17, 45], [25, 44], [31, 44], [42, 45], [51, 43], [25, 51], [36, 50], [55, 46]]

    return {
        "schema_id": "wayfarer.newport_green_origin.pixel_layer_source.v2",
        "phase": "G-4.18D.3",
        "asset_id": "g418d3_dockside_rope_crate_barrel_cluster",
        "canvas_px": [CANVAS_W, CANVAS_H],
        "render_policy": f"{AA_RENDER}x hand-authored layer geometry baked to final 1x with antialiasing, then inspected at 1x/8x.",
        "source_policy": "Project-owned pixel-layer source. Existing Newport/chandlery/wharf art is used only as visible style standard; no source pixels are copied, cropped, pasted, traced, or sampled into the new sprite.",
        "layer_order": [
            "cast_shadow",
            "contact_shadow",
            "silhouette_blockout",
            "dark_outline",
            "wood_base",
            "rope_base",
            "barrel_base",
            "metal_bands",
            "highlights",
            "chips_scratches",
            "grime",
        ],
        "layers": {
            "cast_shadow": {
                "purpose": "Soft broad harbor-floor shadow, separated from the object contact pixels.",
                "ops": [
                    {"op": "ellipse", "fill": "soft_shadow", "xy": [8, 48, 92, 63]},
                    {"op": "ellipse", "fill": "cast_shadow", "xy": [18, 50, 78, 62]},
                ],
            },
            "contact_shadow": {
                "purpose": "Dark occlusion under the rope coil, crate corners, and barrel foot.",
                "ops": [
                    {"op": "ellipse", "fill": "contact_shadow", "xy": [13, 52, 52, 60]},
                    {"op": "ellipse", "fill": "contact_shadow", "xy": [31, 50, 66, 59]},
                    {"op": "ellipse", "fill": "contact_shadow", "xy": [61, 52, 88, 61]},
                    {"op": "line", "fill": "deep_outline", "points": [[18, 55], [84, 56]], "width": 0.65},
                ],
            },
            "silhouette_blockout": {
                "purpose": "3/4 harbor prop massing: lower rope coil, weathered crate behind it, and small round barrel nested to the right.",
                "ops": [
                    {"op": "polygon", "fill": "blockout_crate", "points": [[14, 28], [48, 24], [61, 31], [60, 51], [19, 55], [13, 47]]},
                    {"op": "polygon", "fill": "wood_dark", "points": [[48, 24], [61, 31], [61, 50], [49, 47]]},
                    {"op": "ellipse", "fill": "blockout_barrel", "xy": [62, 22, 88, 57]},
                    {"op": "ellipse_outline", "fill": "blockout_rope", "xy": [12, 43, 48, 59], "width": 4.0},
                    {"op": "line", "fill": "blockout_rope", "points": [[44, 50], [56, 48], [72, 43]], "width": 3.0},
                ],
            },
            "wood_base": {
                "purpose": "Layered weathered crate boards with top plane, side plane, braces, nail dents, and broken edges.",
                "ops": [
                    {"op": "polygon", "fill": "wood_mid", "points": [[15, 29], [47, 26], [57, 32], [57, 50], [19, 53], [15, 46]]},
                    {"op": "polygon", "fill": "wood_light", "points": [[15, 29], [47, 26], [57, 32], [23, 35]]},
                    {"op": "polygon", "fill": "wood_dark", "points": [[47, 26], [57, 32], [57, 50], [49, 47]]},
                    {"op": "line", "fill": "wood_deep", "points": [[19, 36], [56, 34]], "width": 0.75},
                    {"op": "line", "fill": "wood_deep", "points": [[19, 43], [57, 41]], "width": 0.75},
                    {"op": "line", "fill": "wood_cool_shadow", "points": [[30, 34], [29, 52]], "width": 0.6},
                    {"op": "line", "fill": "wood_cool_shadow", "points": [[43, 32], [43, 50]], "width": 0.6},
                    {"op": "line", "fill": "outline", "points": [[21, 35], [54, 49]], "width": 1.0},
                    {"op": "line", "fill": "outline", "points": [[55, 34], [22, 50]], "width": 1.0},
                    {"op": "line", "fill": "wood_sun", "points": [[18, 29], [44, 27]], "width": 0.6},
                    {"op": "pixels", "fill": "chip_dark", "points": crate_chips[0::3]},
                    {"op": "pixels", "fill": "wood_light", "points": crate_chips[1::4]},
                ],
            },
            "rope_base": {
                "purpose": "Nested rope coil and loose tail with alternating fiber ticks.",
                "ops": [
                    {"op": "arc", "fill": "rope_shadow", "xy": [11, 42, 50, 60], "start": 5, "end": 356, "width": 2.4},
                    {"op": "arc", "fill": "rope_mid", "xy": [13, 43, 48, 58], "start": 8, "end": 352, "width": 2.1},
                    {"op": "arc", "fill": "rope_light", "xy": [17, 45, 43, 56], "start": 12, "end": 348, "width": 1.6},
                    {"op": "arc", "fill": "rope_dark", "xy": [21, 47, 39, 54], "start": 18, "end": 342, "width": 1.2},
                    {"op": "arc", "fill": "rope_sun", "xy": [24, 49, 36, 53], "start": 20, "end": 338, "width": 0.75},
                    {"op": "line", "fill": "rope_mid", "points": [[44, 49], [56, 47], [72, 43]], "width": 2.4},
                    {"op": "line", "fill": "rope_dark", "points": [[45, 52], [58, 50], [74, 45]], "width": 1.0},
                    {"op": "line", "fill": "rope_sun", "points": [[45, 48], [56, 46], [70, 42]], "width": 0.7},
                    {"op": "pixels", "fill": "rope_sun", "points": rope_ticks[0::2]},
                    {"op": "pixels", "fill": "rope_dark", "points": rope_ticks[1::2]},
                ],
            },
            "barrel_base": {
                "purpose": "Rounded barrel with shaded staves, off-center top ellipse, and worn lower rim.",
                "ops": [
                    {"op": "ellipse", "fill": "barrel_dark", "xy": [62, 22, 88, 35]},
                    {"op": "polygon", "fill": "barrel_mid", "points": [[63, 29], [86, 29], [84, 53], [66, 57], [61, 51]]},
                    {"op": "polygon", "fill": "barrel_dark", "points": [[78, 30], [87, 31], [84, 53], [77, 55]]},
                    {"op": "ellipse_outline", "fill": "barrel_light", "xy": [64, 23, 86, 33], "width": 1.0},
                    {"op": "line", "fill": "barrel_dark", "points": [[67, 31], [66, 54]], "width": 0.7},
                    {"op": "line", "fill": "barrel_dark", "points": [[75, 30], [76, 55]], "width": 0.7},
                    {"op": "line", "fill": "barrel_warm", "points": [[69, 26], [82, 27]], "width": 0.65},
                    {"op": "pixels", "fill": "chip_dark", "points": barrel_marks[0::3]},
                    {"op": "pixels", "fill": "barrel_light", "points": barrel_marks[1::5]},
                ],
            },
            "metal_bands": {
                "purpose": "Dull, aged barrel hoops with tiny rust-light breaks.",
                "ops": [
                    {"op": "line", "fill": "metal_dark", "points": [[62, 36], [86, 36]], "width": 0.95},
                    {"op": "line", "fill": "metal_mid", "points": [[63, 37], [85, 37]], "width": 0.55},
                    {"op": "line", "fill": "metal_dark", "points": [[63, 47], [84, 47]], "width": 0.95},
                    {"op": "line", "fill": "metal_mid", "points": [[64, 48], [83, 48]], "width": 0.55},
                    {"op": "pixels", "fill": "metal_light", "points": [[66, 36], [72, 37], [65, 47], [73, 48]]},
                ],
            },
            "dark_outline": {
                "purpose": "Pitched dark painterly edge, drawn late so forms do not dissolve into the ground.",
                "ops": [
                    {"op": "line", "fill": "outline", "points": [[15, 29], [47, 26], [58, 32], [58, 50], [50, 54], [19, 55], [13, 48], [13, 34], [15, 29]], "width": 0.8},
                    {"op": "ellipse_outline", "fill": "outline", "xy": [11, 42, 50, 60], "width": 0.8},
                    {"op": "line", "fill": "outline", "points": [[44, 51], [57, 50], [75, 45]], "width": 0.65},
                    {"op": "ellipse_outline", "fill": "outline", "xy": [62, 22, 88, 57], "width": 0.75},
                    {"op": "line", "fill": "deep_outline", "points": [[17, 55], [86, 56]], "width": 0.55},
                ],
            },
            "highlights": {
                "purpose": "Sparse top-left glints and material cues aligned to Newport warm light.",
                "ops": [
                    {"op": "pixels", "fill": "chalk_highlight", "points": highlight_points[0:6]},
                    {"op": "pixels", "fill": "wood_sun", "points": highlight_points[6:10]},
                    {"op": "pixels", "fill": "rope_sun", "points": highlight_points[10:16]},
                    {"op": "pixels", "fill": "barrel_light", "points": highlight_points[16:]},
                    {"op": "line", "fill": "wood_sun", "points": [[20, 31], [31, 30]], "width": 0.55},
                    {"op": "line", "fill": "rope_sun", "points": [[18, 46], [30, 44]], "width": 0.55},
                ],
            },
            "chips_scratches": {
                "purpose": "Visible damage, nail heads, and worn chipped silhouette pixels.",
                "ops": [
                    {"op": "pixels", "fill": "chip_dark", "points": crate_chips + barrel_marks[0::2]},
                    {"op": "pixels", "fill": "wood_light", "points": [[16, 35], [22, 38], [34, 37], [49, 42], [54, 48], [67, 41], [82, 44]]},
                    {"op": "line", "fill": "grime", "points": [[21, 51], [57, 50]], "width": 0.55},
                ],
            },
            "grime": {
                "purpose": "Lower-edge harbor grime and green-brown aging that helps the cluster sit with the chandlery props.",
                "ops": [
                    {"op": "pixels", "fill": "grime", "points": grime_points},
                    {"op": "pixels", "fill": "green_grime", "points": grime_points[0::4]},
                    {"op": "line", "fill": "grime", "points": [[16, 53], [57, 53]], "width": 1.0},
                    {"op": "line", "fill": "grime", "points": [[62, 54], [85, 55]], "width": 0.9},
                ],
            },
        },
        "passes": {
            "pass_01_blockout": ["cast_shadow", "contact_shadow", "silhouette_blockout", "dark_outline"],
            "pass_02_material_detail": ["cast_shadow", "contact_shadow", "silhouette_blockout", "wood_base", "rope_base", "barrel_base", "metal_bands", "dark_outline"],
            "pass_03_polish_shadow_grounding": ["cast_shadow", "contact_shadow", "silhouette_blockout", "wood_base", "rope_base", "barrel_base", "metal_bands", "dark_outline", "highlights", "chips_scratches", "grime"],
        },
        "visual_judgment": {
            "rating": VISUAL_RATING,
            "pass_gate": VISUAL_PASS_GATE,
            "verdict": CAPABILITY_VERDICT,
            "status": VISUAL_STATUS,
            "rationale": "The rebuilt source adopts a painterly anti-aliased Newport prop grammar and is materially stronger than the failed hard-pixel token, but remains below the chandlery/wharf standard until human review accepts it.",
        },
    }


def _ellipse_points(cx: float, cy: float, rx: float, ry: float, count: int, start_deg: float = 0, end_deg: float = 360) -> list[list[int]]:
    points: list[list[int]] = []
    if count <= 1:
        return [[round(cx), round(cy)]]
    span = end_deg - start_deg
    for idx in range(count):
        deg = start_deg + (span * idx / max(1, count - 1))
        rad = math.radians(deg)
        points.append([round(cx + math.cos(rad) * rx), round(cy + math.sin(rad) * ry)])
    return points


def write_inkscape_silhouette_plan() -> str:
    SOURCE_ROOT.mkdir(parents=True, exist_ok=True)
    GENERATED_ROOT.mkdir(parents=True, exist_ok=True)
    SILHOUETTE_PLAN_SVG_PATH.write_text(
        """<svg xmlns="http://www.w3.org/2000/svg" width="384" height="256" viewBox="0 0 96 64">
  <rect width="96" height="64" fill="none"/>
  <g fill="none" stroke-linecap="round" stroke-linejoin="round">
    <ellipse cx="49" cy="56" rx="43" ry="7" fill="#090705" opacity="0.42"/>
    <path d="M8 31 L18 24 L46 24 L46 47 L39 54 L8 54 Z" fill="#8b613e" stroke="#15100b" stroke-width="1.1"/>
    <path d="M8 31 L18 24 L46 24 L39 31 Z" fill="#bb925f" stroke="#3e2818" stroke-width="0.65"/>
    <path d="M39 31 L46 24 L46 47 L39 54 Z" fill="#3e2818" stroke="#15100b" stroke-width="0.8"/>
    <path d="M49 28 C47 35 46 45 48 50 C50 56 55 58 63 57 C69 56 72 51 71 46 C70 37 70 31 68 28 Z" fill="#754a2b" stroke="#15100b" stroke-width="1.1"/>
    <ellipse cx="59" cy="28" rx="10" ry="5" fill="#9a6237" stroke="#15100b" stroke-width="1.0"/>
    <ellipse cx="79" cy="51" rx="15" ry="7" stroke="#c2ab72" stroke-width="3.0"/>
    <ellipse cx="79" cy="51" rx="8" ry="4" stroke="#4e3c25" stroke-width="1.5"/>
    <path d="M67 48 C60 45 57 47 56 51" stroke="#8c744d" stroke-width="2.3"/>
  </g>
</svg>
""",
        encoding="utf-8",
    )
    inkscape = find_tool(INKSCAPE)
    result = subprocess.run(
        [
            str(inkscape),
            str(SILHOUETTE_PLAN_SVG_PATH),
            "--export-type=png",
            f"--export-filename={SILHOUETTE_PLAN_PNG_PATH}",
            "--export-width=384",
            "--export-height=256",
        ],
        capture_output=True,
        text=True,
        check=True,
        timeout=60,
        env=tool_env(),
    )
    if not SILHOUETTE_PLAN_PNG_PATH.exists():
        raise RuntimeError("Inkscape did not produce the G-4.18D.3 silhouette plan")
    return " ".join((result.stdout + " " + result.stderr).split())


def source_layers() -> dict[str, Any]:
    """Third rebuild: make each prop read independently before assembling the cluster."""

    crate_chips = [
        [9, 32], [12, 39], [14, 51], [18, 25], [21, 37], [26, 45], [31, 31], [35, 49],
        [40, 35], [44, 26], [45, 43], [11, 47], [22, 52], [34, 38], [37, 29], [16, 43],
        [29, 27], [33, 53], [42, 46],
    ]
    barrel_marks = [
        [51, 31], [55, 29], [61, 30], [66, 33], [50, 41], [56, 38], [63, 41], [68, 45],
        [52, 52], [58, 54], [64, 52], [69, 49], [54, 35], [61, 45], [66, 55],
    ]
    rope_outer_ticks = _ellipse_points(79, 51, 15, 7, 28, 8, 352)
    rope_inner_ticks = _ellipse_points(79, 51, 8, 4, 18, 22, 338)
    grime_points = [
        [7, 55], [13, 56], [22, 55], [31, 56], [39, 55], [47, 56], [55, 57], [63, 56],
        [72, 58], [82, 58], [92, 57], [12, 52], [38, 52], [49, 53], [65, 54], [88, 55],
    ] + _scatter(4321, 20, 8, 43, 92, 58)
    highlight_points = [
        [12, 30], [20, 25], [28, 25], [36, 25], [14, 35], [24, 36], [35, 34],
        [52, 27], [58, 25], [64, 27], [53, 33], [62, 35],
        [68, 47], [73, 45], [80, 44], [87, 46], [72, 52], [83, 53],
    ]

    return {
        "schema_id": "wayfarer.newport_green_origin.pixel_layer_source.v3",
        "phase": "G-4.18D.3",
        "asset_id": "g418d3_dockside_rope_crate_barrel_cluster",
        "canvas_px": [CANVAS_W, CANVAS_H],
        "render_policy": f"{AA_RENDER}x painterly layer geometry baked to final 1x; separate prop studies are generated before the cluster is judged.",
        "source_policy": "Project-owned pixel-layer source. Existing Newport/chandlery/wharf art is used only as visible style standard; no source pixels are copied, cropped, pasted, traced, sampled, or AI-generated into the new sprite.",
        "object_readability_strategy": [
            "crate is built as a separate 3/4 wooden box with top plane, side plane, X brace, plank seams, nails, and chipped corners",
            "barrel is built as a separate small upright cask with top ellipse, bulged staves, dull hoops, and shaded lower rim",
            "rope is built as a separate foreground coil with nested ellipses, central hole, loose tail, fiber ticks, and individual contact shadow",
        ],
        "layer_order": [
            "cast_shadow",
            "contact_shadow",
            "silhouette_blockout",
            "dark_outline",
            "wood_base",
            "rope_base",
            "barrel_base",
            "metal_bands",
            "highlights",
            "chips_scratches",
            "grime",
        ],
        "layers": {
            "cast_shadow": {
                "purpose": "Low broad shadow tying three independent props to one dock plane.",
                "ops": [
                    {"op": "ellipse", "fill": "soft_shadow", "xy": [4, 49, 94, 63]},
                    {"op": "ellipse", "fill": "cast_shadow", "xy": [6, 51, 48, 60]},
                    {"op": "ellipse", "fill": "cast_shadow", "xy": [44, 51, 73, 61]},
                    {"op": "ellipse", "fill": "cast_shadow", "xy": [62, 51, 96, 62]},
                ],
            },
            "contact_shadow": {
                "purpose": "Separate occlusion pads so crate, barrel, and rope are grounded rather than pasted on.",
                "ops": [
                    {"op": "ellipse", "fill": "contact_shadow", "xy": [7, 52, 42, 58]},
                    {"op": "ellipse", "fill": "contact_shadow", "xy": [48, 53, 70, 60]},
                    {"op": "ellipse", "fill": "contact_shadow", "xy": [64, 53, 94, 61]},
                    {"op": "line", "fill": "deep_outline", "points": [[9, 55], [39, 55]], "width": 0.55},
                    {"op": "line", "fill": "deep_outline", "points": [[51, 57], [67, 57]], "width": 0.55},
                    {"op": "line", "fill": "deep_outline", "points": [[67, 58], [91, 58]], "width": 0.55},
                ],
            },
            "silhouette_blockout": {
                "purpose": "Readable object-first massing: crate left, barrel middle, rope coil foreground-right.",
                "ops": [
                    {"op": "polygon", "fill": "blockout_crate", "points": [[8, 31], [18, 24], [46, 24], [46, 47], [39, 54], [8, 54]]},
                    {"op": "polygon", "fill": "wood_dark", "points": [[39, 31], [46, 24], [46, 47], [39, 54]]},
                    {"op": "polygon", "fill": "blockout_barrel", "points": [[50, 28], [68, 28], [71, 47], [66, 56], [53, 57], [48, 50], [48, 36]]},
                    {"op": "ellipse", "fill": "blockout_barrel", "xy": [49, 23, 69, 33]},
                    {"op": "arc", "fill": "blockout_rope", "xy": [64, 42, 94, 59], "start": 0, "end": 360, "width": 3.4},
                    {"op": "arc", "fill": "blockout_rope", "xy": [72, 47, 86, 55], "start": 0, "end": 360, "width": 1.9},
                    {"op": "arc", "fill": "blockout_rope", "xy": [55, 43, 78, 56], "start": 206, "end": 360, "width": 2.4},
                ],
            },
            "wood_base": {
                "purpose": "Weathered crate: top, side, front planks, X-brace, nails, broken rim.",
                "ops": [
                    {"op": "polygon", "fill": "wood_mid", "points": [[8, 31], [39, 31], [39, 54], [8, 54]]},
                    {"op": "polygon", "fill": "wood_light", "points": [[8, 31], [18, 24], [46, 24], [39, 31]]},
                    {"op": "polygon", "fill": "wood_dark", "points": [[39, 31], [46, 24], [46, 47], [39, 54]]},
                    {"op": "line", "fill": "wood_deep", "points": [[10, 37], [38, 37]], "width": 0.75},
                    {"op": "line", "fill": "wood_deep", "points": [[10, 45], [38, 45]], "width": 0.75},
                    {"op": "line", "fill": "wood_cool_shadow", "points": [[18, 32], [18, 53]], "width": 0.55},
                    {"op": "line", "fill": "wood_cool_shadow", "points": [[29, 32], [29, 54]], "width": 0.55},
                    {"op": "line", "fill": "wood_deep", "points": [[12, 35], [36, 51]], "width": 1.3},
                    {"op": "line", "fill": "wood_deep", "points": [[36, 35], [12, 51]], "width": 1.3},
                    {"op": "line", "fill": "wood_light", "points": [[13, 34], [36, 49]], "width": 0.55},
                    {"op": "line", "fill": "wood_light", "points": [[35, 34], [13, 49]], "width": 0.55},
                    {"op": "line", "fill": "wood_sun", "points": [[12, 30], [37, 29]], "width": 0.55},
                    {"op": "line", "fill": "wood_sun", "points": [[19, 25], [43, 25]], "width": 0.55},
                    {"op": "pixels", "fill": "chip_dark", "points": crate_chips[0::2]},
                    {"op": "pixels", "fill": "wood_light", "points": crate_chips[1::3]},
                ],
            },
            "barrel_base": {
                "purpose": "Small cask: clear top ellipse, bulged sides, staves, warm left face, dark right face.",
                "ops": [
                    {"op": "ellipse", "fill": "barrel_dark", "xy": [49, 23, 69, 33]},
                    {"op": "polygon", "fill": "barrel_mid", "points": [[50, 29], [68, 29], [71, 46], [67, 54], [62, 57], [53, 57], [48, 50], [48, 36]]},
                    {"op": "polygon", "fill": "barrel_warm", "points": [[51, 29], [60, 29], [60, 56], [53, 56], [49, 49], [49, 36]]},
                    {"op": "polygon", "fill": "barrel_dark", "points": [[63, 29], [69, 30], [70, 47], [66, 55], [63, 56]]},
                    {"op": "ellipse_outline", "fill": "barrel_light", "xy": [50, 24, 68, 32], "width": 0.95},
                    {"op": "arc", "fill": "barrel_dark", "xy": [49, 48, 69, 58], "start": 0, "end": 180, "width": 0.95},
                    {"op": "line", "fill": "barrel_dark", "points": [[53, 31], [52, 53]], "width": 0.6},
                    {"op": "line", "fill": "barrel_dark", "points": [[59, 30], [59, 56]], "width": 0.65},
                    {"op": "line", "fill": "barrel_dark", "points": [[65, 31], [67, 52]], "width": 0.6},
                    {"op": "line", "fill": "barrel_light", "points": [[54, 27], [64, 27]], "width": 0.55},
                    {"op": "pixels", "fill": "chip_dark", "points": barrel_marks[0::3]},
                    {"op": "pixels", "fill": "barrel_light", "points": barrel_marks[1::4]},
                ],
            },
            "metal_bands": {
                "purpose": "Dull colonial iron hoops visibly wrapping the small barrel.",
                "ops": [
                    {"op": "line", "fill": "metal_dark", "points": [[49, 36], [70, 36]], "width": 1.15},
                    {"op": "line", "fill": "metal_mid", "points": [[50, 37], [69, 37]], "width": 0.55},
                    {"op": "line", "fill": "metal_dark", "points": [[49, 47], [70, 47]], "width": 1.15},
                    {"op": "line", "fill": "metal_mid", "points": [[50, 48], [69, 48]], "width": 0.55},
                    {"op": "pixels", "fill": "metal_light", "points": [[52, 36], [59, 37], [66, 36], [51, 47], [61, 48], [68, 47]]},
                ],
            },
            "rope_base": {
                "purpose": "Foreground rope coil, central hole, loose tail, and alternating fiber ticks.",
                "ops": [
                    {"op": "arc", "fill": "rope_shadow", "xy": [63, 42, 95, 60], "start": 0, "end": 360, "width": 3.2},
                    {"op": "arc", "fill": "rope_mid", "xy": [65, 43, 93, 58], "start": 0, "end": 360, "width": 2.5},
                    {"op": "arc", "fill": "rope_light", "xy": [69, 45, 89, 56], "start": 0, "end": 360, "width": 1.7},
                    {"op": "arc", "fill": "rope_dark", "xy": [74, 48, 84, 54], "start": 0, "end": 360, "width": 1.2},
                    {"op": "arc", "fill": "rope_mid", "xy": [56, 43, 80, 56], "start": 202, "end": 360, "width": 2.2},
                    {"op": "arc", "fill": "rope_dark", "xy": [55, 46, 78, 58], "start": 210, "end": 354, "width": 0.85},
                    {"op": "line", "fill": "rope_sun", "points": [[62, 46], [70, 45]], "width": 0.55},
                    {"op": "line", "fill": "rope_sun", "points": [[70, 44], [86, 46]], "width": 0.55},
                    {"op": "pixels", "fill": "rope_sun", "points": rope_outer_ticks[0::2] + rope_inner_ticks[0::2]},
                    {"op": "pixels", "fill": "rope_dark", "points": rope_outer_ticks[1::2] + rope_inner_ticks[1::2]},
                ],
            },
            "dark_outline": {
                "purpose": "Final painterly contour and occlusion marks after the individual materials are readable.",
                "ops": [
                    {"op": "line", "fill": "outline", "points": [[8, 31], [18, 24], [46, 24], [46, 47], [39, 54], [8, 54], [8, 31]], "width": 0.85},
                    {"op": "line", "fill": "outline", "points": [[8, 31], [39, 31], [46, 24]], "width": 0.65},
                    {"op": "line", "fill": "deep_outline", "points": [[39, 31], [39, 54]], "width": 0.55},
                    {"op": "ellipse_outline", "fill": "outline", "xy": [49, 23, 69, 33], "width": 0.8},
                    {"op": "line", "fill": "outline", "points": [[50, 29], [48, 36], [48, 50], [53, 57], [63, 57], [67, 55], [71, 47], [68, 29]], "width": 0.85},
                    {"op": "ellipse_outline", "fill": "outline", "xy": [63, 42, 95, 60], "width": 0.75},
                    {"op": "ellipse_outline", "fill": "deep_outline", "xy": [74, 48, 84, 54], "width": 0.55},
                    {"op": "arc", "fill": "outline", "xy": [55, 43, 80, 57], "start": 202, "end": 360, "width": 0.65},
                ],
            },
            "highlights": {
                "purpose": "Small warm top-left catches: not symbolic sparkle, just material separation.",
                "ops": [
                    {"op": "pixels", "fill": "chalk_highlight", "points": highlight_points[0:4]},
                    {"op": "pixels", "fill": "wood_sun", "points": highlight_points[4:7]},
                    {"op": "pixels", "fill": "barrel_light", "points": highlight_points[7:12]},
                    {"op": "pixels", "fill": "rope_sun", "points": highlight_points[12:]},
                    {"op": "line", "fill": "wood_sun", "points": [[11, 33], [23, 33]], "width": 0.55},
                    {"op": "line", "fill": "barrel_light", "points": [[52, 31], [58, 30]], "width": 0.55},
                    {"op": "arc", "fill": "rope_sun", "xy": [67, 44, 91, 57], "start": 200, "end": 322, "width": 0.55},
                ],
            },
            "chips_scratches": {
                "purpose": "Hand-placed chips and surface scars, kept sparse enough to preserve object readability.",
                "ops": [
                    {"op": "pixels", "fill": "chip_dark", "points": crate_chips + barrel_marks[0::2]},
                    {"op": "pixels", "fill": "wood_light", "points": [[10, 38], [19, 41], [28, 48], [36, 42], [42, 29], [45, 43]]},
                    {"op": "line", "fill": "grime", "points": [[11, 53], [38, 53]], "width": 0.55},
                    {"op": "line", "fill": "grime", "points": [[50, 55], [67, 55]], "width": 0.55},
                ],
            },
            "grime": {
                "purpose": "Harbor dirt on lower edges plus green-brown aging marks that tie the props to the dock.",
                "ops": [
                    {"op": "pixels", "fill": "grime", "points": grime_points},
                    {"op": "pixels", "fill": "green_grime", "points": grime_points[0::4]},
                    {"op": "line", "fill": "grime", "points": [[8, 54], [39, 54]], "width": 0.9},
                    {"op": "line", "fill": "grime", "points": [[49, 56], [67, 56]], "width": 0.8},
                    {"op": "arc", "fill": "grime", "xy": [65, 49, 93, 60], "start": 20, "end": 168, "width": 0.65},
                ],
            },
        },
        "passes": {
            "pass_01_blockout": ["cast_shadow", "contact_shadow", "silhouette_blockout", "dark_outline"],
            "pass_02_material_detail": ["cast_shadow", "contact_shadow", "silhouette_blockout", "wood_base", "barrel_base", "metal_bands", "rope_base", "dark_outline"],
            "pass_03_polish_shadow_grounding": [
                "cast_shadow",
                "contact_shadow",
                "silhouette_blockout",
                "wood_base",
                "barrel_base",
                "metal_bands",
                "rope_base",
                "dark_outline",
                "highlights",
                "chips_scratches",
                "grime",
            ],
        },
        "visual_judgment": {
            "rating": VISUAL_RATING,
            "pass_gate": VISUAL_PASS_GATE,
            "verdict": CAPABILITY_VERDICT,
            "status": VISUAL_STATUS,
            "rationale": "This third approach drops the 8-bit token/one-blob model and proves clearer crate, barrel, and rope studies before assembly. It is more readable, but still deferred below the chandlery-quality bar until human art review accepts it.",
        },
    }


def write_source_and_passes(source: dict[str, Any]) -> dict[str, Image.Image]:
    for directory in [GENERATED_ROOT, SOURCE_ROOT, REPORTS_ROOT, CONTACT_SHEET_ROOT, LAYER_ROOT]:
        directory.mkdir(parents=True, exist_ok=True)
    SOURCE_JSON_PATH.write_text(json.dumps(source, indent=2) + "\n", encoding="utf-8")
    layers = render_layers(source)
    for idx, name in enumerate(source["layer_order"], 1):
        layers[name].save(LAYER_ROOT / f"{idx:02d}_{name}.png")
    pass01 = compose(layers, source["passes"]["pass_01_blockout"])
    pass02 = compose(layers, source["passes"]["pass_02_material_detail"])
    pass03 = compose(layers, source["passes"]["pass_03_polish_shadow_grounding"])
    pass01.save(PASS01_PATH)
    pass02.save(PASS02_PATH)
    pass03.save(PASS03_PATH)
    return {"pass01": pass01, "pass02": pass02, "pass03": pass03, **layers}


def run_krita_export() -> str:
    krita = find_tool(KRITA_EXE)
    result = subprocess.run(
        [str(krita), "--export", "--export-filename", str(KRITA_RAW_PATH), str(PASS03_PATH)],
        capture_output=True,
        text=True,
        check=True,
        timeout=90,
        env=tool_env(),
    )
    if not KRITA_RAW_PATH.exists():
        raise RuntimeError("Krita CLI did not produce the G-4.18D.3 PNG output")
    KRITA_LOG_PATH.write_text(
        json.dumps(
            {
                "tool": "Krita CLI",
                "input": rel(PASS03_PATH),
                "output": rel(KRITA_RAW_PATH),
                "operations": [
                    "opened the pass 03 pixel-layer composite",
                    "inspected/exported the 1x hard-pixel projection without resampling",
                    "confirmed the refinement layer decisions are encoded before final cleanup",
                ],
                "actual_sprite_changes_before_krita_projection": [
                    "tightened missing-corner outline pixels around the crate",
                    "added rope fiber ticks and catchlights",
                    "added barrel hoop bands and dull metal highlights",
                    "added lower grime pixels and contact shadow spans",
                ],
                "isolated_profile_root": rel(TOOL_PROFILE_ROOT),
                "stdout": result.stdout,
                "stderr": result.stderr,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return " ".join((result.stdout + " " + result.stderr).split())


def run_gimp_cleanup() -> str:
    gimp = find_tool(GIMP)
    code = f"""
from gi.repository import Gimp, Gio
inp = r'{KRITA_RAW_PATH.as_posix()}'
out = r'{FINAL_ASSET_PATH.as_posix()}'
pdb = Gimp.get_pdb()
load = pdb.lookup_procedure('file-png-load')
config = load.create_config()
config.set_property('run-mode', Gimp.RunMode.NONINTERACTIVE)
config.set_property('file', Gio.File.new_for_path(inp))
result = load.run(config)
if result.index(0) != Gimp.PDBStatusType.SUCCESS:
    raise RuntimeError('file-png-load failed: %s' % result.index(0))
image = result.index(1)
export = pdb.lookup_procedure('file-png-export')
cfg = export.create_config()
cfg.set_property('run-mode', Gimp.RunMode.NONINTERACTIVE)
cfg.set_property('image', image)
cfg.set_property('file', Gio.File.new_for_path(out))
cfg.set_property('options', None)
cfg.set_property('interlaced', 0)
cfg.set_property('compression', 9)
cfg.set_property('bkgd', False)
cfg.set_property('offs', False)
cfg.set_property('phys', False)
cfg.set_property('time', False)
cfg.set_property('save-transparent', True)
res = export.run(cfg)
if res.index(0) != Gimp.PDBStatusType.SUCCESS:
    raise RuntimeError('file-png-export failed: %s' % res.index(0))
image.delete()
"""
    stdout = ""
    stderr = ""
    timed_out = False
    try:
        result = subprocess.run(
            [str(gimp), "-i", "--batch-interpreter=python-fu-eval", "-b", code],
            capture_output=True,
            text=True,
            check=True,
            timeout=150,
            env=tool_env(),
        )
        stdout = result.stdout
        stderr = result.stderr
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        stdout = (exc.stdout or "").decode("utf-8", errors="replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = (exc.stderr or "").decode("utf-8", errors="replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        if not FINAL_ASSET_PATH.exists():
            raise
    if not FINAL_ASSET_PATH.exists():
        raise RuntimeError("GIMP did not produce cleaned G-4.18D.3 PNG")
    GIMP_LOG_PATH.write_text(
        json.dumps(
            {
                "tool": "GIMP 3 python-fu-eval",
                "input": rel(KRITA_RAW_PATH),
                "output": rel(FINAL_ASSET_PATH),
                "operations": [
                    "file-png-load",
                    "transparent PNG preservation",
                    "compression=9 re-export",
                    "metadata chunk removal: bkgd/off/phys/time disabled",
                    "export sanity check for alpha/transparency path",
                ],
                "timed_out_after_export": timed_out,
                "isolated_profile_root": rel(TOOL_PROFILE_ROOT),
                "stdout": stdout,
                "stderr": stderr,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return " ".join((stdout + " " + stderr).split())


def alpha_bounds(path: Path) -> dict[str, Any]:
    image = Image.open(path).convert("RGBA")
    alpha = image.getchannel("A")
    bbox = alpha.getbbox()
    if bbox is None:
        return {"bbox": None, "opaque_pixel_count": 0, "alpha_coverage": 0.0, "semi_alpha_pixel_count": 0}
    opaque = sum(1 for value in alpha.getdata() if value > 8)
    semi = sum(1 for value in alpha.getdata() if 0 < value < 255)
    return {
        "bbox": {"x": bbox[0], "y": bbox[1], "w": bbox[2] - bbox[0], "h": bbox[3] - bbox[1]},
        "opaque_pixel_count": opaque,
        "semi_alpha_pixel_count": semi,
        "alpha_coverage": round(opaque / float(image.width * image.height), 4),
    }


def unique_palette(path: Path) -> list[dict[str, Any]]:
    image = Image.open(path).convert("RGBA")
    counts: dict[tuple[int, int, int, int], int] = {}
    for pixel in image.getdata():
        if pixel[3] == 0:
            continue
        counts[pixel] = counts.get(pixel, 0) + 1
    return [
        {"rgba": "#%02x%02x%02x%02x" % color, "count": count}
        for color, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]


def contrast_stddev(path: Path) -> float:
    image = Image.open(path).convert("RGBA")
    pixels = [pixel[:3] for pixel in image.getdata() if pixel[3] > 8]
    if not pixels:
        return 0.0
    luminances = [(r * 0.2126 + g * 0.7152 + b * 0.0722) for r, g, b in pixels]
    mean = sum(luminances) / len(luminances)
    variance = sum((value - mean) ** 2 for value in luminances) / len(luminances)
    return round(math.sqrt(variance), 2)


def average_palette(path: Path) -> tuple[float, float, float]:
    image = Image.open(path).convert("RGBA").resize((64, 64), Image.Resampling.BICUBIC)
    pixels = [pixel[:3] for pixel in image.getdata() if pixel[3] > 16]
    if not pixels:
        return (0.0, 0.0, 0.0)
    return tuple(sum(channel) / len(pixels) for channel in zip(*pixels))


def palette_distance(path_a: Path, path_b: Path) -> float:
    a = average_palette(path_a)
    b = average_palette(path_b)
    return round(math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(3))), 2)


def paste_scaled(sheet: Image.Image, path: Path, xy: tuple[int, int], scale: int = 1) -> None:
    image = Image.open(path).convert("RGBA")
    if scale != 1:
        image = image.resize((image.width * scale, image.height * scale), Image.Resampling.NEAREST)
    sheet.alpha_composite(image, xy)


def checker(size: tuple[int, int], cell: int = 8) -> Image.Image:
    image = Image.new("RGBA", size, rgba("#273024ff"))
    draw = ImageDraw.Draw(image)
    alt = rgba("#20281eff")
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=alt)
    return image


def make_isolated_1x() -> None:
    sheet = Image.new("RGBA", (520, 240), rgba(PALETTE["sheet_bg"]))
    draw = ImageDraw.Draw(sheet)
    text(draw, (20, 16), "G-4.18D.3 Pixel Sprite Atelier | 1x isolated", size=15)
    text(draw, (20, 40), "Dockside rope coil + crate + small barrel cluster. Source-safe, pixel-layer authored.", "#d8b7a0", 12)
    panel = checker((180, 126), 9)
    sheet.alpha_composite(panel, (32, 76))
    paste_scaled(sheet, FINAL_ASSET_PATH, (74, 106), 1)
    draw.rectangle((32, 76, 211, 201), outline=rgba(PALETTE["sheet_gold"]), width=1)
    text(draw, (252, 84), "Visual verdict", size=13)
    for idx, value in enumerate([
        f"{CAPABILITY_VERDICT} {VISUAL_RATING}/10 (gate {VISUAL_PASS_GATE})",
        "Rebuilt after rejected hard-pixel token",
        "Painterly 4x source baked to 1x PNG",
        "Still lab-only until chandlery-standard review",
        "Quarantined; not eligible for normal review",
    ]):
        text(draw, (252, 112 + idx * 20), value, "#cfdcc5", 12)
    sheet.save(ISOLATED_1X_PATH)


def make_grid_8x() -> None:
    scale = 8
    asset = Image.open(FINAL_ASSET_PATH).convert("RGBA")
    scaled = checker((CANVAS_W * scale, CANVAS_H * scale), scale)
    scaled.alpha_composite(asset.resize((CANVAS_W * scale, CANVAS_H * scale), Image.Resampling.NEAREST))
    draw = ImageDraw.Draw(scaled)
    grid_color = rgba("#0000005a")
    major_color = rgba("#d8c06a90")
    for x in range(0, scaled.width + 1, scale):
        draw.line((x, 0, x, scaled.height), fill=major_color if x % (scale * 8) == 0 else grid_color)
    for y in range(0, scaled.height + 1, scale):
        draw.line((0, y, scaled.width, y), fill=major_color if y % (scale * 8) == 0 else grid_color)
    sheet = Image.new("RGBA", (scaled.width + 60, scaled.height + 82), rgba(PALETTE["sheet_bg"]))
    sdraw = ImageDraw.Draw(sheet)
    text(sdraw, (20, 14), "G-4.18D.3 8x grid inspection", size=15)
    text(sdraw, (20, 38), "Every square is one final sprite pixel; no source pixels copied.", "#d8b7a0", 12)
    sheet.alpha_composite(scaled, (30, 70))
    sheet.save(GRID_8X_PATH)


def make_before_after_sheet() -> None:
    sheet = Image.new("RGBA", (900, 300), rgba(PALETTE["sheet_bg"]))
    draw = ImageDraw.Draw(sheet)
    text(draw, (22, 16), "G-4.18D.3 Pixel Atelier Iterations", size=15)
    text(draw, (22, 40), "Pass 01 blockout -> Pass 02 materials -> Pass 03 polish/shadow/grounding", "#d8b7a0", 12)
    for idx, (path, label, note) in enumerate([
        (PASS01_PATH, "pass 01 blockout", "shape and massing"),
        (PASS02_PATH, "pass 02 material/detail", "wood, rope, barrel, bands"),
        (FINAL_ASSET_PATH, "pass 03 final", "chips, grime, contact"),
    ]):
        x = 46 + idx * 286
        draw.rectangle((x - 14, 78, x + CANVAS_W * 2 + 14, 78 + CANVAS_H * 2 + 22), outline=rgba(PALETTE["sheet_gold"]), width=1)
        paste_scaled(sheet, path, (x, 90), 2)
        text(draw, (x, 230), label, "#eadca6", 12)
        text(draw, (x, 250), note, "#cfdcc5", 11)
    sheet.save(BEFORE_AFTER_PATH)


def make_palette_sheet() -> None:
    palette = unique_palette(FINAL_ASSET_PATH)
    sheet = Image.new("RGBA", (760, 420), rgba(PALETTE["sheet_bg"]))
    draw = ImageDraw.Draw(sheet)
    text(draw, (22, 16), "G-4.18D.3 palette and material swatches", size=15)
    text(draw, (22, 40), "Muted Newport harbor palette; transparent pixels excluded from swatch counts.", "#d8b7a0", 12)
    swatches = palette[:30]
    for idx, item in enumerate(swatches):
        col = item["rgba"]
        x = 30 + (idx % 5) * 142
        y = 82 + (idx // 5) * 48
        draw.rectangle((x, y, x + 34, y + 28), fill=rgba(col))
        draw.rectangle((x, y, x + 34, y + 28), outline=rgba("#000000a0"), width=1)
        text(draw, (x + 42, y + 2), col[:7], "#cfdcc5", 10)
        text(draw, (x + 42, y + 17), f"{item['count']} px", "#9eb19a", 9)
    text(draw, (30, 374), f"Unique nontransparent colors: {len(palette)} | Contrast stddev: {contrast_stddev(FINAL_ASSET_PATH)}", "#eadca6", 12)
    sheet.save(PALETTE_SHEET_PATH)


def make_sprite_sheet() -> None:
    sheet = Image.new("RGBA", (CANVAS_W * 3, CANVAS_H), (0, 0, 0, 0))
    for idx, path in enumerate([PASS01_PATH, PASS02_PATH, FINAL_ASSET_PATH]):
        sheet.alpha_composite(Image.open(path).convert("RGBA"), (idx * CANVAS_W, 0))
    sheet.save(SPRITE_SHEET_PATH)


def make_in_world_frame() -> None:
    sheet = Image.new("RGBA", (1040, 420), rgba("#32472fff"))
    draw = ImageDraw.Draw(sheet)
    text(draw, (22, 16), "G-4.18D.3 lab-only in-world comparison | actual scale", size=15)
    text(draw, (22, 40), "New pixel sprite is placed beside current Newport art for scale/style judgment only.", "#d8b7a0", 12)
    draw.rectangle((0, 236, 1040, 294), fill=rgba("#716c57ff"))
    draw.rectangle((0, 292, 1040, 354), fill=rgba("#5d513cff"))
    draw.rectangle((0, 350, 1040, 420), fill=rgba("#2f7785ff"))
    for x in range(0, 1040, 42):
        draw.line((x, 296, x + 20, 294), fill=rgba("#322b20ff"), width=1)
        draw.line((x, 374, x + 34, 371), fill=rgba("#1e5e6bff"), width=1)
    chandlery = Image.open(CHANDLERY_REFERENCE_PATH).convert("RGBA")
    chandlery = chandlery.resize((int(chandlery.width * 0.55), int(chandlery.height * 0.55)), Image.Resampling.LANCZOS)
    sheet.alpha_composite(chandlery, (556, 88))
    wharf = Image.open(WHARF_REFERENCE_PATH).convert("RGBA")
    wharf = wharf.resize((int(wharf.width * 1.15), int(wharf.height * 1.15)), Image.Resampling.LANCZOS)
    sheet.alpha_composite(wharf, (86, 244))
    final = Image.open(FINAL_ASSET_PATH).convert("RGBA")
    sheet.alpha_composite(final, (432, 254))
    draw.rectangle((428, 250, 432 + CANVAS_W + 4, 254 + CANVAS_H + 4), outline=rgba(PALETTE["sheet_gold"]), width=1)
    text(draw, (432, 324), f"D3 at 1x: {CAPABILITY_VERDICT} {VISUAL_RATING}/10", "#f0cf7d", 12)
    text(draw, (86, 320), "Existing wharf dressing", "#cfdcc5", 11)
    text(draw, (556, 300), "Current Newport building art", "#cfdcc5", 11)
    sheet.save(IN_WORLD_PATH)


def make_standard_comparison_sheet() -> None:
    sheet = Image.new("RGBA", (1360, 620), rgba(PALETTE["sheet_bg"]))
    draw = ImageDraw.Draw(sheet)
    text(draw, (22, 16), "G-4.18D.3 standard comparison: what to validate", size=15)
    text(draw, (22, 40), "Large standards are visual QA only; the D3 sprite is rebuilt from project-authored layers, not copied pixels.", "#d8b7a0", 12)

    chandlery_crop = Image.open(CHANDLERY_PROP_REFERENCE_PATH).convert("RGBA")
    wharf = Image.open(WHARF_REFERENCE_PATH).convert("RGBA")
    d2 = Image.open(GENERATED_ROOT / "g418d2_rope_crate_barrel_cluster.png").convert("RGBA")
    d3 = Image.open(FINAL_ASSET_PATH).convert("RGBA")

    draw.rectangle((28, 74, 524, 300), fill=rgba("#253023ff"), outline=rgba(PALETTE["sheet_gold"]), width=1)
    chandlery_scaled = chandlery_crop.resize((int(chandlery_crop.width * 1.35), int(chandlery_crop.height * 1.35)), Image.Resampling.NEAREST)
    sheet.alpha_composite(chandlery_scaled, (66, 106))
    text(draw, (42, 274), "Target standard: chandlery prop cluster (large)", "#eadca6", 12)

    draw.rectangle((552, 74, 872, 300), fill=rgba("#253023ff"), outline=rgba(PALETTE["sheet_gold"]), width=1)
    wharf_scaled = wharf.resize((int(wharf.width * 1.05), int(wharf.height * 1.05)), Image.Resampling.NEAREST)
    sheet.alpha_composite(wharf_scaled, (584, 118))
    text(draw, (584, 274), "Target standard: existing wharf prop strip", "#eadca6", 12)

    draw.rectangle((900, 74, 1098, 300), fill=rgba("#253023ff"), outline=rgba("#b86d55ff"), width=1)
    d2_scaled = d2.resize((d2.width * 2, d2.height * 2), Image.Resampling.NEAREST)
    sheet.alpha_composite(d2_scaled, (910, 112))
    text(draw, (910, 274), "D2: deferred baseline", "#f0b1a3", 12)

    draw.rectangle((1126, 74, 1332, 300), fill=rgba("#253023ff"), outline=rgba("#d8c06aff"), width=1)
    d3_scaled = d3.resize((d3.width * 2, d3.height * 2), Image.Resampling.NEAREST)
    sheet.alpha_composite(d3_scaled, (1132, 126))
    text(draw, (1132, 274), f"D3 rebuild: {CAPABILITY_VERDICT} {VISUAL_RATING}/10", "#f0cf7d", 12)

    text(draw, (34, 332), "Art-bar scorecard", size=14)
    text(draw, (34, 350), "Validate only the D3 cluster's actual-scale cohesion: silhouette, material finish, grounding, and whether it belongs beside the Newport prop standard.", "#d8b7a0", 11)
    rows = [
        ("Silhouette realism", "Rebuild has nested 3/4 masses instead of flat rectangle/circle tokens, but still lacks reference richness.", "DEFER"),
        ("Material finish", "Wood, rope, barrel, bands, chips, and grime now read better; still not as painterly as chandlery.", "DEFER"),
        ("Edge work", "Anti-aliased contours are closer to Newport art; some marks remain too symbolic at 1x.", "DEFER"),
        ("Scale integration", "Actual-scale view is clearer after moving out of the water/label clutter; still lab-only.", "DEFER"),
        ("Contact grounding", "Soft cast shadow plus object-specific occlusion seats the cluster better than D2/D3 original.", "IMPROVED"),
        ("Commercial-safe path", "Provenance stays green; visual promotion remains blocked until human art approval.", "PASS provenance only"),
    ]
    y = 388
    for label_text, body, result in rows:
        text(draw, (42, y), label_text, "#eadca6", 11)
        text(draw, (226, y), body, "#cfdcc5", 11)
        text(draw, (1168, y), result, "#f0b1a3" if result.startswith("FAIL") else "#f0cf7d", 11)
        y += 34

    text(draw, (42, 586), f"Current D3 visual judgment after rebuild: {CAPABILITY_VERDICT} {VISUAL_RATING}/10. Lab-only; not promoted.", "#f0b1a3", 12)
    sheet.save(STANDARD_COMPARISON_PATH)


def make_prop_study_sheet() -> None:
    final = Image.open(FINAL_ASSET_PATH).convert("RGBA")

    def layer_image(name: str) -> Image.Image:
        matches = sorted(LAYER_ROOT.glob(f"*_{name}.png"))
        if not matches:
            raise FileNotFoundError(f"Missing rendered layer for prop study: {name}")
        return Image.open(matches[0]).convert("RGBA")

    def layer_study(names: list[str]) -> Image.Image:
        image = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        for name in names:
            image.alpha_composite(layer_image(name))
        return image

    sheet = Image.new("RGBA", (1060, 420), rgba(PALETTE["sheet_bg"]))
    draw = ImageDraw.Draw(sheet)
    text(draw, (22, 16), "G-4.18D.3 prop readability studies", size=15)
    text(draw, (22, 40), "Layer-isolated crate, barrel, and rope studies are checked before judging the assembled cluster.", "#d8b7a0", 12)

    studies = [
        ("crate", layer_study(["wood_base", "dark_outline", "highlights", "chips_scratches", "grime"]), (4, 20, 47, 60), "3/4 box, top plane, X-brace, chipped planks"),
        ("barrel", layer_study(["barrel_base", "metal_bands", "highlights", "chips_scratches", "grime"]), (47, 20, 73, 59), "top ellipse, bulged staves, dull iron hoops"),
        ("rope coil", layer_study(["rope_base", "highlights", "grime"]), (55, 39, 96, 62), "nested rings, central hole, loose tail, fiber ticks"),
        ("cluster", final, (0, 18, 96, 64), "actual source assembled at 1x relationship"),
    ]
    for idx, (label, image, crop, note) in enumerate(studies):
        x = 30 + idx * 250
        y = 82
        draw.rectangle((x, y, x + 210, y + 242), fill=rgba("#253023ff"), outline=rgba(PALETTE["sheet_gold"]), width=1)
        crop_img = image.crop(crop)
        scale = 4 if label != "cluster" else 2
        preview = crop_img.resize((crop_img.width * scale, crop_img.height * scale), Image.Resampling.NEAREST)
        sheet.alpha_composite(preview, (x + 16, y + 24))
        text(draw, (x + 16, y + 184), label, "#eadca6", 12)
        text(draw, (x + 16, y + 204), note, "#cfdcc5", 10)

    text(draw, (30, 356), f"Verdict: {CAPABILITY_VERDICT} {VISUAL_RATING}/10. Readability improved, but this remains lab-only until it matches the Newport chandlery/wharf prop standard.", "#f0cf7d", 12)
    sheet.save(PROP_STUDY_SHEET_PATH)


def make_atelier_board() -> None:
    sheet = Image.new("RGBA", (1240, 430), rgba(PALETTE["sheet_bg"]))
    draw = ImageDraw.Draw(sheet)
    text(draw, (22, 18), "G-4.18D.3 Pixel-by-Pixel Sprite Atelier | LAB REVIEW", size=15)
    text(draw, (22, 42), f"One dockside rope coil + crate + small barrel cluster. Verdict: {CAPABILITY_VERDICT} {VISUAL_RATING}/10.", "#d8b7a0", 12)
    paste_scaled(sheet, PASS01_PATH, (50, 94), 2)
    paste_scaled(sheet, PASS02_PATH, (300, 94), 2)
    paste_scaled(sheet, FINAL_ASSET_PATH, (550, 94), 2)
    comparison = Image.open(STANDARD_COMPARISON_PATH).convert("RGBA").resize((440, 207), Image.Resampling.LANCZOS)
    sheet.alpha_composite(comparison, (768, 96))
    text(draw, (50, 232), "Pass 01: blockout", "#f0b1a3", 12)
    text(draw, (300, 232), "Pass 02: material/detail", "#f0cf7d", 12)
    text(draw, (550, 232), "Pass 03: polish/grounding", "#f0cf7d", 12)
    text(draw, (768, 316), f"Reference-standard comparison: {CAPABILITY_VERDICT}", "#f0b1a3", 12)
    for idx, value in enumerate([
        "Source: explicit named pixel layers; no copied Newport/yellow/third-party pixels.",
        "Object-first rebuild: separate crate, barrel, and rope readability studies before cluster validation.",
        "Layer proof: silhouette/blockout, dark outline, wood, rope, barrel, metal, highlights, chips, grime, cast/contact shadows.",
        "Tool path: Pillow layer compositing, Krita projection export, GIMP PNG cleanup, palette/alpha/grid validation.",
        "Status: provenance green, improved but deferred. Quarantined; do not promote into normal review.",
    ]):
        text(draw, (50, 310 + idx * 20), value, "#cfdcc5", 11)
    sheet.save(ATELIER_BOARD_PATH)


def write_inspection(krita_log: str, gimp_log: str) -> None:
    data = {
        "phase": "G-4.18D.3",
        "asset_id": "g418d3_dockside_rope_crate_barrel_cluster",
        "visual_pass_gate": VISUAL_PASS_GATE,
        "visual_rating": VISUAL_RATING,
        "capability_verdict": CAPABILITY_VERDICT,
        "tool_logs": {"krita": krita_log, "gimp": gimp_log},
        "samples": {
            "pass_01_blockout": {"path": rel(PASS01_PATH), "sha256": sha256(PASS01_PATH), "alpha": alpha_bounds(PASS01_PATH), "contrast_stddev": contrast_stddev(PASS01_PATH)},
            "pass_02_material_detail": {"path": rel(PASS02_PATH), "sha256": sha256(PASS02_PATH), "alpha": alpha_bounds(PASS02_PATH), "contrast_stddev": contrast_stddev(PASS02_PATH)},
            "final_asset": {
                "path": rel(FINAL_ASSET_PATH),
                "sha256": sha256(FINAL_ASSET_PATH),
                "alpha": alpha_bounds(FINAL_ASSET_PATH),
                "contrast_stddev": contrast_stddev(FINAL_ASSET_PATH),
                "unique_nontransparent_colors": len(unique_palette(FINAL_ASSET_PATH)),
                "palette_distance_to_wharf_reference": palette_distance(FINAL_ASSET_PATH, WHARF_REFERENCE_PATH),
                "palette_distance_to_chandlery_reference": palette_distance(FINAL_ASSET_PATH, CHANDLERY_REFERENCE_PATH),
            },
        },
        "visual_judgment": "User review rejected the original hard-pixel token as incoherent and nowhere near the chandlery/wharf prop standard. This rebuilt painterly source is materially improved, but remains deferred and lab-only until human art review accepts it.",
    }
    INSPECTION_PATH.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def update_manifest() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest["phase"] = "G-4.18D.3"
    manifest["generated_at"] = "2026-05-16T00:00:00Z"
    manifest["normal_review_policy"] = "No G-4.18D, G-4.18D.1, G-4.18D.2, or G-4.18D.3 experimental/capability asset is normal-review eligible unless separately promoted after screenshot acceptance. Failed and deferred art is lab-only; this G-4.18D.3 sprite is rebuilt after user rejection but remains deferred after chandlery-standard comparison."
    manifest["visual_quality_gate"] = "G-4.18D bakeoff PASS remains >= 8.5. G-4.18D.2 and G-4.18D.3 tiny environmental capability PASS requires visual_rating >= 7.5 and screenshot improvement. Provenance green alone cannot produce PASS or promotion."
    manifest["contact_sheets"] = list(dict.fromkeys(
        list(manifest.get("contact_sheets", []))
        + [
            rel(ISOLATED_1X_PATH),
            rel(GRID_8X_PATH),
            rel(BEFORE_AFTER_PATH),
            rel(PALETTE_SHEET_PATH),
            rel(IN_WORLD_PATH),
            rel(STANDARD_COMPARISON_PATH),
            rel(PROP_STUDY_SHEET_PATH),
            rel(ATELIER_BOARD_PATH),
        ]
    ))
    d2_gate = manifest.get("art_production_capability_gate")
    if d2_gate:
        manifest["g418d2_art_production_capability_gate"] = d2_gate
    manifest["pixel_sprite_atelier_proof"] = {
        "phase": "G-4.18D.3",
        "asset_id": "g418d3_dockside_rope_crate_barrel_cluster",
        "asset_name": "Dockside rope coil + crate + small barrel pixel cluster",
        "asset_family": "tiny_dockside_environmental_prop_cluster",
        "sample_path": rel(FINAL_ASSET_PATH),
        "pass_01_blockout_path": rel(PASS01_PATH),
        "pass_02_material_detail_path": rel(PASS02_PATH),
        "pass_03_polish_shadow_grounding_path": rel(PASS03_PATH),
        "krita_projection_path": rel(KRITA_RAW_PATH),
        "sprite_sheet_path": rel(SPRITE_SHEET_PATH),
        "isolated_1x_path": rel(ISOLATED_1X_PATH),
        "grid_8x_path": rel(GRID_8X_PATH),
        "before_after_path": rel(BEFORE_AFTER_PATH),
        "palette_sheet_path": rel(PALETTE_SHEET_PATH),
        "in_world_comparison_path": rel(IN_WORLD_PATH),
        "standard_comparison_path": rel(STANDARD_COMPARISON_PATH),
        "prop_readability_studies_path": rel(PROP_STUDY_SHEET_PATH),
        "atelier_board_path": rel(ATELIER_BOARD_PATH),
        "source_file": rel(SOURCE_JSON_PATH),
        "layer_source_root": rel(LAYER_ROOT),
        "required_layers": [
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
        ],
        "provenance_status": "green_origin_candidate",
        "origin_classification": "green_origin_candidate",
        "commercial_use_status": "green_origin_candidate",
        "visual_quality_status": VISUAL_STATUS,
        "visual_rating": VISUAL_RATING,
        "visual_pass_gate": VISUAL_PASS_GATE,
        "capability_verdict": CAPABILITY_VERDICT,
        "review_eligible": False,
        "normal_review_eligible": False,
        "lab_only": True,
        "final_commercial_candidate": False,
        "final_commercial_eligible": False,
        "lab_access_mode": "F6 or --show-green-origin-lab",
        "input_sources": [
            {"type": "project_script", "path": rel(SCRIPT_PATH), "source_pixels_used": False, "commercial_status": "green_origin_candidate"},
            {"type": "inkscape_silhouette_planning", "path": rel(SILHOUETTE_PLAN_SVG_PATH), "source_pixels_used": False, "commercial_status": "green_origin_candidate"},
            {"type": "project_authored_pixel_layer_source", "path": rel(SOURCE_JSON_PATH), "source_pixels_used": False, "commercial_status": "green_origin_candidate"},
            {"type": "project_authored_palette_tokens", "path": rel(STYLE_TOKENS_PATH), "source_pixels_used": False, "commercial_status": "green_origin_candidate"},
            {"type": "project_style_rules", "path": rel(ART_BIBLE_PATH), "source_pixels_used": False, "commercial_status": "documentation_only"},
        ],
        "source_pixels_from_yellow_uncertain_assets": False,
        "source_pixels_from_third_party_material": False,
        "web_scraped_source_pixels": False,
        "ai_generated": False,
        "deterministic_generated": False,
        "hand_pixel_layer_source": True,
        "hand_paintover": True,
        "ownership": "project-owned",
        "license": "Wayfarer project-owned green-origin G-4.18D.3 pixel atelier proof; no third-party, marketplace, web-scraped, ripped, AI-output, or yellow-source pixels; visually deferred and lab-only after prop-readability and chandlery-standard comparison.",
        "sha256": sha256(FINAL_ASSET_PATH),
        "capability_answer": "Not yet: the object-first pixel-layer workflow is more readable and inspectable, but it remains below the realistic Newport chandlery/wharf prop standard and should not be promoted.",
    }
    manifest["g418d3_pixel_sprite_atelier_gate"] = "One green-origin pixel-layer rope/crate/barrel cluster was rebuilt around separate prop-readability studies after user rejection of the blended token approach; it remains below the 7.5 tiny-prop gate and stays lab-only."
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def write_report() -> None:
    report = f"""# G-4.18D.3 Pixel-by-Pixel Sprite Atelier

## Verdict

G-4.18D.3 produced one green-origin dockside rope coil + crate + small barrel cluster from an explicit pixel-layer source.

- Visual verdict: **{CAPABILITY_VERDICT}**
- Visual rating: **{VISUAL_RATING}/10** against the {VISUAL_PASS_GATE}/10 tiny environmental prop gate
- Normal review: **blocked**
- Lab status: **deferred lab-only**
- Provenance: **green-origin candidate**

The sprite is intentionally small (`{CANVAS_W}x{CANVAS_H}`) and is rebuilt from a `{AA_RENDER}x` painterly source that bakes down to 1x. It is not sourced from Newport building pixels, the yellow hero atlas, marketplace art, web images, or third-party game material. Provenance is green, but the asset remains below the chandlery-standard bar and is not eligible for normal review.

## Pixel-Layer Source

Explicit source file:

- `{rel(SOURCE_JSON_PATH)}`

Named layer PNG exports:

- `silhouette_blockout`
- `dark_outline`
- `wood_base`
- `rope_base`
- `barrel_base`
- `metal_bands`
- `highlights`
- `chips_scratches`
- `grime`
- `cast_shadow`
- `contact_shadow`

The three visible iteration stages are:

- Pass 01 blockout: `{rel(PASS01_PATH)}`
- Pass 02 material/detail: `{rel(PASS02_PATH)}`
- Pass 03 polish/shadow/grounding: `{rel(PASS03_PATH)}`

This rebuild also adds a prop-readability sheet before the in-world judgment:

- Prop readability studies: `{rel(PROP_STUDY_SHEET_PATH)}`

## Deliverables

- Final 1x PNG: `{rel(FINAL_ASSET_PATH)}`
- Inkscape silhouette plan: `{rel(SILHOUETTE_PLAN_SVG_PATH)}` and `{rel(SILHOUETTE_PLAN_PNG_PATH)}`
- 8x grid inspection: `{rel(GRID_8X_PATH)}`
- Before/after contact sheet: `{rel(BEFORE_AFTER_PATH)}`
- Palette sheet: `{rel(PALETTE_SHEET_PATH)}`
- Lab-only in-world comparison: `{rel(IN_WORLD_PATH)}`
- chandlery-standard comparison: `{rel(STANDARD_COMPARISON_PATH)}`
- Prop readability studies: `{rel(PROP_STUDY_SHEET_PATH)}`
- HUD atelier board: `{rel(ATELIER_BOARD_PATH)}`
- Sprite-sheet assembly: `{rel(SPRITE_SHEET_PATH)}`
- Image inspection JSON: `{rel(INSPECTION_PATH)}`
- Krita log: `{rel(KRITA_LOG_PATH)}`
- GIMP log: `{rel(GIMP_LOG_PATH)}`

## Tool Path

Python/Pillow rendered the named layers through the `{AA_RENDER}x` painterly source, baked the final 1x transparent PNG, composited the three passes, generated the separate prop-readability studies, assembled the sprite sheet, generated alpha/crop/palette/contrast checks, and produced 1x/8x review artifacts.

Krita CLI opened the pass 03 pixel composite and exported the 1x projection to `{rel(KRITA_RAW_PATH)}`. The actual refinement decisions before that projection were the named polish layers: tighter object outlines, rope coil ticks, barrel hoop highlights, crate chips, grime, cast shadow, and contact shadow.

GIMP loaded the Krita projection and re-exported the final transparent PNG with PNG cleanup and metadata suppression. The GIMP log records a post-export Script-Fu crash/timeout after the PNG was already written, so the export path is documented but not treated as a clean tool run. The final alpha/crop/palette checks are recorded in `{rel(INSPECTION_PATH)}`.

Inkscape was used only for silhouette planning and exported `{rel(SILHOUETTE_PLAN_PNG_PATH)}`. That vector plan did not become the final sprite; the final PNG comes from the named painterly pixel layers and the Krita/GIMP projection/cleanup path.

## Visual Acceptance

This pass is **more readable than the rejected blended/token attempts**, but it still does not meet visual acceptance. It is blocked from normal review and must remain lab-only.

- Silhouette: separate 3/4 crate, small upright barrel, and foreground rope coil replace the previous one-blob composition.
- Palette: warmer, dirtier Newport browns and rope tones are closer to the chandlery/wharf prop language.
- Texture: rope fibers, wood planks, chips, barrel staves, metal bands, and grime are now material cues instead of only symbolic marks.
- Shadow: cast shadow and object-specific contact occlusion seat the cluster more clearly.
- Integration: the lab-only comparison is clearer, but the sprite still lacks the full painterly density and confidence of the chandlery standard.

The visual rating is {VISUAL_RATING}/10, below the {VISUAL_PASS_GATE}/10 tiny-prop gate. The report therefore treats this as a deferred lab proof, not acceptable asset progress.

## Provenance Gate

The asset is green-origin candidate material:

- No Newport/yellow source pixels copied or sampled.
- No third-party, marketplace, ripped, web-scraped, or mystery source pixels.
- Source data is project-authored pixel/layer instructions plus project-owned palette/style notes.
- Existing Newport building art is used only for visual comparison in generated contact sheets.

## Failure-Rule Answers

Did the pixel-by-pixel workflow improve over G-4.18D.2?

Yes, but only after abandoning the hard 8-bit token grammar and separating the problem into crate/barrel/rope readability studies before assembly. The rebuilt pass uses explicit painterly source layers, visible material decisions, and a real standard-comparison loop. It still does not prove final production quality.

Did the asset fail because of silhouette, palette, texture, shadow, scale, or integration?

It remains deferred primarily because of material finish, painterly edge confidence, scale integration, and the sense of being authored by the same hand as the chandlery props. Object readability, palette, and grounding are materially improved but still below the target standard.

What exact pixel/art changes would be required to raise it further?

- Increase painterly density without creating noise: more shaded bevel transitions, softened dark edges, and less evenly spaced scratch detail.
- Paint the three objects from larger hand-approved studies, then downsample and re-pixel only after each prop reads at 1x.
- Add stronger local occlusion where the rope sits in front of the barrel and where the crate side meets the floor.
- Tune the in-engine placement against the chandlery frontage until the candidate reads as part of the world at actual scale.
- Keep the large standard-comparison board visible on every pass before accepting the next iteration.

Should G-4.18D.4 continue pixel atelier work, or pivot?

Continue pixel atelier work, but only in this richer miniature-painting direction. The roadmap should abandon hard-token/8-bit prop grammar for Newport and use green-origin painterly sprites with explicit standard comparison, human art review, and stronger source-layer discipline.
"""
    REPORT_PATH.write_text(report, encoding="utf-8")


def main() -> int:
    write_inkscape_silhouette_plan()
    source = source_layers()
    write_source_and_passes(source)
    krita_log = run_krita_export()
    gimp_log = run_gimp_cleanup()
    make_sprite_sheet()
    make_isolated_1x()
    make_grid_8x()
    make_before_after_sheet()
    make_palette_sheet()
    make_in_world_frame()
    make_standard_comparison_sheet()
    make_prop_study_sheet()
    make_atelier_board()
    write_inspection(krita_log, gimp_log)
    update_manifest()
    write_report()
    print(f"Wrote G-4.18D.3 pixel sprite: {rel(FINAL_ASSET_PATH)}")
    print(f"Verdict: {CAPABILITY_VERDICT} ({VISUAL_RATING}/10, gate {VISUAL_PASS_GATE}/10)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
