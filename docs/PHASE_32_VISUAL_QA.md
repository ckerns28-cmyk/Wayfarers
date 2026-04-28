# Phase 32 Visual QA (Atlas Contract Verification)

Use this checklist when integrating any new building/prop atlas in Phase 32.

## A) Scale and rendering invariants
- [ ] Tile size remains `32px`.
- [ ] Viewport remains `22x14` tiles.
- [ ] Player visual size remains ~`59x59` px.
- [ ] NPC visual size remains ~`55x55` px.
- [ ] Common enemy visuals remain ~`52-54` px.
- [ ] Canvas remains `image-rendering: pixelated`.
- [ ] `ctx.imageSmoothingEnabled = false` is preserved in world render loop.

## B) Atlas load and mapping checks
- [ ] Building atlas PNG loads from expected path.
- [ ] Prop atlas PNG loads from expected path.
- [ ] No known-bad quarantine atlas paths are active.
- [ ] Every required building sprite ID exists in atlas manifest.
- [ ] Every required prop sprite ID used by world mapping exists in atlas manifest.
- [ ] No out-of-bounds crops (`sx/sy/sw/sh`) for any mapped sprite.
- [ ] No blank/checkerboard crops in mapped production entries.

## C) Building contract checks
- [ ] Required building types are present:
  - [ ] `inn_tavern`
  - [ ] `mercantile_shop`
  - [ ] `village_hall_meeting_house`
  - [ ] `residence_small_a`
  - [ ] `residence_small_b`
  - [ ] `residence_large`
  - [ ] `hunter_lodge_or_outfitter`
  - [ ] `pond_boathouse_or_utility_shed`
  - [ ] `storage_shed`
- [ ] Building draw sizes are within `<= 6x6` tiles (`<= 192x192 px`).
- [ ] Anchor points align doors/footings to world tiles.
- [ ] Collision uses configured `collision` rects (not full sprite bounds).
- [ ] Interaction tiles line up with visible entrance tiles.
- [ ] Labels are readable and placed consistently.

## D) Prop contract checks
- [ ] Fence pieces align cleanly to `32x32` tile grid.
- [ ] Barrel/crate sizes do not visually overpower characters.
- [ ] Bench/sign/notice board silhouettes are legible at gameplay camera distance.
- [ ] Lamp posts and tall signs layer correctly when marked `above_entities`.
- [ ] Wells and dock pieces maintain top-down / slight 3-quarter consistency.
- [ ] Shoreline props and market goods avoid noisy visual clutter.

## E) Art acceptance checks
- [ ] PNGs are true RGBA transparency.
- [ ] No baked checkerboard backgrounds.
- [ ] Crops are tight and metadata-complete.
- [ ] Perspective matches top-down / slight 3-quarter RPG view.
- [ ] Style aligns with 1760s Newport-inspired Hearthvale.
- [ ] No oversized illustration-style crops.

## F) Rollout safety checks
- [ ] Fallback rendering remains available for unmapped/missing sprites.
- [ ] Save/load works after atlas integration.
- [ ] Quests/combat/interactions unchanged by asset swap.
- [ ] No map collision regressions around buildings/props.
- [ ] Visual QA pass recorded before enabling production toggles.
