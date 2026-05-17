#!/usr/bin/env python3
"""Generate the G-4.19 player visual identity foundation assets.

The G-4.19 player is source-authored and deterministic: no web, marketplace,
third-party, or yellow review pixels are used. The script creates the runtime
atlas, a contact sheet, a manifest, and a QA report, then updates the Newport
visual production registry so the old drawn placeholder is no longer treated as
the normal-review player target.
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


PHASE = "G-4.19"
FAMILY_ID = "player_wayfarer_foundation_g419"
FRAME_SIZE = 64
FRAME_COLUMNS = 3
DIRECTIONS = ["down", "up", "left", "right"]
FRAME_KINDS = ["idle", "walk_a", "walk_b"]

SCRIPT_PATH = Path(__file__).resolve()
PLAYER_ROOT = SCRIPT_PATH.parents[1]
PROJECT_ROOT = PLAYER_ROOT.parents[1]
REPO_ROOT = PROJECT_ROOT.parent
SOURCE_DIR = PLAYER_ROOT / "source_authored"
ATLAS_DIR = PLAYER_ROOT / "atlases"
GENERATED_DIR = PLAYER_ROOT / "generated"
CONTACT_DIR = PLAYER_ROOT / "contact_sheets"
MANIFEST_DIR = PLAYER_ROOT / "manifests"
REPORT_DIR = PLAYER_ROOT / "reports"
DOC_REPORT_DIR = REPO_ROOT / "docs" / "reports"
REGISTRY_PATH = PROJECT_ROOT / "art_pipeline" / "newport" / "manifests" / "newport_visual_production_registry.json"

ATLAS_PATH = ATLAS_DIR / "player_wayfarer_foundation_g419_v1.png"
SOURCE_GRID_PATH = GENERATED_DIR / "player_wayfarer_foundation_g419_source_grid.png"
CONTACT_SHEET_PATH = CONTACT_DIR / "player_wayfarer_foundation_g419_contact_sheet.png"
MANIFEST_PATH = MANIFEST_DIR / "player_wayfarer_foundation_g419_manifest.json"
QA_REPORT_PATH = REPORT_DIR / "player_wayfarer_foundation_g419_extraction_qa.json"
STYLE_TOKENS_PATH = SOURCE_DIR / "g419_player_identity_style_tokens.json"
BRIEF_PATH = SOURCE_DIR / "g419_player_visual_identity_brief.md"
PHASE_REPORT_PATH = DOC_REPORT_DIR / "G419_PLAYER_VISUAL_IDENTITY_FOUNDATION.md"


PALETTE = {
    "outline": "#15191b",
    "outline_soft": "#283033",
    "shadow": (0, 0, 0, 72),
    "skin": "#d6a978",
    "skin_light": "#edc493",
    "skin_shadow": "#9a694d",
    "hair": "#352519",
    "hair_hi": "#5a3921",
    "coat": "#26384a",
    "coat_shadow": "#182633",
    "coat_hi": "#3d5872",
    "shirt": "#e6d7b8",
    "shirt_shadow": "#bba77d",
    "scarf": "#2c8a82",
    "scarf_hi": "#5bb7aa",
    "belt": "#69472a",
    "belt_hi": "#ad7c45",
    "trousers": "#3f4d50",
    "trousers_shadow": "#293336",
    "boot": "#251d18",
    "boot_hi": "#4d3526",
    "satchel": "#8b5d31",
    "satchel_hi": "#bd8751",
    "brass": "#d7b65c",
}


def ensure_dirs() -> None:
    for path in [SOURCE_DIR, ATLAS_DIR, GENERATED_DIR, CONTACT_DIR, MANIFEST_DIR, REPORT_DIR, DOC_REPORT_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def rgba(color: str | tuple[int, int, int, int], alpha: int | None = None) -> tuple[int, int, int, int]:
    if isinstance(color, tuple):
        return color
    color = color.lstrip("#")
    r = int(color[0:2], 16)
    g = int(color[2:4], 16)
    b = int(color[4:6], 16)
    return (r, g, b, 255 if alpha is None else alpha)


def rect(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill: str, outline: str | None = None) -> None:
    draw.rectangle(box, fill=rgba(fill), outline=rgba(outline) if outline else None)


def ellipse(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill: str | tuple[int, int, int, int], outline: str | None = None) -> None:
    draw.ellipse(box, fill=rgba(fill), outline=rgba(outline) if outline else None)


def poly(draw: ImageDraw.ImageDraw, points: list[tuple[int, int]], fill: str, outline: str | None = None) -> None:
    draw.polygon(points, fill=rgba(fill), outline=rgba(outline) if outline else None)


def line(draw: ImageDraw.ImageDraw, points: list[tuple[int, int]], fill: str, width: int = 1) -> None:
    draw.line(points, fill=rgba(fill), width=width)


def draw_shadow(draw: ImageDraw.ImageDraw, step: int) -> None:
    wobble = 1 if step == 1 else (-1 if step == 2 else 0)
    ellipse(draw, (19 + wobble, 51, 45 + wobble, 60), PALETTE["shadow"])
    ellipse(draw, (24 + wobble, 53, 40 + wobble, 58), (0, 0, 0, 44))


def leg_positions(direction: str, step: int) -> tuple[tuple[int, int, int, int], tuple[int, int, int, int]]:
    if direction in {"down", "up"}:
        if step == 1:
            return (23, 41, 30, 56), (34, 41, 41, 53)
        if step == 2:
            return (24, 41, 31, 53), (34, 41, 41, 56)
        return (25, 41, 31, 54), (33, 41, 39, 54)
    if step == 1:
        return (27, 42, 33, 56), (36, 42, 42, 52)
    if step == 2:
        return (27, 42, 33, 52), (36, 42, 42, 56)
    return (29, 42, 35, 54), (35, 42, 41, 54)


def draw_boots(draw: ImageDraw.ImageDraw, legs: tuple[tuple[int, int, int, int], tuple[int, int, int, int]], facing_left: bool = False) -> None:
    for i, leg in enumerate(legs):
        x0, _y0, x1, y1 = leg
        toe = -3 if facing_left else 3
        if i == 0 and facing_left:
            toe = -4
        elif i == 1 and not facing_left:
            toe = 4
        rect(draw, (x0, y1 - 4, x1, y1), PALETTE["boot"], PALETTE["outline"])
        rect(draw, (min(x0, x0 + toe), y1 - 2, max(x1, x1 + toe), y1 + 1), PALETTE["boot"], PALETTE["outline"])
        line(draw, [(x0 + 1, y1 - 4), (x1 - 1, y1 - 4)], PALETTE["boot_hi"])


def draw_down(draw: ImageDraw.ImageDraw, step: int) -> None:
    draw_shadow(draw, step)
    bob = -1 if step == 1 else (1 if step == 2 else 0)
    legs = leg_positions("down", step)
    for leg in legs:
        rect(draw, leg, PALETTE["trousers_shadow"], PALETTE["outline"])
        rect(draw, (leg[0] + 1, leg[1], leg[2] - 1, leg[3] - 5), PALETTE["trousers"])
    draw_boots(draw, legs)

    poly(draw, [(21, 25 + bob), (43, 25 + bob), (46, 43 + bob), (39, 49 + bob), (25, 49 + bob), (18, 43 + bob)], PALETTE["coat"], PALETTE["outline"])
    poly(draw, [(25, 27 + bob), (39, 27 + bob), (38, 43 + bob), (32, 47 + bob), (26, 43 + bob)], PALETTE["coat_hi"], None)
    rect(draw, (28, 28 + bob, 36, 42 + bob), PALETTE["shirt"], PALETTE["outline_soft"])
    rect(draw, (24, 39 + bob, 40, 43 + bob), PALETTE["belt"], PALETTE["outline"])
    rect(draw, (31, 39 + bob, 34, 42 + bob), PALETTE["brass"])
    poly(draw, [(27, 27 + bob), (32, 33 + bob), (37, 27 + bob), (34, 36 + bob), (30, 36 + bob)], PALETTE["scarf"], PALETTE["outline_soft"])
    line(draw, [(31, 29 + bob), (34, 34 + bob)], PALETTE["scarf_hi"])

    arm_swing = 2 if step == 1 else (-2 if step == 2 else 0)
    rect(draw, (16, 28 + bob - arm_swing, 22, 43 + bob - arm_swing), PALETTE["coat_shadow"], PALETTE["outline"])
    rect(draw, (42, 28 + bob + arm_swing, 48, 43 + bob + arm_swing), PALETTE["coat_shadow"], PALETTE["outline"])
    ellipse(draw, (16, 42 + bob - arm_swing, 22, 48 + bob - arm_swing), PALETTE["skin"], PALETTE["outline_soft"])
    ellipse(draw, (42, 42 + bob + arm_swing, 48, 48 + bob + arm_swing), PALETTE["skin"], PALETTE["outline_soft"])

    ellipse(draw, (23, 9 + bob, 41, 27 + bob), PALETTE["skin"], PALETTE["outline"])
    rect(draw, (25, 20 + bob, 39, 27 + bob), PALETTE["skin_light"])
    poly(draw, [(23, 14 + bob), (26, 8 + bob), (38, 7 + bob), (42, 14 + bob), (40, 17 + bob), (34, 13 + bob), (27, 16 + bob)], PALETTE["hair"], PALETTE["outline"])
    rect(draw, (28, 17 + bob, 30, 19 + bob), PALETTE["outline"])
    rect(draw, (35, 17 + bob, 37, 19 + bob), PALETTE["outline"])
    rect(draw, (30, 23 + bob, 36, 24 + bob), PALETTE["skin_shadow"])
    line(draw, [(27, 11 + bob), (36, 9 + bob)], PALETTE["hair_hi"])


def draw_up(draw: ImageDraw.ImageDraw, step: int) -> None:
    draw_shadow(draw, step)
    bob = -1 if step == 1 else (1 if step == 2 else 0)
    legs = leg_positions("up", step)
    for leg in legs:
        rect(draw, leg, PALETTE["trousers_shadow"], PALETTE["outline"])
        rect(draw, (leg[0] + 1, leg[1], leg[2] - 1, leg[3] - 5), PALETTE["trousers"])
    draw_boots(draw, legs)

    poly(draw, [(21, 25 + bob), (43, 25 + bob), (46, 43 + bob), (39, 49 + bob), (25, 49 + bob), (18, 43 + bob)], PALETTE["coat_shadow"], PALETTE["outline"])
    poly(draw, [(25, 27 + bob), (39, 27 + bob), (41, 43 + bob), (32, 48 + bob), (23, 43 + bob)], PALETTE["coat"], None)
    line(draw, [(31, 28 + bob), (31, 46 + bob)], PALETTE["coat_hi"])
    rect(draw, (22, 37 + bob, 40, 41 + bob), PALETTE["belt"], PALETTE["outline"])
    poly(draw, [(39, 29 + bob), (47, 34 + bob), (45, 45 + bob), (38, 43 + bob)], PALETTE["satchel"], PALETTE["outline"])
    line(draw, [(40, 31 + bob), (45, 37 + bob)], PALETTE["satchel_hi"])

    arm_swing = 2 if step == 1 else (-2 if step == 2 else 0)
    rect(draw, (16, 28 + bob + arm_swing, 22, 44 + bob + arm_swing), PALETTE["coat_shadow"], PALETTE["outline"])
    rect(draw, (42, 28 + bob - arm_swing, 48, 44 + bob - arm_swing), PALETTE["coat_shadow"], PALETTE["outline"])
    ellipse(draw, (16, 42 + bob + arm_swing, 22, 48 + bob + arm_swing), PALETTE["skin_shadow"], PALETTE["outline_soft"])
    ellipse(draw, (42, 42 + bob - arm_swing, 48, 48 + bob - arm_swing), PALETTE["skin_shadow"], PALETTE["outline_soft"])

    ellipse(draw, (23, 9 + bob, 41, 27 + bob), PALETTE["hair"], PALETTE["outline"])
    poly(draw, [(24, 16 + bob), (27, 8 + bob), (37, 8 + bob), (41, 16 + bob), (39, 24 + bob), (32, 27 + bob), (25, 24 + bob)], PALETTE["hair"], None)
    line(draw, [(27, 11 + bob), (37, 12 + bob), (39, 18 + bob)], PALETTE["hair_hi"])
    poly(draw, [(25, 26 + bob), (32, 32 + bob), (39, 26 + bob), (36, 34 + bob), (28, 34 + bob)], PALETTE["scarf"], PALETTE["outline_soft"])


def draw_side(draw: ImageDraw.ImageDraw, step: int, facing_left: bool) -> None:
    draw_shadow(draw, step)
    bob = -1 if step == 1 else (1 if step == 2 else 0)
    mirror = -1 if facing_left else 1
    legs = leg_positions("left" if facing_left else "right", step)
    for leg in legs:
        rect(draw, leg, PALETTE["trousers_shadow"], PALETTE["outline"])
        rect(draw, (leg[0] + 1, leg[1], leg[2] - 1, leg[3] - 5), PALETTE["trousers"])
    draw_boots(draw, legs, facing_left)

    # Coat, collar, and scarf are drawn symmetrically enough to read after mirror.
    poly(draw, [(24, 25 + bob), (41, 26 + bob), (45, 42 + bob), (39, 49 + bob), (27, 48 + bob), (21, 42 + bob)], PALETTE["coat"], PALETTE["outline"])
    rect(draw, (29, 28 + bob, 38, 42 + bob), PALETTE["shirt"], PALETTE["outline_soft"])
    rect(draw, (25, 39 + bob, 42, 43 + bob), PALETTE["belt"], PALETTE["outline"])
    rect(draw, (36 if facing_left else 29, 39 + bob, 39 if facing_left else 32, 42 + bob), PALETTE["brass"])
    if facing_left:
        poly(draw, [(35, 27 + bob), (29, 34 + bob), (35, 36 + bob), (39, 28 + bob)], PALETTE["scarf"], PALETTE["outline_soft"])
    else:
        poly(draw, [(29, 27 + bob), (35, 34 + bob), (29, 36 + bob), (25, 28 + bob)], PALETTE["scarf"], PALETTE["outline_soft"])

    arm_swing = 2 if step == 1 else (-2 if step == 2 else 0)
    front_x = 20 if facing_left else 42
    back_x = 41 if facing_left else 18
    rect(draw, (front_x, 28 + bob + arm_swing, front_x + 6, 43 + bob + arm_swing), PALETTE["coat_shadow"], PALETTE["outline"])
    rect(draw, (back_x, 28 + bob - arm_swing, back_x + 6, 43 + bob - arm_swing), PALETTE["coat_shadow"], PALETTE["outline"])
    ellipse(draw, (front_x, 42 + bob + arm_swing, front_x + 6, 48 + bob + arm_swing), PALETTE["skin"], PALETTE["outline_soft"])

    head_box = (23, 9 + bob, 41, 27 + bob)
    ellipse(draw, head_box, PALETTE["skin"], PALETTE["outline"])
    if facing_left:
        poly(draw, [(40, 11 + bob), (35, 7 + bob), (25, 9 + bob), (22, 15 + bob), (24, 22 + bob), (32, 16 + bob), (39, 17 + bob)], PALETTE["hair"], PALETTE["outline"])
        rect(draw, (25, 17 + bob, 27, 19 + bob), PALETTE["outline"])
        rect(draw, (23, 22 + bob, 29, 24 + bob), PALETTE["skin_shadow"])
        rect(draw, (23, 18 + bob, 26, 21 + bob), PALETTE["skin_light"])
        line(draw, [(35, 10 + bob), (27, 11 + bob)], PALETTE["hair_hi"])
    else:
        poly(draw, [(24, 11 + bob), (29, 7 + bob), (39, 9 + bob), (42, 15 + bob), (40, 22 + bob), (32, 16 + bob), (25, 17 + bob)], PALETTE["hair"], PALETTE["outline"])
        rect(draw, (37, 17 + bob, 39, 19 + bob), PALETTE["outline"])
        rect(draw, (35, 22 + bob, 41, 24 + bob), PALETTE["skin_shadow"])
        rect(draw, (38, 18 + bob, 41, 21 + bob), PALETTE["skin_light"])
        line(draw, [(29, 10 + bob), (37, 11 + bob)], PALETTE["hair_hi"])

    satchel_x = 38 if facing_left else 20
    poly(draw, [(satchel_x, 32 + bob), (satchel_x + 7, 35 + bob), (satchel_x + 6, 45 + bob), (satchel_x - 1, 43 + bob)], PALETTE["satchel"], PALETTE["outline"])
    line(draw, [(satchel_x + 1, 34 + bob), (satchel_x + 6, 39 + bob)], PALETTE["satchel_hi"])


def render_frame(direction: str, kind: str) -> Image.Image:
    step = 0 if kind == "idle" else (1 if kind == "walk_a" else 2)
    image = Image.new("RGBA", (FRAME_SIZE, FRAME_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    if direction == "down":
        draw_down(draw, step)
    elif direction == "up":
        draw_up(draw, step)
    elif direction == "left":
        draw_side(draw, step, True)
    elif direction == "right":
        draw_side(draw, step, False)
    else:
        raise ValueError(direction)
    return image


def generate_atlas() -> tuple[Image.Image, list[dict[str, Any]]]:
    atlas = Image.new("RGBA", (FRAME_COLUMNS * FRAME_SIZE, len(DIRECTIONS) * FRAME_SIZE), (0, 0, 0, 0))
    frames: list[dict[str, Any]] = []
    for row, direction in enumerate(DIRECTIONS):
        for col, kind in enumerate(FRAME_KINDS):
            frame = render_frame(direction, kind)
            x = col * FRAME_SIZE
            y = row * FRAME_SIZE
            atlas.alpha_composite(frame, (x, y))
            frames.append(
                {
                    "id": f"{kind}_{direction}",
                    "animation": f"{'idle' if kind == 'idle' else 'walk'}_{direction}",
                    "kind": kind,
                    "direction": direction,
                    "region": {"x": x, "y": y, "w": FRAME_SIZE, "h": FRAME_SIZE},
                    "foot_anchor": {"x": 32, "y": 56},
                    "body_bounds": {"x": 16, "y": 7, "w": 32, "h": 52},
                    "contact_shadow": True,
                }
            )
    return atlas, frames


def write_style_tokens() -> None:
    tokens = {
        "schema_id": "wayfarer.player_identity.g419.style_tokens.v1",
        "phase": PHASE,
        "family_id": FAMILY_ID,
        "generation_method": "project-owned deterministic Python/Pillow source authored in repo",
        "source_pixels_from_yellow_or_third_party_assets": False,
        "visual_direction": {
            "identity": "Newport harbor-town wayfarer: readable human adventurer, grounded in colonial-fantasy port clothes without ornate MMO armor.",
            "silhouette": "small human-scale figure with coat taper, boots, satchel, teal scarf accent, and dark hair.",
            "scale_goal": "roughly 40-44 visible pixels tall in-game after runtime scale, smaller than door height and readable at gameplay zoom.",
            "future_hooks": ["outfit colorways", "equipment overlays", "tool poses", "NPC differentiation", "multiplayer readability"],
        },
        "palette": {key: (value if isinstance(value, str) else list(value)) for key, value in PALETTE.items()},
        "runtime_anchor": {"foot_anchor": [32, 56], "frame_size": [FRAME_SIZE, FRAME_SIZE], "recommended_visual_scale": 0.82},
    }
    STYLE_TOKENS_PATH.write_text(json.dumps(tokens, indent=2) + "\n", encoding="utf-8")


def write_brief() -> None:
    BRIEF_PATH.write_text(
        "\n".join(
            [
                "# G-4.19 Player Visual Identity Brief",
                "",
                "Generation mode: project-owned deterministic source-authored sprite script.",
                "No image model prompt, web source, marketplace source, yellow review pixels, or third-party pixels are used.",
                "",
                "The player should read as a human-scale Wayfarer who belongs in the accepted Newport harbor town: muted navy wool coat, cream shirt, leather boots, satchel, and teal scarf accent. The foundation is intentionally restrained so later passes can add equipment, outfits, tools, class cues, and multiplayer/NPC differentiation without replacing the runtime contract.",
                "",
                "Required animations for this pass: idle_down, idle_up, idle_left, idle_right, walk_down, walk_up, walk_left, walk_right.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def write_contact_sheet(atlas: Image.Image, frames: list[dict[str, Any]]) -> None:
    scale = 3
    pad = 18
    row_label_w = 72
    label_h = 20
    sheet_w = row_label_w + FRAME_COLUMNS * FRAME_SIZE * scale + pad * 2
    sheet_h = len(DIRECTIONS) * (FRAME_SIZE * scale + label_h) + pad * 2 + 42
    sheet = Image.new("RGBA", (sheet_w, sheet_h), rgba("#2b2b25"))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 14)
        title_font = ImageFont.truetype("arial.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
        title_font = font
    draw.text((pad, 10), "G-4.19 Player Visual Identity Foundation - directional atlas/contact proof", fill=rgba("#f0e4c7"), font=title_font)
    draw.text((pad, 30), "Project-owned deterministic source; runtime animations: idle and walk in four directions", fill=rgba("#bfc6b8"), font=font)
    y0 = pad + 42
    for row, direction in enumerate(DIRECTIONS):
        row_y = y0 + row * (FRAME_SIZE * scale + label_h)
        draw.text((pad, row_y + label_h + 8), direction.upper(), fill=rgba("#f0e4c7"), font=font)
        for col, kind in enumerate(FRAME_KINDS):
            x = pad + row_label_w + col * FRAME_SIZE * scale
            label = f"{kind}_{direction}"
            frame = atlas.crop((col * FRAME_SIZE, row * FRAME_SIZE, (col + 1) * FRAME_SIZE, (row + 1) * FRAME_SIZE)).resize((FRAME_SIZE * scale, FRAME_SIZE * scale), Image.Resampling.NEAREST)
            sheet.alpha_composite(frame, (x, row_y + label_h))
            draw.rectangle((x, row_y + label_h, x + FRAME_SIZE * scale, row_y + label_h + FRAME_SIZE * scale), outline=rgba("#83785a"))
            draw.text((x + 4, row_y + 4), label, fill=rgba("#d9c891"), font=font)
    sheet.save(CONTACT_SHEET_PATH)


def alpha_bounds(image: Image.Image) -> dict[str, int]:
    alpha = image.getchannel("A")
    bbox = alpha.getbbox()
    if bbox is None:
        return {"x": 0, "y": 0, "w": 0, "h": 0}
    x0, y0, x1, y1 = bbox
    return {"x": x0, "y": y0, "w": x1 - x0, "h": y1 - y0}


def write_manifest(frames: list[dict[str, Any]], atlas: Image.Image) -> None:
    manifest = {
        "schema_id": "wayfarer.player_identity.g419.manifest.v1",
        "phase": PHASE,
        "family_id": FAMILY_ID,
        "status": "APPROVED_TEMPORARY",
        "origin_classification": "project_owned_deterministic_source_authored",
        "provenance_status": "green_origin_project_authored",
        "commercial_use_status": "not_final_commercial_promoted",
        "source_pixels_from_yellow_uncertain_assets": False,
        "source_pixels_from_third_party_material": False,
        "web_scraped_source_pixels": False,
        "runtime_asset": "art_pipeline/player_identity/atlases/player_wayfarer_foundation_g419_v1.png",
        "source_grid": "art_pipeline/player_identity/generated/player_wayfarer_foundation_g419_source_grid.png",
        "contact_sheet": "art_pipeline/player_identity/contact_sheets/player_wayfarer_foundation_g419_contact_sheet.png",
        "style_tokens": "art_pipeline/player_identity/source_authored/g419_player_identity_style_tokens.json",
        "brief": "art_pipeline/player_identity/source_authored/g419_player_visual_identity_brief.md",
        "generation_script": "art_pipeline/player_identity/scripts/generate_g419_player_identity_assets.py",
        "validation_script": "art_pipeline/player_identity/scripts/validate_g419_player_identity.py",
        "frame_size": {"w": FRAME_SIZE, "h": FRAME_SIZE},
        "atlas_dimensions": {"w": atlas.width, "h": atlas.height},
        "runtime_scale": 0.82,
        "animations": {
            "idle_down": ["idle_down"],
            "idle_up": ["idle_up"],
            "idle_left": ["idle_left"],
            "idle_right": ["idle_right"],
            "walk_down": ["idle_down", "walk_a_down", "idle_down", "walk_b_down"],
            "walk_up": ["idle_up", "walk_a_up", "idle_up", "walk_b_up"],
            "walk_left": ["idle_left", "walk_a_left", "idle_left", "walk_b_left"],
            "walk_right": ["idle_right", "walk_a_right", "idle_right", "walk_b_right"],
        },
        "frames": frames,
        "extensibility": {
            "equipment_layers": "Future overlays should share the 64x64 frame contract and foot anchor.",
            "outfit_variants": "Palette swaps or authored replacement atlases can reuse the same Player.gd animation contract.",
            "npc_differentiation": "NPCs should inherit the scale/anchor standard while changing silhouette, clothes, and readable accents.",
        },
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def write_qa_report(atlas: Image.Image, frames: list[dict[str, Any]]) -> None:
    frame_reports = []
    failures: list[str] = []
    for frame in frames:
        region = frame["region"]
        crop = atlas.crop((region["x"], region["y"], region["x"] + region["w"], region["y"] + region["h"]))
        bounds = alpha_bounds(crop)
        alpha = crop.getchannel("A")
        alpha_bytes = alpha.tobytes()
        coverage = sum(1 for value in alpha_bytes if value > 0)
        opaque = sum(1 for value in alpha_bytes if value > 220)
        if bounds["w"] <= 0 or bounds["h"] <= 0:
            failures.append(f"{frame['id']} blank")
        if bounds["x"] < 8 or bounds["x"] + bounds["w"] > 56 or bounds["y"] < 4 or bounds["y"] + bounds["h"] > 62:
            failures.append(f"{frame['id']} unsafe bounds {bounds}")
        if not (500 <= coverage <= 1350):
            failures.append(f"{frame['id']} unexpected alpha coverage {coverage}")
        if opaque < 280:
            failures.append(f"{frame['id']} too little opaque body coverage {opaque}")
        frame_reports.append({"id": frame["id"], "alpha_bounds": bounds, "alpha_coverage": coverage, "opaque_pixels": opaque})

    required_animations = [
        "idle_down",
        "idle_up",
        "idle_left",
        "idle_right",
        "walk_down",
        "walk_up",
        "walk_left",
        "walk_right",
    ]
    report = {
        "schema_id": "wayfarer.player_identity.g419.extraction_qa.v1",
        "phase": PHASE,
        "family_id": FAMILY_ID,
        "status": "PASS" if not failures else "FAIL",
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "atlas_path": "art_pipeline/player_identity/atlases/player_wayfarer_foundation_g419_v1.png",
        "contact_sheet_path": "art_pipeline/player_identity/contact_sheets/player_wayfarer_foundation_g419_contact_sheet.png",
        "required_animations": required_animations,
        "frames_checked": len(frames),
        "frame_reports": frame_reports,
        "failures": failures,
        "provenance": {
            "project_owned_deterministic_source": True,
            "third_party_pixels": False,
            "yellow_review_pixels": False,
            "web_scraped_pixels": False,
            "final_commercial_promoted": False,
        },
    }
    QA_REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("G-4.19 QA failed: " + "; ".join(failures))


def update_visual_registry() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    registry["phase"] = PHASE
    registry["generated_at"] = dt.date.today().isoformat()
    registry["policy"] = (
        "G-4.19 establishes the Player Visual Identity Foundation under the autonomous pre-G-5 protocol. "
        "The active player sprite family is project-owned deterministic source-authored art, not final-commercial promoted, "
        "with preserved script, style tokens, manifest, contact sheet, QA, and runtime integration. "
        "The old drawn player placeholder is deprecated from normal review."
    )
    for wave in registry.get("production_wave_plan", []):
        if wave.get("wave_id") == "wave_5_character_npc_standard":
            wave["status"] = "in_progress_g419_player_visual_identity_foundation"
            wave["acceptance_note"] = (
                "G-4.19 establishes the player visual identity foundation first: directional idle/walk contract, "
                "human-scale Newport grounding, and a repeatable provenance-safe character asset path. NPC variants remain future work."
            )
            wave["accepted_pack_count"] = 1
            wave["accepted_asset_count"] = 1

    entries = registry.setdefault("asset_entries", [])
    for entry in entries:
        if entry.get("asset_id") == "player_placeholder_drawn":
            entry["current_usage"] = {
                "normal_review": False,
                "lab_only": False,
                "runtime_target": "Deprecated by G-4.19 player_wayfarer_foundation_g419",
                "usage_notes": "Historical drawn scale/debug avatar only; not active in normal review after G-4.19.",
            }
            entry["rebuild_status"] = "DEPRECATED_DO_NOT_USE"
            entry["deprecated_visual_target"] = True
            entry["notes"] = "Replaced by the G-4.19 Player Visual Identity Foundation directional sprite atlas."

    new_entry = {
        "asset_id": FAMILY_ID,
        "name": "Wayfarer Player Visual Identity Foundation",
        "category": "CHARACTER_PLAYER_SPRITE_FOUNDATION",
        "path": "art_pipeline/player_identity/atlases/player_wayfarer_foundation_g419_v1.png",
        "source_provenance_status": "green_origin_project_authored_deterministic",
        "current_usage": {
            "normal_review": True,
            "lab_only": False,
            "runtime_target": "Player AnimatedSprite2D Visual node",
            "usage_notes": "Active normal-review player sprite foundation for G-4.19; final-commercial promotion remains a later art/legal gate.",
        },
        "visual_quality_status": "APPROVED_TEMPORARY",
        "gameplay_role": "Readable human-scale player identity, directional idle/walk foundation, collision/camera/interaction compatible.",
        "rebuild_status": "APPROVED_TEMPORARY",
        "player_identity_artifacts": {
            "manifest": "art_pipeline/player_identity/manifests/player_wayfarer_foundation_g419_manifest.json",
            "style_tokens": "art_pipeline/player_identity/source_authored/g419_player_identity_style_tokens.json",
            "brief": "art_pipeline/player_identity/source_authored/g419_player_visual_identity_brief.md",
            "generation_script": "art_pipeline/player_identity/scripts/generate_g419_player_identity_assets.py",
            "validation_script": "art_pipeline/player_identity/scripts/validate_g419_player_identity.py",
            "atlas": "art_pipeline/player_identity/atlases/player_wayfarer_foundation_g419_v1.png",
            "contact_sheet": "art_pipeline/player_identity/contact_sheets/player_wayfarer_foundation_g419_contact_sheet.png",
            "validation_report": "art_pipeline/player_identity/reports/player_wayfarer_foundation_g419_extraction_qa.json",
        },
        "animation_contract": [
            "idle_down",
            "idle_up",
            "idle_left",
            "idle_right",
            "walk_down",
            "walk_up",
            "walk_left",
            "walk_right",
        ],
        "provenance_detail": {
            "project_owned_deterministic_source": True,
            "source_pixels_from_yellow_uncertain_assets": False,
            "source_pixels_from_third_party_material": False,
            "web_scraped_source_pixels": False,
            "final_commercial_promoted": False,
        },
        "notes": "G-4.19 staged character foundation. It belongs with Newport at gameplay zoom and preserves future outfit/equipment/NPC expansion hooks without claiming final-commercial art status.",
    }
    existing_index = next((i for i, entry in enumerate(entries) if entry.get("asset_id") == FAMILY_ID), None)
    if existing_index is None:
        entries.append(new_entry)
    else:
        entries[existing_index] = new_entry
    REGISTRY_PATH.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")


def write_phase_report() -> None:
    PHASE_REPORT_PATH.write_text(
        "\n".join(
            [
                "# G-4.19 Player Visual Identity Foundation",
                "",
                "Status: implementation candidate pending validation, runtime screenshots, and Agent Council authority verdict.",
                "",
                "G-4.19 replaces the drawn scale/debug player placeholder with a source-authored directional player sprite foundation. The active player now has a real runtime atlas, contact sheet, manifest, QA report, and animation contract for idle/walk in four directions.",
                "",
                "## Scope",
                "",
                "- Active player sprite foundation: `player_wayfarer_foundation_g419`.",
                "- Runtime animations: `idle_down`, `idle_up`, `idle_left`, `idle_right`, `walk_down`, `walk_up`, `walk_left`, `walk_right`.",
                "- Integration target: `Player.tscn` uses an `AnimatedSprite2D` visual node; `Player.gd` drives facing and walk/idle state while preserving camera, collision, spawn, and interaction hooks.",
                "- Provenance: project-owned deterministic source-authored art. No yellow review pixels, third-party pixels, web-scraped pixels, or marketplace material are used.",
                "- Commercial status: approved temporary foundation only; not final-commercial promoted.",
                "",
                "## Art Direction",
                "",
                "The player reads as a Newport harbor-town wayfarer: muted navy coat, leather boots, cream shirt, satchel, teal scarf accent, and grounded human scale. The silhouette is intentionally restrained so later equipment, outfits, tools, NPC differentiation, and multiplayer readability can extend the same frame contract.",
                "",
                "## Evidence Package",
                "",
                "- Atlas: `wayfarer_godot_vertical_slice/art_pipeline/player_identity/atlases/player_wayfarer_foundation_g419_v1.png`.",
                "- Contact sheet: `wayfarer_godot_vertical_slice/art_pipeline/player_identity/contact_sheets/player_wayfarer_foundation_g419_contact_sheet.png`.",
                "- Manifest: `wayfarer_godot_vertical_slice/art_pipeline/player_identity/manifests/player_wayfarer_foundation_g419_manifest.json`.",
                "- QA report: `wayfarer_godot_vertical_slice/art_pipeline/player_identity/reports/player_wayfarer_foundation_g419_extraction_qa.json`.",
                "- Style tokens: `wayfarer_godot_vertical_slice/art_pipeline/player_identity/source_authored/g419_player_identity_style_tokens.json`.",
                "- Screenshot wrapper: `wayfarer_godot_vertical_slice/tools/capture_g419_runtime_screenshots.ps1`.",
                "",
                "## Completion Bar",
                "",
                "G-4.19 is not accepted until validators pass, mandatory runtime screenshots are generated and inspected, and the Agent Council assigns `COUNCIL_PASS_READY_FOR_PR`.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    ensure_dirs()
    write_style_tokens()
    write_brief()
    atlas, frames = generate_atlas()
    atlas.save(ATLAS_PATH)
    atlas.save(SOURCE_GRID_PATH)
    write_contact_sheet(atlas, frames)
    write_manifest(frames, atlas)
    write_qa_report(atlas, frames)
    update_visual_registry()
    write_phase_report()
    print(f"PASS: generated {PHASE} player identity assets")
    print(ATLAS_PATH)
    print(CONTACT_SHEET_PATH)
    print(MANIFEST_PATH)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
