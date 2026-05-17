# Wayfarer Codex Guidance

This repository uses Codex as a production collaborator, not as an automatic approver. Every future pass should preserve the creative direction, technical gates, and review discipline below.

## Durable Rules

- Always run branch/PR preflight before implementation: confirm current branch, latest `origin/main`, clean working tree, remote permission health, and open PR state.
- Do not touch files outside this repository.
- Do not merge anything unless Chris explicitly asks for a merge.
- Preserve the G-4.21B/G-4.22A runtime screenshot automation and keep clean no-HUD/no-debug capture available.
- Preserve the Newport atelier asset pipeline, provenance validation, and asset quarantine rules.
- Validators passing does not equal design approval.
- Visual, gameplay, world-design, UX, and art-direction passes require screenshots or explicit `NEEDS_HUMAN_REVIEW`.
- PR summaries must separate technical validation from design acceptance.
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

Use `tools/wayfarer_agent_council.py` and the docs under `docs/agents`, `docs/factories`, `docs/checklists`, and `docs/templates` to structure production review. The council produces recommendations for Chris only. It must never say "Approved by Chris" and must never auto-merge.
