# G-16 Island Landmark and Point-of-Interest Pass

Phase ID: G-16

Branch: `codex/g-16-island-poi-landmarks`

Commit: `pending_branch_commit_before_pr`

PR number: `pending_open_pr`

Merge status: `pending`

Status: PASS

Human review required: no

Agent Council verdict: `COUNCIL_PASS_READY_FOR_PR`

Next phase: G-16A Island Atelier Asset Family Pass

## Purpose

Give the opening island memorable, quest-relevant destinations instead of leaving it as merely connected terrain. This phase keeps the Newport origin pointed at the North Star: authored pre-Revolutionary harbor-world mystery, readable exploration, atelier-standard craft, and the kind of first-session place memory expected from inspiration games like Tibia and Ragnarok Online.

## Implementation

- Added `wayfarer_godot_vertical_slice/data/world_layout/island_poi_landmarks_v1.json` as the G-16 landmark/POI source of truth.
- Extended `NewportTownBlueprint.gd` with required POI specs, return-landmark routing, optional secret data, reachability probes, detail blockers, screenshot viewpoints, and `opening_island_poi_landmarks_contract()`.
- Extended `Main.gd` with the runtime G-16 contract for validators and proof capture.
- Extended `MapLayer.gd` with authored island POIs: signal overlook, old road marker, cove hidden landing, wooded grove, farm/service edge, quest clue site, optional secret location, and return landmark.
- Added G-16 runtime screenshot automation and validator coverage.

Files changed:

- `docs/reports/G16_ISLAND_LANDMARK_POI_PASS.md`
- `docs/reports/G16_ISLAND_LANDMARK_POI_PASS.json`
- `docs/reports/OPENING_VILLAGE_ISLAND_AUTONOMOUS_EXECUTION_LEDGER.md`
- `docs/reports/OPENING_VILLAGE_ISLAND_AUTONOMOUS_EXECUTION_LEDGER.json`
- `docs/roadmaps/OPENING_VILLAGE_ISLAND_PRODUCTION_ROADMAP.json`
- `tools/wayfarer_agent_council.py`
- `wayfarer_godot_vertical_slice/data/world_layout/island_poi_landmarks_v1.json`
- `wayfarer_godot_vertical_slice/data/world_layout/opening_island_world_topology_v1.json`
- `wayfarer_godot_vertical_slice/scenes/Main.gd`
- `wayfarer_godot_vertical_slice/scenes/map/MapLayer.gd`
- `wayfarer_godot_vertical_slice/scripts/NewportTownBlueprint.gd`
- `wayfarer_godot_vertical_slice/tools/capture_g16_runtime_screenshots.gd`
- `wayfarer_godot_vertical_slice/tools/capture_g16_runtime_screenshots.gd.uid`
- `wayfarer_godot_vertical_slice/tools/capture_g16_runtime_screenshots.ps1`
- `wayfarer_godot_vertical_slice/tools/validate_island_poi_landmarks.py`

## Screenshot Proof

Manifest:

`wayfarer_godot_vertical_slice/artifacts/review/g16_runtime_screenshots/g16_runtime_screenshot_manifest.json`

Screenshots:

- `g16_01_signal_overlook_landmark.png`
- `g16_02_old_road_marker_and_grove.png`
- `g16_03_cove_hidden_landing.png`
- `g16_04_farm_service_edge_settlement.png`
- `g16_05_quest_clue_optional_secret.png`
- `g16_06_return_landmark_debug_disabled.png`

Inspection result: PASS. The regenerated captures show no HUD, no debug overlays, recognizable POI destinations, a return landmark, an optional secret location, a cove/landing destination, and a service-edge settlement read that gives the island purpose beyond town.

## Acceptance

- Player can name or recognize destinations: PASS
- Each POI supports exploration or quest purpose: PASS
- POIs are not random props: PASS
- Optional secret location exists: PASS
- Return landmark visible from multiple routes: PASS
- Art/world score: 8.6

## Scores

- Design score: 8.6
- World/layout score: 8.6
- Art direction score: 8.6
- UX/readability score: 8.6
- Technical stability score: 8.7
- Atelier/provenance result: PASS
- North Star result: PASS. G-16 turns the island route into a set of memorable destinations with mystery, return orientation, and future quest affordance; OVI-1 remains incomplete until G-22.

## Validation

- PASS: G-16 runtime screenshots regenerated from Godot 4.6.2.
- PASS: `validate_island_poi_landmarks.py`
- PASS: `validate_island_world_cohesion.py`
- PASS: `validate_village_to_island_transition.py`
- PASS: `validate_island_world_topology.py`
- PASS: `validate_opening_village_island_roadmap.py`
- PASS: `validate_opening_village_island_execution_ledger.py`
- PASS: `validate_vertical_slice.gd`
- PASS: route-probe collision repair verified after moving G-16 landmark collision footprints off walk/debug probes.
- PASS expected in Agent Council validator sweep before PR.
