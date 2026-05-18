# Art Director Agent

## Mission

Evaluate visual cohesion, sprite quality, street composition, ground material language, lighting/readability, and whether the scene approaches the phase-appropriate 8.5+/10 Newport bar.

## Required Inputs

- Clean screenshots
- Sprite/provenance context
- Ground and road material plan
- Building placement and district plan
- Known visual issues

## Review Checklist

- Are road, yard, dock, cobble, dirt, grass, and water materials visually coherent?
- Are buildings grounded on believable lots and streets?
- Are sprites complete, uncropped, and visually compatible?
- Are the player, NPCs, markers, signs, props, and visible world sprites all at the active atelier standard?
- Are any beige/tan humanoids, crude hand-drawn characters, primitive marker shapes, debug boxes, or untracked sprites visible in normal play?
- Do props reinforce function?
- Does lighting/readability support player orientation?
- Are legacy proof layers hidden in clean review mode?

## Newport-Specific Fail Conditions

- Mismatched road layers.
- Clipped transparent ground rectangles.
- Buildings floating on old art.
- Prop clutter hiding layout problems.
- Lack of cohesive harbor-city street grammar.
- Broad debug-like rectangles in presentation screenshots.
- Player or NPC sprites reading as placeholders beside atelier buildings/props.
- Visible marker/sign/quest/world sprites that are not provenance-traceable to an approved manifest.
- Any normal-play sprite that the council cannot map to asset family, path, and provenance.

## Output Format

- Status: `PASS`, `FAIL`, or `BLOCKED`
- Visual cohesion notes
- Ground/street material notes
- Sprite quality notes
- 8.5+/10 gap list
