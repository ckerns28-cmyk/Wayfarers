# G-4.22R Pre-G-5 Roadmap Execution And Gate Reopen Report

- Previous reported status: G-5 readiness reached.
- Current status: G-5 readiness reopened as `UNPROVEN / COUNCIL_FAIL_NEEDS_CODE_FIX`.
- Reason 1: runtime screenshot evidence shows visual-standard regressions in the playable Newport hero slice.
- Reason 2: pre-G-5 roadmap execution proof was not visible enough phase-by-phase to justify a compressed G-5 readiness claim.
- Human review required: no.
- Action: Codex must audit, repair, validate, screenshot, council-review, and continue autonomously.

## Reopen Evidence

The previous G-4.22 council result is treated as a false-positive gate after new runtime visual evidence contradicted the pass. The external QA artifact supplied by Chris showed player/NPC/world sprites that did not meet the active atelier standard. Repo-local runtime artifacts also support reopening:

- `wayfarer_godot_vertical_slice/artifacts/review/g422_runtime_screenshots/g422_01_visual_gate_normal_hud.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g423b_runtime_screenshots/g423b_07_player_walkability_proof.png`

Observed failures:

- Central player/character styling read far below the surrounding atelier buildings and props.
- Simple beige/tan humanoid NPC placeholders were visible in normal runtime views.
- Some sign/marker/quest/world objects read as crude placeholder shapes.
- The runtime presentation mixed detailed Newport atelier environment work with non-atelier character/world sprites.
- The screenshot contradiction means the gate must fail even though prior validators and council text passed.

## Process Failure

The reopened gate also records a process issue: the pre-G-5 roadmap must be proven as a ledger of individual phases, not a compressed statement that later PRs merged. Each pre-G-5 roadmap item must show implementation evidence, screenshot evidence where applicable, validation evidence, Agent Council judgment, PR/merge evidence, and a current PASS status before the G-5 readiness package can be accepted.

## Remediation Direction

This branch repairs forward from `main` without rewriting history. The deterministic geometric G-4.22R scratch character pack created during remediation was rejected as below the atelier standard and is not approved. The active repair path uses a painterly, source-preserved character sheet, local transparent extraction, manifest-backed player/NPC atlases, Godot runtime integration, stronger validators, screenshot proof, and a roadmap execution ledger gate.

Deprecated final states are not used for this reopened gate. The only acceptable council outcomes are `COUNCIL_PASS_READY_FOR_PR`, `COUNCIL_FAIL_NEEDS_CODE_FIX`, or `BLOCKED_REQUIRES_HUMAN_ESCALATION`.
