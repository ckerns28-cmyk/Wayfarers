# Wayfarer Tech Debt Register (Pre-Phase 20)

| Issue | Severity | Affected system | Recommended fix phase | Notes |
|---|---|---|---|---|
| Hardcoded quest logic | high | Quest system, dialogue events | 22 (Second Quest Chain) + 27 (Save Schema Hardening) | Hunter progression is implemented with explicit stage handlers/events instead of data-driven generalized quest scripting. |
| Hardcoded NPC state | medium | NPC dialogue and world-state reactions | 18 follow-up + 22 | NPC behavior roots are condition-based but still tightly authored per character in one script blob. |
| Brittle save/load migrations | high | Save/load | 27 | Legacy compatibility paths exist, but migration behavior is manual and version-specific, increasing regression risk. |
| Map/entity coupling | high | World architecture, transitions, collision | 23 + 28 | World coordinates, interactables, enemies, and scene transitions are colocated and tightly linked. |
| Object persistence risks | medium | Persistent object system | 19 follow-up + 27 | Persistent object state map works but lacks stronger schema validation and object lifecycle tooling. |
| UI clipping risks | medium | Dialogue/vendor/HUD UI | 17 follow-up + 26 | Layout uses fixed/floating panels and mixed scaling rules that can clip at edge viewport sizes. |
| Duplicated item/combat logic | medium | Combat, inventory, rewards | 21 + 25 | Reward and stat updates are handled in several direct code paths rather than consolidated calculators/services. |
| Old transition code should be removed | medium | Zone transition flow | 14/15 cleanup pass | Transition lock/timing logic has layered patches and legacy guard paths that should be simplified. |
| Placeholder visual systems | low | Rendering/art pipeline | 26 | Art stack remains a placeholder slice with mixed visual sources and temporary sprite conventions. |
| Progression/XP not meaningful yet | high | Progression design, balance | 20 + 21 | XP accumulates but does not drive level-based growth, build identity, or difficulty pacing yet. |
