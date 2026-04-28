# Wayfarer Sprite Atlas Contract (Phase 32T)

## Runtime constants
- Tile size: `TILE = 32`
- Character draw targets:
  - Player: scale `0.92` (~59x59)
  - Village NPCs: scale `0.86` (~55x55)
  - Wolves: scale `0.82` (~52x52)
  - Bandits: scale `0.83-0.85` (~53-54)
  - Rook: scale `0.92` (~59x59)

## Building footprint assumptions
- `inn_tavern`: `6x5`
- `mercantile_shop`: `5x5`
- `village_hall_meeting_house`: `6x5`
- `residence_small`: `4x4`
- `residence_large`: `5x4`
- `hunter_lodge_or_outfitter`: `4x4`
- `pond_boathouse_or_waterfront_shed`: `5x3`

## Production envelope and atlas sizes
- Building hard envelope: max `6x6` tiles (`192x192` px)
- Practical building range: `3x3` to `6x5`
- Building atlas target: `2048x2048` preferred (`1024x2048` acceptable)
- Prop atlas target: `1024x1024` preferred (`2048x1024` acceptable)
- Grid basis: `32x32`

## Filenames and folders
- Buildings folder: `wayfarer_v7_github_ready/worker/assets/wayfarer/buildings/`
  - `hearthvale_buildings_atlas_v1.png`
  - `hearthvale_buildings_atlas_v1.manifest.json`
- Props folder: `wayfarer_v7_github_ready/worker/assets/wayfarer/props/`
  - `hearthvale_props_atlas_v1.png`
  - `hearthvale_props_atlas_v1.manifest.json`

## Placement and anchors
- Building anchor = front-ground contact.
- `anchorX` = center-front px from sprite crop origin.
- `anchorY` = bottom walkable row px from sprite crop origin.
- Runtime placement:
  - `drawX = tileToScreen(b.x,b.y).x + (b.anchorX*TILE) - sprite.anchorX`
  - `drawY = tileToScreen(b.x,b.y).y + (b.anchorY*TILE) - sprite.anchorY`
- Defaults if omitted:
  - `anchorX = floor(w/2)`
  - `anchorY = h - 1`

## Collision / interaction rules
- Collision must use tile rects only (typically bottom 1-2 rows).
- Roof/overhang art does **not** create collision.
- Interaction points are explicit doorway threshold tiles.
- Label anchors are explicit metadata.
- Props default to bottom-center ground anchoring.
- Tall props may use `renderLayer: "above_entities"`.

## Manifest entry contract
Each building/prop entry includes:
- `id`
- `atlas`
- `sourceRect` (`x,y,w,h`)
- `tileFootprint` (`w,h`)
- `anchorX`, `anchorY`
- `collisionRect`
- `interactionRect` (if applicable)
- `labelAnchor` (if applicable)
- `renderLayer` (if applicable)
- rollout flags (`proofEnabled`, `productionReady`)

## Proof-mode rollout contract
- Feature flag: `USE_HEARTHVALE_ATLAS_PROOF`
- Proof-only Phase 32T integration:
  - Buildings: village hall + mercantile
  - Props: bench, barrel, crate, signpost
- All non-proof assets remain on fallback rendering until staged expansion passes QA.
