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

Current G-4.9.7 target: G-4.9.7 is a Street Vignette Polish Gate on top of
the accepted G-4.9.6 placement fix. It keeps crop seating, vertical grounding,
camera, and debug-default behavior intact while tightening horizontal spacing,
dressing remaining gaps with existing props, strengthening sidewalk/curb/road/
harbor-walk/water readability, and muting rear lot blocks so the first
player-facing review looks less like staged geometry.

Current G-4.10 result: the active Godot scene has reset from vignette polish
to starter harbor town buildout. The three accepted hero buildings remain as
style anchors, but the scene now defines a scalable 16-lot starter district
plan with a harborfront commercial street, working wharf and pier layer,
inland residential/civic/support lots, and a readable movement loop from main
street to dock access to inland lanes and back. Temporary future lots are
muted planned foundations, not debug rectangles. The HUD review identity
should show `Godot G-4.10 Starter Harbor Town Buildout Reset`.

Current G-4.10A result: G-4.10 exposed the same crop/anchor issue that blocked
the original hero buildings. G-4.10A pauses town expansion and normalizes the
active building pipeline: every visible starter-town building now renders from
an isolated padded sprite, every placed building references a reusable
`BuildingCatalog.building_definition()`, and the three water-bottom harbor
buildings are reserved for wharf/water lots instead of being treated like dry
streetfront buildings. The HUD review identity should show
`Godot G-4.10A Building Anchor/Crop Gate`.

Current G-4.11 result: the starter town asset kit is expanded and accepted as
an asset-integration milestone. The active kit now includes inn/tavern,
mercantile, counting house, chandlery, shop house, market shed, custom house,
large residence, boarding house, small residence, cooperage shed, dock
warehouse, wharf boathouse, and dock storehouse. The church-coded village hall
is not the starter civic anchor; it is demoted as deferred chapel/meeting-house
art.

Current G-4.12 result: the expanded kit has been recomposed and dressed into a
more believable Newport Starter Harbor without adding gameplay systems.
Frontage spacing is less grid-like, the commercial street / dock economy /
inland civic-residential layers have clearer visual identities, planned lots
are muted into background yards, and the wharf buildings remain beside the
main wharf with readable side landings onto their own dock platforms. The HUD
review identity should show `Godot G-4.12 Starter Town Composition + Dressing`.

Current G-4.12B result: the same town composition now has a surface-cohesion
pass for clean visual review. Roads, sidewalks, dock planks, wharf edges,
water, shoreline contact, yards, fences, laundry, role-based prop clusters,
and muted background lots have been restyled so the non-building environment
better matches the detailed Newport building art. The HUD review identity
should show `Godot G-4.12B Surface Cohesion Gate`.

Current G-4.13A result: building visual bounds, planning lot bounds, collision
footprints, interaction zones, and foot anchors are separate concepts. The
full tall sprite rectangle is review-only; the player is blocked by shallow
ground-contact `collision_footprint` rectangles. This fixes the road behind
the mercantile/counting-house row and prepares planning-only rowhouse slots for
G-4.13B. The HUD review identity should show `Godot G-4.13A Building Footprint
Walkability Gate`.

Current G-4.13A.1 result: the remaining marked rear-lane choke near the
tavern/mercantile/small-residence area has a specific owner and fix. The
blocking contact came from `DetailBlocker_mercantile_front_crates`,
`DetailBlocker_west_alley_rope`, and the grown player radius touching
`Building_b_mercantile` at its western/rear footprint edge. The hotfix moves
those decorative blockers onto visibly solid frontage clutter, tightens the
mercantile ground footprint, and adds debug-only route probes for the marked
lane, rear roads, cross-lanes, commercial street, and dock layer. The HUD
review identity should show `Godot G-4.13A.1 Walkability Blocker Hotfix`.

Current G-4.13B result: three narrow infill buildings are active without
changing the town footprint or undoing G-4.13A footprints. After screenshot
review, the infill was re-seated as purposeful street-wall fabric rather than
back-lot gap filling: the tavern and mercantile planning/visual widths were
tightened, the mercantile was nudged east, and `b_clerk_townhouse` now occupies
the tavern-to-mercantile street-wall slot. `b_printer_rowhouse` moved out of
the too-tight shop-house gap to the east market street edge, and
`b_dockworker_rowhouse` now uses the four-unit clapboard rowhouse art from
Newport pack A instead of duplicating the boarding-house sprite. The
counting-to-chandlery, shop-to-market, and inland/civic townhouse slots stay
deferred because they protect walkability or currently read as orphaned
placement. The HUD review identity should show `Godot G-4.13B Rowhouse Infill
Density`.

Current G-4.23A result: the G-4.22A walkable-city blockout was not treated as
design approval. This pass tightens Newport around a more readable harborfront
avenue, visible uphill connectors, and a back street behind the first
waterfront road. Broad slab-like road polygons were narrowed, old proof/legacy
ground overlays remain off, and the provenance-tracked G-4.20A atelier
terrain, path, shoreline, and building-grounding transitions are reintroduced
as controlled clean-review material glue rather than random decoration.
Follow-up repair within the pass expands the surrounding city fabric into
ordered upper and side frontage instead of isolated building drops, and the
starter camera moves closer to the streets so the player reads as entering a
city rather than observing one from a distance. Enclosed lot cells now fill the
street grid with yards, service courts, civic lawns, market courts, thresholds,
and low walls instead of leaving raw green gaps between roads. Tavern/Inn
remains the west social anchor, the market and civic roads stay walkable, and
new G-4.23A runtime screenshot automation captures the required whole-town,
harborfront, uphill-road, back-street, tavern/market, and walkability proof
views. Visual acceptance still requires human review.

Current G-4.23B result: the G-4.23A street grammar is preserved while the
remaining debug/zoning read is repaired toward an authored harbor city. The pass
softens old translucent outer lot and road overlays, adds irregular ground
patches, cobble wear, verge strips, thresholds, service lanes, market pockets,
and yard edges, and strengthens the harborfront with piers, dock seams, bollards,
mooring points, rope coils, crates, cargo/loading zones, fishery/service hints,
and water-edge transitions. Tavern/Inn remains the west social anchor, the
commercial/civic/residential/service districts have clearer frontage logic, and
the review camera now frames harbor, avenue, civic/commercial/tavern focus, and
uphill fabric together. The HUD review identity should show `Godot G-4.23B
Newport Authored Street + Harbor Immersion Repair`. A new G-4.23B screenshot
wrapper captures whole-town, working harborfront, Tavern/Inn, uphill connector,
back street, building frontage/lot grounding, and player walkability proof.
Technical validation can pass; design/art/world/UX acceptance still requires
human visual review.

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

## G-4 Visual Foundation Charter: 8.0 Exit Gate

Status: permanent G-4 rule.

Wayfarer cannot exit G-4 until the origin city reaches an 8.0+ visual
foundation in the player-facing review build.

Canonical review reference:
`wayfarer_godot_vertical_slice/docs/G4_VISUAL_FOUNDATION_CHARTER.md`.

Wayfarer North Star:

Wayfarer is being built toward a full MMORPG-scale fantasy world. The current
Godot slice is the origin city: a Newport, Rhode Island-inspired 1700s harbor
town that should feel like the player's first real home base in a much larger
world. The long-term game includes quests, monsters, magic, equipment,
exploration, progression, interiors, NPCs, player identity, and a
revolutionary-political story backbone with fantasy layered underneath.

Current focus:

- Do not build those gameplay systems yet.
- Make the origin city visually satisfying, stylistically unified,
  commercially safe, and technically scalable.
- Evaluate every change against long-term MMORPG viability, Newport 1700s
  fantasy theme, visual cohesion, legal provenance, player immersion, and
  roadmap sequencing.

G-4 exit requirement:

- Do not recommend moving to G-5 until the review build reaches an 8.0+
  visual foundation.
- A validator pass is not an art pass. If screenshots do not look better, the
  pass is not accepted as visual progress.
- Screenshot review must support the rating; automated validation only proves
  contracts, provenance, and regressions.

8.0+ visual foundation means:

- The town feels authored, not assembled.
- Buildings, streets, docks, props, player, and HUD belong to one art
  direction.
- No player-facing debug rectangles or placeholder stickers dominate the
  scene.
- At least one hero street/dock slice looks like the real game.
- The HUD/UI has intentional fantasy/MMORPG styling.
- Yellow temporary art is clearly marked as temporary.
- Green-origin art production is proven.
- Screenshot review supports the rating, not just automated validation.

Permanent production role expectation:

- The project should be reviewed as a master game programmer, art director,
  systems designer, production lead, and scrum master would review it.
- Do not merely satisfy validators; protect the game's long-term world scale,
  production pipeline, source safety, player immersion, and phase order.

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

## G-4.9.7: Street Vignette Polish Gate

Status: acceptance polish after the G-4.9.6 placement fix.

G-4.9.7 preserves the accepted building extraction, crop seating, vertical
grounding, camera, and debug-label behavior. It is scoped to player-facing
streetscape polish:

- HUD identity: `Godot G-4.9.7 Street Vignette Polish Gate`.
- Horizontal spacing is adjusted only enough to make the three accepted
  buildings feel like a natural Newport frontage rather than evenly staged
  test sprites.
- Remaining gaps are dressed as loading/setback space with existing props.
- Sidewalk, curb, road, harbor walk, dock edge, and water receive stronger
  tonal separation.
- Rear lot silhouettes are muted so they read as background massing instead
  of temporary debug rectangles.
- Contact shadows under props, stoops, lamps, dock details, and building
  bases are used to reduce floating.
- No Worker files, `wrangler.toml`, interiors, economy, inventory, combat,
  save systems, or map expansion are included.

Acceptance:

- Latest itch upload shows the G-4.9.7 build label.
- The three accepted buildings remain seated with no crop/seating regression.
- Player walkable space in front of each building and toward the pier-facing
  edge remains obvious.
- Background lots no longer read as debug geometry.

## G-4.10: Starter Harbor Town Buildout Reset

Status: ready for manual itch upload.

G-4.10 deliberately stops treating the current scene as a finished three-
building vignette. The three accepted waterfront buildings are preserved as
style anchors, then placed inside the first real Newport-inspired starter
harbor district plan.

Implemented:

- HUD identity: `Godot G-4.10 Starter Harbor Town Buildout Reset`.
- Branch: `codex/g-4-10-starter-harbor-town-buildout-reset`.
- Active buildings: 9, across harborfront commercial, working wharf, and
  inland residential/civic layers.
- Total district lots: 16, including 7 muted planned future lots.
- Harborfront/commercial row: inn/tavern, mercantile, counting house,
  chandlery, shop-house frontage, plus future fishmonger/warehouse slots.
- Dock/wharf layer: wharf apron, three pier fingers, market/storehouse
  anchors, cargo, barrels, crates, ropes, fish racks, nets, boats, posts, and
  dock-service planned lots.
- Inland layer: village hall/civic anchor, harbor cottage, planned residences,
  civic-residence slot, support lane, fences, clothesline, and yard dressing.
- Navigation loop: main street frontage -> wharf/dock access -> pier/service
  work layer -> inland cross lane/support lane -> main street return.
- Validation checks active building count, 10-16 lot range, planned-lot
  manifest, missing-asset manifest, no NPCs, seating metadata, and route
  reachability.

Missing asset manifest for G-4.11:

- small home variants
- warehouse
- chandlery/fishmonger
- dock shack
- civic/residence variant
- market stall
- carts
- crates
- barrels
- rope coils
- signs
- fencing

Before NPCs/quests begin:

- Replace planned-lot silhouettes with matching Newport building/prop assets.
- Confirm manual itch review reads as a working harbor district, not a staged
  strip.
- Keep player movement through street, dock, pier, and inland loop clean.
- Keep interiors, economy, combat, inventory, save systems, and quest/NPC
  placement out of scope until the town asset kit is expanded.

## G-4.10A: Building Asset Anchor + Crop Normalization

Status: ready for manual itch upload.

G-4.10A is a corrective gate before any more town expansion. The G-4.10 layout
direction is preserved, but all currently visible buildings now go through a
normalized reusable definition path instead of one-off sprite placement.

Implemented:

- HUD identity: `Godot G-4.10A Building Anchor/Crop Gate`.
- Branch: `codex/g-4-10a-building-anchor-crop-normalization`.
- Active buildings: 11, across harborfront commercial, working wharf, and
  inland residential/civic layers.
- Every active building uses `BuildingCatalog.building_definition()` with
  texture path, full isolated sprite region, visual scale, foot anchor,
  collision, interaction zone, shadow, and district role metadata.
- The active G-4.10 building sprites render from isolated padded PNGs so
  atlas-neighbor bleed does not appear in review.
- `b_dock_storehouse`, `b_wharf_boathouse`, and `b_dock_warehouse` are
  reserved for water/wharf placement and validated as harbor-integrated
  buildings instead of dry streetfront buildings.
- Debug overlays remain hidden by default for review. Press `B` to toggle the
  G-4.10A building anchor/collision/interaction overlay, or `F3` for the full
  building-debug overlay.
- Validation now fails if a starter-town building lacks a reusable definition,
  isolated sprite source, or normalized anchor metadata.

Root cause:

- G-4.10 expanded from the accepted hero buildings into more atlas-sourced
  buildings. Some of those crops still used live atlas regions or regions with
  neighboring sprite pixels, and the placement path relied on per-instance
  anchors that were not a stable building asset contract. The fix is isolated
  source images plus reusable definitions that own the foot-anchor and
  collision/interaction geometry.

Before G-4.11:

- Manually review the itch build with debug off and confirm no visible roofs,
  sides, storefronts, bases, or harbor buildings are cropped.
- Keep G-4.11 focused on asset-kit expansion and replacement art after this
  crop/anchor gate is accepted.
- Do not add NPCs, quests, economy, combat, inventory, save systems, or
  interiors until the starter district art kit and traversal read are stable.

## G-4.11: Town Asset Kit Expansion / Missing Building Set

Status: accepted as the asset-integration milestone for the starter harbor.

Implemented:

- HUD identity: `Godot G-4.11 Town Asset Kit Expansion`.
- Branch: `codex/g-4-11-town-asset-kit-expansion`.
- Active buildings: 14, across harborfront commercial, working wharf, inland
  residential/civic, and support-lane layers.
- Integrated roles: inn/tavern, mercantile, counting house, chandlery, shop
  house, market shed, custom house, large residence, boarding house, small
  residence, cooperage shed, dock warehouse, wharf boathouse, and dock
  storehouse.
- The church-looking hall is deliberately demoted to deferred chapel /
  meeting-house art and is not active as the starter civic anchor.
- Every active starter building uses the reusable building-definition system.

Deferred asset needs:

- Dedicated fishmonger storefront.
- Final cooperage / barrel-shop art.
- Blacksmith or smithy art, if the role belongs in the starter town.
- More small-home variants.
- Dedicated cart, crate, barrel, rope, sign, fence, and lantern sprites.

## G-4.12: Starter Town Composition + Dressing

Status: ready for manual itch upload.

G-4.12 deliberately uses the accepted G-4.11 building kit instead of adding
more buildings. The work targets composition, town logic, role-based dressing,
lot treatment, road readability, and dock transitions.

Implemented:

- HUD identity: `Godot G-4.12 Starter Town Composition + Dressing`.
- Branch: `codex/g-4-12-starter-town-composition-dressing`.
- Harborfront commercial buildings have small frontage-depth and spacing
  variations so the street reads less like an asset board.
- The commercial street is dressed with role-specific signs, stoops, crates,
  barrels, market tables, rope, and lamps.
- The dock / wharf layer uses extended narrow side landings, cargo, rope,
  nets, fish racks, rowboats, and waterline clutter to clarify how goods move
  between water, storage, market, and street.
- Inland civic/residential/support lots are dressed with cleaner custom-house
  frontage, fences, yards, benches, clotheslines, shrubs, cooperage barrels,
  and wood clutter.
- Planned lots and distant blocks are visually muted into background yards or
  planned silhouettes instead of debug rectangles.
- Debug overlays stay hidden by default for clean review. Press `B` for
  building seating overlays or `F3` for full building debug overlays.

Before NPCs/quests begin:

- G-4.13B should use the corrected footprints for townhouse/rowhouse infill
  without closing rear roads, side lanes, or dock approaches.
- G-4.13C should integrate the prop atlas and role-based dressing.
- G-4.13D should complete final navigation, collision, approach-zone,
  interaction-zone, dock-access, and invisible-blocker validation across the
  expanded starter town.

## G-4.12B: Newport Surface Cohesion + Clean Review Gate

Status: ready for manual itch upload.

G-4.12B keeps the accepted G-4.12 starter town composition and focuses on the
environment around the buildings. It is a visual cohesion gate, not a gameplay
or navigation-validation phase.

Implemented:

- HUD identity: `Godot G-4.12B Surface Cohesion Gate`.
- Branch: `codex/g-4-12b-surface-cohesion-clean-review`.
- Clean review remains the default: building overlays are hidden unless `B` or
  `F3` is toggled, and `F2` controls review metadata.
- Roads and sidewalks received worn surface patches, grime, seams, edge
  variation, and less rectangular material breaks.
- Dock and wharf surfaces received plank weathering, edge shadows, stronger
  post/piling language, side-landing contact, cargo clusters, and transition
  detail.
- Water and shoreline received depth bands, extra ripple variation, and
  waterline contact marks near dock buildings and wharf structures.
- Residential/civic/support lots received yard paths, shrubs, low walls,
  benches, softened fences, clotheslines, and domestic clutter.
- Background lots were restyled as faded structures, yards, low walls, and
  distant town silhouettes instead of obvious layout blocks.
- Role-based prop clusters were strengthened for tavern, mercantile, counting
  house/custom house, chandlery, shop/market, residences/boarding house,
  cooperage, and dock warehouse/boathouse/storehouse reads.

Still weak / deferred:

- Many environment details are still drawn primitives. Dedicated painterly
  prop sprites for carts, sacks, crates, barrels, rope, signs, fences, and
  lanterns would improve final cohesion.
- G-4.13A should happen only after this visual pass is accepted and should
  focus first on separating building visual bounds from physical footprints.

## G-4.13A: Building Footprint / Collision / Walkability Gate

Status: implemented; accepted only with the G-4.13A.1 hotfix below.

G-4.13A fixes the blocker found during G-4.12B review: several red debug
rectangles were effectively tall visual sprite bounds, so visually open rear
roads behind `b_mercantile` and `b_counting_house` could not be walked
reliably. This pass keeps the town footprint and building placement stable.

Implemented:

- HUD identity: `Godot G-4.13A Building Footprint Walkability Gate`.
- Branch: `codex/g-4-13a-building-footprint-walkability-gate`.
- Runtime building metadata now separates `visual_bounds`, `lot_bounds`,
  `collision_footprint`, `interaction_zone`, `foot_anchor`, and y-sort data.
- The actual `StaticBody2D` uses `collision_footprint`, not `visual_bounds` or
  `lot_bounds`.
- Active town buildings received tight ground-contact footprints:
  `b_inn_tavern`, `b_mercantile`, `b_counting_house`,
  `b_chandlery_front`, `b_shop_house`, `b_market_shed`, `b_custom_house`,
  `b_large_residence`, `b_boarding_house`, `b_res_small`,
  `b_cooperage_shed`, `b_dock_warehouse`, `b_wharf_boathouse`, and
  `b_dock_storehouse`.
- `B`/`F3` overlays label visual bounds, lot bounds, collision footprint,
  interaction zone, foot anchor, and y-sort marker so the actual blocker is
  obvious.
- Validator samples confirm the rear road behind the mercantile/counting-house
  row, harborfront rear road, west/central/east cross-lanes, and dock walk do
  not hit building collision.
- G-4.13B planning-only infill slots are recorded for tavern-to-mercantile,
  counting-house-to-chandlery, shop-to-market, inland civic, and support-lane
  gaps.

Remaining known issues:

- The infill slots are not active buildings yet.
- Prop atlas integration is still deferred to G-4.13C.
- Final whole-town manual route validation remains G-4.13D.

## G-4.13A.1: Remaining Walkability Blocker Hotfix

Status: implemented for local validation.

G-4.13A.1 fixes the remaining black-box marked rear-lane blocker from the
review screenshots without changing the town footprint or advancing rowhouse,
prop-atlas, or gameplay-system work.

Root cause:

- The exact blocking owners at the marked lane throat were
  `DetailBlocker_mercantile_front_crates`, `DetailBlocker_west_alley_rope`,
  and the grown player collision radius against `Building_b_mercantile`.
- The crates and rope were separate scenery blockers placed in visually open
  road/lane space.
- The mercantile collision footprint was already separated from its tall
  `visual_bounds`, but its rear/west edge still pinched the intended lane once
  the player body radius was included.

Implemented:

- HUD identity: `Godot G-4.13A.1 Walkability Blocker Hotfix`.
- Branch: `codex/g-4-13a-1-walkability-blocker-hotfix`.
- `b_mercantile` keeps a solid base/foundation blocker, but its
  `collision_footprint` is slightly narrower and shallower so the rear lane is
  no longer blocked by the shop's painted facade area.
- `mercantile_front_crates` and `west_alley_rope` detail blockers were moved
  onto lower frontage clutter where they read as visible obstructions instead
  of invisible rear-lane blockers.
- `B`/`F3` debug now also labels collision-layer owners such as
  `DetailBlocker_*` and shows debug-only route probe markers.
- The validator now checks all collision owners, not only building bodies, for
  route samples and G-4.13A.1 probes.

Routes revalidated:

- black-box marked rear lane north/west of `b_mercantile`
- road behind `b_mercantile`
- road behind `b_counting_house`
- lane near `b_res_small`
- tavern/mercantile rear-lane throat
- inland road to commercial row access
- commercial row to dock-layer access
- central/east rear roads, commercial street, and dock boardwalk

Remaining known issues:

- G-4.13B now owns rowhouse/townhouse density work.
- Prop atlas integration is still deferred to G-4.13C.
- G-4.13D remains the final whole-town manual navigation/collision pass.

## G-4.13B: Townhouse / Rowhouse Infill + Density Pass

Status: implemented for local validation.

G-4.13B makes Newport Starter Harbor feel more like a tight 1770s harbor
village street without adding gameplay systems, expanding the town footprint,
or touching the JavaScript Worker route.

Implemented:

- HUD identity: `Godot G-4.13B Rowhouse Infill Density`.
- Branch: `codex/g-4-13b-rowhouse-townhouse-infill-density`.
- Active infill:
  - `b_printer_rowhouse`: `newport_narrow_merchant_townhouse_a`, placed in
    `slot_market_east_edge_narrow_shop` as a narrow print-shop/rowhouse on
    the east market street edge after the shop-house gap proved too tight.
  - `b_clerk_townhouse`: `newport_formal_townhouse_block_a`, placed in
    `slot_tavern_mercantile_narrow_rowhouse` after tightening tavern and
    mercantile planning bounds and nudging the mercantile east.
  - `b_dockworker_rowhouse`: `newport_waterfront_shop_house`, placed in
    `slot_support_lane_boarding_gap` as four-unit clapboard support-lane
    lodging beside the boarding-house block.
- Deferred infill:
  - `slot_counting_chandlery_lane_edge_shop`, kept open to preserve the
    central cross-lane and rear-road sightline.
  - `slot_shop_market_townhouse_pair`, deferred because the shop-house visual
    bounds/frontage make that gap too tight for readable rowhouse placement.
  - `slot_cottage_customs_inland_townhouse`, deferred because the earlier
    placement read as an isolated yard object rather than street fabric.
- Every active infill building uses the separated G-4.13A metadata:
  `visual_bounds`, `lot_bounds`, `collision_footprint`, `interaction_zone`,
  `foot_anchor`, and y-sort/debug data. Full sprite bounds are not blocking
  collision.

Future story hooks now supported by location:

- Printer rowhouse: revolutionary pamphlet lead, apprentice errand, rented-room
  rumor, or suspicious printing job.
- Clerk townhouse: customs-clerk lodging, family dispute, suspicious neighbor,
  or quiet artifact-discovery start.
- Dockworker rowhouse: missing-person lead, wharf-job connection, or boarding
  neighbor rumor.

Routes revalidated:

- road behind `b_mercantile`
- road behind `b_counting_house`
- rear road / lane near `b_res_small`, tavern, and mercantile
- inland civic road and central cross-lane
- main commercial street
- commercial row to dock-layer access
- wharf boardwalk and dock layer
- new infill approach probes below the clerk, printer, and dockworker rowhouses

Remaining known issues:

- `newport_chandlery_cottage` and `newport_market_frontage_row` remain
  deferred candidates for later layout or role passes.
- Prop atlas integration is still deferred to G-4.13C.
- G-4.13D remains the final whole-town manual navigation/collision validation
  pass after prop dressing.

## G-4.14B: Building Grounding + Entity Contract Repair

Status: implemented for local validation.

G-4.14B preserves the G-4.14A building metadata and interaction contract, then
repairs the building-object foundations that QA flagged in the manual itch
review loop.

Implemented:

- HUD identity: `Godot G-4.14B Building Grounding + Entity Contract Repair`.
- Branch: `codex/g-4-14b-building-grounding-entity-repair`.
- Building definitions expose `door_anchor`, `y_sort_anchor`, and
  `ground_contact_rect` alongside the existing gameplay metadata.
- `Building.gd` now exposes `get_prompt_text()`,
  `is_player_in_interaction_area()`, `get_door_anchor_local()`, and
  `get_ground_contact_rect()` without removing the G-4.14A methods.
- Player prompts are tied to tight doorway interaction areas instead of a broad
  street-radius check, and the on-screen label is smaller.
- The QA overlay remains default-off and can show footprint, interaction area,
  door anchor, base/y-sort anchor, and building identity when toggled.
- Commercial-row thresholds and row-front cargo props were moved into the
  street-side band so they support the grounding read instead of cutting
  through building bases.

Verified scope:

- Counting House / civic building.
- Harbor Residence / large residence.
- Harbor Mercantile / shopfront commercial building.
- Dock Storehouse / harbor warehouse-style building.

## G-4.15: Village Layout Using Object Rules

Status: implemented for local validation and screenshot review.

G-4.15 uses the G-4.14B building-object contract to recompose the existing
starter harbor without adding interiors, new systems, new buildings, new art,
or map expansion.

Implemented:

- HUD identity: `Godot G-4.15 Village Layout Using Object Rules`.
- Branch: `codex/g-4-15-village-layout-object-rules`.
- Each active starter-harbor building now carries an explicit parcel rule:
  `parcel_id`, `district_band`, `frontage_line_y`, `setback_from_road`,
  `side_gap_minimum`, `door_path_target`, `prop_band`, `ground_pad`, and
  `lot_type`.
- Commercial, market, civic, residential, support-lane, and dock bands draw
  parcel-specific pads, stoops, frontage paths, prop bands, and subtle gutters.
- The Shop House / Market Shed / Printer Rowhouse cluster was modestly opened
  up so the shop no longer reads as a squeezed leftover facade.
- Commercial-row props were moved into side/prop bands so doorway interaction
  zones remain clear.
- `B` building seating overlay now uses compact labels; `F3` keeps detailed
  labels for full object-contract inspection.

District and band adjustments:

- Upper civic/residential band: yards and road-facing walks make houses and the
  Custom House read as seated parcels instead of floating sprites.
- Middle commercial band: stone pads, thresholds, door paths, and parcel gutters
  clarify the street frontage while preserving the shared curb datum.
- Lower dock band: plank work pads and cargo zones connect warehouse objects to
  the wharf logic.

Visual QA rubric:

- Target: 8.5/10 or better.
- Current self-score recorded in `NewportTownBlueprint.gd`: 8.5-8.7 across
  grounding, doors, spacing, prop purpose, walkability, harbor identity,
  y-sort/depth, screenshot read, and not-pasted feel.

Remaining known visual issues:

- Cargo props now have the G-4.18D atelier standard lock; remaining non-cargo
  props still need themed atelier packs.
- The road/ground textures remain procedural and will benefit from final
  painterly surface assets later.
- No interiors are included yet; public doors continue to use the existing
  stub messages.

## G-4.16: Newport Art Cohesion Reset

Status: implemented for local validation and screenshot review.

G-4.16 is an art-direction foundation pass, not a position nudge. It preserves
the G-4.15 building object rules while raising the surrounding surfaces and
props toward the visual standard set by the Newport building sprites.

Implemented:

- HUD identity: `Godot G-4.16 Newport Art Cohesion Reset`.
- Branch: `codex/g-4-16-newport-art-cohesion-reset`.
- Newport Visual Cohesion Rules are now documented in
  `wayfarer_godot_vertical_slice/docs/NEWPORT_ART_BIBLE.md` as a permanent
  acceptance gate.
- A Visual Mismatch Audit is documented in
  `wayfarer_godot_vertical_slice/docs/NEWPORT_VISUAL_MISMATCH_AUDIT.md`.
- `MapLayer.gd` exposes a G-4.16 reusable surface kit covering commercial
  street, curb/sidewalk, dirt paths, grass-road transitions, dock planks,
  pier edges, building-base/shadow support, and service lanes.
- Main street, frontage pads, dock planks, harbor edge, grass/yards, service
  lanes, and hero props have been redrawn/restyled from that kit.
- Debug/parcel/propland rectangles no longer dominate normal review; they are
  restyled into surface wear, pads, yards, and service-lane marks. Explicit
  object-rule debug remains toggle-only.
- `F4` and `--review-no-hud` provide no-HUD screenshot review mode.
- `tools/package_itch_web.sh` now creates both the stable itch ZIP and a
  versioned ZIP so the newest upload candidate is clear.

Permanent future-art rule:

- Player character sprite sheets, NPC sprite sheets, monsters, items, weapons,
  armor, equipment, animation style, combat VFX, and UI-world objects must
  follow the Newport Visual Cohesion Rules before review acceptance.

Validation gates:

- Validator expects the G-4.16 build label and surface-kit API.
- Validator confirms the surface kit material manifest, no-HUD screenshot mode,
  clean review default, and the G-4.16 `surface_kit_pass` plan marker.

## G-4.17: Newport Asset Pipeline + Hero Street Atlas Proof

Status: implemented for local validation, export/package, and browser review.

G-4.17 starts the scalable Newport art pipeline. It does not try to repaint the
whole town. Instead, it uses the existing building sprites as measurable style
references, creates a manifest-backed atlas workflow, and proves the approach
on one central commercial-row section.

Permanent roadmap principle:

- The building sprites define the visual standard. Future terrain, props,
  characters, NPCs, monsters, equipment, UI-world objects, VFX, interiors, and
  interactables must match this standard before they are accepted into the
  review build.

Implemented:

- HUD identity: `Godot G-4.17 Newport Asset Pipeline + Hero Street Atlas`.
- Branch: `codex/g-4-17-newport-asset-pipeline-hero-street-atlas`.
- Newport pipeline structure under `wayfarer_godot_vertical_slice/art_pipeline/newport/`.
- Python/Pillow style extraction from in-repo building sprites, producing a
  markdown report, palette contact sheet, and JSON style values manifest.
- Newport terrain/prop manifest schema and hero street asset manifest with
  source, ownership/license, atlas region, scale, collision, y-sort, contact
  shadow, visual cohesion, placeholder/final, and review eligibility fields.
- Project-owned generated hero atlas at
  `art_pipeline/newport/atlases/newport_hero_street_atlas_v1.png`.
- Central commercial-row proof uses atlas road, curb/sidewalk/stoop,
  building-base shadow, dirt/wear, grass-edge, dock/market transition, and
  prop-cluster pieces.
- Weak procedural props in the hero proof rectangle are skipped and replaced by
  atlas clusters with muted Newport palette, dark edge treatment, material
  detail, contact shadow, and door/window/player scale discipline.
- The G-4.16 procedural surface kit remains as fallback outside the hero proof.
- Screenshot review path is documented in
  `art_pipeline/newport/reports/G417_SCREENSHOT_REVIEW_PATH.md`.

Known blocker:

- The current player is still a temporary scale/debug avatar. A dedicated
  player sprite-sheet pipeline pass is required before player art is accepted.
  NPCs and monsters cannot be introduced until character style rules are
  defined. Equipment, armor, weapons, and combat VFX must match the future
  player/NPC sprite detail.

Validation gates:

- Validator expects the G-4.17 build label.
- Validator confirms the G-4.16 fallback surface-kit API and the G-4.17 hero
  atlas material API.
- Validator confirms pipeline folders, generated reports/contact sheets,
  style/asset manifests, atlas file, asset source ownership/license, and
  review-eligible manifest flags.

## G-4.18: Newport Proprietary Asset Factory + Style Unification

Status: implemented for local validation, export/package, and browser review.

G-4.18 locks legal/source safety and uses the Newport building sprites as the
art authority for a more coherent hero commercial strip. This pass is not
gameplay. It replaces the weaker G-4.17 review-facing prop/ground assumptions
with a project-owned asset factory, a canonical provenance manifest, and a
street/dock/prop restyle that better belongs to the same coastal-colonial art
family as the buildings.

Permanent rule:

- No asset enters the player-facing review build unless it passes both Newport
  Visual Cohesion and Asset Provenance gates.

Implemented:

- HUD identity: `Godot G-4.18 Newport Proprietary Asset Factory + Style Unification`.
- Branch: `codex/g-4-18-newport-proprietary-asset-factory-style-unification`.
- Canonical manifest: `wayfarer_godot_vertical_slice/art_pipeline/newport/manifests/newport_asset_manifest.json`.
- Provenance audit: `wayfarer_godot_vertical_slice/art_pipeline/newport/reports/G417_G418_ASSET_PROVENANCE_AUDIT.md`.
- Project-owned Newport asset factory in
  `art_pipeline/newport/scripts/generate_newport_asset_factory.py`, with
  deterministic Pillow output, documented Newport building crops, and local
  Blender 5.1 procedural support components where listed.
- G-4.17 prior prop-sheet crops are removed from normal review output.
- Hero street patch now uses multiple cobble/curb/grass/dirt transition pieces
  with ragged edges and contact shadows instead of one obvious rectangle.
- Hero props are rescaled and restyled as Newport building-derived/generated
  clusters with contact shadows.
- Dock pieces use finer plank rhythm, weathered variation, dark waterline
  contact, post shadows, and irregular pier edges.
- Player mismatch is explicitly deferred: the current player remains temporary
  scale/debug art, and G-4.19 or soon after must begin the player/NPC sprite
  foundation before NPC, monster, combat, or equipment review.

Validation gates:

- Validator expects the G-4.18 build label and G-4.18 hero atlas API.
- Validator confirms canonical and compatibility manifests, provenance audit,
  generated proof sheet, generated atlas pieces, Blender support script, and
  review-eligible provenance fields.
- Python provenance validation rejects third-party, web-scraped, mystery, and
  prior prop-sheet source pixels.

## G-4.18A: Newport Building Sprite Provenance Audit

Status: implemented as an audit/gate pass. No new building art expansion should
resume until yellow building sprites are either source-cleared or replaced.

G-4.18A audits the upstream building sprites that G-4.17/G-4.18 used as visual
authority and crop sources. The pass adds a dedicated building provenance
manifest, documents reverse/similarity search results, and keeps uncertain
sprites out of final/commercial classification.

Permanent Building Sprite Provenance Gate:

- Every active normal-review building sprite must have an entry in
  `wayfarer_godot_vertical_slice/art_pipeline/newport/manifests/newport_building_sprite_provenance.json`.
- Green status requires project-owned, generated-for-Wayfarer, properly
  licensed, or otherwise commercially usable source proof.
- Yellow status is temporary review art only and cannot become final/commercial
  art without source-chain evidence or replacement.
- Red or unknown status is not review eligible.
- No ripped game sprite, unlicensed marketplace pack, mystery PNG, or
  undocumented third-party-derived art may enter final Wayfarer art.

Implemented:

- Building provenance manifest:
  `wayfarer_godot_vertical_slice/art_pipeline/newport/manifests/newport_building_sprite_provenance.json`.
- Building provenance report:
  `wayfarer_godot_vertical_slice/art_pipeline/newport/reports/G418A_BUILDING_SPRITE_PROVENANCE_AUDIT.md`.
- Specific chandlery/outfitter audit for
  `newport_chandlery_outfitter_front_isolated.png`.
- Validator coverage in
  `art_pipeline/newport/scripts/validate_newport_asset_provenance.py` so active
  normal-review building sprites require provenance entries.
- All current building sprites are yellow, not green, because upstream atlas
  source files have no in-repo prompt, PSD/layer source, generation log, or
  explicit commercial license record.

## G-4.18B: Green-Origin Newport Art Factory

Status: provenance infrastructure accepted; visual result not accepted.

Temporary yellow review art may be used to prototype composition, scale, and
gameplay, but final-commercial Wayfarer art must come from green-origin assets
with documented provenance. Yellow assets cannot be used as pixel sources for
green final art.

G-4.18B starts the separate `art_pipeline/newport_green_origin/` factory. Assets
in this namespace must come from deterministic project scripts, hand-authored
project parameters, or documented project-owned/commercial-compatible sources.
The current Newport buildings and crop-derived G-4.17/G-4.18 hero atlas remain
`temporary_review_yellow`, not `final_commercial_green`.

G-4.18B proved that the green-origin/provenance pipeline can produce
source-safer assets, but it failed the visual bar. The weak generated proof
must not remain in normal review just because it is legally cleaner.
Green-origin is required, but green-origin alone is not enough.

Permanent correction:

- A source-safe asset is still rejected if it weakens the screenshot.
- The weak proof may remain as pipeline evidence, bakeoff reference, or
  quarantine material, but not as player-facing visual progress.
- Future green-origin candidates must be judged against the same Newport
  art-direction, immersion, and 8.0+ screenshot standard as yellow review art.

## G-4.18C: Quarantine Weak Green-Origin Proof

Status: implemented as the G-4.18C review baseline correction.

G-4.18C removes weak green-origin proof art from normal review while preserving
the provenance infrastructure learned from G-4.18B.

Green-origin is necessary but not sufficient. An asset can be legally clean and
still visually rejected. The G-4.18B proof family remains provenance-green, but
it is `visual_failed_g418b_proof`, `lab_only=true`, and
`normal_review_eligible=false` until a later art method improves it.

Acceptance:

- Weak green-origin proof assets are quarantined from normal player-facing
  review output.
- Green-Origin Lab mode (`F6` or `--show-green-origin-lab`) exposes the proof
  only as labeled lab/provenance evidence.
- Provenance scripts, manifests, audit notes, and contact sheets remain
  available as production infrastructure.
- Review docs explain that the proof failed visually even if it improved legal
  hygiene.
- Normal screenshots do not regress by showing weaker legal-clean placeholders.
- `G418C_GREEN_ORIGIN_VISUAL_RETROSPECTIVE.md` records the visual failure and
  required next production-method bakeoff.

## G-4.18D: Art Production Method Bakeoff

Status: implemented as the Newport atelier cargo pipeline lock.

G-4.18D locks the Newport atelier cargo source sheet as the minimum prop
quality bar for future Newport themed packs. The accepted sheet contains a
wooden crate, coopered barrel, rope coil, and composed wharf cargo cluster with
readable silhouettes, dense material detail, authored-looking pixel texture,
believable wood/metal/rope weathering, natural overlap/depth, and game-ready
3/4 perspective.

The prior weak deterministic/procedural cargo cluster is deprecated as a
visual target. It may remain as lab/provenance evidence, but future wharf proof
work must judge cargo and prop dressing against the atelier sheet and its
transparent extracted sprites.

Locked reusable pattern:

- 10/10 source sheet.
- Saved prompt/source artifact.
- Local extraction script.
- Transparent sprites with clean bounds and no magenta background or halo.
- Atlas, contact sheet, manifest, provenance report, and extraction QA report.
- Godot placement using manifest-style asset IDs, consistent scale, pivot, and
  grounding data.
- Automated validation before any themed rollout continues.

Next recommended rollout order after this lock:

- Dock clutter expansion, implemented first as G-4.19A.
- Terrain edge dressing.
- Signs/lamps/posts.
- Market goods/carts.
- Shopfront props.
- NPC/player standards.

Acceptance:

- `art_pipeline/newport_atelier/` contains the source image, saved prompt,
  extraction script, transparent sprites, atlas, contact sheet, manifest, and
  reports.
- Extraction QA fails on magenta background, magenta halo/fringe, poor crop
  padding, cut-off edges, unreadable sprites, or source/manifest identity
  mismatch.
- Godot normal cargo placement uses the extracted atelier assets, not the old
  weak cargo proof.
- Assets remain `green_origin_candidate_pending_license_review`; they are not
  final-commercial approved until the project license policy explicitly clears
  AI-assisted generated artwork.
- Future city-wide rollout proceeds through themed atelier packs only after
  this lock passes validation.

## G-4.19A: Newport Dock Clutter Atelier Pack

Status: implemented as the first city rollout pack from the G-4.18D atelier
standard.

G-4.19A creates the Newport dock/wharf clutter pack without redesigning the
pipeline: saved exact prompt, saved source sheet, local extraction script,
transparent sprites, atlas, contact sheet, manifest, provenance report,
extraction QA, Godot placement, and validation.

The pack includes bollards, mooring hardware, fishing net, sacks/fish baskets,
anchor, dock repair planks, dock lantern, and shoreline debris candidates. The
in-world proof places only a controlled subset around wharf, cargo, market
edge, harbor edge, and service path clusters so the port gains atmosphere
without visual noise or navigation confusion.

Acceptance:

- All assets remain `ai_assisted_green_origin_candidate_pending_license_review`.
- No source pixel path uses yellow/uncertain assets, web images, marketplace
  packs, or third-party sprites.
- Extracted sprites have transparent bounds with no magenta background, no
  magenta halo, no cut-off edges, and readable silhouettes.
- Godot placement respects scale, grounding, pivot, depth/overlap, and the
  no-over-scatter policy.

## G-4.19B: Newport Visual Production System & Core Asset Audit

Status: implemented as a production registry, core asset audit, roadmap
discipline pass, and validator expansion.

G-4.19B stops the Newport visual pipeline from continuing as isolated
single-sheet passes. Newport is the playable starting town/village for
Wayfarer, so production now moves through mass atelier waves that support a
believable coastal town, readable navigation, harbor/market/civic/residential
organization, emotional invitation to explore, gameplay readiness, and
consistency with the G-4.18D/G-4.19A atelier standard.

This pass does not create new sprite sheets, rebuild buildings, redesign the
game, or quick-patch visual assets. It creates the trust structure needed to
scale production:

- `art_pipeline/newport/manifests/newport_visual_production_registry.json`
  classifies major Newport visual assets by category, path, provenance,
  current usage, visual quality, gameplay role, and rebuild status.
- `art_pipeline/newport/reports/G419B_NEWPORT_VISUAL_PRODUCTION_AUDIT.md`
  records the core building audit, non-building audit, mass production waves,
  and validator expectations.
- Current buildings are useful temporary review/layout anchors, but they remain
  `temporary_review_yellow` until rebuilt or source-cleared.
- Old/unverified assets are not automatically final.
- All future visual assets must follow the G-4.18D/G-4.19A atelier pipeline:
  saved source/prompt, extraction script, transparent sprites, atlas/contact
  sheet, manifest/provenance report, QA, Godot placement, and validation.

Special building lock:

- The Newport Tavern/Inn is a designated centerpiece, not a generic tavern.
- The future rebuild direction is brick construction, two sets of large
  twin-stack chimneys, Hotel Viking-inspired grand coastal hotel presence,
  warm windows, heavy fireplaces, maritime prestige, and fantasy charm.
- The current tavern crop is classified `REBUILD_REQUIRED_CENTERPIECE` and
  remains only a temporary review placeholder.

Production waves:

- Wave 1: environmental believability - terrain edge dressing,
  cobble/path transitions, shoreline dressing, road borders, and
  mud/grass/stone blend pieces.
- Wave 2: town identity - signs, lamps, posts, notice boards, banners, and
  civic markers.
- Wave 3: economy/life - market carts, crates of goods, shopfront props,
  merchant tables, and baskets/barrels/sacks variants.
- Wave 4: building rebuild or enhancement - only after audit decisions are
  accepted, with the Tavern/Inn as an anchor rebuild.
- Wave 5: character/NPC standard - only after the town environment has enough
  visual context.

Acceptance:

- Registry entries have status, category, path, provenance/source status,
  usage, gameplay role, and rebuild status.
- Assets cannot be marked final without final provenance.
- Deprecated visual targets cannot be used in normal/final MapLayer paths.
- Atelier assets must keep source, prompt, extraction, atlas, contact sheet,
  manifest, provenance report, and QA artifacts.
- G-4.18D cargo and G-4.19A dock clutter remain visible and validated.

## G-4.20A: Newport Environmental Believability Atelier Wave

Status: implemented as the first mass atelier production wave.

G-4.20A moves Newport from isolated prop packs to controlled environmental
believability production. This wave exists to make the playable starting town
feel grounded, navigable, and physically coherent before larger identity,
economy, building, or character passes begin.

The wave adds four themed atelier packs:

- Terrain edge dressing for grass-to-road, mud-to-cobble, dirt borders, worn
  corners, tufts, stones, weeds, and puddles.
- Cobble/path transitions for market-spine walking surfaces, broken cobble,
  dirt-worn patches, road shoulders, and plank/cobble seams.
- Shoreline/harbor edge dressing for seaweed, shells, wet rocks, driftwood,
  wet sand/mud, tide puddles, eelgrass, and harbor debris.
- Building grounding and service-lane accents for doorstep stones,
  foundation shadows, wall weeds, repair boards, barrels/crates, wash tubs,
  low fencing, and firewood.

Production artifacts live under `art_pipeline/newport_atelier/` and include
the exact prompts, source generated sheets, extracted transparent sprites,
atlases, contact sheets, manifests, extraction QA, provenance reports, and the
wave manifest/report. New entries are registered in
`art_pipeline/newport/manifests/newport_visual_production_registry.json` as
AI-assisted green-origin candidates pending final license policy approval.

Placement is deliberately controlled. The normal scene uses a subset around
wharf-to-town transitions, road/grass edges, dock/shoreline edges, market
spine grounding, and non-centerpiece building bases. It must not over-scatter,
block navigation, cover important entrances, hide path readability, or use
clutter to mask broken composition.

Building rebuild comes after this environmental glue unless the audit forces
an earlier correction. The Tavern/Inn remains locked as a future
`REBUILD_REQUIRED_CENTERPIECE`: brick construction, two sets of large
twin-stack chimneys, Hotel Viking-inspired coastal landmark presence, warm
social hub, quest anchor, and player landmark. G-4.20A does not patch or treat
the current tavern as final.

Acceptance:

- Three to five environmental atelier sheets are produced under the locked
  G-4.18D/G-4.19A pipeline; G-4.20A ships four.
- Every pack has source sheet, saved prompt, transparent sprite extraction,
  atlas, contact sheet, manifest, QA, and provenance report.
- New assets are registered with source/provenance status, usage, visual
  quality, gameplay role, rebuild/final status, and notes.
- No magenta background or halo remains in extracted sprites.
- Controlled in-world placement improves Newport's believability and
  navigation while preserving G-4.18D cargo and G-4.19A dock clutter.
- Validators fail clearly for missing wave artifacts, missing registry status,
  final assets without provenance, deprecated final targets, magenta/halo
  extraction remnants, and missing/deprecated MapLayer references.

## G-4.20B: Newport Town Identity Atelier Wave

Status: implemented as the second controlled atelier production wave.

G-4.20B adds signage, lamps, wayfinding, civic/market markers, and shopfront
support assets so Newport reads as a believable playable starting town with
stronger identity, orientation, and market-spine memory. It builds on the
G-4.20A environmental believability pass instead of starting a parallel or
stacked branch.

The wave adds four themed atelier packs:

- Signs and shop markers for mercantile, fishmonger, warehouse, inn/rooms,
  harbor direction, bracket, plaque, and temporary Tavern/Inn sign candidates.
- Lamps and wayfinding for street lamps, dock lantern posts, signposts,
  bollard lanterns, harbor markers, rope-rail posts, pier lanterns, and coastal
  waystones.
- Civic and market identity for notice boards, market banners, harbor bulletin
  boards, small flags, civic plaques, posting poles, pennant signs, and dock
  rules boards.
- Shopfront support accents for awnings, display crates, folded cloth, slates,
  hanging baskets, planters, rope pennants, and basket/parcel displays.

Production artifacts live under `art_pipeline/newport_atelier/` and include
the exact prompts, source generated sheets, extracted transparent sprites,
atlases, contact sheets, manifests, extraction QA, provenance reports, and the
town identity wave manifest/report. New entries are registered in
`art_pipeline/newport/manifests/newport_visual_production_registry.json` as
AI-assisted green-origin candidates pending final license policy approval.

Placement is controlled around the market spine, harbor/wharf wayfinding,
civic identity points, shopfront believability, and player orientation. It
must not block navigation, over-decorate, make signs visually noisy, or treat
any current unverified building as final.

This is not a building rebuild pass. Core buildings remain under their audit
status, and the Tavern/Inn remains locked as a future
`REBUILD_REQUIRED_CENTERPIECE`: brick construction, two sets of large
twin-stack chimneys, Hotel Viking-inspired coastal landmark presence, warm
social hub, quest anchor, and player landmark. G-4.20B may register temporary
Tavern/Inn sign candidates, but it does not patch, finalize, or rebuild the
Tavern/Inn.

Acceptance:

- Three to five town identity atelier sheets are produced under the locked
  G-4.18D/G-4.19A pipeline; G-4.20B ships four.
- Every pack has source sheet, saved prompt, transparent sprite extraction,
  atlas, contact sheet, manifest, QA, and provenance report.
- New assets are registered with source/provenance status, usage, visual
  quality, gameplay role, rebuild/final status, and notes.
- No magenta background or halo remains in extracted sprites.
- Controlled in-world placement improves Newport's identity and navigation
  while preserving G-4.20A environmental believability assets.
- Validators fail clearly for missing wave artifacts, missing registry status,
  final assets without provenance, deprecated final targets, magenta/halo
  extraction remnants, and missing/deprecated MapLayer references.

## G-4.21A: Newport Core Building Atelier Rebuild Wave 1

Status: implemented as the first controlled core-building atelier rebuild wave.

G-4.21A begins the Newport core building atelier rebuild. This is the first
true architectural pass for the starting town: the buildings are rebuilt as a
coherent Newport coastal fantasy family for orientation, emotional memory,
gameplay clarity, and believable playable density, not as isolated asset
accumulation.

The required hero asset is the Tavern/Inn. Its direction is brick
construction, two front/back bridged twin-stack chimney sets, warm windows, a clear
entrance, strong foundation grounding, old Newport/coastal prestige, and a
Hotel Viking-inspired coastal landmark presence without direct copying. It is
the social hub, quest anchor, and player landmark, and it must visually outrank
ordinary shops and homes.

Wave 1 also rebuilds a controlled proof subset around the Tavern/Inn:

- Mercantile / General Store for the market spine.
- Wharf Warehouse / Dock Office for the working harbor economy.
- Two quieter residence/cottage variants for residential streets.
- Cooperage workshop / service building for service-lane and dock-adjacent
  town life.

Production artifacts live under `art_pipeline/newport_atelier/` and include
the exact prompt, source generated sheet, extracted transparent sprites, atlas,
contact sheet, manifests, extraction QA, and provenance reports. New building
entries are registered in
`art_pipeline/newport/manifests/newport_visual_production_registry.json` and
`art_pipeline/newport/manifests/newport_building_sprite_provenance.json` as
AI-assisted green-origin candidates pending final license policy approval.

Old building assets are retained. Replaced old/unverified buildings are not
automatically final; their registry status is updated so they cannot be treated
as current final visual targets. Controlled in-world placement is wired through
`BuildingCatalog` without deleting old files, over-placing buildings, masking
layout problems, or finalizing collision/navigation beyond the current proof
validation.

Acceptance:

- Tavern/Inn hero asset is present, registered, and validated as brick with two
  front/back bridged twin-stack chimney sets and Hotel Viking-inspired-but-not-copied
  landmark presence.
- At least three additional building types ship with the same source/prompt,
  extraction, atlas/contact sheet, manifest, QA, and provenance chain.
- New buildings are registered with status/provenance and controlled proof
  placement.
- Old building statuses are updated without deleting old assets.
- Validators fail clearly for missing building artifacts, missing Tavern/Inn
  hero QA, deprecated active targets, missing MapLayer/BuildingCatalog assets,
  magenta halo/background remnants, cropped sprites, and missing transparent
  bounds metadata where detectable.

## G-4.23A: Newport Street Grammar + Ground Cohesion Repair

Status: implemented for local validation and human visual review.

G-4.23A repairs the G-4.22A visual-state problem Chris identified: a scene can
validate technically while still reading as broad prototype ground bands and
disconnected placement rather than a coherent colonial harbor city.

Implemented:

- HUD identity: `Godot G-4.23A Newport Street Grammar + Ground Cohesion Repair`.
- Branch: `codex/g-4-23a-newport-street-grammar`.
- The harborfront avenue is narrower and stays visually parallel to the wharf
  instead of filling the town with a wide gray blockout slab.
- West, central, east, and market uphill connector roads are drawn first and
  remain visible as routes from harbor work into civic/residential town.
- The back street behind the first waterfront road has a more legible street
  surface and yard/civic frontage rather than a disconnected horizontal pad.
- Additional upper-town and side-edge building fabric now follows shared
  frontage lines, with lot thresholds and fences aligned to the streets so the
  review camera does not read as empty green space around a small set piece.
- Enclosed residential, civic, market, and service lot cells fill the major
  gaps between streets with purposeful yards and work courts rather than
  scatter dressing.
- Starter harbor-town camera framing is closer to the street and buildings,
  giving player movement a more entered-city perspective without enlarging the
  player sprite.
- G-4.20A atelier terrain/path/shoreline/building-grounding placements are
  visible in clean review as provenance-tracked material transitions, while
  older G-4.17/G-4.18 proof overlays remain gated behind
  `G422A_SHOW_LEGACY_PROOF_OVERLAYS`.
- Buildings keep the existing collision/pathing contract and are visually tied
  to lots, yards, docks, civic spaces, and frontage thresholds without adding
  decorative clutter to hide unresolved layout.
- A G-4.23A screenshot wrapper captures whole town, harborfront avenue, uphill
  connector road, back street, tavern/market anchor, and player walkability
  proof while preserving the G-4.22A wrapper.

Acceptance:

- Technical validation can pass only the engineering gate.
- Design/art/world/UX acceptance remains `NEEDS_HUMAN_REVIEW` until Chris
  reviews the fresh screenshots against the Newport 8.5+/10 bar.
- Remaining issues must be separated from validation status in PR summaries.

## G-4.23B: Newport Authored Street + Harbor Immersion Repair

Status: implemented for local validation and human visual review.

G-4.23B repairs Chris's G-4.23A classification of TECHNICAL PASS / DESIGN NEEDS
REPAIR. It keeps the proven harbor avenue, uphill roads, back street, and
ordered frontage rows, but moves the scene away from a debug/zoning diagram and
toward an authored colonial harbor-city starter scene.

Implemented:

- HUD identity: `Godot G-4.23B Newport Authored Street + Harbor Immersion Repair`.
- Branch: `codex/g-4-23b-newport-authored-street-harbor-immersion`.
- Build metadata records `REVIEW_HOST = itch`, `REVIEW_CHANNEL = manual ZIP`,
  and the G-4.23B source branch without packaging a ZIP.
- Old translucent outer-town lot and street overlays are softened, and the main
  lot read is replaced by irregular ground patches, yards, service courts,
  stoops, fences, frontage thresholds, and worn door paths.
- Harborfront economy gains dock seams, piers/fingers, loading surfaces,
  bollards, mooring points, rope coils, crates, cargo piles, fishery/service
  hints, ramps/steps, and water-edge transitions with purposeful placement.
- Tavern/Inn remains the centerpiece and is integrated into a street/market
  social pocket rather than pasted beside a road.
- Mercantile/shop buildings face the avenue with clearer commercial frontage,
  while civic, residential, and service buildings sit on more believable lots,
  yards, or work courts.
- Subtle irregularity is added through broken cobble patches, compacted dirt
  feathers, narrowed service lanes, soft ground boundaries, and uneven old-town
  edges without destroying G-4.23A clarity.
- Camera framing is adjusted so the first runtime review presents harbor,
  waterfront avenue, Tavern/Inn/commercial/civic focus, uphill connectors, and
  back street fabric in one coherent view.
- The G-4.23B screenshot wrapper captures whole town, working harborfront
  avenue, Tavern/Inn social anchor, uphill connector road, back street/service
  lane, building frontage/lot grounding, and player walkability proof while
  preserving no-HUD review capture.
- The Agent Council runner now uses phase-aware screenshot wrapper selection,
  so G-4.23B reports list the G-4.23B capture gate while preserving the older
  G-4.22A automation paths.

Acceptance:

- Technical validation can pass only the engineering gate.
- Design/art/world/UX acceptance remains `NEEDS_HUMAN_REVIEW` until Chris
  reviews the G-4.23B screenshots/playable scene against the Newport 8.5+/10
  bar.
- Remaining risks include temporary player/NPC scale/style, temporary
  provenance-limited building art, and residual procedural ground artifacts.
- PR summaries must classify this as ready for human visual review, not as
  approved final design.

## G-4.18E: Green-Origin Hero-Quality Asset Family

Status: planned.

G-4.18E creates one green-origin asset family that is good enough to be placed
beside the current yellow buildings without lowering the scene quality.

Acceptance:

- The family is source-safe, documented, and repeatable.
- It contains enough variants to prove production scale, not just a one-off
  hero image.
- It improves the hero street/dock screenshot compared with the quarantined
  G-4.18B proof.
- The manifest marks it green-origin and review-eligible only after visual
  review confirms it belongs in the Newport fantasy-harbor art direction.

## G-4.19: Player Visual Identity Foundation

Status: planned.

G-4.19 replaces the temporary scale/debug avatar direction with a player visual
identity foundation that can support a long-term MMORPG character pipeline.

Acceptance:

- The player belongs with the Newport buildings, streets, docks, and props at
  the active camera scale.
- The design anticipates equipment, animation, class/fantasy identity, and
  future multiplayer readability without building those systems yet.
- Yellow or temporary character art is clearly labeled and cannot be mistaken
  for final player identity.
- Normal screenshots improve in both HUD and no-HUD modes.

## G-4.20: HUD/UI Visual Redesign

Status: planned.

G-4.20 gives the player-facing HUD/UI intentional fantasy/MMORPG styling
without adding gameplay systems.

Acceptance:

- HUD panels, labels, interaction prompts, review identity, and dialogue
  surfaces feel like part of Wayfarer rather than debug or raw engine UI.
- The HUD supports screenshots instead of covering the scene.
- No-HUD and HUD captures both look appealing.
- Review metadata remains available but does not dominate normal player-facing
  presentation.

## G-4.21: Origin City Hero Slice

Status: planned.

G-4.21 composes the strongest green-origin/yellow-clearly-marked assets,
player foundation, HUD redesign, and Newport surface grammar into one
hero-quality street/dock slice.

Acceptance:

- The slice feels like the real game, not a prototype board.
- Streets, docks, buildings, props, player, HUD, and camera framing support a
  single Newport 1700s fantasy home-base read.
- Yellow temporary art is visible only when explicitly accepted as temporary
  and documented.
- Screenshots show the authored slice in normal, no-HUD, and close-up review.

## G-4.22: 8.0 Visual Foundation Review Gate

Status: planned G-4 exit gate.

G-4.22 is the formal review gate for exiting G-4.

Acceptance:

- The origin city receives an 8.0+ visual foundation rating from screenshot
  review, not just validator output.
- The review packet includes normal HUD, no-HUD, hero street/dock, UI/HUD,
  yellow-art inventory, green-origin production proof, and debug-overlay proof
  captures.
- The town feels authored rather than assembled.
- Buildings, streets, docks, props, player, and HUD belong to one art
  direction.
- At least one hero street/dock slice looks like the real game.
- Asset provenance rules are active; yellow art is clearly temporary; the
  green-origin replacement method is proven.
- Only after this gate is accepted may G-5 be recommended.

## G-5: Migration Architecture

Design how future gameplay systems will move from the JavaScript codebase to
Godot. This is a planning phase, not a porting phase. It may begin only after
G-4.22 accepts the 8.0+ origin city visual foundation review gate.

## G-6: Production Cutover Planning

Define the eventual production-hosting decision, rollback plan, QA gates, and
criteria for replacing the JavaScript Worker route. The Worker remains
production-facing until this phase explicitly changes that.
