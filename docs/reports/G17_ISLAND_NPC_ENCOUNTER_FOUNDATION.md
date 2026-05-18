# G-17 Island NPC / Encounter / Ambient Life Foundation

Phase ID: G-17

Branch: `codex/g-17-island-npc-encounter-foundation`

Commit: `50b4f16a6d32590613126c111334d53ff2e45d4d`

PR number: `pending_open_pr`

Merge status: `pending`

Status: PASS

Human review required: no

Reason: G-17 is an ordinary autonomous phase inside the larger OVI-1 runway. It does not stop for Chris unless a true blocker occurs.

Agent Council verdict: `COUNCIL_PASS_READY_FOR_PR`

Next phase: G-18 Opening Quest Extension: From Whispers to the Island

## Purpose

Make the opening island feel alive beyond Newport without pretending that spawnable sprites are enough. This pass adds purposeful, grounded island NPCs and ambient encounters tied to route stations, rumors, the missing-manifest mystery, and the return-to-town hook.

The bar is authored-world pull: the island should feel like a lived borderland outside a pre-Revolutionary harbor town, with the social texture and mystery momentum expected from the Tibia/Ragnarok inspiration set.

## Implementation

- Added `wayfarer_godot_vertical_slice/data/world_layout/island_npc_encounter_foundation_v1.json` as the source of truth for G-17 island NPCs, stations, roles, dialogue seeds, movement policy, proof paths, and acceptance.
- Extended `NewportTownBlueprint.gd` with G-17 island NPC specs, ambient rhythm specs, and `opening_island_npc_encounter_contract()`.
- Extended `Main.gd` with runtime island NPC spawning, rhythm configuration, debug proof ticks, drift detection, bark suppression, and the live G-17 contract.
- Extended `AtelierTownNpc.gd` so island NPCs use island runtime groups while preserving starter-village groups for village NPCs.
- Added runtime screenshot and motion-proof automation for no-HUD/no-debug island-life proof.
- Replaced the G-17 validator stub with source, runtime, screenshot, motion, atelier, and report validation.

## NPC / Encounter Set

- Isla Brooke, farmhand: pasture crossing, service-edge life, signal-rise warning.
- Tomas Reed, dock runner: hidden landing, cove cargo mark, missing-manifest clue pressure.
- Elias Ward, suspicious courier: old road marker, coded whisper bridge from the tavern path.
- Mara Oren, coast patrol: signal overlook, lantern warning language, island tension.
- Annelise Crow, rumor contact: return landmark, report-home hook, village momentum.

Movement is grounded, no-glide: island NPCs use facing changes, idle pauses, and barks while remaining anchored until dedicated walk sheets exist.

## Screenshot Proof

Manifest:

`wayfarer_godot_vertical_slice/artifacts/review/g17_runtime_screenshots/g17_runtime_screenshot_manifest.json`

Screenshots:

- `g17_01_island_life_wide.png`
- `g17_02_farmhand_service_edge.png`
- `g17_03_dock_runner_cove_watch.png`
- `g17_04_suspicious_courier_old_road.png`
- `g17_05_signal_patrol_overlook.png`
- `g17_06_return_rumor_contact_debug_disabled.png`

## Motion Proof

Trace:

`wayfarer_godot_vertical_slice/artifacts/review/g17_motion_proof/g17_island_npc_motion_trace.json`

Timestamped frame sequence:

- `g17_motion_frame_00.png`
- `g17_motion_frame_01.png`
- `g17_motion_frame_02.png`
- `g17_motion_frame_03.png`
- `g17_motion_frame_04.png`

Motion result: PASS. The proof shows stable ground anchors, facing/bark state changes, visible ground shadows, no hover, no glide, no slide, and no static-sprite translation.

## Acceptance

- Island does not feel empty: PASS
- NPCs reinforce opening mystery: PASS
- Each NPC has purpose, station, interaction/bark, and quest or world relevance: PASS
- All visible NPCs use approved atelier sprite assets: PASS
- NPC motion/grounding score: 8.6
- Design score: 8.6
- World/layout score: 8.6
- Art direction score: 8.6
- UX/readability score: 8.6
- Technical stability score: 8.7
- Atelier/provenance result: PASS
- North Star result: PASS

## Validation

Commands:

- `powershell -ExecutionPolicy Bypass -File wayfarer_godot_vertical_slice/tools/capture_g17_runtime_screenshots.ps1`
- `python wayfarer_godot_vertical_slice/tools/validate_island_npc_encounter_foundation.py`
- `python wayfarer_godot_vertical_slice/tools/validate_character_motion_foundation.py`
- `python wayfarer_godot_vertical_slice/tools/validate_npc_population_and_routes.py`
- `python wayfarer_godot_vertical_slice/tools/validate_runtime_atelier_asset_consistency.py`
- `python wayfarer_godot_vertical_slice/tools/validate_opening_village_island_roadmap.py`
- `python wayfarer_godot_vertical_slice/tools/validate_opening_village_island_execution_ledger.py`
- `godot --headless --path wayfarer_godot_vertical_slice --script res://tools/validate_vertical_slice.gd`
- `tools/wayfarer_agent_council.py --phase "G-17 Island NPC / Encounter / Ambient Life Foundation" --run-validators`
- `git diff --check`
- `git diff --cached --check`

Validation result: PASS. G-17 proves a grounded island-life foundation without promoting fake walking or non-atelier placeholders. OVI-1 remains incomplete until G-22.
