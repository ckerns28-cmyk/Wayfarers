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
- [ ] Enter North Road and confirm region remains stable.
- [ ] Enter Abandoned Tollhouse and verify hard transition (no bounce loop, safe spawn, cooldown behavior).
- [ ] Fight interior bandits and confirm encounter difficulty feels fair for Level 3–5 loadouts.
- [ ] Confirm Rook the Tollkeeper appears clearly named and feels stronger than normal bandits.
- [ ] Defeat Rook and verify one-time mini-boss rewards (XP/coins/Old Toll Key, Traveler's Charm path).
- [ ] Open tollhouse chest after Rook defeat and verify one-time loot behavior.
- [ ] On first chest open, verify Chronicle prints `Opened the tollhouse chest.` + `Loot acquired:` + per-reward lines, and on-screen reward notifications appear (`+ Item` / `+Coins`).
- [ ] Interact with the already-open tollhouse chest and verify no rewards are granted and Chronicle logs `The tollhouse chest is empty.`.
- [ ] Defeat Rook, save/reload, and confirm no duplicate boss rewards are granted on revisit (Rook does not respawn and rewards are not re-issued).
- [ ] Save/reload after Rook defeat and verify: Rook stays defeated, chest state persists, rewards do not duplicate.
- [ ] Equip Traveler's Charm from Inventory and verify Equipment panel shows `Trinket: Traveler's Charm` with DEF increase reflected in combat mitigation.
- [ ] Objective panel context check (with no active quest): before Rook defeat = clear tollhouse, after Rook defeat/chest closed = open chest, after chest open = cleared/explore text depending on location.
- [ ] Regression sweep: Hearthvale, North Road, Mirror Cave, Merchant Rowan, Hunter Garran, Edrin Vale, inventory/equipment, and level/XP all remain functional.
