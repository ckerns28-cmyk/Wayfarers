# G-9A Journal, Objective, and Quest State Foundation

Phase status: `PASS`

Branch: `codex/g-9a-journal-objective-state`

Council verdict: `COUNCIL_PASS_READY_FOR_PR`

## Purpose

G-9A gives the opening loop real in-session quest state instead of a static
prompt. The player can now make landfall, find Edrin Vale, advance the missing
ledger line, follow a tavern whisper, and receive a small progression reward.

This is not the full G-10 10-15 minute quest arc. It is the foundation that
lets G-10 build richer content on objective state, journal feedback, NPC-driven
progression, optional clue paths, and reward state.

## Runtime Systems

- Added `QuestState.gd` as the session quest-state tracker.
- Added `FirstLightQuest.gd` for the First Light / Whispers Before Dawn
  objective flow.
- Added `first_light_whispers_before_dawn.json` as structured quest data.
- Added `Player.interaction_triggered(target, text)` so quest progression can
  react to the actual interacted NPC/building.
- Added `Main.starter_village_quest_contract()` and debug playthrough helpers
  for validation and screenshot proof.
- Added `HUD.apply_quest_snapshot()` and `HUD.journal_objective_contract()` so
  the quest panel behaves as a journal/objective surface.
- Objective updated feedback is visible in the quest panel as objectives
  advance through the missing ledger line and tavern whisper beats.

## Objective Flow

| Step | Runtime Result |
| --- | --- |
| Make landfall | Completed automatically when the session starts in Newport Harbor. |
| Report to Counting House | Completed by interacting with Edrin Vale. |
| Investigate missing line | Advanced by dockworker, merchant, notice-board, or rumor clues. |
| Follow tavern whisper | Advanced by Bess Armitage at the Tavern/Inn. |
| Choose next lead | Opens the next lead: Edrin, the wharf, or the rear service gate. |

Reward/progression update: `Reward: Resolve +5 for following the tavern whisper`.

## Screenshot Evidence

Runtime screenshot manifest:
`wayfarer_godot_vertical_slice/artifacts/review/g9a_runtime_screenshots/g9a_runtime_screenshot_manifest.json`

Council-inspected frames:

- `g9a_01_wide_newport_normal_gameplay_view.png`: PASS for initial Journal -
  First Light objective state.
- `g9a_09_player_interacting_with_counting_house_clerk.png`: PASS for Edrin
  interaction advancing the missing ledger objective.
- `g9a_10_player_interacting_at_tavern_rumor_location.png`: PASS for tavern
  whisper progression and Resolve reward state.
- `g9a_11_quest_prompt_journal_objective_proof.png`: PASS for journal,
  objective update, rumor, and reward feedback fitting the quest panel.
- `g9a_14_debug_overlays_disabled.png`: PASS for normal play without debug
  overlays.
- `g9a_15_contact_sheet_provenance_proof.png`: PASS for final quest contract
  with reward log and next-lead state.

## Validation Results

| Check | Result |
| --- | --- |
| Godot import validation | PASS |
| Vertical slice validator | PASS |
| G-9A screenshot capture and PNG verification | PASS |
| Opening quest arc validator | PASS |
| Interaction UX validator | PASS |
| Runtime atelier asset consistency validator | PASS |
| Starter Village roadmap validator | PASS |
| Starter Village execution ledger validator | PASS |
| Git diff whitespace check | PASS |

## Phase Scores

| Category | Score |
| --- | --- |
| UX/readability score | 8.6/10 |
| Design score | 8.5/10 |
| Narrative score | 8.6/10 |
| Gameplay hook score | 8.5/10 |
| Art direction score | 8.5/10 |
| World/layout score | 8.5/10 |
| NPC animation score | 8.5/10 |
| Technical stability score | 8.8/10 |
| Performance/build score | 8.7/10 |

## Council Finding

G-9A passes because First Light now has real runtime quest state, objective
completion, journal feedback, dialogue-driven advancement, optional clue-source
support, and a reward/progression update. The next production need is G-10,
which must expand this foundation into a compelling 10-15 minute opening quest
arc rather than adding more static text.
