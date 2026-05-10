"""Render an approximate Wayfarer Godot Vertical Slice screenshot.

This is a Python/PIL approximation of what Godot would render. We use it
to produce gameplay and collision-debug stills when Godot is not available
on the build machine. Final review screenshots should still be captured
from Godot itself once the export runs locally.
"""
from PIL import Image, ImageDraw, ImageFont
import os
import math
import random
import json
from typing import Iterable, Tuple

ATLAS_DIR = "/home/user/Wayfarers/wayfarer_godot_vertical_slice/assets/buildings"
OUT_DIR = "/home/user/Wayfarers/wayfarer_godot_vertical_slice/artifacts/screenshots"
TILE = 32
WORLD_W = 1600
WORLD_H = 1024
VIEW_W = 1280
VIEW_H = 720
PLAYER = (860, 548)
NPC = (892, 516)

CAMERA_LEFT = max(0, min(WORLD_W - VIEW_W, PLAYER[0] - VIEW_W // 2))
CAMERA_TOP = max(0, min(WORLD_H - VIEW_H, PLAYER[1] - VIEW_H // 2))


def w2s(x, y):
    return (int(x - CAMERA_LEFT), int(y - CAMERA_TOP))


def tile_rect(x, y, w=1, h=1):
    return (x * TILE, y * TILE, (x + w) * TILE, (y + h) * TILE)


def lerp_color(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def draw_tiled_rect(draw, rect_tiles, base, alt, line_color=(0, 0, 0, 20)):
    x0, y0, w, h = rect_tiles
    for ty in range(y0, y0 + h):
        for tx in range(x0, x0 + w):
            n = ((tx * 19 + ty * 31) % 100) / 100.0
            color = lerp_color(base, alt, n * 0.35)
            x0w, y0w = tx * TILE, ty * TILE
            x1w, y1w = (tx + 1) * TILE, (ty + 1) * TILE
            x0s, y0s = w2s(x0w, y0w)
            x1s, y1s = w2s(x1w, y1w)
            if x1s < 0 or y1s < 0 or x0s > VIEW_W or y0s > VIEW_H:
                continue
            draw.rectangle([x0s, y0s, x1s, y1s], fill=color)
            draw.rectangle([x0s, y0s, x1s - 1, y1s - 1], outline=line_color)


def draw_ground(draw):
    draw_tiled_rect(draw, (0, 0, 50, 32), (0x5f, 0x80, 0x52), (0x45, 0x6b, 0x45))
    draw_tiled_rect(draw, (4, 5, 7, 5), (0x6f, 0x8c, 0x5d), (0x53, 0x77, 0x4a), (0, 0, 0, 8))
    draw_tiled_rect(draw, (35, 4, 9, 7), (0x6a, 0x89, 0x59), (0x50, 0x6f, 0x4c), (0, 0, 0, 8))
    draw_tiled_rect(draw, (5, 23, 11, 5), (0x58, 0x77, 0x47), (0x45, 0x68, 0x3f), (0, 0, 0, 8))


def draw_roads(draw):
    draw_tiled_rect(draw, (4, 18, 40, 2), (0xa9, 0x92, 0x6a), (0x8b, 0x76, 0x53))
    draw_tiled_rect(draw, (6, 14, 32, 2), (0xa3, 0x8d, 0x69), (0x85, 0x73, 0x55))
    draw_tiled_rect(draw, (18, 9, 12, 6), (0x9a, 0x9a, 0x85), (0x77, 0x7b, 0x6f))
    draw_tiled_rect(draw, (15, 6, 2, 14), (0xa9, 0x92, 0x6a), (0x88, 0x74, 0x52))
    draw_tiled_rect(draw, (24, 6, 2, 14), (0xa9, 0x92, 0x6a), (0x88, 0x74, 0x52))
    draw_tiled_rect(draw, (33, 8, 2, 12), (0xa9, 0x92, 0x6a), (0x88, 0x74, 0x52))
    draw_tiled_rect(draw, (10, 6, 28, 2), (0x9f, 0x89, 0x64), (0x80, 0x6d, 0x50))
    for tx, ty in [(13, 12), (27, 10), (37, 16), (8, 17), (43, 18)]:
        x0w = tx * TILE + 11
        y0w = ty * TILE + 11
        x1w = (tx + 1) * TILE - 11
        y1w = (ty + 1) * TILE - 11
        x0s, y0s = w2s(x0w, y0w)
        x1s, y1s = w2s(x1w, y1w)
        draw.rectangle([x0s, y0s, x1s, y1s], fill=(0xb7, 0x75, 0x4d))


def draw_wharf_water(draw):
    draw_tiled_rect(draw, (0, 22, 50, 10), (0x34, 0x6c, 0x7f), (0x1f, 0x51, 0x65), (0, 0, 0, 10))
    draw_tiled_rect(draw, (4, 21, 40, 1), (0x7c, 0x72, 0x58), (0x5d, 0x56, 0x44))
    for pier in [(9, 18, 3, 8), (20, 18, 3, 8), (31, 18, 3, 8)]:
        draw_tiled_rect(draw, pier, (0x8f, 0x6d, 0x48), (0x65, 0x4b, 0x34))
        x0t, y0t, wt, ht = pier
        for y in range(y0t, y0t + ht):
            x0s, ys = w2s(x0t * TILE, y * TILE)
            x1s, _ = w2s((x0t + wt) * TILE, y * TILE)
            draw.line([x0s, ys, x1s, ys], fill=(0, 0, 0, 41), width=2)
    for x in range(0, 50):
        wave_y = 23 * TILE + ((x % 3) * 3)
        x0s, y0s = w2s(x * TILE + 8, wave_y)
        x1s, y1s = w2s(x * TILE + 24, wave_y)
        if y0s < 0 or y0s > VIEW_H:
            continue
        draw.line([x0s, y0s, x1s, y1s], fill=(191, 242, 255), width=2)


def draw_props(draw):
    for tx, ty in [(11, 18), (22, 18), (32, 18), (35, 18), (8, 12), (42, 14)]:
        cx, cy = w2s(tx * TILE + 16, ty * TILE + 18)
        draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(0x75, 0x54, 0x3a))
        draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=(0xc0, 0x9b, 0x62), width=2)
    for tx, ty in [(5, 20), (14, 21), (28, 19), (45, 21)]:
        x0, y0 = w2s(tx * TILE + 7, ty * TILE + 7)
        x1, y1 = w2s((tx + 1) * TILE - 7, (ty + 1) * TILE - 7)
        draw.rectangle([x0, y0, x1, y1], fill=(0x9b, 0x70, 0x42), outline=(0x39, 0x28, 0x19), width=2)
    for tx, ty in [(7, 7), (41, 7), (5, 15), (45, 12)]:
        cx, cy = w2s(tx * TILE + 16, ty * TILE + 20)
        draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(0x2f, 0x5d, 0x35))
        cx2, cy2 = w2s(tx * TILE + 9, ty * TILE + 13)
        draw.ellipse([cx2 - 8, cy2 - 8, cx2 + 8, cy2 + 8], fill=(0x3d, 0x70, 0x42))


BUILDINGS = [
    dict(id="inn_tavern", atlas="hearthvale_buildings_atlas_v1.png",
         region=(33, 45, 385, 373), draw_width=240,
         anchor=(192.5, 373), position=(417, 676),
         collision=dict(size=(216, 46), offset=(0, -23)),
         interaction=dict(size=(92, 48), offset=(4, 20)),
         door_offset=(4, 0)),
    dict(id="dock_storehouse", atlas="hearthvale_newport_structure_pack_v1_b.png",
         region=(51, 836, 361, 377), draw_width=242,
         anchor=(180.5, 377), position=(1060, 704),
         collision=dict(size=(186, 54), offset=(0, -27)),
         interaction=dict(size=(120, 52), offset=(0, 20)),
         door_offset=(0, 0)),
    dict(id="custom_house", atlas="hearthvale_newport_structure_pack_v1_a.png",
         region=(68, 873, 350, 292), draw_width=226,
         anchor=(175, 292), position=(941, 467),
         collision=dict(size=(160, 46), offset=(0, -23)),
         interaction=dict(size=(86, 48), offset=(0, 18)),
         door_offset=(0, 0)),
    dict(id="merchant_shop_house", atlas="hearthvale_newport_structure_pack_v1_a.png",
         region=(418, 76, 410, 332), draw_width=243,
         anchor=(205, 332), position=(740, 633),
         collision=dict(size=(174, 42), offset=(0, -21)),
         interaction=dict(size=(82, 48), offset=(-16, 18)),
         door_offset=(-16, 0)),
    dict(id="large_residence", atlas="hearthvale_newport_structure_pack_v1_a.png",
         region=(864, 86, 351, 315), draw_width=227,
         anchor=(175.5, 315), position=(698, 443),
         collision=dict(size=(168, 42), offset=(0, -21)),
         interaction=dict(size=(88, 48), offset=(0, 18)),
         door_offset=(0, 0)),
]


def paste_building(canvas, b):
    atlas = Image.open(os.path.join(ATLAS_DIR, b["atlas"])).convert("RGBA")
    rx, ry, rw, rh = b["region"]
    crop = atlas.crop((rx, ry, rx + rw, ry + rh))
    scale = b["draw_width"] / rw
    new_size = (max(1, int(round(rw * scale))), max(1, int(round(rh * scale))))
    sprite = crop.resize(new_size, Image.LANCZOS)
    # Position: sprite.position in node coords = -anchor * scale.
    ax, ay = b["anchor"]
    sx_node = -ax * scale
    sy_node = -ay * scale
    px, py = b["position"]
    sx_world = px + sx_node
    sy_world = py + sy_node
    sx, sy = w2s(sx_world, sy_world)
    canvas.alpha_composite(sprite, (sx, sy))
    return dict(b=b, sx=sx, sy=sy, scale=scale, sprite_size=new_size)


def draw_collision_debug(draw, placements):
    for p in placements:
        b = p["b"]
        scale = p["scale"]
        # Sprite outline (yellow)
        x0 = p["sx"]; y0 = p["sy"]
        x1 = x0 + p["sprite_size"][0]; y1 = y0 + p["sprite_size"][1]
        draw.rectangle([x0, y0, x1, y1], outline=(242, 242, 76, 220), width=2)
        # Foot anchor world
        fx_world, fy_world = b["position"]
        fx, fy = w2s(fx_world, fy_world)
        # Collision rect
        col_sz = b["collision"]["size"]
        col_off = b["collision"]["offset"]
        cx_world = fx_world + col_off[0]
        cy_world = fy_world + col_off[1]
        cx_left = cx_world - col_sz[0] / 2; cx_right = cx_world + col_sz[0] / 2
        cy_top = cy_world - col_sz[1] / 2; cy_bot = cy_world + col_sz[1] / 2
        cxl, cyt = w2s(cx_left, cy_top); cxr, cyb = w2s(cx_right, cy_bot)
        # Translucent fill via separate overlay
        fill = Image.new("RGBA", (max(1, cxr - cxl), max(1, cyb - cyt)), (255, 89, 89, 76))
        draw._image.alpha_composite(fill, (cxl, cyt))
        draw.rectangle([cxl, cyt, cxr, cyb], outline=(255, 51, 51, 242), width=2)
        # Interaction rect
        ix_sz = b["interaction"]["size"]
        ix_off = b["interaction"]["offset"]
        ix_world = fx_world + ix_off[0]; iy_world = fy_world + ix_off[1]
        ixl = ix_world - ix_sz[0] / 2; ixr = ix_world + ix_sz[0] / 2
        iyt = iy_world - ix_sz[1] / 2; iyb = iy_world + ix_sz[1] / 2
        ixl_s, iyt_s = w2s(ixl, iyt); ixr_s, iyb_s = w2s(ixr, iyb)
        ifill = Image.new("RGBA", (max(1, ixr_s - ixl_s), max(1, iyb_s - iyt_s)), (89, 216, 255, 64))
        draw._image.alpha_composite(ifill, (ixl_s, iyt_s))
        draw.rectangle([ixl_s, iyt_s, ixr_s, iyb_s], outline=(64, 178, 255, 242), width=2)
        # Foot anchor (green cross)
        draw.line([fx - 8, fy, fx + 8, fy], fill=(26, 255, 115), width=2)
        draw.line([fx, fy - 8, fx, fy + 8], fill=(26, 255, 115), width=2)
        draw.ellipse([fx - 3, fy - 3, fx + 3, fy + 3], fill=(26, 255, 115))
        # Door marker
        dx, dy = w2s(fx_world + b["door_offset"][0], fy_world + b["door_offset"][1])
        draw.ellipse([dx - 4, dy - 4, dx + 4, dy + 4], fill=(255, 217, 76))
        # Label
        try:
            font = ImageFont.load_default()
            draw.text((p["sx"] + 4, p["sy"] + 4), b["id"], fill=(255, 255, 255), font=font)
        except Exception:
            pass


def draw_player(draw):
    px, py = w2s(*PLAYER)
    # head
    draw.ellipse([px - 12, py - 43, px + 12, py - 19], fill=(0xf3, 0xd6, 0xa0))
    draw.rectangle([px - 9, py - 20, px + 9, py + 6], fill=(0x4a, 0x6f, 0xa3))
    draw.rectangle([px - 11, py + 4, px + 11, py + 12], fill=(0x2f, 0x47, 0x69))
    draw.line([px - 15, py - 10, px + 15, py - 10], fill=(0xd2, 0xb9, 0x78), width=3)


def draw_npc(draw):
    nx, ny = w2s(*NPC)
    draw.ellipse([nx - 11, ny - 39, nx + 11, ny - 17], fill=(0xd5, 0xb3, 0x84))
    draw.rectangle([nx - 9, ny - 20, nx + 9, ny + 8], fill=(0x6c, 0x4b, 0x7f))
    draw.rectangle([nx - 12, ny + 4, nx + 12, ny + 12], fill=(0x47, 0x34, 0x5a))
    draw.line([nx - 13, ny - 21, nx + 13, ny - 21], fill=(0x25, 0x1b, 0x25), width=4)


def draw_hud(image):
    # Left panel
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    odraw.rectangle([18, 18, 376, 218], fill=(20, 24, 32, 200), outline=(60, 70, 90, 255))
    try:
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()
    except Exception:
        font_title = font_body = None
    odraw.text((34, 30), "Wayfarer", fill=(255, 255, 255), font=font_title)
    odraw.text((34, 70), "Build label: Godot Vertical Slice", fill=(184, 199, 220), font=font_body)
    odraw.text((34, 90), "Objective: The Still Water Objective:", fill=(255, 255, 255), font=font_body)
    odraw.text((34, 106), "Speak with Edrin Vale", fill=(255, 255, 255), font=font_body)
    odraw.text((34, 132), "Current zone: Newport Harbor Test", fill=(220, 220, 220), font=font_body)
    odraw.text((34, 156), "Level 1    HP 52/52", fill=(219, 234, 255), font=font_body)
    # Interaction prompt
    px, py = w2s(*PLAYER)
    odraw.text((px + 18, py - 48), "E: Speak with Edrin Vale",
        fill=(255, 235, 173), font=font_body)
    image.alpha_composite(overlay)


def render(out_path, debug=False):
    image = Image.new("RGBA", (VIEW_W, VIEW_H), (0, 0, 0, 255))
    draw = ImageDraw.Draw(image, "RGBA")
    # Map layers in draw order: ground -> roads -> wharf_water -> props
    draw_ground(draw)
    draw_roads(draw)
    draw_wharf_water(draw)
    draw_props(draw)
    # Buildings y-sorted with player+NPC
    items = []
    placements = []
    for b in BUILDINGS:
        items.append(("building", b["position"][1], b))
    items.append(("player", PLAYER[1], None))
    items.append(("npc", NPC[1], None))
    items.sort(key=lambda x: x[1])
    for kind, _y, payload in items:
        if kind == "building":
            placements.append(paste_building(image, payload))
        elif kind == "player":
            draw_player(draw)
        else:
            draw_npc(draw)
    if debug:
        draw_collision_debug(draw, placements)
    draw_hud(image)
    image.convert("RGB").save(out_path, format="PNG", optimize=True)
    print(f"wrote {out_path}")


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    random.seed(0)
    render(os.path.join(OUT_DIR, "vertical_slice_gameplay.png"), debug=False)
    render(os.path.join(OUT_DIR, "vertical_slice_collision_debug.png"), debug=True)
