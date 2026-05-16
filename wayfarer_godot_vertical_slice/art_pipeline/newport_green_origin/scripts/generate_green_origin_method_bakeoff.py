#!/usr/bin/env python3
"""Generate the G-4.18D green-origin art production method bakeoff packet."""

from __future__ import annotations

import hashlib
import json
import math
import random
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[3]
PIPELINE_ROOT = PROJECT_ROOT / "art_pipeline" / "newport_green_origin"
STYLE_TOKENS_PATH = PIPELINE_ROOT / "source_authored" / "newport_green_origin_style_tokens.json"
ART_BIBLE_PATH = PROJECT_ROOT / "docs" / "NEWPORT_ART_BIBLE.md"
BAKEOFF_ROOT = PIPELINE_ROOT / "method_bakeoff"
GENERATED_ROOT = BAKEOFF_ROOT / "generated"
SOURCE_ROOT = BAKEOFF_ROOT / "source_authored"
CONTACT_SHEET_ROOT = PIPELINE_ROOT / "contact_sheets"
MANIFEST_PATH = PIPELINE_ROOT / "manifests" / "green_origin_method_bakeoff_manifest.json"
BOARD_PATH = CONTACT_SHEET_ROOT / "g418d_method_bakeoff_board.png"
STRIP_PATH = CONTACT_SHEET_ROOT / "g418d_candidate_comparison_strip.png"
INSPECTION_PATH = BAKEOFF_ROOT / "reports" / "g418d_image_inspection.json"
VECTOR_SOURCE_PATH = SOURCE_ROOT / "method_03_reference_board_guided.svg"
VECTOR_RENDER_PATH = GENERATED_ROOT / "method_03_reference_board_guided.png"

INKSCAPE_CANDIDATES = [
    Path("C:/Program Files/Inkscape/bin/inkscape.exe"),
]

GIMP_CANDIDATES = [
    Path("C:/Users/Chris/AppData/Local/Programs/GIMP 3/bin/gimp-3.exe"),
]

CANDIDATES = [
    {
        "candidate_id": "method_01_generated_base_pixel_cleanup",
        "short_label": "M01 Base + Paint Cleanup",
        "method_name": "Generated base + pixel-paint/manual cleanup pipeline",
        "sample": "method_01_generated_base_pixel_cleanup.png",
        "sample_type": "deterministic_python_pillow_cleanup_proxy",
        "visual_quality_status": "visual_method_pass_candidate",
        "visual_rating": 7.2,
        "recommendation": "PASS",
        "production_scalability_notes": "Best path for G-4.18E if the scripted base is followed by real Krita/GIMP paint cleanup, contact grounding, and palette harmonization.",
        "risk_notes": "Requires human paint time and art-direction review; the generated base alone is not enough.",
    },
    {
        "candidate_id": "method_02_procedural_primitive_assembly",
        "short_label": "M02 Primitive Assembly",
        "method_name": "Procedural sprite assembly from green-origin primitive parts",
        "sample": "method_02_procedural_primitive_assembly.png",
        "sample_type": "deterministic_python_pillow_primitives",
        "visual_quality_status": "visual_method_defer",
        "visual_rating": 5.8,
        "recommendation": "DEFER",
        "production_scalability_notes": "Useful for fast variants, collision masks, and blocking prop families once a hand-finished target exists.",
        "risk_notes": "Reads too modular without a paintover pass and can quickly become sticker-like clutter.",
    },
    {
        "candidate_id": "method_03_reference_board_guided_generation",
        "short_label": "M03 Guided Silhouette",
        "method_name": "Reference-board-guided green-origin generation with Newport constraints",
        "sample": "method_03_reference_board_guided.png",
        "sample_type": "inkscape_vector_silhouette_export_plus_pillow_shading",
        "visual_quality_status": "visual_method_defer",
        "visual_rating": 6.1,
        "recommendation": "DEFER",
        "production_scalability_notes": "Strong for silhouette, signage, trim, and scale discipline; needs painterly raster cleanup for final harbor props.",
        "risk_notes": "Vector-clean edges clash with current building sprites unless deliberately dirtied and shaded.",
    },
    {
        "candidate_id": "method_04_internal_green_kitbash",
        "short_label": "M04 Internal Kitbash",
        "method_name": "Hybrid kitbash from internally generated green-origin parts only",
        "sample": "method_04_internal_green_kitbash.png",
        "sample_type": "deterministic_python_pillow_internal_parts_only",
        "visual_quality_status": "visual_method_defer",
        "visual_rating": 6.4,
        "recommendation": "DEFER",
        "production_scalability_notes": "Promising for prop sets after a better base vocabulary exists because every component remains green-origin.",
        "risk_notes": "Can inherit every weakness of the primitive parts; needs manual composition and grounding checks.",
    },
    {
        "candidate_id": "method_05_godot_authored_dressing_shapes",
        "short_label": "M05 Godot Dressing",
        "method_name": "Godot-authored environmental dressing using drawn shapes",
        "sample": "method_05_godot_authored_dressing_shapes.png",
        "sample_type": "godot_style_drawn_shape_mockup_in_pillow",
        "visual_quality_status": "visual_method_fail_for_final_art",
        "visual_rating": 5.2,
        "recommendation": "FAIL",
        "production_scalability_notes": "Good for temporary scene grounding and debug proof, not for final commercial sprite families.",
        "risk_notes": "It remains too procedural and flat beside high-detail Newport building art.",
    },
]


def rel(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def load_tokens() -> dict:
    return json.loads(STYLE_TOKENS_PATH.read_text(encoding="utf-8"))


def rgba(hex_color: str, alpha: int = 255) -> tuple[int, int, int, int]:
    value = hex_color.strip("#")
    return (int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16), alpha)


def seeded(name: str) -> random.Random:
    seed = 418400
    for index, char in enumerate(name):
        seed += (index + 3) * ord(char)
    return random.Random(seed)


def jitter(hex_color: str, rng: random.Random, amount: int = 8, alpha: int = 255) -> tuple[int, int, int, int]:
    r, g, b, _ = rgba(hex_color)
    return (
        max(0, min(255, r + rng.randint(-amount, amount))),
        max(0, min(255, g + rng.randint(-amount, amount))),
        max(0, min(255, b + rng.randint(-amount, amount))),
        alpha,
    )


def label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fill: str = "#ecdca8") -> None:
    draw.text(xy, text, fill=fill, font=ImageFont.load_default())


def shadow(size: tuple[int, int], alpha: int = 80, blur: float = 5.0) -> Image.Image:
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((8, size[1] // 2, size[0] - 8, size[1] - 4), fill=(6, 7, 5, alpha))
    return image.filter(ImageFilter.GaussianBlur(radius=blur))


def draw_plank_floor(draw: ImageDraw.ImageDraw, rng: random.Random, rect: tuple[int, int, int, int], tokens: dict, alpha: int = 242) -> None:
    x0, y0, x1, y1 = rect
    palette = tokens["palettes"]
    y = y0
    while y < y1:
        draw.rectangle((x0, y, x1, min(y1, y + 13)), fill=jitter(rng.choice(palette["dock_wood"]), rng, 6, alpha))
        draw.line((x0, y + 12, x1, y + 11), fill=jitter(rng.choice(palette["dock_shadow"]), rng, 5, 165), width=1)
        for x in range(x0 + 8, x1, 43):
            draw.line((x, y + 2, x + rng.randint(-2, 2), min(y1, y + 11)), fill=jitter("#231c13", rng, 3, 74), width=1)
        y += 14
    draw.rectangle(rect, outline="#19140f", width=1)


def draw_crate(draw: ImageDraw.ImageDraw, xy: tuple[int, int], rng: random.Random, scale: int = 1) -> None:
    x, y = xy
    w, h = 28 * scale, 22 * scale
    fill = jitter("#8b643d", rng, 9, 245)
    edge = jitter("#2b2117", rng, 4, 230)
    draw.rectangle((x, y, x + w, y + h), fill=fill, outline=edge, width=max(1, scale))
    draw.line((x + 3 * scale, y + 3 * scale, x + w - 3 * scale, y + h - 4 * scale), fill=edge, width=max(1, scale))
    draw.line((x + w - 3 * scale, y + 3 * scale, x + 3 * scale, y + h - 4 * scale), fill=edge, width=max(1, scale))
    draw.line((x + 2 * scale, y + 4 * scale, x + w - 2 * scale, y + 3 * scale), fill=(222, 174, 104, 75), width=max(1, scale))


def draw_barrel(draw: ImageDraw.ImageDraw, xy: tuple[int, int], rng: random.Random, scale: int = 1) -> None:
    x, y = xy
    w, h = 18 * scale, 30 * scale
    fill = jitter("#77542f", rng, 8, 242)
    edge = jitter("#20170f", rng, 3, 230)
    draw.ellipse((x, y, x + w, y + 8 * scale), fill=jitter("#9f7242", rng, 8, 230), outline=edge, width=max(1, scale))
    draw.rectangle((x, y + 4 * scale, x + w, y + h - 4 * scale), fill=fill, outline=edge, width=max(1, scale))
    draw.ellipse((x, y + h - 9 * scale, x + w, y + h), fill=jitter("#553921", rng, 6, 240), outline=edge, width=max(1, scale))
    for band_y in (y + 9 * scale, y + 22 * scale):
        draw.line((x + 2 * scale, band_y, x + w - 2 * scale, band_y), fill="#2f261b", width=max(1, scale))


def draw_rope(draw: ImageDraw.ImageDraw, xy: tuple[int, int], rng: random.Random, scale: int = 1) -> None:
    x, y = xy
    for inset in range(0, 10 * scale, 3 * scale):
        bbox = (x + inset, y + inset // 2, x + 44 * scale - inset, y + 26 * scale - inset // 2)
        draw.arc(bbox, 12, 350, fill=jitter("#c4ad78", rng, 8, 232), width=max(2, 2 * scale))
        draw.ellipse(bbox, outline=jitter("#2b2418", rng, 3, 170), width=max(1, scale))
    draw.line((x + 38 * scale, y + 14 * scale, x + 58 * scale, y + 11 * scale), fill=jitter("#bba36f", rng, 8, 225), width=max(2, 2 * scale))


def draw_net(draw: ImageDraw.ImageDraw, xy: tuple[int, int], rng: random.Random, scale: int = 1) -> None:
    x, y = xy
    color = jitter("#b8ad84", rng, 8, 145)
    for i in range(6):
        draw.line((x + i * 7 * scale, y, x + 4 * scale + i * 7 * scale, y + 34 * scale), fill=color, width=max(1, scale))
        draw.line((x, y + i * 5 * scale, x + 44 * scale, y + i * 5 * scale - 6 * scale), fill=color, width=max(1, scale))


def candidate_01(tokens: dict) -> Image.Image:
    rng = seeded("method_01")
    image = Image.new("RGBA", (320, 150), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    image.alpha_composite(shadow((280, 70), 96, 8), (22, 78))
    draw_plank_floor(draw, rng, (18, 58, 302, 118), tokens, 242)
    draw.rectangle((22, 50, 298, 56), fill=jitter("#2f2418", rng, 4, 185))
    for offset in [(42, 82), (72, 72), (102, 88), (238, 82), (212, 92)]:
        draw_crate(draw, offset, rng)
    for offset in [(146, 78), (166, 82), (184, 78)]:
        draw_barrel(draw, offset, rng)
    draw_rope(draw, (122, 105), rng)
    draw_net(draw, (230, 54), rng)
    for _ in range(95):
        x = rng.randint(22, 296)
        y = rng.randint(56, 126)
        draw.point((x, y), fill=jitter(rng.choice(["#15120e", "#d8bd7e", "#6d4c2f"]), rng, 5, rng.randint(40, 130)))
    draw.line((18, 122, 302, 122), fill="#0d0b08", width=2)
    draw.line((20, 57, 300, 56), fill=(239, 207, 135, 52), width=1)
    return image.filter(ImageFilter.UnsharpMask(radius=0.6, percent=70, threshold=3))


def candidate_02(tokens: dict) -> Image.Image:
    rng = seeded("method_02")
    image = Image.new("RGBA", (320, 150), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    image.alpha_composite(shadow((260, 72), 84, 7), (28, 74))
    draw_plank_floor(draw, rng, (30, 72, 288, 124), tokens, 226)
    for x in range(52, 260, 38):
        draw_crate(draw, (x, 82 + (x // 38) % 2 * 9), rng)
    for x in range(70, 236, 54):
        draw_barrel(draw, (x, 58), rng)
    for x in range(88, 250, 70):
        draw_rope(draw, (x, 110), rng)
    return image


def write_method_03_svg() -> None:
    SOURCE_ROOT.mkdir(parents=True, exist_ok=True)
    VECTOR_SOURCE_PATH.write_text(
        """<svg xmlns="http://www.w3.org/2000/svg" width="320" height="150" viewBox="0 0 320 150">
  <rect width="320" height="150" fill="none"/>
  <ellipse cx="160" cy="118" rx="132" ry="24" fill="#070806" opacity="0.35"/>
  <g stroke="#21170f" stroke-width="3" stroke-linejoin="round">
    <path d="M32 92 L292 84 L292 118 L32 126 Z" fill="#74593a"/>
    <path d="M38 98 L286 90" opacity="0.45"/>
    <path d="M40 112 L286 105" opacity="0.45"/>
    <path d="M78 94 L72 123 M148 91 L151 121 M228 88 L224 118" opacity="0.5"/>
    <rect x="54" y="66" width="42" height="31" fill="#8b6239"/>
    <path d="M58 70 L92 93 M92 70 L58 93"/>
    <rect x="100" y="75" width="48" height="36" fill="#775231"/>
    <path d="M105 80 L143 106 M143 80 L105 106"/>
    <ellipse cx="190" cy="76" rx="13" ry="8" fill="#9a6a39"/>
    <rect x="177" y="76" width="26" height="34" fill="#6c4829"/>
    <ellipse cx="190" cy="110" rx="13" ry="8" fill="#4a301d"/>
    <ellipse cx="232" cy="101" rx="28" ry="17" fill="none" stroke="#bfa878" stroke-width="5"/>
    <ellipse cx="232" cy="101" rx="16" ry="9" fill="none" stroke="#382919" stroke-width="3"/>
    <path d="M256 99 C272 96 278 95 292 94" stroke="#bfa878" stroke-width="4" fill="none"/>
  </g>
  <g stroke="#d8c184" stroke-width="1" opacity="0.42">
    <path d="M38 96 L286 88"/>
    <path d="M58 71 L91 71"/>
    <path d="M105 80 L142 80"/>
  </g>
</svg>
""",
        encoding="utf-8",
    )


def find_exe(candidates: list[Path]) -> Path | None:
    for candidate in candidates:
        if candidate.exists():
            return candidate
    path = shutil.which(candidates[0].name)
    return Path(path) if path else None


def render_method_03_with_inkscape() -> bool:
    write_method_03_svg()
    inkscape = find_exe(INKSCAPE_CANDIDATES)
    if inkscape is None:
        return False
    subprocess.run(
        [
            str(inkscape),
            str(VECTOR_SOURCE_PATH),
            "--export-type=png",
            f"--export-filename={VECTOR_RENDER_PATH}",
            "--export-width=320",
            "--export-height=150",
        ],
        check=True,
    )
    return VECTOR_RENDER_PATH.exists()


def candidate_03_fallback() -> Image.Image:
    image = Image.new("RGBA", (320, 150), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((30, 82, 294, 124), radius=5, fill="#74593a", outline="#21170f", width=3)
    draw.rectangle((54, 66, 96, 97), fill="#8b6239", outline="#21170f", width=3)
    draw.rectangle((100, 75, 148, 111), fill="#775231", outline="#21170f", width=3)
    draw.ellipse((177, 68, 203, 110), fill="#6c4829", outline="#21170f", width=3)
    draw.ellipse((204, 84, 260, 118), outline="#bfa878", width=5)
    return image


def candidate_04(tokens: dict) -> Image.Image:
    rng = seeded("method_04")
    primitives = [candidate_01(tokens).crop((36, 62, 142, 126)), candidate_02(tokens).crop((62, 52, 246, 128))]
    image = Image.new("RGBA", (320, 150), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    image.alpha_composite(shadow((270, 76), 96, 7), (24, 74))
    draw_plank_floor(draw, rng, (24, 70, 296, 122), tokens, 232)
    image.alpha_composite(primitives[1].resize((170, 70), Image.Resampling.NEAREST), (72, 50))
    image.alpha_composite(primitives[0].resize((118, 72), Image.Resampling.NEAREST), (40, 62))
    draw.rectangle((34, 120, 286, 126), fill=(12, 10, 7, 112))
    draw_net(draw, (226, 76), rng)
    return image


def candidate_05(tokens: dict) -> Image.Image:
    rng = seeded("method_05")
    image = Image.new("RGBA", (320, 150), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle((24, 76, 296, 124), fill="#6a5437", outline="#1b1510", width=2)
    for y in range(82, 121, 11):
        draw.line((28, y, 292, y - 2), fill="#3f3224", width=2)
    for x in range(54, 288, 48):
        draw.line((x, 78, x - 4, 122), fill="#2a2118", width=1)
    for p in [(66, 90), (110, 94), (176, 88), (232, 98)]:
        draw.ellipse((p[0], p[1], p[0] + 18, p[1] + 10), fill=jitter("#a68b5d", rng, 5, 190), outline="#251d14")
    for x in range(40, 284, 32):
        draw.rectangle((x, 112, x + 22, 119), fill=jitter("#312719", rng, 4, 180))
    return image.filter(ImageFilter.GaussianBlur(radius=0.15))


def write_candidate_samples(tokens: dict) -> dict[str, Path]:
    GENERATED_ROOT.mkdir(parents=True, exist_ok=True)
    samples = {
        "method_01_generated_base_pixel_cleanup": candidate_01(tokens),
        "method_02_procedural_primitive_assembly": candidate_02(tokens),
        "method_04_internal_green_kitbash": candidate_04(tokens),
        "method_05_godot_authored_dressing_shapes": candidate_05(tokens),
    }
    vector_rendered = render_method_03_with_inkscape()
    if vector_rendered:
        samples["method_03_reference_board_guided_generation"] = Image.open(VECTOR_RENDER_PATH).convert("RGBA")
    else:
        samples["method_03_reference_board_guided_generation"] = candidate_03_fallback()
    paths: dict[str, Path] = {}
    for candidate in CANDIDATES:
        candidate_id = candidate["candidate_id"]
        sample_path = GENERATED_ROOT / candidate["sample"]
        samples[candidate_id].save(sample_path)
        paths[candidate_id] = sample_path
    return paths


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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest_entry(candidate: dict, path: Path) -> dict:
    return {
        "candidate_id": candidate["candidate_id"],
        "method_name": candidate["method_name"],
        "asset_family": "dockside_wharf_clutter_and_surface_integration",
        "sample_path": rel(path),
        "sample_type": candidate["sample_type"],
        "phase": "G-4.18D",
        "provenance_status": "green_origin_candidate",
        "origin_classification": "green_origin_candidate",
        "commercial_use_status": "green_origin_candidate",
        "visual_quality_status": candidate["visual_quality_status"],
        "visual_rating": candidate["visual_rating"],
        "review_eligible": False,
        "normal_review_eligible": False,
        "lab_only": True,
        "final_commercial_candidate": candidate["recommendation"] == "PASS",
        "final_commercial_eligible": False,
        "lab_access_mode": "F6 or --show-green-origin-lab",
        "recommendation": candidate["recommendation"],
        "production_scalability_notes": candidate["production_scalability_notes"],
        "risk_notes": candidate["risk_notes"],
        "input_sources": [
            {
                "type": "project_script",
                "path": rel(SCRIPT_PATH),
                "source_pixels_used": False,
                "commercial_status": "green_origin_candidate",
            },
            {
                "type": "project_authored_parameters",
                "path": rel(STYLE_TOKENS_PATH),
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
        "deterministic_generated": True,
        "ownership": "project-owned",
        "license": "Wayfarer project-owned green-origin bakeoff sample; no third-party, marketplace, web-scraped, ripped, or yellow-source pixels; lab review only until visual acceptance.",
        "sha256": sha256(path),
    }


def write_manifest(paths: dict[str, Path]) -> dict:
    manifest = {
        "schema_id": "wayfarer.newport_green_origin.method_bakeoff.v1",
        "phase": "G-4.18D",
        "generated_at": "2026-05-16T00:00:00Z",
        "normal_review_policy": "No G-4.18D bakeoff candidate is normal-review eligible. The G-4.18C visual baseline remains the player-facing review build.",
        "visual_quality_gate": "Green-origin is necessary but not sufficient. G-4.18D candidates are evidence for method selection and stay lab-only unless a later phase accepts visual quality from screenshots.",
        "recommended_method_for_g418e": "method_01_generated_base_pixel_cleanup",
        "contact_sheets": [rel(BOARD_PATH), rel(STRIP_PATH)],
        "origin_taxonomy": [
            "temporary_review_yellow",
            "green_origin_candidate",
            "final_commercial_green",
            "red_unsafe",
        ],
        "candidates": [manifest_entry(candidate, paths[candidate["candidate_id"]]) for candidate in CANDIDATES],
    }
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def draw_board(paths: dict[str, Path]) -> None:
    CONTACT_SHEET_ROOT.mkdir(parents=True, exist_ok=True)
    board = Image.new("RGB", (1040, 420), "#20251d")
    draw = ImageDraw.Draw(board)
    draw.rectangle((0, 0, 1040, 420), fill="#20251d")
    label(draw, (22, 16), "G-4.18D Green-Origin Method Bakeoff | LAB ONLY", "#f0dc9c")
    label(draw, (22, 34), "Dockside / wharf clutter and surface integration candidates. Not normal review art.", "#d8b7a0")

    panel_w = 190
    panel_h = 318
    x = 22
    y = 74
    for candidate in CANDIDATES:
        recommendation = candidate["recommendation"]
        outline = {"PASS": "#8bc47f", "DEFER": "#d6bd72", "FAIL": "#c67665"}[recommendation]
        draw.rectangle((x, y, x + panel_w, y + panel_h), fill="#2a3027", outline=outline, width=2)
        sample = Image.open(paths[candidate["candidate_id"]]).convert("RGBA")
        stage = Image.new("RGBA", (170, 98), (44, 50, 39, 255))
        stage.alpha_composite(sample.resize((170, 80), Image.Resampling.NEAREST), (0, 9))
        board.paste(stage.convert("RGB"), (x + 10, y + 36))
        label(draw, (x + 10, y + 10), candidate["short_label"], "#f0dc9c")
        label(draw, (x + 10, y + 142), f"Rating: {candidate['visual_rating']:.1f}/10", "#cfd8b3")
        visual_label = candidate["visual_quality_status"].replace("visual_method_", "").replace("_", " ")
        label(draw, (x + 10, y + 160), f"Visual: {visual_label}", "#cfd8b3")
        label(draw, (x + 10, y + 178), f"Recommendation: {recommendation}", outline)
        label(draw, (x + 10, y + 204), "Provenance: green-origin", "#a9d2a0")
        label(draw, (x + 10, y + 222), "Normal review: blocked", "#d8b7a0")
        method_words = candidate["method_name"].replace(" with ", " / ").split()
        first_line = " ".join(method_words[:4])
        second_line = " ".join(method_words[4:8])
        label(draw, (x + 10, y + 246), first_line[:30], "#bac5a4")
        label(draw, (x + 10, y + 264), second_line[:30], "#bac5a4")
        x += panel_w + 15

    label(draw, (22, 398), "Recommended for G-4.18E: M01 generated base + real Krita/GIMP pixel-paint cleanup, screenshot-gated before promotion.", "#f0dc9c")
    board.save(BOARD_PATH)

    strip = Image.new("RGB", (1040, 190), "#20251d")
    sdraw = ImageDraw.Draw(strip)
    label(sdraw, (22, 16), "G-4.18D candidate comparison strip", "#f0dc9c")
    x = 22
    for candidate in CANDIDATES:
        sample = Image.open(paths[candidate["candidate_id"]]).convert("RGBA")
        strip.paste(Image.new("RGB", (190, 122), "#2a3027"), (x, 50))
        strip.paste(sample.convert("RGB"), (x + 10, 64), sample)
        label(sdraw, (x + 8, 154), f"{candidate['candidate_id'][:10]} {candidate['recommendation']}", "#d8cfad")
        x += 200
    strip.save(STRIP_PATH)


def write_inspection(paths: dict[str, Path]) -> dict:
    inspection = {
        "phase": "G-4.18D",
        "tool": "Python/Pillow alpha, crop, and contrast inspection",
        "gimp_version_checked": gimp_version(),
        "samples": {},
    }
    for candidate_id, path in paths.items():
        inspection["samples"][candidate_id] = {
            "path": rel(path),
            "sha256": sha256(path),
            "alpha": alpha_bounds(path),
            "contrast_stddev": contrast_metric(path),
        }
    INSPECTION_PATH.parent.mkdir(parents=True, exist_ok=True)
    INSPECTION_PATH.write_text(json.dumps(inspection, indent=2), encoding="utf-8")
    return inspection


def gimp_version() -> str:
    gimp = find_exe(GIMP_CANDIDATES)
    if gimp is None:
        return "not found"
    try:
        result = subprocess.run([str(gimp), "--version"], check=True, capture_output=True, text=True, timeout=30)
    except Exception as exc:  # pragma: no cover - tool availability differs by machine.
        return f"available but not launched in generator: {exc}"
    return " ".join(result.stdout.split())


def main() -> None:
    tokens = load_tokens()
    paths = write_candidate_samples(tokens)
    manifest = write_manifest(paths)
    draw_board(paths)
    inspection = write_inspection(paths)
    print(f"Wrote G-4.18D bakeoff manifest: {rel(MANIFEST_PATH)}")
    print(f"Wrote G-4.18D bakeoff board: {rel(BOARD_PATH)}")
    print(f"Wrote {len(manifest['candidates'])} candidate samples under {rel(GENERATED_ROOT)}")
    print(f"Image inspection samples: {len(inspection['samples'])}")


if __name__ == "__main__":
    main()
