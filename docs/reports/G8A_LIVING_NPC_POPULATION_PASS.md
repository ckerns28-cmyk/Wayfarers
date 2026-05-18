# G-8A Living NPC Population Pass

Phase status: `PASS`

Branch: `codex/g-8a-living-npc-population`

Council verdict: `COUNCIL_PASS_READY_FOR_PR`

## Purpose

G-8A makes Newport feel inhabited without reintroducing the hover/glide failure
that G-8 removed. The pass adds named, role-bearing NPCs to tavern, dock,
counting-house, commercial, civic, and rear-service stations. Each NPC has a
purpose in town, a district, a route intent, an idle behavior, a dialogue seed,
quest relevance, and manifest-backed atelier sprite provenance.

No static portrait-like NPC may drift across the map. Until dedicated walk
sheets exist, G-8A uses the accepted
`stationary_work_pose_until_dedicated_walk_sheets` policy: fewer grounded NPCs
are better than a crowded village of sliding cutouts.

## Runtime NPC Cast

| NPC | Role | District | Station | Quest / Rumor Relevance |
| --- | --- | --- | --- | --- |
| Edrin Vale | counting_house_clerk | inland_residential_civic | counting_house_records_route | First Light counting-house objective and missing ledger line. |
| Bess Armitage | tavern_keeper | harborfront_commercial | tavern_front_threshold | Tavern whisper hook and Third Toast rumor path. |
| Mara Pike | dockworker | working_wharf | west_fish_offload | Missing manifest line and harbor labor testimony. |
| Honor Finch | merchant_shopkeeper | harborfront_commercial | east_market_cart | Merchant/street path and coin-trail clue. |
| Nora Vale | rumor_carrier | inland_residential_civic | civic_notice_board | Optional notice clue between civic square and tavern. |
| Silas Crowe | suspicious_patron | support_lane | tavern_rear_service_gate | Optional secret path through rear service lane. |
| Jonah Reed | dockworker_courier | working_wharf | east_storehouse_queue | Harbor work path and storehouse-to-counting-house pressure. |

## Runtime Changes

- Added `AtelierTownNpc.gd` and `AtelierTownNpc.tscn` as reusable, grounded,
  interactable town NPC nodes.
- Converted the prior map-painted NPC placement layer into runtime NPC nodes
  for normal play while suppressing duplicate painted stand-ins.
- Added `starter_village_npc_specs()` and `starter_village_npc_spec()` to
  `NewportTownBlueprint.gd`.
- Added G-8A population metadata to `MapLayer.gd`, including role, station,
  route intent, idle behavior, dialogue seed, quest relevance, and placement
  purpose for every visible NPC.
- Extended Edrin Vale with a G-8A population contract while preserving the G-8
  grounded motion contract.
- Added G-8A vertical-slice checks for role coverage, contracts, shadows,
  `AnimatedSprite2D` visuals, and disabled route walking.
- Added G-8A screenshot capture with NPC population contracts in the manifest.

## Screenshot Evidence

Runtime screenshot manifest:
`wayfarer_godot_vertical_slice/artifacts/review/g8a_runtime_screenshots/g8a_runtime_screenshot_manifest.json`

Council-inspected frames:

- `g8a_01_wide_newport_normal_gameplay_view.png`: PASS for normal-play town
  population distribution across tavern, civic, market, and wharf stations.
- `g8a_04_player_near_tavern_inn.png`: PASS for Bess Armitage and Silas Crowe
  making the Tavern/Inn read as a social rumor hub.
- `g8a_06_player_at_dock_wharf_work_area.png`: PASS for dockworker and courier
  roles supporting harbor labor without blocking movement.
- `g8a_08_npc_idle_and_walking_proof.png`: PASS for no static NPC glide; walk
  requests resolve to grounded idle until dedicated walk sheets exist.
- `g8a_09_player_interacting_with_counting_house_clerk.png`: PASS for Edrin
  Vale as the counting-house anchor of the opening objective.
- `g8a_15_contact_sheet_provenance_proof.png`: PASS for manifest-backed G-4.22R
  atelier NPC atlas use and population contracts.

## Validation Results

| Check | Result |
| --- | --- |
| Godot import validation | PASS |
| Vertical slice validator | PASS |
| G-8A screenshot capture and PNG verification | PASS |
| NPC population and routes validator | PASS |
| Character motion foundation validator | PASS |
| G-4.22R runtime asset consistency validator | PASS |
| Runtime atelier asset consistency validator | PASS |
| Starter Village roadmap validator | PASS |
| Starter Village execution ledger validator | PASS |
| Git diff whitespace check | PASS |

## Phase Scores

| Category | Score |
| --- | --- |
| NPC population score | 8.5/10 |
| NPC motion/grounding score | 8.5/10 |
| Design score | 8.5/10 |
| Art direction score | 8.5/10 |
| World/layout score | 8.5/10 |
| Narrative score | 8.5/10 |
| UX/readability score | 8.5/10 |
| Technical stability score | 8.8/10 |
| Performance/build score | 8.7/10 |

## Council Finding

G-8A passes because Newport now has a grounded, purposeful, quest-relevant
starter population without static cutout movement. The NPCs are not decoration
only: they point toward tavern whispers, harbor rumors, counting-house pressure,
merchant motives, and optional secret paths.

The council does not certify SV-1. The next production need is G-9, where
interaction prompts, labels, signs, and objective guidance must stop reading as
debug UI and become tasteful player-facing guidance.
