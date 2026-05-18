# Wayfarer Codex Guidance

This repository uses Codex as a production collaborator, not as an automatic approver. Every future pass should preserve the creative direction, technical gates, and review discipline below.

## Durable Rules

- Always run branch/PR preflight before implementation: confirm current branch, latest `origin/main`, clean working tree, remote permission health, and open PR state.
- Do not touch files outside this repository.
- Do not merge anything unless Chris explicitly asks for a merge, except for
  roadmap-bound autonomous phases covered by the current autonomous merge
  authorization below.
- Preserve the G-4.21B/G-4.22A runtime screenshot automation and keep clean no-HUD/no-debug capture available.
- Preserve the Newport atelier asset pipeline, provenance validation, and asset quarantine rules.
- Validators passing does not equal design approval.
- Preserve the pre-G-5 roadmap execution ledger and fail G-5 readiness if any required row is missing or not `PASS`.
- SV-0 locks the production tooling stack for Starter Village work. Future
  phases must use the locked SV-0 tooling stack where applicable, or explain
  the exception in the Agent Council report and fail if the exception creates
  an unvalidated one-off system.
- Until the SV-1 Starter Village Playable Obsession Gate, follow
  `docs/PRE_G5_AUTONOMOUS_PRODUCTION_PROTOCOL.md`: the Wayfarer Agent Council
  is the default QA and acceptance authority for ordinary roadmap-bound
  autonomous phases.
- Visual, gameplay, world-design, UX, and art-direction passes require screenshot evidence inspected by the Agent Council, or a true `BLOCKED_REQUIRES_HUMAN_ESCALATION` blocker.
- Movement phases require movement proof: timestamped frame sequences, GIF,
  or video showing idle/walk/facing changes, grounded anchors, and no
  static-sprite glide.
- Screenshot evidence can overrule a written report. If captured proof shows route/building confusion, tavern/commercial/civic ordering problems, phase-blocking ground patchwork, hovering or sliding NPCs, debug artifacts, unclear objective state, or non-atelier runtime sprites, the council must fail the phase and Codex must repair the branch.
- Do not use `NEEDS_HUMAN_REVIEW`, `READY_FOR_HUMAN_VISUAL_REVIEW`, `AWAITING_CHRIS_REVIEW`, or `TECHNICAL_PASS_ONLY` as final states for ordinary pre-G-5 phases.
- PR summaries must separate technical validation from design acceptance.
- All visible normal-play hero-slice sprites must be atelier-standard and provenance-traceable unless hidden behind debug-only behavior.
- Player and NPC sprites must always be atelier-standard; crude humanoid placeholders, beige/tan stand-ins, primitive sign/marker shapes, debug boxes, and untracked runtime sprites may not appear in normal screenshots.
- Do not solve layout problems with random prop scatter.
- Do not hide ground or street problems with clutter.
- Buildings must sit on believable streets, lots, yards, docks, alleys, or civic spaces.
- Newport city passes must prove street grammar, ground cohesion, player/NPC walkability, district logic, and visual cohesion.

## Newport Review Bar

Newport is the first major proof that Wayfarer can support a believable handcrafted fantasy/colonial harbor RPG settlement. Newport work must be reviewed as a town, not as an asset board.

Newport review must ask:

- Does the settlement read as a harbor city?
- Is there a waterfront avenue parallel to the harbor?
- Are roads visibly running uphill from harbor into town?
- Is there a back street behind the first road?
- Are civic, market, tavern, harbor, service, and residential districts legible?
- Are buildings grounded on coherent lots rather than old prototype art?
- Is the ground/street material language unified?
- Can players and NPCs plausibly move through the space?
- Do props support function instead of hiding layout problems?
- Does the pass approach the Newport 8.5+/10 bar for its phase?

## Agent Council

Use `tools/wayfarer_agent_council.py`, `docs/PRE_G5_AUTONOMOUS_PRODUCTION_PROTOCOL.md`, and the docs under `docs/agents`, `docs/factories`, `docs/checklists`, and `docs/templates` to structure production review. For ordinary roadmap-bound autonomous work before SV-1, the council produces the final authority verdict: `COUNCIL_PASS_READY_FOR_PR`, `COUNCIL_FAIL_NEEDS_CODE_FIX`, or `BLOCKED_REQUIRES_HUMAN_ESCALATION`. It must never say "Approved by Chris." The council tool itself does not merge; Codex may merge an ordinary autonomous PR after the required merge gates below pass.

## Autonomous Merge Authorization

Chris's May 2026 Starter Village directive pre-authorizes Codex to merge
ordinary roadmap-bound autonomous PRs until the `SV-1 STARTER VILLAGE PLAYABLE
OBSESSION GATE` when all of the following are true:

- branch and PR preflight is current,
- required local validators pass,
- runtime screenshots/proof pass where applicable,
- Agent Council final verdict is `COUNCIL_PASS_READY_FOR_PR`,
- the PR is green,
- the PR is mergeable,
- no hard stop condition exists.

Explicit Chris approval is still required only for destructive operations,
unsafe file operations, budget/tool purchase decisions, unresolvable GitHub
authentication or permission problems, major creative forks with multiple valid
directions, asset licensing/provenance blockers, and the formal SV-1 milestone
review.
