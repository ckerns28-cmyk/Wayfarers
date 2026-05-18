# Starter Village Autonomous Execution Ledger

Milestone: `SV-1 STARTER VILLAGE PLAYABLE OBSESSION GATE`

Starting main after G-6 merge: `a6ec338f795f7f61c9974af5a3338a37e165aa11`

PR #461 result: already merged when checked on 2026-05-18; its head
`9a46df19dca4e5e74403230aa779e32c60dff1ba` is contained in local main after
fast-forward to `a6ec338f795f7f61c9974af5a3338a37e165aa11`.

Autonomous merge-governance result: recurring per-PR Chris merge approval is no
longer a blocker for ordinary roadmap-bound autonomous PRs before SV-1 when the
autonomous merge rule is satisfied.

Structured ledger source:
`docs/reports/STARTER_VILLAGE_AUTONOMOUS_EXECUTION_LEDGER.json`

## Status Taxonomy

- `PASS`
- `IN_PROGRESS`
- `PENDING`
- `FAIL_NEEDS_CODE_FIX`
- `BLOCKED_REQUIRES_HUMAN_ESCALATION`

Deprecated final states are forbidden.

## Ledger Summary

| Phase | Roadmap Item | Branch | PR | Current Status | Evidence |
| --- | --- | --- | --- | --- | --- |
| G-7 | Newport Living Origin Village Masterplan Lock | `codex/sv1-autonomous-roadmap` | #462 merged | PASS | `docs/reports/G7_NEWPORT_LIVING_ORIGIN_VILLAGE_MASTERPLAN_LOCK.md`, roadmap JSON, ledger JSON, G-7 council report, and G-7 validators. |
| G-7A | Street, Lot, and Ground Cohesion Reconstruction | `codex/g-7a-street-lot-ground-cohesion` | #463 merged | PASS | `docs/reports/G7A_STREET_LOT_GROUND_COHESION_RECONSTRUCTION.md`, G-7A council report, runtime screenshot manifest, vertical-slice validator, world-cohesion validator, and atelier runtime validator. |
| G-7B | Harbor, Wharf, and Commercial Spine Cohesion | `codex/g-7b-harbor-commercial-spine` | #464 merged | PASS | `docs/reports/G7B_HARBOR_WHARF_COMMERCIAL_SPINE_COHESION.md`, G-7B council report, runtime screenshot manifest, vertical-slice validator, world-cohesion validator, NPC route validator, and atelier runtime validator. |
| G-7C | Landmark and District Identity Pass | `codex/g-7c-landmark-district-identity` | #465 merged | PASS | `docs/reports/G7C_LANDMARK_DISTRICT_IDENTITY_PASS.md`, G-7C council report, runtime screenshot manifest, vertical-slice validator, world-cohesion validator, interaction UX validator, and atelier runtime validator. |
| G-8 | Atelier Character and NPC Movement Foundation | `codex/g-8-character-motion-foundation` | #466 merged | PASS | `docs/reports/G8_ATELIER_CHARACTER_AND_NPC_MOVEMENT_FOUNDATION.md`, G-8 council report, runtime screenshot manifest, vertical-slice validator, character motion validator, and atelier runtime validator. |
| G-8A | Living NPC Population Pass | `codex/g-8a-living-npc-population` | #467 merged | PASS | `docs/reports/G8A_LIVING_NPC_POPULATION_PASS.md`, G-8A council report, runtime screenshot manifest, vertical-slice validator, NPC population/route validator, character motion validator, and atelier runtime validator. |
| G-9 | Interaction UX and Diegetic Prompt Pass | `codex/g-9-interaction-ux-prompts` | pending current phase PR | PASS | `docs/reports/G9_INTERACTION_UX_DIEGETIC_PROMPT_PASS.md`, G-9 council report, runtime screenshot manifest, vertical-slice validator, interaction UX validator, and atelier runtime validator. |
| G-9A | Journal, Objective, and Quest State Foundation | pending | pending | PENDING | Must add real quest state, journal/objective feedback, and progression update. |
| G-10 | Opening Quest Arc: First Light / Whispers Before Dawn | pending | pending | PENDING | Must make the opening quest playable for 10-15 meaningful minutes. |
| G-10A | Tavern Whisper System | pending | pending | PENDING | Must make Tavern/Inn a social gameplay hub with rumor content. |
| G-10B | Multi-Path Starter Choice Foundation | pending | pending | PENDING | Must support at least two NPC advancement paths and optional clue discovery. |
| G-11 | Living Town Rhythm Pass | pending | pending | PENDING | Must add believable town rhythm, barks, pauses, and route behavior. |
| G-11A | Audio/Atmosphere Placeholder-Free Foundation | pending | pending | PENDING | Must add safe hooks or document non-blocking integration points. |
| G-12 | First-Session Fun, Pacing, and Readability Pass | pending | pending | PENDING | Must prove the first 15-20 minutes are readable, paced, and fun. |
| G-13 | Browser Build, Performance, and Regression Hardening | pending | pending | PENDING | Must harden import, vertical slice, screenshots, review build, input, performance, and assets. |
| G-14 | SV-1 Starter Village Playable Obsession Gate | pending | pending | PENDING | Must produce final SV-1 review package and stop for Chris. |

## Current Phase

Current phase after G-9: `G-9A Journal, Objective, and Quest State Foundation`.

G-9 replaces debug-like in-world prompt copy with compact
`E: Action - Name` prompts, tightens prompt presentation, points the HUD first
objective from the Counting House to the tavern whisper, and records runtime
screenshot proof for route, dialogue, objective-update, and debug-off states.
G-9A must now turn that guidance into real quest state, objective completion,
journal feedback, session persistence, and a reward/progression beat.
