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
true hard blocker occurs. After the May 19, 2026 human screenshot override, do
not move from G-22 into an outward field-loop phase until OVI-2 repairs Newport
as an origin-village immersion gate.

Production-playable never means merely functional. Each phase is judged against
authored world pull, readable routes, grounded NPC life, mystery, reward, social
texture, atelier-standard craft, and the inspiration bar set by games such as
Tibia and Ragnarok Online.

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
| G-15 | Opening Island Masterplan + World Topology | `codex/g-15-opening-island-topology` | #481 merged | PASS | `wayfarer_godot_vertical_slice/data/world_layout/opening_island_world_topology_v1.json`, `docs/reports/G15_OPENING_ISLAND_MASTERPLAN_WORLD_TOPOLOGY.md`, and `wayfarer_godot_vertical_slice/data/visual_qa/g15_topology_screenshot_viewpoint_manifest.json` define the authored island structure, routes, loops, danger/safety gradient, quest destination, optional secret, return path, and future OVI-1 screenshot viewpoints. |
| G-15A | Village-to-Island Transition Pass | `codex/g-15a-village-island-transition` | #482 merged | PASS | `wayfarer_godot_vertical_slice/data/world_layout/village_to_island_transition_v1.json`, `docs/reports/G15A_VILLAGE_TO_ISLAND_TRANSITION_PASS.md`, and `wayfarer_godot_vertical_slice/artifacts/review/g15a_runtime_screenshots/g15a_runtime_screenshot_manifest.json` prove the village exit, island entry threshold, first mystery beyond town, and debug-overlays-disabled transition proof. |
| G-15B | Island Terrain, Ground, and Route Cohesion | `codex/g-15b-island-world-cohesion` | #483 merged | PASS | `wayfarer_godot_vertical_slice/data/world_layout/island_world_cohesion_v1.json`, `docs/reports/G15B_ISLAND_TERRAIN_GROUND_ROUTE_COHESION.md`, and `wayfarer_godot_vertical_slice/artifacts/review/g15b_runtime_screenshots/g15b_runtime_screenshot_manifest.json` prove No patchwork terrain, Routes lead somewhere, looped return paths, shoreline separation, blocked/walkable space, and clean no-HUD/no-debug proof with ambient bark text suppressed. |
| G-16 | Island Landmark and Point-of-Interest Pass | `codex/g-16-island-poi-landmarks` | #484 merged | PASS | `wayfarer_godot_vertical_slice/data/world_layout/island_poi_landmarks_v1.json`, `docs/reports/G16_ISLAND_LANDMARK_POI_PASS.md`, and `wayfarer_godot_vertical_slice/artifacts/review/g16_runtime_screenshots/g16_runtime_screenshot_manifest.json` prove the signal overlook, old road marker, cove hidden landing, wooded grove, service edge, quest clue site, optional secret location, return landmark, and no-HUD/no-debug POI proof. |
| G-16A | Island Atelier Asset Family Pass | `codex/g-16a-island-atelier-asset-family` | #485 merged | PASS | `wayfarer_godot_vertical_slice/data/world_layout/island_atelier_asset_family_v1.json`, `docs/reports/G16A_ISLAND_ATELIER_ASSET_FAMILY_PASS.md`, and `wayfarer_godot_vertical_slice/artifacts/review/g16a_runtime_screenshots/g16a_runtime_screenshot_manifest.json` prove No placeholders, Atelier compliance PASS, manifest/provenance/source proof, no crude markers, and Newport-cohesive island asset families. |
| G-17 | Island NPC / Encounter / Ambient Life Foundation | `codex/g-17-island-npc-encounter-foundation` | #486 merged | PASS | `wayfarer_godot_vertical_slice/data/world_layout/island_npc_encounter_foundation_v1.json`, `docs/reports/G17_ISLAND_NPC_ENCOUNTER_FOUNDATION.md`, `wayfarer_godot_vertical_slice/artifacts/review/g17_runtime_screenshots/g17_runtime_screenshot_manifest.json`, and `wayfarer_godot_vertical_slice/artifacts/review/g17_motion_proof/g17_island_npc_motion_trace.json` prove purposeful island NPCs, grounded/no-glide motion, quest/world relevance, and atelier-standard NPC assets. |
| G-18 | Opening Quest Extension: From Whispers to the Island | `codex/g-18-opening-quest-village-to-island` | #487 merged | PASS | `docs/reports/G18_OPENING_QUEST_VILLAGE_TO_ISLAND.md`, `wayfarer_godot_vertical_slice/artifacts/review/g18_runtime_screenshots/g18_runtime_screenshot_manifest.json`, and `wayfarer_godot_vertical_slice/artifacts/review/g18_quest_playthrough/quest_playthrough_state_trace.json` prove Whispers Before Dawn is playable from Newport rumors through island evidence, optional clue, return/report, reward, and next hook. |
| G-18A | Multi-Path Rumor and Choice Foundation | `codex/g-18a-multipath-rumor-choice-foundation` | #488 merged | PASS | `docs/reports/G18A_MULTIPATH_RUMOR_CHOICE_FOUNDATION.md`, `wayfarer_godot_vertical_slice/artifacts/review/g18a_runtime_screenshots/g18a_runtime_screenshot_manifest.json`, and `wayfarer_godot_vertical_slice/artifacts/review/g18a_quest_branch_proof/multipath_branch_trace.json` prove counting-house, tavern, dockworker/harbor, and optional island clue paths without broken branches. |
| G-19R | Newport Scale + Street Blockout Source of Truth | `codex/g-19r-newport-scale-street-blockout-source-of-truth` | #489 merged; #495 corrective merge | PASS | `docs/design/NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.json`, measured SVG/PNG blockout, scale metrics, district/street/lot/NPC/quest/camera plans, source governance, and G-19R validators. Supplemental G-19R PR #495 records Chris screenshot critique fails the current G-19 direction and adds Newport harbor reconstruction guardrails proving district structure, avenue widths, wharf dimensions, building/person scale, dockworker landing stations, and roof/body station repair. |
| G-19S | Newport Blockout-To-Godot Runtime Reconstruction | `codex/g-19s-newport-blockout-to-godot-runtime-reconstruction` | #490 merged | PASS | `wayfarer_godot_vertical_slice/data/world_layout/g19s_newport_runtime_reconstruction_v1.json`, runtime streets/lots/wharf/NPC stations derived from G-19R, `docs/reports/G19S_NEWPORT_BLOCKOUT_TO_GODOT_RUNTIME_RECONSTRUCTION.md`, and `wayfarer_godot_vertical_slice/artifacts/review/g19s_runtime_screenshots/g19s_runtime_screenshot_manifest.json`. |
| G-19 | Player Guidance, Map, Journal, and Interaction Polish | `codex/g-19-player-guidance-map-journal-interaction-polish` | #491 merged | PASS | `wayfarer_godot_vertical_slice/data/ux/g19_player_guidance_map_journal_interaction_v1.json`, HUD route/location guidance, NPC-priority interaction prompts, `docs/reports/G19_PLAYER_GUIDANCE_MAP_JOURNAL_INTERACTION_POLISH.md`, and `wayfarer_godot_vertical_slice/artifacts/review/g19_player_guidance_screenshots/g19_player_guidance_screenshot_manifest.json` prove readable first-session guidance without debug UI. |
| G-20 | First-Session Gameplay Loop and Reward Pass | `codex/g-20-first-session-gameplay-loop-reward-pass` | #492 merged | PASS | `wayfarer_godot_vertical_slice/data/quests/g20_first_session_gameplay_loop_reward_v1.json`, `FirstLightQuest.debug_first_session_gameplay_loop_reward_contract()`, HUD reward feedback, refreshed G-12/G-18 regression proof, `docs/reports/G20_FIRST_SESSION_GAMEPLAY_LOOP_REWARD_PASS.md`, `docs/reports/G20_WAYFARER_AGENT_COUNCIL_TOOL_RUN.md`, and `wayfarer_godot_vertical_slice/artifacts/review/g20_first_session_gameplay_loop/g20_first_session_screenshot_manifest.json` prove a 28-minute first-session loop with 13 Resolve, named contacts, island evidence, return/report, and a dawn reason to continue. |
| G-21 | Opening Island Performance, Browser Build, and Regression Hardening | `codex/g-21-opening-island-performance-browser-build-regression-hardening` | #493 merged | PASS | G-21 updates review build identity to `G-21`, hardens the package script and validator, generates stable/versioned review ZIPs with root `index.html`, captures browser canvas proof with zero warning/error console entries, records `g21_browser_build_hardening_manifest.json`, merged at `5e29b0be37245bdc8c3e2c38018f492aa6adf222`, and handed off to G-22 OVI-1. |
| G-22 | OVI-1 Opening Village + Island Production Playable Gate | `codex/g-22-ovi1-opening-village-island-production-playable-gate` | #494 open | PASS | Full OVI-1 review package created: `docs/reports/G22_OVI1_OPENING_VILLAGE_ISLAND_REVIEW_PACKAGE.md`, `wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/g22_ovi1_screenshot_manifest.json`, `wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_motion_proof/g22_ovi1_motion_proof_manifest.json`, `wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_quest_playthrough/quest_playthrough_state_trace.json`, browser ZIP proof, validators, and Agent Council verdict `COUNCIL_PASS_READY_FOR_PR`. Stop for Chris with PR #494. |
| OVI-2 | Newport Origin Village Immersion & City-Planning Gate | `codex/ovi-2-newport-origin-immersion-gate` | pending PR | PASS | Human screenshot override gate: `docs/reports/OVI2_NEWPORT_ORIGIN_IMMERSION_CITY_PLANNING_GATE.md`, `docs/reports/OVI2_NEWPORT_ORIGIN_IMMERSION_AGENT_COUNCIL_REPORT.md`, `wayfarer_godot_vertical_slice/data/world_layout/ovi2_newport_origin_immersion_city_plan_v1.json`, `wayfarer_godot_vertical_slice/artifacts/review/ovi2_newport_origin_immersion/ovi2_newport_origin_immersion_screenshot_manifest.json`, and the OVI-2 screenshot package prove Newport origin-village immersion/city-planning repair. Do not proceed to an outward field-loop phase. |

## G-19R Source-Of-Truth Gate

The G-19R source-of-truth gate blocks additional Newport runtime placement until the measured blockout, scale metrics, district plan, street hierarchy, lot plan, NPC route plan, quest beat map, camera viewpoints, manifest, validators, and Agent Council design review pass.

Future Newport runtime reconstruction must update or validate against `docs/design/NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.json` and the mirrored planning artifacts under `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/`.

## G-19S Runtime Reconstruction Gate

G-19S consumes the approved G-19R source-of-truth blockout and rebuilds Newport runtime placement from it. Runtime reconstruction must keep `runtime_layout_matches_G19R_source_of_truth` and `no_new_layout_invented_in_Godot` true, preserve measured street widths, use G-19R lots/frontages for major building placement, keep NPCs stationed until grounded walk animation exists, and provide canonical G-19R screenshot proof with HUD/debug overlays disabled.

## OVI-2 Newport Origin Immersion Gate

OVI-2 is the human screenshot override gate that corrects a false sense of
readiness after OVI-1/G-19R validators passed. It is not an outward gameplay
expansion and it is not a cosmetic polish pass.

Required OVI-2 proof:

- `docs/reports/OVI2_NEWPORT_ORIGIN_IMMERSION_CITY_PLANNING_GATE.md`
- `docs/reports/OVI2_NEWPORT_ORIGIN_IMMERSION_AGENT_COUNCIL_REPORT.md`
- `wayfarer_godot_vertical_slice/data/world_layout/ovi2_newport_origin_immersion_city_plan_v1.json`
- `wayfarer_godot_vertical_slice/artifacts/review/ovi2_newport_origin_immersion/ovi2_newport_origin_immersion_screenshot_manifest.json`
- `wayfarer_godot_vertical_slice/artifacts/review/ovi2_newport_origin_immersion/ovi2_01_player_spawn_first_impression_hud.png`
- `wayfarer_godot_vertical_slice/artifacts/review/ovi2_newport_origin_immersion/ovi2_02_player_spawn_first_impression_no_hud.png`
- `wayfarer_godot_vertical_slice/artifacts/review/ovi2_newport_origin_immersion/ovi2_03_harborfront_avenue.png`
- `wayfarer_godot_vertical_slice/artifacts/review/ovi2_newport_origin_immersion/ovi2_04_tavern_inn_district.png`
- `wayfarer_godot_vertical_slice/artifacts/review/ovi2_newport_origin_immersion/ovi2_05_counting_house_civic_district.png`
- `wayfarer_godot_vertical_slice/artifacts/review/ovi2_newport_origin_immersion/ovi2_06_shopfront_commercial_street.png`
- `wayfarer_godot_vertical_slice/artifacts/review/ovi2_newport_origin_immersion/ovi2_07_wharf_dock_service_district.png`
- `wayfarer_godot_vertical_slice/artifacts/review/ovi2_newport_origin_immersion/ovi2_08_wide_town_composition.png`
- `wayfarer_godot_vertical_slice/artifacts/review/ovi2_newport_origin_immersion/ovi2_09_movement_route_through_town.png`
- `wayfarer_godot_vertical_slice/artifacts/review/ovi2_newport_origin_immersion/ovi2_10_before_after_reference_current_failure.png`

OVI-2 current status: PASS. The branch preserves G-19R/G-19S movement and lot
source contracts while replacing slab-like runtime surfaces with segmented
streets, parcel frontages, civic terrace, rear lanes, wharf work aprons, and
purpose-bound atelier district props.

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

## G-22 OVI-1 Review Package Record

- current main commit: `5e29b0be37245bdc8c3e2c38018f492aa6adf222`
- OVI-1 PR: #494 (`https://github.com/ckerns28-cmyk/Wayfarers/pull/494`)
- clean worktree proof: Preflight before G-22 branch: clean worktree at 5e29b0be37245bdc8c3e2c38018f492aa6adf222.
- no open PR proof: Preflight before G-22 branch: gh pr list --state open returned [].
- screenshot manifest: `wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/g22_ovi1_screenshot_manifest.json`
- motion proof: `wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_motion_proof/g22_ovi1_motion_proof_manifest.json`
- quest playthrough: `wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_quest_playthrough/quest_playthrough_state_trace.json`
- browser review ZIP: `wayfarer_godot_vertical_slice/artifacts/wayfarers-tale-godot-web.zip`
- agent council final verdict: `COUNCIL_PASS_READY_FOR_PR`
