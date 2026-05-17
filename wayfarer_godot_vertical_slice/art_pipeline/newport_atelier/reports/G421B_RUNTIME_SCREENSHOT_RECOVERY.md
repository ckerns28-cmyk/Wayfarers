# G-4.21B Runtime Screenshot Recovery

Status: PASS

## Root Cause

The failed G-4.21A runtime proof attempt used true Godot headless mode for a viewport screenshot workflow. Godot maps `--headless` to the headless display driver, which is not a reliable visual rendering path for runtime screenshots in this project. The same failed path also let Godot use its default `user://logs` target under `C:/Users/Chris/AppData/Roaming/Godot/app_userdata/Wayfarer Godot Vertical Slice/logs`; under the sandboxed run, Godot printed `Failed to open 'user://logs/godot2026-05-16T21.00.04.log'` and then crashed before producing screenshots.

`project.godot` has no custom user directory or repo-local file logging override. The project path was correct, output directory creation was not the blocker, and the asset/import validations remained green.

## Recovery

Added a deterministic non-headless capture path:

- `res://tools/capture_g421b_runtime_screenshots.gd`
- `tools/capture_g421b_runtime_screenshots.ps1`

The capture script refuses the headless display driver, creates the output directory before writing, starts `res://scenes/Main.tscn`, enables review/no-HUD mode through `set_review_screenshot_mode(true)`, waits for render frames, positions the player/camera at each requested review target, saves PNGs, and writes a manifest.

Command used on this machine:

```powershell
.\tools\capture_g421b_runtime_screenshots.ps1 -GodotBin "C:\Users\Chris\Downloads\Godot_v4.6.2-stable_win64.exe\Godot_v4.6.2-stable_win64_console.exe"
```

The wrapper expands to Godot runtime capture with:

```powershell
--path "C:\Users\Chris\Documents\New project\wayfarer_godot_vertical_slice" --windowed --resolution 1600x1000 --display-driver windows --rendering-driver opengl3 --rendering-method gl_compatibility --log-file "C:\Users\Chris\Documents\New project\wayfarer_godot_vertical_slice\artifacts\review\g421b_runtime_screenshots\godot_capture.log" --script res://tools/capture_g421b_runtime_screenshots.gd
```

Capture mode:

- Non-headless: yes
- Display driver: Windows
- Rendering method: `gl_compatibility`
- Rendering driver: `opengl3`
- Godot version: 4.6.2-stable (official)
- HUD hidden: yes

## Screenshot Artifacts

Generated repo-local review artifacts:

- `artifacts/review/g421b_runtime_screenshots/g421b_01_whole_town.png`
- `artifacts/review/g421b_runtime_screenshots/g421b_02_tavern_inn_closeup.png`
- `artifacts/review/g421b_runtime_screenshots/g421b_03_market_spine.png`
- `artifacts/review/g421b_runtime_screenshots/g421b_04_wharf.png`
- `artifacts/review/g421b_runtime_screenshots/g421b_05_res_small.png`
- `artifacts/review/g421b_runtime_screenshots/g421b_06_cooperage_shed.png`
- `artifacts/review/g421b_runtime_screenshots/g421b_runtime_screenshot_manifest.json`
- `artifacts/review/g421b_runtime_screenshots/godot_capture.log`

The artifacts directory is intentionally git-ignored; these files are local proof outputs, not source assets.

## Capture Coordinates

- `g421b_01_whole_town.png`: whole town / broad Newport view, player `Vector2(800, 575)`, zoom `Vector2(0.72, 0.72)`, offset `Vector2(0, -20)`
- `g421b_02_tavern_inn_closeup.png`: `b_inn_tavern`, player `Vector2(254, 616)`, zoom `Vector2(1.18, 1.18)`, offset `Vector2(0, -92)`
- `g421b_03_market_spine.png`: `b_mercantile`, player `Vector2(580, 616)`, zoom `Vector2(1.12, 1.12)`, offset `Vector2(0, -72)`
- `g421b_04_wharf.png`: `b_dock_warehouse`, player `Vector2(486, 758)`, zoom `Vector2(1.04, 1.04)`, offset `Vector2(0, -64)`
- `g421b_05_res_small.png`: `b_res_small`, player `Vector2(437, 432)`, zoom `Vector2(1.02, 1.02)`, offset `Vector2(0, -44)`
- `g421b_06_cooperage_shed.png`: `b_cooperage_shed`, player `Vector2(264, 432)`, zoom `Vector2(1.08, 1.08)`, offset `Vector2(0, -44)`

## Verification

- Capture log scan for `ERROR`, `WARNING`, `SCRIPT ERROR`, `Crash`, and `Failed`: PASS, no matches
- PNG count: PASS, 6 files
- PNG readability: PASS, all files opened through Pillow
- PNG dimensions: PASS, all files are 1600x1000 and non-empty

## Validation

- Godot import validation: PASS
- `validate_vertical_slice.gd`: PASS, `failureCount=0`
- `validate_newport_asset_provenance.py`: PASS
- G-4.21A extraction script validation: PASS
- Asset hygiene: PASS
- `git diff --check`: PASS

No new art, gameplay, placement, balance, release build, or itch upload work was performed.
