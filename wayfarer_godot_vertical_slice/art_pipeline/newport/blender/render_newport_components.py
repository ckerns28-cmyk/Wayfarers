"""Blender 5.1 component render helper for G-4.18 Newport prop support art.

Run with:
blender --background --factory-startup --python art_pipeline/newport/blender/render_newport_components.py
"""

from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path

import bpy
from mathutils import Vector


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[3]
OUT_ROOT = PROJECT_ROOT / "art_pipeline" / "newport" / "generated_assets" / "blender_components"
OUT_ROOT.mkdir(parents=True, exist_ok=True)


def clear_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def mat(name: str, color: tuple[float, float, float, float]) -> bpy.types.Material:
    material = bpy.data.materials.new(name)
    material.diffuse_color = color
    return material


WOOD = mat("weathered_umber_wood", (0.43, 0.28, 0.15, 1.0))
WOOD_DARK = mat("dark_endgrain", (0.12, 0.08, 0.04, 1.0))
ROPE = mat("muted_rope", (0.64, 0.51, 0.31, 1.0))
STONE = mat("dark_shadow", (0.06, 0.05, 0.04, 1.0))


def look_at(obj: bpy.types.Object, target: Vector) -> None:
    direction = target - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def setup_camera() -> None:
    light_data = bpy.data.lights.new("softbox", "AREA")
    light = bpy.data.objects.new("softbox", light_data)
    bpy.context.collection.objects.link(light)
    light.location = (0, -5, 5)
    light.data.energy = 450
    light.data.size = 5

    camera_data = bpy.data.cameras.new("Camera")
    camera = bpy.data.objects.new("Camera", camera_data)
    bpy.context.collection.objects.link(camera)
    camera.location = (3.8, -6.0, 4.2)
    look_at(camera, Vector((0, 0, 0.6)))
    camera.data.type = "ORTHO"
    camera.data.ortho_scale = 4.0
    bpy.context.scene.camera = camera

    bpy.context.scene.render.resolution_x = 640
    bpy.context.scene.render.resolution_y = 420
    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.eevee.taa_render_samples = 64
    bpy.context.scene.render.engine = "BLENDER_EEVEE"
    bpy.context.scene.view_settings.view_transform = "Standard"
    bpy.context.scene.view_settings.look = "Medium High Contrast"


def add_cube(name: str, loc: tuple[float, float, float], scale: tuple[float, float, float], material: bpy.types.Material) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(material)
    bevel = obj.modifiers.new("small bevels", "BEVEL")
    bevel.width = 0.025
    bevel.segments = 1
    obj.modifiers.new("weighted normals", "WEIGHTED_NORMAL")
    return obj


def add_barrel(loc: tuple[float, float, float], radius: float = 0.28, depth: float = 0.55) -> None:
    bpy.ops.mesh.primitive_cylinder_add(vertices=18, radius=radius, depth=depth, location=loc, rotation=(math.pi / 2, 0, 0))
    body = bpy.context.object
    body.name = "barrel_body"
    body.data.materials.append(WOOD)
    bevel = body.modifiers.new("soft bands", "BEVEL")
    bevel.width = 0.018
    bevel.segments = 1
    body.modifiers.new("weighted normals", "WEIGHTED_NORMAL")
    for z in [-0.18, 0.18]:
        add_cube("barrel_band", (loc[0], loc[1] + z, loc[2]), (radius * 2.06, 0.025, radius * 1.82), WOOD_DARK)


def add_rope_coil(loc: tuple[float, float, float], radius: float = 0.32) -> None:
    for i, r in enumerate([radius, radius * 0.72, radius * 0.46]):
        bpy.ops.mesh.primitive_torus_add(major_radius=r, minor_radius=0.025, major_segments=36, minor_segments=6, location=(loc[0], loc[1], loc[2] + i * 0.018))
        torus = bpy.context.object
        torus.name = "rope_coil"
        torus.scale.y = 0.62
        torus.data.materials.append(ROPE)


def add_market_table() -> None:
    add_cube("tabletop", (0, 0, 0.78), (1.6, 0.7, 0.12), WOOD)
    for x in [-0.62, 0.62]:
        for y in [-0.22, 0.22]:
            add_cube("table_leg", (x, y, 0.35), (0.10, 0.10, 0.62), WOOD_DARK)
    for x in [-0.44, -0.18, 0.08, 0.34]:
        add_cube("produce", (x, -0.04, 0.90), (0.16, 0.12, 0.08), ROPE)


def add_fence_segment() -> None:
    for x in [-0.9, -0.3, 0.3, 0.9]:
        add_cube("fence_post", (x, 0, 0.52), (0.10, 0.12, 1.05), WOOD_DARK)
    add_cube("fence_rail_top", (0, 0, 0.78), (2.15, 0.10, 0.11), WOOD)
    add_cube("fence_rail_low", (0, 0, 0.42), (2.15, 0.10, 0.11), WOOD)


def add_crate_stack() -> None:
    add_cube("crate_a", (-0.34, 0, 0.33), (0.62, 0.48, 0.52), WOOD)
    add_cube("crate_b", (0.26, 0.03, 0.29), (0.48, 0.46, 0.45), WOOD)
    add_cube("crate_c", (-0.12, -0.05, 0.82), (0.50, 0.42, 0.42), WOOD)
    for x in [-0.62, -0.12, 0.48]:
        add_cube("crate_slat", (x, -0.27, 0.61), (0.05, 0.05, 0.48), WOOD_DARK)


def render_component(component_id: str, builder) -> dict[str, str]:
    clear_scene()
    setup_camera()
    builder()
    bpy.context.scene.render.filepath = str(OUT_ROOT / f"{component_id}.png")
    bpy.ops.render.render(write_still=True)
    return {
        "component_id": component_id,
        "file": str((OUT_ROOT / f"{component_id}.png").relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "source": "Blender 5.1 procedural mesh render created locally for Wayfarer G-4.18",
    }


def main() -> None:
    components = [
        render_component("market_table", add_market_table),
        render_component("fence_segment", add_fence_segment),
        render_component("crate_stack", add_crate_stack),
        render_component("barrel", lambda: add_barrel((0, 0, 0.52))),
        render_component("rope_coil", lambda: add_rope_coil((0, 0, 0.12))),
    ]
    manifest = {
        "schema_id": "wayfarer.newport.blender_components.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tool": "Blender 5.1",
        "ownership": "project-owned locally generated procedural mesh renders",
        "third_party_pixels": False,
        "components": components,
    }
    (OUT_ROOT / "newport_blender_components_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("Wrote Blender Newport components")


if __name__ == "__main__":
    main()
