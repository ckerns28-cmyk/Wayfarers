# Wayfarers Art Pipeline Contract (Phase 32)

This contract defines what is required for **production** external sprites (buildings + props).

## Current status

- External PNG atlas loading remains enabled and instrumented in `worker/src/index.js` (`atlasManifests`, `initAtlasImages`, probe/load runtime diagnostics).
- `drawImage` atlas rendering remains supported.
- The currently uploaded medieval town building/prop sheets are treated as **debug/proof assets only** and are blocked from production placement.

## Production building sprite requirements

All production building sprites must satisfy the following:

1. **True transparent PNG background**
   - PNG alpha channel must represent transparency.
   - No checkerboard baked into RGB pixels.

2. **Consistent pixel-art style**
   - Must match in-game palette and detail density.
   - No illustration-scale rendering.

3. **Atlas metadata contract**
   - Every sprite entry includes valid numeric atlas metadata:
     - crop: `sx`, `sy`, `sw`, `sh`
     - anchors: `anchorX`, `anchorY`
     - draw size: `drawW`, `drawH` (or omitted to use `sw`/`sh`)
   - Crop rectangle must be in-bounds for the loaded sheet.

4. **Fixed cells or explicit metadata**
   - Use either:
     - fixed cell grid atlas, or
     - explicit per-sprite crop metadata (current code path).

5. **Tight object bounds**
   - Crops must tightly bound the object with minimal dead space.
   - No giant uncropped regions.

6. **Map-appropriate gameplay scale**
   - Sprite draw size must fit map readability and current player/world scale.
   - Buildings must not cover huge portions of the map.

7. **Perspective requirement**
   - Top-down or slight 3/4 RPG perspective to match existing world art.

8. **Visual vs collision bounds**
   - Visual sprite bounds remain decoupled from collision/interaction bounds.
   - Collision stays tile-driven by gameplay data.

## Production safety gates

Before drawing any external atlas sprite in production, the renderer validates:

- atlas asset `productionReady === true`
- sprite entry `productionReady === true`
- sprite entry `debugOnly !== true`
- production atlas path is enabled
- sprite ID exists and metadata is valid
- selected source is not a known bad/test sheet
- crop dimensions are within production limits
- draw dimensions are within map-scale limits
- crop must match transparent/tight-crop expectations (blank/checkerboard heuristic)
- atlas crop passes existing runtime load/bounds/blank-check heuristic

If any check fails, renderer falls back to the procedural building renderer.

## Debug/proof mode usage

- Known bad sheet crops may still be inspected via atlas debug/proof tooling.
- They are intentionally blocked from production world placement until replaced with compliant assets.
