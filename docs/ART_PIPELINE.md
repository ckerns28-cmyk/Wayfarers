# Art Pipeline (Phase 32H Option B)

## Asset folders
Wayfarer sprite assets are served from Worker static assets:

- `wayfarer_v7_github_ready/worker/assets/wayfarer/terrain/`
- `wayfarer_v7_github_ready/worker/assets/wayfarer/buildings/`
- `wayfarer_v7_github_ready/worker/assets/wayfarer/characters/`
- `wayfarer_v7_github_ready/worker/assets/wayfarer/props/`
- `wayfarer_v7_github_ready/worker/assets/wayfarer/ui/`

## Atlas manifest format
Manifests are defined in `worker/src/index.js` under `atlasManifests`.

Each atlas entry contains:
- `imagePath`
- `tileSize`
- `sprites[spriteId] = { sx, sy, sw, sh, anchorX?, anchorY? }`

## Draw order
Current renderer order:
1. Ground terrain
2. Roads / shoreline / water
3. Props behind entities (`layer !== "above_entities"`)
4. Building sprites (atlas with placeholder fallback)
5. Entities / NPCs / hostiles / player
6. Props above entities (`layer === "above_entities"`)
7. Labels / UI

## Collision vs visuals
Building placement is data-driven and split into:
- visual placement (`spriteId`, `x/y`, `w/h`, `anchorX/anchorY`)
- collision bounds (`collision:{x,y,w,h}`)
- interaction tile (`interaction:{x,y,w,h}`)
- label data (`label:{x,y,text}`)

## Scaling and pixel rules
- Tile size: `32px`
- Character frame size: `64px`
- `image-rendering: pixelated` on canvas
- `ctx.imageSmoothingEnabled = false` in world scene render paths

## Replacing placeholder assets
1. Drop PNG sheets into matching folders.
2. Keep filenames matching current manifest paths, or update `atlasManifests` paths.
3. Update `sprites` source rectangles/anchors.
4. Validate in browser (missing files auto-fallback to clearly marked placeholder building draw).
