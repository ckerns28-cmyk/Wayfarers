# Wayfarer Tech Debt Register (Pre-Phase 20)

| Issue | Severity | Affected system | Recommended fix phase | Notes |
|---|---|---|---|---|
| Hardcoded quest logic | high | Quest system, dialogue events | 22 (Second Quest Chain) + 27 (Save Schema Hardening) | Hunter progression is implemented with explicit stage handlers/events instead of data-driven generalized quest scripting. |
| Hardcoded NPC state | medium | NPC dialogue and world-state reactions | 18 follow-up + 22 | NPC behavior roots are condition-based but still tightly authored per character in one script blob. |
| Save migration coverage breadth | medium | Save/load | 28 follow-up | Core migration/repair and schema versioning are centralized, but coverage still depends on manual scenario testing for newly-added systems. |
| Map/entity coupling | high | World architecture, transitions, collision | 23 + 28 | World coordinates, interactables, enemies, and scene transitions are colocated and tightly linked. |
| Object persistence lifecycle tooling | medium | Persistent object system | 28 follow-up | Canonical object IDs + repair normalization exist, but lifecycle visualization/debug tools are still minimal. |
| Save backup retention policy | low | Save/load | 28 follow-up | Backup key is maintained before writes/migrations, but no rotation or age/size policy exists yet. |
| UI clipping risks | medium | Dialogue/vendor/HUD UI | 17 follow-up + 26 | Layout uses fixed/floating panels and mixed scaling rules that can clip at edge viewport sizes. |
| Duplicated item/combat logic | medium | Combat, inventory, rewards | 25 | Reward and stat updates are still spread across direct code paths even after introducing shared balance constants. |
| Old transition code should be removed | medium | Zone transition flow | 14/15 cleanup pass | Transition lock/timing logic has layered patches and legacy guard paths that should be simplified. |
| Placeholder visual systems | low | Rendering/art pipeline | 26 | Art stack remains a placeholder slice with mixed visual sources and temporary sprite conventions. |
| Combat balance constants are script-local | medium | Combat/economy tuning pipeline | 24 + 25 | Balance is centralized in one object but still embedded in the runtime script; external data authoring/validation is not in place yet. |
| Chronicle log compression is lightweight | low | Combat readability/UI | 24 | Duplicate-combat suppression is simple and message-based; richer batching may be needed if enemy counts increase. |
| Economy tuning is handcrafted | medium | Vendor/loot economy | 25 | Prices and drop rates are manually tuned and can drift without simulation tooling or telemetry feedback. |
