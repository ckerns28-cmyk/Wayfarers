param(
    [string]$GodotBin = ""
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$ProjectRoot = Join-Path $RepoRoot "wayfarer_godot_vertical_slice"
$OutDir = Join-Path $ProjectRoot "artifacts\review\ovi2_newport_origin_immersion"
$LogPath = Join-Path $OutDir "godot_capture.log"

if (-not $GodotBin) {
    if ($env:GODOT_BIN) {
        $GodotBin = $env:GODOT_BIN
    } else {
        $GodotBin = "C:\Users\Chris\Downloads\Godot_v4.6.2-stable_win64.exe\Godot_v4.6.2-stable_win64_console.exe"
    }
}

if (-not (Test-Path -LiteralPath $GodotBin)) {
    throw "Godot console binary not found: $GodotBin"
}

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$args = @(
    "--path", $ProjectRoot,
    "--windowed",
    "--resolution", "1600x1000",
    "--display-driver", "windows",
    "--audio-driver", "Dummy",
    "--rendering-driver", "opengl3",
    "--rendering-method", "gl_compatibility",
    "--log-file", $LogPath,
    "--script", "res://tools/capture_ovi2_runtime_screenshots.gd"
)

Write-Host "Running OVI-2 Newport origin immersion screenshot capture:"
Write-Host "& `"$GodotBin`" $($args -join ' ')"
& $GodotBin @args
exit $LASTEXITCODE
