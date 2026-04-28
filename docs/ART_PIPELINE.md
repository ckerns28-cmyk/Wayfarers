# Art Pipeline (Phase 32T)

## Asset folders
Wayfarer sprite assets are served from Worker static assets:

- `wayfarer_v7_github_ready/worker/assets/wayfarer/terrain/`
- `wayfarer_v7_github_ready/worker/assets/wayfarer/buildings/`
- `wayfarer_v7_github_ready/worker/assets/wayfarer/characters/`
- `wayfarer_v7_github_ready/worker/assets/wayfarer/props/`
- `wayfarer_v7_github_ready/worker/assets/wayfarer/ui/`

## Hearthvale atlas files (Phase 32T)
- Building atlas PNG target: `hearthvale_buildings_atlas_v1.png`
- Building manifest: `hearthvale_buildings_atlas_v1.manifest.json`
- Prop atlas PNG target: `hearthvale_props_atlas_v1.png`
- Prop manifest: `hearthvale_props_atlas_v1.manifest.json`

## Runtime source of truth
- Runtime integration: `wayfarer_v7_github_ready/worker/src/index.js`
- Contract: `docs/SPRITE_ATLAS_CONTRACT.md`
- Visual QA: `docs/PHASE_32_VISUAL_QA.md`

## Manifest structure
Each manifest entry supplies at minimum:
- `id`
- `atlas`
- `sourceRect` (`x,y,w,h`)
- `tileFootprint` (`w,h` in tiles)
- `anchorX`,`anchorY`
- `collisionRect`
- `interactionRect` (if applicable)
- `labelAnchor` (if applicable)
- `renderLayer` (if needed)
- rollout flags: `proofEnabled`, `productionReady`

## Proof-mode behavior
- Toggle: `USE_HEARTHVALE_ATLAS_PROOF` in `index.js`.
- Default is `false` for production safety.
- In proof mode only:
  - Buildings: `b_village_hall`, `b_mercantile`
  - Props: `bench`, `barrel`, `crate`, `signPost`
- If atlas/manifest load fails, rendering falls back to procedural/tile fallback (no crash path).

## Collision and interaction policy
- Building collision remains tile-rect driven (`collision` in world data), not sprite bounds.
- Roof/overhang visuals never add collision.
- Door interaction points remain explicit doorway threshold tiles.

## Next expansion step
After proof validation, add transparent production-ready atlas PNGs and progressively enable additional building IDs by flipping per-entry `proofEnabled` and then global production flags.
