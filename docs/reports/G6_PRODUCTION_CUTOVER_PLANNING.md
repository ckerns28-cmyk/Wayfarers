# G-6 Production Cutover Planning

Generated: 2026-05-18

## Status

- Phase: `G-6 Production Cutover Planning`
- Starting synced main commit: `fe45b2a6dbd41de00b37b5897790c54b6c5d7090`
- Branch: `codex/g-6-production-cutover-planning`
- Phase type: production cutover planning, not production cutover execution
- Production route change: no
- JavaScript Worker route: remains the production-facing Phase 35.13R route
- Godot route: remains the Newport browser-review and migration-validation route
- Cutover authorized now: no
- Council verdict: `COUNCIL_PASS_READY_FOR_PR`
- Human review required for this planning pass: no
- Next roadmap phase after this PR: no later phase is currently defined in `docs/WAYFARER_GODOT_ROADMAP.md`

## Why G-6 Exists

G-5 created the migration architecture that prevents future Godot work from copying the JavaScript Worker wholesale or replacing production before gameplay parity exists. G-6 defines the production safety envelope around that future change: route ownership, rollback, save compatibility, hosted QA, visual proof, and the exact gates that must pass before a later cutover PR may replace the JavaScript Worker route.

This phase deliberately does not change production hosting. The Worker is still the only complete route for quests, combat, inventory, economy, save/load, persistence, dungeons, and production deployment. Godot has an accepted Newport runtime foundation and migration plan, but not yet the migrated gameplay systems required for production replacement.

## Source Evidence

| Source | Evidence Used |
| --- | --- |
| `docs/WAYFARER_GODOT_ROADMAP.md` | G-6 asks for production-hosting decision, rollback plan, QA gates, and replacement criteria. |
| `docs/reports/G5_MIGRATION_ARCHITECTURE.md` | G-5 requires G-6 before replacing the Worker route. |
| `docs/reports/G5_MIGRATION_ARCHITECTURE.json` | Lists G-5.1 through G-5.9 migration work that must feed cutover readiness. |
| `wayfarer_godot_vertical_slice/WEB_DELIVERY.md` | Documents Godot as a parallel browser-review route and the Worker as production-facing. |
| `wrangler.toml` | Root production deployment still points to `wayfarer_v7_github_ready/worker/src/index.js`. |
| `wayfarer_v7_github_ready/worker/wrangler.toml` | Worker package deployment definition remains intact. |
| `wayfarer_v7_github_ready/worker/src/index.js` | Current complete gameplay and production reference implementation. |
| `docs/MULTIPLAYER_ARCHITECTURE.md` | Future Worker/Durable Object/D1 trust boundary that cutover must not undermine. |
| `docs/SAVE_SCHEMA.md` | Save schema v2 compatibility contract for any future route replacement. |
| `docs/reports/PRE_G5_ROADMAP_EXECUTION_LEDGER.json` | Pre-G-5 proof remains the prerequisite visual/runtime foundation. |

## Hosting Decision Matrix

| Decision | Status | Reason | Guardrail |
| --- | --- | --- | --- |
| Keep the JavaScript Worker as production route | SELECTED_FOR_NOW | It is still the complete gameplay, save, and deployment reference. | G-5.1 through G-5.9 must produce parity evidence before replacement is reconsidered. |
| Continue Godot as itch.io review route | ACTIVE_REVIEW_PATH | It proves Godot runtime and screenshots without disturbing production. | Every review build needs commit, validation, screenshot, and upload evidence. |
| Separate Cloudflare Pages Godot preview | DEFERRED_PREVIEW_OPTION | Useful once export size/upload constraints are solved. | Must remain a preview project, not the production Worker route. |
| Replace Worker with Godot route | NOT_AUTHORIZED | Godot gameplay parity does not exist yet. | Only a future explicit cutover PR may edit production routing. |
| Hybrid Worker ingress plus Godot client | FUTURE_CANDIDATE | Best matches future server-authoritative direction. | Requires SaveService, EntityRegistry, and parity fixtures first. |

## Hard Cutover Preconditions

- G-5.1 through G-5.9 are implemented or explicitly superseded with equivalent evidence.
- Worker golden fixtures exist for saves, movement, quests, inventory/equipment, combat outcomes, persistent objects, UI feedback, and deployment smoke behavior.
- Godot imports, repairs, preserves, exports, and reloads Worker save schema v2 without player progress loss.
- Godot gameplay services own migrated systems; sprites, HUD, animations, and scene scripts do not own canonical mutations.
- Side-by-side Worker/Godot parity reports pass for the core loop, quests, combat, inventory, economy, dungeon persistence, and save/load.
- Normal-play Godot screenshots pass the active atelier runtime asset consistency gate with no placeholder or debug-only world assets.
- Remote checks pass on the future cutover PR, including route-protection validation proving rollback is still possible.
- Rollback rehearsal demonstrates how to restore the Worker route and preserve or downgrade saves safely.
- Release notes separate caveats from blockers.

## QA Gates

| Gate | Blocking Evidence |
| --- | --- |
| Branch and remote preflight | Latest `origin/main`, clean worktree, no conflicting open PRs, remote auth healthy. |
| Production route protection | Root `wrangler.toml` still points at `wayfarer_v7_github_ready/worker/src/index.js` unless the PR is the explicit final cutover PR. |
| G-5 parity evidence | G-5.1 through G-5.9 implementation reports, validators, screenshots where player-facing, and council verdicts. |
| Save compatibility round trip | Worker schema v2 fixtures import, repair, preserve unknown fields where possible, export, and reload without progress loss. |
| Godot web export served validation | Fresh Godot Web export launches from a served browser-like route, not only from local editor state. |
| Runtime visual QA | No-HUD/no-debug screenshots prove the player, NPCs, markers, props, streets, harbor, and UI meet the active visual bar. |
| Performance and browser matrix | Desktop browser smoke coverage, input latency, load time, memory, crash-free runtime, and fallback notes. |
| Rollback rehearsal | Documented restore path for Worker routing, save compatibility, and rollback timing. |
| Release authority | Agent Council final authority report for the cutover PR and explicit merge/cutover authorization. |

## Cutover Runbook

1. Freeze the current production route by recording the Worker deployment, source commit, root `wrangler.toml`, Worker assets directory, and known-good hosted behavior.
2. Build the Godot candidate from the validated commit and serve it from a preview route.
3. Run Worker/Godot parity fixtures, save round trips, vertical slice validation, runtime asset consistency validation, and browser smoke checks.
4. Capture and inspect screenshots for normal play, no-HUD/no-debug state, UI feedback, combat, quest, inventory, and player readability.
5. Prepare an explicit cutover PR. Only that PR may edit production routing files, and it must include rollback commands and QA evidence.
6. Verify GitHub checks and hosted smoke results before merging.
7. Monitor served gameplay, save/load, first quest, combat, inventory, and rollback readiness after merge/deploy.

## Rollback Plan

1. Restore root deployment routing to `wayfarer_v7_github_ready/worker/src/index.js` and `./wayfarer_v7_github_ready/worker/assets`.
2. Preserve migrated save backups and, if needed, export Worker-readable schema v2 payloads before downgrading the route.
3. Redeploy the known-good Worker commit.
4. Verify the production URL loads, player state persists, first quest works, combat works, inventory works, and save/load remains intact.
5. Capture rollback evidence and document any player-facing caveats.

## Route Protection

The following files must not be changed by this planning phase:

- `wrangler.toml`
- `wayfarer_v7_github_ready/worker/wrangler.toml`

The validator must fail if the root `wrangler.toml` stops pointing to `wayfarer_v7_github_ready/worker/src/index.js` during G-6.

## Known Caveats

- G-6 defines cutover safety but does not implement G-5.1 through G-5.9 migration systems.
- Godot remains a browser-review and migration-validation route until parity implementation and cutover proof exist.
- Cloudflare Pages remains a separate preview option and not the production replacement route.

## Blockers To Actual Cutover

- G-5 migration implementation sequence is not complete.
- Godot save compatibility bridge is not implemented.
- Worker/Godot parity fixture suite is not implemented.
- Rollback rehearsal has not been executed against an actual cutover candidate.

These block actual production replacement only. They do not block this G-6 planning PR.

## Deliverables

- Cutover plan: `docs/reports/G6_PRODUCTION_CUTOVER_PLANNING.md`
- Machine-readable cutover plan: `docs/reports/G6_PRODUCTION_CUTOVER_PLANNING.json`
- Validator: `wayfarer_godot_vertical_slice/tools/validate_g6_production_cutover.py`
- Council report: `docs/reports/G6_PRODUCTION_CUTOVER_AGENT_COUNCIL_REPORT.md`
- Roadmap/checklist/web-delivery updates documenting route protection and QA gates.

## Recommendation

Pass G-6 as a production cutover planning phase once the validator and existing Godot/G-5/pre-G-5 gates pass. Merge the PR only if remote checks are green. After merge, stop at the roadmap boundary unless a new roadmap phase is added, because no phase after G-6 is currently defined in `docs/WAYFARER_GODOT_ROADMAP.md`.
