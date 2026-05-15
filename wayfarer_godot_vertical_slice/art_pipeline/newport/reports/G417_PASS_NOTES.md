# G-4.17 Pass Notes

## Tool Use

- GitHub connector: used for preflight. PR #430 was confirmed merged with merge commit `b8b1785e`, and no open PRs targeting `main` were found before feature work.
- Local Git/Godot/Python/Pillow: used for branch creation, asset extraction, atlas generation, Godot import, and vertical-slice validation.
- Game Studio plugin: inspected available asset-pipeline guidance. It was not used to generate, transform, or validate files because the available skill was focused on browser 3D GLB/glTF assets, while this pass required Godot 2D bitmap atlas work under the Newport Visual Cohesion Rules.
- Chrome/browser review: used against the local exported `web_build/` served
  by `tools/serve_web_build.py`. One-shot Chrome screenshots captured the
  Godot loader too early, so final evidence was captured through Chrome DevTools
  Protocol after the canvas reported the game running. Screenshots were written
  under ignored local evidence path `artifacts/screenshots/g417/`:
  `normal_full_harbor.png`, `no_hud_full_harbor.png`,
  `hero_street_atlas_closeup.png`, `dock_harbor_closeup.png`, and
  `debug_overlay_proof.png`.

## Asset Provenance

- No scraped web art was used.
- The style reference extractor reads only in-repository building sprites.
- The hero street atlas is project-owned generated bitmap art produced by
  `art_pipeline/newport/scripts/generate_hero_street_atlas.py`.
- Review eligibility, placeholder/final flags, atlas regions, source,
  ownership, license, scale, collision, y-sort, and contact-shadow requirements
  are recorded in `art_pipeline/newport/manifests/newport_hero_street_assets.json`.

## Known Blocker

The current player remains a temporary scale/debug avatar. A dedicated player
sprite-sheet pipeline pass is required before character art can be accepted.
NPCs and monsters should not be introduced until character style rules exist,
and equipment, armor, weapons, and combat VFX must match the future
player/NPC sprite detail.
