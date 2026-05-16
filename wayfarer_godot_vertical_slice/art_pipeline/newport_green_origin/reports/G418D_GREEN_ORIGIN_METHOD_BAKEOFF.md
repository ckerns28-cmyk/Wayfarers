# G-4.18D Green-Origin Method Bakeoff

## Result

G-4.18D compares green-origin production methods for dockside/wharf clutter
and surface-integration art without advancing normal review art. The normal
player-facing build remains the G-4.18C protected baseline; all bakeoff samples
are lab-only evidence.

G-4.18D does not advance normal review art unless a candidate is later accepted
by screenshot review in a later phase.

## North Star Relevance

Wayfarer needs a commercial-safe art pipeline that can eventually support an
MMORPG-scale origin city, not just one-off validator-green props. The Newport
harbor must feel like the player's first real home base: weathered, grounded,
readable, and cohesive beside the current high-quality building sprites.

The bakeoff focuses on the asset family most likely to reveal pipeline truth:
dockside planks, pilings, rope, crates, barrels, grime, shadows, waterline
contact, and work-area dressing.

## Current Failure Being Addressed

G-4.18B proved provenance infrastructure, but the generated dock proof failed
visually. It read as tiny, pasted-on, under-grounded clutter. G-4.18C correctly
quarantined that proof behind Green-Origin Lab mode. G-4.18D asks which method
has the best chance of producing green-origin art that can eventually match the
Newport building quality.

## Tools Used

- Git/GitHub: confirmed PR #437 merged into `main`, no open PRs targeted
  `main`, and the branch started from latest `origin/main`.
- Python/Pillow: generated candidate samples, proof boards, alpha/crop checks,
  contrast checks, hashes, and the method manifest.
- Inkscape: exported the reference-board-guided vector silhouette candidate.
- GIMP 3.2.4: verified installed for PNG cleanup and future manual export
  sanity; kept repo outputs repeatable through Pillow for this bakeoff.
- Krita: verified available as the appropriate manual paint cleanup tool for
  the recommended G-4.18E method; no interactive paint edits were promoted in
  this automated bakeoff.
- Godot: validates lab-only wiring and exports the review build.
- Chrome: captures exported-build screenshots for normal and lab review.

## Candidate Comparison

| Candidate | Method | Visual Rating | Provenance / Legal | Risk | Recommendation |
| --- | --- | ---: | --- | --- | --- |
| M01 | Generated base + pixel-paint/manual cleanup pipeline | 7.2 | `green_origin_candidate`, project-owned, no yellow or third-party pixels | Requires real Krita/GIMP paint cleanup and art-direction time; generator alone is not enough | PASS |
| M02 | Procedural sprite assembly from green-origin primitive parts | 5.8 | `green_origin_candidate`, project-owned, no yellow or third-party pixels | Fast but modular; likely to become sticker clutter without paintover | DEFER |
| M03 | Reference-board-guided green-origin generation with Newport constraints | 6.1 | `green_origin_candidate`, Inkscape/Pillow authored shapes, no yellow or third-party pixels | Good silhouettes, too vector-clean without raster dirt and painterly shading | DEFER |
| M04 | Hybrid kitbash from internally generated green-origin parts only | 6.4 | `green_origin_candidate`, internal generated parts only | Promising once parts improve; inherits weak primitive vocabulary today | DEFER |
| M05 | Godot-authored environmental dressing using drawn shapes and shadows | 5.2 | `green_origin_candidate`, authored code shapes, no yellow or third-party pixels | Useful for scene grounding and debug proof, too flat for final commercial sprites | FAIL |

## Recommendation For G-4.18E

Advance M01 as the G-4.18E production method: generated base plus real
Krita/GIMP pixel-paint cleanup, then screenshot-gated review before any normal
review promotion. It has the strongest path to matching the current Newport
building quality because it combines repeatable green-origin generation with
human art direction, palette harmonization, grime, contact shadows, and scale
correction.

M04 is the backup method once M01 creates a stronger internal green-origin part
vocabulary. M02 and M03 remain useful support methods, but neither should drive
hero-quality asset production alone. M05 should remain a Godot dressing/debug
technique only.

## Lab-Only Evidence

- Manifest:
  `art_pipeline/newport_green_origin/manifests/green_origin_method_bakeoff_manifest.json`
- Bakeoff board:
  `art_pipeline/newport_green_origin/contact_sheets/g418d_method_bakeoff_board.png`
- Candidate strip:
  `art_pipeline/newport_green_origin/contact_sheets/g418d_candidate_comparison_strip.png`
- Automated image inspection:
  `art_pipeline/newport_green_origin/method_bakeoff/reports/g418d_image_inspection.json`

All candidates remain `normal_review_eligible=false`, `lab_only=true`, and
`final_commercial_eligible=false`. The single PASS recommendation identifies a
method for the next experiment, not a final-commercial asset.
