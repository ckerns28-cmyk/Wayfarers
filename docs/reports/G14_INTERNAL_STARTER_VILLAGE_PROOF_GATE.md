# G-14 Internal Starter Village Proof Gate

Date: 2026-05-18

Branch: `codex/g-14-internal-starter-village-proof`

Starting main commit: `2d9364cc9261914012ce9eea68e47ad7442ef0c7`

Human review required: no

Reason: G-14 is now an internal checkpoint inside the larger OVI-1 autonomous
runway.

Next phase: G-15 Opening Island Masterplan + World Topology

## Scope

G-14 proves the Newport-inspired starter village is strong enough to support
the wider opening island experience. It does not claim OVI-1 completion and it
does not stop for Chris.

## Required Outcomes

| Outcome | Result | Evidence |
| --- | --- | --- |
| Village cohesion verified | PASS | G-12 recurring screenshot set, G-13 browser regression report, Newport world/layout validators, and council score. |
| NPC motion verified | PASS | G-8 character motion foundation, G-8A population proof, G-11 rhythm proof, and no-static-glide policy. |
| Opening tavern/counter-house/harbor quest verified | PASS | First Light / Whispers Before Dawn reports, quest validators, G-10/G-10A/G-10B/G-12 proof, and journal/objective proof. |
| Interaction UX verified | PASS | Interaction UX validator, G-9/G-12 screenshot proof, and compact prompt/journal behavior. |
| Browser/review identity verified | PASS | G-13 review build identity, web ZIP package, and browser build hardening validator. |
| Atelier/provenance compliance verified | PASS | Runtime atelier asset consistency validator and Newport provenance validators. |

## Scores

| Discipline | Score |
| --- | --- |
| Town cohesion | 8.6 |
| NPC motion/grounding | 8.6 |
| Opening village quest clarity | 8.7 |
| Tavern whisper hook | 8.7 |
| UX/readability | 8.7 |
| Technical stability | PASS / 8.8 |
| Atelier/provenance | PASS |

## Proof Paths

Screenshot manifest:
`wayfarer_godot_vertical_slice/artifacts/review/g12_runtime_screenshots/g12_runtime_screenshot_manifest.json`

Representative screenshots:

- `wayfarer_godot_vertical_slice/artifacts/review/g12_runtime_screenshots/g12_01_wide_newport_normal_gameplay_view.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g12_runtime_screenshots/g12_02_player_arrival_at_harbor.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g12_runtime_screenshots/g12_03_player_on_route_to_counting_house.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g12_runtime_screenshots/g12_04_player_near_tavern_inn.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g12_runtime_screenshots/g12_09_player_interacting_with_counting_house_clerk.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g12_runtime_screenshots/g12_10_player_interacting_at_tavern_rumor_location.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g12_runtime_screenshots/g12_11_quest_prompt_journal_objective_proof.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g12_runtime_screenshots/g12_14_debug_overlays_disabled.png`

Motion proof:

- `wayfarer_godot_vertical_slice/artifacts/review/g8_runtime_screenshots/g8_runtime_screenshot_manifest.json`
- `wayfarer_godot_vertical_slice/artifacts/review/g8a_runtime_screenshots/g8a_runtime_screenshot_manifest.json`
- `wayfarer_godot_vertical_slice/artifacts/review/g11_runtime_screenshots/g11_runtime_screenshot_manifest.json`

Quest proof:

- `wayfarer_godot_vertical_slice/artifacts/review/g10_runtime_screenshots/g10_runtime_screenshot_manifest.json`
- `wayfarer_godot_vertical_slice/artifacts/review/g10a_runtime_screenshots/g10a_runtime_screenshot_manifest.json`
- `wayfarer_godot_vertical_slice/artifacts/review/g10b_runtime_screenshots/g10b_runtime_screenshot_manifest.json`
- `wayfarer_godot_vertical_slice/artifacts/review/g12_runtime_screenshots/g12_runtime_screenshot_manifest.json`

Browser/review package:

- `wayfarer_godot_vertical_slice/artifacts/wayfarers-tale-godot-web.zip`
- `wayfarer_godot_vertical_slice/artifacts/wayfarers-tale-godot-g-13-browser-build-performance-and-regression-hardening.zip`

## Validation

Required local validation passed for the G-14 proof gate:

- OVI-1 roadmap and ledger validators
- Starter Village roadmap and execution ledger validators
- First-session playability validator
- G-13 browser build hardening validator
- Opening quest arc validator
- Tavern whisper system validator
- Interaction UX validator
- Character motion foundation validator
- NPC population and routes validator
- Runtime atelier asset consistency validator
- Starter Village layout source usage validator
- Newport visual ordering validator
- Godot import and vertical slice validator through Agent Council run
- `git diff --check`
- `git diff --cached --check`

## Caveats

The opening island region is not yet production-playable. That is not a G-14
blocker because G-14 is now an internal village checkpoint. Island topology,
transition, terrain cohesion, landmarks, island assets, island NPCs, and the
village-to-island quest extension are owned by G-15 through G-18A and must be
fixed autonomously if they fail.

## Final Result

Agent Council verdict: `COUNCIL_PASS_READY_FOR_PR`

G-14 status: PASS

Human review required: no

Reason: G-14 is now an internal checkpoint inside the larger OVI-1 autonomous
runway.

Next phase: G-15 Opening Island Masterplan + World Topology
