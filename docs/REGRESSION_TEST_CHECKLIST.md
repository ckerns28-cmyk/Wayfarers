# Wayfarer Regression Test Checklist (Manual)

## Movement
- [ ] Walk around Hearthvale.
- [ ] Walk into Eastern Woods without teleport jump.
- [ ] Return to Hearthvale naturally.

## NPCs
- [ ] Talk to Edrin Vale.
- [ ] Edrin shows branching dialogue options (Mirror Pond / cave / Wayfarer / goodbye).
- [ ] If Mirror Cave chest is opened, Edrin references change near Mirror Pond.
- [ ] Talk to Merchant Rowan.
- [ ] Rowan opens shop only via “Show me your goods.”
- [ ] Rowan provides advice and Hearthvale dialogue branches.
- [ ] If player owns Iron Sword, Rowan comments on improved gear.
- [ ] Talk to Hunter Garran.
- [ ] Hunter shows correct Hunter’s Request state (not started / active / ready turn-in / completed).
- [ ] Hunter active dialogue shows objective progress reminders.
- [ ] Hunter completion cannot be claimed twice.
- [ ] Hunter repeatable flavor lines mention wolves, bandits, Eastern Woods, and survival.
- [ ] Dialogue choices can be selected by number keys and clickable options.
- [ ] Dialogue panel always includes a clear exit path and closes correctly.
- [ ] Dialogue panel remains readable with no clipping or HUD overlap.

## Vendor
- [ ] Buy Small Potion.
- [ ] Buy Leather Armor.
- [ ] Sell Wolf Pelt.
- [ ] Coins update correctly.

## Inventory
- [ ] Items stack.
- [ ] Equipment displays correctly.
- [ ] Consumables appear correctly.

## Equipment
- [ ] Equip Rusty Sword.
- [ ] Equip Iron Sword.
- [ ] Equip Leather Armor.
- [ ] Damage changes correctly.

## Combat
- [ ] Fight wolf.
- [ ] Fight bandit.
- [ ] Enemy drops loot.
- [ ] Enemies respawn.
- [ ] Death/respawn works.

## Quest
- [ ] Hunter’s Request displays completed state.
- [ ] Completed quests do not reward twice.
- [ ] Active quest reminders remain accurate after save/load.

## Dungeon
- [ ] Enter Mirror Cave.
- [ ] Fight cave wolf.
- [ ] Open chest.
- [ ] Receive Iron Sword.
- [ ] Exit cave.

## Save/load
- [ ] Save in Hearthvale.
- [ ] Save in Eastern Woods.
- [ ] Save in Mirror Cave if supported.
- [ ] Reload preserves state.
- [ ] Reload preserves completed quest states and prevents duplicate turn-in rewards.

## Foundation lock validation
- [ ] Load a legacy save that lacks `saveSchemaVersion` and verify no crash.
- [ ] Confirm default fields initialize safely when missing.
- [ ] Verify debug-only keys function: F6, F7/F8/F9, F10, Shift+F10.
- [ ] Confirm chronicle no longer floods repeated transition/combat miss spam.
