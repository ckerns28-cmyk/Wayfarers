# Newport Town Godot Foundation

G-4.1 replaces the reduced Newport Harbor Test scene with a player-facing
Newport-inspired starting port town in Godot. The JavaScript Worker remains the
separate Phase 35.13R production/reference route.

G-4.2 keeps the same building foundation and focuses on lived-in composition:
street-level spawn framing, reduced test-grid readability, narrower walk
surfaces, harbor clutter, shoreline detail, and small physical blockers that
shape movement without changing quests or systems.

G-4.3 responds to screenshot review showing that the town still felt like
sprites placed on a grid canvas. It keeps the building set but recomposes the
visible world around continuous streets, shaped wharf edges, clustered
frontage clutter, and a tighter first-screen waterfront arrival.

G-4.4 keeps the same building count and treats the first 60-90 seconds of
movement as the acceptance target: wharf start, dockside work area,
commercial frontage, civic/church square, and inland residential/service edge.

G-4.5 is a one-street seating proof for the waterfront commercial frontage.
It keeps the town footprint and building count stable, then makes five
frontage buildings sit on a shared street plane with explicit visual-base
anchors, frontage points, collision rectangles, y-sort markers, grounding
shadows, and a `B` debug overlay.

G-4.6 responds to screenshot review that showed G-4.5 still failed at player
scale. It does not defend the five-building layout. It shrinks the acceptance
target to three waterfront buildings, one authored street/stoop plane, one
player, and one camera frame.

G-4.7 responds to screenshot review that showed G-4.6 also failed. It stops
town work and switches to a four-variant visual calibration board for scale,
camera, sidewalk, stoop, curb, street, and building anchor grammar.

## Source Of Truth

The Godot town layout is authored in:

- `scripts/NewportTownBlueprint.gd`: map dimensions, road hierarchy, water,
  wharf/pier layout, districts, building placements, spawn, and QA targets.
- `scripts/BuildingCatalog.gd`: atlas source, tight regions, anchors, and draw
  widths for the current building sprites.

`Main.gd`, `MapLayer.gd`, `CollisionNavigationLayer.gd`, and
`tools/validate_vertical_slice.gd` consume the blueprint instead of each keeping
their own Newport map assumptions.

## Implemented Districts

- `harbor_wharf`: harbor basin, seawall, wharf supports, waterfront apron,
  central pier, and multiple dock fingers.
- `waterfront_commercial`: inn, mercantile, counting house, chandlery,
  shop-house, and townhouse frontage.
- `civic_district`: village hall, custom house, civic square, civic green, and
  connector road.
- `upper_residential_terrace`: large residence, Georgian residence, elite
  mansion, prestige block, gardens, and formal frontage.
- `service_outfitter_lane`: harbor cottage, townhouse row, service dependency,
  hunter lodge/outfitter, and rough service-lane edge.

## Implemented Buildings

The G-4.1 town implements all 19 Newport reference building IDs:

1. `b_boathouse`
2. `b_dock_storehouse`
3. `b_market_shed`
4. `b_inn_tavern`
5. `b_mercantile`
6. `b_counting_house`
7. `b_chandlery_front`
8. `b_shop_house`
9. `b_custom_house`
10. `b_village_hall`
11. `b_res_small`
12. `b_townhouse_row_a`
13. `b_townhouse_row_b`
14. `b_service_dependency`
15. `b_hunter_lodge`
16. `b_res_large`
17. `b_georgian_residence`
18. `b_elite_mansion`
19. `b_prestige_block`

## Asset Reuse And Substitutes

The pass uses the existing painterly building atlases in
`assets/buildings/`. No colored-box replacements were added.

Temporary substitutions:

- `b_market_shed` uses the closest market/frontage shed cell from Newport pack
  B.
- `b_service_dependency` uses the compact service shed from the base Hearthvale
  atlas.
- `b_prestige_block` uses the formal townhouse block from Newport pack B.

These are acceptable for the G-4.1 town foundation. Future art passes can
replace them with more exact source art while keeping the same building IDs and
blueprint slots.

## Movement And Collision

G-4.1 through G-4.7 provide practical collision/navigation support only:

- Building bodies block the player at the visual base/foot line.
- Water collision is generated from blueprint water tiles while leaving wharf
  street and pier tiles walkable.
- The player spawns on the wharf apron route and can reach dockside work
  clutter, commercial frontage, the civic square, pier frontage, upper
  residential road, and service lane.
- G-4.2 adds small detail blockers for crates, tables, benches, and dockside
  clutter so streets feel shaped without trapping the player.
- G-4.4 moves market/table blockers off the center of the route and adds a few
  dockside blockers to give the wharf edge weight without blocking the first
  walk.
- G-4.5 calibrates the waterfront proof street so building collision follows
  physical base/body rectangles instead of the full painterly sprite image.
- G-4.6 limits the active proof scene to three proof-street buildings so scale,
  stoops, sidewalk, street, wharf edge, collision, and camera can be judged
  without the rest of the town confusing the result.
- G-4.7 is a calibration mode, not a town mode: it shows four side-by-side
  visual treatments and keeps debug off by default.

This deliberately avoids recreating the JavaScript seating-contract audit.
Godot uses sprite anchors, collision shapes, and a route-oriented playability
validator instead.

## G-4.2 Lived-In Pass

G-4.2 does not add more buildings. It keeps all 19 G-4.1 building IDs and
improves the inhabited-town read:

- Camera: closer zoom with a slight waterfront offset so the first screen feels
  like arrival inside the town, not a full map overview.
- Streets: road, alley, plaza, and wharf surfaces draw narrower than their
  route tiles, with softer outlines and less exposed grid.
- Waterfront: crates, barrels, posts, rope coils, market table, fish rack, net
  bundles, rowboat, and shoreline rocks.
- Districts: commercial/civic/residential placements are nudged into less
  even spacing while preserving the existing Newport building set.
- HUD: reduced width and translucent panel styling so it does not dominate the
  spawn view.

The validator checks camera zoom/offset, lived-in detail density, detail
blocker count, 19-building presence, districts, and core route reachability.

## G-4.3 Harbor Town Recompose

G-4.3 is not a building-count phase. It keeps all 19 building IDs from G-4.1
and addresses the map-as-grid problem directly:

- Ground: large continuous district washes replace visible tile-by-tile grass
  across the first screen.
- Streets: waterfront street, civic connector, upper residential road, service
  lanes, civic plaza, and wharf apron are drawn as shaped walk surfaces rather
  than exposed square test bands.
- Waterfront: water, shoreline, wharf apron, pier planks, posts, rocks, boats,
  rope, nets, barrels, crates, and market tables are composed around the
  harbor edge and useful building fronts.
- Clustering: commercial/civic/waterfront details are placed around doors,
  market frontages, dock storehouse edges, and service yards so buildings feel
  tied to their district instead of floating evenly on open grass.
- Review framing: the player spawns on the waterfront street, the camera is
  tighter, and the HUD is smaller/less opaque so the first screen reads as an
  in-town arrival.

The expected visible review identity is:

```text
Build label: Godot G-4.3 Harbor Town Recompose
Phase: G-4.3 | Review host: itch
Channel: manual ZIP
Branch: codex/g-4-3-newport-harbor-town-recomposition
```

## G-4.4 Harbor Walk Acceptance

G-4.4 is a player-scale walk pass. It does not add buildings or gameplay
systems. It makes the existing town easier to read while walking:

- Route: player spawn moves to the wharf apron at `(736, 620)`, with route QA
  targets for harbor start, dockside working area, commercial frontage,
  central pier frontage, civic landmark, residential edge, and service lane.
- HUD: compact review mode is the default so screenshots show more town. The
  build label and phase stay visible; `F2` toggles extended metadata.
- Camera: a slightly tighter walking zoom and softer offset keep the player
  readable while letting landmarks enter the frame instead of presenting the
  whole map at once.
- Waterfront: wharf apron, pier heads, posts, market tables, fish racks, rope,
  nets, rowboats, barrels, and crates are repositioned around the actual walk
  path.
- District read: commercial frontage gets signs/crates/barrels, civic gets
  smaller green/plaza edges, and inland/service areas retain fences,
  clothesline, woodpile, and yard clutter.

Review vistas for the manual itch upload:

1. Wharf view: start near `(736, 620)`. The view should show the wharf apron,
   dock posts, waterline, market tables, rope/net/fish details, and piers.
2. Commercial street view: walk north/east around `(704, 572)`. The view
   should show grounded shopfronts, signs, barrels, crates, and a narrower
   waterfront street.
3. Civic/inland view: walk north to around `(650, 384)`. The view should show
   the civic/church/custom-house square with the inland route toward
   residential and service edges.

The expected visible review identity is:

```text
Build label: Godot G-4.4 Harbor Walk Acceptance
Phase: G-4.4 | Review host: itch
Channel: manual ZIP
Branch: codex/g-4-4-newport-harbor-walk-acceptance
```

## G-4.5 Building Seating Proof

G-4.5 focuses on one believable street instead of more buildings. The proof
street is the waterfront commercial frontage:

1. `b_inn_tavern`
2. `b_mercantile`
3. `b_counting_house`
4. `b_chandlery_front`
5. `b_shop_house`

For these buildings, the Node2D position now represents the calibrated
visual-base and y-sort plane for the street frontage. The sprite is offset from
that plane with a source-pixel `visual_base_anchor`, while collision,
frontage, door, shadow, and y-sort markers are separate metadata. This lets
painterly rooflines and side overhangs extend visually without turning the
entire painted image into collision or making the building float above the
street.

The proof street also gets a shared cobbled/apron surface, door-step alignment,
and subtler base shadows so doors face walkable street space instead of broad
grid rectangles.

Press `B` during review to toggle the seating overlay for proof-street
buildings. The overlay is off by default and shows:

- base/footline marker
- frontage marker
- collision rectangle
- y-sort/depth anchor
- building ID label

Implementation details are documented in
`wayfarer_godot_vertical_slice/docs/BUILDING_SEATING_AND_ANCHORS.md`.

The expected visible review identity is:

```text
Build label: Godot G-4.5 Building Seating Proof
Phase: G-4.5 | Review host: itch
Channel: manual ZIP
Branch: codex/g-4-5-building-seating-calibration-one-street-proof
```

## G-4.6 Three-Building Street Proof

G-4.6 is an honesty pass after the failed G-4.5 screenshot. The active review
build intentionally shows only three waterfront commercial buildings:

1. `b_mercantile`
2. `b_counting_house`
3. `b_chandlery_front`

The proof frame changes:

- Building count is reduced from 19/5 visible proof buildings to 3 active
  proof buildings.
- Edrin is removed from the proof frame so the player is the only character.
- Building draw widths are overridden for this proof so they sit closer to
  player street scale.
- The old broad tan slab is replaced by a narrow sidewalk, stoop pads, curb,
  darker cobbled street, wharf strip, and harbor hint.
- Camera zoom/offset are tuned for one street frame instead of town overview.
- `B` still toggles the seating overlay, now scoped to the three proof
  buildings.

The expected visible review identity is:

```text
Build label: Godot G-4.6 Three-Building Street Proof
Phase: G-4.6 | Review host: itch
Channel: manual ZIP
Branch: codex/g-4-6-three-building-street-plane-proof
```

## G-4.7 Visual Scale And Street Grammar Calibration

G-4.7 does not expand Newport. It preserves G-4.6 as a failed baseline and
shows four comparison treatments:

1. Variant A: current scale reference, deliberately labeled likely failing.
2. Variant B: smaller player / more human scale.
3. Variant C: lower camera / tighter street vignette.
4. Variant D: integrated sidewalk, stoop, curb, narrower lane, wharf strip, and
   base props.

The active calibration IDs are:

1. `g47_a_mercantile`
2. `g47_a_counting_house`
3. `g47_b_mercantile`
4. `g47_b_counting_house`
5. `g47_c_mercantile`
6. `g47_c_counting_house`
7. `g47_d_mercantile`
8. `g47_d_counting_house`

Art-direction recommendation: Variant D is the candidate town standard if the
manual itch screenshot clearly reads better than G-4.6. The smaller player
scale around `0.76` to `0.78` is the preferred human-scale direction. The
building sprites remain viable only with hand-authored anchors, frontages,
collision rectangles, shadows, and occasional draw-width overrides.

The expected visible review identity is:

```text
Build label: Godot G-4.7 Scale Grammar Calibration
Phase: G-4.7 | Review host: itch
Channel: manual ZIP
Branch: codex/g-4-7-visual-scale-street-grammar-calibration
```

## Deferred

- Final art parity with JavaScript Phase 35.13R.
- Quests, combat, inventory, save migration, and production cutover.
- Butler automation and Cloudflare Pages deployment.
- New source art for exact per-building replacements.

Manual review still requires uploading
`wayfarer_godot_vertical_slice/artifacts/wayfarers-tale-godot-web.zip` to itch.
