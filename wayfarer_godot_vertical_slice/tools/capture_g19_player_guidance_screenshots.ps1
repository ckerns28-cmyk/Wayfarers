param(
    [string]$GodotBin = "C:\Users\Chris\Downloads\Godot_v4.6.2-stable_win64.exe\Godot_v4.6.2-stable_win64_console.exe"
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
$OutDir = Join-Path $ProjectRoot "artifacts\review\g19_player_guidance_screenshots"
$LogPath = Join-Path $OutDir "godot_capture.log"

if (!(Test-Path $GodotBin)) {
    throw "Godot console executable not found: $GodotBin"
}

if (!(Test-Path $OutDir)) {
    New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
}

$arguments = @(
    "--path", $ProjectRoot,
    "--windowed",
    "--resolution", "1600x1000",
    "--display-driver", "windows",
    "--audio-driver", "Dummy",
    "--rendering-driver", "opengl3",
    "--rendering-method", "gl_compatibility",
    "--log-file", $LogPath,
    "--script", "res://tools/capture_g19_player_guidance_screenshots.gd"
)

Write-Host "Running G-19 player guidance screenshot capture:"
Write-Host $GodotBin $arguments

& $GodotBin @arguments
$exitCode = $LASTEXITCODE
if ($exitCode -ne 0) {
    throw "Godot capture failed with exit code $exitCode. See $LogPath"
}

Write-Host "G-19 screenshot capture log: $LogPath"
