# G-4.22R Pre-G-5 Atelier Consistency Gate Repair

- Previous gate result: `COUNCIL_PASS_READY_FOR_PR`.
- Current status after new screenshot evidence: `COUNCIL_FAIL_NEEDS_CODE_FIX` until this remediation validates.
- Human review required: no.
- Action: Codex must fix autonomously with runtime asset replacement, provenance, screenshots, validators, and council audit.
- Reason: runtime visual evidence showed non-atelier / placeholder / style-inconsistent playable hero-slice sprites.
- Rejected attempt: a deterministic geometric G-4.22R scratch pack was created during remediation and rejected by visual QA as far below atelier standard.
- Accepted replacement path: painterly AI-assisted source sheet, local chroma-key extraction, manifest-backed runtime atlases, and runtime validation.

Deprecated final states are not used here: `NEEDS_HUMAN_REVIEW`, `READY_FOR_HUMAN_VISUAL_REVIEW`, `AWAITING_CHRIS_REVIEW`, `VISUAL_REVIEW_REQUIRED`, and `TECHNICAL_PASS_ONLY` remain invalid for this ordinary pre-G-5 repair.

## Runtime Asset Repair

- Player atlas: `wayfarer_godot_vertical_slice/art_pipeline/player_identity/atlases/player_wayfarer_atelier_g422r_v1.png`.
- NPC atlas: `wayfarer_godot_vertical_slice/art_pipeline/player_identity/atlases/newport_npc_atelier_g422r_v1.png`.
- Source sheet: `wayfarer_godot_vertical_slice/art_pipeline/player_identity/source_generated/g422r_atelier_characters_source_imagegen.png`.
- Source prompt: `wayfarer_godot_vertical_slice/art_pipeline/player_identity/source_generated/g422r_atelier_characters_prompt.txt`.
- Contact sheet: `wayfarer_godot_vertical_slice/art_pipeline/player_identity/contact_sheets/newport_atelier_characters_g422r_contact_sheet.png`.

## Runtime Failures Repaired

- Player runtime atlas no longer points at the lower-quality G-4.19 foundation for normal gate review.
- Edrin Vale no longer draws a primitive placeholder humanoid in `_draw()`.
- Newport normal-play NPC anchors are classified as `npc_atelier`, not `npc_placeholder`.
- Normal G-4.10+ prop drawing no longer renders crude sign posts or humanoid placeholders in the main hero-slice view.
- Low-bar marker/sign assets, blank notice-board style props, primitive bench/lantern/signpost props, and normal-play layout-guide overlays are hidden until they have atelier-standard replacements.
