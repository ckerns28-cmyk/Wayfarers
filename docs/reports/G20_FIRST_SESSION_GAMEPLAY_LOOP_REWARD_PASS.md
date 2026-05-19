# G-20 First-Session Gameplay Loop and Reward Pass

Branch: `codex/g-20-first-session-gameplay-loop-reward-pass`

Human review required: no

Council verdict: `COUNCIL_PASS_READY_FOR_PR`

## Purpose

G-20 makes the opening fun, not just functional. The phase binds the source-driven Newport layout, the G-19 guidance layer, and the Whispers Before Dawn village-to-island quest into a first 20-30 minutes loop:

arrival -> orientation -> Counting House talk -> wharf investigation -> Tavern/Inn whisper -> route choice -> island road exploration -> hidden landing discovery -> return/report -> reward and dawn hook.

## Source Contract

Primary source:

- `wayfarer_godot_vertical_slice/data/quests/g20_first_session_gameplay_loop_reward_v1.json`

Source dependencies:

- `docs/design/NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.json`
- `wayfarer_godot_vertical_slice/data/world_layout/g19s_newport_runtime_reconstruction_v1.json`
- `wayfarer_godot_vertical_slice/data/ux/g19_player_guidance_map_journal_interaction_v1.json`
- `wayfarer_godot_vertical_slice/data/quests/whispers_before_dawn_village_to_island_v1.json`
- `wayfarer_godot_vertical_slice/data/quests/whispers_before_dawn_multipath_rumor_choice_v1.json`

The G-20 contract explicitly blocks a paper pass: it requires beat mapping, reward cadence, screenshots, runtime trace, no dead objective state, and a reason to continue.

## First-Session Loop

Target duration: first 20-30 minutes.

Runtime estimate: 28 minutes.

Loop beats:

- Arrive at Newport Harbor and receive a journal objective.
- Orient along the harborfront road toward the Counting House.
- Talk to Edrin Vale and learn the missing manifest line matters.
- Investigate wharf labor and connect the problem to the harbor economy.
- Hear the Third Toast at the Tavern/Inn and receive Resolve feedback.
- Choose a lead through wharf lanterns, commercial/rear routes, or trusted contacts.
- Unlock the island road from Newport's eastern edge.
- Follow the old road and signal clue to the hidden landing.
- Discover physical evidence and earn a second Resolve reward.
- Return/report through Annelise and Edrin, ending with the dawn signal hook.

## Reward Cadence

- Journal orientation: readable first objective and route.
- `Reward: Resolve +5 for following the tavern whisper`.
- `Named contact: Edrin Vale`.
- `Access: old road island lead`.
- `Reward: Resolve +8 for proving the island clue`.
- `Named contact: Annelise Crow`.
- Dawn hook: Edrin names the Governor's men and the first-light threat.

Runtime reward total: `13 Resolve`.

## Runtime Proof

Runtime hooks added:

- `FirstLightQuest.debug_first_session_gameplay_loop_reward_contract()`
- `Main.first_session_gameplay_loop_reward_contract()`
- `HUD.first_session_reward_loop_contract()`

Proof artifacts:

- `wayfarer_godot_vertical_slice/artifacts/review/g20_first_session_gameplay_loop/g20_first_session_screenshot_manifest.json`
- `wayfarer_godot_vertical_slice/artifacts/review/g20_first_session_gameplay_loop/g20_first_session_trace.json`
- `wayfarer_godot_vertical_slice/artifacts/review/g20_first_session_gameplay_loop/g20_first_session_playtest_log.md`

Canonical screenshots:

- `g20_01_arrival_goal.png`
- `g20_02_counting_house_first_talk.png`
- `g20_03_wharf_investigation_reward.png`
- `g20_04_tavern_whisper_social_hook.png`
- `g20_05_choice_branch_next_lead.png`
- `g20_06_island_exit_reward_hook.png`
- `g20_07_old_road_explore.png`
- `g20_08_hidden_landing_discovery.png`
- `g20_09_return_report_choice.png`
- `g20_10_final_reward_next_hook.png`
- `g20_11_debug_disabled_first_session.png`

## Acceptance

- `first_session_playable`: PASS
- `player_receives_feedback_and_reward`: PASS
- `player_has_reason_to_continue`: PASS
- `no_dead_objective_states`: PASS
- `gameplay_hook_score`: 8.7
- `reward_cadence_score`: 8.7
- `world_cohesion_score`: 8.6
- `player_orientation_score`: 8.7
- `quest_geography_integration_score`: 8.7
- `implementation_readiness_score`: 8.7

## Harsh-Critic Result

The pass does not claim OVI-1 completion. It passes because the first-session loop now has a source contract, a runtime simulation, visible reward proof, quest-geography continuity, and a concrete reason to keep playing. It would fail if the screenshots contradicted the report, if the player reached a dead objective state, if rewards were only hidden in code, or if the island discovery did not return to Newport with a meaningful hook.

Next phase: G-21 Opening Island Performance, Browser Build, and Regression Hardening.
