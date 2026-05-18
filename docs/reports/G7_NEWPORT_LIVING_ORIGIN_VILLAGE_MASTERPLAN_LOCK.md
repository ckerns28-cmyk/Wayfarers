# G-7 Newport Living Origin Village Masterplan Lock

Phase: `G-7`

Branch: `codex/sv1-autonomous-roadmap`

Status: `COUNCIL_PASS_READY_FOR_PR` for the masterplan lock. This does not
claim the current runtime screenshot is visually acceptable. The screenshot is
the failing baseline that G-7A must repair.

## Purpose

G-7 turns the post-G-6 correction into an actionable authored-town contract.
Newport must stop being evaluated as a collection of good assets and start
being built as the first playable home base of a fantasy/colonial harbor RPG.

## Failing Baseline Evidence

Inspected local runtime proof:

- `wayfarer_godot_vertical_slice/artifacts/review/g422r_runtime_screenshots/g422r_01_wide_newport_normal_gameplay_view.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g422r_runtime_screenshots/g422r_05_player_near_npcs.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g422r_runtime_screenshots/g422r_12_wider_town_cohesion_no_placeholder_mix.png`

Council classification:

- current town cohesion baseline: `2.0/10`,
- asset quality when correctly applied: strong,
- town plan read: failing,
- NPC motion read: failing risk until G-8,
- opening quest hook: present as direction, not yet playable enough.

## Locked Town Grammar

Newport is organized around five readable bands:

| Band | Purpose | Player Read |
| --- | --- | --- |
| Working Wharf | Dock labor, cargo inspection, warehouses, mooring, harbor clues. | The town earns its living from the water. |
| Harborfront Avenue | Tavern/Inn, mercantile, chandlery, market edge, first social/commercial spine. | The first real street and main return route. |
| Counting House / Civic Green | Clerk, customs, notices, ledger pressure, official tension. | The first formal objective and town authority. |
| Rear Service Lane | Cooperage, boarding, dockworker housing, storage, quiet routes. | The back side of harbor commerce and rumor movement. |
| Residential Edge | Homes, class texture, future secrets, social stakes. | People live here; Newport is not only a market board. |

## Player Arrival Route

The first-session route is locked as:

1. Landfall on the wharf.
2. Move north from dock planks onto the harborfront avenue.
3. See the Tavern/Inn as the west social landmark and the counting-house route
   as the official objective.
4. Follow a visible uphill connector to the Counting House / clerk.
5. Receive or discover a ledger/cargo discrepancy.
6. Return toward the Tavern/Inn where whispers reinterpret the errand.
7. Branch toward dockworkers, clerk, merchant/street clue, or optional secret.

The player should see, in order:

1. water, wharf work, and harborfront avenue,
2. the counting-house/civic route and Tavern/Inn landmark,
3. rear service/residential texture that suggests secrets beyond the first
   street.

## District Purpose And Building Reasons

| Building | District | Reason To Exist |
| --- | --- | --- |
| Inn & Tavern | Harborfront Avenue | Social anchor, rumor hub, first memorable landmark, return location. |
| Town Hall / Counting House | Civic Green | Cargo records, official pressure, first objective, ledger mystery. |
| Custom House | Civic Green | External authority, customs pressure, future faction tension. |
| Mercantile | Harborfront Avenue | Merchant motive, supplies, rumor-adjacent commerce. |
| Chandlery | Harborfront Avenue | Rope/sail supply, dock economy, harbor work clue source. |
| Shop House | Harborfront Avenue | Commercial density and future merchant/street path. |
| Market Shed | Harborfront Avenue | Public trade, barks, optional observation clue. |
| Printer Rowhouse | Harborfront Avenue | Pamphlet/unrest hook and future secret path. |
| Clerk Townhouse | Harborfront Avenue | Lodging, private rumor, social bridge between tavern and official world. |
| Dock Warehouse | Working Wharf | Cargo inspection, missing line clue, work-life proof. |
| Wharf Boathouse | Working Wharf | Waterline work, mooring route, lantern/signal clue. |
| Dock Storehouse | Working Wharf | Stored cargo, suspicious omission, dockworker route. |
| Cooperage Shed | Rear Service Lane | Barrel/warehouse support and service-lane clue logic. |
| Boarding House | Rear Service Lane | Labor housing, class texture, dockworker social clue. |
| Dockworker Rowhouse | Rear Service Lane | NPC home/work path and future missing-person hook. |
| Harbor Cottage | Residential Edge | Town humanity, not just commerce. |
| Harbor Residence | Residential Edge | Class contrast and future faction pressure. |

## Opening Quest Beat Map

Opening arc: `First Light / Whispers Before Dawn`

| Beat | Location | Gameplay Role |
| --- | --- | --- |
| Make landfall | Wharf arrival | Orient the player to harbor work and town scale. |
| Find the clerk | Counting House / civic green | First objective and official pressure. |
| Missing line | Warehouse, dock ledger, cargo inspection | Investigate cargo discrepancy. |
| First whisper | Tavern threshold or suspicious patron | Reframe the errand as dangerous rumor. |
| The Third Toast | Tavern interior/exterior social pocket | Coded phrase and first trust test. |
| Lantern at the Wharf | Waterline/boathouse/storehouse | Optional clue or signal. |
| Hook to continue | Journal/contact/reward | Give reason to return and keep playing. |

## NPC Work/Life Route Contract

G-8/G-8A must implement fewer grounded NPCs before more decorative ones.

| Role | Home/Station | Route Or Behavior |
| --- | --- | --- |
| Clerk / Edrin Vale | Counting House | Stationed, short pacing only after grounded animation exists. |
| Tavern Keeper or Inn Servant | Tavern/Inn | Stationed at tavern threshold or interior hub, rumor lines. |
| Dockworker | Wharf / Dockworker Rowhouse | Walks between cargo and storehouse with pauses, or stands idle until walk cycle is ready. |
| Merchant / Shopkeeper | Mercantile / market spine | Stationed with short shopfront behavior. |
| Rumor Carrier / Suspicious Patron | Tavern to rear lane | Short route only when grounded motion proof exists. |

No static portrait-like NPC may drift across the map. If a full walk cycle is
not ready, the NPC must remain stationed in a grounded idle pose.

## G-7A Repair Instructions

G-7A must change runtime composition, not write more description. Required
repair targets:

- replace disconnected road/ground rectangles with one coherent material
  grammar,
- make the harborfront avenue and uphill roads read at a glance,
- shrink or remove empty green cells that read as editor placeholders,
- seat buildings on lots, stoops, yards, docks, civic spaces, or service
  courts,
- group props by function and district,
- protect walkable routes instead of solving layout with clutter,
- generate the recurring SV-1 screenshot set where applicable,
- fail council review if town cohesion stays below 7.5/10.

## Validation

Required local validators for this phase:

- `python wayfarer_godot_vertical_slice/tools/validate_starter_village_roadmap.py`
- `python wayfarer_godot_vertical_slice/tools/validate_starter_village_execution_ledger.py`
- `python wayfarer_godot_vertical_slice/tools/validate_newport_world_cohesion.py`

## Next Phase

`G-7A Street, Lot, and Ground Cohesion Reconstruction`
