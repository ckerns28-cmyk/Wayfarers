# Wayfarer Godot Roadmap

This roadmap resets the Wayfarer plan around the Godot pivot. The current
scope is G-0 and G-1 only.

The existing Cloudflare Worker remains the JavaScript Phase 35.13R route. The
Godot browser review path is separate. For G-2, the temporary browser-review
host is the existing itch.io project at
`https://wayfarersguild.itch.io/wayfarers-tale`, using a ZIP generated from
`wayfarer_godot_vertical_slice/web_build/`.

Cloudflare Pages remains the preferred separate static-hosting target, but it
is deferred for the current stock Godot export because Pages Direct Upload
rejects the 37,695,054-byte `index.wasm` file as larger than the 25 MB
single-file upload limit.

## Non-goals for G-0 and G-1

- Do not add gameplay features.
- Do not expand the map.
- Do not port inventory, combat, save, or new quests.
- Do not modify the existing JavaScript Worker route.
- Do not treat the Worker Visit button as a Godot preview.

## G-0: Repository Hygiene and Roadmap Reset

Status: current.

- Remove committed `.godot/` generated editor, cache, and import artifacts.
- Keep `.godot/` and `web_build/` ignored.
- Preserve the existing Worker deployment definition in `wrangler.toml`.
- Record the Godot migration phases in this document.

Acceptance:

- `git ls-files ':(glob)**/.godot/**'` returns no tracked generated cache
  files.
- The JavaScript Worker files have no diff.
- This roadmap exists.

## G-1: Separate Browser Review Delivery

Status: current, with G-1.6 itch.io delivery package ready for manual upload.

- Keep the Godot Web export preset pointed at `web_build/index.html`.
- Keep `tools/export_web.sh` exporting into
  `wayfarer_godot_vertical_slice/web_build/`.
- Copy `web_build_template/_headers` into `web_build/_headers` on every
  export.
- Use the single-threaded Godot Web export for the itch.io baseline.
- Package the itch.io upload ZIP from inside `web_build/` so `index.html`
  appears at the ZIP root:

```sh
cd wayfarer_godot_vertical_slice/web_build
zip -r ../wayfarers-tale-godot-web.zip .
cd ../..
```

- Upload `wayfarer_godot_vertical_slice/wayfarers-tale-godot-web.zip` to the
  existing `wayfarersguild / wayfarers-tale` itch.io project as an HTML5
  browser game.
- Prefer "Click to launch in fullscreen" for the first G-2 browser validation.
- Keep Cloudflare Pages documented but deferred until the WASM size or asset
  strategy changes:

```sh
npx wrangler pages deploy wayfarer_godot_vertical_slice/web_build --project-name wayfarers-godot-slice
```

Acceptance:

- The temporary G-2 review URL comes from
  `https://wayfarersguild.itch.io/wayfarers-tale`.
- The ZIP root contains `index.html`, not `web_build/index.html`.
- The existing Worker Visit button still opens JavaScript Phase 35.13R.
- No `/godot/` route is added to the existing Worker.
- Cloudflare Pages is not treated as live until `wayfarers-godot-slice.pages.dev`
  resolves from an actual successful deployment.

## G-2: Slice Baseline Validation

Validate the existing Godot vertical slice as a stable baseline before any
content work. This phase may improve diagnostics and documentation, but it
does not add systems or expand the playable space.

## G-3: Rendering and Input Parity

Review browser rendering, canvas sizing, input focus, and basic movement
behavior against the local Godot baseline. Fix presentation regressions only.

## G-4: Asset Source and Import Discipline

Lock the source-of-truth asset workflow for Godot imports, atlases, import
settings, screenshots, and future art updates. Keep generated caches out of
Git.

## G-5: Migration Architecture

Design how future gameplay systems will move from the JavaScript codebase to
Godot. This is a planning phase, not a porting phase.

## G-6: Production Cutover Planning

Define the eventual production-hosting decision, rollback plan, QA gates, and
criteria for replacing the JavaScript Worker route. The Worker remains
production-facing until this phase explicitly changes that.
