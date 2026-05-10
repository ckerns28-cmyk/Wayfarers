# Wayfarer Godot Roadmap

This roadmap resets the Wayfarer plan around the Godot pivot. The current
scope is G-0 and G-1 only.

The existing Cloudflare Worker remains the JavaScript Phase 35.13R route. The
Godot browser review path is separate and uses a Cloudflare Pages upload from
`wayfarer_godot_vertical_slice/web_build/`.

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

Status: current.

- Keep the Godot Web export preset pointed at `web_build/index.html`.
- Keep `tools/export_web.sh` exporting into
  `wayfarer_godot_vertical_slice/web_build/`.
- Copy `web_build_template/_headers` into `web_build/_headers` on every
  export.
- Deploy browser-review builds to a separate Cloudflare Pages project:

```sh
npx wrangler pages deploy wayfarer_godot_vertical_slice/web_build --project-name wayfarers-godot-slice
```

Acceptance:

- Godot review URL comes from `wayfarers-godot-slice.pages.dev`.
- The existing Worker Visit button still opens JavaScript Phase 35.13R.
- No `/godot/` route is added to the existing Worker.

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
