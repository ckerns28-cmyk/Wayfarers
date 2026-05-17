# G-4.19 Player Visual Identity Foundation

Status: `COUNCIL_PASS_READY_FOR_PR` under the autonomous pre-G-5 production protocol.

G-4.19 replaces the drawn scale/debug player placeholder with a source-authored directional player sprite foundation. The active player now has a real runtime atlas, contact sheet, manifest, QA report, and animation contract for idle/walk in four directions.

## Scope

- Active player sprite foundation: `player_wayfarer_foundation_g419`.
- Runtime animations: `idle_down`, `idle_up`, `idle_left`, `idle_right`, `walk_down`, `walk_up`, `walk_left`, `walk_right`.
- Integration target: `Player.tscn` uses an `AnimatedSprite2D` visual node; `Player.gd` drives facing and walk/idle state while preserving camera, collision, spawn, and interaction hooks.
- Provenance: project-owned deterministic source-authored art. No yellow review pixels, third-party pixels, web-scraped pixels, or marketplace material are used.
- Commercial status: approved temporary foundation only; not final-commercial promoted.

## Art Direction

The player reads as a Newport harbor-town wayfarer: muted navy coat, leather boots, cream shirt, satchel, teal scarf accent, and grounded human scale. The silhouette is intentionally restrained so later equipment, outfits, tools, NPC differentiation, and multiplayer readability can extend the same frame contract.

## Evidence Package

- Atlas: `wayfarer_godot_vertical_slice/art_pipeline/player_identity/atlases/player_wayfarer_foundation_g419_v1.png`.
- Contact sheet: `wayfarer_godot_vertical_slice/art_pipeline/player_identity/contact_sheets/player_wayfarer_foundation_g419_contact_sheet.png`.
- Manifest: `wayfarer_godot_vertical_slice/art_pipeline/player_identity/manifests/player_wayfarer_foundation_g419_manifest.json`.
- QA report: `wayfarer_godot_vertical_slice/art_pipeline/player_identity/reports/player_wayfarer_foundation_g419_extraction_qa.json`.
- Style tokens: `wayfarer_godot_vertical_slice/art_pipeline/player_identity/source_authored/g419_player_identity_style_tokens.json`.
- Screenshot wrapper: `wayfarer_godot_vertical_slice/tools/capture_g419_runtime_screenshots.ps1`.

## Completion Bar

G-4.19 passed its completion bar. Validators passed, mandatory runtime screenshots were generated and inspected, and the Agent Council assigned `COUNCIL_PASS_READY_FOR_PR`.

## Validation And Council Result

- G-4.19 player identity validation: PASS.
- Godot import validation: PASS.
- Vertical slice validation: PASS.
- Newport provenance validation: PASS.
- Retained G-4.18E asset-family validation: PASS.
- Retained G-4.21A extraction validation: PASS via non-mutating `--validate-only`.
- Runtime screenshot capture: PASS, 13 required frames.
- Agent Council report: `docs/reports/G419_PLAYER_VISUAL_IDENTITY_AGENT_COUNCIL_REPORT.md`.
- Final authority verdict: `COUNCIL_PASS_READY_FOR_PR`.
- Human escalation required: NO.
- Next recommended roadmap phase: G-4.20 HUD/UI Visual Redesign.
