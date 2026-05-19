param(
    [string]$GodotBin = ""
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$ProjectRoot = Join-Path $RepoRoot "wayfarer_godot_vertical_slice"
$OutDir = Join-Path $ProjectRoot "artifacts\review\g22_ovi1_motion_proof"
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

$GodotArgs = @(
    "--path", $ProjectRoot,
    "--windowed",
    "--resolution", "1280x720",
    "--display-driver", "windows",
    "--audio-driver", "Dummy",
    "--rendering-driver", "opengl3",
    "--rendering-method", "gl_compatibility",
    "--log-file", $LogPath,
    "--script", "res://tools/capture_g22_player_motion_proof.gd"
)

$QuotedArgs = $GodotArgs | ForEach-Object {
    if ($_ -match "\s") {
        '"' + $_ + '"'
    } else {
        $_
    }
}
$env:G22_PLAYER_MOTION_CAPTURE_COMMAND = '& "' + $GodotBin + '" ' + ($QuotedArgs -join " ")

Write-Host "Running G-22 player motion proof capture:"
Write-Host $env:G22_PLAYER_MOTION_CAPTURE_COMMAND

try {
    & $GodotBin @GodotArgs
    exit $LASTEXITCODE
} finally {
    Remove-Item Env:\G22_PLAYER_MOTION_CAPTURE_COMMAND -ErrorAction SilentlyContinue
}
