# G-10A Tavern Whisper System

Phase status: `PASS`

Branch: `codex/g-10a-tavern-whisper-system`

Council verdict: `COUNCIL_PASS_READY_FOR_PR`

## Purpose

G-10A makes the Tavern/Inn a rumor gameplay hub rather than a decorative stop
on the opening quest route. The Tavern/Inn now has structured whisper data,
quest-relevant rumor interactions, rotating ambient barks, and runtime
contracts that tie Bess, Silas, Nora, and Jonah back to harbor commerce,
missing-ledger pressure, and quiet pre-Revolution tension.

This pass deepens the tavern social center. It does not claim the full G-10B
multi-path starter-choice foundation is complete.

## Runtime Systems

- Added `TavernWhisperSystem.gd` as the runtime rumor/ambient bark source.
- Added `tavern_whispers.json` with Third Toast, rear-gate, notice-board, and
  dock-lantern rumor interactions.
- Wired `FirstLightQuest.gd` so Bess and Silas responses come from the tavern
  whisper system.
- Added `Main.starter_village_tavern_whisper_contract()` so validation and
  screenshot manifests can prove the Tavern/Inn rumor hub at runtime.
- Added G-10A checks to the vertical-slice validator, Agent Council, and
  dedicated tavern whisper validator.
- Added a Newport visual-order gate after screenshot QA showed that route
  corridors and building order around the Tavern/Inn/commercial row could still
  pass as "proof exists" while looking wrong.

## Rumor Content

| Source | Gameplay Purpose |
| --- | --- |
| Bess Armitage | Names the Third Toast and opens the trust/wharf/rear-gate mystery. |
| Silas Crowe | Proves the rear service gate as an optional secret path. |
| Nora Vale | Connects civic notice-board rumors back to tavern trust language. |
| Jonah Reed | Connects tavern shutter behavior to wharf lantern signals. |
| Ambient barks | Rotate small rumors about Customs, cargo, coin, bells, and silence. |

## Visual Order QA Repair

Chris screenshot QA caught a production failure around route/building order:
the tavern and nearby buildings could look like they were sitting in road
overlays rather than on authored lots. This pass now treats that as a council
failure mode, not a cosmetic note.

New hard gate: Council must fail when route corridors render beneath tavern,
commercial, civic, or market building bodies in normal play. The street drawing
now uses `starter_village_route_order_specs()` as its visual-order source, and
the vertical slice validator checks those route segments against actual runtime
building visual bounds.

Required review points now include the tavern-to-clerk street gap,
commercial-block road break, counting-house approach, market connector gaps,
y-sort/layering proof, and debug-off normal play.

## Screenshot Evidence

Runtime screenshot manifest:
`wayfarer_godot_vertical_slice/artifacts/review/g10a_runtime_screenshots/g10a_runtime_screenshot_manifest.json`

Council-inspected frames:

- `g10a_04_player_near_tavern_inn.png`: PASS for Tavern/Inn as visible social
  landmark.
- `g10a_08_npc_idle_and_walking_proof.png`: PASS for Bess stationed at the
  tavern threshold without NPC glide.
- `g10a_10_player_interacting_at_tavern_rumor_location.png`: PASS for Bess and
  the Third Toast rumor line.
- `g10a_12_signs_markers_interaction_ux_proof.png`: PASS for Silas and the
  optional rear-gate secret.
- `g10a_14_debug_overlays_disabled.png`: PASS for normal play with no debug
  markers.

## Validation Results

| Check | Result |
| --- | --- |
| Godot import validation | PASS |
| Vertical slice validator | PASS |
| G-10A screenshot capture and PNG verification | PASS |
| Tavern whisper system validator | PASS |
| Newport visual ordering validator | PASS |
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

G-10A passes only after the Tavern/Inn rumor system and the stricter visual
order review both pass. The next production need is G-10B: support the opening
mystery through multiple advancement paths instead of only proving the tavern
hub.
