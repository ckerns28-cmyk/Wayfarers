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

Current G-2 state: the itch.io page launches the single-threaded Godot Web
export in Chrome and is the active browser-review route. This is not a
production cutover.

Current review rule: itch.io does not update from GitHub. Every Godot
visual/input/review-label change must be exported and packaged with
`tools/package_itch_web.sh`, then
`wayfarer_godot_vertical_slice/artifacts/wayfarers-tale-godot-web.zip` must be
uploaded manually to itch for browser review. Butler automation remains
deferred for the manual ZIP review pass.

The HUD shows visible review identity so a screenshot can prove which ZIP is
live. For G-4.5 the expected label is:

```text
Build label: Godot G-4.5 Building Seating Proof
Phase: G-4.5 | Review host: itch
Channel: manual ZIP
Branch: codex/g-4-5-building-seating-calibration-one-street-proof
```

For G-4.5 the default HUD is compact so the town is easier to review in a
screenshot. Press `F2` during local or itch review to toggle the extended
branch/channel/objective metadata.

Press `B` during local or itch review to toggle the building seating debug
overlay for the G-4.5 proof street. The overlay is off by default and shows
base anchors, frontage markers, collision rectangles, y-sort anchors, and
building IDs only for the proof-street buildings.

Review pipeline roles:

- Source of truth: GitHub plus the Godot project files under
  `wayfarer_godot_vertical_slice/`.
- Generated local build: `wayfarer_godot_vertical_slice/web_build/`.
- Review package:
  `wayfarer_godot_vertical_slice/artifacts/wayfarers-tale-godot-web.zip`.
- Browser host: `https://wayfarersguild.itch.io/wayfarers-tale`.
- Production/reference host: the existing JavaScript Worker route.

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

`web_build/` is `.gitignore`d. Review ZIPs under `artifacts/` are also
ignored. The binary artifacts ship to the temporary browser-review host or a
GitHub Actions artifact, not to Git.

Asset/build hygiene:

- Stable Godot asset `.import` metadata belongs in Git with the tracked asset.
- `.godot/`, `web_build/`, `artifacts/`, and generated ZIP files do not belong
  in Git.
- The Web export preset excludes `artifacts/**`, `web_build/**`, and `*.zip`
  so local screenshots and review packages do not get packed into `index.pck`.
- `tools/package_itch_web.sh` excludes macOS `._*` AppleDouble sidecars so
  external-drive metadata does not leak into itch upload ZIPs.
- Run `bash wayfarer_godot_vertical_slice/tools/validate_asset_hygiene.sh`
  before packaging art/import changes.

## 2. Itch.io delivery (temporary G-2 browser review)

Use itch.io while Cloudflare Pages Direct Upload is blocked by the current
`index.wasm` size.

G-2 browser status:

- Review URL: `https://wayfarersguild.itch.io/wayfarers-tale`
- Browser runtime: Godot `v4.6.2.stable.official.71f334935`
- WebGL mode: WebGL 2.0 / OpenGL ES 3.0 compatibility
- Build configuration: Emscripten 4.0.20, single-threaded, no GDExtension support
- Blocking runtime errors: none observed
- Non-blocking itch/browser iframe warnings: `monetization`, `xr`, and
  `allowfullscreen` feature-policy messages

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

Create the upload ZIP with the deterministic packaging script:

```sh
bash wayfarer_godot_vertical_slice/tools/package_itch_web.sh
```

The script runs `tools/export_web.sh`, removes any previous package output,
creates the ZIP from inside `web_build/`, and writes:

```text
wayfarer_godot_vertical_slice/artifacts/wayfarers-tale-godot-web.zip
```

It also validates the ZIP root:

```sh
zipinfo -1 wayfarer_godot_vertical_slice/artifacts/wayfarers-tale-godot-web.zip
```

The listing must include `index.html` with no `web_build/` prefix.

### Manual mode

1. Pull the latest branch.
2. Run `bash wayfarer_godot_vertical_slice/tools/package_itch_web.sh`.
3. Upload
   `wayfarer_godot_vertical_slice/artifacts/wayfarers-tale-godot-web.zip`
   to `wayfarersguild / wayfarers-tale` on itch.io.
4. Configure the uploaded ZIP to run in browser / embedded HTML.
5. Prefer "Click to launch in fullscreen" for the first validation.
6. Save the page.
7. Open `https://wayfarersguild.itch.io/wayfarers-tale`.
8. Launch the game and visually review.
9. Hard-refresh the itch page if an older build is still visible.
10. Confirm the on-screen build label changed to the expected phase/branch.
11. For G-4.5, optionally press `B` to inspect the proof-street seating
    overlay, then press `B` again before taking normal review screenshots.
12. Capture browser console errors and a screenshot.

Current review checklist:

1. Codex changes Godot source.
2. Codex runs `bash wayfarer_godot_vertical_slice/tools/package_itch_web.sh`.
3. User uploads `wayfarer_godot_vertical_slice/artifacts/wayfarers-tale-godot-web.zip` to itch.
4. User hard-refreshes the itch page.
5. User confirms the HUD shows the expected phase/build label for the branch.

### Artifact-assisted mode

GitHub Actions workflow:

```text
.github/workflows/godot-web-review-build.yml
```

The workflow installs Godot 4.6.2 Standard plus matching Web export templates,
runs `tools/package_itch_web.sh`, and uploads an artifact named:

```text
wayfarers-tale-godot-web
```

Artifact review steps:

1. Open the relevant GitHub Actions run.
2. Download the `wayfarers-tale-godot-web` artifact.
3. Upload the ZIP to the itch.io project manually.
4. Open the itch page and visually review.

This workflow is scaffolded but must be considered unproven until a GitHub
Actions run completes successfully.

### Automated itch mode

The same workflow has an optional butler deploy step. It runs only on `main` or
when manually dispatched with `deploy_to_itch=true`.

Setup:

1. Add `BUTLER_API_KEY` to the repository's GitHub Actions secrets.
2. Run the workflow manually with `deploy_to_itch=true`, or merge to the
   configured branch.
3. The workflow pushes `wayfarer_godot_vertical_slice/web_build` to:

```text
wayfarersguild/wayfarers-tale:web
```

4. Refresh the itch page and visually review.

If `BUTLER_API_KEY` is not configured, the workflow prints:

```text
Skipping itch deploy because BUTLER_API_KEY is not configured.
```

and the artifact build still succeeds.

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

### G-3 local smoke status

The first G-3 rendering/input pass was smoke-tested locally from
`wayfarer_godot_vertical_slice/web_build/` before creating the manual itch
package.

- Godot runtime: `v4.6.2.stable.official.71f334935`
- WebGL mode: WebGL 2.0 / OpenGL ES 3.0 compatibility
- Build configuration: Emscripten 4.0.20, single-threaded, no GDExtension support
- Local browser logs after boot and movement input: no warnings or errors
- Manual itch upload is still required before public visual review

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
