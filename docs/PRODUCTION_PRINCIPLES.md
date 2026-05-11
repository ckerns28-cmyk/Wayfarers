# Wayfarer Production Principles

1. **Roadmap before reaction.**
   - Features are prioritized by roadmap phase, not by ad hoc implementation pressure.

2. **Outdoor roads are continuous world movement.**
   - Region traversal should remain uninterrupted for outdoor zones.

3. **Hard transitions are for caves, dungeons, interiors, and instances.**
   - Use explicit transition states for enclosed spaces only.

4. **Every new persistent object needs objectId/state/save support.**
   - No persistent world object ships without object identity, runtime state, and save serialization.

5. **Every new quest must define stages, objectives, rewards, and save behavior.**
   - Quest content is not complete without lifecycle and persistence definitions.

6. **Every new item must be in the item registry.**
   - Item creation outside the registry is not allowed.

7. **Every new enemy must use the enemy manager and loot table.**
   - Enemy behavior, drops, and respawn must remain manager-driven.

8. **Every system must support save/load.**
   - If data changes over time, migrations/defaults must preserve player progress.

9. **No feature is complete until regression-tested.**
   - Manual checklist coverage is required prior to phase completion.

10. **XP must have a progression purpose before major content expansion.**
    - Content scale should not outpace character growth systems.

11. **Character growth should improve survivability, combat power, or skill identity.**
    - Leveling must produce meaningful gameplay outcomes, not cosmetic counters.
