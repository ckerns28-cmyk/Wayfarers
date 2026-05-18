# Starter Village Tooling Stack

This is the locked SV-0 production stack for the Starter Village roadmap. It
exists because screenshots proved that prior reports could pass while Newport
still looked patchy, scattered, or incorrectly authored.

## Locked Stack

| Need | Adopted Stack |
| --- | --- |
| World/layout source of truth | Repo-local `StarterVillageWorldLayout v1` JSON |
| District/lot/road planning | Godot-native schema plus validators |
| NPC route authoring | Route/station data in world-layout JSON |
| Dialogue/quest authoring | Repo-local quest/dialogue JSON and GDScript systems |
| NPC animation/movement validation | Godot built-in animation/navigation foundations plus motion-proof manifest |
| Visual screenshot regression | Godot screenshot capture plus visual-regression manifest |
| Runtime movement proof | Timestamped Godot frame sequences |
| Unit/integration testing | Existing Godot command-line and Python validators |
| Asset cleanup/contact sheets | Current Python/Pillow extraction and contact-sheet pipeline |
| Ground/material cohesion | Godot-native ground material taxonomy |
| Camera/first impression | Camera2D plus authored viewpoints |

## Authoritative Files

- `docs/reports/SV0_FREE_TOOLING_INTAKE_PRODUCTION_STACK_LOCK.md`
- `docs/reports/SV0_FREE_TOOLING_INTAKE_PRODUCTION_STACK_LOCK.json`
- `docs/reports/SV0_TOOL_ACQUISITION_MANIFEST.md`
- `docs/reports/SV0_TOOL_ACQUISITION_MANIFEST.json`
- `wayfarer_godot_vertical_slice/data/world_layout/starter_village_world_layout_v1.json`
- `wayfarer_godot_vertical_slice/data/visual_qa/starter_village_visual_regression_manifest_v1.json`
- `wayfarer_godot_vertical_slice/data/movement_proof/starter_village_movement_proof_manifest_v1.json`
- `wayfarer_godot_vertical_slice/data/ground_materials/starter_village_ground_material_stack_v1.json`
- `wayfarer_godot_vertical_slice/tools/validate_sv0_tooling_stack.py`
- `wayfarer_godot_vertical_slice/tools/validate_sv0_tool_acquisition_manifest.py`

## Production Rules

- Layout phases must start from district, route, lot, and anchor data.
- Props are placed last and never used to hide ground or street failures.
- Dialogue and quest content must remain data-driven and validator-visible.
- Movement phases must produce motion proof, not still screenshots only.
- Visual regression checks are warnings; council art/world judgment still rules.
- Screenshot contradictions force repair on the branch.
- New external tools stay spike-only until license, CI, rollback, and web/review build safety are proven.

## External Tool Policy

External tools are not rejected forever. They are simply not allowed to become
runtime or roadmap dependencies until a spike proves they are free,
license-safe, portable, validateable, and reversible.

The Tool Acquisition Manifest is the standing intake record. Codex may
download, install, configure, and use free, license-safe, reversible tools for
autonomous Starter Village roadmap execution when the tool is documented in the
manifest, requires no payment or paid trial, stores no credentials/secrets, has
a rollback path, and installs only in approved project/tool locations.

Preferred install locations if a later spike is approved:

- Portable tools: `D:/Wayfarer/tools`
- Godot addons: `wayfarer_godot_vertical_slice/addons`

No SV-0 step authorizes deleting, moving, or modifying unrelated external-drive
files, old files, photos, or non-Wayfarer folders.
