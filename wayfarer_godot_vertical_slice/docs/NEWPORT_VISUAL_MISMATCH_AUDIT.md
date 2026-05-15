# Newport Visual Mismatch Audit

This audit records why the pre-G-4.16 scene did not yet match the Newport
building sprites even after G-4.15 fixed object rules, scale, footprints, and
placement.

## Current Mismatch Categories

- Flat road surfaces: the commercial street still read as a broad painted band
  with repeated procedural marks rather than a built, repaired, walked-on
  street. It needed cobble density, rutting, curb shadow, and authored patches.
- Flat grass fields: residential and background areas used soft green blocks.
  They lacked grass texture, worn thresholds, yard variation, and believable
  transitions into road or building bases.
- Dirt and off-road paths: paths were mostly thick strokes. They did not show
  edge dirt, stones, scuffed centers, or human-scale wear at doors.
- Dock and harbor wood: wharf boards were too simple beside the painterly
  buildings. They needed directional planks, board seams, nails, dark end
  contact, waterline grime, and stronger pier-edge shadows.
- Water edge treatment: water and shoreline were serviceable but still flatter
  than the building art. The edge needed layered depth, scum, dark contact, and
  irregular pier-shadow cues.
- Laundry line: bright cloth rectangles read as low-detail placeholder art.
  In hero review they are replaced by muted harbor net/canvas lines until
  proper shaded cloth assets exist.
- Fences: thin pale lines and tiny posts did not match the building outlines.
  Fences need rails, darker posts, shadow, and reduced brightness.
- Barrels, crates, and market tables: useful for layout, but too simple for
  hero screenshots. They needed bevels, internal planks/bands, highlights,
  shadows, and darker outlines.
- Debug and parcel rectangles: lot and prop-band rectangles were helpful for
  layout review but too dominant in the player-facing build. Normal review now
  restyles these into natural wear, pads, yards, and service-lane marks; hard
  debug remains toggle-only.
- Building shadows and footprints: G-4.15 object rules are correct, but the
  surrounding ground needed curb/stoop pieces and material contact so buildings
  felt embedded rather than pasted down.
- Player sprite mismatch: the current player is a functional scale marker. It
  is not final art and does not yet match the Newport building density.
- Future NPC/monster style risk: adding gameplay characters with lower-detail
  sprites would immediately break the scene. Character, monster, equipment,
  item, and VFX work must obey the Newport Visual Cohesion Rules.

## G-4.16 Corrections

- Main commercial street now uses the G-4.16 commercial street surface with
  cobble variation, worn patches, curb panels, darker edge contact, and less
  flat fill.
- Building frontage pads now use sidewalk/curb pieces, authored thresholds,
  dirt paths, grass transitions, and natural prop wear instead of visible
  rule rectangles.
- Wharf and pier pieces now use higher-detail plank drawing with board
  direction, seams, nails, weathering, dark lips, posts, and pier edge scum.
- Grass, yards, and service lanes use mottled ground, tufts, worn path edges,
  and reduced lot-outline visibility.
- Hero props have upgraded shading/detail, and bright laundry is replaced by
  muted harbor net/canvas lines.
- F4 and `--review-no-hud` provide a no-HUD review screenshot mode so the town
  can be judged without the upper-left HUD covering the civic/residential band.

## G-4.17 Asset-Pipeline Proof

- The central commercial row now has an atlas-based proof area layered over the
  procedural fallback: cobbled harbor road, curb/sidewalk/stoop strip,
  building contact shadow, dirt/wear transitions, grass edge, and dock/market
  transition.
- Weak central procedural props in the proof rectangle are skipped and replaced
  with generated atlas prop clusters that include dark outlines or dark-side
  shading, material detail, muted Newport colors, and contact shadows.
- The prior project prop sheet
  `wayfarer_v7_github_ready/worker/assets/wayfarer/props/hearthvale_props_atlas_v1_transparent.png`
  was audited during G-4.17 and is retained only as historical source context.
  It is not eligible for G-4.18 normal review output.
- Follow-up browser review removed source-background rectangles from the wharf
  and shop prop clusters so atlas props stay transparent and seated by contact
  shadows rather than looking like pasted crop boxes.
- The atlas is project-owned generated art. Source, ownership/license,
  placeholder/final flags, atlas regions, scale, collision behavior, y-sort
  behavior, contact-shadow requirements, cohesion status, and review
  eligibility are recorded in the Newport asset manifest.
- Outside the hero proof, the G-4.16 procedural surface kit remains an accepted
  fallback until later atlas passes replace more of the town.

Known blocker:

- The current player remains a temporary scale/debug avatar. A dedicated player
  sprite-sheet pipeline pass is required before player art can be accepted.
  NPCs and monsters should not be introduced until character style rules are
  defined, and equipment, armor, weapons, and combat VFX must match the future
  player/NPC sprite detail.
- The broader dock/wharf system still needs a dedicated atlas pass to
  synchronize the dockhouse sprite plank angles, harbor wharf surfaces, pier
  lips, and waterline contact treatment across the whole map.

## G-4.18 Provenance And Style Unification

- The hero atlas source policy is now locked in
  `art_pipeline/newport/manifests/newport_asset_manifest.json`.
- Review-facing hero assets are deterministic project-owned generated output,
  documented local Blender support components, and exact project-owned Newport
  building crop composites where listed. No third-party game sprites, ripped
  assets, marketplace/demo/sample assets, mystery assets, web-scraped art, or
  copied prior prop-sheet pixels are allowed.
- The central street proof now breaks the prior hard rectangular read with
  multiple cobble patches, ragged grass/cobble feathering, curb/stoop strips,
  building-base contact shadow, dirt wear, and a dock transition layer.
- Hero props now use Newport building crop detail and muted generated support
  pieces instead of the earlier low-detail placeholder shapes.
- Dock pieces now use finer plank rhythm, reduced black grid outlining, dark
  waterline contact, post-shadow strips, and weathered project-owned wharf
  material.
- Permanent rule: No asset enters the player-facing review build unless it
  passes both Newport Visual Cohesion and Asset Provenance gates.
- The player remains temporary scale/debug art. G-4.19 or soon after must
  begin the player/NPC sprite-style foundation, and no NPC, monster, combat, or
  equipment system should enter normal review until character style is solved.
