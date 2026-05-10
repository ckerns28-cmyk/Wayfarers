#!/usr/bin/env bash
# Exports the Wayfarer Godot Vertical Slice to a static web folder that can
# be uploaded to a separate Cloudflare Pages project. Does NOT touch the
# existing JavaScript wayfarer_v7_github_ready build.
#
# Requirements (local machine):
#   - Godot 4.6.2-stable (Standard, not Mono) installed and on $PATH as
#     `godot` (or override with GODOT=/path/to/godot)
#   - Godot Web export templates of the exact same version installed.
#     Editor -> Project -> Export -> Manage Export Templates -> Download.
#
# Output: ./web_build/ inside the Godot project (sibling to project.godot).
# That folder is what gets uploaded to Cloudflare Pages.

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GODOT_BIN="${GODOT:-godot}"
PRESET="${PRESET:-Web}"
OUTPUT_DIR="${OUTPUT_DIR:-$PROJECT_ROOT/web_build}"
OUTPUT_HTML="$OUTPUT_DIR/index.html"

mkdir -p "$OUTPUT_DIR"

cd "$PROJECT_ROOT"

# Headless --import primes resources without opening the editor.
"$GODOT_BIN" --headless --path "$PROJECT_ROOT" --import

# Actual web export.
"$GODOT_BIN" --headless --path "$PROJECT_ROOT" \
    --export-release "$PRESET" "$OUTPUT_HTML"

# Make sure Cloudflare Pages serves the cross-origin isolation headers that
# Godot's web build needs for SharedArrayBuffer / threaded WASM.
HEADERS_FILE="$OUTPUT_DIR/_headers"
if [ ! -f "$HEADERS_FILE" ]; then
    cp "$PROJECT_ROOT/web_build_template/_headers" "$HEADERS_FILE"
fi

echo
echo "Web export written to: $OUTPUT_DIR"
ls -1 "$OUTPUT_DIR"
