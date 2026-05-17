param(
    [switch]$RunValidators,
    [switch]$Help,
    [string]$Phase = "G-4.22P",
    [int]$TargetPr = 449,
    [string]$GodotBin = "",
    [string]$PythonBin = ""
)

$ErrorActionPreference = "Stop"

if ($Help) {
    Write-Host "Wayfarer Agent Council"
    Write-Host ""
    Write-Host "Usage:"
    Write-Host "  powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\run_wayfarer_agent_council.ps1"
    Write-Host "  powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\run_wayfarer_agent_council.ps1 -RunValidators"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -RunValidators       Run validators instead of listing SKIPPED_WITH_COMMAND."
    Write-Host "  -Phase <label>       Phase label for the generated report. Default: G-4.22P."
    Write-Host "  -TargetPr <number>   PR number to inspect for Newport classification context. Default: 449."
    Write-Host "  -GodotBin <path>     Godot console executable path."
    Write-Host "  -PythonBin <path>    Python executable path."
    exit 0
}

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$ScriptPath = Join-Path $PSScriptRoot "wayfarer_agent_council.py"

if (-not (Test-Path -LiteralPath $ScriptPath)) {
    throw "Could not find council script at $ScriptPath"
}

if ([string]::IsNullOrWhiteSpace($PythonBin)) {
    $LocalPython = Join-Path $env:LOCALAPPDATA "Programs\Python\Python313\python.exe"
    if (Test-Path -LiteralPath $LocalPython) {
        $PythonBin = $LocalPython
    } else {
        $PythonBin = "python"
    }
}

$CouncilArgs = @(
    $ScriptPath,
    "--phase",
    $Phase,
    "--target-pr",
    "$TargetPr"
)

if ($RunValidators) {
    $CouncilArgs += "--run-validators"
}

if (-not [string]::IsNullOrWhiteSpace($GodotBin)) {
    $CouncilArgs += "--godot-bin"
    $CouncilArgs += $GodotBin
}

Push-Location $RepoRoot
try {
    & $PythonBin @CouncilArgs
} finally {
    Pop-Location
}
