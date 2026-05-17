# G-4.21A Newport Core Building Atelier Rebuild Wave 1

## Result

G-4.21A begins the Newport core building atelier rebuild. This is the first
architectural pass for the starting town: buildings are rebuilt as a coherent
coastal fantasy family for orientation, memory, gameplay clarity, and believable
density rather than accumulated as isolated sprites.

## Source Chain

- Source image: `art_pipeline/newport_atelier/source_generated/g421a_core_building_rebuild_wave_1_sheet_imagegen.png`
- Prompt record: `art_pipeline/newport_atelier/source_generated/g421a_core_building_rebuild_wave_1_prompt.txt`
- Extraction script: `art_pipeline/newport_atelier/scripts/extract_g421a_core_building_assets.py`
- Output atlas: `art_pipeline/newport_atelier/atlases/newport_atelier_core_buildings_wave_1_v1.png`
- Manifest: `art_pipeline/newport_atelier/manifests/newport_atelier_core_buildings_wave_1_manifest.json`
- Contact sheet: `art_pipeline/newport_atelier/contact_sheets/newport_atelier_core_buildings_wave_1_contact_sheet.png`
- Extraction QA report: `art_pipeline/newport_atelier/reports/newport_atelier_core_buildings_wave_1_extraction_qa.json`
- Base standard: `art_pipeline/newport_atelier/reports/G418D_ATELIER_CARGO_STANDARD.md`
- Prior rollout reference: `art_pipeline/newport_atelier/reports/G419A_NEWPORT_DOCK_CLUTTER_ATELIER_PACK.md`

No yellow Newport building pixels, third-party sprite sheets, marketplace assets,
web images, or ripped game art were supplied as source inputs.

## Tavern/Inn Hero Lock

The Tavern/Inn is the required G-4.21A hero asset and centerpiece. Direction:
brick construction, two front/back bridged twin-stack chimney sets, warm windows, clear
entrance, strong stone foundation, old Newport/coastal prestige, social hub,
quest anchor, player landmark, and Hotel Viking-inspired coastal landmark
presence without direct copying.

## Generated Buildings

- `atelier_newport_tavern_inn_hero_01` -> `b_inn_tavern`: `centerpiece_tavern_inn_hero_building`, rating `9.3/10`, replaces `inn_tavern_v1`
- `atelier_newport_mercantile_store_01` -> `b_mercantile`: `mercantile_general_store_building`, rating `9.0/10`, replaces `mercantile_shop`
- `atelier_newport_wharf_warehouse_01` -> `b_dock_warehouse`: `wharf_warehouse_dock_office_building`, rating `9.0/10`, replaces `newport_dockside_storehouse`
- `atelier_newport_harbor_cottage_gabled_01` -> `b_res_small`: `small_residence_cottage_variant`, rating `8.9/10`, replaces `residence_small`
- `atelier_newport_harbor_cottage_dormer_01` -> `b_boarding_house`: `small_residence_cottage_variant`, rating `8.9/10`, replaces `newport_modest_clapboard_residence_a`
- `atelier_newport_cooperage_workshop_01` -> `b_cooperage_shed`: `workshop_cooperage_service_building`, rating `8.9/10`, replaces `service_dependency_shed`

## Building QA

The QA report checks clean transparent bounds, no magenta background or halo,
no cropped roof/chimney/wall/foundation, visible bases, readable entrances,
sensible pivot/base anchors, scale compatibility, non-floating placement, and
Tavern/Inn-specific brick/twin-stack/hero/not-direct-copy confirmations.

## Old Building Handling

Old building assets are not deleted. Replaced yellow targets are marked as
deprecated or no longer active visual targets in the Newport visual production
registry and building provenance manifest. Any old assets still present are
temporary history/placeholders only, not final.

## Placement Policy

The controlled proof subset is wired through `BuildingCatalog` for the Tavern,
Mercantile, Dock Warehouse, Harbor Cottage, Boarding House cottage variant, and
Cooperage workshop. Existing G-4.18D through G-4.20B atelier assets remain valid
and visible.
