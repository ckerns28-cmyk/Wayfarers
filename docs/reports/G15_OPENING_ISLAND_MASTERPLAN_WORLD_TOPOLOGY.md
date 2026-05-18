# G-15 Opening Island Masterplan + World Topology

Date: 2026-05-18

Branch: `codex/g-15-opening-island-topology`

Starting main commit: `74f13668c2e70e7418e2317c0e1dc1a65f9c49bc`

## Purpose

G-15 designs the opening island as a coherent playable region, not a random
extension of Newport. It creates the authoritative topology source that later
terrain, POI, NPC, quest, UX, and browser-hardening phases must use.

Authoritative source:
`wayfarer_godot_vertical_slice/data/world_layout/opening_island_world_topology_v1.json`

Screenshot viewpoint manifest:
`wayfarer_godot_vertical_slice/data/visual_qa/g15_topology_screenshot_viewpoint_manifest.json`

G-15 is a topology/masterplan phase. Runtime island screenshots begin in the
transition and terrain implementation passes, then are regenerated fresh for the
G-22 OVI-1 proof package.

## Island Structure

The island is structured as:

1. safe village core
2. harbor edge
3. outskirts
4. farms/pastures or service lands
5. wooded paths
6. rocky coast or cove
7. old road / signal point / ruin / lookout
8. quest destination
9. optional secret
10. return path

## Authored Routes

| Route | Purpose |
| --- | --- |
| `village_to_signal_route` | The first readable path out of town toward a visible signal/overlook. |
| `signal_to_clue_route` | Converts tavern/counter-house mystery into physical evidence. |
| `cove_loop_route` | Adds optional coastal exploration without empty sprawl. |
| `return_to_newport_route` | Gives the player a clean return/report path after discovery. |

## Landmarks

- Harbor overlook / signal point
- Old road marker
- Hidden landing / cove remnant
- Return landmark visible from the route back to Newport

## Quest Topology

Whispers Before Dawn now has a planned island progression:

- island lead from tavern, counting house, or harbor
- village exit threshold
- wooded trail mystery
- old road marker confirmation
- physical evidence at the clue site
- optional secret cache
- return/report choice

## G-15 Acceptance

| Criterion | Result |
| --- | --- |
| Island reads as one authored place | PASS |
| Player understands how to leave town and explore | PASS |
| Routes loop naturally | PASS |
| No patchwork terrain | PASS |
| No meaningless empty sprawl | PASS |
| World/layout score | 8.6 |

## Validation

- `validate_island_world_topology.py`: PASS
- `validate_opening_village_island_roadmap.py`: PASS
- `validate_opening_village_island_execution_ledger.py`: PASS
- `g15_topology_screenshot_viewpoint_manifest.json`: PASS
- `git diff --check`: PASS
- `git diff --cached --check`: PASS

## Council Result

Agent Council verdict: `COUNCIL_PASS_READY_FOR_PR`

Next phase: G-15A Village-to-Island Transition Pass
