# Newport Town Godot Foundation

G-4.1 replaces the reduced Newport Harbor Test scene with a player-facing
Newport-inspired starting port town in Godot. The JavaScript Worker remains the
separate Phase 35.13R production/reference route.

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

G-4.1 provides practical collision/navigation support only:

- Building bodies block the player at the visual base/foot line.
- Water collision is generated from blueprint water tiles while leaving wharf
  street and pier tiles walkable.
- The player spawns on the waterfront route and can reach the civic square,
  wharf/pier frontage, upper residential road, and service lane.

This deliberately avoids recreating the JavaScript seating-contract audit.
Godot uses sprite anchors, collision shapes, and a route-oriented playability
validator instead.

## Deferred

- Final art parity with JavaScript Phase 35.13R.
- Quests, combat, inventory, save migration, and production cutover.
- Butler automation and Cloudflare Pages deployment.
- New source art for exact per-building replacements.

Manual review still requires uploading
`wayfarer_godot_vertical_slice/artifacts/wayfarers-tale-godot-web.zip` to itch.
