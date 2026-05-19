# G-19S Newport Blockout-To-Godot Runtime Reconstruction

Phase: `G-19S`
Branch: `codex/g-19s-newport-blockout-to-godot-runtime-reconstruction`
Starting main commit: `f089baf36cb664519f0efd65824140979db4634f`
Source of truth: `docs/design/NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.json`
Runtime source: `wayfarer_godot_vertical_slice/data/world_layout/g19s_newport_runtime_reconstruction_v1.json`

## Verdict

G-19S implements the approved G-19R Newport source-of-truth blockout into the Godot runtime without inventing a new layout.

Agent Council verdict: `COUNCIL_PASS_READY_FOR_PR`

The phase does not claim OVI-1 production-playable completion. It clears the corrective runtime layout gate so the next phase can polish first-session guidance and quest readability on top of a measured town plan.

## Runtime Contract

- `runtime_layout_matches_G19R_source_of_truth`: true
- `no_new_layout_invented_in_Godot`: true
- Main commercial avenue: `12.0` character widths
- Harborfront road: `10.0` character widths
- Rear service lane: `5.5` character widths
- Wharf apron: `10.5` character widths
- Player arrival spawn: `(430, 920)`
- Counting house clerk spawn: `(1080, 555)`
- NPC movement policy: stationed until dedicated grounded walk animation exists
- Canonical G-19R camera viewpoints are consumed by the G-19S capture script

## Implemented Runtime Changes

- Rebuilt Newport road scale in `NewportTownBlueprint.gd` from G-19R tile/world rects.
- Repositioned major buildings by lot/frontage/orientation using the G-19R lot plan.
- Repositioned player, Edrin, and major village NPC stations to planned quest/NPC route pause points.
- Added `g19s_newport_runtime_reconstruction_v1.json` as the Godot-facing runtime source.
- Added source-driven map drawing for measured streets, lot grounding, wharf water, dock paths, working harbor props, tavern landmarks, counting-house civic markers, and exit guideposts.
- Added `g19s_runtime_reconstruction_contract()` for runtime proof and screenshot manifests.
- Added G-19S screenshot capture from canonical G-19R camera viewpoints.
- Added the G-19S validator and updated future source-alignment governance.

## Visual Proof

Screenshot directory: `wayfarer_godot_vertical_slice/artifacts/review/g19s_runtime_screenshots/`

Required captures:

- `g19s_01_wide_town_cohesion_view.png`
- `g19s_02_arrival_harbor_view.png`
- `g19s_03_counting_house_route_view.png`
- `g19s_04_tavern_landmark_view.png`
- `g19s_05_commercial_avenue_view.png`
- `g19s_06_harbor_work_view.png`
- `g19s_07_rear_service_lane_view.png`
- `g19s_08_npc_route_proof_view.png`
- `g19s_09_village_exit_to_island_view.png`
- `g19s_10_quest_interaction_view.png`
- `g19s_11_debug_disabled_view.png`

Manifest: `wayfarer_godot_vertical_slice/artifacts/review/g19s_runtime_screenshots/g19s_runtime_screenshot_manifest.json`

## Harsh-Critic Fix Loop

The first G-19S screenshot pass failed internal art-direction review because source lot pads read too much like translucent editor/blockout rectangles in normal runtime. The implementation was corrected by replacing hard lot overlays with softer yard/frontage grounding and reducing road opacity while preserving measured street widths. The screenshots were recaptured after the fix.

## Validation

Commands:

- `python wayfarer_godot_vertical_slice/tools/validate_g19s_newport_runtime_reconstruction.py`
- `python wayfarer_godot_vertical_slice/tools/validate_newport_layout_source_alignment.py`
- `python wayfarer_godot_vertical_slice/tools/validate_opening_village_island_roadmap.py`
- `python wayfarer_godot_vertical_slice/tools/validate_opening_village_island_execution_ledger.py`
- `Godot --headless --path wayfarer_godot_vertical_slice --import`
- `powershell -File wayfarer_godot_vertical_slice/tools/capture_g19s_runtime_screenshots.ps1`
- `tools/wayfarer_agent_council.py --phase "G-19S Newport Blockout-To-Godot Runtime Reconstruction" --run-validators`
- `git diff --check`
- `git diff --cached --check`

Expected result: PASS after this report, council report, and ledger updates are present.

## North Star Assessment

G-19S advances Newport from a patchy coordinate arrangement toward a source-driven harbor town. The runtime now has broad human-scale streets, a real wharf edge, a tavern landmark, a counting-house route, commercial frontages, rear/service logic, planned NPC stations, and a clear island exit. Residual first-session guidance, quest polish, and final runtime delight remain for G-19 and later OVI phases.
