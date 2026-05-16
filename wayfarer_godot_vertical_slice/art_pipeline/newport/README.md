# Newport Asset Pipeline

G-4.17 introduced the first production-facing Newport asset pipeline. G-4.18
turns it into a proprietary asset factory and provenance gate. The building
sprites remain the visual authority; this folder exists to make terrain and
prop work measurable, repeatable, source-safe, and reviewable before anything
is accepted into the build.

Folders:

- `source_refs/`: project-owned style references and provenance notes.
- `blender/`: local Blender 5.1 procedural component render helpers used only
  when their output is documented and palette-stylized by the factory.
- `generated_assets/`: generated project-owned hero-strip pieces and local
  support component output.
- `generated_contact_sheets/`: generated palettes, reference sheets, and visual QA sheets.
- `manifests/`: style values, schema notes, and asset manifest JSON files.
- `atlases/`: generated or imported atlas sheets used by the hero proof.
- `reports/`: markdown reports for art direction, screenshot review, and pass notes.
- `scripts/`: Python/Pillow tools for extraction, generation, and validation support.

No unlicensed scraped web art belongs here. No third-party game sprites,
ripped assets, mystery art, or marketplace/demo/sample assets without explicit
compatible licensing belong here.

Permanent gate:

No asset enters the player-facing review build unless it passes both Newport
Visual Cohesion and Asset Provenance gates.

Any atlas or prop used by the review build must have source,
ownership/license, placeholder/final state, provenance status, and review
eligibility recorded in `manifests/newport_asset_manifest.json`.

Green-origin production is required for final art, but it is not automatically
review-eligible. If a source-safe generated proof looks weaker in screenshots,
it must be quarantined as pipeline evidence until the art method improves.
G-4.18C records that split with `visual_quality_status`,
`normal_review_eligible`, `lab_only`, and `final_commercial_eligible` fields.

The G-4 exit bar is an 8.0+ origin city visual foundation: the Newport harbor
town must feel authored, unified across buildings/streets/docks/props/player/
HUD, free of dominant debug/placeholders in normal review, and supported by
normal, no-HUD, hero slice, HUD/UI, yellow-art, and green-origin evidence
screenshots.
