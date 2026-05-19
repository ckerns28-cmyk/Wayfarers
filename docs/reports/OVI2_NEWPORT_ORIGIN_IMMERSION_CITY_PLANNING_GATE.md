# OVI-2 Newport Origin Village Immersion & City-Planning Gate

Purpose: repair Newport as Wayfarer's origin village / harbor town before any
outward field-loop, combat, wilderness, dungeon, or larger quest expansion.

Baseline commit: `e36949f3fa824ebee178f048a59f8f1778483c2f`

Branch: `codex/ovi-2-newport-origin-immersion-gate`

This phase exists because the human screenshot review overruled the previous
technical-green interpretation. OVI-2 is about origin-village immersion and
not outward gameplay expansion.

## Human Screenshot Failure Summary

The OVI-1/G-19R validating Newport screenshot still read as an artificial test
map: giant translucent road/region slabs, isolated building sprites, weak street
hierarchy, little parcel frontage, empty flat negative space, and a first screen
that did not feel like a real origin harbor town.

The baseline reference used for practical before/after review is:
`wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/01_village_wide_cohesion.png`

## Forensic Diagnosis

The artificial read came from source rendering, not from a missing debug toggle.
The large rectangles were not debug overlays; they were intentional runtime road
and ground surfaces.

Primary causes:

- `MapLayer._draw_g19s_source_truth_street_plan()` drew the measured G-19R
  navigation corridors with very large `_draw_newport_commercial_street(Rect2(...))`
  calls.
- The legacy G-7A ground foundation added broad rectangular terrace washes under
  the town.
- The G-19S props branch returned before later district-density passes could make
  frontages, thresholds, service lanes, and wharf work areas carry the scene.
- Building anchors were source-driven, but the visual surface language did not
  make those anchors read as parcels, streets, blocks, civic spaces, and working
  harbor edges.

## Town-Planning Design Rules

- Keep the G-19R/G-19S measured walkable layout and NPC station rules.
- Replace slab roads with segmented harborfront avenue pieces, edges, wear,
  curbs, and material transitions.
- Give the tavern/inn an integrated frontage, warm entry, service edge, and rear
  lane relationship.
- Tie the counting house/civic district to the main avenue with a visible civic
  terrace and first-objective public notice language.
- Align commercial shops, signs, awnings, carts, and goods to street frontage.
- Make the wharf read as a working harbor economy with cargo, rope, bollards,
  dock rules, fish baskets, net drying, lanterns, and plank/cobble transitions.
- Use props to explain function and story; do not scatter filler into open space.
- Preserve movement lanes, NPC route correctness, the roof-station repair, and
  y-sort/occlusion behavior.

## Implementation Changes

- Added `ovi2_newport_origin_immersion_contract()` to
  `wayfarer_godot_vertical_slice/scripts/NewportTownBlueprint.gd` and exposed it
  through `wayfarer_godot_vertical_slice/scenes/Main.gd`.
- Added the structured city-plan source:
  `wayfarer_godot_vertical_slice/data/world_layout/ovi2_newport_origin_immersion_city_plan_v1.json`.
- Rebuilt the G-19S visual street path in
  `wayfarer_godot_vertical_slice/scenes/map/MapLayer.gd` so the active renderer
  uses OVI-2 segmented lots, avenue segments, civic terrace, rear service lanes,
  wharf aprons, curbs, and district props.
- Removed the broad G-7A rectangular ground washes that contributed to the flat
  slab-plane read.
- Added OVI-2 screenshot tooling and a validator:
  `wayfarer_godot_vertical_slice/tools/capture_ovi2_runtime_screenshots.gd`,
  `wayfarer_godot_vertical_slice/tools/capture_ovi2_runtime_screenshots.ps1`,
  and `wayfarer_godot_vertical_slice/tools/validate_ovi2_newport_origin_immersion.py`.
- Updated the OVI roadmap and ledger so OVI-2 is explicitly Newport origin
  immersion/city-planning work, not a field gameplay loop.

## Spatial Relationship Summary

- Tavern/Inn: west social anchor on the harborfront avenue, with lanterns,
  threshold planters, brick stoop, service goods, and rear-lane context.
- Counting House / Civic: official first-objective anchor tied to a civic terrace,
  notice board, flags, posting pole, harbor bulletin board, and road plan.
- Shops / Market: commercial frontage uses signs, awnings, lamps, goods, carts,
  and directional signposting without blocking the movement lane.
- Wharf / Dock / Service: harbor work aprons connect to dock planks and waterline
  identity through cargo, rope, bollards, fish baskets, dock rules, and lanterns.
- Roads / Lanes: the main avenue, civic connector, rear service lanes, and wharf
  apron are segmented surfaces with edges and wear, not one flat rectangle.
- NPCs: existing grounded/stationed NPC policy remains intact; no NPC is moved
  onto roofs or building bodies.

## Screenshot Artifact Paths

- `wayfarer_godot_vertical_slice/artifacts/review/ovi2_newport_origin_immersion/ovi2_newport_origin_immersion_screenshot_manifest.json`
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

## Validation Table

| Validation | Result |
| --- | --- |
| OVI-2 immersion/city-planning validator | PASS |
| OVI-1 gate validator | PASS |
| First-session gameplay loop validator | PASS |
| Newport reconstruction validator | PASS |
| G-22 player motion proof validator | PASS |
| NPC route validator | PASS |
| Roadmap validation | PASS |
| Ledger validation | PASS |
| Starter-village layout source usage validation | PASS |
| Newport visual ordering validation | PASS |
| Godot vertical slice validation | PASS |
| Screenshot capture tooling | PASS |
| git diff --check | PASS |
| Agent Council report | PASS |

## Known Limitations

Automated validation now catches the obvious slab-plane, missing screenshot, and
frontage/identity proof failures, but it still cannot fully judge beauty,
player desire to explore, or every art-direction taste call. Agent Council
screenshot inspection remains part of the gate.

## Remaining Art-Direction Risks

The pass materially improves the first-screen and district read, but Newport
can still gain more bespoke building silhouettes, crowd rhythm, animated harbor
details, and custom micro-vignettes in later city-focused phases.

## Agent Council Verdict

Final verdict: `COUNCIL_PASS_READY_FOR_PR`
