# Visual Scale And Street Grammar Calibration

G-4.7 exists because the G-4.6 three-building proof still failed visually. It
isolated the problem, but it did not solve it: the street looked like a stage
backdrop, the player did not feel human-scaled against the buildings, the road
was still a flat slab, and debug markers measured the failure rather than
making the frontage believable.

Do not rebuild the Newport town from G-4.6. Use this calibration board first.
G-4.8 applies the recommended Variant D grammar to one real playable proof
street and no longer displays the four-panel board.

## Variants

The active review build shows four side-by-side treatments.

Variant A: Current Scale Reference

- Preserves the broad-slab grammar as a comparison baseline.
- Uses the current larger player reference.
- Expected to fail or read weakest.

Variant B: Smaller Player / More Human Scale

- Keeps a clear storefront comparison.
- Uses a smaller player figure to test whether the town reads more human.
- Useful mainly for player-scale judgment.

Variant C: Lower Camera / Closer Street Vignette

- Uses a tighter foreground/midground street band.
- Reduces the feeling of a flat overhead map.
- Useful mainly for camera/framing judgment.

Variant D: Integrated Sidewalk/Stoop Treatment

- Recommended candidate.
- Uses sidewalk, stoop pads, curb/gutter, narrower cobbled lane, wharf strip,
  darker edge lines, props, and smaller player scale.
- Intended to test the actual street grammar that should become the town
  standard if visual review confirms it.

## Art Direction Recommendation

Recommended standard: Variant D, if the manual itch screenshot confirms that
it clearly reads better than G-4.6.

Player scale: the smaller player treatment, around `0.76` to `0.78` of the
current proof-frame figure, appears most promising for a human-scale street.

Building sprites: the existing painterly sprite approach remains plausible,
but only with hand-authored per-building anchors and street integration. A
generic center/bottom placement model is not enough.

Building metadata must stay authored per building:

- visual base anchor
- frontage point
- collision rectangle
- y-sort/depth anchor
- shadow/base footprint
- optional draw-width override when a sprite reads out of scale

If Variant D still reads like cutouts on a stage, the correct classification is
`BUILDING_STREET_GRAMMAR_FAILED` or `SPRITE_APPROACH_NEEDS_RETHINK`, not a pass.

## Review Controls

Press `B` to toggle the calibration building overlay. It is off by default.
The final visual must read correctly with debug off.

## G-4.8 Application

G-4.8 uses Variant D as the active proof-street standard:

- one playable street vignette, not a comparison board
- `0.78` player visual scale
- four hand-seated buildings: `b_mercantile`, `b_counting_house`,
  `b_chandlery_front`, and `b_shop_house`
- integrated sidewalk/apron strip, stoop pads, curb/gutter, narrow cobbled
  lane, wharf plank edge, and water beyond
- per-building anchors, frontages, collision rectangles, y-sort anchors, and
  shadow/base footprints

If the manual itch screenshot still reads like pasted sprites on a slab, do
not scale the grammar back up. Classify the result as
`PROOF_STREET_STILL_NOT_BELIEVABLE` or `BUILDING_STREET_GRAMMAR_FAILED`.

## G-4.9 Vignette Direction

G-4.8 proved that alignment alone is not enough. G-4.9 keeps the Variant D
grammar but reframes it as art direction:

- reduce from four buildings to three
- cluster building spacing instead of even strip placement
- move the player closer to storefronts
- narrow the road lane further
- make sidewalk, stoops, curb, wharf edge, and harbor water read as one
  composed scene
- concentrate props at bases and edges so buildings feel inhabited

The G-4.9 result should be judged with debug off. If it still looks like an
alignment strip, the correct classification is
`STILL_LOOKS_LIKE_CALIBRATION_STRIP` or `STREET_PLANE_STILL_FAILED`.
