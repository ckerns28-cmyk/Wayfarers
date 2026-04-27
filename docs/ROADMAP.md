# Wayfarer Production Roadmap

## Production Roadmap Audit (Pre-Phase 20)

This audit was performed before beginning **Phase 20: Character Progression Foundation**.

### Current system status

| System | Status | Notes |
|---|---|---|
| Movement | working | Grid movement with interpolation, collision checks, and directional lock handling is in place. |
| Interaction | working | Proximity + click interaction manager supports NPCs and world objects. |
| Dialogue UI | working | Dialogue panel supports branch choices, number keys, click selection, and exit actions. |
| NPC dialogue trees | working | JSON-driven node trees for Edrin, Hunter Garran, Merchant Rowan with condition-based roots. |
| Quest objective system | working | Objective normalization, increment/complete, lock handling, and quest serialization exist. |
| Hunter's Request staged quest flow | working | Stage progression from wolf/pelt loop to cave relic recovery and turn-in is implemented. |
| Combat | working | Player and enemy attack cadence, damage resolution, and defeat handling are implemented. |
| Death / respawn | working | Player defeat triggers respawn flow to Hearthvale square. |
| Multi-enemy support | working | Arrays and respawn timers handle multiple wolves/bandits/mirror cave wolves. |
| Enemy variants | working | Distinct enemy groups/behaviors/loot paths exist (wolf, bandit, cave wolf). |
| Inventory | working | Registry-backed inventory supports stackable and non-stackable items. |
| Equipment | working | Weapon/armor equip/unequip and stat effect wiring are in place. |
| Armor / defense | working | Equipped armor contributes defense reduction through bonus helpers. |
| Vendor buying | working | Merchant buy flow checks coins and item registry cost. |
| Vendor selling | working | Sell flow supports per-item value and equip-safe restrictions. |
| Consumables | working | Consumables heal and clamp to max HP with quantity decrement. |
| Save/load | partially working | Save schema versioning/defaults exist; migration logic is still brittle and tightly coupled to current quest/object model. |
| Continuous outdoor regions | working | Outdoor region definitions and boundary-based zone detection are active. |
| Mirror Cave dungeon | working | Enter/exit transition flow and cave map state are implemented. |
| Dungeon chest/reward gating | working | Chest supports sealed/closed/open state with quest-stage gating and one-time reward behavior. |
| Persistent world objects | partially working | Object persistence exists via objectId state map, but serialization coupling risk remains. |
| Object states: sealed / closed / open | working | Mirror Cave chest state resolver enforces staged state transitions. |
| Walk-in cave entrance | working | Dedicated interactable cave entrance + hard transition is in place. |
| Signs / interactable objects | working | Signposts and other non-NPC world interactables are registered and persisted. |

## Completed Phases

1. Movement
2. Interaction
3. Dialogue
4. Quest system
5. Combat
6. Inventory
7. Equipment
8. Multi-enemy combat
9. Vendor selling
10. Vendor buying + consumables
11. Item-based quest
12. Enemy variants
13. Armor
14. Continuous outdoor regions
15. Mirror Cave dungeon
16. Staged quest progression
17. Dialogue UI / NPC clarity
18. NPC personality foundation
19. Persistent World Objects
20. Character Progression Foundation
21. Combat Balance / Difficulty Curve
22. Second Quest Chain / Main Story Thread

## Upcoming Phases

23. Second Outdoor Region
24. Second Dungeon / Mini-Boss
25. Skill Use Progression
26. Art Direction Replacement Pass
27. Save Schema Hardening
28. Multiplayer Architecture Planning
29. Shared World Prototype
30. MMO Systems Foundation
