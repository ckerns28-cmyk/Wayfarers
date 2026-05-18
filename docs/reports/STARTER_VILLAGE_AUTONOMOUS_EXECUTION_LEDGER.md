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
| SV-0 | Free Tooling Intake Production Stack Lock | `codex/sv0-free-tooling-stack` | #473 merged | PASS | `docs/reports/SV0_FREE_TOOLING_INTAKE_PRODUCTION_STACK_LOCK.md`, structured stack JSON, tooling roadmap, authoritative world-layout source, visual QA manifest, movement proof manifest, ground stack, SV-0 validator, and `docs/reports/SV0_FREE_TOOLING_AGENT_COUNCIL_REPORT.md`. |
| G-7 | Newport Living Origin Village Masterplan Lock | `codex/sv1-autonomous-roadmap` | #462 merged | PASS | `docs/reports/G7_NEWPORT_LIVING_ORIGIN_VILLAGE_MASTERPLAN_LOCK.md`, roadmap JSON, ledger JSON, G-7 council report, and G-7 validators. |
| G-7A | Street, Lot, and Ground Cohesion Reconstruction | `codex/g-7a-street-lot-ground-cohesion`; corrective subpass `codex/g-7a-tool-backed-layout-repair` | #463 merged; corrective PR pending | PASS with corrective subpass council-passing | `docs/reports/G7A_STREET_LOT_GROUND_COHESION_RECONSTRUCTION.md`, G-7A council report, runtime screenshot manifest, vertical-slice validator, world-cohesion validator, atelier runtime validator, plus `docs/reports/G7A_SV0_TOOL_BACKED_LAYOUT_REPAIR.md`, `docs/reports/G7A_SV0_TOOL_BACKED_LAYOUT_REPAIR_AGENT_COUNCIL_REPORT.md`, and `validate_starter_village_layout_source_usage.py`. |
| G-7B | Harbor, Wharf, and Commercial Spine Cohesion | `codex/g-7b-harbor-commercial-spine` | #464 merged | PASS | `docs/reports/G7B_HARBOR_WHARF_COMMERCIAL_SPINE_COHESION.md`, G-7B council report, runtime screenshot manifest, vertical-slice validator, world-cohesion validator, NPC route validator, and atelier runtime validator. |
| G-7C | Landmark and District Identity Pass | `codex/g-7c-landmark-district-identity` | #465 merged | PASS | `docs/reports/G7C_LANDMARK_DISTRICT_IDENTITY_PASS.md`, G-7C council report, runtime screenshot manifest, vertical-slice validator, world-cohesion validator, interaction UX validator, and atelier runtime validator. |
| G-8 | Atelier Character and NPC Movement Foundation | `codex/g-8-character-motion-foundation` | #466 merged | PASS | `docs/reports/G8_ATELIER_CHARACTER_AND_NPC_MOVEMENT_FOUNDATION.md`, G-8 council report, runtime screenshot manifest, vertical-slice validator, character motion validator, and atelier runtime validator. |
| G-8A | Living NPC Population Pass | `codex/g-8a-living-npc-population` | #467 merged | PASS | `docs/reports/G8A_LIVING_NPC_POPULATION_PASS.md`, G-8A council report, runtime screenshot manifest, vertical-slice validator, NPC population/route validator, character motion validator, and atelier runtime validator. |
| G-9 | Interaction UX and Diegetic Prompt Pass | `codex/g-9-interaction-ux-prompts` | #468 merged | PASS | `docs/reports/G9_INTERACTION_UX_DIEGETIC_PROMPT_PASS.md`, G-9 council report, runtime screenshot manifest, vertical-slice validator, interaction UX validator, and atelier runtime validator. |
| G-9A | Journal, Objective, and Quest State Foundation | `codex/g-9a-journal-objective-state` | #469 merged | PASS | `docs/reports/G9A_JOURNAL_OBJECTIVE_QUEST_STATE_FOUNDATION.md`, G-9A council report, runtime screenshot manifest, vertical-slice validator, opening quest validator, interaction UX validator, and atelier runtime validator. |
| G-10 | Opening Quest Arc: First Light / Whispers Before Dawn | `codex/g-10-opening-quest-arc` | #470 merged | PASS | `docs/reports/G10_OPENING_QUEST_ARC_FIRST_LIGHT_WHISPERS_BEFORE_DAWN.md`, G-10 council report, runtime screenshot manifest, vertical-slice validator, opening quest validator, interaction UX validator, and atelier runtime validator. |
| G-10A | Tavern Whisper System | `codex/g-10a-tavern-whisper-system` | #471 merged | PASS | `docs/reports/G10A_TAVERN_WHISPER_SYSTEM.md`, G-10A council report, runtime screenshot manifest, vertical-slice validator, tavern whisper validator, Newport visual-order validator, opening quest validator, interaction UX validator, and atelier runtime validator. |
| G-10B | Multi-Path Starter Choice Foundation | `codex/g-10b-multi-path-starter-choice` | pending current phase PR | PASS | `docs/reports/G10B_MULTI_PATH_STARTER_CHOICE_FOUNDATION.md`, G-10B council report, runtime screenshot manifest, vertical-slice validator, multi-path starter choice validator, opening quest validator, tavern whisper validator, Newport visual-order validator, interaction UX validator, and atelier runtime validator. |
| G-11 | Living Town Rhythm Pass | pending | pending | PENDING | Must add believable town rhythm, barks, pauses, and route behavior. |
| G-11A | Audio/Atmosphere Placeholder-Free Foundation | pending | pending | PENDING | Must add safe hooks or document non-blocking integration points. |
| G-12 | First-Session Fun, Pacing, and Readability Pass | pending | pending | PENDING | Must prove the first 15-20 minutes are readable, paced, and fun. |
| G-13 | Browser Build, Performance, and Regression Hardening | pending | pending | PENDING | Must harden import, vertical slice, screenshots, review build, input, performance, and assets. |
| G-14 | SV-1 Starter Village Playable Obsession Gate | pending | pending | PENDING | Must produce final SV-1 review package and stop for Chris. |

## Current Phase

Current phase after Chris screenshot QA and SV-0 merge: `G-7A-SV0 Tool-Backed
Layout Repair`.

G-10B adds a runtime-backed multi-path choice foundation for First Light:
counting-house, harbor-work, tavern-rumor, merchant-street, and optional
secret routes can now advance the opening mystery without a single railroaded
click path. However, screenshot evidence showed the process still allowed
patchwork layout, visual-order confusion, false stable reads, and mismatched
building scale to survive. SV-0 locked the free production stack; G-7A-SV0 now
applies that source-of-truth process to runtime lot assignments, building
scale, false tavern-stable reads, overlap/cutoff risks, and screenshot proof.

Chris screenshot QA also exposed that the prior process let route/building
order pass as long as proof screenshots existed. G-10A added a hard visual-order
gate: route corridors are drawn from an explicit contract and are validated
against runtime building visual bounds. G-10B extends the process so screenshots
can overrule written report claims; any visible phase-blocking contradiction
must force `COUNCIL_FAIL_NEEDS_CODE_FIX`.
