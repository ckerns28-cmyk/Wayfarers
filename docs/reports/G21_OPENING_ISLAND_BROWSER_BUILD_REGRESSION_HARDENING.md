# G-21 Opening Island Performance, Browser Build, and Regression Hardening

Branch: `codex/g-21-opening-island-performance-browser-build-regression-hardening`

Human review required: no

Council verdict: `COUNCIL_PASS_READY_FOR_PR`

## Purpose

G-21 hardens the combined Newport village and opening island review path after
G-20. This is not a new layout, quest, or sprite-placement phase. It proves that
the current source-driven opening can be exported, packaged, loaded in a browser
review surface, and regression-checked without stale build identity or hidden
web packaging failures before OVI-1.

## Review Build Identity

- `BuildInfo.gd` reports `BUILD_PHASE = G-21`.
- Visible build metadata labels the review build as
  `Godot G-21 Opening Island Performance, Browser Build, and Regression Hardening`.
- `SOURCE_BRANCH` is
  `codex/g-21-opening-island-performance-browser-build-regression-hardening`.
- `PLAYER_STYLE_ROADMAP_NOTE` now names the G-19R/G-19S/G-20 source-driven
  proof chain and the OVI-1 browser review route.
- `validate_vertical_slice.gd` enforces the G-21 review identity while retaining
  the existing atelier/runtime consistency gates.
- `tools/package_itch_web.sh` fails if the package build phase, label, or source
  branch drift from the active G-21 review package.

## Browser-Review ZIP

Generated review artifacts:

- `wayfarer_godot_vertical_slice/artifacts/wayfarers-tale-godot-web.zip`
- `wayfarer_godot_vertical_slice/artifacts/wayfarers-tale-godot-g-21-opening-island-performance-browser-build-and-regression-hardening.zip`

Package checks:

- `index.html` is at ZIP root.
- `web_build/index.html` is absent.
- Required Godot web files are present:
  `index.html`, `index.js`, `index.pck`, `index.wasm`,
  `index.audio.worklet.js`, and `index.audio.position.worklet.js`.
- Stable ZIP size: `107885759` bytes.
- Versioned ZIP size: `107885759` bytes.
- Stable and versioned SHA-256:
  `2726646EBCE3D7FC6E9D35E2AC02A4254AD633A1943B96145194A70BC3113BF8`.
- ZIP and `web_build/` outputs remain generated/ignored artifacts, not tracked
  source files.

## Browser Proof

Tracked proof manifest:

- `wayfarer_godot_vertical_slice/artifacts/review/g21_browser_build_hardening/g21_browser_build_hardening_manifest.json`

Browser proof artifacts:

- `wayfarer_godot_vertical_slice/artifacts/review/g21_browser_build_hardening/g21_browser_review_identity_proof.jpg`
- `wayfarer_godot_vertical_slice/artifacts/review/g21_browser_build_hardening/g21_browser_review_loaded_surface.jpg`
- `wayfarer_godot_vertical_slice/artifacts/review/g21_browser_build_hardening/g21_browser_review_loaded_console_log.json`

The browser route served `web_build/index.html` locally with COOP/COEP headers
matching the review-host requirement, loaded the Godot canvas at
`http://127.0.0.1:8766/index.html`, and captured the actual Newport gameplay
surface. The loaded surface shows the working wharf apron, player sprite, HUD
state, and journal objective in a browser canvas. Browser warning/error log:
`[]`.

## Regression Scope

G-21 does not claim the final OVI-1 review package. It hardens the route that
OVI-1 will use:

- G-19R source-of-truth Newport blockout remains the layout authority.
- G-19S runtime reconstruction remains the Newport placement authority.
- G-19 player guidance remains active in the runtime HUD/journal route.
- G-20 first-session gameplay and reward proof remains the quest/reward source.
- G-21 adds browser packaging identity, ZIP shape, browser load proof, and
  validator governance for the review build.

## Validation

Required local validation set:

- `wayfarer_godot_vertical_slice/tools/package_itch_web.sh`
- `python wayfarer_godot_vertical_slice/tools/validate_browser_build_hardening.py`
- `Godot --headless --path . --script res://tools/validate_vertical_slice.gd`
- `python wayfarer_godot_vertical_slice/tools/validate_opening_village_island_roadmap.py`
- `python wayfarer_godot_vertical_slice/tools/validate_opening_village_island_execution_ledger.py`
- `tools/validate_asset_hygiene.sh`
- `tools/wayfarer_agent_council.py --phase "G-21 Opening Island Performance, Browser Build, and Regression Hardening" --run-validators`
- `git diff --check`
- `git diff --cached --check`

Agent Council runtime screenshot regeneration intentionally reuses
`capture_g20_first_session_gameplay_loop_screenshots.ps1` as the current
canonical first-session regression set, while G-21 adds browser-specific proof
through `g21_browser_build_hardening_manifest.json`.

## Technical Versus Design Acceptance

Technical validation: PASS for the build/review route once the validator set is
green.

Design acceptance: PASS only for this hardening scope. The phase does not lower
the North Star or claim OVI-1 completion. It passes because a first-session
reviewer can load the current village/island build through the browser route
without stale metadata, ZIP nesting mistakes, missing core export files, or
browser-console failures.

## Acceptance

- Browser/review artifact is valid: PASS
- BuildInfo metadata is current: PASS
- Package script drift protection: PASS
- Web export ZIP root shape: PASS
- Browser canvas load proof: PASS
- Warning/error console log: PASS
- Generated artifacts remain ignored: PASS
- Regression chain from G-19R/G-19S/G-20 remains intact: PASS
- Human review required: no

## Harsh-Critic Result

The phase would fail if it only updated text labels, if the review ZIP nested
`web_build/`, if the browser route only showed a loader forever, if the console
reported blocking web errors, or if G-21 tried to bypass the G-19R/G-19S source
layout. The loaded browser proof and manifest clear this gate, but OVI-1 remains
the real playable review milestone.

Next phase: G-22 OVI-1 Opening Village + Island Production Playable Gate.
