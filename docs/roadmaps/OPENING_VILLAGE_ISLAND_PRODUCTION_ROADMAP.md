# Opening Village + Island Production Roadmap

Milestone: `OVI-1 Opening Village + Island Production Playable Gate`

Source authorization: Chris May 2026 live steering addendum: do not stop at
G-14; continue autonomously until the opening village and opening island region
are production-playable at the North Star standard.

Structured source:
`docs/roadmaps/OPENING_VILLAGE_ISLAND_PRODUCTION_ROADMAP.json`

Execution ledger:
`docs/reports/OPENING_VILLAGE_ISLAND_AUTONOMOUS_EXECUTION_LEDGER.md`

## Prime Directive

The next true Chris review milestone is not G-14 and not SV-1 by itself.
The active autonomous target is:

`OVI-1 Opening Village + Island Production Playable Gate`

Codex continues ordinary roadmap-bound autonomous production until OVI-1 is
complete, or until a true hard blocker occurs.

G-14 still happens, but it is now:

`G-14 Internal Starter Village Proof Gate`

Human review required: no

Reason: G-14 is now an internal checkpoint inside the larger OVI-1 autonomous
runway.

Next phase: G-15 Opening Island Masterplan + World Topology

If G-14 fails, Codex fixes it autonomously. If G-14 passes, Codex opens and
merges the PR when green and mergeable, syncs main, updates the ledger, and
continues immediately to G-15.

## North Star

Wayfarer must feel like a handcrafted fantasy/colonial harbor RPG with MMORPG
ambition. The opening should make a first-time player want to keep playing.
The world must feel authored, alive, mysterious, readable, and
production-intentional.

Production-playable never means merely functional. Each phase must be judged
against the pull and craft discipline of inspiration games such as Tibia and
Ragnarok Online: readable routes, memorable places, grounded NPC life, mystery,
reward, social texture, and a world that feels worth returning to.

OVI-1 passes only when the player can sit down, arrive in the Newport-inspired
village, feel tavern whispers and pre-Revolution tension, move through a
cohesive harbor town, follow a playable quest out into the island, discover a
meaningful clue, return or continue with momentum, and want to keep playing.

## Mandatory Production Roles

Every phase report must include:

- Scrum Master
- World-class Game Designer
- Game Programmer
- Art Director
- World/Layout Designer
- Narrative Designer
- Quest Designer
- Animation/NPC Behavior Director
- UX Designer
- QA Analyst
- Build/Release Engineer

Allowed final verdicts remain:

- `COUNCIL_PASS_READY_FOR_PR`
- `COUNCIL_FAIL_NEEDS_CODE_FIX`
- `BLOCKED_REQUIRES_HUMAN_ESCALATION`

Do not use `NEEDS_HUMAN_REVIEW`, `READY_FOR_HUMAN_VISUAL_REVIEW`,
`AWAITING_CHRIS_REVIEW`, or `TECHNICAL_PASS_ONLY` as final states for ordinary
G-14 through G-21 phases.

## Autonomous Production Loop

For every phase from G-14 through G-22:

1. Start from latest main and run branch/PR preflight.
2. Create a focused branch.
3. Implement the phase.
4. Validate.
5. Generate screenshot, motion, quest, and browser proof where applicable.
6. Run the Agent Council.
7. Fix if failed.
8. Commit, push, open PR.
9. Verify remote checks.
10. Merge if green, mergeable, council-passing, and no hard stop exists.
11. Sync main.
12. Update the ledger.
13. Continue to the next phase.

Do not stop for Chris between G-14 and G-22.

## Phase Sequence

| Phase | Title | Required Result |
| --- | --- | --- |
| G-14 | Internal Starter Village Proof Gate | Proves the village is cohesive, playable, quest-ready, UX-readable, and atelier/provenance compliant enough to support island production. |
| G-15 | Opening Island Masterplan + World Topology | Designs the island as an authored playable region with roads, coastline, trails, landmarks, quest routes, danger/safety gradient, loops, and camera viewpoints. |
| G-15A | Village-to-Island Transition Pass | Makes leaving the village intentional, readable, natural, and exciting. |
| G-15B | Island Terrain, Ground, and Route Cohesion | Replaces patchwork terrain with cohesive paths, coast, grass/stone/dirt logic, blocked/walkable reads, loops, and sightlines. |
| G-16 | Island Landmark and Point-of-Interest Pass | Adds memorable island destinations that support exploration and quest purpose. |
| G-16A | Island Atelier Asset Family Pass | Raises island assets to Newport atelier discipline with manifest/provenance/source proof. |
| G-17 | Island NPC / Encounter / Ambient Life Foundation | Makes the island feel alive with grounded, purposeful, quest-relevant NPCs or encounters. |
| G-18 | Opening Quest Extension: From Whispers to the Island | Extends Whispers Before Dawn from village rumors into island clue discovery, return/report, reward, and hook. |
| G-18A | Multi-Path Rumor and Choice Foundation | Keeps the opening from becoming a single railroaded path with counting-house, tavern, harbor, and optional island clue routes. |
| G-19R | Newport Scale + Street Blockout Source of Truth | Corrective layout-first gate with measured blockout, source JSON, districts, streets, lots, NPC routes, quest beats, cameras, and future governance. |
| G-19S | Newport Blockout-To-Godot Runtime Reconstruction | Implements the approved G-19R blockout into Godot without inventing a new layout. |
| G-19 | Player Guidance, Map, Journal, and Interaction Polish | Makes the first session readable without debug UI after G-19R/G-19S layout correction. |
| G-20 | First-Session Gameplay Loop and Reward Pass | Makes the opening fun: arrive, orient, talk, investigate, explore, discover, return/report, reward, and continue. |
| G-21 | Opening Island Performance, Browser Build, and Regression Hardening | Hardens the combined village/island browser review build, metadata, proof regeneration, performance, and regression gates. |
| G-22 | OVI-1 Opening Village + Island Production Playable Gate | The next true Chris review milestone: full review package from current main. |

## Acceptance Summary

G-14 acceptance:

- Village cohesion >= 8.5
- NPC motion/grounding >= 8.5
- Opening village quest clarity >= 8.5
- Tavern whisper hook >= 8.5
- UX/readability >= 8.5
- Technical stability PASS
- Atelier/provenance PASS
- Human review required: no
- Next phase: G-15 Opening Island Masterplan + World Topology

G-19R corrective acceptance:

- A measured town blockout exists as SVG, PNG, and JSON.
- Scale is derived from the current player/camera data.
- Street widths are defined in character widths.
- Districts, lots, NPC routes, quest beats, and camera viewpoints are planned before runtime placement.
- Future phases fail if major Newport layout edits bypass the source of truth.
- G-19S must implement the approved blockout rather than inventing a new layout.
- G-19S must pass `validate_g19s_newport_runtime_reconstruction.py`,
  `validate_newport_layout_source_alignment.py`, canonical G-19R screenshot
  capture, and Agent Council runtime review before guidance/quest polish resumes.

G-15 through G-21 acceptance:

- Island reads as one authored place.
- Player understands how to leave town and explore.
- Routes loop naturally and lead somewhere.
- No patchwork terrain or meaningless empty sprawl.
- Required POIs are memorable and quest/exploration relevant.
- Island assets are atelier-standard, provenance-traceable, and placeholder-free.
- Island NPCs or encounters have purpose, dialogue/barks/interaction, grounding,
  route or station, and world or quest relevance.
- Whispers Before Dawn is playable from arrival through island clue and return
  or continuing hook.
- At least two village paths can advance the opening thread.
- At least one optional clue changes or enriches the journal.
- The first 20-30 minutes are playable, rewarded, readable, and compelling.
- Browser/review artifact is stable, current, and regression-hardened.

G-22 / OVI-1 acceptance:

- Village cohesion >= 8.5
- Island cohesion >= 8.5
- Village-to-island transition >= 8.5
- Art direction >= 8.5
- World/layout believability >= 8.5
- NPC motion/grounding >= 8.5
- Opening quest gameplay >= 8.5
- Narrative hook >= 8.5
- UX/readability >= 8.5
- First-session fun >= 8.5
- Technical stability >= 8.5
- Atelier/provenance compliance PASS
- Browser/review readiness PASS
- North Star alignment PASS

When G-22 passes, stop for Chris with the full OVI-1 review package.

## Required OVI-1 Proof

Fresh final proof must be generated from current main.

Screenshot directory:
`wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/`

Required screenshots:

1. `01_village_wide_cohesion.png`
2. `02_player_arrival_harbor.png`
3. `03_counting_house_route.png`
4. `04_tavern_rumor_hub.png`
5. `05_commercial_avenue.png`
6. `06_harbor_wharf_work_area.png`
7. `07_village_exit_to_island.png`
8. `08_island_entry_transition.png`
9. `09_island_main_trail.png`
10. `10_island_landmark_signal_or_overlook.png`
11. `11_island_cove_or_hidden_landing.png`
12. `12_island_optional_discovery.png`
13. `13_npc_village_movement.png`
14. `14_npc_island_movement.png`
15. `15_quest_journal_village_step.png`
16. `16_quest_journal_island_step.png`
17. `17_return_to_town_or_next_hook.png`
18. `18_interaction_ux_proof.png`
19. `19_ysort_layering_proof.png`
20. `20_debug_overlays_disabled.png`
21. `21_browser_review_identity_proof.png`
22. `22_contact_sheet_player_npc_world_assets.png`

Screenshot manifest:
`wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/g22_ovi1_screenshot_manifest.json`

Motion proof:
`wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_motion_proof/`

Quest playthrough proof:
`wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_quest_playthrough/`

Required quest playthrough files:

- `quest_playthrough_log.md`
- `quest_playthrough_state_trace.json`
- `quest_playthrough_screenshot_manifest.json`

## OVI-1 Review Package

G-22 OVI-1 Opening Village + Island Production Playable Gate is the next true
Chris review milestone.

When G-22 passes, create:

- `docs/reports/G22_OVI1_OPENING_VILLAGE_ISLAND_REVIEW_PACKAGE.md`
- `docs/reports/G22_OVI1_OPENING_VILLAGE_ISLAND_REVIEW_PACKAGE.json`
- `docs/reports/G22_OVI1_AGENT_COUNCIL_REPORT.md`
- `docs/reports/OVI1_REVIEW_INDEX.md`
- `docs/reports/OVI1_REVIEW_INDEX.json`

The package must include current main commit, clean worktree proof, no open PR
proof, all phases completed, all phase PRs, all phase reports, screenshot
manifests, motion proof, quest playthrough proof, browser/review build
artifacts, validators, Agent Council reports, required scores, known caveats,
true blockers if any, and final recommendation.

## Hard Stops

Stop only for:

- OVI-1 Opening Village + Island Production Playable Gate completed
- GitHub authentication/permission failure
- unresolvable merge conflict
- unsafe/destructive operation risk
- asset licensing/provenance blocker
- tooling failure preventing validation/proof after serious debugging
- major creative fork requiring Chris decision
- budget/spending/tool-purchase decision

Do not stop for G-14 passing, bad screenshots, failed validators, poor island
cohesion, hovering NPCs, broken quest steps, ugly UX, missing proof, or failed
council review. Those are production failures to fix autonomously.
