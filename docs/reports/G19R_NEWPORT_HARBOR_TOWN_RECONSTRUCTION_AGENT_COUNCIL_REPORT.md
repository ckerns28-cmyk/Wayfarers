# G-19R Newport Harbor Town Reconstruction PASS Wayfarer Agent Council Report

TECHNICAL PASS DOES NOT EQUAL DESIGN PASS.

For ordinary roadmap-bound work before OVI-1, this report is the council authority verdict after validators and screenshot review. This tool never merges, never impersonates Chris, and never converts technical validation alone into creative approval.

## Summary

- Generated: 2026-05-19 19:45:05 UTC
- Repo root: `C:\Users\Chris\Documents\New project`
- Phase ID: G-19R Newport Harbor Town Reconstruction PASS
- Branch: `codex/g-19-player-guidance-journal-polish`
- Commit: `1d93fe18faecacab2d708915622896366299dcbd`
- origin/main: `bb769e7b25a15c10cc4c79e312f7faca4adbe358`
- Current branch PR: #495 G-19R Newport reconstruction PASS - https://github.com/ckerns28-cmyk/Wayfarers/pull/495
- Target PR check: #495 G-19R Newport reconstruction PASS (OPEN, draft) - https://github.com/ckerns28-cmyk/Wayfarers/pull/495
- PR number if available: #495
- Final Authority Verdict: COUNCIL_PASS_READY_FOR_PR
- Final recommended next phase: Continue OVI roadmap from latest main; first-session bridge standard is spawn -> orient -> receive objective -> move through village -> reach landmark/NPC -> journal updates -> next breadcrumb appears.
- Human escalation required: NO
- Escalation blocker: None.

## Final Authority Verdict

Final Authority Verdict: `COUNCIL_PASS_READY_FOR_PR`

| Field | Result |
| --- | --- |
| Phase ID | G-19R Newport Harbor Town Reconstruction PASS |
| Branch | codex/g-19-player-guidance-journal-polish |
| Commit | 1d93fe18faecacab2d708915622896366299dcbd |
| PR number if available | #495 |
| Screenshot review | inspected |
| Design score | 8.6/10 |
| Art direction score | 8.6/10 |
| World/layout score | 8.6/10 |
| Gameplay/readability score | 8.5/10 |
| Technical stability score | 8.6/10 |
| QA regression result | PASS: required local validators rerun on merged G-19R branch; first-session loop passes on latest main baseline. |
| Build/release result | PASS_PENDING_REMOTE_PR_CHECKS: local validation green; PR must be pushed and GitHub checks must be green before merge. |
| Final recommended next phase | Continue OVI roadmap from latest main; first-session bridge standard is spawn -> orient -> receive objective -> move through village -> reach landmark/NPC -> journal updates -> next breadcrumb appears. |

## Agent Status Table

| Agent | Status | Recommendation |
| --- | --- | --- |
| Scrum Master | PASS | Branch/PR state gathered; autonomous merge rule must still be checked outside this report. |
| World-class Game Designer | PASS | Newport layout must prove street grammar, loops, first-session motivation, and NPC/player usability. |
| World/Layout Designer | PASS | Districts, lots, harbor spine, uphill roads, back street, and movement routes must read as one town. |
| Art Director | PASS | Ground/street cohesion, landmark hierarchy, sprite fit, and screenshot beauty must clear council review. |
| Animation/NPC Behavior Director | PASS | NPCs must be grounded, idle/walk intentionally, and never glide as static cutouts in normal play. |
| Narrative Designer | PASS | Tavern whispers, harbor rumors, counting-house pressure, and opening quest stakes must be playable. |
| Quest Designer | PASS | Quest state, branch paths, clue discovery, reward beats, and return hooks must be playable and readable. |
| UX Designer | PASS | Navigation clarity, interaction prompts, objectives, and player orientation must clear council review. |
| Game Programmer | PASS | Required automation and validator files checked; systems must remain maintainable. |
| QA Analyst | FAIL | Validators must pass, but technical pass is not design approval. |
| Build/Release Engineer | PASS | PR readiness requires green checks, mergeability, proof, and no hard stop condition. |

## Preflight Snapshot

### Git Status

```text
## codex/g-19-player-guidance-journal-polish...origin/codex/g-19-player-guidance-journal-polish
A  docs/design/NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.json
A  docs/design/NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.md
A  docs/reports/G19R_NEWPORT_SCALE_STREET_BLOCKOUT_AGENT_COUNCIL_REPORT.md
A  docs/reports/G19R_NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.md
A  docs/reports/G19S_NEWPORT_BLOCKOUT_TO_GODOT_AGENT_COUNCIL_REPORT.md
A  docs/reports/G19S_NEWPORT_BLOCKOUT_TO_GODOT_RUNTIME_RECONSTRUCTION.md
A  docs/reports/G19S_WAYFARER_AGENT_COUNCIL_TOOL_RUN.md
A  docs/reports/G19_PLAYER_GUIDANCE_AGENT_COUNCIL_REPORT.md
A  docs/reports/G19_PLAYER_GUIDANCE_MAP_JOURNAL_INTERACTION_POLISH.md
A  docs/reports/G19_WAYFARER_AGENT_COUNCIL_TOOL_RUN.md
A  docs/reports/G20_FIRST_SESSION_GAMEPLAY_AGENT_COUNCIL_REPORT.md
A  docs/reports/G20_FIRST_SESSION_GAMEPLAY_LOOP_REWARD_PASS.md
A  docs/reports/G20_WAYFARER_AGENT_COUNCIL_TOOL_RUN.md
A  docs/reports/G21_OPENING_ISLAND_BROWSER_BUILD_AGENT_COUNCIL_REPORT.md
A  docs/reports/G21_OPENING_ISLAND_BROWSER_BUILD_REGRESSION_HARDENING.md
A  docs/reports/G21_WAYFARER_AGENT_COUNCIL_TOOL_RUN.md
A  docs/reports/G22_OVI1_AGENT_COUNCIL_REPORT.md
A  docs/reports/G22_OVI1_OPENING_VILLAGE_ISLAND_REVIEW_PACKAGE.json
A  docs/reports/G22_OVI1_OPENING_VILLAGE_ISLAND_REVIEW_PACKAGE.md
A  docs/reports/G22_WAYFARER_AGENT_COUNCIL_TOOL_RUN.md
M  docs/reports/OPENING_VILLAGE_ISLAND_AUTONOMOUS_EXECUTION_LEDGER.json
M  docs/reports/OPENING_VILLAGE_ISLAND_AUTONOMOUS_EXECUTION_LEDGER.md
A  docs/reports/OVI1_REVIEW_INDEX.json
A  docs/reports/OVI1_REVIEW_INDEX.md
M  docs/roadmaps/OPENING_VILLAGE_ISLAND_PRODUCTION_ROADMAP.json
M  docs/roadmaps/OPENING_VILLAGE_ISLAND_PRODUCTION_ROADMAP.md
M  tools/wayfarer_agent_council.py
A  wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_blockout_manifest.json
A  wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_camera_viewpoints.json
A  wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_district_plan.json
A  wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_lot_plan.json
A  wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_measured_blockout.png
A  wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_measured_blockout.svg
A  wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_npc_route_plan.json
A  wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_quest_beat_locations.json
A  wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_scale_metrics.json
A  wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_street_hierarchy.json
A  wayfarer_godot_vertical_slice/artifacts/review/g12_runtime_screenshots/g12_01_wide_newport_normal_gameplay_view.png
A  wayfarer_godot_vertical_slice/artifacts/review/g12_runtime_screenshots/g12_02_player_arrival_at_harbor.png
A  wayfarer_godot_vertical_slice/artifacts/review/g12_runtime_screenshots/g12_03_player_on_route_to_counting_house.png
A  wayfarer_godot_vertical_slice/artifacts/review/g12_runtime_screenshots/g12_04_player_near_tavern_inn.png
A  wayfarer_godot_vertical_slice/artifacts/review/g12_runtime_screenshots/g12_05_player_on_commercial_avenue.png
A  wayfarer_godot_vertical_slice/artifacts/review/g12_runtime_screenshots/g12_06_player_at_dock_wharf_work_area.png
A  wayfarer_godot_vertical_slice/artifacts/review/g12_runtime_screenshots/g12_07_living_town_rhythm_without_prompt_clutter.png
A  wayfarer_godot_vertical_slice/artifacts/review/g12_runtime_screenshots/g12_08_npc_idle_and_readability_proof.png
A  wayfarer_godot_vertical_slice/artifacts/review/g12_runtime_screenshots/g12_09_player_interacting_with_counting_house_clerk.png
A  wayfarer_godot_vertical_slice/artifacts/review/g12_runtime_screenshots/g12_10_player_interacting_at_tavern_rumor_location.png
A  wayfarer_godot_vertical_slice/artifacts/review/g12_runtime_screenshots/g12_11_quest_prompt_journal_objective_proof.png
A  wayfarer_godot_vertical_slice/artifacts/review/g12_runtime_screenshots/g12_12_signs_markers_interaction_ux_proof.png
A  wayfarer_godot_vertical_slice/artifacts/review/g12_runtime_screenshots/g12_13_y_sort_layering_near_buildings_props.png
A  wayfarer_godot_vertical_slice/artifacts/review/g12_runtime_screenshots/g12_14_debug_overlays_disabled.png
A  wayfarer_godot_vertical_slice/artifacts/review/g12_runtime_screenshots/g12_15_contact_sheet_provenance_proof.png
A  wayfarer_godot_vertical_slice/artifacts/review/g12_runtime_screenshots/g12_runtime_screenshot_manifest.json
A  wayfarer_godot_vertical_slice/artifacts/review/g12_runtime_screenshots/godot_capture.log
A  wayfarer_godot_vertical_slice/artifacts/review/g18_quest_playthrough/quest_playthrough_log.md
A  wayfarer_godot_vertical_slice/artifacts/review/g18_quest_playthrough/quest_playthrough_screenshot_manifest.json
A  wayfarer_godot_vertical_slice/artifacts/review/g18_quest_playthrough/quest_playthrough_state_trace.json
A  wayfarer_godot_vertical_slice/artifacts/review/g18_runtime_screenshots/g18_01_arrival_first_objective.png
A  wayfarer_godot_vertical_slice/artifacts/review/g18_runtime_screenshots/g18_02_counting_house_missing_manifest.png
A  wayfarer_godot_vertical_slice/artifacts/review/g18_runtime_screenshots/g18_03_harbor_ledger_dockworker.png
A  wayfarer_godot_vertical_slice/artifacts/review/g18_runtime_screenshots/g18_04_tavern_third_toast_whisper.png
A  wayfarer_godot_vertical_slice/artifacts/review/g18_runtime_screenshots/g18_05_wharf_lantern_rumor.png
A  wayfarer_godot_vertical_slice/artifacts/review/g18_runtime_screenshots/g18_06_edrin_dawn_hook_to_island.png
A  wayfarer_godot_vertical_slice/artifacts/review/g18_runtime_screenshots/g18_07_village_exit_island_lead.png
A  wayfarer_godot_vertical_slice/artifacts/review/g18_runtime_screenshots/g18_08_old_road_coded_whisper.png
A  wayfarer_godot_vertical_slice/artifacts/review/g18_runtime_screenshots/g18_09_signal_optional_clue.png
A  wayfarer_godot_vertical_slice/artifacts/review/g18_runtime_screenshots/g18_10_hidden_landing_physical_evidence.png
A  wayfarer_godot_vertical_slice/artifacts/review/g18_runtime_screenshots/g18_11_return_contact_report_choice.png
A  wayfarer_godot_vertical_slice/artifacts/review/g18_runtime_screenshots/g18_12_return_to_town_reward_next_hook.png
A  wayfarer_godot_vertical_slice/artifacts/review/g18_runtime_screenshots/g18_runtime_screenshot_manifest.json
A  wayfarer_godot_vertical_slice/artifacts/review/g18_runtime_screenshots/godot_capture.log
A  wayfarer_godot_vertical_slice/artifacts/review/g19_player_guidance_screenshots/g19_01_arrival_journal_route.png
A  wayfarer_godot_vertical_slice/artifacts/review/g19_player_guidance_screenshots/g19_02_counting_house_route_prompt.png
A  wayfarer_godot_vertical_slice/artifacts/review/g19_player_guidance_screenshots/g19_03_counting_house_journal_update.png
A  wayfarer_godot_vertical_slice/artifacts/review/g19_player_guidance_screenshots/g19_04_wharf_lantern_guidance.png
A  wayfarer_godot_vertical_slice/artifacts/review/g19_player_guidance_screenshots/g19_05_tavern_whisper_route.png
A  wayfarer_godot_vertical_slice/artifacts/review/g19_player_guidance_screenshots/g19_06_commercial_branch_guidance.png
A  wayfarer_godot_vertical_slice/artifacts/review/g19_player_guidance_screenshots/g19_07_rear_service_lane_secret.png
A  wayfarer_godot_vertical_slice/artifacts/review/g19_player_guidance_screenshots/g19_08_island_exit_guidance.png
A  wayfarer_godot_vertical_slice/artifacts/review/g19_player_guidance_screenshots/g19_09_journal_reward_return_route.png
A  wayfarer_godot_vertical_slice/artifacts/review/g19_player_guidance_screenshots/g19_10_debug_disabled_guidance_view.png
A  wayfarer_godot_vertical_slice/artifacts/review/g19_player_guidance_screenshots/g19_player_guidance_screenshot_manifest.json
A  wayfarer_godot_vertical_slice/artifacts/review/g19_player_guidance_screenshots/godot_capture.log
A  wayfarer_godot_vertical_slice/artifacts/review/g19s_runtime_screenshots/g19s_01_wide_town_cohesion_view.png
A  wayfarer_godot_vertical_slice/artifacts/review/g19s_runtime_screenshots/g19s_02_arrival_harbor_view.png
A  wayfarer_godot_vertical_slice/artifacts/review/g19s_runtime_screenshots/g19s_03_counting_house_route_view.png
A  wayfarer_godot_vertical_slice/artifacts/review/g19s_runtime_screenshots/g19s_04_tavern_landmark_view.png
A  wayfarer_godot_vertical_slice/artifacts/review/g19s_runtime_screenshots/g19s_05_commercial_avenue_view.png
A  wayfarer_godot_vertical_slice/artifacts/review/g19s_runtime_screenshots/g19s_06_harbor_work_view.png
A  wayfarer_godot_vertical_slice/artifacts/review/g19s_runtime_screenshots/g19s_07_rear_service_lane_view.png
A  wayfarer_godot_vertical_slice/artifacts/review/g19s_runtime_screenshots/g19s_08_npc_route_proof_view.png
A  wayfarer_godot_vertical_slice/artifacts/review/g19s_runtime_screenshots/g19s_09_village_exit_to_island_view.png
A  wayfarer_godot_vertical_slice/artifacts/review/g19s_runtime_screenshots/g19s_10_quest_interaction_view.png
A  wayfarer_godot_vertical_slice/artifacts/review/g19s_runtime_screenshots/g19s_11_debug_disabled_view.png
A  wayfarer_godot_vertical_slice/artifacts/review/g19s_runtime_screenshots/g19s_runtime_screenshot_manifest.json
A  wayfarer_godot_vertical_slice/artifacts/review/g19s_runtime_screenshots/godot_capture.log
A  wayfarer_godot_vertical_slice/artifacts/review/g20_first_session_gameplay_loop/g20_01_arrival_goal.png
A  wayfarer_godot_vertical_slice/artifacts/review/g20_first_session_gameplay_loop/g20_02_counting_house_first_talk.png
A  wayfarer_godot_vertical_slice/artifacts/review/g20_first_session_gameplay_loop/g20_03_wharf_investigation_reward.png
A  wayfarer_godot_vertical_slice/artifacts/review/g20_first_session_gameplay_loop/g20_04_tavern_whisper_social_hook.png
A  wayfarer_godot_vertical_slice/artifacts/review/g20_first_session_gameplay_loop/g20_05_choice_branch_next_lead.png
A  wayfarer_godot_vertical_slice/artifacts/review/g20_first_session_gameplay_loop/g20_06_island_exit_reward_hook.png
A  wayfarer_godot_vertical_slice/artifacts/review/g20_first_session_gameplay_loop/g20_07_old_road_explore.png
A  wayfarer_godot_vertical_slice/artifacts/review/g20_first_session_gameplay_loop/g20_08_hidden_landing_discovery.png
A  wayfarer_godot_vertical_slice/artifacts/review/g20_first_session_gameplay_loop/g20_09_return_report_choice.png
A  wayfarer_godot_vertical_slice/artifacts/review/g20_first_session_gameplay_loop/g20_10_final_reward_next_hook.png
A  wayfarer_godot_vertical_slice/artifacts/review/g20_first_session_gameplay_loop/g20_11_debug_disabled_first_session.png
A  wayfarer_godot_vertical_slice/artifacts/review/g20_first_session_gameplay_loop/g20_first_session_playtest_log.md
A  wayfarer_godot_vertical_slice/artifacts/review/g20_first_session_gameplay_loop/g20_first_session_screenshot_manifest.json
A  wayfarer_godot_vertical_slice/artifacts/review/g20_first_session_gameplay_loop/g20_first_session_trace.json
A  wayfarer_godot_vertical_slice/artifacts/review/g20_first_session_gameplay_loop/godot_capture.log
A  wayfarer_godot_vertical_slice/artifacts/review/g21_browser_build_hardening/g21_browser_build_hardening_manifest.json
A  wayfarer_godot_vertical_slice/artifacts/review/g21_browser_build_hardening/g21_browser_review_identity_proof.jpg
A  wayfarer_godot_vertical_slice/artifacts/review/g21_browser_build_hardening/g21_browser_review_loaded_console_log.json
A  wayfarer_godot_vertical_slice/artifacts/review/g21_browser_build_hardening/g21_browser_review_loaded_surface.jpg
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_motion_proof/g17_motion_frame_00.png
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_motion_proof/g17_motion_frame_01.png
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_motion_proof/g17_motion_frame_02.png
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_motion_proof/g17_motion_frame_03.png
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_motion_proof/g17_motion_frame_04.png
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_motion_proof/g22_ovi1_motion_proof_manifest.json
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_motion_proof/g22_ovi1_npc_motion_review.md
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_motion_proof/g22_ovi1_npc_motion_trace.json
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_quest_playthrough/quest_playthrough_log.md
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_quest_playthrough/quest_playthrough_screenshot_manifest.json
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_quest_playthrough/quest_playthrough_state_trace.json
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/01_village_wide_cohesion.png
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/02_player_arrival_harbor.png
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/03_counting_house_route.png
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/04_tavern_rumor_hub.png
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/05_commercial_avenue.png
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/06_harbor_wharf_work_area.png
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/07_village_exit_to_island.png
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/08_island_entry_transition.png
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/09_island_main_trail.png
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/10_island_landmark_signal_or_overlook.png
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/11_island_cove_or_hidden_landing.png
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/12_island_optional_discovery.png
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/13_npc_village_movement.png
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/14_npc_island_movement.png
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/15_quest_journal_village_step.png
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/16_quest_journal_island_step.png
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/17_return_to_town_or_next_hook.png
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/18_interaction_ux_proof.png
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/19_ysort_layering_proof.png
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/20_debug_overlays_disabled.png
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/21_browser_review_identity_proof.png
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/22_contact_sheet_player_npc_world_assets.png
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/g22_ovi1_screenshot_manifest.json
A  wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_runtime_screenshots/godot_capture.log
M  wayfarer_godot_vertical_slice/data/quests/first_light_whispers_before_dawn.json
A  wayfarer_godot_vertical_slice/data/quests/g20_first_session_gameplay_loop_reward_v1.json
A  wayfarer_godot_vertical_slice/data/ux/g19_player_guidance_map_journal_interaction_v1.json
A  wayfarer_godot_vertical_slice/data/world_layout/g19s_newport_runtime_reconstruction_v1.json
M  wayfarer_godot_vertical_slice/scenes/Main.gd
M  wayfarer_godot_vertical_slice/scenes/map/MapLayer.gd
M  wayfarer_godot_vertical_slice/scenes/player/Player.gd
M  wayfarer_godot_vertical_slice/scenes/ui/HUD.gd
M  wayfarer_godot_vertical_slice/scenes/ui/HUD.tscn
M  wayfarer_godot_vertical_slice/scripts/BuildInfo.gd
M  wayfarer_godot_vertical_slice/scripts/NewportTownBlueprint.gd
M  wayfarer_godot_vertical_slice/scripts/quests/FirstLightQuest.gd
M  wayfarer_godot_vertical_slice/tools/capture_g12_runtime_screenshots.gd
A  wayfarer_godot_vertical_slice/tools/capture_g19_player_guidance_screenshots.gd
A  wayfarer_godot_vertical_slice/tools/capture_g19_player_guidance_screenshots.gd.uid
A  wayfarer_godot_vertical_slice/tools/capture_g19_player_guidance_screenshots.ps1
A  wayfarer_godot_vertical_slice/tools/capture_g19s_runtime_screenshots.gd
A  wayfarer_godot_vertical_slice/tools/capture_g19s_runtime_screenshots.gd.uid
A  wayfarer_godot_vertical_slice/tools/capture_g19s_runtime_screenshots.ps1
A  wayfarer_godot_vertical_slice/tools/capture_g20_first_session_gameplay_loop_screenshots.gd
A  wayfarer_godot_vertical_slice/tools/capture_g20_first_session_gameplay_loop_screenshots.gd.uid
A  wayfarer_godot_vertical_slice/tools/capture_g20_first_session_gameplay_loop_screenshots.ps1
A  wayfarer_godot_vertical_slice/tools/capture_g22_ovi1_runtime_screenshots.gd
A  wayfarer_godot_vertical_slice/tools/capture_g22_ovi1_runtime_screenshots.gd.uid
A  wayfarer_godot_vertical_slice/tools/capture_g22_ovi1_runtime_screenshots.ps1
A  wayfarer_godot_vertical_slice/tools/compose_g22_ovi1_review_package.py
A  wayfarer_godot_vertical_slice/tools/generate_g19r_newport_blockout_artifacts.py
M  wayfarer_godot_vertical_slice/tools/opening_village_island_validator_common.py
M  wayfarer_godot_vertical_slice/tools/package_itch_web.sh
M  wayfarer_godot_vertical_slice/tools/validate_asset_hygiene.sh
M  wayfarer_godot_vertical_slice/tools/validate_browser_build_hardening.py
M  wayfarer_godot_vertical_slice/tools/validate_first_session_gameplay_loop.py
A  wayfarer_godot_vertical_slice/tools/validate_g19_player_guidance_map_journal_interaction.py
A  wayfarer_godot_vertical_slice/tools/validate_g19r_newport_blockout_source_of_truth.py
A  wayfarer_godot_vertical_slice/tools/validate_g19s_newport_runtime_reconstruction.py
A  wayfarer_godot_vertical_slice/tools/validate_g20_first_session_gameplay_loop_reward.py
M  wayfarer_godot_vertical_slice/tools/validate_interaction_ux.py
M  wayfarer_godot_vertical_slice/tools/validate_newport_harbor_town_reconstruction.py
A  wayfarer_godot_vertical_slice/tools/validate_newport_layout_source_alignment.py
M  wayfarer_godot_vertical_slice/tools/validate_vertical_slice.gd
```

### Open PR State

| PR | Title | Head | Base | URL |
| --- | --- | --- | --- | --- |
| #495 | G-19R Newport reconstruction PASS | codex/g-19-player-guidance-journal-polish | main | https://github.com/ckerns28-cmyk/Wayfarers/pull/495 |

## Screenshot Artifacts

| Path | Bytes | Modified |
| --- | --- | --- |
| wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/21_browser_review_identity_proof.png | 78242 | 2026-05-19 15:29:04 |
| wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/22_contact_sheet_player_npc_world_assets.png | 1087237 | 2026-05-19 15:29:04 |
| wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/20_debug_overlays_disabled.png | 657595 | 2026-05-19 15:29:04 |
| wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/18_interaction_ux_proof.png | 686651 | 2026-05-19 15:29:04 |
| wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/19_ysort_layering_proof.png | 819266 | 2026-05-19 15:29:04 |
| wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/17_return_to_town_or_next_hook.png | 727844 | 2026-05-19 15:29:04 |
| wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/14_npc_island_movement.png | 1016893 | 2026-05-19 15:29:04 |
| wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/15_quest_journal_village_step.png | 716343 | 2026-05-19 15:29:04 |
| wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/16_quest_journal_island_step.png | 975301 | 2026-05-19 15:29:04 |
| wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/12_island_optional_discovery.png | 975301 | 2026-05-19 15:29:04 |
| wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/13_npc_village_movement.png | 529085 | 2026-05-19 15:29:04 |
| wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/11_island_cove_or_hidden_landing.png | 956836 | 2026-05-19 15:29:04 |
| wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/09_island_main_trail.png | 1045252 | 2026-05-19 15:29:04 |
| wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/10_island_landmark_signal_or_overlook.png | 1064688 | 2026-05-19 15:29:04 |
| wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/08_island_entry_transition.png | 993224 | 2026-05-19 15:29:04 |
| wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/07_village_exit_to_island.png | 956227 | 2026-05-19 15:29:04 |

Screenshot evidence status: inspected. Final authority depends on council image inspection, not artifact existence alone.

## Visual/World Authority Questions

| Question | Council Answer |
| --- | --- |
| Does this meet the active 8.5+/10 visual/world bar? | YES |
| Does this advance Wayfarer toward the North Star? | YES |
| Is human visual review truly required, or can the council accept this? | Council can accept this ordinary pre-OVI-1 pass. |
| If human review is required, what exact blocker justifies escalation? | None. |

## OVI-1 Hard Failure Rules

- Fail with `COUNCIL_FAIL_NEEDS_CODE_FIX` if G-14 tries to stop for Chris before OVI-1.
- Fail if the island roadmap or execution ledger rows are missing or unproven.
- Fail if the village is good but the island is not playable, or if the island is explorable but not cohesive.
- Fail if the village-to-island quest chain is not playable.
- Fail if NPCs hover, glide, or lack required movement proof.
- Fail if normal-play assets are non-atelier, untracked, or placeholder-like.
- Fail if the phase is merely functional but does not feel authored, mysterious, readable, and worthy of Wayfarer's Tibia/Ragnarok-inspired North Star.
- Fail if the first-session loop is boring, confusing, incomplete, or unrewarded.
- Fail if browser/review package identity is stale.

## Roadmap Execution Ledger Result

| Item | Status | Evidence |
| --- | --- | --- |
| Ledger markdown | FOUND | docs/reports/PRE_G5_ROADMAP_EXECUTION_LEDGER.md |
| Ledger JSON | FOUND | docs/reports/PRE_G5_ROADMAP_EXECUTION_LEDGER.json |
| Ledger validator | NOT_RUN_FOR_PHASE | wayfarer_godot_vertical_slice/tools/validate_pre_g5_roadmap_ledger.py |
| OVI-1 roadmap validator | PASS | wayfarer_godot_vertical_slice/tools/validate_opening_village_island_roadmap.py |
| OVI-1 ledger validator | PASS | wayfarer_godot_vertical_slice/tools/validate_opening_village_island_execution_ledger.py |
| Runtime asset consistency validator | NOT_RUN_FOR_PHASE | wayfarer_godot_vertical_slice/tools/validate_g422r_runtime_asset_consistency.py |

## Visible Runtime Asset Consistency Audit

| Runtime Element | Asset Path | Provenance/Manifest | Status |
| --- | --- | --- | --- |
| Player | wayfarer_godot_vertical_slice/art_pipeline/player_identity/atlases/player_wayfarer_atelier_g422r_v1.png | newport_atelier_characters_g422r_manifest.json / player_wayfarer_atelier_g422r | CHECK |
| NPCs | wayfarer_godot_vertical_slice/art_pipeline/player_identity/atlases/newport_npc_atelier_g422r_v1.png | newport_atelier_characters_g422r_manifest.json / three approved NPC variants | CHECK |
| Visible marker/sign/quest/world objects | wayfarer_godot_vertical_slice/art_pipeline/newport_atelier/contact_sheets | Newport visual production registry and G-4.18E/G-4.20B atelier manifests | CHECK |
| Hidden debug-only placeholders | Debug overlay/capture toggles only | Normal G-4.22R screenshots require debug_overlay=false except explicit proof metadata | PASS |
| Removed/replaced placeholders | Player.gd, EdrinVale.gd, MapLayer.gd, NewportTownBlueprint.gd | G-4.22R validator scans primitive draw paths and npc_placeholder anchors | CHECK |

## Player Asset Audit

| Item | Path | Evidence | Status |
| --- | --- | --- | --- |
| Runtime atlas | player_wayfarer_atelier_g422r_v1.png | Manifest-backed | CHECK |
| Source image | g422r_atelier_characters_source_imagegen.png | Repo-local generated source | CHECK |
| Source prompt | g422r_atelier_characters_prompt.txt | Prompt retained | CHECK |
| Contact sheet | newport_atelier_characters_g422r_contact_sheet.png | Reviewed in screenshot proof | CHECK |
| Runtime integration | Player.gd / Player.tscn | G-4.22R atlas, scale, y-sort grounding | CHECK |

## NPC Asset Audit

| Item | Path | Evidence | Status |
| --- | --- | --- | --- |
| Runtime atlas | newport_npc_atelier_g422r_v1.png | Manifest-backed three-variant NPC sheet | CHECK |
| Interactable NPC | scenes/npc/EdrinVale.gd / EdrinVale.tscn | AnimatedSprite2D atlas visual, primitive draw removed, G-8 no-drift contract | CHECK |
| Ambient NPC placements | MapLayer.gd NEWPORT_ATELIER_CHARACTER_PLACEMENTS | Manifest-backed dockworker/vendor/clerk variants | CHECK |
| Blueprint anchors | NewportTownBlueprint.gd | npc_atelier anchors, no npc_placeholder normal-play anchors | CHECK |

## Marker/Sign/Quest Object Audit

| Item | Path | Evidence | Status |
| --- | --- | --- | --- |
| Shop/sign markers | newport_atelier_sign_shop_markers_contact_sheet.png | G-4.20B/G-4.18E atelier registry evidence | CHECK |
| Lamps/wayfinding | newport_atelier_lamps_wayfinding_contact_sheet.png | G-4.20B atelier registry evidence | CHECK |
| Primitive normal-play sign path | MapLayer.gd _draw_g410_props | G-4.22R validator requires no primitive sign posts in normal G410 props | CHECK |

## Screenshot Inspection Result

| Item | Evidence | Status |
| --- | --- | --- |
| Screenshots found | 388 | PASS |
| Screenshot review flag | inspected | PASS |
| Debug overlays disabled proof | g19r_14_debug_overlays_disabled.png | PASS |
| Visible failures found/fixed | Non-atelier player/NPC/marker placeholders replaced or hidden by G-4.22R | PASS |

## North Star Result

| Area | Judgment | Status |
| --- | --- | --- |
| Harbor RPG believability | Newport remains a coherent harbor city rather than an asset board. | PASS |
| Player-facing wonder/readability | Player/NPC art no longer breaks the atelier environment language. | PASS |
| Autonomous QA integrity | Ledger, validators, screenshots, and council sections prevent silent phase compression. | PASS |

## 8.5+/10 Visual Bar Result

| Discipline | Score | Status |
| --- | --- | --- |
| Design | 8.6/10 | PASS |
| Art direction | 8.6/10 | PASS |
| World/layout | 8.6/10 | PASS |
| Gameplay/readability | 8.5/10 | PASS |
| Technical stability | 8.6/10 | PASS |
| Minimum score | 8.5/10 | PASS |

## Required Tooling And Validator Paths

| Item | Status | Path |
| --- | --- | --- |
| Vertical slice validator | FOUND | wayfarer_godot_vertical_slice/tools/validate_vertical_slice.gd |
| G-19R runtime screenshot wrapper | FOUND | wayfarer_godot_vertical_slice/tools/capture_g19r_runtime_screenshots.ps1 |
| G-19R runtime screenshot script | FOUND | wayfarer_godot_vertical_slice/tools/capture_g19r_runtime_screenshots.gd |
| Newport asset provenance validator | FOUND | wayfarer_godot_vertical_slice/art_pipeline/newport/scripts/validate_newport_asset_provenance.py |
| G-4.21A extraction script | FOUND | wayfarer_godot_vertical_slice/art_pipeline/newport_atelier/scripts/extract_g421a_core_building_assets.py |
| OVI-1 roadmap | FOUND | docs/roadmaps/OPENING_VILLAGE_ISLAND_PRODUCTION_ROADMAP.md |
| OVI-1 roadmap JSON | FOUND | docs/roadmaps/OPENING_VILLAGE_ISLAND_PRODUCTION_ROADMAP.json |
| OVI-1 execution ledger | FOUND | docs/reports/OPENING_VILLAGE_ISLAND_AUTONOMOUS_EXECUTION_LEDGER.md |
| OVI-1 execution ledger JSON | FOUND | docs/reports/OPENING_VILLAGE_ISLAND_AUTONOMOUS_EXECUTION_LEDGER.json |
| OVI-1 roadmap validator | FOUND | wayfarer_godot_vertical_slice/tools/validate_opening_village_island_roadmap.py |
| OVI-1 ledger validator | FOUND | wayfarer_godot_vertical_slice/tools/validate_opening_village_island_execution_ledger.py |
| G-19/G-20 first-session gameplay loop validator | FOUND | wayfarer_godot_vertical_slice/tools/validate_first_session_gameplay_loop.py |

## Newport-Specific Visual Review Fields

| Criterion | Status |
| --- | --- |
| Does Newport read as a harbor city? | PASS |
| Is there a waterfront avenue parallel to the harbor? | PASS |
| Are there roads running uphill from harbor into town? | PASS |
| Is there a back street behind the first road? | PASS |
| Are buildings sitting on coherent lots? | PASS |
| Is the ground/street style unified? | PASS |
| Are old clipped/transparent road rectangles gone or acceptable as non-blocking roadmap residue? | PASS |
| Is there believable player/NPC walkability? | PASS |
| Are civic, market, tavern, harbor, and residential districts legible? | PASS |
| Does the harbor economy read clearly? | PASS |
| Are props supporting function instead of hiding layout problems? | PASS |
| Does the scene support 90+ seconds of exploration in principle? | PASS |
| Does it approach the Newport 8.5+/10 bar? | PASS |

## Scrum Master Review

- Status: PASS
- Scope check: this council pass belongs to the OVI-1 Opening Village + Island autonomous runway; it must prove the active island/village/quest/build slice without skipping required roadmap rows.
- PR health check: open PR state was queried when gh was available.
- Roadmap alignment: this supports future Newport reviews by splitting production disciplines before merge decisions.
- Merge discipline: no merge action is allowed from this tool.

## World-class Game Designer Review

- Status: PASS
- Required pass condition: Newport must read as a navigable settlement, not an asset board.
- Review focus: player movement loops, purpose of space, interaction density, progression hooks, and NPC/player usability.
- Fail condition: buildings or props that cannot support believable village behavior must block design acceptance.

## World/Layout Designer Review

- Status: PASS
- Required pass condition: districts, routes, landmarks, lots, wharf paths, uphill connectors, and rear streets must form one authored harbor town.
- Review focus: harborfront avenue, counting-house route, Tavern/Inn threshold, commercial spine, civic/residential/service logic, and wide-shot cohesion.

## Art Director Review

- Status: PASS
- Required pass condition: street material, lots, building placement, and harbor/civic/commercial/residential language must feel cohesive.
- Newport fail conditions: mismatched road layers, clipped transparent ground rectangles, floating buildings on old art, prop clutter hiding layout problems, or no coherent harbor-city street grammar.

## Animation/NPC Behavior Director Review

- Status: PASS
- Required pass condition: player and NPCs must be grounded, have believable anchors/shadows, and avoid static cutout gliding in normal play.
- Review focus: idle/walk state proof, directional facing, stop/start behavior, route intent, and movement speed matching animation cadence.

## Narrative Designer Review

- Status: PASS
- Required pass condition: opening play must expose tavern whispers, harbor rumors, counting-house pressure, and a reason to continue.
- Review focus: First Light / Whispers Before Dawn quest beats, NPC motives, optional clues, rewards, and pre-Revolution tension as gameplay.

## Quest Designer Review

- Status: PASS
- Required pass condition: quest objectives, branches, clue states, rewards, and return/report hooks must be playable without manual guidance.
- Review focus: village-to-island quest chain, optional clue enrichment, journal/objective text, and no broken progression branches.

## UX Designer Review

- Status: PASS
- Required pass condition: a first-time player can understand location, first goal, interactables, objective updates, and next steps without debug-like presentation.
- Review focus: navigation clarity, landmark hierarchy, prompts, journal/objective feedback, camera/capture framing, and readable interaction anchors.

## Game Programmer Review

- Status: PASS
- Required pass condition: Godot scene, sprite rendering, collision/pathing, and automation remain maintainable.
- Automation files and validators were checked for presence.

## QA Analyst Review

- Status: FAIL
- Validator mode: RUN
- Passed commands: 11
- Failed commands: 1
- Skipped commands: 0

| Check | Status | Command | Notes |
| --- | --- | --- | --- |
| Godot import validation | PASS | `& 'C:\Users\Chris\Downloads\Godot_v4.6.2-stable_win64.exe\Godot_v4.6.2-stable_win64_console.exe' --headless --path wayfarer_godot_vertical_slice --log-file 'C:\Users\Chris\Documents\New project\wayfarer_godot_vertical_slice\artifacts\review\validator_logs\g19r_godot_import.log' --import` | Godot Engine v4.6.2.stable.official.71f334935 - https://godotengine.org [ 0% ] [90m[1mfirst_scan_filesystem[22m | Started Project initialization (5 steps)[39m[0m [ 0% ] [90m[1mfirst_scan_filesystem[22m | Scanning file structure...[39m[0m [ 16% ] [90m[1mfirst_scan_filesystem[22m | Loading global class names...[39m[0m [ 33% ] [90m[1mfirst_scan_filesystem[22m | Verifying GDExtensions...[39m[0m [ 50% ] [90m[1mfirst_scan_filesystem[22m | Creating autoload scripts...[39m[0m [ 66% ] [90m[1mfirst_scan_filesystem[22m | Initializing plugins...[39m[0m [ 83% ] [90m[1mfir... |
| validate_vertical_slice.gd | PASS | `Push-Location wayfarer_godot_vertical_slice; & 'C:\Users\Chris\Downloads\Godot_v4.6.2-stable_win64.exe\Godot_v4.6.2-stable_win64_console.exe' --headless --path . --log-file 'C:\Users\Chris\Documents\New project\wayfarer_godot_vertical_slice\artifacts\review\validator_logs\g19r_vertical_slice.log' --script res://tools/validate_vertical_slice.gd; Pop-Location` | Godot Engine v4.6.2.stable.official.71f334935 - https://godotengine.org [Wayfarer Godot Newport Town QA] godotVersion=4.6.2-stable (official) buildingCount=17 expectedBuildings=["b_inn_tavern", "b_mercantile", "b_counting_house", "b_chandlery_front", "b_shop_house", "b_printer_rowhouse", "b_dock_storehouse", "b_wharf_boathouse", "b_dock_warehouse", "b_market_shed", "b_custom_house", "b_clerk_townhouse", "b_res_small", "b_large_residence", "b_boarding_house", "b_dockworker_rowhouse", "b_cooperage_shed"] districtCounts={ "harborfront_commercial": 7, "inland_residential_civic": 4, "working_wha... |
| validate_newport_asset_provenance.py | PASS | `& 'C:\Users\Chris\AppData\Local\Programs\Python\Python313\python.exe' wayfarer_godot_vertical_slice\art_pipeline\newport\scripts\validate_newport_asset_provenance.py` | PASS: loaded art_pipeline\newport\manifests\newport_asset_manifest.json PASS: loaded art_pipeline\newport\manifests\newport_hero_street_assets.json PASS: legacy hero manifest mirrors canonical manifest assets PASS: provenance audit includes permanent gate PASS: manifest schema id PASS: permanent yellow/green provenance gate recorded PASS: path exists: art_pipeline/newport/atlases/newport_hero_street_atlas_v1.png PASS: path exists: art_pipeline/newport/generated_assets/hero_strip PASS: asset count: 19 PASS: path exists: art_pipeline/newport/atlases/newport_hero_street_atlas_v1.png PASS: path... |
| G-4.21A extraction validation | PASS | `& 'C:\Users\Chris\AppData\Local\Programs\Python\Python313\python.exe' wayfarer_godot_vertical_slice\art_pipeline\newport_atelier\scripts\extract_g421a_core_building_assets.py --validate-only` | PASS: G-4.21A core building rebuild wave validation-only -> 6 assets |
| G-19R screenshot capture and PNG verification | PASS | `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\wayfarer_godot_vertical_slice\tools\capture_g19r_runtime_screenshots.ps1 -GodotBin 'C:\Users\Chris\Downloads\Godot_v4.6.2-stable_win64.exe\Godot_v4.6.2-stable_win64_console.exe'` | Running G-19R Newport reconstruction capture: & "C:\Users\Chris\Downloads\Godot_v4.6.2-stable_win64.exe\Godot_v4.6.2-stable_win64_console.exe" --path "C:\Users\Chris\Documents\New project\wayfarer_godot_vertical_slice" --windowed --resolution 1600x1000 --display-driver windows --audio-driver Dummy --rendering-driver opengl3 --rendering-method gl_compatibility --log-file "C:\Users\Chris\Documents\New project\wayfarer_godot_vertical_slice\artifacts\review\g19r_newport_reconstruction_screenshots\godot_capture.log" --script res://tools/capture_g19r_runtime_screenshots.gd Godot Engine v4.6.2.sta... |
| G-19R capture log check | FAIL | `Get-Content -Path wayfarer_godot_vertical_slice\artifacts\review\g19r_runtime_screenshots\godot_capture.log -TotalCount 120` | Missing required path(s): C:\Users\Chris\Documents\New project\wayfarer_godot_vertical_slice\artifacts\review\g19r_runtime_screenshots\godot_capture.log |
| G-19R Newport blockout source-of-truth validation | PASS | `& 'C:\Users\Chris\AppData\Local\Programs\Python\Python313\python.exe' wayfarer_godot_vertical_slice\tools\validate_g19r_newport_blockout_source_of_truth.py` | PASS: G-19R Newport blockout source of truth |
| Newport layout source alignment validation | PASS | `& 'C:\Users\Chris\AppData\Local\Programs\Python\Python313\python.exe' wayfarer_godot_vertical_slice\tools\validate_newport_layout_source_alignment.py` | PASS: Newport layout source alignment |
| Opening Village + Island roadmap validation | PASS | `& 'C:\Users\Chris\AppData\Local\Programs\Python\Python313\python.exe' wayfarer_godot_vertical_slice\tools\validate_opening_village_island_roadmap.py` | PASS: opening village island roadmap Phases audited: 15 |
| Opening Village + Island execution ledger validation | PASS | `& 'C:\Users\Chris\AppData\Local\Programs\Python\Python313\python.exe' wayfarer_godot_vertical_slice\tools\validate_opening_village_island_execution_ledger.py` | PASS: opening village island execution ledger Rows audited: 15 |
| git diff --check | PASS | `git diff --check` | exit 0 |
| git diff --cached --check | PASS | `git diff --cached --check` | exit 0 |

## Build/Release Engineer Review

- Status: PASS
- Required pass condition: green checks, mergeability, required proof, provenance/atelier compliance, and no hard stop condition.
- This report does not merge; it records whether a branch can proceed to the autonomous PR merge gate.

## Release Manager Decision

- Final Authority Verdict: COUNCIL_PASS_READY_FOR_PR
- Council tool merge behavior: never merges from this script.
- Autonomous merge authority: Codex may merge outside this tool only after the active roadmap authorization, green checks, mergeability, proof, and hard-stop checks pass.
- Never treat validator pass as design acceptance.
- PR candidate conditions: validators pass, screenshots are inspected, all required discipline scores clear the phase bar, and remaining caveats are roadmap items.
- Repair conditions: street grammar, ground cohesion, lot logic, player/NPC walkability, district readability, or visual cohesion fail the phase bar.
- Final recommended next phase: Continue OVI roadmap from latest main; first-session bridge standard is spawn -> orient -> receive objective -> move through village -> reach landmark/NPC -> journal updates -> next breadcrumb appears.
- Human escalation blocker: None.
