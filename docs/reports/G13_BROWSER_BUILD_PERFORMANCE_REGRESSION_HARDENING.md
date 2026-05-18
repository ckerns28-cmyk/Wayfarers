# G-13 Browser Build, Performance, and Regression Hardening

Date: 2026-05-18

Branch: `codex/g-13-browser-build-hardening`

## Scope

G-13 hardens the Starter Village browser-review route after G-12. The phase
does not claim final SV-1 design acceptance; it proves the Godot route, review
build identity, browser-review ZIP, screenshot regression route, input/review
metadata route, performance envelope, and accumulated asset/quest/UX validators
are stable enough for the G-14 review package.

## Review Build Identity

- `BuildInfo.gd` now reports `BUILD_PHASE = G-13`.
- Visible HUD metadata now labels the build as
  `Godot G-13 Browser Build, Performance, and Regression Hardening`.
- `SOURCE_BRANCH` is `codex/g-13-browser-build-hardening`.
- `validate_vertical_slice.gd` enforces the G-13 review identity while retaining
  the existing G-4.21/G-4.22/G-4.22R HUD and atelier runtime asset gates.
- `tools/package_itch_web.sh` now fails packaging if `BUILD_PHASE`,
  `BUILD_LABEL`, or `SOURCE_BRANCH` drift from the active G-13 review package.

## Browser-Review ZIP

The deterministic web package route passed after invoking Git Bash with the
Godot executable path quoted safely for `C:\Users\Chris\Documents\New project`.

Generated artifacts:

- `wayfarer_godot_vertical_slice/artifacts/wayfarers-tale-godot-web.zip`
- `wayfarer_godot_vertical_slice/artifacts/wayfarers-tale-godot-g-13-browser-build-performance-and-regression-hardening.zip`

Package checks:

- `index.html` is at ZIP root.
- `web_build/index.html` is absent.
- Required Godot web files are present:
  `index.html`, `index.js`, `index.pck`, `index.wasm`,
  `index.audio.worklet.js`, and `index.audio.position.worklet.js`.
- Stable ZIP size: 103M.
- Versioned ZIP size: 103M.

## Runtime Screenshot Regression

G-13 reused the G-12 recurring screenshot route as the browser-regression proof
set, because this phase is hardening the review route rather than adding a new
visual feature slice.

Fresh capture output:

- `wayfarer_godot_vertical_slice/artifacts/review/g12_runtime_screenshots/g12_runtime_screenshot_manifest.json`
- 15 PNG proof frames from wide normal gameplay through debug-off proof and
  contact/provenance proof.

Spot-checked frames:

- `g12_01_wide_newport_normal_gameplay_view.png`
- `g12_10_player_interacting_at_tavern_rumor_location.png`
- `g12_14_debug_overlays_disabled.png`

Screenshot review result: PASS for G-13 build/regression scope. The frames show
the harbor-town route still renders, dialogue and journal surfaces remain
readable, no debug overlays are visible in the debug-off proof, and normal
runtime sprites remain atelier/provenance-gated.

## Validation

Passed locally:

- Godot 4.6.2 import via package route.
- Godot `validate_vertical_slice.gd`.
- `validate_browser_build_hardening.py`.
- `validate_first_session_playability.py`.
- `validate_opening_quest_arc.py`.
- `validate_interaction_ux.py`.
- `validate_living_town_rhythm.py`.
- `validate_audio_atmosphere_hooks.py`.
- `validate_runtime_atelier_asset_consistency.py`.
- `validate_starter_village_layout_source_usage.py`.
- `validate_newport_visual_ordering.py`.
- `validate_sv0_tooling_stack.py`.
- `validate_sv0_tool_acquisition_manifest.py`.
- `validate_starter_village_roadmap.py`.
- `validate_starter_village_execution_ledger.py`.

## Technical Versus Design Acceptance

Technical validation: PASS. G-13 proves the browser build/package/regression
route is stable enough for PR review.

Design acceptance: limited to G-13 hardening scope. Chris's May 2026 OVI-1
addendum supersedes the old human-stop language: G-14 is now an internal
Starter Village proof checkpoint, must record `Human review required: no`, and
continues to `G-15 Opening Island Masterplan + World Topology` if it passes.
The next true human review milestone is OVI-1.

## Current Council Status

Agent Council report:
`docs/reports/G13_BROWSER_BUILD_AGENT_COUNCIL_REPORT.md`

Final Authority Verdict: `COUNCIL_PASS_READY_FOR_PR`
