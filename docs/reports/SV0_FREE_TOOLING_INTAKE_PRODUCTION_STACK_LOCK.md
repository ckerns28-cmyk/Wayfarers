# SV-0 Free Tooling Intake Production Stack Lock

Phase: `SV-0`

Branch: `codex/sv0-free-tooling-stack`

Purpose: lock a free, safe, validated production stack before continuing the
Starter Village roadmap. The stack is meant to make screenshots harder to fool,
layout authoring less random, NPC movement provable, and council acceptance more
grounded in runtime evidence.

## Executive Decision

SV-0 adopts repo-local, Godot-native production tooling first.

No paid tools were added. No unknown-license tools were added. No external
drive contents, old files, or photos were moved or modified. No Godot addon was
installed. External tools remain spike-only or deferred until they prove license,
CI, web/review build, and rollback safety.

Primary locked sources:

- `wayfarer_godot_vertical_slice/data/world_layout/starter_village_world_layout_v1.json`
- `wayfarer_godot_vertical_slice/data/visual_qa/starter_village_visual_regression_manifest_v1.json`
- `wayfarer_godot_vertical_slice/data/movement_proof/starter_village_movement_proof_manifest_v1.json`
- `wayfarer_godot_vertical_slice/data/ground_materials/starter_village_ground_material_stack_v1.json`
- `docs/reports/SV0_FREE_TOOLING_INTAKE_PRODUCTION_STACK_LOCK.json`

## Category Decisions

| Category | Decision | Locked Tool |
| --- | --- | --- |
| World / Map / District Authoring | `ADOPT_NOW` | Wayfarer Godot-native `StarterVillageWorldLayout v1` |
| Dialogue / Quest Authoring | `ADOPT_NOW` | Wayfarer data-driven quest/dialogue JSON |
| NPC Movement / Animation Foundation | `ADOPT_NOW` | Godot built-in navigation/animation classes plus route JSON |
| Automated Visual QA | `ADOPT_NOW` | Godot screenshot capture plus visual-regression manifest |
| Runtime Movement Proof | `ADOPT_NOW` | Godot timestamped frame-sequence proof |
| Godot Unit / Integration Testing | `ADOPT_NOW` | Godot command-line integration validators |
| Art Cleanup / Animation Tools | `ADOPT_NOW` | Current Python/Pillow extraction and contact-sheet pipeline |
| Ground / Material Cohesion | `ADOPT_NOW` | Wayfarer Godot-native ground material stack |
| Camera / First Impression Polish | `ADOPT_NOW` | Godot-native Camera2D plus authored viewpoint data |

## External Tool Intake

| Tool | Decision | Reason |
| --- | --- | --- |
| LDtk | `SPIKE_ONLY` | Strong map/object authoring candidate, but importer and Godot 4.6.2 export safety must be proven before adoption. |
| Tiled | `DEFER` | Mature free editor, but import/export and GPL-toolchain isolation should be proven later. |
| Dialogue Manager | `SPIKE_ONLY` | Promising MIT dialogue addon; not needed before custom quest/dialogue data becomes limiting. |
| Dialogic | `DEFER` | Larger feature surface than SV-1 needs right now. |
| LimboAI | `DEFER` | Behavior trees are unnecessary before grounded route/idle movement exists. |
| Playwright | `SPIKE_ONLY` | Useful for G-13 browser/review route after web export is stable. |
| pixelmatch | `SPIKE_ONLY` | Useful warning diff later; not art-direction authority. |
| scikit-image / SSIM | `DEFER` | Heavier perceptual comparison, not needed before baseline warning checks. |
| FFmpeg | `SPIKE_ONLY` | Can convert frame sequences later if portable license mode is pinned. |
| OBS Studio | `DEFER` | Manual GUI capture is less reproducible than frame sequences. |
| GUT | `SPIKE_ONLY` | Good future Godot unit testing option, but current command-line validators already cover SV-1 contracts. |
| Pixelorama | `SPIKE_ONLY` | Useful manual sprite cleanup candidate if manifest-backed source edits need a dedicated editor. |
| LibreSprite | `DEFER` | Redundant with current pipeline and Pixelorama spike option. |
| Krita | `DEFER` | Too broad for immediate sprite-sheet QA gates. |
| Material Maker | `SPIKE_ONLY` | Possible future ground-texture source after taxonomy is locked. |
| Godot TileSet/TileMapLayer | `SPIKE_ONLY` | Candidate to replace hand-drawn ground patches after G-7A source-of-truth pass. |
| Phantom Camera | `DEFER` | Current Camera2D and authored viewpoints are sufficient until cohesion and NPC movement are stronger. |

## New Gate Rules

- Every future Starter Village phase must use the locked SV-0 stack where applicable.
- If a phase bypasses a required tool, the council must record why or fail.
- New one-off systems that duplicate locked stack responsibilities are failures unless explicitly justified.
- Visual diff can warn, but it cannot pass art direction.
- Screenshots can override reports.
- screenshots can override reports when captured evidence contradicts a written pass.
- Movement phases require motion proof: video, GIF, or timestamped frame sequence.
- G-7A and later layout work must begin from the world-layout source, not ad hoc coordinate sprawl.

## Validation

SV-0 validator:

`wayfarer_godot_vertical_slice/tools/validate_sv0_tooling_stack.py`

The validator checks that each tool category has a decision, adopted tools have
license/cost/version/install/rollback/provenance fields, deferred tools are not
required by later validators, and the required source-of-truth files exist.

## Source Notes

Primary public sources checked during intake include the official GitHub/docs
pages for LDtk, Tiled, Dialogue Manager, Dialogic, LimboAI, Playwright,
pixelmatch, FFmpeg, GUT, Pixelorama, LibreSprite, Material Maker, Phantom Camera,
and Godot documentation. The locked SV-0 stack does not depend on installing any
of them.

## Council Verdict

Final authority verdict: `COUNCIL_PASS_READY_FOR_PR`

Recommended next phase after merge: `G-7/G-7A tool-backed layout repair path`
with `SV-0` checks active before the next runtime layout pass.
