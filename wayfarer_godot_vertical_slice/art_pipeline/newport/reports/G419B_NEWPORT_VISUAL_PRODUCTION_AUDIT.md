# G-4.19B Newport Visual Production System & Core Asset Audit

Status: production-structure pass. No new sprite sheets were generated, no
building sprites were rebuilt, and no map placement was redesigned.

## North Star

Newport is the starting town/village for Wayfarer. It must become a
believable, enjoyable, navigable opening location, not merely a collection of
pretty props.

Every visual asset and placement decision should support:

- believable coastal town identity
- readable player navigation
- harbor, market, civic, and residential organization
- emotional invitation to explore
- gameplay readiness
- visual consistency with the G-4.18D/G-4.19A atelier standard

## Registry

The production registry now lives at:

`art_pipeline/newport/manifests/newport_visual_production_registry.json`

It classifies major Newport visual assets by ID/name, category, file path,
source/provenance status, current usage, visual quality status, gameplay role,
rebuild status, and notes. Building entries also include provenance confidence,
atelier consistency, scale/perspective fit, grounding quality, and town role.

Registry status vocabulary:

- `APPROVED_FINAL`
- `APPROVED_TEMPORARY`
- `NEEDS_REWORK`
- `REBUILD_REQUIRED`
- `REBUILD_REQUIRED_CENTERPIECE`
- `DEPRECATED_DO_NOT_USE`
- `PROVENANCE_UNKNOWN`

No current Newport visual asset is promoted to `APPROVED_FINAL` in this pass.
The G-4.18D cargo and G-4.19A dock clutter packs are approved temporary
review-quality atelier targets while AI-assisted final license policy remains
pending.

## Building Audit Summary

The current active building set remains playable and useful for composition
review, but it is not final trusted art. The G-4.18A provenance audit already
classified the current building sprites as `temporary_review_yellow`; G-4.19B
adds North Star role/readiness classification on top of that provenance gate.

General building verdict:

- Current buildings may remain in normal review as temporary layout,
  navigation, and district-identity anchors.
- Current buildings must not be treated as final source-trusted art.
- Current buildings should be rebuilt or source-cleared before any final
  Newport visual lock.
- Building rebuild/enhancement is Wave 4, after environmental and town-life
  context improves enough to judge buildings in-place.

Active building roles audited:

- Tavern/Inn: harborfront social hub and landmark.
- Mercantile, shop house, chandlery: commercial row and shop navigation.
- Counting house and custom house: civic/economic authority.
- Market shed and sacks/baskets support: market/economy read.
- Storehouses, dock warehouse, boathouse: working-wharf mass and waterline
  identity.
- Small residence, large residence, boarding house, clerk/dockworker rowhouses:
  residential/support-lane life.
- Cooperage shed: harbor craft/service role.

## Tavern/Inn Centerpiece Lock

The Newport Tavern/Inn is no longer a generic tavern. It is an anchor asset.

Locked future direction:

- brick construction
- two sets of large twin-stack chimneys
- inspired by the grand coastal hotel presence of Hotel Viking
- larger, warmer, and more memorable than ordinary town buildings
- major player landmark, social hub, and quest anchor
- historic coastal inn with old brick, warm windows, heavy fireplaces,
  maritime town prestige, and fantasy charm

Current asset verdict:

`REBUILD_REQUIRED_CENTERPIECE`

The current `inn_tavern_v1_isolated.png` crop is usable as a temporary review
placeholder, but it does not clearly support the locked direction. It lacks
the brick Hotel Viking-inspired presence, the required twin-stack chimney
language, and the scale/memorability needed for Newport's major social anchor.
Do not patch it quickly. Treat it as a Wave 4 centerpiece rebuild.

## Non-Building Audit Summary

Cargo/props:

- G-4.18D atelier cargo is the accepted visual quality target for cargo props:
  crate, barrel, rope coil, and wharf cargo cluster.
- Older deterministic/procedural cargo reads and yellow hero cargo clusters are
  not final targets.

Dock clutter:

- G-4.19A dock clutter is the first follow-on atelier rollout pack:
  bollards, mooring hardware, fishing net, sacks/fish baskets, anchor/rope,
  repair planks, lantern, and shoreline debris.
- Only the controlled subset is placed in normal review. Anchor/rope and
  shoreline debris remain available but unplaced until a later no-over-scatter
  decision.

Terrain, paths, shoreline, and harbor visuals:

- G-4.18 hero-street terrain/path/shoreline pieces remain useful temporary
  yellow review art.
- They are not automatically final and should be replaced or promoted through
  Wave 1 production discipline.
- G-4.16 procedural surfaces remain a playable fallback, not final art.

Signs, lamps, posts, market props:

- Some temporary yellow/procedural signs, lamps, posts, fences, benches, and
  shopfront/market dressing still support navigation and town life.
- They are Wave 2/Wave 3 candidates, not final assets.

Characters/NPCs:

- The player is still drawn procedural placeholder art.
- Edrin Vale remains disabled in the current starter-town review.
- Character/NPC art should wait for Wave 5 after Newport's environment has
  enough visual context for scale/style judgment.

Lab-only/deprecated visual targets:

- G-4.18B green-origin proof assets are provenance evidence only after their
  visual failure.
- G-4.18D.1 M01B and G-4.18D.2 capability assets remain lab/provenance
  evidence, not normal-review or final visual targets.

## Mass Production Waves

G-4.19B changes Newport visual work from isolated single-sheet passes to
production waves.

Wave 1 - Environmental believability:

- terrain edge dressing
- cobble/path transitions
- shoreline dressing
- road borders
- mud/grass/stone blend pieces

Wave 2 - Town identity:

- signs
- lamps
- posts
- notice boards
- banners
- civic markers

Wave 3 - Economy/life:

- market carts
- crates of goods
- shopfront props
- merchant tables
- baskets/barrels/sacks variants

Wave 4 - Building rebuild or enhancement:

- begins only after audit decisions are accepted
- includes the Tavern/Inn centerpiece rebuild
- treats current yellow building art as temporary unless source-cleared

Wave 5 - Character/NPC standard:

- begins only after the town environment has enough visual context
- replaces the drawn player/NPC placeholders with a durable style standard

## Validator Expectations

G-4.19B validation should protect:

- registry entries missing status, category, or path
- missing provenance/source status
- assets marked final without final provenance
- deprecated assets used in normal/final paths
- atelier assets missing required artifacts
- MapLayer references to deprecated visual targets outside lab-only scope
- G-4.18D cargo and G-4.19A dock clutter continuing to validate and render
