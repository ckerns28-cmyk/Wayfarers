# G-11 Living Town Rhythm Pass

Status: `PASS`

Branch: `codex/g-11-living-town-rhythm-pass`

G-11 adds a runtime-backed living town rhythm layer for Newport without pretending that one-frame NPC portraits can walk. NPCs now have authored district rhythms, facing changes, idle pauses, ambient bark seeds, station lists, and runtime proof snapshots. The movement policy is explicit: `stationary_no_glide_rhythm_until_dedicated_walk_sheets`.

## Scope

- Added `starter_village_town_rhythm_specs()` and `starter_village_town_rhythm_contract()` to the Newport blueprint.
- Added runtime rhythm integration in `Main.gd`.
- Added `configure_rhythm()`, `apply_town_rhythm_tick()`, `town_rhythm_contract()`, and focused `AmbientBarkLabel` support to Edrin and generic town NPCs.
- Added `validate_living_town_rhythm.py`.
- Added G-11 screenshot capture and motion-proof manifest generation.
- Updated the Agent Council to include G-11 rhythm validation and report language.

## Authored Rhythms

| Rhythm | District | Purpose |
| --- | --- | --- |
| `dock_work_bell` | Working wharf | Dock work behavior for rope, cargo, tide, and missing-line pressure. |
| `tavern_whisper_pulse` | Harborfront commercial | Tavern social behavior around Bess, Silas, the Third Toast, and rear-lane whispers. |
| `market_street_trade` | Harborfront commercial | Merchant street behavior tying coin, goods, and the wharf to the opening mystery. |
| `counting_house_watch` | Inland residential/civic | Civic notice and ledger-watch behavior for Edrin and Nora. |
| `rear_gate_suspicion` | Support lane | Rear service lane behavior for secret-path tension. |

## Runtime Proof

Screenshot manifest:

`wayfarer_godot_vertical_slice/artifacts/review/g11_runtime_screenshots/g11_runtime_screenshot_manifest.json`

Recurring proof set:

- `g11_01_wide_newport_normal_gameplay_view.png`
- `g11_02_player_arrival_at_harbor.png`
- `g11_03_player_on_route_to_counting_house.png`
- `g11_04_player_near_tavern_inn.png`
- `g11_05_player_on_commercial_avenue.png`
- `g11_06_player_at_dock_wharf_work_area.png`
- `g11_07_player_near_npc_movement_path.png`
- `g11_08_npc_idle_and_rhythm_proof.png`
- `g11_09_player_interacting_with_counting_house_clerk.png`
- `g11_10_player_interacting_at_tavern_rumor_location.png`
- `g11_11_quest_prompt_journal_objective_proof.png`
- `g11_12_signs_markers_interaction_ux_proof.png`
- `g11_13_y_sort_layering_near_buildings_props.png`
- `g11_14_debug_overlays_disabled.png`
- `g11_15_contact_sheet_provenance_proof.png`

The manifest also includes a timestamped town-rhythm proof sequence. No static NPC sprite translates across the map. Position drift is expected to remain `false`; moving actor count is expected to remain `0` until dedicated walk sheets exist.

## QA Notes

- Wide and debug-off views were re-captured after the first inspection caught excessive bark text in the town-wide frame.
- Focused barks are now forced only for the target NPC in rhythm proof views.
- Dialogue proof suppresses ambient bark display so dialogue panels do not compete with ambient text.
- Ground/material patchwork remains a G-12 review risk and cannot be hidden by NPC activity.

## Validation

- PASS: Godot import validation.
- PASS: G-11 runtime screenshot capture and PNG verification.
- PASS: living town rhythm validator.
- PASS: NPC population and routes validator.
- PASS: runtime atelier asset consistency validator.
- PASS: Starter Village roadmap validator.
- PASS: Starter Village execution ledger validator after ledger update.
- PASS: git diff checks after final staging.

## Council Scores

| Discipline | Score |
| --- | --- |
| Design | 8.5 |
| Art direction | 8.5 |
| World/layout | 8.5 |
| NPC rhythm / animation safety | 8.5 |
| Narrative support | 8.5 |
| UX/readability | 8.5 |
| Technical stability | 8.7 |

## Result

G-11 passes as a living town rhythm foundation, not as a full NPC locomotion pass. The correct path remains: no hover-walking, no static sprite gliding, and no fake movement. Future animation work must add dedicated walk sheets before NPCs can physically traverse routes.

Next phase: `G-11A Audio/Atmosphere Placeholder-Free Foundation`.
