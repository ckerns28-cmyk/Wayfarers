# G-2 Godot Baseline Validation

Status: itch.io browser baseline pass. The Godot vertical slice launches in
Chrome from the temporary itch.io browser-review page, renders the canvas, and
is stable enough to unblock G-3 rendering/input parity work. Cloudflare Pages
Direct Upload remains blocked/deferred for the current stock Godot export
because `index.wasm` is larger than 25 MB.

Date: 2026-05-10
Branch: `codex/g-2-godot-itch-baseline-validation`

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
wayfarer_godot_vertical_slice/artifacts/wayfarers-tale-godot-web.zip
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
3. Upload `wayfarer_godot_vertical_slice/artifacts/wayfarers-tale-godot-web.zip`.
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

## Itch.io Browser Runtime Validation

Validation target:

```text
https://wayfarersguild.itch.io/wayfarers-tale
```

Browser:

```text
Google Chrome 147.0.7727.138
```

Live Chrome screenshot evidence was captured in the Codex thread with the
itch.io game page active, DevTools console open, and the Godot canvas visible.

Runtime result: pass.

- itch page loads.
- Godot loader has completed and the game canvas is visible.
- No permanent black screen.
- No missing `index.html`, `index.js`, `index.pck`, or `index.wasm` failures
  were visible in DevTools.
- No SharedArrayBuffer or cross-origin isolation fatal error.
- WebGL initialized.
- No fatal console errors.

Observed console runtime:

```text
Godot Engine v4.6.2.stable.official.71f334935
OpenGL API OpenGL ES 3.0 (WebGL 2.0 (OpenGL ES 3.0 Chromium)) Compatibility
Build configuration: Emscripten 4.0.20, single-threaded, no GDExtension support.
```

Observed non-blocking console warnings:

```text
Unrecognized feature: 'monetization'.
Unrecognized feature: 'xr'.
Allow attribute will take precedence over 'allowfullscreen'.
```

These warnings are classified as itch/browser iframe feature-policy warnings,
not Godot runtime failures. They do not block G-2.

## Itch.io Input And Focus Validation

Result: pass for G-2 baseline.

- Mouse/canvas focus is usable for the browser-review build.
- Keyboard movement is accepted after click/focus in the game area.
- Arrow/WASD-style movement remains the expected G-2 control surface for the
  current slice.
- No stuck-input state was reported after interacting with the itch frame.
- No page scrolling or browser focus theft was reported during movement.
- Fullscreen launch is the preferred itch review mode and remains suitable for
  G-2 validation.
- Returning from fullscreen did not expose a blocking input regression in this
  validation pass.

## Itch.io Camera And Viewport Validation

Result: pass for G-2 baseline.

- Initial camera framing is usable and centers the current Newport Harbor Test
  slice around the player/NPC interaction area.
- Camera follow is functioning.
- The visible viewport contains the current reduced slice without a permanent
  black region or catastrophic clipping.
- HUD remains readable in the browser view.
- World scale is stable enough for baseline review.
- Fullscreen is preferred for further G-3 inspection because it removes itch
  iframe framing ambiguity.

Deferred to G-3:

- Final camera smoothing feel.
- Exact viewport containment and scaling policy.
- Rendering/input parity against the JavaScript production reference.

## Itch.io Rendering Baseline Validation

Result: pass for G-2 baseline.

- Sprites are sharp enough for baseline inspection.
- Texture filtering remains consistent with the existing nearest-filter Godot
  baseline.
- Tile alignment is coherent across grass, roads, and water.
- Sprite grounding and origins are substantially simpler to reason about than
  the JavaScript painterly seating/audit stack.
- Y-sort/depth ordering is stable enough for the current slice.
- Alpha handling around buildings and props is acceptable.
- Terrain, road, harbor/water, and building placement readability are adequate
  for G-2.
- Browser scaling artifacts are not blocking.

This is not a full visual-parity claim against JavaScript Phase 35.13R Newport.
The Godot slice is smaller and rougher by design; G-2 only validates that Godot
is a viable browser renderer/input baseline for the next pass.

## High-Level JS Reference Comparison

JavaScript Phase 35.13R remains stronger as the production reference:

- More complete town composition.
- More complete QA/reference state.
- Production-facing Worker route.

Known JavaScript renderer pain points still motivating the Godot path:

- Seating contract complexity.
- Viewport audit complexity.
- Painterly sprite grounding disagreements with tile contracts.

G-2 conclusion:

Godot appears to reduce renderer/camera/sprite-origin complexity through local
scene nodes, explicit anchors, camera containment, and y-sort behavior. The itch
browser baseline is stable enough to unblock G-3 rendering/input parity work.

## G-2.5 Visual Review Loop

Status: artifact-assisted review loop restored locally; GitHub Actions workflow
is scaffolded and remains unproven until it runs successfully in CI.

Source of truth:

- GitHub repository.
- `wayfarer_godot_vertical_slice/project.godot`
- `wayfarer_godot_vertical_slice/export_presets.cfg`
- Godot source/assets/scenes under `wayfarer_godot_vertical_slice/`.

Generated local build:

```text
wayfarer_godot_vertical_slice/web_build/
```

Review package:

```text
wayfarer_godot_vertical_slice/artifacts/wayfarers-tale-godot-web.zip
```

Packaging command:

```sh
bash wayfarer_godot_vertical_slice/tools/package_itch_web.sh
```

The packaging script:

- Runs `tools/export_web.sh`.
- Removes the previous ZIP.
- Creates the ZIP from inside `web_build/`.
- Validates `index.html` at the ZIP root.
- Fails if `web_build/index.html` is present.
- Prints ZIP path, file count, total size, and the first 40 entries.

Local package proof from G-2.5:

```text
PASS: index.html is at ZIP root.
PASS: ZIP does not contain web_build/index.html.
ZIP path: wayfarer_godot_vertical_slice/artifacts/wayfarers-tale-godot-web.zip
File count: 10
Total size: 15M
```

ZIP root:

```text
_headers
index.apple-touch-icon.png
index.audio.position.worklet.js
index.audio.worklet.js
index.html
index.icon.png
index.js
index.pck
index.png
index.wasm
```

GitHub Actions artifact workflow:

```text
.github/workflows/godot-web-review-build.yml
```

Expected artifact name:

```text
wayfarers-tale-godot-web
```

The workflow downloads Godot 4.6.2 Standard and the matching export templates
from the official Godot download archive, runs the package script, and uploads
the ZIP artifact. The workflow is not claimed proven until a GitHub Actions run
completes successfully.

Optional itch deploy:

- Uses butler.
- Pushes `wayfarer_godot_vertical_slice/web_build` to
  `wayfarersguild/wayfarers-tale:web`.
- Runs only on `main` or a manual workflow dispatch with `deploy_to_itch=true`.
- Skips without failing ordinary artifact builds when `BUTLER_API_KEY` is not
  configured.

## G-3 Rendering/Input Parity Pass

Status: first visible Godot-forward pass prepared for manual itch ZIP review.

Branch:

```text
codex/g-3-godot-rendering-input-parity
```

Scope:

- No JavaScript Worker files, routes, gameplay systems, or production cutover
  logic were changed.
- The Godot slice remains the same reduced Newport Harbor Test scene.
- G-3 does not attempt final visual parity with JavaScript Phase 35.13R.

Implemented baseline improvements:

- Player camera setup now applies explicit world limits, reset-on-start, and
  slightly tighter smoothing from the controller script.
- Gameplay key events are handled by the main scene to reduce browser scroll
  and focus leakage while playing.
- Focus-out clears the interaction latch to reduce stuck-input risk after
  switching away from the browser frame.
- HUD panels recalculate from the active viewport so browser resize and
  fullscreen review keep the status and dialogue surfaces readable.
- 2D pixel snap is enabled for transforms and vertices; nearest texture
  filtering remains active.
- Buildings, the player, and Edrin Vale now draw small ground shadows for
  clearer footing and y-sort review.
- Road/plaza outlines, shoreline definition, and water wave detail were
  adjusted for readability only. No map expansion or content additions were
  made.

Validation:

- Godot QA script result: pass, `failureCount=0`.
- Local browser smoke URL: `http://127.0.0.1:8790/`.
- Browser runtime: Godot `v4.6.2.stable.official.71f334935`.
- WebGL mode: WebGL 2.0 / OpenGL ES 3.0 compatibility.
- Build configuration: Emscripten 4.0.20, single-threaded, no GDExtension support.
- Local browser logs after boot and movement input: no warnings or errors.

Review delivery:

- Itch.io remains the G-3 browser-review host:
  `https://wayfarersguild.itch.io/wayfarers-tale`.
- Itch does not update automatically from GitHub.
- A fresh `wayfarer_godot_vertical_slice/artifacts/wayfarers-tale-godot-web.zip`
  must be uploaded manually before public visual review.
- Butler automation remains deferred for this manual ZIP review pass.
- Cloudflare Pages remains deferred for the current stock export because
  `index.wasm` exceeds the 25 MB Direct Upload single-file limit.

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

- Continue browser review from the live itch.io page.
- Keep Cloudflare Pages deferred until the WASM size or delivery strategy is
  changed.
- Review camera smoothing and viewport containment against the desired browser
  feel.
