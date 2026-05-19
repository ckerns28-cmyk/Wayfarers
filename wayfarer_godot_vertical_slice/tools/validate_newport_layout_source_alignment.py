#!/usr/bin/env python3
"""Guard future Newport runtime layout changes against source-of-truth bypass."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from opening_village_island_validator_common import PROJECT_ROOT, REPO_ROOT, load_json, print_result, require_path


SOURCE_JSON = REPO_ROOT / "docs" / "design" / "NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.json"
ARTIFACT_DIR = PROJECT_ROOT / "artifacts" / "planning" / "g19r_newport_blockout"
MANIFEST = ARTIFACT_DIR / "g19r_newport_blockout_manifest.json"

SOURCE_PATH_PREFIXES = (
    "docs/design/NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH",
    "wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/",
    "wayfarer_godot_vertical_slice/data/world_layout/g19s_newport_runtime_reconstruction_v1.json",
)

MAJOR_RUNTIME_LAYOUT_PATHS = (
    "wayfarer_godot_vertical_slice/scripts/NewportTownBlueprint.gd",
    "wayfarer_godot_vertical_slice/scenes/map/MapLayer.gd",
    "wayfarer_godot_vertical_slice/scenes/Main.gd",
    "wayfarer_godot_vertical_slice/data/world_layout/",
)

MINOR_DOCUMENTATION_PATHS = (
    "docs/reports/",
    "docs/roadmaps/",
)

NON_LAYOUT_RUNTIME_CONTRACT_PATHS = {
    "wayfarer_godot_vertical_slice/scenes/Main.gd",
}

NON_LAYOUT_RUNTIME_TOKEN_GROUPS = (
    (
        "player_guidance_polish_contract",
        "set_player_world_position",
        "source_runtime_layout",
    ),
    (
        "first_session_gameplay_loop_reward_contract",
        "source_loop",
        "reward_feedback_visible",
        "quest_geography_loop",
    ),
)

LAYOUT_MUTATION_TOKENS = (
    "NEWPORT_TOWN.",
    "MapLayer.",
    "Rect2(",
    "Vector2(",
    "road",
    "street",
    "lot",
    "district",
    "wharf",
    "building",
    "spawn",
    "add_child(",
)


def main() -> int:
    failures: list[str] = []
    require_path(SOURCE_JSON, failures, "Newport layout source of truth JSON")
    require_path(MANIFEST, failures, "G-19R blockout manifest")
    source = load_json(SOURCE_JSON, failures)
    manifest = load_json(MANIFEST, failures)
    if isinstance(source, dict):
        validate_source(source, failures)
    if isinstance(manifest, dict):
        validate_manifest(manifest, failures)
    validate_git_alignment(failures)
    return print_result("Newport layout source alignment", failures)


def validate_source(source: dict[str, Any], failures: list[str]) -> None:
    if source.get("phase") != "G-19R":
        failures.append("Newport source-of-truth phase must be G-19R")
    governance = source.get("future_placement_governance", {})
    if not isinstance(governance, dict):
        failures.append("Newport source-of-truth missing future_placement_governance")
        return
    if governance.get("major_layout_files_guarded") in (None, []):
        failures.append("Newport source-of-truth governance missing guarded file list")
    if "major Newport street, lot, district, wharf, NPC route, quest beat, or camera placement changes" not in str(governance.get("rule", "")):
        failures.append("Newport source-of-truth governance must explicitly guard major placement changes")
    if "G-19S" not in str(governance.get("g19s_requirement", "")):
        failures.append("Newport source-of-truth governance must name G-19S consumption requirement")


def validate_manifest(manifest: dict[str, Any], failures: list[str]) -> None:
    if manifest.get("future_placement_governance_present") is not True:
        failures.append("G-19R manifest must record future_placement_governance_present=true")
    if manifest.get("source_of_truth") != "docs/design/NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.json":
        failures.append("G-19R manifest source_of_truth path mismatch")
    artifact_paths = [str(item.get("path", "")) for item in manifest.get("artifacts", []) if isinstance(item, dict)]
    required = [
        "g19r_newport_measured_blockout.svg",
        "g19r_newport_measured_blockout.png",
        "g19r_newport_street_hierarchy.json",
        "g19r_newport_lot_plan.json",
        "g19r_newport_camera_viewpoints.json",
    ]
    for name in required:
        if not any(path.endswith(name) for path in artifact_paths):
            failures.append(f"G-19R manifest missing source artifact for future alignment: {name}")


def changed_paths() -> set[str]:
    paths: set[str] = set()
    commands = [
        ["git", "diff", "--name-only", "origin/main...HEAD"],
        ["git", "diff", "--name-only"],
        ["git", "diff", "--name-only", "--cached"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    ]
    for args in commands:
        result = subprocess.run(args, cwd=REPO_ROOT, text=True, capture_output=True, check=False)
        if result.returncode != 0:
            continue
        paths.update(line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip())
    return paths


def combined_diff(path: str) -> str:
    chunks: list[str] = []
    commands = [
        ["git", "diff", "--unified=0", "origin/main...HEAD", "--", path],
        ["git", "diff", "--unified=0", "--", path],
        ["git", "diff", "--unified=0", "--cached", "--", path],
    ]
    for args in commands:
        result = subprocess.run(args, cwd=REPO_ROOT, text=True, capture_output=True, check=False)
        if result.returncode == 0 and result.stdout:
            chunks.append(result.stdout)
    return "\n".join(chunks)


def is_non_layout_runtime_contract_change(path: str) -> bool:
    if path not in NON_LAYOUT_RUNTIME_CONTRACT_PATHS:
        return False
    diff_text = combined_diff(path)
    if not diff_text:
        return False
    changed_lines = []
    for line in diff_text.splitlines():
        if line.startswith(("+++", "---", "@@")):
            continue
        if line.startswith(("+", "-")):
            changed_lines.append(line[1:])
    changed_text = "\n".join(changed_lines)
    if not any(all(token in changed_text for token in token_group) for token_group in NON_LAYOUT_RUNTIME_TOKEN_GROUPS):
        return False
    layout_terms = [
        token
        for token in LAYOUT_MUTATION_TOKENS
        if token in changed_text and token not in ("source_runtime_layout",)
    ]
    return not layout_terms


def matches_any(path: str, prefixes: tuple[str, ...]) -> bool:
    return any(path == prefix or path.startswith(prefix) for prefix in prefixes)


def validate_git_alignment(failures: list[str]) -> None:
    changed = changed_paths()
    if not changed:
        return
    major_runtime_changes = sorted(
        path
        for path in changed
        if matches_any(path, MAJOR_RUNTIME_LAYOUT_PATHS)
        and not is_non_layout_runtime_contract_change(path)
    )
    source_changes = sorted(path for path in changed if matches_any(path, SOURCE_PATH_PREFIXES))
    if major_runtime_changes and not source_changes:
        failures.append(
            "Major Newport runtime layout changes were detected without source-of-truth updates: "
            + ", ".join(major_runtime_changes)
        )
    code_layout_changes = [
        path
        for path in major_runtime_changes
        if not matches_any(path, MINOR_DOCUMENTATION_PATHS)
    ]
    if code_layout_changes and source_changes:
        source_names = " ".join(source_changes)
        for required in [
            "g19r_newport_street_hierarchy.json",
            "g19r_newport_lot_plan.json",
            "g19r_newport_camera_viewpoints.json",
        ]:
            if required not in source_names and not (ARTIFACT_DIR / required).exists():
                failures.append(f"Major runtime layout change requires source artifact: {required}")


if __name__ == "__main__":
    sys.exit(main())
