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
