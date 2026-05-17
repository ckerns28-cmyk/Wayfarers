# Pre-G-5 Autonomous Production Protocol

This protocol governs ordinary Wayfarer roadmap work until the G-5 readiness
gate. It changes the default acceptance authority from Chris to the Wayfarer
Agent Council for pre-G-5 production phases.

## Operating Model

The default loop is:

1. Codex builds the phase.
2. Required technical validators pass.
3. Required screenshots or review captures are generated.
4. The Wayfarer Agent Council inspects the evidence against the North Star and
   the phase's 8.5+/10 visual/world/layout bar.
5. Codex fixes failures on the same branch until the council reaches a final
   authority verdict.
6. Passing phases produce a PR-ready result and the next roadmap phase is
   selected.

Chris is not the default QA gate for ordinary pre-G-5 work. A normal visual QA
pass is not a valid escalation reason by itself.

## Authority

The Agent Council is the default QA and acceptance gate for pre-G-5 work. The
council verdict is authoritative for ordinary phases once it has reviewed:

- branch and PR preflight,
- relevant diffs and roadmap scope,
- validation commands and results,
- screenshot evidence for visual/layout/player-facing work,
- North Star fit,
- design, art direction, world/layout, gameplay/readability, technical
  stability, QA regression, and build/release risk.

Validators passing remains required, but a technical pass is not enough. The
council must explicitly accept or reject the player-facing result.

## Required Status Taxonomy

Use exactly one final authority verdict:

- `COUNCIL_PASS_READY_FOR_PR`
- `COUNCIL_FAIL_NEEDS_CODE_FIX`
- `BLOCKED_REQUIRES_HUMAN_ESCALATION`

`COUNCIL_PASS_READY_FOR_PR` means validators passed, screenshot evidence was
generated and inspected when relevant, the work clears the phase bar, and any
remaining caveats are roadmap items rather than blockers.

`COUNCIL_FAIL_NEEDS_CODE_FIX` means the work is not acceptable yet. Codex must
repair the branch, regenerate evidence, rerun validators, and rerun council
review before moving on.

`BLOCKED_REQUIRES_HUMAN_ESCALATION` is reserved for true blockers only:

- G-5 readiness gate,
- major creative fork with multiple valid directions,
- legal/licensing/provenance blocker,
- GitHub permission/authentication blocker,
- unsafe or destructive operation risk,
- unresolvable merge conflict,
- roadmap contradiction that cannot be resolved from existing docs,
- tooling or platform failure that prevents required validation or screenshots.

## Deprecated Statuses

These are deprecated as final states for ordinary pre-G-5 work:

- `NEEDS_HUMAN_REVIEW`
- `READY_FOR_HUMAN_VISUAL_REVIEW`
- `AWAITING_CHRIS_REVIEW`
- `TECHNICAL_PASS_ONLY`

They may appear in historical reports, but new reports must not use them as the
final state for ordinary phases.

## Screenshot Requirement

Screenshot evidence is mandatory for visual, layout, art-direction, UX,
gameplay-readability, camera, sprite, map, and player-facing changes. The
council must inspect the screenshots directly. Artifact existence alone is not
acceptance.

Clean no-HUD/no-debug capture must remain available. Existing G-4.21B/G-4.22A
automation and Newport screenshot wrappers must be preserved unless a later
phase deliberately replaces them with an equal or stronger capture gate.

## Council Report Contract

Every final council report must include:

- final authority verdict,
- phase ID,
- branch,
- commit,
- PR number if available,
- screenshot paths,
- validation commands and results,
- design score,
- art direction score,
- world/layout score,
- gameplay/readability score,
- technical stability score,
- QA regression result,
- build/release result,
- final recommended next phase.

For visual/world/layout phases, the report must explicitly answer:

- Does this meet the 8.5+/10 pre-G-5 visual/world bar?
- Does this advance Wayfarer toward the North Star?
- Is human visual review truly required, or can the council accept this?
- If human review is required, what exact blocker justifies escalation?

## Phase Continuity

Do not start a new roadmap phase while the current phase is ambiguous,
technically-only, or waiting on ordinary human visual review. Failed phases stay
on the same branch until repaired. Passing phases can proceed to PR readiness
and then next-phase selection. The system should continue phase-to-phase until
the G-5 gate.
