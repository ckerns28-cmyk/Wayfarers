#!/usr/bin/env bash
# Build the Godot Web export and stage it for the existing Cloudflare
# Worker so the /godot/ route serves the slice.
#
# Two destinations get the same files:
#   1. wayfarer_godot_vertical_slice/export/web/
#        Canonical export output. Source-truth for both the /godot/ Worker
#        route and any future separate Cloudflare Pages project.
#   2. wayfarer_v7_github_ready/worker/assets/godot/
#        What the existing Worker (wrangler.toml -> ./wayfarer_v7_github_ready
#        /worker/assets) actually serves at /godot/* on Cloudflare. The JS
#        site at / is unaffected; this is an additive subdirectory.
#
# Requirements (local machine):
#   - Godot 4.6.2-stable (Standard, not Mono) on $PATH as `godot`, or
#     override with GODOT=/path/to/godot.
#   - Godot Web export templates of the same version installed via
#     Editor -> Project -> Export -> Manage Export Templates -> Download.
#
# After running, commit the new files in BOTH directories and push. The
# Cloudflare Worker auto-deploys on push and serves the slice at /godot/.

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "$PROJECT_ROOT/.." && pwd)"

GODOT_BIN="${GODOT:-godot}"
PRESET="${PRESET:-Web}"
EXPORT_DIR="${EXPORT_DIR:-$PROJECT_ROOT/export/web}"
SERVE_DIR="${SERVE_DIR:-$REPO_ROOT/wayfarer_v7_github_ready/worker/assets/godot}"
EXPORT_HTML="$EXPORT_DIR/index.html"

mkdir -p "$EXPORT_DIR" "$SERVE_DIR"

cd "$PROJECT_ROOT"

# Headless --import primes resources without opening the editor.
"$GODOT_BIN" --headless --path "$PROJECT_ROOT" --import

# Actual web export against the "Web" preset in export_presets.cfg.
"$GODOT_BIN" --headless --path "$PROJECT_ROOT" \
    --export-release "$PRESET" "$EXPORT_HTML"

# Mirror canonical export -> Worker serving directory. Use rsync if it
# exists (faster + deletes stale files); otherwise fall back to cp.
if command -v rsync >/dev/null 2>&1; then
    rsync -a --delete --exclude '.gitkeep' "$EXPORT_DIR/" "$SERVE_DIR/"
else
    find "$SERVE_DIR" -mindepth 1 -not -name '.gitkeep' -delete
    cp -r "$EXPORT_DIR"/. "$SERVE_DIR"/
fi

echo
echo "Godot web export written to:"
echo "  canonical : $EXPORT_DIR"
echo "  serving   : $SERVE_DIR"
ls -1 "$EXPORT_DIR"
echo
echo "Next step: commit both directories and push. Cloudflare will then"
echo "serve the slice at https://wayfarers.ckerns28.workers.dev/godot/."
