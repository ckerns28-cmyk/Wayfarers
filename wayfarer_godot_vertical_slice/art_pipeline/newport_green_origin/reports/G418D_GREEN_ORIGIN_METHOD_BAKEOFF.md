# G-4.18D Green-Origin Method Bakeoff

## Corrected Result

G-4.18D produced no accepted visual candidate. The original PASS verdict for
M01 was incorrect: M01 was only the least-bad raw substrate, not Newport-quality
finished art.

M01 is downgraded to DEFER / raw-material candidate only. M02, M03, M04, and
M05 are FAIL for final or normal review art. No G-4.18D candidate is eligible
for normal review, final-commercial promotion, or use as proof that the
green-origin pipeline has reached the required visual bar.

## North Star Relevance

Wayfarer needs a commercial-safe art pipeline that can eventually support an
MMORPG-scale origin city, not validator-green placeholders. The Newport harbor
must feel weathered, grounded, readable, and cohesive beside the current
high-quality building sprites.

The G-4.18D bakeoff remains useful evidence because it exposed the failure
mode: provenance and green validators can pass while the art still looks flat,
pasted-on, and under-authored.

## Corrected Candidate Comparison

| Candidate | Method | Visual Rating | Corrected Verdict | Reason |
| --- | --- | ---: | --- | --- |
| M01 | Generated base + pixel-paint/manual cleanup pipeline | 7.2 | DEFER | Raw substrate only. Too flat and procedural to pass screenshot review. |
| M02 | Procedural primitive assembly | 5.8 | FAIL | Modular, pasted-on, and not Newport-quality. |
| M03 | Reference-board-guided silhouette generation | 6.1 | FAIL | Useful silhouette idea, but too vector-clean and simple. |
| M04 | Internal green kitbash | 6.4 | FAIL | Inherits weak parts and reads as collage clutter. |
| M05 | Godot-authored dressing shapes | 5.2 | FAIL | Debug/blockout technique, not production art. |

## Gate Correction

PASS now requires `visual_rating >= 8.5` plus screenshot acceptance. A candidate
below that bar cannot set `recommendation=PASS`, cannot be
`final_commercial_candidate=true`, and cannot be promoted by validator success
alone.

Legal/provenance status is separate from visual quality:

- provenance green + visual failed/deferred = lab-only
- provenance yellow + visual good = temporary review only
- provenance green + visual good = possible future final-commercial candidate
- unknown source = blocked from final-commercial
- visual failed = blocked from normal review unless explicitly shown in lab/debug

## Lab-Only Evidence

- Corrected manifest:
  `art_pipeline/newport_green_origin/manifests/green_origin_method_bakeoff_manifest.json`
- Corrected bakeoff board:
  `art_pipeline/newport_green_origin/contact_sheets/g418d1_corrected_bakeoff_board.png`
- Corrected candidate strip:
  `art_pipeline/newport_green_origin/contact_sheets/g418d1_candidate_comparison_strip.png`

G-4.18D does not advance normal review art.
