# Newport Asset Pipeline

G-4.17 introduces the first production-facing Newport asset pipeline. The
building sprites remain the visual authority; this folder exists to make future
terrain and prop work measurable, repeatable, and reviewable before anything is
accepted into the build.

Folders:

- `source_refs/`: project-owned style references and provenance notes.
- `generated_contact_sheets/`: generated palettes, reference sheets, and visual QA sheets.
- `manifests/`: style values, schema notes, and asset manifest JSON files.
- `atlases/`: generated or imported atlas sheets used by the hero proof.
- `reports/`: markdown reports for art direction, screenshot review, and pass notes.
- `scripts/`: Python/Pillow tools for extraction, generation, and validation support.

No unlicensed scraped web art belongs here. Any atlas or prop used by the
review build must have source, ownership/license, placeholder/final state, and
review eligibility recorded in a manifest.
