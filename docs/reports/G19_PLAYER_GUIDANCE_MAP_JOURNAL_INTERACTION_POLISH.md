# G-19 Player Guidance, Map, Journal, and Interaction Polish

Phase: `G-19`
Branch: `codex/g-19-player-guidance-map-journal-interaction-polish`
Status: `PASS` pending PR

## Summary

G-19 makes the rebuilt G-19S Newport layout readable to a first-session player without debug UI. The HUD now names the player's current town band, the journal includes a compact route line, and objective copy uses the approved harborfront road, Counting House, wharf apron, Tavern/Inn, rear service lane, and east island-exit geography.

This is not an OVI-1 production-playable claim. It is the guidance polish gate between the source-driven Newport reconstruction and the G-20 fun/reward loop pass.

## Player Guidance Result

- The first objective now tells the player to follow the harborfront road to Edrin Vale at the Counting House.
- Journal route hints change with objective state: wharf apron, merchant row, civic notice board, Tavern/Inn, rear service lane, east guidepost, old road marker, hidden landing, and return/report routes.
- The HUD location label updates from world position, including `Working Wharf Apron`, `Harborfront Road`, `Counting House Steps`, `Tavern/Inn Quarter`, `Commercial Avenue`, `Rear Service Lane`, and `East Road - Island Exit`.
- Interaction targeting now gives NPCs priority over nearby building doors so Edrin, Bess, and other quest NPCs do not lose focus to adjacent facade prompts.
- No debug-looking prompts: normal prompt copy remains compact (`E: Talk - ...`, `E: Enter - ...`) and avoids `Press E` world text.

## Source And Proof

- Guidance source: `wayfarer_godot_vertical_slice/data/ux/g19_player_guidance_map_journal_interaction_v1.json`
- G-19S runtime layout source: `wayfarer_godot_vertical_slice/data/world_layout/g19s_newport_runtime_reconstruction_v1.json`
- Capture manifest: `wayfarer_godot_vertical_slice/artifacts/review/g19_player_guidance_screenshots/g19_player_guidance_screenshot_manifest.json`
- Screenshot proof: 10 HUD-visible guidance views, including arrival route, counting-house prompt/update, wharf lantern, tavern whisper, commercial branch, rear service secret, island exit, return route, and debug-disabled guidance view.

## Validation

- `validate_g19_player_guidance_map_journal_interaction.py` - PASS
- `validate_first_session_gameplay_loop.py` - PASS
- `validate_interaction_ux.py` - PASS
- `validate_newport_layout_source_alignment.py` - PASS
- `validate_opening_village_island_roadmap.py` - PASS
- `validate_opening_village_island_execution_ledger.py` - PASS
- `validate_vertical_slice.gd` - PASS
- `capture_g19_player_guidance_screenshots.ps1` - PASS

## Scores

- ux_readability_score: 8.6
- Player orientation score: 8.6
- Quest-geography integration score: 8.6
- Technical stability score: 8.7

## Residual Work

G-20 must make the first-session loop fun, rewarded, and paced, rather than merely readable. G-19 proves the player can understand where to go; G-20 must prove they want to keep going.
