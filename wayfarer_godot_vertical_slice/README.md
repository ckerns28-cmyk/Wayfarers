# Wayfarer Godot Vertical Slice

This is a separate Godot 4.x prototype for testing whether Wayfarer should move
away from the custom JavaScript canvas engine. The existing JavaScript build
remains untouched in `wayfarer_v7_github_ready/` and should be treated as the
reference prototype.

## Scope

- One small Newport/Hearthvale harbor-town scene.
- Top-down player movement with collision and camera follow.
- Layered map structure: ground, roads/plaza, wharf/water, props, collision/navigation.
- Seventeen active starter-harbor building objects across civic, residential, commercial, support, and dock bands.
- Each building is a Godot object with sprite, parcel rule, foot/y-sort anchor, collision shape, door anchor, and interaction/frontage area.
- Newport Visual Cohesion and Asset Provenance gates now guard surfaces, props, player/NPC/monster art, equipment, VFX, and UI-world objects before review acceptance.
- G-4 cannot exit until the origin city reaches an 8.0+ visual foundation in
  screenshot review; see `docs/G4_VISUAL_FOUNDATION_CHARTER.md`.
- The G-4.16 surface kit remains the fallback outside the hero area.
- G-4.18 adds the proprietary Newport asset factory and restyles the central commercial-row atlas proof for street, curb/stoop, base shadow, grass edge, and dock transition.
- G-4.18D locks the Newport atelier cargo sheet as the new prop quality bar; normal cargo placement now uses extracted transparent atelier sprites instead of the weak deterministic/procedural cargo cluster.
- G-4.19A adds the first follow-on themed atelier rollout pack: Newport dock clutter, with saved prompt/source, extracted transparent sprites, atlas/contact sheet, manifest, provenance report, QA, and controlled wharf placement.
- G-4.19B adds the Newport visual production registry and core asset audit, shifting future work from isolated sheets to atelier production waves for a believable playable starting town.
- G-4.20A is the first mass atelier production wave: Newport environmental believability, adding controlled terrain-edge, cobble/path, shoreline/harbor, and building-grounding assets while keeping building rebuilds and the Tavern/Inn centerpiece pass deferred.
- G-4.20B is the Town Identity atelier wave: signage, lamps, wayfinding, civic/market markers, and shopfront support assets that improve Newport readability and navigation while keeping core building rebuilds and the Tavern/Inn centerpiece pass deferred.
- G-4.21A begins the Newport core building atelier rebuild with a controlled Tavern/Inn hero asset, mercantile, wharf warehouse, two cottage variants, and cooperage/service building. The Tavern/Inn is brick, Hotel Viking-inspired without direct copy, and uses two front/back bridged twin-stack chimney sets.
- Green-origin art is required, but weak green-origin proof art must be
  quarantined from normal review if it lowers the screenshot bar.
- NPCs are disabled for the current town-layout review pass.
- Minimal HUD with build identity, review host, and interaction/dialogue feedback.

## Controls

- Move: WASD or arrow keys
- Interact: E
- Toggle no-HUD screenshot review mode: F4
- Toggle Green-Origin Lab proof mode: F6
- Toggle full debug overlay (visual bounds / lot bounds / collision footprint / interaction / anchors): F3
- Toggle building seating overlay only: B
- Toggle HUD review metadata: F2

## Run

Open this folder in Godot 4.x and run `res://scenes/Main.tscn`.

## Validation

Run the scene-contract check from this folder:

```sh
godot --headless --path . --script res://tools/validate_vertical_slice.gd
```

Validation is not visual acceptance. A G-4 pass is accepted as visual progress
only when the screenshot packet shows a better authored Newport origin city.

Current G-4.18 review captures should be stored in `artifacts/screenshots/g418/`:

- `normal_full_harbor.png`
- `no_hud_full_harbor.png`
- `no_hud_hero_commercial_strip_closeup.png`
- `dock_harbor_closeup.png`
- `provenance_safe_hero_asset_proof.png`
- `debug_overlay_proof.png`

The repeatable capture path is documented in
`art_pipeline/newport/reports/G417_G418_ASSET_PROVENANCE_AUDIT.md` and the
review scripts/artifacts generated for this pass.

## Web Delivery

See `WEB_DELIVERY.md`. The Godot slice exports to `web_build/` (gitignored)
via `tools/export_web.sh`, then `tools/package_itch_web.sh` creates the
manual HTML5 ZIP used for itch review. The stable upload path is
`artifacts/wayfarers-tale-godot-web.zip`; the script also creates a versioned
ZIP such as `artifacts/wayfarers-tale-godot-g-4-18-newport-proprietary-asset-factory-style-unification.zip`.

## Slice Intent

This project is not a migration. It is a placement/depth/collision test bed
to answer whether Godot solves the seating problems that the
JavaScript/canvas implementation kept fighting.
