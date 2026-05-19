# G-19R Newport Scale + Street Blockout Agent Council Report

TECHNICAL PASS DOES NOT EQUAL DESIGN PASS.

G-19R is a corrective design-production gate. It is not a runtime sprite placement pass and it must not claim Newport is production-playable. The inspected proof for this phase is the measured SVG/PNG/JSON source-of-truth blockout, with future implementation blocked from ad hoc major layout edits.

## Summary

| Field | Result |
| --- | --- |
| Phase | G-19R Newport Scale + Street Blockout Source of Truth |
| Branch | `codex/g-19r-newport-scale-street-blockout-source-of-truth` |
| Starting main commit | `6e8c5fc59c827d1b3adf84eb90a452c7092f4e57` |
| Figma/FigJam used | No. Repo-contained SVG/PNG/JSON was used to avoid account/cloud friction. |
| Fallback blockout method | Python/Pillow generated measured SVG, PNG, and JSON artifacts. |
| Visual proof inspected | `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_measured_blockout.png` |
| Source of truth | `docs/design/NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.json` |
| Human escalation required | No |
| Final verdict | `COUNCIL_PASS_READY_FOR_PR` |
| Required next phase | G-19S Newport Blockout-To-Godot Runtime Reconstruction |

The council tool was executed with validators enabled. Its generic runtime screenshot fields are not the authority for this planning gate because G-19R explicitly forbids further runtime placement until the blockout passes. Runtime screenshot proof becomes mandatory again in G-19S when the approved blockout is reconstructed in Godot.

## Required Council Roles

| Role | Verdict | Notes |
| --- | --- | --- |
| Scrum Master | PASS | G-19R was correctly inserted as a corrective prerequisite before further Newport runtime placement, with G-19S queued as the implementation phase. |
| World-Class Game Designer | PASS | The plan now frames Newport as an origin-town play space with arrival, orientation, rumor pull, harbor labor, and island exit beats. |
| World/Layout Designer | PASS | Districts, street hierarchy, lots, frontages, and service backs are authored before sprite placement. |
| Art Director | PASS | The blockout separates ground languages and landmark hierarchy so later art cannot hide missing town structure with prop clutter. |
| Level Designer | PASS | The main street, rear lane, dock paths, alleys, and exit road are measured in character widths and tied to player purpose. |
| Narrative/Quest Designer | PASS | Opening quest beats now belong to specific town geography instead of being bolted onto arbitrary coordinates. |
| Animation/NPC Behavior Director | PASS | NPC routes distinguish stationary behavior from movement and forbid static-sprite glide until grounded animation proof exists. |
| UX Designer | PASS | Camera viewpoints and sightlines answer where the player arrived, where the counting house and tavern are, where harbor work happens, and where town exits. |
| Game Programmer | PASS | Validators and future source alignment guard are present, with runtime implementation required to consume or validate against source artifacts. |
| QA Analyst | PASS | Required G-19R validators pass, artifact completeness is machine-checkable, and no production-playable claim is made. |
| Build/Release Engineer | PASS | The phase uses repo-contained free artifacts, no payment path, no credentials, and no cloud-only source of truth. |

## Harsh-Critic Review

| Question | Answer |
| --- | --- |
| Did Codex use design-production thinking instead of code-only implementation? | YES. Browser research, historical harbor precedent, measured blockout, district planning, route planning, quest geography, and camera planning drove the work before runtime placement. |
| Was a measured blockout created? | YES. The SVG/PNG blockout shows districts, road widths, lots, NPC routes, quest route, arrival, exit, camera markers, and player-scale measurements. |
| Does the blockout solve the human-scale street problem? | YES FOR PLANNING. The current 3-tile road is recorded as 3.53 character widths and explicitly rejected; G-19R defines a 12-character-width main street, 7.5-character secondary street, 5.5-character rear lane, 3.5-character alley, and 10.5-character wharf apron. G-19S must prove this in runtime. |
| Does the town now have district logic? | YES. Harbor/wharf, counting house, tavern/inn, commercial avenue, rear service, residential edge, civic notice, hidden rumor, and village exit districts each have gameplay and narrative purpose. |
| Does the road hierarchy make sense? | YES. Waterfront road, commercial avenue, rear service street, dock paths, alley connectors, and island exit road create a readable arrival-to-town-to-island path. |
| Do buildings have lots/frontages/orientation? | YES. Major lots specify frontage street, entry orientation, lot size, footprint target, setback, adjacent props, NPC use, quest use, and sightline purpose. |
| Does the wharf feel like a working harbor in plan? | YES. The wharf district includes a working apron, dock paths, storage/service lots, cargo functions, and dockworker routes rather than decorative dock scatter. |
| Does the tavern function as the rumor hub in the plan? | YES. The tavern is a landmark lot at the hinge between commercial route and rear service access, with rumor carrier/patron use and quest beats mapped to it. |
| Does the counting house have a clear route and role? | YES. The arrival route leads from harbor to counting house, and the clerk/runner route links manifest, dock clue, and commercial pressure. |
| Do NPC routes support life and quest flow? | YES. Dockworker, clerk/runner, tavern rumor carrier, merchant, and guard/courier/sailor routes have stations, paths, pause points, facing, quest interactions, and movement constraints. |
| Do quest beats belong to the town geography? | YES. Arrival, first objective, missing manifest, dock clue, tavern whisper, two-NPC rumor, island lead, exit, hidden clue, and return/report all map to specific districts and objects. |
| Do camera viewpoints support human-scale play? | YES. The camera plan defines canonical views for cohesion, arrival, counting-house route, tavern landmark, commercial avenue, harbor work, rear service lane, NPC route proof, exit, quest interaction, and debug-disabled review. |
| Is there a source of truth future phases must follow? | YES. Future major runtime layout work must update or validate against the G-19R source-of-truth JSON and planning artifacts. |
| Is human review required? | NO. This ordinary autonomous corrective gate has enough repo-contained proof for the council to pass without Chris. |

## Scorecard

| Area | Score | Verdict |
| --- | --- | --- |
| Blockout/layout plan | 8.8/10 | PASS |
| World cohesion plan | 8.7/10 | PASS |
| Player orientation plan | 8.6/10 | PASS |
| Quest-geography integration | 8.7/10 | PASS |
| Implementation-readiness | 8.6/10 | PASS |

The council tried to disprove the pass. The remaining weakness is not the source plan; it is the unimplemented runtime scene. That weakness is assigned to G-19S and remains phase-blocking for any production-playable claim.

## Evidence

| Evidence | Path |
| --- | --- |
| Design source of truth markdown | `docs/design/NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.md` |
| Design source of truth JSON | `docs/design/NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.json` |
| Phase report | `docs/reports/G19R_NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.md` |
| Measured blockout SVG | `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_measured_blockout.svg` |
| Measured blockout PNG | `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_measured_blockout.png` |
| Scale metrics | `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_scale_metrics.json` |
| District plan | `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_district_plan.json` |
| Street hierarchy | `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_street_hierarchy.json` |
| Lot plan | `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_lot_plan.json` |
| NPC route plan | `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_npc_route_plan.json` |
| Quest beat locations | `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_quest_beat_locations.json` |
| Camera viewpoints | `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_camera_viewpoints.json` |
| Manifest | `wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_blockout_manifest.json` |
| G-19R validator | `wayfarer_godot_vertical_slice/tools/validate_g19r_newport_blockout_source_of_truth.py` |
| Future alignment validator | `wayfarer_godot_vertical_slice/tools/validate_newport_layout_source_alignment.py` |

## Validator Results

| Validator | Result |
| --- | --- |
| `validate_g19r_newport_blockout_source_of_truth.py` | PASS |
| `validate_newport_layout_source_alignment.py` | PASS |
| `validate_opening_village_island_roadmap.py` | PASS |
| `validate_opening_village_island_execution_ledger.py` | PASS |
| `git diff --check` | PASS |

## Governance

G-19R passes only as a source-of-truth gate. G-19S must implement the approved blockout into Godot, generate canonical runtime screenshots from the G-19R camera viewpoints, compare runtime placement to the source artifacts, and fail if the scene invents a new layout or falls back to ad hoc coordinate tuning.

Final Authority Verdict: `COUNCIL_PASS_READY_FOR_PR`
