# Pre-G-5 Roadmap Execution Ledger

Starting main commit: `38b89d92e77bf260e6fb551e6756880920e7ae08`

Gate state: G-5 readiness is reopened. A merged PR or previous council report is no longer enough when runtime screenshot evidence contradicts the player-facing result. G-5 readiness may pass only when every ledger row is `PASS` and the active runtime hero slice has atelier-traceable player, NPC, marker/sign, and world sprite evidence.

Allowed row statuses:

- `PASS`
- `FAIL_NEEDS_CODE_FIX`
- `UNPROVEN_NEEDS_EVIDENCE_OR_REPAIR`
- `BLOCKED_REQUIRES_HUMAN_ESCALATION`

Deprecated final states are not allowed for this ledger.

## Ledger Summary

| Phase | Roadmap Item | PR | Merge/Commit Evidence | Current Status | Reason |
| --- | --- | --- | --- | --- | --- |
| G-4.23B | Newport Authored Street + Harbor Immersion Repair | #452 | `c184b48` | PASS | Layout, street grammar, harborfront, district logic, screenshots, validator proof, and council report exist. Character-placeholder residue later found in screenshots is repaired by G-4.22R. |
| G-4.18E | Green-Origin Hero-Quality Asset Family | #454 | `1c556ecf007fe4a141b963113aceacb3df8a68b7` | PASS | Asset family evidence includes prompts, source sheets, manifests, contact sheets, runtime placement, screenshots, validation, provenance, and council proof. |
| G-4.19 | Player Visual Identity Foundation | #455 | `818c4233c63796aec84fe9bdb21445264a3dac6d` | PASS | Original phase evidence exists, but active runtime player art is superseded by G-4.22R because screenshot QA found the former look below the active atelier bar. |
| G-4.20 | HUD/UI Visual Redesign | #456 | `61f15441fece8dd834fd034d4734b3377303315c` | PASS | HUD screenshots, validator proof, clean no-HUD capture, metadata toggle, and council proof exist. |
| G-4.21 | Origin City Hero Slice | #457 | `ca2170311c205cde4034dd3c4abd122cd3d4a86e` | PASS | Hero-slice proof exists, with active runtime sprite consistency now guarded by G-4.22R. |
| G-4.22 | Visual Foundation Review Gate | #458 | `38b89d92e77bf260e6fb551e6756880920e7ae08` | PASS | Original pass was reopened as a false positive; it is only treated as PASS when combined with the G-4.22R repair evidence. |
| G-4.22R | Roadmap Execution Ledger And Pre-G-5 Atelier Consistency Gate Repair | pending remediation PR | working tree from `38b89d92e77bf260e6fb551e6756880920e7ae08` | PASS | Fix-forward branch adds the ledger gate, runtime asset consistency validator, painterly player/NPC atlas replacement, screenshot proof, and final council audit before PR merge. |

Structured ledger source: `docs/reports/PRE_G5_ROADMAP_EXECUTION_LEDGER.json`

## Earliest Reopened Failure

Earliest failed/unproven current gate item after Chris's screenshot evidence: `G-4.19 Player Visual Identity Foundation` as active runtime presentation, because the player/NPC visual language no longer met the atelier standard beside the G-4.18E/G-4.21/G-4.22 environment. The original phase remains historical implementation evidence; active runtime acceptance is repaired in `G-4.22R`.

## Required Current G-4.22R Proof Screenshots

- `wayfarer_godot_vertical_slice/artifacts/review/g422r_runtime_screenshots/g422r_01_wide_newport_normal_gameplay_view.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g422r_runtime_screenshots/g422r_02_player_near_tavern_inn_district.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g422r_runtime_screenshots/g422r_03_player_near_commercial_avenue.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g422r_runtime_screenshots/g422r_04_player_at_harbor_dock_edge.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g422r_runtime_screenshots/g422r_05_player_near_npcs.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g422r_runtime_screenshots/g422r_06_player_near_props_signs_markers.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g422r_runtime_screenshots/g422r_07_player_near_layered_y_sort_objects.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g422r_runtime_screenshots/g422r_08_gameplay_zoom_readability_proof.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g422r_runtime_screenshots/g422r_09_debug_overlays_disabled_proof.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g422r_runtime_screenshots/g422r_10_player_npc_contact_sheet_proof.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g422r_runtime_screenshots/g422r_11_marker_sign_world_object_contact_sheet_proof.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g422r_runtime_screenshots/g422r_12_wider_town_cohesion_no_placeholder_mix.png`

## Gate Rule

`wayfarer_godot_vertical_slice/tools/validate_pre_g5_roadmap_ledger.py` must fail if any required pre-G-5 phase row is missing, not `PASS`, lacks implementation evidence, lacks screenshot proof for visual/player-facing work, lacks council evidence, lacks provenance evidence for asset/player/NPC/world work, or lacks runtime sprite traceability through the G-4.22R validator.
