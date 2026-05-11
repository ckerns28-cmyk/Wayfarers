# Vertical Slice Notes

## What This Tests

The slice isolates the problems that made Newport hard in the JavaScript build:

- visual foot anchors instead of tile guesses
- collision shapes that match visible building bases
- Y-sort depth using Godot scene objects
- interaction/frontage points positioned at obvious doors
- harbor-town readability without placing all 19 production buildings

## Early Read

Godot's scene/object model is a better fit for the placement problem than the
custom canvas stack. Buildings own their sprite, collision, interaction area,
and visual anchor in one object. The player and buildings live under one
Y-sorted parent, which directly addresses the in-front/behind problem without
a large custom depth-sort contract.

## Sprite Source Truth (delivery pass)

The atlas regions on each building were re-derived from the source PNGs in
`assets/buildings/`. Each PNG is a 3×3 grid of 418×418 cells with zero gutter
between adjacent sprites. The previous regions overshot cell boundaries and
were pulling slivers of neighboring buildings into the rendered scene. The
fixes:

| Building              | Old region (x,y,w,h)         | New region (x,y,w,h)         | What changed                                                                                                                                                |
| --------------------- | ---------------------------- | ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `inn_tavern`          | `(24, 36, 446, 436)`         | `(33, 45, 385, 373)`         | Old region overshot 52px right and 54px down into the awning building and the small-house cell. Tightened to the inn's bounding box inside cell (0,0).      |
| `dock_storehouse`     | `(365, 865, 385, 350)`       | `(51, 836, 361, 377)`        | Old region spanned cells (0,0)→(1,0) of pack_b row 2 and was rendering a sliver of the chapel + dock-with-crane. Repointed to the gray storehouse w/ crane. |
| `custom_house`        | `(42, 824, 368, 357)`        | `(68, 873, 350, 292)`        | Old region had 49px of empty atlas padding at the top and a stray sliver of the dock-house cell on the right. Tightened to the cottage bbox.                |
| `merchant_shop_house` | `(434, 78, 398, 320)`        | `(418, 76, 410, 332)`        | Old region clipped the left 16px of the columned mansion (col-1) and undershot 12px on the bottom. Snapped to the full bbox.                                |
| `large_residence`     | `(841, 65, 372, 334)`        | `(864, 86, 351, 315)`        | Old region included transparent padding outside the row-house. Tightened to the row-house bbox.                                                             |

Building world positions were nudged a few pixels (10-22px per building) so the
visible base center stays where reviewers saw it in PR #387 even though the
foot anchor is now exactly on the visible base. See `scenes/Main.gd` for the
final values. No `position` was used to hide sliver contamination — every
sliver fix is at the region/source level.

The atlas grid contract for the Godot slice is in `SPRITE_ATLAS_GODOT.md`
(the JS build's `docs/SPRITE_ATLAS_CONTRACT.md` is separate and unchanged).

## Debug Proof Mode

Press `F3` while the slice is running to toggle the per-building debug
overlay. It draws (for each building):

- yellow sprite-region outline
- red collision-rect fill + outline (the body that blocks the player)
- blue interaction-rect fill + outline (the frontage zone)
- green foot-anchor cross at the building's visible base
- yellow door-marker dot

The same overlay is captured in
`artifacts/screenshots/vertical_slice_collision_debug.png`.

## Validation Result

`tools/validate_vertical_slice.gd` now enforces:

- world Y-sort is on; player, HUD, map, and 5 expected buildings exist
- every building has a non-null `AtlasTexture` whose region is within the
  source atlas and has positive size
- foot anchor sits on the visible base (sprite bottom ≈ FootAnchor)
- collision overlaps the lower visible/base area (and does not float below
  the visible building)
- interaction rect's X overlaps the door marker and the rect extends south
  of the door (player walks up to the door from the south)
- there's a valid stand-position south of at least two buildings (player
  can stand in front)
- there's a valid stand-position north of at least two buildings (Y-sort
  reachable)
- every building's sprite is fully inside the initial camera view

Running locally:

```sh
godot --headless --path . --script res://tools/validate_vertical_slice.gd
```

Re-run after any change to `scenes/Main.gd`, `scenes/buildings/`, or the
source atlas PNGs.

## Web Delivery

See `WEB_DELIVERY.md`. The Godot slice ships to a **separate** Cloudflare
Pages project (`wayfarers-godot-slice`) and does NOT replace the existing
`wayfarers` Worker that still serves `wayfarer_v7_github_ready/`.

## Not Decided Yet

This does not decide full migration. The next review should judge the running
screenshot and hands-on movement around the five buildings before any
inventory, combat, save, or quest systems are ported.

## Remaining Risks

- The screenshots in `artifacts/screenshots/` were regenerated by the PIL
  approximation in `tools/render_slice_approx.py` because the build machine
  for this pass did not have Godot installed. The geometry, positions, and
  atlas crops are exact; the tile shading is approximate. Re-export from
  Godot locally before the next review snapshot.
- Cloudflare Pages cannot currently build Godot exports on its own image,
  so the upload step is manual. The Git-integrated path in
  `WEB_DELIVERY.md` is the documented future state, not the current state.
- The `merchant_shop_house` cell in `pack_v1_a.png` is a columned mansion,
  not a literal shop-with-awning. The slice ID is preserved for the
  validator's expected-buildings list; a future content pass can decide
  whether to rename the slot or repoint it at a different cell.
