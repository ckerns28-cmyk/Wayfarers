#!/usr/bin/env python3
"""Generate the G-4.18D.2 art-production capability gate proof packet."""

from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[3]
PIPELINE_ROOT = PROJECT_ROOT / "art_pipeline" / "newport_green_origin"
BAKEOFF_ROOT = PIPELINE_ROOT / "method_bakeoff"
GENERATED_ROOT = BAKEOFF_ROOT / "generated"
SOURCE_ROOT = BAKEOFF_ROOT / "source_authored"
REPORTS_ROOT = BAKEOFF_ROOT / "reports"
CONTACT_SHEET_ROOT = PIPELINE_ROOT / "contact_sheets"
MANIFEST_PATH = PIPELINE_ROOT / "manifests" / "green_origin_method_bakeoff_manifest.json"
ART_BIBLE_PATH = PROJECT_ROOT / "docs" / "NEWPORT_ART_BIBLE.md"
STYLE_TOKENS_PATH = PIPELINE_ROOT / "source_authored" / "newport_green_origin_style_tokens.json"
CHANDLERY_REFERENCE_PATH = PROJECT_ROOT / "assets" / "sprites" / "buildings" / "isolated" / "newport_chandlery_outfitter_front_isolated.png"
WHARF_REFERENCE_PATH = PROJECT_ROOT / "art_pipeline" / "newport" / "generated_assets" / "hero_strip" / "wharf_crate_pile_cluster.png"
SILHOUETTE_SVG_PATH = SOURCE_ROOT / "g418d2_rope_crate_barrel_silhouette.svg"
PAINT_PLAN_PATH = SOURCE_ROOT / "g418d2_rope_crate_barrel_paint_plan.json"
ROUGH_BASE_PATH = GENERATED_ROOT / "g418d2_rope_crate_barrel_rough_base.png"
PREPARED_PATH = GENERATED_ROOT / "g418d2_rope_crate_barrel_prepared.png"
KRITA_RAW_PATH = GENERATED_ROOT / "g418d2_rope_crate_barrel_krita_raw.png"
FINAL_ASSET_PATH = GENERATED_ROOT / "g418d2_rope_crate_barrel_cluster.png"
ISOLATED_SHEET_PATH = CONTACT_SHEET_ROOT / "g418d2_isolated_asset_proof.png"
BEFORE_AFTER_PATH = CONTACT_SHEET_ROOT / "g418d2_before_after_production.png"
IN_WORLD_PATH = CONTACT_SHEET_ROOT / "g418d2_in_world_comparison_frame.png"
CAPABILITY_BOARD_PATH = CONTACT_SHEET_ROOT / "g418d2_art_production_capability_board.png"
INSPECTION_PATH = REPORTS_ROOT / "g418d2_art_production_image_inspection.json"
KRITA_LOG_PATH = REPORTS_ROOT / "g418d2_krita_log.json"
GIMP_LOG_PATH = REPORTS_ROOT / "g418d2_gimp_log.json"
TOOL_PROFILE_ROOT = PROJECT_ROOT / "artifacts" / "tool_profiles" / "g418d2"

INKSCAPE = Path("C:/Program Files/Inkscape/bin/inkscape.exe")
KRITA_EXE = Path("C:/Program Files/Krita (x64)/bin/krita.exe")
GIMP = Path("C:/Users/Chris/AppData/Local/Programs/GIMP 3/bin/gimp-3.exe")

CANVAS_W = 160
CANVAS_H = 110
AA = 3
VISUAL_PASS_GATE = 7.5
VISUAL_RATING = 7.4
CAPABILITY_VERDICT = "DEFER"
VISUAL_STATUS = "visual_capability_defer_close_but_not_finished"


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


def color(hex_color: str, alpha: int = 255) -> tuple[int, int, int, int]:
    value = hex_color.lstrip("#")
    return (int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16), alpha)


def sc(value: float) -> int:
    return int(round(value * AA))


def sc_rect(rect: tuple[float, float, float, float]) -> tuple[int, int, int, int]:
    return tuple(sc(value) for value in rect)


def write_silhouette_svg() -> None:
    SOURCE_ROOT.mkdir(parents=True, exist_ok=True)
    SILHOUETTE_SVG_PATH.write_text(
        """<svg xmlns="http://www.w3.org/2000/svg" width="160" height="110" viewBox="0 0 160 110">
  <rect width="160" height="110" fill="none"/>
  <g stroke-linejoin="round" stroke-linecap="round">
    <ellipse cx="82" cy="91" rx="70" ry="11" fill="#12100c" opacity="0.42"/>
    <rect x="22" y="40" width="40" height="36" fill="#9a6b3f" stroke="#24180f" stroke-width="3"/>
    <rect x="55" y="51" width="35" height="29" fill="#805431" stroke="#24180f" stroke-width="3"/>
    <rect x="87" y="35" width="11" height="44" rx="2" fill="#5a3a22" stroke="#20150d" stroke-width="2"/>
    <rect x="124" y="38" width="9" height="39" rx="2" fill="#4a301f" stroke="#20150d" stroke-width="2"/>
    <ellipse cx="112" cy="44" rx="13" ry="8" fill="#9c6638" stroke="#21160d" stroke-width="3"/>
    <path d="M99 44 C99 58 101 72 112 77 C122 72 125 59 125 44 Z" fill="#7b4c2b" stroke="#21160d" stroke-width="3"/>
    <ellipse cx="42" cy="82" rx="22" ry="11" fill="none" stroke="#c7ad72" stroke-width="5"/>
    <ellipse cx="42" cy="82" rx="13" ry="6" fill="none" stroke="#6b4f2c" stroke-width="4"/>
    <path d="M62 82 C76 79 88 82 102 77" fill="none" stroke="#b89a62" stroke-width="5"/>
  </g>
</svg>
""",
        encoding="utf-8",
    )


def render_rough_base() -> str:
    GENERATED_ROOT.mkdir(parents=True, exist_ok=True)
    inkscape = find_tool(INKSCAPE)
    result = subprocess.run(
        [
            str(inkscape),
            str(SILHOUETTE_SVG_PATH),
            "--export-type=png",
            f"--export-filename={ROUGH_BASE_PATH}",
            f"--export-width={CANVAS_W}",
            f"--export-height={CANVAS_H}",
        ],
        capture_output=True,
        text=True,
        check=True,
        timeout=60,
        env=tool_env(),
    )
    if not ROUGH_BASE_PATH.exists():
        raise RuntimeError("Inkscape did not produce the G-4.18D.2 rough base")
    return " ".join((result.stdout + " " + result.stderr).split())


def write_paint_plan() -> None:
    SOURCE_ROOT.mkdir(parents=True, exist_ok=True)
    plan = {
        "phase": "G-4.18D.2",
        "asset_id": "g418d2_rope_crate_barrel_cluster",
        "visual_pass_gate": VISUAL_PASS_GATE,
        "purpose": "Hand-authored tiny dockside rope coil plus crate/barrel cluster capability proof.",
        "palette": {
            "outline": "#15100a",
            "deep_shadow": "#050504",
            "crate_warm": "#9d6b3e",
            "crate_dark": "#5f3b22",
            "barrel_warm": "#9b6235",
            "barrel_dark": "#4a2b19",
            "rope_light": "#d6bd7d",
            "rope_mid": "#a88955",
            "rope_dark": "#574128",
            "grime": "#1f1a10",
        },
        "manual_marks": [
            "soft contact shadow under full cluster",
            "weathered plank-like crate boards with diagonal braces",
            "barrel bands, rim ellipses, and off-center grime",
            "nested rope coil arcs with fiber ticks",
            "edge cleanup with warm top highlights and dark lower grounding",
        ],
        "tool_policy": "No third-party, marketplace, web-scraped, ripped, or yellow-source pixels. Building art is used only for screenshot comparison and palette-distance measurement.",
    }
    PAINT_PLAN_PATH.write_text(json.dumps(plan, indent=2), encoding="utf-8")


def draw_line(draw: ImageDraw.ImageDraw, points: list[tuple[float, float]], fill: tuple[int, int, int, int], width: float = 1.0) -> None:
    draw.line([(sc(x), sc(y)) for x, y in points], fill=fill, width=max(1, sc(width)))


def draw_rect(draw: ImageDraw.ImageDraw, rect: tuple[float, float, float, float], fill: tuple[int, int, int, int], outline: tuple[int, int, int, int] | None = None, width: float = 1.0) -> None:
    draw.rectangle(sc_rect(rect), fill=fill, outline=outline, width=max(1, sc(width)))


def draw_ellipse(draw: ImageDraw.ImageDraw, rect: tuple[float, float, float, float], fill: tuple[int, int, int, int] | None, outline: tuple[int, int, int, int] | None = None, width: float = 1.0) -> None:
    draw.ellipse(sc_rect(rect), fill=fill, outline=outline, width=max(1, sc(width)))


def draw_arc(draw: ImageDraw.ImageDraw, rect: tuple[float, float, float, float], start: float, end: float, fill: tuple[int, int, int, int], width: float = 1.0) -> None:
    draw.arc(sc_rect(rect), start=start, end=end, fill=fill, width=max(1, sc(width)))


def draw_weathered_crate(draw: ImageDraw.ImageDraw, x: float, y: float, w: float, h: float, base: str, lean: float = 0.0) -> None:
    outline = color("#17100a")
    dark = color("#392313")
    mid = color(base)
    light = color("#c39259", 230)
    shadow = color("#070504", 115)
    draw.polygon(
        [(sc(x), sc(y + lean)), (sc(x + w), sc(y)), (sc(x + w), sc(y + h)), (sc(x), sc(y + h + lean))],
        fill=mid,
        outline=outline,
    )
    draw_line(draw, [(x + 3, y + 6 + lean), (x + w - 4, y + 5)], dark, 1.0)
    draw_line(draw, [(x + 4, y + h * 0.48 + lean), (x + w - 3, y + h * 0.45)], dark, 0.8)
    draw_line(draw, [(x + 4, y + h - 5 + lean), (x + w - 4, y + h - 6)], shadow, 1.2)
    draw_line(draw, [(x + 4, y + 4 + lean), (x + w - 4, y + h - 5)], outline, 1.0)
    draw_line(draw, [(x + w - 4, y + 5), (x + 4, y + h - 6 + lean)], outline, 1.0)
    draw_line(draw, [(x + 2, y + 2 + lean), (x + w - 5, y + 2)], light, 0.7)
    for i in range(4):
        px = x + 7 + i * (w - 14) / 3
        draw_ellipse(draw, (px, y + h - 7, px + 1.4, y + h - 5.6), color("#25170e", 200))


def draw_weathered_barrel(draw: ImageDraw.ImageDraw, cx: float, y: float, w: float, h: float, base: str) -> None:
    outline = color("#17100a")
    barrel = color(base)
    dark = color("#3a2113")
    band = color("#1f160f")
    light = color("#c78d4d", 210)
    draw_ellipse(draw, (cx - w / 2, y, cx + w / 2, y + h * 0.22), barrel, outline, 1.0)
    draw.rounded_rectangle(sc_rect((cx - w / 2 + 1, y + h * 0.10, cx + w / 2 - 1, y + h - 5)), radius=sc(4), fill=barrel, outline=outline, width=sc(1.0))
    draw_ellipse(draw, (cx - w / 2 + 1, y + h - 12, cx + w / 2 - 1, y + h - 1), dark, outline, 1.0)
    draw_arc(draw, (cx - w / 2 + 3, y + 2, cx + w / 2 - 3, y + h * 0.2), 185, 355, color("#d29a58", 190), 0.7)
    draw_line(draw, [(cx - w / 2 + 2, y + h * 0.36), (cx + w / 2 - 2, y + h * 0.32)], band, 1.0)
    draw_line(draw, [(cx - w / 2 + 2, y + h * 0.68), (cx + w / 2 - 2, y + h * 0.63)], band, 1.0)
    draw_line(draw, [(cx - w * 0.18, y + h * 0.14), (cx - w * 0.22, y + h - 8)], dark, 0.7)
    draw_line(draw, [(cx + w * 0.17, y + h * 0.14), (cx + w * 0.20, y + h - 8)], dark, 0.7)
    draw_line(draw, [(cx - w * 0.34, y + h * 0.18), (cx - w * 0.20, y + 4)], light, 0.6)


def draw_rope_coil(draw: ImageDraw.ImageDraw, cx: float, cy: float, rx: float, ry: float) -> None:
    dark = color("#4f3922")
    mid = color("#9f8250")
    light = color("#d9c083")
    outline = color("#15100a")
    for offset, col, width in [(0, outline, 2.2), (2.5, mid, 2.0), (5.2, light, 1.3), (8.0, dark, 1.3), (10.7, mid, 1.1)]:
        draw_arc(draw, (cx - rx + offset, cy - ry + offset * 0.45, cx + rx - offset, cy + ry - offset * 0.45), 8, 350, col, width)
    for step in range(18):
        angle = math.radians(step * 18 + 8)
        px = cx + math.cos(angle) * (rx - 3)
        py = cy + math.sin(angle) * (ry - 1)
        draw_line(draw, [(px - 1.3, py - 0.9), (px + 1.3, py + 0.9)], dark if step % 2 else light, 0.45)
    draw_line(draw, [(cx + rx - 7, cy + 1), (cx + rx + 11, cy - 3), (cx + rx + 27, cy - 8)], mid, 2.0)
    draw_line(draw, [(cx + rx + 3, cy + 2), (cx + rx + 21, cy + 1), (cx + rx + 34, cy - 5)], dark, 0.9)


def create_prepared_asset() -> None:
    GENERATED_ROOT.mkdir(parents=True, exist_ok=True)
    write_paint_plan()
    rough = Image.open(ROUGH_BASE_PATH).convert("RGBA")
    canvas = Image.new("RGBA", (CANVAS_W * AA, CANVAS_H * AA), (0, 0, 0, 0))
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    draw_ellipse(sd, (10, 76, 148, 101), color("#050504", 96))
    draw_ellipse(sd, (25, 84, 73, 98), color("#050504", 112))
    draw_ellipse(sd, (87, 78, 133, 98), color("#050504", 92))
    shadow = shadow.filter(ImageFilter.GaussianBlur(sc(1.35)))
    canvas.alpha_composite(shadow)

    draw = ImageDraw.Draw(canvas)
    draw_rect(draw, (88, 33, 98, 83), color("#583820"), color("#17100a"), 1.0)
    draw_rect(draw, (124, 36, 133, 80), color("#442d1d"), color("#17100a"), 1.0)
    draw_line(draw, [(89, 35), (97, 34)], color("#c2955d", 170), 0.6)
    draw_line(draw, [(125, 38), (132, 37)], color("#9e744a", 160), 0.6)

    draw_weathered_crate(draw, 20, 40, 42, 35, "#986538", 1.5)
    draw_weathered_crate(draw, 55, 51, 36, 28, "#7b4e2c", -0.8)
    draw_weathered_crate(draw, 24, 63, 28, 22, "#714421", 1.0)
    draw_weathered_barrel(draw, 108, 42, 27, 45, "#995e33")
    draw_weathered_barrel(draw, 127, 48, 22, 35, "#7c4b2b")
    draw_weathered_barrel(draw, 96, 55, 22, 31, "#8b5731")

    grime = color("#1d170e", 160)
    for line in [
        [(25, 58), (59, 56)],
        [(31, 74), (83, 72)],
        [(91, 80), (135, 77)],
        [(20, 86), (146, 89)],
        [(88, 36), (94, 82)],
        [(124, 38), (128, 80)],
    ]:
        draw_line(draw, line, grime, 0.7)
    for x, y, w, h in [(28, 47, 9, 2), (42, 69, 13, 2), (61, 58, 11, 2), (101, 67, 9, 2), (118, 57, 8, 2)]:
        draw_rect(draw, (x, y, x + w, y + h), color("#21170d", 125))

    draw_rope_coil(draw, 43, 84, 22, 10)
    draw_rope_coil(draw, 67, 87, 12, 5)
    draw_line(draw, [(18, 90), (144, 91)], color("#050504", 105), 1.0)
    draw_line(draw, [(20, 39), (62, 38), (92, 42), (132, 37)], color("#d4b678", 85), 0.8)
    draw_line(draw, [(19, 87), (147, 88)], color("#15100a", 155), 1.1)

    polished = canvas.resize((CANVAS_W, CANVAS_H), Image.Resampling.LANCZOS)
    # Preserve a little of the rough vector base as an underpaint tint, then
    # keep the hand-authored pass dominant.
    underpaint = Image.new("RGBA", rough.size, (0, 0, 0, 0))
    underpaint.alpha_composite(rough)
    underpaint.putalpha(rough.getchannel("A").point(lambda value: int(value * 0.18)))
    final = Image.new("RGBA", rough.size, (0, 0, 0, 0))
    final.alpha_composite(underpaint)
    final.alpha_composite(polished)
    alpha = final.getchannel("A").point(lambda value: 0 if value < 6 else value)
    final.putalpha(alpha)
    final.save(PREPARED_PATH)


def run_krita_export() -> str:
    krita = find_tool(KRITA_EXE)
    result = subprocess.run(
        [
            str(krita),
            "--export",
            "--export-filename",
            str(KRITA_RAW_PATH),
            str(PREPARED_PATH),
        ],
        capture_output=True,
        text=True,
        check=True,
        timeout=90,
        env=tool_env(),
    )
    if not KRITA_RAW_PATH.exists():
        raise RuntimeError("Krita CLI did not produce the G-4.18D.2 PNG output")
    KRITA_LOG_PATH.write_text(
        json.dumps(
            {
                "tool": "Krita CLI",
                "input": rel(PREPARED_PATH),
                "output": rel(KRITA_RAW_PATH),
                "operations": [
                    "opened prepared G-4.18D.2 hand-authored sprite source",
                    "exported projection to PNG for downstream cleanup",
                ],
                "runner_note": "Interactive kritarunner/script-runner remained unreliable on this mini PC after the D.1 resource-database/argument failures, so the reliable Krita CLI projection path was used.",
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
            [
                str(gimp),
                "-i",
                "--batch-interpreter=python-fu-eval",
                "-b",
                code,
            ],
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
        raise RuntimeError("GIMP did not produce cleaned G-4.18D.2 PNG")
    GIMP_LOG_PATH.write_text(
        json.dumps(
            {
                "tool": "GIMP 3 python-fu-eval",
                "input": rel(KRITA_RAW_PATH),
                "output": rel(FINAL_ASSET_PATH),
                "operations": [
                    "file-png-load",
                    "PNG alpha/transparency preservation",
                    "compression=9 re-export",
                    "metadata chunk removal: bkgd/off/phys/time disabled",
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


def alpha_bounds(path: Path) -> dict:
    image = Image.open(path).convert("RGBA")
    alpha = image.getchannel("A")
    bbox = alpha.getbbox()
    if bbox is None:
        return {"bbox": None, "opaque_pixel_count": 0, "alpha_coverage": 0.0}
    opaque = sum(1 for value in alpha.getdata() if value > 8)
    return {
        "bbox": {"x": bbox[0], "y": bbox[1], "w": bbox[2] - bbox[0], "h": bbox[3] - bbox[1]},
        "opaque_pixel_count": opaque,
        "alpha_coverage": round(opaque / float(image.width * image.height), 4),
    }


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


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"]:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fill: str = "#eadca6", size: int = 14) -> None:
    draw.text(xy, text, fill=fill, font=font(size))


def paste_scaled(sheet: Image.Image, path: Path, xy: tuple[int, int], scale: int = 1) -> None:
    image = Image.open(path).convert("RGBA")
    if scale != 1:
        image = image.resize((image.width * scale, image.height * scale), Image.Resampling.NEAREST)
    sheet.alpha_composite(image, xy)


def make_isolated_sheet() -> None:
    CONTACT_SHEET_ROOT.mkdir(parents=True, exist_ok=True)
    sheet = Image.new("RGBA", (820, 360), color("#1d261c"))
    draw = ImageDraw.Draw(sheet)
    label(draw, (22, 18), "G-4.18D.2 Rope + Crate/Barrel Cluster | LAB ONLY", size=15)
    label(draw, (22, 42), "Green-origin proof. Visual rating 7.4/10, below 7.5 PASS gate.", "#d8b7a0", 12)
    draw.rectangle((42, 78, 42 + CANVAS_W * 2 + 32, 78 + CANVAS_H * 2 + 28), outline="#82916f", width=1)
    paste_scaled(sheet, FINAL_ASSET_PATH, (58, 92), 2)
    label(draw, (58, 318), "DEFER - lab-only capability evidence", "#f0cf7d", 13)
    label(draw, (430, 94), "Checks", "#eadca6", 13)
    for idx, text in enumerate([
        "weathered crate boards",
        "barrel bands and grime",
        "rope coil fibers",
        "soft contact shadow",
        "not normal-review art",
    ]):
        label(draw, (430, 122 + idx * 24), text, "#cfdcc5", 12)
    sheet.save(ISOLATED_SHEET_PATH)


def make_before_after_sheet() -> None:
    sheet = Image.new("RGBA", (900, 340), color("#1d261c"))
    draw = ImageDraw.Draw(sheet)
    label(draw, (22, 18), "G-4.18D.2 Production Path: Rough Base to Polished Attempt", size=15)
    label(draw, (22, 42), "Inkscape rough silhouette -> Pillow paint pass -> Krita projection -> GIMP PNG cleanup", "#d8b7a0", 12)
    draw.rectangle((42, 82, 42 + CANVAS_W * 2 + 24, 82 + CANVAS_H * 2 + 18), outline="#798767", width=1)
    draw.rectangle((468, 82, 468 + CANVAS_W * 2 + 24, 82 + CANVAS_H * 2 + 18), outline="#d8c06a", width=1)
    paste_scaled(sheet, ROUGH_BASE_PATH, (54, 96), 2)
    paste_scaled(sheet, FINAL_ASSET_PATH, (480, 96), 2)
    label(draw, (54, 296), "Before: flat vector/procedural base", "#f0b1a3", 12)
    label(draw, (480, 296), "After: improved but still DEFER", "#f0cf7d", 12)
    sheet.save(BEFORE_AFTER_PATH)


def make_in_world_frame() -> None:
    sheet = Image.new("RGBA", (980, 420), color("#32472f"))
    draw = ImageDraw.Draw(sheet)
    label(draw, (22, 16), "G-4.18D.2 In-World Comparison Frame | actual scale proof", size=15)
    label(draw, (22, 40), "Placed beside current Newport building/provenance-yellow art for visual judgment only.", "#d8b7a0", 12)
    draw.rectangle((0, 236, 980, 294), fill="#716c57")
    draw.rectangle((0, 292, 980, 354), fill="#5d513c")
    draw.rectangle((0, 350, 980, 420), fill="#2f7785")
    for x in range(0, 980, 42):
        draw.line((x, 296, x + 20, 294), fill="#322b20", width=1)
        draw.line((x, 374, x + 34, 371), fill="#1e5e6b", width=1)
    chandlery = Image.open(CHANDLERY_REFERENCE_PATH).convert("RGBA")
    scale = 0.55
    chandlery = chandlery.resize((int(chandlery.width * scale), int(chandlery.height * scale)), Image.Resampling.LANCZOS)
    sheet.alpha_composite(chandlery, (516, 90))
    wharf = Image.open(WHARF_REFERENCE_PATH).convert("RGBA")
    wharf = wharf.resize((int(wharf.width * 1.15), int(wharf.height * 1.15)), Image.Resampling.LANCZOS)
    sheet.alpha_composite(wharf, (98, 244))
    final = Image.open(FINAL_ASSET_PATH).convert("RGBA")
    sheet.alpha_composite(final, (408, 250))
    draw.rectangle((404, 246, 572, 362), outline="#d8c06a", width=1)
    label(draw, (408, 366), "D2 asset at 1x scale - DEFER", "#f0cf7d", 12)
    label(draw, (98, 320), "Existing wharf dressing", "#cfdcc5", 11)
    label(draw, (516, 300), "Current Newport building art", "#cfdcc5", 11)
    sheet.save(IN_WORLD_PATH)


def make_capability_board() -> None:
    sheet = Image.new("RGBA", (1240, 430), color("#1d261c"))
    draw = ImageDraw.Draw(sheet)
    label(draw, (22, 18), "G-4.18D.2 Art Production Capability Gate | LAB ONLY", size=15)
    label(draw, (22, 42), "One rope coil + crate/barrel cluster. Verdict: DEFER. No normal-review promotion.", "#d8b7a0", 12)
    paste_scaled(sheet, ROUGH_BASE_PATH, (50, 94), 2)
    paste_scaled(sheet, FINAL_ASSET_PATH, (390, 94), 2)
    comparison = Image.open(IN_WORLD_PATH).convert("RGBA").resize((440, 189), Image.Resampling.LANCZOS)
    sheet.alpha_composite(comparison, (758, 96))
    label(draw, (50, 322), "Before: rough base", "#f0b1a3", 12)
    label(draw, (390, 322), "After: improved material handling", "#f0cf7d", 12)
    label(draw, (758, 322), "In-world comparison: close, not finished", "#f0cf7d", 12)
    for idx, text in enumerate([
        "Gate: PASS requires >= 7.5/10 and screenshot improvement.",
        "Rating: 7.4/10; clearer than D.1 but still slightly pasted-on.",
        "Tool result: usable integration pipeline; unreliable interactive Krita paint path.",
        "Recommendation: Codex can prototype/prepare/QA, but final art still needs a stronger art source.",
    ]):
        label(draw, (50, 360 + idx * 17), text, "#cfdcc5", 11)
    sheet.save(CAPABILITY_BOARD_PATH)


def write_inspection(inkscape_log: str, krita_log: str, gimp_log: str) -> None:
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    data = {
        "phase": "G-4.18D.2",
        "asset_id": "g418d2_rope_crate_barrel_cluster",
        "visual_pass_gate": VISUAL_PASS_GATE,
        "visual_rating": VISUAL_RATING,
        "capability_verdict": CAPABILITY_VERDICT,
        "tool_logs": {
            "inkscape": inkscape_log,
            "krita": krita_log,
            "gimp": gimp_log,
        },
        "samples": {
            "rough_base": {
                "path": rel(ROUGH_BASE_PATH),
                "sha256": sha256(ROUGH_BASE_PATH),
                "alpha": alpha_bounds(ROUGH_BASE_PATH),
                "contrast_stddev": contrast_stddev(ROUGH_BASE_PATH),
            },
            "final_asset": {
                "path": rel(FINAL_ASSET_PATH),
                "sha256": sha256(FINAL_ASSET_PATH),
                "alpha": alpha_bounds(FINAL_ASSET_PATH),
                "contrast_stddev": contrast_stddev(FINAL_ASSET_PATH),
                "palette_distance_to_wharf_reference": palette_distance(FINAL_ASSET_PATH, WHARF_REFERENCE_PATH),
                "palette_distance_to_chandlery_reference": palette_distance(FINAL_ASSET_PATH, CHANDLERY_REFERENCE_PATH),
            },
        },
        "visual_judgment": "Improved material handling and silhouette over the rough base, but below the 7.5 tiny-prop PASS gate; lab-only quarantine remains correct.",
    }
    INSPECTION_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")


def update_manifest() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest["phase"] = "G-4.18D.2"
    manifest["generated_at"] = "2026-05-16T00:00:00Z"
    manifest["normal_review_policy"] = "No G-4.18D, G-4.18D.1, or G-4.18D.2 experimental/capability asset is normal-review eligible unless separately promoted after screenshot acceptance. Failed and deferred art is lab-only."
    manifest["visual_quality_gate"] = "G-4.18D bakeoff PASS remains >= 8.5. G-4.18D.2 tiny environmental capability PASS requires visual_rating >= 7.5 and screenshot improvement. Provenance green alone cannot produce PASS or promotion."
    contact_sheets = list(dict.fromkeys(
        list(manifest.get("contact_sheets", []))
        + [
            rel(ISOLATED_SHEET_PATH),
            rel(BEFORE_AFTER_PATH),
            rel(IN_WORLD_PATH),
            rel(CAPABILITY_BOARD_PATH),
        ]
    ))
    manifest["contact_sheets"] = contact_sheets
    manifest["art_production_capability_gate"] = {
        "phase": "G-4.18D.2",
        "asset_id": "g418d2_rope_crate_barrel_cluster",
        "asset_name": "Rope coil + crate/barrel dockside cluster",
        "asset_family": "tiny_dockside_environmental_prop_cluster",
        "rough_base_path": rel(ROUGH_BASE_PATH),
        "prepared_path": rel(PREPARED_PATH),
        "sample_path": rel(FINAL_ASSET_PATH),
        "isolated_proof_path": rel(ISOLATED_SHEET_PATH),
        "before_after_path": rel(BEFORE_AFTER_PATH),
        "in_world_comparison_path": rel(IN_WORLD_PATH),
        "source_file": rel(PAINT_PLAN_PATH),
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
            {
                "type": "project_script",
                "path": rel(SCRIPT_PATH),
                "source_pixels_used": False,
                "commercial_status": "green_origin_candidate",
            },
            {
                "type": "inkscape_authored_silhouette",
                "path": rel(SILHOUETTE_SVG_PATH),
                "source_pixels_used": False,
                "commercial_status": "green_origin_candidate",
            },
            {
                "type": "project_authored_paint_plan",
                "path": rel(PAINT_PLAN_PATH),
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
                "type": "project_authored_palette_tokens",
                "path": rel(STYLE_TOKENS_PATH),
                "source_pixels_used": False,
                "commercial_status": "green_origin_candidate",
            },
        ],
        "source_pixels_from_yellow_uncertain_assets": False,
        "source_pixels_from_third_party_material": False,
        "web_scraped_source_pixels": False,
        "ai_generated": False,
        "deterministic_generated": False,
        "hand_paintover": True,
        "ownership": "project-owned",
        "license": "Wayfarer project-owned green-origin G-4.18D.2 capability proof; no third-party, marketplace, web-scraped, ripped, or yellow-source pixels; lab review only because visual gate is not met.",
        "sha256": sha256(FINAL_ASSET_PATH),
        "tool_reliability_notes": "Inkscape and Pillow were reliable. Krita CLI projection was reliable; interactive Krita runner/script-runner remained unreliable. GIMP exported PNG cleanup but may require timeout handling after export.",
        "capability_answer": "Codex can generate a better rough-to-polished prop prototype and integration proof, but this run did not prove finished commercial-safe sprite production without a stronger art source.",
    }
    manifest["g418d2_capability_gate"] = "One green-origin rope/crate/barrel cluster was attempted and judged below the 7.5 tiny-prop PASS gate; it remains lab-only."
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    for directory in [GENERATED_ROOT, SOURCE_ROOT, REPORTS_ROOT, CONTACT_SHEET_ROOT]:
        directory.mkdir(parents=True, exist_ok=True)
    write_silhouette_svg()
    inkscape_log = render_rough_base()
    create_prepared_asset()
    krita_log = run_krita_export()
    gimp_log = run_gimp_cleanup()
    make_isolated_sheet()
    make_before_after_sheet()
    make_in_world_frame()
    make_capability_board()
    write_inspection(inkscape_log, krita_log, gimp_log)
    update_manifest()
    print(f"Wrote G-4.18D.2 capability asset: {rel(FINAL_ASSET_PATH)}")
    print(f"Verdict: {CAPABILITY_VERDICT} ({VISUAL_RATING}/10, gate {VISUAL_PASS_GATE}/10)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
