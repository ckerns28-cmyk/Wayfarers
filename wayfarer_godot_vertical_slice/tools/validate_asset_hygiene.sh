#!/usr/bin/env bash
# Verifies the Godot slice keeps source assets and generated review artifacts
# separated. Run from the repo root or anywhere inside the repo.

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "$PROJECT_ROOT/.." && pwd)"

failures=0

fail() {
    echo "FAIL: $*"
    failures=$((failures + 1))
}

pass() {
    echo "PASS: $*"
}

require_file() {
    local path="$1"
    local label="$2"
    if [ -f "$path" ]; then
        pass "$label"
    else
        fail "$label missing: $path"
    fi
}

check_no_tracked() {
    local pattern="$1"
    local label="$2"
    local matches
    matches="$(git -C "$REPO_ROOT" ls-files "$pattern")"
    if [ -z "$matches" ]; then
        pass "$label not tracked"
    else
        fail "$label tracked"
        printf "%s\n" "$matches"
    fi
}

require_file "$PROJECT_ROOT/docs/ASSET_WORKFLOW.md" "asset workflow doc"
require_file "$PROJECT_ROOT/docs/SPRITE_ANCHORS.md" "sprite anchors doc"
require_file "$PROJECT_ROOT/SPRITE_ATLAS_GODOT.md" "atlas contract doc"
require_file "$PROJECT_ROOT/export_presets.cfg" "Godot export preset"
require_file "$PROJECT_ROOT/tools/package_itch_web.sh" "itch package script"

check_no_tracked ':(glob)**/.godot/**' ".godot cache files"
check_no_tracked ':(glob)**/web_build/**' "web_build export files"
check_no_tracked ':(glob)**/artifacts/**' "generated artifacts"
check_no_tracked ':(glob)**/*.zip' "generated ZIP files"

if grep -Fq '! -name "._*"' "$PROJECT_ROOT/tools/package_itch_web.sh"; then
    pass "package script excludes AppleDouble sidecars"
else
    fail "package script should exclude AppleDouble sidecars"
fi

if grep -Fq 'exclude_filter="artifacts/**,web_build/**,*.zip"' "$PROJECT_ROOT/export_presets.cfg"; then
    pass "export preset excludes generated folders"
else
    fail "export preset should exclude artifacts/**, web_build/**, and generated ZIPs"
fi

while IFS= read -r asset_path; do
    import_path="${asset_path}.import"
    if [ -f "$import_path" ]; then
        pass "import file exists for ${asset_path#$PROJECT_ROOT/}"
    else
        fail "missing import file for ${asset_path#$PROJECT_ROOT/}"
        continue
    fi

    rel_import="${import_path#$REPO_ROOT/}"
    if git -C "$REPO_ROOT" ls-files --error-unmatch "$rel_import" >/dev/null 2>&1; then
        pass "import file tracked for ${asset_path#$PROJECT_ROOT/}"
    else
        fail "import file is not tracked: $rel_import"
    fi
done < <(find "$PROJECT_ROOT/assets" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \) ! -name "._*" | LC_ALL=C sort)

if [ "$failures" -eq 0 ]; then
    echo "Asset hygiene status: PASS"
else
    echo "Asset hygiene status: FAIL ($failures issue(s))"
    exit 1
fi
