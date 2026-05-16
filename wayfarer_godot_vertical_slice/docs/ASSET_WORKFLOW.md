# Godot Asset Workflow

This document defines the source-of-truth and import discipline for the
Wayfarer Godot vertical slice. It applies only to
`wayfarer_godot_vertical_slice/`; the JavaScript Worker remains the separate
Phase 35.13R production/reference route.

## Current Inventory

Tracked Godot asset folders:

- `assets/buildings/`: current building atlas PNGs used by the vertical slice.
- `art_pipeline/newport/`: G-4.18 source refs, generated assets/contact sheets,
  manifests, generated atlases, Blender support scripts, reports, and
  Python/Pillow scripts for Newport terrain/prop production.
- `scenes/`: scene files plus scene scripts and stable `.gd.uid` metadata.
- `scripts/`: shared Godot-side metadata helpers such as `BuildInfo.gd`.

Tracked texture/atlas files:

- `assets/buildings/hearthvale_buildings_atlas_v1.png`
- `assets/buildings/hearthvale_newport_structure_pack_v1_a.png`
- `assets/buildings/hearthvale_newport_structure_pack_v1_b.png`

Tracked Godot import metadata:

- `assets/buildings/hearthvale_buildings_atlas_v1.png.import`
- `assets/buildings/hearthvale_newport_structure_pack_v1_a.png.import`
- `assets/buildings/hearthvale_newport_structure_pack_v1_b.png.import`

Generated local files and folders:

- `.godot/`
- `web_build/`
- `artifacts/`
- `*.zip` review packages
- `._*` AppleDouble sidecars from some external drive formats

Source-of-truth ambiguity found in G-4:

- Current building atlas PNGs are already Godot-ready atlases, but the original
  source art is not separated from the atlas sheets yet.
- Reference/debug screenshots were previously tracked under `artifacts/`, which
  is the generated review-output folder. G-4 removes those from the Git index
  and reserves `assets/references/` for future committed reference screenshots.

## Source-Of-Truth Layout

Do not move the current atlas PNGs in this pass. For the existing slice,
`assets/buildings/` remains the canonical atlas location.

Future additions should use this layout:

```text
wayfarer_godot_vertical_slice/assets/
  source/       Original art, layered files, untrimmed source exports.
  sprites/      Individual Godot-ready sprites, if not atlas-packed yet.
  atlases/      New atlas sheets and atlas manifests.
  references/   Committed reference screenshots or visual targets.
```

Current compatibility rule:

- Existing building atlases stay in `assets/buildings/` until a deliberate
  migration pass moves them and updates every `res://` reference.
- Newport production-pipeline outputs live in `art_pipeline/newport/` while the
  pipeline is being established. Any generated/imported asset used in the
  review build must have a manifest entry with source, ownership/license,
  provenance status, placeholder/final state, and review eligibility.
- No asset enters the player-facing review build unless it passes both Newport
  Visual Cohesion and Asset Provenance gates.
- Green-origin art is required for final production, but green-origin alone is
  not enough. Weak source-safe proof art must be quarantined from normal review
  if it lowers screenshot quality.
- Yellow art is temporary review art only and must be clearly marked in
  manifests, review notes, and replacement queues.
- New atlas families should prefer `assets/atlases/<domain>/`.
- New original art should go in `assets/source/<domain>/`.
- New committed reference screenshots should go in `assets/references/<phase>/`.
- Local screenshots made during browser/export review stay in `artifacts/` and
  are ignored.
- The Web export preset excludes `artifacts/**`, `web_build/**`, generated ZIP
  files, and `art_pipeline/newport/source_refs/**` so local review evidence and
  historical source-reference pixels do not get packed into `index.pck`.

Sprite and atlas metadata lives in:

- `SPRITE_ATLAS_GODOT.md` for current atlas cells and regions.
- `docs/SPRITE_ANCHORS.md` for origin, grounding, collision, and y-sort rules.
- `art_pipeline/newport/manifests/*.json` for Newport style values and terrain/
  prop asset manifests.

## Import Discipline

Commit these files:

- Source art and Godot-ready asset files that are part of the project.
- Stable Godot `.import` files for tracked assets.
- Stable `.gd.uid` files generated for tracked scripts.
- `.tscn`, `.gd`, `.cfg`, and documentation files.

Do not commit these files:

- `.godot/` editor/import cache output.
- `web_build/` browser export output.
- `artifacts/` review screenshots, package output, and local evidence.
- Generated ZIP files.
- `.DS_Store` or `._*` AppleDouble metadata.

Do not export these files into browser builds:

- `artifacts/**`
- `web_build/**`
- `*.zip`
- `art_pipeline/newport/source_refs/**`

Texture import expectations for the current atlas PNGs:

- `compress/mode=0`
- `mipmaps/generate=false`
- `process/fix_alpha_border=true`
- `process/premult_alpha=false`
- `metadata.vram_texture=false`

Rendering expectations:

- Project texture filtering remains nearest:
  `textures/canvas_textures/default_texture_filter=0`.
- Pixel snapping remains enabled:
  `rendering/2d/snap/snap_2d_transforms_to_pixel=true` and
  `rendering/2d/snap/snap_2d_vertices_to_pixel=true`.
- Building sprites explicitly use nearest filtering in `Building.gd`.

## Atlas And Naming Rules

Atlas expectations:

- Current building atlas sheets are 3 x 3 grids of 418 px cells.
- Region rectangles must stay inside the tight sprite bounds documented in
  `SPRITE_ATLAS_GODOT.md`.
- No region may bleed across a neighboring cell boundary.
- Atlas region changes require a validator run and visual review package.

Naming conventions:

- Buildings: stable snake_case ids, e.g. `inn_tavern`, `dock_storehouse`.
- Props: stable snake_case ids grouped by prop family.
- Player/NPCs: scene names use PascalCase; ids and groups use snake_case.
- Terrain, water, and roads: name by material plus tile or region purpose,
  e.g. `worn_path`, `shallow_water`, `harbor_pier`.
- New atlas files should include domain, pack name, and version:
  `<domain>_<pack>_v<major>.png`.

## Review Workflow For Art Updates

1. Add or update source art in the appropriate asset source folder.
2. Add or update Godot-ready sprites or atlases.
3. Let Godot regenerate stable `.import` metadata, then commit it with the
   asset.
4. Document atlas regions and anchor assumptions.
5. Add or update the Newport manifest entry, including source, exact crop path
   and crop rectangle when copied pixels are used, license/ownership,
   provenance status, placeholder/final flag, and review eligibility.
6. Run `bash wayfarer_godot_vertical_slice/tools/validate_asset_hygiene.sh`.
7. Run `bash wayfarer_godot_vertical_slice/tools/package_itch_web.sh`.
8. Upload `wayfarer_godot_vertical_slice/artifacts/wayfarers-tale-godot-web.zip`
   to itch manually.
9. Hard-refresh `https://wayfarersguild.itch.io/wayfarers-tale` and confirm the
   on-screen build label before visual review.
10. Capture the required screenshot packet and evaluate whether the pass
    improves the origin city. A validator pass is not an art pass.
11. Do not recommend G-5 until G-4.22 accepts the 8.0+ visual foundation gate.

Cloudflare Pages remains deferred for the current stock export because
`index.wasm` exceeds the 25 MB Direct Upload single-file limit.
