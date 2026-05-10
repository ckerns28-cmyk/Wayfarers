# Wayfarer Godot Vertical Slice

This is a separate Godot 4.x prototype for testing whether Wayfarer should move away from the custom JavaScript canvas engine. The existing JavaScript build remains untouched in `wayfarer_v7_github_ready` and should be treated as the reference prototype.

## Scope

- One small Newport/Hearthvale harbor-town scene.
- Top-down player movement with collision and camera follow.
- Layered map structure: ground, roads/plaza, wharf/water, props, collision/navigation.
- Five production-style building scene instances:
  - inn/tavern
  - dock storehouse
  - custom house
  - merchant shop house
  - large residence
- Each building is a Godot object with sprite, foot anchor, collision shape, and interaction/frontage area.
- One interactable NPC: Edrin Vale.
- Minimal HUD and one objective: “The Still Water Objective: Speak with Edrin Vale”.

## Controls

- Move: WASD or arrow keys
- Interact: E

## Run

Open this folder in Godot 4.x and run `res://scenes/Main.tscn`.

## Validation

Run the scene-contract check from this folder:

```sh
Godot --headless --path . --script res://tools/validate_vertical_slice.gd
```

Current review captures are stored in `artifacts/screenshots/`:

- `vertical_slice_gameplay.png`
- `vertical_slice_collision_debug.png`

## Slice Intent

This project is not a migration. It is a placement/depth/collision test bed to answer whether Godot solves the seating problems that the JavaScript/canvas implementation kept fighting.
