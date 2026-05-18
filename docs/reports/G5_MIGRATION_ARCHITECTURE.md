# G-5 Migration Architecture

Generated: 2026-05-18

## Status

- Phase: `G-5 Migration Architecture`
- Starting synced main commit: `fcfca18c17d4d7b0de05f31d82fba7e18ceca811`
- Branch: `codex/g-5-migration-architecture`
- Phase type: planning architecture, not gameplay porting
- Production route change: no
- JavaScript Worker route: remains the production/reference route until G-6 explicitly changes cutover policy
- Godot route: remains the Newport browser-review/runtime track
- Council verdict: `COUNCIL_PASS_READY_FOR_PR`
- Human review required for this planning pass: no
- Next recommended roadmap phase after this PR: `G-6 Production Cutover Planning`

## Why G-5 Exists

The JavaScript Worker still contains the mature vertical-slice gameplay route: movement, regions, interactions, dialogue, quests, combat, loot, inventory, equipment, vendor flow, consumables, save/load, persistent objects, dungeons, runtime QA, and Cloudflare deployment. Godot now has an accepted Newport visual/runtime foundation, but it does not yet own those gameplay systems.

G-5 is the architecture bridge. It defines how systems move from the Worker into Godot without copying a 15,000-line browser bundle into scene scripts, losing save compatibility, or replacing the production route before G-6 cutover planning.

## Source Evidence

| Source | Evidence Used |
| --- | --- |
| `docs/WAYFARER_GODOT_ROADMAP.md` | G-5 is planning-only and starts only after the G-4.22 visual foundation gate. |
| `docs/SYSTEMS_OVERVIEW.md` | Current gameplay systems and invariants to preserve. |
| `docs/SAVE_SCHEMA.md` | Save schema v2, fields, migration, repair, and id conventions. |
| `docs/MULTIPLAYER_ARCHITECTURE.md` | Future server-authoritative boundaries and Cloudflare Worker plus Durable Object plus D1 direction. |
| `docs/GAME_DESIGN_BIBLE.md` | Core loop, tone, progression, quest, combat, reward, and NPC design rules. |
| `wayfarer_v7_github_ready/worker/src/index.js` | Current JS source of truth for gameplay behavior and QA. |
| `wayfarer_godot_vertical_slice/scenes/Main.gd` | Godot Newport scene assembly, review toggles, and building placement. |
| `wayfarer_godot_vertical_slice/scenes/player/Player.gd` | Godot player movement, camera, prompt, visual state. |
| `wayfarer_godot_vertical_slice/scenes/ui/HUD.gd` | Godot HUD, dialogue, metadata/no-HUD review mode. |
| `wayfarer_godot_vertical_slice/scripts/NewportTownBlueprint.gd` | Godot Newport world layout source. |

## Non-Negotiable Rules

- Do not port gameplay by pasting Worker code into Godot scene scripts.
- Do not replace the JavaScript Worker route during G-5.
- Do not treat Godot art readiness as gameplay parity.
- Do not migrate save/load after combat, quests, or rewards. Save compatibility comes first.
- Do not allow UI/HUD code to own canonical gameplay mutations.
- Do not make multiplayer trust promises until single-player domain services and persistence adapters exist.
- Every migrated gameplay system needs contracts, fixtures, validators, and screenshot/council proof when player-facing.

## Target Godot Boundaries

| Boundary | Responsibility |
| --- | --- |
| `GameState` | Canonical player, quest, world, creature, inventory, progression, and systems state. |
| `SaveService` | Save schema migration, repair, validation, local adapter, future server adapter, and compatibility export. |
| `ZoneService` | Zone ids, region membership, transitions, safe spawns, camera bounds, and future network zone assignment. |
| `InteractionService` | Proximity/click/key interactions against stable entity ids. |
| `DialogueQuestService` | Dialogue roots, conditions, quest lifecycle, objectives, and reward commands. |
| `InventoryEconomyService` | Item registry, inventory stacking, equipment, vendor pricing, buy/sell, and consumables. |
| `CombatService` | Combat formulas, enemy state, cooldowns, defeat, loot, XP, skill XP, and outcome events. |
| `EntityRegistry` | Stable ids for players, NPCs, enemies, world objects, doors, chests, signs, and persistent objects. |
| `PresentationAdapters` | Sprites, animations, HUD, Chronicle, prompts, toasts, floating text, VFX, camera, and screenshots. |
| `MigrationQA` | Golden fixtures, parity validators, save compatibility, visual evidence, and council reports. |

## Migration System Inventory

| System | Current JS Owner | Current Godot Surface | G-5 Owner | Order | Primary Risk |
| --- | --- | --- | --- | --- | --- |
| Movement, camera, zone | Worker grid/interpolation/region logic | `Player.gd`, `Main.gd`, `CollisionNavigationLayer.gd` | `ZoneService` | G-5.2 | Grid-to-continuous semantics can change reachability and combat range. |
| Interaction, dialogue, quest | `InteractionManager`, `DialogueFramework`, `QuestStateSystem` | `EdrinVale.gd`, prompt, HUD dialogue | `DialogueQuestService` | G-5.4 | Hardcoded quest/NPC paths can duplicate rewards or drop branch reactivity. |
| Inventory, equipment, economy | `ITEM_REGISTRY`, vendor, consumables, stacking | HUD placeholders only | `InventoryEconomyService` | G-5.5 | Mutation side effects can drift from save and quest objectives. |
| Combat, enemies, loot, progression | Enemy loops, damage, loot, XP, skills | Not ported | `CombatService` | G-5.6 | Client-authoritative formulas must become pure and server-reusable later. |
| Save/load/persistence | `migrateSave`, `repairSave`, `saveGame`, `loadGame`, localStorage | Not ported | `SaveService` | G-5.3 | Legacy player progress must be preserved before any cutover. |
| World objects/dungeons | Persistent ids, Mirror Cave, Tollhouse, Rook, chests | Not ported | `EntityRegistry` plus `ZoneService` | G-5.7 | Reward duplication and cleared-state loss are player-trust failures. |
| UI/HUD/Chronicle feedback | DOM HUD, sidebar, dialogue, vendor, toasts, Chronicle | `HUD.gd` | `PresentationAdapters` | G-5.8 | Player-facing feedback must remain explicit and screenshot-validated. |
| Deployment/QA/multiplayer boundary | Worker route, runtime QA, Wrangler, future DO/D1 plan | Godot validators and screenshot capture | `MigrationQA` | G-5.9 | Cutover before parity and rollback criteria would violate roadmap safety. |

## Migration Sequence

1. `G-5.1 Contract Extraction And Golden Fixtures`

   Extract Worker behavior contracts and golden fixtures for save payloads, movement samples, quest states, inventory/equipment mutations, combat formulas, object states, and UI feedback events. No Godot gameplay porting starts before this package exists.

2. `G-5.2 Godot State Kernel Skeleton`

   Add Godot service boundaries and data models: `GameState`, `EntityRegistry`, `ZoneService`, and `MigrationQA`. The scene should still play as Newport, but gameplay authority begins moving out of node scripts.

3. `G-5.3 Save Compatibility Bridge`

   Teach Godot to read, migrate, repair, preserve, and export Wayfarer save schema v2. Golden Worker saves must round-trip without losing level, HP, XP, inventory, equipment, quests, persistent objects, dungeon state, or systems fields.

4. `G-5.4 Interaction, Dialogue, Quest Foundation`

   Migrate NPC/object interaction, dialogue branch conditions, quest lifecycle, objectives, and reward commands. Hunter's Request and The Still Water become contract fixtures before new quest content is added.

5. `G-5.5 Inventory, Equipment, Economy Foundation`

   Migrate item registry, stacking, equip rules, vendor buy/sell, consumables, HP caps, Survival XP, and save persistence.

6. `G-5.6 Combat, Enemy, Loot Foundation`

   Migrate combat formulas, wolf/bandit/cave-wolf/Rook state, cooldowns, defeat, loot, XP, skills, respawn, and feedback events through pure outcome services.

7. `G-5.7 Dungeon Persistent Object Foundation`

   Migrate Mirror Cave, Abandoned Tollhouse, chest states, Echo Fragment, Rook defeat, cleared-state persistence, and transition safety.

8. `G-5.8 Player-Facing Feedback Integration`

   Bind gameplay domain events to Godot HUD, dialogue, Chronicle, toasts, floating text, animations, and screenshot-validated UI proof.

9. `G-5.9 Parity And Cutover Readiness Evidence`

   Produce side-by-side JS/Godot parity validation, performance evidence, visual evidence, gap register, and G-6 inputs.

## Save Compatibility Policy

Godot must treat `docs/SAVE_SCHEMA.md` as a compatibility contract, not a suggestion. The migration path is:

1. Import Worker schema v2 payloads.
2. Apply equivalent migration and repair behavior.
3. Preserve unknown/future-safe data where possible.
4. Reject or quarantine invalid saves without wiping richer progress.
5. Export payloads that remain understandable by the Worker until G-6 decides otherwise.

The first gameplay migration implementation after G-5 must create golden save fixtures before changing any reward, quest, combat, inventory, or dungeon behavior.

## Multiplayer Boundary Policy

G-5 does not implement multiplayer. It protects the future multiplayer plan by insisting that Godot gameplay systems be service-owned and deterministic enough to move under server authority later.

The future Cloudflare shape remains:

- Worker as ingress/router.
- Durable Objects for zone-local authority.
- D1 for canonical persistence.
- Client rendering and input capture as presentation.

Single-player Godot migration must not make this harder by baking canonical mutations into sprites, HUD panels, animations, or local-only scene state.

## QA Gates For Future Migration PRs

Every gameplay migration PR must include:

- Source behavior inventory from the Worker.
- Data contract or fixture for the system being migrated.
- Godot service/module implementation.
- Save/load compatibility where state is affected.
- Headless validator or parity test.
- Godot vertical slice validation.
- Screenshot proof for player-facing UI, world, combat, dialogue, feedback, or visual changes.
- Agent Council report separating technical pass from design/player-facing acceptance.
- PR/merge evidence before the next migration slice begins.

## Current G-5 Deliverables

- Architecture report: `docs/reports/G5_MIGRATION_ARCHITECTURE.md`
- Machine-readable inventory: `docs/reports/G5_MIGRATION_ARCHITECTURE.json`
- Validator: `wayfarer_godot_vertical_slice/tools/validate_g5_migration_architecture.py`
- Council report: `docs/reports/G5_MIGRATION_ARCHITECTURE_AGENT_COUNCIL_REPORT.md`
- Roadmap update: `docs/WAYFARER_GODOT_ROADMAP.md`
- Regression checklist update: `docs/REGRESSION_TEST_CHECKLIST.md`
- Tech debt register update: `docs/TECH_DEBT_REGISTER.md`

## Recommendation

Pass G-5 as a planning architecture phase once the validator and existing Godot/pre-G-5 gates pass. Then proceed to `G-6 Production Cutover Planning` on a fresh synced branch. G-6 must define hosting ownership, rollback, save compatibility policy, remote checks, and replacement criteria before any production route is changed.
