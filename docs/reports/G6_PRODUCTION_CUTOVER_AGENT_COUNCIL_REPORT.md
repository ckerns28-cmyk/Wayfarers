# G-6 Wayfarer Agent Council Report

Generated: 2026-05-18

## Summary

- Phase ID: G-6
- Phase name: Production Cutover Planning
- Branch: `codex/g-6-production-cutover-planning`
- Starting synced main commit: `fe45b2a6dbd41de00b37b5897790c54b6c5d7090`
- Phase type: planning and release safety
- Production route changed: no
- JavaScript Worker remains production route: yes
- Godot remains browser-review/migration route: yes
- Cutover authorized now: no
- Final Authority Verdict: `COUNCIL_PASS_READY_FOR_PR`
- Human escalation required: no
- Final recommended next phase: no later phase is defined in `docs/WAYFARER_GODOT_ROADMAP.md`

## Roadmap Execution Result

| Question | Council Answer |
| --- | --- |
| Did G-6 start only after G-5 was merged and synced? | PASS |
| Does this phase define production-hosting decision, rollback plan, QA gates, and replacement criteria? | PASS |
| Does the Worker remain production-facing during this phase? | PASS |
| Does this phase avoid a hidden production cutover? | PASS |
| Does this package explain why actual replacement is not authorized yet? | PASS |
| Does it identify the next roadmap boundary honestly? | PASS |

## Production Route Audit

| Area | Judgment | Status |
| --- | --- | --- |
| Root deployment route | `wrangler.toml` still points at `wayfarer_v7_github_ready/worker/src/index.js`. | PASS |
| Worker asset route | Root assets remain `./wayfarer_v7_github_ready/worker/assets`. | PASS |
| Worker package | `wayfarer_v7_github_ready/worker/wrangler.toml` remains source evidence and is not changed by this planning phase. | PASS |
| Godot review route | Godot remains a parallel review/migration track. | PASS |
| Cutover authorization | Actual production replacement is explicitly not authorized by G-6. | PASS |

## Hosting Decision Audit

| Decision | Council Judgment | Status |
| --- | --- | --- |
| Keep JS Worker production route | Correct current decision because it is still the complete gameplay/save/deploy route. | PASS |
| Continue Godot review route | Correct for screenshot/runtime validation without production risk. | PASS |
| Cloudflare Pages preview | Acceptable only as a separate preview target after upload constraints are solved. | PASS |
| Replace Worker with Godot | Correctly blocked until parity, save, and rollback gates pass. | PASS |
| Hybrid Worker/API plus Godot client | Valid future direction, but not before migrated services and persistence boundaries exist. | PASS |

## Rollback Readiness Audit

| Requirement | Result |
| --- | --- |
| Restore route path named | PASS |
| Save preservation policy named | PASS |
| Worker redeploy path named | PASS |
| Production smoke evidence required | PASS |
| Rollback evidence report required | PASS |

## QA Gate Audit

| Gate | Status |
| --- | --- |
| Branch and remote preflight | PASS |
| Production route protection | PASS |
| G-5 parity evidence required before future replacement | PASS |
| Save compatibility round trip required | PASS |
| Godot web export served validation required | PASS |
| Runtime visual QA required | PASS |
| Performance/browser matrix required | PASS |
| Rollback rehearsal required | PASS |
| Release authority required | PASS |

## Scrum Master Review

- Status: PASS
- G-6 is scoped correctly as cutover planning and release safety.
- The plan refuses to compress missing G-5.1 through G-5.9 implementation into a pretend launch.
- The next boundary is honest: the roadmap currently ends after G-6, so a new phase must be defined before autonomous implementation continues.

## Game Designer Review

- Status: PASS
- Player trust is protected by blocking cutover until quests, combat, inventory, economy, dungeon persistence, and save/load parity exist.
- The plan keeps the current playable JS route intact while Godot matures.
- Caveats are separated from blockers.

## Art Director Review

- Status: PASS
- The G-4.22R atelier runtime asset consistency gate remains a hard future cutover requirement.
- Future player-facing cutover candidates require no-HUD/no-debug screenshots and council inspection.
- No visual standard is lowered by this planning phase.

## Game Programmer Review

- Status: PASS
- The plan protects root route files and avoids accidental production edits.
- Save compatibility, parity fixtures, and rollback rehearsal are correctly blocking gates.
- The new validator makes route safety machine-checkable.

## QA Review

- Status: PASS
- G-6 has a machine-readable plan and validator.
- The QA gates are concrete enough to fail a future unsafe cutover PR.
- Technical pass is not treated as player-facing release acceptance.

## Validation Results

| Check | Result |
| --- | --- |
| `validate_g6_production_cutover.py` | PASS |
| `validate_g5_migration_architecture.py` | PASS |
| `validate_pre_g5_roadmap_ledger.py` | PASS |
| `validate_g422r_runtime_asset_consistency.py` | PASS |
| Godot import validation | PASS |
| `validate_vertical_slice.gd` | PASS |
| `validate_newport_asset_provenance.py` | PASS |
| Python compile check for G-6 validator | PASS |
| G-6 JSON syntax validation | PASS |
| `git diff --check` | PASS |
| `git diff --cached --check` | PASS |

## World/Narrative Review

- Status: PASS
- Production replacement is blocked until quest, NPC, dungeon, and persistent object parity is proven.
- The plan protects continuity for The Still Water, Hunter's Request, Mirror Cave, Abandoned Tollhouse, and Rook state.

## UX Review

- Status: PASS
- Future cutover requires served-browser validation and player-facing screenshot proof.
- HUD, dialogue, quest, combat, inventory, save, and rollback behavior are all named as release evidence.

## Technical Artist Review

- Status: PASS
- Runtime visual QA and the atelier sprite/provenance gate remain required for future production candidates.
- Godot review builds remain separate from production until route replacement is explicitly authorized.

## Release Manager Decision

- Final Authority Verdict: `COUNCIL_PASS_READY_FOR_PR`
- This PR is safe to open after validators pass.
- It must not change production hosting.
- After merge and synced-main confirmation, stop at the roadmap boundary unless a new roadmap phase is added.
