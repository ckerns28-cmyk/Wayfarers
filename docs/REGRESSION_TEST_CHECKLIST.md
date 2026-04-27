# Wayfarer Regression Test Checklist (Manual)

## Movement
- [ ] Walk around Hearthvale.
- [ ] Walk into Eastern Woods without teleport jump.
- [ ] Return to Hearthvale naturally.

## NPCs
- [ ] Talk to Edrin Vale.
- [ ] Talk to Merchant Rowan.
- [ ] Talk to Hunter Garran.

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

## Foundation lock validation
- [ ] Load a legacy save that lacks `saveSchemaVersion` and verify no crash.
- [ ] Confirm default fields initialize safely when missing.
- [ ] Verify debug-only keys function: F6, F7/F8/F9, F10, Shift+F10.
- [ ] Confirm chronicle no longer floods repeated transition/combat miss spam.
