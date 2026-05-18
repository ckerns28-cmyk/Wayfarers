param(
    [string]$GodotBin = $env:GODOT_BIN
)

$ErrorActionPreference = "Stop"

$ProjectRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$OutDir = Join-Path $ProjectRoot "artifacts\review\g18a_runtime_screenshots"
$QuestOutDir = Join-Path $ProjectRoot "artifacts\review\g18a_quest_branch_proof"
$LogPath = Join-Path $OutDir "godot_capture.log"

if ([string]::IsNullOrWhiteSpace($GodotBin)) {
    $GodotBin = "godot"
}

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
New-Item -ItemType Directory -Force -Path $QuestOutDir | Out-Null

$GodotArgs = @(
    "--path", $ProjectRoot,
    "--windowed",
    "--resolution", "1600x1000",
    "--display-driver", "windows",
    "--audio-driver", "Dummy",
    "--rendering-driver", "opengl3",
    "--rendering-method", "gl_compatibility",
    "--log-file", $LogPath,
    "--script", "res://tools/capture_g18a_multipath_choice_proof.gd"
)

$QuotedArgs = $GodotArgs | ForEach-Object {
    if ($_ -match "\s") {
        '"' + $_ + '"'
    } else {
        $_
    }
}
$env:G18A_CAPTURE_COMMAND = '& "' + $GodotBin + '" ' + ($QuotedArgs -join " ")

Write-Host "Running G-18A multi-path choice proof capture:"
Write-Host $env:G18A_CAPTURE_COMMAND

try {
    & $GodotBin @GodotArgs
    exit $LASTEXITCODE
} finally {
    Remove-Item Env:\G18A_CAPTURE_COMMAND -ErrorAction SilentlyContinue
}
