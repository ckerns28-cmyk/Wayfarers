# Web Delivery: Godot Vertical Slice

The Godot vertical slice is delivered as a static Web export for browser
review. For G-2, the temporary review host is the existing itch.io project:

```text
https://wayfarersguild.itch.io/wayfarers-tale
```

Cloudflare Pages remains the preferred separate static-hosting target, but
Direct Upload is deferred for the current stock Godot export because
`index.wasm` is larger than Cloudflare Pages' 25 MB single-file upload limit.

The existing JavaScript Wayfarer site in `wayfarer_v7_github_ready/` (served
by the Worker defined in `/wrangler.toml`) is not touched by this pipeline and
remains the production-facing Phase 35.13R route.

## 1. Local export

Requirements:

- Godot 4.6.2-stable Standard (not Mono) on `$PATH` as `godot`, or override
  with `GODOT=/path/to/godot` when running the script.
- Web export templates of the exact same Godot version installed locally:
  Editor → *Project* → *Export* → *Manage Export Templates* → *Download*.

From the repo root:

```sh
bash wayfarer_godot_vertical_slice/tools/export_web.sh
```

The script runs the headless export against the `Web` preset declared in
`export_presets.cfg`, drops the output into
`wayfarer_godot_vertical_slice/web_build/`, and copies the Cloudflare
`_headers` template into the same folder.

Equivalent raw commands if you prefer to invoke Godot by hand:

```sh
cd wayfarer_godot_vertical_slice
godot --headless --path . --import
godot --headless --path . --export-release "Web" web_build/index.html
cp web_build_template/_headers web_build/_headers
```

Expected output in `web_build/`:

- `index.html`
- `index.js`
- `index.pck`
- `index.wasm`
- `index.audio.worklet.js`
- `index.audio.position.worklet.js`
- `index.icon.png`, `index.apple-touch-icon.png`
- `_headers` (copied from `web_build_template/_headers`)

`index.worker.js` may be absent for the single-threaded Godot Web export. Do
not treat that as a blocker unless `index.html` references it or the browser
fails because of it.

The current G-2 export is single-threaded:

```text
GODOT_THREADS_ENABLED = false
godot.web.template_release.wasm32.nothreads.wasm
```

That is the desired itch.io baseline because it avoids requiring
SharedArrayBuffer and server-side COOP/COEP headers. `_headers` remains useful
for Cloudflare Pages documentation, but itch.io does not consume Cloudflare
`_headers` files.

`web_build/` is `.gitignore`d. The binary artifacts ship to the temporary
browser-review host or a future static host, not to GitHub.

## 2. Itch.io delivery (temporary G-2 browser review)

Use itch.io while Cloudflare Pages Direct Upload is blocked by the current
`index.wasm` size.

Current export envelope after the G-1.6 re-export:

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

The itch.io HTML5 ZIP requirements are satisfied for the current export:

- `index.html` is present.
- `index.wasm` is below the 200 MB individual extracted-file limit.
- The extracted content is below the 500 MB limit.
- The extracted file count is below 1,000.

Create the upload ZIP from inside `web_build/` so `index.html` is at the ZIP
root:

```sh
cd wayfarer_godot_vertical_slice/web_build
zip -r ../wayfarers-tale-godot-web.zip .
cd ../..
```

Validate the ZIP root:

```sh
zipinfo -1 wayfarer_godot_vertical_slice/wayfarers-tale-godot-web.zip
```

The listing must include `index.html` with no `web_build/` prefix.

Manual itch.io upload steps:

1. Open the itch.io project edit page for `wayfarersguild / wayfarers-tale`.
2. Set the project kind/type to HTML / HTML5 browser game if it is not already set.
3. Upload `wayfarer_godot_vertical_slice/wayfarers-tale-godot-web.zip`.
4. Configure the uploaded ZIP to run in browser / embedded HTML.
5. Prefer "Click to launch in fullscreen" for the first G-2 browser validation.
6. Save the page.
7. Open the public itch page.
8. Launch the game.
9. Capture browser console errors and a screenshot.

Manual browser smoke checklist after upload:

- itch page loads.
- Game launch button appears.
- Godot loader appears.
- No missing `index.html`, `index.js`, `index.pck`, or `index.wasm`.
- No SharedArrayBuffer / cross-origin isolation fatal error.
- No permanent black screen.
- Canvas appears.
- Keyboard input works after click/focus.
- Fullscreen launch works.
- Movement does not cause page scrolling or browser focus theft.

If SharedArrayBuffer or cross-origin isolation errors appear, classify the
result as `THREADING_EXPORT_INCOMPATIBLE_WITH_ITCH`, switch to a
single-thread Web export, re-export, re-zip, and re-upload.

## 3. Cloudflare delivery (deferred: separate Pages project)

The JavaScript site is currently served by the `wayfarers` Cloudflare
Worker. To keep that build untouched and still let reviewers play the Godot
slice in a browser, host the Godot export as its **own** Cloudflare Pages
project.

Current state for this export:

- Pages project name accepted: `wayfarers-godot-slice`.
- Direct Upload is blocked because `index.wasm` is 37,695,054 bytes, over the
  25 MB single-file upload limit.
- Cloudflare Pages remains deferred unless `index.wasm` is reduced or another
  asset strategy is chosen.
- The existing Worker route remains the production-facing JavaScript Phase
  35.13R route.

### Direct upload

From the repo root, after running the local export:

```sh
npx wrangler pages deploy wayfarer_godot_vertical_slice/web_build --project-name wayfarers-godot-slice
```

Cloudflare should publish to `https://wayfarers-godot-slice.pages.dev` once
the single-file size blocker is resolved. That URL is not the active G-2
browser-review link while Direct Upload is blocked.

The existing Worker Visit button still opens the JavaScript Phase 35.13R
Worker route. It is not the Godot preview.

### Dashboard upload

1. Cloudflare dashboard → *Workers & Pages* → *Create* → *Pages* → *Upload
   assets*. Name the project `wayfarers-godot-slice`.
2. Drag-drop the contents of `wayfarer_godot_vertical_slice/web_build/`
   (the files, not the folder).
3. Cloudflare will publish to `https://wayfarers-godot-slice.pages.dev`.
   That URL is the Godot browser-review link.

### Build / output config (if connecting via Git instead)

| Setting          | Value                                                   |
| ---------------- | ------------------------------------------------------- |
| Production branch | `main`                                                  |
| Build command    | `bash wayfarer_godot_vertical_slice/tools/export_web.sh` |
| Build output     | `wayfarer_godot_vertical_slice/web_build`               |
| Root directory   | *(repo root)*                                           |

The Git-connected path requires Godot + Web templates on Cloudflare's build
image, which is not currently provisioned. Until that is set up, the
preferred path is the **manual upload** above after running
`tools/export_web.sh` locally.

### Cross-origin isolation headers

`web_build_template/_headers` sets:

```
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

Threaded Godot Web exports require those headers for SharedArrayBuffer.
Cloudflare Pages reads `_headers` automatically; do not move or rename that
file for Cloudflare delivery. The current itch.io review export is
single-threaded and does not rely on these headers.

## 4. Alternative delivery options

Listed for future planning only. G-1.6 does not add a new Worker route, does
not add production cutover logic, and does not change the existing Worker
Visit button.

- **Preview-only static folder.** Drop `web_build/` on any static host
  (Netlify, GitHub Pages with `_headers` adapted to that host's syntax,
  `python -m http.server` for local-only review). The current single-threaded
  export does not require COOP/COEP headers; a future threaded export would.

## 5. What still runs the JavaScript game

`wrangler.toml` continues to point at
`wayfarer_v7_github_ready/worker/src/index.js` and
`wayfarer_v7_github_ready/worker/assets/`. The Godot delivery is a
parallel preview only; the JS Worker stays the production-facing build
until a future migration pass replaces it explicitly.
