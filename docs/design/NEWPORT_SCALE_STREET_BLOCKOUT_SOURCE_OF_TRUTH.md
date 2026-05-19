# Newport Scale + Street Blockout Source Of Truth

Phase: `G-19R Newport Scale + Street Blockout Source of Truth`

Status: `PASS`

Starting main commit: `6e8c5fc59c827d1b3adf84eb90a452c7092f4e57`

This is the mandatory design-source gate before further Newport runtime placement. It replaces code-first coordinate tuning with a measured, inspectable town plan that future Godot work must consume or validate against.

## Tooling Decision

Figma/FigJam was not used. The reason is practical: G-19R needed a repo-contained artifact set with no cloud-only dependency, no account friction, no payment path, and no credentials. The compatible planning artifact is:

- `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_measured_blockout.svg`
- `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_measured_blockout.png`
- machine-readable JSON plans in the same directory

## Browser Research Applied

- The Level Design Book flow guidance was used for movement, wayfinding, metrics, and the need to verify layout through blockout/playtest: https://book.leveldesignbook.com/process/layout/flow
- The Level Design Book critical path guidance was used for player start, exits, labeled beats, and route arrows: https://book.leveldesignbook.com/process/layout/criticalpath
- National Park Service Salem Maritime history was used for wharf, warehouse, custom-house, and port-trade logic: https://www.nps.gov/articles/000/history.htm
- Colonial Williamsburg tavern history was used to frame the tavern as a public/social/rumor/economic node: https://www.colonialwilliamsburg.org/discover/historic-area/historic-places/a-time-travelers-guide-to-early-american-taverns/
- National Park Service Annapolis material was used as a colonial seaport/planned-town precedent: https://www.nps.gov/stsp/learn/annapolis.htm

## Scale Derivation

The current player atlas alpha bounds are `27.2` world units wide after runtime scale. The current 3-tile Newport road band is `3.529` character widths, which is below the 10-15 character-width target for a main harbor/commercial street.

Selected G-19R targets:

- Main commercial/harbor street: `12.0` character widths, `326.4` world units.
- Secondary street: `7.5` character widths.
- Rear/service lane: `5.5` character widths.
- Alley/service cut-through: `3.5` character widths.
- Wharf working apron: `10.5` character widths.
- NPC route clearance: `2.5` character widths.

## Town Plan

Newport is planned as a 1700s-inspired harbor origin village with these authored districts:

- Harbor / wharf district: working arrival, cargo, dock clue, visible economy.
- Counting House / clerk district: official manifest pressure and first objective.
- Tavern / inn rumor hub: landmark social node and whisper network.
- Commercial avenue: storefront spine connecting tavern, clerk, market, and exit.
- Rear service lane: back-of-house route for deliveries, clues, and believable lots.
- Residential edge: homes for workers and clerks so the town is not only a shop row.
- Village-to-island exit: east threshold toward exploration.
- Civic notice board: in-world objective/journal anchor.
- Hidden rumor/clue route: optional service path between tavern/rear lane and wharf.

## Governance

After G-19R, all major Newport placement work must derive from:

- `docs/design/NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.json`
- `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_district_plan.json`
- `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_street_hierarchy.json`
- `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_lot_plan.json`
- `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_npc_route_plan.json`
- `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_quest_beat_locations.json`
- `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_camera_viewpoints.json`

Major runtime layout edits in `NewportTownBlueprint.gd`, `MapLayer.gd`, `Main.gd`, or `data/world_layout/` must update the source-of-truth artifacts. Minor tuning is allowed only when documented and when it does not change street widths, lot frontage, district boundaries, NPC route intent, quest beat geography, or canonical cameras.

Next phase: `G-19S Newport Blockout-To-Godot Runtime Reconstruction`.
