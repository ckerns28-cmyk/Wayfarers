#!/usr/bin/env bash
# Builds the Godot Web export and packages an itch.io-ready HTML5 ZIP.
# The ZIP root must contain index.html directly; do not zip web_build/ itself.

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EXPORT_SCRIPT="$PROJECT_ROOT/tools/export_web.sh"
WEB_BUILD_DIR="$PROJECT_ROOT/web_build"
ARTIFACT_DIR="$PROJECT_ROOT/artifacts"
ZIP_PATH="$ARTIFACT_DIR/wayfarers-tale-godot-web.zip"
BUILD_INFO="$PROJECT_ROOT/scripts/BuildInfo.gd"

fail() {
    echo "FAIL: $*" >&2
    exit 1
}

find_python_bin() {
    is_working_python() {
        local candidate="$1"
        [ -n "$candidate" ] || return 1
        "$candidate" -c 'import sys, zipfile' >/dev/null 2>&1
    }

    if [ -n "${PYTHON:-}" ] && [ -x "$PYTHON" ] && is_working_python "$PYTHON"; then
        printf "%s\n" "$PYTHON"
        return 0
    fi

    local windows_python="$HOME/AppData/Local/Programs/Python/Python313/python.exe"
    if [ -x "$windows_python" ] && is_working_python "$windows_python"; then
        printf "%s\n" "$windows_python"
        return 0
    fi

    if command -v python3 >/dev/null 2>&1; then
        local python3_bin
        python3_bin="$(command -v python3)"
        if is_working_python "$python3_bin"; then
            printf "%s\n" "$python3_bin"
            return 0
        fi
    fi

    if command -v python >/dev/null 2>&1; then
        local python_bin
        python_bin="$(command -v python)"
        if is_working_python "$python_bin"; then
            printf "%s\n" "$python_bin"
            return 0
        fi
    fi

    return 1
}

PYTHON_BIN="$(find_python_bin || true)"

create_zip() {
    local zip_path="$1"
    local file_list="$2"

    if command -v zip >/dev/null 2>&1; then
        zip -X -q "$zip_path" -@ < "$file_list"
        return 0
    fi

    [ -n "$PYTHON_BIN" ] || fail "zip is required when Python is unavailable."
    "$PYTHON_BIN" - "$zip_path" "$file_list" <<'PY'
import sys
import zipfile

zip_path = sys.argv[1]
file_list = sys.argv[2]

with open(file_list, "r", encoding="utf-8") as handle:
    entries = [line.strip() for line in handle if line.strip()]

with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for entry in entries:
        archive.write(entry, entry)
PY
}

list_zip_entries() {
    local zip_path="$1"

    if command -v zipinfo >/dev/null 2>&1; then
        zipinfo -1 "$zip_path"
        return 0
    fi

    [ -n "$PYTHON_BIN" ] || fail "zipinfo is required when Python is unavailable."
    "$PYTHON_BIN" - "$zip_path" <<'PY'
import sys
import zipfile

with zipfile.ZipFile(sys.argv[1], "r") as archive:
    for name in archive.namelist():
        print(name)
PY
}

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
        ! -name "._*" \
        | sed 's#^\./##' \
        | LC_ALL=C sort > "$tmp_file_list"
    create_zip "$ZIP_PATH" "$tmp_file_list"
)

zip_entries="$(list_zip_entries "$ZIP_PATH")"

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
build_phase="$(awk -F'"' '/BUILD_PHASE/ {print $2; exit}' "$BUILD_INFO")"
build_label="$(awk -F'"' '/BUILD_LABEL/ {print $2; exit}' "$BUILD_INFO")"
version_slug="$(
    printf "%s %s\n" "$build_phase" "$build_label" \
        | tr '[:upper:]' '[:lower:]' \
        | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//; s/-godot-g-[0-9]+-[0-9]+//'
)"
VERSIONED_ZIP_PATH="$ARTIFACT_DIR/wayfarers-tale-godot-$version_slug.zip"
cp -p "$ZIP_PATH" "$VERSIONED_ZIP_PATH"

echo
echo "ZIP path: $ZIP_PATH"
echo "Versioned ZIP path: $VERSIONED_ZIP_PATH"
echo "File count: $file_count"
echo "Total size: $zip_size"
echo
echo "First 40 ZIP entries:"
printf "%s\n" "$zip_entries" | sed -n '1,40p'
