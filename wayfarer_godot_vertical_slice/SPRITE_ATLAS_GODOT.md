# Wayfarer Godot Slice — Atlas Contract

This is the atlas contract for the **Godot vertical slice only**. The
JavaScript build has its own contract in `docs/SPRITE_ATLAS_CONTRACT.md`
and is not affected by this document.

## Source files

```
wayfarer_godot_vertical_slice/assets/buildings/
  hearthvale_buildings_atlas_v1.png            (1254 x 1254)
  hearthvale_newport_structure_pack_v1_a.png   (1254 x 1254)
  hearthvale_newport_structure_pack_v1_b.png   (1254 x 1254)
```

## Grid layout

Each PNG is a **3 × 3 grid** of 418 × 418 cells:

```
col 0          col 1          col 2
x ∈ [0, 418)   x ∈ [418, 836) x ∈ [836, 1254)
```

Same for rows. Adjacent cells share an edge — **there is no inter-sprite
gutter in source**. A `Rect2` whose right edge lands at x=418, x=836, or
the atlas width is therefore at the very edge of the next sprite's
content; any rounding into the next pixel column will pull a sliver of a
neighbor into the result.

## Region rule

When you reference one cell from an atlas, use a `Rect2` whose
edges sit **inside or exactly on** the cell boundary, and whose
position+size matches the tight bounding box of the visible sprite (i.e.
the smallest rect that contains all non-background pixels of that cell).

For our three atlases the tight bounding boxes per cell are:

```
v1                  pack_a              pack_b
(33, 45, 385, 373)  (57, 57, 361, 361)  (39, 19, 379, 385)
(418, 67, 384, 351) (418, 76, 410, 332) (418, 67, 397, 336)
(855, 10, 323, 408) (864, 86, 351, 315) (840, 60, 380, 348)
(61, 418, 357, 418) (61, 418, 357, 372) (105, 433, 313, 403)
(418, 418, 418, 418)(418, 470, 418, 313)(418, 475, 418, 322)
(836, 418, 381, 418)(836, 451, 273, 385)(836, 444, 366, 352)
(44, 836, 367, 343) (68, 873, 350, 292) (51, 836, 361, 377)
(461, 903, 372, 322)(418, 885, 418, 300)(430, 838, 406, 357)
(878, 836, 271, 348)(836, 836, 370, 352)(836, 842, 373, 355)
```

`tools/render_slice_approx.py` and `tools/validate_vertical_slice.gd` both
assume regions live inside these bounding boxes.

## Currently used cells (slice)

| Slice id              | Atlas    | Cell (row, col) | Region                |
| --------------------- | -------- | --------------- | --------------------- |
| `inn_tavern`          | v1       | (0, 0)          | `(33, 45, 385, 373)`  |
| `dock_storehouse`     | pack_b   | (2, 0)          | `(51, 836, 361, 377)` |
| `custom_house`        | pack_a   | (2, 0)          | `(68, 873, 350, 292)` |
| `merchant_shop_house` | pack_a   | (0, 1)          | `(418, 76, 410, 332)` |
| `large_residence`     | pack_a   | (0, 2)          | `(864, 86, 351, 315)` |

## Anchors

- Anchor is in **region-local pixel coordinates** (top-left of the region
  is `(0, 0)`).
- For this slice all five buildings use `anchor = (region.w / 2, region.h)`
  so the foot anchor lands at the bottom-center of the sprite (the
  visible base of the building).
- `Building.gd` sets `sprite.position = -anchor * scale` so the foot
  anchor maps to the building Node2D's origin.

## Collision / interaction

- Collision body is a `RectangleShape2D` sized to roughly the lower
  10–14% of the building visual; positioned with
  `collision_offset.y = -collision_size.y / 2` so it spans from
  `y = -collision_size.y` (top of foundation) to `y = 0` (the visible
  base = foot anchor).
- Interaction area is a `RectangleShape2D` placed *south* of the foot
  anchor (positive y, in front of the door). Its X is aligned with the
  building's door marker.

## When you add a new building

1. Pick a single 418×418 cell. Do not cross cell boundaries.
2. Compute (or look up above) the tight bounding box for that cell.
3. Set `region` to the bounding box, `source_size` to `region.size`,
   `anchor` to `(region.size.x / 2, region.size.y)`.
4. Set `position` to where the visible base of the building should appear
   in world coords.
5. Set `collision_size`, `collision_offset`, `interaction_size`,
   `interaction_offset`, `door_offset` so the validator passes.
6. Re-run `tools/validate_vertical_slice.gd` and the F3 debug overlay
   before committing.
