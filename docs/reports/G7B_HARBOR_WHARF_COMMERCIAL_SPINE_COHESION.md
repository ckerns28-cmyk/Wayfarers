# G-7B Harbor, Wharf, and Commercial Spine Cohesion

Phase status: `PASS`

Branch: `codex/g-7b-harbor-commercial-spine`

Council verdict: `COUNCIL_PASS_READY_FOR_PR`

## Purpose

G-7B makes the harbor read as Newport's economic engine instead of a decorative waterfront. The runtime pass turns the wharf into a working waterfront with purpose-grouped labor zones and a commercial avenue connected to harbor labor.

This is not the SV-1 finish line. The town still needs stronger landmark identity, grounded character motion, diegetic interaction UX, and the playable opening quest arc.

## Runtime Changes

- Added G-7B runtime contract constants to `MapLayer.gd` and `NewportTownBlueprint.gd`.
- Added functional wharf work-zone surfaces for fish offload, manifest cargo, rope/mooring service, and storehouse queue activity.
- Added trade-route traces from wharf labor to market, merchant frontage, and counting-house records.
- Added provenance-safe G-4.18E harbor/commercial atlas placements for fish baskets, cargo stacks, rope coils, bollards, lantern service, market goods, barrel queues, and net drying.
- Kept the main harborfront, wharf boardwalk, and counting-house route visually readable and unblocked.

## Screenshot Evidence

Runtime screenshot manifest:
`wayfarer_godot_vertical_slice/artifacts/review/g7b_runtime_screenshots/g7b_runtime_screenshot_manifest.json`

Council-inspected frames:

- `g7b_01_wide_newport_normal_gameplay_view.png`: PASS for broad harbor/commercial spine read.
- `g7b_03_route_to_counting_house.png`: PASS for manifest-cargo route support.
- `g7b_05_commercial_avenue.png`: PASS for commercial avenue connected to harbor labor.
- `g7b_06_dock_wharf_work_area.png`: PASS for distinct fish, manifest, rope, and storehouse work zones.
- `g7b_11_objective_route_readability_area.png`: PASS for readable wharf-to-counting-house path.
- `g7b_14_debug_overlays_disabled.png`: PASS for normal-play proof without editor/debug guide overlays.

## Validation Results

| Check | Result |
| --- | --- |
| Godot import validation | PASS |
| Vertical slice validator | PASS |
| G-7B screenshot capture and PNG verification | PASS |
| Newport world cohesion validator | PASS |
| NPC population and routes validator | PASS |
| Runtime atelier asset consistency validator | PASS |

## Phase Scores

| Category | Score |
| --- | --- |
| harbor/world score: 8.5 | PASS |
| Design score | 8.5/10 |
| Art direction score | 8.5/10 |
| World/layout score | 8.5/10 |
| UX/readability score | 8.3/10 |
| Technical stability score | 8.8/10 |
| Performance/build score | 8.7/10 |
| Town cohesion score | 7.8/10 |

## Council Finding

G-7B passes because the harbor now has an authored labor grammar: fish offload to market, manifest cargo to counting house, rope/mooring service to chandlery/storehouse, and market transfer to the commercial avenue. Dock objects support function rather than random scatter, and they do not block or confuse navigation in the inspected runtime screenshots.

G-7C next: make the village memorable by strengthening Tavern/Inn, counting house, commercial row, harbor work, rear service lane, residential edge, and civic notice-board identity.
