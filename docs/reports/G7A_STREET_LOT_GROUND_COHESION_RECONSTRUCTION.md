# G-7A Street, Lot, and Ground Cohesion Reconstruction

Phase: `G-7A`

Branch: `codex/g-7a-street-lot-ground-cohesion`

Commit: `pending_current_phase_commit`

PR: `pending_current_phase_pr`

## Purpose

G-7A turns the G-7 masterplan into runtime town grammar. The goal is not to
finish Newport to SV-1 quality; it is to move the visible baseline from Chris's
approximately 2/10 patchwork town cohesion signal to a playable, connected
7.5+ foundation that G-7B, G-7C, and G-8 can build on.

## Runtime Changes

- Added a G-7A cohesion pass to `MapLayer.gd` with one continuous harborfront
  avenue, one rear/back street, a subdued service lane, uphill connectors, and
  a wharf apron that ties road, dock, and water together.
- Replaced the older stack of translucent planning washes in normal play with a
  single subdued lot-foundation layer for the tavern, clerk/mercantile block,
  counting house, custom house, chandlery/shop, market, residential blocks,
  support lots, and wharf lots.
- Softened old tan service-lane strokes so they read as worn paths instead of
  debug-like route markers.
- Kept debug/blockout guides and primitive normal-play markers hidden.
- Added a 15-shot G-7A runtime screenshot harness preserving no-HUD capture.

## Roads Lead Somewhere

Roads lead somewhere: PASS.

The wide screenshot now shows a harborfront route parallel to the wharf, a
rear/back street behind the waterfront road, uphill connectors between harbor
commerce and civic/residential blocks, and service traces that connect market,
tavern, and dock work. The wharf edge is no longer isolated from the road
system.

## Town Cohesion Score

Town cohesion score: `7.6/10`

Council read: PASS for G-7A, not SV-1. The town now reads as one planned harbor
village foundation, but it still needs G-7B harbor/commercial purpose, G-7C
landmark identity, G-8 grounded motion, and later quest/NPC/UX passes before it
can approach the 8.5+ SV-1 bar.

## Screenshot Evidence

Manifest:
`wayfarer_godot_vertical_slice/artifacts/review/g7a_runtime_screenshots/g7a_runtime_screenshot_manifest.json`

The manifest contains the full 15-view recurring screenshot set:

1. `g7a_01_wide_newport_normal_gameplay_view.png`
2. `g7a_02_player_arrival_at_harbor.png`
3. `g7a_03_route_to_counting_house.png`
4. `g7a_04_player_near_tavern_inn.png`
5. `g7a_05_commercial_avenue.png`
6. `g7a_06_dock_wharf_work_area.png`
7. `g7a_07_npc_movement_path_area.png`
8. `g7a_08_npc_idle_and_walking_proof_area.png`
9. `g7a_09_counting_house_interaction_area.png`
10. `g7a_10_tavern_rumor_location_area.png`
11. `g7a_11_objective_route_readability_area.png`
12. `g7a_12_signs_markers_interaction_ux_area.png`
13. `g7a_13_y_sort_layering_near_buildings.png`
14. `g7a_14_debug_overlays_disabled.png`
15. `g7a_15_provenance_no_new_assets_contact_sheet_area.png`

## Validation Results

- PASS: Godot import validation.
- PASS: vertical slice validator.
- PASS: G-7A screenshot capture and PNG verification.
- PASS: Newport world cohesion validator.
- PASS: runtime atelier asset consistency validator.
- PASS: starter village roadmap validator.
- PASS: starter village execution ledger validator.
- PASS: `git diff --check`.

## Known Caveats

- NPCs still need the G-8 grounded motion foundation; this phase does not
  certify animation quality.
- Harbor work purpose is readable enough for G-7A but still needs the G-7B
  economic spine pass.
- Tavern/Inn remains a visual/social anchor, but G-10A must make whisper
  gameplay real.
- Top/background buildings are retained as town depth and will need later
  landmark/district polish.

## G-7B Next

G-7B next: harbor/commercial spine cohesion.

Next phase: `G-7B Harbor, Wharf, and Commercial Spine Cohesion`.

G-7B must make harbor labor, market goods, counting-house commerce, and wharf
routes read as the economic engine of the town.
