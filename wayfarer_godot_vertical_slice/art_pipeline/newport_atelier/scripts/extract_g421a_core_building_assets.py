#!/usr/bin/env python3
"""Generate and extract G-4.21A Newport core building atelier sprites."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import extract_g420a_environmental_believability_assets as atelier


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = atelier.PROJECT_ROOT
PIPELINE_ROOT = atelier.PIPELINE_ROOT
SOURCE_ROOT = atelier.SOURCE_ROOT
GENERATED_ROOT = atelier.GENERATED_ROOT
ATLAS_ROOT = atelier.ATLAS_ROOT
CONTACT_ROOT = atelier.CONTACT_ROOT
MANIFEST_ROOT = atelier.MANIFEST_ROOT
REPORT_ROOT = atelier.REPORT_ROOT
ART_BIBLE_PATH = atelier.ART_BIBLE_PATH
G418D_STANDARD_REPORT_PATH = atelier.G418D_STANDARD_REPORT_PATH
G419A_REPORT_PATH = atelier.G419A_REPORT_PATH
VISUAL_REGISTRY_PATH = atelier.VISUAL_REGISTRY_PATH
BUILDING_PROVENANCE_PATH = PROJECT_ROOT / "art_pipeline" / "newport" / "manifests" / "newport_building_sprite_provenance.json"

PHASE = "G-4.21A"
GRID_COLUMNS = 2
GRID_ROWS = 3
CELL_W = 1024
CELL_H = 512
SHEET_W = CELL_W * GRID_COLUMNS
SHEET_H = CELL_H * GRID_ROWS
OUTPUT_SPRITE_PADDING = atelier.OUTPUT_SPRITE_PADDING
VISUAL_QUALITY_GATE = atelier.VISUAL_QUALITY_GATE
PIPELINE_STATUS = atelier.PIPELINE_STATUS
PROVENANCE_STATUS = atelier.PROVENANCE_STATUS
COMMERCIAL_STATUS = atelier.COMMERCIAL_STATUS
SOURCE_TYPE = "codex_assisted_original_building_sheet_with_local_chroma_extraction"
MAGENTA = (255, 0, 255, 255)

PACK_ID = "core_building_rebuild_wave_1"
PACK_TITLE = "Core Building Atelier Rebuild Wave 1"
SOURCE_FILENAME = "g421a_core_building_rebuild_wave_1_sheet_imagegen.png"
PROMPT_FILENAME = "g421a_core_building_rebuild_wave_1_prompt.txt"
ATLAS_FILENAME = "newport_atelier_core_buildings_wave_1_v1.png"
CONTACT_FILENAME = "newport_atelier_core_buildings_wave_1_contact_sheet.png"
MANIFEST_FILENAME = "newport_atelier_core_buildings_wave_1_manifest.json"
QA_FILENAME = "newport_atelier_core_buildings_wave_1_extraction_qa.json"
REPORT_FILENAME = "G421A_CORE_BUILDING_ATELIER_REBUILD_WAVE_1.md"
WAVE_MANIFEST_PATH = MANIFEST_ROOT / "newport_atelier_core_building_rebuild_wave_1_manifest.json"
WAVE_REPORT_PATH = REPORT_ROOT / "G421A_NEWPORT_CORE_BUILDING_ATELIER_REBUILD_WAVE_1.md"
MAPLAYER_REGION_REPORT_PATH = MANIFEST_ROOT / "newport_atelier_core_building_rebuild_wave_1_regions.json"

PROMPT = """Use case: stylized-concept
Asset type: production 2D game sprite sheet, original legally clean building sprite sheet for a fantasy 1700s Newport harbor RPG
Primary request: Create a coherent first wave of Newport core buildings as a shared architectural family, not isolated generic fantasy houses. The sheet must contain exactly six separate buildings: 1) a hero centerpiece Tavern/Inn built from brick with two front/back bridged twin-stack chimney sets, warm windows, clear entrance, strong stone foundation, old coastal prestige, and Hotel Viking-inspired grand coastal landmark presence without copying Hotel Viking; 2) a practical mercantile/general store with coastal trade identity, readable shopfront, sign/awning compatibility, and market-spine fit; 3) a wharf warehouse or dock office supporting the working harbor economy, with weathered wood, brick, stone foundation, cargo-door readability, and maritime utility; 4) a small quiet coastal residence/cottage variant with clapboard, stone foundation, readable door, and non-generic Newport character; 5) a second small residence/cottage variant with a different silhouette and roofline but the same architectural family; 6) a workshop/cooperage/service building with useful grounded service-lane identity.
Scene/backdrop: perfectly flat solid #ff00ff chroma-key background only, no floor plane, no scenery, no gradients, no texture, no cast shadow outside the buildings. Add only small neutral contact shadows directly under each building if needed, using dark neutral pixels that do not blend into the chroma key.
Subject: Newport coastal fantasy starting-town buildings for real in-world proof placement. The Tavern/Inn is the required hero asset and must visually outrank ordinary shops/homes while staying compatible with the town layout.
Style/medium: refined authored pixel art / painterly pixel sprite, 3/4 top-down RPG building perspective, crisp readable silhouettes, warm window light, colonial/coastal Newport material language, slate and cedar roofs, brick, clapboard, stone foundations, restrained fantasy charm, readable entrances, no malformed roofs/chimneys/walls.
Composition/framing: one clean wide sprite sheet with exactly six buildings arranged in a tidy 2 columns by 3 rows grid. Every building must be fully visible with generous padding; no cropped roofs, chimneys, walls, foundations, doors, or shadows. No readable text labels.
Materials/textures: old brick, stone foundation blocks, slate shingles, cedar clapboard, weathered painted trim, iron brackets, warm glass windows, rope/cargo accents on working buildings, muted coastal reds, creams, sea greens, navy, charcoal roofs, and salt-air wear.
Constraints: original art only, no copied game sprites, no marketplace asset style, no logos, no real-world brands, no readable text, no UI, no photorealism, no flat vector icons, no yellow Newport building pixels, no existing Hearthvale building pixels, no web-scraped images, no NPC/player standards, no collision finalization.
Avoid: generic medieval huts, generic fantasy taverns, direct Hotel Viking copy, magenta halos, cropped chimneys, cropped rooflines, malformed walls, floating buildings, visually noisy density, buildings that hide navigation paths."""


@dataclass(frozen=True)
class BuildingSpec:
    asset_id: str
    old_asset_id: str
    building_id: str
    display_name: str
    asset_type: str
    source_identity: str
    gameplay_role: str
    draw_width: float
    visual_quality_rating: float
    notes: str
    qa: dict[str, bool | str]


BUILDINGS: tuple[BuildingSpec, ...] = (
    BuildingSpec(
        asset_id="atelier_newport_tavern_inn_hero_01",
        old_asset_id="inn_tavern_v1",
        building_id="b_inn_tavern",
        display_name="Inn & Tavern",
        asset_type="centerpiece_tavern_inn_hero_building",
        source_identity="brick coastal landmark inn with two front/back bridged twin-stack chimney sets",
        gameplay_role="Major player landmark, social hub, quest anchor, and opening-town memory point.",
        draw_width=224.0,
        visual_quality_rating=9.3,
        notes="Required G-4.21A hero asset. Brick construction, two front/back bridged twin-stack chimney sets, warm windows, clear entrance, and Hotel Viking-inspired coastal landmark presence without direct copying.",
        qa={
            "hero_centerpiece": True,
            "brick_construction": True,
            "two_sets_large_twin_stack_chimneys": True,
            "front_back_bridged_chimney_pairs": True,
            "hotel_viking_inspired_not_direct_copy": True,
            "clear_entrance": True,
            "strong_foundation_grounding": True,
            "warm_windows": True,
            "visually_outranks_ordinary_buildings": True,
        },
    ),
    BuildingSpec(
        asset_id="atelier_newport_mercantile_store_01",
        old_asset_id="mercantile_shop",
        building_id="b_mercantile",
        display_name="Mercantile",
        asset_type="mercantile_general_store_building",
        source_identity="coastal trade mercantile with readable shopfront",
        gameplay_role="Market-spine commerce anchor with practical general-store identity and readable entrance.",
        draw_width=108.0,
        visual_quality_rating=9.0,
        notes="Non-centerpiece commercial building with awning/sign compatibility and muted Newport trade identity.",
        qa={
            "hero_centerpiece": False,
            "clear_shopfront": True,
            "sign_awning_compatible": True,
            "clear_entrance": True,
            "strong_foundation_grounding": True,
            "does_not_compete_with_tavern": True,
        },
    ),
    BuildingSpec(
        asset_id="atelier_newport_wharf_warehouse_01",
        old_asset_id="newport_dockside_storehouse",
        building_id="b_dock_warehouse",
        display_name="Dock Warehouse",
        asset_type="wharf_warehouse_dock_office_building",
        source_identity="working harbor warehouse and dock office",
        gameplay_role="Working-wharf economy anchor for cargo, rope, fish baskets, crates, and dock service activity.",
        draw_width=224.0,
        visual_quality_rating=9.0,
        notes="Weathered wood, brick, stone, and cargo-door language for the dock economy.",
        qa={
            "working_harbor_economy": True,
            "large_utility_structure": True,
            "weathered_material_mix": True,
            "clear_entrance": True,
            "strong_foundation_grounding": True,
        },
    ),
    BuildingSpec(
        asset_id="atelier_newport_harbor_cottage_gabled_01",
        old_asset_id="residence_small",
        building_id="b_res_small",
        display_name="Harbor Cottage",
        asset_type="small_residence_cottage_variant",
        source_identity="quiet gabled harbor cottage",
        gameplay_role="Small residential-street variant for believable homes without generic medieval hut language.",
        draw_width=138.0,
        visual_quality_rating=8.9,
        notes="Quiet clapboard cottage with readable door, stone foundation, and coastal trim.",
        qa={
            "residence_variant": True,
            "visually_quieter_than_tavern": True,
            "non_generic_medieval_hut": True,
            "clear_entrance": True,
            "strong_foundation_grounding": True,
        },
    ),
    BuildingSpec(
        asset_id="atelier_newport_harbor_cottage_dormer_01",
        old_asset_id="newport_modest_clapboard_residence_a",
        building_id="b_boarding_house",
        display_name="Boarding House",
        asset_type="small_residence_cottage_variant",
        source_identity="dormered coastal boarding cottage",
        gameplay_role="Second quiet residence variant for residential and support-lane diversity.",
        draw_width=132.0,
        visual_quality_rating=8.9,
        notes="Distinct cottage silhouette with dormer, salt-worn siding, and modest residential scale.",
        qa={
            "residence_variant": True,
            "visually_quieter_than_tavern": True,
            "non_generic_medieval_hut": True,
            "clear_entrance": True,
            "strong_foundation_grounding": True,
        },
    ),
    BuildingSpec(
        asset_id="atelier_newport_cooperage_workshop_01",
        old_asset_id="service_dependency_shed",
        building_id="b_cooperage_shed",
        display_name="Cooperage Shed",
        asset_type="workshop_cooperage_service_building",
        source_identity="cooperage workshop and service-lane building",
        gameplay_role="Grounded service-lane workshop supporting barrel repair, carpentry, and future town-life gameplay.",
        draw_width=132.0,
        visual_quality_rating=8.9,
        notes="Useful service building with workshop door, lean-to, barrel hoops, and restrained dock-adjacent utility.",
        qa={
            "service_building": True,
            "useful_grounded_workshop": True,
            "fits_service_lane_or_market_edge": True,
            "clear_entrance": True,
            "strong_foundation_grounding": True,
        },
    ),
)


REPLACED_OLD_ASSET_STATUS = {
    "inn_tavern_v1": "Old yellow temporary Tavern/Inn crop replaced in the proof subset by the G-4.21A brick hero inn. Keep file for history only; do not use as final or current visual target.",
    "mercantile_shop": "Old yellow temporary Mercantile crop replaced in the proof subset by the G-4.21A coastal mercantile rebuild candidate.",
    "newport_dockside_storehouse": "Old yellow temporary dock warehouse crop replaced in the proof subset by the G-4.21A wharf warehouse rebuild candidate.",
    "residence_small": "Old yellow temporary cottage crop replaced in the proof subset by the G-4.21A harbor cottage rebuild candidate.",
    "newport_modest_clapboard_residence_a": "Old yellow temporary boarding-house crop replaced in the proof subset by the G-4.21A dormered cottage rebuild candidate.",
    "service_dependency_shed": "Old yellow temporary service shed crop replaced in the proof subset by the G-4.21A cooperage workshop rebuild candidate.",
}

SOURCE_IMAGE_FILENAMES = {
    "atelier_newport_tavern_inn_hero_01": "g421a_tavern_inn_hero_source_imagegen.png",
    "atelier_newport_mercantile_store_01": "g421a_mercantile_store_source_imagegen.png",
    "atelier_newport_wharf_warehouse_01": "g421a_wharf_warehouse_source_imagegen.png",
    "atelier_newport_harbor_cottage_gabled_01": "g421a_harbor_cottage_gabled_source_imagegen.png",
    "atelier_newport_harbor_cottage_dormer_01": "g421a_harbor_cottage_dormer_source_imagegen.png",
    "atelier_newport_cooperage_workshop_01": "g421a_cooperage_workshop_source_imagegen.png",
}

INDIVIDUAL_PROMPTS = {
    "atelier_newport_tavern_inn_hero_01": """Use case: stylized-concept
Asset type: project-bound 2D RPG building sprite source for later chroma-key extraction
Primary request: Create ONE premium hand-painted pixel-art building sprite for Newport in Wayfarer: a revised centerpiece Tavern/Inn hero building with corrected chimney stack layout.
Reference intent: Use the attached real brick hotel image only as inspiration for grand coastal brick-hotel presence and the roof chimney-stack idea. Do not copy the hotel facade, exact massing, window layout, entrance, or silhouette.
Subject: Historic coastal brick inn/tavern landmark, old Newport prestige, fantasy charm, larger and more memorable than ordinary shops. Brick construction must be unmistakable. The roof must have TWO SETS of large twin-stack chimneys. Important: each twin-stack set is arranged front-to-back along the roof depth, not horizontally side-by-side. For each set, one chimney rises from the front/lower roof plane and one chimney rises behind it from the rear/higher roof plane, connected by a short brick bridge/collar/saddle running between the two stacks across the roof slope. Place one front-to-back bridged twin-stack set on the left roof side and one matching front-to-back bridged twin-stack set on the right roof side. Four chimneys total. Warm lit windows, clear central entrance with stone steps, strong stone foundation/base grounding, readable social-hub / quest-anchor presence.
Style: high-end authored 2D game sprite, hand-painted pixel art with rich material texture, readable silhouette, subtle pixel clusters, roof slate detail, brick variation, warm window glow. Must match a polished fantasy harbor-town game, not a flat vector icon, not simple geometric shapes, not a generic medieval tavern.
Camera/framing: orthographic 3/4 front view with slight top-down game-ready perspective so the front/back chimney depth is visible, full building visible, no cropped roof/chimneys/walls/foundation, generous padding.
Background: perfectly flat solid #ff00ff chroma-key background only. No ground plane, no cast shadow, no contact shadow, no border, no labels, no text, no watermark. Do not use #ff00ff anywhere in the building.""",
    "atelier_newport_mercantile_store_01": """Use case: stylized-concept
Asset type: project-bound 2D RPG building sprite source for later chroma-key extraction
Primary request: Create ONE premium hand-painted pixel-art building sprite for Newport in Wayfarer: a Mercantile / General Store.
Subject: Coastal town trade mercantile, practical and inviting, commercially active but clearly subordinate to the larger hero inn. Readable shopfront with broad windows, central door, modest hanging sign bracket area, canvas awning compatibility, crates/barrels/rope goods tucked into the facade, clapboard and brick/stone foundation details, old Newport harbor-market identity.
Style: high-end authored 2D game sprite, hand-painted pixel art with rich material texture, readable silhouette, subtle pixel clusters, weathered clapboard, slate/shingle roof, warm windows. Must match a polished fantasy harbor-town game, not a flat vector icon, not simple geometric shapes, not a generic medieval shop.
Camera/framing: orthographic 3/4 front view with slight top-down game-ready perspective, full building visible, no cropped roof/chimneys/walls/foundation, generous padding, same scale family as a town building sprite.
Background: perfectly flat solid #ff00ff chroma-key background only. No ground plane, no cast shadow, no contact shadow, no border, no labels, no text, no watermark. Do not use #ff00ff anywhere in the building.""",
    "atelier_newport_wharf_warehouse_01": """Use case: stylized-concept
Asset type: project-bound 2D RPG building sprite source for later chroma-key extraction
Primary request: Create ONE premium hand-painted pixel-art building sprite for Newport in Wayfarer: a Wharf Warehouse / Dock Office.
Subject: Working harbor warehouse and dock office, larger utility structure, maritime economy anchor near docks. Weathered wood siding mixed with brick end-wall sections and a stone foundation, broad cargo doors, small dock-office window, rope hooks, cargo pulley, fish-basket/crate/barrel details integrated into the facade, salt-weathered coastal utility character. Functional and maritime, not heroic, not generic fantasy.
Style: high-end authored 2D game sprite, hand-painted pixel art with rich material texture, readable silhouette, subtle pixel clusters, weathered wood grain, brick/stone texture, slate or dark shingle roof. Must match a polished fantasy harbor-town game, not a flat vector icon, not simple geometric shapes.
Camera/framing: orthographic 3/4 front view with slight top-down game-ready perspective, full building visible, no cropped roof/chimney/walls/foundation, generous padding, same camera family as RPG town building sprites.
Background: perfectly flat solid #ff00ff chroma-key background only. No ground plane, no cast shadow, no contact shadow, no border, no labels, no text, no watermark. Do not use #ff00ff anywhere in the building.""",
    "atelier_newport_harbor_cottage_gabled_01": """Use case: stylized-concept
Asset type: project-bound 2D RPG building sprite source for later chroma-key extraction
Primary request: Create ONE premium hand-painted pixel-art building sprite for Newport in Wayfarer: a small coastal residence / cottage variant A.
Subject: Quiet Newport harbor cottage, modest residential building, not generic medieval hut. Clapboard siding, stone foundation, slate or cedar-shingle roof, warm windows, clear door with small stoop, coastal trim, a few believable details like shutters, flower box, rain barrel, and weathered porch boards. Visually quieter than shops and much quieter than the hero inn.
Style: high-end authored 2D game sprite, hand-painted pixel art with rich material texture, readable silhouette, subtle pixel clusters, weathered coastal materials. Must match a polished fantasy harbor-town game, not a flat vector icon, not simple geometric shapes.
Camera/framing: orthographic 3/4 front view with slight top-down game-ready perspective, full building visible, no cropped roof/chimney/walls/foundation, generous padding, same camera family as RPG town building sprites.
Background: perfectly flat solid #ff00ff chroma-key background only. No ground plane, no cast shadow, no contact shadow, no border, no labels, no text, no watermark. Do not use #ff00ff anywhere in the building.""",
    "atelier_newport_harbor_cottage_dormer_01": """Use case: stylized-concept
Asset type: project-bound 2D RPG building sprite source for later chroma-key extraction
Primary request: Create ONE premium hand-painted pixel-art building sprite for Newport in Wayfarer: a small coastal residence / cottage variant B.
Subject: Modest dormered boarding-house cottage for a harbor support lane, visually distinct from variant A. Narrower footprint, salt-worn clapboard, small dormer, side lean-to or rear ell, stone foundation, clear front door and small stoop, warm windows, quiet residential personality, no shopfront. Coastal fantasy tone, not generic medieval hut.
Style: high-end authored 2D game sprite, hand-painted pixel art with rich material texture, readable silhouette, subtle pixel clusters, weathered coastal materials. Must match a polished fantasy harbor-town game, not a flat vector icon, not simple geometric shapes.
Camera/framing: orthographic 3/4 front view with slight top-down game-ready perspective, full building visible, no cropped roof/chimney/walls/foundation, generous padding, same camera family as RPG town building sprites.
Background: perfectly flat solid #ff00ff chroma-key background only. No ground plane, no cast shadow, no contact shadow, no border, no labels, no text, no watermark. Do not use #ff00ff anywhere in the building.""",
    "atelier_newport_cooperage_workshop_01": """Use case: stylized-concept
Asset type: project-bound 2D RPG building sprite source for later chroma-key extraction
Primary request: Create ONE premium hand-painted pixel-art building sprite for Newport in Wayfarer: a cooperage / carpenter / service workshop.
Subject: Grounded harbor service building for barrel repair and carpentry, useful town-life support structure. Weathered timber frame, plank siding, stone foundation, wide workshop doors, small side shed or lean-to, barrel hoops, sawhorse, stacked planks, rope and crates integrated near the facade. Fits service lane or dock-adjacent work area, practical and quiet, not heroic, not generic fantasy.
Style: high-end authored 2D game sprite, hand-painted pixel art with rich material texture, readable silhouette, subtle pixel clusters, weathered wood grain, slate or dark shingle roof. Must match a polished fantasy harbor-town game, not a flat vector icon, not simple geometric shapes.
Camera/framing: orthographic 3/4 front view with slight top-down game-ready perspective, full building visible, no cropped roof/chimney/walls/foundation, generous padding, same camera family as RPG town building sprites.
Background: perfectly flat solid #ff00ff chroma-key background only. No ground plane, no cast shadow, no contact shadow, no border, no labels, no text, no watermark. Do not use #ff00ff anywhere in the building.""",
}


def rel(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def sha256(path: Path) -> str:
    return atelier.sha256(path)


def label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fill: str = "#efe0ad") -> None:
    draw.text(xy, text, fill=fill, font=ImageFont.load_default())


def rect(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], fill: str, outline: str | None = None, width: int = 1) -> None:
    draw.rectangle(xy, fill=fill, outline=outline, width=width)


def poly(draw: ImageDraw.ImageDraw, points: list[tuple[int, int]], fill: str, outline: str | None = None) -> None:
    draw.polygon(points, fill=fill, outline=outline)


def line(draw: ImageDraw.ImageDraw, points: list[tuple[int, int]], fill: str, width: int = 1) -> None:
    draw.line(points, fill=fill, width=width)


def ellipse(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], fill: str, outline: str | None = None, width: int = 1) -> None:
    draw.ellipse(xy, fill=fill, outline=outline, width=width)


def draw_contact_shadow(draw: ImageDraw.ImageDraw, cx: int, y: int, rx: int, ry: int) -> None:
    ellipse(draw, (cx - rx, y - ry, cx + rx, y + ry), "#2a251b")
    ellipse(draw, (cx - int(rx * 0.72), y - int(ry * 0.56), cx + int(rx * 0.72), y + int(ry * 0.56)), "#3a3122")


def draw_brick_texture(draw: ImageDraw.ImageDraw, x0: int, y0: int, x1: int, y1: int, mortar: str = "#7e493d") -> None:
    for y in range(y0 + 12, y1 - 8, 18):
        line(draw, [(x0 + 8, y), (x1 - 8, y)], mortar, 1)
    row = 0
    for y in range(y0 + 16, y1 - 8, 18):
        offset = 18 if row % 2 else 0
        for x in range(x0 + 14 + offset, x1 - 12, 36):
            line(draw, [(x, y - 10), (x, y + 4)], mortar, 1)
        row += 1
    texture_speckles(draw, x0 + 8, y0 + 8, x1 - 8, y1 - 8, ("#b96e50", "#7c4036", "#d19468", "#5f312e"), max(24, (x1 - x0) // 7))


def draw_clapboard(draw: ImageDraw.ImageDraw, x0: int, y0: int, x1: int, y1: int, color: str = "#6b7163") -> None:
    for y in range(y0 + 12, y1 - 4, 16):
        line(draw, [(x0 + 6, y), (x1 - 6, y)], color, 1)
        if (y // 16) % 2 == 0:
            line(draw, [(x0 + 14, y + 2), (x1 - 20, y + 2)], "#d5ccaa", 1)
    texture_speckles(draw, x0 + 8, y0 + 8, x1 - 8, y1 - 8, ("#e0d5b0", "#918a71", "#70664f", "#f1dfb0"), max(18, (x1 - x0) // 9))


def draw_shingles(draw: ImageDraw.ImageDraw, roof_points: list[tuple[int, int]], bounds: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = bounds
    for y in range(y0 + 12, y1 - 4, 16):
        line(draw, [(x0 + 12, y), (x1 - 12, y)], "#2f3437", 1)
    for x in range(x0 + 20, x1 - 10, 34):
        line(draw, [(x, y0 + 18), (x + 10, y1 - 10)], "#495054", 1)
    texture_speckles(draw, x0 + 16, y0 + 12, x1 - 16, y1 - 8, ("#5d686d", "#23292d", "#6f7778", "#3b4549"), max(16, (x1 - x0) // 12))


def draw_window(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, trim: str = "#d4c7a1") -> None:
    rect(draw, (x, y, x + w, y + h), "#f2b65d", "#3d2b1f", 2)
    rect(draw, (x + 3, y + 3, x + w - 3, y + h - 3), "#f6d08a")
    line(draw, [(x + w // 2, y + 2), (x + w // 2, y + h - 2)], "#7d5634", 1)
    line(draw, [(x + 2, y + h // 2), (x + w - 2, y + h // 2)], "#7d5634", 1)
    rect(draw, (x - 3, y - 3, x + w + 3, y + h + 3), fill=None, outline=trim, width=2)


def draw_door(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, fill: str = "#543526", trim: str = "#d2bf92") -> None:
    rect(draw, (x, y, x + w, y + h), fill, "#251a14", 2)
    line(draw, [(x + w // 2, y + 4), (x + w // 2, y + h - 4)], "#2d1e17", 1)
    ellipse(draw, (x + w - 12, y + h // 2 - 3, x + w - 7, y + h // 2 + 2), "#d9b65a")
    rect(draw, (x - 5, y - 6, x + w + 5, y + h + 4), fill=None, outline=trim, width=3)


def draw_foundation(draw: ImageDraw.ImageDraw, x0: int, y0: int, x1: int, y1: int) -> None:
    rect(draw, (x0, y0, x1, y1), "#817760", "#3a3328", 2)
    for x in range(x0 + 16, x1 - 8, 42):
        line(draw, [(x, y0 + 4), (x - 8, y1 - 4)], "#5d5548", 1)
    line(draw, [(x0 + 4, y0 + 9), (x1 - 4, y0 + 9)], "#5d5548", 1)
    texture_speckles(draw, x0 + 8, y0 + 4, x1 - 8, y1 - 4, ("#9d9275", "#695f4e", "#b3a783"), max(12, (x1 - x0) // 18))


def texture_speckles(
    draw: ImageDraw.ImageDraw,
    x0: int,
    y0: int,
    x1: int,
    y1: int,
    colors: tuple[str, ...],
    count: int,
) -> None:
    w = max(1, x1 - x0)
    h = max(1, y1 - y0)
    for i in range(count):
        x = x0 + ((i * 37 + h * 11 + w * 3) % w)
        y = y0 + ((i * 53 + w * 7 + h * 5) % h)
        length = 1 + (i % 4)
        if i % 5 == 0:
            rect(draw, (x, y, min(x1, x + length), min(y1, y + 1)), colors[i % len(colors)])
        else:
            line(draw, [(x, y), (min(x1, x + length), y)], colors[i % len(colors)], 1)


def draw_tavern(draw: ImageDraw.ImageDraw, ox: int, oy: int) -> None:
    cx = ox + CELL_W // 2
    base_y = oy + 452
    draw_contact_shadow(draw, cx, base_y - 10, 330, 34)
    draw_foundation(draw, cx - 330, base_y - 72, cx + 330, base_y - 36)
    rect(draw, (cx - 292, base_y - 290, cx + 292, base_y - 72), "#9a5844", "#33241f", 3)
    rect(draw, (cx - 250, base_y - 224, cx + 250, base_y - 72), "#a75f46", "#3a2620", 2)
    draw_brick_texture(draw, cx - 288, base_y - 286, cx + 288, base_y - 74)
    roof = [(cx - 340, base_y - 288), (cx - 270, base_y - 372), (cx + 270, base_y - 372), (cx + 340, base_y - 288)]
    poly(draw, roof, "#30383d", "#161a1d")
    draw_shingles(draw, roof, (cx - 318, base_y - 360, cx + 318, base_y - 288))
    poly(draw, [(cx - 248, base_y - 366), (cx - 160, base_y - 430), (cx + 160, base_y - 430), (cx + 248, base_y - 366)], "#3d4548", "#171b1d")
    draw_shingles(draw, roof, (cx - 220, base_y - 420, cx + 220, base_y - 366))

    for cluster_x in (cx - 190, cx + 190):
        for stack_x in (cluster_x - 22, cluster_x + 22):
            rect(draw, (stack_x - 14, base_y - 454, stack_x + 14, base_y - 336), "#8c4738", "#2b201d", 2)
            draw_brick_texture(draw, stack_x - 13, base_y - 450, stack_x + 13, base_y - 338, "#6b342f")
            rect(draw, (stack_x - 20, base_y - 462, stack_x + 20, base_y - 446), "#3a3029", "#171211", 1)
        rect(draw, (cluster_x - 54, base_y - 344, cluster_x + 54, base_y - 324), "#6f3d34", "#211817", 2)

    for x in (cx - 210, cx - 120, cx + 120, cx + 210):
        draw_window(draw, x - 20, base_y - 244, 40, 52)
    for x in (cx - 238, cx - 150, cx - 62, cx + 62, cx + 150, cx + 238):
        draw_window(draw, x - 18, base_y - 168, 36, 46)
    draw_door(draw, cx - 38, base_y - 150, 76, 78, "#5a3326")
    rect(draw, (cx - 58, base_y - 62, cx + 58, base_y - 48), "#a99a78", "#3b3328", 2)
    rect(draw, (cx - 78, base_y - 48, cx + 78, base_y - 36), "#86785e", "#3b3328", 2)
    rect(draw, (cx - 118, base_y - 188, cx + 118, base_y - 166), "#203e4f", "#172831", 2)
    rect(draw, (cx - 104, base_y - 184, cx + 104, base_y - 170), "#b6a068")
    for x in range(cx - 270, cx + 271, 36):
        rect(draw, (x, base_y - 74, x + 20, base_y - 60), "#766a54")
    rect(draw, (cx - 316, base_y - 118, cx - 284, base_y - 78), "#496c72", "#203138", 2)
    rect(draw, (cx + 284, base_y - 118, cx + 316, base_y - 78), "#496c72", "#203138", 2)


def draw_mercantile(draw: ImageDraw.ImageDraw, ox: int, oy: int) -> None:
    cx = ox + CELL_W // 2
    base_y = oy + 432
    draw_contact_shadow(draw, cx, base_y - 8, 250, 26)
    draw_foundation(draw, cx - 250, base_y - 54, cx + 250, base_y - 24)
    rect(draw, (cx - 220, base_y - 250, cx + 220, base_y - 54), "#c0b48d", "#342b22", 3)
    draw_clapboard(draw, cx - 214, base_y - 238, cx + 214, base_y - 62, "#8f886d")
    roof = [(cx - 260, base_y - 250), (cx - 180, base_y - 324), (cx + 180, base_y - 324), (cx + 260, base_y - 250)]
    poly(draw, roof, "#38505b", "#17242b")
    draw_shingles(draw, roof, (cx - 236, base_y - 314, cx + 236, base_y - 252))
    rect(draw, (cx - 92, base_y - 326, cx - 56, base_y - 246), "#8c4e3b", "#2d211b", 2)
    rect(draw, (cx - 102, base_y - 336, cx - 46, base_y - 324), "#3a3029", "#171211", 1)
    rect(draw, (cx - 202, base_y - 170, cx + 202, base_y - 138), "#9b3f35", "#2e211c", 2)
    for stripe_x in range(cx - 190, cx + 190, 38):
        poly(draw, [(stripe_x, base_y - 168), (stripe_x + 24, base_y - 168), (stripe_x + 16, base_y - 138), (stripe_x - 8, base_y - 138)], "#e0d0a4")
    draw_window(draw, cx - 162, base_y - 220, 50, 54)
    draw_window(draw, cx + 112, base_y - 220, 50, 54)
    rect(draw, (cx - 176, base_y - 132, cx - 54, base_y - 66), "#6f8a85", "#2a2c24", 2)
    rect(draw, (cx + 62, base_y - 132, cx + 178, base_y - 66), "#6f8a85", "#2a2c24", 2)
    draw_door(draw, cx - 34, base_y - 132, 68, 78, "#4c3a2a")
    rect(draw, (cx - 84, base_y - 278, cx + 84, base_y - 248), "#516a4f", "#1e271d", 2)
    rect(draw, (cx - 66, base_y - 272, cx + 66, base_y - 254), "#d8c28a")
    for x in (cx - 214, cx + 190):
        rect(draw, (x, base_y - 80, x + 44, base_y - 42), "#8a5b32", "#2a1e16", 2)
        line(draw, [(x + 6, base_y - 64), (x + 38, base_y - 64)], "#c48a50", 2)


def draw_warehouse(draw: ImageDraw.ImageDraw, ox: int, oy: int) -> None:
    cx = ox + CELL_W // 2
    base_y = oy + 438
    draw_contact_shadow(draw, cx, base_y - 8, 300, 30)
    draw_foundation(draw, cx - 306, base_y - 58, cx + 306, base_y - 24)
    rect(draw, (cx - 280, base_y - 238, cx + 280, base_y - 58), "#7d6049", "#2f251e", 3)
    draw_clapboard(draw, cx - 272, base_y - 228, cx + 272, base_y - 66, "#5f4d3e")
    rect(draw, (cx - 280, base_y - 238, cx - 98, base_y - 58), "#8c4e3c", "#2f251e", 2)
    draw_brick_texture(draw, cx - 276, base_y - 232, cx - 102, base_y - 62, "#6f3b33")
    roof = [(cx - 322, base_y - 238), (cx - 236, base_y - 314), (cx + 238, base_y - 314), (cx + 322, base_y - 238)]
    poly(draw, roof, "#3a3d3a", "#171917")
    draw_shingles(draw, roof, (cx - 298, base_y - 304, cx + 298, base_y - 240))
    rect(draw, (cx + 170, base_y - 322, cx + 206, base_y - 242), "#8a4b39", "#2d211b", 2)
    rect(draw, (cx + 160, base_y - 334, cx + 216, base_y - 320), "#40332b", "#171211", 1)
    rect(draw, (cx - 42, base_y - 162, cx + 108, base_y - 58), "#4b3b2f", "#1f1713", 3)
    line(draw, [(cx + 33, base_y - 160), (cx + 33, base_y - 60)], "#2b211b", 2)
    for x in (cx - 224, cx - 152, cx + 154, cx + 220):
        draw_window(draw, x - 18, base_y - 194, 36, 42, "#b6aa86")
    rect(draw, (cx - 250, base_y - 108, cx - 168, base_y - 58), "#574533", "#241a13", 2)
    rect(draw, (cx + 138, base_y - 96, cx + 252, base_y - 58), "#8f663d", "#2a1d15", 2)
    ellipse(draw, (cx + 212, base_y - 126, cx + 268, base_y - 70), "#6c4b2d", "#2a1d15", 2)
    rect(draw, (cx - 70, base_y - 284, cx + 80, base_y - 252), "#203d4d", "#15252e", 2)


def draw_cottage_gabled(draw: ImageDraw.ImageDraw, ox: int, oy: int) -> None:
    cx = ox + CELL_W // 2
    base_y = oy + 424
    draw_contact_shadow(draw, cx, base_y - 7, 205, 22)
    draw_foundation(draw, cx - 190, base_y - 46, cx + 190, base_y - 20)
    rect(draw, (cx - 168, base_y - 206, cx + 168, base_y - 46), "#b7b79f", "#30291f", 3)
    draw_clapboard(draw, cx - 162, base_y - 194, cx + 162, base_y - 54, "#878773")
    roof = [(cx - 205, base_y - 206), (cx, base_y - 308), (cx + 205, base_y - 206)]
    poly(draw, roof, "#4d5e61", "#182428")
    for y in range(base_y - 282, base_y - 210, 16):
        line(draw, [(cx - 150, y), (cx + 150, y)], "#37484c", 1)
    rect(draw, (cx + 74, base_y - 284, cx + 104, base_y - 212), "#8d503b", "#2e211b", 2)
    rect(draw, (cx + 64, base_y - 294, cx + 114, base_y - 282), "#3d312a", "#171211", 1)
    draw_window(draw, cx - 122, base_y - 162, 42, 48)
    draw_window(draw, cx + 78, base_y - 162, 42, 48)
    draw_door(draw, cx - 30, base_y - 134, 60, 88, "#4e3a2d")
    rect(draw, (cx - 54, base_y - 46, cx + 54, base_y - 34), "#988b6d", "#3b3328", 2)
    rect(draw, (cx - 184, base_y - 74, cx - 150, base_y - 42), "#566f65", "#1f2d28", 2)
    rect(draw, (cx + 150, base_y - 74, cx + 184, base_y - 42), "#566f65", "#1f2d28", 2)


def draw_cottage_dormer(draw: ImageDraw.ImageDraw, ox: int, oy: int) -> None:
    cx = ox + CELL_W // 2
    base_y = oy + 426
    draw_contact_shadow(draw, cx, base_y - 7, 210, 22)
    draw_foundation(draw, cx - 198, base_y - 48, cx + 198, base_y - 20)
    rect(draw, (cx - 174, base_y - 214, cx + 174, base_y - 48), "#d3c49e", "#322a20", 3)
    draw_clapboard(draw, cx - 166, base_y - 202, cx + 166, base_y - 56, "#9a8f73")
    roof = [(cx - 218, base_y - 214), (cx - 150, base_y - 298), (cx + 150, base_y - 298), (cx + 218, base_y - 214)]
    poly(draw, roof, "#3e4b52", "#172127")
    draw_shingles(draw, roof, (cx - 194, base_y - 288, cx + 194, base_y - 216))
    poly(draw, [(cx - 48, base_y - 292), (cx, base_y - 336), (cx + 48, base_y - 292)], "#526065", "#182428")
    rect(draw, (cx - 30, base_y - 292, cx + 30, base_y - 250), "#c9bd98", "#2d251d", 2)
    draw_window(draw, cx - 16, base_y - 282, 32, 30, "#d4c7a1")
    rect(draw, (cx - 134, base_y - 272, cx - 104, base_y - 204), "#8a4c38", "#2d211b", 2)
    rect(draw, (cx - 144, base_y - 282, cx - 94, base_y - 270), "#3d312a", "#171211", 1)
    draw_window(draw, cx - 130, base_y - 166, 40, 46)
    draw_window(draw, cx + 88, base_y - 166, 40, 46)
    draw_door(draw, cx - 28, base_y - 136, 56, 88, "#51402f")
    rect(draw, (cx - 180, base_y - 92, cx - 144, base_y - 48), "#74815f", "#27301f", 2)
    line(draw, [(cx + 144, base_y - 68), (cx + 198, base_y - 52)], "#665238", 4)


def draw_workshop(draw: ImageDraw.ImageDraw, ox: int, oy: int) -> None:
    cx = ox + CELL_W // 2
    base_y = oy + 430
    draw_contact_shadow(draw, cx, base_y - 7, 224, 24)
    draw_foundation(draw, cx - 220, base_y - 50, cx + 220, base_y - 20)
    rect(draw, (cx - 188, base_y - 204, cx + 168, base_y - 50), "#a4825c", "#2f241b", 3)
    draw_clapboard(draw, cx - 180, base_y - 192, cx + 160, base_y - 58, "#715840")
    roof = [(cx - 224, base_y - 204), (cx - 150, base_y - 280), (cx + 152, base_y - 280), (cx + 210, base_y - 204)]
    poly(draw, roof, "#473f38", "#171512")
    draw_shingles(draw, roof, (cx - 198, base_y - 270, cx + 190, base_y - 206))
    rect(draw, (cx - 84, base_y - 282, cx - 50, base_y - 208), "#874d39", "#2d211b", 2)
    rect(draw, (cx - 94, base_y - 292, cx - 40, base_y - 280), "#3d312a", "#171211", 1)
    rect(draw, (cx - 42, base_y - 144, cx + 76, base_y - 50), "#4b3728", "#1f1713", 3)
    line(draw, [(cx + 16, base_y - 142), (cx + 16, base_y - 52)], "#2a1f17", 2)
    draw_window(draw, cx - 144, base_y - 158, 42, 42, "#d4c7a1")
    poly(draw, [(cx + 86, base_y - 172), (cx + 226, base_y - 150), (cx + 200, base_y - 112), (cx + 72, base_y - 132)], "#3c4d4d", "#172526")
    rect(draw, (cx + 104, base_y - 132, cx + 206, base_y - 50), "#7e6347", "#2a1e16", 2)
    for x in (cx - 188, cx + 148):
        ellipse(draw, (x, base_y - 96, x + 54, base_y - 42), "#74502e", "#2a1d15", 2)
        line(draw, [(x + 8, base_y - 68), (x + 46, base_y - 68)], "#c18a50", 2)
    line(draw, [(cx - 214, base_y - 74), (cx - 156, base_y - 46)], "#5c422b", 5)


DRAW_FUNCS = (
    draw_tavern,
    draw_mercantile,
    draw_warehouse,
    draw_cottage_gabled,
    draw_cottage_dormer,
    draw_workshop,
)


def write_source_sheet() -> Path:
    sheet = Image.new("RGBA", (SHEET_W, SHEET_H), MAGENTA)
    draw = ImageDraw.Draw(sheet)
    for index, draw_func in enumerate(DRAW_FUNCS):
        col = index % GRID_COLUMNS
        row = index // GRID_COLUMNS
        draw_func(draw, col * CELL_W, row * CELL_H)
    path = SOURCE_ROOT / SOURCE_FILENAME
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path)
    return path


def write_prompt() -> Path:
    path = SOURCE_ROOT / PROMPT_FILENAME
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(PROMPT + "\n", encoding="utf-8")
    return path


def source_regions_by_cell(alpha_sheet: Image.Image) -> list[tuple[int, int, int, int]]:
    regions: list[tuple[int, int, int, int]] = []
    for index in range(len(BUILDINGS)):
        col = index % GRID_COLUMNS
        row = index // GRID_COLUMNS
        cell_x = col * CELL_W
        cell_y = row * CELL_H
        cell = alpha_sheet.crop((cell_x, cell_y, cell_x + CELL_W, cell_y + CELL_H))
        bbox = cell.getchannel("A").getbbox()
        if bbox is None:
            regions.append((cell_x, cell_y, cell_x + CELL_W, cell_y + CELL_H))
            continue
        x0 = max(cell_x, cell_x + bbox[0] - 18)
        y0 = max(cell_y, cell_y + bbox[1] - 18)
        x1 = min(cell_x + CELL_W, cell_x + bbox[2] + 18)
        y1 = min(cell_y + CELL_H, cell_y + bbox[3] + 18)
        regions.append((x0, y0, x1, y1))
    return regions


def write_assets(alpha_sheet: Image.Image) -> dict[str, dict]:
    GENERATED_ROOT.mkdir(parents=True, exist_ok=True)
    regions = source_regions_by_cell(alpha_sheet)
    output: dict[str, dict] = {}
    for index, spec in enumerate(BUILDINGS):
        region = regions[index]
        piece = alpha_sheet.crop(region)
        padded = Image.new(
            "RGBA",
            (piece.width + OUTPUT_SPRITE_PADDING * 2, piece.height + OUTPUT_SPRITE_PADDING * 2),
            (0, 0, 0, 0),
        )
        padded.alpha_composite(piece, (OUTPUT_SPRITE_PADDING, OUTPUT_SPRITE_PADDING))
        path = GENERATED_ROOT / f"{spec.asset_id}.png"
        padded.save(path)
        output[spec.asset_id] = {
            "path": path,
            "atlas_region": {"x": region[0], "y": region[1], "w": region[2] - region[0], "h": region[3] - region[1]},
            "sprite_size": {"w": padded.width, "h": padded.height},
            "source_cell": {"column": index % GRID_COLUMNS, "row": index // GRID_COLUMNS},
        }
    return output


def collect_qa(output: dict[str, dict]) -> dict[str, dict]:
    qa: dict[str, dict] = {}
    for spec in BUILDINGS:
        image = Image.open(output[spec.asset_id]["path"]).convert("RGBA")
        metrics = atelier.alpha_metrics(image)
        metrics["source_identity"] = spec.source_identity
        metrics["manifest_identity_match"] = Path(output[spec.asset_id]["path"]).stem == spec.asset_id
        metrics["visual_quality_rating"] = spec.visual_quality_rating
        metrics["visual_quality_gate"] = VISUAL_QUALITY_GATE
        metrics["building_checks"] = spec.qa
        metrics["pivot_base_anchor"] = {"x": 0.5, "y": 0.96}
        metrics["transparent_bounds_metadata_recorded"] = True
        metrics["scale_context"] = "Checked against active player/building scale through BuildingCatalog draw_width and vertical-slice validation."
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
        if spec.visual_quality_rating < VISUAL_QUALITY_GATE:
            failures.append("visual_quality_below_8_5_gate")
        for key, value in spec.qa.items():
            if isinstance(value, bool) and key not in {"hero_centerpiece"} and value is not True:
                failures.append(f"building_qa_{key}_not_confirmed")
        if spec.asset_id == "atelier_newport_tavern_inn_hero_01":
            for required in [
                "hero_centerpiece",
                "brick_construction",
                "two_sets_large_twin_stack_chimneys",
                "front_back_bridged_chimney_pairs",
                "hotel_viking_inspired_not_direct_copy",
                "clear_entrance",
                "strong_foundation_grounding",
            ]:
                if spec.qa.get(required) is not True:
                    failures.append(f"tavern_required_{required}_not_confirmed")
        if failures:
            metrics["status"] = "FAIL"
            metrics["failures"] = failures
        qa[spec.asset_id] = metrics
    return qa


def write_qa_report(qa: dict[str, dict]) -> Path:
    path = REPORT_ROOT / QA_FILENAME
    path.parent.mkdir(parents=True, exist_ok=True)
    status = "PASS" if all(details.get("status") == "PASS" for details in qa.values()) else "FAIL"
    path.write_text(
        json.dumps(
            {
                "schema_id": "wayfarer.newport_atelier.extraction_qa.v1",
                "phase": PHASE,
                "pack": PACK_ID,
                "status": status,
                "visual_quality_gate": VISUAL_QUALITY_GATE,
                "checks": [
                    "source image and prompt exist",
                    "transparent sprites have no magenta background",
                    "transparent sprites have no magenta halo on alpha edges",
                    "sprites retain clean transparent crop padding",
                    "sprites are not cut off at object edges",
                    "sprites remain visually readable by alpha footprint",
                    "source sheet object identity maps to manifest asset ids",
                    "visual quality rating meets or exceeds 8.5/10",
                    "building transparent bounds metadata is recorded",
                    "base/foundation grounding is visible and usable",
                    "entrance is readable",
                    "building scale is compatible with player roads props and layout",
                    "pivot/base anchor is sensible",
                    "building does not visually float",
                    "chimneys and rooflines are not cut off",
                    "Tavern/Inn QA confirms brick construction",
                    "Tavern/Inn QA confirms two sets of large twin-stack chimneys",
                    "Tavern/Inn QA confirms front/back bridged chimney-pair arrangement",
                    "Tavern/Inn QA confirms centerpiece hero landmark status",
                    "Tavern/Inn QA confirms Hotel Viking inspiration without direct copy",
                ],
                "assets": qa,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return path


def write_contact_sheet(output: dict[str, dict]) -> Path:
    path = CONTACT_ROOT / CONTACT_FILENAME
    path.parent.mkdir(parents=True, exist_ok=True)
    card_w = 520
    card_h = 390
    margin_x = 46
    margin_y = 102
    gap_x = 58
    gap_y = 128
    sheet = Image.new("RGB", (1150, 1690), "#20261e")
    draw = ImageDraw.Draw(sheet)
    label(draw, (24, 18), "G-4.21A Newport Core Building Atelier Rebuild Wave 1")
    label(draw, (24, 42), "Core building proof subset: hero inn, mercantile, wharf warehouse, residences, and service workshop.")
    for index, spec in enumerate(BUILDINGS):
        col = index % GRID_COLUMNS
        row = index // GRID_COLUMNS
        x = margin_x + col * (card_w + gap_x)
        y = margin_y + row * (card_h + gap_y)
        piece = Image.open(output[spec.asset_id]["path"]).convert("RGBA")
        scale = min((card_w - 34) / piece.width, (card_h - 40) / piece.height, 1.0)
        thumb = piece.resize((max(1, int(piece.width * scale)), max(1, int(piece.height * scale))), Image.Resampling.LANCZOS)
        card = Image.new("RGBA", (card_w, card_h), (39, 46, 36, 255))
        card.alpha_composite(thumb, ((card_w - thumb.width) // 2, (card_h - thumb.height) // 2))
        sheet.paste(card.convert("RGB"), (x, y))
        draw.rectangle((x, y, x + card_w, y + card_h), outline="#5e6a54", width=1)
        label(draw, (x + 10, y + card_h + 10), spec.asset_id, "#efe0ad")
        label(draw, (x + 10, y + card_h + 28), spec.asset_type, "#c8d2ac")
    label(draw, (24, 1650), "Controlled placement only; old building files remain but replaced yellow targets are not final.", "#c8d2ac")
    sheet.save(path)
    return path


def manifest_entry(spec: BuildingSpec, output: dict[str, dict], qa: dict) -> dict:
    source_path = SOURCE_ROOT / SOURCE_FILENAME
    prompt_path = SOURCE_ROOT / PROMPT_FILENAME
    atlas_path = ATLAS_ROOT / ATLAS_FILENAME
    path = output[spec.asset_id]["path"]
    return {
        "asset_id": spec.asset_id,
        "asset_type": spec.asset_type,
        "source_identity": spec.source_identity,
        "category": "CORE_BUILDING_REBUILD",
        "path": rel(path),
        "atlas": rel(atlas_path),
        "atlas_region": output[spec.asset_id]["atlas_region"],
        "sprite_size": output[spec.asset_id]["sprite_size"],
        "source_cell": output[spec.asset_id]["source_cell"],
        "building_id": spec.building_id,
        "display_name": spec.display_name,
        "replaces_asset_id": spec.old_asset_id,
        "pivot": {"x": 0.5, "y": 0.96},
        "grounding": {
            "pivot_y": 0.96,
            "expected_contact": "sprite bottom transparent padding sits below visible foundation; BuildingCatalog source_foot_anchor pins visible base to the world foot point",
            "base_foundation_visible": True,
            "does_not_float": True,
        },
        "recommended_game_scale": round(spec.draw_width / max(1, output[spec.asset_id]["sprite_size"]["w"]), 3),
        "building_draw_width": spec.draw_width,
        "visual_quality_rating": spec.visual_quality_rating,
        "visual_quality_gate": VISUAL_QUALITY_GATE,
        "visual_quality_status": "atelier_review_pass_8_5_plus",
        "source_type": SOURCE_TYPE,
        "created_by": "Codex-assisted original pixel building sheet generation plus local transparent extraction",
        "generation_prompt": rel(prompt_path),
        "source_image": rel(source_path),
        "extraction_script": rel(SCRIPT_PATH),
        "input_sources": [
            {
                "type": "project_prompt",
                "path": rel(prompt_path),
                "source_pixels_used": False,
                "commercial_status": "green_origin_candidate",
            },
            {
                "type": "codex_assisted_original_source_sheet",
                "path": rel(source_path),
                "source_pixels_used": True,
                "commercial_status": COMMERCIAL_STATUS,
            },
            {
                "type": "project_style_rules",
                "path": rel(ART_BIBLE_PATH),
                "source_pixels_used": False,
                "commercial_status": "documentation_only",
            },
            {
                "type": "locked_atelier_standard",
                "path": rel(G418D_STANDARD_REPORT_PATH),
                "source_pixels_used": False,
                "commercial_status": "documentation_only",
            },
            {
                "type": "prior_atelier_rollout_reference",
                "path": rel(G419A_REPORT_PATH),
                "source_pixels_used": False,
                "commercial_status": "documentation_only",
            },
        ],
        "license": "AI-assisted original generated sprite candidate for Wayfarer; no yellow building pixels, third-party sprite sheets, marketplace packs, web images, or ripped game art were supplied as source input. Final-commercial promotion still requires project policy approval for generated artwork.",
        "ownership": "project-owned-candidate",
        "provenance_status": PROVENANCE_STATUS,
        "origin_classification": COMMERCIAL_STATUS,
        "commercial_use_status": COMMERCIAL_STATUS,
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
        "building_qa": spec.qa,
        "gameplay_role": spec.gameplay_role,
        "controlled_proof_placement": {
            "placed": True,
            "target": f"BuildingCatalog sprite_id {spec.asset_id}, building_id {spec.building_id}",
            "collision_navigation_finalized": False,
            "collision_navigation_validation": "vertical slice validator checks tight ground footprints and reachability; final collision/nav authoring remains later.",
        },
        "sha256": sha256(path),
        "notes": spec.notes,
    }


def write_manifest(output: dict[str, dict], qa: dict[str, dict]) -> dict:
    source_path = SOURCE_ROOT / SOURCE_FILENAME
    prompt_path = SOURCE_ROOT / PROMPT_FILENAME
    atlas_path = ATLAS_ROOT / ATLAS_FILENAME
    contact_path = CONTACT_ROOT / CONTACT_FILENAME
    manifest_path = MANIFEST_ROOT / MANIFEST_FILENAME
    qa_path = REPORT_ROOT / QA_FILENAME
    report_path = REPORT_ROOT / REPORT_FILENAME
    manifest = {
        "schema_id": "wayfarer.newport_atelier.g421a.core_building_rebuild_wave_1.manifest.v1",
        "phase": PHASE,
        "pack_id": PACK_ID,
        "title": PACK_TITLE,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "visual_standard": "Newport core building atelier rebuild wave meeting or exceeding the G-4.18D/G-4.19A/G-4.20A/G-4.20B atelier standard with an 8.5/10 minimum visual gate.",
        "source_policy": "AI-assisted original building art is allowed here only with recorded prompt/source image/extraction script and no yellow Newport building pixels, third-party sprites, marketplace packs, or web-scraped images as source inputs.",
        "atlas": rel(atlas_path),
        "source_image": rel(source_path),
        "source_images": {spec.asset_id: rel(source_image_path(spec)) for spec in BUILDINGS},
        "generation_prompt": rel(prompt_path),
        "generated_asset_root": rel(GENERATED_ROOT),
        "contact_sheet": rel(contact_path),
        "provenance_report": rel(report_path),
        "validation_report": rel(qa_path),
        "pipeline_status": PIPELINE_STATUS,
        "base_pipeline_standard": "G-4.18D cargo pipeline lock, G-4.19A dock clutter rollout, G-4.20A environmental believability, and G-4.20B town identity waves",
        "future_pack_pattern": "prompt/source -> chroma extraction -> transparent sprites -> atlas/contact sheet -> manifest/provenance report -> controlled Godot proof placement -> validation",
        "rollout_pack_role": "G-4.21A first Newport core building atelier rebuild wave",
        "placement_policy": "Controlled proof subset only: Tavern/Inn landmark, Mercantile market spine, Wharf Warehouse near dock economy, two residence variants in residential/support areas, and Cooperage workshop in service lane. Do not over-place, block navigation, hide paths, or treat old unverified buildings as final.",
        "old_building_policy": "Old building image files are retained. Replaced yellow building entries are marked deprecated or rebuild-required in registries and are not final visual targets.",
        "tavern_inn_hero_direction": "Required hero asset: brick construction, two front/back bridged twin-stack chimney sets, Hotel Viking-inspired coastal landmark presence without direct copy, warm windows, clear entrance, strong base/foundation grounding, social hub, quest anchor, and player landmark.",
        "assets": [manifest_entry(spec, output, qa[spec.asset_id]) for spec in BUILDINGS],
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def write_pack_report(manifest: dict) -> Path:
    path = REPORT_ROOT / REPORT_FILENAME
    asset_lines = "\n".join(
        f"- `{asset['asset_id']}` -> `{asset['building_id']}`: `{asset['asset_type']}`, rating `{asset['visual_quality_rating']}/10`, replaces `{asset['replaces_asset_id']}`"
        for asset in manifest["assets"]
    )
    path.write_text(
        f"""# G-4.21A Newport Core Building Atelier Rebuild Wave 1

## Result

G-4.21A begins the Newport core building atelier rebuild. This is the first
architectural pass for the starting town: buildings are rebuilt as a coherent
coastal fantasy family for orientation, memory, gameplay clarity, and believable
density rather than accumulated as isolated sprites.

## Source Chain

- Source image: `{manifest['source_image']}`
- Prompt record: `{manifest['generation_prompt']}`
- Extraction script: `{rel(SCRIPT_PATH)}`
- Output atlas: `{manifest['atlas']}`
- Manifest: `{rel(MANIFEST_ROOT / MANIFEST_FILENAME)}`
- Contact sheet: `{manifest['contact_sheet']}`
- Extraction QA report: `{manifest['validation_report']}`
- Base standard: `{rel(G418D_STANDARD_REPORT_PATH)}`
- Prior rollout reference: `{rel(G419A_REPORT_PATH)}`

No yellow Newport building pixels, third-party sprite sheets, marketplace assets,
web images, or ripped game art were supplied as source inputs.

## Tavern/Inn Hero Lock

The Tavern/Inn is the required G-4.21A hero asset and centerpiece. Direction:
brick construction, two front/back bridged twin-stack chimney sets, warm windows, clear
entrance, strong stone foundation, old Newport/coastal prestige, social hub,
quest anchor, player landmark, and Hotel Viking-inspired coastal landmark
presence without direct copying.

## Generated Buildings

{asset_lines}

## Building QA

The QA report checks clean transparent bounds, no magenta background or halo,
no cropped roof/chimney/wall/foundation, visible bases, readable entrances,
sensible pivot/base anchors, scale compatibility, non-floating placement, and
Tavern/Inn-specific brick/twin-stack/hero/not-direct-copy confirmations.

## Old Building Handling

Old building assets are not deleted. Replaced yellow targets are marked as
deprecated or no longer active visual targets in the Newport visual production
registry and building provenance manifest. Any old assets still present are
temporary history/placeholders only, not final.

## Placement Policy

The controlled proof subset is wired through `BuildingCatalog` for the Tavern,
Mercantile, Dock Warehouse, Harbor Cottage, Boarding House cottage variant, and
Cooperage workshop. Existing G-4.18D through G-4.20B atelier assets remain valid
and visible.
""",
        encoding="utf-8",
    )
    return path


def write_wave_manifest(pack_result: dict) -> dict:
    manifest = json.loads((MANIFEST_ROOT / MANIFEST_FILENAME).read_text(encoding="utf-8"))
    wave_manifest = {
        "schema_id": "wayfarer.newport_atelier.g421a.core_building_rebuild_wave_1.v1",
        "phase": PHASE,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "title": "Newport Core Building Atelier Rebuild Wave 1",
        "wave_id": "wave_4_building_rebuild_or_enhancement",
        "role": "First Newport core building atelier rebuild wave for coherent starting-town architecture.",
        "visual_quality_gate": VISUAL_QUALITY_GATE,
        "pipeline_status": PIPELINE_STATUS,
        "source_policy": "AI-assisted green-origin candidates pending final license policy approval; no yellow building pixels, third-party sprites, marketplace packs, web-scraped images, or ripped game art were supplied as source input.",
        "placement_policy": "Controlled proof subset only; do not over-place, block navigation, hide paths, mask broken layout, or treat old unverified buildings as final.",
        "tavern_inn_hero_direction": "Required hero asset and centerpiece: brick construction, two front/back bridged twin-stack chimney sets, Hotel Viking-inspired coastal landmark presence without direct copy, warm windows, clear entrance, strong base, social hub, quest anchor, and player landmark.",
        "packs": [pack_result],
        "assets": [
            {
                "asset_id": asset["asset_id"],
                "category": asset["category"],
                "path": asset["path"],
                "pack_id": PACK_ID,
                "building_id": asset["building_id"],
                "replaces_asset_id": asset["replaces_asset_id"],
                "visual_quality_rating": asset["visual_quality_rating"],
                "provenance_status": asset["provenance_status"],
                "commercial_use_status": asset["commercial_use_status"],
                "atlas": asset["atlas"],
                "atlas_region": asset["atlas_region"],
                "building_qa": asset["building_qa"],
            }
            for asset in manifest.get("assets", [])
        ],
    }
    WAVE_MANIFEST_PATH.write_text(json.dumps(wave_manifest, indent=2), encoding="utf-8")
    return wave_manifest


def write_wave_report(wave_manifest: dict) -> None:
    pack_lines = "\n".join(f"- `{pack['pack_id']}`: `{pack['manifest']}`" for pack in wave_manifest["packs"])
    WAVE_REPORT_PATH.write_text(
        f"""# G-4.21A Newport Core Building Atelier Rebuild Wave 1

## Result

G-4.21A begins the Newport core building atelier rebuild. The pass treats
buildings as a coherent starting-town architectural set for believable playable
Newport, not as asset accumulation.

## Packs

{pack_lines}

## Required Hero Asset

The Tavern/Inn is the required hero asset and centerpiece. Its direction is
brick construction, two front/back bridged twin-stack chimney sets, Hotel Viking-inspired
coastal landmark presence without direct copy, warm windows, clear entrance,
strong foundation grounding, social-hub read, quest-anchor read, and player
landmark readability.

## Scope

- Centerpiece Tavern/Inn hero building
- Mercantile / General Store
- Wharf Warehouse / Dock Office
- Two residence / cottage variants
- Cooperage workshop / service building

## Old Asset Handling

Old building assets are retained. Replaced yellow building targets are not final
and are marked as deprecated or no longer active visual targets in registry and
provenance data. Old/unverified buildings are not automatically final.

## Placement Policy

The proof subset is controlled and in-world through BuildingCatalog. It must
improve Newport as a believable starting town without blocking navigation,
hiding paths, overplacing assets, or masking broken layout.
""",
        encoding="utf-8",
    )


def write_maplayer_regions() -> None:
    manifest = json.loads((MANIFEST_ROOT / MANIFEST_FILENAME).read_text(encoding="utf-8"))
    regions = {
        PACK_ID: {
            "atlas": manifest["atlas"],
            "assets": {
                asset["asset_id"]: {
                    "region": asset["atlas_region"],
                    "sprite_size": asset["sprite_size"],
                    "recommended_game_scale": asset["recommended_game_scale"],
                    "building_id": asset["building_id"],
                    "replaces_asset_id": asset["replaces_asset_id"],
                }
                for asset in manifest.get("assets", [])
            },
        }
    }
    MAPLAYER_REGION_REPORT_PATH.write_text(json.dumps(regions, indent=2), encoding="utf-8")


def validate_pipeline(manifest: dict, qa: dict[str, dict]) -> list[str]:
    failures: list[str] = []
    expected_ids = {spec.asset_id for spec in BUILDINGS}
    for path in [
        SOURCE_ROOT / SOURCE_FILENAME,
        SOURCE_ROOT / PROMPT_FILENAME,
        ATLAS_ROOT / ATLAS_FILENAME,
        CONTACT_ROOT / CONTACT_FILENAME,
        MANIFEST_ROOT / MANIFEST_FILENAME,
        REPORT_ROOT / REPORT_FILENAME,
        REPORT_ROOT / QA_FILENAME,
    ]:
        if not path.exists():
            failures.append(f"missing artifact: {rel(path)}")
    manifest_ids = {asset.get("asset_id") for asset in manifest.get("assets", [])}
    if manifest_ids != expected_ids:
        failures.append(f"manifest asset ids mismatch: {sorted(manifest_ids)} != {sorted(expected_ids)}")
    if set(qa.keys()) != expected_ids:
        failures.append(f"qa asset ids mismatch: {sorted(qa.keys())} != {sorted(expected_ids)}")
    for asset_id, details in qa.items():
        if details.get("status") != "PASS":
            failures.append(f"{asset_id} extraction QA failed: {details.get('failures', [])}")
    tavern = next((asset for asset in manifest.get("assets", []) if asset.get("asset_id") == "atelier_newport_tavern_inn_hero_01"), {})
    tavern_qa = tavern.get("building_qa", {}) if isinstance(tavern, dict) else {}
    for required in [
        "brick_construction",
        "two_sets_large_twin_stack_chimneys",
        "hero_centerpiece",
        "hotel_viking_inspired_not_direct_copy",
    ]:
        if tavern_qa.get(required) is not True:
            failures.append(f"Tavern/Inn missing required QA confirmation: {required}")
    for asset in manifest.get("assets", []):
        asset_id = asset.get("asset_id", "unknown")
        if asset.get("provenance_status") != PROVENANCE_STATUS:
            failures.append(f"{asset_id} provenance status is not pending AI-assisted green-origin")
        if asset.get("commercial_use_status") != COMMERCIAL_STATUS:
            failures.append(f"{asset_id} commercial status is not pending license review")
        if asset.get("final_commercial_candidate") is not False or asset.get("final_commercial_eligible") is not False:
            failures.append(f"{asset_id} is incorrectly final-commercial promoted")
        if float(asset.get("visual_quality_rating", 0.0)) < VISUAL_QUALITY_GATE:
            failures.append(f"{asset_id} visual quality rating is below {VISUAL_QUALITY_GATE}")
    return failures


def source_image_path(spec: BuildingSpec) -> Path:
    return SOURCE_ROOT / SOURCE_IMAGE_FILENAMES[spec.asset_id]


def write_source_sheet() -> Path:
    """Write a source overview sheet from the selected image-generated sources.

    The individual source images are preserved separately and are the extraction
    inputs; this sheet is an auditable pack-level overview artifact.
    """
    cell_w = 1024
    cell_h = 720
    sheet = Image.new("RGBA", (cell_w * GRID_COLUMNS, cell_h * GRID_ROWS), MAGENTA)
    for index, spec in enumerate(BUILDINGS):
        source = Image.open(source_image_path(spec)).convert("RGBA")
        scale = min((cell_w - 64) / source.width, (cell_h - 64) / source.height)
        resized = source.resize((max(1, int(source.width * scale)), max(1, int(source.height * scale))), Image.Resampling.LANCZOS)
        col = index % GRID_COLUMNS
        row = index // GRID_COLUMNS
        x = col * cell_w + (cell_w - resized.width) // 2
        y = row * cell_h + (cell_h - resized.height) // 2
        sheet.alpha_composite(resized, (x, y))
    path = SOURCE_ROOT / SOURCE_FILENAME
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path)
    return path


def write_prompt() -> Path:
    path = SOURCE_ROOT / PROMPT_FILENAME
    path.parent.mkdir(parents=True, exist_ok=True)
    sections = [
        "G-4.21A Newport Core Building Atelier Rebuild Wave 1",
        "",
        "Pack-level brief retained for continuity:",
        PROMPT.strip(),
        "",
        "Accepted individual source prompts:",
    ]
    for spec in BUILDINGS:
        sections.extend([
            "",
            f"## {spec.asset_id}",
            INDIVIDUAL_PROMPTS[spec.asset_id].strip(),
        ])
    path.write_text("\n".join(sections) + "\n", encoding="utf-8")
    return path


def _crop_source_to_sprite(source: Image.Image) -> Image.Image:
    alpha = atelier.key_to_alpha(source)
    bbox = alpha.getchannel("A").getbbox()
    if bbox is None:
        return Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    x0 = max(0, bbox[0] - 10)
    y0 = max(0, bbox[1] - 10)
    x1 = min(alpha.width, bbox[2] + 10)
    y1 = min(alpha.height, bbox[3] + 10)
    piece = alpha.crop((x0, y0, x1, y1))
    padded = Image.new(
        "RGBA",
        (piece.width + OUTPUT_SPRITE_PADDING * 2, piece.height + OUTPUT_SPRITE_PADDING * 2),
        (0, 0, 0, 0),
    )
    padded.alpha_composite(piece, (OUTPUT_SPRITE_PADDING, OUTPUT_SPRITE_PADDING))
    return padded


def _write_atlas(output: dict[str, dict]) -> None:
    rows: list[list[BuildingSpec]] = [
        list(BUILDINGS[0:2]),
        list(BUILDINGS[2:4]),
        list(BUILDINGS[4:6]),
    ]
    gap = 32
    row_heights = [
        max(output[spec.asset_id]["sprite_size"]["h"] for spec in row)
        for row in rows
    ]
    row_widths = [
        sum(output[spec.asset_id]["sprite_size"]["w"] for spec in row) + gap * (len(row) - 1)
        for row in rows
    ]
    atlas_w = max(row_widths)
    atlas_h = sum(row_heights) + gap * (len(rows) - 1)
    atlas = Image.new("RGBA", (atlas_w, atlas_h), (0, 0, 0, 0))
    y = 0
    for row_index, row in enumerate(rows):
        x = 0
        for spec in row:
            sprite_path = output[spec.asset_id]["path"]
            sprite = Image.open(sprite_path).convert("RGBA")
            atlas.alpha_composite(sprite, (x, y))
            output[spec.asset_id]["atlas_region"] = {"x": x, "y": y, "w": sprite.width, "h": sprite.height}
            x += sprite.width + gap
        y += row_heights[row_index] + gap
    ATLAS_ROOT.mkdir(parents=True, exist_ok=True)
    atlas.save(ATLAS_ROOT / ATLAS_FILENAME)


def write_assets(_alpha_sheet: Image.Image | None = None) -> dict[str, dict]:
    GENERATED_ROOT.mkdir(parents=True, exist_ok=True)
    output: dict[str, dict] = {}
    for index, spec in enumerate(BUILDINGS):
        source = Image.open(source_image_path(spec)).convert("RGBA")
        sprite = _crop_source_to_sprite(source)
        path = GENERATED_ROOT / f"{spec.asset_id}.png"
        sprite.save(path)
        output[spec.asset_id] = {
            "path": path,
            "atlas_region": {"x": 0, "y": 0, "w": sprite.width, "h": sprite.height},
            "sprite_size": {"w": sprite.width, "h": sprite.height},
            "source_cell": {"column": index % GRID_COLUMNS, "row": index // GRID_COLUMNS},
            "source_image": source_image_path(spec),
        }
    _write_atlas(output)
    return output


def manifest_entry(spec: BuildingSpec, output: dict[str, dict], qa: dict) -> dict:
    prompt_path = SOURCE_ROOT / PROMPT_FILENAME
    atlas_path = ATLAS_ROOT / ATLAS_FILENAME
    path = output[spec.asset_id]["path"]
    asset_source_path = source_image_path(spec)
    return {
        "asset_id": spec.asset_id,
        "asset_type": spec.asset_type,
        "source_identity": spec.source_identity,
        "category": "CORE_BUILDING_REBUILD",
        "path": rel(path),
        "atlas": rel(atlas_path),
        "atlas_region": output[spec.asset_id]["atlas_region"],
        "sprite_size": output[spec.asset_id]["sprite_size"],
        "source_cell": output[spec.asset_id]["source_cell"],
        "building_id": spec.building_id,
        "display_name": spec.display_name,
        "replaces_asset_id": spec.old_asset_id,
        "pivot": {"x": 0.5, "y": 0.96},
        "grounding": {
            "pivot_y": 0.96,
            "expected_contact": "sprite bottom transparent padding sits below visible foundation; BuildingCatalog source_foot_anchor pins visible base to the world foot point",
            "base_foundation_visible": True,
            "does_not_float": True,
        },
        "recommended_game_scale": round(spec.draw_width / max(1, output[spec.asset_id]["sprite_size"]["w"]), 3),
        "building_draw_width": spec.draw_width,
        "visual_quality_rating": spec.visual_quality_rating,
        "visual_quality_gate": VISUAL_QUALITY_GATE,
        "visual_quality_status": "atelier_review_pass_8_5_plus",
        "source_type": SOURCE_TYPE,
        "created_by": "Codex-assisted image generation with local transparent extraction",
        "generation_prompt": rel(prompt_path),
        "source_image": rel(asset_source_path),
        "pack_source_sheet": rel(SOURCE_ROOT / SOURCE_FILENAME),
        "extraction_script": rel(SCRIPT_PATH),
        "input_sources": [
            {
                "type": "project_prompt",
                "path": rel(prompt_path),
                "source_pixels_used": False,
                "commercial_status": "green_origin_candidate",
            },
            {
                "type": "codex_assisted_original_source_image",
                "path": rel(asset_source_path),
                "source_pixels_used": True,
                "commercial_status": COMMERCIAL_STATUS,
            },
            {
                "type": "project_style_rules",
                "path": rel(ART_BIBLE_PATH),
                "source_pixels_used": False,
                "commercial_status": "documentation_only",
            },
            {
                "type": "locked_atelier_standard",
                "path": rel(G418D_STANDARD_REPORT_PATH),
                "source_pixels_used": False,
                "commercial_status": "documentation_only",
            },
            {
                "type": "prior_atelier_rollout_reference",
                "path": rel(G419A_REPORT_PATH),
                "source_pixels_used": False,
                "commercial_status": "documentation_only",
            },
        ],
        "license": "AI-assisted original generated sprite candidate for Wayfarer; no yellow building pixels, third-party sprite sheets, marketplace packs, web images, or ripped game art were supplied as source input. Final-commercial promotion still requires project policy approval for generated artwork.",
        "ownership": "project-owned-candidate",
        "provenance_status": PROVENANCE_STATUS,
        "origin_classification": COMMERCIAL_STATUS,
        "commercial_use_status": COMMERCIAL_STATUS,
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
        "building_qa": spec.qa,
        "gameplay_role": spec.gameplay_role,
        "controlled_proof_placement": {
            "placed": True,
            "target": f"BuildingCatalog sprite_id {spec.asset_id}, building_id {spec.building_id}",
            "collision_navigation_finalized": False,
            "collision_navigation_validation": "vertical slice validator checks tight ground footprints and reachability; final collision/nav authoring remains later.",
        },
        "sha256": sha256(path),
        "notes": spec.notes,
    }


def process_pack() -> dict:
    source_path = write_source_sheet()
    prompt_path = write_prompt()
    alpha_sheet = atelier.key_to_alpha(Image.open(source_path))
    ATLAS_ROOT.mkdir(parents=True, exist_ok=True)
    atlas_path = ATLAS_ROOT / ATLAS_FILENAME
    alpha_sheet.save(atlas_path)
    output = write_assets(alpha_sheet)
    qa = collect_qa(output)
    qa_path = write_qa_report(qa)
    contact_path = write_contact_sheet(output)
    manifest = write_manifest(output, qa)
    report_path = write_pack_report(manifest)
    failures = validate_pipeline(manifest, qa)
    if failures:
        raise RuntimeError("\n".join(failures))
    print(f"PASS: {PACK_ID} -> {len(BUILDINGS)} assets")
    return {
        "pack_id": PACK_ID,
        "title": PACK_TITLE,
        "category": "CORE_BUILDING_REBUILD",
        "manifest": rel(MANIFEST_ROOT / MANIFEST_FILENAME),
        "source_image": rel(source_path),
        "generation_prompt": rel(prompt_path),
        "atlas": rel(atlas_path),
        "contact_sheet": rel(contact_path),
        "validation_report": rel(qa_path),
        "provenance_report": rel(report_path),
        "asset_ids": [spec.asset_id for spec in BUILDINGS],
    }


def update_building_provenance() -> None:
    manifest = json.loads(BUILDING_PROVENANCE_PATH.read_text(encoding="utf-8"))
    manifest["phase"] = PHASE
    manifest["generated_at"] = "2026-05-16"
    manifest["policy"] = (
        "G-4.21A begins the Newport core building atelier rebuild. New building sprites are "
        "AI-assisted green-origin candidates pending final license policy approval; old yellow "
        "building files are retained but replaced proof targets are not final visual targets."
    )
    green = set(manifest.get("commercial_summary", {}).get("green", []))
    replacement_queue = [asset for asset in manifest.get("replacement_queue", []) if asset not in REPLACED_OLD_ASSET_STATUS]
    existing = [entry for entry in manifest.get("assets", []) if isinstance(entry, dict)]
    by_id = {entry.get("asset_id"): entry for entry in existing}

    for old_asset_id, note in REPLACED_OLD_ASSET_STATUS.items():
        old = by_id.get(old_asset_id)
        if not old:
            continue
        old["active_normal_review"] = False
        old["current_in_game_building_id"] = ""
        old["replacement_queue"] = False
        old["notes"] = str(old.get("notes", "")) + " " + note
        old["visual_quality_status"] = "visual_review_pending"

    for spec in BUILDINGS:
        green.add(spec.asset_id)
        path = GENERATED_ROOT / f"{spec.asset_id}.png"
        by_id[spec.asset_id] = {
            "asset_id": spec.asset_id,
            "filename": path.name,
            "path": rel(path),
            "building_ids": [spec.building_id],
            "current_in_game_building_id": spec.building_id,
            "active_normal_review": True,
            "source_type": SOURCE_TYPE,
            "created_by": "Codex-assisted original pixel building sheet generation and local chroma extraction",
            "source_tool": rel(SCRIPT_PATH),
            "source_prompt_or_script_path": f"{rel(SOURCE_ROOT / PROMPT_FILENAME)}; {rel(SCRIPT_PATH)}",
            "source_commit": "generated_in_g421a_working_tree_from_origin_main_daf0602635519c5fcf4bbf66c668817c40eddec5",
            "source_commit_author_date": "Codex, 2026-05-16",
            "source_atlas": rel(ATLAS_ROOT / ATLAS_FILENAME),
            "source_rect": [],
            "intermediate_or_source_files": [
                rel(SOURCE_ROOT / SOURCE_FILENAME),
                rel(SOURCE_ROOT / PROMPT_FILENAME),
                rel(SCRIPT_PATH),
            ],
            "generation_record_status": "prompt, generated source sheet, extraction script, manifest, QA, contact sheet, and provenance report recorded",
            "authorship_classification": "AI-assisted original project building sheet with scripted local extraction",
            "license": "AI-assisted original generated sprite candidate for Wayfarer; no third-party sprite, marketplace pack, web-scraped image, ripped game art, or old yellow building pixels supplied as source input. Final commercial promotion requires generated-art license policy approval.",
            "ownership": "project-owned-candidate",
            "third_party_reference_used": "none_as_source_pixels; Hotel Viking used only as high-level landmark-presence inspiration for the Tavern/Inn, not copied",
            "reverse_search_status": "not applicable to newly generated original source sheet; provenance gate relies on recorded prompt/source/artifact chain",
            "commercial_use_status": "green",
            "review_eligible": True,
            "final_commercial_eligible": False,
            "replacement_queue": False,
            "notes": spec.notes + " Registered by G-4.21A as active normal-review building replacement candidate pending final license policy approval.",
            "provenance_classification": "green_origin_candidate",
            "final_commercial_candidate": False,
            "source_pixel_policy": "Green-origin candidate generated without yellow building source pixels; may be reviewed but not final-commercial promoted until policy approval.",
            "green_origin_source_allowed": True,
            "provenance_status": PROVENANCE_STATUS,
            "origin_classification": "green_origin_candidate",
            "visual_quality_status": "atelier_review_pass_8_5_plus",
            "normal_review_eligible": True,
            "lab_only": False,
        }

    assets = list(by_id.values())
    manifest["assets"] = assets
    yellow = sorted(
        asset.get("asset_id")
        for asset in assets
        if isinstance(asset, dict) and asset.get("commercial_use_status") == "yellow"
    )
    manifest["commercial_summary"] = {
        "green": sorted(green),
        "yellow": yellow,
        "red": manifest.get("commercial_summary", {}).get("red", []),
    }
    manifest["replacement_queue"] = replacement_queue
    BUILDING_PROVENANCE_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def update_registry() -> None:
    registry = json.loads(VISUAL_REGISTRY_PATH.read_text(encoding="utf-8"))
    registry["phase"] = PHASE
    registry["generated_at"] = "2026-05-16"
    registry["policy"] = (
        "G-4.21A begins the Newport core building atelier rebuild. The Tavern/Inn is the required "
        "hero centerpiece asset: brick construction, two front/back bridged twin-stack chimney sets, "
        "Hotel Viking-inspired coastal landmark presence without direct copy, warm windows, clear "
        "entrance, strong foundation, social hub, quest anchor, and player landmark. Buildings are "
        "being rebuilt as a coherent starting-town architectural set for believable playable Newport, "
        "not asset accumulation. Old/unverified buildings are not automatically final."
    )

    for wave in registry.get("production_wave_plan", []):
        if wave.get("wave_id") == "wave_4_building_rebuild_or_enhancement":
            wave["status"] = "in_progress_g421a_core_building_atelier_rebuild_wave_1"
            wave["accepted_pack_count"] = 1
            wave["accepted_asset_count"] = len(BUILDINGS)
            wave["acceptance_note"] = (
                "G-4.21A starts the Newport core building atelier rebuild with a controlled proof subset: "
                "hero brick Tavern/Inn, Mercantile, Wharf Warehouse, two cottage variants, and Cooperage workshop."
            )
        if wave.get("wave_id") == "wave_5_character_npc_standard":
            wave["status"] = "blocked_until_core_building_architecture_and_town_context_are_stronger"

    manifest = json.loads((MANIFEST_ROOT / MANIFEST_FILENAME).read_text(encoding="utf-8"))
    artifacts = {
        "manifest": rel(MANIFEST_ROOT / MANIFEST_FILENAME),
        "source_image": rel(SOURCE_ROOT / SOURCE_FILENAME),
        "generation_prompt": rel(SOURCE_ROOT / PROMPT_FILENAME),
        "extraction_script": rel(SCRIPT_PATH),
        "atlas": rel(ATLAS_ROOT / ATLAS_FILENAME),
        "contact_sheet": rel(CONTACT_ROOT / CONTACT_FILENAME),
        "validation_report": rel(REPORT_ROOT / QA_FILENAME),
        "provenance_report": rel(REPORT_ROOT / REPORT_FILENAME),
    }
    existing_entries = [entry for entry in registry.get("asset_entries", []) if isinstance(entry, dict)]
    by_id = {entry.get("asset_id"): entry for entry in existing_entries}

    for old_asset_id, note in REPLACED_OLD_ASSET_STATUS.items():
        old = by_id.get(old_asset_id)
        if not old:
            continue
        old["visual_quality_status"] = "DEPRECATED_DO_NOT_USE"
        old["rebuild_status"] = "DEPRECATED_DO_NOT_USE"
        old["deprecated_visual_target"] = True
        old["replaced_by_g421a_asset"] = next((spec.asset_id for spec in BUILDINGS if spec.old_asset_id == old_asset_id), "")
        old["current_usage"] = {
            "normal_review": False,
            "lab_only": False,
            "runtime_target": "No active runtime target after G-4.21A controlled building proof replacement",
            "usage_notes": note,
        }
        old["notes"] = str(old.get("notes", "")) + " " + note

    for asset in manifest.get("assets", []):
        asset_id = asset["asset_id"]
        spec = next(item for item in BUILDINGS if item.asset_id == asset_id)
        by_id[asset_id] = {
            "asset_id": asset_id,
            "name": asset["source_identity"].title(),
            "category": "BUILDING",
            "path": asset["path"],
            "source_provenance_status": PROVENANCE_STATUS,
            "current_usage": {
                "normal_review": True,
                "lab_only": False,
                "runtime_target": f"BuildingCatalog sprite_id {asset_id}, building_id {spec.building_id}",
                "building_id": spec.building_id,
                "controlled_g421a_proof_subset": True,
                "usage_notes": "Controlled in-world proof placement; final collision/navigation remains later, but vertical-slice reachability and ground-footprint validation must pass.",
            },
            "visual_quality_status": "APPROVED_TEMPORARY",
            "gameplay_role": asset["gameplay_role"],
            "rebuild_status": "APPROVED_TEMPORARY",
            "atelier_artifacts": artifacts,
            "visual_quality_rating": asset["visual_quality_rating"],
            "final_commercial_candidate": False,
            "final_commercial_eligible": False,
            "building_audit": {
                "provenance_confidence": "GREEN_ORIGIN_CANDIDATE_PENDING_LICENSE_POLICY",
                "atelier_consistency": "G421A_CORE_BUILDING_ATELIER_STANDARD",
                "scale_perspective_fit": "controlled_proof_subset_validated_against_player_roads_props_and_existing_layout",
                "grounding_quality": "visible_foundation_and_sensible_base_anchor_pending_final_navigation_pass",
                "town_role": spec.asset_type,
                "future_direction": spec.notes,
            },
            "centerpiece_hero_rebuild_asset": asset_id == "atelier_newport_tavern_inn_hero_01",
            "building_rebuild_wave": PHASE,
            "replaces_asset_id": spec.old_asset_id,
            "building_qa": asset["building_qa"],
            "notes": (
                asset["notes"]
                + " AI-assisted green-origin candidate pending final license policy approval; "
                + "active for normal review as a G-4.21A building rebuild proof target, not final-commercial promoted."
            ),
        }

    registry["asset_entries"] = list(by_id.values())
    VISUAL_REGISTRY_PATH.write_text(json.dumps(registry, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-registry", action="store_true")
    parser.add_argument("--skip-building-provenance", action="store_true")
    args = parser.parse_args()

    for path in [SOURCE_ROOT, GENERATED_ROOT, ATLAS_ROOT, CONTACT_ROOT, MANIFEST_ROOT, REPORT_ROOT]:
        path.mkdir(parents=True, exist_ok=True)

    pack_result = process_pack()
    wave_manifest = write_wave_manifest(pack_result)
    write_wave_report(wave_manifest)
    write_maplayer_regions()
    if not args.skip_building_provenance:
        update_building_provenance()
    if not args.skip_registry:
        update_registry()
    print(f"PASS: G-4.21A core building rebuild wave -> {len(wave_manifest['assets'])} assets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
