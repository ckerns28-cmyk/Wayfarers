# Wayfarer Godot Roadmap

This roadmap resets the Wayfarer plan around the Godot pivot. The current
scope is G-0 and G-1 only.

The existing Cloudflare Worker remains the JavaScript Phase 35.13R route. The
Godot browser review path is separate. For G-2, the temporary browser-review
host is the existing itch.io project at
`https://wayfarersguild.itch.io/wayfarers-tale`, using a ZIP generated from
`wayfarer_godot_vertical_slice/web_build/`.

G-2.5 restores the repeatable visual review loop: source changes produce an
ignored local Web build, an ignored itch-ready ZIP under
`wayfarer_godot_vertical_slice/artifacts/`, and a GitHub Actions artifact for
manual itch upload. Optional butler deploy is available only when
`BUTLER_API_KEY` is configured.

Current G-2 result: the itch.io page launches the single-threaded Godot Web
export in Chrome and unblocks G-3 rendering/input parity work. This is a
browser-review route only; it is not a production cutover.

Current G-3 result: the first scoped Godot rendering/input pass is ready for
manual itch ZIP review. It improves camera setup, browser input handling,
viewport-aware HUD placement, pixel snapping, sprite/building grounding, and
terrain/road/water readability without expanding the slice or touching the
JavaScript Worker.

Current G-3.1 result: the Godot HUD includes visible review identity for the
manual itch upload loop. A screenshot should show `Godot G-3.1 Review Clarity`,
`itch`, `manual ZIP`, and `codex/g-3-1-godot-review-clarity` when the newest
ZIP is live.

Current G-4 result: the Godot asset workflow is locked for the existing slice.
Current building atlas PNGs stay in `assets/buildings/`; stable `.import`
metadata is tracked; `.godot/`, `web_build/`, `artifacts/`, generated ZIPs, and
external-drive `._*` sidecars remain ignored. The Web export preset also
excludes generated review folders so local screenshots and ZIPs do not leak
into `index.pck`. Future source art, sprite sheets, atlases, references, and
anchor rules are documented under `wayfarer_godot_vertical_slice/docs/`.

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
- Package the itch.io upload ZIP with the deterministic script:

```sh
bash wayfarer_godot_vertical_slice/tools/package_itch_web.sh
```

- Upload
  `wayfarer_godot_vertical_slice/artifacts/wayfarers-tale-godot-web.zip` to
  the existing `wayfarersguild / wayfarers-tale` itch.io project as an HTML5
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

Status: pass on itch.io browser-review route.

Validate the existing Godot vertical slice as a stable baseline before any
content work. This phase may improve diagnostics and documentation, but it
does not add systems or expand the playable space.

Acceptance:

- itch.io page launches Godot in browser.
- Canvas appears with no permanent black screen.
- WebGL initializes.
- Single-threaded export avoids SharedArrayBuffer / cross-origin isolation
  blockers.
- Input/focus and viewport behavior are stable enough for G-3.
- Existing JavaScript Worker remains the Phase 35.13R production/reference
  route.

## G-3: Rendering and Input Parity

Status: first scoped implementation pass ready for manual itch upload.

Review browser rendering, canvas sizing, input focus, and basic movement
behavior against the local Godot baseline. Fix presentation regressions only.

G-3.0 notes:

- Camera configuration is centralized in the player controller with explicit
  world limits, current-camera reset, and slightly tighter smoothing.
- Gameplay key events are marked handled by the main scene, and focus-out
  clears the interaction latch to reduce stuck-input risk.
- The HUD now recalculates panel placement from the active viewport so resize
  and fullscreen review keep the status/dialogue panels readable.
- Pixel snap is enabled for 2D transforms/vertices, while nearest texture
  filtering remains the baseline.
- Buildings, the player, and Edrin Vale have subtle ground shadows to clarify
  sprite footing and y-sort readability.
- Roads, plaza, shoreline, and water waves received contrast-only readability
  changes. No map expansion or content additions were made.
- Local validation passed through the Godot QA script and a local browser smoke
  test. Itch still requires a fresh manual ZIP upload for visual review.

G-3.1 notes:

- The HUD now displays the review phase, build label, host, channel, and source
  branch so manual itch uploads are visually verifiable.
- The review label is static Godot-side metadata for this pass; CI and Butler
  injection remain deferred.
- No gameplay, map, route, asset-workflow, or JavaScript Worker changes are
  included.
- Manual review requires uploading the generated ZIP, hard-refreshing itch,
  and confirming the on-screen label changed before evaluating visuals.

Prerequisite review loop:

- Manual mode: run `tools/package_itch_web.sh`, upload the artifact ZIP to
  itch, then review the page.
- Artifact-assisted mode: download the `wayfarers-tale-godot-web` artifact from
  `.github/workflows/godot-web-review-build.yml`, upload it to itch, then
  review the page.
- Automated itch mode: configure `BUTLER_API_KEY`, run the workflow manually
  with `deploy_to_itch=true` or merge to the configured branch, then review the
  refreshed itch page.

The GitHub Actions workflow exists but remains unproven until it completes
successfully in GitHub Actions.

## G-4: Asset Source and Import Discipline

Status: current.

Lock the source-of-truth asset workflow for Godot imports, atlases, import
settings, screenshots, and future art updates. Keep generated caches out of
Git.

G-4 decisions:

- Existing Godot atlas sheets remain in `assets/buildings/` for this slice.
- Future original art should use `assets/source/<domain>/`.
- Future individual sprites should use `assets/sprites/<domain>/`.
- Future new atlas families should use `assets/atlases/<domain>/`.
- Future committed reference screenshots should use
  `assets/references/<phase>/`.
- Local browser/export evidence stays in ignored `artifacts/`.
- `artifacts/**`, `web_build/**`, and `*.zip` are excluded from the Web export
  package.
- Stable Godot `.import` files for tracked assets should be committed.
- Godot `.godot/` cache/editor output should never be committed.
- Sprite grounding and y-sort rules are documented in
  `wayfarer_godot_vertical_slice/docs/SPRITE_ANCHORS.md`.
- Asset hygiene is checked with
  `bash wayfarer_godot_vertical_slice/tools/validate_asset_hygiene.sh`.

Acceptance:

- No `.godot/`, `web_build/`, `artifacts/`, or generated ZIP files are tracked.
- Current tracked atlas PNGs have tracked `.import` metadata.
- Future art updates have documented source, import, atlas, anchor, and review
  expectations.
- Existing JavaScript Worker remains the Phase 35.13R production/reference
  route.

## G-5: Migration Architecture

Design how future gameplay systems will move from the JavaScript codebase to
Godot. This is a planning phase, not a porting phase. It may begin after G-4
asset hygiene passes and the G-4 ZIP is manually reviewed on itch.

## G-6: Production Cutover Planning

Define the eventual production-hosting decision, rollback plan, QA gates, and
criteria for replacing the JavaScript Worker route. The Worker remains
production-facing until this phase explicitly changes that.
