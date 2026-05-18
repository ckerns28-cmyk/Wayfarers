# G-9 Interaction UX and Diegetic Prompt Pass

Phase status: `PASS`

Branch: `codex/g-9-interaction-ux-prompts`

Council verdict: `COUNCIL_PASS_READY_FOR_PR`

## Purpose

G-9 turns the first layer of Newport interaction guidance from debug-like copy
into compact player-facing prompts. The pass keeps the interaction language
clear enough for a first-time player while removing the old "Press E to..."
instructional feel from normal in-world prompts.

The result is not the final SV-1 journal system. G-9 is the readability and
prompt presentation pass that prepares G-9A to add real quest state, objective
completion, journal feedback, and persistence.

## Runtime Changes

- Added the player `prompt_ux_contract()` for the
  `compact_diegetic_action_name_no_debug_marker` prompt style.
- Tightened the in-world prompt label to a smaller 12px, 160px-wide centered
  prompt so review zoom does not create oversized floating labels.
- Updated building interaction prompts from old debug-like copy to
  `E: Enter - Name` or `E: Inspect - Name`.
- Updated Edrin Vale and reusable atelier NPC prompts to `E: Talk - Name`.
- Updated the HUD first objective to point the player from the Counting House
  toward the tavern whisper.
- Added objective-update and rumor-guidance copy for proof frames:
  `Objective updated: ask about the missing ledger line.` and
  `Rumor: the Third Toast begins at the Tavern/Inn.`
- Added G-9 runtime screenshot capture and manifest proof.
- Extended `validate_interaction_ux.py` and `validate_vertical_slice.gd` so
  compact prompts, objective guidance, and debug-copy absence are runtime
  checked.

## Prompt Contract

| Target | Required Prompt |
| --- | --- |
| Harbor Mercantile | `E: Enter - Harbor Mercantile` |
| Inn & Tavern | `E: Enter - Inn & Tavern` |
| Dock Storehouse | `E: Inspect - Dock Storehouse` |
| Edrin Vale | `E: Talk - Edrin Vale` |
| Bess Armitage | `E: Talk - Bess Armitage` |

Normal play prompts must not use `Press E` copy, crude debug markers, oversized
labels, or prototype sign objects as the primary interaction affordance.

## Screenshot Evidence

Runtime screenshot manifest:
`wayfarer_godot_vertical_slice/artifacts/review/g9_runtime_screenshots/g9_runtime_screenshot_manifest.json`

Council-inspected frames:

- `g9_01_wide_newport_normal_gameplay_view.png`: PASS for clear first-goal HUD
  language without debug overlays.
- `g9_03_player_on_route_to_counting_house.png`: PASS for compact
  `E: Talk - Edrin Vale` prompt on the first route.
- `g9_05_player_on_commercial_avenue.png`: PASS for compact
  `E: Enter - Harbor Mercantile` prompt on the commercial spine.
- `g9_09_player_interacting_with_counting_house_clerk.png`: PASS for readable
  dialogue at the counting-house objective.
- `g9_10_player_interacting_at_tavern_rumor_location.png`: PASS for readable
  tavern/rumor interaction proof.
- `g9_11_quest_prompt_journal_objective_proof.png`: PASS for objective-update
  and rumor-guidance feedback.
- `g9_14_debug_overlays_disabled.png`: PASS for normal-play screenshot proof
  without debug overlays or crude markers.

## Validation Results

| Check | Result |
| --- | --- |
| Godot import validation | PASS |
| Vertical slice validator | PASS |
| G-9 screenshot capture and PNG verification | PASS |
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
| Art direction score | 8.5/10 |
| World/layout score | 8.5/10 |
| Narrative score | 8.5/10 |
| NPC animation score | 8.5/10 |
| Technical stability score | 8.8/10 |
| Performance/build score | 8.7/10 |

## Council Finding

G-9 passes because the player-facing interaction layer now names nearby
interactables cleanly, points the first objective toward the Counting House and
tavern whisper, and avoids debug-like prompt language in normal play.

The council does not certify SV-1. The next production need is G-9A, where the
opening objective must become real quest state with journal feedback, objective
completion, dialogue-driven progress, and a reward/progression beat.
