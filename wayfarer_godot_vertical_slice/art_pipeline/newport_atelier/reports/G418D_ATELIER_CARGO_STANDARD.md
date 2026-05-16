# G-4.18D Newport Atelier Cargo Standard

## Result

This pass establishes the accepted 10/10 cargo prop quality target for the
Newport city-wide sprite rollout. The source sheet is an AI-assisted original
generation selected for art direction quality, then locally extracted into
transparent game sprites and a review atlas.

## Source Chain

- Source image: `art_pipeline/newport_atelier/source_generated/g418d_atelier_cargo_sheet_imagegen.png`
- Prompt record: `art_pipeline/newport_atelier/source_generated/g418d_atelier_cargo_prompt.txt`
- Extraction script: `art_pipeline/newport_atelier/scripts/extract_atelier_cargo_assets.py`
- Output atlas: `art_pipeline/newport_atelier/atlases/newport_atelier_cargo_v1.png`
- Manifest: `art_pipeline/newport_atelier/manifests/newport_atelier_cargo_manifest.json`
- Contact sheet: `art_pipeline/newport_atelier/contact_sheets/newport_atelier_cargo_contact_sheet.png`
- Extraction QA report: `art_pipeline/newport_atelier/reports/newport_atelier_cargo_extraction_qa.json`

No yellow Newport building pixels, third-party sprite sheets, marketplace
assets, web images, or ripped game art were supplied as source inputs.

## Classification

These assets are `green_origin_candidate_pending_license_review`: they are
review-eligible and legally documented as original AI-assisted candidates, but
final-commercial promotion still requires project policy approval for generated
art. They are now the visual target for the city-wide sprite buildout.

The weak deterministic/procedural cargo cluster and the deferred G-4.18D.2
capability proof are deprecated as visual targets. They remain useful as
provenance/process evidence only.

## Generated Assets

- `atelier_newport_crate_01`: `crate_prop`, `green_origin_candidate_pending_license_review`
- `atelier_newport_barrel_01`: `barrel_prop`, `green_origin_candidate_pending_license_review`
- `atelier_newport_rope_coil_01`: `rope_prop`, `green_origin_candidate_pending_license_review`
- `atelier_wharf_cargo_cluster_01`: `crate_barrel_rope_prop_cluster`, `green_origin_candidate_pending_license_review`

## City-Wide Standard

Every future Newport prop, terrain object, UI-world item, character accessory,
dock detail, sign, cart, market good, and building-adjacent dressing sprite
should be judged against this density: believable material construction, crisp
3/4 RPG read, dark painterly contours, muted 1700s Newport palette, salt-worn
surface storytelling, and contact grounding.

Reusable production pattern:

1. 10/10 source sheet.
2. Saved prompt/source artifact.
3. Local extraction script.
4. Transparent sprites with clean bounds and no magenta fringe.
5. Atlas, contact sheet, manifest, provenance report, and QA report.
6. Godot placement using manifest-style IDs, scale, and pivot/grounding data.
7. Automated validation before rollout.

Recommended rollout after this lock: dock clutter expansion, terrain edge
dressing, signs/lamps/posts, market goods/carts, shopfront props, then
NPC/player standards.
