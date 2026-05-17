param(
    [string]$GodotBin = "godot"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$projectRoot = Join-Path $repoRoot "wayfarer_godot_vertical_slice"
$outDir = Join-Path $projectRoot "artifacts\review\g422_runtime_screenshots"
$script = "res://tools/capture_g422_runtime_screenshots.gd"

New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$logPath = Join-Path $outDir "godot_capture.log"
$commandText = @(
    "& `"$GodotBin`"",
    "--path `"$projectRoot`"",
    "--windowed",
    "--resolution 1600x1000",
    "--display-driver windows",
    "--audio-driver Dummy",
    "--rendering-driver opengl3",
    "--rendering-method gl_compatibility",
    "--log-file `"$logPath`"",
    "--script $script"
) -join " "

$env:G422_CAPTURE_COMMAND = $commandText

Write-Host "Running G-4.22 runtime screenshot capture:"
Write-Host $commandText

& $GodotBin `
    --path $projectRoot `
    --windowed `
    --resolution 1600x1000 `
    --display-driver windows `
    --audio-driver Dummy `
    --rendering-driver opengl3 `
    --rendering-method gl_compatibility `
    --log-file $logPath `
    --script $script

exit $LASTEXITCODE
