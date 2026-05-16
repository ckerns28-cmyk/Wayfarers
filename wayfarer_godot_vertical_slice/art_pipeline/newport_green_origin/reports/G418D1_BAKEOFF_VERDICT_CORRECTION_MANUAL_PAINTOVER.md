# G-4.18D.1 Bakeoff Verdict Correction + Manual Paintover Proof

## Result

G-4.18D.1 corrects the bad G-4.18D verdict. M01 is no longer PASS; it is DEFER
/ raw material only. M02-M05 are FAIL. G-4.18D produced no accepted visual
candidate.

M01B was created as a focused manual paintover proof from M01. It improves
contact grounding, rope/net readability, grime, edge breakup, and palette
warmth, but it still does not meet the 8.5 visual bar beside the current
Newport art. M01B is DEFER and lab-only.

## Tools Used

- Git/GitHub: started from latest `origin/main`, confirmed PR #438 was merged,
  and confirmed no open PRs targeted `main`.
- Python/Pillow: authored the M01B paint plan, alpha/crop/contrast checks,
  palette-distance checks, proof boards, and comparison frames.
- Inkscape: constructed and exported the M01B net/rope/signage silhouette
  overlay from project-authored SVG.
- Krita: opened the prepared M01B paintover source and exported the projection
  to PNG. The kritarunner layer-paint path was attempted, but the mini PC
  produced runner argument/resource-database failures and openDocument timeout
  behavior, so no PASS was claimed from that path.
- GIMP 3.2.4: loaded the Krita export and re-exported PNG with transparency
  preservation and metadata/chunk cleanup; GIMP completed the file export but
  required timeout handling after export.
- Godot/Chrome: required for scene validation, web export, and browser screenshot
  review.

## M01B Verdict

| Item | Status |
| --- | --- |
| Provenance | green-origin candidate |
| Visual rating | 7.8 / 10 |
| PASS gate | 8.5 / 10 plus screenshot acceptance |
| Verdict | DEFER |
| Review scope | lab-only |
| Promotion | blocked |

Why M01B does not pass:

- The paintover is closer to wharf material language, but the base still reads
  too slab-like at actual scale.
- The detail density and lighting remain weaker than the current Newport
  building-adjacent prop clusters.
- The proof improves the evidence packet, but it does not yet improve the normal
  player-facing screenshot.

## Evidence Packet

- Isolated M01B proof:
  `art_pipeline/newport_green_origin/contact_sheets/g418d1_m01b_isolated_proof.png`
- In-world comparison frame:
  `art_pipeline/newport_green_origin/contact_sheets/g418d1_m01b_in_world_comparison_frame.png`
- Corrected bakeoff board:
  `art_pipeline/newport_green_origin/contact_sheets/g418d1_corrected_bakeoff_board.png`
- Image inspection:
  `art_pipeline/newport_green_origin/method_bakeoff/reports/g418d1_m01b_image_inspection.json`
- Krita log:
  `art_pipeline/newport_green_origin/method_bakeoff/reports/g418d1_krita_paintover_log.json`
- GIMP log:
  `art_pipeline/newport_green_origin/method_bakeoff/reports/g418d1_gimp_cleanup_log.json`

## Production Recommendation

Do not promote M01B. Keep it lab-only as proof that manual cleanup can improve a
green-origin substrate, but use a stronger production path next: a deliberately
painted green-origin prop sheet with thumbnails, silhouette approval, dedicated
Krita paint time, and screenshot comparison before any manifest PASS.
