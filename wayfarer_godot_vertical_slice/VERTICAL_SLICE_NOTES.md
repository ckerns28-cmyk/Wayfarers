# Vertical Slice Notes

## What This Tests

The slice isolates the problems that made Newport hard in the JavaScript build:

- visual foot anchors instead of tile guesses
- collision shapes that match visible building bases
- Y-sort depth using Godot scene objects
- interaction/frontage points positioned at obvious doors
- harbor-town readability without placing all 19 production buildings

## Early Read

Godot's scene/object model is a better fit for the placement problem than the custom canvas stack. Buildings can own their sprite, collision, interaction area, and visual anchor in one object. The player and buildings can live under one Y-sorted parent, which directly addresses the in-front/behind problem without a large custom depth-sort contract.

The current capture shows the five-building slice seated more cleanly than the JavaScript Newport view: all building sprites are complete, base anchors are visible, the first-view camera does not crop the structures, and debug collision shapes sit on building bases instead of arbitrary tile-sized blocks.

## Validation Result

`tools/validate_vertical_slice.gd` currently passes:

- Godot version: 4.6.2 stable
- buildingCount: 5
- failureCount: 0
- status: PASS

## Not Decided Yet

This does not decide full migration. The next review should judge the running screenshot and hands-on movement around the five buildings before any inventory, combat, save, or quest systems are ported.
