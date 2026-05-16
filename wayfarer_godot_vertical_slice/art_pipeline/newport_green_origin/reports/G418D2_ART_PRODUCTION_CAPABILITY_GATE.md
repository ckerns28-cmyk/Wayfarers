# G-4.18D.2 Art Production Capability Gate

## Verdict

G-4.18D.2 produced one green-origin rope coil + crate/barrel dockside cluster,
but it does not clear the tiny-prop visual gate. The asset is rated 7.4 / 10
against a 7.5 / 10 PASS threshold and remains DEFER / lab-only.

The pass did prove that Codex can improve a flat procedural/vector base into a
more readable dockside prop prototype with better material handling, rope
fibers, barrel bands, grime, and contact shadow. It did not prove finished
commercial-safe art production at the current Newport building quality.

## Asset

| Field | Value |
| --- | --- |
| Asset id | `g418d2_rope_crate_barrel_cluster` |
| Target | rope coil + crate/barrel dockside cluster |
| Provenance | green-origin candidate |
| Visual rating | 7.4 / 10 |
| PASS gate | 7.5 / 10 plus screenshot improvement |
| Verdict | DEFER |
| Normal review | blocked |
| Final-commercial promotion | blocked |

Why it does not pass:

- The silhouette is clear and materially improved, but the cluster still reads
  slightly assembled rather than fully hand-finished.
- The rope and crate details work in isolation, but at actual game scale the
  asset is only close to the Newport row, not comfortably part of it.
- The contact shadow helps grounding, but the object still risks a pasted-on
  read beside the existing building bases.

## Tool Use

- Inkscape: authored and exported the rough silhouette base:
  `method_bakeoff/source_authored/g418d2_rope_crate_barrel_silhouette.svg`.
- Python/Pillow: authored the paint pass, alpha/crop checks, contrast checks,
  palette-distance checks, before/after board, isolated proof, and in-world
  comparison frame.
- Krita: opened the prepared sprite source and exported the projection through
  Krita CLI. The interactive kritarunner/script-runner path remained unreliable
  after the G-4.18D.1 resource-database and argument failures.
- GIMP 3.2.4: loaded the Krita export and re-exported the final PNG with
  transparency preservation and PNG metadata cleanup. GIMP completed export but
  still logged a post-export Script-Fu crash/flush warning.
- Godot + Chrome: required for the final validation and exported-build screenshot
  packet.

Tool logs:

- `method_bakeoff/reports/g418d2_krita_log.json`
- `method_bakeoff/reports/g418d2_gimp_log.json`
- `method_bakeoff/reports/g418d2_art_production_image_inspection.json`

## Proof Images

- Isolated asset proof:
  `art_pipeline/newport_green_origin/contact_sheets/g418d2_isolated_asset_proof.png`
- Before/after production proof:
  `art_pipeline/newport_green_origin/contact_sheets/g418d2_before_after_production.png`
- In-world comparison frame:
  `art_pipeline/newport_green_origin/contact_sheets/g418d2_in_world_comparison_frame.png`
- Lab capability board:
  `art_pipeline/newport_green_origin/contact_sheets/g418d2_art_production_capability_board.png`

## Failure Analysis

Was the failure due to tool access?

Partly. Inkscape, Pillow, Krita CLI, and GIMP export were usable, but the
interactive Krita script-runner/manual paint path is still not reliable on this
mini PC. GIMP also still needs timeout/crash handling after export. The tool
chain can produce and clean a PNG, but it is not yet a comfortable finished-art
painting workflow.

Was the failure due to art-direction execution?

Yes. The asset improved from rough base to polished attempt, but it still falls
short of the Newport building row's finish, edge confidence, and integrated
material depth.

Was the failure due to Codex not being able to perform finished-art production?

For this pass, yes. Codex produced a useful prototype and proof packet, but did
not demonstrate a finished commercial-safe environmental sprite that should move
into normal review.

Should future phases use Codex only for integration/validation and source final
art elsewhere?

Until a stronger art source or a reliable interactive paint workflow exists,
yes. Codex should remain responsible for provenance gates, manifests, toolchain
automation, proof boards, Godot integration, validator logic, and screenshot QA.
Finished Newport-quality prop art should come from a stronger dedicated art
source, with Codex validating and integrating it.

## Production Recommendation

Do not advance to G-4.18E on the assumption that Codex can finish green-origin
environmental sprites alone. Keep this asset lab-only, preserve it as capability
evidence, and require a stronger final-art source before any normal-review or
commercial-safe promotion.
