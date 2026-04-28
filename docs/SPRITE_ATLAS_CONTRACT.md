# Wayfarer Sprite Atlas Contract (Phase 32S)

## Scope and phase lock
This contract locks **Phase 32** game-ready atlas requirements for buildings and world props.

- No gameplay/system behavior changes are required by this document.
- No map redesign is required by this document.
- This is the production-art handoff spec for future atlas generation and upload.

---

## 1) Runtime scale contract (current game truth)

### Core world scale
- **Tile size:** `32x32` pixels (`TILE = 32`).
- **Default world viewport:** `22 x 14` tiles (`VIEW_TILES_X`, `VIEW_TILES_Y`) = `704 x 448` world pixels.
- **Character source frame size:** `64x64` pixels; rendered down/up via per-entity scale multipliers.

### Character visual size at runtime
Using `drawW = round(64 * scale)`, `drawH = round(64 * scale)`:

- **Player (Wayfarer):** scale `0.92` => ~`59x59` px visual.
- **Village NPCs (Edrin/Hunter/Merchant):** scale `0.86` => ~`55x55` px visual.
- **Wolves:** scale `0.82` => ~`52x52` px visual.
- **Bandits:** scale `0.83-0.85` => ~`53-54x53-54` px visual.
- **Rook (elite):** scale `0.92` => ~`59x59` px visual.

**Interpretation for art:** Character bodies are approximately `1.6-1.85` tiles tall visually, while collision remains tile-based.

### Building visual footprint (current placed buildings)
Building `w/h` are in **tiles** and should remain the gameplay footprint baseline:

- `inn_tavern`: `6x5` tiles
- `mercantile_shop`: `5x5` tiles
- `village_hall_meeting_house`: `6x5` tiles
- `residence_small`: `4x4` tiles
- `residence_large`: `5x4` tiles
- `hunter_lodge_or_outfitter`: `4x4` tiles
- `pond_boathouse_or_waterfront_shed`: `5x3` tiles

For Phase 32S contract completeness, add one missing production type:
- `storage_shed`: **recommended gameplay footprint** `3x3` tiles.

### Canvas/world scaling rules
- Canvas internal resolution is set to panel CSS size (`canvas.width/height = floor(panel rect)`).
- World is rendered in tile-space to that canvas with no secondary camera zoom multiplier.
- Viewport centering uses camera offsets:
  - `offsetX = floor((canvas.width - VIEW_TILES_X*TILE)/2)`
  - `offsetY = floor((canvas.height - VIEW_TILES_Y*TILE)/2)`

### Camera scaling rules
- Camera follows player by tile target position and clamps to map bounds.
- Camera shake applies transient **pixel offsets only**; it does not alter zoom or tile scale.

### Pixel-art filtering rules (must remain)
- Canvas CSS uses `image-rendering: pixelated`.
- Render path enforces `ctx.imageSmoothingEnabled = false`.
- This is mandatory for all production atlas draws.

---

## 2) Production building atlas requirements

## 2.1 Atlas sheet dimensions and grid
Recommended production format:

- **Primary:** `2048x2048` transparent PNG
- **Alternate:** `1024x2048` transparent PNG (if packing is cleaner)
- **Cell size:** `32x32` base cell grid alignment for all sprite anchors/footprints.

Two acceptable metadata modes:

1. **Fixed-cell mode (preferred for authoring consistency):**
   - Buildings authored inside fixed virtual cells measured in tile units.
   - Sprite crop can still be tight, but anchor must map to cell footprint.
2. **Explicit-mapped mode (acceptable):**
   - Per-sprite explicit `{sx, sy, sw, sh, drawW, drawH, anchorX, anchorY}`.
   - Requires complete manifest metadata with no inferred values.

### 2.2 Building draw size envelope
To fit runtime safety limits and map readability:

- **Hard max draw size:** `6x6 tiles` (`192x192 px`) per sprite draw.
- **Hard max crop size:** `192x192 px`.
- **Target practical range:** `3x3` to `6x5` tiles, depending on building type.

### 2.3 Building type contract (required production set)
All dimensions below are in **tile units** (`tileW x tileH`) with suggested visual overhang budget.

| Building type | Gameplay visual footprint | Recommended draw box | Notes |
|---|---:|---:|---|
| `inn_tavern` | `6x5` | `6x5` (or `6x6` with roof overhang) | Main social hub silhouette |
| `mercantile_shop` | `5x5` | `5x5` | Strong storefront readability |
| `village_hall_meeting_house` | `6x5` | `6x5` | Civic landmark |
| `residence_small_a` | `4x4` | `4x4` | Distinct from B by roof/porch/chimney |
| `residence_small_b` | `4x4` | `4x4` | Alternate silhouette/palette details |
| `residence_large` | `5x4` | `5x4` (optionally `5x5`) | Slightly upscale family residence |
| `hunter_lodge_or_outfitter` | `4x4` | `4x4` | Outdoor/workshop cues |
| `pond_boathouse_or_utility_shed` | `5x3` | `5x3` | Waterfront profile |
| `storage_shed` | `3x3` | `3x3` | Service/storage utility structure |

### 2.4 Anchor point rules (buildings)
Building anchors must lock to the **front-ground contact point**:

- `anchorX`: center-front in pixels from sprite crop origin.
- `anchorY`: bottom walkable contact row in pixels from sprite crop origin.
- Runtime draw formula assumes building world anchor maps to tile anchor:
  - `drawX = tileToScreen(b.x,b.y).x + (b.anchorX*TILE) - sprite.anchorX`
  - `drawY = tileToScreen(b.x,b.y).y + (b.anchorY*TILE) - sprite.anchorY`

Default building tile anchors (when unspecified):
- `anchorX = floor(w/2)`
- `anchorY = h-1`

### 2.5 Collision footprint rules (buildings)
Collision must remain separate from full sprite art.

- Collision is defined in tile rectangles (`collision:{x,y,w,h}`).
- Typical contract: bottom `1-2` tile rows of each building footprint are solid.
- Roof/chimney/upper facade overhang must **not** add collision.
- Never use full sprite bounding box as collision.

### 2.6 Door / interact point rules
Each building requires one explicit interaction rect:

- `interaction:{x,y,w,h}`
- Default size: `1x1` tile.
- Position: door threshold tile centered on entrance.
- Must be reachable from path tile without clipping into collision.

### 2.7 Label anchor rules
Each building must define label tile and text:

- `label:{x,y,text}`
- Label tile should sit near front/upper facade center (usually 1 tile above doorway row).
- Label position must avoid overlap with roof peaks where possible.

---

## 3) Production prop atlas requirements

## 3.1 Prop atlas dimensions and grid
- **Recommended:** `1024x1024` transparent PNG.
- **If needed:** `2048x1024` for expansion.
- **Grid basis:** `32x32` cells.

### 3.2 Prop size classes (draw size targets)
All below are in pixels and tile equivalents.

| Prop group | Typical draw size | Tile equivalent | Notes |
|---|---:|---:|---|
| Fences | `32x32` straight segments | `1x1` | Include end/corner/gate variants |
| Barrels | `24-32 x 24-32` | ~`1x1` | Keep low profile |
| Crates | `24-32 x 24-32` | ~`1x1` | Distinct top-face read |
| Benches | `32-64 x 24-32` | `1x1` to `2x1` | Long side readability |
| Signs (post) | `32x48` | `1x1.5` | Can render above entities via layer flag |
| Notice board | `32-48 x 48-64` | `1-1.5 x 1.5-2` | High interaction clarity |
| Lamps / lantern posts | `32x48` to `32x64` | `1x1.5-2` | Night readability silhouette |
| Well | `32-48 x 32-48` | `1-1.5 x 1-1.5` | Centerpiece utility prop |
| Dock pieces | `32x32` modules | `1x1` | straight/corner/T/intersection |
| Shoreline props | `16-32 x 16-32` | sub-tile to `1x1` | reeds, rocks, driftwood |
| Market goods | `16-32 x 16-32` | sub-tile to `1x1` | sacks, bundles, baskets |

### 3.3 Prop anchors and layers
- Default prop ground anchor is tile bottom-center (`x + TILE/2`, `y + TILE`).
- Atlas entries must provide `anchorX/anchorY` when sprite is not exactly `32x32`.
- Tall props (signs, lamps, notice board) may use `layer:"above_entities"`.

### 3.4 Prop collision/interact guidance
- Most decorative props remain non-blocking unless gameplay requires collision.
- Blocking props should use tile blocking in world data; not sprite bounds.
- Interactable props (e.g., notice board) should define explicit interaction tile(s).

---

## 4) Art requirements (production acceptance)

All future building/prop atlas submissions must satisfy:

1. **True transparent PNG** (RGBA, no fake alpha).
2. **No baked checkerboard background** (hard reject).
3. **Tight crop** around each sprite (no massive empty margins).
4. **Fixed-cell or explicit metadata mapping** for every sprite.
5. **Top-down / slight 3-quarter RPG perspective** aligned with current world.
6. **Scale match to current player/map proportions** (32px tile world, ~52-59px character visuals).
7. **Style coherence:** 1760s Newport-inspired Hearthvale; colonial coastal New England tone.
8. **No oversized illustration crops** that exceed map readability or production limits.

---

## 5) Naming, placement, and Codex mapping workflow

## 5.1 File naming
Use lowercase snake_case with version/date suffix.

### Buildings atlas file
- `hearthvale_buildings_atlas_v1.png`

### Props atlas file
- `hearthvale_props_atlas_v1.png`

### Manifest sprite IDs (required)
Buildings:
- `inn_tavern`
- `mercantile_shop`
- `village_hall_meeting_house`
- `residence_small_a`
- `residence_small_b`
- `residence_large`
- `hunter_lodge_or_outfitter`
- `pond_boathouse_or_utility_shed`
- `storage_shed`

Props (minimum families; variant suffixes allowed):
- `fence_straight`, `fence_corner`, `fence_gate`
- `barrel_a`, `barrel_b`
- `crate_a`, `crate_b`
- `bench_wood`
- `sign_post`
- `notice_board`
- `lamp_post`
- `well_stone`
- `dock_straight`, `dock_corner`, `dock_t`
- `shore_reeds`, `shore_rock`, `shore_driftwood`
- `market_sack`, `market_basket`, `market_crate_goods`

## 5.2 Asset placement paths
Upload future production PNGs to:

- `wayfarer_v7_github_ready/worker/assets/wayfarer/buildings/`
- `wayfarer_v7_github_ready/worker/assets/wayfarer/props/`

## 5.3 Codex mapping steps after upload
1. Update `atlasManifests.buildings.imagePath` and `atlasManifests.props.imagePath`.
2. Add/replace sprite metadata entries (`sx/sy/sw/sh/drawW/drawH/anchorX/anchorY`).
3. Set `productionReady:true` per approved sprite entry.
4. Enable atlas switches only when QA passes:
   - `allowProductionSprites:true`
   - `USE_PRODUCTION_BUILDING_ATLAS = true`
5. Expand `BUILDING_SPRITE_ID_BY_BUILDING_ID` and `PROP_SPRITE_BY_WORLD_TYPE` mappings to final IDs.
6. Keep fallback rendering path intact for missing/failed sprite entries.
7. Run Phase 32 visual QA checklist before merge.

---

## 6) Out-of-contract content (explicitly excluded)
- Combat rebalance
- Quest logic changes
- Save schema changes
- UI redesign
- World/map layout redesign
- New gameplay mechanics

This contract is art-pipeline and atlas-integration only.
