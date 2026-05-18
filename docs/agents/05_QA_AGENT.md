# QA Agent

## Mission

Run or list exact validation commands, classify skipped commands explicitly, and separate technical pass from design acceptance.

## Required Commands

Godot import validation:

```powershell
& 'C:\Users\Chris\Downloads\Godot_v4.6.2-stable_win64.exe\Godot_v4.6.2-stable_win64_console.exe' --headless --path wayfarer_godot_vertical_slice --import
```

Vertical slice validation:

```powershell
& 'C:\Users\Chris\Downloads\Godot_v4.6.2-stable_win64.exe\Godot_v4.6.2-stable_win64_console.exe' --headless --path . --script res://tools/validate_vertical_slice.gd
```

Newport asset provenance:

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" wayfarer_godot_vertical_slice\art_pipeline\newport\scripts\validate_newport_asset_provenance.py
```

G-4.21A extraction validation:

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" wayfarer_godot_vertical_slice\art_pipeline\newport_atelier\scripts\extract_g421a_core_building_assets.py --skip-registry --skip-building-provenance
```

Screenshot capture and PNG verification:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\wayfarer_godot_vertical_slice\tools\capture_g422a_runtime_screenshots.ps1 -GodotBin 'C:\Users\Chris\Downloads\Godot_v4.6.2-stable_win64.exe\Godot_v4.6.2-stable_win64_console.exe'
```

Pre-G-5 runtime sprite consistency:

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" wayfarer_godot_vertical_slice\tools\validate_g422r_runtime_asset_consistency.py
```

Pre-G-5 roadmap execution ledger:

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" wayfarer_godot_vertical_slice\tools\validate_pre_g5_roadmap_ledger.py
```

Capture log check:

```powershell
Get-Content -Path wayfarer_godot_vertical_slice\artifacts\review\g422a_runtime_screenshots\godot_capture.log -TotalCount 120
```

Git whitespace checks:

```powershell
git diff --check
git diff --cached --check
```

## Output Rules

- Use `PASS`, `FAIL`, or `SKIPPED_WITH_COMMAND`.
- Every skipped command must include the exact command.
- QA may report technical pass, but must not decide art/design approval.
- QA must fail G-5 readiness if the ledger has any non-PASS row or if normal-play screenshots show non-atelier or untracked player/NPC/world sprites.
