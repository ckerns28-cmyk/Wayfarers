#!/usr/bin/env bash
# Builds the Godot Web export and packages an itch.io-ready HTML5 ZIP.
# The ZIP root must contain index.html directly; do not zip web_build/ itself.

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EXPORT_SCRIPT="$PROJECT_ROOT/tools/export_web.sh"
WEB_BUILD_DIR="$PROJECT_ROOT/web_build"
ARTIFACT_DIR="$PROJECT_ROOT/artifacts"
ZIP_PATH="$ARTIFACT_DIR/wayfarers-tale-godot-web.zip"

fail() {
    echo "FAIL: $*" >&2
    exit 1
}

command -v zip >/dev/null 2>&1 || fail "zip is required."
command -v zipinfo >/dev/null 2>&1 || fail "zipinfo is required."

"$EXPORT_SCRIPT"

rm -f "$ZIP_PATH"
mkdir -p "$ARTIFACT_DIR"

for required in \
    index.html \
    index.js \
    index.pck \
    index.wasm \
    index.audio.worklet.js \
    index.audio.position.worklet.js
do
    [ -f "$WEB_BUILD_DIR/$required" ] || fail "Missing web export file: $required"
done

tmp_file_list="$(mktemp "${TMPDIR:-/tmp}/wayfarer-itch-zip-list.XXXXXX")"
trap 'rm -f "$tmp_file_list"' EXIT

(
    cd "$WEB_BUILD_DIR"
    find . -type f ! -name ".DS_Store" \
        | sed 's#^\./##' \
        | LC_ALL=C sort > "$tmp_file_list"
    zip -X -q "$ZIP_PATH" -@ < "$tmp_file_list"
)

zip_entries="$(zipinfo -1 "$ZIP_PATH")"

if printf "%s\n" "$zip_entries" | grep -qx "index.html"; then
    echo "PASS: index.html is at ZIP root."
else
    fail "index.html is not at ZIP root."
fi

if printf "%s\n" "$zip_entries" | grep -qx "web_build/index.html"; then
    fail "ZIP incorrectly contains web_build/index.html."
else
    echo "PASS: ZIP does not contain web_build/index.html."
fi

file_count="$(printf "%s\n" "$zip_entries" | sed '/^$/d' | wc -l | tr -d ' ')"
zip_size="$(du -h "$ZIP_PATH" | awk '{print $1}')"

echo
echo "ZIP path: $ZIP_PATH"
echo "File count: $file_count"
echo "Total size: $zip_size"
echo
echo "First 40 ZIP entries:"
printf "%s\n" "$zip_entries" | sed -n '1,40p'
