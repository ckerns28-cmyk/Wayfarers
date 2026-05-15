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
  `debug_overlay_proof.png`. The final reviewed capture set was refreshed from
  the rebuilt web package after the source-ref prop sheet and wharf draw-order
  corrections.

## Asset Provenance

- No scraped web art was used.
- The style reference extractor reads only in-repository building sprites.
- The prior project prop sheet
  `wayfarer_v7_github_ready/worker/assets/wayfarer/props/hearthvale_props_atlas_v1_transparent.png`
  and its manifest were copied into `art_pipeline/newport/source_refs/` as
  project-owned source refs after review feedback called out that these sheets
  were expected to be incorporated.
- The hero street atlas is project-owned generated/derived bitmap art produced
  by `art_pipeline/newport/scripts/generate_hero_street_atlas.py`. Road, curb,
  base-shadow, and wharf materials are derived from Newport building sprite
  crops; props and secondary objects are cropped from the prior project prop
  atlas where available.
- Review eligibility, placeholder/final flags, atlas regions, source,
  ownership, license, scale, collision, y-sort, and contact-shadow requirements
  are recorded in `art_pipeline/newport/manifests/newport_hero_street_assets.json`.

## Review Feedback Response

The first G-4.17 proof still read as mismatched procedural ground art below
high-detail buildings. The follow-up revision tightens the proof area by
tiling the derived atlas across the full central commercial row and wharf edge,
then replacing the hand-drawn hero props with crops from the project-owned
prior prop sheet. The prop-cluster generator was also corrected so wharf and
shop clusters stay transparent with contact shadows instead of carrying
rectangular building-background fragments from their source crops.

The browser review still shows that the broader harbor wharf and building-dock
angle language needs its own atlas pass. G-4.17 proves the pipeline and raises
the central proof area, but it does not mark the entire dock/wharf system final.

## Known Blocker

The current player remains a temporary scale/debug avatar. A dedicated player
sprite-sheet pipeline pass is required before character art can be accepted.
NPCs and monsters should not be introduced until character style rules exist,
and equipment, armor, weapons, and combat VFX must match the future
player/NPC sprite detail.
