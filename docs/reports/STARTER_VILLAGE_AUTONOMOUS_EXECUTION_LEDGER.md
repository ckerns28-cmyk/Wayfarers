# Starter Village Autonomous Execution Ledger

Milestone: `SV-1 INTERNAL STARTER VILLAGE PROOF GATE`

Starting main after G-6 merge: `a6ec338f795f7f61c9974af5a3338a37e165aa11`

PR #461 result: already merged when checked on 2026-05-18; its head
`9a46df19dca4e5e74403230aa779e32c60dff1ba` is contained in local main after
fast-forward to `a6ec338f795f7f61c9974af5a3338a37e165aa11`.

Autonomous merge-governance result: recurring per-PR Chris merge approval is no
longer a blocker for ordinary roadmap-bound autonomous PRs before OVI-1 when the
autonomous merge rule is satisfied.

Chris's May 2026 OVI-1 addendum supersedes the old SV-1 human-stop language.
G-14 is now an internal checkpoint inside the larger OVI-1 autonomous runway.
Human review required: no. Next phase: G-15 Opening Island Masterplan + World
Topology.

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
| G-7A | Street, Lot, and Ground Cohesion Reconstruction | `codex/g-7a-street-lot-ground-cohesion`; corrective subpass `codex/g-7a-tool-backed-layout-repair` | #463 merged; #474 merged | PASS | `docs/reports/G7A_STREET_LOT_GROUND_COHESION_RECONSTRUCTION.md`, G-7A council report, runtime screenshot manifest, vertical-slice validator, world-cohesion validator, atelier runtime validator, plus `docs/reports/G7A_SV0_TOOL_BACKED_LAYOUT_REPAIR.md`, `docs/reports/G7A_SV0_TOOL_BACKED_LAYOUT_REPAIR_AGENT_COUNCIL_REPORT.md`, and `validate_starter_village_layout_source_usage.py`. |
| G-7B | Harbor, Wharf, and Commercial Spine Cohesion | `codex/g-7b-harbor-commercial-spine` | #464 merged | PASS | `docs/reports/G7B_HARBOR_WHARF_COMMERCIAL_SPINE_COHESION.md`, G-7B council report, runtime screenshot manifest, vertical-slice validator, world-cohesion validator, NPC route validator, and atelier runtime validator. |
| G-7C | Landmark and District Identity Pass | `codex/g-7c-landmark-district-identity` | #465 merged | PASS | `docs/reports/G7C_LANDMARK_DISTRICT_IDENTITY_PASS.md`, G-7C council report, runtime screenshot manifest, vertical-slice validator, world-cohesion validator, interaction UX validator, and atelier runtime validator. |
| G-8 | Atelier Character and NPC Movement Foundation | `codex/g-8-character-motion-foundation` | #466 merged | PASS | `docs/reports/G8_ATELIER_CHARACTER_AND_NPC_MOVEMENT_FOUNDATION.md`, G-8 council report, runtime screenshot manifest, vertical-slice validator, character motion validator, and atelier runtime validator. |
| G-8A | Living NPC Population Pass | `codex/g-8a-living-npc-population` | #467 merged | PASS | `docs/reports/G8A_LIVING_NPC_POPULATION_PASS.md`, G-8A council report, runtime screenshot manifest, vertical-slice validator, NPC population/route validator, character motion validator, and atelier runtime validator. |
| G-9 | Interaction UX and Diegetic Prompt Pass | `codex/g-9-interaction-ux-prompts` | #468 merged | PASS | `docs/reports/G9_INTERACTION_UX_DIEGETIC_PROMPT_PASS.md`, G-9 council report, runtime screenshot manifest, vertical-slice validator, interaction UX validator, and atelier runtime validator. |
| G-9A | Journal, Objective, and Quest State Foundation | `codex/g-9a-journal-objective-state` | #469 merged | PASS | `docs/reports/G9A_JOURNAL_OBJECTIVE_QUEST_STATE_FOUNDATION.md`, G-9A council report, runtime screenshot manifest, vertical-slice validator, opening quest validator, interaction UX validator, and atelier runtime validator. |
| G-10 | Opening Quest Arc: First Light / Whispers Before Dawn | `codex/g-10-opening-quest-arc` | #470 merged | PASS | `docs/reports/G10_OPENING_QUEST_ARC_FIRST_LIGHT_WHISPERS_BEFORE_DAWN.md`, G-10 council report, runtime screenshot manifest, vertical-slice validator, opening quest validator, interaction UX validator, and atelier runtime validator. |
| G-10A | Tavern Whisper System | `codex/g-10a-tavern-whisper-system` | #471 merged | PASS | `docs/reports/G10A_TAVERN_WHISPER_SYSTEM.md`, G-10A council report, runtime screenshot manifest, vertical-slice validator, tavern whisper validator, Newport visual-order validator, opening quest validator, interaction UX validator, and atelier runtime validator. |
| G-10B | Multi-Path Starter Choice Foundation | `codex/g-10b-multi-path-starter-choice` | #472 merged | PASS | `docs/reports/G10B_MULTI_PATH_STARTER_CHOICE_FOUNDATION.md`, G-10B council report, runtime screenshot manifest, vertical-slice validator, multi-path starter choice validator, opening quest validator, tavern whisper validator, Newport visual-order validator, interaction UX validator, and atelier runtime validator. |
| G-11 | Living Town Rhythm Pass | `codex/g-11-living-town-rhythm-pass` | #475 merged | PASS | `docs/reports/G11_LIVING_TOWN_RHYTHM_PASS.md`, G-11 council report, runtime screenshot manifest, living town rhythm validator, NPC route validator, vertical-slice validator, and atelier runtime validator. |
| G-11A | Audio/Atmosphere Placeholder-Free Foundation | `codex/g-11a-audio-atmosphere-hooks` | #476 merged | PASS | `docs/reports/G11A_AUDIO_ATMOSPHERE_PLACEHOLDER_FREE_FOUNDATION.md`, G-11A council report, placeholder-free audio hook registry, hook-only runtime contract, audio atmosphere validator, vertical-slice validator, screenshot capture baseline, and atelier runtime validator. |
| G-12 | First-Session Fun, Pacing, and Readability Pass | `codex/g-12-first-session-playability` | #477 open | PASS | `docs/reports/G12_FIRST_SESSION_FUN_PACING_READABILITY_PASS.md`, `docs/reports/G12_FIRST_SESSION_AGENT_COUNCIL_REPORT.md`, G-12 runtime screenshot manifest, first-session playability validator, prompt/dialogue/bark overlap suppression, Game Studio playtest method, vertical-slice validator, opening quest validator, interaction UX validator, living town rhythm validator, and atelier runtime validator. |
| G-13 | Browser Build, Performance, and Regression Hardening | `codex/g-13-browser-build-hardening` | pending open PR | PASS | `docs/reports/G13_BROWSER_BUILD_PERFORMANCE_REGRESSION_HARDENING.md`, `docs/reports/G13_BROWSER_BUILD_AGENT_COUNCIL_REPORT.md`, fresh G-12 regression screenshot manifest, G-13 stable/versioned browser-review ZIPs, package root checks, vertical-slice validator, browser build hardening validator, first-session/quest/UX/rhythm/audio/layout/atelier validators, and Agent Council run-validators mode. |
| G-14 | SV-1 Internal Starter Village Proof Gate | pending | pending | PENDING | Must prove village cohesion, NPC motion, opening village quest clarity, tavern whisper hook, UX/readability, browser identity, and atelier/provenance; then merge and continue to G-15. |

## Current Phase

Current phase after G-13: `G-14 SV-1 Internal Starter Village Proof Gate`.

G-13 hardened the browser-review route after G-12. `BuildInfo.gd` now reports
`G-13`, the HUD metadata and vertical-slice validator enforce the active
browser-hardening identity, and `tools/package_itch_web.sh` fails if the review
phase, label, or source branch drift from the G-13 package contract. The web
package route produced both the stable upload ZIP and
`wayfarers-tale-godot-g-13-browser-build-performance-and-regression-hardening.zip`
with `index.html` at ZIP root and no `web_build/index.html` nesting. G-13 also
reran the G-12 recurring screenshot route as browser-regression proof and
received `COUNCIL_PASS_READY_FOR_PR` from the Agent Council. This is a
technical/build hardening pass, not an OVI-1 milestone review.

G-12 adds a runtime-backed first-session playability gate. The new capture
set proves harbor arrival, route readability, Tavern/Inn rumor interaction,
quest objective progress, reward/contact hook, debug-off normal play, and
camera focus safety. The validator now fails if dialogue and interaction
prompts overlap, if focused prompts/dialogue are cluttered by ambient barks,
or if required player-facing targets are clipped in proof screenshots.

G-11A adds a placeholder-free audio/atmosphere foundation without loading,
referencing, or bundling any audio assets. Harbor ambience, Tavern/Inn ambience,
surface footsteps, quest updates, and interaction feedback now have hook-only
runtime events and a data registry. Production playback remains disabled until
future audio assets have license, provenance, web-export validation, and
rollback documentation.

G-11 adds a runtime-backed living town rhythm layer: dock work, tavern social
pressure, merchant street behavior, civic notice activity, and rear-gate
suspicion now have authored rhythm contracts, focused ambient barks, facing
changes, pauses, and timestamped proof. It deliberately preserves the no-glide
rule: NPC route walking remains disabled until dedicated walk sheets exist.

G-10B added a runtime-backed multi-path choice foundation for First Light:
counting-house, harbor-work, tavern-rumor, merchant-street, and optional
secret routes can now advance the opening mystery without a single railroaded
click path. However, screenshot evidence showed the process still allowed
patchwork layout, visual-order confusion, false stable reads, and mismatched
building scale to survive. SV-0 locked the free production stack; G-7A-SV0
applied that source-of-truth process to runtime lot assignments, building
scale, false tavern-stable reads, overlap/cutoff risks, and screenshot proof.

Chris screenshot QA also exposed that the prior process let route/building
order pass as long as proof screenshots existed. G-10A added a hard visual-order
gate: route corridors are drawn from an explicit contract and are validated
against runtime building visual bounds. G-10B extends the process so screenshots
can overrule written report claims; any visible phase-blocking contradiction
must force `COUNCIL_FAIL_NEEDS_CODE_FIX`.
