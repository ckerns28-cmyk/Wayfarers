# Opening Village + Island Autonomous Execution Ledger

Milestone: `OVI-1 Opening Village + Island Production Playable Gate`

Starting main commit for OVI control-plane addendum:
`05453e9cc2241e3b1985774f2c97cf7c42abe217`

Structured ledger source:
`docs/reports/OPENING_VILLAGE_ISLAND_AUTONOMOUS_EXECUTION_LEDGER.json`

Roadmap source:
`docs/roadmaps/OPENING_VILLAGE_ISLAND_PRODUCTION_ROADMAP.md`

## Steering Addendum Result

G-14 is now an internal checkpoint inside the larger OVI-1 autonomous runway.

Human review required: no

Reason: G-14 is now an internal checkpoint inside the larger OVI-1 autonomous
runway.

Next phase: G-15 Opening Island Masterplan + World Topology

The next true Chris review milestone is `OVI-1 Opening Village + Island
Production Playable Gate`. Do not stop for Chris between G-14 and G-22 unless a
true hard blocker occurs.

## Status Taxonomy

- `PASS`
- `IN_PROGRESS`
- `PENDING`
- `FAIL_NEEDS_CODE_FIX`
- `BLOCKED_REQUIRES_HUMAN_ESCALATION`

Deprecated human-review final states are forbidden for ordinary G-14 through
G-21 phases.

Agent Council pass verdict for merge-ready phases: `COUNCIL_PASS_READY_FOR_PR`

## Ledger Summary

| Phase | Roadmap Item | Branch | PR | Current Status | Evidence |
| --- | --- | --- | --- | --- | --- |
| G-14 | Internal Starter Village Proof Gate | `codex/g-14-internal-starter-village-proof` | #480 merged | PASS | `docs/reports/G14_INTERNAL_STARTER_VILLAGE_PROOF_GATE.md`, structured proof JSON, G-14 Agent Council report, village screenshots, motion proof manifests, quest proof manifests, browser-review ZIPs, and validators. Human review required: no. |
| G-15 | Opening Island Masterplan + World Topology | `codex/g-15-opening-island-topology` | pending open PR | PASS | `wayfarer_godot_vertical_slice/data/world_layout/opening_island_world_topology_v1.json`, `docs/reports/G15_OPENING_ISLAND_MASTERPLAN_WORLD_TOPOLOGY.md`, and `wayfarer_godot_vertical_slice/data/visual_qa/g15_topology_screenshot_viewpoint_manifest.json` define the authored island structure, routes, loops, danger/safety gradient, quest destination, optional secret, return path, and future OVI-1 screenshot viewpoints. |
| G-15A | Village-to-Island Transition Pass | pending | pending | PENDING | Must make leaving Newport readable, natural, and mysterious. |
| G-15B | Island Terrain, Ground, and Route Cohesion | pending | pending | PENDING | Must remove patchwork terrain, disconnected paths, empty sprawl, and unreadable transitions. |
| G-16 | Island Landmark and Point-of-Interest Pass | pending | pending | PENDING | Must create memorable, quest-relevant island destinations and at least one optional discovery. |
| G-16A | Island Atelier Asset Family Pass | pending | pending | PENDING | Must make all visible island assets atelier-standard and provenance-traceable. |
| G-17 | Island NPC / Encounter / Ambient Life Foundation | pending | pending | PENDING | Must add purposeful, grounded, quest/world-relevant island life with movement proof where applicable. |
| G-18 | Opening Quest Extension: From Whispers to the Island | pending | pending | PENDING | Must make Whispers Before Dawn playable from village rumors to island clue and return/report hook. |
| G-18A | Multi-Path Rumor and Choice Foundation | pending | pending | PENDING | Must support counting-house, tavern, harbor, and optional island clue paths without broken branches. |
| G-19 | Player Guidance, Map, Journal, and Interaction Polish | pending | pending | PENDING | Must make first-session route/objective/interaction guidance readable without debug UI. |
| G-20 | First-Session Gameplay Loop and Reward Pass | pending | pending | PENDING | Must make the opening 20-30 minute loop fun, rewarded, readable, and compelling. |
| G-21 | Opening Island Performance, Browser Build, and Regression Hardening | pending | pending | PENDING | Must harden combined village/island review build, identity, proof regeneration, performance, and checks. |
| G-22 | OVI-1 Opening Village + Island Production Playable Gate | pending | pending | PENDING | Must generate the full OVI-1 review package from current main and then stop for Chris. |

## Required Per-Phase Report Fields

Every phase row must be upgraded from `PENDING` only when the implementation
report records phase ID, branch, commit, PR number, merge status, files changed,
screenshot paths, motion proof where applicable, quest proof where applicable,
validator results, design score, world/layout score, art direction score, NPC
motion score where applicable, quest/narrative score where applicable,
UX/readability score, technical stability score, atelier/provenance result,
North Star result, Agent Council verdict, and next phase.

## Final OVI-1 Review Package

When G-22 passes, this ledger must include an `ovi1_review_package` record with:

- current main commit
- clean worktree proof
- no open PR proof
- all completed phases and merged PRs
- all phase reports
- all screenshot manifests
- all motion proof artifacts
- all quest playthrough proof
- browser/review ZIP path
- validator summary
- village cohesion score
- island cohesion score
- village-to-island transition score
- NPC motion/grounding score
- opening quest gameplay score
- narrative hook score
- first-session fun score
- UX/readability score
- technical stability score
- atelier/provenance result
- Agent Council final verdict
- final recommendation
