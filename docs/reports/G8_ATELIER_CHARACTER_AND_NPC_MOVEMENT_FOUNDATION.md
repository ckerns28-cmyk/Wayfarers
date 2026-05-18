# G-8 Atelier Character and NPC Movement Foundation

Phase status: `PASS`

Branch: `codex/g-8-character-motion-foundation`

Council verdict: `COUNCIL_PASS_READY_FOR_PR`

## Purpose

G-8 fixes the visible hover/glide risk in the starter village character layer.
No static portrait-like NPC may drift through normal play. The player now has
an explicit grounded motion contract, and the visible interactable NPC is
stationary until dedicated walk sheets can ship.

This is not SV-1 completion. G-8A next must expand the living NPC population
while preserving the no-hover/no-glide rule.

## Runtime Changes

- Added player foot-anchor, ground-shadow, idle/walk state, and animation
  cadence contract metadata.
- Converted Edrin Vale from a static `Sprite2D` visual to an
  `AnimatedSprite2D` using the accepted G-4.22R NPC atlas.
- Added Edrin's `motion_foundation_contract()` and `set_review_motion_state()`
  proof API.
- Disabled Edrin route walking in normal play until a dedicated NPC walk sheet
  exists; the accepted compromise is fewer moving NPCs rather than static
  cutout glide.
- Updated runtime and atelier validators to require the G-8 grounded-motion
  contract and reject primitive placeholder drawing.
- Added G-8 runtime screenshot capture with movement-state metadata.

## Screenshot Evidence

Runtime screenshot manifest:
`wayfarer_godot_vertical_slice/artifacts/review/g8_runtime_screenshots/g8_runtime_screenshot_manifest.json`

Council-inspected frames:

- `g8_01_wide_newport_normal_gameplay_view.png`: PASS for normal-play no-debug
  proof with grounded character layer.
- `g8_03_player_route_to_counting_house_walk_up.png`: PASS for player
  `walk_up` state at route scale.
- `g8_04_player_walk_down_grounded.png`: PASS for player feet/shadow grounding.
- `g8_08_npc_idle_and_stationary_walk_request_proof.png`: PASS for Edrin
  stationary-no-drift behavior when a walk request is applied.
- `g8_14_debug_overlays_disabled.png`: PASS for no route labels, debug boxes,
  or primitive motion placeholders.
- `g8_15_provenance_character_motion_contract.png`: PASS for manifest-backed
  atelier character provenance.

## Validation Results

| Check | Result |
| --- | --- |
| Godot import validation | PASS |
| Vertical slice validator | PASS |
| G-8 screenshot capture and PNG verification | PASS |
| Character motion foundation validator | PASS |
| G-4.22R runtime asset consistency validator | PASS |
| Runtime atelier asset consistency validator | PASS |
| Starter Village roadmap validator | PASS |
| Starter Village execution ledger validator | PASS |
| Git diff whitespace check | PASS |

## Phase Scores

| Category | Score |
| --- | --- |
| NPC motion/grounding score | 8.5/10 |
| Design score | 8.5/10 |
| Art direction score | 8.5/10 |
| World/layout score | 8.5/10 |
| UX/readability score | 8.5/10 |
| Technical stability score | 8.8/10 |
| Performance/build score | 8.7/10 |

## Council Finding

G-8 passes because normal play no longer asks a static NPC portrait to slide
around the village. Player motion has grounded directional walk/idle proof, and
Edrin has a grounded, manifest-backed `AnimatedSprite2D` foundation with route
walking disabled until real NPC walk frames exist.

The council does not certify SV-1. The town still needs a broader living NPC
cast, purposeful stations/routes, opening quest state, tavern whisper gameplay,
and first-session pacing proof.

G-8A next: add purposeful NPC roles, stations, routes or stationary work
behaviors, names/labels, dialogue seeds, quest relevance, and atelier
provenance without reintroducing hover/glide.
