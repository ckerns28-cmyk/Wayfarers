# Wayfarer Godot Slice — Atlas Contract

This is the atlas contract for the **Godot vertical slice only**. The
JavaScript build has its own contract in `docs/SPRITE_ATLAS_CONTRACT.md`
and is not affected by this document.

For broader source art, import metadata, generated artifact, and anchor
discipline, see:

- `docs/ASSET_WORKFLOW.md`
- `docs/SPRITE_ANCHORS.md`

## Source files

```
wayfarer_godot_vertical_slice/assets/buildings/
  hearthvale_buildings_atlas_v1.png            (1254 x 1254)
  hearthvale_newport_structure_pack_v1_a.png   (1254 x 1254)
  hearthvale_newport_structure_pack_v1_b.png   (1254 x 1254)

wayfarer_godot_vertical_slice/assets/sprites/buildings/isolated/
  mercantile_shop_isolated.png
  newport_counting_house_civic_exchange_isolated.png
  newport_chandlery_outfitter_front_isolated.png
  newport_shopfront_awning_isolated.png
```

G-4.9.1 isolates the active proof-street storefronts from the atlases because
manual review showed neighboring cell fragments at their edges. The atlas PNGs
remain source material; the four listed isolated files are the runtime review
sprites for `b_mercantile`, `b_counting_house`, `b_chandlery_front`, and
`b_shop_house`.

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

`scripts/BuildingCatalog.gd` and `tools/validate_vertical_slice.gd` both
assume regions live inside these bounding boxes.

For isolated G-4.9.1 storefronts, `BuildingCatalog.gd` uses a full-image
region on the standalone PNG instead of the original atlas cell.

## Currently used cells

G-4.1 centralizes atlas usage in `scripts/BuildingCatalog.gd`. The table below
shows the building ids currently present in the Newport starting town and the
sprite ids they use.

| Building id              | Sprite id                               |
| ------------------------ | --------------------------------------- |
| `b_boathouse`            | `newport_wharf_boathouse_large`         |
| `b_dock_storehouse`      | `newport_dockside_storehouse_long`      |
| `b_market_shed`          | `newport_market_shed_stalls`            |
| `b_inn_tavern`           | `inn_tavern_v1`                         |
| `b_mercantile`           | `mercantile_shop`                       |
| `b_counting_house`       | `newport_counting_house_civic_exchange` |
| `b_chandlery_front`      | `newport_chandlery_outfitter_front`     |
| `b_shop_house`           | `newport_shopfront_awning`              |
| `b_custom_house`         | `newport_custom_house_civic_front`      |
| `b_village_hall`         | `village_hall_meeting_house`            |
| `b_res_small`            | `residence_small`                       |
| `b_townhouse_row_a`      | `newport_narrow_merchant_townhouse_a`   |
| `b_townhouse_row_b`      | `newport_modest_clapboard_residence_a`  |
| `b_service_dependency`   | `service_dependency_shed`               |
| `b_hunter_lodge`         | `hunter_lodge_or_outfitter`             |
| `b_res_large`            | `residence_large`                       |
| `b_georgian_residence`   | `newport_georgian_merchant_residence_a` |
| `b_elite_mansion`        | `newport_elite_mansion_white`           |
| `b_prestige_block`       | `newport_formal_townhouse_block_a`      |

## Anchors

- Anchor is in **region-local pixel coordinates** (top-left of the region
  is `(0, 0)`).
- Current Newport town buildings use `anchor = (region.w / 2, region.h)` so
  the foot anchor lands at the bottom-center of the sprite (the visible base of
  the building).
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
