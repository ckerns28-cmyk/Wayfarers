# Wayfarer Art Direction

## Phase 23 Lock Statement

This document defines the official creative and visual standards for Wayfarer as of **Phase 23 — Creative Direction / Art Direction Lock**. It is the baseline for all environment, character, UI, and interaction visuals until the full production replacement pass.

## Game Visual Target

Wayfarer targets a:

- top-down pixel RPG presentation
- classic MMORPG readability standards
- clarity inspired by late-1990s to early-2000s RPGs
- moody mythic fantasy tone
- grounded presentation (not cartoonish)
- mysterious atmosphere that remains playable at all times

## Visual Pillars

1. **Readable silhouettes**
   - Every gameplay-relevant actor (player, NPC, enemy, interactable) must be identifiable by shape first, color second.
2. **Consistent tile scale**
   - World objects must conform to a fixed tile and sprite scale grid.
3. **Consistent lighting direction**
   - One implied world light direction for all assets.
4. **Grounded medieval-fantasy materials**
   - Wood, stone, cloth, leather, iron, earth, moss; avoid glossy high-fantasy surfaces.
5. **Restrained color palette**
   - Mid-saturation, readable values, sparse high-chroma accents.
6. **Clear interaction targets**
   - Interactable objects should be easy to locate without looking like UI widgets in-world.
7. **Atmosphere without readability loss**
   - Mood is important, but gameplay readability is non-negotiable.

## Pixel Scale Rules

### Baseline Scale

- **Tile size:** 32x32 pixels (authoring baseline)
- **Gameplay zoom rule:** all combat and interaction silhouettes must remain readable at standard camera distance

### Sprite and Object Footprints

- **Player sprite footprint:** 1x1 tile collision footprint; sprite art may overhang vertically (up to ~1.5 tiles visual height)
- **NPC footprint:** 1x1 tile collision footprint with stronger contrast separation from terrain
- **Enemy footprint:**
  - Wolves: 1x1 tile
  - Bandits: 1x1 tile
  - Future elite enemies may exceed 1x1 but must preserve clear contact and hit readability
- **Prop footprint:**
  - Small props: 1x1 tile
  - Medium props: 1x2 or 2x1 tiles
  - Large props/landmarks: 2x2+ tiles, with collision clearly implied by silhouette
- **Building tile dimensions:** modular multiples of 32 (e.g., 3x3, 4x3, 5x4 tile footprints)
- **Cave/dungeon tile dimensions:** 32x32 tile grid, using modular wall/floor transitions in full-tile increments

### Readability Rules

- Characters must remain readable at gameplay zoom.
- NPCs must not blend into terrain values.
- Enemies must be identifiable by silhouette before animation.
- Interactable objects must stand out subtly (value/outline/shape cue), without neon/high-saturation overuse.

## Color and Lighting Direction

### Palette Direction

- Overall palette is muted, natural, and value-structured.
- Use accent colors intentionally for faction, quest ownership, danger, or narrative focus.

### Regional / System Color Guidance

- **Grass tones:** desaturated olive/forest greens; avoid bright lime except in rare magical areas
- **Dirt/path tones:** warm browns and dusty umbers; roads should read as navigational anchors
- **Stone/cave tones:** cool grays, slate blues, and mineral desaturation
- **Water tones:** deep desaturated blue-green; shallow edges slightly lighter but never tropical
- **Building tones:** weathered wood browns, soot-muted roofs, pale plaster highlights
- **Enemy colors:** higher local contrast than terrain; threat readability over realism when in conflict
- **NPC accent colors:** restrained but role-coded accents (scarves, trims, tools, packs)
- **UI colors:** neutral dark backplates + light text + selective gold/amber/teal accents for importance

### Lighting Rule (Locked)

- **Implied light source direction: top-left**.
- **Shadow fall direction: down-right**.
- This rule applies to characters, props, buildings, terrain details, and UI bevel styling where relevant.
- Exceptions (e.g., emissive magical effects) must not break base form readability.

## Environment Identity Standards

### Hearthvale (Safe Hub)

- Old village, lived-in, humble, safe-feeling.
- Warm window light at dusk/night.
- Roads must be legible movement guides.
- Human-scale structures; no monumental architecture.
- Clutter should suggest life (tools, crates, signs) without blocking movement readability.

### Eastern Woods

- Darker, wilder, less safe than Hearthvale.
- Denser foliage and uneven ground variation.
- More natural clutter (roots, brush, fallen timber cues).
- Navigable paths remain readable despite increased visual density.

### Mirror Pond

- Still, reflective, mythic.
- Subtly unnatural compared to nearby wilderness.
- Composition should imply narrative importance without explicit UI dependence.
- Effects must remain understated and readable.

### Mirror Cave

- Enclosed, colder, ancient, dangerous.
- Clear visual break from outdoor palette/material treatment.
- Stronger shadow masses and constrained sightline feeling.
- Traversal routes and interactables remain readable in low-key values.

## Character Identity Standards

### Player / Wayfarer

- Readable adventurer silhouette (travel-ready, practical gear).
- Appears capable but not legendary yet.
- Future gear progression must be visually layerable (armor/weapon overlays later).

### Edrin Vale

- Story/mystic NPC silhouette.
- Calm, strange, observant impression.
- Distinct from merchants/hunters via shape language and restrained symbolic accents.

### Hunter Garran

- Practical wilderness silhouette.
- Rugged and survival-focused.
- Combat utility cues (tool belt, cloak, practical weapon posture).

### Merchant Rowan

- Approachability and commerce readability first.
- Clearly merchant-coded through posture/accessories/stall association.
- Warm but grounded presentation.

### Wolves

- Fast natural threat silhouette.
- Lean shape and low posture for immediate threat recognition.

### Bandits

- Humanoid danger class separate from villagers/NPCs.
- Rougher silhouette language, more hostile posture, danger-first readability.

## Interaction Readability Rules

- Cave entrances should be **walk-in triggers** with clear spatial framing.
- Interiors/dungeons should use **hard transitions** (intentional state change).
- Outdoor roads use **continuous world movement**.
- Chests remain visible after opening.
- Opened chests must use a distinct open-state object.
- Sealed objects must explain seal condition in interaction text.
- NPC quest ownership must be clear from labels/dialogue cues.
- Signs and props must reinforce navigation, place identity, and interaction discoverability.

## Current Visual Gap Analysis

### What Current Visuals Satisfy

- Core top-down readability and movement clarity.
- Distinct region separation (outdoor vs cave) at a functional level.
- Basic interactable discoverability is in place.
- Existing vertical slice visuals support full system testing and quest progression.

### What Current Visuals Fail

- Character/NPC/enemy sprite identity is not yet production-distinct enough.
- Material consistency (wood/stone/ground/water) is uneven.
- Lighting direction consistency is incomplete across mixed placeholder assets.
- UI visual hierarchy is functional but lacks cohesive presentation language.
- Some terrain and prop assets still read as placeholder rather than authored world identity.

### Acceptable as Temporary

- Functional placeholder tiles that preserve collision and route readability.
- Temporary prop variants where silhouette and interaction remain clear.
- Interim UI framing where legibility is intact.

### Must Replace Before Public Demo

- Player, key NPC, wolf, and bandit sprite sets.
- Hearthvale building tile cohesion pass.
- Grass/path/water/shoreline baseline set.
- Cave tile set readability and mood pass.
- Chest open/closed/sealed visual states.
- UI frame set and panel consistency pass.

### Can Wait Until Phase 31

- Full armor/weapon overlay suite.
- Broad enemy visual variant expansion.
- High-volume environmental prop set enrichment.
- Advanced effects, emotes, and customization layers.

## Phase 24 Recommendation (Execution Focus)

Phase 24 should prioritize **UX presentation polish and interaction clarity before content expansion**:

1. Unify all core UI panel spacing, typography, and framing.
2. Ensure no modal or panel clips at common gameplay resolutions.
3. Standardize quest/objective/chronicle messaging cadence and priority.
4. Improve interaction prompt clarity for NPCs, doors, cave entrances, and chest states.
5. Validate readability with a quick pass checklist on Hearthvale, Eastern Woods, and Mirror Cave.
