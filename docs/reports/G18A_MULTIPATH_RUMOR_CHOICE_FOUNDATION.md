# G-18A Multi-Path Rumor and Choice Foundation

Phase ID: G-18A

Branch: `codex/g-18a-multipath-rumor-choice-foundation`

Commit: `1e96ba73f7af404b5bdc20806a74b61117f257d1`

PR number: `#488`

Merge status: `merged`

Status: PASS

Human review required: no

Reason: G-18A is an ordinary autonomous phase inside the larger OVI-1 runway. It does not stop for Chris unless a true blocker occurs.

Agent Council verdict: `COUNCIL_PASS_READY_FOR_PR`

Next phase: G-19 Player Guidance, Map, Journal, and Interaction Polish

Merged main commit: `6e8c5fc59c827d1b3adf84eb90a452c7092f4e57`

## Purpose

Make the village-to-island opening feel like an RPG investigation rather than a railroad. Newport must remain the social origin of the world: counting-house pressure, tavern rumor, dockworker harbor knowledge, and optional island clue discovery all need to matter.

The bar is still the North Star: a first-time player should feel that people, places, rumor networks, and route choices are pulling them through a pre-Revolutionary harbor mystery, not that they are clicking through a functional checklist.

## Implementation

- Added `whispers_before_dawn_multipath_rumor_choice_v1.json` as the G-18A source of truth.
- Extended `FirstLightQuest.gd` with `debug_village_to_island_multipath_choice_contract()`.
- Added route-choice state for `island_route_choice`, `optional_clue_enriched_journal`, and `return_report_route_choice`.
- Exposed the branch contract through `Main.opening_village_to_island_multipath_choice_contract()`.
- Added Godot runtime proof capture for branch screenshots, branch trace, screenshot manifest, and branch log.
- Expanded `validate_multipath_rumor_choice_foundation.py` from a roadmap stub into a source/runtime/proof/report validator.

## Required Paths

- Counting-house path: Edrin/Mara/Bess pressure still opens the island lead.
- Tavern rumor path: Bess and Elias turn the Third Toast into coded old-road direction.
- Dockworker/harbor path: harbor labor and wharf lantern knowledge lead to hidden landing evidence.
- Optional island clue path: Mara Oren's signal cache enriches the journal without blocking progress.

## Proof

Screenshot manifest:

`wayfarer_godot_vertical_slice/artifacts/review/g18a_runtime_screenshots/g18a_runtime_screenshot_manifest.json`

Quest branch proof:

- `wayfarer_godot_vertical_slice/artifacts/review/g18a_quest_branch_proof/multipath_branch_log.md`
- `wayfarer_godot_vertical_slice/artifacts/review/g18a_quest_branch_proof/multipath_branch_trace.json`
- `wayfarer_godot_vertical_slice/artifacts/review/g18a_quest_branch_proof/multipath_branch_screenshot_manifest.json`

Required screenshots regenerated:

- `g18a_01_counting_house_path.png`
- `g18a_02_tavern_rumor_path.png`
- `g18a_03_dockworker_harbor_path.png`
- `g18a_04_optional_island_clue_path.png`
- `g18a_05_return_report_choice.png`
- `g18a_06_branch_contract_journal.png`

Inspection result: PASS. Screenshots and branch trace prove distinct village-to-island route state, optional journal enrichment, return/report choice, readable objective updates, and no debug overlays.

## Acceptance

- Player agency exists: PASS
- Quest state supports branching: PASS
- At least two NPCs can advance the main thread: PASS
- Optional discovery enriches the journal: PASS
- Choice changes dialogue, route, or next objective text: PASS
- No broken branches: PASS
- No unclear progression: PASS

Scores:

- Design score: 8.6
- World/layout score: 8.6
- Art direction score: 8.6
- Quest/narrative score: 8.6
- UX/readability score: 8.6
- Technical stability score: 8.7
- Atelier/provenance result: PASS
- North Star result: PASS

## Validation

- PASS: Godot import validation
- PASS: `capture_g18a_multipath_choice_proof.ps1`
- PASS: G-18A runtime screenshot manifest
- PASS: G-18A multi-path branch trace
- PASS: G-18A branch screenshot manifest
- PASS: G-18A branch log
- PASS: `validate_multipath_rumor_choice_foundation.py`
- PASS: Agent Council validator sweep

G-18A does not complete OVI-1. It proves the opening quest is no longer a single railroaded path and is ready for G-19 guidance, journal, map, and interaction polish.
