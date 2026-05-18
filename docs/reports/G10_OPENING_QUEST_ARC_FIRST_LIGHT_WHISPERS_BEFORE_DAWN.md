# G-10 Opening Quest Arc: First Light / Whispers Before Dawn

Phase status: `PASS`

Branch: `codex/g-10-opening-quest-arc`

Council verdict: `COUNCIL_PASS_READY_FOR_PR`

## Purpose

G-10 turns the G-9A quest-state foundation into a playable first-session hook.
The player now lands at Newport Harbor, reports to Edrin Vale at the Counting
House, investigates a missing ledger line, follows the Third Toast rumor at the
Tavern/Inn, chooses a wharf-lantern lead, discovers an optional rear-gate
secret, earns progression, and receives a reason to continue at dawn.

This does not claim the later G-10A tavern whisper system or G-10B multi-path
foundation are complete. It establishes the full opening arc spine those phases
will deepen.

## Playable Quest Beats

| Beat | Runtime Result |
| --- | --- |
| Make landfall | Newport Harbor is logged and the Counting House objective becomes active. |
| Report to Edrin Vale | Edrin confirms the missing ledger line and sends the player to the wharf and Tavern/Inn. |
| Investigate the missing line | Mara Pike or other clue sources confirm the omission is intentional. |
| Hear the Third Toast | Bess Armitage turns the missing line into a tavern-whisper mystery. |
| Choose a rumor path | The player can trust Edrin, ask the wharf, follow merchant/street money, or watch the rear gate. |
| Lantern at the wharf | Jonah Reed confirms the two-lantern signal and the hidden cargo network. |
| Optional secret | Silas Crowe reveals that some messages move through the rear service gate. |
| Hook to continue | Edrin becomes a named contact and asks the player to keep the missing line quiet until dawn. |

Reward/progression updates:

- `Reward: Resolve +5 for following the tavern whisper`
- `Named contact: Edrin Vale`

## Runtime Systems

- Expanded `FirstLightQuest.gd` from five foundation objectives to eight
  opening-arc objectives.
- Added dialogue responses to quest interactions so player-facing NPC text
  reflects current quest state.
- Added wharf-lantern and named-contact objectives.
- Added branch-choice, optional-discovery, and reason-to-continue contracts for
  validators and council proof.
- Expanded `Main.starter_village_quest_contract()` with flags, progress
  updates, response text, and the `G-10` opening-arc marker.
- Updated `first_light_whispers_before_dawn.json` with the G-10 playable arc
  data.

## Screenshot Evidence

Runtime screenshot manifest:
`wayfarer_godot_vertical_slice/artifacts/review/g10_runtime_screenshots/g10_runtime_screenshot_manifest.json`

Council-inspected frames:

- `g10_01_wide_newport_normal_gameplay_view.png`: PASS for initial orientation
  and normal-play HUD state.
- `g10_09_player_interacting_with_counting_house_clerk.png`: PASS for Edrin
  starting the missing-line investigation.
- `g10_10_player_interacting_at_tavern_rumor_location.png`: PASS for Bess,
  Third Toast rumor content, and reward progression.
- `g10_11_quest_prompt_journal_objective_proof.png`: PASS for Jonah's
  wharf-lantern branch and the secure-contact objective.
- `g10_12_signs_markers_interaction_ux_proof.png`: PASS for Silas and the
  optional rear-gate discovery.
- `g10_15_contact_sheet_provenance_proof.png`: PASS for the Edrin named-contact
  reward and dawn hook-to-continue state.

## Validation Results

| Check | Result |
| --- | --- |
| Godot import validation | PASS |
| Vertical slice validator | PASS |
| G-10 screenshot capture and PNG verification | PASS |
| Opening quest arc validator | PASS |
| Interaction UX validator | PASS |
| Runtime atelier asset consistency validator | PASS |
| Starter Village roadmap validator | PASS |
| Starter Village execution ledger validator | PASS |
| Git diff whitespace check | PASS |

## Phase Scores

| Category | Score |
| --- | --- |
| Narrative score | 8.6/10 |
| Gameplay hook score | 8.6/10 |
| UX/readability score | 8.6/10 |
| Design score | 8.6/10 |
| Art direction score | 8.5/10 |
| World/layout score | 8.5/10 |
| NPC animation score | 8.5/10 |
| Technical stability score | 8.8/10 |
| Performance/build score | 8.7/10 |

## Council Finding

G-10 passes because First Light now behaves like a playable opening arc rather
than static lore. It gives the player a location, a first goal, a missing-line
mystery, tavern pressure, wharf confirmation, optional secrecy, a small
progression reward, and a named contact who pulls the player forward.

The next production need is G-10A: make the Tavern/Inn a deeper social gameplay
hub with rotating rumor content and quest-relevant whisper behavior.
