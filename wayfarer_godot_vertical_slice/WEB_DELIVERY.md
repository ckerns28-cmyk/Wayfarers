# Web Delivery: Godot Vertical Slice

The Godot vertical slice is delivered as an additive `/godot/*` route on
the existing Cloudflare Worker, **not** as a replacement for the
JavaScript site at `/`. The same Worker that serves `Build Phase 35.13R`
at `/` now also serves the Godot canvas at `/godot/`. Top-level
`wrangler.toml` and the JS Worker's [assets] binding are unchanged
except for one Worker-code addition that routes `/godot/*` cleanly to
the asset binding without falling back to the JS shell.

Public preview URL once deployed:

```
https://wayfarers.ckerns28.workers.dev/godot/
```

(also accessible as `/godot/index.html`)

## 1. How the routing works

Top-level `wrangler.toml` (unchanged):

```toml
name = "wayfarers"
main = "wayfarer_v7_github_ready/worker/src/index.js"
compatibility_date = "2026-04-23"

[assets]
directory = "./wayfarer_v7_github_ready/worker/assets"
binding = "ASSETS"
```

`wayfarer_v7_github_ready/worker/src/index.js` was extended with a small
addition:

- `/godot` and `/godot/` are rewritten to `/godot/index.html` before the
  asset binding is consulted, so the Worker does not fall back to the JS
  shell HTML for those bare paths.
- `/godot/*` paths are added to `isLikelyStaticAssetRequest` (with
  `.wasm` and `.pck` extensions) so the asset response is preferred even
  for non-existent paths instead of being replaced by the JS shell.
- Every `/godot/*` response gets the cross-origin isolation headers
  Godot's threaded WASM build needs:
  ```
  Cross-Origin-Opener-Policy: same-origin
  Cross-Origin-Embedder-Policy: require-corp
  Cross-Origin-Resource-Policy: same-origin
  ```

The JS site at `/` is unaffected — the headers are only injected on the
`/godot/*` branch and the existing routing for `/`, `/assets/*`,
`/tiles/*`, and the SPA fallback is unchanged.

## 2. Files served at /godot/

The Worker reads files from
`wayfarer_v7_github_ready/worker/assets/godot/`. That directory currently
contains a **placeholder `index.html`** — visiting `/godot/` shows
"Build label: Godot Vertical Slice (export pending)" with instructions
for the operator. The placeholder is what is live on the next Cloudflare
deploy and is the proof that the route is wired.

Once `tools/export_web.sh` runs locally with Godot installed, the real
Godot export overwrites the placeholder, and `/godot/` then renders the
five-building Hearthvale slice.

## 3. Local export workflow

Requirements:

- Godot 4.6.2-stable Standard (not Mono) on `$PATH` as `godot`, or
  override with `GODOT=/path/to/godot`.
- Web export templates of the same Godot version installed locally:
  Editor → *Project* → *Export* → *Manage Export Templates* → *Download*.

From the repo root:

```sh
bash wayfarer_godot_vertical_slice/tools/export_web.sh
```

The script:

1. Runs `godot --headless --import` to prime resources.
2. Runs `godot --headless --export-release "Web"` against the `Web`
   preset declared in `export_presets.cfg`, landing the build in
   `wayfarer_godot_vertical_slice/export/web/`.
3. Mirrors the export into
   `wayfarer_v7_github_ready/worker/assets/godot/` so the existing
   Worker auto-serves it on the next deploy.

Equivalent raw commands if you prefer to invoke Godot by hand:

```sh
cd wayfarer_godot_vertical_slice
godot --headless --path . --import
godot --headless --path . --export-release "Web" export/web/index.html
rsync -a --delete export/web/ ../wayfarer_v7_github_ready/worker/assets/godot/
```

Expected files in `wayfarer_godot_vertical_slice/export/web/` after a
real export:

- `index.html`
- `index.js`
- `index.pck`
- `index.wasm`
- `index.audio.worklet.js`
- `index.audio.position.worklet.js`
- `index.worker.js` (Godot 4.x dispatch worker)
- `index.icon.png`, `index.apple-touch-icon.png`

After the script finishes, commit BOTH directories and push:

```sh
git add wayfarer_godot_vertical_slice/export/web \
        wayfarer_v7_github_ready/worker/assets/godot
git commit -m "Deploy Godot vertical slice web export"
git push
```

Cloudflare's existing Worker deploy auto-picks up the new files and
`/godot/` switches from the placeholder to the real Godot canvas.

## 4. Cloudflare config (no changes required)

The Worker that already serves the JS site is the same Worker that now
serves `/godot/*`. There is **no separate Cloudflare Pages project to
create** for the simple route-share path described above. The Worker
build/output configuration is unchanged:

| Setting          | Value                                                   |
| ---------------- | ------------------------------------------------------- |
| Worker name      | `wayfarers`                                             |
| Worker entry     | `wayfarer_v7_github_ready/worker/src/index.js`          |
| Static assets    | `./wayfarer_v7_github_ready/worker/assets`              |
| New /godot/ root | `wayfarer_v7_github_ready/worker/assets/godot/`         |

If a separate Pages project is desired later, point Cloudflare Pages at
`wayfarer_godot_vertical_slice/export/web/` (the canonical export
folder) and configure `_headers` from
`web_build_template/_headers`. The existing route-share path keeps
working alongside it.

## 5. Verifying the deploy

After Cloudflare publishes the next commit:

1. Visit `https://wayfarers.ckerns28.workers.dev/` and confirm the JS
   site still shows `Build Phase 35.13R`.
2. Visit `https://wayfarers.ckerns28.workers.dev/godot/`:
   - If the export step has not run yet: you see the "Build label:
     Godot Vertical Slice (export pending)" placeholder. The route is
     correctly wired and waiting for binaries.
   - If the export step has run: the page loads the Godot canvas with
     `Build label: Godot Vertical Slice` in the in-game HUD and the
     five buildings of the Newport slice.
3. Open DevTools → Network → confirm responses for `/godot/index.html`,
   `/godot/index.wasm`, `/godot/index.pck` carry
   `Cross-Origin-Opener-Policy: same-origin` and
   `Cross-Origin-Embedder-Policy: require-corp`. Without those headers
   Godot's WASM module fails to initialize.

## 6. What still runs the JavaScript game

The Worker code that builds the JS shell, the `[assets]` binding, the
`/assets/*` rewrite logic, and the `wayfarer_v7_github_ready/` source
tree are all untouched aside from adding the additive `/godot/*` branch
and the `godot/` subfolder. The JS production tag (`Build Phase 35.13R`)
continues to serve at `/`.
