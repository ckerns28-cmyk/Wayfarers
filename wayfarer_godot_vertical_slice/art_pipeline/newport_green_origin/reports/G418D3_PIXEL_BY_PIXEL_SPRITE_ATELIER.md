# G-4.18D.3 Pixel-by-Pixel Sprite Atelier

## Verdict

G-4.18D.3 produced one green-origin dockside rope coil + crate + small barrel cluster from an explicit pixel-layer source.

- Visual verdict: **DEFER**
- Visual rating: **7.1/10** against the 7.5/10 tiny environmental prop gate
- Normal review: **blocked**
- Lab status: **deferred lab-only**
- Provenance: **green-origin candidate**

The sprite is intentionally small (`96x64`) and is rebuilt from a `4x` painterly source that bakes down to 1x. It is not sourced from Newport building pixels, the yellow hero atlas, marketplace art, web images, or third-party game material. Provenance is green, but the asset remains below the chandlery-standard bar and is not eligible for normal review.

## Pixel-Layer Source

Explicit source file:

- `art_pipeline/newport_green_origin/method_bakeoff/source_authored/g418d3_rope_crate_barrel_pixel_layers.json`

Named layer PNG exports:

- `silhouette_blockout`
- `dark_outline`
- `wood_base`
- `rope_base`
- `barrel_base`
- `metal_bands`
- `highlights`
- `chips_scratches`
- `grime`
- `cast_shadow`
- `contact_shadow`

The three visible iteration stages are:

- Pass 01 blockout: `art_pipeline/newport_green_origin/method_bakeoff/generated/g418d3_pass01_blockout.png`
- Pass 02 material/detail: `art_pipeline/newport_green_origin/method_bakeoff/generated/g418d3_pass02_material_detail.png`
- Pass 03 polish/shadow/grounding: `art_pipeline/newport_green_origin/method_bakeoff/generated/g418d3_pass03_polish_shadow_grounding.png`

This rebuild also adds a prop-readability sheet before the in-world judgment:

- Prop readability studies: `art_pipeline/newport_green_origin/contact_sheets/g418d3_prop_readability_studies.png`

## Deliverables

- Final 1x PNG: `art_pipeline/newport_green_origin/method_bakeoff/generated/g418d3_dockside_rope_crate_barrel_cluster.png`
- Inkscape silhouette plan: `art_pipeline/newport_green_origin/method_bakeoff/source_authored/g418d3_painterly_silhouette_plan.svg` and `art_pipeline/newport_green_origin/method_bakeoff/generated/g418d3_painterly_silhouette_plan.png`
- 8x grid inspection: `art_pipeline/newport_green_origin/contact_sheets/g418d3_enlarged_grid_8x.png`
- Before/after contact sheet: `art_pipeline/newport_green_origin/contact_sheets/g418d3_before_after_pixel_atelier.png`
- Palette sheet: `art_pipeline/newport_green_origin/contact_sheets/g418d3_palette_sheet.png`
- Lab-only in-world comparison: `art_pipeline/newport_green_origin/contact_sheets/g418d3_lab_in_world_comparison.png`
- chandlery-standard comparison: `art_pipeline/newport_green_origin/contact_sheets/g418d3_standard_comparison_chandlery_wharf.png`
- Prop readability studies: `art_pipeline/newport_green_origin/contact_sheets/g418d3_prop_readability_studies.png`
- HUD atelier board: `art_pipeline/newport_green_origin/contact_sheets/g418d3_pixel_sprite_atelier_board.png`
- Sprite-sheet assembly: `art_pipeline/newport_green_origin/method_bakeoff/generated/g418d3_dockside_rope_crate_barrel_sprite_sheet.png`
- Image inspection JSON: `art_pipeline/newport_green_origin/method_bakeoff/reports/g418d3_pixel_sprite_image_inspection.json`
- Krita log: `art_pipeline/newport_green_origin/method_bakeoff/reports/g418d3_krita_log.json`
- GIMP log: `art_pipeline/newport_green_origin/method_bakeoff/reports/g418d3_gimp_log.json`

## Tool Path

Python/Pillow rendered the named layers through the `4x` painterly source, baked the final 1x transparent PNG, composited the three passes, generated the separate prop-readability studies, assembled the sprite sheet, generated alpha/crop/palette/contrast checks, and produced 1x/8x review artifacts.

Krita CLI opened the pass 03 pixel composite and exported the 1x projection to `art_pipeline/newport_green_origin/method_bakeoff/generated/g418d3_dockside_rope_crate_barrel_krita_raw.png`. The actual refinement decisions before that projection were the named polish layers: tighter object outlines, rope coil ticks, barrel hoop highlights, crate chips, grime, cast shadow, and contact shadow.

GIMP loaded the Krita projection and re-exported the final transparent PNG with PNG cleanup and metadata suppression. The GIMP log records a post-export Script-Fu crash/timeout after the PNG was already written, so the export path is documented but not treated as a clean tool run. The final alpha/crop/palette checks are recorded in `art_pipeline/newport_green_origin/method_bakeoff/reports/g418d3_pixel_sprite_image_inspection.json`.

Inkscape was used only for silhouette planning and exported `art_pipeline/newport_green_origin/method_bakeoff/generated/g418d3_painterly_silhouette_plan.png`. That vector plan did not become the final sprite; the final PNG comes from the named painterly pixel layers and the Krita/GIMP projection/cleanup path.

## Visual Acceptance

This pass is **more readable than the rejected blended/token attempts**, but it still does not meet visual acceptance. It is blocked from normal review and must remain lab-only.

- Silhouette: separate 3/4 crate, small upright barrel, and foreground rope coil replace the previous one-blob composition.
- Palette: warmer, dirtier Newport browns and rope tones are closer to the chandlery/wharf prop language.
- Texture: rope fibers, wood planks, chips, barrel staves, metal bands, and grime are now material cues instead of only symbolic marks.
- Shadow: cast shadow and object-specific contact occlusion seat the cluster more clearly.
- Integration: the lab-only comparison is clearer, but the sprite still lacks the full painterly density and confidence of the chandlery standard.

The visual rating is 7.1/10, below the 7.5/10 tiny-prop gate. The report therefore treats this as a deferred lab proof, not acceptable asset progress.

## Provenance Gate

The asset is green-origin candidate material:

- No Newport/yellow source pixels copied or sampled.
- No third-party, marketplace, ripped, web-scraped, or mystery source pixels.
- Source data is project-authored pixel/layer instructions plus project-owned palette/style notes.
- Existing Newport building art is used only for visual comparison in generated contact sheets.

## Failure-Rule Answers

Did the pixel-by-pixel workflow improve over G-4.18D.2?

Yes, but only after abandoning the hard 8-bit token grammar and separating the problem into crate/barrel/rope readability studies before assembly. The rebuilt pass uses explicit painterly source layers, visible material decisions, and a real standard-comparison loop. It still does not prove final production quality.

Did the asset fail because of silhouette, palette, texture, shadow, scale, or integration?

It remains deferred primarily because of material finish, painterly edge confidence, scale integration, and the sense of being authored by the same hand as the chandlery props. Object readability, palette, and grounding are materially improved but still below the target standard.

What exact pixel/art changes would be required to raise it further?

- Increase painterly density without creating noise: more shaded bevel transitions, softened dark edges, and less evenly spaced scratch detail.
- Paint the three objects from larger hand-approved studies, then downsample and re-pixel only after each prop reads at 1x.
- Add stronger local occlusion where the rope sits in front of the barrel and where the crate side meets the floor.
- Tune the in-engine placement against the chandlery frontage until the candidate reads as part of the world at actual scale.
- Keep the large standard-comparison board visible on every pass before accepting the next iteration.

Should G-4.18D.4 continue pixel atelier work, or pivot?

Continue pixel atelier work, but only in this richer miniature-painting direction. The roadmap should abandon hard-token/8-bit prop grammar for Newport and use green-origin painterly sprites with explicit standard comparison, human art review, and stronger source-layer discipline.
