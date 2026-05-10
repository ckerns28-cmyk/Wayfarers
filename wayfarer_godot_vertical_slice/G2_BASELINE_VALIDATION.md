# G-2 Godot Baseline Validation

Status: local baseline pass, itch.io upload package ready for manual G-2
browser review. Cloudflare Pages Direct Upload is blocked/deferred for the
current stock Godot export because `index.wasm` is larger than 25 MB.

Date: 2026-05-10
Branch: `codex/g-1-6-itch-godot-browser-review`

## Scope Guard

G-2 validates the existing Godot vertical slice as a rendering and browser
delivery baseline. It does not add gameplay, expand the map, port JavaScript
systems, or alter the production JavaScript Worker route.

The JavaScript Phase 35.13R Worker remains the production-facing route and the
authoritative gameplay reference.

## Environment

- Godot binary: `4.6.2.stable.official.71f334935`
- Export template version: `4.6.2.stable`
- Godot source: official Godot 4.6.2-stable macOS Standard archive
- Export templates: official Godot 4.6.2-stable export templates
- Temporary validation home: `/private/tmp/wayfarer-godot-home`

## Export Validation

Command:

```sh
HOME=/private/tmp/wayfarer-godot-home \
GODOT=/private/tmp/wayfarer-godot-4.6.2/Godot.app/Contents/MacOS/Godot \
bash wayfarer_godot_vertical_slice/tools/export_web.sh
```

Result: pass.

Generated files in `web_build/`:

- `_headers`
- `index.html`
- `index.js`
- `index.pck`
- `index.wasm`
- `index.audio.worklet.js`
- `index.audio.position.worklet.js`
- `index.icon.png`
- `index.apple-touch-icon.png`
- `index.png`

`index.worker.js` was not emitted by this Godot 4.6.2 export. Browser logs
identify the build as:

```text
Build configuration: Emscripten 4.0.20, single-threaded, no GDExtension support.
```

The exported HTML also reports:

```text
GODOT_THREADS_ENABLED = false
```

The generated JS references:

```text
godot.web.template_release.wasm32.nothreads.wasm
```

This is the desired itch.io baseline because it does not require
SharedArrayBuffer or server-side COOP/COEP headers to initialize.

Non-fatal export warning observed from the downloaded macOS app in headless
mode:

```text
ERROR: Condition "ret != noErr" is true. Returning: ""
   at: get_system_ca_certificates (platform/macos/os_macos.mm:1028)
```

The export still completed successfully.

## Runtime Validation

Local test URL:

```text
http://127.0.0.1:8790/
```

The local server served the export with:

- `Cross-Origin-Opener-Policy: same-origin`
- `Cross-Origin-Embedder-Policy: require-corp`
- `Cross-Origin-Resource-Policy: same-origin`
- `Content-Type: application/wasm` for `index.wasm`
- `Content-Type: application/octet-stream` for `index.pck`

Cold browser boot result after fixes:

- Title: `Wayfarer Godot Vertical Slice`
- Canvas count: 1
- Startup timing: about 8.9 seconds from navigation through wait window
- Console errors after cold start: 0
- Console warnings after cold start: 0
- WASM initialized
- No permanent black screen
- No infinite loading state

Captured evidence:

- `artifacts/screenshots/g2_local_browser_baseline.png`
- `artifacts/screenshots/g2_local_input_after_keys.png`

## Fixes Required For Baseline Functionality

The first browser run exposed exported atlas failures:

```text
ERROR: Error opening file 'res://assets/buildings/hearthvale_buildings_atlas_v1.png'.
ERROR: Failed to load atlas image: res://assets/buildings/hearthvale_buildings_atlas_v1.png
```

Root cause:

`Image.load_from_file()` attempted to read raw source PNG files at runtime.
The Web export packages imported `CompressedTexture2D` resources instead.

Correction:

`Main.gd` now loads atlas resources with:

```gdscript
ResourceLoader.load(path, "Texture2D") as Texture2D
```

This is an import/runtime correction only. It does not change placement,
content, regions, gameplay, or map design.

The export script now clears the default ignored `web_build/` folder before
headless import/export. Without this, repeat exports can import previous
export icons and leave `.import` files in the browser output.

## Input And Focus Validation

Procedure:

- Opened the cold local browser export.
- Clicked the single canvas.
- Sent movement keys:
  `ArrowRight`, `ArrowDown`, `ArrowLeft`, `W`, `A`, `S`, `D`.

Result: pass.

- Keyboard input was responsive.
- Canvas accepted focus after click.
- Player/camera moved visibly.
- No stuck-input state observed.
- No fresh console errors or warnings after input.
- No page scrolling or browser focus theft observed in the validation pass.

## Rendering Baseline Findings

Pass:

- Atlas textures render in browser after switching to exported `Texture2D`
  resources.
- Alpha handling appears correct around building silhouettes.
- Default canvas texture filter is nearest (`default_texture_filter=0`), so
  sprites remain crisp rather than blurred.
- Building placement uses explicit foot anchors and sprite offsets.
- `World.y_sort_enabled = true` gives Godot a simpler, more stable route for
  depth ordering than the JavaScript seating/placement audit stack.
- Camera follow works in browser.
- Camera limits contain the current slice bounds.
- No catastrophic clipping or black-screen failure observed.

Diagnostic notes:

- The vertical slice is a reduced validation scene, not visual parity with the
  full JavaScript Phase 35.13R production map.
- Godot naturally improves the risk areas that made the JavaScript renderer
  expensive: sprite origins are local node data, grounding is explicit through
  anchors, and y-sort gives deterministic draw order.
- Current camera smoothing is visible but stable. G-3 should review whether
  smoothing speed and viewport containment match the intended final feel.

## Atlas And Import Findings

Tracked atlas import settings are suitable for this baseline:

- `compress/mode=0`
- `mipmaps/generate=false`
- `process/fix_alpha_border=true`
- `process/premult_alpha=false`

The Web export packages `.ctex` imports into `index.pck`; browser runtime
must load them as Godot resources, not raw PNG files.

The export generated `BuildingDebugOverlay.gd.uid`, matching the repository
pattern of tracking `.gd.uid` files beside source scripts.

## Itch.io G-2 Browser Review Delivery

Temporary browser-review host:

```text
https://wayfarersguild.itch.io/wayfarers-tale
```

The current upload ZIP is:

```text
wayfarer_godot_vertical_slice/wayfarers-tale-godot-web.zip
```

The ZIP was created from inside `wayfarer_godot_vertical_slice/web_build/`, so
`index.html` is at the ZIP root.

ZIP root proof:

```text
index.apple-touch-icon.png
index.wasm
index.icon.png
index.html
index.png
index.audio.worklet.js
index.js
_headers
index.audio.position.worklet.js
index.pck
```

Current export size envelope:

| Item | Size |
| ---- | ---- |
| `index.html` | 5,460 bytes |
| `index.js` | 315,759 bytes |
| `index.pck` | 5,876,736 bytes |
| `index.wasm` | 37,695,054 bytes |
| `index.audio.worklet.js` | 7,298 bytes |
| `index.audio.position.worklet.js` | 2,973 bytes |
| `_headers` | 462 bytes |
| Extracted total | 42 MB on disk, 43,942,839 bytes uncompressed in ZIP |
| Extracted file count | 10 files |

This is within itch.io's HTML5 ZIP envelope for the G-2 upload:

- `index.wasm` is below the 200 MB individual extracted-file limit.
- Extracted content is below the 500 MB total limit.
- Extracted file count is below 1,000.

Manual upload steps:

1. Open the itch.io project edit page for `wayfarersguild / wayfarers-tale`.
2. Set the project kind/type to HTML / HTML5 browser game if needed.
3. Upload `wayfarer_godot_vertical_slice/wayfarers-tale-godot-web.zip`.
4. Configure the uploaded ZIP to run in browser / embedded HTML.
5. Prefer "Click to launch in fullscreen" for the first G-2 browser validation.
6. Save the page.
7. Open the public itch page.
8. Launch the game.
9. Capture browser console errors and a screenshot.

Post-upload smoke checklist:

- itch page loads.
- Game launch button appears.
- Godot loader appears.
- No missing `index.html`, `index.js`, `index.pck`, or `index.wasm`.
- No SharedArrayBuffer / cross-origin isolation fatal error.
- No permanent black screen.
- Canvas appears.
- Keyboard input works after click/focus.
- Fullscreen launch works.
- No browser scroll/focus stealing during movement.

## Cloudflare Pages Delivery

Deploy command attempted:

```sh
npx wrangler pages deploy wayfarer_godot_vertical_slice/web_build --project-name wayfarers-godot-slice
```

Prior result: blocked before upload because `CLOUDFLARE_API_TOKEN` was not set.

Wrangler reached the deploy flow but failed in this non-interactive
environment because `CLOUDFLARE_API_TOKEN` is not set.

```text
In a non-interactive environment, it's necessary to set a
CLOUDFLARE_API_TOKEN environment variable for wrangler to work.
```

Current Pages URL check:

```sh
curl -L -I https://wayfarers-godot-slice.pages.dev/
```

Result:

```text
curl: (6) Could not resolve host: wayfarers-godot-slice.pages.dev
```

This suggests the Pages project or published hostname is not currently
available from this environment until a token-backed deploy is completed.

G-1.6 update:

- Pages project name was accepted: `wayfarers-godot-slice`.
- Direct Upload rejected the current export because `index.wasm` is
  37,695,054 bytes, over Cloudflare Pages' 25 MB single-file upload limit.
- Cloudflare Pages remains deferred unless `index.wasm` is reduced or another
  asset strategy is chosen.
- The existing JavaScript Worker remains the production-facing Phase 35.13R
  route.

## JavaScript Worker Isolation

Verified no diffs in:

- `wrangler.toml`
- `wayfarer_v7_github_ready/worker/src/index.js`
- `wayfarer_v7_github_ready/worker/assets/**`

No `/godot/` route was added to the existing Worker.

## G-2 / G-3 Follow-ups

- Manually upload `wayfarers-tale-godot-web.zip` to itch.io.
- Run the itch browser smoke checklist and capture console output plus a
  screenshot.
- Keep Cloudflare Pages deferred until the WASM size or delivery strategy is
  changed.
- Review camera smoothing and viewport containment against the desired browser
  feel.
