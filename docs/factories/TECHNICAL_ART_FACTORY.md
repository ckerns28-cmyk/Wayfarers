# Technical Art Factory

## Purpose

Create a technical-art review for provenance, atlas integrity, layering, contact shadows, transitions, and asset-pipeline compliance.

## Inputs

- Provenance validator output
- Atlas manifests
- Sprite rendering screenshots
- MapLayer layering changes
- Screenshot artifact list

## Procedure

1. Check active sprite provenance.
2. Check atlas region integrity.
3. Check layering and y-sort risks.
4. Check contact shadows and grounding.
5. Check that lab/deprecated assets are gated.
6. Check ground transitions for clipped artifact rectangles.

## Required Output

```markdown
## Technical Artist Review
- Status:
- Provenance:
- Atlas/Sprite Integrity:
- Layering/Grounding:
- Pipeline Compliance:
- Council Authority Contribution:
```

## Fail Fast

Fail if provenance, atlas integrity, layering, or clean-review artifact gates regress.
