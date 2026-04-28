# Phase 32 Visual QA (Atlas Proof Integration)

## A) Safety gates
- [ ] `USE_HEARTHVALE_ATLAS_PROOF` defaults to `false` in production branch.
- [ ] Fallback buildings still render when atlas manifest or PNG fails to load.
- [ ] No black screen / blank world on atlas load failure.
- [ ] No white proof blocks.
- [ ] No giant raw-sheet overlays.

## B) Proof set currently integrated
### Buildings (proof-only)
- [ ] `b_village_hall` -> `village_hall_meeting_house`
- [ ] `b_mercantile` -> `mercantile_shop`

### Props (proof-only)
- [ ] `bench` -> `bench_market`
- [ ] `barrel` -> `barrel_oak`
- [ ] `crate` -> `crate_market`
- [ ] `signPost` -> `signpost_square`

## C) Geometry and gameplay invariants
- [ ] Tile size remains `32`.
- [ ] Building draw envelope remains `<= 192x192`.
- [ ] Collision remains tile-rect only (roof overhang non-colliding).
- [ ] Door thresholds remain reachable.
- [ ] Labels and interaction anchors remain explicit.

## D) Atlas correctness
- [ ] Crops are in-bounds (`sx/sy/sw/sh`).
- [ ] Transparency is correct in integrated sprites.
- [ ] No checkerboard/white-backed source content reaches world rendering.
- [ ] Pixel crispness preserved (`imageSmoothingEnabled=false`, CSS pixelated).

## E) Known limitations
- Proof manifests and loader are integrated, but final atlas PNGs must still be supplied in the target folders.
- Non-proof building roles remain on fallback rendering until staged rollout continues.

## F) Recommended next step
Upload transparent, game-ready `hearthvale_buildings_atlas_v1.png` + `hearthvale_props_atlas_v1.png`, run proof mode in QA, then expand by one building role per pass.
