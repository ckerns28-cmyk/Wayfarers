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
  - **The Still Water** main-story progression.

## Main Story Thread (Phase 22)

### The Still Water (Edrin Vale)
- Edrin initiates the first true main-story chain and serves as the guiding voice for Wayfarer identity.
- Mirror Pond is now treated as an active mystery point, not only ambient lore.
- Quest flow:
  1) Speak with Edrin.
  2) Inspect Mirror Pond and witness delayed reflection.
  3) Return to Edrin for interpretation.
  4) Enter Mirror Cave.
  5) Recover the Echo Fragment (persistent object, no duplication).
  6) Return to Edrin for completion.
- Design intent:
  - Narrative progression first, power progression second.
  - Reward is modest and should not overshadow Hunter's Request.
  - Must stay compatible with existing Mirror Cave chest/relic flow.

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

## Outdoor Region Identity (Phase 25)

- **Hearthvale Square:** safe village hub where NPC utility, quest turn-ins, and vendors stay readable.
- **Eastern Woods:** active wilderness combat lane with regular wolf/bandit pressure and cave access.
- **North Road:** quieter road leaving Hearthvale; more open space, worn travel markers, sparse trees, and lightly ominous roadside clutter.
- North Road should stay **continuous** with Hearthvale movement (no hard transition), use existing systems/art language, and remain balanced for roughly **Level 2–5** travelers.

## Second Dungeon / Mini-Boss (Phase 26)

- **Abandoned Tollhouse:** a compact interior dungeon connected to North Road through a hard transition doorway.
- Theme: derelict roadside checkpoint reclaimed by bandits.
- Intended role: first structured humanoid combat challenge before larger dungeon ambitions.
- Layout rule: readable, small interior with one narrow entry hall, one side room, and one main chamber.
- **Rook the Tollkeeper:** first named mini-boss encounter (bandit baseline behavior, elevated stats, no complex mechanics yet).
- Mini-bosses are stronger named enemies with persistent defeat state and meaningful rewards.
- Rook rewards include the **Old Toll Key** and access to tollhouse post-boss reward flow (including Traveler's Charm support).
- Chronicle mini-boss feedback: after defeating Rook, log `Rook the Tollkeeper defeated.` then log a separate `Boss rewards:` list (XP, coins, and any item rewards) rather than folding rewards into generic bandit lines.
- Abandoned Tollhouse clear condition: set `abandonedTollhouseCleared=true` only when **both** conditions are met: (1) Rook defeated and (2) tollhouse chest opened.
- Cleared-state persistence rule: once cleared, Rook remains defeated, the chest remains open, rewards do not duplicate, and contextual objectives can surface `Abandoned Tollhouse cleared.` while near North Road/tollhouse.
- Tollhouse chest reward clarity rule: first valid open logs `Opened the tollhouse chest.`, followed by `Loot acquired:` and one line per reward. Re-interaction logs `The tollhouse chest is empty.` and grants nothing.
- Traveler's Charm behavior (Phase 26B): Charm is a trinket, grants **+1 DEF**, can be equipped from Inventory, and displays in Equipment under `Trinket`.

## Combat Balance & Difficulty Curve (Phase 21)

### Early-game combat goals
- **Level 1:** wolves are dangerous but manageable 1v1, bandits are scary, cave wolves are risky.
- **Level 2:** wolves should feel noticeably easier, bandits should be manageable with gear and consumables, cave wolves still demand respect.
- **Level 3:** player should feel clearly stronger and capable of clearing Mirror Cave with good play.
- **Level 4+:** current slice should feel safer and act as onboarding for future harder zones.

### Enemy role definitions
- **Wolf:** baseline outdoor pressure enemy. Moderate HP, moderate damage, lower XP/coin payouts.
- **Bandit:** higher-threat humanoid encounter in overworld. Hits harder than wolves and pays better XP/coins.
- **Cave Wolf:** upgraded wolf for Mirror Cave. Stronger than overworld wolves, better rewards, and tuned to make cave runs tense without immediate death loops.

### Leveling impact on combat
- Max HP, base attack bonus, and base defense bonus scale per level.
- Early breakpoints are tuned so Level 2 is reachable quickly through normal questing/combat, while Level 3 typically requires cave progress and/or additional fights.
- The slice should avoid accidental fast-tracking to Level 5 unless players intentionally grind.

### Item and economy notes
- Healing Herb is the cheap, small sustain option.
- Small Potion is the stronger, pricier combat recovery option.
- Leather Armor remains an early gear goal, with meaningful survivability impact.
- Iron Sword remains a notable damage upgrade over Rusty Sword.
- Wolf material drop/value tuning should limit runaway early sell income while still making hunting worthwhile.
