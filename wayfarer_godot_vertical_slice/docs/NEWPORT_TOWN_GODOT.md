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

G-4.1 and G-4.2 provide practical collision/navigation support only:

- Building bodies block the player at the visual base/foot line.
- Water collision is generated from blueprint water tiles while leaving wharf
  street and pier tiles walkable.
- The player spawns on the waterfront route and can reach the civic square,
  wharf/pier frontage, upper residential road, and service lane.
- G-4.2 adds small detail blockers for crates, tables, benches, and dockside
  clutter so streets feel shaped without trapping the player.

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

## Deferred

- Final art parity with JavaScript Phase 35.13R.
- Quests, combat, inventory, save migration, and production cutover.
- Butler automation and Cloudflare Pages deployment.
- New source art for exact per-building replacements.

Manual review still requires uploading
`wayfarer_godot_vertical_slice/artifacts/wayfarers-tale-godot-web.zip` to itch.
