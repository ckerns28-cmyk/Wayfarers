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
- NPCs are disabled for the current town-layout review pass.
- Minimal HUD with build identity, review host, and interaction/dialogue feedback.

## Controls

- Move: WASD or arrow keys
- Interact: E
- Toggle full debug overlay (visual bounds / lot bounds / collision footprint / interaction / anchors): F3
- Toggle building seating overlay only: B

## Run

Open this folder in Godot 4.x and run `res://scenes/Main.tscn`.

## Validation

Run the scene-contract check from this folder:

```sh
godot --headless --path . --script res://tools/validate_vertical_slice.gd
```

Current review captures are stored in `artifacts/screenshots/`:

- `g415/normal_full_harbor.png`
- `g415/normal_upper_band.png`
- `g415/normal_middle_commercial_row.png`
- `g415/normal_dock_band.png`
- `g415/building_seating_overlay.png`
- `g415/door_interaction_prompt.png`
- `g415/street_no_prompt.png`
- `g415/full_debug_overlay.png`

## Web Delivery

See `WEB_DELIVERY.md`. The Godot slice exports to `web_build/` (gitignored)
via `tools/export_web.sh`, then `tools/package_itch_web.sh` creates the
manual HTML5 ZIP used for itch review.

## Slice Intent

This project is not a migration. It is a placement/depth/collision test bed
to answer whether Godot solves the seating problems that the
JavaScript/canvas implementation kept fighting.
