# Web Build Template

Files in this directory are copied alongside the Godot Web export so the
resulting `web_build/` is ready to upload to Cloudflare Pages or any other
static host that respects `_headers` syntax.

- `_headers` — Cloudflare Pages headers file. Sets the cross-origin
  isolation headers (`Cross-Origin-Opener-Policy: same-origin` and
  `Cross-Origin-Embedder-Policy: require-corp`) that Godot's web build
  needs for `SharedArrayBuffer` / threaded WASM. Without these, the page
  loads but the WASM module fails to initialize and the canvas stays black.

`tools/export_web.sh` copies the contents of this folder into `web_build/`
after Godot finishes exporting, so you do not have to remember to add the
headers by hand.
