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

## O. Shared World Prototype (Phase 30)
- [ ] Open two browser sessions against the same environment and confirm both connect successfully.
- [ ] Spawn both players in **Hearthvale Square** and confirm each sees the other player's name label.
- [ ] Move Player A and confirm Player B sees synchronized movement updates.
- [ ] Move Player B and confirm Player A sees synchronized movement updates.
- [ ] Leave/rejoin with Player A and confirm safe position restore from server-backed state.
- [ ] Verify single-player combat, inventory, quests, and save/load loops still function in solo session mode.
- [ ] Verify no trading UI, PvP interactions, party controls, guild systems, or chat features are exposed.
- [ ] Verify Mirror Cave and Abandoned Tollhouse remain private/solo-instance behavior in this phase.
