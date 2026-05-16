# G-4.17 Screenshot Review Path

All review screenshots are local evidence and should stay under
`artifacts/screenshots/g417/`, which is ignored by Git.

Required captures for this and future Newport art passes:

- `normal_full_harbor.png`: default HUD, normal review mode, full starter harbor framing.
- `no_hud_full_harbor.png`: press `F4` or launch with `--review-no-hud`.
- `hero_street_atlas_closeup.png`: central commercial row around the mercantile, counting house, and chandlery.
- `dock_harbor_closeup.png`: lower wharf/dock transition and harbor edge.
- `debug_overlay_proof.png`: press `F3` for object contracts; press `B` only when seating overlay proof is specifically needed.

G-4.18C adds the Green-Origin Lab comparison packet:

- `normal_review_dock_without_failed_green_origin_proof.png`: same dock area
  with the failed proof hidden from normal review.
- `green_origin_lab_mode_proof.png`: full scene with `F6` or
  `--show-green-origin-lab` enabled.
- `green_origin_lab_mode_dock_proof_closeup.png`: same dock area with the
  lab-only proof visible and labeled.

## G-4 Visual Foundation Review Rule

Wayfarer cannot exit G-4 until the origin city reaches an 8.0+ visual
foundation in screenshot review.

For G-4.22 and every visual pass leading into it, the review packet must show:

- normal full-harbor HUD capture
- no-HUD full-harbor capture
- hero street/dock close-up that looks like the real game
- HUD/UI capture proving intentional fantasy/MMORPG styling
- yellow temporary art inventory or capture notes
- green-origin production proof and source/provenance notes
- debug-overlay proof showing contracts without treating debug visuals as
  player-facing art

Rating rules:

- A validator pass is not an art pass.
- If screenshots do not look better, the pass is not accepted as visual
  progress.
- Green-origin art is required for final production, but weak green-origin art
  must be quarantined from normal review if it lowers the visual bar.
- Green-Origin Lab mode is provenance/debug evidence, not normal review art.
- The 8.0+ rating must be argued from the screenshots: authored town read,
  unified art direction, non-dominating placeholders, real-game hero slice,
  fantasy/MMORPG HUD, yellow-art clarity, and proven green-origin method.

Mini PC workflow:

1. Run `tools/package_itch_web.sh` from the repo root or Godot slice.
2. Upload `artifacts/wayfarers-tale-godot-web.zip` to itch if reviewing the public page.
3. Open the browser build in Chrome and confirm the HUD shows the current phase label.
4. Capture the required normal and no-HUD images. Normal and no-HUD captures must not show hard parcel/debug rectangles or failed lab-only art.
5. For G-4.18C, press `F6` or launch with `--show-green-origin-lab` only for the lab proof captures.
6. Compare the hero street atlas close-up against the building sprites. The pass is not complete if the street, curb, base shadows, grass edge, or hero props still read as layout markers.

Local build review should serve `web_build/index.html` with the same isolation
and MIME headers documented in `_headers`:

```sh
python wayfarer_godot_vertical_slice/tools/serve_web_build.py --directory wayfarer_godot_vertical_slice/web_build --port 8765
```

Itch review remains the player-facing browser evidence path.
