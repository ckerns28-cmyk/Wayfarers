param(
    [string]$GodotBin = $env:GODOT_BIN
)

$ErrorActionPreference = "Stop"

$ProjectRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$OutDir = Join-Path $ProjectRoot "artifacts\review\g422a_runtime_screenshots"
$LogPath = Join-Path $OutDir "godot_capture.log"

if ([string]::IsNullOrWhiteSpace($GodotBin)) {
    $GodotBin = "godot"
}

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$GodotArgs = @(
    "--path", $ProjectRoot,
    "--windowed",
    "--resolution", "1600x1000",
    "--display-driver", "windows",
    "--audio-driver", "Dummy",
    "--rendering-driver", "opengl3",
    "--rendering-method", "gl_compatibility",
    "--log-file", $LogPath,
    "--script", "res://tools/capture_g422a_runtime_screenshots.gd"
)

$QuotedArgs = $GodotArgs | ForEach-Object {
    if ($_ -match "\s") {
        '"' + $_ + '"'
    } else {
        $_
    }
}
$env:G422A_CAPTURE_COMMAND = '& "' + $GodotBin + '" ' + ($QuotedArgs -join " ")

Write-Host "Running G-4.22A runtime screenshot capture:"
Write-Host $env:G422A_CAPTURE_COMMAND

try {
    & $GodotBin @GodotArgs
    exit $LASTEXITCODE
} finally {
    Remove-Item Env:\G422A_CAPTURE_COMMAND -ErrorAction SilentlyContinue
}
