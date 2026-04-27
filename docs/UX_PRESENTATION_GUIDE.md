# Wayfarer UX Presentation Guide

This guide locks the presentation standards for gameplay UI and player-facing feedback systems.

## Core UX Principles

- Text readability is prioritized over decoration.
- Important actions must be obvious without tutorial dependency.
- Quest state must always be clear from at least one persistent UI surface.
- Every modal must have a clear exit path.
- UI must never clip off-screen at supported gameplay resolutions.

## Presentation Standards by System

### Dialogue Boxes

- Anchor to a predictable screen region.
- NPC name and dialogue body must be visually separated.
- Choice entries require clear hover/selection states.
- Keyboard and pointer navigation should remain equivalent.
- Exit action must always be visible.

### Vendor Panels

- Split buy/sell affordances clearly.
- Show item name, price/value, and owned quantity in one scan line.
- Confirm insufficient currency with immediate, readable feedback.
- Exit/close control is always present and consistently placed.

### Inventory Display

- Preserve a stable slot grid to reduce scan effort.
- Equipped status must be explicit and persistent.
- Consumables, equipment, and quest-relevant items should be distinguishable at a glance.
- Empty states should be unobtrusive but readable.

### Quest Objectives

- Active objective text should be concise and imperative.
- Completed steps should visibly transition state.
- Multi-stage quests should clearly indicate current stage.
- If a quest is blocked/sealed, reason text should be explicit.

### Chronicle / Log Messages

- Keep entries short, useful, and chronological.
- Priority events (quest updates, level-up, key items) should stand out with subtle emphasis.
- Avoid flooding repeated low-value messages.

### Interaction Prompts

- Prompt appears near interaction target or at a consistent UI anchor.
- Prompt copy format should be concise (verb + target).
- Hidden/disabled interactions should provide reason when attempted.

### NPC Labels

- Labels should remain readable against terrain via contrast/backplate treatment.
- Quest-relevant NPCs should have a subtle but clear ownership marker.
- Labels should avoid overlap where possible.

### Enemy Target Labels

- Show enemy name and level/threat context when targeted.
- Target highlight should be readable but not visually noisy.
- Maintain consistency across wolves, bandits, and future enemy classes.

### Level-Up Notifications

- Must be unmissable but short-lived.
- Show key gains (e.g., level, HP/stat delta) in one compact block.
- Should not block immediate combat controls unless explicitly modal.

### Item Pickup Notifications

- Include item name and quantity change.
- Stack updates should compress repeated pickups.
- Notification placement must not obscure critical combat/interaction UI.

## Layout, Clipping, and Layering Rules

- No core panel may render outside the viewport.
- Use safe margins for all anchored panels.
- Overlapping UI layers must follow a stable priority (e.g., modal > panel > world labels > decorative effects).
- Transient notifications must not hide critical modal controls.

## Accessibility and Readability Baselines

- Maintain sufficient text/background contrast in all zones (including dark cave scenes).
- Avoid low-size ornate fonts for body text.
- Favor short lines and predictable spacing.
- Reserve color-only state signaling for secondary reinforcement; primary meaning should also be shape/text/icon based.

## QA Checklist for Phase 24

1. Verify no clipping for dialogue, vendor, inventory, and quest panels at supported resolutions.
2. Verify every modal has a visible close/exit action.
3. Validate active quest clarity during stage transitions.
4. Validate chronicle entries for concise usefulness.
5. Verify prompt clarity on NPCs, cave entrance, chest states, and signs.
