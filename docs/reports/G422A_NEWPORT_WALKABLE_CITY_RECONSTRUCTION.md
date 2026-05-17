# G-4.22A Newport Walkable City Reconstruction Blockout

## Diagnosis

The previous Newport composition read as an attractive asset board rather than a town because the buildings were still arranged primarily as horizontal rows on a flat presentation field. The player could see good sprites, but the ground plan did not yet explain why buildings were there, where NPCs would walk, or how harbor work moved into town.

The main failures were:

- The harborfront did not read as a real avenue with roads running uphill from it.
- Civic, residential, commercial, and wharf buildings shared a similar shelf-like placement instead of defining districts.
- Legacy proof overlays, ghost background buildings, rectangular garden pads, and broad translucent ground chunks made the street surface look clipped and staged.
- The old meeting-house crop briefly acted as a Town Hall anchor, which failed the visual/provenance direction and made the civic area feel like random old art.
- Several open green rectangles lacked fences, yards, gates, or alley boundaries, so negative space did not yet read as purposeful city blocks.

## New District Structure

G-4.22A rebuilds the starter plan around a harbor avenue with streets running north/uphill from it:

- Waterfront/wharf district: boardwalk, piers, cargo aprons, warehouse/boathouse/storehouse frontage, dock workers, dock rules board, inspection spots.
- Main market/commercial street: Tavern/Inn, clerk rowhouse, mercantile, chandlery, shop house, market shed, printer rowhouse, shared avenue paving, curb breaks, signs, vendor props.
- Civic district: Town Hall / Counting House is now the civic frontage at the top of the central uphill road, paired with the Custom House on the civic cross street.
- Tavern/Inn anchor district: the G-4.21A hero inn remains the west avenue landmark and is connected directly to the market spine and wharf approach.
- Residential/backstreet district: cottages, large residence, boarding house, dockworker rowhouse, fences, small yards, side routes, and support-lane boundaries.
- Service/alley routes: west and central service lanes connect avenue traffic to the working wharf without forcing all movement through one horizontal street.

The old active `b_village_hall` Town Hall placement was removed from the starter set. The sprite remains deferred in the catalog, but G-4.22A does not promote it as active review art.

## Walking Loops

- Harbor loop: waterfront avenue -> wharf apron -> west/central/east pier routes -> dock warehouse, boathouse, storehouse -> service alley return.
- Market loop: Tavern/Inn -> clerk rowhouse -> mercantile -> chandlery -> shop house -> market shed -> printer corner -> east market road.
- Civic/residential loop: central uphill road -> Town Hall / Counting House -> Custom House -> residential backstreet -> east support lane -> return to the avenue.

These loops are represented in `NewportTownBlueprint.walking_loop_specs()` and validated through route targets/probes.

## Interaction Anchors

G-4.22A adds or repositions anchors for:

- Tavern/Inn entrance
- Town Hall / Counting House entrance
- Counting-house records window
- Mercantile entrance
- Chandlery entrance
- Shop House entrance
- Town notice board
- Dock rules board
- Dock worker placeholders
- Market vendor placeholder
- Harbor cargo inspection spots
- Well/bench civic interaction
- Service-alley barrels/crates
- Cooperage hoops/barrels

NPC placeholder sprites were added along the avenue, uphill roads, wharf, and market route to prove human-scale circulation.

## Street And Terrain Cleanup

Clean review mode now keeps legacy proof art behind explicit flags:

- `G422A_SHOW_BLOCKOUT_GUIDES = false`
- `G422A_SHOW_LEGACY_PROOF_OVERLAYS = false`

Presentation-breaking items removed or gated in clean screenshots:

- G-4.17/G-4.18 proof street and wharf overlays
- G-4.20A legacy terrain/cobble/shoreline/building-grounding atlas placements
- old non-cargo hero prop clusters
- ghost background buildings
- non-dock G-4.15 ground pads
- rectangular garden-bed pads that made the ground read as clipped staging art

Street texture now stays inside irregular street polygons instead of spilling across road bounding boxes.

## Screenshot Capture

Command used:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\capture_g422a_runtime_screenshots.ps1 -GodotBin 'C:\Users\Chris\Downloads\Godot_v4.6.2-stable_win64.exe\Godot_v4.6.2-stable_win64_console.exe'
```

Generated screenshots:

- `wayfarer_godot_vertical_slice/artifacts/review/g422a_runtime_screenshots/g422a_01_whole_town.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g422a_runtime_screenshots/g422a_02_tavern_market_anchor.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g422a_runtime_screenshots/g422a_03_harbor_loop.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g422a_runtime_screenshots/g422a_04_civic_residential_loop.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g422a_runtime_screenshots/g422a_05_backstreet_service_route.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g422a_runtime_screenshots/g422a_06_player_walkability_proof.png`

Manifest:

- `wayfarer_godot_vertical_slice/artifacts/review/g422a_runtime_screenshots/g422a_runtime_screenshot_manifest.json`

## Validation Results

- Godot import validation: PASS
- `tools/validate_vertical_slice.gd`: PASS
- `art_pipeline/newport/scripts/validate_newport_asset_provenance.py`: PASS
- G-4.21A extraction validation: PASS
- Runtime screenshot capture: PASS
- Screenshot PNG verification: PASS for all six captures
- Capture log: clean, no debug/HUD capture errors
- Walkability probes: PASS for harbor, market, civic, residential, wharf, and service-alley routes

## Remaining Gaps Before 8.5+/10

- Newport still needs a dedicated final street/terrain art kit. The current Godot-authored street family is more coherent, but it is still a blockout surface.
- Several non-atelier building sprites remain temporary yellow review art and should be rebuilt or replaced before final-commercial confidence.
- The civic district needs bespoke final Town Hall art. G-4.22A uses the stronger Counting House/Custom House pair as a readable provisional civic anchor.
- NPCs are placeholders only. Next passes need actual route behaviors, schedules, job stations, door usage, and crowd rules.
- Interiors and door transitions are still stubs.
- Yards and block interiors now read more intentionally, but they need richer handmade edge dressing and less rectangular final art.
- Collision/pathing validation is route-based; full navigation mesh and NPC avoidance still need deeper tests.
