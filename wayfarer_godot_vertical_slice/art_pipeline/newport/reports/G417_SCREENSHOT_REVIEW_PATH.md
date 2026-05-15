# G-4.17 Screenshot Review Path

All review screenshots are local evidence and should stay under
`artifacts/screenshots/g417/`, which is ignored by Git.

Required captures for this and future Newport art passes:

- `normal_full_harbor.png`: default HUD, normal review mode, full starter harbor framing.
- `no_hud_full_harbor.png`: press `F4` or launch with `--review-no-hud`.
- `hero_street_atlas_closeup.png`: central commercial row around the mercantile, counting house, and chandlery.
- `dock_harbor_closeup.png`: lower wharf/dock transition and harbor edge.
- `debug_overlay_proof.png`: press `F3` for object contracts; press `B` only when seating overlay proof is specifically needed.

Mini PC workflow:

1. Run `tools/package_itch_web.sh` from the repo root or Godot slice.
2. Upload `artifacts/wayfarers-tale-godot-web.zip` to itch if reviewing the public page.
3. Open the browser build in Chrome and confirm the HUD shows `Godot G-4.17 Newport Asset Pipeline + Hero Street Atlas`.
4. Capture the five images above. Normal and no-HUD captures must not show hard parcel/debug rectangles.
5. Compare the hero street atlas close-up against the building sprites. The pass is not complete if the street, curb, base shadows, grass edge, or hero props still read as layout markers.

Local build review should serve `web_build/index.html` with the same isolation
and MIME headers documented in `_headers`:

```sh
python wayfarer_godot_vertical_slice/tools/serve_web_build.py --directory wayfarer_godot_vertical_slice/web_build --port 8765
```

Itch review remains the player-facing browser evidence path.
