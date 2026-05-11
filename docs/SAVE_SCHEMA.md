# Wayfarer Save Schema

## Current version
- `saveSchemaVersion`: **2**
- Save key: `wayfarer.save.v1`
- Backup key: `wayfarer.save.v1.backup`

## Top-level structure
- `version` (legacy content version, currently `13`)
- `saveSchemaVersion`
- `reason`
- `savedAt`
- `player`
- `quests`
- `world`
- `systems`

## Player fields (saved)
- `player.zoneId`
- `player.position.x/y`
- `player.hp`
- `player.maxHp`
- `player.level`
- `player.xp`
- `player.coins`
- `player.baseAttackBonus`
- `player.baseDefenseBonus`
- `player.inventory[]` (`itemId`, `quantity`)
- `player.equipment` (`weapon`, `armor`, `trinket`)
- `player.skills` (`swordsmanship`, `defense`, `survival` with `level` + `xp`)

## Quest fields (saved)
- `quests.questStates[]`
  - includes objective progress/current amounts/completed flags
- `quests.completedQuests[]`
- `quests.activeQuests[]`

Tracked quest IDs:
- `hunters_request`
- `the_still_water`
- `mirror_pond_listening`

## World fields (saved)
- `world.triggeredEvents[]`
- `world.stateChanges.pondAwakened`
- `world.persistentObjects`
- `world.mirrorCave`
  - `chestDiscovered`
  - `chestOpened`
  - `cleared`
- `world.tollhouse`
  - `abandonedTollhouseDiscovered`
  - `rookTollkeeperDefeated`
  - `chestState`
  - `abandonedTollhouseCleared`
- `world.hunterQuest`
  - `hunterQuestStage`
  - `hunterQuestRewardClaimed`
- `world.creatures`
  - wolves/bandits/tollhouseBandits/mirrorCaveWolves state
  - rook mini-boss state

## Systems fields (saved)
- `systems.currentObjective`
- `systems.discoveredLocations[]`
- `systems.devMode`

## Migration rules (`migrateSave`)
- Missing or old `saveSchemaVersion` is treated as legacy and migrated to schema `2`.
- Missing structures (`skills`, `equipment.trinket`, `persistentObjects`, `systems`) are initialized safely.
- Legacy object IDs are mapped to canonical IDs:
  - `tollhouse_reward_chest` -> `tollhouse_chest`
  - `echo_fragment` -> `echo_fragment_object`
  - `east_road_sign` -> `north_road_notice`
  - `mirror_pond_interaction` -> `mirror_pond`
- Existing progress is preserved whenever source fields are valid.
- Tollhouse cleared state may be inferred safely from persisted mini-boss/chest state to avoid reward duplication paths.

## Validation/repair rules (`repairSave`)
- Clamp player position to current zone map bounds.
- Clamp `hp` into `[0, maxHp]`.
- Reconcile level from XP (never below XP-implied level).
- Normalize inventory entries and drop invalid item rows.
- Ensure equipped items are valid; if equipped valid item is missing from inventory, restore one copy.
- Normalize persistent object registry and ensure canonical object entries exist.
- If a quest is marked completed, objective entries are repaired to completed.
- Repair emits development warnings instead of wiping save data.

## Persistent object ID conventions
Use stable object IDs as save keys (not display names):
- `mirror_cave_chest`
- `echo_fragment_object`
- `tollhouse_chest`
- `north_road_notice`
- `mirror_pond`
- `rook_tollkeeper_state`
- `abandoned_tollhouse_state`

## Item ID conventions
Use item IDs, including:
- `rusty_sword`
- `iron_sword`
- `leather_armor`
- `travelers_charm`
- `small_potion`
- `wolf_pelt`
- `small_fang`
- `old_toll_key`
- `echo_fragment`

## Derived stat guidance
Saved source-of-truth fields:
- level/xp
- base attack/defense
- skills/equipment/inventory

Derived on runtime (not directly trusted):
- total attack
- total defense
- trinket/skill combat bonuses
