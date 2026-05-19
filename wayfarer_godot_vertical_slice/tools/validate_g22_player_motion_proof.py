#!/usr/bin/env python3
"""Validate the G-22 OVI-1 player motion proof.

This deliberately checks for the failure Chris called out: a static player
sprite translating across the map. The proof must show actual displacement,
distinct walk frames, body offset changes, and shadow pulse changes.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROJECT_ROOT.parent
PLAYER_GD = PROJECT_ROOT / "scenes" / "player" / "Player.gd"
CAPTURE_GD = PROJECT_ROOT / "tools" / "capture_g22_player_motion_proof.gd"
PROOF_DIR = PROJECT_ROOT / "artifacts" / "review" / "g22_ovi1_motion_proof"
MANIFEST = PROOF_DIR / "g22_player_motion_proof_manifest.json"
CONTACT_SHEET = PROOF_DIR / "g22_player_motion_contact_sheet.png"
CLEAR_WATERFRONT_AVENUE_Y_RANGE = (580.0, 660.0)


def load_json(path: Path, failures: list[str]) -> dict[str, Any] | None:
    if not path.exists():
        failures.append(f"Missing JSON artifact: {relative(path)}")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        failures.append(f"Invalid JSON {relative(path)}: {exc}")
    return None


def relative(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def require_text(path: Path, tokens: list[str], failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"Missing source file: {relative(path)}")
        return ""
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        if token not in text:
            failures.append(f"{relative(path)} missing token: {token}")
    return text


def main() -> int:
    failures: list[str] = []
    require_text(
        PLAYER_GD,
        [
            "G22_PLAYER_MOTION_CORRECTIVE_PASS",
            "PLAYER_GLIDE_GUARD_POLICY",
            "player_motion_corrective_contract",
            "player_motion_debug_state",
            "_last_actual_displacement",
            "_sync_walk_frame_from_distance",
            "_apply_locomotion_pose",
        ],
        failures,
    )
    require_text(
        CAPTURE_GD,
        [
            "START_POSITION := Vector2(675.0, 612.0)",
            "clear waterfront avenue lane",
        ],
        failures,
    )
    manifest = load_json(MANIFEST, failures)
    if isinstance(manifest, dict):
        if manifest.get("schema_id") != "wayfarer.g22.player_motion_proof.v1":
            failures.append("G-22 player motion manifest schema mismatch")
        if manifest.get("phase") != "G-22":
            failures.append("G-22 player motion manifest phase mismatch")
        if manifest.get("status") != "PASS":
            failures.append(f"G-22 player motion manifest is not PASS: {manifest.get('status')}")
        if "clear waterfront avenue lane" not in str(manifest.get("proof_intent", "")):
            failures.append("G-22 player motion proof must record that the lane is clear waterfront avenue, not roof")
        contract = manifest.get("player_motion_contract", {})
        if not isinstance(contract, dict) or contract.get("no_static_sprite_glide") is not True:
            failures.append("G-22 player motion contract does not assert no_static_sprite_glide")
        if isinstance(contract, dict) and contract.get("animation_frame_source") != "actual_move_and_slide_displacement":
            failures.append("G-22 player motion contract must be driven by actual move_and_slide displacement")
        sequence = manifest.get("frame_sequence", [])
        if not isinstance(sequence, list) or len(sequence) < 6:
            failures.append("G-22 player motion proof must include at least six frame samples")
        else:
            for frame in sequence:
                if not isinstance(frame, dict):
                    failures.append("G-22 player motion frame entry is not an object")
                    continue
                frame_path = PROJECT_ROOT / str(frame.get("path", "")).replace("res://", "")
                if not frame_path.exists():
                    failures.append(f"G-22 player motion frame missing: {relative(frame_path)}")
                if frame.get("status") != "PASS":
                    failures.append(f"G-22 player motion frame not PASS: {frame.get('filename')}")
                state = frame.get("player_state", {})
                if isinstance(state, dict):
                    position = state.get("global_position", {})
                    if isinstance(position, dict):
                        y = float(position.get("y", 0.0))
                        if not (CLEAR_WATERFRONT_AVENUE_Y_RANGE[0] <= y <= CLEAR_WATERFRONT_AVENUE_Y_RANGE[1]):
                            failures.append(f"G-22 player motion frame left the clear waterfront avenue lane: {frame.get('filename')}")
        evaluation = manifest.get("motion_evaluation", {})
        if not isinstance(evaluation, dict):
            failures.append("G-22 player motion evaluation is missing")
        else:
            if evaluation.get("status") != "PASS":
                failures.append(f"G-22 player motion evaluation is not PASS: {evaluation.get('failure')}")
            checks = {
                "total_position_delta_px": 70.0,
                "unique_animation_frames": 3,
                "unique_visual_offsets": 3,
                "unique_shadow_scales": 2,
                "moving_animation_samples": 5,
                "nonzero_actual_displacement_samples": 5,
            }
            for key, minimum in checks.items():
                value = evaluation.get(key, 0)
                if isinstance(minimum, float):
                    if float(value) < minimum:
                        failures.append(f"G-22 player motion evaluation {key} below {minimum}: {value}")
                elif int(value) < minimum:
                    failures.append(f"G-22 player motion evaluation {key} below {minimum}: {value}")
            if evaluation.get("no_static_sprite_translation") is not True:
                failures.append("G-22 player motion evaluation did not reject static-sprite translation")
        contact = manifest.get("contact_sheet", {})
        if not CONTACT_SHEET.exists():
            failures.append(f"G-22 player motion contact sheet missing: {relative(CONTACT_SHEET)}")
        if not isinstance(contact, dict) or contact.get("status") != "PASS":
            failures.append("G-22 player motion contact sheet is not PASS in manifest")
    if failures:
        print("FAIL: G-22 player motion proof")
        for failure in failures:
            print(" - " + failure)
        return 1
    print("PASS: G-22 player motion proof")
    print(f"manifest={relative(MANIFEST)}")
    print(f"contact_sheet={relative(CONTACT_SHEET)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
