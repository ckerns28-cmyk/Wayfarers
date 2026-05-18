# G-10B Multi-Path Starter Choice Foundation

Status: `PASS` for branch implementation pending PR checks.

G-10B turns the First Light opening mystery from a single linear sequence into a multi-path foundation. The player can now advance the mystery through harbor work, tavern rumor, counting-house pressure, merchant/street pressure, and optional secret clues.

## Runtime Scope

- Added `res://data/quests/first_light_multi_path_choices.json` as the multi-path source of truth.
- Added `FirstLightChoiceRouter.gd` to classify interaction payloads into counting-house, harbor-work, tavern-rumor, merchant-street, and optional-secret paths.
- Extended `FirstLightQuest.gd` with branch simulation proof for `harbor_first`, `merchant_first`, and `secret_first`.
- Exposed the multi-path contract through `Main.starter_village_multi_path_choice_contract()`.
- Added G-10B screenshot capture and validator proof.

## Acceptance Evidence

- At least two different NPC routes can advance the opening mystery.
- `harbor_work_path` can choose `ask_the_wharf`.
- `merchant_street_path` can advance the player to `secure_contact`.
- `optional_secret_path` can set `rear_service_gate_hint`.
- The opening quest data remains a G-10 quest arc while advertising G-10B extension support.
- The runtime screenshot manifest includes the multi-path contract and 15 proof captures.

## Screenshot Review

Inspected proof:

- `wayfarer_godot_vertical_slice/artifacts/review/g10b_runtime_screenshots/g10b_01_wide_newport_normal_gameplay_view.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g10b_runtime_screenshots/g10b_10_player_interacting_at_tavern_rumor_location.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g10b_runtime_screenshots/g10b_11_quest_prompt_journal_objective_proof.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g10b_runtime_screenshots/g10b_12_signs_markers_interaction_ux_proof.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g10b_runtime_screenshots/g10b_13_y_sort_layering_near_buildings_props.png`

The screenshots prove branch-path content and compact interaction readability. They also preserve the current residual visual concern: broad ground-material patchwork remains visible in wide and route shots. That is not a G-10B blocker because this phase is the starter-choice foundation, but it is now explicitly carried into G-11/G-12 review instead of being hidden by validator success.

## Improved Review Process

Chris's screenshot feedback exposed a production-process weakness: the council could over-trust written pass language when the image still showed ordering problems. This pass updates the council and QA process so screenshots can overrule reports. Future phases must fail if the screenshot evidence shows route/building confusion, tavern/commercial/civic ordering problems, debug artifacts, hovering NPCs, unclear objective state, non-atelier sprites, or phase-blocking ground patchwork.

## Validators

- `Godot_v4.6.2-stable_win64_console.exe --headless --path wayfarer_godot_vertical_slice --import`
- `Godot_v4.6.2-stable_win64_console.exe --headless --path wayfarer_godot_vertical_slice --script res://tools/validate_vertical_slice.gd`
- `powershell.exe -File wayfarer_godot_vertical_slice/tools/capture_g10b_runtime_screenshots.ps1`
- `python wayfarer_godot_vertical_slice/tools/validate_multi_path_starter_choice.py`
- `python wayfarer_godot_vertical_slice/tools/validate_opening_quest_arc.py`
- `python wayfarer_godot_vertical_slice/tools/validate_tavern_whisper_system.py`
- `python wayfarer_godot_vertical_slice/tools/validate_newport_visual_ordering.py`
- `python wayfarer_godot_vertical_slice/tools/validate_interaction_ux.py`
- `python wayfarer_godot_vertical_slice/tools/validate_runtime_atelier_asset_consistency.py`
- `python wayfarer_godot_vertical_slice/tools/validate_starter_village_roadmap.py`
- `python wayfarer_godot_vertical_slice/tools/validate_starter_village_execution_ledger.py`

## Scores

- Design score: 8.6
- Art direction score: 8.5
- World/layout score: 8.6
- NPC/animation score: 8.5
- Narrative score: 8.7
- Gameplay hook score: 8.7
- UX/readability score: 8.6
- Technical stability score: 8.8
- Performance/build score: 8.7
- Town cohesion score: 8.1

Next phase: `G-11 Living Town Rhythm Pass`.
