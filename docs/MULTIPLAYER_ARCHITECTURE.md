# Wayfarer Multiplayer Architecture Plan (Phase 29)

## Scope and constraints

This document defines a **planning-only** architecture for the first multiplayer milestone.

- This is not MMO-complete scope.
- This does not add zones, quests, enemies, or new gameplay loops.
- This prepares **Phase 30: Shared World Prototype**.

## 1) Audit: current client-owned assumptions

Current implementation keeps essentially all simulation local to the browser runtime inside `worker/src/index.js`.

### Evidence summary from current code

- Player movement input, collision checks, and movement resolution are local (`keys`, `updateInput`, `tryPlayerStep`, `canMoveTo`).
- Player/enemy positions are local mutable state (`player.targetX/Y`, enemy arrays, `smoothMove`).
- Enemy spawn/respawn, AI movement, and attack cadence are local (`updateWolf`, `updateBandit`, `wolfAttack`, `banditAttack`).
- Combat and damage are local (`tryPlayerAttack`, `applyIncomingDamage`, `defeatWolf`, `defeatBandit`).
- Loot, XP, coins, and inventory mutations are local (`rollEnemyLoot`, `grantPlayerXp`, `addItemToInventory`).
- Equipment and stats are local (`equipWeapon`, `equipArmor`, `getTotalAttackDamage`, `getTotalDefenseRating`).
- Quest and object state are local with in-memory event + object registries (`questSystem`, `persistentObjects`).
- Save/load is localStorage based (`saveGame`, `loadGame`) with schema migration/repair.
- Zone transitions and zone identity are local flags and coordinate checks (`enterMirrorCave`, `exitMirrorCave`, `updateOutdoorRegionFromPosition`).

### Classification table

| System | Current owner | Multiplayer classification | Notes |
|---|---|---|---|
| Movement input capture | Client | A — can remain client-side for now | Client sends movement intent; server validates final position. |
| Player position | Client | B — must become server-authoritative | Needed for anti-teleport and shared presence consistency. |
| Enemy spawning/respawn | Client | B — must become server-authoritative | Prevents client-forced farm loops and divergence. |
| Enemy movement/AI | Client | C — hybrid temporarily | Server owns canonical tile position; client interpolates. |
| Combat resolution | Client | B — must become server-authoritative | Hit validation and outcome must be authoritative. |
| Damage calculations | Client | B — must become server-authoritative | Prevents tampered damage/defense values. |
| Loot drops | Client | B — must become server-authoritative | Prevents client-generated drops. |
| Inventory mutation | Client | B — must become server-authoritative | Client becomes request-only for mutations. |
| Equipment mutation | Client | C — hybrid temporarily | Server validates equips; client predicts UI state optionally. |
| Quest progression | Client | B — must become server-authoritative | Prevents forged completion/reward claims. |
| Object/chest state | Client | B — must become server-authoritative | Prevents duplicate chest and interaction rewards. |
| Save/load | Client localStorage | D — needs refactor before multiplayer | Must split local cache from canonical server save writes. |
| Zone transitions | Client flags/teleport functions | C — hybrid temporarily | Client requests transition; server approves and publishes zone assignment. |

## 2) Multiplayer target definition (Phase 30)

## Phase 30: Shared World Prototype

Goal:

- 2+ players can appear in the same shared **Hearthvale / North Road** world.
- Players can see each other move in real time.
- Each player keeps personal inventory/quests/progression.
- Persistent world objects remain persistent.
- No trading, parties, chat, guilds, or PvP yet.

Non-goals:

- No full economy sync between players.
- No group dungeon flow.
- No social system surface beyond nearby player visibility and name labels.

## 3) Server authority model

### Server-authoritative (required)

- Position validation (tile boundaries, collision, max speed).
- Zone membership and transition approval.
- Enemy state machine (spawn, movement, HP, cooldown, death).
- Enemy damage and player damage outcomes.
- Loot generation and reward grants.
- Persistent object state (chests/sign/object toggles).
- Dungeon cleared flags and anti-duplicate reward rules.
- Canonical save writes.

### Client-authoritative (presentation-only)

- Rendering and camera.
- HUD/UI composition.
- Input capture.
- Animation interpolation and local VFX.
- Optional short-lived prediction for responsiveness.

### Temporary hybrid allowances

- Client sends movement intent at input cadence; server rebroadcasts accepted transforms.
- Client can render optimistic movement between authoritative updates.
- Client can display immediate swing animation while waiting for combat result event.

## 4) Cloudflare architecture recommendation (simplest viable)

Current deployment already uses a Cloudflare Worker entrypoint and static assets in Wrangler config.

### Recommended Phase 30 topology

1. **Edge Worker (HTTP/WebSocket router)**
   - Handles auth/session bootstrap (anonymous player token initially).
   - Routes zone socket connections to zone Durable Objects.
   - Exposes save/profile read/write API.

2. **Durable Object: `ZoneRoomDO` (one per active zone instance)**
   - Authoritative runtime state for shared zones (player presence, positions, enemy snapshots for shared spaces).
   - Owns broadcast stream (`player_joined`, `player_left`, `player_position`, etc.).
   - Applies server-side movement validation and rate limiting.

3. **Durable Object: `PlayerSessionDO` (optional in Phase 30, recommended by Phase 31)**
   - Tracks active connection(s), reconnection grace window, idempotency tokens.
   - Helps prevent duplicate join/disconnect races.

4. **D1 as canonical persistence**
   - Tables for player profile/save blobs, quest state, inventory/equipment, persistent object state.
   - Transactional writes for reward/idempotency-sensitive actions.

5. **KV for read-mostly config/cache**
   - Optional: content snapshot cache, message-of-the-day, zone metadata.
   - Not canonical for mutable transactional gameplay state.

6. **R2 optional (not required for Phase 30)**
   - For long-lived telemetry dumps, replay logs, or backup snapshots.

### Why this is the simplest viable option

- Durable Objects are a natural match for zone-local authoritative state + websocket fanout.
- D1 provides SQL transactions needed for anti-duplication guarantees.
- Worker stays thin as ingress/router.

## 5) World instancing rules

### Shared (Phase 30)

- Hearthvale Square
- North Road
- Eastern Woods

### Private / solo-instance (Phase 30)

- Mirror Cave
- Abandoned Tollhouse

### Rationale

Dungeon content currently mixes personal quest gates, chest reward states, and clear flags; keeping dungeons private avoids premature shared-loot conflict rules.

### Future path (post-Phase 30)

- Add party-scoped dungeon instances (`instanceType=party`, `instanceId=partyId+zoneId`).
- Add lockstep reward rules (need/greed or per-player instanced loot).

## 6) Multiplayer-ready player data model

Use a canonical server profile object (shape shown conceptually):

```ts
interface PlayerProfile {
  playerId: string;
  displayName: string;
  currentZone: string;
  position: { x: number; y: number; facing?: "up"|"down"|"left"|"right" };
  level: number;
  xp: number;
  skills: Record<string, { level: number; xp: number }>;
  inventory: Array<{ itemId: string; quantity: number }>;
  equipment: { weapon: string|null; armor: string|null; trinket: string|null };
  questState: unknown;
  persistentObjectState: Record<string, unknown>;
  lastSavedAt: string; // ISO8601
}
```

Design notes:

- `playerId` must be immutable and globally unique.
- `displayName` can be mutable with validation.
- Keep auth decoupled by adding `authProvider`/`accountId` later without breaking save shape.

## 7) Network message types (Phase 30)

### Client → Server

- `join_zone`
- `leave_zone`
- `move_input`
- `position_ack` (optional)
- `interact_object`
- `attack`
- `use_item`
- `save_request`
- `ping`

### Server → Client

- `zone_snapshot`
- `player_joined`
- `player_left`
- `player_position`
- `entity_spawned`
- `entity_updated`
- `combat_result`
- `loot_result`
- `object_state_updated`
- `save_result`
- `error`
- `reject_action`

### Envelope recommendation

```json
{
  "type": "player_position",
  "seq": 1842,
  "serverTime": 1710000000000,
  "payload": {}
}
```

Use monotonic `seq` for reconciliation and debugging.

## 8) Anti-cheat and trust boundaries

Client **must never be trusted** to decide:

- Item grants or quantity changes.
- XP, coins, level, or skill promotion.
- Enemy kill confirmation.
- Chest reward issuance.
- Quest completion state.
- Arbitrary position setting.
- Equipment stat authority.

Client role:

- Send intent (`move_input`, `attack`, `interact_object`, etc.).
- Render authoritative results from server.

Server role:

- Validate preconditions and cooldowns.
- Apply mutation through canonical state layer.
- Emit outcomes to requesting player + observers.

## 9) Refactors required before Phase 30

| Refactor | Priority | Why |
|---|---|---|
| Extract deterministic state mutation layer from render/input loop | **Blocker** | Current update/draw/input are tightly interleaved in one script; server-side reuse is not viable yet. |
| Separate canonical game state from UI/HUD state | **Blocker** | Many mutations trigger direct UI/save side effects; needs clean domain layer boundaries. |
| Normalize entity IDs across players/enemies/world objects | **Blocker** | Needed for network events, snapshots, and reconciliation. |
| Isolate combat formulas/outcome resolver into pure functions | **Blocker** | Required for server-authoritative outcomes and shared tests. |
| Isolate inventory/equipment mutation APIs with validation | **Blocker** | Needed so all item/equip mutations pass one authority path. |
| Isolate quest mutation APIs/event handlers | **Recommended before multiplayer** | Current quest events are broad and local; should become explicit server commands. |
| Replace direct localStorage writes with persistence adapter | **Recommended before multiplayer** | Enables server persistence without breaking offline regression workflows. |
| Build zone entity registry abstraction | **Recommended before multiplayer** | Simplifies snapshot + diff messaging. |
| Remove remaining direct DOM coupling in core logic | **Recommended before multiplayer** | Needed to run logic headlessly in DO/runtime tests. |
| Prediction/reconciliation smoothing | **Can wait** | Not required for basic Phase 30 proof. |
| Party/chat/social channel architecture | **Can wait** | Explicitly out of Phase 30 scope. |

## 10) Phase 30 concrete implementation scope

### In scope

- Shared presence in Hearthvale/North Road/Eastern Woods.
- Two+ players visible simultaneously.
- Basic movement synchronization.
- Join/leave events and labels.
- Server-backed zone state in Durable Object.
- Persist + restore last safe position.

### Out of scope

- Trading, parties, guilds, chat.
- PvP.
- Shared loot arbitration (unless strictly required for bug prevention).
- Shared dungeon instances.

### Acceptance criteria

- Open two browser sessions.
- Both players appear in Hearthvale.
- Moving Player A updates on Player B screen with acceptable latency.
- Disconnect/rejoin restores safe position from server profile.
- Existing single-player loops still function when run in local solo mode.

## 11) Delivery checklist for this planning phase

- `docs/MULTIPLAYER_ARCHITECTURE.md` (this document).
- Roadmap updated for Phase 29 planning completion and Phase 30 scope.
- Tech debt register updated with multiplayer blockers.
- Regression checklist updated with Phase 30 multiplayer checks.

## 12) Final recommendation

### Readiness

**Partially ready** for Phase 30. Content systems are mature enough, but architectural boundaries are not yet multiplayer-safe.

### Required first refactors

1. Extract authoritative domain mutation layer (combat/inventory/quest/object state).
2. Introduce persistence adapter boundary (local + server backends).
3. Introduce zone/entity registry and ID normalization.

### Highest-risk systems

1. Save/load and reward idempotency during reconnects.
2. Quest/object reward duplication under concurrent interactions.
3. Combat consistency when client prediction diverges from server.
4. Tight coupling between simulation and DOM/UI updates.

### Recommended first implementation task for Phase 30

Implement **`ZoneRoomDO` + websocket presence and authoritative movement validation only** (no combat sync yet), then prove two-session shared Hearthvale movement before expanding to combat/object authority.
