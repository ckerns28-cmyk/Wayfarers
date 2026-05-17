# G-4.21 Origin City Hero Slice

Status: `COUNCIL_PASS_READY_FOR_PR` under the autonomous pre-G-5 production protocol.

G-4.21 composes the accepted Newport street/dock layout, G-4.18E prop family, G-4.19 player visual identity foundation, and G-4.20 HUD into the first origin city hero-slice screenshot packet.

## Scope

- Hero-slice framing: normal HUD, clean no-HUD, close-up street/dock, Tavern/Inn to harbor, player/HUD/world cohesion, and wide Newport readability.
- Runtime systems: no inventory, combat, save, quest-system, NPC, or map expansion work.
- Provenance: this pass does not promote yellow or AI-assisted candidate assets to final commercial status.
- Review authority: screenshots must be inspected by the Agent Council before PR readiness.

## Completion Result

G-4.21 passed automated validation, runtime screenshot capture, council screenshot inspection, and the Agent Council final authority verdict. Human visual review is not required for this ordinary pre-G-5 phase.

## Validation Result

- PASS: Godot import validation.
- PASS: Vertical slice validation, including G-4.21 hero-slice composition checks.
- PASS: Newport provenance validation.
- PASS: Retained G-4.18E hero asset-family validation.
- PASS: Retained G-4.19 player identity validation.
- PASS: Retained G-4.21A non-mutating extraction validation.
- PASS: G-4.21 runtime screenshot capture.
- PASS: Python compile checks.
- PASS: `git diff --check`.
- PASS: Agent Council report with final authority verdict `COUNCIL_PASS_READY_FOR_PR`.

## Evidence Package

- Screenshot wrapper: `wayfarer_godot_vertical_slice/tools/capture_g421_runtime_screenshots.ps1`.
- Screenshot script: `wayfarer_godot_vertical_slice/tools/capture_g421_runtime_screenshots.gd`.
- Screenshot output: `wayfarer_godot_vertical_slice/artifacts/review/g421_runtime_screenshots/`.
- Council report: `docs/reports/G421_ORIGIN_CITY_HERO_SLICE_AGENT_COUNCIL_REPORT.md`.

## Council Verdict

- Final authority verdict: `COUNCIL_PASS_READY_FOR_PR`.
- Design score: 8.6/10.
- Art direction score: 8.6/10.
- World/layout score: 8.6/10.
- Gameplay/readability score: 8.7/10.
- Technical stability score: 8.8/10.
- Human escalation required: no.
- Next recommended phase: G-4.22 8.0 Visual Foundation Review Gate.
