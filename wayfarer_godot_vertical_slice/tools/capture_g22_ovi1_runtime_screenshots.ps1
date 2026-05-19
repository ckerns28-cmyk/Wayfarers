param(
    [string]$GodotBin = ""
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$ProjectRoot = Join-Path $RepoRoot "wayfarer_godot_vertical_slice"
$OutDir = Join-Path $ProjectRoot "artifacts\review\g22_ovi1_runtime_screenshots"
$LogPath = Join-Path $OutDir "godot_capture.log"
$Composer = Join-Path $ProjectRoot "tools\compose_g22_ovi1_review_package.py"
$PythonBin = Join-Path $env:LOCALAPPDATA "Programs\Python\Python313\python.exe"

if (-not (Test-Path -LiteralPath $PythonBin)) {
    $PythonBin = "python"
}

if (-not (Test-Path -LiteralPath $Composer)) {
    throw "G-22 composer missing: $Composer"
}

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

Write-Host "Composing G-22 OVI-1 review screenshot package:"
Write-Host "& `"$PythonBin`" `"$Composer`" --capture-only"
& $PythonBin $Composer --capture-only
$exitCode = $LASTEXITCODE
if ($exitCode -ne 0) {
    throw "G-22 OVI-1 capture package composition failed with exit code $exitCode."
}

if (-not (Test-Path -LiteralPath $LogPath)) {
    throw "G-22 OVI-1 capture log was not written: $LogPath"
}

Write-Host "G-22 OVI-1 screenshot manifest: $(Join-Path $ProjectRoot 'artifacts\review\g22_ovi1_review_screenshots\g22_ovi1_screenshot_manifest.json')"
Write-Host "G-22 OVI-1 capture log: $LogPath"
