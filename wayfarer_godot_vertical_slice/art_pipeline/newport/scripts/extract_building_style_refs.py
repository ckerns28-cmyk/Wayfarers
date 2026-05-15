#!/usr/bin/env python3
"""Extract measurable Newport style targets from existing building sprites."""

from __future__ import annotations

import json
import math
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean

from PIL import Image, ImageDraw, ImageFont


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[3]
PIPELINE_ROOT = PROJECT_ROOT / "art_pipeline" / "newport"
REPORT_PATH = PIPELINE_ROOT / "reports" / "newport_building_style_reference.md"
CONTACT_SHEET_PATH = PIPELINE_ROOT / "generated_contact_sheets" / "newport_building_palette_contact_sheet.png"
STYLE_JSON_PATH = PIPELINE_ROOT / "manifests" / "newport_building_style_values.json"

REFERENCE_GLOBS = [
    PROJECT_ROOT / "assets" / "sprites" / "buildings" / "isolated",
    PROJECT_ROOT / "assets" / "buildings",
]


def rel(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def luminance(rgb: tuple[int, int, int]) -> float:
    r, g, b = rgb
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def saturation(rgb: tuple[int, int, int]) -> float:
    r, g, b = [v / 255.0 for v in rgb]
    hi = max(r, g, b)
    lo = min(r, g, b)
    if hi <= 0.0:
        return 0.0
    return (hi - lo) / hi


def quantize_rgb(rgb: tuple[int, int, int], step: int = 16) -> tuple[int, int, int]:
    return tuple(min(255, int(v // step * step + step // 2)) for v in rgb)


def hex_color(rgb: tuple[int, int, int]) -> str:
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def nontransparent_pixels(image: Image.Image) -> tuple[list[tuple[int, int, int]], tuple[int, int, int, int]]:
    rgba = image.convert("RGBA")
    pixels: list[tuple[int, int, int]] = []
    xs: list[int] = []
    ys: list[int] = []
    width, height = rgba.size
    for y in range(height):
        for x in range(width):
            r, g, b, a = rgba.getpixel((x, y))
            if a > 16:
                pixels.append((r, g, b))
                xs.append(x)
                ys.append(y)
    if not pixels:
        return [], (0, 0, 0, 0)
    return pixels, (min(xs), min(ys), max(xs) + 1, max(ys) + 1)


def top_colors(pixels: list[tuple[int, int, int]], limit: int) -> list[dict]:
    counter = Counter(quantize_rgb(pixel) for pixel in pixels)
    total = max(1, sum(counter.values()))
    return [
        {
            "hex": hex_color(color),
            "rgb": list(color),
            "share": round(count / total, 4),
            "luminance": round(luminance(color), 1),
            "saturation": round(saturation(color), 3),
        }
        for color, count in counter.most_common(limit)
    ]


def color_band(pixels: list[tuple[int, int, int]], low: float, high: float, limit: int) -> list[dict]:
    band = [pixel for pixel in pixels if low <= luminance(pixel) < high]
    return top_colors(band, limit)


def approximate_edge_density(image: Image.Image, bbox: tuple[int, int, int, int]) -> float:
    if bbox == (0, 0, 0, 0):
        return 0.0
    crop = image.convert("RGBA").crop(bbox).resize((96, 96))
    samples = 0
    edges = 0
    for y in range(95):
        for x in range(95):
            r, g, b, a = crop.getpixel((x, y))
            if a < 16:
                continue
            right = crop.getpixel((x + 1, y))
            down = crop.getpixel((x, y + 1))
            for other in [right, down]:
                if other[3] < 16:
                    continue
                delta = abs(r - other[0]) + abs(g - other[1]) + abs(b - other[2])
                samples += 1
                if delta > 42:
                    edges += 1
    return round(edges / max(1, samples), 4)


def collect_sources() -> list[Path]:
    paths: list[Path] = []
    for root in REFERENCE_GLOBS:
        if root.exists():
            paths.extend(sorted(path for path in root.glob("*.png") if not path.name.startswith("._")))
    return paths


def analyze() -> dict:
    sources = collect_sources()
    all_pixels: list[tuple[int, int, int]] = []
    sprite_rows: list[dict] = []

    for path in sources:
        image = Image.open(path).convert("RGBA")
        pixels, bbox = nontransparent_pixels(image)
        if not pixels:
            continue
        all_pixels.extend(pixels[:: max(1, len(pixels) // 30000)])
        bbox_w = max(0, bbox[2] - bbox[0])
        bbox_h = max(0, bbox[3] - bbox[1])
        visible_area = max(1, bbox_w * bbox_h)
        opaque_density = round(len(pixels) / visible_area, 4)
        sprite_rows.append(
            {
                "file": rel(path),
                "size": list(image.size),
                "visible_bbox": list(bbox),
                "visible_size": [bbox_w, bbox_h],
                "opaque_density": opaque_density,
                "edge_density": approximate_edge_density(image, bbox),
                "dominant": top_colors(pixels, 5),
            }
        )

    draw_width_targets = [116, 132, 138, 146, 150, 154, 166, 176, 181, 190, 210, 220, 280]
    visible_widths = [row["visible_size"][0] for row in sprite_rows if row["visible_size"][0] > 0]
    visible_heights = [row["visible_size"][1] for row in sprite_rows if row["visible_size"][1] > 0]
    edge_densities = [row["edge_density"] for row in sprite_rows]

    style = {
        "schema_id": "wayfarer.newport.building_style_values.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_count": len(sprite_rows),
        "source_files": [row["file"] for row in sprite_rows],
        "dominant_palette_bands": top_colors(all_pixels, 16),
        "outline_dark_edge_samples": color_band(all_pixels, 0, 58, 8),
        "common_shadow_colors": color_band(all_pixels, 58, 104, 8),
        "midtone_material_colors": color_band(all_pixels, 104, 168, 10),
        "highlight_colors": [
            color
            for color in color_band(all_pixels, 168, 256, 10)
            if color["saturation"] <= 0.55 or color["luminance"] >= 190
        ][:8],
        "approximate_sprite_pixel_density": {
            "mean_opaque_density": round(mean([row["opaque_density"] for row in sprite_rows]), 4),
            "mean_edge_density": round(mean(edge_densities), 4),
            "visible_width_range_px": [min(visible_widths), max(visible_widths)] if visible_widths else [0, 0],
            "visible_height_range_px": [min(visible_heights), max(visible_heights)] if visible_heights else [0, 0],
            "draw_width_targets_world_px": draw_width_targets,
        },
        "material_notes": {
            "wood": "Weathered tan and umber boards, dark end grain, sparse warm highlights, visible seams.",
            "stone": "Grey-brown slabs/cobbles with chipped warm highlights and green-brown shadow edges.",
            "clapboard": "Muted off-white, blue-grey, and tan siding with dark painterly outlines and narrow plank rhythm.",
            "roof": "Low-saturation red-brown, charcoal, or moss-dark roof masses with edge highlights.",
            "metal_glass": "Small dark accents with restrained blue-grey or warm cream highlights, never saturated.",
        },
        "contact_shadow_examples": {
            "direction": "south/southeast",
            "alpha_range": [0.10, 0.24],
            "color_family": "dark umber, green-brown, blue-green",
            "shape": "soft ellipse or irregular strip under base/props, not a hard black outline",
        },
        "door_window_scale_references": {
            "door_height_to_drawn_building_height": "roughly 0.16-0.26 in the active street sprites",
            "window_height_to_door_height": "roughly 0.35-0.55",
            "hero_prop_height_rule": "barrels, crates, signs, and tables must stay clearly below door height",
            "player_note": "current player is a temporary scale/debug avatar and is not a style reference",
        },
        "per_sprite": sprite_rows,
    }
    return style


def write_report(style: dict) -> None:
    lines: list[str] = []
    lines.append("# Newport Building Style Reference")
    lines.append("")
    lines.append("Generated by `art_pipeline/newport/scripts/extract_building_style_refs.py` from project-owned in-repo building sprites.")
    lines.append("")
    lines.append("This report supports art direction; it does not replace human review.")
    lines.append("")
    lines.append("## Dominant Palette Bands")
    lines.append("")
    for color in style["dominant_palette_bands"]:
        lines.append(f"- `{color['hex']}` share `{color['share']}` luminance `{color['luminance']}` saturation `{color['saturation']}`")
    lines.append("")
    lines.append("## Outline And Dark Edge Samples")
    lines.append("")
    for color in style["outline_dark_edge_samples"]:
        lines.append(f"- `{color['hex']}`")
    lines.append("")
    lines.append("## Common Shadow Colors")
    lines.append("")
    for color in style["common_shadow_colors"]:
        lines.append(f"- `{color['hex']}`")
    lines.append("")
    lines.append("## Highlight Colors")
    lines.append("")
    for color in style["highlight_colors"]:
        lines.append(f"- `{color['hex']}`")
    lines.append("")
    lines.append("## Approximate Sprite Pixel Density")
    lines.append("")
    density = style["approximate_sprite_pixel_density"]
    lines.append(f"- Mean opaque density: `{density['mean_opaque_density']}`")
    lines.append(f"- Mean edge density: `{density['mean_edge_density']}`")
    lines.append(f"- Visible width range: `{density['visible_width_range_px'][0]}-{density['visible_width_range_px'][1]}` px")
    lines.append(f"- Visible height range: `{density['visible_height_range_px'][0]}-{density['visible_height_range_px'][1]}` px")
    lines.append(f"- Active draw-width targets: `{density['draw_width_targets_world_px']}` world px")
    lines.append("")
    lines.append("## Material Notes")
    lines.append("")
    for material, note in style["material_notes"].items():
        lines.append(f"- {material}: {note}")
    lines.append("")
    lines.append("## Contact Shadow Examples")
    lines.append("")
    for key, value in style["contact_shadow_examples"].items():
        lines.append(f"- {key}: `{value}`")
    lines.append("")
    lines.append("## Door And Window Scale References")
    lines.append("")
    for key, value in style["door_window_scale_references"].items():
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("## Per-Sprite Measurements")
    lines.append("")
    lines.append("| File | Visible size | Opaque density | Edge density | Top colors |")
    lines.append("| ---- | ------------ | -------------- | ------------ | ---------- |")
    for row in style["per_sprite"]:
        colors = ", ".join(color["hex"] for color in row["dominant"][:4])
        lines.append(f"| `{row['file']}` | `{row['visible_size'][0]}x{row['visible_size'][1]}` | `{row['opaque_density']}` | `{row['edge_density']}` | `{colors}` |")
    lines.append("")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def make_contact_sheet(style: dict) -> None:
    font = ImageFont.load_default()
    swatch_w = 72
    swatch_h = 54
    label_h = 18
    margin = 18
    section_gap = 28
    width = 1200
    sections = [
        ("dominant", style["dominant_palette_bands"][:12]),
        ("dark edges", style["outline_dark_edge_samples"][:8]),
        ("shadows", style["common_shadow_colors"][:8]),
        ("highlights", style["highlight_colors"][:8]),
    ]
    height = margin + len(sections) * (swatch_h + label_h + section_gap) + 220
    sheet = Image.new("RGB", (width, height), "#283025")
    draw = ImageDraw.Draw(sheet)
    y = margin
    draw.text((margin, y), "Newport building style reference palette", fill="#f1e0ad", font=font)
    y += 28
    for title, colors in sections:
        draw.text((margin, y), title, fill="#f1e0ad", font=font)
        y += 18
        x = margin
        for color in colors:
            rgb = tuple(color["rgb"])
            draw.rectangle((x, y, x + swatch_w, y + swatch_h), fill=rgb)
            draw.rectangle((x, y, x + swatch_w, y + swatch_h), outline="#1b1711", width=2)
            draw.text((x, y + swatch_h + 3), color["hex"], fill="#f4e7bf", font=font)
            x += swatch_w + 16
        y += swatch_h + label_h + section_gap

    thumb_y = y + 4
    draw.text((margin, thumb_y), "source sprite thumbnails", fill="#f1e0ad", font=font)
    thumb_y += 20
    x = margin
    for row in style["per_sprite"][:10]:
        path = PROJECT_ROOT / row["file"]
        image = Image.open(path).convert("RGBA")
        image.thumbnail((88, 88))
        tile = Image.new("RGBA", (96, 96), (46, 53, 39, 255))
        tile.alpha_composite(image, ((96 - image.size[0]) // 2, (96 - image.size[1]) // 2))
        sheet.paste(tile.convert("RGB"), (x, thumb_y))
        draw.rectangle((x, thumb_y, x + 96, thumb_y + 96), outline="#1b1711", width=1)
        x += 108
        if x + 100 > width:
            break

    CONTACT_SHEET_PATH.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(CONTACT_SHEET_PATH)


def main() -> None:
    for path in [REPORT_PATH.parent, CONTACT_SHEET_PATH.parent, STYLE_JSON_PATH.parent]:
        path.mkdir(parents=True, exist_ok=True)
    style = analyze()
    STYLE_JSON_PATH.write_text(json.dumps(style, indent=2), encoding="utf-8")
    write_report(style)
    make_contact_sheet(style)
    print(f"Wrote {rel(REPORT_PATH)}")
    print(f"Wrote {rel(CONTACT_SHEET_PATH)}")
    print(f"Wrote {rel(STYLE_JSON_PATH)}")


if __name__ == "__main__":
    main()
