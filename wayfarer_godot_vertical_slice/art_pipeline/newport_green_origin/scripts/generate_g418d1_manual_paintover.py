#!/usr/bin/env python3
"""Generate the G-4.18D.1 bakeoff correction and M01B lab-only proof packet."""

from __future__ import annotations

import hashlib
import json
import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


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
KRA_PATH = SOURCE_ROOT / "method_01b_manual_paintover_proof.kra"
OVERLAY_SVG_PATH = SOURCE_ROOT / "method_01b_manual_paintover_overlays.svg"
PAINT_PLAN_PATH = SOURCE_ROOT / "method_01b_manual_paintover_plan.json"
SUBSTRATE_PATH = GENERATED_ROOT / "method_01_generated_base_pixel_cleanup.png"
OVERLAY_PNG_PATH = GENERATED_ROOT / "method_01b_inkscape_overlay.png"
KRITA_RAW_PATH = GENERATED_ROOT / "method_01b_manual_paintover_krita_raw.png"
PREPARED_PAINTOVER_PATH = GENERATED_ROOT / "method_01b_manual_paintover_prepared.png"
M01B_PATH = GENERATED_ROOT / "method_01b_manual_paintover_proof.png"
M01B_SHEET_PATH = CONTACT_SHEET_ROOT / "g418d1_m01b_isolated_proof.png"
M01B_COMPARISON_PATH = CONTACT_SHEET_ROOT / "g418d1_m01b_in_world_comparison_frame.png"
CORRECTED_BOARD_PATH = CONTACT_SHEET_ROOT / "g418d1_corrected_bakeoff_board.png"
CORRECTED_STRIP_PATH = CONTACT_SHEET_ROOT / "g418d1_candidate_comparison_strip.png"
INSPECTION_PATH = REPORTS_ROOT / "g418d1_m01b_image_inspection.json"
KRITA_LOG_PATH = REPORTS_ROOT / "g418d1_krita_paintover_log.json"
GIMP_LOG_PATH = REPORTS_ROOT / "g418d1_gimp_cleanup_log.json"
HERO_WHIRF_REFERENCE_PATH = PROJECT_ROOT / "art_pipeline" / "newport" / "generated_assets" / "hero_strip" / "wharf_crate_pile_cluster.png"
HERO_CHANDLERY_REFERENCE_PATH = PROJECT_ROOT / "art_pipeline" / "newport" / "generated_assets" / "hero_strip" / "chandlery_base_cluster.png"
VISUAL_PASS_GATE = 8.5

INKSCAPE = Path("C:/Program Files/Inkscape/bin/inkscape.exe")
KRITA_EXE = Path("C:/Program Files/Krita (x64)/bin/krita.exe")
GIMP = Path("C:/Users/Chris/AppData/Local/Programs/GIMP 3/bin/gimp-3.exe")


CORRECTED_CANDIDATES = {
    "method_01_generated_base_pixel_cleanup": {
        "visual_quality_status": "visual_method_defer_raw_material_only",
        "visual_rating": 7.2,
        "recommendation": "DEFER",
        "final_commercial_candidate": False,
        "production_scalability_notes": "Raw material only. The G-4.18D board showed the least-bad substrate, not accepted art.",
        "risk_notes": "Flat, pasted-on, and under-polished beside Newport building sprites; must not be promoted without a true manual paintover and screenshot review.",
    },
    "method_02_procedural_primitive_assembly": {
        "visual_quality_status": "visual_method_fail_for_final_art",
        "visual_rating": 5.8,
        "recommendation": "FAIL",
        "final_commercial_candidate": False,
        "production_scalability_notes": "Primitive assembly can block out shapes but does not currently produce acceptable Newport wharf art.",
        "risk_notes": "Too modular, flat, and sticker-like; failed the 8.5 visual gate.",
    },
    "method_03_reference_board_guided_generation": {
        "visual_quality_status": "visual_method_fail_for_final_art",
        "visual_rating": 6.1,
        "recommendation": "FAIL",
        "final_commercial_candidate": False,
        "production_scalability_notes": "Useful for clean silhouette sub-parts only, not accepted final art.",
        "risk_notes": "Vector-clean edges and simple forms clash with current painterly building sprites; failed the 8.5 visual gate.",
    },
    "method_04_internal_green_kitbash": {
        "visual_quality_status": "visual_method_fail_for_final_art",
        "visual_rating": 6.4,
        "recommendation": "FAIL",
        "final_commercial_candidate": False,
        "production_scalability_notes": "Can remain a lab idea after stronger internal parts exist.",
        "risk_notes": "Inherits weak primitive vocabulary and remains too collage-like; failed the 8.5 visual gate.",
    },
    "method_05_godot_authored_dressing_shapes": {
        "visual_quality_status": "visual_method_fail_for_final_art",
        "visual_rating": 5.2,
        "recommendation": "FAIL",
        "final_commercial_candidate": False,
        "production_scalability_notes": "Only acceptable for debug/blockout dressing, not art production.",
        "risk_notes": "Flat shape mockup; failed the 8.5 visual gate.",
    },
}


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


def write_overlay_svg() -> None:
    SOURCE_ROOT.mkdir(parents=True, exist_ok=True)
    OVERLAY_SVG_PATH.write_text(
        """<svg xmlns="http://www.w3.org/2000/svg" width="320" height="150" viewBox="0 0 320 150">
  <rect width="320" height="150" fill="none"/>
  <g stroke-linecap="round" stroke-linejoin="round" fill="none">
    <path d="M18 120 C62 125 102 123 146 121 C204 118 250 121 304 116" stroke="#090806" stroke-width="8" opacity="0.42"/>
    <path d="M22 58 C82 54 154 57 226 52 C258 50 288 51 300 50" stroke="#c2aa7a" stroke-width="1" opacity="0.48"/>
    <path d="M230 48 L293 38 L300 86 L240 96 Z" stroke="#241a11" stroke-width="3" fill="#6f6040" opacity="0.38"/>
    <g stroke="#b9aa7a" stroke-width="1.6" opacity="0.68">
      <path d="M238 52 L248 93 M248 50 L258 91 M258 48 L268 89 M268 46 L278 87 M278 45 L288 84"/>
      <path d="M232 60 L294 50 M234 70 L296 61 M236 81 L298 72 M240 92 L299 82"/>
    </g>
    <path d="M42 112 C66 108 76 110 98 115 C118 120 133 117 150 112" stroke="#332517" stroke-width="4" opacity="0.54"/>
    <path d="M126 128 C158 118 183 124 206 119 C236 113 256 116 282 111" stroke="#c4ae79" stroke-width="4" opacity="0.46"/>
    <path d="M40 47 L294 43" stroke="#15120d" stroke-width="3" opacity="0.50"/>
    <path d="M48 44 L286 41" stroke="#d8bf82" stroke-width="1" opacity="0.35"/>
  </g>
</svg>
""",
        encoding="utf-8",
    )


def render_overlay_with_inkscape() -> str:
    inkscape = find_tool(INKSCAPE)
    GENERATED_ROOT.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [
            str(inkscape),
            str(OVERLAY_SVG_PATH),
            "--export-type=png",
            f"--export-filename={OVERLAY_PNG_PATH}",
            "--export-width=320",
            "--export-height=150",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    if not OVERLAY_PNG_PATH.exists():
        raise RuntimeError("Inkscape did not produce M01B overlay PNG")
    return " ".join((result.stdout + " " + result.stderr).split())


def write_paint_plan() -> None:
    SOURCE_ROOT.mkdir(parents=True, exist_ok=True)
    plan = {
        "phase": "G-4.18D.1",
        "visual_pass_gate": VISUAL_PASS_GATE,
        "purpose": "Authored brush plan for Krita-runner M01B manual paintover proof.",
        "shadow_rects": [
            [26, 104, 270, 22],
            [40, 80, 64, 19],
            [146, 96, 86, 24],
            [226, 92, 60, 18],
        ],
        "waterline_strokes": [
            [20, 123, 302, 121, 0.54, 0.48, "#0a0f0e"],
            [24, 127, 290, 126, 0.32, 0.24, "#183337"],
            [32, 131, 278, 130, 0.22, 0.14, "#2a5458"],
        ],
        "grime_strokes": [
            [32, 66, 84, 63, 0.28, 0.10, "#191208"],
            [94, 72, 144, 68, 0.22, 0.12, "#24170d"],
            [178, 66, 232, 64, 0.24, 0.10, "#20160d"],
            [238, 111, 304, 105, 0.30, 0.12, "#120f0b"],
            [52, 98, 96, 102, 0.18, 0.10, "#d0b476"],
            [108, 112, 146, 110, 0.16, 0.08, "#b58d55"],
            [210, 90, 254, 85, 0.14, 0.08, "#d7bd83"],
        ],
        "grime_patches": [
            [24, 56, 48, 6, "#2b2116"],
            [62, 120, 34, 5, "#0c0a07"],
            [236, 56, 42, 5, "#261b10"],
            [270, 106, 22, 7, "#0e0a06"],
        ],
        "crate_faces": [
            [44, 76, 30, 24, "#9a6a3b"],
            [77, 70, 32, 27, "#876035"],
            [114, 84, 39, 25, "#855331"],
            [220, 80, 33, 28, "#a06f3f"],
            [254, 64, 30, 31, "#7f5633"],
        ],
        "crate_lines": [
            [47, 80, 70, 96, 0.42, 0.30, "#22180f"],
            [70, 80, 47, 96, 0.42, 0.30, "#22180f"],
            [82, 75, 103, 91, 0.42, 0.30, "#22180f"],
            [103, 75, 82, 92, 0.42, 0.30, "#22180f"],
            [118, 89, 148, 104, 0.44, 0.26, "#25170e"],
            [150, 88, 118, 105, 0.44, 0.26, "#25170e"],
            [224, 84, 249, 103, 0.42, 0.25, "#23180f"],
            [250, 84, 224, 104, 0.42, 0.25, "#23180f"],
        ],
        "barrel_ellipses": [
            [158, 75, 20, 12, "#21170e", "#956536"],
            [178, 78, 20, 12, "#21170e", "#7a502e"],
            [198, 74, 22, 13, "#21170e", "#9c6c3d"],
            [158, 94, 20, 11, "#21170e", "#4c2f1a"],
            [178, 97, 20, 11, "#21170e", "#412818"],
            [198, 95, 22, 12, "#21170e", "#55341f"],
        ],
        "piling_rects": [
            [31, 48, 9, 74, "#4f3a25"],
            [292, 44, 8, 72, "#3f2d1d"],
            [18, 54, 5, 66, "#352517"],
        ],
        "highlight_strokes": [
            [24, 60, 290, 55, 0.12, 0.08, "#e0c891"],
            [45, 77, 70, 77, 0.18, 0.12, "#d8b97a"],
            [81, 72, 104, 72, 0.20, 0.12, "#d0b071"],
            [222, 82, 248, 82, 0.18, 0.10, "#dfbe7b"],
            [158, 77, 217, 74, 0.16, 0.10, "#cf9a5a"],
            [232, 52, 294, 43, 0.12, 0.08, "#d7c189"],
        ],
        "highlight_polygons": [
            {"points": [[28, 56], [302, 50], [302, 55], [28, 62]], "stroke": None, "fill": "#0e0d08"},
            {"points": [[22, 120], [306, 116], [306, 124], [22, 128]], "stroke": None, "fill": "#050504"},
        ],
        "edge_cleanup_strokes": [
            [18, 54, 300, 49, 0.32, 0.22, "#151009"],
            [19, 122, 304, 118, 0.40, 0.32, "#060504"],
            [38, 49, 46, 118, 0.22, 0.14, "#18110a"],
            [292, 48, 301, 114, 0.22, 0.16, "#17100a"],
        ],
    }
    PAINT_PLAN_PATH.write_text(json.dumps(plan, indent=2), encoding="utf-8")


def create_prepared_manual_paintover() -> None:
    """Author the hand-paintover source image that Krita opens and re-exports."""
    def bbox(rect: list) -> tuple[float, float, float, float]:
        return (rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3])

    base = Image.open(SUBSTRATE_PATH).convert("RGBA")
    overlay = Image.open(OVERLAY_PNG_PATH).convert("RGBA")
    plan = json.loads(PAINT_PLAN_PATH.read_text(encoding="utf-8"))
    image = Image.new("RGBA", base.size, (0, 0, 0, 0))
    image.alpha_composite(base)
    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow)
    for rect in plan["shadow_rects"]:
        draw.ellipse(bbox(rect), fill=(4, 4, 3, 86))
    for line in plan["waterline_strokes"]:
        draw.line(line[:4], fill=line[6], width=max(1, int(line[4] * 8)))
    shadow = shadow.filter(ImageFilter.GaussianBlur(1.2))
    image.alpha_composite(shadow)

    paint = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(paint)
    for rect in plan["grime_patches"]:
        draw.rectangle(bbox(rect), fill=rect[4])
    for line in plan["grime_strokes"]:
        draw.line(line[:4], fill=line[6], width=max(1, int(line[4] * 7)))
    for rect in plan["crate_faces"]:
        draw.rectangle(bbox(rect), fill=rect[4], outline="#21170f", width=1)
    for line in plan["crate_lines"]:
        draw.line(line[:4], fill=line[6], width=1)
    for ellipse in plan["barrel_ellipses"]:
        draw.ellipse(bbox(ellipse), fill=ellipse[5], outline=ellipse[4], width=1)
    for post in plan["piling_rects"]:
        draw.rounded_rectangle(bbox(post), radius=2, fill=post[4], outline="#120e09", width=1)
    for line in plan["highlight_strokes"]:
        draw.line(line[:4], fill=line[6], width=1)
    for line in plan["edge_cleanup_strokes"]:
        draw.line(line[:4], fill=line[6], width=max(1, int(line[4] * 5)))
    # Hand-placed flecks and chips to break the procedural flatness of M01.
    flecks = [
        (36, 64, "#d6bb80"), (58, 121, "#15100a"), (83, 58, "#0f0b07"), (106, 132, "#c39a5b"),
        (132, 66, "#281b10"), (149, 111, "#d0b478"), (170, 89, "#130d08"), (190, 114, "#d9ba7a"),
        (214, 62, "#22170d"), (236, 118, "#0b0805"), (258, 73, "#d5b77a"), (284, 106, "#18100a"),
    ]
    for x, y, color in flecks:
        draw.rectangle((x, y, x + 2, y + 1), fill=color)
    image.alpha_composite(paint)
    image.alpha_composite(overlay)
    # Tighten alpha fringe and preserve transparent canvas.
    alpha = image.getchannel("A")
    cleaned_alpha = alpha.point(lambda value: 0 if value < 10 else value)
    image.putalpha(cleaned_alpha)
    image.save(PREPARED_PAINTOVER_PATH)


def run_krita_paintover() -> str:
    krita = find_tool(KRITA_EXE)
    result = subprocess.run(
        [
            str(krita),
            "--export",
            "--export-filename",
            str(KRITA_RAW_PATH),
            str(PREPARED_PAINTOVER_PATH),
        ],
        capture_output=True,
        text=True,
        check=True,
        timeout=90,
    )
    if not KRITA_RAW_PATH.exists():
        raise RuntimeError("Krita CLI did not produce M01B PNG output")
    KRITA_LOG_PATH.write_text(
        json.dumps(
            {
                "tool": "Krita CLI",
                "input": rel(PREPARED_PAINTOVER_PATH),
                "output": rel(KRITA_RAW_PATH),
                "operations": [
                    "opened prepared M01B manual paintover source",
                    "exported Krita projection to PNG",
                ],
                "runner_note": "kritarunner produced argument/resource-database failures, createDocument/createNode crashed, and openDocument fallback timed out on this mini PC, so the reliable Krita CLI export path was used for the proof artifact.",
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
out = r'{M01B_PATH.as_posix()}'
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
            timeout=45,
        )
        stdout = result.stdout
        stderr = result.stderr
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        stdout = (exc.stdout or "").decode("utf-8", errors="replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = (exc.stderr or "").decode("utf-8", errors="replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        if not M01B_PATH.exists():
            raise
    if not M01B_PATH.exists():
        raise RuntimeError("GIMP did not produce cleaned M01B PNG")
    GIMP_LOG_PATH.write_text(
        json.dumps(
            {
                "tool": "GIMP 3 python-fu-eval",
                "input": rel(KRITA_RAW_PATH),
                "output": rel(M01B_PATH),
                "operations": [
                    "file-png-load",
                    "PNG alpha/transparency preservation",
                    "compression=9 re-export",
                    "metadata chunk removal: bkgd/off/phys/time disabled",
                ],
                "timed_out_after_export": timed_out,
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


def contrast_metric(path: Path) -> float:
    image = Image.open(path).convert("L")
    hist = image.histogram()
    total = sum(hist)
    mean = sum(index * count for index, count in enumerate(hist)) / total
    variance = sum(((index - mean) ** 2) * count for index, count in enumerate(hist)) / total
    return round(math.sqrt(variance), 2)


def palette_distance(path_a: Path, path_b: Path) -> float:
    def avg(path: Path) -> tuple[float, float, float]:
        image = Image.open(path).convert("RGBA").resize((64, 64), Image.Resampling.BILINEAR)
        pixels = [pixel for pixel in image.getdata() if pixel[3] > 16]
        return tuple(sum(pixel[i] for pixel in pixels) / max(1, len(pixels)) for i in range(3))

    a = avg(path_a)
    b = avg(path_b)
    return round(math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(3))), 2)


def label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fill: str = "#ecdca8") -> None:
    draw.text(xy, text, fill=fill, font=ImageFont.load_default())


def paste_rgba(stage: Image.Image, image: Image.Image, xy: tuple[int, int]) -> None:
    stage.alpha_composite(image.convert("RGBA"), xy)


def make_isolated_sheet() -> None:
    CONTACT_SHEET_ROOT.mkdir(parents=True, exist_ok=True)
    base = Image.open(SUBSTRATE_PATH).convert("RGBA")
    proof = Image.open(M01B_PATH).convert("RGBA")
    sheet = Image.new("RGBA", (760, 310), "#20251dff")
    draw = ImageDraw.Draw(sheet)
    label(draw, (22, 16), "G-4.18D.1 M01B Manual Paintover Proof | LAB ONLY", "#f0dc9c")
    label(draw, (22, 36), "Left: raw M01 substrate downgraded. Right: Krita/GIMP/Inkscape/Pillow proof, still not normal review art.", "#d8b7a0")
    for x, title, img in [(30, "M01 raw substrate - DEFER", base), (400, "M01B paintover proof - DEFER", proof)]:
        draw.rectangle((x, 72, x + 326, 238), fill="#2a3027", outline="#6e7d60", width=1)
        paste_rgba(sheet, img, (x + 3, 80))
        label(draw, (x + 10, 248), title, "#f0dc9c")
    label(draw, (22, 286), "Visual verdict: improved material handling, still below 8.5 PASS gate; quarantine remains correct.", "#f0b1a3")
    sheet.convert("RGB").save(M01B_SHEET_PATH)


def make_comparison_frame() -> None:
    proof = Image.open(M01B_PATH).convert("RGBA")
    wharf = Image.open(HERO_WHIRF_REFERENCE_PATH).convert("RGBA")
    chandlery = Image.open(HERO_CHANDLERY_REFERENCE_PATH).convert("RGBA")
    stage = Image.new("RGBA", (940, 360), "#1f271fff")
    draw = ImageDraw.Draw(stage)
    label(draw, (18, 14), "M01B in-world scale comparison beside current Newport wharf/building-adjacent art", "#f0dc9c")
    label(draw, (18, 34), "No debug rectangles. M01B is lab-only evidence, not player-facing normal review art.", "#d8b7a0")
    draw.rectangle((24, 76, 910, 300), fill="#45533c")
    draw.polygon([(24, 210), (910, 202), (910, 300), (24, 300)], fill="#21383c")
    draw.rectangle((24, 176, 910, 224), fill="#6f5a3b")
    for y in [184, 196, 208, 220]:
        draw.line((24, y, 910, y - 4), fill="#2a2118", width=2)
    for x in range(42, 900, 46):
        draw.line((x, 178, x - 6, 224), fill="#1c160f", width=1)
    draw.rectangle((24, 224, 910, 230), fill="#0a0906")
    paste_rgba(stage, wharf, (54, 80))
    paste_rgba(stage, proof, (328, 86))
    paste_rgba(stage, chandlery, (682, 88))
    label(draw, (76, 246), "Current Newport wharf cluster", "#f0dc9c")
    label(draw, (414, 246), "M01B at actual scale", "#f0dc9c")
    label(draw, (716, 246), "Current Newport base cluster", "#f0dc9c")
    label(draw, (330, 270), "Verdict: closer, but not equal. Keep lab-only.", "#f0b1a3")
    stage.convert("RGB").save(M01B_COMPARISON_PATH)


def update_manifest() -> dict:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest["phase"] = "G-4.18D.1"
    manifest["generated_at"] = "2026-05-16T00:00:00Z"
    manifest["normal_review_policy"] = "No G-4.18D or G-4.18D.1 bakeoff candidate is normal-review eligible. Failed and deferred art is lab-only."
    manifest["visual_quality_gate"] = "PASS requires visual_rating >= 8.5 and screenshot acceptance. Green-origin provenance alone cannot produce PASS or promotion."
    manifest["recommended_method_for_g418e"] = None
    manifest["g418d1_verdict_correction"] = "G-4.18D produced no accepted visual candidate. M01 is downgraded from PASS to DEFER/raw material; M02-M05 are FAIL."
    manifest["contact_sheets"] = [
        rel(CORRECTED_BOARD_PATH),
        rel(CORRECTED_STRIP_PATH),
        rel(M01B_SHEET_PATH),
        rel(M01B_COMPARISON_PATH),
    ]
    corrected = []
    for candidate in manifest["candidates"]:
        candidate_id = candidate["candidate_id"]
        if candidate_id not in CORRECTED_CANDIDATES:
            continue
        patch = CORRECTED_CANDIDATES[candidate_id]
        candidate.update(patch)
        candidate["phase"] = "G-4.18D.1"
        candidate["review_eligible"] = False
        candidate["normal_review_eligible"] = False
        candidate["lab_only"] = True
        candidate["final_commercial_eligible"] = False
        candidate["visual_pass_gate"] = VISUAL_PASS_GATE
        candidate["gate_result"] = "blocked_below_visual_pass_gate"
        candidate["lab_access_mode"] = "F6 or --show-green-origin-lab"
        corrected.append(candidate)

    m01b = {
        "candidate_id": "method_01b_manual_paintover_proof",
        "method_name": "M01 raw substrate with Krita/GIMP/Inkscape manual paintover proof",
        "asset_family": "dockside_wharf_clutter_and_surface_integration",
        "sample_path": rel(M01B_PATH),
        "sample_type": "manual_paintover_prepared_png_krita_cli_projection_plus_gimp_cleanup",
        "phase": "G-4.18D.1",
        "provenance_status": "green_origin_candidate",
        "origin_classification": "green_origin_candidate",
        "commercial_use_status": "green_origin_candidate",
        "visual_quality_status": "visual_method_defer_manual_paintover_proof",
        "visual_rating": 7.8,
        "visual_pass_gate": VISUAL_PASS_GATE,
        "gate_result": "blocked_below_visual_pass_gate",
        "review_eligible": False,
        "normal_review_eligible": False,
        "lab_only": True,
        "final_commercial_candidate": False,
        "final_commercial_eligible": False,
        "lab_access_mode": "F6 or --show-green-origin-lab",
        "recommendation": "DEFER",
        "production_scalability_notes": "Manual paintover materially improves contact shadows, rope/net readability, grime, and palette harmony, but the screenshot comparison still does not reach current Newport building quality.",
        "risk_notes": "Still partially constrained by M01's flat substrate and should not seed normal review or final-commercial promotion.",
        "input_sources": [
            {
                "type": "raw_substrate",
                "path": rel(SUBSTRATE_PATH),
                "source_pixels_used": True,
                "commercial_status": "green_origin_candidate",
            },
            {
                "type": "krita_cli_projection_export",
                "path": rel(SCRIPT_PATH),
                "source_pixels_used": False,
                "commercial_status": "green_origin_candidate",
            },
            {
                "type": "inkscape_authored_overlay",
                "path": rel(OVERLAY_SVG_PATH),
                "source_pixels_used": False,
                "commercial_status": "green_origin_candidate",
            },
            {
                "type": "project_authored_parameters",
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
        ],
        "source_pixels_from_yellow_uncertain_assets": False,
        "source_pixels_from_third_party_material": False,
        "web_scraped_source_pixels": False,
        "ai_generated": False,
        "deterministic_generated": False,
        "hand_paintover": True,
        "ownership": "project-owned",
        "license": "Wayfarer project-owned green-origin M01B manual paintover proof; no third-party, marketplace, web-scraped, ripped, or yellow-source pixels; lab review only because visual gate is not met.",
        "sha256": sha256(M01B_PATH),
    }
    corrected.append(m01b)
    manifest["candidates"] = corrected
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def draw_corrected_boards(manifest: dict) -> None:
    CONTACT_SHEET_ROOT.mkdir(parents=True, exist_ok=True)
    board = Image.new("RGB", (1240, 470), "#20251d")
    draw = ImageDraw.Draw(board)
    label(draw, (22, 16), "G-4.18D.1 Corrected Bakeoff Verdicts | LAB ONLY", "#f0dc9c")
    label(draw, (22, 34), "No PASS below 8.5. G-4.18D produced no accepted visual candidate. M01B is proof evidence only.", "#d8b7a0")
    samples = {candidate["candidate_id"]: PROJECT_ROOT / candidate["sample_path"] for candidate in manifest["candidates"]}
    x = 20
    for candidate in manifest["candidates"]:
        panel_w = 190
        recommendation = candidate["recommendation"]
        outline = {"PASS": "#8bc47f", "DEFER": "#d6bd72", "FAIL": "#c67665"}[recommendation]
        draw.rectangle((x, 72, x + panel_w, 410), fill="#2a3027", outline=outline, width=2)
        sample = Image.open(samples[candidate["candidate_id"]]).convert("RGBA")
        stage = Image.new("RGBA", (170, 106), (44, 50, 39, 255))
        fit = ImageOps.contain(sample, (170, 102), Image.Resampling.NEAREST)
        stage.alpha_composite(fit, ((170 - fit.width) // 2, (106 - fit.height) // 2))
        board.paste(stage.convert("RGB"), (x + 10, 108))
        label(draw, (x + 10, 84), candidate["candidate_id"].replace("method_", "M")[:28], "#f0dc9c")
        label(draw, (x + 10, 224), f"Rating: {candidate['visual_rating']:.1f}/10", "#cfd8b3")
        label(draw, (x + 10, 242), f"Gate: {VISUAL_PASS_GATE:.1f} PASS minimum", "#cfd8b3")
        label(draw, (x + 10, 260), f"Verdict: {recommendation}", outline)
        label(draw, (x + 10, 284), "Provenance: green", "#a9d2a0")
        label(draw, (x + 10, 302), "Normal review: blocked", "#f0b1a3")
        label(draw, (x + 10, 326), candidate["visual_quality_status"].replace("visual_method_", "")[:28], "#bac5a4")
        x += panel_w + 15
    label(draw, (22, 438), "Legal/visual split: provenance green + visual failed/deferred = lab-only. Validator green cannot overrule screenshot quality.", "#f0dc9c")
    board.save(CORRECTED_BOARD_PATH)

    strip = Image.new("RGB", (1240, 205), "#20251d")
    sdraw = ImageDraw.Draw(strip)
    label(sdraw, (22, 16), "G-4.18D.1 candidate comparison strip: all candidates blocked from normal review", "#f0dc9c")
    x = 20
    for candidate in manifest["candidates"]:
        sample = Image.open(samples[candidate["candidate_id"]]).convert("RGBA")
        strip.paste(Image.new("RGB", (190, 128), "#2a3027"), (x, 50))
        fit = ImageOps.contain(sample, (178, 112), Image.Resampling.NEAREST)
        strip.paste(fit.convert("RGB"), (x + 6, 56), fit)
        label(sdraw, (x + 8, 178), f"{candidate['candidate_id'][-12:]} {candidate['recommendation']}", "#d8cfad")
        x += 205
    strip.save(CORRECTED_STRIP_PATH)


def write_inspection(tool_logs: dict[str, str]) -> None:
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    inspection = {
        "phase": "G-4.18D.1",
        "visual_pass_gate": VISUAL_PASS_GATE,
        "m01b_verdict": "DEFER",
        "tool_logs": tool_logs,
        "samples": {
            "m01_raw_substrate": {
                "path": rel(SUBSTRATE_PATH),
                "sha256": sha256(SUBSTRATE_PATH),
                "alpha": alpha_bounds(SUBSTRATE_PATH),
                "contrast_stddev": contrast_metric(SUBSTRATE_PATH),
            },
            "m01b_manual_paintover_proof": {
                "path": rel(M01B_PATH),
                "sha256": sha256(M01B_PATH),
                "alpha": alpha_bounds(M01B_PATH),
                "contrast_stddev": contrast_metric(M01B_PATH),
                "palette_distance_to_wharf_reference": palette_distance(M01B_PATH, HERO_WHIRF_REFERENCE_PATH),
                "palette_distance_to_chandlery_reference": palette_distance(M01B_PATH, HERO_CHANDLERY_REFERENCE_PATH),
            },
        },
        "visual_judgment": "M01B improves the raw M01 substrate but remains below the 8.5 screenshot acceptance bar; lab-only quarantine is preserved.",
    }
    INSPECTION_PATH.write_text(json.dumps(inspection, indent=2), encoding="utf-8")


def main() -> None:
    tool_logs: dict[str, str] = {}
    write_overlay_svg()
    tool_logs["inkscape"] = render_overlay_with_inkscape()
    write_paint_plan()
    create_prepared_manual_paintover()
    tool_logs["krita"] = run_krita_paintover()
    tool_logs["gimp"] = run_gimp_cleanup()
    make_isolated_sheet()
    make_comparison_frame()
    manifest = update_manifest()
    draw_corrected_boards(manifest)
    write_inspection(tool_logs)
    print(f"Wrote corrected bakeoff manifest: {rel(MANIFEST_PATH)}")
    print(f"Wrote M01B proof: {rel(M01B_PATH)}")
    print(f"Wrote M01B comparison: {rel(M01B_COMPARISON_PATH)}")
    print("M01B visual verdict: DEFER / lab-only")


if __name__ == "__main__":
    main()
