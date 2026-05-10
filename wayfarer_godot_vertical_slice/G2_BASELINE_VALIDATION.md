# G-2 Godot Baseline Validation

Status: local baseline pass, Cloudflare Pages deployment blocked by missing
`CLOUDFLARE_API_TOKEN`.

Date: 2026-05-10
Branch: `codex/g-2-godot-baseline-validation`

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

## Cloudflare Pages Delivery

Deploy command attempted:

```sh
npx wrangler pages deploy wayfarer_godot_vertical_slice/web_build --project-name wayfarers-godot-slice
```

Result: blocked before upload.

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

## JavaScript Worker Isolation

Verified no diffs in:

- `wrangler.toml`
- `wayfarer_v7_github_ready/worker/src/index.js`
- `wayfarer_v7_github_ready/worker/assets/**`

No `/godot/` route was added to the existing Worker.

## G-3 Blockers

- Complete a token-backed Cloudflare Pages deployment.
- Re-test `https://wayfarers-godot-slice.pages.dev` headers and browser boot
  after upload.
- Decide whether the absence of `index.worker.js` is acceptable for the
  single-threaded Godot 4.6.2 Web export, or whether G-3 should explicitly
  target a threaded export profile.
- Review camera smoothing and viewport containment against the desired browser
  feel.
