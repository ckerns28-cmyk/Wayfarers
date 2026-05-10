# Web Delivery: Godot Vertical Slice

The Godot vertical slice is delivered as a static Web export hosted on a
**separate** Cloudflare Pages project. The existing JavaScript Wayfarer site
in `wayfarer_v7_github_ready/` (served by the Worker defined in
`/wrangler.toml`) is not touched by this pipeline.

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
- `index.worker.js` (Godot 4.x dispatch worker)
- `index.icon.png`, `index.apple-touch-icon.png`
- `_headers` (copied from `web_build_template/_headers`)

`web_build/` is `.gitignore`d. The binary artifacts ship to Cloudflare, not
to GitHub.

## 2. Cloudflare delivery (preferred: separate Pages project)

The JavaScript site is currently served by the `wayfarers` Cloudflare
Worker. To keep that build untouched and still let reviewers play the Godot
slice in a browser, host the Godot export as its **own** Cloudflare Pages
project.

### One-time setup

1. Cloudflare dashboard → *Workers & Pages* → *Create* → *Pages* → *Upload
   assets*. Name the project `wayfarers-godot-slice`.
2. Drag-drop the contents of `wayfarer_godot_vertical_slice/web_build/`
   (the files, not the folder).
3. Cloudflare will publish to `https://wayfarers-godot-slice.pages.dev`.
   That URL is the review preview link.

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

Without those headers Godot's Web build loads but the WASM module never
initializes (the canvas stays black). Cloudflare Pages reads `_headers`
automatically; do not move or rename that file.

## 3. Alternative delivery options

Listed in case the separate Pages project is not viable for a particular
reviewer.

- **B. Route on the existing site, e.g. `/godot/`.** Add a `[[routes]]`
  rule to a *new* Worker (do NOT modify `wrangler.toml`) that serves
  `web_build/` from `/godot/`. The cross-origin isolation headers must be
  set per response; a Pages site does this for free, a Worker needs
  explicit header writes.
- **C. Preview-only static folder.** Drop `web_build/` on any static host
  (Netlify, GitHub Pages with `_headers` adapted to that host's syntax,
  `python -m http.server` for local-only review). For local-only use, the
  cross-origin headers can be skipped at the cost of the threaded WASM
  optimizations; see Godot's documentation on
  `--rendering-driver opengl3_compatibility`.

## 4. What still runs the JavaScript game

`wrangler.toml` continues to point at
`wayfarer_v7_github_ready/worker/src/index.js` and
`wayfarer_v7_github_ready/worker/assets/`. The Godot delivery is a
parallel preview only; the JS Worker stays the production-facing build
until a future migration pass replaces it explicitly.
