# Wayfarer Game Design Bible

## Game
**Wayfarer**

## Genre
Top-down pixel RPG / MMO-inspired vertical slice

## Core Loop
Town → Wilderness → Combat → Loot → Sell → Buy → Dungeon → Upgrade → Quest Turn-in

## Current Player Fantasy
A new wayfarer proving themselves around Hearthvale and Mirror Pond.

## Current Tone
Mythic, grounded, moody, old-school RPG.

## Design Rules
- Outdoor road travel should feel continuous.
- Hard transitions are reserved for caves, dungeons, interiors, and instances.
- NPCs should have clear identities and reasons to exist.
- NPC dialogue must be branching, data-driven where possible, and include a clear exit choice.
- NPC dialogue should react to quest state, key world interactions, and notable equipment milestones.
- Loot should connect to vendors, quests, or equipment.
- Every system should support save/load.
- Every new feature must preserve the vertical slice.

## Hearthvale NPC Roles (Phase 18)

### Edrin Vale — Story / Mystery NPC
- Quiet, observant local mystic tied to Mirror Pond.
- Handles main-story tone setting, mythic history, and Wayfarer identity.
- Should never issue Hunter's Request.
- Dialogue reacts to:
  - Mirror Pond listening progression.
  - Mirror Cave relic disturbance (opened chest).

### Hunter Garran — Combat / Wilderness NPC
- Direct and practical wilderness mentor.
- Owns **Hunter's Request** lifecycle:
  - Not Started: clear offer.
  - Active: objective/progress reminder.
  - Ready to Turn In: completion branch.
  - Completed: acknowledgement with no duplicate reward path.
- Provides repeatable flavor/advice on wolves, bandits, Eastern Woods, and survival.

### Merchant Rowan — Economy / Utility NPC
- Friendly, opportunistic trader with local knowledge.
- Vendor UI must open only through dialogue choice (**Show me your goods**).
- Provides advice and Hearthvale flavor lines.
- Dialogue reacts to notable gear milestone (player owns Iron Sword).

## Foundation-Lock Notes (Phase 17)
- Preserve the Hearthvale → Eastern Woods → Mirror Cave slice as the canonical path.
- Prioritize reliability, data safety, and readability over net-new content.
- Keep combat/inventory/vendor/quest flows interoperable with save/load at all times.

## Character Progression Rules (Phase 20)
- XP now feeds a level progression track instead of being cosmetic.
- Levels increase core survivability and combat power (Max HP, base attack bonus, base defense bonus).
- Level-up stat growth is immediate and persistent across save/load.
- Character progression is intentionally foundational: no skill tree yet.
- Future expansion: **Skill Use Progression** will layer on top of this level baseline.
