# Wayfarer Visual QA Checklist (Phase 32)

## Core readability checks
- [ ] Player sprite remains readable on town grass, forest grass, roads, water-adjacent tiles, cave floor, and tollhouse floor.
- [ ] NPC silhouettes are visually distinct from enemies without relying only on labels.
- [ ] Enemies are readable at combat distance (wolves vs bandits vs Rook).
- [ ] Current target label styling is clearer than non-target labels.

## World / terrain checks
- [ ] Paths are readable and lead naturally through Hearthvale, North Road, and Eastern Woods.
- [ ] Grass/forest transition seams are not harsh rectangular blocks.
- [ ] Water edge and shoreline at Mirror Pond read clearly from gameplay zoom.
- [ ] Mirror Pond looks visually distinct from regular water and feels slightly mystical.
- [ ] Cave and tollhouse entrances are obvious at first glance.

## Object/prop checks
- [ ] Chests are readable in closed/open states in Mirror Cave and Abandoned Tollhouse.
- [ ] Signs/notices are visually identifiable as interactables.
- [ ] Fences, trees, and clutter reinforce region identity without obstructing readability.

## UI checks
- [ ] UI panel art style matches world tone (not raw web-app look).
- [ ] Tabs, buttons, dialogue, and vendor panel remain functional and visually coherent.
- [ ] Notifications/toasts remain readable and unclipped.
- [ ] Labels do not overlap badly in common combat scenarios.

## Region identity checks
- [ ] Hearthvale Square reads warm/safe/organized.
- [ ] Eastern Woods reads denser/wilder/more dangerous.
- [ ] Mirror Pond reads special/mystic.
- [ ] North Road reads sparse/exposed/ominous.
- [ ] Mirror Cave reads cold/enclosed/ancient.
- [ ] Abandoned Tollhouse reads occupied/broken/bandit-controlled.

## Regression checks (must remain stable)
- [ ] Movement and collision unchanged.
- [ ] Zone transitions (cave/tollhouse enter/exit) work.
- [ ] NPC interaction, combat, loot, vendors, and quest progression work.
- [ ] Save/load integrity unaffected by visual pass.

## Screenshot quality gate
- [ ] Before/after screenshot pair shows clear visible improvement from Phase 31 to Phase 32.
