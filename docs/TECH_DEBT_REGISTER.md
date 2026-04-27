# Wayfarer Tech Debt Register (Pre-Phase 20)

| Issue | Severity | Affected system | Recommended fix phase | Notes |
|---|---|---|---|---|
| Hardcoded quest logic | high | Quest system, dialogue events | 22 (Second Quest Chain) + 27 (Save Schema Hardening) | Hunter progression is implemented with explicit stage handlers/events instead of data-driven generalized quest scripting. |
| Hardcoded NPC state | medium | NPC dialogue and world-state reactions | 18 follow-up + 22 | NPC behavior roots are condition-based but still tightly authored per character in one script blob. |
| Brittle save/load migrations | high | Save/load | 27 | Legacy compatibility paths exist, but migration behavior is manual and version-specific, increasing regression risk. |
| Map/entity coupling | high | World architecture, transitions, collision | 23 + 28 | World coordinates, interactables, enemies, and scene transitions are colocated and tightly linked. |
| Object persistence risks | medium | Persistent object system | 19 follow-up + 27 | Persistent object state map works but lacks stronger schema validation and object lifecycle tooling. |
| UI clipping risks | medium | Dialogue/vendor/HUD UI | 17 follow-up + 26 | Layout uses fixed/floating panels and mixed scaling rules that can clip at edge viewport sizes. |
| Duplicated item/combat logic | medium | Combat, inventory, rewards | 25 | Reward and stat updates are still spread across direct code paths even after introducing shared balance constants. |
| Old transition code should be removed | medium | Zone transition flow | 14/15 cleanup pass | Transition lock/timing logic has layered patches and legacy guard paths that should be simplified. |
| Placeholder visual systems | low | Rendering/art pipeline | 26 | Art stack remains a placeholder slice with mixed visual sources and temporary sprite conventions. |
| Combat balance constants are script-local | medium | Combat/economy tuning pipeline | 24 + 25 | Balance is centralized in one object but still embedded in the runtime script; external data authoring/validation is not in place yet. |
| Chronicle log compression is lightweight | low | Combat readability/UI | 24 | Duplicate-combat suppression is simple and message-based; richer batching may be needed if enemy counts increase. |
| Economy tuning is handcrafted | medium | Vendor/loot economy | 25 | Prices and drop rates are manually tuned and can drift without simulation tooling or telemetry feedback. |
