# G-4.23B Newport Authored Street + Harbor Immersion Repair

TECHNICAL PASS DOES NOT EQUAL DESIGN PASS.

This report records the G-4.23B production repair for Chris review. It does not
claim visual approval, does not claim approval by Chris, and does not request or
perform a merge.

## Decision Classification

Final decision classification: READY FOR HUMAN VISUAL REVIEW

Technical validation status: PASS

Design/art/world/UX acceptance status: NEEDS_HUMAN_REVIEW

No itch ZIP was packaged in this pass.

## Scope

G-4.23B repairs the G-4.23A Newport scene from a readable street-grammar
blockout toward an authored starter harbor city. The pass stays inside the
existing Newport layout, rendering, provenance, and screenshot automation
surface. It does not add NPC behavior, quests, combat, interiors, or new
gameplay systems.

## What Changed From G-4.23A

- Build identity moved to `G-4.23B` with the required label, host, review
  channel, and source branch.
- Debug-like lot rectangles were reduced in clean review and replaced in the
  main city read with irregular ground patches, frontage thresholds, worn paths,
  fences, stoops, yard edges, and market/civic/service courts.
- The old outer-town street overlays were softened so the scene reads less like
  translucent zoning bands while preserving the harbor avenue, uphill roads, and
  back street established by G-4.23A.
- Harborfront economy was strengthened with authored dock seams, piers, loading
  surfaces, bollards, mooring points, rope coils, crates, cargo piles, fishery
  points, service edges, and water-transition hints.
- Tavern/Inn, commercial fronts, civic buildings, residential rows, and service
  buildings now have clearer thresholds to streets, yards, market pockets, or
  loading areas.
- The clean review render now shows G-4.20A/G-4.20B provenance-safe terrain,
  grounding, signage, lamp, wayfinding, civic, market, and shopfront accents
  where they support city function.
- Starter harbor camera framing was adjusted to show the harbor at bottom,
  civic/commercial/tavern focus, uphill fabric, and fewer cropped edge reads.
- New G-4.23B screenshot automation captures the required proof set while
  preserving no-HUD review screenshots.
- The vertical-slice validator now checks the G-4.23B build identity, Newport
  plan marker, authored street/harbor grammar, and screenshot script presence.
- The Wayfarer Agent Council runner now selects the current phase screenshot
  wrapper for G-4.23B while still listing preserved G-4.22A automation.

## Screenshot Artifacts

Generated at:
`wayfarer_godot_vertical_slice/artifacts/review/g423b_runtime_screenshots/`

- `g423b_01_whole_town.png`
- `g423b_02_working_harborfront_avenue.png`
- `g423b_03_tavern_inn_social_anchor.png`
- `g423b_04_uphill_connector_road.png`
- `g423b_05_backstreet_service_lane.png`
- `g423b_06_building_frontage_grounding.png`
- `g423b_07_player_walkability_proof.png`

The screenshots are proof artifacts for human review. They are not design
approval by themselves.

## Technical Validation

- PASS: Godot import validation.
- PASS: `validate_vertical_slice.gd`.
- PASS: Newport provenance validator.
- PASS: G-4.21A core building extraction validation with registry/provenance
  writes skipped.
- PASS: G-4.23B screenshot wrapper.
- PASS: `git diff --check`.
- PASS: `git diff --cached --check` after final staging.
- PASS: final Wayfarer Agent Council report with validators enabled.

## Visual Review Notes

Improvements visible in the G-4.23B proof set:

- Harborfront now reads more like a working waterfront with piers, loading
  clusters, mooring hardware, service points, and water-edge transitions.
- The Tavern/Inn remains the west social anchor and now sits in a more legible
  street/market pocket rather than beside a bare road slab.
- Commercial and civic frontages face the avenue or back street with clearer
  thresholds.
- Uphill connectors, the back street, and wharf access remain readable without
  returning to chaotic placement.
- The first whole-town review frame shows the harbor, town fabric, and uphill
  settlement logic together.

Known visual/design risks for Chris review:

- The scene still contains procedural placeholder ground and some faint layout
  ghosts; G-4.23B reduces the debug read but does not make Newport final art.
- Player/NPC scale and style remain temporary and intentionally deferred.
- Some building art is temporary review art under provenance rules, not final
  commercial art.
- Visual wonder, compression, curiosity, class texture, and 8.5+/10 world read
  need human judgment from the screenshots and playable review.

## Human Review Needed

Chris should review whether the G-4.23B screenshots and playable build now read
as an authored colonial harbor starter city rather than a functional layout
diagram. Specific review targets:

- working harbor economy
- waterfront avenue parallel to harbor work
- uphill roads and back street clarity
- Tavern/Inn social anchoring
- commercial/civic/residential/service district legibility
- lot and frontage grounding
- unified street/ground material language
- player/NPC walkability implications
- whether remaining placeholder artifacts block the Newport 8.5+/10 bar

## Non-Goals Preserved

- No merge performed.
- No itch ZIP packaged.
- No new systems, quests, combat, NPC behavior, or interiors added.
- No unapproved asset promotion.
- No claim of Chris approval.
