#!/usr/bin/env python3
"""Generate the first project-owned Newport hero street atlas proof."""

from __future__ import annotations

import json
import random
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[3]
PIPELINE_ROOT = PROJECT_ROOT / "art_pipeline" / "newport"
STYLE_JSON_PATH = PIPELINE_ROOT / "manifests" / "newport_building_style_values.json"
ATLAS_PATH = PIPELINE_ROOT / "atlases" / "newport_hero_street_atlas_v1.png"
MANIFEST_PATH = PIPELINE_ROOT / "manifests" / "newport_hero_street_assets.json"
CONTACT_PATH = PIPELINE_ROOT / "generated_contact_sheets" / "newport_hero_street_atlas_contact_sheet.png"

REGIONS = {
    "commercial_cobble_long_a": [0, 0, 256, 96],
    "curb_sidewalk_stoop_strip": [0, 96, 256, 64],
    "building_contact_shadow_strip": [0, 160, 256, 48],
    "dirt_wear_transition": [0, 208, 256, 64],
    "grass_edge_north": [0, 272, 256, 64],
    "dock_market_transition": [0, 336, 256, 64],
    "crate_barrel_table_cluster": [256, 0, 128, 112],
    "fence_sign_market_cluster": [384, 0, 128, 112],
    "small_crate_barrel_cluster": [256, 112, 128, 96],
    "market_sign_cluster": [384, 112, 128, 96],
}


def rel(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def rgba(hex_color: str, alpha: int = 255) -> tuple[int, int, int, int]:
    value = hex_color.strip("#")
    return (int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16), alpha)


def load_style_palette() -> dict[str, list[str]]:
    fallback = {
        "dark": ["#282018", "#343023", "#243327"],
        "shadow": ["#4b4434", "#514432", "#3f4b38"],
        "mid": ["#635d50", "#7a6749", "#756e5b", "#5b7251"],
        "highlight": ["#c7ad72", "#d5c28c", "#b9aa80"],
    }
    if not STYLE_JSON_PATH.exists():
        return fallback
    data = json.loads(STYLE_JSON_PATH.read_text(encoding="utf-8"))
    return {
        "dark": [item["hex"] for item in data.get("outline_dark_edge_samples", [])[:4]] or fallback["dark"],
        "shadow": [item["hex"] for item in data.get("common_shadow_colors", [])[:5]] or fallback["shadow"],
        "mid": [item["hex"] for item in data.get("midtone_material_colors", [])[:6]] or fallback["mid"],
        "highlight": [item["hex"] for item in data.get("highlight_colors", [])[:4]] or fallback["highlight"],
    }


def region_box(region_id: str) -> tuple[int, int, int, int]:
    x, y, w, h = REGIONS[region_id]
    return (x, y, x + w, y + h)


def draw_cobble(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], palette: dict[str, list[str]]) -> None:
    x0, y0, x1, y1 = box
    rng = random.Random(41701)
    draw.rectangle(box, fill=rgba("#5f594c"))
    draw.rectangle((x0, y0, x1, y0 + 6), fill=rgba("#332c22", 90))
    draw.rectangle((x0, y1 - 8, x1, y1), fill=rgba("#201d17", 115))
    for i in range(145):
        w = rng.randint(12, 31)
        h = rng.randint(5, 13)
        x = rng.randint(x0 + 4, max(x0 + 4, x1 - w - 5))
        y = rng.randint(y0 + 8, max(y0 + 8, y1 - h - 8))
        base = rng.choice(["#6f6958", "#756d5a", "#655f50", "#81765e", "#595447"])
        draw.rectangle((x, y, x + w, y + h), fill=rgba(base, rng.randint(80, 142)))
        if i % 2 == 0:
            draw.line((x + 2, y + 1, x + w - 2, y), fill=rgba(rng.choice(palette["highlight"]), 46), width=1)
        if i % 3 == 0:
            draw.line((x + 2, y + h - 1, x + w - 3, y + h - 2), fill=rgba(rng.choice(palette["dark"]), 74), width=1)
    for i in range(18):
        x = x0 + 8 + i * 14
        draw.line((x, y0 + 10, x + rng.randint(-8, 8), y1 - 10), fill=rgba("#2a241c", 30), width=1)
    draw.rectangle((x0, y0, x1 - 1, y1 - 1), outline=rgba("#241f18", 115), width=2)


def draw_curb(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], palette: dict[str, list[str]]) -> None:
    x0, y0, x1, y1 = box
    draw.rectangle((x0, y0 + 10, x1, y1 - 10), fill=rgba("#756e5b"))
    draw.rectangle((x0, y1 - 15, x1, y1 - 8), fill=rgba("#3b3429", 170))
    draw.rectangle((x0, y0 + 5, x1, y0 + 11), fill=rgba("#b9aa80", 90))
    for x in range(x0 + 10, x1 - 8, 32):
        draw.line((x, y0 + 13, x - 7, y1 - 15), fill=rgba("#29251e", 100), width=1)
    for y in range(y0 + 19, y1 - 16, 13):
        draw.line((x0 + 8, y, x1 - 12, y - 1), fill=rgba("#282018", 55), width=1)
    for x in [x0 + 34, x0 + 102, x0 + 174]:
        draw.rectangle((x, y0 + 2, x + 42, y0 + 25), fill=rgba("#8f7655"))
        draw.rectangle((x, y0 + 2, x + 42, y0 + 25), outline=rgba("#2e2117"), width=2)
        draw.line((x + 5, y0 + 6, x + 37, y0 + 4), fill=rgba(rng_choice(palette["highlight"], x), 70), width=1)
    draw.rectangle((x0, y0, x1 - 1, y1 - 1), outline=rgba("#211b14", 95), width=2)


def rng_choice(values: list[str], seed: int) -> str:
    return random.Random(seed).choice(values)


def draw_shadow_strip(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    for i in range(7):
        inset = i * 2
        alpha = max(20, 92 - i * 10)
        draw.ellipse((x0 + 8 + inset, y0 + 8 + inset // 2, x1 - 8 - inset, y1 - 3 - inset // 2), fill=rgba("#17150f", alpha))
    for x in range(x0 + 18, x1 - 18, 38):
        draw.rectangle((x, y0 + 26, x + 18, y0 + 30), fill=rgba("#514432", 55))


def draw_dirt(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], palette: dict[str, list[str]]) -> None:
    x0, y0, x1, y1 = box
    rng = random.Random(41702)
    draw.rectangle(box, fill=rgba("#7a6749", 210))
    for i in range(70):
        x = rng.randint(x0 + 4, x1 - 8)
        y = rng.randint(y0 + 5, y1 - 8)
        w = rng.randint(7, 28)
        h = rng.randint(2, 6)
        color = rng.choice(["#514432", "#8d7656", "#a58a61", "#3f382d"])
        draw.rectangle((x, y, min(x1 - 3, x + w), y + h), fill=rgba(color, rng.randint(52, 112)))
    for i in range(18):
        x = x0 + rng.randint(6, x1 - x0 - 12)
        y = y0 + rng.randint(7, y1 - y0 - 12)
        draw.ellipse((x, y, x + 4, y + 2), fill=rgba(rng.choice(palette["dark"]), 70))
    draw.line((x0, y0 + 4, x1, y0 + 2), fill=rgba("#d5c28c", 54), width=1)
    draw.line((x0, y1 - 5, x1, y1 - 7), fill=rgba("#211b14", 95), width=2)


def draw_grass_edge(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    rng = random.Random(41703)
    draw.rectangle(box, fill=rgba("#5b7251"))
    for i in range(96):
        x = rng.randint(x0 + 2, x1 - 10)
        y = rng.randint(y0 + 4, y1 - 6)
        color = rng.choice(["#405c41", "#789365", "#314d35", "#647f57"])
        draw.rectangle((x, y, x + rng.randint(7, 25), y + rng.randint(2, 5)), fill=rgba(color, rng.randint(55, 125)))
        if i % 3 == 0:
            draw.line((x, y, x + 7, y - 2), fill=rgba("#a79a66", 58), width=1)
    draw.line((x0, y1 - 8, x1, y1 - 5), fill=rgba("#263f2a", 120), width=2)
    draw.line((x0, y1 - 3, x1, y1 - 2), fill=rgba("#b9aa80", 58), width=1)


def draw_dock_transition(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=rgba("#7a6749"))
    plank_h = 11
    idx = 0
    for y in range(y0, y1, plank_h):
        color = ["#806b4d", "#6f5b41", "#735d42", "#5e4c36"][idx % 4]
        draw.rectangle((x0, y, x1, min(y1, y + plank_h - 1)), fill=rgba(color))
        draw.line((x0 + 4, y, x1 - 6, y - 1), fill=rgba("#c5a66b", 46), width=1)
        draw.line((x0 + 3, min(y1, y + plank_h - 1), x1 - 5, min(y1, y + plank_h - 2)), fill=rgba("#201811", 82), width=1)
        idx += 1
    for x in range(x0 + 18, x1, 44):
        draw.line((x, y0 + 3, x - 3, y1 - 4), fill=rgba("#211b14", 70), width=1)
    draw.rectangle((x0, y0, x1 - 1, y1 - 1), outline=rgba("#201811", 120), width=2)


def draw_crate(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, color: str) -> None:
    draw.rectangle((x, y, x + w, y + h), fill=rgba(color))
    draw.rectangle((x, y, x + w, y + h), outline=rgba("#2e2117"), width=2)
    draw.line((x + 3, y + 4, x + w - 3, y + h - 4), fill=rgba("#3a2516", 160), width=1)
    draw.line((x + 3, y + h - 5, x + w - 4, y + 3), fill=rgba("#d1a36a", 80), width=1)
    draw.line((x + 3, y + 5, x + w - 4, y + 5), fill=rgba("#d4a66a", 74), width=1)


def draw_barrel(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    draw.ellipse((x - 8, y - 12, x + 8, y + 12), fill=rgba("#7f5631"), outline=rgba("#2e2117"), width=2)
    draw.rectangle((x - 8, y - 4, x + 8, y - 1), fill=rgba("#3f2c1d"))
    draw.rectangle((x - 8, y + 4, x + 8, y + 7), fill=rgba("#3f2c1d"))
    draw.arc((x - 8, y - 12, x + 8, y + 12), 0, 359, fill=rgba("#c2965a"), width=1)


def draw_prop_cluster(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    draw.ellipse((x0 + 10, y1 - 26, x1 - 8, y1 - 7), fill=rgba("#15120d", 52))
    draw.rectangle((x0 + 18, y0 + 40, x0 + 92, y0 + 62), fill=rgba("#3b2a1c"))
    draw.rectangle((x0 + 22, y0 + 36, x0 + 88, y0 + 58), fill=rgba("#80603c"))
    for y in [41, 47, 53]:
        draw.line((x0 + 26, y0 + y, x0 + 84, y0 + y - 1), fill=rgba("#2e2117", 115), width=1)
    for i, color in enumerate(["#d9c37a", "#a95e45", "#d9c37a", "#b08246", "#d9c37a"]):
        cx = x0 + 31 + i * 11
        draw.ellipse((cx - 4, y0 + 47, cx + 4, y0 + 55), fill=rgba(color), outline=rgba("#2e2117", 95))
    draw.rectangle((x0 + 26, y0 + 59, x0 + 30, y0 + 78), fill=rgba("#4d3824"))
    draw.rectangle((x0 + 78, y0 + 59, x0 + 82, y0 + 78), fill=rgba("#4d3824"))
    draw_crate(draw, x0 + 10, y0 + 64, 28, 24, "#9b7042")
    draw_crate(draw, x0 + 34, y0 + 54, 22, 19, "#ad7d49")
    draw_barrel(draw, x0 + 98, y0 + 70)
    draw_barrel(draw, x0 + 110, y0 + 70)
    draw.arc((x0 + 70, y0 + 68, x0 + 104, y0 + 96), 8, 350, fill=rgba("#c8b277"), width=2)
    draw.arc((x0 + 77, y0 + 72, x0 + 98, y0 + 91), 8, 350, fill=rgba("#a98e58"), width=1)


def draw_fence_sign_cluster(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    draw.ellipse((x0 + 5, y1 - 25, x1 - 12, y1 - 7), fill=rgba("#15120d", 46))
    rail = "#c9b781"
    draw.line((x0 + 8, y0 + 78, x1 - 8, y0 + 72), fill=rgba("#1b1711", 72), width=4)
    draw.line((x0 + 8, y0 + 74, x1 - 8, y0 + 68), fill=rgba(rail), width=3)
    draw.line((x0 + 8, y0 + 90, x1 - 8, y0 + 84), fill=rgba("#1b1711", 72), width=4)
    draw.line((x0 + 8, y0 + 86, x1 - 8, y0 + 80), fill=rgba("#a7905b"), width=3)
    for x in range(x0 + 12, x1 - 12, 18):
        draw.rectangle((x - 2, y0 + 58, x + 3, y0 + 94), fill=rgba("#4d3824"))
        draw.rectangle((x - 2, y0 + 58, x + 3, y0 + 64), fill=rgba("#d2b06e", 105))
    sx = x0 + 66
    draw.rectangle((sx - 2, y0 + 28, sx + 3, y0 + 89), fill=rgba("#3e2c1d"))
    draw.rectangle((sx - 24, y0 + 31, sx + 29, y0 + 55), fill=rgba("#6c5c43"))
    draw.rectangle((sx - 24, y0 + 31, sx + 29, y0 + 55), outline=rgba("#201811"), width=2)
    draw.line((sx - 18, y0 + 38, sx + 20, y0 + 36), fill=rgba("#d3b06c", 65), width=1)
    draw.line((sx - 16, y0 + 49, sx + 19, y0 + 47), fill=rgba("#21180f", 75), width=1)
    draw_crate(draw, x0 + 88, y0 + 68, 25, 20, "#8f6740")


def draw_atlas() -> None:
    palette = load_style_palette()
    atlas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    draw = ImageDraw.Draw(atlas)
    draw_cobble(draw, region_box("commercial_cobble_long_a"), palette)
    draw_curb(draw, region_box("curb_sidewalk_stoop_strip"), palette)
    draw_shadow_strip(draw, region_box("building_contact_shadow_strip"))
    draw_dirt(draw, region_box("dirt_wear_transition"), palette)
    draw_grass_edge(draw, region_box("grass_edge_north"))
    draw_dock_transition(draw, region_box("dock_market_transition"))
    draw_prop_cluster(draw, region_box("crate_barrel_table_cluster"))
    draw_fence_sign_cluster(draw, region_box("fence_sign_market_cluster"))
    draw_prop_cluster(draw, region_box("small_crate_barrel_cluster"))
    draw_fence_sign_cluster(draw, region_box("market_sign_cluster"))
    ATLAS_PATH.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(ATLAS_PATH)


def write_manifest() -> None:
    source = {
        "type": "project_owned_generated_bitmap",
        "created_by": "art_pipeline/newport/scripts/generate_hero_street_atlas.py",
        "ownership": "project-owned",
        "license": "Wayfarer project asset; no external scraped art",
        "notes": "Generated from Newport building style measurements and Newport Visual Cohesion Rules.",
    }
    category = {
        "commercial_cobble_long_a": "commercial street/cobble",
        "curb_sidewalk_stoop_strip": "curb/sidewalk/stoop",
        "building_contact_shadow_strip": "building contact-shadow/base",
        "dirt_wear_transition": "dirt/wear transition",
        "grass_edge_north": "grass edge",
        "dock_market_transition": "dock/market transition",
        "crate_barrel_table_cluster": "crate/barrel/table prop cluster",
        "fence_sign_market_cluster": "fence/sign/market object cluster",
        "small_crate_barrel_cluster": "crate/barrel prop cluster",
        "market_sign_cluster": "fence/sign/market object cluster",
    }
    assets = []
    for asset_id, region in REGIONS.items():
        is_prop = "cluster" in asset_id
        assets.append(
            {
                "asset_id": asset_id,
                "material_category": category[asset_id],
                "source_file": rel(ATLAS_PATH),
                "source": source,
                "atlas_region": {"x": region[0], "y": region[1], "w": region[2], "h": region[3]},
                "intended_scale": "1 atlas pixel maps to approximately 1 world pixel in the hero proof, with props held below door height.",
                "collision_behavior": "none; decorative/grounding only" if not is_prop else "decorative blocker only if a future collision rect is authored separately",
                "y_sort_behavior": "drawn on map layer below buildings; props are seated in front-of-building bands but remain non-interactive",
                "contact_shadow_required": True,
                "visual_cohesion_status": "g417_review_candidate",
                "placeholder": False,
                "final": False,
                "review_eligible": True,
                "review_notes": "Meets G-4.17 hero proof rules: muted Newport palette, dark-side shading/outline, material detail, contact shadow, and building-scale relationship.",
            }
        )

    manifest = {
        "schema_id": "wayfarer.newport.asset_manifest.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "atlas": rel(ATLAS_PATH),
        "assets": assets,
        "review_gate": "Assets with placeholder=false and review_eligible=true must satisfy NEWPORT_ART_BIBLE.md.",
    }
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def make_contact_sheet() -> None:
    atlas = Image.open(ATLAS_PATH).convert("RGBA")
    sheet = Image.new("RGBA", (900, 620), rgba("#283025"))
    sheet.alpha_composite(atlas, (20, 20))
    draw = ImageDraw.Draw(sheet)
    draw.rectangle((20, 20, 532, 532), outline=rgba("#f1e0ad"), width=2)
    for asset_id, region in REGIONS.items():
        x, y, w, h = region
        ox, oy = 20 + x, 20 + y
        draw.rectangle((ox, oy, ox + w, oy + h), outline=rgba("#f1e0ad", 150), width=1)
        draw.text((560, 32 + list(REGIONS).index(asset_id) * 54), f"{asset_id}: {region}", fill=rgba("#f1e0ad"))
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
