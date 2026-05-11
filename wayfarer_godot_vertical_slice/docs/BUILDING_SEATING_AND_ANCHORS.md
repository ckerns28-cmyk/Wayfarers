# Building Seating And Anchors

G-4.5 introduces a practical seating model for painterly building sprites. The
goal is one proof street where buildings sit on a shared ground plane, face a
walkable frontage, sort correctly against the player, and expose collision that
matches the physical building base instead of the entire painted image.

This model is intentionally smaller than the old JavaScript seating-contract
audit. The Godot contract is source metadata plus visual inspection through the
`B` debug overlay.

## Proof Street Scope

The first calibrated street is the waterfront commercial frontage in
`scripts/NewportTownBlueprint.gd`.

Proof-street building IDs:

1. `b_inn_tavern`
2. `b_mercantile`
3. `b_counting_house`
4. `b_chandlery_front`
5. `b_shop_house`

These buildings are marked with `proof_street = true` and join the
`proof_street_buildings` group at runtime.

## Runtime Meaning

For proof-street buildings, the building `Node2D.position` means the calibrated
visual-base plane for the street frontage. It is also the default y-sort plane.

`Sprite2D.centered` is disabled. The sprite is placed from the calibrated base:

```gdscript
sprite.position = -visual_base_anchor * scale_factor + sprite_offset
```

This means the painted roof, walls, porch, side overhangs, and decorative
shadow can extend around the base without redefining the building's walkable
or sortable footprint.

## Metadata Fields

`visual_base_anchor`

The source-region pixel position of the real visual base or footline. This is
not always the bottom of the atlas crop, because painterly sprites may include
padding, water, shadow, or decorative trim below the true ground contact.

`sprite_offset`

A final world-pixel nudge after scale. Keep this small. If a building needs a
large correction, recheck the source `visual_base_anchor` first.

`visual_base_width`

The width of the visible footline marker shown in seating debug mode.

`frontage_offset`

The local world-space point where the building faces walkable street or apron
space. Door and interaction markers use this same frontage plane unless a
building needs a special case.

`collision_rect`

The local world-space physical body/base rectangle. It should cover the solid
building body near the ground plane, not roof overhangs, painted shadows,
chimneys, signboards, or the full source image.

`y_sort_offset`

The local world-space marker for the depth/sort plane. The proof street keeps
this at `Vector2.ZERO`, so the building node position remains the sorting
anchor.

`shadow_size` and `shadow_offset`

The subtle grounding ellipse under the visual base. It should help the sprite
read as seated on the street without overpowering the art.

## Debug Overlay

Press `B` to toggle the proof-street seating overlay. It is off by default.

The overlay shows:

- base/footline marker
- frontage marker
- collision rectangle
- y-sort/depth anchor
- building ID label

`F3` still toggles the broader building debug overlay. Use `B` for G-4.5
seating review because it only targets the proof street.

## Adding Future Buildings

1. Choose the intended street edge or frontage point in world space.
2. Place the building node at the visual base and y-sort plane.
3. Measure or estimate `visual_base_anchor` from the source region.
4. Keep `sprite_offset` small and review the door/base against the street.
5. Set `frontage_offset` toward real walkable street space.
6. Set `collision_rect` to the solid ground-level body, not the whole image.
7. Set `shadow_size` and `shadow_offset` under the visual base.
8. Review with `B` enabled and debug off.
9. Run `tools/validate_vertical_slice.gd`.

The acceptance test is player-scale: the player should be able to walk in
front of the building, read the door/frontage, and understand why the building
sorts and blocks movement where it does.
