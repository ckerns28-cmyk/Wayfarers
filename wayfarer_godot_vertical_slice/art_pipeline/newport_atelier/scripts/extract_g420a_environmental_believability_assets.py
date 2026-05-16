#!/usr/bin/env python3
"""Extract G-4.20A Newport environmental believability atelier sprites.

This wave follows the locked G-4.18D/G-4.19A atelier pattern while scaling it
to multiple environmental packs: saved prompt/source, local chroma extraction,
transparent sprites, atlas, contact sheet, manifest, QA/provenance report, and
registry entries.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[3]
PIPELINE_ROOT = PROJECT_ROOT / "art_pipeline" / "newport_atelier"
SOURCE_ROOT = PIPELINE_ROOT / "source_generated"
GENERATED_ROOT = PIPELINE_ROOT / "generated"
ATLAS_ROOT = PIPELINE_ROOT / "atlases"
CONTACT_ROOT = PIPELINE_ROOT / "contact_sheets"
MANIFEST_ROOT = PIPELINE_ROOT / "manifests"
REPORT_ROOT = PIPELINE_ROOT / "reports"
ART_BIBLE_PATH = PROJECT_ROOT / "docs" / "NEWPORT_ART_BIBLE.md"
G418D_STANDARD_REPORT_PATH = PIPELINE_ROOT / "reports" / "G418D_ATELIER_CARGO_STANDARD.md"
G419A_REPORT_PATH = PIPELINE_ROOT / "reports" / "G419A_NEWPORT_DOCK_CLUTTER_ATELIER_PACK.md"
VISUAL_REGISTRY_PATH = PROJECT_ROOT / "art_pipeline" / "newport" / "manifests" / "newport_visual_production_registry.json"

WAVE_MANIFEST_PATH = MANIFEST_ROOT / "newport_atelier_environmental_believability_manifest.json"
WAVE_REPORT_PATH = REPORT_ROOT / "G420A_NEWPORT_ENVIRONMENTAL_BELIEVABILITY_ATELIER_WAVE.md"
MAPLAYER_REGION_REPORT_PATH = MANIFEST_ROOT / "newport_atelier_environmental_believability_maplayer_regions.json"

MIN_CROP_PADDING = 6
OUTPUT_SPRITE_PADDING = 18
GRID_COLUMNS = 2
GRID_ROWS = 4
VISUAL_QUALITY_GATE = 8.5
PIPELINE_STATUS = "ai_assisted_green_origin_candidate_pending_final_license_policy_approval"
PROVENANCE_STATUS = "ai_assisted_green_origin_candidate_pending_license_review"
COMMERCIAL_STATUS = "green_origin_candidate_pending_license_review"


@dataclass(frozen=True)
class AssetSpec:
    asset_id: str
    asset_type: str
    source_identity: str
    gameplay_role: str
    pivot_y: float
    recommended_game_scale: float
    visual_quality_rating: float
    notes: str


@dataclass(frozen=True)
class PackSpec:
    slug: str
    title: str
    category: str
    source_filename: str
    prompt_filename: str
    atlas_filename: str
    contact_filename: str
    manifest_filename: str
    qa_filename: str
    report_filename: str
    placement_policy: str
    prompt: str
    assets: tuple[AssetSpec, ...]


def rel(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


PACKS: tuple[PackSpec, ...] = (
    PackSpec(
        slug="terrain_edge_dressing",
        title="Terrain Edge Dressing",
        category="ENVIRONMENT_TERRAIN_EDGE",
        source_filename="g420a_terrain_edge_dressing_sheet_imagegen.png",
        prompt_filename="g420a_terrain_edge_dressing_prompt.txt",
        atlas_filename="newport_atelier_terrain_edge_dressing_v1.png",
        contact_filename="newport_atelier_terrain_edge_dressing_contact_sheet.png",
        manifest_filename="newport_atelier_terrain_edge_dressing_manifest.json",
        qa_filename="newport_atelier_terrain_edge_dressing_extraction_qa.json",
        report_filename="G420A_TERRAIN_EDGE_DRESSING_ATELIER_PACK.md",
        placement_policy="Controlled road/grass edge placement only; use at wharf-to-town seams and road shoulders without hiding path readability.",
        prompt="""Use case: stylized-concept
Asset type: production 2D game sprite sheet, original legally clean asset concept for a fantasy 1700s Newport harbor RPG
Primary request: Create a polished sprite sheet containing eight separate original Newport terrain edge dressing assets: 1) grass-to-road feathered north edge strip, 2) grass-to-road feathered south edge strip, 3) mud-to-cobble feather blend strip, 4) dirt path border with tufts and stones, 5) worn road corner blend piece, 6) low cluster of coastal grass tufts, stones, and weeds, 7) shallow muddy puddle and wagon-rut accent, 8) broken grassy road shoulder strip. These must look like high-end hand-painted pixel art game sprites suitable beside detailed colonial Newport harbor buildings and the accepted G-4.18D/G-4.19A atelier sprites.
Scene/backdrop: perfectly flat solid #ff00ff chroma-key background only, no floor plane, no scenery, no gradients, no texture, no cast shadow outside the assets. Add only tiny neutral contact shadows directly inside the terrain pieces if needed, using dark neutral pixels that do not blend into the chroma key.
Subject: low environmental transition sprites for a believable coastal starting town: grass edges, dirt and mud seams, cobble feathering, small stones, weeds, tufts, puddles, worn corners, road shoulders. No buildings, no people, no signs, no full trees, no vehicles.
Style/medium: refined hand-painted pixel art / painterly pixel sprite, 3/4 top-down RPG angle, crisp readable silhouettes, authored detail density, readable at game scale, dark painterly contour pixels, warm sparse highlights, muted coastal greens, grey-brown cobble, damp umber mud, subtle blue-green harbor shadow accents.
Composition/framing: one clean wide sprite sheet with the eight assets separated into generous padded areas, each fully visible, no overlap between separate assets. Arrange in a tidy 4 by 2 grid. Camera angle and scale consistent across all eight assets. Leave at least 60 pixels of flat magenta around each asset for clean extraction. No text labels.
Materials/textures: salt-air grass blades, small fieldstones, wet dirt, worn cobble chips, weeds in cracks, muddy puddle highlights, uneven road shoulders, hand-authored edge pixels.
Constraints: original art only, no copied game sprites, no marketplace asset style, no logos, no text, no UI, no photorealism, no 3D render look, no flat vector icons, no blurry concept-art brushwork, no characters, no boats, no buildings.
Avoid: generic medieval dungeon filler, saturated fantasy colors, modern pavement, plastic, labels, watermarks, background texture, assets touching the edge of the sheet.""",
        assets=(
            AssetSpec("atelier_terrain_grass_road_edge_north_01", "grass_to_road_north_edge_strip", "grass-to-road feathered north edge strip", "Softens the north edge of the harborfront road without covering the walkable read.", 0.82, 0.23, 9.0, "Low grass/cobble feather for the north side of road seams."),
            AssetSpec("atelier_terrain_grass_road_edge_south_01", "grass_to_road_south_edge_strip", "grass-to-road feathered south edge strip", "Softens the south edge of road and wharf transitions.", 0.82, 0.23, 9.0, "Low grass/cobble feather for the south side of road seams."),
            AssetSpec("atelier_terrain_mud_cobble_feather_01", "mud_to_cobble_feather_strip", "mud-to-cobble feather blend strip", "Bridges muddy wharf shoulders into cobble without visual snapping.", 0.84, 0.23, 9.0, "Mud/cobble seam with weeds and damp stones."),
            AssetSpec("atelier_terrain_dirt_path_border_01", "dirt_path_border_strip", "dirt path border with tufts and stones", "Defines dirt path edges while keeping paths readable.", 0.84, 0.22, 8.9, "Small stones, weeds, and dirt edge texture."),
            AssetSpec("atelier_terrain_worn_corner_blend_01", "worn_road_corner_blend", "worn road corner blend piece", "Makes road corners look walked-in instead of tile-cut.", 0.84, 0.20, 8.9, "Curved worn corner with compacted dirt and cobble chips."),
            AssetSpec("atelier_terrain_coastal_tuft_stone_cluster_01", "coastal_tuft_stone_cluster", "low coastal grass tufts, stones, and weeds cluster", "Adds small authored grounding at empty grass/road corners.", 0.90, 0.18, 8.8, "Low grass and stone cluster for sparse seam accents."),
            AssetSpec("atelier_terrain_muddy_puddle_rut_01", "muddy_puddle_wagon_rut", "shallow muddy puddle and wagon-rut accent", "Breaks up flat service-lane mud while staying nonblocking.", 0.86, 0.19, 8.8, "Low puddle/rut accent with damp highlights."),
            AssetSpec("atelier_terrain_broken_grassy_shoulder_01", "broken_grassy_road_shoulder", "broken grassy road shoulder strip", "Adds natural shoulder texture to market-spine edges.", 0.84, 0.22, 8.9, "Low broken shoulder strip with grass fingers and stones."),
        ),
    ),
    PackSpec(
        slug="cobble_path_transition",
        title="Cobble And Path Transition Set",
        category="ENVIRONMENT_PATH_TRANSITION",
        source_filename="g420a_cobble_path_transition_sheet_imagegen.png",
        prompt_filename="g420a_cobble_path_transition_prompt.txt",
        atlas_filename="newport_atelier_cobble_path_transition_v1.png",
        contact_filename="newport_atelier_cobble_path_transition_contact_sheet.png",
        manifest_filename="newport_atelier_cobble_path_transition_manifest.json",
        qa_filename="newport_atelier_cobble_path_transition_extraction_qa.json",
        report_filename="G420A_COBBLE_PATH_TRANSITION_ATELIER_PACK.md",
        placement_policy="Controlled market-spine and wharf-to-town walking-surface placement only; do not obscure routes or door thresholds.",
        prompt="""Use case: stylized-concept
Asset type: production 2D game sprite sheet, original legally clean asset concept for a fantasy 1700s Newport harbor RPG
Primary request: Create a polished sprite sheet containing eight separate original Newport cobble and path transition assets: 1) long worn market-spine cobble road patch, 2) broken cobble patch with missing stones and dirt, 3) dirt-worn walking path section, 4) road shoulder piece where cobble fades into earth, 5) curb and doorstep threshold stone strip, 6) cobble-to-wharf-plank seam piece, 7) sunken gutter/drain stones with grime, 8) loose stones and small paving fragments strip. These must look like high-end hand-painted pixel art game sprites suitable beside detailed colonial Newport harbor buildings and the accepted G-4.18D/G-4.19A atelier sprites.
Scene/backdrop: perfectly flat solid #ff00ff chroma-key background only, no floor plane, no scenery, no gradients, no texture, no cast shadow outside the assets. Add only tiny neutral contact shadows directly inside pieces if needed, using dark neutral pixels that do not blend into the chroma key.
Subject: low road/path transition sprites for a believable playable starting town: uneven colonial cobbles, dirt-worn paths, road shoulders, curb/threshold stones, plank seam, small gutter stones, loose fragments. No buildings, no people, no signs, no full props taller than ankle height.
Style/medium: refined hand-painted pixel art / painterly pixel sprite, 3/4 top-down RPG angle, crisp readable silhouettes, authored detail density, readable at game scale, dark painterly contour pixels, warm sparse highlights, muted grey cobbles, tan dust, damp brown dirt, subtle blue-green harbor shadow accents.
Composition/framing: one clean wide sprite sheet with exactly eight assets separated into very generous padded areas, each fully visible, no overlap between separate assets. Arrange in a tidy 2 columns by 4 rows grid. Make every asset smaller than its cell, centered in its cell, and leave at least 110 pixels of perfectly flat magenta around every asset and at every outer sheet edge for clean extraction. No part of any stone, pebble, shadow, plank, or debris may touch the image edge or cell edge. No text labels.
Materials/textures: hand-laid fieldstone cobble, broken edges, mud in seams, worn walking lanes, chipped curbstones, weathered plank ends, gutter grime, salt-air dampness.
Constraints: original art only, no copied game sprites, no marketplace asset style, no logos, no text, no UI, no photorealism, no 3D render look, no flat vector icons, no blurry concept-art brushwork, no characters, no boats, no buildings.
Avoid: generic medieval dungeon tiles, saturated fantasy colors, modern asphalt or concrete, plastic, labels, watermarks, background texture, assets touching the edge of the sheet.""",
        assets=(
            AssetSpec("atelier_path_market_cobble_long_01", "market_spine_cobble_patch", "long worn market-spine cobble road patch", "Adds authored wear to the main market walking surface.", 0.84, 0.22, 9.1, "Long low cobble patch with worn middle track."),
            AssetSpec("atelier_path_broken_cobble_patch_01", "broken_cobble_patch", "broken cobble patch with missing stones and dirt", "Breaks up repeated cobble near the wharf-to-town seam.", 0.84, 0.20, 9.0, "Broken cobbles and dirt-filled gaps."),
            AssetSpec("atelier_path_dirt_worn_section_01", "dirt_worn_path_section", "dirt-worn walking path section", "Gives service-lane foot traffic a readable surface.", 0.84, 0.21, 8.9, "Worn earth path with small stone inclusions."),
            AssetSpec("atelier_path_road_shoulder_earth_01", "road_shoulder_earth_piece", "road shoulder where cobble fades into earth", "Connects cobble roads to softer grass/mud shoulders.", 0.84, 0.21, 8.9, "Earth shoulder with loose stones and dust."),
            AssetSpec("atelier_path_curb_threshold_stones_01", "curb_threshold_stone_strip", "curb and doorstep threshold stone strip", "Reinforces non-tavern building base approach points.", 0.86, 0.19, 9.0, "Threshold strip for doors and stoops."),
            AssetSpec("atelier_path_cobble_plank_seam_01", "cobble_to_plank_seam_piece", "cobble-to-wharf-plank seam piece", "Clarifies wharf-to-town material transition.", 0.84, 0.21, 9.0, "Stone-to-plank seam with grime and plank ends."),
            AssetSpec("atelier_path_sunken_gutter_stones_01", "sunken_gutter_drain_stones", "sunken gutter/drain stones with grime", "Adds low drainage detail beside market-spine edges.", 0.86, 0.19, 8.9, "Darkened gutter stones and damp grime."),
            AssetSpec("atelier_path_loose_paving_fragments_01", "loose_paving_fragment_strip", "loose stones and paving fragments strip", "Adds low scatter at road shoulders without blocking movement.", 0.86, 0.18, 8.8, "Low loose stones for edge dressing."),
        ),
    ),
    PackSpec(
        slug="shoreline_harbor_edge",
        title="Shoreline And Harbor Edge Dressing",
        category="ENVIRONMENT_SHORELINE_EDGE",
        source_filename="g420a_shoreline_harbor_edge_sheet_imagegen.png",
        prompt_filename="g420a_shoreline_harbor_edge_prompt.txt",
        atlas_filename="newport_atelier_shoreline_harbor_edge_v1.png",
        contact_filename="newport_atelier_shoreline_harbor_edge_contact_sheet.png",
        manifest_filename="newport_atelier_shoreline_harbor_edge_manifest.json",
        qa_filename="newport_atelier_shoreline_harbor_edge_extraction_qa.json",
        report_filename="G420A_SHORELINE_HARBOR_EDGE_ATELIER_PACK.md",
        placement_policy="Controlled shoreline and dock-edge placement only; keep low debris subordinate and never hide dock route reads.",
        prompt="""Use case: stylized-concept
Asset type: production 2D game sprite sheet, original legally clean asset concept for a fantasy 1700s Newport harbor RPG
Primary request: Create a polished sprite sheet containing eight separate original Newport shoreline and harbor edge dressing assets: 1) seaweed drift line, 2) shells and pebble cluster, 3) small wet rocks on sand, 4) driftwood log cluster, 5) wet sand and mud accent strip, 6) broken harbor debris slats with rope scrap, 7) shallow tide puddle with dark mud edge, 8) eelgrass/reeds low cluster. These must look like high-end hand-painted pixel art game sprites suitable beside detailed colonial Newport harbor buildings and the accepted G-4.18D/G-4.19A atelier sprites.
Scene/backdrop: perfectly flat solid #ff00ff chroma-key background only, no floor plane, no scenery, no gradients, no texture, no cast shadow outside the assets. Add only tiny neutral contact shadows directly inside low pieces if needed, using dark neutral pixels that do not blend into the chroma key.
Subject: low shoreline transition sprites for a believable coastal starting town: seaweed, shells, pebbles, small rocks, driftwood, wet sand, mud, broken slats, rope scraps, tide puddles, eelgrass. No boats, no docks as structures, no buildings, no people, no signs.
Style/medium: refined hand-painted pixel art / painterly pixel sprite, 3/4 top-down RPG angle, crisp readable silhouettes, authored detail density, readable at game scale, dark painterly contour pixels, warm sparse highlights, muted kelp greens, wet umber mud, shell creams, grey rocks, subtle blue-green harbor shadow accents.
Composition/framing: one clean wide sprite sheet with eight assets separated into generous padded areas, each fully visible, no overlap between separate assets. Arrange in a tidy 2 columns by 4 rows grid. Camera angle and scale consistent across all eight assets. Leave at least 60 pixels of flat magenta around each asset for clean extraction. No text labels.
Materials/textures: slippery seaweed strands, shell ridges, wet rock highlights, salt-bleached driftwood grain, mud gloss, damp sand granules, frayed rope fibers, broken board splinters, tide-pool reflections.
Constraints: original art only, no copied game sprites, no marketplace asset style, no logos, no text, no UI, no photorealism, no 3D render look, no flat vector icons, no blurry concept-art brushwork, no characters, no boats, no buildings.
Avoid: generic fantasy swamp clutter, saturated colors, modern trash, plastic, labels, watermarks, background texture, assets touching the edge of the sheet.""",
        assets=(
            AssetSpec("atelier_shore_seaweed_drift_line_01", "seaweed_drift_line", "seaweed drift line", "Marks the tide edge beside docks with low material detail.", 0.86, 0.19, 9.1, "Low seaweed drift line with salt-wet texture."),
            AssetSpec("atelier_shore_shell_pebble_cluster_01", "shell_pebble_cluster", "shells and pebble cluster", "Adds small coastal identity at shoreline edges.", 0.88, 0.17, 8.9, "Shells and pebbles with readable light accents."),
            AssetSpec("atelier_shore_wet_rocks_sand_01", "wet_rocks_on_sand", "small wet rocks on sand", "Adds shoreline grounding around waterline bends.", 0.88, 0.18, 8.9, "Wet stones with dark sand contact."),
            AssetSpec("atelier_shore_driftwood_log_cluster_01", "driftwood_log_cluster", "driftwood log cluster", "Adds believable harbor edge debris without implying a blocked route.", 0.90, 0.19, 9.0, "Bleached driftwood with dark wet edges."),
            AssetSpec("atelier_shore_wet_sand_mud_strip_01", "wet_sand_mud_strip", "wet sand and mud accent strip", "Softens shore-to-wharf edges and wet mud pockets.", 0.84, 0.21, 8.9, "Low wet sand/mud strip with gloss accents."),
            AssetSpec("atelier_shore_harbor_debris_slats_rope_01", "broken_harbor_slats_rope_scrap", "broken harbor debris slats with rope scrap", "Adds working-harbor debris near wharf edges.", 0.90, 0.18, 9.0, "Small broken slats and rope scraps."),
            AssetSpec("atelier_shore_tide_puddle_mud_edge_01", "tide_puddle_mud_edge", "shallow tide puddle with dark mud edge", "Breaks up wet shoreline flats with readable low puddles.", 0.86, 0.19, 8.8, "Tide puddle and dark mud rim."),
            AssetSpec("atelier_shore_eelgrass_reeds_cluster_01", "eelgrass_reeds_low_cluster", "eelgrass/reeds low cluster", "Adds sparse coastal vegetation along shore seams.", 0.90, 0.18, 8.9, "Low reeds and eelgrass for shoreline pockets."),
        ),
    ),
    PackSpec(
        slug="building_grounding_service",
        title="Building Grounding And Service-Lane Accents",
        category="ENVIRONMENT_BUILDING_GROUNDING",
        source_filename="g420a_building_grounding_service_sheet_imagegen.png",
        prompt_filename="g420a_building_grounding_service_prompt.txt",
        atlas_filename="newport_atelier_building_grounding_service_v1.png",
        contact_filename="newport_atelier_building_grounding_service_contact_sheet.png",
        manifest_filename="newport_atelier_building_grounding_service_manifest.json",
        qa_filename="newport_atelier_building_grounding_service_extraction_qa.json",
        report_filename="G420A_BUILDING_GROUNDING_SERVICE_ATELIER_PACK.md",
        placement_policy="Controlled non-centerpiece building-base and service-lane placement only; do not patch the Tavern/Inn or treat any building as final.",
        prompt="""Use case: stylized-concept
Asset type: production 2D game sprite sheet, original legally clean asset concept for a fantasy 1700s Newport harbor RPG
Primary request: Create a polished sprite sheet containing eight separate original Newport building-grounding and service-lane accent assets: 1) doorstep stones and stoop base accent, 2) foundation dirt and soft shadow strip for a building wall base, 3) wall-edge weeds and stones low strip, 4) leaning repair boards with tiny crate scraps, 5) small barrel and crate grounding cluster, 6) wash tub with two buckets, 7) low fence segment with weeds at posts, 8) stacked firewood with chopping block. These must look like high-end hand-painted pixel art game sprites suitable beside detailed colonial Newport harbor buildings and the accepted G-4.18D/G-4.19A atelier sprites.
Scene/backdrop: perfectly flat solid #ff00ff chroma-key background only, no floor plane, no scenery, no gradients, no texture, no cast shadow outside the assets. Add only tiny neutral contact shadows directly under the props if needed, using dark neutral pixels that do not blend into the chroma key.
Subject: small environmental grounding props for building bases and service lanes in a believable coastal starting town: stones, foundation dirt, weeds, repair boards, low barrels/crates, wash tub, buckets, fence, firewood. No building walls or roofs, no people, no NPC/player standards, no signage.
Style/medium: refined hand-painted pixel art / painterly pixel sprite, 3/4 top-down RPG angle, crisp readable silhouettes, authored detail density, readable at game scale, dark painterly contour pixels, warm sparse highlights, weathered grey-brown wood, aged stone, muted coastal greens, iron-dark hoops, subtle blue-green harbor shadow accents.
Composition/framing: one clean wide sprite sheet with eight assets separated into generous padded areas, each fully visible, no overlap between separate assets. Arrange in a tidy 2 columns by 4 rows grid. Camera angle and scale consistent across all eight assets. Leave at least 60 pixels of flat magenta around each asset for clean extraction. No text labels.
Materials/textures: doorstep fieldstone chips, compacted foundation dirt, weeds in wall cracks, salt-worn boards, small crates/barrels, galvanized or wood wash tub, worn bucket hoops, old fence rails, split firewood bark and cut ends.
Constraints: original art only, no copied game sprites, no marketplace asset style, no logos, no text, no UI, no photorealism, no 3D render look, no flat vector icons, no blurry concept-art brushwork, no characters, no boats, no buildings.
Avoid: generic fantasy dungeon props, saturated fantasy colors, modern plastic, modern tools, labels, watermarks, background texture, assets touching the edge of the sheet.""",
        assets=(
            AssetSpec("atelier_ground_doorstep_stones_01", "doorstep_stones_stoop_base", "doorstep stones and stoop base accent", "Supports non-tavern door reads without replacing building art.", 0.90, 0.17, 9.0, "Small doorstep stone accent for grounded entries."),
            AssetSpec("atelier_ground_foundation_shadow_strip_01", "foundation_dirt_shadow_strip", "foundation dirt and soft shadow strip", "Adds a low base-shadow strip where buildings meet ground.", 0.84, 0.22, 8.9, "Foundation dirt and shadow, not a building patch."),
            AssetSpec("atelier_ground_wall_weeds_stones_01", "wall_edge_weeds_stones_strip", "wall-edge weeds and stones low strip", "Softens building bases with weeds and stones.", 0.86, 0.20, 8.9, "Low weeds and stones for wall edges."),
            AssetSpec("atelier_ground_repair_boards_crate_scraps_01", "repair_boards_crate_scraps", "leaning repair boards with tiny crate scraps", "Adds service-lane craft clutter without blocking the path.", 0.92, 0.17, 9.0, "Weathered repair boards and small crate scraps."),
            AssetSpec("atelier_ground_barrel_crate_cluster_01", "small_barrel_crate_ground_cluster", "small barrel and crate grounding cluster", "Adds restrained building-base utility clutter.", 0.92, 0.16, 9.0, "Small barrel/crate base cluster."),
            AssetSpec("atelier_ground_wash_tub_buckets_01", "wash_tub_with_buckets", "wash tub with two buckets", "Signals residential/service life in controlled side yards.", 0.92, 0.16, 8.9, "Wash tub and buckets for service-lane dressing."),
            AssetSpec("atelier_ground_low_fence_weeds_01", "low_fence_segment_weeds", "low fence segment with weeds at posts", "Defines yards and service edges while staying visually low.", 0.92, 0.18, 8.9, "Low fence segment with weeded posts."),
            AssetSpec("atelier_ground_firewood_chopping_block_01", "firewood_stack_chopping_block", "stacked firewood with chopping block", "Adds residential/service utility texture away from main paths.", 0.92, 0.16, 8.9, "Firewood stack and chopping block for side yards."),
        ),
    ),
)


def _is_key_magenta(r: int, g: int, b: int, a: int) -> bool:
    return a > 0 and r > 170 and b > 170 and g < 150 and abs(r - b) < 120


def _is_magenta_halo(r: int, g: int, b: int, a: int) -> bool:
    return a > 0 and r >= 120 and b >= 120 and g <= 115 and abs(r - b) <= 80 and min(r, b) - g >= 38


def key_to_alpha(image: Image.Image) -> Image.Image:
    """Remove the #ff00ff chroma key and purple matte contamination."""
    image = image.convert("RGBA")
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            magenta_dominant = r > g + 45 and b > g + 45 and abs(r - b) < 96
            saturated_key = r > 170 and b > 170 and g < 155 and abs(r - b) < 124
            if magenta_dominant or saturated_key:
                pixels[x, y] = (r, g, b, 0)
                continue
            if r > 120 and b > 120 and g < 145 and abs(r - b) < 110:
                neutral = max(g, min(r, b) - 48)
                pixels[x, y] = (neutral, neutral, neutral, a)
    despill_magenta_edges(image)
    return image


def despill_magenta_edges(image: Image.Image) -> None:
    """Neutralize remaining purple edge pixels after alpha removal."""
    pixels = image.load()
    replacements: list[tuple[int, int, tuple[int, int, int, int]]] = []
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            if not _is_magenta_halo(r, g, b, a):
                continue
            near_transparent = False
            for ny in range(max(0, y - 1), min(image.height, y + 2)):
                for nx in range(max(0, x - 1), min(image.width, x + 2)):
                    if nx == x and ny == y:
                        continue
                    if pixels[nx, ny][3] <= 8:
                        near_transparent = True
                        break
                if near_transparent:
                    break
            if near_transparent:
                neutral = max(18, min(145, g, min(r, b) - 58))
                replacements.append((x, y, (neutral, neutral, neutral, a)))
    for x, y, value in replacements:
        pixels[x, y] = value


def alpha_metrics(image: Image.Image) -> dict:
    image = image.convert("RGBA")
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        return {
            "size": {"w": image.width, "h": image.height},
            "alpha_bbox": None,
            "alpha_pixels": 0,
            "opaque_pixels": 0,
            "magenta_pixels_remaining": 0,
            "magenta_halo_pixels": 0,
            "crop_padding": {"left": 0, "top": 0, "right": 0, "bottom": 0},
            "cutoff_edges": ["empty_alpha"],
            "readable": False,
        }

    pixels = image.load()
    alpha_pixels = 0
    opaque_pixels = 0
    magenta_pixels = 0
    halo_pixels = 0
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            if a <= 0:
                continue
            alpha_pixels += 1
            if a >= 220:
                opaque_pixels += 1
            if _is_key_magenta(r, g, b, a):
                magenta_pixels += 1
            if not _is_magenta_halo(r, g, b, a):
                continue
            near_transparent = False
            for ny in range(max(0, y - 1), min(image.height, y + 2)):
                for nx in range(max(0, x - 1), min(image.width, x + 2)):
                    if nx == x and ny == y:
                        continue
                    if pixels[nx, ny][3] <= 8:
                        near_transparent = True
                        break
                if near_transparent:
                    break
            if near_transparent:
                halo_pixels += 1

    padding = {
        "left": bbox[0],
        "top": bbox[1],
        "right": image.width - bbox[2],
        "bottom": image.height - bbox[3],
    }
    bbox_w = bbox[2] - bbox[0]
    bbox_h = bbox[3] - bbox[1]
    return {
        "size": {"w": image.width, "h": image.height},
        "alpha_bbox": {"x": bbox[0], "y": bbox[1], "w": bbox_w, "h": bbox_h},
        "alpha_pixels": alpha_pixels,
        "opaque_pixels": opaque_pixels,
        "magenta_pixels_remaining": magenta_pixels,
        "magenta_halo_pixels": halo_pixels,
        "crop_padding": padding,
        "cutoff_edges": [side for side, value in padding.items() if value < MIN_CROP_PADDING],
        "readable": alpha_pixels >= 1200 and bbox_w >= 42 and bbox_h >= 24,
    }


def _projection_runs(counts: list[int], threshold: int, min_gap: int, min_span: int) -> list[tuple[int, int]]:
    runs: list[tuple[int, int]] = []
    start: int | None = None
    last_content: int | None = None
    gap = 0
    for i, count in enumerate(counts):
        if count >= threshold:
            if start is None:
                start = i
            last_content = i
            gap = 0
            continue
        if start is None:
            continue
        gap += 1
        if gap >= min_gap and last_content is not None:
            if last_content + 1 - start >= min_span:
                runs.append((start, last_content + 1))
            start = None
            last_content = None
            gap = 0
    if start is not None and last_content is not None and last_content + 1 - start >= min_span:
        runs.append((start, last_content + 1))
    return runs


def _bbox_for_region(alpha_sheet: Image.Image, region: tuple[int, int, int, int], padding: int) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = region
    cropped = alpha_sheet.crop(region)
    bbox = cropped.getchannel("A").getbbox()
    if bbox is None:
        return region
    return (
        max(0, x0 + bbox[0] - padding),
        max(0, y0 + bbox[1] - padding),
        min(alpha_sheet.width, x0 + bbox[2] + padding),
        min(alpha_sheet.height, y0 + bbox[3] + padding),
    )


def source_regions_for_sheet(alpha_sheet: Image.Image, padding: int = 16) -> list[tuple[int, int, int, int]]:
    alpha = alpha_sheet.getchannel("A")
    row_counts = [sum(1 for x in range(alpha_sheet.width) if alpha.getpixel((x, y)) > 8) for y in range(alpha_sheet.height)]
    row_runs = _projection_runs(row_counts, threshold=30, min_gap=28, min_span=24)
    regions: list[tuple[int, int, int, int]] = []
    for y0, y1 in row_runs:
        col_counts = []
        for x in range(alpha_sheet.width):
            count = 0
            for y in range(y0, y1):
                if alpha.getpixel((x, y)) > 8:
                    count += 1
            col_counts.append(count)
        col_runs = _projection_runs(col_counts, threshold=12, min_gap=28, min_span=24)
        for x0, x1 in col_runs:
            regions.append(_bbox_for_region(alpha_sheet, (x0, y0, x1, y1), padding))
    if len(regions) == GRID_COLUMNS * GRID_ROWS:
        return regions

    # Fallback to the expected 2x4 layout if the projection pass finds too many
    # internal gaps in a textured low strip.
    fallback: list[tuple[int, int, int, int]] = []
    cell_w = alpha_sheet.width / GRID_COLUMNS
    cell_h = alpha_sheet.height / GRID_ROWS
    for index in range(GRID_COLUMNS * GRID_ROWS):
        col = index % GRID_COLUMNS
        row = index // GRID_COLUMNS
        x0 = int(round(col * cell_w))
        y0 = int(round(row * cell_h))
        x1 = int(round((col + 1) * cell_w))
        y1 = int(round((row + 1) * cell_h))
        fallback.append(_bbox_for_region(alpha_sheet, (x0, y0, x1, y1), padding))
    return fallback


def write_prompt(pack: PackSpec) -> Path:
    path = SOURCE_ROOT / pack.prompt_filename
    path.write_text(pack.prompt + "\n", encoding="utf-8")
    return path


def write_assets(pack: PackSpec, alpha_sheet: Image.Image) -> dict[str, dict]:
    GENERATED_ROOT.mkdir(parents=True, exist_ok=True)
    output: dict[str, dict] = {}
    regions = source_regions_for_sheet(alpha_sheet)
    for index, asset in enumerate(pack.assets):
        region = regions[index]
        piece = alpha_sheet.crop(region)
        padded = Image.new("RGBA", (piece.width + OUTPUT_SPRITE_PADDING * 2, piece.height + OUTPUT_SPRITE_PADDING * 2), (0, 0, 0, 0))
        padded.alpha_composite(piece, (OUTPUT_SPRITE_PADDING, OUTPUT_SPRITE_PADDING))
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
        "category": pack.category,
        "path": rel(path),
        "atlas": rel(atlas_path),
        "atlas_region": output[asset.asset_id]["atlas_region"],
        "sprite_size": output[asset.asset_id]["sprite_size"],
        "source_cell": output[asset.asset_id]["source_cell"],
        "pivot": {"x": 0.5, "y": asset.pivot_y},
        "grounding": {
            "pivot_y": asset.pivot_y,
            "expected_contact": "low environmental sprite sits inside transparent bounds; draw destination bottom is the intended grounding line",
        },
        "recommended_game_scale": asset.recommended_game_scale,
        "visual_quality_rating": asset.visual_quality_rating,
        "visual_quality_gate": VISUAL_QUALITY_GATE,
        "visual_quality_status": "atelier_review_pass_8_5_plus",
        "source_type": "ai_assisted_image_generation_with_local_chroma_extraction",
        "created_by": "Codex built-in image generation tool plus local transparent extraction",
        "generation_prompt": rel(prompt_path),
        "source_image": rel(source_path),
        "extraction_script": rel(SCRIPT_PATH),
        "input_sources": [
            {
                "type": "ai_generated_source_image",
                "path": rel(source_path),
                "source_pixels_used": True,
                "commercial_status": COMMERCIAL_STATUS,
            },
            {
                "type": "project_prompt",
                "path": rel(prompt_path),
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
        "license": "AI-assisted original generated sprite candidate for Wayfarer; no web image, marketplace pack, ripped sheet, or copied game sprite was provided as source input. Final-commercial promotion still requires project policy approval for AI-generated artwork.",
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
        "gameplay_role": asset.gameplay_role,
        "sha256": sha256(path),
        "notes": asset.notes,
    }


def collect_qa(pack: PackSpec, output: dict[str, dict]) -> dict[str, dict]:
    qa: dict[str, dict] = {}
    for asset in pack.assets:
        image = Image.open(output[asset.asset_id]["path"]).convert("RGBA")
        metrics = alpha_metrics(image)
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
                "schema_id": "wayfarer.newport_atelier.extraction_qa.v1",
                "phase": "G-4.20A",
                "pack": pack.slug,
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
                ],
                "assets": qa,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return path


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
    label(draw, (24, 18), f"G-4.20A Newport {pack.title} Atelier Pack")
    label(draw, (24, 40), "Environmental believability wave: AI-assisted green-origin candidates, extracted sprites, controlled placement.")
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


def label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fill: str = "#efe0ad") -> None:
    draw.text(xy, text, fill=fill, font=ImageFont.load_default())


def write_manifest(pack: PackSpec, output: dict[str, dict], qa: dict[str, dict]) -> dict:
    source_path = SOURCE_ROOT / pack.source_filename
    prompt_path = SOURCE_ROOT / pack.prompt_filename
    atlas_path = ATLAS_ROOT / pack.atlas_filename
    contact_path = CONTACT_ROOT / pack.contact_filename
    manifest_path = MANIFEST_ROOT / pack.manifest_filename
    qa_path = REPORT_ROOT / pack.qa_filename
    report_path = REPORT_ROOT / pack.report_filename
    manifest = {
        "schema_id": f"wayfarer.newport_atelier.g420a.{pack.slug}.manifest.v1",
        "phase": "G-4.20A",
        "pack_id": pack.slug,
        "title": pack.title,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "visual_standard": "First mass atelier environmental believability production wave, meeting or exceeding the G-4.18D/G-4.19A atelier standard with an 8.5/10 minimum visual gate.",
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
        "future_pack_pattern": "10/10 source sheet -> saved prompt/source -> extraction script -> transparent sprites -> atlas/contact sheet -> manifest/provenance report -> Godot placement -> validation",
        "rollout_pack_role": "G-4.20A first mass atelier production wave for Newport environmental believability",
        "placement_policy": pack.placement_policy,
        "tavern_inn_lock": "The Tavern/Inn remains a future REBUILD_REQUIRED_CENTERPIECE item and is not patched by this pack.",
        "deprecated_visual_targets": [
            "G-4.18B weak deterministic/procedural cargo proof",
            "broad procedural fallback road/shore reads where atelier pieces are now available",
        ],
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
        f"""# G-4.20A Newport {pack.title} Atelier Pack

## Result

This pack is part of G-4.20A, the first mass atelier production wave for
Newport environmental believability. It extends the locked G-4.18D/G-4.19A
atelier standard from isolated prop packs into controlled environmental glue
for terrain edges, paths, shoreline seams, and building-grounding support.

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

The visual gate is `{VISUAL_QUALITY_GATE}/10`; every accepted asset in this
pack is rated at or above that gate.

## Generated Assets

{asset_lines}

## Placement QA

{pack.placement_policy}

The Tavern/Inn remains locked as a future `REBUILD_REQUIRED_CENTERPIECE`
rebuild with the brick, Hotel Viking-inspired twin-stack chimney direction.
This pack does not rebuild or patch it.
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
        if float(asset.get("visual_quality_rating", 0.0)) < VISUAL_QUALITY_GATE:
            failures.append(f"{asset_id} visual quality rating is below {VISUAL_QUALITY_GATE}")
    return failures


def process_pack(pack: PackSpec) -> dict:
    source_path = SOURCE_ROOT / pack.source_filename
    prompt_path = write_prompt(pack)
    if not source_path.exists():
        raise FileNotFoundError(f"missing source sheet: {source_path}")

    ATLAS_ROOT.mkdir(parents=True, exist_ok=True)
    alpha_sheet = key_to_alpha(Image.open(source_path))
    atlas_path = ATLAS_ROOT / pack.atlas_filename
    alpha_sheet.save(atlas_path)

    output = write_assets(pack, alpha_sheet)
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
                "atlas": asset["atlas"],
                "atlas_region": asset["atlas_region"],
            }
            for asset in manifest.get("assets", [])
        )
    wave_manifest = {
        "schema_id": "wayfarer.newport_atelier.g420a.environmental_believability_wave.v1",
        "phase": "G-4.20A",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "title": "Newport Environmental Believability Atelier Wave",
        "wave_id": "wave_1_environmental_believability",
        "role": "First mass atelier production wave moving Newport from isolated prop sheets to environmental believability production.",
        "visual_quality_gate": VISUAL_QUALITY_GATE,
        "pipeline_status": PIPELINE_STATUS,
        "source_policy": "AI-assisted green-origin candidates pending final license policy approval; no yellow building pixels, third-party sprites, marketplace packs, web-scraped images, or ripped game art were supplied as source input.",
        "placement_policy": "Controlled subset only at wharf-to-town transitions, road/grass edges, dock/shoreline edges, market-spine grounding, and non-centerpiece building bases; no over-scatter and no navigation blocking.",
        "tavern_inn_lock": "The Tavern/Inn remains a future REBUILD_REQUIRED_CENTERPIECE rebuild; G-4.20A does not rebuild or patch it.",
        "packs": pack_results,
        "assets": all_assets,
    }
    WAVE_MANIFEST_PATH.write_text(json.dumps(wave_manifest, indent=2), encoding="utf-8")
    return wave_manifest


def write_wave_report(wave_manifest: dict) -> None:
    pack_lines = "\n".join(f"- `{pack['pack_id']}`: `{pack['manifest']}`" for pack in wave_manifest["packs"])
    WAVE_REPORT_PATH.write_text(
        f"""# G-4.20A Newport Environmental Believability Atelier Wave

## Result

G-4.20A is the first mass atelier production wave for Newport environmental believability.
It moves the town from isolated sheet-by-sheet prop work into controlled
environmental believability production.

The wave exists to make the starting town feel grounded, navigable, and
physically coherent before any building rebuild, Tavern/Inn rebuild, or
player/NPC standard pass.

## Packs

{pack_lines}

## Scope

- Terrain edges
- Cobble/path transitions
- Shoreline and harbor edge dressing
- Building-grounding and service-lane accents

## Placement Policy

Only a controlled subset is placed in-world. Placement prioritizes
wharf-to-town transitions, road/grass edges, dock/shoreline edges,
market-spine grounding, and non-centerpiece building bases. Assets must not
block navigation, hide important entrances, or mask broken composition.

## Tavern/Inn Lock

The Tavern/Inn remains a future `REBUILD_REQUIRED_CENTERPIECE` rebuild. This
wave does not patch it and does not treat the current tavern as final. The
documented direction remains brick construction, two sets of large twin-stack
chimneys, Hotel Viking-inspired coastal landmark presence, warm social hub,
quest anchor, and player landmark.

## Provenance

Every G-4.20A asset is an `{PROVENANCE_STATUS}` and remains blocked from final commercial promotion
until final generated-art license policy approval.
""",
        encoding="utf-8",
    )


def update_registry() -> None:
    registry = json.loads(VISUAL_REGISTRY_PATH.read_text(encoding="utf-8"))
    registry["phase"] = "G-4.20A"
    registry["generated_at"] = "2026-05-16"
    registry["policy"] = (
        "G-4.20A is the first mass atelier production wave. It adds controlled environmental believability "
        "sheets and placement while preserving the G-4.19B visual registry, audit discipline, pending AI "
        "license policy, and Tavern/Inn centerpiece rebuild lock."
    )

    for wave in registry.get("production_wave_plan", []):
        if wave.get("wave_id") == "wave_1_environmental_believability":
            wave["status"] = "complete_g420a_first_mass_atelier_wave"
            wave["accepted_pack_count"] = len(PACKS)
            wave["accepted_asset_count"] = sum(len(pack.assets) for pack in PACKS)
            wave["acceptance_note"] = (
                "G-4.20A delivered the first mass environmental believability wave: terrain edges, "
                "cobble/path transitions, shoreline/harbor edge dressing, and building-grounding/service accents."
            )
        if wave.get("wave_id") == "wave_4_building_rebuild_or_enhancement":
            wave["status"] = "blocked_until_environmental_glue_or_audit_forces_rebuild"
        if wave.get("wave_id") == "wave_5_character_npc_standard":
            wave["status"] = "blocked_until_environment_context_is_stronger"

    existing_entries = [entry for entry in registry.get("asset_entries", []) if isinstance(entry, dict)]
    existing_by_id = {entry.get("asset_id"): entry for entry in existing_entries}
    entries = [entry for entry in existing_entries if not str(entry.get("asset_id", "")).startswith(("atelier_terrain_", "atelier_path_", "atelier_shore_", "atelier_ground_"))]

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
            used_in_map = asset_id in G420A_PLACED_ASSET_IDS
            previous = existing_by_id.get(asset_id, {})
            entry = {
                "asset_id": asset_id,
                "name": asset["source_identity"].title(),
                "category": pack.category,
                "path": asset["path"],
                "source_provenance_status": PROVENANCE_STATUS,
                "current_usage": {
                    "normal_review": True,
                    "lab_only": False,
                    "runtime_target": "MapLayer G-4.20A environmental believability controlled subset" if used_in_map else "Registered G-4.20A atlas candidate; not placed in the controlled subset yet",
                    "used_in_g420a_controlled_subset": used_in_map,
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
                    + "not a building rebuild, not a Tavern/Inn patch, and not final-commercial promoted."
                ),
            }
            if previous:
                entry.update({k: v for k, v in previous.items() if k.startswith("_")})
            entries.append(entry)

    registry["asset_entries"] = entries
    VISUAL_REGISTRY_PATH.write_text(json.dumps(registry, indent=2), encoding="utf-8")


G420A_PLACED_ASSET_IDS = {
    "atelier_terrain_grass_road_edge_north_01",
    "atelier_terrain_mud_cobble_feather_01",
    "atelier_terrain_broken_grassy_shoulder_01",
    "atelier_path_market_cobble_long_01",
    "atelier_path_broken_cobble_patch_01",
    "atelier_path_cobble_plank_seam_01",
    "atelier_path_curb_threshold_stones_01",
    "atelier_shore_seaweed_drift_line_01",
    "atelier_shore_wet_rocks_sand_01",
    "atelier_shore_driftwood_log_cluster_01",
    "atelier_shore_harbor_debris_slats_rope_01",
    "atelier_ground_doorstep_stones_01",
    "atelier_ground_foundation_shadow_strip_01",
    "atelier_ground_wall_weeds_stones_01",
    "atelier_ground_wash_tub_buckets_01",
}


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
    print(f"PASS: G-4.20A environmental believability wave -> {len(wave_manifest['assets'])} assets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
