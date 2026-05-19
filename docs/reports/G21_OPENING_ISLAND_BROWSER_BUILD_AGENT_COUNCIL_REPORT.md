# G-21 Browser Build Agent Council Report

Branch: `codex/g-21-opening-island-performance-browser-build-regression-hardening`

Phase: G-21 Opening Island Performance, Browser Build, and Regression Hardening

Human review required: no

Final verdict: `COUNCIL_PASS_READY_FOR_PR`

## Council Result

The council reviewed G-21 as a release/readiness gate for the current Newport
and opening island experience. The phase is allowed to pass because the active
browser build identity is current, the package route produces review-safe ZIPs,
the exported build loads in a browser canvas with no warning/error console log,
and the proof remains tied to the G-19R/G-19S/G-20 source chain.

## Council Roles

| Role | Result | Harsh-critic finding |
|---|---:|---|
| Scrum Master | PASS | G-21 is correctly sequenced after the merged G-20 pass and must continue to G-22 rather than stop for Chris. |
| World-Class Game Designer | PASS | This phase does not add gameplay, but it protects the first-session loop from stale review-build identity and browser delivery failure. |
| World/Layout Designer | PASS | No ad hoc Newport layout edits were made; G-19R/G-19S remain the placement authority. |
| Level Designer | PASS | Browser proof loads the current wharf/objective surface, so the first-session route remains accessible for review. |
| Art Director | PASS | No placeholder art or visual clutter was added; the proof shows existing atelier-standard runtime presentation. |
| Narrative/Quest Designer | PASS | G-20's journal/objective hook remains visible in the loaded browser surface. |
| Animation/NPC Behavior Director | PASS | G-21 makes no new NPC motion claims; motion proof remains deferred to the relevant runtime and OVI-1 gates. |
| UX Designer | PASS | HUD and journal text render in-browser without debug overlays or stale build metadata. |
| Game Programmer | PASS | BuildInfo, package drift protection, vertical-slice identity checks, and browser hardening validator are current. |
| QA Analyst | PASS | The phase requires ZIP inspection, browser canvas proof, console-log proof, roadmap/ledger validation, asset hygiene, and Agent Council validator execution. |
| Build/Release Engineer | PASS | The generated stable and versioned G-21 ZIPs have root `index.html`, no `web_build/index.html`, required Godot web files, matching hashes, and ignored generated outputs. |

## Harsh-Critic Questions

Would this impress a first-time player?

Not by itself, and the council does not pretend otherwise. G-21 passes because
it makes the browser review route trustworthy for the G-19R/G-19S/G-20 player
experience that OVI-1 will judge.

Would this hold up against top-tier RPG/MMORPG starter-zone expectations?

For build delivery, yes. The exported build loads into live Newport gameplay
with HUD/journal context and no browser warning/error log. The final playable
experience still belongs to G-22.

Does the player understand where they are and what to do?

The loaded browser proof shows `Working Wharf Apron`, the player HUD, and the
First Light journal objective routing the player along the harborfront road to
Edrin Vale at the Counting House.

Does the screenshot prove the claim?

Yes for G-21 scope: the loader proof shows the exported Godot app booting, and
the loaded proof shows the runtime canvas rendering actual Newport gameplay in
the browser.

Are we hiding behind validators?

No. The validator now requires the browser proof manifest, loaded gameplay
screenshot, console log, ZIP shape, current BuildInfo identity, and roadmap
ledger continuation.

Is human review required?

No. There is no creative fork, paid-tool blocker, auth failure, unsafe
operation, or asset provenance blocker.

## Scores

| Score | Value |
|---|---:|
| Build/review readiness score | 8.8 |
| Technical stability score | 8.8 |
| Regression governance score | 8.7 |
| UX readability in browser score | 8.6 |
| North Star protection score | 8.6 |
| Implementation-readiness score | 8.8 |

## Required Proof

- Build identity: `wayfarer_godot_vertical_slice/scripts/BuildInfo.gd`
- Package route: `wayfarer_godot_vertical_slice/tools/package_itch_web.sh`
- Validator: `wayfarer_godot_vertical_slice/tools/validate_browser_build_hardening.py`
- Proof manifest: `wayfarer_godot_vertical_slice/artifacts/review/g21_browser_build_hardening/g21_browser_build_hardening_manifest.json`
- Loader screenshot: `wayfarer_godot_vertical_slice/artifacts/review/g21_browser_build_hardening/g21_browser_review_identity_proof.jpg`
- Loaded browser screenshot: `wayfarer_godot_vertical_slice/artifacts/review/g21_browser_build_hardening/g21_browser_review_loaded_surface.jpg`
- Browser console log: `wayfarer_godot_vertical_slice/artifacts/review/g21_browser_build_hardening/g21_browser_review_loaded_console_log.json`
- Agent Council tool report: `docs/reports/G21_WAYFARER_AGENT_COUNCIL_TOOL_RUN.md`
- Runtime regression capture: `wayfarer_godot_vertical_slice/tools/capture_g20_first_session_gameplay_loop_screenshots.ps1`
- Stable ZIP: `wayfarer_godot_vertical_slice/artifacts/wayfarers-tale-godot-web.zip`
- Versioned ZIP: `wayfarer_godot_vertical_slice/artifacts/wayfarers-tale-godot-g-21-opening-island-performance-browser-build-and-regression-hardening.zip`

## Verdict

`COUNCIL_PASS_READY_FOR_PR`

G-21 can proceed to PR after validators and Agent Council tool execution pass.
After merge, continue immediately to G-22 OVI-1 Opening Village + Island
Production Playable Gate.
