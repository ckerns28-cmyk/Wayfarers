# Wayfarer Systems Overview

This document summarizes the current vertical-slice systems and what must remain stable.

## Player state
- **What it does:** Stores core player progression and runtime combat state.
- **Important state fields:** `player.hp`, `player.maxHp`, `player.xp`, `player.coins`, `player.inventory`, `player.equipment`, tile/px coordinates, movement/combat impulse fields.
- **Must not break:** Health bounds, coin/xp persistence, equipment effects, inventory integrity.

## Movement
- **What it does:** Grid-based tile movement with smooth interpolation and directional input.
- **Important state fields:** `player.targetX/targetY`, `player.px/py`, `player.moving`, `zoneTransitionLockedUntil`, key state sets.
- **Must not break:** Movement collision checks, directional blocking during transitions, stable movement in all zones.

## Camera
- **What it does:** Centers viewport around player while clamping to world bounds.
- **Important state fields:** `VIEW_TILES_X`, `VIEW_TILES_Y`, camera tile offsets.
- **Must not break:** Correct visible region boundaries in overworld and Mirror Cave.

## Regions
- **What it does:** Maintains continuous outdoor regions (Hearthvale Square / Eastern Woods) and zone naming.
- **Important state fields:** `OUTDOOR_REGION_DEFS`, `currentZoneId`, `lastLoggedZoneEntryId`.
- **Must not break:** Outdoor traversal continuity and zone detection.

## Dungeon transitions
- **What it does:** Executes hard transition flow for Mirror Cave enter/exit.
- **Important state fields:** `isInMirrorCave`, `transitionState`, `zoneTransitionLockedUntil`.
- **Must not break:** Transition timing, spawn/return tiles, no stuck-transition states.

## NPC interaction
- **What it does:** Registers interactable NPCs and world objects in range-based interaction manager.
- **Important state fields:** `interactionManager.interactables`, NPC coordinates.
- **Must not break:** E key and click interactions for Edrin Vale, Hunter Garran, Merchant Rowan, cave entrance/exit/chest.

## Dialogue states
- **What it does:** Runs node-based dialogue sessions and emits progression events.
- **Important state fields:** dialogue JSON nodes, `dialogueSystem.activeSession`, event hooks.
- **Must not break:** Dialogue branching, quest activation/report events, choice input.

## Quest states
- **What it does:** Tracks quest lifecycle (Not Started, Active, Ready To Turn In, Completed).
- **Important state fields:** `QuestState`, per-quest `state`, `progress`, objective arrays.
- **Must not break:** State transitions, completion gating, no duplicate completion rewards.

## Objective tracking
- **What it does:** Advances objective counters and completion flags from combat/interactions.
- **Important state fields:** objective `currentAmount`, `requiredAmount`, `completed`, lock rules for gated objectives.
- **Must not break:** Kill/item/interaction updates and objective completion ordering.

## Combat
- **What it does:** Handles player attack cadence, enemy attacks, damage, defeat, and respawn.
- **Important state fields:** cooldown timestamps, attack ranges, HP, recoil/lunge fields.
- **Must not break:** Hit detection, death/respawn, damage scaling from equipment.

## Enemy manager
- **What it does:** Owns wolf/bandit/cave-wolf behavior loops, aggro movement, and respawns.
- **Important state fields:** spawn tables, hostile arrays, respawn timers, last decision/attack timestamps.
- **Must not break:** Multi-enemy handling, respawn consistency, per-zone active hostile filtering.

## Loot tables
- **What it does:** Defines weighted drops and item quantities per enemy type.
- **Important state fields:** `WOLF_LOOT_TABLE`, `BANDIT_LOOT_TABLE`, item registry lookups.
- **Must not break:** Drop validity, stack-safe inventory insertion.

## Inventory
- **What it does:** Stores stacked/non-stacked items, supports add/remove/quantity queries.
- **Important state fields:** `player.inventory`, `ITEM_REGISTRY`, normalization helpers.
- **Must not break:** Stacking behavior, starter weapon safety, save/load compatibility.

## Equipment
- **What it does:** Applies weapon/armor bonuses and equips from inventory.
- **Important state fields:** `player.equipment.weapon/armor/trinket`, bonus helpers.
- **Must not break:** Weapon/armor bonus calculations, equipped-item constraints, no invalid equipped IDs.

## Vendor
- **What it does:** Handles buy/sell UI and transaction logic for Merchant Rowan.
- **Important state fields:** `VENDOR_BUY_INVENTORY`, buy/sell costs, coin updates.
- **Must not break:** Coin accounting, equip-safe selling constraints, vendor UI click behavior.

## Consumables
- **What it does:** Uses healing consumables from inventory and restores HP.
- **Important state fields:** item `type`, `healAmount`, player HP.
- **Must not break:** HP cap enforcement, quantity decrement, save update after use.

## Save/load
- **What it does:** Persists player, quest, world flags, and creature state to localStorage.
- **Important state fields:** `SAVE_KEY`, `saveSchemaVersion`, save `version`, player/world/quest payloads.
- **Must not break:** Backward loading of older saves, safe default initialization for missing fields, no wipe on partial legacy data.

## Persistent flags
- **What it does:** Tracks one-time world state such as pond awakening and cave chest open state.
- **Important state fields:** `worldEvents`, `worldTriggeredEvents`, `mirrorCave.chest.opened`, `mirrorCave.cleared`.
- **Must not break:** One-time world event behavior and chest persistence across saves.

## Debug-only developer tools
- **What it does:** Exposes non-production helper keybinds for reset/recovery workflows.
- **Important controls:** `F6` heal full, `F7/F8/F9` teleport, `F10` reset quest, `Shift+F10` reset full save.
- **Must not break:** Normal gameplay input paths or shipped progression behavior.
