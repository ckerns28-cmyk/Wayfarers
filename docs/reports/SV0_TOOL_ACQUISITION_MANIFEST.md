# SV-0 Tool Acquisition Manifest

Phase: `SV-0`

Branch: `codex/g-7a-tool-backed-layout-repair`

Purpose: record every free tool, addon, package, and repo-local production
system evaluated for Starter Village authoring and QA after Chris authorized
free, license-safe, reversible tooling intake.

## Acquisition Result

No paid tools were used. No paid trials were started. No payment information was
entered. No Google/browser credentials were used. No credentials, cookies,
tokens, or secrets were stored. No tools were downloaded or installed outside
the repository during this addendum pass.

The current locked stack remains intentionally conservative:

- repo-local world/layout source of truth,
- repo-local quest/dialogue data,
- Godot built-in movement, animation, camera, and command-line test support,
- Godot screenshot and frame-sequence proof,
- Python/Pillow atelier extraction and contact-sheet review,
- repo-local validators and Agent Council gates.

External free tools remain available for documented spikes only when they prove
license safety, CI usefulness, web/review build safety, and rollback clarity.

## Category Decisions

| Category | Decision | Adopted now |
| --- | --- | --- |
| World / Map / District Authoring | `ADOPT_NOW` | Godot-native StarterVillageWorldLayout schema |
| Dialogue / Quest Authoring | `ADOPT_NOW` | Wayfarer data-driven quest/dialogue JSON |
| NPC Movement / Animation Foundation | `ADOPT_NOW` | Godot built-ins plus custom route data |
| Automated Visual QA | `ADOPT_NOW` | Godot screenshots plus repo-local visual QA validators |
| Runtime Movement Proof | `ADOPT_NOW` | Godot frame-sequence capture proof |
| Godot Unit / Integration Testing | `ADOPT_NOW` | Godot command-line and Python integration validators |
| Art Cleanup / Animation Review | `ADOPT_NOW` | Python/Pillow extraction and contact sheets |
| Ground / Material Cohesion | `ADOPT_NOW` | Godot-native ground material taxonomy and atelier sheets |
| Camera / First Impression Polish | `ADOPT_NOW` | Godot-native Camera2D and authored viewpoints |

## Deferred Or Spike-Only Tools

The following free tools were evaluated but not made dependencies of the current
roadmap pass: LDtk, Tiled, Dialogue Manager, Dialogic, LimboAI, Playwright,
pixelmatch, SSIM/scikit-image, FFmpeg, OBS Studio, GUT, Pixelorama, LibreSprite,
Krita, Material Maker, TileSet/TileMapLayer migration, and Phantom Camera.

The reason is not reluctance to use tools. It is production discipline: no
external tool becomes required until it is proven free, license-safe, reversible,
CI-visible, and harmless to Godot web/review export.

## Validation

Validator:

`wayfarer_godot_vertical_slice/tools/validate_sv0_tool_acquisition_manifest.py`

The validator fails if an adopted tool lacks license/free/install/rollback/source
data, if any adopted tool requires payment or stores credentials, if a required
SV-0 category lacks a decision, or if a deferred tool is marked required by later
validators.

Structured manifest:

`docs/reports/SV0_TOOL_ACQUISITION_MANIFEST.json`
