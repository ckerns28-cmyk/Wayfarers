# G-4.18A Building Sprite Provenance Audit

Generated: `2026-05-15`

## Result

No Newport building sprite currently qualifies as green/final-commercial art.
All active building sprites are yellow because the in-repo isolated PNGs are
reproducible crops from tracked atlas files, but the upstream atlas PNGs were
GitHub-uploaded binaries with no original prompt, PSD/layer file, generation
log, source art package, or explicit commercial license in the repo.

The current sprites may remain temporary review art only. They must not be
classified as final/commercial Wayfarer art until the source chain is proven or
the buildings are replaced with source-safe project-owned art.

## Building Sprite Provenance Gate

Permanent gate: every building sprite used in normal review must have an entry
in `art_pipeline/newport/manifests/newport_building_sprite_provenance.json`.

Rules:

- Green assets may enter final/commercial classification only when ownership,
  source, license, and third-party reference status are documented.
- Yellow assets are temporary review art only and must stay out of final or
  commercial classification.
- Red or unknown assets are not review eligible and must be replaced before
  use.
- No sprite from another game, ripped asset sheet, unlicensed marketplace pack,
  mystery PNG, or unlicensed third-party source may become final Wayfarer art.

## Inventory

| Filename | Current in-game building id | First sprite commit | Author/date | Intermediate/source files | Prompt/source/generation log | Authorship classification | Known source/license status | Commercial-use confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `inn_tavern_v1_isolated.png` | `b_inn_tavern` | `3aea72349c9e6e630280e694780ee9c21cd7c379` | ckerns28-cmyk, 2026-05-12 13:57:28 -0400 | `assets/buildings/hearthvale_buildings_atlas_v1.png`; `tools/extract_building_sprites.gd` | Crop script only; no prompt/PSD/log | Derived crop; upstream source unknown | In-repo atlas first appeared as upload; no explicit license | yellow |
| `mercantile_shop_isolated.png` | `b_mercantile` | `dcf9c2fc989ea9351d61e90b90ad88226262090d` | ckerns28-cmyk, 2026-05-11 14:06:55 -0400 | `assets/buildings/hearthvale_buildings_atlas_v1.png`; `tools/extract_building_sprites.gd` | Crop script only; no prompt/PSD/log | Derived crop; upstream source unknown | In-repo atlas first appeared as upload; no explicit license | yellow |
| `newport_chandlery_outfitter_front_isolated.png` | `b_chandlery_front` | `dcf9c2fc989ea9351d61e90b90ad88226262090d` | ckerns28-cmyk, 2026-05-11 14:06:55 -0400 | `assets/buildings/hearthvale_newport_structure_pack_v1_b.png`; `tools/extract_building_sprites.gd` | Crop script only; no prompt/PSD/log | Derived crop; upstream source unknown | In-repo atlas first appeared as upload; no explicit license | yellow |
| `newport_counting_house_civic_exchange_isolated.png` | `b_counting_house` | `dcf9c2fc989ea9351d61e90b90ad88226262090d` | ckerns28-cmyk, 2026-05-11 14:06:55 -0400 | `assets/buildings/hearthvale_newport_structure_pack_v1_b.png`; `tools/extract_building_sprites.gd` | Crop script only; no prompt/PSD/log | Derived crop; upstream source unknown | In-repo atlas first appeared as upload; no explicit license | yellow |
| `newport_custom_house_civic_front_isolated.png` | `b_custom_house` | `71f003de83f39f966e38c2d62b952342ec72c450` | ckerns28-cmyk, 2026-05-12 19:59:08 -0400 | `assets/buildings/hearthvale_newport_structure_pack_v1_b.png`; `tools/extract_building_sprites.gd` | Crop script only; no prompt/PSD/log | Derived crop; upstream source unknown | In-repo atlas first appeared as upload; no explicit license | yellow |
| `newport_dockside_storehouse_isolated.png` | `b_dock_warehouse` | `3aea72349c9e6e630280e694780ee9c21cd7c379` | ckerns28-cmyk, 2026-05-12 13:57:28 -0400 | `assets/buildings/hearthvale_newport_structure_pack_v1_b.png`; `tools/extract_building_sprites.gd` | Crop script only; no prompt/PSD/log | Derived crop; upstream source unknown | In-repo atlas first appeared as upload; no explicit license | yellow |
| `newport_dockside_storehouse_long_isolated.png` | `b_dock_storehouse` | `3aea72349c9e6e630280e694780ee9c21cd7c379` | ckerns28-cmyk, 2026-05-12 13:57:28 -0400 | `assets/buildings/hearthvale_newport_structure_pack_v1_a.png`; `tools/extract_building_sprites.gd` | Crop script only; no prompt/PSD/log | Derived crop; upstream source unknown | In-repo atlas first appeared as upload; no explicit license | yellow |
| `newport_large_front_residence_isolated.png` | `b_large_residence` | `71f003de83f39f966e38c2d62b952342ec72c450` | ckerns28-cmyk, 2026-05-12 19:59:08 -0400 | `assets/buildings/hearthvale_newport_structure_pack_v1_a.png`; `tools/extract_building_sprites.gd` | Crop script only; no prompt/PSD/log | Derived crop; upstream source unknown | In-repo atlas first appeared as upload; no explicit license | yellow |
| `newport_market_shed_stalls_isolated.png` | `b_market_shed` | `3aea72349c9e6e630280e694780ee9c21cd7c379` | ckerns28-cmyk, 2026-05-12 13:57:28 -0400 | `assets/buildings/hearthvale_newport_structure_pack_v1_b.png`; `tools/extract_building_sprites.gd` | Crop script only; no prompt/PSD/log | Derived crop; upstream source unknown | In-repo atlas first appeared as upload; no explicit license | yellow |
| `newport_modest_clapboard_residence_a_isolated.png` | `b_boarding_house` | `71f003de83f39f966e38c2d62b952342ec72c450` | ckerns28-cmyk, 2026-05-12 19:59:08 -0400 | `assets/buildings/hearthvale_newport_structure_pack_v1_b.png`; `tools/extract_building_sprites.gd` | Crop script only; no prompt/PSD/log | Derived crop; upstream source unknown | In-repo atlas first appeared as upload; no explicit license | yellow |
| `newport_shopfront_awning_isolated.png` | `b_shop_house` | `dcf9c2fc989ea9351d61e90b90ad88226262090d` | ckerns28-cmyk, 2026-05-11 14:06:55 -0400 | `assets/buildings/hearthvale_newport_structure_pack_v1_a.png`; `tools/extract_building_sprites.gd` | Crop script only; no prompt/PSD/log | Derived crop; upstream source unknown | In-repo atlas first appeared as upload; no explicit license | yellow |
| `newport_wharf_boathouse_large_isolated.png` | `b_wharf_boathouse` | `3aea72349c9e6e630280e694780ee9c21cd7c379` | ckerns28-cmyk, 2026-05-12 13:57:28 -0400 | `assets/buildings/hearthvale_newport_structure_pack_v1_a.png`; `tools/extract_building_sprites.gd` | Crop script only; no prompt/PSD/log | Derived crop; upstream source unknown | In-repo atlas first appeared as upload; no explicit license | yellow |
| `residence_small_isolated.png` | `b_res_small` | `3aea72349c9e6e630280e694780ee9c21cd7c379` | ckerns28-cmyk, 2026-05-12 13:57:28 -0400 | `assets/buildings/hearthvale_buildings_atlas_v1.png`; `tools/extract_building_sprites.gd` | Crop script only; no prompt/PSD/log | Derived crop; upstream source unknown | In-repo atlas first appeared as upload; no explicit license | yellow |
| `service_dependency_shed_isolated.png` | `b_cooperage_shed` | `71f003de83f39f966e38c2d62b952342ec72c450` | ckerns28-cmyk, 2026-05-12 19:59:08 -0400 | `assets/buildings/hearthvale_buildings_atlas_v1.png`; `tools/extract_building_sprites.gd` | Crop script only; no prompt/PSD/log | Derived crop; upstream source unknown | In-repo atlas first appeared as upload; no explicit license | yellow |
| `village_hall_meeting_house_isolated.png` | Deferred; `b_village_hall` only outside normal G-4.18A review | `3aea72349c9e6e630280e694780ee9c21cd7c379` | ckerns28-cmyk, 2026-05-12 13:57:28 -0400 | `assets/buildings/hearthvale_buildings_atlas_v1.png`; `tools/extract_building_sprites.gd` | Crop script only; no prompt/PSD/log | Derived crop; upstream source unknown | In-repo atlas first appeared as upload; no explicit license | yellow |

## Active Atlas-Region Sprites

Normal review also uses three BuildingCatalog atlas regions that are not
standalone isolated PNGs. These are included in the manifest so the active
review gate covers the whole town:

| Sprite id | Building id | Atlas | Region | Status |
| --- | --- | --- | --- | --- |
| `newport_narrow_merchant_townhouse_a` | `b_printer_rowhouse` | `hearthvale_newport_structure_pack_v1_a.png` | `[836, 451, 273, 385]` | yellow |
| `newport_formal_townhouse_block_a` | `b_clerk_townhouse` | `hearthvale_newport_structure_pack_v1_b.png` | `[444, 67, 371, 336]` | yellow |
| `newport_waterfront_shop_house` | `b_dockworker_rowhouse` | `hearthvale_newport_structure_pack_v1_a.png` | `[864, 86, 351, 315]` | yellow |

## Source Chain

- `hearthvale_buildings_atlas_v1.png` first entered repository history as
  `wayfarer_v7_github_ready/worker/assets/wayfarer/buildings/hearthvale_buildings_atlas_v1_transparent.png`
  in commit `eecb68d138a5ca6ff7d11784ad3c77701984557d` (`Add files via upload`,
  2026-04-28), then entered the Godot slice in commit
  `33f528e4062d7269cc2368a387f7a37b6c809737`.
- `hearthvale_newport_structure_pack_v1_a.png` and
  `hearthvale_newport_structure_pack_v1_b.png` first entered repository history
  in commit `585f2d55832344d8fc494805da073bb9f4bd898e` (`Add files via upload`,
  2026-05-03), then entered the Godot slice in commit
  `33f528e4062d7269cc2368a387f7a37b6c809737`.
- `tools/extract_building_sprites.gd` documents crop rectangles, padding, and
  cleanup rectangles for every isolated PNG. It does not document how the
  upstream atlas art was created.

## Chandlery/Outfitter Audit

Audited sprite:
`assets/sprites/buildings/isolated/newport_chandlery_outfitter_front_isolated.png`

Findings:

- First entered the isolated sprite folder in commit
  `dcf9c2fc989ea9351d61e90b90ad88226262090d` (`Updates`, 2026-05-11
  14:06:55 -0400, ckerns28-cmyk).
- It was modified in commit `85ce1356db3299cd73a961900491a09db5872444`
  and again in commit `3aea72349c9e6e630280e694780ee9c21cd7c379`.
- Its documented crop source is
  `assets/buildings/hearthvale_newport_structure_pack_v1_b.png`, rect
  `[815, 444, 387, 352]`, padded by `tools/extract_building_sprites.gd`.
- The source atlas first appeared in repo history as a GitHub binary upload,
  with no prompt, source PSD/layer file, original generation record, or
  explicit license document found.
- No in-repo record says whether the chandlery was AI-generated, hand-authored,
  derived from external references, or imported from another source.
- Web filename and descriptive searches did not find an identical third-party
  asset. This lowers match concern but does not prove ownership.

Decision:

`newport_chandlery_outfitter_front_isolated.png` fails final/commercial
provenance review. It may remain temporary review art while replacement or
source-chain evidence is produced. It cannot currently be treated as final
project-owned art.

## Reverse Search

Tools used:

- Local git history and source-tree audit.
- Codex web search exact filename queries.
- Codex web search descriptive similarity queries.

Limitation:

No upload-based Google Lens/TinEye interaction was available in this session.
The search pass is therefore a documented web similarity screen, not a full
image-forensic clearance.

Exact filename searches performed:

`inn_tavern_v1_isolated.png`, `mercantile_shop_isolated.png`,
`newport_chandlery_outfitter_front_isolated.png`,
`newport_counting_house_civic_exchange_isolated.png`,
`newport_custom_house_civic_front_isolated.png`,
`newport_dockside_storehouse_isolated.png`,
`newport_dockside_storehouse_long_isolated.png`,
`newport_large_front_residence_isolated.png`,
`newport_market_shed_stalls_isolated.png`,
`newport_modest_clapboard_residence_a_isolated.png`,
`newport_shopfront_awning_isolated.png`,
`newport_wharf_boathouse_large_isolated.png`,
`residence_small_isolated.png`,
`service_dependency_shed_isolated.png`,
`village_hall_meeting_house_isolated.png`,
`hearthvale_buildings_atlas_v1.png`,
`hearthvale_newport_structure_pack_v1_a.png`,
`hearthvale_newport_structure_pack_v1_b.png`,
`newport_chandlery_outfitter_front`.

Descriptive/similarity searches performed:

- `colonial chandlery outfitter storefront game sprite rope barrels anchor`
- `Newport chandlery outfitter building sprite`
- `colonial harbor shop game asset rope barrels storefront sprite`
- `isometric colonial shop building sprite green storefront`
- `front facing colonial tavern building sprite dark roof porch game asset`
- `colonial mercantile shop building sprite barrels sign game asset`
- `colonial counting house civic exchange building sprite game asset`
- `colonial shopfront awning building sprite game asset`
- `colonial market shed stalls building sprite game asset`
- `colonial wharf boathouse building sprite game asset`
- `dockside storehouse warehouse building sprite colonial harbor game asset`
- `front facing colonial custom house civic building sprite game asset`
- `site:itch.io colonial building sprite asset pack shop tavern market`
- `site:itch.io harbor building sprite asset pack colonial shop`
- `site:gamedevmarket.net colonial building sprite asset pack harbor shop`
- `site:craftpix.net colonial building sprite asset pack harbor shop`

Matches reviewed:

| Match/source | Search reason | Result |
| --- | --- | --- |
| [Free Pixel Art Medieval Village Mini Pack](https://freepixelart.itch.io/free-pixel-art-medieval-village-mini-pack-90-sprites) | marketplace-style building pack screen | Generic medieval pack; not identical |
| [150x Pixel Art Medieval Buildings & Shops](https://pixel-1992.itch.io/150x-pixel-art-medieval-buildings-shops-full-commercial-asset-pack-64x64-128x) | shop/building pack screen | Generic AI-assisted medieval pack; not identical |
| [Pixel Art Market Square - RPG Shop and NPC Assets Pack](https://craftpix.net/product/pixel-art-market-square-rpg-shop-and-npc-assets-pack/) | market/stall similarity screen | Generic market pack; not identical |
| [Liso Library Pier](https://www.gamedevmarket.net/asset/liso-library-pier) | harbor/rope/anchor similarity screen | Pier/prop pack; not identical |
| [Wood Set by Pixless](https://pixless.itch.io/wood-set) | barrel/wood prop similarity screen | Prop pack; not identical |

No identical match was found by exact filename or descriptive web search. No
source can be upgraded to green from this result alone.

## Status Buckets

Green:

- None.

Yellow/uncertain:

- `inn_tavern_v1`
- `mercantile_shop`
- `newport_chandlery_outfitter_front`
- `newport_counting_house_civic_exchange`
- `newport_custom_house_civic_front`
- `newport_dockside_storehouse`
- `newport_dockside_storehouse_long`
- `newport_large_front_residence`
- `newport_market_shed_stalls`
- `newport_modest_clapboard_residence_a`
- `newport_shopfront_awning`
- `newport_wharf_boathouse_large`
- `residence_small`
- `service_dependency_shed`
- `village_hall_meeting_house`
- `newport_narrow_merchant_townhouse_a`
- `newport_formal_townhouse_block_a`
- `newport_waterfront_shop_house`

Red/unsafe:

- None identified as a known ripped, third-party, or unlicensed marketplace
  match during this pass.

Replacement Queue:

All yellow assets above need one of the following before final/commercial use:

- original generation record and commercial-use terms;
- original layered/source files proving project ownership;
- documented external license compatible with Wayfarer commercial use;
- replacement with newly generated or hand-authored project-owned building art.
