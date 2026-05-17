# G-4.20 HUD/UI Visual Redesign

Status: `COUNCIL_PASS_READY_FOR_PR` under the autonomous pre-G-5 production protocol.

G-4.20 replaces the default debug-heavy HUD presentation with a restrained fantasy/MMORPG interface that belongs beside the accepted Newport streets, props, and G-4.19 player identity foundation.

## Scope

- Player-facing HUD: compact Wayfarer identity, Newport region label, level/status text, health and resolve bars, and a top-right quest panel.
- Review metadata: build label, phase/host, channel, branch, and production note remain available through the existing review metadata toggle but are hidden by default.
- Interaction UI: dialogue and prompt presentation are restyled to match the brass/parchment/harbor palette.
- Screenshot support: normal HUD captures and clean no-HUD captures are preserved through a G-4.20 runtime capture script.
- Non-goal: no inventory, combat, quest system, save, NPC, or progression mechanics were added.

## Completion Bar

G-4.20 passed its completion bar. Automated validation, runtime screenshot capture, council screenshot inspection, and the Agent Council final authority verdict all passed.

## Validation And Council Result

- Godot import validation: PASS.
- Vertical slice validation, including G-4.20 HUD contract checks: PASS.
- Newport provenance validation: PASS.
- Retained G-4.18E hero asset-family validation: PASS.
- Retained G-4.19 player identity validation: PASS.
- Retained G-4.21A non-mutating extraction validation: PASS.
- G-4.20 runtime screenshot capture: PASS, 6 required frames.
- Python compile checks: PASS.
- `git diff --check` and `git diff --cached --check`: PASS.
- Agent Council report: `docs/reports/G420_HUD_UI_VISUAL_REDESIGN_AGENT_COUNCIL_REPORT.md`.
- Final authority verdict: `COUNCIL_PASS_READY_FOR_PR`.
- Human escalation required: NO.
- Next recommended roadmap phase: G-4.21 Origin City Hero Slice.

## Evidence Package

- HUD scene: `wayfarer_godot_vertical_slice/scenes/ui/HUD.tscn`.
- HUD script: `wayfarer_godot_vertical_slice/scenes/ui/HUD.gd`.
- Screenshot wrapper: `wayfarer_godot_vertical_slice/tools/capture_g420_runtime_screenshots.ps1`.
- Screenshot script: `wayfarer_godot_vertical_slice/tools/capture_g420_runtime_screenshots.gd`.
- Screenshot output: `wayfarer_godot_vertical_slice/artifacts/review/g420_runtime_screenshots/`.
- Council report: `docs/reports/G420_HUD_UI_VISUAL_REDESIGN_AGENT_COUNCIL_REPORT.md`.
