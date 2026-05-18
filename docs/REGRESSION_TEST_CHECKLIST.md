# Wayfarer Regression Test Checklist (Manual)

## A. Town loop
- [ ] Talk to Edrin Vale.
- [ ] Talk to Hunter Garran.
- [ ] Talk to Merchant Rowan.

## B. Combat loop
- [ ] Fight wolf.
- [ ] Level 1 + Rusty Sword vs wolf feels threatening but fair (no instant deletion).
- [ ] Level 2 + Leather Armor vs wolf shows meaningful damage reduction.
- [ ] Fight bandit.
- [ ] Bandit with Leather Armor equipped feels dangerous but not unfair.
- [ ] Die and respawn.
- [ ] Respawn occurs in safe position with restored HP and no immediate attack chain.
- [ ] Enemies respawn.

## C. Economy loop
- [ ] Loot item.
- [ ] Wolf pelt/fang accumulation does not spike too quickly during normal quest routing.
- [ ] Sell item.
- [ ] Buy potion.
- [ ] Buy healing herb.
- [ ] Confirm potion/herb prices feel meaningful against normal coin gain.
- [ ] Use potion.

## D. Equipment loop
- [ ] Equip weapon.
- [ ] Equip armor.
- [ ] Confirm damage changes.

## E. Quest loop
- [ ] Start Hunter's Request.
- [ ] Collect pelts.
- [ ] Return to Hunter.
- [ ] Enter cave.
- [ ] Retrieve relic.
- [ ] Complete quest.
- [ ] Confirm no duplicate reward.

## F. Dungeon loop
- [ ] Walk into Mirror Cave entrance.
- [ ] Exit Mirror Cave.
- [ ] Fight cave wolf and confirm cave threat > overworld wolf threat.
- [ ] Chest sealed/closed/open behavior.
- [ ] Save/reload in or around cave.

## G. Persistent objects
- [ ] Read sign.
- [ ] Open chest.
- [ ] Save/reload.
- [ ] Confirm object state persists.

## H. Save/load
- [ ] Save in Hearthvale.
- [ ] Save in Eastern Woods.
- [ ] Save after quest completion.
- [ ] Save after chest state changes.
- [ ] Save/load preserves level, XP, max HP/current HP, equipment, and inventory values.
- [ ] Save/load preserves zone and quest progression while in Mirror Cave flow.
- [ ] Reload and confirm state.

## I. Progression pacing (Phase 21)
- [ ] Complete Hunter's Request + several wolf kills + Mirror Cave clear.
- [ ] Confirm end state is typically Level 2 or Level 3 (not Level 5 without heavy grinding).

## J. Main story thread — The Still Water (Phase 22)
- [ ] Talk to Edrin Vale and start **The Still Water**.
- [ ] Inspect Mirror Pond and confirm delayed-reflection message appears.
- [ ] Return to Edrin and advance to Mirror Cave objective.
- [ ] Enter Mirror Cave and confirm objective advances.
- [ ] Recover Echo Fragment and confirm no duplicate can be obtained.
- [ ] Return to Edrin and complete **The Still Water**.
- [ ] Confirm Hunter's Request remains functional/completable in same save.
- [ ] Confirm Mirror Cave chest/relic behavior remains unchanged.
- [ ] Save/load during each stage preserves quest stage, Echo Fragment state, and inventory.
- [ ] Confirm dialogue panel close behavior still works during Edrin conversations.

## K. Second Outdoor Region — North Road (Phase 25)
- [ ] Walk north from Hearthvale without teleport/screen snap and confirm zone updates to **North Road**.
- [ ] Walk back south to Hearthvale and confirm smooth return and correct zone label.
- [ ] Read North Road sign and verify prompt, sign text, and clean close behavior.
- [ ] Open roadside crate/chest and verify one-time minor loot behavior.
- [ ] Save/reload after opening crate/chest and confirm opened state persists.
- [ ] Fight North Road enemies and confirm combat/XP/loot balance remains modest.
- [ ] Confirm no enemy spawns directly on the North Road entrance path.
- [ ] Save/load while standing in North Road and verify player position + HUD zone text remain correct.

## L. Second Dungeon / Mini-Boss — Abandoned Tollhouse (Phase 26)
- [ ] POI discovery test: approach or enter the tollhouse and verify `Discovered: Abandoned Tollhouse.` appears once.
- [ ] Environmental sign test: read the tollhouse roadside notice and verify text appears/closes cleanly.
- [ ] Enter North Road and confirm region remains stable.
- [ ] Enter Abandoned Tollhouse and verify hard transition (no bounce loop, safe spawn, cooldown behavior).
- [ ] Fight interior bandits and confirm encounter difficulty feels fair for Level 3–5 loadouts.
- [ ] Confirm Rook the Tollkeeper appears clearly named and feels stronger than normal bandits.
- [ ] Rook defeat feedback test: verify Chronicle logs `Rook the Tollkeeper defeated.` and a clear `Boss rewards:` list.
- [ ] Defeat Rook and verify one-time mini-boss rewards (XP/coins/Old Toll Key, Traveler's Charm path).
- [ ] Open tollhouse chest after Rook defeat and verify one-time loot behavior.
- [ ] On first chest open, verify Chronicle prints `Opened the tollhouse chest.` + `Loot acquired:` + per-reward lines, and on-screen reward notifications appear (`+ Item` / `+Coins`).
- [ ] Chest reward feedback test: verify inventory reflects each listed chest reward exactly once.
- [ ] Interact with the already-open tollhouse chest and verify no rewards are granted and Chronicle logs `The tollhouse chest is empty.`.
- [ ] Defeat Rook, save/reload, and confirm no duplicate boss rewards are granted on revisit (Rook does not respawn and rewards are not re-issued).
- [ ] Save/reload after Rook defeat and verify: Rook stays defeated, chest state persists, rewards do not duplicate.
- [ ] Cleared-state persistence test: after Rook defeat + chest open, verify cleared state survives save/reload and objective text returns to exploration.
- [ ] Equip Traveler's Charm from Inventory and verify Equipment panel shows `Trinket: Traveler's Charm` with DEF increase reflected in combat mitigation.
- [ ] Objective panel context check (with no active quest): before clear = `Explore the Abandoned Tollhouse.`, after Rook defeat/chest closed = `Open the tollhouse chest.`, after clear = `Explore Hearthvale and the surrounding roads.`.
- [ ] Regression sweep: Hearthvale, North Road, Mirror Cave, Merchant Rowan, Hunter Garran, Edrin Vale, inventory/equipment, and level/XP all remain functional.

## M. Skill Use Progression (Phase 27)
- [ ] Hit enemies with a melee weapon and confirm Swordsmanship XP increases on successful hits only.
- [ ] Defeat enemies with a melee weapon and confirm Swordsmanship defeat XP is granted.
- [ ] Verify Swordsmanship levels up at 50/125/250/450 XP and melee damage bonus applies (+1 at Lv2-3, +2 at Lv4-5).
- [ ] Take enemy damage while armor is equipped and confirm Defense XP increases.
- [ ] Confirm Defense level bonuses increase total defense but incoming damage still has a minimum of 1.
- [ ] Defeat an enemy while armored and confirm encounter-survival Defense XP bonus applies.
- [ ] Use Healing Herb/Small Potion while damaged and confirm Survival XP increases and healing bonus applies by Survival level.
- [ ] Attempt to use healing items at full HP and confirm item is not consumed and no Survival XP is granted.
- [ ] Save, reload, and confirm skill levels + skill XP persist alongside level/XP, HP, inventory, and equipment.
- [ ] Confirm Equipment panel clearly shows Traveler's Charm trinket defense bonus and total mitigation reflects it.

## N. Save Schema / Architecture Hardening (Phase 28)
- [ ] Fresh save: start new game, save, reload, and confirm no console errors.
- [ ] Advanced save: verify Hunter's Request complete + The Still Water complete + tollhouse cleared + skills/equipment/trinket all persist.
- [ ] Missing field simulation: remove `player.skills` from save JSON and confirm defaults are restored safely.
- [ ] Missing persistent object registry simulation: remove `world.persistentObjects` and confirm no duplicate chest/object rewards.
- [ ] Corrupt save simulation: set invalid JSON in `wayfarer.save.v1`, reload, and verify graceful recovery/reset behavior.
- [ ] Equipment consistency: equipped weapon/armor/trinket persist and remain inventory-safe after reload.
- [ ] Quest consistency: completed quests stay completed and rewards cannot be duplicated after migration.
- [ ] Dungeon consistency: Mirror Cave chest + Tollhouse chest + Rook defeated states persist through save/load.
- [ ] Schema migration: load a save with missing `saveSchemaVersion` and confirm it migrates to `saveSchemaVersion: 2`.
- [ ] Backup behavior: confirm `wayfarer.save.v1.backup` is written before migration overwrite/save writes.

## O. Vertical Slice Quality Gate (Phase 30)

### A. New/fresh flow
- [ ] Start game.
- [ ] Confirm Current Objective is immediately readable.
- [ ] Talk to Edrin, Hunter Garran, and Merchant Rowan.
- [ ] Start Hunter's Request and confirm objective updates.
- [ ] Progress naturally from Hearthvale to wolves without getting stuck.

### B. Combat feel
- [ ] Fight a wolf and confirm hit/miss readability in Chronicle.
- [ ] Fight a bandit and confirm incoming damage is readable.
- [ ] Use potion during combat.
- [ ] Level up and confirm visible level-up feedback.
- [ ] Skill up and confirm toast/log appears once per level gain.
- [ ] Die and respawn; confirm defeat/respawn feedback is clear.

### C. Quest progression
- [ ] Complete Hunter's Request.
- [ ] Complete The Still Water.
- [ ] Confirm no duplicate quest rewards on repeated turn-ins.

### D. Dungeon checks
- [ ] Enter and exit Mirror Cave.
- [ ] Confirm Mirror Cave chest gating (sealed/closed/open) behavior.
- [ ] Confirm Mirror Cave chest and Echo Fragment states persist through save/load.

### E. Tollhouse checks
- [ ] Discover Abandoned Tollhouse from North Road.
- [ ] Defeat Rook and confirm mini-boss defeat messaging.
- [ ] Open tollhouse chest and verify reward feedback (Chronicle + toasts + inventory).
- [ ] Confirm tollhouse cleared state persists after save/load.

### F. UI readability
- [ ] Sidebar tabs switch reliably (Inventory/Equipment/Skills/Chronicle).
- [ ] No clipping in objective, dialogue, or vendor panels at normal desktop sizes.
- [ ] Dialogue opens/closes without stuck modal behavior.
- [ ] Vendor panel opens/closes and buy/sell actions remain usable.
- [ ] Chronicle remains accessible during normal play flow.

### G. Save/load regression
- [ ] Save after major milestones (quest completion, chest opens, Rook defeat).
- [ ] Reload and confirm zone, quest, rewards, inventory, skills, and objective text remain correct.

## P. Combat Feel & Reward Polish (Phase 31)

### A. Wolf fight feel
- [ ] Fight wolf and confirm player-hit feedback is visible (damage number + readable combat log).
- [ ] Confirm enemy hit on player is clearly communicated (damage number + HP movement + Chronicle).
- [ ] Confirm Chronicle remains readable during repeated exchanges (no excessive duplicate spam).

### B. Bandit fight feel
- [ ] Fight bandit and confirm current target label is clear when multiple enemies are nearby.
- [ ] Confirm enemy HP readability in labels remains legible during movement/combat.

### C. Rook mini-boss moment
- [ ] Enter Rook range and confirm first-encounter callout appears.
- [ ] Defeat Rook and confirm strong defeat line + reward toasts.
- [ ] Confirm chest unlock feedback is visible and understandable.

### D. Chest/loot feedback
- [ ] Open tollhouse chest and verify clear per-reward feedback.
- [ ] Confirm no duplicate chest rewards after chest is already open.

### E. Level-up feedback
- [ ] Gain a level and confirm level-up callout appears.
- [ ] Confirm stat changes are listed clearly (HP/Attack/Defense where applicable).

### F. Skill-up feedback
- [ ] Trigger skill level gain and verify `Skill Up` notification includes skill level.
- [ ] Confirm Skills panel reflects the upgraded level/progress.

### G. Healing feedback
- [ ] Use potion/herb while damaged and verify use + HP restored feedback is explicit.
- [ ] Confirm full-HP healing use is blocked (no item consumed, clear message).
- [ ] Confirm Survival XP gain messaging appears when applicable.

### H. Death/respawn clarity
- [ ] Die in combat and confirm defeat messaging is explicit.
- [ ] Confirm respawn is safe and avoids immediate attack loop.

### I. Full regression sweep after feel pass
- [ ] Sidebar tabs remain functional.
- [ ] Save/load remains stable with existing saves.
- [ ] Merchant Rowan, Hunter Garran, and Edrin Vale interactions remain functional.
- [ ] Mirror Cave flow remains functional.
- [ ] Tollhouse cleared state remains preserved if previously cleared.

## Q. Newport Town-Phase Served Validation Merge Gate

A Newport town-phase PR is **not complete** unless the PR body includes pasted served evidence from the live served URL.

- [ ] Live served URL used for validation is included in PR body.
- [ ] Final `[Wayfarer QA Report]` line is pasted from served browser console output.
- [ ] Final `[Building Placement Contract QA]` line is pasted from served browser console output.
- [ ] Final `[Newport Visual Composition QA]` line is pasted from served browser console output.
- [ ] Final `[Harbor Composition QA]` line is pasted from served browser console output.
- [ ] Final `[Newport Masterplan QA]` line is pasted from served browser console output.
- [ ] Final `[Building Visual Solidity QA]` line is pasted from served browser console output (status=PASS, walkableSolidOverlapCount=0 for every production building).
- [ ] Final `[Active Player Solid Overlap Probe]` line is pasted from served browser console output (overlappingSolidBuildingId=none, status=PASS).
- [ ] Screenshot evidence is attached (atlasDebug, non-debug, freshSpawn).

Do not claim served validation is complete unless the actual served browser console output is pasted into the PR body.

## R. Godot Vertical Slice Delivery (parallel preview)

The Godot vertical slice ships to a **separate** Cloudflare Pages project and
must not replace the live JavaScript site. Until that pass is approved,
`wrangler.toml` continues to point at `wayfarer_v7_github_ready/`.

### A. Source-truth validation
- [ ] `godot --headless --path wayfarer_godot_vertical_slice --script res://tools/validate_vertical_slice.gd` reports `status=PASS` and `failureCount=0`.
- [ ] Validator includes the stricter checks (no missing AtlasTexture regions, foot anchor on visible base, collision overlaps lower visible/base, interaction adjacent to door, player can stand south/north of ≥2 buildings, all five buildings inside the initial camera).

### B. Sprite region audit (Phase delivery pass)
- [ ] `inn_tavern` region `(33, 45, 385, 373)` shows the blue 3-story inn with no sliver from the awning building or the small white house.
- [ ] `dock_storehouse` region `(51, 836, 361, 377)` shows the gray storehouse with crane (NOT the chapel-with-porch the old region was bleeding into).
- [ ] `custom_house` region `(68, 873, 350, 292)` shows the dockside cottage with no padding crops.
- [ ] `merchant_shop_house` region `(418, 76, 410, 332)` shows the columned mansion with its full left edge.
- [ ] `large_residence` region `(864, 86, 351, 315)` shows the brown row-house with no transparent gutter.

### C. Anchor / collision / interaction proof
- [ ] Press `F3` in-game and confirm the per-building debug overlay draws sprite outline (yellow), collision rect (red), interaction rect (blue), foot anchor (green cross), and door marker (yellow dot).
- [ ] Confirm each collision rect sits on the building's visible base/foundation.
- [ ] Confirm each interaction rect sits directly south of (in front of) the visible door.
- [ ] Move the player south of any building and confirm collision blocks correctly.
- [ ] Move the player north of large_residence and merchant_shop_house and confirm Y-sort draws the player behind the closer building.

### D. Web export and Cloudflare delivery
- [ ] `bash wayfarer_godot_vertical_slice/tools/export_web.sh` produces `web_build/index.html` plus `.wasm`/`.pck`/`.js` siblings and copies `_headers` from `web_build_template/`.
- [ ] Upload `web_build/` to the `wayfarers-godot-slice` Cloudflare Pages project (see `WEB_DELIVERY.md`).
- [ ] Visit the published `https://wayfarers-godot-slice.pages.dev` (or equivalent preview URL) and confirm: canvas renders, player walks, Edrin Vale prompt appears, F3 toggles the debug overlay.
- [ ] Confirm the existing JavaScript site served by the `wayfarers` Worker is still unchanged (no visual or behavioral regression at the production URL).

## S. G-5 Migration Architecture

G-5 is a planning architecture phase. It must not replace the JavaScript Worker
route or port gameplay systems by copying Worker code into Godot scene scripts.

### A. Architecture package
- [ ] `docs/reports/G5_MIGRATION_ARCHITECTURE.md` exists and states G-5 is planning-only.
- [ ] `docs/reports/G5_MIGRATION_ARCHITECTURE.json` includes all required migration system rows.
- [ ] `docs/reports/G5_MIGRATION_ARCHITECTURE_AGENT_COUNCIL_REPORT.md` records `COUNCIL_PASS_READY_FOR_PR`.
- [ ] `wayfarer_godot_vertical_slice/tools/validate_g5_migration_architecture.py` reports `PASS`.

### B. Worker reference protection
- [ ] The JavaScript Worker route remains the production/reference route.
- [ ] `wayfarer_v7_github_ready/worker/src/index.js` remains source evidence, not copied gameplay port material.
- [ ] G-6 is still required before any production route replacement.

### C. Migration readiness
- [ ] Golden Worker save fixtures are listed as the first implementation dependency.
- [ ] Save compatibility bridge is ordered before quest, combat, inventory, reward, dungeon, or cutover work.
- [ ] Movement/camera/zone, interaction/dialogue/quest, inventory/equipment/economy, combat/enemy/loot/progression, save/load/persistence, world objects/dungeons, UI/HUD/Chronicle, and deployment/QA systems all have future Godot owners and validation gates.
- [ ] Future player-facing migration work still requires screenshot proof and Agent Council inspection.

## T. G-6 Production Cutover Planning

G-6 defines production cutover criteria and rollback safety. It must not replace
the JavaScript Worker route by accident.

### A. Cutover package
- [ ] `docs/reports/G6_PRODUCTION_CUTOVER_PLANNING.md` exists and states G-6 is planning-only.
- [ ] `docs/reports/G6_PRODUCTION_CUTOVER_PLANNING.json` includes the hosting decision matrix, QA gates, cutover runbook, and rollback runbook.
- [ ] `docs/reports/G6_PRODUCTION_CUTOVER_AGENT_COUNCIL_REPORT.md` records `COUNCIL_PASS_READY_FOR_PR`.
- [ ] `wayfarer_godot_vertical_slice/tools/validate_g6_production_cutover.py` reports `PASS`.

### B. Production route protection
- [ ] Root `wrangler.toml` still points at `wayfarer_v7_github_ready/worker/src/index.js`.
- [ ] Root `wrangler.toml` still uses `./wayfarer_v7_github_ready/worker/assets`.
- [ ] The Godot route remains a review/migration route and not the production replacement.
- [ ] Any future route replacement PR has explicit cutover authority and rollback evidence.

### C. Cutover readiness gates
- [ ] G-5.1 through G-5.9 parity evidence exists before any future replacement.
- [ ] Worker save schema v2 round-trips through Godot without progress loss before any future replacement.
- [ ] Served Godot Web export validation, runtime visual QA, performance/browser matrix, rollback rehearsal, and Agent Council release authority are all required before any future replacement.

## U. SV-0 Starter Village Tooling Stack

- [ ] `wayfarer_godot_vertical_slice/tools/validate_sv0_tooling_stack.py` reports `PASS`.
- [ ] The authoritative world-layout source identifies districts, lots, roads, alleys, dock paths, NPC routes, interaction zones, quest beats, and screenshot viewpoints before new placement work begins.
- [ ] The visual regression manifest covers the recurring Newport views and is treated as a warning system, not automatic art approval.
- [ ] Runtime movement proof is produced for NPC/player movement phases before the Agent Council can pass them.
- [ ] Ground/material cohesion follows the locked Godot-native material stack before props or clutter are used.
- [ ] No paid, unknown-license, admin-only, or external-drive-modifying tool is required for the Starter Village path.
