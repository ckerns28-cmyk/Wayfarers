# G-4.19A Newport Dock Clutter Atelier Pack

## Result

G-4.19A is the first Newport city rollout pack built from the G-4.18D atelier
cargo standard. It keeps the locked production pattern intact and extends the
wharf proof with authored-looking dock clutter instead of procedural filler.

## Source Chain

- Source image: `art_pipeline/newport_atelier/source_generated/g419a_atelier_dock_clutter_sheet_imagegen.png`
- Prompt record: `art_pipeline/newport_atelier/source_generated/g419a_atelier_dock_clutter_prompt.txt`
- Extraction script: `art_pipeline/newport_atelier/scripts/extract_atelier_dock_clutter_assets.py`
- Output atlas: `art_pipeline/newport_atelier/atlases/newport_atelier_dock_clutter_v1.png`
- Manifest: `art_pipeline/newport_atelier/manifests/newport_atelier_dock_clutter_manifest.json`
- Contact sheet: `art_pipeline/newport_atelier/contact_sheets/newport_atelier_dock_clutter_contact_sheet.png`
- Extraction QA report: `art_pipeline/newport_atelier/reports/newport_atelier_dock_clutter_extraction_qa.json`
- Base standard: `art_pipeline/newport_atelier/reports/G418D_ATELIER_CARGO_STANDARD.md`

No yellow Newport building pixels, third-party sprite sheets, marketplace
assets, web images, or ripped game art were supplied as source inputs.

## Classification

These assets are `ai_assisted_green_origin_candidate_pending_license_review`.
They are review-eligible as original AI-assisted candidates, but final
commercial promotion remains blocked until the project approves its final
license policy for generated artwork.

## Generated Assets

- `atelier_dock_bollards_01`: `bollard_pair_prop`, `green_origin_candidate_pending_license_review`
- `atelier_mooring_hardware_01`: `rope_post_mooring_hardware_cluster`, `green_origin_candidate_pending_license_review`
- `atelier_fishing_net_bundle_01`: `fishing_net_bundle_prop`, `green_origin_candidate_pending_license_review`
- `atelier_sacks_fish_baskets_01`: `sacks_and_fish_baskets_cluster`, `green_origin_candidate_pending_license_review`
- `atelier_anchor_rope_01`: `anchor_and_rope_prop`, `green_origin_candidate_pending_license_review`
- `atelier_dock_repair_planks_01`: `stacked_planks_dock_repair_boards`, `green_origin_candidate_pending_license_review`
- `atelier_dock_lantern_01`: `dock_lantern_prop`, `green_origin_candidate_pending_license_review`
- `atelier_shoreline_debris_01`: `shoreline_debris_cluster`, `green_origin_candidate_pending_license_review`

## Placement QA

The in-game proof uses a controlled subset only. The placements are clustered
around docks, cargo frontage, market/harbor edges, and service paths. The pack
does not attempt city-wide scatter in this pass.

Validation criteria for placement:

1. Scale remains consistent with G-4.18D cargo sprites.
2. Destination bottoms match placement `ground_y`.
3. Pivots stay near the lower center of each prop.
4. Props are drawn from transparent atlas regions with no magenta halo.
5. Props do not block navigation or hide critical walkable path reads.
6. Low shoreline debris stays visually subordinate to cargo and buildings.

## Reusable Production Pattern

10/10 source sheet -> saved prompt/source -> extraction script -> transparent
sprites -> atlas/contact sheet -> manifest/provenance report -> Godot placement
-> validation.
