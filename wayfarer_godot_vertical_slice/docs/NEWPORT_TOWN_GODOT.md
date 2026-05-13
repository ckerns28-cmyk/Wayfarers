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
shadows, and a `B` debug overlay. G-4.13A later separates those older
collision rectangles into visual bounds, lot bounds, and tight collision
footprints.

G-4.6 responds to screenshot review that showed G-4.5 still failed at player
scale. It does not defend the five-building layout. It shrinks the acceptance
target to three waterfront buildings, one authored street/stoop plane, one
player, and one camera frame.

G-4.7 responds to screenshot review that showed G-4.6 also failed. It stops
town work and switches to a four-variant visual calibration board for scale,
camera, sidewalk, stoop, curb, street, and building anchor grammar.

G-4.8 applies the G-4.7 recommendation as one actual proof street. It removes
the four-panel board, keeps the smaller player scale, and uses the Variant D
sidewalk/stoop/curb/narrow-lane grammar on four hand-seated waterfront
buildings.

G-4.9 responds to review that G-4.8 was still too much like an engineering
alignment strip. It reduces the vignette to three buildings, moves the player
closer to the storefronts, tightens the camera, narrows the road, and clusters
base detail so the first screen reads as a cozy playable harbor street.

G-4.9.1 responds to review that G-4.9 could not be judged because several
building sprites still showed neighboring atlas content at their edges. It
does not continue street tuning. It isolates the proof-street building sprites
into standalone PNGs and switches the catalog to those files first.

G-4.10 resets the work from three-building vignette polish into the first
starter harbor district buildout. The three accepted hero buildings remain as
style anchors, but the active scene now has a 16-lot district plan with
harborfront commercial, working wharf, inland civic/residential, and support
lane layers.

G-4.10A pauses town expansion for a building asset gate. The G-4.10 layout is
kept, but every currently visible building is now backed by an isolated padded
sprite and a reusable `BuildingCatalog.building_definition()` entry with
texture path, source region, draw scale, foot anchor, collision, interaction,
shadow, and district-role metadata.

G-4.11 expands the starter town asset kit without adding gameplay. It keeps
the harborfront street, wharf/service layer, inland civic/residential layer,
and expandable lot plan, then integrates additional Newport-compatible
buildings through the normalized building definition system. The
church-looking village hall is no longer the central civic anchor; it is
demoted as a deferred chapel/meeting-house asset, and the starter civic read is
now the custom house / harbor administration role.

G-4.12 uses that accepted building kit as a composition and dressing pass. It
does not add buildings or gameplay systems; it varies frontage placement,
tones down prototype lot rectangles, clarifies the commercial / dock / inland
district reads, adds role-specific prop clusters, and extends the wharf side
landings so the water-bottom warehouse, boathouse, and storehouse read as
reachable dock platforms beside the main wharf.

G-4.12B is a surface cohesion gate on top of that composition. It keeps the
same town and building kit, then improves roads, sidewalks, docks, water,
shoreline contact, yards, fences, laundry, role-based prop clusters, and muted
background depth so the non-building environment supports the quality of the
building art. It is still not navigation/collision validation and adds no
gameplay systems.

## Source Of Truth

The Godot town layout is authored in:

- `scripts/NewportTownBlueprint.gd`: map dimensions, road hierarchy, water,
  wharf/pier layout, districts, building placements, spawn, and QA targets.
- `scripts/BuildingCatalog.gd`: atlas or isolated sprite source, region,
  anchor, draw width, reusable building definitions, and the asset-kit audit.

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

G-4.1 through G-4.11 provide practical collision/navigation support only:

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
- G-4.8 is a one-street proof mode: it shows only `b_mercantile`,
  `b_counting_house`, `b_chandlery_front`, and `b_shop_house` on the chosen
  Variant D street grammar. Debug still toggles with `B` and remains off by
  default.
- G-4.9 is an art-direction vignette mode: it keeps only `b_mercantile`,
  `b_counting_house`, and `b_chandlery_front`, moves the spawn onto the
  storefront lane, and treats harbor/water as foreground context rather than
  a separating map band.
- G-4.10 is a starter district mode: it keeps the accepted hero buildings,
  adds compatible existing anchor buildings, draws planned future lots as
  muted foundations/silhouettes, and validates the main street -> dock ->
  inland lane -> main street loop before any NPCs or quests are added.
- G-4.10A keeps that district mode but requires every active building to use a
  normalized reusable definition. Debug overlays are hidden by default for
  review; press `B` to show building footprints, collision, interaction zones,
  and anchors for the starter-town buildings.
- G-4.11 expands the active starter kit to fourteen normalized buildings:
  harborfront commerce, wharf/service buildings, harbor administration,
  residences, a boarding house, and a temporary cooperage shed. Player movement
  still uses the same harborfront -> dock -> inland lane loop.

## G-4.10 Starter Harbor District

G-4.10 is the first pass after the vignette gate. It should not be reviewed as
another tiny polish task. The product target is the beginning of a believable
functional Newport-inspired starting village that can later support NPCs,
shops, quests, docks, and town traversal.

Implemented structure:

- Harborfront/commercial row: `b_inn_tavern`, `b_mercantile`,
  `b_counting_house`, `b_chandlery_front`, and `b_shop_house`.
- Dock/wharf layer: `b_market_shed`, `b_dock_storehouse`,
  `b_wharf_boathouse`, `b_dock_warehouse`, wharf apron, three pier fingers,
  dock clutter, rope, cargo, barrels, crates, nets, fish racks, rowboats, and
  post lines.
- Inland/background layer: `b_village_hall`, `b_res_small`, planned homes,
  civic-residence slot, support lane, fencing, clothesline, planting beds, and
  muted town-block massing.
- Planned future lots: `lot_west_fishmonger_future`,
  `lot_east_warehouse_future`, `lot_civic_residence_future`,
  `lot_lane_home_a_future`, and `lot_lane_home_b_future`.
- Movement loop: harborfront main street, storefront doors, wharf edge,
  west/central/east piers, dock access, inland cross lane, support lanes, and
  return to the main street.

The active layout data lives in `NewportTownBlueprint.gd`:

- `STARTER_HARBOR_BUILDING_IDS` lists the currently instantiated buildings.
- `STARTER_HARBOR_PLANNED_LOT_IDS` lists intentional future-lot markers.
- `starter_lot_specs()` maps actual/planned lots to districts and roles.
- `starter_district_plan()` records the district structure and loop intent.
- `missing_asset_manifest()` is the asset TODO list for G-4.11.

Missing asset manifest:

- small home variants
- warehouse
- chandlery/fishmonger
- dock shack
- civic/residence variant
- market stall
- carts
- crates
- barrels
- rope coils
- signs
- fencing

G-4.11 replaces three of those planned inland/support lots with matching
Newport building art. G-4.12 should now focus on composition and dressing:
street spacing, district dressing, prop clusters, signage, road/dock
transitions, and visual storytelling.

## G-4.10A Building Asset Gate

Root cause: G-4.10 correctly expanded the starter district, but several new
buildings were still rendered from loose atlas regions or crops that included
neighboring sprite pixels. They also used per-instance placement metadata
instead of a single reusable building definition that owned the foot anchor and
ground contact.

Implemented correction:

- Isolated padded PNGs now drive all active G-4.10A buildings.
- `BuildingCatalog.sprite_config()` records the texture path and full isolated
  sprite region for each active sprite.
- `BuildingCatalog.building_definition()` records the reusable building asset
  contract: building ID, display name, sprite source, visual scale, foot anchor,
  collision footprint, interaction zone, shadow/contact ellipse, district role,
  and harbor-integration flag where needed. G-4.13A also separates visual bounds
  and lot bounds from that collision footprint.
- `NewportTownBlueprint.building_specs()` places buildings by `definition_id`
  and layout position. The blueprint no longer has to hardcode each crop,
  anchor, collision, and interaction rectangle.
- The three water-bottom assets are dedicated wharf/water buildings:
  `b_dock_storehouse`, `b_wharf_boathouse`, and `b_dock_warehouse`.
- Planned lots now remain limited to future fishmonger/service, east
  warehouse/chandlery, civic residence, and support-lane homes.
- The validator fails if an active starter-town building lacks a definition,
  project building sprite source, normalized anchor, or valid crop/grounding
  behavior.

To add the next building safely:

1. Prefer an existing isolated sprite when available; otherwise register a
   verified atlas-pack region and inspect the crop/anchor in review.
2. If a source region includes neighbors or unsafe padding, add or adjust its
   isolated crop in `tools/extract_building_sprites.gd` and run the extractor.
3. Add the sprite source to `BuildingCatalog.sprite_config()`.
4. Add the reusable prefab-style entry to
   `BuildingCatalog.building_definition()`.
5. Place it in `NewportTownBlueprint.building_specs()` with `_catalog_building`
   and a matching `starter_lot_specs()` actual lot.
6. Run `tools/validate_vertical_slice.gd` before packaging.

This deliberately avoids recreating the JavaScript seating-contract audit.
Godot uses sprite anchors, collision shapes, and a route-oriented playability
validator instead.

## G-4.11 Town Asset Kit Expansion

Status: implemented as an asset-kit expansion pass only. No NPCs, quests,
combat, inventory, economy, save systems, interiors, or Worker route changes
were added.

Build label: Godot G-4.11 Town Asset Kit Expansion

Active starter mix:

- Harborfront/commercial row: `b_inn_tavern`, `b_mercantile`,
  `b_counting_house`, `b_chandlery_front`, `b_shop_house`, plus
  `b_market_shed` as market/fish-stall frontage.
- Dock/warehouse/service layer: `b_dock_storehouse`, `b_wharf_boathouse`, and
  `b_dock_warehouse`.
- Inland/civic/residential/support layer: `b_custom_house`, `b_res_small`,
  `b_large_residence`, `b_boarding_house`, and `b_cooperage_shed`.
- Planned placeholders remaining: `lot_west_fishmonger_future` and
  `lot_east_warehouse_future`.

Asset audit by role:

- Tavern / inn: `inn_tavern_v1` integrated.
- Mercantile / general goods: `mercantile_shop` and `newport_shopfront_awning`
  integrated; `newport_market_frontage_row` deferred as a duplicate frontage
  variant.
- Counting house / administrative office: `newport_counting_house_civic_exchange`
  integrated; `newport_formal_townhouse_block_a` is available but deferred for
  a later row-house or residential-block purpose.
- Chandlery / rope / sail shop: `newport_chandlery_outfitter_front`
  integrated; `newport_chandlery_cottage` deferred.
- Warehouse: `newport_dockside_storehouse_long` and
  `newport_dockside_storehouse` integrated.
- Dock shack / dock service: `newport_wharf_boathouse_large` integrated;
  `service_dependency_shed` integrated as a temporary cooperage/service shed.
- Fishmonger: `newport_market_shed_stalls` integrated as a market/fish-stall
  stand-in; a dedicated fishmonger storefront is still missing.
- Cooperage / barrel shop: `service_dependency_shed` stands in for now; final
  cooperage art is still needed.
- Blacksmith / smithy: no suitable Newport-starting-town asset found.
- Small residence: `residence_small` and `newport_modest_clapboard_residence_a`
  integrated.
- Large residence / boarding house: `newport_large_front_residence`
  integrated; `residence_large`, `newport_georgian_merchant_residence_a`,
  `newport_elite_garden_mansion_a`, and `newport_elite_mansion_white` deferred
  because they are either redundant or too grand for this starter pass.
- Civic / customs / harbor master building: `newport_custom_house_civic_front`
  integrated as `b_custom_house` using the dedicated left-side custom-house
  building from Newport pack B. It is intentionally classified as a customs /
  harbor administration building, not a church.
- Church / chapel: `village_hall_meeting_house` is present but demoted to
  `Meeting House Chapel`; it is not active as the starter town civic anchor.

Church-looking hall decision:

- Replaced in the active starter layout. `b_village_hall` no longer appears in
  `STARTER_HARBOR_BUILDING_IDS`, `building_specs()`, or actual starter lots.
- The active central civic role is now `b_custom_house`, intentionally reading
  as customs / harbor administration using the dedicated custom-house asset.
- The old hall remains cataloged only as a deferred chapel/meeting-house asset
  so future roadmap decisions can use it deliberately instead of accidentally.

Definition-system update:

- Every active G-4.11 building is placed with `_catalog_building()` and a
  `definition_id`.
- `BuildingCatalog.building_definition()` now records `building_id`,
  `display_name`, `role`, `texture_path`, `visual_scale`, `foot_anchor`,
  `visual_bounds`, `lot_bounds`, `collision_footprint`, `collision_shape`,
  `collision_rect`, `interaction_zone`, `interaction_zone_placeholder`,
  `interaction_size`, `interaction_offset`, `district_placement_tags`, and
  `notes`.
- New G-4.11 definitions: `b_custom_house`, `b_large_residence`,
  `b_boarding_house`, and `b_cooperage_shed`.
- G-4.11 review cleanup isolates the custom house, large residence, boarding
  house, and cooperage shed into transparent per-building sprites so neighboring
  sheet pixels do not bleed into the active town.
- Existing definitions remain normalized for the harborfront and wharf assets.

Props and dressing:

- Existing G-4.10 harbor identity props remain: barrels, crates, rope coils,
  signs, fences, dock posts, cargo piles, market tables, fish racks, nets,
  rowboats, lanterns, wharf planks, and waterline clutter.
- G-4.11 adds more support-lane and inland/civic prop dressing around the
  custom house, residence, boarding house, and cooperage shed.
- The three water-base wharf buildings are positioned in the blue water pockets
  immediately below the main wharf edge and laterally beside the pier fingers,
  with the background dock fingers shortened into narrow gangways and side
  landings so players can read a path from the wharf onto each building's own
  dock instead of seeing the building art pasted on top of broad brown dock
  slabs or floating out of reach.

Still missing for the starter village:

- Dedicated fishmonger storefront.
- Final cooperage / barrel-shop art.
- Blacksmith or smithy art, if that role belongs in the starter town.
- More small-home variants that are not obvious repeats.
- Dedicated prop sprites for carts, crates, barrels, rope coils, sign variants,
  fencing variants, and lantern variants.
- A deliberate chapel/church roadmap decision if that building should exist in
  Newport at all.

## G-4.12 Starter Town Composition + Dressing

Status: implemented as a composition and dressing pass only. No NPCs, quests,
combat, inventory, economy, save systems, interiors, or Worker route changes
were added.

Build label: Godot G-4.12 Starter Town Composition + Dressing

Composition changes:

- The G-4.11 building kit remains active, but harborfront buildings now have
  slight frontage-depth variation instead of a perfectly even asset row.
- The custom house, residences, boarding house, and cooperage keep the inland /
  support structure while reading more like civic lots, yards, and work lanes.
- Wharf building positions remain in the blue water pockets beside the main
  wharf, with extended narrow side landings from the pier fingers to make a
  practical walk path onto each building's own dock platform.
- Planned future lots remain, but their rendering is muted into low planned
  yards / silhouettes rather than high-contrast debug rectangles.

District identity:

- Harborfront commercial street: tavern, mercantile, counting house, chandlery,
  shop house, and market shed are dressed as a working shopfront street with
  signs, thresholds, crates, barrels, market tables, rope, and lamps.
- Dock / wharf layer: the wharf apron, pier fingers, side landings, cargo,
  rope, nets, fish racks, rowboats, and waterline clutter now tell a clearer
  goods-movement story between water, storage, market, and street.
- Inland civic / residential / support layer: the custom house has a cleaner
  frontage, residences and boarding house have fences, clotheslines, shrubs,
  benches, and yard texture, and the cooperage is dressed with barrels and
  wood clutter.

Technical notes:

- All active buildings still use `_catalog_building()` and reusable
  `BuildingCatalog.building_definition()` entries.
- Debug overlays remain off by default for clean visual review. Press `B` for
  building seating overlays or `F3` for full building debug overlays.
- The G-4.12 validator expected the G-4.12 label, clean review default, the
  G-4.12 district plan marker, and higher lived-in detail density. Later gates
  advance the build label while preserving this clean review contract.

Still remaining before NPC / quest work:

- G-4.13B should use the corrected footprints for townhouse/rowhouse density
  without closing the rear road, cross-lanes, or dock approaches.
- G-4.13C should integrate the prop atlas and role-based dressing.
- G-4.13D should perform final navigation/collision/interaction-zone
  validation across town entry, harborfront, dock side landings, and inland
  civic/support areas.
- Dedicated fishmonger storefront, final cooperage art, blacksmith/smithy if
  needed, more small-home variants, carts, and dedicated prop sprites remain
  useful asset needs.

## G-4.12B Surface Cohesion Gate

Status: implemented as a clean visual review gate. It does not add buildings,
NPCs, quests, combat, inventory, economy, interiors, save systems, or Worker
route changes.

Build label: Godot G-4.12B Surface Cohesion Gate

Clean review mode:

- Default review presentation has building debug overlays hidden.
- Press `B` to toggle the building seating overlay.
- Press `F3` to toggle the full building debug overlay.
- Press `F2` to toggle review metadata on the HUD.

Surface and environment changes:

- Roads and sidewalks gained worn patches, edge grime, seam lines, dirt
  variation, and less rigid material breaks while preserving route readability.
- Docks and wharf surfaces gained plank weathering, darker edge shadows,
  stronger pilings/post language, side-landing contact, and cargo/waterline
  support.
- Water gained depth bands, extra ripples, dock/building contact scum, and
  clearer separation between deep water, shoreline, and wharf edges.
- Residential/civic yards gained paths, shrubs, low walls, softened fences,
  clotheslines, benches, and domestic clutter so they read as lived-in lots.
- Background blocks were restyled with faded distant structures, low walls,
  tree/shrub depth, and muted silhouettes instead of prominent layout blocks.
- Role-based prop clusters now better distinguish tavern/social frontage,
  mercantile goods, civic/custom-house order, chandlery rope/cargo, market
  tables, cooperage hoops/wood/barrels, domestic yards, and dockside freight.

Known weak spots before G-4.13A:

- Roads, water, and props are still drawn primitives rather than dedicated
  painterly sprite assets, so final art can still raise cohesion further.
- Dedicated cart, sack, crate, barrel, rope, fence, lantern, and sign sprites
  would improve the town once available.
- Building collision must be separated from the tall front-facing sprite
  rectangles before prop-atlas integration or final navigation validation.

## G-4.13A Building Footprint Walkability Gate

Status: implemented as the footprint/collision correction pass after the
G-4.12B surface gate. It does not add NPCs, quests, combat, inventory,
economy, interiors, rowhouses, prop-atlas integration, town expansion, or
Worker route changes.

Build label: Godot G-4.13A Building Footprint Walkability Gate

Issue found:

- The debug overlay showed red blocking rectangles that effectively matched
  tall painted building bounds on several front-facing sprites.
- Those rectangles overlapped the commercial rear road, especially behind
  `b_mercantile` and `b_counting_house`, so visually open lanes could feel
  blocked by invisible building height.

Collision model after G-4.13A:

- `visual_bounds`: full rendered sprite rectangle for art/crop review only.
- `lot_bounds`: planning/composition rectangle for lots and future density.
- `collision_footprint`: the only blocking body; a shallow base/foundation
  footprint near the ground contact.
- `interaction_zone`: the frontage standing rectangle aligned to doors.
- `foot_anchor`: local ground contact at the node origin.
- `y_sort_offset`: remains `Vector2.ZERO`; buildings sort from their foot
  anchor/frontage plane.

Adjusted active building footprints:

| Building id | Footprint treatment |
| --- | --- |
| `b_inn_tavern` | shallow tavern foundation strip, not the roof/body art |
| `b_mercantile` | tight shop base so the rear road stays walkable |
| `b_counting_house` | tight civic-shop base so the rear road stays walkable |
| `b_chandlery_front` | storefront base only; side-lane props remain separate blockers |
| `b_shop_house` | storefront base only |
| `b_market_shed` | wider low shed base, still separate from sprite height |
| `b_custom_house` | civic base/foundation only |
| `b_large_residence` | house base/foundation only |
| `b_boarding_house` | narrow house base/foundation only |
| `b_res_small` | cottage base/foundation only |
| `b_cooperage_shed` | compact shed base/foundation only |
| `b_dock_warehouse` | dockside warehouse ground-contact footprint |
| `b_wharf_boathouse` | boathouse ground-contact footprint |
| `b_dock_storehouse` | storehouse ground-contact footprint |

Validated routes in this gate:

- road behind `b_mercantile`
- road behind `b_counting_house`
- harborfront commercial rear road generally
- west, central, and east cross-lanes
- inland road to commercial street access
- commercial street frontage and dock-layer walk

Debug overlay meaning:

- Yellow outline: `visual_bounds`
- Amber outline/fill: `lot_bounds`
- Red fill/outline: `collision_footprint`, the actual blocker
- Blue fill/outline: `interaction_zone`
- Green/cyan/magenta markers: foot anchor, frontage, door, and y-sort points

Planned G-4.13B rowhouse/townhouse infill slots:

- `slot_tavern_mercantile_narrow_rowhouse`
- `slot_counting_chandlery_lane_edge_shop`
- `slot_shop_market_townhouse_pair`
- `slot_cottage_customs_inland_townhouse`
- `slot_support_lane_boarding_gap`

Remaining known issues:

- Roads, water, and props still need final painterly asset support.
- Infill slots are planning metadata only; no rowhouse sprites are active yet.
- G-4.13D still needs final manual navigation/collision/interaction-zone
  validation after rowhouse density and prop-atlas dressing.

## G-4.13A.1 Walkability Blocker Hotfix

Status: implemented as the remaining G-4.13A acceptance hotfix. It does not add
rowhouses, prop-atlas assets, NPCs, quests, combat, inventory, economy,
interiors, town expansion, or Worker route changes.

Build label: Godot G-4.13A.1 Walkability Blocker Hotfix

Issue found:

- The black-box marked rear-lane location near the tavern, mercantile, and
  `b_res_small` area still blocked the player even though it looked like open
  road/lane space.
- Runtime collision-owner probing found the exact owners:
  `DetailBlocker_mercantile_front_crates`, `DetailBlocker_west_alley_rope`, and
  grown player-body contact with `Building_b_mercantile`.
- The detail blockers were not building bounds; they were prop/scenery
  collision rectangles sitting too high in the lane. The mercantile base was
  also wide enough that the player radius pinched the lane edge.

Fix:

- `b_mercantile` keeps a real base/foundation `collision_footprint`, but it is
  slightly narrower and shallower than the G-4.13A version.
- `mercantile_front_crates` and `west_alley_rope` were moved down to visible
  frontage clutter so they no longer occupy the rear-lane throat.
- The collision/navigation debug overlay labels detail-blocker owners and adds
  debug-only route probes. Clean review mode leaves these hidden.
- The validator now checks route samples against building, prop/detail, water,
  and map collision owners rather than only building footprints.

Routes revalidated:

- black-box marked rear lane north/west of `b_mercantile`
- road behind `b_mercantile`
- road behind `b_counting_house`
- lane near `b_res_small`
- tavern/mercantile rear-lane throat
- inland road to commercial row access
- commercial row to dock-layer access
- central/east rear roads, commercial street, and dock boardwalk

Files changed for the hotfix:

- `scripts/BuildInfo.gd`
- `scripts/BuildingCatalog.gd`
- `scripts/NewportTownBlueprint.gd`
- `scenes/Main.gd`
- `scenes/map/CollisionNavigationLayer.gd`
- `tools/validate_vertical_slice.gd`
- `docs/NEWPORT_TOWN_GODOT.md`
- `docs/WAYFARER_GODOT_ROADMAP.md`

Remaining known issues:

- G-4.13B now owns rowhouse/townhouse infill activation.
- Prop atlas integration is still deferred to G-4.13C.
- G-4.13D remains the final whole-town manual navigation/collision validation
  pass.

## G-4.13B Townhouse / Rowhouse Infill + Density Pass

Status: implemented for local validation. It does not add NPCs, quests, combat,
inventory, economy, interiors, town expansion, prop atlas integration, or Worker
route changes.

Build label: Godot G-4.13B Rowhouse Infill Density

Asset audit:

- `newport_narrow_merchant_townhouse_a`: activated as a narrow
  shop-house/rowhouse for `b_printer_rowhouse`, now seated on the east market
  street edge after the shop-house gap proved too tight.
- `newport_narrow_clapboard_townhouse_b`: activated as the
  `b_clerk_townhouse` asset between the tavern and mercantile, preserving a
  complete narrow-building read instead of shrinking the full three-bay formal
  block or slicing one bay out of it.
- `newport_formal_townhouse_block_a`: retained as available deferred art for a
  larger formal residential row.
- `newport_formal_townhouse_single_bay`: rejected after QA because the crop
  reads like a cut facade column rather than a whole townhouse.
- `newport_waterfront_shop_house`: activated as the four-unit clapboard
  `b_dockworker_rowhouse`, replacing the duplicate boarding-house sprite.
- Deferred candidates: `newport_chandlery_cottage` and
  `newport_market_frontage_row`.

Infill slots used:

- `slot_tavern_mercantile_narrow_rowhouse`: active with `b_clerk_townhouse`
  as a complete narrow clapboard townhouse, keeping visible daylight from both
  neighbors without miniaturizing the three-bay source block or showing a
  sliced facade bay.
- `slot_support_lane_boarding_gap`: active with `b_dockworker_rowhouse`,
  seated as a four-unit lane-front rowhouse beside the boarding-house block
  while keeping the east support-lane return readable.
- `slot_market_east_edge_narrow_shop`: active with `b_printer_rowhouse`,
  seated on the east market street edge while keeping market approach and dock
  access walkable.

Infill slots deferred:

- `slot_counting_chandlery_lane_edge_shop`: deferred because this gap protects
  the rear road and central cross-lane sightline.
- `slot_shop_market_townhouse_pair`: deferred because visual review showed the
  shop-house frontage/bounds make that gap too tight for readable placement.
- `slot_cottage_customs_inland_townhouse`: deferred because the earlier
  townhouse read as an isolated yard object, not a purposeful village street
  edge.

New building definitions:

- `b_printer_rowhouse`: role `printer_rowhouse`, future hooks for a
  revolutionary pamphlet, apprentice errand, rented-room rumor, or suspicious
  print job.
- `b_clerk_townhouse`: role `clerk_lodging`, future hooks for customs lodging,
  family dispute, suspicious neighbor, or quiet artifact discovery.
- `b_dockworker_rowhouse`: role `dockworker_lodging`, future hooks for a
  missing person, wharf job, or neighbor rumor.

Collision/footprint model:

- Each active infill building uses the G-4.13A split metadata:
  `visual_bounds`, `lot_bounds`, `collision_footprint`, `interaction_zone`,
  `foot_anchor`, district tags, and y-sort/debug data.
- The visual sprite rectangles are review/art bounds only. New blocking
  collision is a shallow ground-contact footprint near the building base.
- Interaction zones remain south/frontage-aligned.

G-4.13B.4 clerk townhouse complete asset fix:

- Build label: Godot G-4.13B.4 Clerk Townhouse Complete Asset Fix.
- Replaces the rejected single-bay crop with a complete narrow clapboard
  townhouse from the same Newport source pack.
- Adds validation guards that reject both squat miniature-block reads and
  over-narrow sliced-column reads for the clerk townhouse.

Routes revalidated:

- road behind `b_mercantile`
- road behind `b_counting_house`
- tavern / mercantile / `b_res_small` rear-lane throat
- central and east rear roads
- inland civic road and cross-lane
- commercial street
- commercial row to dock-layer access
- wharf boardwalk and dock layer
- new route probes below the tavern/mercantile clerk rowhouse, east market-edge
  printer rowhouse, and dockworker infill buildings

Files changed for the pass:

- `scripts/BuildInfo.gd`
- `scripts/BuildingCatalog.gd`
- `scripts/NewportTownBlueprint.gd`
- `tools/validate_vertical_slice.gd`
- `docs/NEWPORT_TOWN_GODOT.md`
- `docs/WAYFARER_GODOT_ROADMAP.md`

Remaining known issues:

- Prop atlas integration and role-based dressing remain deferred to G-4.13C.
- G-4.13D remains the final whole-town navigation/collision/interaction-zone
  validation pass.
- Some currently deferred narrow-building candidates may need isolated crops or
  a later placement pass before use.

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

## G-4.8 Variant D Proof Street

G-4.8 converts the G-4.7 recommendation into a playable street vignette. It is
not a town expansion and does not revive the calibration board.

Active proof buildings:

1. `b_mercantile`
2. `b_counting_house`
3. `b_chandlery_front`
4. `b_shop_house`

Street grammar:

- player visual scale is `0.78`
- sidewalk/apron sits directly under building bases
- stoop pads align with each authored door/frontage
- a dark curb/gutter separates sidewalk from the narrower cobbled street lane
- the wharf plank edge and harbor water sit below the street instead of
  reading as a detached map band
- small crates, barrels, rope, lamps, signs, and dock posts establish base
  rhythm without adding more buildings

Each proof building keeps hand-authored seating metadata: visual base anchor,
frontage offset, collision rectangle, y-sort anchor, shadow/base area, and
draw width. This remains necessary; one generic seating value is still not
trusted for painterly building sprites.

The expected visible review identity is:

```text
Build label: Godot G-4.8 Variant D Proof Street
Phase: G-4.8 | Review host: itch
Channel: manual ZIP
Branch: codex/g-4-8-variant-d-proof-street
```

Manual itch review must decide whether this looks materially better than the
G-4.6 failure and the G-4.7 board. If it still looks like pasted sprites on a
slab, do not scale this grammar to Newport.

## G-4.9 Newport Street Vignette

G-4.9 keeps the Variant D direction but stops presenting it as a technical
strip. It is one composed, playable street vignette for manual itch review.

Active vignette buildings:

1. `b_mercantile`
2. `b_counting_house`
3. `b_chandlery_front`

Art-direction changes:

- player visual scale remains `0.78`
- player spawn moves closer to storefronts at `(675, 612)`
- camera zoom tightens so the first screenshot frames the street, not a board
- building spacing is clustered with small uneven setbacks
- sidewalk/apron, stoops, curb, and narrow cobbled lane replace the broad
  proof-strip feeling
- foreground wharf planks and water give harbor context without separating the
  player from the buildings
- crates, barrels, signs, lamps, rope, weeds, nets, table goods, and dock
  posts are clustered at building bases and street edges

The expected visible review identity is:

```text
Build label: Godot G-4.9 Street Vignette
Phase: G-4.9 | Review host: itch
Channel: manual ZIP
Branch: codex/g-4-9-newport-street-vignette-art-direction
```

Manual itch review must decide whether this finally feels like a cozy harbor
street. If it still reads as a calibration strip, do not scale it back to the
full Newport town.

## G-4.9.1 Sprite Crop Isolation

G-4.9.1 fixes the source-image blocker before further street composition. The
proof-street buildings had been using atlas rectangles that included or exposed
neighboring sprite fragments. The browser scene now uses isolated PNGs with
transparent padding:

| Building id | Sprite id | Isolated output |
| --- | --- | --- |
| `b_mercantile` | `mercantile_shop` | `assets/sprites/buildings/isolated/mercantile_shop_isolated.png` |
| `b_counting_house` | `newport_counting_house_civic_exchange` | `assets/sprites/buildings/isolated/newport_counting_house_civic_exchange_isolated.png` |
| `b_chandlery_front` | `newport_chandlery_outfitter_front` | `assets/sprites/buildings/isolated/newport_chandlery_outfitter_front_isolated.png` |
| `b_shop_house` | `newport_shopfront_awning` | `assets/sprites/buildings/isolated/newport_shopfront_awning_isolated.png` |

The expected visible review identity is:

```text
Build label: Godot G-4.9.1 Sprite Crop Isolation
Phase: G-4.9.1 | Review host: itch
Channel: manual ZIP
Branch: codex/g-4-9-1-building-sprite-crop-isolation
```

Acceptance is intentionally narrow: no proof-street building may show pieces
of a neighboring atlas building. If any contamination remains after upload,
classify the pass as `SPRITE_CROP_CONTAMINATION_REMAINS`.

The proof street also began treating each building as an occupied lot rather
than a flat facade. That early `lot_rect`/`collision_rect` coupling was later
corrected in G-4.13A: `lot_bounds` remains planning/debug context, while the
blocking `collision_footprint` is a tight ground-contact base.

## G-4.9.5 and G-4.9.6 Street Review Stack

G-4.9.5 preserves the accepted crop/seating work and changes only the street
frontage spacing: horizontal building positions, intentional alleys/setbacks,
and nearby prop stitching. It does not change building extraction, vertical
grounding, camera logic, gameplay systems, interiors, or map scope.

G-4.9.6 is the clean review gate for that vignette. The expected visible
review identity is:

```text
Build label: Godot G-4.9.6 Street Vignette Acceptance Gate
Phase: G-4.9.6 | Review host: itch
Channel: manual ZIP
Branch: codex/g-4-9-6-street-vignette-acceptance-gate
```

Normal review mode must show a player-facing scene: no red/yellow/blue
debug rectangles, no anchor markers, and no building IDs. The seating overlay
remains available with `B` for inspection, but must be off before screenshots
used for acceptance.

After G-4.9.6, G-4.9.7 provided the final street-vignette polish gate. G-4.10
then resets the work from vignette polish into the starter harbor town
buildout described above.

## G-4.9.7 Street Vignette Polish Gate

G-4.9.7 keeps the accepted G-4.9.4/G-4.9.6 building crops, anchors,
vertical seating, camera, and debug-default behavior. It only polishes the
current street vignette:

```text
Build label: Godot G-4.9.7 Street Vignette Polish Gate
Phase: G-4.9.7 | Review host: itch
Channel: manual ZIP
Branch: codex/g-4-9-7-street-vignette-polish-gate
```

The pass tightens the three-building horizontal rhythm, dresses the remaining
gaps as loading/setback space with existing props, strengthens sidewalk/curb/
road/harbor-walk/water separation, adds subtle contact shadows to street and
dock details, and restyles the rear lot blocks as muted background silhouettes.
It does not add new buildings, interiors, quests, combat, inventory, save
systems, production cutover, or a larger map.

## Deferred

- Final art parity with JavaScript Phase 35.13R.
- Quests, combat, inventory, save migration, and production cutover.
- Butler automation and Cloudflare Pages deployment.
- New source art for exact per-building replacements.

Manual review still requires uploading
`wayfarer_godot_vertical_slice/artifacts/wayfarers-tale-godot-web.zip` to itch.
