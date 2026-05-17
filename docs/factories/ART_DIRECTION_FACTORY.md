# Art Direction Factory

## Purpose

Create an art-direction review for visual cohesion, sprite quality, grounding, street/terrain language, and the Newport 8.5+/10 bar.

## Inputs

- Clean screenshots
- Sprite/provenance notes
- Ground/street plan
- Known visual issues
- Art direction docs

## Procedure

1. Review ground and road material unity.
2. Review building grounding and street composition.
3. Review prop function.
4. Review lighting/readability.
5. Identify whether legacy proof/debug artifacts appear.
6. Decide whether the scene approaches the phase target.

## Required Output

```markdown
## Art Director Review
- Visual Review Status: PASS / FAIL / NEEDS_HUMAN_REVIEW
- Ground/Street Cohesion:
- Building/Sprite Cohesion:
- Composition:
- 8.5+/10 Gap:
- Recommendation for Chris:
```

## Fail Fast

Fail Newport passes with mismatched road layers, clipped transparent rectangles, floating buildings, or prop clutter masking layout problems.
