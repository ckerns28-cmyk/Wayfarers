# Wayfarer Godot Vertical Slice

This is a separate Godot 4.x prototype for testing whether Wayfarer
should move away from the custom JavaScript canvas engine. The existing
JavaScript build at `wayfarer_v7_github_ready/` continues to serve as
the production site at `/` and is **not** replaced by this slice.

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
- Minimal HUD and one objective: "The Still Water Objective: Speak with Edrin Vale".

## Controls

- Move: WASD or arrow keys
- Interact: E
- Toggle debug overlay (sprite outline / collision / interaction / foot anchor): F3

## Run locally in Godot

Open this folder in Godot 4.x (`File → Open Project`) and run
`res://scenes/Main.tscn`. Confirms the slice without any web export.

## Validation (headless)

```sh
godot --headless --path . --script res://tools/validate_vertical_slice.gd
```

Current review captures live in `artifacts/screenshots/`:

- `vertical_slice_gameplay.png`
- `vertical_slice_collision_debug.png`

## Export Web build locally

```sh
bash wayfarer_godot_vertical_slice/tools/export_web.sh
```

The script:

1. Runs `godot --headless --import` to prime resources.
2. Runs `godot --headless --export-release "Web"` against the `Web`
   preset in `export_presets.cfg`.
3. Writes the canonical export to
   `wayfarer_godot_vertical_slice/export/web/`.
4. Mirrors the export into
   `wayfarer_v7_github_ready/worker/assets/godot/` so the existing
   Cloudflare Worker auto-serves it at `/godot/*` on the next deploy.

Requirements: Godot 4.6.2-stable (Standard, not Mono) on `$PATH`, and
the matching Web export templates installed.

## Cloudflare delivery

The slice is served by the **existing** Cloudflare Worker (top-level
`wrangler.toml` → `wayfarers`), which already deploys the JS site at
`/`. A small additive route was added to the Worker entry
(`wayfarer_v7_github_ready/worker/src/index.js`) so that `/godot/*`
serves files from `wayfarer_v7_github_ready/worker/assets/godot/` with
the Cross-Origin-Opener-Policy / Cross-Origin-Embedder-Policy headers
that Godot's threaded WASM build needs.

| Cloudflare setting              | Value                                                        |
| ------------------------------- | ------------------------------------------------------------ |
| Worker name                     | `wayfarers`                                                  |
| Worker entry (top-level config) | `wayfarer_v7_github_ready/worker/src/index.js`               |
| `[assets].directory`            | `./wayfarer_v7_github_ready/worker/assets`                   |
| `[assets].binding`              | `ASSETS`                                                     |
| Build command                   | *(none — wrangler deploys directly)*                         |
| Output directory                | *(none — `[assets].directory` is the served root)*           |
| New Godot route                 | `/godot/*` → `wayfarer_v7_github_ready/worker/assets/godot/` |

Production preview URL once the Worker redeploys after this commit:

```
https://wayfarers.ckerns28.workers.dev/godot/
```

Until `tools/export_web.sh` runs, that URL serves a placeholder page
labeled `Build label: Godot Vertical Slice (export pending)` so the
route is verifiably live without any Godot binaries committed yet. JS
production at `/` is untouched and continues to ship `Build Phase
35.13R`.

See `WEB_DELIVERY.md` for the full step-by-step including verification
checklist and an alternative separate Cloudflare Pages path if the
route-share approach is ever swapped out.

## Slice Intent

This project is not a migration. It is a placement/depth/collision
test bed to answer whether Godot solves the seating problems that the
JavaScript/canvas implementation kept fighting.
