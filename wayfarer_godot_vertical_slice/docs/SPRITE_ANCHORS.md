# Sprite Anchors And Grounding

This document keeps the Godot sprite-origin model explicit and intentionally
simple. The goal is to avoid recreating the JavaScript seating-contract and
viewport-audit complexity inside Godot.

## Grounding Rule

Every placed world sprite needs one clear logical origin:

- Building sprites anchor at the visual base or foot line.
- Player and NPC sprites anchor at their feet.
- Props anchor at their contact point with the ground unless a specific scene
  documents another rule.
- Terrain, water, and roads are tile/region aligned and do not use painterly
  overhang anchors.

For the current building slice, `Building.gd` maps the region-local anchor to
the `Node2D` origin:

```text
sprite.position = -anchor * scale
```

The current convention is:

```text
anchor = Vector2(region_width / 2, region_height)
```

That places the node origin at the bottom-center of the visible sprite.

## Painterly Overhangs

Large buildings may visually overhang their logical placement. Roofs, awnings,
chimneys, signs, rope, rails, shrubs, and transparent silhouettes can extend
well above or sideways from the foot line.

Those visual overhangs must not redefine the gameplay footprint. Keep these
concerns separate:

- Sprite region: the visible painterly image.
- Foot anchor: the visual base used for placement and y-sort.
- Collision shape: the walk-blocking lower footprint.
- Interaction shape: the player-facing activation area.
- Door marker: the visible or projected doorway target.

Decorative ground shadows are allowed when they clarify footing. Shadows should
stay visual-only and should not affect collision or interaction.

## Collision And Interaction

Collision should describe the believable lower footprint, not the full painted
rectangle.

For current buildings:

- Collision rectangles sit near the base and end at or slightly above the foot
  anchor.
- Interaction rectangles sit south of the foot anchor and align to the door.
- Debug overlays should be used when changing anchors, collision, or
  interaction areas.

Player and NPC collision should stay centered around the feet/body footprint,
not around the full head-to-foot visual height.

## Y-Sort And Depth

Godot's y-sort should remain the primary depth strategy:

- `World.y_sort_enabled = true`.
- Building node origins are their foot anchors.
- Player and NPC node origins are their feet.
- Do not add broad z-index overrides for normal world sprites.
- UI and interaction labels may use explicit high z-index values because they
  are readability overlays, not world depth participants.

Use scene origins and collision nodes rather than broad visual contract audits.
If a sprite appears wrong, fix its anchor, region, or collision node locally.

## Adding A New Sprite

When importing future sprites:

1. Put original art in `assets/source/<domain>/` when available.
2. Put individual Godot-ready sprites in `assets/sprites/<domain>/` or atlas
   sheets in `assets/atlases/<domain>/`.
3. Track the Godot `.import` file generated for the asset.
4. Document the anchor assumption in this file or the relevant atlas contract.
5. Keep atlas region rectangles tight and inside their source cell boundaries.
6. Run the Godot validator and the asset hygiene script before packaging.
7. Package an itch review ZIP and visually confirm the sprite in browser.

Do not add a new visual-contract audit layer unless a real, repeated defect
proves that simple anchors and node-local collision are insufficient.
