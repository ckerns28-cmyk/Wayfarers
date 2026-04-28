# Art Pipeline (Phase 32S)

## Asset folders
Wayfarer sprite assets are served from Worker static assets:

- `wayfarer_v7_github_ready/worker/assets/wayfarer/terrain/`
- `wayfarer_v7_github_ready/worker/assets/wayfarer/buildings/`
- `wayfarer_v7_github_ready/worker/assets/wayfarer/characters/`
- `wayfarer_v7_github_ready/worker/assets/wayfarer/props/`
- `wayfarer_v7_github_ready/worker/assets/wayfarer/ui/`

## Source of truth
- Runtime atlas integration and drawing logic: `wayfarer_v7_github_ready/worker/src/index.js`
- Game-ready atlas contract: `docs/SPRITE_ATLAS_CONTRACT.md`
- Phase visual QA checklist: `docs/PHASE_32_VISUAL_QA.md`

## Atlas manifest format
Atlas manifests are defined in `worker/src/index.js` under `atlasManifests`.

Each atlas entry contains:
- `imagePath`
- `tileSize`
- `sprites[spriteId] = { sx, sy, sw, sh, drawW?, drawH?, anchorX?, anchorY?, productionReady? }`

## Draw order (world)
1. Terrain / roads / water / shoreline
2. Buildings
3. Props behind entities (`layer !== "above_entities"`)
4. Entities (NPCs, enemies, player)
5. Props above entities (`layer === "above_entities"`)
6. Labels / UI overlays

## Collision vs visuals
Building placement remains data-driven and split into:
- visual placement (`spriteId`, `x/y`, `w/h`, `anchorX/anchorY`)
- collision bounds (`collision:{x,y,w,h}`)
- interaction tile (`interaction:{x,y,w,h}`)
- label anchor (`label:{x,y,text}`)

## Scaling and pixel rules
- Tile size: `32px`
- Character frame size: `64px`
- Canvas CSS: `image-rendering: pixelated`
- Render path: `ctx.imageSmoothingEnabled = false`

## Integration workflow for new production sheets
1. Place PNGs in `worker/assets/wayfarer/buildings/` and `worker/assets/wayfarer/props/`.
2. Update `atlasManifests.*.imagePath` to new files.
3. Add/update `sprites` metadata entries.
4. Map world IDs to sprite IDs (`BUILDING_SPRITE_ID_BY_BUILDING_ID`, `PROP_SPRITE_BY_WORLD_TYPE`).
5. Mark approved sprites with `productionReady:true`.
6. Enable production toggles only after QA pass.
7. Validate using `docs/PHASE_32_VISUAL_QA.md`.

## Constraints
- Do not introduce gameplay/system/map changes as part of art swaps.
- Keep fallback rendering paths intact during rollout.
