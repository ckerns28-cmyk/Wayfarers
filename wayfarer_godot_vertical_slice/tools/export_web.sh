#!/usr/bin/env bash
# Exports the Wayfarer Godot Vertical Slice to a static web folder that can
# be uploaded to a separate Cloudflare Pages project. Does NOT touch the
# existing JavaScript wayfarer_v7_github_ready build.
#
# Requirements (local machine):
#   - Godot 4.6.2-stable (Standard, not Mono). The script checks, in order:
#     GODOT=/path/to/godot, $PATH, common macOS app locations, and current
#     macOS AppTranslocation launches.
#   - Godot Web export templates of the exact same version installed.
#     Editor -> Project -> Export -> Manage Export Templates -> Download.
#
# Output: ./web_build/ inside the Godot project (sibling to project.godot).
# That folder is what gets uploaded to Cloudflare Pages.

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PRESET="${PRESET:-Web}"
OUTPUT_DIR="${OUTPUT_DIR:-$PROJECT_ROOT/web_build}"
OUTPUT_HTML="$OUTPUT_DIR/index.html"

find_godot_bin() {
    if [ -n "${GODOT:-}" ]; then
        if [ -x "$GODOT" ]; then
            printf "%s\n" "$GODOT"
            return 0
        fi
        echo "GODOT is set but is not executable: $GODOT" >&2
        return 1
    fi

    if command -v godot >/dev/null 2>&1; then
        command -v godot
        return 0
    fi

    local candidate
    local candidates=(
        "/Applications/Godot.app/Contents/MacOS/Godot"
        "$HOME/Applications/Godot.app/Contents/MacOS/Godot"
    )

    for candidate in "${candidates[@]}"; do
        if [ -x "$candidate" ]; then
            printf "%s\n" "$candidate"
            return 0
        fi
    done

    local translocation_root
    local translocated_godot
    local translocation_roots=(
        "${TMPDIR:-/tmp}/AppTranslocation"
        "/private/var/folders"
    )

    for translocation_root in "${translocation_roots[@]}"; do
        [ -d "$translocation_root" ] || continue
        translocated_godot="$(
            find "$translocation_root" -maxdepth 10 \
                -path "*/Godot.app/Contents/MacOS/Godot" \
                -type f -print -quit 2>/dev/null || true
        )"
        if [ -n "$translocated_godot" ] && [ -x "$translocated_godot" ]; then
            printf "%s\n" "$translocated_godot"
            return 0
        fi
    done

    cat >&2 <<'EOF'
Could not find Godot.
Set GODOT=/path/to/Godot.app/Contents/MacOS/Godot or install Godot in /Applications.
EOF
    return 1
}

GODOT_BIN="$(find_godot_bin)"

if [ "$OUTPUT_DIR" != "$PROJECT_ROOT/web_build" ]; then
    echo "Refusing to clean non-default OUTPUT_DIR: $OUTPUT_DIR" >&2
    exit 1
fi

rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

cd "$PROJECT_ROOT"

echo "Using Godot: $GODOT_BIN"
"$GODOT_BIN" --version
echo

# Headless --import primes resources without opening the editor.
"$GODOT_BIN" --headless --path "$PROJECT_ROOT" --import

# Actual web export.
"$GODOT_BIN" --headless --path "$PROJECT_ROOT" \
    --export-release "$PRESET" "$OUTPUT_HTML"

# Make sure Cloudflare Pages serves the cross-origin isolation headers that
# Godot's web build needs for SharedArrayBuffer / threaded WASM. Copy every
# export so stale local headers cannot drift from the committed template.
HEADERS_FILE="$OUTPUT_DIR/_headers"
cp "$PROJECT_ROOT/web_build_template/_headers" "$HEADERS_FILE"

echo
echo "Web export written to: $OUTPUT_DIR"
ls -1 "$OUTPUT_DIR"
