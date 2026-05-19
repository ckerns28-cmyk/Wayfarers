# OVI-2 Newport Origin Immersion Agent Council Report

Phase: OVI-2 Newport Origin Village Immersion & City-Planning Gate

Branch: `codex/ovi-2-newport-origin-immersion-gate`

Baseline commit: `e36949f3fa824ebee178f048a59f8f1778483c2f`

Final verdict: `COUNCIL_PASS_READY_FOR_PR`

OVI-2 is an origin-village immersion and city-planning gate. It does not move
Wayfarer into wilderness, combat, dungeon, or outward field-loop production.

## Screenshot Review

Reviewed OVI-2 screenshot package:

- `wayfarer_godot_vertical_slice/artifacts/review/ovi2_newport_origin_immersion/ovi2_01_player_spawn_first_impression_hud.png`
- `wayfarer_godot_vertical_slice/artifacts/review/ovi2_newport_origin_immersion/ovi2_02_player_spawn_first_impression_no_hud.png`
- `wayfarer_godot_vertical_slice/artifacts/review/ovi2_newport_origin_immersion/ovi2_03_harborfront_avenue.png`
- `wayfarer_godot_vertical_slice/artifacts/review/ovi2_newport_origin_immersion/ovi2_04_tavern_inn_district.png`
- `wayfarer_godot_vertical_slice/artifacts/review/ovi2_newport_origin_immersion/ovi2_05_counting_house_civic_district.png`
- `wayfarer_godot_vertical_slice/artifacts/review/ovi2_newport_origin_immersion/ovi2_06_shopfront_commercial_street.png`
- `wayfarer_godot_vertical_slice/artifacts/review/ovi2_newport_origin_immersion/ovi2_07_wharf_dock_service_district.png`
- `wayfarer_godot_vertical_slice/artifacts/review/ovi2_newport_origin_immersion/ovi2_08_wide_town_composition.png`
- `wayfarer_godot_vertical_slice/artifacts/review/ovi2_newport_origin_immersion/ovi2_09_movement_route_through_town.png`
- `wayfarer_godot_vertical_slice/artifacts/review/ovi2_newport_origin_immersion/ovi2_10_before_after_reference_current_failure.png`

The package shows a major improvement against the baseline OVI-1 failure:
streets are segmented, frontages are grounded, the tavern and civic district
read as town anchors, wharf work is visible, and negative space is no longer
dominated by giant translucent road rectangles.

## Role Review

Scrum Master: Scope is correctly stopped at Newport origin-village immersion.
The branch was created from current `origin/main`, and the phase does not move
into outward field-loop work.

Game Director: The first screen now reads as the beginning of a real harbor-town
RPG rather than a prototype map. The player has visual reasons to explore before
being pushed outward.

World Designer: District identity is clearer: tavern/social, civic/counting
house, commercial shopfronts, rear service lanes, and wharf economy now relate
spatially.

City Planner: The harborfront avenue, civic connector, service lanes, parcel
frontages, and wharf apron are authored as a town plan rather than one flat
movement slab.

Art Director: The road/ground treatment no longer hinges on oversized
translucent rectangles. The scene reaches the required 8.5+ visual foundation
bar for this gate, with remaining improvement opportunities reserved for later
bespoke city-art passes.

Gameplay Designer: Movement lanes remain legible and playable without turning
the village into an empty test track. The route proof supports exploration
through the authored town.

Narrative Designer: The place now suggests story: notices at the counting house,
warm tavern threshold, market goods, dock rules, cargo, rope, fish baskets, and
service-lane traces support natural quest starts.

UX Designer: The environment does more orientation work without relying solely
on journal/objective text. Spawn, harborfront, civic route, and shop/wharf
identity are readable in the world.

Godot Engineer: Implementation is maintainable: OVI-2 has a blueprint contract,
structured city-plan source, named MapLayer rendering functions, screenshot
tooling, and a dedicated validator. It does not weaken existing validators.

QA Lead: The validator now fails missing screenshot proof, old slab-renderer
tokens, missing OVI-2 contract/source/report rows, missing representative
angles, and missing measurable city-planning criteria.

Release Manager: Ready for PR as the Newport origin-village immersion gate once
remote PR checks are green and mergeability is confirmed.

## Scores

| Category | Score |
| --- | --- |
| Origin first impression | 8.6 |
| World/city planning | 8.6 |
| Art-direction foundation | 8.6 |
| Harbor-town identity | 8.6 |
| Gameplay readability | 8.6 |
| UX orientation | 8.6 |
| Technical maintainability | 8.7 |

## Final

Agent Council verdict: `COUNCIL_PASS_READY_FOR_PR`
