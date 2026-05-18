# Starter Village Playable Obsession Roadmap

Milestone: `SV-1 STARTER VILLAGE PLAYABLE OBSESSION GATE`

Starting main after G-6 merge: `a6ec338f795f7f61c9974af5a3338a37e165aa11`

This roadmap supersedes the old post-G-6 gap. The next stop is not another
planning endpoint; it is a playable Newport-inspired origin village that makes
a first-time player understand where they are, find the harbor/counting
house/tavern route, hear rumors, meet believable NPCs, advance an opening
quest, and want to keep playing.

## North Star

Wayfarer is a handcrafted fantasy/colonial harbor RPG with MMORPG ambition.
Newport must read as a believable 1700s-inspired harbor starting town, not a
prop board. The player should feel:

- I have arrived somewhere real.
- I know where I am.
- I know what I can do next.
- I am curious about the whispers.
- The tavern matters.
- The harbor matters.
- The town has secrets.
- The NPCs belong here.
- I want to keep playing.

## Current Baseline

Latest screenshot evidence after G-6 shows strong asset quality but failing
playable-village cohesion:

- town cohesion is approximately 2/10,
- buildings, roads, props, open spaces, and districts do not yet feel like one
  authored place,
- ground and road overlays still read as disconnected patches,
- the player path and village identity are not yet compelling,
- NPCs are visually improved but can read as hovering/gliding if static sprites
  move without grounded motion,
- the opening quest direction exists but does not yet deliver tavern whispers,
  harbor rumors, or pre-Revolution pressure as gameplay.

This is a council failure signal, not a human-review blocker.

## Autonomous Production Loop

For each phase:

1. Sync latest main and run branch/PR preflight.
2. Create a branch from latest main.
3. Implement the phase.
4. Run required validators.
5. Generate screenshots/proof where applicable.
6. Inspect evidence internally.
7. Run the Wayfarer Agent Council.
8. Fix failures on the same branch until the council passes.
9. Commit, push, open PR, verify remote checks.
10. Merge automatically if green, mergeable, council-passing, and no hard stop
    condition exists.
11. Sync main, update the ledger, and continue.

Ordinary roadmap-bound autonomous PRs before SV-1 are pre-authorized to merge
when the autonomous merge rule in `AGENTS.md` and
`docs/PRE_G5_AUTONOMOUS_PRODUCTION_PROTOCOL.md` is satisfied.

SV-0 now precedes renewed layout work. The Starter Village Tooling Stack locks
the source-of-truth map schema, runtime movement proof, screenshot visual
regression warnings, dialogue/quest authoring approach, asset cleanup workflow,
and ground/material cohesion rules before G-7/G-7A continues.

## Phase Sequence

| Phase | Title | Required Result |
| --- | --- | --- |
| SV-0 | Free Tooling Intake Production Stack Lock | Locks the free, safe production stack, authoritative world-layout source, visual QA warnings, movement proof, quest/dialogue authoring, asset cleanup, and ground-cohesion workflows. |
| G-7 | Newport Living Origin Village Masterplan Lock | Defines the authored town grammar, districts, first route, opening quest locations, and NPC work/life routes. |
| G-7A | Street, Lot, and Ground Cohesion Reconstruction | Rebuilds Newport into one coherent physical town with connected streets, real lots, unified materials, and no debug-like patchwork. |
| G-7B | Harbor, Wharf, and Commercial Spine Cohesion | Makes the harbor the economic engine with purposeful work zones, connected commerce, and readable wharf movement. |
| G-7C | Landmark and District Identity Pass | Makes Tavern/Inn, Counting House, commercial row, harbor work, rear service lane, residential edge, and notice-board civic point memorable. |
| G-8 | Atelier Character and NPC Movement Foundation | Eliminates hover/glide motion with grounded idle/walk/facing state foundations. |
| G-8A | Living NPC Population Pass | Adds purposeful NPC roles, stations/routes, names/labels, dialogue seeds, and atelier/provenance compliance. |
| G-9 | Interaction UX and Diegetic Prompt Pass | Replaces debug-like prompts/markers with tasteful guidance and readable interactables. |
| G-9A | Journal, Objective, and Quest State Foundation | Adds quest state, objective completion, feedback, and session persistence for the opening loop. |
| G-10 | Opening Quest Arc: First Light / Whispers Before Dawn | Makes the first 10-15 minutes playable around landfall, counting-house ledger trouble, tavern whispers, and a continuing hook. |
| G-10A | Tavern Whisper System | Makes the Tavern/Inn a gameplay social hub with rumor dialogue and ambient whisper lines. |
| G-10B | Multi-Path Starter Choice Foundation | Supports harbor work, tavern rumor, counting-house/clerk, merchant/street, and optional secret approaches. |
| G-11 | Living Town Rhythm Pass | Adds idle/walk loops, ambient barks, dock work, tavern/social behavior, merchant/street rhythm, and meaningful pauses. |
| G-11A | Audio/Atmosphere Placeholder-Free Foundation | Adds safe atmosphere hooks or documents future hook points without unsafe placeholder audio. |
| G-12 | First-Session Fun, Pacing, and Readability Pass | Playtests the first 15-20 minutes for clarity, pacing, curiosity, prompts, NPC usefulness, and no dead objective states. |
| G-13 | Browser Build, Performance, and Regression Hardening | Hardens Godot import, vertical slice, screenshots, review build, input, performance, assets, and route stability. |
| G-14 | SV-1 Starter Village Playable Obsession Gate | Produces the final review package and stops for Chris. |

Current execution status after G-10B and Chris screenshot QA: the next pass is
SV-0, not more placement work. First Light has a playable opening arc, a
runtime-backed Tavern/Inn rumor system, and a multi-path starter choice
foundation, but screenshot evidence shows the review process still lets
patchwork layout, mismatched buildings, false stable reads, and overlapping
visual order escape. SV-0 locks the tooling and QA process before the next
G-7/G-7A tool-backed layout repair continues.

G-10A added a standing visual-order review gate after screenshot QA caught
road/building order problems around the Tavern/Inn and commercial row. G-10B
extends that process: screenshots can overrule written report claims when they
show phase-blocking route/building confusion, debug artifacts, NPC glide,
unclear objectives, non-atelier sprites, or current-phase ground patchwork.

## G-7 Masterplan Contract

G-7 defines Newport as an authored settlement before G-7A changes the physical
map. The locked town plan must include:

- district grammar for harborfront, tavern, counting house, commercial, civic,
  residential, service, rear-street, and wharf zones,
- player arrival path from landfall to counting house to Tavern/Inn,
- harborfront road parallel to the water,
- roads visibly running uphill from harbor into town,
- a back street behind the first waterfront road,
- alleys, docks, wharf paths, and uphill connectors,
- landmarks and first/second/third read order,
- opening quest beats and where they happen,
- NPC home/work/walk logic,
- a building-purpose ledger so every building exists for a reason,
- explicit prohibition on random prop scatter as a layout fix.

## World-Class Starter Village Standard

Within 10 seconds the player understands where they are and what the first goal
is. Within 60 seconds the player can move naturally and identify the harbor,
tavern, counting-house path, and living NPC activity. Within 3 minutes the
player can complete or advance a meaningful objective. Within 10 minutes the
player has heard a rumor, met at least two memorable NPC roles, and has a
reason to care. Within 15-20 minutes the player has completed a satisfying loop
of exploration, dialogue, quest progress, reward, and mystery.

## Recurring Screenshot Set

Visual/world/player/NPC/quest UX phases must preserve or produce:

1. wide Newport normal gameplay view,
2. player arrival at harbor,
3. player on route to counting house,
4. player near Tavern/Inn,
5. player on commercial avenue,
6. player at dock/wharf work area,
7. player near NPC movement path,
8. NPC idle and walking proof,
9. player interacting with counting house/clerk,
10. player interacting at tavern/rumor location,
11. quest prompt/journal/objective proof,
12. signs/markers/interaction UX proof,
13. y-sort/layering proof near buildings/props,
14. debug overlays disabled proof,
15. contact sheet/provenance proof for new assets.

Animation/NPC phases must also produce a frame sequence, animated capture, GIF,
or timestamped screenshot series proving motion state changes.

## Council Roles

Every phase report must include Scrum Master, Game Designer, World/Layout
Designer, Art Director, Animation/NPC Behavior Director, Narrative Designer, UX
Designer, Game Programmer, QA Analyst, and Build/Release Engineer review.

Allowed final verdicts:

- `COUNCIL_PASS_READY_FOR_PR`
- `COUNCIL_FAIL_NEEDS_CODE_FIX`
- `BLOCKED_REQUIRES_HUMAN_ESCALATION`

Deprecated final states remain forbidden:

- `NEEDS_HUMAN_REVIEW`
- `READY_FOR_HUMAN_VISUAL_REVIEW`
- `AWAITING_CHRIS_REVIEW`
- `VISUAL_REVIEW_REQUIRED`
- `TECHNICAL_PASS_ONLY`

## Hard Stops

Stop only for SV-1 completion, GitHub permission/auth failure, unresolvable
merge conflict, unsafe/destructive operation risk, asset licensing/provenance
blocker, tooling failure that prevents required proof after serious debugging,
major creative fork with multiple valid roadmap-valid directions, or
budget/spending/tool-purchase decision.
