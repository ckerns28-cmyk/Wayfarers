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

Current G-4.1 result: the Godot slice now constructs a Newport-inspired
starting port town instead of the five-building harbor test scene. The town
blueprint implements all 19 Newport reference building IDs across harbor wharf,
waterfront commercial, civic, upper residential, and service/outfitter
districts. The HUD review identity should show `Godot G-4.1 Newport Starting
Town` after the new ZIP is uploaded to itch.

Current G-4.2 result: the Godot town keeps the 19-building Newport foundation
but shifts the review target from building count to lived-in harbor feel. The
spawn view is closer and more intentional, streets/plazas render as narrower
walkable surfaces instead of full test-grid bands, the waterfront has crates,
barrels, posts, rope, market tables, netting, shoreline detail, and small
physical blockers, and district clusters are nudged to feel less evenly spaced.
The HUD review identity should show `Godot G-4.2 Lived-In Harbor Pass`.

Current G-4.3 result: the latest screenshot review showed that G-4.2 still
read as building sprites pasted onto a visible grid. G-4.3 keeps the same
19-building Newport set but recomposes the first-screen experience around a
street-level waterfront arrival: continuous ground washes replace tile-board
backgrounds, shaped roads/plazas/wharf edges replace full-grid bands, harbor
detail is clustered around useful frontages, the camera is tighter, and the
HUD is smaller so the player sees the town instead of a label panel. The HUD
review identity should show `Godot G-4.3 Harbor Town Recompose`.

Current G-4.4 result: the Newport town keeps the same building count and now
targets the first 60-90 seconds of player movement. The authored route starts
on the wharf apron, leads through dockside work clutter, crosses commercial
frontage, reaches the civic/church square, and connects to the inland
residential/service edge. The HUD defaults to compact review mode with
build/phase still visible, camera framing is tuned for walking, and props are
clustered to shape readable harbor, commercial, civic, and residential beats.
The HUD review identity should show `Godot G-4.4 Harbor Walk Acceptance`.

Current G-4.5 result: the Godot town now has a one-street building seating
proof for the waterfront commercial frontage. The proof street keeps the same
buildings but gives each one explicit visual-base anchors, frontage points,
collision rects, y-sort markers, shadow rectangles, and debug review markers.
Press `B` to toggle the proof-street seating overlay during review. The HUD
review identity should show `Godot G-4.5 Building Seating Proof`.

Current G-4.6 result: screenshot review showed G-4.5 was not acceptable. The
active proof has been reduced to three waterfront buildings, one street/stoop
plane, one player, and one camera frame. The HUD review identity should show
`Godot G-4.6 Three-Building Street Proof`. Do not treat this as accepted until
the manually uploaded itch screenshot clearly reads better than G-4.5.

Current G-4.7 result: screenshot review showed G-4.6 also failed. The Godot
build now shows a four-variant visual calibration board instead of a town:
A current failing reference, B smaller player scale, C lower street vignette,
and D integrated sidewalk/stoop/curb street grammar. Variant D is the
art-direction recommendation, but it is not accepted until manual itch review
confirms it clearly improves on G-4.6. The HUD review identity should show
`Godot G-4.7 Scale Grammar Calibration`.

Current G-4.8 result: the G-4.7 board has been replaced by one playable
Variant D proof street. The active scene uses four hand-seated waterfront
buildings, a `0.78` player scale, integrated sidewalk/stoops/curb, a narrower
cobbled lane, wharf edge, harbor water, and proof-street debug markers toggled
with `B`. The HUD review identity should show
`Godot G-4.8 Variant D Proof Street`. Screenshot review still found that it
read like an engineering alignment strip, so it is superseded by G-4.9.

Current G-4.9 result: the active Godot scene is a smaller Newport street
vignette, not a calibration strip. It uses three waterfront buildings,
closer storefront spacing, uneven setbacks, a `0.78` player scale, tighter
camera framing, a narrower street lane, sidewalk/stoops/curb, foreground
wharf context, and base clutter around doors. The HUD review identity should
show `Godot G-4.9 Street Vignette`.

Current G-4.9.1 result: G-4.9 visual review exposed a harder blocker than
street composition: proof-street building crops were still contaminated by
neighboring atlas cells. G-4.9.1 does not tune the street. It isolates
`b_mercantile`, `b_counting_house`, `b_chandlery_front`, and `b_shop_house`
into standalone transparent PNGs, switches the Godot catalog to those files,
updates the review identity to `Godot G-4.9.1 Sprite Crop Isolation`, and
expands proof-street collision from shallow facade strips into occupied
building lots.

Current G-4.9.5 result: G-4.9.5 resumes street composition only after the
G-4.9.4 crop/seating gate is preserved. It keeps the accepted vertical
seating, extraction, grounding, camera, and player scale, then adjusts only
horizontal spacing, lot gaps, alleys/setbacks, and nearby props so the three
waterfront buildings read more like one Newport street frontage.

Current G-4.9.6 target: G-4.9.6 is a small Street Vignette Acceptance Gate.
It does not change the accepted seating or spacing. It converts the current
street vignette into a clean player-facing review build: debug overlays are
off by default, building IDs/debug labels are hidden in normal review mode,
the G-4.9.6 build identity is visible, and validation confirms sidewalk/
street reachability plus no crop/seating regression.

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

## G-4.1: Newport Starting Town Construction

Status: current.

Build the player-facing Newport-inspired starting town foundation in Godot.
This is the first Godot pass where the visible world should read as a starting
port settlement rather than a small renderer/input test slice.

G-4.1 implementation notes:

- `scripts/NewportTownBlueprint.gd` defines the map size, water, wharf deck,
  pier fingers, road hierarchy, districts, building placements, player spawn,
  and route QA targets.
- `scripts/BuildingCatalog.gd` defines the current atlas regions and draw
  profiles used by those placements.
- The town places all 19 reference IDs:
  `b_boathouse`, `b_dock_storehouse`, `b_market_shed`, `b_inn_tavern`,
  `b_mercantile`, `b_counting_house`, `b_chandlery_front`, `b_shop_house`,
  `b_custom_house`, `b_village_hall`, `b_res_small`,
  `b_townhouse_row_a`, `b_townhouse_row_b`, `b_service_dependency`,
  `b_hunter_lodge`, `b_res_large`, `b_georgian_residence`,
  `b_elite_mansion`, and `b_prestige_block`.
- The implemented districts are harbor wharf, waterfront commercial, civic
  district, upper residential terrace, and service/outfitter lane.
- Movement validation confirms the player spawns on the waterfront route and
  can reach the wharf/pier frontage, civic square, upper residential road, and
  service lane.
- Manual itch upload remains required for browser review.

Deferred:

- Final visual parity with the JavaScript Newport composition.
- New quests, combat, inventory, save migration, and production cutover.
- Exact replacement art for every temporary substitute.

## G-4.2: Lived-In Harbor Composition

Status: current.

Make the existing Newport town foundation feel inhabited and walkable without
adding gameplay systems or expanding the map.

G-4.2 notes:

- The building set remains the same 19 Newport IDs; this is not a placement
  count phase.
- The initial camera is closer to the player and offset toward the waterfront
  composition so the spawn reads as a street-level arrival rather than a map
  overview.
- Road, alley, wharf, and plaza surfaces are drawn narrower than their
  underlying route tiles, with softer edges and reduced grid outlines.
- Harbor details include crates, barrels, rope coils, bollards, market tables,
  fish racks, net bundles, a rowboat, shoreline rocks, signs, fences, a
  clothesline, and woodpile details.
- Small static detail blockers shape movement around clutter while leaving the
  core route graph reachable.
- QA keeps the 19-building check, district checks, route reachability, camera
  zoom/offset, and detail-blocker count.

Deferred:

- New prop atlas art.
- Quests, combat, inventory, save migration, and production cutover.
- Full JS visual parity.

## G-4.3: Newport Harbor Town Recomposition

Status: ready for manual itch upload.

Make the town feel authored as a playable harbor place, not an overview map
with clip-art buildings. This phase is a composition/readability pass; it does
not add quests, combat, inventory, save migration, production cutover, or
JavaScript Worker changes.

G-4.3 notes:

- The 19-building Newport foundation remains intact. This is not a building
  count pass.
- Spawn and camera now frame the waterfront street more tightly so the player
  begins inside the town fabric instead of reading the whole scene as a map.
- `MapLayer.gd` now draws continuous grass/district washes, shaped streets,
  civic plaza, wharf apron, shoreline, water, plank docks, and frontage
  details instead of exposing tile outlines across the whole scene.
- Existing harbor props are clustered around shopfronts, wharf edges, piers,
  market frontage, and service yards to make the walkable space feel used.
- The HUD is narrower, less opaque, and uses the G-4.3 build label for visual
  upload verification.

Acceptance:

- Latest itch upload should show `Godot G-4.3 Harbor Town Recompose`.
- The first screen should no longer read primarily as a grid/test map.
- A 60-90 second walk should feel more like moving through a structured harbor
  town with waterfront, commercial, civic, service, and residential areas.
- Manual itch upload remains required for browser review.

## G-4.4: Newport Harbor Walk Acceptance

Status: ready for manual itch upload.

Finalize the current town enough that the first 60-90 seconds of movement read
as a playable harbor settlement rather than a placed-building map. This phase
keeps the 19-building set and focuses on route feel, camera, HUD, clutter,
collision, and review vistas.

G-4.4 notes:

- The player now starts on the wharf apron route, not in a broad overview
  position.
- The route beats are explicit in `NewportTownBlueprint.gd`: harbor/wharf
  start, dockside working area, commercial frontage, central pier frontage,
  civic landmark, residential edge, and service lane.
- The wharf apron and waterfront street have tighter walk surfaces, more dock
  posts, market tables placed off the main path, rope/net/fish/boat details,
  and blocker positions that shape space without trapping the player.
- The HUD defaults to compact review mode with build label and phase visible;
  extended metadata can be toggled with `F2` for review screenshots.
- Camera zoom and offset are tuned for walking through town rather than seeing
  the whole layout at once.

Review vistas:

- Wharf view: from the spawn near `(736, 620)`, the player should see the
  wharf apron, market tables, dock posts, waterline, piers, and harbor clutter
  without the HUD dominating the scene.
- Commercial street view: around `(704, 572)`, the player should see
  shopfront/commercial buildings grounded against a narrower waterfront street
  with crates, barrels, signs, and rope clusters defining storefront pressure.
- Civic/inland view: around `(650, 384)`, the player should see the civic
  square/church/custom-house landmark composition and the inland road leading
  toward residential/service edges.

Acceptance:

- Latest itch upload should show `Godot G-4.4 Harbor Walk Acceptance`.
- The first 60-90 seconds of walking should naturally pass through wharf,
  dockside, commercial, civic, and inland/residential beats.
- Props and collision should shape movement without blocking the core route.
- Manual itch upload remains required for browser review.

## G-4.5: Building Seating Calibration And One-Street Proof

Status: failed visual review; superseded by G-4.6.

Fix the foundational visual problem where painterly buildings looked pasted
onto the street plane. This phase does not add buildings or gameplay. It
creates one correct waterfront commercial proof street, then documents the
model for scaling across Newport.

G-4.5 notes:

- Proof street IDs: `b_inn_tavern`, `b_mercantile`, `b_counting_house`,
  `b_chandlery_front`, and `b_shop_house`.
- Building `Node2D.position` now explicitly means the visual base/y-sort
  plane for proof-street buildings.
- Proof-street configs include `visual_base_anchor`, `frontage_offset`,
  `collision_rect`, `shadow_size`, `shadow_offset`, `y_sort_offset`, and
  `proof_street`.
- The proof sidewalk/apron under those buildings is drawn as one continuous
  seating surface, with door steps and curb lines aligned to the calibrated
  frontages.
- Press `B` to toggle the seating debug overlay for proof-street buildings.
  It is off by default and shows base/footline, frontage, collision, y-sort
  anchor, sprite outline, and building label.

Visual review result:

- The latest G-4.5 screenshot still read as oversized pasted sprites on a
  broad tan slab.
- The debug overlay explained the failure instead of proving a believable
  street.
- G-4.5 is not accepted as the model for scaling across Newport.

## G-4.6: Three-Building Street Plane Proof

Status: failed visual review; superseded by G-4.7.

G-4.6 starts smaller:

- Active proof buildings: `b_mercantile`, `b_counting_house`, and
  `b_chandlery_front`.
- The rest of the town is not instantiated in the proof frame.
- Edrin is removed so the frame contains one player only.
- The street plane is authored as sidewalk, stoop pads, curb, cobbled lane,
  wharf strip, and harbor hint instead of the broad tan road slab.
- Building draw widths are overridden for the proof so the player reads closer
  to street scale.
- Camera zoom/offset frame one street instead of a town overview.
- Press `B` to inspect seating markers for the three proof buildings.

Acceptance:

- Latest itch upload should show `Godot G-4.6 Three-Building Street Proof`.
- The manual itch screenshot must clearly read better than the G-4.5 failure
  before this can be called successful.
- If it still fails, classify honestly as
  `PROOF_STREET_STILL_NOT_SEATED`, `BUILDING_SCALE_MODEL_FAILED`, or
  `ART_ASSET_REAUTHORING_REQUIRED`.

Visual review result:

- G-4.6 still looked like oversized building cutouts behind a flat road slab.
- The player still did not feel human-scaled into the street.
- The street plane still did not connect convincingly to building bases.
- G-4.6 is not accepted as the town grammar.

## G-4.7: Visual Scale And Street Grammar Calibration

Status: superseded by G-4.8.

G-4.7 stops town work and creates a visual calibration board:

- Variant A: current scale reference, labeled likely failing.
- Variant B: smaller player / more human scale.
- Variant C: lower camera / closer street vignette.
- Variant D: integrated sidewalk, stoops, curb, narrower cobbled lane, wharf
  strip, grounding, and base props.

G-4.7 notes:

- Active building count is 8: two comparable storefront/civic-commercial
  sprites per variant.
- Debug overlay toggles with `B` and remains off by default.
- The actual controllable player uses the smaller D-scale treatment.
- Recommended direction is Variant D if visual review confirms it.
- Current player sprite should be rescaled smaller for town work.
- Building anchors must remain hand-authored per building; a generic seating
  model is not sufficient.

Acceptance:

- Latest itch upload should show `Godot G-4.7 Scale Grammar Calibration`.
- At least one treatment must clearly look better than G-4.6 before G-4 can be
  called unblocked.
- If no treatment works, classify as `NO_VARIANT_LOOKS_ACCEPTABLE`,
  `BUILDING_STREET_GRAMMAR_FAILED`, or `SPRITE_APPROACH_NEEDS_RETHINK`.

## G-4.8: Variant D Proof Street

Status: failed visual review; superseded by G-4.9.

G-4.8 stops showing the calibration board and applies the recommended Variant
D grammar to one real playable proof street:

- Active proof buildings: `b_mercantile`, `b_counting_house`,
  `b_chandlery_front`, and `b_shop_house`.
- Player visual scale: `0.78`, matching the preferred B/D calibration scale.
- Street treatment: integrated sidewalk/apron, stoop pads, dark curb/gutter,
  narrow cobbled lane, wharf plank edge, harbor water, base props, and dock
  posts.
- Seating model: each proof building keeps hand-authored visual base,
  frontage, collision, y-sort, shadow, and draw-width metadata.
- Debug: press `B` to toggle proof-street seating markers; debug is off by
  default and must not be needed for the visual to read.

Acceptance:

- Latest itch upload should show `Godot G-4.8 Variant D Proof Street`.
- The build should open to one street scene, not a four-variant comparison
  board.
- The street must look materially better than the G-4.6 failed proof and the
  G-4.7 board before the grammar is scaled back to the Newport town.
- If it still reads as pasted sprites on a slab, classify as
  `PROOF_STREET_STILL_NOT_BELIEVABLE`, `BUILDING_STREET_GRAMMAR_FAILED`, or
  `VARIANT_D_NOT_VIABLE`.

Visual review result:

- G-4.8 improved technical alignment but still felt like four storefronts
  behind a broad flat strip.
- The player was too far from the storefronts.
- The scene still read as a proof layout instead of a cozy playable street.

## G-4.9: Newport Street Vignette Art Direction

Status: visually blocked by sprite crop contamination; superseded by G-4.9.1.

G-4.9 turns the chosen Variant D grammar into one smaller street vignette:

- Active vignette buildings: `b_mercantile`, `b_counting_house`, and
  `b_chandlery_front`.
- Player visual scale remains `0.78`, but spawn moves closer to the storefront
  lane so the player can stand in front of doors.
- The road is no longer a long alignment slab: it is a narrower cobbled lane
  with a distinct sidewalk/apron, stoop thresholds, curb/gutter, foreground
  wharf planks, and harbor water as context.
- Base props and small blockers are clustered around doors and street edges:
  crates, barrels, rope, signs, lamps, weeds, table goods, dock posts, nets,
  and a rowboat.
- Camera zoom is tighter for a composed first screenshot.
- Debug seating markers still toggle with `B` and remain off by default.

Acceptance:

- Latest itch upload should show `Godot G-4.9 Street Vignette`.
- The first screenshot should look like a cozy harbor street, not a debug
  calibration strip.
- If it still reads as pasted buildings on a slab, classify as
  `STILL_LOOKS_LIKE_CALIBRATION_STRIP`, `STREET_PLANE_STILL_FAILED`, or
  `BUILDING_SEATING_STILL_FAILED`.

## G-4.9.1: Building Sprite Crop Isolation Hotfix

Status: ready for manual itch upload; not accepted until screenshot review
confirms no neighboring building fragments are visible.

G-4.9.1 fixes the sprite-source blocker before any further street art
direction:

- `b_mercantile` uses `assets/sprites/buildings/isolated/mercantile_shop_isolated.png`.
- `b_counting_house` uses `assets/sprites/buildings/isolated/newport_counting_house_civic_exchange_isolated.png`.
- `b_chandlery_front` uses `assets/sprites/buildings/isolated/newport_chandlery_outfitter_front_isolated.png`.
- `b_shop_house` uses `assets/sprites/buildings/isolated/newport_shopfront_awning_isolated.png`.
- The source atlases remain tracked as source material, but these four
  proof-street sprites no longer render from unsafe atlas subregions.
- Proof-street `collision_rect`/`lot_rect` metadata now blocks the occupied
  building volume behind the frontage instead of only a shallow facade strip.
- The HUD review identity should show
  `Godot G-4.9.1 Sprite Crop Isolation`.

Acceptance:

- Latest itch upload shows the G-4.9.1 build label.
- No active proof-street building shows pieces of neighboring atlas buildings
  on its left or right edge.
- If contamination remains, classify as `SPRITE_CROP_CONTAMINATION_REMAINS`
  and do not resume street-vignette composition.

## G-4.9.5: Newport Streetscape Spacing and Believability

Status: active stacked follow-up after the accepted crop/seating gate.

G-4.9.5 keeps the G-4.9.4 crop, seating, grounded baselines, camera, and
vertical placement logic intact. It only adjusts the street frontage
composition:

- Tighten excessive horizontal gaps between the three accepted buildings.
- Preserve the center/civic building as visually important without isolating
  it from the frontage.
- Make any remaining gap read intentionally as an alley, loading area, or
  civic setback.
- Use existing props to bridge empty sidewalk space.
- Keep Worker files, `wrangler.toml`, interiors, economy, combat, inventory,
  save systems, and map expansion out of scope.

Acceptance:

- Latest itch upload should show `Godot G-4.9.5 Streetscape Spacing`.
- The three accepted buildings keep their crop/seating behavior.
- The street reads less like isolated test sprites and more like one
  believable Newport frontage.

## G-4.9.6: Street Vignette Acceptance Gate

Status: clean review-mode gate after G-4.9.5.

G-4.9.6 is not an art expansion pass. It freezes the accepted G-4.9.4/G-4.9.5
building seating and spacing, then prepares a clean player-facing itch review
build:

- HUD identity: `Godot G-4.9.6 Street Vignette Acceptance Gate`.
- Red/yellow/blue debug overlays are off by default.
- Building IDs and debug names are not visible in normal review mode.
- Seating debug remains available only through the debug toggle/mode.
- Validation confirms the player can walk the sidewalk/street area, reach
  the three storefronts, and avoid crop/seating regressions.
- No Worker files, `wrangler.toml`, interiors, economy, inventory, combat,
  save systems, or larger map work are included.

Acceptance:

- Latest itch upload shows the G-4.9.6 build label.
- First screenshot is a clean game view, not a debug proof.
- If debug overlays or building labels appear by default, classify as
  `DEBUG_REVIEW_BLOCKER`.

## G-4.10: Newport Harbor Walk Acceptance

Status: next phase after G-4.9.6 is visually accepted.

G-4.10 turns the accepted street/dock vignette into a 60-90 second
player-facing Newport harbor walk. It should use the existing street/dock
scene and accepted building grammar rather than jumping to interiors,
economy, inventory, combat, save systems, or full map expansion.

## G-5: Migration Architecture

Design how future gameplay systems will move from the JavaScript codebase to
Godot. This is a planning phase, not a porting phase. It may begin only after
G-4.10 establishes an accepted 60-90 second Newport harbor walk on itch.

## G-6: Production Cutover Planning

Define the eventual production-hosting decision, rollback plan, QA gates, and
criteria for replacing the JavaScript Worker route. The Worker remains
production-facing until this phase explicitly changes that.
