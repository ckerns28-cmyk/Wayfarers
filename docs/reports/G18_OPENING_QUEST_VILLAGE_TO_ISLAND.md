# G-18 Opening Quest Extension: From Whispers to the Island

Phase ID: G-18

Branch: `codex/g-18-opening-quest-village-to-island`

Commit: `9526ea0133c93190f80695e1d83995d018f2d81f`

PR number: `#487`

Merge status: `pending`

Status: PASS

Human review required: no

Reason: G-18 is an ordinary autonomous phase inside the larger OVI-1 runway. It does not stop for Chris unless a true blocker occurs.

Agent Council verdict: `COUNCIL_PASS_READY_FOR_PR`

Next phase: G-18A Multi-Path Rumor and Choice Foundation

## Purpose

Extend Whispers Before Dawn from Newport's harbor, counting house, tavern, and wharf rumor network into a playable opening island investigation. This village-to-island quest chain is judged against the North Star: Newport must feel like the origin of a larger pre-Revolutionary harbor RPG, not a functional demo that happens to advance objectives.

The inspiration bar remains Tibia/Ragnarok-style first-session pull: memorable town routes, NPC social texture, a road out of safety, a discoverable clue, a reward beat, and a reason to keep playing.

## Implementation

- Extended `FirstLightQuest.gd` with G-18 objectives: island lead, old-road travel, physical evidence, return/report choice, and the renewed dawn hook.
- Added island NPC quest handling for Isla Brooke, Elias Ward, Mara Oren, Tomas Reed, and Annelise Crow.
- Preserved the existing G-10/G-12 town proof path by keeping the original Edrin dawn hook behavior intact.
- Added `debug_village_to_island_playthrough_contract()` and exposed it through `Main.gd` as `opening_village_to_island_quest_contract()`.
- Added `whispers_before_dawn_village_to_island_v1.json` as the G-18 source of truth.
- Added runtime proof capture for screenshots, quest state trace, screenshot manifest, and quest playthrough log.
- Expanded `validate_opening_quest_village_to_island.py` to validate source, runtime contracts, proof artifacts, scores, reports, and OVI ledger integration.

## Playthrough Beats

- Arrival and first objective at Newport Harbor.
- Edrin confirms the missing manifest line at the Counting House.
- Dockworker/harbor clue makes the ledger gap physical.
- Bess and the Third Toast turn rumor into coded direction.
- Jonah's wharf lantern gives the island route social proof.
- Isla turns the village edge into a deliberate island lead.
- Elias carries the coded whisper onto the old road.
- Mara Oren adds the optional signal clue.
- Tomas reveals physical evidence at the hidden landing.
- Annelise frames the return/report choice.
- Edrin accepts the proof and gives the next dawn hook.

## Proof

Screenshot manifest:

`wayfarer_godot_vertical_slice/artifacts/review/g18_runtime_screenshots/g18_runtime_screenshot_manifest.json`

Quest proof:

- `wayfarer_godot_vertical_slice/artifacts/review/g18_quest_playthrough/quest_playthrough_log.md`
- `wayfarer_godot_vertical_slice/artifacts/review/g18_quest_playthrough/quest_playthrough_state_trace.json`
- `wayfarer_godot_vertical_slice/artifacts/review/g18_quest_playthrough/quest_playthrough_screenshot_manifest.json`

Required screenshots regenerated:

- `g18_01_arrival_first_objective.png`
- `g18_02_counting_house_missing_manifest.png`
- `g18_03_harbor_ledger_dockworker.png`
- `g18_04_tavern_third_toast_whisper.png`
- `g18_05_wharf_lantern_rumor.png`
- `g18_06_edrin_dawn_hook_to_island.png`
- `g18_07_village_exit_island_lead.png`
- `g18_08_old_road_coded_whisper.png`
- `g18_09_signal_optional_clue.png`
- `g18_10_hidden_landing_physical_evidence.png`
- `g18_11_return_contact_report_choice.png`
- `g18_12_return_to_town_reward_next_hook.png`

Inspection result: PASS. Screenshots show journal/objective updates, authored village-to-island route intent, a physical island clue, optional signal clue, return/report social hook, and no debug overlays.

## Acceptance

- Village-to-island quest chain playable end to end: PASS
- Player knows next objective: PASS
- Quest state updates correctly: PASS
- Dialogue supports the story: PASS
- Island exploration has purpose: PASS
- At least two ways to gather/confirm the lead: PASS
- Optional clue enriches the journal: PASS
- Reward/progression beat exists: PASS
- Meaningful return-to-town moment exists: PASS

Scores:

- Design score: 8.6
- World/layout score: 8.6
- Art direction score: 8.6
- Opening quest gameplay score: 8.6
- Narrative hook score: 8.6
- UX/readability score: 8.6
- Technical stability score: 8.7
- Atelier/provenance result: PASS
- North Star result: PASS

## Validation

- PASS: Godot import validation
- PASS: `capture_g18_quest_playthrough.ps1`
- PASS: G-18 runtime screenshot manifest
- PASS: G-18 quest playthrough state trace
- PASS: G-18 quest playthrough screenshot manifest
- PASS: G-18 quest playthrough log
- PASS: `validate_opening_quest_village_to_island.py`
- PASS: Agent Council validator sweep

G-18 does not complete OVI-1. It proves the first village-to-island quest spine is playable and ready for G-18A branching/choice hardening.
