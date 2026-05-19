# G-19R Newport Scale + Street Blockout Source Of Truth

Final status: `PASS`

Branch: `codex/g-19r-newport-scale-street-blockout-source-of-truth`

Starting main commit: `6e8c5fc59c827d1b3adf84eb90a452c7092f4e57`

## Correction

G-19R stops Newport from advancing as a code-coordinate problem. It establishes a measured, human-readable, machine-checkable town plan before more Godot placement, island expansion, quest expansion, or production-playable claims.

## Tools Used

- Browser research for level-design flow/blockout thinking and 1700s harbor/tavern context.
- Repo Godot/Python source inspection for current player, collision, camera, viewport, and map scale.
- Deterministic Python/Pillow generator for SVG/PNG/JSON blockout artifacts.
- JSON validators for G-19R artifact completeness and future layout-source alignment.

Figma/FigJam used: no. Fallback method: repo-contained SVG/PNG/JSON measured blockout.

## Scale Metrics Summary

- Player visual width: `27.2` world units.
- Player visual height: `65.92` world units.
- Player collision/body width: `20.0` world units.
- Player collision/body height: `28.0` world units.
- Gameplay viewport assumption: `1280x720` at zoom `1.38`.
- Main street target: `12.0` character widths.
- Current 3-tile road audit: `3.529` character widths, not acceptable proof.

## Artifact Paths

- `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_measured_blockout.svg`
- `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_measured_blockout.png`
- `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_scale_metrics.json`
- `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_district_plan.json`
- `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_street_hierarchy.json`
- `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_lot_plan.json`
- `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_npc_route_plan.json`
- `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_quest_beat_locations.json`
- `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_camera_viewpoints.json`
- `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_blockout_manifest.json`

## Plan Summary

Street hierarchy: main commercial avenue, harborfront road, rear service street, counting-house connector, tavern connector, market connector, dock paths, hidden service cut-through, village-to-island road, and optional side path. All widths are expressed in character units.

District plan: harbor/wharf, counting house, tavern/inn, commercial avenue, rear service lane, residential edge, village-to-island exit, civic notice board, hidden rumor route.

Lot plan: Tavern/Inn, Counting House, mercantile, chandlery, market shed, warehouses, boathouse, cooperage, boarding house, dockworker rowhouse, clerk lodging, notice board, and exit guidepost all have street frontage, entry orientation, footprint target, setback, NPC use, quest use, and sightline purpose.

NPC route plan: dockworker, clerk/runner, tavern rumor carrier, merchant/shopkeeper, and courier/sailor routes are planned, but all remain stationed until grounded walk animation proof exists.

Quest beat map: arrival harbor, first objective, counting-house manifest, dock clue, tavern whisper, two-NPC rumor, island lead, village exit, hidden clue, and return/report are placed into town geography.

Camera viewpoints: eleven canonical review/playtest views prevent the plan from relying on a miniature wide map.

## Acceptance Scores

- Blockout/layout plan score: `8.7`
- World cohesion plan score: `8.7`
- Player orientation plan score: `8.6`
- Quest-geography integration score: `8.6`
- Implementation-readiness score: `8.6`

All scores meet or exceed 8.5.

## Validators

- `wayfarer_godot_vertical_slice/tools/validate_g19r_newport_blockout_source_of_truth.py`
- `wayfarer_godot_vertical_slice/tools/validate_newport_layout_source_alignment.py`

Agent Council verdict: `COUNCIL_PASS_READY_FOR_PR`

Next phase: `G-19S Newport Blockout-To-Godot Runtime Reconstruction`
