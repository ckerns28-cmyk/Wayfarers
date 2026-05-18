# G-7C Landmark and District Identity Pass

Phase status: `PASS`

Branch: `codex/g-7c-landmark-district-identity`

Council verdict: `COUNCIL_PASS_READY_FOR_PR`

## Purpose

G-7C makes the village more memorable by strengthening the Tavern/Inn centerpiece, Counting House civic notice anchor, commercial shop row, harbor work area, rear service lane, residential edge, and small civic notice-board location.

This is not SV-1 completion. G-8 next must fix the known player/NPC hover-glide risk with grounded movement states.

## Runtime Changes

- Added G-7C runtime and blueprint contract markers.
- Added atelier-safe district identity placements for the Tavern/Inn threshold, civic notice anchor, commercial row, harbor work landmark, rear service lane, and residential edge.
- Reused accepted G-4.18E, town identity, and environmental grounding atlases.
- Kept crude/debug marker assets hidden from normal play.
- Preserved clear movement routes around all landmark props.

## Screenshot Evidence

Runtime screenshot manifest:
`wayfarer_godot_vertical_slice/artifacts/review/g7c_runtime_screenshots/g7c_runtime_screenshot_manifest.json`

Council-inspected frames:

- `g7c_01_wide_newport_normal_gameplay_view.png`: PASS for landmark/district read.
- `g7c_04_player_near_tavern_inn.png`: PASS for Tavern/Inn centerpiece and rumor-threshold identity.
- `g7c_05_commercial_avenue.png`: PASS for commercial row and harbor-commerce identity.
- `g7c_09_counting_house_interaction_area.png`: PASS for Counting House civic notice anchor.
- `g7c_12_signs_markers_interaction_ux_area.png`: PASS for civic notice location without crude debug markers.
- `g7c_14_debug_overlays_disabled.png`: PASS for normal-play proof.

## Validation Results

| Check | Result |
| --- | --- |
| Godot import validation | PASS |
| Vertical slice validator | PASS |
| G-7C screenshot capture and PNG verification | PASS |
| Newport world cohesion validator | PASS |
| Interaction UX validator | PASS |

## Phase Scores

| Category | Score |
| --- | --- |
| art/world score: 8.5 | PASS |
| Design score | 8.5/10 |
| Art direction score | 8.5/10 |
| World/layout score | 8.5/10 |
| UX/readability score | 8.5/10 |
| Technical stability score | 8.8/10 |
| Performance/build score | 8.7/10 |
| Town cohesion score | 8.0/10 |

## Council Finding

G-7C passes because the town now has a stronger landmark hierarchy. The Tavern/Inn reads as a social centerpiece, the Counting House has an official civic notice anchor, commerce and harbor work are visually distinct, the rear service lane has its own identity, and the residential edge has lived-in grounding.

The council does not certify SV-1. NPC movement still requires G-8, the opening quest remains future work, and first-session pacing is not yet proven.

G-8 next: replace hover/glide risks with grounded idle, walk, facing, stop/start, pathing, and shadow treatment.
