#!/usr/bin/env python3
"""Validate the G-4.19 player visual identity foundation."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from PIL import Image


PHASE = "G-4.19"
FAMILY_ID = "player_wayfarer_foundation_g419"
REQUIRED_ANIMATIONS = [
    "idle_down",
    "idle_up",
    "idle_left",
    "idle_right",
    "walk_down",
    "walk_up",
    "walk_left",
    "walk_right",
]
REQUIRED_FRAME_IDS = [
    "idle_down",
    "walk_a_down",
    "walk_b_down",
    "idle_up",
    "walk_a_up",
    "walk_b_up",
    "idle_left",
    "walk_a_left",
    "walk_b_left",
    "idle_right",
    "walk_a_right",
    "walk_b_right",
]

SCRIPT_PATH = Path(__file__).resolve()
PLAYER_ROOT = SCRIPT_PATH.parents[1]
PROJECT_ROOT = PLAYER_ROOT.parents[1]
REPO_ROOT = PROJECT_ROOT.parent

ATLAS_PATH = PLAYER_ROOT / "atlases" / "player_wayfarer_foundation_g419_v1.png"
CONTACT_SHEET_PATH = PLAYER_ROOT / "contact_sheets" / "player_wayfarer_foundation_g419_contact_sheet.png"
MANIFEST_PATH = PLAYER_ROOT / "manifests" / "player_wayfarer_foundation_g419_manifest.json"
QA_REPORT_PATH = PLAYER_ROOT / "reports" / "player_wayfarer_foundation_g419_extraction_qa.json"
STYLE_TOKENS_PATH = PLAYER_ROOT / "source_authored" / "g419_player_identity_style_tokens.json"
BRIEF_PATH = PLAYER_ROOT / "source_authored" / "g419_player_visual_identity_brief.md"
GENERATOR_PATH = PLAYER_ROOT / "scripts" / "generate_g419_player_identity_assets.py"
PLAYER_SCENE_PATH = PROJECT_ROOT / "scenes" / "player" / "Player.tscn"
PLAYER_SCRIPT_PATH = PROJECT_ROOT / "scenes" / "player" / "Player.gd"
BUILD_INFO_PATH = PROJECT_ROOT / "scripts" / "BuildInfo.gd"
REGISTRY_PATH = PROJECT_ROOT / "art_pipeline" / "newport" / "manifests" / "newport_visual_production_registry.json"
PHASE_REPORT_PATH = REPO_ROOT / "docs" / "reports" / "G419_PLAYER_VISUAL_IDENTITY_FOUNDATION.md"


def rel(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def load_json(path: Path, failures: list[str]) -> Any:
    if not path.exists():
        failures.append(f"missing {rel(path)}")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        failures.append(f"invalid json {rel(path)}: {exc}")
        return None


def require_path(path: Path, failures: list[str]) -> None:
    if not path.exists():
        failures.append(f"missing {rel(path)}")


def check_image(path: Path, failures: list[str], expected_size: tuple[int, int] | None = None) -> Image.Image | None:
    require_path(path, failures)
    if not path.exists():
        return None
    try:
        image = Image.open(path).convert("RGBA")
    except OSError as exc:
        failures.append(f"could not open image {rel(path)}: {exc}")
        return None
    if expected_size and image.size != expected_size:
        failures.append(f"{rel(path)} size {image.size} != {expected_size}")
    alpha = image.getchannel("A")
    bbox = alpha.getbbox()
    if bbox is None:
        failures.append(f"{rel(path)} is fully transparent")
    elif bbox[0] < 0 or bbox[1] < 0 or bbox[2] > image.width or bbox[3] > image.height:
        failures.append(f"{rel(path)} alpha bounds out of range")
    return image


def check_manifest(failures: list[str]) -> None:
    manifest = load_json(MANIFEST_PATH, failures)
    if not isinstance(manifest, dict):
        return
    if manifest.get("schema_id") != "wayfarer.player_identity.g419.manifest.v1":
        failures.append("G-4.19 manifest schema mismatch")
    if manifest.get("phase") != PHASE:
        failures.append("G-4.19 manifest phase mismatch")
    if manifest.get("family_id") != FAMILY_ID:
        failures.append("G-4.19 manifest family mismatch")
    if manifest.get("commercial_use_status") == "final_commercial_green":
        failures.append("G-4.19 player must not be final-commercial promoted")
    for bool_key in [
        "source_pixels_from_yellow_uncertain_assets",
        "source_pixels_from_third_party_material",
        "web_scraped_source_pixels",
    ]:
        if manifest.get(bool_key) is not False:
            failures.append(f"G-4.19 manifest must mark {bool_key}=false")
    animations = manifest.get("animations", {})
    if not isinstance(animations, dict):
        failures.append("G-4.19 manifest animations must be an object")
        animations = {}
    for animation in REQUIRED_ANIMATIONS:
        if animation not in animations:
            failures.append(f"G-4.19 manifest missing animation {animation}")
    frames = manifest.get("frames", [])
    if not isinstance(frames, list):
        failures.append("G-4.19 manifest frames must be a list")
        frames = []
    frame_ids = {str(frame.get("id", "")) for frame in frames if isinstance(frame, dict)}
    for frame_id in REQUIRED_FRAME_IDS:
        if frame_id not in frame_ids:
            failures.append(f"G-4.19 manifest missing frame {frame_id}")
    for field in ["runtime_asset", "source_grid", "contact_sheet", "style_tokens", "brief", "generation_script", "validation_script"]:
        value = str(manifest.get(field, ""))
        if not value:
            failures.append(f"G-4.19 manifest missing {field}")
        elif not (PROJECT_ROOT / value).exists():
            failures.append(f"G-4.19 manifest path missing {field}: {value}")


def check_qa(failures: list[str]) -> None:
    qa = load_json(QA_REPORT_PATH, failures)
    if not isinstance(qa, dict):
        return
    if qa.get("schema_id") != "wayfarer.player_identity.g419.extraction_qa.v1":
        failures.append("G-4.19 QA schema mismatch")
    if qa.get("phase") != PHASE or qa.get("family_id") != FAMILY_ID:
        failures.append("G-4.19 QA phase/family mismatch")
    if qa.get("status") != "PASS":
        failures.append("G-4.19 QA status must be PASS")
    if int(qa.get("frames_checked", 0)) != 12:
        failures.append("G-4.19 QA must check 12 frames")
    provenance = qa.get("provenance", {})
    if not isinstance(provenance, dict):
        failures.append("G-4.19 QA provenance must be object")
        return
    if provenance.get("project_owned_deterministic_source") is not True:
        failures.append("G-4.19 QA must mark project-owned deterministic source")
    for key in ["third_party_pixels", "yellow_review_pixels", "web_scraped_pixels", "final_commercial_promoted"]:
        if provenance.get(key) is not False:
            failures.append(f"G-4.19 QA provenance must mark {key}=false")


def check_registry(failures: list[str]) -> None:
    registry = load_json(REGISTRY_PATH, failures)
    if not isinstance(registry, dict):
        return
    if registry.get("phase") != PHASE:
        failures.append("visual production registry phase must be G-4.19")
    policy = str(registry.get("policy", ""))
    for required in ["G-4.19", "Player Visual Identity Foundation", "not final-commercial promoted", "old drawn player placeholder is deprecated"]:
        if required not in policy:
            failures.append(f"visual production registry G-4.19 policy missing: {required}")
    entries = registry.get("asset_entries", [])
    if not isinstance(entries, list):
        failures.append("visual production registry entries must be list")
        return
    by_id = {str(entry.get("asset_id", "")): entry for entry in entries if isinstance(entry, dict)}
    player = by_id.get(FAMILY_ID)
    if not isinstance(player, dict):
        failures.append("G-4.19 player asset missing from visual production registry")
        return
    usage = player.get("current_usage", {})
    if not isinstance(usage, dict) or usage.get("normal_review") is not True:
        failures.append("G-4.19 player asset must be active for normal review")
    if player.get("rebuild_status") != "APPROVED_TEMPORARY":
        failures.append("G-4.19 player rebuild status must be APPROVED_TEMPORARY")
    provenance = player.get("provenance_detail", {})
    if not isinstance(provenance, dict):
        failures.append("G-4.19 player provenance detail missing")
    else:
        if provenance.get("project_owned_deterministic_source") is not True:
            failures.append("G-4.19 player registry must mark deterministic source")
        for key in ["source_pixels_from_yellow_uncertain_assets", "source_pixels_from_third_party_material", "web_scraped_source_pixels", "final_commercial_promoted"]:
            if provenance.get(key) is not False:
                failures.append(f"G-4.19 player registry must mark {key}=false")
    placeholder = by_id.get("player_placeholder_drawn")
    if not isinstance(placeholder, dict):
        failures.append("historical player placeholder entry missing")
    else:
        placeholder_usage = placeholder.get("current_usage", {})
        if isinstance(placeholder_usage, dict) and placeholder_usage.get("normal_review") is True:
            failures.append("drawn player placeholder must not remain normal-review")
        if placeholder.get("rebuild_status") != "DEPRECATED_DO_NOT_USE":
            failures.append("drawn player placeholder must be deprecated")


def check_runtime_integration(failures: list[str]) -> None:
    for path in [PLAYER_SCENE_PATH, PLAYER_SCRIPT_PATH, BUILD_INFO_PATH, PHASE_REPORT_PATH, STYLE_TOKENS_PATH, BRIEF_PATH, GENERATOR_PATH]:
        require_path(path, failures)
    if PLAYER_SCENE_PATH.exists():
        scene = PLAYER_SCENE_PATH.read_text(encoding="utf-8")
        if 'node name="Visual" type="AnimatedSprite2D"' not in scene:
            failures.append("Player.tscn must include Visual AnimatedSprite2D")
    if PLAYER_SCRIPT_PATH.exists():
        script = PLAYER_SCRIPT_PATH.read_text(encoding="utf-8")
        for required in [
            "PLAYER_SPRITE_ATLAS_PATH",
            "player_wayfarer_foundation_g419_v1.png",
            "func set_review_visual_state",
            "_configure_visual_sprite",
            "_update_visual_animation",
        ]:
            if required not in script:
                failures.append(f"Player.gd missing {required}")
        for forbidden in ["draw_circle(", "draw_rect(", "draw_line("]:
            if forbidden in script:
                failures.append(f"Player.gd still uses drawn placeholder primitive: {forbidden}")
    if BUILD_INFO_PATH.exists():
        build_info = BUILD_INFO_PATH.read_text(encoding="utf-8")
        if "PLAYER_STYLE_ROADMAP_NOTE" not in build_info:
            failures.append("BuildInfo.gd must retain the player/style roadmap note hook")
        if "player" not in build_info.lower() and "wayfarer" not in build_info.lower():
            failures.append("BuildInfo.gd should still describe the player-facing Wayfarer presentation")


def main() -> int:
    failures: list[str] = []
    atlas = check_image(ATLAS_PATH, failures, (192, 256))
    check_image(CONTACT_SHEET_PATH, failures)
    if atlas:
        frame_alpha_failures = 0
        for row in range(4):
            for col in range(3):
                frame = atlas.crop((col * 64, row * 64, (col + 1) * 64, (row + 1) * 64))
                alpha = frame.getchannel("A")
                bbox = alpha.getbbox()
                if bbox is None:
                    frame_alpha_failures += 1
                elif bbox[0] < 8 or bbox[1] < 4 or bbox[2] > 56 or bbox[3] > 62:
                    frame_alpha_failures += 1
        if frame_alpha_failures:
            failures.append(f"{frame_alpha_failures} G-4.19 player frames have unsafe alpha bounds")
    check_manifest(failures)
    check_qa(failures)
    check_registry(failures)
    check_runtime_integration(failures)
    if failures:
        print("FAIL: G-4.19 player identity validation")
        for failure in failures:
            print(" - " + failure)
        return 1
    print("PASS: G-4.19 player identity validation")
    print(f"Atlas: {rel(ATLAS_PATH)}")
    print(f"Contact sheet: {rel(CONTACT_SHEET_PATH)}")
    print(f"Manifest: {rel(MANIFEST_PATH)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
