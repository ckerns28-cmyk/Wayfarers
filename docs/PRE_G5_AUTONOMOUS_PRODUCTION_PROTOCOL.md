# Pre-G-5 Autonomous Production Protocol

This protocol governed ordinary Wayfarer roadmap work until the G-5 readiness
gate. After G-6, Chris extended the same autonomous production model through
the `SV-1 STARTER VILLAGE PLAYABLE OBSESSION GATE`. It changes the default
acceptance authority from Chris to the Wayfarer Agent Council for ordinary
roadmap-bound autonomous production phases before SV-1.

## Operating Model

The default loop is:

1. Codex builds the phase.
2. Required technical validators pass.
3. Required screenshots or review captures are generated.
4. The Wayfarer Agent Council inspects the evidence against the North Star and
   the phase's 8.5+/10 visual/world/layout bar.
5. Codex fixes failures on the same branch until the council reaches a final
   authority verdict.
6. Passing phases produce a PR-ready result, a green/mergeable PR is merged by
   Codex under the autonomous authorization, main is synced, and the next
   roadmap phase is selected.

Chris is not the default QA gate for ordinary pre-SV-1 roadmap work. A normal
visual QA pass is not a valid escalation reason by itself.

The roadmap must be executed as visible phase evidence, not as a compressed
summary. Each pre-SV-1 item needs implementation evidence, screenshot evidence
where applicable, validation evidence, Agent Council judgment, PR/merge
evidence, and an authoritative row in the active execution ledger before its
milestone gate can pass.

## Authority

The Agent Council is the default QA and acceptance gate for ordinary pre-SV-1
roadmap work. The council verdict is authoritative for ordinary phases once it
has reviewed:

- branch and PR preflight,
- relevant diffs and roadmap scope,
- validation commands and results,
- screenshot evidence for visual/layout/player-facing work,
- North Star fit,
- design, art direction, world/layout, gameplay/readability, technical
  stability, QA regression, and build/release risk.

Validators passing remains required, but a technical pass is not enough. The
council must explicitly accept or reject the player-facing result.

## Autonomous Merge Rule

For roadmap-bound autonomous phases before the SV-1 gate, Codex is
pre-authorized to merge the PR when:

- branch/PR preflight is current,
- the required validators pass,
- screenshot/runtime proof exists and has been inspected when applicable,
- the Agent Council final authority verdict is `COUNCIL_PASS_READY_FOR_PR`,
- the PR is green,
- the PR is mergeable,
- no hard stop condition exists.

Chris merge approval remains required only for destructive operations, unsafe
file operations, budget/tool purchase decisions, unresolvable GitHub
authentication or permission problems, major creative forks with multiple valid
directions, asset licensing/provenance blockers, and the formal SV-1 review.
Do not leave ordinary green council-passing autonomous PRs open solely for
per-PR human merge approval.

## Pre-G-5 Roadmap Ledger Gate

`wayfarer_godot_vertical_slice/tools/validate_pre_g5_roadmap_ledger.py` is part
of the readiness gate. It must fail G-5 readiness if any required pre-G-5
roadmap phase is missing from the ledger, has a status other than `PASS`, lacks
PR/commit evidence, lacks screenshot evidence for visual/player-facing work,
lacks Agent Council art/world/player-facing judgment, lacks provenance evidence
for asset/player/NPC/world work, or cannot trace visible runtime sprites through
the approved asset/provenance manifests.

A merged PR is evidence, not acceptance by itself. A later gate cannot silently
substitute for the proof package of an earlier roadmap phase.

## Atelier-Only Playable Hero-Slice Rule

All visible playable hero-slice world sprites must meet the active atelier
standard unless explicitly hidden behind debug-only behavior.

This includes:

- player,
- NPCs,
- buildings,
- props,
- signs,
- street objects,
- harbor objects,
- market objects,
- roadside objects,
- quest/world markers,
- interaction markers,
- character-like objects,
- any visible normal-play runtime sprite.

Hard requirements:

- Player sprites must always be atelier-standard.
- NPC sprites must always be atelier-standard.
- No hand-drawn placeholder characters are allowed in normal play.
- No beige/tan humanoid placeholders are allowed in normal play.
- No crude debug boxes, circles, or simple sign markers are allowed in normal
  play.
- No unknown or untracked runtime sprite may appear in the playable hero slice.
- No red/yellow/unknown-provenance sprite may be promoted into the playable
  hero slice.
- If a placeholder is required for debugging, it must be hidden behind a debug
  flag and absent from normal screenshots.

If a validator cannot prove a visible world sprite is approved and
provenance-classified, the gate fails.

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

- formal SV-1 milestone review,
- major creative fork with multiple valid directions,
- legal/licensing/provenance blocker,
- GitHub permission/authentication blocker,
- unsafe or destructive operation risk,
- unresolvable merge conflict,
- roadmap contradiction that cannot be resolved from existing docs,
- tooling or platform failure that prevents required validation or screenshots.

## Deprecated Statuses

These are deprecated as final states for ordinary pre-SV-1 work:

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

Screenshots are allowed to overrule a written report. If the captured game view
contradicts the claimed pass -- for example roads visually run under major
buildings, the tavern/counting-house/commercial order is confusing, ground
materials read as disconnected patches, NPCs hover or glide, objective guidance
is unclear, debug artifacts are visible, or normal-play sprites fail atelier
provenance -- the council must return `COUNCIL_FAIL_NEEDS_CODE_FIX` and the
branch must be repaired before PR readiness.

Every visual/player-facing phase before SV-1 must include a short screenshot
contradiction review in its council report:

- what the screenshots prove,
- what visible concerns remain,
- whether those concerns are blockers for the current phase,
- which next roadmap phase owns any non-blocking concern.

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
- NPC/animation score where applicable,
- narrative score where applicable,
- UX/readability score,
- technical stability score,
- performance/build score,
- QA regression result,
- build/release result,
- final recommended next phase.

For pre-G-5 readiness and visual/player-facing gates, every final council report
must also include:

- Roadmap Execution Ledger Result,
- Visible Runtime Asset Consistency Audit,
- Player Asset Audit,
- NPC Asset Audit,
- Marker/Sign/Quest Object Audit,
- Screenshot Inspection Result,
- North Star Result,
- 8.5+/10 Visual Bar Result.

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
