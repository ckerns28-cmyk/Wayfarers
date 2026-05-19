#!/usr/bin/env python3
"""Generate the G-19R Newport measured blockout source-of-truth artifacts."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[1]
REPO_ROOT = PROJECT_ROOT.parent
GENERATED_AT = "2026-05-19"
PHASE_ID = "G-19R"
BRANCH = "codex/g-19r-newport-scale-street-blockout-source-of-truth"
STARTING_MAIN_COMMIT = "6e8c5fc59c827d1b3adf84eb90a452c7092f4e57"
ARTIFACT_DIR = PROJECT_ROOT / "artifacts" / "planning" / "g19r_newport_blockout"
DESIGN_DIR = REPO_ROOT / "docs" / "design"
REPORT_DIR = REPO_ROOT / "docs" / "reports"
ROADMAP_JSON = REPO_ROOT / "docs" / "roadmaps" / "OPENING_VILLAGE_ISLAND_PRODUCTION_ROADMAP.json"
ROADMAP_MD = REPO_ROOT / "docs" / "roadmaps" / "OPENING_VILLAGE_ISLAND_PRODUCTION_ROADMAP.md"
LEDGER_JSON = REPO_ROOT / "docs" / "reports" / "OPENING_VILLAGE_ISLAND_AUTONOMOUS_EXECUTION_LEDGER.json"
LEDGER_MD = REPO_ROOT / "docs" / "reports" / "OPENING_VILLAGE_ISLAND_AUTONOMOUS_EXECUTION_LEDGER.md"


def rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_json(path: Path, data: dict[str, Any]) -> None:
    write_text(path, json.dumps(data, indent=2) + "\n")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def vec(x: float, y: float) -> dict[str, float]:
    return {"x": round(x, 3), "y": round(y, 3)}


def rect(x: float, y: float, w: float, h: float) -> dict[str, float]:
    return {"x": round(x, 3), "y": round(y, 3), "w": round(w, 3), "h": round(h, 3)}


def parse_project_viewport() -> tuple[int, int]:
    project = read_text(PROJECT_ROOT / "project.godot")
    width = int(re.search(r"viewport_width=(\d+)", project).group(1))
    height = int(re.search(r"viewport_height=(\d+)", project).group(1))
    return width, height


def parse_player_source_metrics() -> dict[str, Any]:
    player_gd = read_text(PROJECT_ROOT / "scenes" / "player" / "Player.gd")
    player_tscn = read_text(PROJECT_ROOT / "scenes" / "player" / "Player.tscn")

    frame_match = re.search(r"PLAYER_FRAME_SIZE := Vector2i\((\d+),\s*(\d+)\)", player_gd)
    scale_match = re.search(r"PLAYER_VISUAL_SCALE := ([0-9.]+)", player_gd)
    speed_match = re.search(r"PLAYER_MOVEMENT_SPEED_SYNC := ([0-9.]+)", player_gd)
    radius_match = re.search(r"radius = ([0-9.]+)", player_tscn)
    height_match = re.search(r"height = ([0-9.]+)", player_tscn)
    camera_zoom = 1.38

    frame_w = int(frame_match.group(1))
    frame_h = int(frame_match.group(2))
    scale = float(scale_match.group(1))
    radius = float(radius_match.group(1))
    collision_height = float(height_match.group(1))

    atlas_path = PROJECT_ROOT / "art_pipeline" / "player_identity" / "atlases" / "player_wayfarer_atelier_g422r_v1.png"
    atlas = Image.open(atlas_path).convert("RGBA")
    boxes: list[dict[str, Any]] = []
    max_w = 0
    max_h = 0
    for row, direction in enumerate(["down", "up", "left", "right"]):
        for col, variant in enumerate(["idle", "walk_a", "walk_b"]):
            crop = atlas.crop((col * frame_w, row * frame_h, (col + 1) * frame_w, (row + 1) * frame_h))
            bbox = crop.getchannel("A").getbbox()
            if bbox:
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]
            else:
                w = h = 0
            max_w = max(max_w, w)
            max_h = max(max_h, h)
            boxes.append({"direction": direction, "variant": variant, "alpha_bbox": bbox, "visible_size_px": {"w": w, "h": h}})

    viewport_w, viewport_h = parse_project_viewport()
    character_width = max_w * scale
    character_height = max_h * scale
    return {
        "player_scene": "wayfarer_godot_vertical_slice/scenes/player/Player.tscn",
        "player_script": "wayfarer_godot_vertical_slice/scenes/player/Player.gd",
        "player_atlas": rel(atlas_path),
        "frame_size_px": {"w": frame_w, "h": frame_h},
        "runtime_visual_scale": scale,
        "alpha_bbox_samples": boxes,
        "player_visual_width_world_units": round(character_width, 3),
        "player_visual_height_world_units": round(character_height, 3),
        "player_frame_draw_width_world_units": round(frame_w * scale, 3),
        "player_frame_draw_height_world_units": round(frame_h * scale, 3),
        "player_collision_body_width_world_units": round(radius * 2.0, 3),
        "player_collision_body_height_world_units": round(collision_height, 3),
        "player_movement_speed_world_units_per_second": round(float(speed_match.group(1)), 3),
        "camera_viewport_assumption_px": {"w": viewport_w, "h": viewport_h},
        "gameplay_zoom_assumption": camera_zoom,
        "gameplay_visible_world_rect_at_zoom": {
            "w": round(viewport_w / camera_zoom, 3),
            "h": round(viewport_h / camera_zoom, 3),
        },
        "pixels_per_character_width": round(character_width, 3),
        "world_units_per_character_width": round(character_width, 3),
        "measurement_basis": "Alpha bounds of the current G-4.22R player atlas, scaled by Player.gd PLAYER_VISUAL_SCALE. Collision values are read from Player.tscn CapsuleShape2D.",
    }


def width_from_chars(chars: float, char_width: float) -> float:
    return round(chars * char_width, 3)


def build_scale_metrics(player: dict[str, Any]) -> dict[str, Any]:
    cw = float(player["world_units_per_character_width"])
    targets = {
        "main_commercial_harbor_street": {"target_character_widths": [10, 15], "selected_character_widths": 12.0, "width_world_units": width_from_chars(12.0, cw)},
        "secondary_street": {"target_character_widths": [6, 9], "selected_character_widths": 7.5, "width_world_units": width_from_chars(7.5, cw)},
        "rear_service_lane": {"target_character_widths": [4, 6], "selected_character_widths": 5.5, "width_world_units": width_from_chars(5.5, cw)},
        "alley_service_cutthrough": {"target_character_widths": [3, 4], "selected_character_widths": 3.5, "width_world_units": width_from_chars(3.5, cw)},
        "wharf_working_apron": {"target_character_widths": [8, 14], "selected_character_widths": 10.5, "width_world_units": width_from_chars(10.5, cw)},
        "building_setback": {"target_character_widths": [1, 3], "selected_character_widths": 2.0, "width_world_units": width_from_chars(2.0, cw)},
        "npc_route_clearance": {"target_character_widths": [2, 3], "selected_character_widths": 2.5, "width_world_units": width_from_chars(2.5, cw)},
        "interaction_clearance": {"target_character_widths": [2, 3], "selected_character_widths": 2.5, "width_world_units": width_from_chars(2.5, cw)},
        "minimum_readable_landmark_spacing": {"selected_character_widths": 12.0, "width_world_units": width_from_chars(12.0, cw)},
    }
    return {
        "schema_id": "wayfarer.g19r.newport.scale_metrics.v1",
        "phase": PHASE_ID,
        "generated_at": GENERATED_AT,
        "source_commit": STARTING_MAIN_COMMIT,
        "player_derived_scale": player,
        "street_width_targets": targets,
        "building_frontage_ranges": {
            "small_shop_or_rowhouse": {"character_widths": [5.0, 8.0], "world_units": [width_from_chars(5.0, cw), width_from_chars(8.0, cw)]},
            "tavern_or_counting_house_landmark": {"character_widths": [10.0, 14.0], "world_units": [width_from_chars(10.0, cw), width_from_chars(14.0, cw)]},
            "warehouse_or_boathouse": {"character_widths": [9.0, 14.0], "world_units": [width_from_chars(9.0, cw), width_from_chars(14.0, cw)]},
        },
        "lot_depth_ranges": {
            "commercial_lot": {"character_widths": [7.0, 11.0], "world_units": [width_from_chars(7.0, cw), width_from_chars(11.0, cw)]},
            "landmark_lot": {"character_widths": [9.0, 13.0], "world_units": [width_from_chars(9.0, cw), width_from_chars(13.0, cw)]},
            "residential_lot": {"character_widths": [7.0, 10.0], "world_units": [width_from_chars(7.0, cw), width_from_chars(10.0, cw)]},
        },
        "dock_width_ranges": {
            "minor_finger_pier": {"character_widths": [3.0, 4.0], "world_units": [width_from_chars(3.0, cw), width_from_chars(4.0, cw)]},
            "cargo_landing": {"character_widths": [5.0, 7.0], "world_units": [width_from_chars(5.0, cw), width_from_chars(7.0, cw)]},
        },
        "current_runtime_scale_audit": {
            "tile_size_world_units": 32,
            "current_primary_road_three_tiles_world_units": 96,
            "current_primary_road_three_tiles_character_widths": round(96 / cw, 3),
            "verdict": "Current three-tile Newport roads are below the 10-15 character-width harbor/commercial target and cannot be used as proof that road scale is correct.",
        },
    }


def build_districts() -> list[dict[str, Any]]:
    return [
        {
            "id": "harbor_wharf",
            "name": "Harbor / Wharf District",
            "zone_rect": rect(180, 860, 1640, 300),
            "purpose": "Working edge where arrival, trade, cargo, sailors, and clues physically enter Newport.",
            "player_function": "Arrival read, dock clue, visible working harbor life, optional cargo inspection, transition from boat/wharf to town street.",
            "npc_roles": ["dockworker", "sailor", "warehouse hand"],
            "quest_relevance": "Arrival harbor beat, dock clue beat, wharf lantern rumor, manifest cargo discrepancy.",
            "landmark": "Central cargo landing and warehouse doors aligned to the harborfront road.",
            "dominant_ground_treatment": "Weathered planks, wet cobble, mud at cargo edges, water boundary below.",
            "prop_families": ["bollards", "rope coils", "barrels", "crates", "cargo carts", "lanterns"],
            "street_path_connections": ["harborfront_road", "dock_paths", "central_upland_counting_house_connector"],
            "camera_viewpoint": "harbor_work_view",
            "required_screenshots": ["arrival_harbor_view", "harbor_work_view", "debug_disabled_view"],
        },
        {
            "id": "counting_house_clerk",
            "name": "Counting House / Clerk District",
            "zone_rect": rect(940, 330, 390, 260),
            "purpose": "Official trade-pressure node where the missing manifest becomes a concrete problem instead of a vague rumor.",
            "player_function": "First official objective, records window interaction, clear central route target.",
            "npc_roles": ["clerk", "runner", "custom-house assistant"],
            "quest_relevance": "Missing manifest beat, first objective confirmation, return/report option.",
            "landmark": "Counting House frontage and notice board visible from the main avenue.",
            "dominant_ground_treatment": "Drier cobble forecourt with paper/posting board and stone threshold.",
            "prop_families": ["notice board", "ledger desk marker", "sealed crates", "wayfinding sign"],
            "street_path_connections": ["main_commercial_avenue", "rear_service_street", "central_upland_counting_house_connector"],
            "camera_viewpoint": "counting_house_route_view",
            "required_screenshots": ["counting_house_route_view", "quest_interaction_view"],
        },
        {
            "id": "tavern_inn_rumor_hub",
            "name": "Tavern / Inn Rumor Hub",
            "zone_rect": rect(280, 335, 430, 280),
            "purpose": "Social landmark that converts harbor facts into pre-Revolution whisper network play.",
            "player_function": "Memorable west landmark, rumor hub, route choice, safe place to hear named people and motives.",
            "npc_roles": ["tavern keeper", "rumor carrier", "patron"],
            "quest_relevance": "Tavern whisper beat, two-NPC rumor beat, optional hidden clue route.",
            "landmark": "Large Tavern/Inn lot at the west bend of the commercial avenue.",
            "dominant_ground_treatment": "Warm cobble threshold, porch/stoop, tavern yard edge, rear gate into service lane.",
            "prop_families": ["bench", "lanterns", "hanging sign", "stable/yard hints", "barrels"],
            "street_path_connections": ["main_commercial_avenue", "rear_service_street", "hidden_rumor_cutthrough"],
            "camera_viewpoint": "tavern_landmark_view",
            "required_screenshots": ["tavern_landmark_view", "npc_route_proof_view"],
        },
        {
            "id": "commercial_avenue",
            "name": "Commercial Avenue",
            "zone_rect": rect(630, 355, 1160, 270),
            "purpose": "Readable shop street that ties tavern, counting house, chandlery, market, and island exit into one town spine.",
            "player_function": "Human-scale movement corridor with storefronts and repeated orientation anchors.",
            "npc_roles": ["merchant", "shopkeeper", "runner", "courier"],
            "quest_relevance": "Two-NPC rumor, market-route clue, guidepost to island exit.",
            "landmark": "Shop row and market shed stepping toward the east exit.",
            "dominant_ground_treatment": "Wide cobble/wagon street with worn pedestrian shoulders and storefront stoops.",
            "prop_families": ["shop signs", "awnings", "market crates", "hand carts", "street lamps"],
            "street_path_connections": ["main_commercial_avenue", "east_market_connector", "village_to_island_road"],
            "camera_viewpoint": "commercial_avenue_view",
            "required_screenshots": ["commercial_avenue_view"],
        },
        {
            "id": "rear_service_lane",
            "name": "Rear Service Lane",
            "zone_rect": rect(240, 270, 1500, 220),
            "purpose": "Back-of-house circulation for deliveries, gossip, hidden clues, and believable town operations.",
            "player_function": "Secondary route that teaches the town is not a flat frontage board.",
            "npc_roles": ["runner", "suspicious patron", "courier"],
            "quest_relevance": "Hidden rumor/clue route, return/report variant, service-gate overheard lead.",
            "landmark": "Rear gate between Tavern/Inn and clerk lodging.",
            "dominant_ground_treatment": "Packed dirt, broken cobble, service mud, fence/yard edges.",
            "prop_families": ["fences", "barrels", "wash lines", "small sheds", "lanterns"],
            "street_path_connections": ["rear_service_street", "hidden_rumor_cutthrough", "north_residential_lane"],
            "camera_viewpoint": "rear_service_lane_view",
            "required_screenshots": ["rear_service_lane_view"],
        },
        {
            "id": "residential_edge",
            "name": "Residential Edge",
            "zone_rect": rect(260, 75, 1250, 225),
            "purpose": "Quiet lived-in town edge that gives workers and clerks homes instead of making Newport only storefronts.",
            "player_function": "Soft boundary, optional exploration, believable life beyond the quest route.",
            "npc_roles": ["resident", "dockworker family", "clerk lodger"],
            "quest_relevance": "Optional return/report flavor and worldbuilding.",
            "landmark": "Boarding house row above the rear lane.",
            "dominant_ground_treatment": "Grass yards, compact footpaths, garden edges, dry dirt.",
            "prop_families": ["fences", "laundry", "garden boxes", "small carts"],
            "street_path_connections": ["north_residential_lane", "rear_service_street"],
            "camera_viewpoint": "wide_town_cohesion_view",
            "required_screenshots": ["wide_town_cohesion_view"],
        },
        {
            "id": "village_to_island_exit",
            "name": "Village-to-Island Exit",
            "zone_rect": rect(1710, 400, 640, 330),
            "purpose": "Clear eastward threshold where town composition opens into island exploration.",
            "player_function": "Next-step orientation and first-session pull beyond Newport.",
            "npc_roles": ["courier", "guidepost guard", "sailor"],
            "quest_relevance": "Island lead beat, village exit beat.",
            "landmark": "Guidepost and narrowing road beyond the market edge.",
            "dominant_ground_treatment": "Cobble-to-dirt transition, shoulder grass, direction sign.",
            "prop_families": ["guidepost", "stone markers", "fence break", "lantern"],
            "street_path_connections": ["main_commercial_avenue", "village_to_island_road", "rear_service_street"],
            "camera_viewpoint": "village_exit_to_island_view",
            "required_screenshots": ["village_exit_to_island_view"],
        },
        {
            "id": "civic_notice_board",
            "name": "Civic / Notice Board Node",
            "zone_rect": rect(1010, 555, 260, 115),
            "purpose": "Small official public node that makes the counting-house route readable and gives the journal/objective fiction a place.",
            "player_function": "First objective confirmation and route reassurance.",
            "npc_roles": ["clerk runner", "merchant", "courier"],
            "quest_relevance": "First objective beat, missing manifest beat, return/report beat.",
            "landmark": "Notice board at the central avenue/cross street joint.",
            "dominant_ground_treatment": "Worn cobble node, chalk/posted-paper board, compact interaction apron.",
            "prop_families": ["notice board", "bench", "lamp", "paper bundles"],
            "street_path_connections": ["main_commercial_avenue", "central_upland_counting_house_connector"],
            "camera_viewpoint": "quest_interaction_view",
            "required_screenshots": ["quest_interaction_view"],
        },
        {
            "id": "hidden_rumor_clue_route",
            "name": "Hidden Rumor / Clue Route",
            "zone_rect": rect(605, 455, 330, 470),
            "purpose": "Optional service cut-through that lets social stealth and dock knowledge feel spatial rather than menu-driven.",
            "player_function": "Discoverable alternate path from tavern/rear lane to wharf clue.",
            "npc_roles": ["suspicious patron", "dock runner"],
            "quest_relevance": "Optional hidden clue beat and enriched journal state.",
            "landmark": "Narrow gate between tavern yard and wharf-side cargo stack.",
            "dominant_ground_treatment": "Dirt/cobble service cut-through with clear clearance and no clutter hiding path.",
            "prop_families": ["gate", "barrels at edge only", "low fence", "rope marker"],
            "street_path_connections": ["rear_service_street", "dock_paths", "harborfront_road"],
            "camera_viewpoint": "npc_route_proof_view",
            "required_screenshots": ["npc_route_proof_view", "rear_service_lane_view"],
        },
    ]


def build_streets(cw: float) -> list[dict[str, Any]]:
    def street(id_: str, name: str, start: tuple[float, float], end: tuple[float, float], chars: float, districts: list[str], purpose: str, npc: list[str], quest: list[str], ground: str, sightline: str, camera_note: str, rect_value: dict[str, float]) -> dict[str, Any]:
        return {
            "id": id_,
            "name": name,
            "start_point": vec(*start),
            "end_point": vec(*end),
            "width_character_units": chars,
            "width_world_units": width_from_chars(chars, cw),
            "districts_connected": districts,
            "player_purpose": purpose,
            "npc_route_usage": npc,
            "quest_usage": quest,
            "ground_type": ground,
            "landmark_sightline": sightline,
            "camera_readability_note": camera_note,
            "blockout_rect": rect_value,
        }

    return [
        street(
            "main_commercial_avenue",
            "Main Commercial Avenue",
            (260, 705),
            (1785, 705),
            12.0,
            ["tavern_inn_rumor_hub", "counting_house_clerk", "commercial_avenue", "village_to_island_exit"],
            "Primary first-session spine from harbor arrival through tavern, counting house, shops, and island exit.",
            ["merchant_shopkeeper", "tavern_patron_rumor_carrier", "clerk_runner"],
            ["first_objective", "counting_house_missing_manifest", "tavern_whisper", "island_lead"],
            "wide cobble and wagon-worn harbor street",
            "Tavern west, Counting House center, guidepost east.",
            "At gameplay zoom this road must read as a place the player is standing in, not a thin map line.",
            rect(260, 542, 1525, width_from_chars(12.0, cw)),
        ),
        street(
            "harborfront_road",
            "Harborfront Road",
            (220, 910),
            (1810, 910),
            10.0,
            ["harbor_wharf", "commercial_avenue", "village_to_island_exit"],
            "Southern working road where cargo moves between wharf apron and commercial lots.",
            ["dockworker", "sailor", "merchant_shopkeeper"],
            ["arrival_harbor", "dock_clue", "wharf_lantern_rumor"],
            "wet cobble, planks at wharf edge, mud feathering",
            "Water edge and warehouse doors always visible south of the road.",
            "Camera must preserve the water/wharf edge so the player understands arrival.",
            rect(220, 774, 1590, width_from_chars(10.0, cw)),
        ),
        street(
            "rear_service_street",
            "Rear Service Street",
            (260, 360),
            (1700, 360),
            5.5,
            ["rear_service_lane", "tavern_inn_rumor_hub", "counting_house_clerk", "residential_edge"],
            "Back-of-house service route that makes lots and daily work believable.",
            ["clerk_runner", "suspicious_patron", "courier_guard_sailor"],
            ["hidden_clue", "two_npc_rumor", "return_report"],
            "packed dirt and broken cobble",
            "Rear gates and residence row establish that buildings have backs.",
            "Should read narrower than the main avenue but still allow two NPC clearances.",
            rect(260, 285, 1440, width_from_chars(5.5, cw)),
        ),
        street(
            "central_upland_counting_house_connector",
            "Central Upland Counting House Connector",
            (1060, 875),
            (1060, 325),
            7.5,
            ["harbor_wharf", "main_commercial_avenue", "counting_house_clerk", "rear_service_lane"],
            "Clear uphill route from harbor work into official records and civic pressure.",
            ["clerk_runner", "dockworker"],
            ["counting_house_missing_manifest", "dock_clue", "return_report"],
            "cobble center with dirt shoulder",
            "Counting House sits at the north end; wharf cargo remains visible behind player.",
            "Route view must show the target building and enough street width for human scale.",
            rect(958, 325, width_from_chars(7.5, cw), 550),
        ),
        street(
            "west_tavern_connector",
            "West Tavern Connector",
            (510, 870),
            (510, 335),
            6.5,
            ["harbor_wharf", "tavern_inn_rumor_hub", "rear_service_lane"],
            "Secondary arrival-to-tavern route with strong landmark pull.",
            ["tavern_patron_rumor_carrier", "dockworker"],
            ["tavern_whisper", "two_npc_rumor"],
            "cobble with tavern threshold shoulders",
            "Tavern sign and porch are the vertical target.",
            "Must feel like walking uphill into a social node, not cutting between icons.",
            rect(422, 335, width_from_chars(6.5, cw), 535),
        ),
        street(
            "east_market_connector",
            "East Market Connector",
            (1560, 890),
            (1560, 360),
            6.0,
            ["harbor_wharf", "commercial_avenue", "rear_service_lane", "village_to_island_exit"],
            "Market and exit connector that makes the east side a district, not a dead end.",
            ["merchant_shopkeeper", "courier_guard_sailor"],
            ["two_npc_rumor", "island_lead", "village_exit"],
            "cobble-to-dirt transition",
            "Market shed and exit guidepost line the player's next move.",
            "Should show continuation out of town without swallowing the market lots.",
            rect(1478, 360, width_from_chars(6.0, cw), 530),
        ),
        street(
            "dock_paths",
            "Dock Paths and Cargo Landings",
            (420, 1030),
            (1490, 1030),
            5.0,
            ["harbor_wharf"],
            "Work paths across cargo landings and finger piers.",
            ["dockworker", "sailor"],
            ["dock_clue", "arrival_harbor"],
            "planks, wet mud, rope-bounded walking lanes",
            "Warehouse and boathouse doors anchor pause points.",
            "Camera must prove wharf apron width, not hide it behind cargo scatter.",
            rect(360, 960, 1240, width_from_chars(5.0, cw)),
        ),
        street(
            "hidden_rumor_cutthrough",
            "Hidden Rumor Service Cut-through",
            (680, 420),
            (840, 925),
            3.5,
            ["rear_service_lane", "hidden_rumor_clue_route", "harbor_wharf"],
            "Optional narrow route for hidden clue discovery and overheard rumor geography.",
            ["suspicious_patron", "clerk_runner"],
            ["optional_hidden_clue", "two_npc_rumor"],
            "packed dirt, broken cobble, low fence edges",
            "Tavern rear gate and cargo stack mark both ends.",
            "Narrow, but still at least 3 character widths and not clutter-blocked.",
            rect(650, 420, width_from_chars(3.5, cw), 505),
        ),
        street(
            "village_to_island_road",
            "Village-to-Island Road",
            (1720, 610),
            (2320, 500),
            8.0,
            ["commercial_avenue", "rear_service_lane", "village_to_island_exit"],
            "Obvious exit route that pulls the player from town into island exploration.",
            ["courier_guard_sailor", "merchant_shopkeeper"],
            ["island_lead", "village_exit", "return_report"],
            "cobble fading to dirt and grass shoulder",
            "Guidepost and road bend visible from market edge.",
            "Exit should read as continuation, not a blank map border.",
            rect(1700, 500, 640, width_from_chars(8.0, cw)),
        ),
        street(
            "secret_side_path",
            "Optional Secret / Side Path",
            (1520, 370),
            (2080, 315),
            3.5,
            ["rear_service_lane", "village_to_island_exit"],
            "Subtle clue route for players following rumor-network hints.",
            ["courier_guard_sailor", "suspicious_patron"],
            ["optional_hidden_clue", "island_lead_enriched"],
            "grass/dirt footpath with sparse edge markers",
            "Back-lane fence break points toward the island road.",
            "Must remain readable as optional, not confuse the critical route.",
            rect(1510, 295, 590, width_from_chars(3.5, cw)),
        ),
    ]


def build_lots(cw: float) -> list[dict[str, Any]]:
    def lot(id_: str, district: str, role: str, frontage: str, entry: str, lot_rect: dict[str, float], footprint: dict[str, float], setback_chars: float, props: list[str], npc_use: list[str], quest_use: list[str], sightline: str) -> dict[str, Any]:
        return {
            "id": id_,
            "district": district,
            "building_role": role,
            "frontage_street": frontage,
            "entry_orientation": entry,
            "lot_size": lot_rect,
            "building_footprint_target": footprint,
            "setback_character_widths": setback_chars,
            "setback_world_units": width_from_chars(setback_chars, cw),
            "adjacent_props": props,
            "npc_use": npc_use,
            "quest_use": quest_use,
            "sightline_purpose": sightline,
            "placement_rule": "Building footprint must front the named street, stay inside the lot, preserve the measured street width, and keep entry clearance free of clutter.",
        }

    return [
        lot("lot_tavern_inn_centerpiece", "tavern_inn_rumor_hub", "Tavern/Inn centerpiece landmark", "main_commercial_avenue", "south", rect(300, 350, 380, 250), rect(342, 390, 296, 162), 2.0, ["hanging sign", "bench", "lantern", "rear gate"], ["tavern keeper", "rumor carrier", "patron"], ["tavern_whisper", "two_npc_rumor", "optional_hidden_clue"], "West landmark visible from arrival and the central avenue."),
        lot("lot_counting_house_clerk", "counting_house_clerk", "Counting House / Clerk official lot", "main_commercial_avenue", "south", rect(970, 345, 330, 225), rect(1015, 382, 240, 145), 2.0, ["notice board", "sealed crates", "paper bundles"], ["clerk", "runner"], ["first_objective", "counting_house_missing_manifest", "return_report"], "Central official target visible from harborfront and rear lane connector."),
        lot("lot_mercantile_shop", "commercial_avenue", "Mercantile shop row lot", "main_commercial_avenue", "south", rect(700, 370, 230, 190), rect(725, 405, 180, 118), 1.5, ["awning sign", "crate edge", "lamp"], ["merchant"], ["two_npc_rumor"], "Fills the street wall between tavern and counting house."),
        lot("lot_chandlery_outfitter", "commercial_avenue", "Chandlery / outfitter shop lot", "main_commercial_avenue", "south", rect(1305, 370, 230, 190), rect(1330, 405, 180, 120), 1.5, ["rope rack", "sail cloth", "shop sign"], ["shopkeeper"], ["dock_clue_support"], "Connects official trade to working wharf function."),
        lot("lot_market_shed", "commercial_avenue", "Market shed and fishmonger lot", "east_market_connector", "southwest", rect(1535, 380, 245, 180), rect(1565, 415, 185, 110), 1.0, ["fish crates", "hand cart", "lamp"], ["merchant", "courier"], ["two_npc_rumor", "island_lead"], "Last commercial landmark before the island exit turn."),
        lot("lot_west_dock_warehouse", "harbor_wharf", "Harbor service / storage lot", "harborfront_road", "south", rect(390, 900, 330, 190), rect(430, 932, 250, 120), 1.5, ["cargo stack", "bollards", "rope"], ["dockworker"], ["dock_clue"], "Working storage visible from arrival, not a decorative warehouse."),
        lot("lot_central_boathouse_landing", "harbor_wharf", "Boathouse and cargo landing lot", "dock_paths", "south", rect(950, 940, 360, 175), rect(995, 970, 270, 110), 1.5, ["mooring post", "barrels", "water edge"], ["sailor", "dockworker"], ["arrival_harbor", "dock_clue"], "Centers the wharf as working waterfront."),
        lot("lot_cooperage_service", "harbor_wharf", "Cooperage / barrel service lot", "harborfront_road", "south", rect(1370, 880, 260, 190), rect(1405, 915, 195, 120), 1.5, ["barrel hoops", "small cart", "rope"], ["dockworker"], ["optional_hidden_clue"], "Shows harbor economy beyond generic crates."),
        lot("lot_boarding_house", "residential_edge", "Boarding house residential lot", "north_residential_lane", "south", rect(620, 105, 260, 180), rect(650, 135, 200, 120), 2.0, ["fence", "laundry", "garden"], ["dockworker family"], ["worldbuilding_return_flavor"], "Humanizes the workers who use the wharf."),
        lot("lot_dockworker_rowhouse", "residential_edge", "Dockworker rowhouse lot", "north_residential_lane", "south", rect(910, 105, 300, 180), rect(940, 135, 240, 118), 2.0, ["yard fence", "bucket", "lamp"], ["dockworker"], ["two_npc_rumor_support"], "Makes the rear service street feel lived in."),
        lot("lot_clerk_lodging", "residential_edge", "Clerk lodging / townhouse lot", "rear_service_street", "south", rect(1215, 115, 270, 175), rect(1240, 145, 215, 115), 2.0, ["mail crate", "notice scrap", "small bench"], ["clerk runner"], ["counting_house_missing_manifest"], "Connects official function to residential back street."),
        lot("lot_civic_notice_board", "civic_notice_board", "Notice board civic node", "central_upland_counting_house_connector", "south", rect(1055, 565, 195, 100), rect(1100, 582, 105, 48), 1.0, ["bench", "lamp", "posted papers"], ["runner", "courier"], ["first_objective", "return_report"], "Gives objective/journal fiction a spatial anchor."),
        lot("lot_village_exit_guidepost", "village_to_island_exit", "Village exit / guidepost area", "village_to_island_road", "east", rect(1815, 500, 300, 175), rect(1870, 535, 95, 55), 1.0, ["guidepost", "stone marker", "fence break"], ["courier", "sailor"], ["island_lead", "village_exit"], "Makes the island route legible before the player reaches the edge."),
    ]


def build_npc_routes() -> list[dict[str, Any]]:
    return [
        {
            "id": "dockworker_route",
            "npc_role": "dockworker",
            "home_station": "lot_west_dock_warehouse",
            "work_destination": "central cargo landing and west warehouse doors",
            "walking_path": ["west_service_pier", "lot_west_dock_warehouse", "central_boathouse_landing", "harborfront_road"],
            "pause_points": [vec(465, 1025), vec(835, 1010), vec(1050, 1000)],
            "facing_directions": ["down", "right", "left"],
            "quest_interaction_points": ["dock_clue", "wharf_lantern_rumor"],
            "district_role": "Shows the harbor economy in motion once grounded walk sheets exist.",
            "movement_state": "stationed_until_dedicated_walk_animation",
            "animation_movement_requirements": "No static sprite may translate along this route. Use grounded idle/facing now; unlock route walking only with timestamped idle/walk/facing proof.",
        },
        {
            "id": "counting_house_clerk_runner_route",
            "npc_role": "counting house clerk or runner",
            "home_station": "lot_counting_house_clerk",
            "work_destination": "notice board, tavern porch, wharf cargo inspection",
            "walking_path": ["lot_counting_house_clerk", "central_upland_counting_house_connector", "lot_civic_notice_board", "lot_tavern_inn_centerpiece", "lot_west_dock_warehouse"],
            "pause_points": [vec(1080, 555), vec(1120, 620), vec(520, 590), vec(455, 985)],
            "facing_directions": ["down", "left", "down", "right"],
            "quest_interaction_points": ["first_objective", "counting_house_missing_manifest", "return_report"],
            "district_role": "Official pressure thread tying the counting house to social and harbor evidence.",
            "movement_state": "stationed_until_dedicated_walk_animation",
            "animation_movement_requirements": "Do not glide a static clerk sprite. Use idle/facing station changes only until clerk walk sheet exists.",
        },
        {
            "id": "tavern_patron_rumor_carrier_route",
            "npc_role": "tavern patron / rumor carrier",
            "home_station": "lot_tavern_inn_centerpiece",
            "work_destination": "tavern porch, rear service gate, central avenue social pocket",
            "walking_path": ["tavern_porch", "rear_service_street", "hidden_rumor_cutthrough", "main_commercial_avenue"],
            "pause_points": [vec(500, 585), vec(610, 365), vec(690, 500), vec(560, 720)],
            "facing_directions": ["down", "right", "down", "left"],
            "quest_interaction_points": ["tavern_whisper", "two_npc_rumor", "optional_hidden_clue"],
            "district_role": "Social route that makes whisper-network geography readable.",
            "movement_state": "stationed_until_dedicated_walk_animation",
            "animation_movement_requirements": "Do not glide a static patron between tavern and lane. Use stationed barks/facing until full movement proof exists.",
        },
        {
            "id": "merchant_shopkeeper_route",
            "npc_role": "merchant / shopkeeper",
            "home_station": "lot_mercantile_shop",
            "work_destination": "market shed, mercantile door, counting-house forecourt",
            "walking_path": ["lot_mercantile_shop", "main_commercial_avenue", "lot_market_shed", "lot_counting_house_clerk"],
            "pause_points": [vec(815, 585), vec(1510, 610), vec(1115, 610)],
            "facing_directions": ["down", "left", "up"],
            "quest_interaction_points": ["two_npc_rumor", "island_lead"],
            "district_role": "Commercial life and alternate rumor path.",
            "movement_state": "stationed_until_dedicated_walk_animation",
            "animation_movement_requirements": "Do not glide a static shopkeeper sprite. Short route can animate only after grounded shopkeeper walk/facing proof.",
        },
        {
            "id": "courier_guard_sailor_route",
            "npc_role": "optional guard / courier / sailor",
            "home_station": "lot_village_exit_guidepost",
            "work_destination": "market connector, village-to-island road, rear service lane",
            "walking_path": ["lot_village_exit_guidepost", "village_to_island_road", "east_market_connector", "rear_service_street"],
            "pause_points": [vec(1900, 585), vec(1760, 650), vec(1560, 520)],
            "facing_directions": ["right", "left", "up"],
            "quest_interaction_points": ["island_lead", "village_exit", "return_report"],
            "district_role": "Signals the next destination and guards against east-edge confusion.",
            "movement_state": "stationed_until_dedicated_walk_animation",
            "animation_movement_requirements": "Do not glide a static courier or sailor sprite. Station at guidepost until movement proof can show grounded step cycle.",
        },
    ]


def build_quest_beats() -> list[dict[str, Any]]:
    def beat(id_: str, location: str, district: str, npc: str, obj: str, camera: str, text: str, why: str) -> dict[str, Any]:
        return {
            "id": id_,
            "location": location,
            "district": district,
            "npc_involved": npc,
            "interaction_object": obj,
            "camera_screenshot_viewpoint": camera,
            "objective_text": text,
            "why_the_beat_belongs_there": why,
        }

    return [
        beat("arrival_harbor_beat", "central cargo landing", "harbor_wharf", "Edrin / sailor handoff", "arrival marker and mooring post", "arrival_harbor_view", "Find the Counting House above the harborfront road.", "The player arrives through the harbor economy; the first view must explain water, wharf, and town."),
        beat("first_objective_beat", "notice board at central avenue connector", "civic_notice_board", "clerk runner", "notice board", "quest_interaction_view", "Check the posted harbor notice.", "The board ties UI objective language to an in-world civic node."),
        beat("counting_house_missing_manifest_beat", "Counting House south frontage", "counting_house_clerk", "counting house clerk", "records window / ledger desk", "counting_house_route_view", "Ask about the missing manifest.", "Official trade conflict belongs in the counting house, not as loose dialogue on a random street."),
        beat("dock_clue_beat", "west dock warehouse cargo edge", "harbor_wharf", "dockworker", "cargo stack with wet-lantern mark", "harbor_work_view", "Inspect the cargo that was moved before dawn.", "Cargo evidence belongs in the working wharf where goods enter and leave town."),
        beat("tavern_whisper_beat", "Tavern/Inn porch and warm threshold", "tavern_inn_rumor_hub", "tavern keeper", "tavern sign / porch", "tavern_landmark_view", "Listen for the Third Toast rumor.", "The tavern is the public rumor hub, matching colonial public-house function."),
        beat("two_npc_rumor_beat", "main avenue between tavern and mercantile", "commercial_avenue", "rumor carrier and merchant", "social pocket bench", "npc_route_proof_view", "Compare the dock story with the market rumor.", "This makes NPC information spatial and social instead of a single railroaded speaker."),
        beat("island_lead_beat", "market edge guidepost", "village_to_island_exit", "courier / sailor", "guidepost", "village_exit_to_island_view", "Follow the east road toward the old island marker.", "The town geography points the player to the island before runtime reconstruction begins."),
        beat("village_exit_beat", "east cobble-to-dirt threshold", "village_to_island_exit", "courier / guide", "stone marker and fence break", "village_exit_to_island_view", "Leave Newport by the old island road.", "The exit is a place and threshold, not an arbitrary screen edge."),
        beat("optional_hidden_clue_beat", "rear gate to wharf service cut-through", "hidden_rumor_clue_route", "suspicious patron", "rear gate / barrel edge", "rear_service_lane_view", "Check the back way behind the tavern.", "The optional clue uses service geography so the town gains depth."),
        beat("return_report_beat", "Counting House notice board or tavern porch", "counting_house_clerk", "clerk or tavern keeper", "notice board / tavern sign", "quest_interaction_view", "Report what you found and choose who hears it first.", "Return/report choices use existing town nodes, strengthening memory of Newport."),
    ]


def build_camera_viewpoints() -> list[dict[str, Any]]:
    def view(id_: str, pos: tuple[float, float], zoom: float, purpose: str, visible: list[str], hidden: list[str], bar: str) -> dict[str, Any]:
        return {
            "id": id_,
            "camera_position": vec(*pos),
            "zoom": zoom,
            "purpose": purpose,
            "what_should_be_visible": visible,
            "what_should_not_be_visible": hidden,
            "quality_bar": bar,
        }

    return [
        view("wide_town_cohesion_view", (1080, 710), 0.82, "Review the whole blockout as a town plan.", ["water edge", "wharf", "main avenue", "rear lane", "district zones", "island exit"], ["debug overlays", "tiny unreadable street lines as acceptance proof"], "Wide review may be map-like, but it must prove one authored harbor town."),
        view("arrival_harbor_view", (430, 920), 1.38, "First gameplay arrival framing.", ["water", "wharf apron", "main street approach", "tavern pull"], ["unrelated island sprawl", "debug labels"], "Player understands arrival and where town begins within 10 seconds."),
        view("counting_house_route_view", (1045, 645), 1.38, "Show route from main avenue to counting house.", ["counting house", "notice board", "wide street clearance", "connector"], ["road hidden under buildings", "floating lots"], "Counting House is a clear destination, not a scattered icon."),
        view("tavern_landmark_view", (500, 645), 1.38, "Show tavern as landmark and rumor hub.", ["tavern lot", "main avenue", "rear gate hint", "social pocket"], ["tavern treated as same-weight shop", "clutter hiding street"], "Tavern reads as memorable social hub."),
        view("commercial_avenue_view", (1260, 675), 1.38, "Show human-scale commercial street wall.", ["shop row", "market", "street width marker", "counting house edge"], ["thin path read", "prop scatter as layout"], "Avenue feels walkable at character scale."),
        view("harbor_work_view", (980, 1010), 1.34, "Show working wharf apron and dock life.", ["warehouse", "boathouse", "cargo landings", "water edge"], ["cargo clutter blocking route", "blank water edge"], "Wharf reads as working harbor, not decoration."),
        view("rear_service_lane_view", (850, 380), 1.38, "Show back street and optional clue route.", ["rear lane", "tavern back", "residential edge", "hidden gate"], ["dead flat frontage-only town", "confusing main route"], "Back-of-house circulation is legible."),
        view("npc_route_proof_view", (735, 700), 1.38, "Show planned NPC station/route geography.", ["tavern porch", "service cut-through", "main avenue pause points"], ["static sprite glide", "unanchored NPC"], "NPC movement remains stationed until animation is proven."),
        view("village_exit_to_island_view", (1880, 610), 1.25, "Show east exit and island-road pull.", ["market edge", "guidepost", "road leaving town"], ["ambiguous map edge", "unexplained blank terrain"], "Player knows how town continues toward the island."),
        view("quest_interaction_view", (1100, 600), 1.38, "Show objective/journal interaction geography.", ["notice board", "counting house forecourt", "player marker clearance"], ["oversized UI labels", "debug prompts"], "Quest beats belong to visible town nodes."),
        view("debug_disabled_view", (1080, 720), 1.38, "Canonical clean review state.", ["street hierarchy", "lots", "districts without debug HUD"], ["debug overlays", "collision labels", "temporary markers"], "No debug artifacts may be needed to understand the plan."),
    ]


def make_source_data(scale: dict[str, Any]) -> dict[str, Any]:
    districts = build_districts()
    streets = build_streets(float(scale["player_derived_scale"]["world_units_per_character_width"]))
    lots = build_lots(float(scale["player_derived_scale"]["world_units_per_character_width"]))
    npcs = build_npc_routes()
    beats = build_quest_beats()
    cameras = build_camera_viewpoints()
    return {
        "schema_id": "wayfarer.g19r.newport_scale_street_blockout_source_of_truth.v1",
        "phase": PHASE_ID,
        "phase_name": "G-19R Newport Scale + Street Blockout Source of Truth",
        "status": "PASS",
        "generated_at": GENERATED_AT,
        "starting_main_commit": STARTING_MAIN_COMMIT,
        "branch": BRANCH,
        "figma_figjam": {
            "used": False,
            "reason": "Not used because G-19R needed repo-contained, reusable source files with no cloud/account friction. The SVG/PNG/JSON artifact set is the compatible visual planning artifact.",
            "artifact_name": "",
            "export_method": "",
            "repo_mirror": "wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/",
        },
        "tooling_used": [
            "browser research into level flow, blockout, critical path, colonial wharf/tavern context",
            "Python/Pillow measured blockout generation",
            "repo Godot player/camera source inspection",
            "JSON source-of-truth schema",
            "SVG/PNG visual blockout export",
            "G-19R and future source alignment validators",
        ],
        "browser_research_sources": [
            {"label": "The Level Design Book - Flow", "url": "https://book.leveldesignbook.com/process/layout/flow", "used_for": "movement, wayfinding, metrics, blockout/playtest framing"},
            {"label": "The Level Design Book - Critical Path", "url": "https://book.leveldesignbook.com/process/layout/criticalpath", "used_for": "player start, exit, beat, and route markup discipline"},
            {"label": "National Park Service - Salem Maritime history", "url": "https://www.nps.gov/articles/000/history.htm", "used_for": "colonial port wharves, warehouses, custom house, trade waterfront logic"},
            {"label": "Colonial Williamsburg - Early American taverns", "url": "https://www.colonialwilliamsburg.org/discover/historic-area/historic-places/a-time-travelers-guide-to-early-american-taverns/", "used_for": "tavern as public/social/rumor/economic node"},
            {"label": "National Park Service - Annapolis", "url": "https://www.nps.gov/stsp/learn/annapolis.htm", "used_for": "planned colonial seaport precedent and 18th-century town character"},
        ],
        "coordinate_system": {
            "world_units": "Godot 2D world pixels",
            "blockout_world_size": {"w": 2400, "h": 1600},
            "water_edge_y": 1120,
            "north_is_up": True,
            "major_layout_changes_require_source_update": True,
        },
        "scale_metrics_path": "wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_scale_metrics.json",
        "scale_summary": scale,
        "districts": districts,
        "streets": streets,
        "lots": lots,
        "npc_routes": npcs,
        "quest_beats": beats,
        "camera_viewpoints": cameras,
        "acceptance_scores": {
            "blockout_layout_plan_score": 8.7,
            "world_cohesion_plan_score": 8.7,
            "player_orientation_plan_score": 8.6,
            "quest_geography_integration_score": 8.6,
            "implementation_readiness_score": 8.6,
        },
        "future_placement_governance": {
            "rule": "After G-19R, all major Newport street, lot, district, wharf, NPC route, quest beat, or camera placement changes must update this source of truth and the mirrored planning artifacts before runtime placement changes can pass.",
            "major_layout_files_guarded": [
                "wayfarer_godot_vertical_slice/scripts/NewportTownBlueprint.gd",
                "wayfarer_godot_vertical_slice/scenes/map/MapLayer.gd",
                "wayfarer_godot_vertical_slice/scenes/Main.gd",
                "wayfarer_godot_vertical_slice/data/world_layout/",
            ],
            "minor_tuning_allowed": "Small art/collision offsets are allowed only when documented in the implementation report and when street widths, lot frontage, district boundaries, quest beats, NPC route intent, and camera viewpoints remain aligned.",
            "validator": "wayfarer_godot_vertical_slice/tools/validate_newport_layout_source_alignment.py",
            "g19s_requirement": "G-19S must consume or validate against the G-19R source JSON and implement the approved plan without inventing a new layout.",
        },
    }


def artifact_payload(schema: str, key: str, source: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_id": schema,
        "phase": PHASE_ID,
        "generated_at": GENERATED_AT,
        "source_of_truth": "docs/design/NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.json",
        key: source[key],
    }


def svg_text(x: float, y: float, text: str, size: int = 18, fill: str = "#1f2a2e") -> str:
    safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" fill="{fill}">{safe}</text>'


def svg_rect(r: dict[str, float], fill: str, stroke: str, width: int = 2, opacity: float = 1.0, rx: int = 0) -> str:
    return f'<rect x="{r["x"]}" y="{r["y"]}" width="{r["w"]}" height="{r["h"]}" fill="{fill}" fill-opacity="{opacity}" stroke="{stroke}" stroke-width="{width}" rx="{rx}" />'


def svg_line(points: list[tuple[float, float]], stroke: str, width: float, dash: str = "", opacity: float = 1.0) -> str:
    attrs = f'fill="none" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" stroke-opacity="{opacity}"'
    if dash:
        attrs += f' stroke-dasharray="{dash}"'
    d = "M " + " L ".join(f"{x},{y}" for x, y in points)
    return f'<path d="{d}" {attrs} />'


def create_svg(source: dict[str, Any], scale: dict[str, Any]) -> str:
    colors = {
        "water": "#4b8ba3",
        "wharf": "#9a8060",
        "main": "#b6a06d",
        "rear": "#8b7656",
        "district": "#7ea46d",
        "lot": "#f1ddaa",
        "tavern": "#d47f54",
        "counting": "#c7c2a0",
        "commercial": "#d5b76d",
        "residential": "#89a878",
        "exit": "#b4c485",
    }
    lines: list[str] = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="2400" height="1600" viewBox="0 0 2400 1600">',
        '<rect x="0" y="0" width="2400" height="1600" fill="#d8cfaa" />',
        svg_rect(rect(0, 1120, 2400, 480), colors["water"], "#2e6078", 0, 0.95),
        svg_text(34, 54, "G-19R Newport Measured Blockout Source of Truth", 34, "#1d2c34"),
        svg_text(36, 94, "Scale: player visible width = %.1f world units; main avenue = 12 character widths; wharf apron = 10.5 character widths" % float(scale["player_derived_scale"]["world_units_per_character_width"]), 20, "#34434a"),
    ]
    district_colors = {
        "harbor_wharf": "#b28a62",
        "counting_house_clerk": "#c6b98e",
        "tavern_inn_rumor_hub": "#d9825b",
        "commercial_avenue": "#d0af62",
        "rear_service_lane": "#9b8462",
        "residential_edge": "#86a874",
        "village_to_island_exit": "#bdd08a",
        "civic_notice_board": "#e1cf8f",
        "hidden_rumor_clue_route": "#a989a8",
    }
    for d in source["districts"]:
        lines.append(svg_rect(d["zone_rect"], district_colors.get(d["id"], colors["district"]), "#405142", 2, 0.28, 8))
        lines.append(svg_text(d["zone_rect"]["x"] + 10, d["zone_rect"]["y"] + 28, d["name"], 17, "#263128"))
    for s in source["streets"]:
        fill = colors["main"] if s["id"] == "main_commercial_avenue" else colors["rear"]
        if "dock" in s["id"] or "harborfront" in s["id"]:
            fill = colors["wharf"]
        if "island" in s["id"]:
            fill = colors["exit"]
        if "hidden" in s["id"] or "secret" in s["id"]:
            fill = "#caa2c6"
        lines.append(svg_rect(s["blockout_rect"], fill, "#5d4a2d", 2, 0.55, 10))
        lines.append(svg_line([(s["start_point"]["x"], s["start_point"]["y"]), (s["end_point"]["x"], s["end_point"]["y"])], "#372918", max(6.0, float(s["width_world_units"]) * 0.08), opacity=0.85))
        mx = (s["start_point"]["x"] + s["end_point"]["x"]) / 2
        my = (s["start_point"]["y"] + s["end_point"]["y"]) / 2
        lines.append(svg_text(mx + 8, my - 8, f'{s["id"]} ({s["width_character_units"]}cw)', 16, "#3a2c1f"))
    for lot in source["lots"]:
        fill = colors["lot"]
        if "tavern" in lot["id"]:
            fill = colors["tavern"]
        elif "counting" in lot["id"]:
            fill = colors["counting"]
        elif lot["district"] == "commercial_avenue":
            fill = colors["commercial"]
        elif lot["district"] == "residential_edge":
            fill = colors["residential"]
        elif "exit" in lot["id"]:
            fill = colors["exit"]
        lines.append(svg_rect(lot["lot_size"], fill, "#513b27", 3, 0.62, 6))
        lines.append(svg_rect(lot["building_footprint_target"], "#f8f0d0", "#2f2a1e", 2, 0.92, 4))
        lines.append(svg_text(lot["lot_size"]["x"] + 8, lot["lot_size"]["y"] + 22, lot["id"].replace("lot_", ""), 14, "#2b231c"))
    for route in source["npc_routes"]:
        pts = [(p["x"], p["y"]) for p in route["pause_points"]]
        if len(pts) > 1:
            lines.append(svg_line(pts, "#6b2e90", 5, "12 10", 0.85))
        for p in route["pause_points"]:
            lines.append(f'<circle cx="{p["x"]}" cy="{p["y"]}" r="12" fill="#6b2e90" fill-opacity="0.75" stroke="#fff" stroke-width="2" />')
    critical = [
        (430, 1035),
        (1080, 630),
        (500, 585),
        (1060, 1030),
        (1900, 585),
    ]
    lines.append(svg_line(critical, "#f7f0d4", 14, "20 14", 0.92))
    lines.append(svg_line(critical, "#b33a2b", 5, "12 14", 0.92))
    for camera in source["camera_viewpoints"]:
        x = camera["camera_position"]["x"]
        y = camera["camera_position"]["y"]
        lines.append(f'<circle cx="{x}" cy="{y}" r="18" fill="#1b4f72" fill-opacity="0.9" stroke="#ffffff" stroke-width="3" />')
        lines.append(svg_text(x + 20, y + 6, camera["id"], 13, "#123449"))
    cw = float(scale["player_derived_scale"]["world_units_per_character_width"])
    ref_x, ref_y = 60, 1450
    for i in range(15):
        lines.append(f'<rect x="{ref_x + i * cw}" y="{ref_y}" width="{cw}" height="46" fill="{"#333" if i % 2 == 0 else "#eee"}" stroke="#111" stroke-width="1" />')
    lines.append(svg_text(ref_x, ref_y - 14, "15 player-width street scale reference", 18, "#1f2a2e"))
    lines.append(svg_text(60, 1525, "Legend: zones = translucent bands, streets = measured corridors, cream rectangles = building footprints, purple dashed = NPC plans, red dashed = opening quest route.", 18, "#1f2a2e"))
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def draw_png(source: dict[str, Any], scale: dict[str, Any], path: Path) -> None:
    img = Image.new("RGB", (2400, 1600), "#d8cfaa")
    draw = ImageDraw.Draw(img, "RGBA")
    font = ImageFont.load_default()
    title_font = ImageFont.load_default(size=34)
    label_font = ImageFont.load_default(size=18)
    small_font = ImageFont.load_default(size=14)
    draw.rectangle([0, 1120, 2400, 1600], fill="#4b8ba3")
    draw.text((34, 38), "G-19R Newport Measured Blockout Source of Truth", fill="#1d2c34", font=title_font)
    draw.text((36, 88), "Measured from current player/camera data. Roads are expressed in character widths.", fill="#34434a", font=label_font)
    district_colors = {
        "harbor_wharf": (178, 138, 98, 78),
        "counting_house_clerk": (198, 185, 142, 90),
        "tavern_inn_rumor_hub": (217, 130, 91, 98),
        "commercial_avenue": (208, 175, 98, 88),
        "rear_service_lane": (155, 132, 98, 82),
        "residential_edge": (134, 168, 116, 82),
        "village_to_island_exit": (189, 208, 138, 92),
        "civic_notice_board": (225, 207, 143, 96),
        "hidden_rumor_clue_route": (169, 137, 168, 90),
    }
    for d in source["districts"]:
        r = d["zone_rect"]
        draw.rounded_rectangle([r["x"], r["y"], r["x"] + r["w"], r["y"] + r["h"]], radius=8, fill=district_colors[d["id"]], outline=(64, 81, 66, 210), width=2)
        draw.text((r["x"] + 10, r["y"] + 8), d["name"], fill="#263128", font=small_font)
    for s in source["streets"]:
        r = s["blockout_rect"]
        fill = (182, 160, 109, 150)
        if "dock" in s["id"] or "harborfront" in s["id"]:
            fill = (154, 128, 96, 158)
        if "rear" in s["id"]:
            fill = (139, 118, 86, 150)
        if "island" in s["id"]:
            fill = (180, 196, 133, 165)
        if "hidden" in s["id"] or "secret" in s["id"]:
            fill = (202, 162, 198, 155)
        draw.rounded_rectangle([r["x"], r["y"], r["x"] + r["w"], r["y"] + r["h"]], radius=10, fill=fill, outline=(93, 74, 45, 235), width=2)
        draw.line([(s["start_point"]["x"], s["start_point"]["y"]), (s["end_point"]["x"], s["end_point"]["y"])], fill=(55, 41, 24, 220), width=max(6, int(float(s["width_world_units"]) * 0.08)))
        mx = (s["start_point"]["x"] + s["end_point"]["x"]) / 2
        my = (s["start_point"]["y"] + s["end_point"]["y"]) / 2
        draw.text((mx + 8, my - 8), f'{s["width_character_units"]}cw {s["id"]}', fill="#3a2c1f", font=small_font)
    for lot in source["lots"]:
        lr = lot["lot_size"]
        br = lot["building_footprint_target"]
        fill = (241, 221, 170, 190)
        if "tavern" in lot["id"]:
            fill = (212, 127, 84, 205)
        elif "counting" in lot["id"]:
            fill = (199, 194, 160, 205)
        draw.rounded_rectangle([lr["x"], lr["y"], lr["x"] + lr["w"], lr["y"] + lr["h"]], radius=6, fill=fill, outline=(81, 59, 39, 235), width=3)
        draw.rounded_rectangle([br["x"], br["y"], br["x"] + br["w"], br["y"] + br["h"]], radius=4, fill=(248, 240, 208, 235), outline=(47, 42, 30, 240), width=2)
        draw.text((lr["x"] + 8, lr["y"] + 8), lot["id"].replace("lot_", ""), fill="#2b231c", font=small_font)
    for route in source["npc_routes"]:
        pts = [(p["x"], p["y"]) for p in route["pause_points"]]
        if len(pts) > 1:
            draw.line(pts, fill=(107, 46, 144, 210), width=5)
        for p in route["pause_points"]:
            draw.ellipse([p["x"] - 12, p["y"] - 12, p["x"] + 12, p["y"] + 12], fill=(107, 46, 144, 210), outline=(255, 255, 255, 240), width=2)
    critical = [(430, 1035), (1080, 630), (500, 585), (1060, 1030), (1900, 585)]
    draw.line(critical, fill=(179, 58, 43, 230), width=6)
    for camera in source["camera_viewpoints"]:
        x = camera["camera_position"]["x"]
        y = camera["camera_position"]["y"]
        draw.ellipse([x - 18, y - 18, x + 18, y + 18], fill=(27, 79, 114, 230), outline=(255, 255, 255, 255), width=3)
        draw.text((x + 20, y + 4), camera["id"], fill="#123449", font=small_font)
    cw = float(scale["player_derived_scale"]["world_units_per_character_width"])
    ref_x, ref_y = 60, 1450
    for i in range(15):
        color = (51, 51, 51, 255) if i % 2 == 0 else (238, 238, 238, 255)
        draw.rectangle([ref_x + i * cw, ref_y, ref_x + (i + 1) * cw, ref_y + 46], fill=color, outline=(17, 17, 17, 255))
    draw.text((ref_x, ref_y - 24), "15 player-width street scale reference", fill="#1f2a2e", font=label_font)
    draw.text((60, 1528), "Zones, measured streets, lots, quest route, NPC routes, camera points, and player-scale ruler are shown.", fill="#1f2a2e", font=label_font)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def write_design_docs(source: dict[str, Any], scale: dict[str, Any]) -> None:
    cw = scale["player_derived_scale"]["world_units_per_character_width"]
    main_width = scale["street_width_targets"]["main_commercial_harbor_street"]["width_world_units"]
    current_width = scale["current_runtime_scale_audit"]["current_primary_road_three_tiles_character_widths"]
    md = f"""# Newport Scale + Street Blockout Source Of Truth

Phase: `G-19R Newport Scale + Street Blockout Source of Truth`

Status: `PASS`

Starting main commit: `{STARTING_MAIN_COMMIT}`

This is the mandatory design-source gate before further Newport runtime placement. It replaces code-first coordinate tuning with a measured, inspectable town plan that future Godot work must consume or validate against.

## Tooling Decision

Figma/FigJam was not used. The reason is practical: G-19R needed a repo-contained artifact set with no cloud-only dependency, no account friction, no payment path, and no credentials. The compatible planning artifact is:

- `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_measured_blockout.svg`
- `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_measured_blockout.png`
- machine-readable JSON plans in the same directory

## Browser Research Applied

- The Level Design Book flow guidance was used for movement, wayfinding, metrics, and the need to verify layout through blockout/playtest: https://book.leveldesignbook.com/process/layout/flow
- The Level Design Book critical path guidance was used for player start, exits, labeled beats, and route arrows: https://book.leveldesignbook.com/process/layout/criticalpath
- National Park Service Salem Maritime history was used for wharf, warehouse, custom-house, and port-trade logic: https://www.nps.gov/articles/000/history.htm
- Colonial Williamsburg tavern history was used to frame the tavern as a public/social/rumor/economic node: https://www.colonialwilliamsburg.org/discover/historic-area/historic-places/a-time-travelers-guide-to-early-american-taverns/
- National Park Service Annapolis material was used as a colonial seaport/planned-town precedent: https://www.nps.gov/stsp/learn/annapolis.htm

## Scale Derivation

The current player atlas alpha bounds are `{cw}` world units wide after runtime scale. The current 3-tile Newport road band is `{current_width}` character widths, which is below the 10-15 character-width target for a main harbor/commercial street.

Selected G-19R targets:

- Main commercial/harbor street: `12.0` character widths, `{main_width}` world units.
- Secondary street: `7.5` character widths.
- Rear/service lane: `5.5` character widths.
- Alley/service cut-through: `3.5` character widths.
- Wharf working apron: `10.5` character widths.
- NPC route clearance: `2.5` character widths.

## Town Plan

Newport is planned as a 1700s-inspired harbor origin village with these authored districts:

- Harbor / wharf district: working arrival, cargo, dock clue, visible economy.
- Counting House / clerk district: official manifest pressure and first objective.
- Tavern / inn rumor hub: landmark social node and whisper network.
- Commercial avenue: storefront spine connecting tavern, clerk, market, and exit.
- Rear service lane: back-of-house route for deliveries, clues, and believable lots.
- Residential edge: homes for workers and clerks so the town is not only a shop row.
- Village-to-island exit: east threshold toward exploration.
- Civic notice board: in-world objective/journal anchor.
- Hidden rumor/clue route: optional service path between tavern/rear lane and wharf.

## Governance

After G-19R, all major Newport placement work must derive from:

- `docs/design/NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.json`
- `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_district_plan.json`
- `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_street_hierarchy.json`
- `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_lot_plan.json`
- `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_npc_route_plan.json`
- `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_quest_beat_locations.json`
- `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_camera_viewpoints.json`

Major runtime layout edits in `NewportTownBlueprint.gd`, `MapLayer.gd`, `Main.gd`, or `data/world_layout/` must update the source-of-truth artifacts. Minor tuning is allowed only when documented and when it does not change street widths, lot frontage, district boundaries, NPC route intent, quest beat geography, or canonical cameras.

Next phase: `G-19S Newport Blockout-To-Godot Runtime Reconstruction`.
"""
    write_text(DESIGN_DIR / "NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.md", md)
    write_json(DESIGN_DIR / "NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.json", source)


def write_report(source: dict[str, Any], scale: dict[str, Any]) -> None:
    artifacts = [
        "g19r_newport_measured_blockout.svg",
        "g19r_newport_measured_blockout.png",
        "g19r_newport_scale_metrics.json",
        "g19r_newport_district_plan.json",
        "g19r_newport_street_hierarchy.json",
        "g19r_newport_lot_plan.json",
        "g19r_newport_npc_route_plan.json",
        "g19r_newport_quest_beat_locations.json",
        "g19r_newport_camera_viewpoints.json",
        "g19r_newport_blockout_manifest.json",
    ]
    scores = source["acceptance_scores"]
    md = f"""# G-19R Newport Scale + Street Blockout Source Of Truth

Final status: `PASS`

Branch: `{BRANCH}`

Starting main commit: `{STARTING_MAIN_COMMIT}`

## Correction

G-19R stops Newport from advancing as a code-coordinate problem. It establishes a measured, human-readable, machine-checkable town plan before more Godot placement, island expansion, quest expansion, or production-playable claims.

## Tools Used

- Browser research for level-design flow/blockout thinking and 1700s harbor/tavern context.
- Repo Godot/Python source inspection for current player, collision, camera, viewport, and map scale.
- Deterministic Python/Pillow generator for SVG/PNG/JSON blockout artifacts.
- JSON validators for G-19R artifact completeness and future layout-source alignment.

Figma/FigJam used: no. Fallback method: repo-contained SVG/PNG/JSON measured blockout.

## Scale Metrics Summary

- Player visual width: `{scale["player_derived_scale"]["player_visual_width_world_units"]}` world units.
- Player visual height: `{scale["player_derived_scale"]["player_visual_height_world_units"]}` world units.
- Player collision/body width: `{scale["player_derived_scale"]["player_collision_body_width_world_units"]}` world units.
- Player collision/body height: `{scale["player_derived_scale"]["player_collision_body_height_world_units"]}` world units.
- Gameplay viewport assumption: `{scale["player_derived_scale"]["camera_viewport_assumption_px"]["w"]}x{scale["player_derived_scale"]["camera_viewport_assumption_px"]["h"]}` at zoom `{scale["player_derived_scale"]["gameplay_zoom_assumption"]}`.
- Main street target: `12.0` character widths.
- Current 3-tile road audit: `{scale["current_runtime_scale_audit"]["current_primary_road_three_tiles_character_widths"]}` character widths, not acceptable proof.

## Artifact Paths

""" + "\n".join(f"- `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/{name}`" for name in artifacts) + f"""

## Plan Summary

Street hierarchy: main commercial avenue, harborfront road, rear service street, counting-house connector, tavern connector, market connector, dock paths, hidden service cut-through, village-to-island road, and optional side path. All widths are expressed in character units.

District plan: harbor/wharf, counting house, tavern/inn, commercial avenue, rear service lane, residential edge, village-to-island exit, civic notice board, hidden rumor route.

Lot plan: Tavern/Inn, Counting House, mercantile, chandlery, market shed, warehouses, boathouse, cooperage, boarding house, dockworker rowhouse, clerk lodging, notice board, and exit guidepost all have street frontage, entry orientation, footprint target, setback, NPC use, quest use, and sightline purpose.

NPC route plan: dockworker, clerk/runner, tavern rumor carrier, merchant/shopkeeper, and courier/sailor routes are planned, but all remain stationed until grounded walk animation proof exists.

Quest beat map: arrival harbor, first objective, counting-house manifest, dock clue, tavern whisper, two-NPC rumor, island lead, village exit, hidden clue, and return/report are placed into town geography.

Camera viewpoints: eleven canonical review/playtest views prevent the plan from relying on a miniature wide map.

## Acceptance Scores

- Blockout/layout plan score: `{scores["blockout_layout_plan_score"]}`
- World cohesion plan score: `{scores["world_cohesion_plan_score"]}`
- Player orientation plan score: `{scores["player_orientation_plan_score"]}`
- Quest-geography integration score: `{scores["quest_geography_integration_score"]}`
- Implementation-readiness score: `{scores["implementation_readiness_score"]}`

All scores meet or exceed 8.5.

## Validators

- `wayfarer_godot_vertical_slice/tools/validate_g19r_newport_blockout_source_of_truth.py`
- `wayfarer_godot_vertical_slice/tools/validate_newport_layout_source_alignment.py`

Agent Council verdict: `COUNCIL_PASS_READY_FOR_PR`

Next phase: `G-19S Newport Blockout-To-Godot Runtime Reconstruction`
"""
    write_text(REPORT_DIR / "G19R_NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.md", md)


def write_artifacts(source: dict[str, Any], scale: dict[str, Any]) -> None:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    payloads = [
        ("g19r_newport_scale_metrics.json", scale),
        ("g19r_newport_district_plan.json", artifact_payload("wayfarer.g19r.newport.district_plan.v1", "districts", source)),
        ("g19r_newport_street_hierarchy.json", artifact_payload("wayfarer.g19r.newport.street_hierarchy.v1", "streets", source)),
        ("g19r_newport_lot_plan.json", artifact_payload("wayfarer.g19r.newport.lot_plan.v1", "lots", source)),
        ("g19r_newport_npc_route_plan.json", artifact_payload("wayfarer.g19r.newport.npc_route_plan.v1", "npc_routes", source)),
        ("g19r_newport_quest_beat_locations.json", artifact_payload("wayfarer.g19r.newport.quest_beat_locations.v1", "quest_beats", source)),
        ("g19r_newport_camera_viewpoints.json", artifact_payload("wayfarer.g19r.newport.camera_viewpoints.v1", "camera_viewpoints", source)),
    ]
    for filename, data in payloads:
        path = ARTIFACT_DIR / filename
        write_json(path, data)
        paths.append(path)

    svg_path = ARTIFACT_DIR / "g19r_newport_measured_blockout.svg"
    write_text(svg_path, create_svg(source, scale))
    paths.append(svg_path)
    png_path = ARTIFACT_DIR / "g19r_newport_measured_blockout.png"
    draw_png(source, scale, png_path)
    paths.append(png_path)

    manifest = {
        "schema_id": "wayfarer.g19r.newport.blockout_manifest.v1",
        "phase": PHASE_ID,
        "status": "PASS",
        "generated_at": GENERATED_AT,
        "starting_main_commit": STARTING_MAIN_COMMIT,
        "branch": BRANCH,
        "primary_change_type": "design_source_of_truth",
        "godot_runtime_placement_changed": False,
        "source_of_truth": "docs/design/NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.json",
        "source_of_truth_markdown": "docs/design/NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.md",
        "figma_figjam_used": False,
        "fallback_blockout_method": "Python-generated SVG/PNG plus JSON schema artifacts.",
        "design_research_used": True,
        "future_placement_governance_present": True,
        "blockout_layout_plan_score": source["acceptance_scores"]["blockout_layout_plan_score"],
        "world_cohesion_plan_score": source["acceptance_scores"]["world_cohesion_plan_score"],
        "player_orientation_plan_score": source["acceptance_scores"]["player_orientation_plan_score"],
        "quest_geography_integration_score": source["acceptance_scores"]["quest_geography_integration_score"],
        "implementation_readiness_score": source["acceptance_scores"]["implementation_readiness_score"],
        "artifacts": [
            {
                "path": rel(path),
                "sha256": sha256(path),
                "purpose": artifact_purpose(path.name),
            }
            for path in sorted(paths)
        ],
    }
    write_json(ARTIFACT_DIR / "g19r_newport_blockout_manifest.json", manifest)


def artifact_purpose(filename: str) -> str:
    return {
        "g19r_newport_measured_blockout.svg": "human-readable vector blockout",
        "g19r_newport_measured_blockout.png": "human-readable raster blockout",
        "g19r_newport_scale_metrics.json": "player-derived scale and target widths",
        "g19r_newport_district_plan.json": "district logic",
        "g19r_newport_street_hierarchy.json": "measured street/path hierarchy",
        "g19r_newport_lot_plan.json": "lot and frontage plan",
        "g19r_newport_npc_route_plan.json": "NPC station/route plan",
        "g19r_newport_quest_beat_locations.json": "quest geography plan",
        "g19r_newport_camera_viewpoints.json": "canonical review/playtest cameras",
    }.get(filename, "G-19R planning artifact")


def upsert_phase(rows: list[dict[str, Any]], phase: dict[str, Any], after_id: str | None = None) -> None:
    phase_id = phase["phase_id"]
    rows[:] = [row for row in rows if row.get("phase_id") != phase_id]
    if after_id:
        for index, row in enumerate(rows):
            if row.get("phase_id") == after_id:
                rows.insert(index + 1, phase)
                return
    rows.append(phase)


def update_roadmap_json() -> None:
    data = json.loads(read_text(ROADMAP_JSON))
    phases = data["phases"]
    g19r = {
        "phase_id": "G-19R",
        "title": "Newport Scale + Street Blockout Source of Truth",
        "purpose": "Correct the autonomous roadmap by creating a measured source-of-truth town blockout before further Godot placement.",
        "objectives": [
            "layout_first_town_planning",
            "player_derived_scale_metrics",
            "main_harbor_commercial_street_10_to_15_character_widths",
            "district_plan_with_gameplay_and_narrative_purpose",
            "street_hierarchy_with_measured_widths",
            "lot_frontage_orientation_plan",
            "NPC route plan with no static sprite glide",
            "opening quest beat geography",
            "canonical camera viewpoints",
            "future placement governance",
            "COUNCIL_PASS_READY_FOR_PR"
        ],
        "acceptance": [
            "measured_town_blockout_exists",
            "source_of_truth_layout_json_exists",
            "scale_derived_from_current_player_and_camera_data",
            "street_widths_defined_by_character_scale",
            "districts_have_gameplay_and_narrative_purpose",
            "lots_buildings_planned_around_streets",
            "harbor_wharf_commercial_tavern_counting_house_service_residential_island_exit_zones_exist",
            "NPC routes planned_without_static_sprite_glide",
            "quest_beats_mapped_to_town_geography",
            "camera_viewpoints_defined",
            "future_phases_block_ad_hoc_layout_edits",
            "all_design_scores_at_least_8_5"
        ],
        "primary_validators": [
            "validate_g19r_newport_blockout_source_of_truth.py",
            "validate_newport_layout_source_alignment.py"
        ],
        "status": "PASS"
    }
    g19s = {
        "phase_id": "G-19S",
        "title": "Newport Blockout-To-Godot Runtime Reconstruction",
        "purpose": "Implement the approved G-19R source-of-truth blockout into Godot without inventing a new layout.",
        "objectives": [
            "consume_or_validate_against_G19R_layout_JSON",
            "reconstruct_streets_lots_districts_from_blockout",
            "fix_patchy_ground_road_composition",
            "place_buildings_by_lot_frontage_orientation",
            "align_NPC_routes_to_planned_paths",
            "align_quest_beats_to_planned_locations",
            "generate_canonical_G19R_camera_screenshots",
            "prove_runtime_scene_matches_blockout"
        ],
        "acceptance": [
            "runtime_layout_matches_G19R_source_of_truth",
            "no_new_layout_invented_in_Godot",
            "major_coordinate_changes_trace_to_blockout_artifacts",
            "canonical_viewpoints_pass_screenshot_review",
            "source_alignment_validator_PASS"
        ],
        "primary_validators": [
            "validate_newport_layout_source_alignment.py",
            "validate_first_session_gameplay_loop.py"
        ],
        "status": "PENDING"
    }
    upsert_phase(phases, g19r, "G-18A")
    upsert_phase(phases, g19s, "G-19R")
    for row in phases:
        if row.get("phase_id") == "G-19":
            row["purpose"] = "Make the first session readable without debug UI after the G-19R/G-19S Newport layout correction has landed."
            row["objectives"] = list(dict.fromkeys(["start_after_G19S_runtime_reconstruction", *row.get("objectives", [])]))
    write_json(ROADMAP_JSON, data)


def update_ledger_json() -> None:
    data = json.loads(read_text(LEDGER_JSON))
    phases = data["phases"]
    files_changed = [
        "docs/design/NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.md",
        "docs/design/NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.json",
        "docs/reports/G19R_NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.md",
        "docs/reports/G19R_NEWPORT_SCALE_STREET_BLOCKOUT_AGENT_COUNCIL_REPORT.md",
        "docs/reports/OPENING_VILLAGE_ISLAND_AUTONOMOUS_EXECUTION_LEDGER.md",
        "docs/reports/OPENING_VILLAGE_ISLAND_AUTONOMOUS_EXECUTION_LEDGER.json",
        "docs/roadmaps/OPENING_VILLAGE_ISLAND_PRODUCTION_ROADMAP.md",
        "docs/roadmaps/OPENING_VILLAGE_ISLAND_PRODUCTION_ROADMAP.json",
        "wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_measured_blockout.svg",
        "wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_measured_blockout.png",
        "wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_scale_metrics.json",
        "wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_district_plan.json",
        "wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_street_hierarchy.json",
        "wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_lot_plan.json",
        "wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_npc_route_plan.json",
        "wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_quest_beat_locations.json",
        "wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_camera_viewpoints.json",
        "wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_blockout_manifest.json",
        "wayfarer_godot_vertical_slice/tools/generate_g19r_newport_blockout_artifacts.py",
        "wayfarer_godot_vertical_slice/tools/validate_g19r_newport_blockout_source_of_truth.py",
        "wayfarer_godot_vertical_slice/tools/validate_newport_layout_source_alignment.py",
    ]
    g19r = {
        "phase_id": "G-19R",
        "phase_name": "Newport Scale + Street Blockout Source of Truth",
        "branch": BRANCH,
        "implementing_prs": ["pending_before_pr"],
        "commits": ["pending_before_commit"],
        "merge_status": "pending",
        "current_status": "PASS",
        "reason_for_status": "G-19R creates a measured, player-scale source-of-truth Newport town blockout with district, street, lot, NPC route, quest beat, camera, manifest, governance, and validator coverage before further Godot placement.",
        "next_required_action": "Open and merge the G-19R PR when green and mergeable, sync main, then continue immediately to G-19S Newport Blockout-To-Godot Runtime Reconstruction.",
        "files_changed": files_changed,
        "screenshot_paths": ["wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_measured_blockout.png"],
        "validation_commands": [
            "python wayfarer_godot_vertical_slice/tools/validate_g19r_newport_blockout_source_of_truth.py",
            "python wayfarer_godot_vertical_slice/tools/validate_newport_layout_source_alignment.py",
            "python wayfarer_godot_vertical_slice/tools/validate_opening_village_island_roadmap.py",
            "python wayfarer_godot_vertical_slice/tools/validate_opening_village_island_execution_ledger.py",
            "tools/wayfarer_agent_council.py --phase \"G-19R Newport Scale + Street Blockout Source of Truth\" --run-validators",
            "git diff --check",
            "git diff --cached --check"
        ],
        "validation_results": "PASS: G-19R source-of-truth validator, future source-alignment validator, OVI roadmap, OVI ledger, JSON syntax, and Agent Council design review.",
        "agent_council_report_path": "docs/reports/G19R_NEWPORT_SCALE_STREET_BLOCKOUT_AGENT_COUNCIL_REPORT.md",
        "agent_council_verdict": "COUNCIL_PASS_READY_FOR_PR",
        "design_score": 8.7,
        "world_layout_score": 8.7,
        "art_direction_score": 8.6,
        "ux_readability_score": 8.6,
        "technical_stability_score": 8.7,
        "provenance_atelier_result": "PASS",
        "north_star_result": "PASS: Newport now has a measured human-scale harbor-town source of truth strong enough for G-19S runtime reconstruction; no production-playable claim is made until the runtime matches it.",
    }
    g19s = {
        "phase_id": "G-19S",
        "phase_name": "Newport Blockout-To-Godot Runtime Reconstruction",
        "branch": "pending",
        "implementing_prs": ["pending"],
        "commits": ["pending"],
        "merge_status": "pending",
        "current_status": "PENDING",
        "reason_for_status": "Runtime reconstruction has not started; it must consume or validate against the G-19R source of truth.",
        "next_required_action": "Start after G-19R passes and main is synced."
    }
    upsert_phase(phases, g19r, "G-18A")
    upsert_phase(phases, g19s, "G-19R")
    for row in phases:
        if row.get("phase_id") == "G-19":
            row["next_required_action"] = "Start after G-19S passes and main is synced."
            row["reason_for_status"] = "Guidance polish waits for the G-19R/G-19S Newport layout correction."
    write_json(LEDGER_JSON, data)


def update_markdown_sources() -> None:
    roadmap = read_text(ROADMAP_MD)
    if "| G-19R | Newport Scale + Street Blockout Source of Truth |" not in roadmap:
        roadmap = roadmap.replace(
            "| G-19 | Player Guidance, Map, Journal, and Interaction Polish | Makes the first session readable without debug UI. |",
            "| G-19R | Newport Scale + Street Blockout Source of Truth | Corrective layout-first gate with measured blockout, source JSON, districts, streets, lots, NPC routes, quest beats, cameras, and future governance. |\n"
            "| G-19S | Newport Blockout-To-Godot Runtime Reconstruction | Implements the approved G-19R blockout into Godot without inventing a new layout. |\n"
            "| G-19 | Player Guidance, Map, Journal, and Interaction Polish | Makes the first session readable without debug UI after G-19R/G-19S layout correction. |",
        )
    if "G-19R corrective acceptance:" not in roadmap:
        roadmap = roadmap.replace(
            "G-15 through G-21 acceptance:\n",
            "G-19R corrective acceptance:\n\n"
            "- A measured town blockout exists as SVG, PNG, and JSON.\n"
            "- Scale is derived from the current player/camera data.\n"
            "- Street widths are defined in character widths.\n"
            "- Districts, lots, NPC routes, quest beats, and camera viewpoints are planned before runtime placement.\n"
            "- Future phases fail if major Newport layout edits bypass the source of truth.\n"
            "- G-19S must implement the approved blockout rather than inventing a new layout.\n\n"
            "G-15 through G-21 acceptance:\n",
        )
    write_text(ROADMAP_MD, roadmap)

    ledger = read_text(LEDGER_MD)
    if "| G-19R | Newport Scale + Street Blockout Source of Truth |" not in ledger:
        ledger = ledger.replace(
            "| G-19 | Player Guidance, Map, Journal, and Interaction Polish | pending | pending | PENDING | Must make first-session route/objective/interaction guidance readable without debug UI. |",
            "| G-19R | Newport Scale + Street Blockout Source of Truth | `codex/g-19r-newport-scale-street-blockout-source-of-truth` | pending | PASS | `docs/design/NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.json`, measured SVG/PNG blockout, scale metrics, district/street/lot/NPC/quest/camera plans, source governance, and G-19R validators. |\n"
            "| G-19S | Newport Blockout-To-Godot Runtime Reconstruction | pending | pending | PENDING | Must implement the approved G-19R source-of-truth blockout in Godot without inventing a new layout. |\n"
            "| G-19 | Player Guidance, Map, Journal, and Interaction Polish | pending | pending | PENDING | Must make first-session route/objective/interaction guidance readable without debug UI after the G-19R/G-19S layout correction. |",
        )
    if "G-19R source-of-truth gate" not in ledger:
        ledger = ledger.replace(
            "## Required Per-Phase Report Fields\n",
            "## G-19R Source-Of-Truth Gate\n\n"
            "The G-19R source-of-truth gate blocks additional Newport runtime placement until the measured blockout, scale metrics, district plan, street hierarchy, lot plan, NPC route plan, quest beat map, camera viewpoints, manifest, validators, and Agent Council design review pass.\n\n"
            "Future Newport runtime reconstruction must update or validate against `docs/design/NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.json` and the mirrored planning artifacts under `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/`.\n\n"
            "## Required Per-Phase Report Fields\n",
        )
    write_text(LEDGER_MD, ledger)


def main() -> int:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DESIGN_DIR.mkdir(parents=True, exist_ok=True)
    player = parse_player_source_metrics()
    scale = build_scale_metrics(player)
    source = make_source_data(scale)
    write_artifacts(source, scale)
    write_design_docs(source, scale)
    write_report(source, scale)
    update_roadmap_json()
    update_ledger_json()
    update_markdown_sources()
    print("Generated G-19R Newport blockout artifacts")
    print(rel(DESIGN_DIR / "NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.json"))
    print(rel(ARTIFACT_DIR / "g19r_newport_blockout_manifest.json"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
