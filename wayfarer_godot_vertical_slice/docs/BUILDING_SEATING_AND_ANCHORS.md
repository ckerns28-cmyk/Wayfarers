# Building Seating And Anchors

G-4.5 introduced a practical seating model for painterly building sprites, but
the five-building screenshot still read as oversized sprites pasted over a tan
slab. G-4.6 deliberately started smaller, but its three-building screenshot
still read like building cutouts behind a flat road. G-4.7 switched to a
calibration board; G-4.8 applied the recommended Variant D grammar to one
playable proof street, and G-4.9 tightens that proof into a smaller art-
directed street vignette. G-4.9.1 pauses street composition because crop
contamination in the proof-street sprites made seating impossible to judge.

This model is intentionally smaller than the old JavaScript seating-contract
audit. The Godot contract is source metadata plus visual inspection through the
`B` debug overlay.

## Proof Street Scope

The calibrated proof frame is authored in
`scripts/NewportTownBlueprint.gd`.

G-4.9 vignette building IDs:

1. `b_mercantile`
2. `b_counting_house`
3. `b_chandlery_front`

These buildings are marked with `proof_street = true` and join the
`proof_street_buildings` group at runtime.

G-4.9.1 source-image rule: the proof-street storefronts must use isolated
standalone PNGs from `assets/sprites/buildings/isolated/`, not unsafe live
atlas subregions. Seating is only meaningful once the rendered sprite contains
one building and no neighboring atlas fragments.

G-4.9.1 also changes the proof-street collision expectation: a building is not
just a facade strip. Its `collision_rect`/`lot_rect` represents the occupied
building lot behind the street frontage so the player cannot walk through or
behind the building body. The frontage interaction area remains south of the
footline, but the solid lot extends north from the street edge.

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

The local world-space physical building footprint. In the current proof
street, this covers the occupied lot behind the facade, not only the visible
front trim. It should block the playable body of the building while still
ignoring roof overhangs, painted shadows, chimneys, signboards, and transparent
image padding.

`lot_rect`

The same occupied lot expressed for visual/debug review. It is the answer to
"which ground squares does this building actually take up?"

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

`F3` still toggles the broader building debug overlay. Use `B` for G-4.9
seating review because it only targets the active vignette buildings.

## Adding Future Buildings

1. Choose the intended street edge or frontage point in world space.
2. Place the building node at the visual base and y-sort plane.
3. Measure or estimate `visual_base_anchor` from the source region.
4. Keep `sprite_offset` small and review the door/base against the street.
5. Set `frontage_offset` toward real walkable street space.
6. Set `collision_rect`/`lot_rect` to the occupied building lot behind the
   facade, not to a shallow label strip and not to the whole transparent image.
7. Set `shadow_size` and `shadow_offset` under the visual base.
8. Review with `B` enabled and debug off.
9. Run `tools/validate_vertical_slice.gd`.

The acceptance test is player-scale: the player should be able to walk in
front of the building, read the door/frontage, and understand why the building
sorts and blocks movement where it does.
