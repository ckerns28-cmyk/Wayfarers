# G-7A-SV0 Tool-Backed Layout Repair

Phase: `G-7A-SV0`

Branch: `codex/g-7a-tool-backed-layout-repair`

Purpose: repair the Starter Village layout using the SV-0 locked layout source before continuing later living-town passes.

## Screenshot Failures Addressed

- Tavern rear-yard read: the scene implied a stable or fenced horse yard behind/near the tavern. That did not work visually, so the normal-play support props and lot foundations were moved to the actual rear lane or wharf work area.
- Building overlap: the upper/rear houses were crowding and one house could be clipped by the review view. Active support-lane and residential lots now use camera-safe anchors from `starter_village_world_layout_v1.json`.
- Scale mismatch: the rowhouse and adjacent mercantile looked like incompatible building scales. `b_mercantile` now has a larger draw width and an explicit G-7A-SV0 catalog note.
- Source-of-truth bypass: `b_market_shed` was still using a hand-coded fallback coordinate. It now uses `_runtime_lot_foot_tile(...)` like the other active starter buildings.
- Ground patchwork: the broad G-7A ground washes, service connectors, and upper-town road layer were repainted so harborfront avenue, wharf apron, back street, and uphill connectors read as authored town surfaces rather than debug-like translucent slabs.
- Upper-town context: the expanded-town street and lot context now participates in the normal G-7A draw path, but its lot washes are subdued so fences, thresholds, and roads define the district instead of visible editor rectangles.

## Validator Catches

`wayfarer_godot_vertical_slice/tools/validate_starter_village_layout_source_usage.py` now fails if:

- any active starter building lacks an authoritative lot assignment;
- runtime building specs bypass the lot source;
- layout anchors create overlap spacing risks;
- a building anchor risks edge cutoff;
- cooperage or service details move back into a false stable/tavern-yard read;
- old rejected layout tokens remain in normal-play map drawing;
- the mercantile scale repair is removed.

## Locked Placement Contract

- Active layout source: `wayfarer_godot_vertical_slice/data/world_layout/starter_village_world_layout_v1.json`
- Runtime source hook: `NewportTownBlueprint.starter_village_runtime_lot_assignments()`
- Ground/lot rendering hook: `MapLayer._draw_g7a_lot_foundation_overlays()`
- Street/ground repair hook: `MapLayer._draw_g7a_cohesive_ground_foundation()`, `MapLayer._draw_g7a_continuous_street_base()`, and `MapLayer._draw_g423a_expanded_town_streets()`
- Scale repair hook: `BuildingCatalog.gd`
- Latest screenshot proof: `wayfarer_godot_vertical_slice/artifacts/review/g7a_runtime_screenshots/g7a_runtime_screenshot_manifest.json`

## Current Council Standard

This subpass is not allowed to pass from documentation only. It requires the new validator, existing Newport cohesion/visual-order validators, runtime screenshot proof, and Agent Council inspection. If the screenshots still show overlap, cutoff houses, a false tavern stable yard, toy-scale building mismatch, or debug-like route/lot rectangles, the final verdict must be `COUNCIL_FAIL_NEEDS_CODE_FIX`.

Current inspection result: the specific Chris screenshot failures are repaired in the latest G-7A proof set. Newport remains below the SV-1 obsession bar; the next roadmap work must keep improving district identity, NPC grounding/motion, first-session quest pacing, and visual richness instead of treating this corrective pass as final village quality.
