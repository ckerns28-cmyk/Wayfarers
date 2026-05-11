# Phase 32AA.2F — Dense Town Depth Sorting and Occlusion Validation

1. Files changed
- `worker/src/index.js`
- `docs/PHASE_32AA_2F_CODEX_REPORT.md`

2. Phase 33 status
- Phase 33 was **not** started. Work is scoped to Phase 32AA.2F render/depth behavior only.

3. Asset status
- No new assets were added.

4. Render-order logic before fix
- Overworld rendering drew buildings in `world.buildings.forEach(...)` sequence, then drew `propsBehind`, then all actors (NPCs, enemies, player) afterward.
- This meant actor-vs-building occlusion was not based on per-object feet/base Y and could produce wrong overlap in dense layouts.

5. New/confirmed depth-sort logic
- A unified `renderQueue` now includes buildings, behind-entity props, and actors.
- Queue entries are sorted by `sortY` (ascending), then tie-break index for deterministic stability.
- Lower-on-screen feet/base lines (higher Y) render later and appear in front.

6. Atlas building `sortY` calculation
- Atlas buildings now use visual-base sorting:
- `buildingSortY = (b.y * TILE) + (sprite.anchorY ?? anchorPxY)`
- This uses atlas anchor metadata when present, with stable fallback to building anchor pixel baseline.

7. Actor sorting against buildings
- NPCs use `(npc.y + 1) * TILE` as feet/base sort.
- Wolves/bandits/player use pixel feet baseline: `entity.py + TILE`.
- Actors are now interleaved with buildings in the same sorted queue, enabling behind/in-front behavior by feet depth.

8. Locked hero metadata preservation
- Locked hero atlas building identities and village hall metadata were not modified in this phase.

9. Layout redesign status
- Harbor-town structure was preserved; no broad layout redesign was introduced.

10. Known remaining risks
- Exact tie situations (same `sortY`) rely on fixed tie-break ordering and may still need targeted tuning for edge-case overlaps.
- Label density/readability remains mostly unchanged aside from improved geometry occlusion; additional label declutter could be done in a future Phase 32 task.

11. QA instructions
- Run with `atlasDebug=1&atlasPreview=1&decorDebug=1` and verify dense overlaps in Hearthvale.
- Validate tavern/mercantile/village hall overlap order while moving player/NPCs across facades and frontage.
- Toggle collision overlay (`V`) and confirm collision remains movement-only and still matches blocked zones.
- Confirm no fallback/metadata regressions in atlas proof diagnostics (`metadataSource`/`manifestVersion`).
- Ensure debug/status language does not claim production readiness.
