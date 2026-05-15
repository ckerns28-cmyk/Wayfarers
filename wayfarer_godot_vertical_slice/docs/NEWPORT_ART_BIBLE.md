# Newport Art Bible

## Newport Visual Cohesion Rules

The building sprites define the visual standard. Future terrain, props,
characters, NPCs, monsters, equipment, UI-world objects, VFX, interiors, and
interactables must match this standard before they are accepted into the review
build.

G-4.16 made the high-detail Newport building sprites the art standard for the
whole town. G-4.17 turned that rule into a repeatable asset-pipeline gate.
G-4.18 adds the matching legal/source gate.

No asset enters the player-facing review build unless it passes both Newport
Visual Cohesion and Asset Provenance gates.

Any new asset, prop, terrain tile, character, NPC, monster, equipment item,
VFX element, or UI-world object must pass this standard before it is accepted
into a player-facing review build.

Target pixel density / apparent detail:

- World surfaces and props must read within one detail band of the building
  sprites. Large flat fills, single-color roads, single-line fences, and
  unshaded rectangle props are placeholders.
- Ground materials need layered base tone, mid-tone patches, small marks, edge
  dirt, contact shadow, and hand-authored seams or texture breaks.
- Props near hero buildings need bevels, outlines, highlights, cast/contact
  shadows, and material-specific internal detail at normal camera zoom.

Outline and edge rules:

- Buildings use dark painterly contours. Props should use 1-2 px dark outlines
  or dark-side shading at the apparent screen scale.
- Roads, yards, docks, and water should avoid hard debug-box borders. Edges
  must be material transitions: curb stones, dirt feathering, worn grass,
  algae, pier shadow, plank lips, or low walls.

Shadow direction and softness:

- Contact shadows fall slightly south/southeast and stay soft. They should seat
  buildings, props, posts, tables, barrels, crates, and pier edges without
  becoming black outlines.
- Building bases keep the G-4.15 object-rule grounding. Surface shadows support
  those bases; they do not replace anchors, footprints, or collision metadata.

Color palette:

- Newport uses weathered coastal neutrals: grey-brown stone, aged tan planks,
  muted clapboard whites, mossy greens, low-saturation harbor blues, and warm
  rope/lantern accents.
- Avoid saturated toy colors, single-hue green fields, flat brown roads, pure
  white cloth blocks, and high-contrast debug colors in normal review mode.
- Highlights should be warm and sparing; shadows should be green-brown,
  blue-green, or dark umber rather than pure black.

Material rules:

- Wood: plank seams, board variation, nail/dark specks, worn highlights,
  darker end grain, and grounding shadow at contact edges.
- Stone: uneven cobbles, slab seams, chipped highlights, edge grime, and curb
  lips where buildings meet the street.
- Dirt: layered tan/umber tracks, small stones, scuffed darker edges, and
  feathered transitions into grass.
- Grass: mottled fields, tufts, darker patches, worn routes near roads and
  doors, and no plain rectangle lots in review mode.
- Water: depth bands, subdued ripples, dark pier contact, shoreline scum, and
  irregular edge treatment.
- Roads: cobble or compacted road texture with rutting, repair patches, curb
  shadow, and authored thresholds at doors.
- Docks: visibly built from planks with board direction, posts, dark waterline
  contact, weathering, and pier-edge shadow.
- Fences: posts plus rails with shadow/highlight, not single pale lines.
- Cloth: no bright flat laundry in hero review. Cloth must be shaded, muted,
  or replaced by role-appropriate nets/canvas until final art exists.
- Crates/barrels/signs/market props: outlined, shaded, material detailed, and
  seated by contact shadow. Remove or defer any prop that still reads as a
  layout marker.

Scale relationship:

- Buildings define the scale. Door height, stoop depth, curb height, player
  height, barrel/crate size, table height, cart width, dock boards, road width,
  and fence height must all read against the building doors and windows.
- Roads and docks must be walkable but not vacant bands. Door paths and service
  lanes should feel human-scaled.
- Vehicles/carts must not exceed building door/story proportions unless they
  are intentionally large wagons.
- The current player is a temporary scale marker, not final character art.

Review-build acceptance:

- Allowed: Newport-compatible buildings, G-4.16 surface kit materials,
  authored prop clusters, muted construction/lot traces that read as ground,
  debug overlays only when explicitly toggled, and no-HUD screenshots.
- Placeholder art: flat roads, flat grass, hard parcel/debug rectangles,
  generic colored boxes, unshaded line props, bright cloth blocks, props that
  lack contact shadows, and any future character/monster/UI-world element that
  does not match the Newport detail level.
- Hard gate: future player sprite sheets, NPC sprite sheets, monsters,
  equipment, weapons, armor, combat VFX, items, and UI-world objects must meet
  these rules before they can be considered review-ready.

## G-4.16 Surface Kit

Implemented surface-kit materials:

- commercial street surface
- curb and sidewalk edge pieces
- dirt path pieces
- grass-to-road transition pieces
- dock plank pieces
- pier edge pieces
- building base/shadow/footprint support pieces
- alley and service-lane pieces

The kit is currently procedural in `MapLayer.gd` so it can cover the starter
harbor consistently before dedicated bitmap terrain assets exist. Dedicated
terrain sprites may replace these pieces later, but they must preserve the
same material rules and validation gate.

## G-4.17 Asset Pipeline Gate

Pipeline folders live under `art_pipeline/newport/`:

- `source_refs/`
- `generated_contact_sheets/`
- `manifests/`
- `atlases/`
- `reports/`
- `scripts/`

The style extraction script measures the existing building sprites and writes
a markdown report, palette contact sheet, and JSON style manifest. The hero
street atlas generator creates project-owned bitmap atlas pieces and records
source, ownership, license, region, scale, collision, y-sort, contact shadow,
placeholder/final state, and review eligibility in the asset manifest.

Assets marked `placeholder=false` and `review_eligible=true` must satisfy the
Newport Visual Cohesion Rules before they can appear in the review build.

The current player is still a temporary scale/debug avatar. Player sprite
sheets need a dedicated art pipeline pass, and NPCs, monsters, equipment,
armor, weapons, and combat VFX cannot be introduced until character style
rules are defined.

## G-4.18 Asset Provenance Gate

G-4.18 makes `art_pipeline/newport/manifests/newport_asset_manifest.json` the
canonical review manifest. Review-facing hero assets must document:

- asset id and atlas region
- generated piece path and creation script
- material category and intended scale
- exact project-owned crop path and crop rectangle when source pixels are used
- whether any project-owned Wayfarer source pixels are copied
- whether any third-party, web-scraped, marketplace/sample, ripped, or mystery
  source pixels are present
- license/ownership status and review eligibility

G-4.18 allowed sources are deterministic generated Pillow output, local
hand-authored output, documented local Blender procedural support components,
and exact crops from project-owned in-repo Newport building sprites. The old
G-4.17 prior prop-sheet crop path is not eligible for normal review.

The player remains temporary scale/debug art. G-4.19 or soon after must begin
the player/NPC sprite-style foundation, and no NPC, monster, combat, or
equipment system should enter normal review until character style is solved.
