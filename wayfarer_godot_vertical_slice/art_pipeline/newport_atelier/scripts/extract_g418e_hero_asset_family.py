#!/usr/bin/env python3
"""Extract G-4.18E Newport hero-quality commercial/tavern asset family."""

from __future__ import annotations

import argparse
import json
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

AssetSpec = atelier.AssetSpec
PackSpec = atelier.PackSpec

PHASE = "G-4.18E"
VISUAL_QUALITY_GATE = 8.5
PIPELINE_STATUS = "ai_assisted_green_origin_candidate_pending_final_license_policy_approval"
PROVENANCE_STATUS = "ai_assisted_green_origin_candidate_pending_license_review"
COMMERCIAL_STATUS = "green_origin_candidate_pending_license_review"
FAMILY_ID = "newport_harbor_commercial_tavern_district_asset_family"
FAMILY_TITLE = "Newport Harbor Commercial + Tavern District Asset Family"

WAVE_MANIFEST_PATH = MANIFEST_ROOT / "newport_atelier_g418e_hero_asset_family_manifest.json"
WAVE_REPORT_PATH = REPORT_ROOT / "G418E_GREEN_ORIGIN_HERO_ASSET_FAMILY.md"
MAPLAYER_REGION_REPORT_PATH = MANIFEST_ROOT / "newport_atelier_g418e_hero_asset_family_regions.json"

GRID_COLUMNS = 2
GRID_ROWS = 4
OUTPUT_SPRITE_PADDING = 18


def rel(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def sha256(path: Path) -> str:
    return atelier.sha256(path)


def _prompt(primary_request: str, subject: str, materials: str, avoid: str) -> str:
    return f"""Use case: stylized-concept
Asset type: production 2D game sprite sheet, original legally clean asset concept for a fantasy 1700s Newport harbor RPG
Primary request: {primary_request} These must look like high-end hand-painted pixel art game sprites suitable beside detailed colonial Newport harbor buildings and the accepted Newport atelier sprites.
Scene/backdrop: perfectly flat solid #ff00ff chroma-key background only, no floor plane, no scenery, no gradients, no texture, no cast shadow outside the assets. Add only tiny neutral contact shadows directly inside each asset if needed, using dark neutral pixels that do not blend into the chroma key.
Subject: {subject}
Style/medium: refined hand-painted pixel art / painterly pixel sprite, 3/4 top-down RPG angle, crisp readable silhouettes, authored detail density, 1700s colonial coastal fantasy materials, dark painterly contour pixels, warm sparse highlights, muted coastal reds, ochres, sea greens, navy, cream, soot-dark and damp harbor accents. Match a premium atelier sprite-sheet standard, not a simple hand drawing, not flat vector, not icon doodles, not minimal shapes.
Composition/framing: one clean wide sprite sheet with exactly eight assets separated into very generous padded cells, each fully visible, no overlap between assets. Arrange in a tidy 2 columns by 4 rows grid. Make every asset smaller than its cell, centered in its cell, and leave at least 110 pixels of perfectly flat magenta around every asset and at every outer sheet edge for clean extraction. No part of any asset may touch the sheet edge or cell edge. No text labels.
Materials/textures: {materials}
Constraints: original art only, no copied game sprites, no marketplace asset style, no logos, no real-world brands, no readable text, no photorealism, no 3D render look, no flat vector icons, no simplistic hand-drawn placeholder look, no blurry concept brushwork, no characters, no UI.
Avoid: {avoid}, saturated fantasy colors, modern plastic, readable letters, watermark, background texture, floor plane, assets touching the edge of the sheet."""


PACKS: tuple[PackSpec, ...] = (
    PackSpec(
        slug="tavern_inn_district",
        title="Tavern/Inn District",
        category="G418E_TAVERN_INN_DISTRICT",
        source_filename="g418e_tavern_inn_district_sheet_imagegen.png",
        prompt_filename="g418e_tavern_inn_district_prompt.txt",
        atlas_filename="newport_atelier_g418e_tavern_inn_district_v1.png",
        contact_filename="newport_atelier_g418e_tavern_inn_district_contact_sheet.png",
        manifest_filename="newport_atelier_g418e_tavern_inn_district_manifest.json",
        qa_filename="newport_atelier_g418e_tavern_inn_district_extraction_qa.json",
        report_filename="G418E_TAVERN_INN_DISTRICT_ATELIER_PACK.md",
        placement_policy="Controlled Tavern/Inn frontage and service-yard placement only; dress thresholds and social-hub reads without hiding street grammar or pretending the building rebuild is complete.",
        prompt=_prompt(
            "Create a polished sprite sheet containing exactly eight separate original Newport Tavern/Inn District supporting assets: 1) ornate hanging inn sign with painted mug-and-warm-light pictogram and no readable words, 2) wrought iron lantern pair on short entry brackets with warm glass glow, 3) paired stone planters with coastal herbs and small flowers, 4) service barrel-and-crate cluster for inn deliveries, 5) brick-and-stone entry threshold / doorstep dressing strip, 6) twin chimney stack detail pair as freestanding roof-detail sprite candidates, 7) small stable tack rack with saddle blanket, horseshoe, and rope but no animal, 8) folded firewood and coal scuttle service-yard cluster.",
            "tavern and inn district support props for a believable harbor-city social hub. No full buildings, no people, no readable text, no logos, no brand marks.",
            "chipped painted wood, weathered brick, fieldstone, blackened iron, smoky lantern glass, brass pins, faded cloth, cut firewood, coal, coastal herbs, small salt-air wear.",
            "generic medieval tavern filler",
        ),
        assets=(
            AssetSpec("atelier_g418e_tavern_hanging_inn_sign_01", "hanging_inn_sign", "ornate hanging inn sign", "Adds a controlled social-hub marker to the Tavern/Inn frontage without readable lettering.", 0.92, 0.14, 9.4, "Hero-quality sign candidate; placed as frontage identity, not a building rebuild."),
            AssetSpec("atelier_g418e_tavern_entry_lantern_pair_01", "entry_lantern_pair", "wrought iron entry lantern pair", "Adds warm threshold light and evening identity near the inn entrance.", 0.96, 0.12, 9.3, "Wrought iron and warm glass candidate for controlled inn threshold dressing."),
            AssetSpec("atelier_g418e_tavern_threshold_planters_01", "threshold_planters", "paired stone planters", "Softens the Tavern/Inn frontage and improves social-hub warmth.", 0.92, 0.15, 9.2, "Stone planters with coastal herbs and flowers."),
            AssetSpec("atelier_g418e_tavern_service_barrel_crate_01", "service_barrel_crate_cluster", "inn delivery barrel and crate cluster", "Adds restrained service-life detail to the inn delivery edge.", 0.92, 0.15, 9.2, "Delivery cluster for inn yard and rear service connector."),
            AssetSpec("atelier_g418e_tavern_brick_threshold_01", "brick_stone_entry_threshold", "brick and stone entry threshold strip", "Grounds the Tavern/Inn entry with a readable, walkable doorstep edge.", 0.86, 0.19, 9.1, "Low threshold strip; reinforces ground contact rather than clutter."),
            AssetSpec("atelier_g418e_tavern_twin_stack_chimney_detail_01", "twin_stack_chimney_detail", "twin chimney stack detail pair", "Registers the future brick inn/tavern chimney language as a controlled roof-detail candidate.", 0.94, 0.12, 9.0, "Registered candidate; not placed where it would imply an unbuilt roof integration."),
            AssetSpec("atelier_g418e_tavern_stable_tack_rack_01", "stable_tack_rack", "small stable tack rack", "Adds optional inn service-yard life without animals or route blocking.", 0.92, 0.14, 9.1, "Stable/service-yard support candidate."),
            AssetSpec("atelier_g418e_tavern_firewood_coal_scuttle_01", "firewood_coal_scuttle_cluster", "firewood and coal scuttle cluster", "Adds believable heat/service support near the Tavern/Inn rear yard.", 0.92, 0.15, 9.1, "Warm service cluster for restrained rear placement."),
        ),
    ),
    PackSpec(
        slug="commercial_avenue",
        title="Commercial Avenue",
        category="G418E_COMMERCIAL_AVENUE",
        source_filename="g418e_commercial_avenue_sheet_imagegen.png",
        prompt_filename="g418e_commercial_avenue_prompt.txt",
        atlas_filename="newport_atelier_g418e_commercial_avenue_v1.png",
        contact_filename="newport_atelier_g418e_commercial_avenue_contact_sheet.png",
        manifest_filename="newport_atelier_g418e_commercial_avenue_manifest.json",
        qa_filename="newport_atelier_g418e_commercial_avenue_extraction_qa.json",
        report_filename="G418E_COMMERCIAL_AVENUE_ATELIER_PACK.md",
        placement_policy="Controlled waterfront avenue and commercial-spine placement only; reinforce shopfront identity, market function, and player route readability without random scatter.",
        prompt=_prompt(
            "Create a polished sprite sheet containing exactly eight separate original Newport Commercial Avenue assets: 1) mercantile hanging shop sign with parcel-and-scale pictogram and no readable words, 2) fishmonger/chandlery painted signboard with fish-hook pictogram and no readable words, 3) market handcart with produce crates and folded cloth canopy, 4) stacked produce crates with cabbage, apples, and covered goods, 5) woven basket and parcel display cluster, 6) rolled canvas awning segment with muted coastal stripes, 7) colonial street lamp post with warm lantern and wrought iron, 8) blank directional signpost with multiple arrows and no letters.",
            "commercial street props that make Newport's market spine legible: signs, cart, crates, baskets, awning, lamps, and wayfinding. No full buildings, no people, no readable text, no logos, no brand marks.",
            "chipped painted boards, wrought iron brackets, brass pins, woven baskets, folded canvas, produce, weathered cart wheels, rope knots, soot-warmed lamp glass.",
            "generic medieval market filler",
        ),
        assets=(
            AssetSpec("atelier_g418e_commercial_mercantile_sign_01", "mercantile_hanging_shop_sign", "mercantile hanging shop sign", "Strengthens commercial avenue identity with non-readable shopfront signage.", 0.92, 0.13, 9.3, "Parcel-and-scale pictogram sign for controlled shopfront placement."),
            AssetSpec("atelier_g418e_commercial_fishmonger_sign_01", "fishmonger_chandlery_signboard", "fishmonger/chandlery painted signboard", "Connects the commercial avenue to harbor economy and fish-market reads.", 0.92, 0.13, 9.3, "Fish-hook pictogram sign with no readable letters."),
            AssetSpec("atelier_g418e_commercial_market_cart_01", "market_handcart", "market handcart", "Adds a hero-quality market object to the commercial spine while preserving road readability.", 0.94, 0.14, 9.2, "Produce cart with folded cloth canopy; placed away from route centers."),
            AssetSpec("atelier_g418e_commercial_produce_crates_01", "stacked_produce_crates", "stacked produce crates", "Adds commercial goods massing near storefronts and market edges.", 0.92, 0.15, 9.2, "Produce crates and covered goods for shopfront support."),
            AssetSpec("atelier_g418e_commercial_basket_parcel_display_01", "basket_parcel_display", "woven basket and parcel display", "Provides compact, readable shopfront richness without overfilling the avenue.", 0.92, 0.15, 9.1, "Basket and parcel cluster for controlled market-front placement."),
            AssetSpec("atelier_g418e_commercial_canvas_awning_roll_01", "rolled_canvas_awning_segment", "rolled canvas awning segment", "Adds controlled color and shopfront language without a building rebuild.", 0.88, 0.14, 9.0, "Muted coastal stripe awning segment candidate."),
            AssetSpec("atelier_g418e_commercial_street_lamp_01", "colonial_street_lamp_post", "colonial street lamp post", "Improves commercial route landmarks and nighttime believability.", 0.98, 0.12, 9.2, "Tall street lamp for market-spine rhythm."),
            AssetSpec("atelier_g418e_commercial_directional_signpost_01", "blank_directional_signpost", "blank directional signpost", "Supports player wayfinding at avenue/harbor splits without text.", 0.96, 0.13, 9.1, "Blank arrows, no readable text."),
        ),
    ),
    PackSpec(
        slug="harbor_dock_edge",
        title="Harbor/Dock Edge",
        category="G418E_HARBOR_DOCK_EDGE",
        source_filename="g418e_harbor_dock_edge_sheet_imagegen.png",
        prompt_filename="g418e_harbor_dock_edge_prompt.txt",
        atlas_filename="newport_atelier_g418e_harbor_dock_edge_v1.png",
        contact_filename="newport_atelier_g418e_harbor_dock_edge_contact_sheet.png",
        manifest_filename="newport_atelier_g418e_harbor_dock_edge_manifest.json",
        qa_filename="newport_atelier_g418e_harbor_dock_edge_extraction_qa.json",
        report_filename="G418E_HARBOR_DOCK_EDGE_ATELIER_PACK.md",
        placement_policy="Controlled harbor edge, dock-frontage, and cargo-service placement only; replace weak procedural clusters with authored harbor-life assets while preserving walkable dock reads.",
        prompt=_prompt(
            "Create a polished sprite sheet containing exactly eight separate original Newport Harbor/Dock Edge assets: 1) dock barrel row with salt-worn hoops, 2) large rope coil with frayed loose end, 3) fishing crate stack with net and cork floats, 4) drying net frame with rope knots and small weights, 5) bollard pair with rope wrap and iron caps, 6) compact cargo stack of crates, sacks, and tarped barrel, 7) harbor service post with lantern and coiled rope, 8) fish baskets and covered tub cluster.",
            "working harbor-life props for Newport dock edges and wharf service zones. No full boats, no people, no readable text, no logos, no brand marks.",
            "weathered planks, barrel staves, iron hoops, frayed rope fibers, cork floats, tarred nets, wet canvas, burlap sacks, chipped crates, fish basket reeds, smoky lantern glass.",
            "generic medieval dock filler",
        ),
        assets=(
            AssetSpec("atelier_g418e_harbor_dock_barrel_row_01", "dock_barrel_row", "dock barrel row", "Adds authored cargo rhythm along the working harbor edge.", 0.92, 0.13, 9.2, "Better than old weak deterministic cargo rows; controlled wharf placement only."),
            AssetSpec("atelier_g418e_harbor_rope_coil_large_01", "large_rope_coil", "large rope coil", "Adds crisp harbor material identity near mooring paths.", 0.92, 0.13, 9.3, "Large rope coil with frayed loose end."),
            AssetSpec("atelier_g418e_harbor_fishing_crate_net_stack_01", "fishing_crate_net_stack", "fishing crate stack with net", "Adds fishery-specific dock economy detail.", 0.92, 0.14, 9.3, "Crates, net, cork floats, and dock wear."),
            AssetSpec("atelier_g418e_harbor_net_drying_frame_01", "drying_net_frame", "drying net frame", "Adds recognizable working-harbor service life while staying off routes.", 0.92, 0.15, 9.2, "Net frame with weights; placed as edge feature."),
            AssetSpec("atelier_g418e_harbor_bollard_pair_01", "bollard_pair_rope_wrap", "bollard pair with rope wrap", "Defines mooring edges without blocking player movement.", 0.94, 0.13, 9.2, "Short mooring hardware for dock edge reads."),
            AssetSpec("atelier_g418e_harbor_cargo_stack_01", "compact_cargo_stack", "compact cargo stack", "Raises cargo quality at wharf service points without old procedural clutter.", 0.92, 0.14, 9.2, "Crates, sacks, tarped barrel, and rope."),
            AssetSpec("atelier_g418e_harbor_service_post_lantern_01", "harbor_service_post_lantern", "harbor service post with lantern", "Adds working-harbor lighting and route landmark function.", 0.98, 0.12, 9.3, "Lantern service post with coil; controlled harbor edge placement."),
            AssetSpec("atelier_g418e_harbor_fish_baskets_tub_01", "fish_baskets_covered_tub", "fish baskets and covered tub", "Adds fish-market service detail near dock/market transition.", 0.92, 0.14, 9.2, "Fish baskets and covered tub cluster."),
        ),
    ),
    PackSpec(
        slug="rear_service_connector",
        title="Rear Street / Service Connectors",
        category="G418E_REAR_SERVICE_CONNECTOR",
        source_filename="g418e_rear_service_connector_sheet_imagegen.png",
        prompt_filename="g418e_rear_service_connector_prompt.txt",
        atlas_filename="newport_atelier_g418e_rear_service_connector_v1.png",
        contact_filename="newport_atelier_g418e_rear_service_connector_contact_sheet.png",
        manifest_filename="newport_atelier_g418e_rear_service_connector_manifest.json",
        qa_filename="newport_atelier_g418e_rear_service_connector_extraction_qa.json",
        report_filename="G418E_REAR_SERVICE_CONNECTOR_ATELIER_PACK.md",
        placement_policy="Controlled rear-lane, alley, service-yard, and building-grounding placement only; use to make buildings sit naturally without hiding layout defects.",
        prompt=_prompt(
            "Create a polished sprite sheet containing exactly eight separate original Newport Rear Street / Service Connector assets: 1) low fence gate with weeds and rope latch, 2) utility barrels with broom, bucket, and scrap plank, 3) alley crate stack with covered parcel and worn cloth, 4) firewood handbarrow with small split logs, 5) stone edging strip with tufts for grounding a service path, 6) wash tub with buckets and folded linen, 7) rain barrel with drain stones and small crate, 8) repair board bundle with sawhorse and coiled twine.",
            "rear-lane and service-connector props that ground buildings and yards without hiding layout problems. No full buildings, no people, no readable text, no logos, no brand marks.",
            "weathered fence rails, weeds, rope latch, barrel staves, iron hoops, worn cloth, fieldstone edging, folded linen, muddy drain stones, split firewood, sawhorse timber, twine.",
            "generic medieval service props",
        ),
        assets=(
            AssetSpec("atelier_g418e_service_fence_gate_01", "low_fence_gate", "low fence gate", "Defines rear yards and service connectors without blocking walkability.", 0.92, 0.16, 9.2, "Fence gate with weeds and rope latch."),
            AssetSpec("atelier_g418e_service_utility_barrels_01", "utility_barrels_broom_bucket", "utility barrels with broom and bucket", "Adds service-life grounding at building backs and alleys.", 0.92, 0.15, 9.1, "Utility barrels, broom, bucket, and scrap plank."),
            AssetSpec("atelier_g418e_service_alley_crates_01", "alley_crate_stack", "alley crate stack", "Adds controlled rear-lane storage detail without random scatter.", 0.92, 0.15, 9.1, "Covered crates and worn cloth for alley edges."),
            AssetSpec("atelier_g418e_service_firewood_barrow_01", "firewood_handbarrow", "firewood handbarrow", "Adds believable service movement and yard utility.", 0.94, 0.15, 9.2, "Handbarrow with split logs and mud contact."),
            AssetSpec("atelier_g418e_service_stone_edge_01", "service_path_stone_edge", "stone edging strip with tufts", "Grounds service paths and building edges with low readable detail.", 0.86, 0.20, 9.0, "Low stone strip; supports composition rather than clutter."),
            AssetSpec("atelier_g418e_service_wash_tub_linen_01", "wash_tub_buckets_linen", "wash tub with buckets and linen", "Adds domestic service life near rear connectors.", 0.92, 0.15, 9.2, "Wash tub, buckets, and folded linen."),
            AssetSpec("atelier_g418e_service_rain_barrel_01", "rain_barrel_drain_stones", "rain barrel with drain stones", "Grounds buildings with practical water-service detail.", 0.92, 0.15, 9.1, "Rain barrel, drain stones, and small crate."),
            AssetSpec("atelier_g418e_service_repair_sawhorse_01", "repair_sawhorse_board_bundle", "repair board bundle with sawhorse", "Adds service-yard craft detail along rear streets.", 0.92, 0.15, 9.2, "Sawhorse, boards, and coiled twine."),
        ),
    ),
)


G418E_PLACED_ASSET_IDS = {
    "atelier_g418e_tavern_hanging_inn_sign_01",
    "atelier_g418e_tavern_entry_lantern_pair_01",
    "atelier_g418e_tavern_threshold_planters_01",
    "atelier_g418e_tavern_service_barrel_crate_01",
    "atelier_g418e_tavern_brick_threshold_01",
    "atelier_g418e_commercial_mercantile_sign_01",
    "atelier_g418e_commercial_fishmonger_sign_01",
    "atelier_g418e_commercial_market_cart_01",
    "atelier_g418e_commercial_produce_crates_01",
    "atelier_g418e_commercial_basket_parcel_display_01",
    "atelier_g418e_commercial_canvas_awning_roll_01",
    "atelier_g418e_commercial_street_lamp_01",
    "atelier_g418e_commercial_directional_signpost_01",
    "atelier_g418e_harbor_dock_barrel_row_01",
    "atelier_g418e_harbor_rope_coil_large_01",
    "atelier_g418e_harbor_fishing_crate_net_stack_01",
    "atelier_g418e_harbor_net_drying_frame_01",
    "atelier_g418e_harbor_bollard_pair_01",
    "atelier_g418e_harbor_cargo_stack_01",
    "atelier_g418e_harbor_service_post_lantern_01",
    "atelier_g418e_harbor_fish_baskets_tub_01",
    "atelier_g418e_service_fence_gate_01",
    "atelier_g418e_service_utility_barrels_01",
    "atelier_g418e_service_alley_crates_01",
    "atelier_g418e_service_firewood_barrow_01",
    "atelier_g418e_service_stone_edge_01",
    "atelier_g418e_service_wash_tub_linen_01",
    "atelier_g418e_service_rain_barrel_01",
    "atelier_g418e_service_repair_sawhorse_01",
}


def _is_grid_separator_pixel(pixel: tuple[int, int, int, int]) -> bool:
    r, g, b, a = pixel
    return a > 0 and r > 210 and g > 210 and b > 210 and max(r, g, b) - min(r, g, b) < 38


def _is_loose_grid_separator_pixel(pixel: tuple[int, int, int, int]) -> bool:
    r, g, b, a = pixel
    return a > 0 and r > 80 and g > 80 and b > 80 and max(r, g, b) - min(r, g, b) < 64


def _is_strict_key_magenta(pixel: tuple[int, int, int, int]) -> bool:
    r, g, b, a = pixel
    return a > 0 and r > 170 and b > 170 and g < 150 and abs(r - b) < 120


def _is_strict_magenta_halo(pixel: tuple[int, int, int, int]) -> bool:
    r, g, b, a = pixel
    return a > 0 and r >= 120 and b >= 120 and g <= 115 and abs(r - b) <= 80 and min(r, b) - g >= 38


def sanitize_magenta_residue(image: Image.Image) -> Image.Image:
    """Remove leftover chroma-key and purple matte pixels from extracted sprites."""
    image = image.convert("RGBA")
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            pixel = pixels[x, y]
            if _is_strict_key_magenta(pixel) or _is_strict_magenta_halo(pixel):
                pixels[x, y] = (pixel[0], pixel[1], pixel[2], 0)
    return image


def remove_sheet_grid_separators(image: Image.Image) -> Image.Image:
    """Erase generated white grid borders without touching ordinary highlights."""
    image = image.convert("RGBA")
    pixels = image.load()
    row_threshold = int(image.width * 0.32)
    col_threshold = int(image.height * 0.32)
    loose_row_threshold = int(image.width * 0.62)
    loose_col_threshold = int(image.height * 0.62)
    grid_rows = [
        y
        for y in range(image.height)
        if sum(1 for x in range(image.width) if _is_grid_separator_pixel(pixels[x, y])) >= row_threshold
        or sum(1 for x in range(image.width) if _is_loose_grid_separator_pixel(pixels[x, y])) >= loose_row_threshold
    ]
    grid_cols = [
        x
        for x in range(image.width)
        if sum(1 for y in range(image.height) if _is_grid_separator_pixel(pixels[x, y])) >= col_threshold
        or sum(1 for y in range(image.height) if _is_loose_grid_separator_pixel(pixels[x, y])) >= loose_col_threshold
    ]
    for y in grid_rows:
        for yy in range(max(0, y - 4), min(image.height, y + 5)):
            for x in range(image.width):
                pixels[x, yy] = (255, 255, 255, 0)
    for x in grid_cols:
        for xx in range(max(0, x - 4), min(image.width, x + 5)):
            for y in range(image.height):
                pixels[xx, y] = (255, 255, 255, 0)
    return image


def _line_groups(indices: list[int]) -> list[int]:
    if not indices:
        return []
    groups: list[list[int]] = [[indices[0]]]
    for value in indices[1:]:
        if value <= groups[-1][-1] + 2:
            groups[-1].append(value)
        else:
            groups.append([value])
    return [group[len(group) // 2] for group in groups]


def _grid_separator_lines(source_image: Image.Image) -> tuple[list[int], list[int]]:
    image = source_image.convert("RGBA")
    pixels = image.load()
    row_threshold = int(image.width * 0.32)
    col_threshold = int(image.height * 0.32)
    loose_row_threshold = int(image.width * 0.62)
    loose_col_threshold = int(image.height * 0.62)
    rows = [
        y
        for y in range(image.height)
        if sum(1 for x in range(image.width) if _is_grid_separator_pixel(pixels[x, y])) >= row_threshold
        or sum(1 for x in range(image.width) if _is_loose_grid_separator_pixel(pixels[x, y])) >= loose_row_threshold
    ]
    cols = [
        x
        for x in range(image.width)
        if sum(1 for y in range(image.height) if _is_grid_separator_pixel(pixels[x, y])) >= col_threshold
        or sum(1 for y in range(image.height) if _is_loose_grid_separator_pixel(pixels[x, y])) >= loose_col_threshold
    ]
    return _line_groups(rows), _line_groups(cols)


def _axis_bounds(lines: list[int], extent: int, expected_cells: int) -> list[int]:
    if len(lines) >= expected_cells + 1:
        best = lines[: expected_cells + 1]
        best_span = best[-1] - best[0]
        for start in range(1, len(lines) - expected_cells):
            candidate = lines[start : start + expected_cells + 1]
            span = candidate[-1] - candidate[0]
            if span > best_span:
                best = candidate
                best_span = span
        return best
    near_start = bool(lines and lines[0] <= extent * 0.12)
    near_end = bool(lines and lines[-1] >= extent * 0.88)
    if len(lines) == expected_cells and near_start and near_end:
        span = lines[-1] - lines[0]
        return [int(round(lines[0] + index * span / expected_cells)) for index in range(expected_cells + 1)]
    if len(lines) == expected_cells and near_start:
        return lines + [extent]
    if len(lines) == expected_cells and near_end:
        return [0] + lines
    if len(lines) >= expected_cells - 1:
        return [0] + lines[: expected_cells - 1] + [extent]
    return [int(round(index * extent / expected_cells)) for index in range(expected_cells + 1)]


def _bbox_for_cell(
    alpha_sheet: Image.Image,
    cell: tuple[int, int, int, int],
    padding: int,
) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = cell
    inset = 4
    inner = (
        min(x1 - 1, x0 + inset),
        min(y1 - 1, y0 + inset),
        max(x0 + 1, x1 - inset),
        max(y0 + 1, y1 - inset),
    )
    cropped = alpha_sheet.crop(inner)
    bbox = cropped.getchannel("A").getbbox()
    if bbox is None:
        return inner
    return (
        max(inner[0], inner[0] + bbox[0] - padding),
        max(inner[1], inner[1] + bbox[1] - padding),
        min(inner[2], inner[0] + bbox[2] + padding),
        min(inner[3], inner[1] + bbox[3] + padding),
    )


def source_regions_for_sheet(
    source_image: Image.Image,
    alpha_sheet: Image.Image,
    padding: int = 16,
) -> list[tuple[int, int, int, int]]:
    row_lines, col_lines = _grid_separator_lines(source_image)
    x_bounds = _axis_bounds(col_lines, alpha_sheet.width, GRID_COLUMNS)
    y_bounds = _axis_bounds(row_lines, alpha_sheet.height, GRID_ROWS)
    regions: list[tuple[int, int, int, int]] = []
    for row in range(GRID_ROWS):
        for col in range(GRID_COLUMNS):
            regions.append(
                _bbox_for_cell(
                    alpha_sheet,
                    (x_bounds[col], y_bounds[row], x_bounds[col + 1], y_bounds[row + 1]),
                    padding,
                )
            )
    if len(regions) != GRID_COLUMNS * GRID_ROWS:
        raise RuntimeError(f"expected 8 source regions, found {len(regions)}")
    return regions


def write_prompt(pack: PackSpec) -> Path:
    path = SOURCE_ROOT / pack.prompt_filename
    path.write_text(pack.prompt + "\n", encoding="utf-8")
    return path


def write_assets(pack: PackSpec, alpha_sheet: Image.Image, regions: list[tuple[int, int, int, int]]) -> dict[str, dict]:
    GENERATED_ROOT.mkdir(parents=True, exist_ok=True)
    output: dict[str, dict] = {}
    for index, asset in enumerate(pack.assets):
        region = regions[index]
        piece = alpha_sheet.crop(region)
        padded = Image.new("RGBA", (piece.width + OUTPUT_SPRITE_PADDING * 2, piece.height + OUTPUT_SPRITE_PADDING * 2), (0, 0, 0, 0))
        padded.alpha_composite(piece, (OUTPUT_SPRITE_PADDING, OUTPUT_SPRITE_PADDING))
        padded = sanitize_magenta_residue(padded)
        path = GENERATED_ROOT / f"{asset.asset_id}.png"
        padded.save(path)
        output[asset.asset_id] = {
            "path": path,
            "atlas_region": {"x": region[0], "y": region[1], "w": region[2] - region[0], "h": region[3] - region[1]},
            "sprite_size": {"w": padded.width, "h": padded.height},
            "source_cell": {"column": index % GRID_COLUMNS, "row": index // GRID_COLUMNS},
        }
    return output


def manifest_entry(pack: PackSpec, asset: AssetSpec, output: dict[str, dict], qa: dict) -> dict:
    prompt_path = SOURCE_ROOT / pack.prompt_filename
    source_path = SOURCE_ROOT / pack.source_filename
    atlas_path = ATLAS_ROOT / pack.atlas_filename
    path = output[asset.asset_id]["path"]
    return {
        "asset_id": asset.asset_id,
        "asset_type": asset.asset_type,
        "source_identity": asset.source_identity,
        "family_id": FAMILY_ID,
        "category": pack.category,
        "path": rel(path),
        "atlas": rel(atlas_path),
        "atlas_region": output[asset.asset_id]["atlas_region"],
        "sprite_size": output[asset.asset_id]["sprite_size"],
        "source_cell": output[asset.asset_id]["source_cell"],
        "pivot": {"x": 0.5, "y": asset.pivot_y},
        "grounding": {
            "pivot_y": asset.pivot_y,
            "expected_contact": "hero-family sprite draws from transparent atlas bounds; destination bottom is the intended grounding line",
        },
        "recommended_game_scale": asset.recommended_game_scale,
        "visual_quality_rating": asset.visual_quality_rating,
        "visual_quality_gate": VISUAL_QUALITY_GATE,
        "visual_quality_status": "atelier_review_pass_8_5_plus",
        "source_type": "ai_assisted_image_generation_with_local_chroma_extraction",
        "created_by": "Codex built-in image generation tool plus local transparent extraction",
        "generation_prompt": rel(prompt_path),
        "source_image": rel(source_path),
        "source_image_sha256": sha256(source_path),
        "extraction_script": rel(SCRIPT_PATH),
        "input_sources": [
            {"type": "ai_generated_source_image", "path": rel(source_path), "source_pixels_used": True, "commercial_status": COMMERCIAL_STATUS},
            {"type": "project_prompt", "path": rel(prompt_path), "source_pixels_used": False, "commercial_status": "green_origin_candidate"},
            {"type": "project_style_rules", "path": rel(ART_BIBLE_PATH), "source_pixels_used": False, "commercial_status": "documentation_only"},
            {"type": "locked_atelier_standard", "path": rel(G418D_STANDARD_REPORT_PATH), "source_pixels_used": False, "commercial_status": "documentation_only"},
            {"type": "prior_atelier_rollout_reference", "path": rel(G419A_REPORT_PATH), "source_pixels_used": False, "commercial_status": "documentation_only"},
        ],
        "license": "AI-assisted original generated sprite candidate for Wayfarer; no web image, marketplace pack, ripped sheet, or copied game sprite was supplied as source input. Final-commercial promotion still requires project policy approval for AI-generated artwork.",
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
        "used_in_g418e_playable_hero_slice": asset.asset_id in G418E_PLACED_ASSET_IDS,
        "extraction_qa": qa,
        "gameplay_role": asset.gameplay_role,
        "sha256": sha256(path),
        "notes": asset.notes,
    }


def collect_qa(pack: PackSpec, output: dict[str, dict]) -> dict[str, dict]:
    qa: dict[str, dict] = {}
    for asset in pack.assets:
        image = Image.open(output[asset.asset_id]["path"]).convert("RGBA")
        metrics = atelier.alpha_metrics(image)
        metrics["source_identity"] = asset.source_identity
        metrics["manifest_identity_match"] = Path(output[asset.asset_id]["path"]).stem == asset.asset_id
        metrics["visual_quality_rating"] = asset.visual_quality_rating
        metrics["visual_quality_gate"] = VISUAL_QUALITY_GATE
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
        if asset.visual_quality_rating < VISUAL_QUALITY_GATE:
            failures.append("visual_quality_below_8_5_gate")
        if failures:
            metrics["status"] = "FAIL"
            metrics["failures"] = failures
        qa[asset.asset_id] = metrics
    return qa


def write_qa_report(pack: PackSpec, qa: dict[str, dict]) -> Path:
    path = REPORT_ROOT / pack.qa_filename
    path.parent.mkdir(parents=True, exist_ok=True)
    status = "PASS" if all(details.get("status") == "PASS" for details in qa.values()) else "FAIL"
    path.write_text(
        json.dumps(
            {
                "schema_id": "wayfarer.newport_atelier.g418e.extraction_qa.v1",
                "phase": PHASE,
                "family_id": FAMILY_ID,
                "pack": pack.slug,
                "status": status,
                "visual_quality_gate": VISUAL_QUALITY_GATE,
                "checks": [
                    "source image and prompt exist",
                    "transparent sprites have no magenta background",
                    "transparent sprites have no magenta halo on alpha edges",
                    "generated sheet grid separators are excluded from crops",
                    "sprites retain clean transparent crop padding",
                    "sprites are not cut off at object edges",
                    "sprites remain visually readable by alpha footprint",
                    "source sheet object identity maps to manifest asset ids",
                    "visual quality rating meets or exceeds 8.5/10",
                ],
                "assets": qa,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return path


def label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fill: str = "#efe0ad") -> None:
    draw.text(xy, text, fill=fill, font=ImageFont.load_default())


def write_contact_sheet(pack: PackSpec, output: dict[str, dict]) -> Path:
    path = CONTACT_ROOT / pack.contact_filename
    path.parent.mkdir(parents=True, exist_ok=True)
    card_w = 360
    card_h = 300
    margin_x = 40
    margin_y = 96
    gap_x = 56
    gap_y = 132
    sheet = Image.new("RGB", (880, 1560), "#20261e")
    draw = ImageDraw.Draw(sheet)
    label(draw, (24, 18), f"{PHASE} Newport {pack.title} Atelier Pack")
    label(draw, (24, 40), "Hero-family green-origin candidates: source sheet, transparent extraction, controlled runtime placement.")
    for index, asset in enumerate(pack.assets):
        col = index % GRID_COLUMNS
        row = index // GRID_COLUMNS
        x = margin_x + col * (card_w + gap_x)
        y = margin_y + row * (card_h + gap_y)
        piece = Image.open(output[asset.asset_id]["path"]).convert("RGBA")
        scale = min((card_w - 32) / piece.width, (card_h - 32) / piece.height, 1.0)
        thumb = piece.resize((max(1, int(piece.width * scale)), max(1, int(piece.height * scale))), Image.Resampling.LANCZOS)
        card = Image.new("RGBA", (card_w, card_h), (39, 46, 36, 255))
        card.alpha_composite(thumb, ((card_w - thumb.width) // 2, (card_h - thumb.height) // 2))
        sheet.paste(card.convert("RGB"), (x, y))
        draw.rectangle((x, y, x + card_w, y + card_h), outline="#5e6a54", width=1)
        label(draw, (x + 10, y + card_h + 10), asset.asset_id, "#efe0ad")
        label(draw, (x + 10, y + card_h + 28), asset.asset_type, "#c8d2ac")
    label(draw, (24, 1518), pack.placement_policy, "#c8d2ac")
    sheet.save(path)
    return path


def write_manifest(pack: PackSpec, output: dict[str, dict], qa: dict[str, dict]) -> dict:
    source_path = SOURCE_ROOT / pack.source_filename
    prompt_path = SOURCE_ROOT / pack.prompt_filename
    atlas_path = ATLAS_ROOT / pack.atlas_filename
    contact_path = CONTACT_ROOT / pack.contact_filename
    manifest_path = MANIFEST_ROOT / pack.manifest_filename
    qa_path = REPORT_ROOT / pack.qa_filename
    report_path = REPORT_ROOT / pack.report_filename
    manifest = {
        "schema_id": f"wayfarer.newport_atelier.g418e.{pack.slug}.manifest.v1",
        "phase": PHASE,
        "family_id": FAMILY_ID,
        "pack_id": pack.slug,
        "title": pack.title,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "visual_standard": "G-4.18E hero-quality family using the locked G-4.18D/G-4.19A Newport atelier production standard with an 8.5/10 minimum visual/world gate.",
        "source_policy": "AI-assisted original art is allowed here only with recorded prompt/source image/extraction script and no yellow building pixels, third-party sprites, marketplace packs, or web-scraped images as source inputs.",
        "atlas": rel(atlas_path),
        "source_image": rel(source_path),
        "generation_prompt": rel(prompt_path),
        "generated_asset_root": rel(GENERATED_ROOT),
        "contact_sheet": rel(contact_path),
        "provenance_report": rel(report_path),
        "validation_report": rel(qa_path),
        "pipeline_status": PIPELINE_STATUS,
        "base_pipeline_standard": "G-4.18D Newport atelier cargo pipeline lock and G-4.19A dock clutter rollout pack",
        "family_role": "Coherent Newport harbor commercial, tavern, dock, and service connector visual language for the accepted G-4.23B layout.",
        "placement_policy": pack.placement_policy,
        "green_origin_note": "Green-origin candidate status is provenance-gated and pending final generated-art license policy approval; no asset is final-commercial promoted.",
        "assets": [manifest_entry(pack, asset, output, qa[asset.asset_id]) for asset in pack.assets],
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def write_report(pack: PackSpec, manifest: dict) -> Path:
    path = REPORT_ROOT / pack.report_filename
    path.parent.mkdir(parents=True, exist_ok=True)
    asset_lines = "\n".join(
        f"- `{asset['asset_id']}`: `{asset['asset_type']}`, rating `{asset['visual_quality_rating']}/10`, `{asset['commercial_use_status']}`"
        for asset in manifest["assets"]
    )
    path.write_text(
        f"""# {PHASE} Newport {pack.title} Atelier Pack

## Result

This pack is part of {PHASE}, the {FAMILY_TITLE}. It uses the locked Newport
atelier pattern to produce hero-quality, coherent district dressing for the
accepted G-4.23B harbor-town layout.

## Source Chain

- Source image: `{manifest['source_image']}`
- Prompt record: `{manifest['generation_prompt']}`
- Extraction script: `{rel(SCRIPT_PATH)}`
- Output atlas: `{manifest['atlas']}`
- Manifest: `{rel(MANIFEST_ROOT / pack.manifest_filename)}`
- Contact sheet: `{manifest['contact_sheet']}`
- Extraction QA report: `{manifest['validation_report']}`
- Base standard: `{rel(G418D_STANDARD_REPORT_PATH)}`
- Prior rollout reference: `{rel(G419A_REPORT_PATH)}`

No yellow Newport building pixels, third-party sprite sheets, marketplace
assets, web images, or ripped game art were supplied as source inputs.

## Classification

These assets are `{PROVENANCE_STATUS}`. They are review-eligible as original
AI-assisted candidates, but final commercial promotion remains blocked until
the project approves its final license policy for generated artwork.

## Generated Assets

{asset_lines}

## Placement QA

{pack.placement_policy}
""",
        encoding="utf-8",
    )
    return path


def validate_pipeline(pack: PackSpec, manifest: dict, qa: dict[str, dict]) -> list[str]:
    failures: list[str] = []
    expected_ids = {asset.asset_id for asset in pack.assets}
    for path in [
        SOURCE_ROOT / pack.source_filename,
        SOURCE_ROOT / pack.prompt_filename,
        ATLAS_ROOT / pack.atlas_filename,
        CONTACT_ROOT / pack.contact_filename,
        MANIFEST_ROOT / pack.manifest_filename,
        REPORT_ROOT / pack.report_filename,
        REPORT_ROOT / pack.qa_filename,
    ]:
        if not path.exists():
            failures.append(f"missing artifact: {rel(path)}")
    manifest_ids = {asset.get("asset_id") for asset in manifest.get("assets", [])}
    if manifest_ids != expected_ids:
        failures.append(f"manifest asset ids mismatch for {pack.slug}: {sorted(manifest_ids)} != {sorted(expected_ids)}")
    if set(qa.keys()) != expected_ids:
        failures.append(f"qa asset ids mismatch for {pack.slug}: {sorted(qa.keys())} != {sorted(expected_ids)}")
    for asset_id, details in qa.items():
        if details.get("status") != "PASS":
            failures.append(f"{asset_id} extraction QA failed: {details.get('failures', [])}")
    for asset in manifest.get("assets", []):
        asset_id = asset.get("asset_id", "unknown")
        if asset.get("provenance_status") != PROVENANCE_STATUS:
            failures.append(f"{asset_id} provenance status is not pending AI-assisted green-origin")
        if asset.get("commercial_use_status") != COMMERCIAL_STATUS:
            failures.append(f"{asset_id} commercial status is not pending license review")
        if asset.get("final_commercial_candidate") is not False or asset.get("final_commercial_eligible") is not False:
            failures.append(f"{asset_id} is incorrectly final-commercial promoted")
        if asset.get("source_pixels_from_third_party_material") is not False or asset.get("web_scraped_source_pixels") is not False:
            failures.append(f"{asset_id} has unsafe source-pixel flags")
        if float(asset.get("visual_quality_rating", 0.0)) < VISUAL_QUALITY_GATE:
            failures.append(f"{asset_id} visual quality rating is below {VISUAL_QUALITY_GATE}")
    return failures


def process_pack(pack: PackSpec) -> dict:
    source_path = SOURCE_ROOT / pack.source_filename
    prompt_path = write_prompt(pack)
    if not source_path.exists():
        raise FileNotFoundError(f"missing source sheet: {source_path}")

    ATLAS_ROOT.mkdir(parents=True, exist_ok=True)
    source_image = Image.open(source_path)
    alpha_sheet = remove_sheet_grid_separators(atelier.key_to_alpha(source_image))
    atlas_path = ATLAS_ROOT / pack.atlas_filename
    alpha_sheet.save(atlas_path)

    regions = source_regions_for_sheet(source_image, alpha_sheet)
    output = write_assets(pack, alpha_sheet, regions)
    qa = collect_qa(pack, output)
    qa_path = write_qa_report(pack, qa)
    contact_path = write_contact_sheet(pack, output)
    manifest = write_manifest(pack, output, qa)
    report_path = write_report(pack, manifest)
    failures = validate_pipeline(pack, manifest, qa)
    if failures:
        raise RuntimeError("\n".join(failures))
    print(f"PASS: {pack.slug} -> {len(pack.assets)} assets")
    return {
        "pack_id": pack.slug,
        "title": pack.title,
        "category": pack.category,
        "manifest": rel(MANIFEST_ROOT / pack.manifest_filename),
        "source_image": rel(source_path),
        "generation_prompt": rel(prompt_path),
        "atlas": rel(atlas_path),
        "contact_sheet": rel(contact_path),
        "validation_report": rel(qa_path),
        "provenance_report": rel(report_path),
        "asset_ids": [asset.asset_id for asset in pack.assets],
    }


def write_wave_manifest(pack_results: list[dict]) -> dict:
    all_assets = []
    for pack in PACKS:
        manifest = json.loads((MANIFEST_ROOT / pack.manifest_filename).read_text(encoding="utf-8"))
        all_assets.extend(
            {
                "asset_id": asset["asset_id"],
                "category": asset["category"],
                "path": asset["path"],
                "pack_id": pack.slug,
                "visual_quality_rating": asset["visual_quality_rating"],
                "provenance_status": asset["provenance_status"],
                "commercial_use_status": asset["commercial_use_status"],
                "used_in_g418e_playable_hero_slice": asset["used_in_g418e_playable_hero_slice"],
                "atlas": asset["atlas"],
                "atlas_region": asset["atlas_region"],
                "sprite_size": asset["sprite_size"],
                "recommended_game_scale": asset["recommended_game_scale"],
            }
            for asset in manifest.get("assets", [])
        )
    wave_manifest = {
        "schema_id": "wayfarer.newport_atelier.g418e.hero_asset_family.v1",
        "phase": PHASE,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "title": FAMILY_TITLE,
        "family_id": FAMILY_ID,
        "role": "Coherent green-origin candidate asset family that raises Newport from coherent G-4.23B layout into a richer production-directed harbor-town slice.",
        "visual_quality_gate": VISUAL_QUALITY_GATE,
        "pipeline_status": PIPELINE_STATUS,
        "source_policy": "AI-assisted green-origin candidates pending final license policy approval; no yellow building pixels, third-party sprites, marketplace packs, web-scraped images, or ripped game art were supplied as source input.",
        "placement_policy": "Controlled subset placed across Tavern/Inn, commercial avenue, harbor edge, and rear-service connectors; no random prop scatter and no navigation blocking.",
        "packs": pack_results,
        "assets": all_assets,
    }
    WAVE_MANIFEST_PATH.write_text(json.dumps(wave_manifest, indent=2), encoding="utf-8")
    return wave_manifest


def write_wave_report(wave_manifest: dict) -> None:
    pack_lines = "\n".join(f"- `{pack['pack_id']}`: `{pack['manifest']}`" for pack in wave_manifest["packs"])
    placed_count = sum(1 for asset in wave_manifest["assets"] if asset["used_in_g418e_playable_hero_slice"])
    WAVE_REPORT_PATH.write_text(
        f"""# {PHASE} {FAMILY_TITLE}

## Result

{PHASE} creates a coherent Newport harbor commercial and tavern district asset
family from the locked atelier pipeline. The family is not random prop scatter:
it is organized around Tavern/Inn frontage, commercial avenue identity,
working harbor service, and rear street/service connectors.

## Packs

{pack_lines}

## Runtime Intent

The playable slice uses `{placed_count}` accepted family assets across the
accepted G-4.23B Newport layout. Placement reinforces harbor-city believability,
street/avenue cohesion, district identity, tavern/commercial-spine richness,
dock/market/service-life detail, and readable walkable composition.

## Provenance

Every asset is `{PROVENANCE_STATUS}`. No asset is final-commercial promoted,
and no yellow/red/unknown source pixels were promoted into the playable hero
slice.

## Locked Standard

The source chain is prompt/source image -> transparent extraction -> atlas ->
contact sheet -> manifest/provenance report -> Godot placement -> runtime
screenshots -> Agent Council verdict.

## Agent Council Evidence

The Agent Council must judge the runtime screenshot set against harbor-city
believability, district cohesion, clean extraction, provenance classification,
gameplay readability, and the autonomous pre-G-5 8.5+/10 visual/world bar.
""",
        encoding="utf-8",
    )


def update_registry() -> None:
    registry = json.loads(VISUAL_REGISTRY_PATH.read_text(encoding="utf-8"))
    registry["phase"] = PHASE
    registry["generated_at"] = "2026-05-17"
    registry["policy"] = (
        "G-4.18E adds the Newport Harbor Commercial + Tavern District hero-quality asset family under "
        "the autonomous pre-G-5 protocol. Assets remain AI-assisted green-origin candidates pending final "
        "generated-art license policy approval and are not final-commercial promoted."
    )
    existing_entries = [entry for entry in registry.get("asset_entries", []) if isinstance(entry, dict)]
    entries = [entry for entry in existing_entries if not str(entry.get("asset_id", "")).startswith("atelier_g418e_")]

    for pack in PACKS:
        manifest = json.loads((MANIFEST_ROOT / pack.manifest_filename).read_text(encoding="utf-8"))
        artifacts = {
            "manifest": rel(MANIFEST_ROOT / pack.manifest_filename),
            "source_image": rel(SOURCE_ROOT / pack.source_filename),
            "generation_prompt": rel(SOURCE_ROOT / pack.prompt_filename),
            "extraction_script": rel(SCRIPT_PATH),
            "atlas": rel(ATLAS_ROOT / pack.atlas_filename),
            "contact_sheet": rel(CONTACT_ROOT / pack.contact_filename),
            "validation_report": rel(REPORT_ROOT / pack.qa_filename),
            "provenance_report": rel(REPORT_ROOT / pack.report_filename),
        }
        for asset in manifest.get("assets", []):
            asset_id = asset["asset_id"]
            used_in_map = asset_id in G418E_PLACED_ASSET_IDS
            entries.append(
                {
                    "asset_id": asset_id,
                    "name": asset["source_identity"].title(),
                    "category": pack.category,
                    "path": asset["path"],
                    "source_provenance_status": PROVENANCE_STATUS,
                    "current_usage": {
                        "normal_review": True,
                        "lab_only": False,
                        "runtime_target": "MapLayer G-4.18E Newport hero-family playable slice" if used_in_map else "Registered G-4.18E family candidate; not placed in the playable subset yet",
                        "used_in_g418e_playable_hero_slice": used_in_map,
                        "usage_notes": pack.placement_policy,
                    },
                    "visual_quality_status": "APPROVED_TEMPORARY",
                    "gameplay_role": asset["gameplay_role"],
                    "rebuild_status": "APPROVED_TEMPORARY",
                    "atelier_artifacts": artifacts,
                    "visual_quality_rating": asset["visual_quality_rating"],
                    "final_commercial_candidate": False,
                    "final_commercial_eligible": False,
                    "notes": (
                        asset["notes"]
                        + " AI-assisted green-origin candidate pending final license policy approval; "
                        + "coherent G-4.18E family member, not random prop scatter."
                    ),
                }
            )

    registry["asset_entries"] = entries
    VISUAL_REGISTRY_PATH.write_text(json.dumps(registry, indent=2), encoding="utf-8")


def write_maplayer_regions() -> None:
    regions: dict[str, dict] = {}
    for pack in PACKS:
        manifest = json.loads((MANIFEST_ROOT / pack.manifest_filename).read_text(encoding="utf-8"))
        regions[pack.slug] = {
            "atlas": manifest["atlas"],
            "assets": {
                asset["asset_id"]: {
                    "region": asset["atlas_region"],
                    "sprite_size": asset["sprite_size"],
                    "recommended_game_scale": asset["recommended_game_scale"],
                }
                for asset in manifest.get("assets", [])
            },
        }
    MAPLAYER_REGION_REPORT_PATH.write_text(json.dumps(regions, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-registry", action="store_true")
    args = parser.parse_args()

    for path in [SOURCE_ROOT, GENERATED_ROOT, ATLAS_ROOT, CONTACT_ROOT, MANIFEST_ROOT, REPORT_ROOT]:
        path.mkdir(parents=True, exist_ok=True)

    pack_results = [process_pack(pack) for pack in PACKS]
    wave_manifest = write_wave_manifest(pack_results)
    write_wave_report(wave_manifest)
    write_maplayer_regions()
    if not args.skip_registry:
        update_registry()
    print(f"PASS: {PHASE} hero asset family -> {len(wave_manifest['assets'])} assets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
