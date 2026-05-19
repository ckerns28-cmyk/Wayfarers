# G-20 First-Session Gameplay Agent Council Report

Branch: `codex/g-20-first-session-gameplay-loop-reward-pass`

Phase: G-20 First-Session Gameplay Loop and Reward Pass

Human review required: no

Final verdict: `COUNCIL_PASS_READY_FOR_PR`

## First-Session Gameplay Result

The council reviewed G-20 as a design-production gate, not a code-only pass. The approved result is a runtime-backed first 20-30 minute loop with source truth, quest geography, visible reward cadence, screenshot proof, and a reason to continue after the hidden landing evidence returns to Newport.

## Council Roles

| Role | Result | Harsh-critic finding |
|---|---:|---|
| Scrum Master | PASS | G-20 is correctly sequenced after G-19R, G-19S, and G-19; next phase remains G-21, not a stop for Chris. |
| World-class Game Designer | PASS | The loop now has arrival, place orientation, social mystery, investigation, exploration, discovery, reward, and forward threat. |
| World/Layout Designer | PASS | The quest uses the G-19R/G-19S source layout: harbor arrival, Counting House, wharf, Tavern/Inn, east exit, old road, hidden landing, return route. |
| Level Designer | PASS | Player movement is a readable geography loop instead of a sequence of disconnected NPC clicks. |
| Art Director | PASS | G-20 does not add placeholder art or clutter; it relies on the source-driven Newport composition and existing atelier-standard runtime assets. |
| Narrative/Quest Designer | PASS | Whispers Before Dawn now pays off as a harbor conspiracy with the Third Toast, proof, named contacts, and a Governor's-men dawn hook. |
| Animation/NPC Behavior Director | PASS | The proof does not ask static sprites to glide; NPCs remain stationed unless grounded movement proof exists. |
| UX Designer | PASS | Route hints, journal state, reward feedback, and location bands keep the first session readable without debug-looking prompts. |
| Game Programmer | PASS | Runtime contracts and validators make the loop inspectable and machine-checkable. |
| QA Analyst | PASS | The phase adds a G-20 validator, screenshot manifest, trace, playtest log, and debug-disabled proof. |
| Build/Release Engineer | PASS | The phase is PR-ready after local validators, screenshot capture, and Agent Council tool run pass. |

## Harsh-Critic Questions

Would this impress a first-time player?

Yes for this gate. The player now gets a working harbor arrival, a civic contact, a tavern rumor, route choice, island discovery, Resolve feedback, named contacts, and a forward threat.

Would this hold up against top-tier RPG/MMORPG starter-zone expectations?

It is not OVI-1 complete yet, but G-20 reaches the minimum bar for first-session loop structure: place memory, social mystery, physical discovery, reward cadence, and a next hook.

Does the player understand where they are and what to do?

Yes. G-19 route guidance remains active, and G-20 proves the route from harbor to Counting House to wharf/tavern to island and back.

Does the world feel authored, or assembled?

Authored enough for this gate. The loop now relies on districts and streets from the G-19R/G-19S source of truth rather than ad hoc placement.

Does the screenshot prove the claim?

Yes, pending the generated G-20 manifest staying PASS: the canonical screenshots cover arrival, Counting House, wharf, tavern, route choice, island exit, old road, hidden landing, return/report, reward hook, and debug-disabled normal play.

Are rewards visible and meaningful?

Yes. The runtime contract proves `13 Resolve`, named contacts, route unlock, and a dawn threat. The HUD reward contract proves reward feedback is present in player-facing state.

Do quest beats belong to the town geography?

Yes. Each beat uses a planned district or island route and returns the proof to Newport, so the quest is not bolted onto the layout.

Is human review required?

No. There is no creative fork, paid-tool blocker, unsafe operation, or unresolvable tooling failure.

## Scores

| Score | Value |
|---|---:|
| Gameplay hook score | 8.7 |
| Reward cadence score | 8.7 |
| World cohesion score | 8.6 |
| Player orientation score | 8.7 |
| Quest-geography integration score | 8.7 |
| Implementation-readiness score | 8.7 |

## Required Proof

- Source contract: `wayfarer_godot_vertical_slice/data/quests/g20_first_session_gameplay_loop_reward_v1.json`
- Runtime contract: `FirstLightQuest.debug_first_session_gameplay_loop_reward_contract()`
- Main contract: `Main.first_session_gameplay_loop_reward_contract()`
- HUD contract: `HUD.first_session_reward_loop_contract()`
- Validator: `wayfarer_godot_vertical_slice/tools/validate_g20_first_session_gameplay_loop_reward.py`
- Capture wrapper: `wayfarer_godot_vertical_slice/tools/capture_g20_first_session_gameplay_loop_screenshots.ps1`
- Screenshot manifest: `wayfarer_godot_vertical_slice/artifacts/review/g20_first_session_gameplay_loop/g20_first_session_screenshot_manifest.json`
- Trace: `wayfarer_godot_vertical_slice/artifacts/review/g20_first_session_gameplay_loop/g20_first_session_trace.json`
- Playtest log: `wayfarer_godot_vertical_slice/artifacts/review/g20_first_session_gameplay_loop/g20_first_session_playtest_log.md`

## Verdict

`COUNCIL_PASS_READY_FOR_PR`

G-20 can proceed to PR after validators and screenshot capture pass locally. After merge, continue immediately to G-21 Opening Island Performance, Browser Build, and Regression Hardening.
