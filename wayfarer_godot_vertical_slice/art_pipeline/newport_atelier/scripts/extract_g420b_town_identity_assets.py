#!/usr/bin/env python3
"""Extract G-4.20B Newport town identity atelier sprites."""

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
VISUAL_QUALITY_GATE = atelier.VISUAL_QUALITY_GATE
PIPELINE_STATUS = atelier.PIPELINE_STATUS
PROVENANCE_STATUS = atelier.PROVENANCE_STATUS
COMMERCIAL_STATUS = atelier.COMMERCIAL_STATUS

WAVE_MANIFEST_PATH = MANIFEST_ROOT / "newport_atelier_town_identity_manifest.json"
WAVE_REPORT_PATH = REPORT_ROOT / "G420B_NEWPORT_TOWN_IDENTITY_ATELIER_WAVE.md"
MAPLAYER_REGION_REPORT_PATH = MANIFEST_ROOT / "newport_atelier_town_identity_maplayer_regions.json"


def rel(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def sha256(path: Path) -> str:
    return atelier.sha256(path)


PACKS: tuple[PackSpec, ...] = (
    PackSpec(
        slug="sign_shop_markers",
        title="Signs And Shop Markers",
        category="TOWN_IDENTITY_SIGNAGE",
        source_filename="g420b_sign_shop_markers_sheet_imagegen.png",
        prompt_filename="g420b_sign_shop_markers_prompt.txt",
        atlas_filename="newport_atelier_sign_shop_markers_v1.png",
        contact_filename="newport_atelier_sign_shop_markers_contact_sheet.png",
        manifest_filename="newport_atelier_sign_shop_markers_manifest.json",
        qa_filename="newport_atelier_sign_shop_markers_extraction_qa.json",
        report_filename="G420B_SIGN_SHOP_MARKERS_ATELIER_PACK.md",
        placement_policy="Controlled market-spine and harbor-facing shop identity placement only; no readable text, no over-decoration, no navigation blocking, and no Tavern/Inn building finalization.",
        prompt="""Use case: stylized-concept
Asset type: production 2D game sprite sheet, original legally clean asset concept for a fantasy 1700s Newport harbor RPG
Primary request: Create a polished sprite sheet containing exactly eight separate original Newport town identity sign and shop marker assets: 1) temporary tavern/inn hanging sign placeholder with warm social-hub icon but no readable lettering, 2) mercantile hanging sign with small parcel/crate icon, 3) fishmonger sign with simple fish silhouette icon, 4) dock warehouse sign with barrel/anchor mark, 5) inn rooms small board with key/bed icon, 6) harbor directional arrow sign cluster with blank arrows, 7) ornate iron hanging sign bracket, 8) small painted shop plaque board. These must look like high-end hand-painted pixel art game sprites suitable beside detailed colonial Newport harbor buildings and the accepted G-4.18D/G-4.19A/G-4.20A atelier sprites.
Scene/backdrop: perfectly flat solid #ff00ff chroma-key background only, no floor plane, no scenery, no gradients, no texture, no cast shadow outside the assets. Add only tiny neutral contact shadows directly inside the assets if needed, using dark neutral pixels that do not blend into the chroma key.
Subject: signage and shop markers for Newport coastal fantasy identity and wayfinding. No full buildings, no people, no NPC/player standards, no readable text labels, no finalized Tavern/Inn building design.
Style/medium: refined hand-painted pixel art / painterly pixel sprite, 3/4 top-down RPG angle, crisp readable silhouettes, authored detail density, readable at game scale, dark painterly contour pixels, warm sparse highlights, weathered painted wood, wrought iron, brass nailheads, muted coastal reds, ochres, sea greens, navy, off-white accents.
Composition/framing: one clean wide sprite sheet with exactly eight assets separated into very generous padded areas, each fully visible, no overlap between separate assets. Arrange in a tidy 2 columns by 4 rows grid. Make every asset smaller than its cell, centered in its cell, and leave at least 110 pixels of perfectly flat magenta around every asset and at every outer sheet edge for clean extraction. No part of any sign, bracket, chain, arrow, shadow, or nail may touch the image edge or cell edge. No text labels.
Materials/textures: weathered painted wood grain, chipped sign edges, wrought iron curls, brass or iron fasteners, muted coastal paint, subtle salt-air wear.
Constraints: original art only, no copied game sprites, no marketplace asset style, no logos, no real-world brands, no readable text, no UI, no photorealism, no 3D render look, no flat vector icons, no blurry concept-art brushwork, no characters, no boats, no buildings.
Avoid: generic medieval filler, saturated fantasy colors, modern street signs, plastic, readable letters, watermarks, background texture, assets touching the edge of the sheet.""",
        assets=(
            AssetSpec("atelier_sign_tavern_inn_placeholder_01", "temporary_tavern_inn_hanging_sign", "temporary tavern/inn hanging sign placeholder", "Supplies a future-ready inn/tavern sign candidate without finalizing the current Tavern/Inn building.", 0.92, 0.15, 9.1, "Warm social-hub sign candidate; registered only until the future centerpiece rebuild."),
            AssetSpec("atelier_sign_mercantile_crate_marker_01", "mercantile_hanging_sign", "mercantile hanging sign with parcel icon", "Improves mercantile readability along the market spine.", 0.92, 0.15, 9.1, "Weathered green painted shop sign with parcel icon."),
            AssetSpec("atelier_sign_fishmonger_icon_board_01", "fishmonger_hanging_sign", "fishmonger sign with fish icon", "Marks the west fishmonger/harbor market identity without creating a building rebuild.", 0.92, 0.15, 9.0, "Blue fish sign with crisp coastal silhouette."),
            AssetSpec("atelier_sign_dock_warehouse_barrel_anchor_01", "dock_warehouse_sign", "dock warehouse sign with barrel and anchor", "Clarifies working-wharf storage identity.", 0.92, 0.14, 9.1, "Round warehouse marker with barrel and anchor icon."),
            AssetSpec("atelier_sign_inn_rooms_key_board_01", "inn_rooms_small_board", "inn rooms small key and bed board", "Registered inn identity candidate for future non-final use.", 0.92, 0.14, 8.9, "Key and bed board; not placed on the current Tavern/Inn."),
            AssetSpec("atelier_sign_harbor_direction_arrows_01", "harbor_direction_arrow_signpost", "blank harbor directional arrow sign cluster", "Supports wharf-to-town orientation and route readability.", 0.94, 0.16, 9.0, "Blank painted arrows for player orientation."),
            AssetSpec("atelier_sign_hanging_bracket_iron_01", "ornate_iron_hanging_sign_bracket", "ornate iron hanging sign bracket", "Adds reusable sign-support grammar to shopfronts.", 0.92, 0.13, 8.9, "Wrought iron bracket candidate for controlled shopfront support."),
            AssetSpec("atelier_sign_painted_shop_plaque_01", "painted_shop_plaque_board", "small painted shop plaque board", "Adds compact shopfront identity without noisy text.", 0.92, 0.14, 8.9, "Red coastal plaque with ship icon and chipped paint."),
        ),
    ),
    PackSpec(
        slug="lamps_wayfinding",
        title="Lamps Posts And Wayfinding",
        category="TOWN_IDENTITY_WAYFINDING",
        source_filename="g420b_lamps_wayfinding_sheet_imagegen.png",
        prompt_filename="g420b_lamps_wayfinding_prompt.txt",
        atlas_filename="newport_atelier_lamps_wayfinding_v1.png",
        contact_filename="newport_atelier_lamps_wayfinding_contact_sheet.png",
        manifest_filename="newport_atelier_lamps_wayfinding_manifest.json",
        qa_filename="newport_atelier_lamps_wayfinding_extraction_qa.json",
        report_filename="G420B_LAMPS_WAYFINDING_ATELIER_PACK.md",
        placement_policy="Controlled wayfinding placement at market-spine, wharf, and civic approach points only; keep route tiles clear and avoid visual noise.",
        prompt="""Use case: stylized-concept
Asset type: production 2D game sprite sheet, original legally clean asset concept for a fantasy 1700s Newport harbor RPG
Primary request: Create a polished sprite sheet containing exactly eight separate original Newport lamps, posts, and wayfinding assets: 1) colonial street lamp post with warm lantern, 2) dock lantern post with rope wrap, 3) blank multi-arrow signpost, 4) bollard-mounted lantern, 5) harbor road marker stone with simple arrow icon and no letters, 6) rope-rail post pair accent, 7) short pier lantern on crate-height stand, 8) small coastal mile marker/waystone with shell/anchor icon but no readable letters. These must look like high-end hand-painted pixel art game sprites suitable beside detailed colonial Newport harbor buildings and the accepted G-4.18D/G-4.19A/G-4.20A atelier sprites.
Scene/backdrop: perfectly flat solid #ff00ff chroma-key background only, no floor plane, no scenery, no gradients, no texture, no cast shadow outside the assets. Add only tiny neutral contact shadows directly inside the assets if needed, using dark neutral pixels that do not blend into the chroma key.
Subject: lamps, posts, and wayfinding markers for Newport coastal fantasy identity and player orientation. No full buildings, no people, no NPC/player standards, no readable text labels.
Style/medium: refined hand-painted pixel art / painterly pixel sprite, 3/4 top-down RPG angle, crisp readable silhouettes, authored detail density, readable at game scale, dark painterly contour pixels, warm lantern glow contained within glass, muted brass, wrought iron, weathered wood, salt-worn rope, grey harbor stone.
Composition/framing: one clean wide sprite sheet with exactly eight assets separated into very generous padded areas, each fully visible, no overlap between separate assets. Arrange in a tidy 2 columns by 4 rows grid. Make every asset smaller than its cell, centered in its cell, and leave at least 110 pixels of perfectly flat magenta around every asset and at every outer sheet edge for clean extraction. No part of any post, lantern, rope, arrow, shadow, or marker may touch the image edge or cell edge. No text labels.
Materials/textures: wrought iron, smoky glass, brass caps, weathered wood posts, rope lashings, chipped coastal stone, warm candle-lit lantern panes.
Constraints: original art only, no copied game sprites, no marketplace asset style, no logos, no real-world brands, no readable text, no UI, no photorealism, no 3D render look, no flat vector icons, no blurry concept-art brushwork, no characters, no boats, no buildings.
Avoid: generic medieval filler, saturated fantasy colors, modern lamp posts, electric fixtures, plastic, readable letters, watermarks, background texture, assets touching the edge of the sheet.""",
        assets=(
            AssetSpec("atelier_wayfinding_street_lamp_post_01", "colonial_street_lamp_post", "colonial street lamp post", "Frames the market spine and civic approach as intentional town space.", 0.98, 0.14, 9.2, "Tall black iron lamp with contained warm glass glow."),
            AssetSpec("atelier_wayfinding_dock_lantern_post_01", "dock_lantern_post", "dock lantern post with rope wrap", "Marks harbor routes with working-wharf lighting.", 0.98, 0.15, 9.1, "Rope-wrapped post with suspended lantern."),
            AssetSpec("atelier_wayfinding_multi_arrow_signpost_01", "blank_multi_arrow_signpost", "blank multi-arrow signpost", "Improves player orientation at wharf-to-town splits without readable text.", 0.98, 0.16, 9.0, "Weathered directional signpost with blank arrows."),
            AssetSpec("atelier_wayfinding_bollard_lantern_01", "bollard_mounted_lantern", "bollard-mounted lantern", "Adds a low harbor marker where full posts would be too tall.", 0.96, 0.13, 9.1, "Brass lantern mounted on a stout bollard."),
            AssetSpec("atelier_wayfinding_harbor_road_marker_01", "harbor_road_marker_stone", "harbor road marker stone with arrow icon", "Gives the market road a grounded coastal wayfinding accent.", 0.96, 0.13, 8.9, "Chipped stone marker with arrow pictogram."),
            AssetSpec("atelier_wayfinding_rope_rail_post_pair_01", "rope_rail_post_pair", "rope-rail post pair accent", "Defines dock edges without blocking movement.", 0.96, 0.15, 8.9, "Short rope rail with salt-worn posts."),
            AssetSpec("atelier_wayfinding_pier_lantern_stand_01", "short_pier_lantern_stand", "short pier lantern on crate-height stand", "Adds readable pier lighting at working-wharf scale.", 0.96, 0.13, 9.0, "Compact crate-height lantern stand."),
            AssetSpec("atelier_wayfinding_coastal_waystone_01", "coastal_waystone", "small coastal waystone with shell and anchor icon", "Registers coastal civic identity in quieter corners.", 0.96, 0.13, 8.9, "Shell and anchor waystone without letters."),
        ),
    ),
    PackSpec(
        slug="civic_market_identity",
        title="Civic And Market Identity",
        category="TOWN_IDENTITY_CIVIC_MARKET",
        source_filename="g420b_civic_market_identity_sheet_imagegen.png",
        prompt_filename="g420b_civic_market_identity_prompt.txt",
        atlas_filename="newport_atelier_civic_market_identity_v1.png",
        contact_filename="newport_atelier_civic_market_identity_contact_sheet.png",
        manifest_filename="newport_atelier_civic_market_identity_manifest.json",
        qa_filename="newport_atelier_civic_market_identity_extraction_qa.json",
        report_filename="G420B_CIVIC_MARKET_IDENTITY_ATELIER_PACK.md",
        placement_policy="Controlled civic green, market spine, and dock-rules placement only; all postings stay non-readable and routes remain clear.",
        prompt="""Use case: stylized-concept
Asset type: production 2D game sprite sheet, original legally clean asset concept for a fantasy 1700s Newport harbor RPG
Primary request: Create a polished sprite sheet containing exactly eight separate original Newport civic and market identity assets: 1) town notice board with blank parchment postings and no readable words, 2) market banner strand with muted coastal colors, 3) harbor bulletin board on posts with blank notices, 4) small civic flag cluster on short poles, 5) brass civic plaque on stone/wood backing with simple anchor/star icon and no text, 6) posting pole with tied notices and wax seals, 7) market stall hanging pennant sign with blank cloth panel, 8) dock rules board with simple pictogram marks but no readable letters. These must look like high-end hand-painted pixel art game sprites suitable beside detailed colonial Newport harbor buildings and the accepted G-4.18D/G-4.19A/G-4.20A atelier sprites.
Scene/backdrop: perfectly flat solid #ff00ff chroma-key background only, no floor plane, no scenery, no gradients, no texture, no cast shadow outside the assets. Add only tiny neutral contact shadows directly inside the assets if needed, using dark neutral pixels that do not blend into the chroma key.
Subject: civic identity, market identity, bulletin boards, banners, flags, plaques, posting poles, player orientation props. No full buildings, no people, no NPC/player standards, no readable text labels.
Style/medium: refined hand-painted pixel art / painterly pixel sprite, 3/4 top-down RPG angle, crisp readable silhouettes, authored detail density, readable at game scale, dark painterly contour pixels, warm sparse highlights, muted coastal red, navy, ochre, faded cream, sea green, weathered cedar, brass, parchment.
Composition/framing: one clean wide sprite sheet with exactly eight assets separated into very generous padded areas, each fully visible, no overlap between separate assets. Arrange in a tidy 2 columns by 4 rows grid. Make every asset smaller than its cell, centered in its cell, and leave at least 110 pixels of perfectly flat magenta around every asset and at every outer sheet edge for clean extraction. No part of any board, banner, flag, parchment, pole, shadow, or rope may touch the image edge or cell edge. No text labels.
Materials/textures: weathered boards, tacked blank parchment, cloth banners, brass plaque, rope ties, wax seals, salt-air fading, small nails and iron brackets.
Constraints: original art only, no copied game sprites, no marketplace asset style, no logos, no real-world brands, no readable text, no UI, no photorealism, no 3D render look, no flat vector icons, no blurry concept-art brushwork, no characters, no boats, no buildings.
Avoid: generic medieval tournament props, saturated fantasy colors, modern bulletin boards, plastic, readable letters, watermarks, background texture, assets touching the edge of the sheet.""",
        assets=(
            AssetSpec("atelier_civic_town_notice_board_01", "town_notice_board", "town notice board with blank postings", "Gives the civic green a playable public-information landmark.", 0.96, 0.17, 9.1, "Large blank notice board with weathered wood and parchment."),
            AssetSpec("atelier_civic_market_banner_strand_01", "market_banner_strand", "market banner strand", "Adds controlled market color without crowding the street.", 0.72, 0.18, 8.9, "Muted coastal banner strand for market-spine identity."),
            AssetSpec("atelier_civic_harbor_bulletin_board_01", "harbor_bulletin_board", "harbor bulletin board with blank notices", "Marks the working harbor notice point.", 0.96, 0.18, 9.0, "Wide harbor bulletin board with nautical trim."),
            AssetSpec("atelier_civic_flag_cluster_01", "small_civic_flag_cluster", "small civic flag cluster", "Adds civic identity at the custom-house approach.", 0.96, 0.14, 8.9, "Short flag cluster with muted civic colors."),
            AssetSpec("atelier_civic_anchor_plaque_01", "anchor_civic_plaque", "brass civic plaque with anchor star icon", "Supplies a civic marker candidate for future formal building support.", 0.92, 0.14, 9.0, "Brass anchor plaque on painted wood backing."),
            AssetSpec("atelier_civic_posting_pole_01", "posting_pole_with_notices", "posting pole with tied notices and wax seals", "Adds readable public posting detail near market/civic paths.", 0.96, 0.13, 8.9, "Compact posting pole with blank notices."),
            AssetSpec("atelier_civic_market_pennant_sign_01", "market_pennant_sign", "market stall hanging pennant sign", "Adds reusable market identity without text labels.", 0.88, 0.16, 8.8, "Blank cloth pennant sign for market support."),
            AssetSpec("atelier_civic_dock_rules_board_01", "dock_rules_pictogram_board", "dock rules board with simple pictogram marks", "Clarifies harbor rules visually without readable text.", 0.96, 0.16, 9.0, "Pictogram dock board with no letters."),
        ),
    ),
    PackSpec(
        slug="shopfront_support_accents",
        title="Shopfront Support And Town-Color Accents",
        category="TOWN_IDENTITY_SHOPFRONT_SUPPORT",
        source_filename="g420b_shopfront_support_accents_sheet_imagegen.png",
        prompt_filename="g420b_shopfront_support_accents_prompt.txt",
        atlas_filename="newport_atelier_shopfront_support_accents_v1.png",
        contact_filename="newport_atelier_shopfront_support_accents_contact_sheet.png",
        manifest_filename="newport_atelier_shopfront_support_accents_manifest.json",
        qa_filename="newport_atelier_shopfront_support_accents_extraction_qa.json",
        report_filename="G420B_SHOPFRONT_SUPPORT_ACCENTS_ATELIER_PACK.md",
        placement_policy="Controlled shopfront and market support placement only; keep entrances readable, avoid clutter scatter, and do not use these props to treat unverified buildings as final.",
        prompt="""Use case: stylized-concept
Asset type: production 2D game sprite sheet, original legally clean asset concept for a fantasy 1700s Newport harbor RPG
Primary request: Create a polished sprite sheet containing exactly eight separate original Newport shopfront support and town-color accent assets: 1) small folded canvas awning segment, 2) display crate stack with blank price slate and cloth bundles, 3) folded cloth merchant table bundle without table legs, 4) portable merchant board/chalk slate with no readable text, 5) hanging flower basket/window-box accent, 6) small coastal planter with herbs and weathered wood, 7) rope rail accent with painted pennant ties, 8) compact shopfront basket-and-parcel display cluster. These must look like high-end hand-painted pixel art game sprites suitable beside detailed colonial Newport harbor buildings and the accepted G-4.18D/G-4.19A/G-4.20A atelier sprites.
Scene/backdrop: perfectly flat solid #ff00ff chroma-key background only, no floor plane, no scenery, no gradients, no texture, no cast shadow outside the assets. Add only tiny neutral contact shadows directly inside the assets if needed, using dark neutral pixels that do not blend into the chroma key.
Subject: shopfront support props and subtle coastal town-color accents for Newport market identity and navigation. No full buildings, no people, no NPC/player standards, no readable text labels, no finalized Tavern/Inn building design.
Style/medium: refined hand-painted pixel art / painterly pixel sprite, 3/4 top-down RPG angle, crisp readable silhouettes, authored detail density, readable at game scale, dark painterly contour pixels, warm sparse highlights, faded canvas, painted wood, woven baskets, folded cloth, herbs, rope, muted coastal reds, ochres, sea greens, navy, cream.
Composition/framing: one clean wide sprite sheet with exactly eight assets separated into very generous padded areas, each fully visible, no overlap between separate assets. Arrange in a tidy 2 columns by 4 rows grid. Make every asset smaller than its cell, centered in its cell, and leave at least 110 pixels of perfectly flat magenta around every asset and at every outer sheet edge for clean extraction. No part of any awning, crate, basket, board, rope, shadow, or planter may touch the image edge or cell edge. No text labels.
Materials/textures: faded canvas, chipped painted boards, woven reed baskets, folded cloth, chalky slate with abstract smudges only, herbs and coastal flowers, rope knots, small brass/iron fittings.
Constraints: original art only, no copied game sprites, no marketplace asset style, no logos, no real-world brands, no readable text, no UI, no photorealism, no 3D render look, no flat vector icons, no blurry concept-art brushwork, no characters, no boats, no buildings.
Avoid: generic medieval filler, saturated fantasy colors, modern retail props, plastic, readable letters, watermarks, background texture, assets touching the edge of the sheet.""",
        assets=(
            AssetSpec("atelier_shopfront_canvas_awning_segment_01", "folded_canvas_awning_segment", "small folded canvas awning segment", "Adds controlled shopfront color without a building rebuild.", 0.80, 0.18, 9.0, "Red cream and blue folded awning segment."),
            AssetSpec("atelier_shopfront_display_crates_slate_01", "display_crate_stack_with_slate", "display crate stack with blank slate and cloth bundles", "Supports market-spine shopfront believability while keeping doorways clear.", 0.96, 0.17, 9.1, "Display crates with cloth and blank chalk slate."),
            AssetSpec("atelier_shopfront_folded_cloth_bundle_01", "folded_cloth_bundle", "folded cloth merchant bundle", "Adds merchant material texture at market frontage.", 0.92, 0.15, 8.9, "Roped folded cloth stack with coastal colors."),
            AssetSpec("atelier_shopfront_chalk_slate_board_01", "portable_blank_chalk_slate", "portable merchant chalk slate", "Adds shopfront identity without readable lettering.", 0.96, 0.13, 8.9, "Blank portable slate board."),
            AssetSpec("atelier_shopfront_hanging_basket_01", "hanging_basket_window_box", "hanging flower basket/window-box accent", "Adds memory and warmth to non-centerpiece shopfronts.", 0.92, 0.15, 9.0, "Flower basket with strong silhouette and warm color."),
            AssetSpec("atelier_shopfront_coastal_planter_01", "coastal_herb_planter", "small coastal planter with herbs", "Adds grounded town-color near civic and shop edges.", 0.92, 0.15, 9.0, "Weathered herb planter with sea-green boards."),
            AssetSpec("atelier_shopfront_rope_pennant_rail_01", "rope_rail_pennant_accent", "rope rail accent with painted pennant ties", "Defines market edges and wharf approach without hard blocking.", 0.92, 0.18, 8.9, "Low rope rail with muted pennants."),
            AssetSpec("atelier_shopfront_basket_parcel_display_01", "basket_parcel_display_cluster", "compact shopfront basket and parcel display cluster", "Adds compact market goods to shopfront support areas.", 0.96, 0.17, 9.1, "Basket, parcel, and fabric display cluster."),
        ),
    ),
)


G420B_PLACED_ASSET_IDS = {
    "atelier_sign_mercantile_crate_marker_01",
    "atelier_sign_fishmonger_icon_board_01",
    "atelier_sign_dock_warehouse_barrel_anchor_01",
    "atelier_sign_harbor_direction_arrows_01",
    "atelier_sign_hanging_bracket_iron_01",
    "atelier_wayfinding_street_lamp_post_01",
    "atelier_wayfinding_dock_lantern_post_01",
    "atelier_wayfinding_multi_arrow_signpost_01",
    "atelier_wayfinding_bollard_lantern_01",
    "atelier_wayfinding_harbor_road_marker_01",
    "atelier_wayfinding_pier_lantern_stand_01",
    "atelier_civic_town_notice_board_01",
    "atelier_civic_market_banner_strand_01",
    "atelier_civic_flag_cluster_01",
    "atelier_civic_posting_pole_01",
    "atelier_civic_dock_rules_board_01",
    "atelier_shopfront_display_crates_slate_01",
    "atelier_shopfront_chalk_slate_board_01",
    "atelier_shopfront_hanging_basket_01",
    "atelier_shopfront_rope_pennant_rail_01",
}

CROP_REGION_ADJUSTMENTS = {
    "atelier_sign_dock_warehouse_barrel_anchor_01": {"bottom": -28},
    "atelier_sign_harbor_direction_arrows_01": {"top": 26},
}


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
            "expected_contact": "town identity sprite draws from its transparent bounds; destination bottom is the intended grounding line",
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
            {"type": "ai_generated_source_image", "path": rel(source_path), "source_pixels_used": True, "commercial_status": COMMERCIAL_STATUS},
            {"type": "project_prompt", "path": rel(prompt_path), "source_pixels_used": False, "commercial_status": "green_origin_candidate"},
            {"type": "project_style_rules", "path": rel(ART_BIBLE_PATH), "source_pixels_used": False, "commercial_status": "documentation_only"},
            {"type": "locked_atelier_standard", "path": rel(G418D_STANDARD_REPORT_PATH), "source_pixels_used": False, "commercial_status": "documentation_only"},
            {"type": "prior_atelier_rollout_reference", "path": rel(G419A_REPORT_PATH), "source_pixels_used": False, "commercial_status": "documentation_only"},
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


def write_qa_report(pack: PackSpec, qa: dict[str, dict]) -> Path:
    path = REPORT_ROOT / pack.qa_filename
    status = "PASS" if all(details.get("status") == "PASS" for details in qa.values()) else "FAIL"
    path.write_text(
        json.dumps(
            {
                "schema_id": "wayfarer.newport_atelier.extraction_qa.v1",
                "phase": "G-4.20B",
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
                    "temporary Tavern/Inn sign candidate is not placed as a final building patch",
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


def dominant_component_bbox(image: Image.Image) -> tuple[int, int, int, int] | None:
    alpha = image.getchannel("A")
    pixels = alpha.load()
    width = alpha.width
    height = alpha.height
    visited = bytearray(width * height)
    components: list[dict] = []
    for y in range(height):
        for x in range(width):
            idx = y * width + x
            if visited[idx] or pixels[x, y] <= 8:
                continue
            stack = [idx]
            visited[idx] = 1
            component: list[int] = []
            while stack:
                current = stack.pop()
                component.append(current)
                cx = current % width
                cy = current // width
                for ny in range(max(0, cy - 1), min(height, cy + 2)):
                    for nx in range(max(0, cx - 1), min(width, cx + 2)):
                        next_idx = ny * width + nx
                        if visited[next_idx] or pixels[nx, ny] <= 8:
                            continue
                        visited[next_idx] = 1
                        stack.append(next_idx)
            xs = [index % width for index in component]
            ys = [index // width for index in component]
            components.append(
                {
                    "pixels": component,
                    "area": len(component),
                    "bbox": (min(xs), min(ys), max(xs) + 1, max(ys) + 1),
                    "center_y": (min(ys) + max(ys) + 1) * 0.5,
                }
            )
    if not components:
        return None

    largest_component = max(components, key=lambda component: component["area"])
    largest = int(largest_component["area"])
    keep_threshold = max(600, int(largest * 0.03))
    center_y = float(largest_component["center_y"])
    vertical_window = max(48.0, height * 0.32)
    kept = [
        index
        for component in components
        if int(component["area"]) >= keep_threshold and abs(float(component["center_y"]) - center_y) <= vertical_window
        for index in component["pixels"]
    ]
    if not kept:
        kept = largest_component["pixels"]
    xs = [index % width for index in kept]
    ys = [index // width for index in kept]
    return (min(xs), min(ys), max(xs) + 1, max(ys) + 1)


def source_region_for_fixed_cell(alpha_sheet: Image.Image, index: int, padding: int = 18) -> tuple[int, int, int, int]:
    cell_w = alpha_sheet.width // 2
    cell_h = alpha_sheet.height // 4
    col = index % 2
    row = index // 2
    cell_x0 = col * cell_w
    cell_y0 = row * cell_h
    cell_x1 = alpha_sheet.width if col == 1 else cell_x0 + cell_w
    cell_y1 = alpha_sheet.height if row == 3 else cell_y0 + cell_h
    cell = alpha_sheet.crop((cell_x0, cell_y0, cell_x1, cell_y1))
    bbox = dominant_component_bbox(cell)
    if bbox is None:
        return (cell_x0, cell_y0, cell_x1, cell_y1)
    return (
        max(cell_x0, cell_x0 + bbox[0] - padding),
        max(cell_y0, cell_y0 + bbox[1] - padding),
        min(cell_x1, cell_x0 + bbox[2] + padding),
        min(cell_y1, cell_y0 + bbox[3] + padding),
    )


def source_regions_by_component(alpha_sheet: Image.Image, padding: int = 18) -> list[tuple[int, int, int, int]]:
    alpha = alpha_sheet.getchannel("A")
    pixels = alpha.load()
    width = alpha.width
    height = alpha.height
    visited = bytearray(width * height)
    components: list[dict] = []
    for y in range(height):
        for x in range(width):
            idx = y * width + x
            if visited[idx] or pixels[x, y] <= 8:
                continue
            stack = [idx]
            visited[idx] = 1
            component: list[int] = []
            while stack:
                current = stack.pop()
                component.append(current)
                cx = current % width
                cy = current // width
                for ny in range(max(0, cy - 1), min(height, cy + 2)):
                    for nx in range(max(0, cx - 1), min(width, cx + 2)):
                        next_idx = ny * width + nx
                        if visited[next_idx] or pixels[nx, ny] <= 8:
                            continue
                        visited[next_idx] = 1
                        stack.append(next_idx)
            if len(component) < 50:
                continue
            xs = [index % width for index in component]
            ys = [index // width for index in component]
            bbox = (min(xs), min(ys), max(xs) + 1, max(ys) + 1)
            components.append(
                {
                    "area": len(component),
                    "bbox": bbox,
                    "center": VectorLike((bbox[0] + bbox[2]) * 0.5, (bbox[1] + bbox[3]) * 0.5),
                }
            )

    cell_w = width / 2.0
    cell_h = height / 4.0
    centers = [VectorLike((index % 2 + 0.5) * cell_w, (index // 2 + 0.5) * cell_h) for index in range(8)]
    by_cell: list[list[dict]] = [[] for _ in range(8)]
    for component in components:
        center: VectorLike = component["center"]
        nearest = min(range(8), key=lambda index: center.distance_squared_to(centers[index], cell_w, cell_h))
        by_cell[nearest].append(component)

    regions: list[tuple[int, int, int, int]] = []
    for index, cell_components in enumerate(by_cell):
        if not cell_components:
            regions.append(source_region_for_fixed_cell(alpha_sheet, index, padding))
            continue
        largest = max(int(component["area"]) for component in cell_components)
        keep_threshold = max(200, int(largest * 0.02))
        kept = [component for component in cell_components if int(component["area"]) >= keep_threshold]
        x0 = min(int(component["bbox"][0]) for component in kept)
        y0 = min(int(component["bbox"][1]) for component in kept)
        x1 = max(int(component["bbox"][2]) for component in kept)
        y1 = max(int(component["bbox"][3]) for component in kept)
        regions.append((max(0, x0 - padding), max(0, y0 - padding), min(width, x1 + padding), min(height, y1 + padding)))
    return regions


class VectorLike:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def distance_squared_to(self, other: "VectorLike", x_scale: float, y_scale: float) -> float:
        dx = (self.x - other.x) / max(1.0, x_scale)
        dy = (self.y - other.y) / max(1.0, y_scale)
        return dx * dx + dy * dy


def write_assets(pack: PackSpec, alpha_sheet: Image.Image) -> dict[str, dict]:
    GENERATED_ROOT.mkdir(parents=True, exist_ok=True)
    output: dict[str, dict] = {}
    regions = source_regions_by_component(alpha_sheet)
    for index, asset in enumerate(pack.assets):
        region = regions[index]
        adjustment = CROP_REGION_ADJUSTMENTS.get(asset.asset_id, {})
        if adjustment:
            region = (
                region[0] + int(adjustment.get("left", 0)),
                region[1] + int(adjustment.get("top", 0)),
                region[2] + int(adjustment.get("right", 0)),
                region[3] + int(adjustment.get("bottom", 0)),
            )
        piece = alpha_sheet.crop(region)
        padded = Image.new(
            "RGBA",
            (piece.width + atelier.OUTPUT_SPRITE_PADDING * 2, piece.height + atelier.OUTPUT_SPRITE_PADDING * 2),
            (0, 0, 0, 0),
        )
        padded.alpha_composite(piece, (atelier.OUTPUT_SPRITE_PADDING, atelier.OUTPUT_SPRITE_PADDING))
        path = GENERATED_ROOT / f"{asset.asset_id}.png"
        padded.save(path)
        output[asset.asset_id] = {
            "path": path,
            "atlas_region": {"x": region[0], "y": region[1], "w": region[2] - region[0], "h": region[3] - region[1]},
            "sprite_size": {"w": padded.width, "h": padded.height},
            "source_cell": {"column": index % 2, "row": index // 2},
        }
    return output


def write_contact_sheet(pack: PackSpec, output: dict[str, dict]) -> Path:
    path = CONTACT_ROOT / pack.contact_filename
    card_w = 360
    card_h = 300
    margin_x = 40
    margin_y = 96
    gap_x = 56
    gap_y = 132
    sheet = Image.new("RGB", (880, 1840), "#20261e")
    draw = ImageDraw.Draw(sheet)
    label(draw, (24, 18), f"G-4.20B Newport {pack.title} Atelier Pack")
    label(draw, (24, 40), "Town identity wave: AI-assisted green-origin candidates, extracted sprites, controlled wayfinding placement.")
    for index, asset in enumerate(pack.assets):
        col = index % 2
        row = index // 2
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
    label(draw, (24, 1800), pack.placement_policy, "#c8d2ac")
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
        "schema_id": f"wayfarer.newport_atelier.g420b.{pack.slug}.manifest.v1",
        "phase": "G-4.20B",
        "pack_id": pack.slug,
        "title": pack.title,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "visual_standard": "Town Identity atelier wave meeting or exceeding the G-4.18D/G-4.19A/G-4.20A atelier standard with an 8.5/10 minimum visual gate.",
        "source_policy": "AI-assisted original art is allowed here only with recorded prompt/source image/extraction script and no yellow building pixels, third-party sprites, marketplace packs, or web-scraped images as source inputs.",
        "atlas": rel(atlas_path),
        "source_image": rel(source_path),
        "generation_prompt": rel(prompt_path),
        "generated_asset_root": rel(GENERATED_ROOT),
        "contact_sheet": rel(contact_path),
        "provenance_report": rel(report_path),
        "validation_report": rel(qa_path),
        "pipeline_status": PIPELINE_STATUS,
        "base_pipeline_standard": "G-4.18D Newport atelier cargo pipeline lock, G-4.19A dock clutter rollout pack, and G-4.20A environmental believability wave",
        "future_pack_pattern": "10/10 source sheet -> saved prompt/source -> extraction script -> transparent sprites -> atlas/contact sheet -> manifest/provenance report -> Godot placement -> validation",
        "rollout_pack_role": "G-4.20B town identity wave for Newport signage, lamps, wayfinding, civic/market markers, and shopfront support assets",
        "placement_policy": pack.placement_policy,
        "tavern_inn_lock": "The Tavern/Inn remains a future REBUILD_REQUIRED_CENTERPIECE item; temporary sign assets are allowed, but this pack does not rebuild, patch, or finalize the current Tavern/Inn building.",
        "deprecated_visual_targets": [
            "generic placeholder sign/lamp doodles where atelier identity pieces are now available",
            "any use of unproven building art as final visual targets",
        ],
        "assets": [manifest_entry(pack, asset, output, qa[asset.asset_id]) for asset in pack.assets],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def write_report(pack: PackSpec, manifest: dict) -> Path:
    path = REPORT_ROOT / pack.report_filename
    asset_lines = "\n".join(
        f"- `{asset['asset_id']}`: `{asset['asset_type']}`, rating `{asset['visual_quality_rating']}/10`, `{asset['commercial_use_status']}`"
        for asset in manifest["assets"]
    )
    path.write_text(
        f"""# G-4.20B Newport {pack.title} Atelier Pack

## Result

This pack is part of G-4.20B, the Newport Town Identity atelier wave. It adds
signage, lamps, wayfinding, civic markers, market identity, and shopfront support
assets that make the starting town more readable, memorable, and navigable.

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

No yellow Newport building pixels, third-party sprite sheets, marketplace assets,
web images, or ripped game art were supplied as source inputs.

## Classification

These assets are `{PROVENANCE_STATUS}`. They are review-eligible as original
AI-assisted candidates, but final commercial promotion remains blocked from final commercial promotion
until the project approves its final license policy for generated artwork.

The visual gate is `{VISUAL_QUALITY_GATE}/10`; every accepted asset in this
pack is rated at or above that gate.

## Generated Assets

{asset_lines}

## Placement QA

{pack.placement_policy}

The Tavern/Inn remains locked as a future `REBUILD_REQUIRED_CENTERPIECE`
rebuild with the brick, Hotel Viking-inspired twin-stack chimney direction.
This pack may contain a temporary sign candidate, but it does not rebuild,
patch, or finalize the current Tavern/Inn building.
""",
        encoding="utf-8",
    )
    return path


def process_pack(pack: PackSpec) -> dict:
    source_path = SOURCE_ROOT / pack.source_filename
    prompt_path = atelier.write_prompt(pack)
    if not source_path.exists():
        raise FileNotFoundError(f"missing source sheet: {source_path}")

    alpha_sheet = atelier.key_to_alpha(Image.open(source_path))
    atlas_path = ATLAS_ROOT / pack.atlas_filename
    alpha_sheet.save(atlas_path)
    output = write_assets(pack, alpha_sheet)
    qa = atelier.collect_qa(pack, output)
    qa_path = write_qa_report(pack, qa)
    contact_path = write_contact_sheet(pack, output)
    manifest = write_manifest(pack, output, qa)
    report_path = write_report(pack, manifest)
    failures = atelier.validate_pipeline(pack, manifest, qa)
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
        "schema_id": "wayfarer.newport_atelier.g420b.town_identity_wave.v1",
        "phase": "G-4.20B",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "title": "Newport Town Identity Atelier Wave",
        "wave_id": "wave_2_town_identity",
        "role": "Town Identity atelier wave adding signage, lamps, wayfinding, civic and market markers, and shopfront support assets.",
        "visual_quality_gate": VISUAL_QUALITY_GATE,
        "pipeline_status": PIPELINE_STATUS,
        "source_policy": "AI-assisted green-origin candidates pending final license policy approval; no yellow building pixels, third-party sprites, marketplace packs, web-scraped images, or ripped game art were supplied as source input.",
        "placement_policy": "Controlled subset only for market spine readability, harbor/wharf wayfinding, civic identity, shopfront believability, player orientation, and landmark memory; no over-decoration, no navigation blocking, no unreadable visual noise, and no finalization of unverified buildings.",
        "tavern_inn_lock": "The Tavern/Inn remains a future REBUILD_REQUIRED_CENTERPIECE rebuild; G-4.20B may create temporary sign assets but does not rebuild, patch, or finalize it.",
        "packs": pack_results,
        "assets": all_assets,
    }
    WAVE_MANIFEST_PATH.write_text(json.dumps(wave_manifest, indent=2), encoding="utf-8")
    return wave_manifest


def write_wave_report(wave_manifest: dict) -> None:
    pack_lines = "\n".join(f"- `{pack['pack_id']}`: `{pack['manifest']}`" for pack in wave_manifest["packs"])
    WAVE_REPORT_PATH.write_text(
        f"""# G-4.20B Newport Town Identity Atelier Wave

## Result

G-4.20B is the Town Identity atelier wave. It adds signage, lamps,
wayfinding, civic markers, market identity, and shopfront support assets to
support Newport as a believable playable starting town.

This wave follows G-4.20A, which moved Newport from isolated prop packs to
environmental believability production. G-4.20B builds on that foundation by
making the town easier to read, remember, and navigate without rebuilding core
buildings.

## Packs

{pack_lines}

## Scope

- Signs and shop markers
- Lamps, posts, and wayfinding
- Civic and market identity
- Shopfront support and town-color accents

## Placement Policy

Only a controlled subset is placed in-world. Placement prioritizes market
spine readability, harbor/wharf wayfinding, civic identity, shopfront
believability, player orientation, and landmark memory. Assets must not block
navigation, cover entrances, over-decorate the street, create unreadable sign
noise, or make any unverified building look final.

## Tavern/Inn Lock

The Tavern/Inn remains a future `REBUILD_REQUIRED_CENTERPIECE` rebuild. This
wave does not patch it and does not treat the current tavern as final. The
documented direction remains brick construction, two sets of large twin-stack
chimneys, Hotel Viking-inspired coastal landmark presence, warm social hub,
quest anchor, and player landmark.

## Provenance

Every G-4.20B asset is an `{PROVENANCE_STATUS}` and remains blocked from final commercial promotion
until final generated-art license policy approval.
""",
        encoding="utf-8",
    )


def update_registry() -> None:
    registry = json.loads(VISUAL_REGISTRY_PATH.read_text(encoding="utf-8"))
    registry["phase"] = "G-4.20B"
    registry["generated_at"] = "2026-05-16"
    registry["policy"] = (
        "G-4.20B is the Town Identity atelier wave. It adds controlled signage, lamps, wayfinding, "
        "civic/market markers, and shopfront support assets while preserving the G-4.20A environmental "
        "believability wave, pending AI license policy, and Tavern/Inn centerpiece rebuild lock."
    )

    for wave in registry.get("production_wave_plan", []):
        if wave.get("wave_id") == "wave_2_town_identity":
            wave["status"] = "complete_g420b_town_identity_atelier_wave"
            wave["accepted_pack_count"] = len(PACKS)
            wave["accepted_asset_count"] = sum(len(pack.assets) for pack in PACKS)
            wave["acceptance_note"] = (
                "G-4.20B delivered the Town Identity atelier wave: signs/shop markers, lamps/posts/wayfinding, "
                "civic/market identity, and shopfront support/town-color accents."
            )
        if wave.get("wave_id") == "wave_4_building_rebuild_or_enhancement":
            wave["status"] = "blocked_until_identity_and_environmental_glue_or_audit_forces_rebuild"
        if wave.get("wave_id") == "wave_5_character_npc_standard":
            wave["status"] = "blocked_until_town_identity_context_is_stronger"

    existing_entries = [entry for entry in registry.get("asset_entries", []) if isinstance(entry, dict)]
    existing_by_id = {entry.get("asset_id"): entry for entry in existing_entries}
    replaced_prefixes = ("atelier_sign_", "atelier_wayfinding_", "atelier_civic_", "atelier_shopfront_")
    entries = [entry for entry in existing_entries if not str(entry.get("asset_id", "")).startswith(replaced_prefixes)]

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
            used_in_map = asset_id in G420B_PLACED_ASSET_IDS
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
                    "runtime_target": "MapLayer G-4.20B town identity controlled subset" if used_in_map else "Registered G-4.20B atlas candidate; not placed in the controlled subset yet",
                    "used_in_g420b_controlled_subset": used_in_map,
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
                entry.update({k: v for k, v in previous.items() if str(k).startswith("_")})
            entries.append(entry)

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
    print(f"PASS: G-4.20B town identity wave -> {len(wave_manifest['assets'])} assets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
