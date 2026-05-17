# G-4.18E Green-Origin Hero-Quality Asset Family

## Final Authority Verdict

Final authority verdict: `COUNCIL_PASS_READY_FOR_PR`

The Wayfarer Agent Council is the acceptance authority for this ordinary
pre-G-5 production pass under
`docs/PRE_G5_AUTONOMOUS_PRODUCTION_PROTOCOL.md`. Human visual review is not
required because no true escalation blocker is present.

G-4.18E proves the locked Newport atelier pipeline can produce, extract,
register, validate, place, and visually judge a coherent hero-quality asset
family without defaulting back to deterministic or hand-drawn placeholder prop
sets.

## Asset Family

Family: Newport Harbor Commercial + Tavern District Asset Family.

The family contains 32 generated/extracted assets across four coordinated
packs:

- Tavern/Inn District: hanging inn sign, paired lanterns, planters, service
  barrels/crates, brick threshold, stable tack, hearth/service detail, and a
  registered twin-stack chimney detail candidate.
- Commercial Avenue: mercantile and fishmonger signs, market cart, produce
  crates, basket/parcels, awning roll, street lamp, and directional signage.
- Harbor/Dock Edge: dock barrels, large rope coil, fishing crate/net stack,
  drying frame, bollards, cargo stack, harbor lantern post, and fish baskets.
- Rear Street / Service Connectors: fence gate, utility barrels, alley crates,
  firewood barrow, stone edging, wash tub/linen, rain barrel, and repair
  sawhorse.

One registered asset, `atelier_g418e_tavern_twin_stack_chimney_detail_01`, is
not placed in the playable hero slice because roof-detail integration would
need a building-aware attachment pass. It remains registered and validated as a
candidate instead of being forced into a misleading runtime placement.

## Source And Provenance

Source prompts and source sheets are preserved under
`wayfarer_godot_vertical_slice/art_pipeline/newport_atelier/source_generated/`.
Extraction is reproducible through
`wayfarer_godot_vertical_slice/art_pipeline/newport_atelier/scripts/extract_g418e_hero_asset_family.py`.

Classification result:

- `origin_classification`: `green_origin_candidate_pending_license_review`.
- `provenance_status`: `ai_assisted_green_origin_candidate_pending_license_review`.
- `final_commercial_candidate`: `false`.
- `final_commercial_eligible`: `false`.
- No web-scraped, marketplace, yellow building, red, or unknown source pixels
  are promoted into the playable hero slice.

This is a green-origin candidate family, not a final-commercial promotion.

## Runtime Evidence

Screenshot evidence was generated and inspected:

- `wayfarer_godot_vertical_slice/artifacts/review/g418e_runtime_screenshots/g418e_01_tavern_inn_district_asset_dressing.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g418e_runtime_screenshots/g418e_02_commercial_avenue_asset_family.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g418e_runtime_screenshots/g418e_03_harbor_dock_edge_asset_family.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g418e_runtime_screenshots/g418e_04_rear_service_connector_grounding.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g418e_runtime_screenshots/g418e_05_gameplay_zoom_readability.png`
- `wayfarer_godot_vertical_slice/artifacts/review/g418e_runtime_screenshots/g418e_06_wide_newport_cohesion.png`

The screenshot set shows the family improving Tavern/Inn identity, commercial
avenue richness, dock economy readability, rear-service grounding, gameplay
scale readability, and whole-town cohesion without using random prop scatter to
hide street or lot problems.

## Validation Evidence

- PASS: Godot import validation.
- PASS: `validate_vertical_slice.gd`.
- PASS: Newport provenance validator.
- PASS: `validate_g418e_hero_asset_family.py`.
- PASS: G-4.21A core building extraction validation with registry/provenance
  writes skipped.
- PASS: G-4.18E screenshot wrapper and PNG verification.
- PASS: Python `py_compile` for changed Python scripts.
- PASS: `git diff --check`.
- PASS: `git diff --cached --check`.

The first G-4.18E validation loop caught a magenta-residue issue on the rear
service fence gate. The extractor now removes strict key-magenta and purple
matte residue before saving sprites, and the regenerated asset family passes
the G-4.18E validator.

## Council Acceptance Rationale

G-4.18E supports the accepted G-4.23B street/harbor layout instead of fighting
it. The family clusters around existing districts: Tavern/Inn social frontage,
commercial avenue shop/market activity, working dock edge cargo/service life,
and rear-lane grounding. The assets use the locked painterly Newport atelier
standard, transparent extraction, contact shadows, controlled scale, and
district-specific placement.

The Council judges the pass as clearing the 8.5+/10 pre-G-5 visual/art/world
bar for this phase:

- Harbor-city believability: PASS.
- Support for accepted G-4.23B layout: PASS.
- Coherent Newport visual language: PASS.
- Clean extraction/rendering: PASS.
- Provenance classification: PASS.
- Yellow/red/unknown promotion risk: PASS; no incorrect promotion found.
- Gameplay readability: PASS.
- Screenshot sufficiency: PASS.
- Human escalation required: NO.

## Remaining Caveats

- Building sprites remain temporary provenance-limited candidates pending final
  art/licensing policy.
- Player and NPC sprites remain below the surrounding environment quality.
- Some legacy signage and ground artifacts remain roadmap residue; G-4.18E does
  not classify those as new accepted hero assets.
- Final commercial use still requires project policy approval for AI-generated
  artwork.

## Next Phase

Recommended next phase: G-4.19 Player Visual Identity Foundation.

Rationale: Newport now has an accepted authored layout and a coherent
hero-quality asset family. The player/NPC visual language is the most visible
remaining mismatch in gameplay screenshots and should be brought up toward the
environment bar next.
