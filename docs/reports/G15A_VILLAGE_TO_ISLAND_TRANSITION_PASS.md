# G-15A Village-to-Island Transition Pass

Date: 2026-05-18

Branch: `codex/g-15a-village-island-transition`

Starting main commit: `019458be2ceaba569c4b156ea397809fcb704b33`

## Purpose

G-15A makes leaving Newport feel intentional and exciting. It implements a
readable east-gate threshold, a settlement-to-island boundary, an outskirt lane,
and the first old-road mystery beat beyond the village.

Transition source:
`wayfarer_godot_vertical_slice/data/world_layout/village_to_island_transition_v1.json`

Topology source:
`wayfarer_godot_vertical_slice/data/world_layout/opening_island_world_topology_v1.json`

Runtime screenshot manifest:
`wayfarer_godot_vertical_slice/artifacts/review/g15a_runtime_screenshots/g15a_runtime_screenshot_manifest.json`

## Runtime Implementation

- Newport world bounds now support the opening island transition footprint.
- Route rectangles extend the walkable graph from the village edge to the first island lane.
- `opening_island_transition_contract()` exposes the phase source, route rects, viewpoints, walkable samples, and threshold story beats.
- Map rendering adds cohesive outskirt ground, an eastward dirt route, fenced threshold details, lantern/marker cues, and an old-road cache.
- Runtime screenshot automation captures clean no-HUD/no-debug proof of the village exit, island entry threshold, first mystery beyond town, and debug-overlay-disabled transition.

## Acceptance

| Criterion | Result |
| --- | --- |
| Clear town exit | PASS |
| Readable trail/road out of Newport | PASS |
| Settlement-to-island boundary | PASS |
| Environmental storytelling at threshold | PASS |
| First sense of mystery beyond town | PASS |
| Player knows where to go next | PASS |
| Transition feels natural | PASS |
| World opens without confusion | PASS |
| No invisible wall / random edge feeling | PASS |

## Scores

| Discipline | Score |
| --- | --- |
| Design | 8.6 |
| World/layout | 8.6 |
| Art direction | 8.6 |
| UX/readability | 8.6 |
| Technical stability | 8.7 |

## Screenshot Proof

- `wayfarer_godot_vertical_slice/artifacts/review/g15a_runtime_screenshots/g15a_01_village_exit_to_island.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g15a_runtime_screenshots/g15a_02_island_entry_transition.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g15a_runtime_screenshots/g15a_03_first_mystery_beyond_town.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g15a_runtime_screenshots/g15a_04_debug_overlays_disabled.png`

## Validation

- `capture_g15a_runtime_screenshots.ps1`: PASS
- `validate_village_to_island_transition.py`: PASS
- `validate_island_world_topology.py`: PASS
- `validate_opening_village_island_roadmap.py`: PASS
- `validate_opening_village_island_execution_ledger.py`: PASS
- `validate_vertical_slice.gd`: PASS
- `git diff --check`: PASS
- `git diff --cached --check`: PASS

## Council Result

Agent Council verdict: `COUNCIL_PASS_READY_FOR_PR`

Human review required: no

Reason: G-15A is an ordinary autonomous OVI-1 implementation checkpoint.

Next phase: G-15B Island Terrain, Ground, and Route Cohesion
