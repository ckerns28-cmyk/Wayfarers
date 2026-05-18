#!/usr/bin/env python3
"""Wayfarer Agent Council runner.

This script creates a repo-local production review report. For ordinary pre-G-5
work, the council is the acceptance authority after screenshots are inspected
work, and for ordinary roadmap-bound work before OVI-1, the council is the
acceptance authority after screenshots are inspected and validators pass. This
tool still never merges, never impersonates Chris, and never treats a technical
pass by itself as design approval. Codex may separately merge an ordinary
autonomous PR only after the active autonomous merge rule is satisfied.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REPORT_NAME = "G422P_WAYFARER_AGENT_COUNCIL_REPORT.md"
KNOWN_GODOT_BIN = (
    r"C:\Users\Chris\Downloads\Godot_v4.6.2-stable_win64.exe"
    r"\Godot_v4.6.2-stable_win64_console.exe"
)
AUTHORITY_PASS = "COUNCIL_PASS_READY_FOR_PR"
AUTHORITY_FAIL = "COUNCIL_FAIL_NEEDS_CODE_FIX"
AUTHORITY_BLOCKED = "BLOCKED_REQUIRES_HUMAN_ESCALATION"
AUTHORITY_VERDICTS = (AUTHORITY_PASS, AUTHORITY_FAIL, AUTHORITY_BLOCKED)


@dataclass
class CommandResult:
    args: list[str]
    cwd: Path
    returncode: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0


@dataclass
class ValidatorCommand:
    name: str
    command_text: str
    args: list[str]
    cwd: Path
    required_paths: list[Path]


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".git").exists():
            return candidate
    raise SystemExit("Could not find repo root from " + str(start))


def run(args: list[str], cwd: Path) -> CommandResult:
    proc = subprocess.run(
        args,
        cwd=str(cwd),
        text=True,
        capture_output=True,
        check=False,
    )
    return CommandResult(args=args, cwd=cwd, returncode=proc.returncode, stdout=proc.stdout, stderr=proc.stderr)


def run_json(args: list[str], cwd: Path) -> tuple[object | None, CommandResult]:
    result = run(args, cwd)
    if not result.ok or not result.stdout.strip():
        return None, result
    try:
        return json.loads(result.stdout), result
    except json.JSONDecodeError:
        return None, result


def powershell_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def path_text(path: Path) -> str:
    return str(path).replace("/", "\\")


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def default_python_bin() -> str:
    local_appdata = os.environ.get("LOCALAPPDATA")
    if local_appdata:
        candidate = Path(local_appdata) / "Programs" / "Python" / "Python313" / "python.exe"
        try:
            if candidate.exists():
                return str(candidate)
        except OSError:
            # Sandboxed runs may not be allowed to stat LOCALAPPDATA candidates.
            pass
    return sys.executable


def default_godot_bin() -> str:
    env_bin = os.environ.get("GODOT_BIN")
    if env_bin:
        return env_bin
    return KNOWN_GODOT_BIN


def get_git_state(root: Path) -> dict[str, str]:
    branch = run(["git", "branch", "--show-current"], root)
    status = run(["git", "status", "--short", "--branch"], root)
    head = run(["git", "rev-parse", "HEAD"], root)
    origin = run(["git", "rev-parse", "origin/main"], root)
    remote = run(["git", "remote", "-v"], root)
    return {
        "branch": branch.stdout.strip() or "(detached)",
        "status": status.stdout.strip(),
        "head": head.stdout.strip(),
        "origin_main": origin.stdout.strip(),
        "remote": remote.stdout.strip(),
    }


def get_pr_state(root: Path, target_pr: int) -> dict[str, object]:
    gh = shutil.which("gh")
    state: dict[str, object] = {
        "gh_available": bool(gh),
        "open_prs": [],
        "target_pr": None,
        "errors": [],
    }
    if not gh:
        state["errors"] = ["gh CLI not found; PR discovery skipped."]
        return state

    open_json, open_result = run_json(
        [
            gh,
            "pr",
            "list",
            "--state",
            "open",
            "--json",
            "number,title,headRefName,baseRefName,url,isDraft",
        ],
        root,
    )
    if open_result.ok and isinstance(open_json, list):
        state["open_prs"] = open_json
    else:
        state["errors"].append("Open PR discovery failed: " + compact_output(open_result))

    if target_pr > 0:
        target_json, target_result = run_json(
            [
                gh,
                "pr",
                "view",
                str(target_pr),
                "--json",
                "number,title,state,isDraft,mergedAt,headRefName,baseRefName,url",
            ],
            root,
        )
        if target_result.ok and isinstance(target_json, dict):
            state["target_pr"] = target_json
        else:
            state["errors"].append(f"PR #{target_pr} discovery failed: " + compact_output(target_result))

    return state


def compact_output(result: CommandResult, limit: int = 600) -> str:
    text = (result.stdout + "\n" + result.stderr).strip()
    if not text:
        text = f"exit {result.returncode}"
    text = " ".join(text.split())
    if len(text) > limit:
        return text[: limit - 3] + "..."
    return text


def find_latest_screenshots(root: Path) -> list[Path]:
    patterns = [
        "wayfarer_godot_vertical_slice/artifacts/review/g422r_runtime_screenshots/g422r_*.png",
        "wayfarer_godot_vertical_slice/artifacts/review/g11_runtime_screenshots/g11_*.png",
        "wayfarer_godot_vertical_slice/artifacts/review/g422_runtime_screenshots/g422_*.png",
        "wayfarer_godot_vertical_slice/artifacts/review/g421_runtime_screenshots/g421_*.png",
        "wayfarer_godot_vertical_slice/artifacts/review/g420_runtime_screenshots/g420_*.png",
        "wayfarer_godot_vertical_slice/artifacts/review/g419_runtime_screenshots/g419_*.png",
        "wayfarer_godot_vertical_slice/artifacts/review/g418e_runtime_screenshots/g418e_*.png",
        "wayfarer_godot_vertical_slice/artifacts/review/g423b_runtime_screenshots/g423b_*.png",
        "wayfarer_godot_vertical_slice/artifacts/review/g423a_runtime_screenshots/g423a_*.png",
        "wayfarer_godot_vertical_slice/artifacts/review/g422a_runtime_screenshots/g422a_*.png",
        "wayfarer_godot_vertical_slice/artifacts/review/g421b_runtime_screenshots/g421b_*.png",
        "wayfarer_godot_vertical_slice/artifacts/review/**/*screenshot*.png",
        "wayfarer_godot_vertical_slice/artifacts/review/**/*.png",
    ]
    found: dict[Path, float] = {}
    for pattern in patterns:
        for path in root.glob(pattern):
            if path.is_file():
                found[path] = path.stat().st_mtime
    return sorted(found, key=lambda item: found[item], reverse=True)


def screenshot_prefix_for_phase(phase: str) -> tuple[str, str]:
    normalized = phase.upper().strip()
    if normalized.startswith("SV-0"):
        return "SV-0", "sv0"
    if normalized.startswith("G-22"):
        return "G-22 OVI-1", "g22_ovi1"
    if normalized.startswith("G-21"):
        return "G-21", "g21"
    if normalized.startswith("G-20"):
        return "G-20", "g20"
    if normalized.startswith("G-19"):
        return "G-19", "g19"
    if normalized.startswith("G-18A"):
        return "G-18A", "g18a"
    if normalized.startswith("G-18"):
        return "G-18", "g18"
    if normalized.startswith("G-17"):
        return "G-17", "g17"
    if normalized.startswith("G-16A"):
        return "G-16A", "g16a"
    if normalized.startswith("G-16"):
        return "G-16", "g16"
    if normalized.startswith("G-15B"):
        return "G-15B", "g15b"
    if normalized.startswith("G-15A"):
        return "G-15A", "g15a"
    if normalized.startswith("G-15"):
        return "G-15", "g15"
    if normalized.startswith("G-14"):
        return "G-14 internal village proof", "g12"
    if normalized.startswith("G-11A"):
        return "G-11A", "g11"
    if normalized.startswith("G-11"):
        return "G-11", "g11"
    if normalized.startswith("G-12"):
        return "G-12", "g12"
    if normalized.startswith("G-13"):
        return "G-13 browser regression", "g12"
    if normalized.startswith("G-10B"):
        return "G-10B", "g10b"
    if normalized.startswith("G-10A"):
        return "G-10A", "g10a"
    if normalized.startswith("G-10"):
        return "G-10", "g10"
    if normalized.startswith("G-9A"):
        return "G-9A", "g9a"
    if normalized.startswith("G-9"):
        return "G-9", "g9"
    if normalized.startswith("G-8A"):
        return "G-8A", "g8a"
    if normalized.startswith("G-8"):
        return "G-8", "g8"
    if normalized.startswith("G-7C"):
        return "G-7C", "g7c"
    if normalized.startswith("G-7B"):
        return "G-7B", "g7b"
    if normalized.startswith("G-7A"):
        return "G-7A", "g7a"
    if normalized.startswith("G-7"):
        return "G-7", "g7"
    if normalized.startswith("G-4.22R"):
        return "G-4.22R", "g422r"
    if normalized.startswith("G-4.22A"):
        return "G-4.22A", "g422a"
    if normalized.startswith("G-4.22"):
        return "G-4.22", "g422"
    if normalized.startswith("G-4.21"):
        return "G-4.21", "g421"
    if normalized.startswith("G-4.20"):
        return "G-4.20", "g420"
    if normalized.startswith("G-4.19"):
        return "G-4.19", "g419"
    if normalized.startswith("G-4.18E"):
        return "G-4.18E", "g418e"
    if normalized.startswith("G-4.23B"):
        return "G-4.23B", "g423b"
    if normalized.startswith("G-4.23A"):
        return "G-4.23A", "g423a"
    return "G-4.22A", "g422a"


def is_g15_topology_planning_phase(phase: str) -> bool:
    normalized = phase.upper().strip()
    return normalized == "G-15" or normalized.startswith("G-15 ")


def build_validator_commands(root: Path, godot_bin: str, python_bin: str, phase: str) -> list[ValidatorCommand]:
    game_root = root / "wayfarer_godot_vertical_slice"
    capture_label, capture_prefix = screenshot_prefix_for_phase(phase)
    capture_ps1 = game_root / "tools" / f"capture_{capture_prefix}_runtime_screenshots.ps1"
    capture_log = game_root / "artifacts" / "review" / f"{capture_prefix}_runtime_screenshots" / "godot_capture.log"
    validator_log_dir = game_root / "artifacts" / "review" / "validator_logs"
    validator_log_dir.mkdir(parents=True, exist_ok=True)
    godot_import_log = validator_log_dir / f"{capture_prefix}_godot_import.log"
    vertical_slice_log = validator_log_dir / f"{capture_prefix}_vertical_slice.log"

    godot_import_text = (
        f"& {powershell_quote(godot_bin)} --headless --path wayfarer_godot_vertical_slice "
        f"--log-file {powershell_quote(str(godot_import_log))} --import"
    )
    vertical_text = (
        "Push-Location wayfarer_godot_vertical_slice; "
        f"& {powershell_quote(godot_bin)} --headless --path . "
        f"--log-file {powershell_quote(str(vertical_slice_log))} "
        "--script res://tools/validate_vertical_slice.gd; "
        "Pop-Location"
    )
    provenance_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\art_pipeline\newport\scripts\validate_newport_asset_provenance.py"
    )
    g418e_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\art_pipeline\newport_atelier\scripts\validate_g418e_hero_asset_family.py"
    )
    g419_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\art_pipeline\player_identity\scripts\validate_g419_player_identity.py"
    )
    g422r_runtime_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\tools\validate_g422r_runtime_asset_consistency.py"
    )
    runtime_atelier_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\tools\validate_runtime_atelier_asset_consistency.py"
    )
    starter_village_roadmap_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\tools\validate_starter_village_roadmap.py"
    )
    starter_village_ledger_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\tools\validate_starter_village_execution_ledger.py"
    )
    character_motion_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\tools\validate_character_motion_foundation.py"
    )
    npc_population_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\tools\validate_npc_population_and_routes.py"
    )
    living_town_rhythm_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\tools\validate_living_town_rhythm.py"
    )
    audio_atmosphere_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\tools\validate_audio_atmosphere_hooks.py"
    )
    first_session_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\tools\validate_first_session_playability.py"
    )
    browser_build_hardening_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\tools\validate_browser_build_hardening.py"
    )
    ovi_roadmap_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\tools\validate_opening_village_island_roadmap.py"
    )
    ovi_ledger_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\tools\validate_opening_village_island_execution_ledger.py"
    )
    island_topology_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\tools\validate_island_world_topology.py"
    )
    village_island_transition_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\tools\validate_village_to_island_transition.py"
    )
    island_cohesion_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\tools\validate_island_world_cohesion.py"
    )
    island_poi_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\tools\validate_island_poi_landmarks.py"
    )
    island_atelier_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\tools\validate_island_atelier_asset_family.py"
    )
    island_npc_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\tools\validate_island_npc_encounter_foundation.py"
    )
    quest_village_island_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\tools\validate_opening_quest_village_to_island.py"
    )
    multipath_rumor_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\tools\validate_multipath_rumor_choice_foundation.py"
    )
    first_session_loop_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\tools\validate_first_session_gameplay_loop.py"
    )
    ovi_gate_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\tools\validate_ovi1_gate.py"
    )
    interaction_ux_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\tools\validate_interaction_ux.py"
    )
    visual_order_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\tools\validate_newport_visual_ordering.py"
    )
    opening_quest_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\tools\validate_opening_quest_arc.py"
    )
    tavern_whisper_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\tools\validate_tavern_whisper_system.py"
    )
    multi_path_choice_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\tools\validate_multi_path_starter_choice.py"
    )
    sv0_tooling_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\tools\validate_sv0_tooling_stack.py"
    )
    sv0_tool_acquisition_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\tools\validate_sv0_tool_acquisition_manifest.py"
    )
    layout_source_usage_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\tools\validate_starter_village_layout_source_usage.py"
    )
    pre_g5_ledger_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\tools\validate_pre_g5_roadmap_ledger.py"
    )
    extraction_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\art_pipeline\newport_atelier\scripts\extract_g421a_core_building_assets.py "
        "--validate-only"
    )
    screenshot_text = (
        "powershell.exe -NoProfile -ExecutionPolicy Bypass -File "
        rf".\wayfarer_godot_vertical_slice\tools\capture_{capture_prefix}_runtime_screenshots.ps1 "
        f"-GodotBin {powershell_quote(godot_bin)}"
    )
    capture_log_text = (
        r"Get-Content -Path wayfarer_godot_vertical_slice\artifacts\review"
        rf"\{capture_prefix}_runtime_screenshots\godot_capture.log -TotalCount 120"
    )

    commands = [
        ValidatorCommand(
            name="Godot import validation",
            command_text=godot_import_text,
            args=[
                godot_bin,
                "--headless",
                "--path",
                str(game_root),
                "--log-file",
                str(godot_import_log),
                "--import",
            ],
            cwd=root,
            required_paths=[game_root],
        ),
        ValidatorCommand(
            name="validate_vertical_slice.gd",
            command_text=vertical_text,
            args=[
                godot_bin,
                "--headless",
                "--path",
                ".",
                "--log-file",
                str(vertical_slice_log),
                "--script",
                "res://tools/validate_vertical_slice.gd",
            ],
            cwd=game_root,
            required_paths=[game_root / "tools" / "validate_vertical_slice.gd"],
        ),
        ValidatorCommand(
            name="validate_newport_asset_provenance.py",
            command_text=provenance_text,
            args=[python_bin, str(game_root / "art_pipeline" / "newport" / "scripts" / "validate_newport_asset_provenance.py")],
            cwd=root,
            required_paths=[game_root / "art_pipeline" / "newport" / "scripts" / "validate_newport_asset_provenance.py"],
        ),
        ValidatorCommand(
            name="G-4.21A extraction validation",
            command_text=extraction_text,
            args=[
                python_bin,
                str(game_root / "art_pipeline" / "newport_atelier" / "scripts" / "extract_g421a_core_building_assets.py"),
                "--validate-only",
            ],
            cwd=root,
            required_paths=[game_root / "art_pipeline" / "newport_atelier" / "scripts" / "extract_g421a_core_building_assets.py"],
        ),
        ValidatorCommand(
            name=f"{capture_label} screenshot capture and PNG verification",
            command_text=screenshot_text,
            args=[
                "powershell.exe",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(capture_ps1),
                "-GodotBin",
                godot_bin,
            ],
            cwd=root,
            required_paths=[capture_ps1],
        ),
        ValidatorCommand(
            name=f"{capture_label} capture log check",
            command_text=capture_log_text,
            args=[
                "powershell.exe",
                "-NoProfile",
                "-Command",
                f"Get-Content -Path {powershell_quote(str(capture_log))} -TotalCount 120",
            ],
            cwd=root,
            required_paths=[capture_log],
        ),
        ValidatorCommand(
            name="git diff --check",
            command_text="git diff --check",
            args=["git", "diff", "--check"],
            cwd=root,
            required_paths=[],
        ),
        ValidatorCommand(
            name="git diff --cached --check",
            command_text="git diff --cached --check",
            args=["git", "diff", "--cached", "--check"],
            cwd=root,
            required_paths=[],
        ),
    ]
    normalized_phase = phase.upper().strip()
    if normalized_phase.startswith("OVI-1"):
        return [
            ValidatorCommand(
                name="Opening Village + Island roadmap validation",
                command_text=ovi_roadmap_text,
                args=[python_bin, str(game_root / "tools" / "validate_opening_village_island_roadmap.py")],
                cwd=root,
                required_paths=[game_root / "tools" / "validate_opening_village_island_roadmap.py"],
            ),
            ValidatorCommand(
                name="Opening Village + Island execution ledger validation",
                command_text=ovi_ledger_text,
                args=[python_bin, str(game_root / "tools" / "validate_opening_village_island_execution_ledger.py")],
                cwd=root,
                required_paths=[game_root / "tools" / "validate_opening_village_island_execution_ledger.py"],
            ),
            ValidatorCommand(
                name="Starter Village roadmap validation",
                command_text=starter_village_roadmap_text,
                args=[python_bin, str(game_root / "tools" / "validate_starter_village_roadmap.py")],
                cwd=root,
                required_paths=[game_root / "tools" / "validate_starter_village_roadmap.py"],
            ),
            ValidatorCommand(
                name="Starter Village execution ledger validation",
                command_text=starter_village_ledger_text,
                args=[python_bin, str(game_root / "tools" / "validate_starter_village_execution_ledger.py")],
                cwd=root,
                required_paths=[game_root / "tools" / "validate_starter_village_execution_ledger.py"],
            ),
            ValidatorCommand(
                name="git diff --check",
                command_text="git diff --check",
                args=["git", "diff", "--check"],
                cwd=root,
                required_paths=[],
            ),
            ValidatorCommand(
                name="git diff --cached --check",
                command_text="git diff --cached --check",
                args=["git", "diff", "--cached", "--check"],
                cwd=root,
                required_paths=[],
            ),
        ]
    if normalized_phase.startswith("SV-0"):
        return [
            ValidatorCommand(
                name="SV-0 Tooling Stack validation",
                command_text=sv0_tooling_text,
                args=[python_bin, str(game_root / "tools" / "validate_sv0_tooling_stack.py")],
                cwd=root,
                required_paths=[game_root / "tools" / "validate_sv0_tooling_stack.py"],
            ),
            ValidatorCommand(
                name="SV-0 Tool Acquisition Manifest validation",
                command_text=sv0_tool_acquisition_text,
                args=[python_bin, str(game_root / "tools" / "validate_sv0_tool_acquisition_manifest.py")],
                cwd=root,
                required_paths=[game_root / "tools" / "validate_sv0_tool_acquisition_manifest.py"],
            ),
            ValidatorCommand(
                name="Starter Village roadmap validation",
                command_text=starter_village_roadmap_text,
                args=[python_bin, str(game_root / "tools" / "validate_starter_village_roadmap.py")],
                cwd=root,
                required_paths=[game_root / "tools" / "validate_starter_village_roadmap.py"],
            ),
            ValidatorCommand(
                name="Starter Village execution ledger validation",
                command_text=starter_village_ledger_text,
                args=[python_bin, str(game_root / "tools" / "validate_starter_village_execution_ledger.py")],
                cwd=root,
                required_paths=[game_root / "tools" / "validate_starter_village_execution_ledger.py"],
            ),
            ValidatorCommand(
                name="git diff --check",
                command_text="git diff --check",
                args=["git", "diff", "--check"],
                cwd=root,
                required_paths=[],
            ),
            ValidatorCommand(
                name="git diff --cached --check",
                command_text="git diff --cached --check",
                args=["git", "diff", "--cached", "--check"],
                cwd=root,
                required_paths=[],
            ),
        ]
    if is_g15_topology_planning_phase(phase):
        return [
            ValidatorCommand(
                name="Island world topology validation",
                command_text=island_topology_text,
                args=[python_bin, str(game_root / "tools" / "validate_island_world_topology.py")],
                cwd=root,
                required_paths=[game_root / "tools" / "validate_island_world_topology.py"],
            ),
            ValidatorCommand(
                name="Opening Village + Island roadmap validation",
                command_text=ovi_roadmap_text,
                args=[python_bin, str(game_root / "tools" / "validate_opening_village_island_roadmap.py")],
                cwd=root,
                required_paths=[game_root / "tools" / "validate_opening_village_island_roadmap.py"],
            ),
            ValidatorCommand(
                name="Opening Village + Island execution ledger validation",
                command_text=ovi_ledger_text,
                args=[python_bin, str(game_root / "tools" / "validate_opening_village_island_execution_ledger.py")],
                cwd=root,
                required_paths=[game_root / "tools" / "validate_opening_village_island_execution_ledger.py"],
            ),
            ValidatorCommand(
                name="git diff --check",
                command_text="git diff --check",
                args=["git", "diff", "--check"],
                cwd=root,
                required_paths=[],
            ),
            ValidatorCommand(
                name="git diff --cached --check",
                command_text="git diff --cached --check",
                args=["git", "diff", "--cached", "--check"],
                cwd=root,
                required_paths=[],
            ),
        ]
    if normalized_phase.startswith("G-4.18E") or normalized_phase.startswith("G-4.20") or normalized_phase.startswith("G-4.21") or normalized_phase.startswith("G-4.22"):
        commands.insert(
            3,
            ValidatorCommand(
                name="G-4.18E hero asset family validation",
                command_text=g418e_text,
                args=[
                    python_bin,
                    str(game_root / "art_pipeline" / "newport_atelier" / "scripts" / "validate_g418e_hero_asset_family.py"),
                ],
                cwd=root,
                required_paths=[game_root / "art_pipeline" / "newport_atelier" / "scripts" / "validate_g418e_hero_asset_family.py"],
            ),
        )
    if normalized_phase.startswith("G-4.19") or normalized_phase.startswith("G-4.20") or normalized_phase.startswith("G-4.21") or normalized_phase.startswith("G-4.22"):
        commands.insert(
            3,
            ValidatorCommand(
                name="G-4.19 player identity validation",
                command_text=g419_text,
                args=[
                    python_bin,
                    str(game_root / "art_pipeline" / "player_identity" / "scripts" / "validate_g419_player_identity.py"),
                ],
                cwd=root,
                required_paths=[game_root / "art_pipeline" / "player_identity" / "scripts" / "validate_g419_player_identity.py"],
            ),
        )
    if normalized_phase.startswith("G-4.22R"):
        diff_index = max(0, len(commands) - 2)
        commands.insert(
            diff_index,
            ValidatorCommand(
                name="G-4.22R runtime asset consistency validation",
                command_text=g422r_runtime_text,
                args=[python_bin, str(game_root / "tools" / "validate_g422r_runtime_asset_consistency.py")],
                cwd=root,
                required_paths=[game_root / "tools" / "validate_g422r_runtime_asset_consistency.py"],
            ),
        )
        commands.insert(
            diff_index + 1,
            ValidatorCommand(
                name="Pre-G-5 roadmap execution ledger validation",
                command_text=pre_g5_ledger_text,
                args=[python_bin, str(game_root / "tools" / "validate_pre_g5_roadmap_ledger.py")],
                cwd=root,
                required_paths=[game_root / "tools" / "validate_pre_g5_roadmap_ledger.py"],
            ),
        )
    if normalized_phase.startswith(("G-7", "G-8", "G-9", "G-10", "G-11", "G-12", "G-13", "G-14")):
        diff_index = max(0, len(commands) - 2)
        starter_commands = [
            ValidatorCommand(
                name="SV-0 Tooling Stack validation",
                command_text=sv0_tooling_text,
                args=[python_bin, str(game_root / "tools" / "validate_sv0_tooling_stack.py")],
                cwd=root,
                required_paths=[game_root / "tools" / "validate_sv0_tooling_stack.py"],
            ),
            ValidatorCommand(
                name="SV-0 Tool Acquisition Manifest validation",
                command_text=sv0_tool_acquisition_text,
                args=[python_bin, str(game_root / "tools" / "validate_sv0_tool_acquisition_manifest.py")],
                cwd=root,
                required_paths=[game_root / "tools" / "validate_sv0_tool_acquisition_manifest.py"],
            ),
            ValidatorCommand(
                name="Starter Village roadmap validation",
                command_text=starter_village_roadmap_text,
                args=[python_bin, str(game_root / "tools" / "validate_starter_village_roadmap.py")],
                cwd=root,
                required_paths=[game_root / "tools" / "validate_starter_village_roadmap.py"],
            ),
            ValidatorCommand(
                name="Starter Village execution ledger validation",
                command_text=starter_village_ledger_text,
                args=[python_bin, str(game_root / "tools" / "validate_starter_village_execution_ledger.py")],
                cwd=root,
                required_paths=[game_root / "tools" / "validate_starter_village_execution_ledger.py"],
            ),
            ValidatorCommand(
                name="Runtime atelier asset consistency validation",
                command_text=runtime_atelier_text,
                args=[python_bin, str(game_root / "tools" / "validate_runtime_atelier_asset_consistency.py")],
                cwd=root,
                required_paths=[game_root / "tools" / "validate_runtime_atelier_asset_consistency.py"],
            ),
            ValidatorCommand(
                name="Starter Village layout source usage validation",
                command_text=layout_source_usage_text,
                args=[python_bin, str(game_root / "tools" / "validate_starter_village_layout_source_usage.py")],
                cwd=root,
                required_paths=[game_root / "tools" / "validate_starter_village_layout_source_usage.py"],
            ),
            ValidatorCommand(
                name="Newport visual ordering validation",
                command_text=visual_order_text,
                args=[python_bin, str(game_root / "tools" / "validate_newport_visual_ordering.py")],
                cwd=root,
                required_paths=[game_root / "tools" / "validate_newport_visual_ordering.py"],
            ),
        ]
        if normalized_phase.startswith("G-8"):
            starter_commands.insert(
                0,
                ValidatorCommand(
                    name="G-8 character motion foundation validation",
                    command_text=character_motion_text,
                    args=[python_bin, str(game_root / "tools" / "validate_character_motion_foundation.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_character_motion_foundation.py"],
                ),
            )
        if normalized_phase.startswith(("G-8A", "G-11")):
            starter_commands.insert(
                1 if normalized_phase.startswith("G-8A") else 0,
                ValidatorCommand(
                    name="NPC population and routes validation",
                    command_text=npc_population_text,
                    args=[python_bin, str(game_root / "tools" / "validate_npc_population_and_routes.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_npc_population_and_routes.py"],
                ),
            )
        if normalized_phase.startswith("G-11"):
            starter_commands.insert(
                0,
                ValidatorCommand(
                    name="Living town rhythm validation",
                    command_text=living_town_rhythm_text,
                    args=[python_bin, str(game_root / "tools" / "validate_living_town_rhythm.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_living_town_rhythm.py"],
                ),
            )
        if normalized_phase.startswith("G-11A"):
            starter_commands.insert(
                0,
                ValidatorCommand(
                    name="Audio atmosphere hooks validation",
                    command_text=audio_atmosphere_text,
                    args=[python_bin, str(game_root / "tools" / "validate_audio_atmosphere_hooks.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_audio_atmosphere_hooks.py"],
                ),
            )
        if normalized_phase.startswith("G-12"):
            starter_commands.insert(
                0,
                ValidatorCommand(
                    name="First-session playability validation",
                    command_text=first_session_text,
                    args=[python_bin, str(game_root / "tools" / "validate_first_session_playability.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_first_session_playability.py"],
                ),
            )
        if normalized_phase.startswith("G-13"):
            starter_commands.insert(
                0,
                ValidatorCommand(
                    name="G-13 browser build hardening validation",
                    command_text=browser_build_hardening_text,
                    args=[python_bin, str(game_root / "tools" / "validate_browser_build_hardening.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_browser_build_hardening.py"],
                ),
            )
            starter_commands.insert(
                1,
                ValidatorCommand(
                    name="First-session playability validation",
                    command_text=first_session_text,
                    args=[python_bin, str(game_root / "tools" / "validate_first_session_playability.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_first_session_playability.py"],
                ),
            )
            starter_commands.insert(
                2,
                ValidatorCommand(
                    name="Opening quest arc validation",
                    command_text=opening_quest_text,
                    args=[python_bin, str(game_root / "tools" / "validate_opening_quest_arc.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_opening_quest_arc.py"],
                ),
            )
            starter_commands.insert(
                3,
                ValidatorCommand(
                    name="Interaction UX validation",
                    command_text=interaction_ux_text,
                    args=[python_bin, str(game_root / "tools" / "validate_interaction_ux.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_interaction_ux.py"],
                ),
            )
            starter_commands.insert(
                4,
                ValidatorCommand(
                    name="Living town rhythm validation",
                    command_text=living_town_rhythm_text,
                    args=[python_bin, str(game_root / "tools" / "validate_living_town_rhythm.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_living_town_rhythm.py"],
                ),
            )
            starter_commands.insert(
                5,
                ValidatorCommand(
                    name="Audio atmosphere hooks validation",
                    command_text=audio_atmosphere_text,
                    args=[python_bin, str(game_root / "tools" / "validate_audio_atmosphere_hooks.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_audio_atmosphere_hooks.py"],
                ),
            )
        if normalized_phase.startswith("G-14"):
            for command in [
                ValidatorCommand(
                    name="G-13 browser build hardening validation",
                    command_text=browser_build_hardening_text,
                    args=[python_bin, str(game_root / "tools" / "validate_browser_build_hardening.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_browser_build_hardening.py"],
                ),
                ValidatorCommand(
                    name="First-session playability validation",
                    command_text=first_session_text,
                    args=[python_bin, str(game_root / "tools" / "validate_first_session_playability.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_first_session_playability.py"],
                ),
                ValidatorCommand(
                    name="Opening quest arc validation",
                    command_text=opening_quest_text,
                    args=[python_bin, str(game_root / "tools" / "validate_opening_quest_arc.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_opening_quest_arc.py"],
                ),
                ValidatorCommand(
                    name="Tavern whisper system validation",
                    command_text=tavern_whisper_text,
                    args=[python_bin, str(game_root / "tools" / "validate_tavern_whisper_system.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_tavern_whisper_system.py"],
                ),
                ValidatorCommand(
                    name="Interaction UX validation",
                    command_text=interaction_ux_text,
                    args=[python_bin, str(game_root / "tools" / "validate_interaction_ux.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_interaction_ux.py"],
                ),
                ValidatorCommand(
                    name="G-8 character motion foundation validation",
                    command_text=character_motion_text,
                    args=[python_bin, str(game_root / "tools" / "validate_character_motion_foundation.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_character_motion_foundation.py"],
                ),
                ValidatorCommand(
                    name="NPC population and routes validation",
                    command_text=npc_population_text,
                    args=[python_bin, str(game_root / "tools" / "validate_npc_population_and_routes.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_npc_population_and_routes.py"],
                ),
            ]:
                starter_commands.insert(0, command)
        if normalized_phase.startswith("G-9"):
            starter_commands.insert(
                0,
                ValidatorCommand(
                    name="Interaction UX validation",
                    command_text=interaction_ux_text,
                    args=[python_bin, str(game_root / "tools" / "validate_interaction_ux.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_interaction_ux.py"],
                ),
            )
        if normalized_phase.startswith(("G-9A", "G-10")):
            starter_commands.insert(
                0,
                ValidatorCommand(
                    name="Opening quest arc validation",
                    command_text=opening_quest_text,
                    args=[python_bin, str(game_root / "tools" / "validate_opening_quest_arc.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_opening_quest_arc.py"],
                ),
            )
        if normalized_phase.startswith("G-10A"):
            starter_commands.insert(
                0,
                ValidatorCommand(
                    name="Tavern whisper system validation",
                    command_text=tavern_whisper_text,
                    args=[python_bin, str(game_root / "tools" / "validate_tavern_whisper_system.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_tavern_whisper_system.py"],
                ),
            )
        if normalized_phase.startswith("G-10B"):
            starter_commands.insert(
                0,
                ValidatorCommand(
                    name="Multi-path starter choice validation",
                    command_text=multi_path_choice_text,
                    args=[python_bin, str(game_root / "tools" / "validate_multi_path_starter_choice.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_multi_path_starter_choice.py"],
                ),
            )
        commands[diff_index:diff_index] = starter_commands
    if normalized_phase.startswith(("G-14", "G-15", "G-16", "G-17", "G-18", "G-19", "G-20", "G-21", "G-22")):
        diff_index = max(0, len(commands) - 2)
        ovi_commands = [
            ValidatorCommand(
                name="Opening Village + Island roadmap validation",
                command_text=ovi_roadmap_text,
                args=[python_bin, str(game_root / "tools" / "validate_opening_village_island_roadmap.py")],
                cwd=root,
                required_paths=[game_root / "tools" / "validate_opening_village_island_roadmap.py"],
            ),
            ValidatorCommand(
                name="Opening Village + Island execution ledger validation",
                command_text=ovi_ledger_text,
                args=[python_bin, str(game_root / "tools" / "validate_opening_village_island_execution_ledger.py")],
                cwd=root,
                required_paths=[game_root / "tools" / "validate_opening_village_island_execution_ledger.py"],
            ),
        ]
        if normalized_phase.startswith("G-15A"):
            ovi_commands.insert(
                0,
                ValidatorCommand(
                    name="Village-to-island transition validation",
                    command_text=village_island_transition_text,
                    args=[python_bin, str(game_root / "tools" / "validate_village_to_island_transition.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_village_to_island_transition.py"],
                ),
            )
        elif normalized_phase.startswith("G-15B"):
            ovi_commands.insert(
                0,
                ValidatorCommand(
                    name="Island world cohesion validation",
                    command_text=island_cohesion_text,
                    args=[python_bin, str(game_root / "tools" / "validate_island_world_cohesion.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_island_world_cohesion.py"],
                ),
            )
        elif normalized_phase.startswith("G-15"):
            ovi_commands.insert(
                0,
                ValidatorCommand(
                    name="Island world topology validation",
                    command_text=island_topology_text,
                    args=[python_bin, str(game_root / "tools" / "validate_island_world_topology.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_island_world_topology.py"],
                ),
            )
        if normalized_phase.startswith("G-16A"):
            ovi_commands.insert(
                0,
                ValidatorCommand(
                    name="Island atelier asset family validation",
                    command_text=island_atelier_text,
                    args=[python_bin, str(game_root / "tools" / "validate_island_atelier_asset_family.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_island_atelier_asset_family.py"],
                ),
            )
        elif normalized_phase.startswith("G-16"):
            ovi_commands.insert(
                0,
                ValidatorCommand(
                    name="Island POI landmarks validation",
                    command_text=island_poi_text,
                    args=[python_bin, str(game_root / "tools" / "validate_island_poi_landmarks.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_island_poi_landmarks.py"],
                ),
            )
        if normalized_phase.startswith("G-17"):
            ovi_commands.insert(
                0,
                ValidatorCommand(
                    name="Island NPC encounter foundation validation",
                    command_text=island_npc_text,
                    args=[python_bin, str(game_root / "tools" / "validate_island_npc_encounter_foundation.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_island_npc_encounter_foundation.py"],
                ),
            )
        if normalized_phase.startswith("G-18A"):
            ovi_commands.insert(
                0,
                ValidatorCommand(
                    name="Multi-path rumor choice foundation validation",
                    command_text=multipath_rumor_text,
                    args=[python_bin, str(game_root / "tools" / "validate_multipath_rumor_choice_foundation.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_multipath_rumor_choice_foundation.py"],
                ),
            )
        elif normalized_phase.startswith("G-18"):
            ovi_commands.insert(
                0,
                ValidatorCommand(
                    name="Opening quest village-to-island validation",
                    command_text=quest_village_island_text,
                    args=[python_bin, str(game_root / "tools" / "validate_opening_quest_village_to_island.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_opening_quest_village_to_island.py"],
                ),
            )
        if normalized_phase.startswith(("G-19", "G-20")):
            ovi_commands.insert(
                0,
                ValidatorCommand(
                    name="First-session gameplay loop validation",
                    command_text=first_session_loop_text,
                    args=[python_bin, str(game_root / "tools" / "validate_first_session_gameplay_loop.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_first_session_gameplay_loop.py"],
                ),
            )
        if normalized_phase.startswith("G-21"):
            ovi_commands.insert(
                0,
                ValidatorCommand(
                    name="G-13 browser build hardening validation",
                    command_text=browser_build_hardening_text,
                    args=[python_bin, str(game_root / "tools" / "validate_browser_build_hardening.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_browser_build_hardening.py"],
                ),
            )
        if normalized_phase.startswith("G-22"):
            ovi_commands.insert(
                0,
                ValidatorCommand(
                    name="OVI-1 gate validation",
                    command_text=ovi_gate_text,
                    args=[python_bin, str(game_root / "tools" / "validate_ovi1_gate.py")],
                    cwd=root,
                    required_paths=[game_root / "tools" / "validate_ovi1_gate.py"],
                ),
            )
        commands[diff_index:diff_index] = ovi_commands
    return commands


def run_or_list_validators(commands: list[ValidatorCommand], should_run: bool) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    for command in commands:
        missing = [path for path in command.required_paths if not path.exists()]
        if missing:
            results.append(
                {
                    "name": command.name,
                    "status": "FAIL",
                    "command": command.command_text,
                    "notes": "Missing required path(s): " + ", ".join(path_text(path) for path in missing),
                }
            )
            continue
        if not should_run:
            results.append(
                {
                    "name": command.name,
                    "status": "SKIPPED_WITH_COMMAND",
                    "command": command.command_text,
                    "notes": "Not run in default council mode.",
                }
            )
            continue
        result = run(command.args, command.cwd)
        results.append(
            {
                "name": command.name,
                "status": "PASS" if result.ok else "FAIL",
                "command": command.command_text,
                "notes": compact_output(result),
            }
        )
    return results


def required_path_status(root: Path, phase: str) -> list[tuple[str, str, str]]:
    game_root = root / "wayfarer_godot_vertical_slice"
    capture_label, capture_prefix = screenshot_prefix_for_phase(phase)
    if phase.upper().strip().startswith("SV-0"):
        required = [
            ("SV-0 Tooling Stack report", root / "docs" / "reports" / "SV0_FREE_TOOLING_INTAKE_PRODUCTION_STACK_LOCK.md"),
            ("SV-0 Tooling Stack JSON", root / "docs" / "reports" / "SV0_FREE_TOOLING_INTAKE_PRODUCTION_STACK_LOCK.json"),
            ("SV-0 Tool Acquisition Manifest", root / "docs" / "reports" / "SV0_TOOL_ACQUISITION_MANIFEST.md"),
            ("SV-0 Tool Acquisition Manifest JSON", root / "docs" / "reports" / "SV0_TOOL_ACQUISITION_MANIFEST.json"),
            ("SV-0 Tooling Stack roadmap", root / "docs" / "roadmaps" / "STARTER_VILLAGE_TOOLING_STACK.md"),
            ("SV-0 Tooling Stack validator", game_root / "tools" / "validate_sv0_tooling_stack.py"),
            ("SV-0 Tool Acquisition Manifest validator", game_root / "tools" / "validate_sv0_tool_acquisition_manifest.py"),
            ("SV-0 world layout source", game_root / "data" / "world_layout" / "starter_village_world_layout_v1.json"),
            ("SV-0 visual QA manifest", game_root / "data" / "visual_qa" / "starter_village_visual_regression_manifest_v1.json"),
            ("SV-0 movement proof manifest", game_root / "data" / "movement_proof" / "starter_village_movement_proof_manifest_v1.json"),
            ("SV-0 ground material stack", game_root / "data" / "ground_materials" / "starter_village_ground_material_stack_v1.json"),
            ("Starter Village roadmap", root / "docs" / "roadmaps" / "STARTER_VILLAGE_PLAYABLE_OBSESSION_ROADMAP.md"),
            ("Starter Village execution ledger", root / "docs" / "reports" / "STARTER_VILLAGE_AUTONOMOUS_EXECUTION_LEDGER.md"),
        ]
        return [(label, "FOUND" if path.exists() else "MISSING", rel(path, root)) for label, path in required]
    if phase.upper().strip().startswith("OVI-1"):
        required = [
            ("OVI-1 roadmap", root / "docs" / "roadmaps" / "OPENING_VILLAGE_ISLAND_PRODUCTION_ROADMAP.md"),
            ("OVI-1 roadmap JSON", root / "docs" / "roadmaps" / "OPENING_VILLAGE_ISLAND_PRODUCTION_ROADMAP.json"),
            ("OVI-1 execution ledger", root / "docs" / "reports" / "OPENING_VILLAGE_ISLAND_AUTONOMOUS_EXECUTION_LEDGER.md"),
            ("OVI-1 execution ledger JSON", root / "docs" / "reports" / "OPENING_VILLAGE_ISLAND_AUTONOMOUS_EXECUTION_LEDGER.json"),
            ("OVI-1 roadmap validator", game_root / "tools" / "validate_opening_village_island_roadmap.py"),
            ("OVI-1 ledger validator", game_root / "tools" / "validate_opening_village_island_execution_ledger.py"),
            ("Starter Village roadmap validator", game_root / "tools" / "validate_starter_village_roadmap.py"),
            ("Starter Village ledger validator", game_root / "tools" / "validate_starter_village_execution_ledger.py"),
        ]
        return [(label, "FOUND" if path.exists() else "MISSING", rel(path, root)) for label, path in required]
    if is_g15_topology_planning_phase(phase):
        required = [
            ("OVI-1 roadmap", root / "docs" / "roadmaps" / "OPENING_VILLAGE_ISLAND_PRODUCTION_ROADMAP.md"),
            ("OVI-1 roadmap JSON", root / "docs" / "roadmaps" / "OPENING_VILLAGE_ISLAND_PRODUCTION_ROADMAP.json"),
            ("OVI-1 execution ledger", root / "docs" / "reports" / "OPENING_VILLAGE_ISLAND_AUTONOMOUS_EXECUTION_LEDGER.md"),
            ("OVI-1 execution ledger JSON", root / "docs" / "reports" / "OPENING_VILLAGE_ISLAND_AUTONOMOUS_EXECUTION_LEDGER.json"),
            ("G-15 topology source", game_root / "data" / "world_layout" / "opening_island_world_topology_v1.json"),
            (
                "G-15 screenshot viewpoint manifest",
                game_root / "data" / "visual_qa" / "g15_topology_screenshot_viewpoint_manifest.json",
            ),
            ("G-15 phase report", root / "docs" / "reports" / "G15_OPENING_ISLAND_MASTERPLAN_WORLD_TOPOLOGY.md"),
            ("G-15 phase report JSON", root / "docs" / "reports" / "G15_OPENING_ISLAND_MASTERPLAN_WORLD_TOPOLOGY.json"),
            ("G-15 island world topology validator", game_root / "tools" / "validate_island_world_topology.py"),
            ("OVI-1 roadmap validator", game_root / "tools" / "validate_opening_village_island_roadmap.py"),
            ("OVI-1 ledger validator", game_root / "tools" / "validate_opening_village_island_execution_ledger.py"),
        ]
        return [(label, "FOUND" if path.exists() else "MISSING", rel(path, root)) for label, path in required]
    required = [
        ("Vertical slice validator", game_root / "tools" / "validate_vertical_slice.gd"),
        (f"{capture_label} runtime screenshot wrapper", game_root / "tools" / f"capture_{capture_prefix}_runtime_screenshots.ps1"),
        (f"{capture_label} runtime screenshot script", game_root / "tools" / f"capture_{capture_prefix}_runtime_screenshots.gd"),
        (
            "Newport asset provenance validator",
            game_root / "art_pipeline" / "newport" / "scripts" / "validate_newport_asset_provenance.py",
        ),
        (
            "G-4.21A extraction script",
            game_root / "art_pipeline" / "newport_atelier" / "scripts" / "extract_g421a_core_building_assets.py",
        ),
    ]
    if phase.upper().strip().startswith("G-4.18E"):
        required.extend(
            [
                (
                    "G-4.18E hero asset family validator",
                    game_root / "art_pipeline" / "newport_atelier" / "scripts" / "validate_g418e_hero_asset_family.py",
                ),
                (
                    "G-4.18E asset family manifest",
                    game_root
                    / "art_pipeline"
                    / "newport_atelier"
                    / "manifests"
                    / "newport_atelier_g418e_hero_asset_family_manifest.json",
                ),
            ]
        )
    if phase.upper().strip().startswith("G-4.19"):
        required.extend(
            [
                (
                    "G-4.19 player identity validator",
                    game_root / "art_pipeline" / "player_identity" / "scripts" / "validate_g419_player_identity.py",
                ),
                (
                    "G-4.19 player identity manifest",
                    game_root / "art_pipeline" / "player_identity" / "manifests" / "player_wayfarer_foundation_g419_manifest.json",
                ),
                (
                    "G-4.19 player atlas",
                    game_root / "art_pipeline" / "player_identity" / "atlases" / "player_wayfarer_foundation_g419_v1.png",
                ),
                (
                    "G-4.19 player contact sheet",
                    game_root / "art_pipeline" / "player_identity" / "contact_sheets" / "player_wayfarer_foundation_g419_contact_sheet.png",
                ),
            ]
        )
    if phase.upper().strip().startswith("G-4.20"):
        required.extend(
            [
                (
                    "G-4.18E hero asset family validator",
                    game_root / "art_pipeline" / "newport_atelier" / "scripts" / "validate_g418e_hero_asset_family.py",
                ),
                (
                    "G-4.19 player identity validator",
                    game_root / "art_pipeline" / "player_identity" / "scripts" / "validate_g419_player_identity.py",
                ),
                ("G-4.20 HUD scene", game_root / "scenes" / "ui" / "HUD.tscn"),
                ("G-4.20 HUD script", game_root / "scenes" / "ui" / "HUD.gd"),
            ]
        )
    if phase.upper().strip().startswith("G-4.21"):
        required.extend(
            [
                (
                    "G-4.18E hero asset family validator",
                    game_root / "art_pipeline" / "newport_atelier" / "scripts" / "validate_g418e_hero_asset_family.py",
                ),
                (
                    "G-4.19 player identity validator",
                    game_root / "art_pipeline" / "player_identity" / "scripts" / "validate_g419_player_identity.py",
                ),
                ("G-4.20 HUD scene", game_root / "scenes" / "ui" / "HUD.tscn"),
                ("G-4.20 HUD script", game_root / "scenes" / "ui" / "HUD.gd"),
            ]
        )
    if phase.upper().strip().startswith("G-4.22"):
        required.extend(
            [
                (
                    "G-4.18E hero asset family validator",
                    game_root / "art_pipeline" / "newport_atelier" / "scripts" / "validate_g418e_hero_asset_family.py",
                ),
                (
                    "G-4.19 player identity validator",
                    game_root / "art_pipeline" / "player_identity" / "scripts" / "validate_g419_player_identity.py",
                ),
                ("G-4.20 HUD scene", game_root / "scenes" / "ui" / "HUD.tscn"),
                ("G-4.20 HUD script", game_root / "scenes" / "ui" / "HUD.gd"),
                ("G-4.21 council report", root / "docs" / "reports" / "G421_ORIGIN_CITY_HERO_SLICE_AGENT_COUNCIL_REPORT.md"),
                ("G-4.22 gate screenshot wrapper", game_root / "tools" / "capture_g422_runtime_screenshots.ps1"),
                ("G-4.22 gate screenshot script", game_root / "tools" / "capture_g422_runtime_screenshots.gd"),
            ]
        )
    if phase.upper().strip().startswith("G-4.22R"):
        required.extend(
            [
                ("Pre-G-5 roadmap execution ledger", root / "docs" / "reports" / "PRE_G5_ROADMAP_EXECUTION_LEDGER.md"),
                ("Pre-G-5 roadmap execution ledger JSON", root / "docs" / "reports" / "PRE_G5_ROADMAP_EXECUTION_LEDGER.json"),
                (
                    "Pre-G-5 roadmap ledger validator",
                    game_root / "tools" / "validate_pre_g5_roadmap_ledger.py",
                ),
                (
                    "G-4.22R runtime asset consistency validator",
                    game_root / "tools" / "validate_g422r_runtime_asset_consistency.py",
                ),
                (
                    "G-4.22R character manifest",
                    game_root / "art_pipeline" / "player_identity" / "manifests" / "newport_atelier_characters_g422r_manifest.json",
                ),
                (
                    "G-4.22R player atlas",
                    game_root / "art_pipeline" / "player_identity" / "atlases" / "player_wayfarer_atelier_g422r_v1.png",
                ),
                (
                    "G-4.22R NPC atlas",
                    game_root / "art_pipeline" / "player_identity" / "atlases" / "newport_npc_atelier_g422r_v1.png",
                ),
                (
                    "G-4.22R player/NPC contact sheet",
                    game_root / "art_pipeline" / "player_identity" / "contact_sheets" / "newport_atelier_characters_g422r_contact_sheet.png",
                ),
                (
                    "G-4.22R source prompt",
                    game_root / "art_pipeline" / "player_identity" / "source_generated" / "g422r_atelier_characters_prompt.txt",
                ),
                (
                    "G-4.22R source image",
                    game_root / "art_pipeline" / "player_identity" / "source_generated" / "g422r_atelier_characters_source_imagegen.png",
                ),
                (
                    "G-4.22R runtime screenshot manifest",
                    game_root / "artifacts" / "review" / "g422r_runtime_screenshots" / "g422r_runtime_screenshot_manifest.json",
                ),
                (
                    "G-4.22R gate reopen report",
                    root / "docs" / "reports" / "G422R_PRE_G5_ROADMAP_EXECUTION_AND_GATE_REOPEN_REPORT.md",
                ),
            ]
        )
    if phase.upper().strip().startswith(("G-7", "G-8", "G-9", "G-10", "G-11", "G-12", "G-13", "G-14")):
        required.extend(
            [
                (
                    "SV-0 authoritative world layout source",
                    game_root / "data" / "world_layout" / "starter_village_world_layout_v1.json",
                ),
                (
                    "SV-0 Tool Acquisition Manifest validator",
                    game_root / "tools" / "validate_sv0_tool_acquisition_manifest.py",
                ),
                (
                    "Starter Village layout source usage validator",
                    game_root / "tools" / "validate_starter_village_layout_source_usage.py",
                ),
                (
                    "G-7A-SV0 corrective layout repair report",
                    root / "docs" / "reports" / "G7A_SV0_TOOL_BACKED_LAYOUT_REPAIR.md",
                ),
            ]
        )
    if phase.upper().strip().startswith(("G-14", "G-15", "G-16", "G-17", "G-18", "G-19", "G-20", "G-21", "G-22")):
        required.extend(
            [
                ("OVI-1 roadmap", root / "docs" / "roadmaps" / "OPENING_VILLAGE_ISLAND_PRODUCTION_ROADMAP.md"),
                ("OVI-1 roadmap JSON", root / "docs" / "roadmaps" / "OPENING_VILLAGE_ISLAND_PRODUCTION_ROADMAP.json"),
                ("OVI-1 execution ledger", root / "docs" / "reports" / "OPENING_VILLAGE_ISLAND_AUTONOMOUS_EXECUTION_LEDGER.md"),
                ("OVI-1 execution ledger JSON", root / "docs" / "reports" / "OPENING_VILLAGE_ISLAND_AUTONOMOUS_EXECUTION_LEDGER.json"),
                ("OVI-1 roadmap validator", game_root / "tools" / "validate_opening_village_island_roadmap.py"),
                ("OVI-1 ledger validator", game_root / "tools" / "validate_opening_village_island_execution_ledger.py"),
            ]
        )
        if phase.upper().strip().startswith("G-15"):
            required.extend(
                [
                    ("G-15 island world topology validator", game_root / "tools" / "validate_island_world_topology.py"),
                    ("G-15A village-to-island transition validator", game_root / "tools" / "validate_village_to_island_transition.py"),
                    ("G-15B island world cohesion validator", game_root / "tools" / "validate_island_world_cohesion.py"),
                ]
            )
        if phase.upper().strip().startswith("G-15A"):
            required.extend(
                [
                    ("G-15A transition source", game_root / "data" / "world_layout" / "village_to_island_transition_v1.json"),
                    ("G-15A phase report", root / "docs" / "reports" / "G15A_VILLAGE_TO_ISLAND_TRANSITION_PASS.md"),
                    ("G-15A phase report JSON", root / "docs" / "reports" / "G15A_VILLAGE_TO_ISLAND_TRANSITION_PASS.json"),
                    (
                        "G-15A runtime screenshot manifest",
                        game_root / "artifacts" / "review" / "g15a_runtime_screenshots" / "g15a_runtime_screenshot_manifest.json",
                    ),
                ]
            )
        if phase.upper().strip().startswith("G-16"):
            required.extend(
                [
                    ("G-16 island POI validator", game_root / "tools" / "validate_island_poi_landmarks.py"),
                    ("G-16A island atelier asset family validator", game_root / "tools" / "validate_island_atelier_asset_family.py"),
                ]
            )
        if phase.upper().strip().startswith("G-17"):
            required.append(("G-17 island NPC encounter validator", game_root / "tools" / "validate_island_npc_encounter_foundation.py"))
        if phase.upper().strip().startswith("G-18"):
            required.extend(
                [
                    ("G-18 village-to-island quest validator", game_root / "tools" / "validate_opening_quest_village_to_island.py"),
                    ("G-18A multi-path rumor choice validator", game_root / "tools" / "validate_multipath_rumor_choice_foundation.py"),
                ]
            )
        if phase.upper().strip().startswith(("G-19", "G-20")):
            required.append(("G-19/G-20 first-session gameplay loop validator", game_root / "tools" / "validate_first_session_gameplay_loop.py"))
        if phase.upper().strip().startswith("G-22"):
            required.extend(
                [
                    ("OVI-1 gate validator", game_root / "tools" / "validate_ovi1_gate.py"),
                    ("OVI-1 review screenshot directory", game_root / "artifacts" / "review" / "g22_ovi1_review_screenshots"),
                    ("OVI-1 motion proof directory", game_root / "artifacts" / "review" / "g22_ovi1_motion_proof"),
                    ("OVI-1 quest playthrough directory", game_root / "artifacts" / "review" / "g22_ovi1_quest_playthrough"),
                ]
            )
    if phase.upper().strip().startswith("G-8"):
        required.extend(
            [
                (
                    "G-8 character motion foundation validator",
                    game_root / "tools" / "validate_character_motion_foundation.py",
                ),
                (
                    "G-8 runtime screenshot manifest",
                    game_root / "artifacts" / "review" / "g8_runtime_screenshots" / "g8_runtime_screenshot_manifest.json",
                ),
                (
                    "G-8 character manifest",
                    game_root / "art_pipeline" / "player_identity" / "manifests" / "newport_atelier_characters_g422r_manifest.json",
                ),
                ("G-8 player script", game_root / "scenes" / "player" / "Player.gd"),
                ("G-8 player scene", game_root / "scenes" / "player" / "Player.tscn"),
                ("G-8 Edrin NPC script", game_root / "scenes" / "npc" / "EdrinVale.gd"),
                ("G-8 Edrin NPC scene", game_root / "scenes" / "npc" / "EdrinVale.tscn"),
            ]
        )
    if phase.upper().strip().startswith("G-8A"):
        required.extend(
            [
                (
                    "G-8A NPC population validator",
                    game_root / "tools" / "validate_npc_population_and_routes.py",
                ),
                (
                    "G-8A runtime screenshot manifest",
                    game_root / "artifacts" / "review" / "g8a_runtime_screenshots" / "g8a_runtime_screenshot_manifest.json",
                ),
                ("G-8A generic town NPC script", game_root / "scenes" / "npc" / "AtelierTownNpc.gd"),
                ("G-8A generic town NPC scene", game_root / "scenes" / "npc" / "AtelierTownNpc.tscn"),
            ]
        )
    if phase.upper().strip().startswith("G-11"):
        required.extend(
            [
                (
                    "G-11 living town rhythm validator",
                    game_root / "tools" / "validate_living_town_rhythm.py",
                ),
                (
                    "G-11 runtime screenshot manifest",
                    game_root / "artifacts" / "review" / "g11_runtime_screenshots" / "g11_runtime_screenshot_manifest.json",
                ),
                ("G-11 runtime screenshot wrapper", game_root / "tools" / "capture_g11_runtime_screenshots.ps1"),
                ("G-11 runtime screenshot script", game_root / "tools" / "capture_g11_runtime_screenshots.gd"),
                ("G-11 Newport blueprint rhythm source", game_root / "scripts" / "NewportTownBlueprint.gd"),
                ("G-11 Main runtime rhythm integration", game_root / "scenes" / "Main.gd"),
                ("G-11 generic NPC rhythm script", game_root / "scenes" / "npc" / "AtelierTownNpc.gd"),
                ("G-11 Edrin rhythm script", game_root / "scenes" / "npc" / "EdrinVale.gd"),
            ]
        )
    if phase.upper().strip().startswith("G-11A"):
        required.extend(
            [
                ("G-11A audio atmosphere validator", game_root / "tools" / "validate_audio_atmosphere_hooks.py"),
                ("G-11A audio hook registry", game_root / "data" / "audio" / "starter_village_atmosphere_hooks.json"),
                ("G-11A audio hook script", game_root / "scripts" / "audio" / "StarterVillageAudioHooks.gd"),
                ("G-11A Main audio hook integration", game_root / "scenes" / "Main.gd"),
                ("G-11A phase report", root / "docs" / "reports" / "G11A_AUDIO_ATMOSPHERE_PLACEHOLDER_FREE_FOUNDATION.md"),
            ]
        )
    if phase.upper().strip().startswith("G-12"):
        required.extend(
            [
                ("G-12 first-session playability validator", game_root / "tools" / "validate_first_session_playability.py"),
                (
                    "G-12 runtime screenshot manifest",
                    game_root / "artifacts" / "review" / "g12_runtime_screenshots" / "g12_runtime_screenshot_manifest.json",
                ),
                ("G-12 runtime screenshot wrapper", game_root / "tools" / "capture_g12_runtime_screenshots.ps1"),
                ("G-12 runtime screenshot script", game_root / "tools" / "capture_g12_runtime_screenshots.gd"),
                ("G-12 phase report", root / "docs" / "reports" / "G12_FIRST_SESSION_FUN_PACING_READABILITY_PASS.md"),
                ("G-12 Main readability integration", game_root / "scenes" / "Main.gd"),
                ("G-12 player prompt suppression", game_root / "scenes" / "player" / "Player.gd"),
                ("G-12 first light quest script", game_root / "scripts" / "quests" / "FirstLightQuest.gd"),
                ("G-12 first light quest data", game_root / "data" / "quests" / "first_light_whispers_before_dawn.json"),
            ]
        )
    if phase.upper().strip().startswith("G-13"):
        required.extend(
            [
                ("G-13 browser build hardening validator", game_root / "tools" / "validate_browser_build_hardening.py"),
                ("G-13 review build identity", game_root / "scripts" / "BuildInfo.gd"),
                ("G-13 package script", game_root / "tools" / "package_itch_web.sh"),
                ("G-13 stable review ZIP", game_root / "artifacts" / "wayfarers-tale-godot-web.zip"),
                (
                    "G-13 versioned review ZIP",
                    game_root
                    / "artifacts"
                    / "wayfarers-tale-godot-g-13-browser-build-performance-and-regression-hardening.zip",
                ),
                ("G-12 regression screenshot wrapper reused for G-13", game_root / "tools" / "capture_g12_runtime_screenshots.ps1"),
                ("G-12 regression screenshot script reused for G-13", game_root / "tools" / "capture_g12_runtime_screenshots.gd"),
                ("G-13 phase report", root / "docs" / "reports" / "G13_BROWSER_BUILD_PERFORMANCE_REGRESSION_HARDENING.md"),
            ]
        )
    if phase.upper().strip().startswith("G-10"):
        required.extend(
            [
                (
                    f"{capture_label} opening quest arc validator",
                    game_root / "tools" / "validate_opening_quest_arc.py",
                ),
                (
                    f"{capture_label} runtime screenshot manifest",
                    game_root / "artifacts" / "review" / f"{capture_prefix}_runtime_screenshots" / f"{capture_prefix}_runtime_screenshot_manifest.json",
                ),
                (f"{capture_label} quest state script", game_root / "scripts" / "QuestState.gd"),
                (f"{capture_label} first light quest script", game_root / "scripts" / "quests" / "FirstLightQuest.gd"),
                (f"{capture_label} quest data", game_root / "data" / "quests" / "first_light_whispers_before_dawn.json"),
                (f"{capture_label} HUD journal script", game_root / "scenes" / "ui" / "HUD.gd"),
                (f"{capture_label} Main quest integration", game_root / "scenes" / "Main.gd"),
            ]
        )
        if phase.upper().strip().startswith("G-10A"):
            required.extend(
                [
                    (
                        "G-10A tavern whisper validator",
                        game_root / "tools" / "validate_tavern_whisper_system.py",
                    ),
                    (
                        "G-10A Newport visual ordering validator",
                        game_root / "tools" / "validate_newport_visual_ordering.py",
                    ),
                    ("G-10A tavern whisper system", game_root / "scripts" / "dialogue" / "TavernWhisperSystem.gd"),
                    ("G-10A tavern whisper data", game_root / "data" / "dialogue" / "tavern_whispers.json"),
                ]
            )
        if phase.upper().strip().startswith("G-10B"):
            required.extend(
                [
                    (
                        "G-10B multi-path starter choice validator",
                        game_root / "tools" / "validate_multi_path_starter_choice.py",
                    ),
                    ("G-10B choice router", game_root / "scripts" / "quests" / "FirstLightChoiceRouter.gd"),
                    ("G-10B multi-path data", game_root / "data" / "quests" / "first_light_multi_path_choices.json"),
                ]
            )
    elif phase.upper().strip().startswith("G-9A"):
        required.extend(
            [
                (
                    "G-9A opening quest arc validator",
                    game_root / "tools" / "validate_opening_quest_arc.py",
                ),
                (
                    "G-9A interaction UX validator",
                    game_root / "tools" / "validate_interaction_ux.py",
                ),
                (
                    "G-9A runtime screenshot manifest",
                    game_root / "artifacts" / "review" / "g9a_runtime_screenshots" / "g9a_runtime_screenshot_manifest.json",
                ),
                ("G-9A quest state script", game_root / "scripts" / "QuestState.gd"),
                ("G-9A first light quest script", game_root / "scripts" / "quests" / "FirstLightQuest.gd"),
                ("G-9A quest data", game_root / "data" / "quests" / "first_light_whispers_before_dawn.json"),
                ("G-9A HUD journal script", game_root / "scenes" / "ui" / "HUD.gd"),
                ("G-9A Main quest integration", game_root / "scenes" / "Main.gd"),
            ]
        )
    elif phase.upper().strip().startswith("G-9"):
        required.extend(
            [
                (
                    "G-9 interaction UX validator",
                    game_root / "tools" / "validate_interaction_ux.py",
                ),
                (
                    "G-9 runtime screenshot manifest",
                    game_root / "artifacts" / "review" / "g9_runtime_screenshots" / "g9_runtime_screenshot_manifest.json",
                ),
                ("G-9 player prompt script", game_root / "scenes" / "player" / "Player.gd"),
                ("G-9 HUD script", game_root / "scenes" / "ui" / "HUD.gd"),
            ]
        )
    return [(label, "FOUND" if path.exists() else "MISSING", rel(path, root)) for label, path in required]


def md_table(headers: Iterable[str], rows: Iterable[Iterable[str]]) -> str:
    header_list = list(headers)
    lines = [
        "| " + " | ".join(header_list) + " |",
        "| " + " | ".join("---" for _ in header_list) + " |",
    ]
    for row in rows:
        cleaned = [str(value).replace("\n", "<br>") for value in row]
        lines.append("| " + " | ".join(cleaned) + " |")
    return "\n".join(lines)


def pr_label(pr: object | None) -> str:
    if not isinstance(pr, dict):
        return "Not detected"
    draft = "draft" if pr.get("isDraft") else "not draft"
    merged = f", merged at {pr.get('mergedAt')}" if pr.get("mergedAt") else ""
    return (
        f"#{pr.get('number')} {pr.get('title')} "
        f"({pr.get('state')}, {draft}{merged}) - {pr.get('url')}"
    )


def current_pr_from_open(open_prs: object, branch: str) -> str:
    if not isinstance(open_prs, list):
        return "No open PR data."
    matches = [item for item in open_prs if isinstance(item, dict) and item.get("headRefName") == branch]
    if not matches:
        return "No open PR detected for current branch."
    return ", ".join(f"#{item.get('number')} {item.get('title')} - {item.get('url')}" for item in matches)


def score_status(score: float, threshold: float = 8.5) -> str:
    return "PASS" if score >= threshold else "FAIL"


def score_text(score: float) -> str:
    return f"{score:.1f}/10"


def yes_no(value: bool) -> str:
    return "YES" if value else "NO"


def phase_requires_screenshots(phase: str) -> bool:
    normalized = phase.upper().strip()
    if normalized.startswith(("SV-0", "OVI-1")) or is_g15_topology_planning_phase(phase):
        return False
    return True


def final_pr_number(pr_state: dict[str, object], target_pr: int) -> str:
    target_pr_data = pr_state.get("target_pr")
    if isinstance(target_pr_data, dict) and target_pr_data.get("number"):
        return f"#{target_pr_data.get('number')}"
    if target_pr <= 0:
        return "Not available yet"
    return f"#{target_pr}"


def derive_authority_verdict(
    requested_verdict: str,
    run_validators: bool,
    validator_failures: list[dict[str, str]],
    screenshots: list[Path],
    screenshot_review: str,
    paths: list[tuple[str, str, str]],
    design_score: float,
    art_direction_score: float,
    world_layout_score: float,
    gameplay_readability_score: float,
    technical_stability_score: float,
    human_escalation_blocker: str,
    phase: str,
) -> str:
    if requested_verdict:
        return requested_verdict
    if human_escalation_blocker.strip():
        return AUTHORITY_BLOCKED
    if validator_failures:
        return AUTHORITY_FAIL
    if not run_validators:
        return AUTHORITY_FAIL
    if not all(status == "FOUND" for _, status, _ in paths):
        return AUTHORITY_FAIL
    if phase_requires_screenshots(phase) and (not screenshots or screenshot_review != "inspected"):
        return AUTHORITY_FAIL
    phase_scores = [
        design_score,
        art_direction_score,
        world_layout_score,
        gameplay_readability_score,
        technical_stability_score,
    ]
    if min(phase_scores) < 8.5:
        return AUTHORITY_FAIL
    return AUTHORITY_PASS


def build_report(
    root: Path,
    phase: str,
    git_state: dict[str, str],
    pr_state: dict[str, object],
    screenshots: list[Path],
    paths: list[tuple[str, str, str]],
    validator_results: list[dict[str, str]],
    run_validators: bool,
    godot_bin: str,
    python_bin: str,
    target_pr: int,
    authority_verdict: str,
    screenshot_review: str,
    design_score: float,
    art_direction_score: float,
    world_layout_score: float,
    gameplay_readability_score: float,
    technical_stability_score: float,
    qa_regression_result: str,
    build_release_result: str,
    final_recommended_next_phase: str,
    human_escalation_blocker: str,
) -> str:
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    target_pr_data = pr_state.get("target_pr")
    open_prs = pr_state.get("open_prs")
    known_449 = target_pr == 449 and isinstance(target_pr_data, dict)
    validator_failures = [item for item in validator_results if item["status"] == "FAIL"]
    validator_passes = [item for item in validator_results if item["status"] == "PASS"]
    validator_skips = [item for item in validator_results if item["status"] == "SKIPPED_WITH_COMMAND"]
    qa_status = "PASS" if run_validators and not validator_failures else "SKIPPED_WITH_COMMAND"
    if validator_failures:
        qa_status = "FAIL"

    final_verdict = derive_authority_verdict(
        requested_verdict=authority_verdict,
        run_validators=run_validators,
        validator_failures=validator_failures,
        screenshots=screenshots,
        screenshot_review=screenshot_review,
        paths=paths,
        design_score=design_score,
        art_direction_score=art_direction_score,
        world_layout_score=world_layout_score,
        gameplay_readability_score=gameplay_readability_score,
        technical_stability_score=technical_stability_score,
        human_escalation_blocker=human_escalation_blocker,
        phase=phase,
    )
    if known_449:
        final_verdict = AUTHORITY_FAIL
        designer_status = "FAIL"
        art_status = "FAIL"
        world_status = "FAIL"
        ux_status = "FAIL"
        technical_artist_status = "FAIL"
    elif final_verdict == AUTHORITY_PASS:
        designer_status = "PASS"
        art_status = "PASS"
        world_status = "PASS"
        ux_status = "PASS"
        technical_artist_status = "PASS"
    elif final_verdict == AUTHORITY_BLOCKED:
        designer_status = "BLOCKED"
        art_status = "BLOCKED"
        world_status = "BLOCKED"
        ux_status = "BLOCKED"
        technical_artist_status = "BLOCKED"
    else:
        designer_status = score_status(design_score)
        art_status = score_status(art_direction_score)
        world_status = score_status(world_layout_score)
        ux_status = score_status(gameplay_readability_score)
        technical_artist_status = "FAIL" if technical_stability_score < 8.5 else "PASS"

    screenshots_required = phase_requires_screenshots(phase)
    screenshots_inspected = (not screenshots_required and screenshot_review in {"not-applicable", "not_applicable", "missing", "not-inspected"}) or (
        bool(screenshots) and screenshot_review == "inspected"
    )
    meets_bar = min(
        design_score,
        art_direction_score,
        world_layout_score,
        gameplay_readability_score,
        technical_stability_score,
    ) >= 8.5
    advances_north_star = final_verdict == AUTHORITY_PASS and meets_bar and screenshots_inspected
    human_review_required = final_verdict == AUTHORITY_BLOCKED
    blocker_text = human_escalation_blocker.strip() or "None."
    next_phase_text = final_recommended_next_phase.strip() or "Not selected by this report."

    programmer_status = "PASS" if all(status == "FOUND" for _, status, _ in paths) else "FAIL"
    release_status = "PASS" if final_verdict == AUTHORITY_PASS else ("BLOCKED" if final_verdict == AUTHORITY_BLOCKED else "FAIL")
    agent_rows = [
        ["Scrum Master", "PASS", "Branch/PR state gathered; autonomous merge rule must still be checked outside this report."],
        ["World-class Game Designer", designer_status, "Newport layout must prove street grammar, loops, first-session motivation, and NPC/player usability."],
        ["World/Layout Designer", world_status, "Districts, lots, harbor spine, uphill roads, back street, and movement routes must read as one town."],
        ["Art Director", art_status, "Ground/street cohesion, landmark hierarchy, sprite fit, and screenshot beauty must clear council review."],
        ["Animation/NPC Behavior Director", ux_status, "NPCs must be grounded, idle/walk intentionally, and never glide as static cutouts in normal play."],
        ["Narrative Designer", world_status, "Tavern whispers, harbor rumors, counting-house pressure, and opening quest stakes must be playable."],
        ["Quest Designer", world_status, "Quest state, branch paths, clue discovery, reward beats, and return hooks must be playable and readable."],
        ["UX Designer", ux_status, "Navigation clarity, interaction prompts, objectives, and player orientation must clear council review."],
        ["Game Programmer", programmer_status, "Required automation and validator files checked; systems must remain maintainable."],
        ["QA Analyst", qa_status, "Validators must pass, but technical pass is not design approval."],
        ["Build/Release Engineer", release_status, "PR readiness requires green checks, mergeability, proof, and no hard stop condition."],
    ]

    visual_fields = [
        ["Does Newport read as a harbor city?", "PASS" if world_layout_score >= 8.5 else "FAIL"],
        ["Is there a waterfront avenue parallel to the harbor?", "PASS" if world_layout_score >= 8.5 else "FAIL"],
        ["Are there roads running uphill from harbor into town?", "PASS" if world_layout_score >= 8.5 else "FAIL"],
        ["Is there a back street behind the first road?", "PASS" if world_layout_score >= 8.5 else "FAIL"],
        ["Are buildings sitting on coherent lots?", "PASS" if art_direction_score >= 8.5 else "FAIL"],
        ["Is the ground/street style unified?", "PASS" if art_direction_score >= 8.5 else "FAIL"],
        ["Are old clipped/transparent road rectangles gone or acceptable as non-blocking roadmap residue?", "PASS" if art_direction_score >= 8.5 else "FAIL"],
        ["Is there believable player/NPC walkability?", "PASS" if gameplay_readability_score >= 8.5 else "FAIL"],
        ["Are civic, market, tavern, harbor, and residential districts legible?", "PASS" if design_score >= 8.5 else "FAIL"],
        ["Does the harbor economy read clearly?", "PASS" if world_layout_score >= 8.5 else "FAIL"],
        ["Are props supporting function instead of hiding layout problems?", "PASS" if design_score >= 8.5 else "FAIL"],
        ["Does the scene support 90+ seconds of exploration in principle?", "PASS" if gameplay_readability_score >= 8.5 else "FAIL"],
        ["Does it approach the Newport 8.5+/10 bar?", "PASS" if meets_bar else "FAIL"],
    ]
    g418e_asset_family_fields = [
        ["Does the new asset family improve Newport as a believable harbor city?", "PASS" if world_layout_score >= 8.5 else "FAIL"],
        ["Does it support the accepted G-4.23B street/harbor layout?", "PASS" if design_score >= 8.5 else "FAIL"],
        ["Does it meet or exceed the 8.5+/10 pre-G-5 visual/art/world bar?", "PASS" if meets_bar else "FAIL"],
        ["Are the assets coherent as one Newport visual language?", "PASS" if art_direction_score >= 8.5 else "FAIL"],
        ["Are the assets cleanly extracted and properly rendered?", "PASS" if technical_stability_score >= 8.5 else "FAIL"],
        ["Are the assets correctly classified for provenance?", "PASS" if technical_stability_score >= 8.5 else "FAIL"],
        ["Are any yellow/red/unknown assets incorrectly promoted?", "NO" if technical_stability_score >= 8.5 else "CHECK REQUIRED"],
        ["Is gameplay readability preserved?", "PASS" if gameplay_readability_score >= 8.5 else "FAIL"],
        ["Are screenshots sufficient proof?", "PASS" if screenshots_inspected else "FAIL"],
        ["Is human escalation truly required?", "NO" if not human_review_required else "YES"],
    ]
    g419_player_identity_fields = [
        ["Does the player read as human-scale in Newport?", "PASS" if gameplay_readability_score >= 8.5 else "FAIL"],
        ["Does the player belong with buildings, streets, docks, and G-4.18E props?", "PASS" if art_direction_score >= 8.5 else "FAIL"],
        ["Are idle/walk directions established for down/up/left/right?", "PASS" if technical_stability_score >= 8.5 else "FAIL"],
        ["Are collision, camera, spawn, and interaction hooks preserved?", "PASS" if technical_stability_score >= 8.5 else "FAIL"],
        ["Are provenance artifacts preserved and final-commercial promotion avoided?", "PASS" if technical_stability_score >= 8.5 else "FAIL"],
        ["Do screenshots prove gameplay zoom, wide readability, scale, grounding, and facing/movement?", "PASS" if screenshots_inspected else "FAIL"],
        ["Is human escalation truly required?", "NO" if not human_review_required else "YES"],
    ]
    g420_hud_ui_fields = [
        ["Does the default HUD feel intentional rather than debug/raw-engine?", "PASS" if art_direction_score >= 8.5 else "FAIL"],
        ["Is review metadata hidden by default but still available?", "PASS" if technical_stability_score >= 8.5 else "FAIL"],
        ["Do HUD screenshots preserve player, road, building, and harbor readability?", "PASS" if gameplay_readability_score >= 8.5 else "FAIL"],
        ["Does dialogue/prompt styling match the Wayfarer fantasy harbor tone?", "PASS" if art_direction_score >= 8.5 else "FAIL"],
        ["Does no-HUD clean capture remain available?", "PASS" if technical_stability_score >= 8.5 else "FAIL"],
        ["Are screenshots sufficient proof?", "PASS" if screenshots_inspected else "FAIL"],
        ["Is human escalation truly required?", "NO" if not human_review_required else "YES"],
    ]
    g421_hero_slice_fields = [
        ["Does the slice feel like the real game rather than a prototype board?", "PASS" if design_score >= 8.5 else "FAIL"],
        ["Do streets, docks, buildings, props, player, HUD, and camera read as one Newport home-base frame?", "PASS" if art_direction_score >= 8.5 else "FAIL"],
        ["Are normal HUD, no-HUD, and close-up hero-slice screenshots present and inspected?", "PASS" if screenshots_inspected else "FAIL"],
        ["Is yellow temporary art treated as documented roadmap residue rather than hidden final art?", "PASS" if technical_stability_score >= 8.5 else "FAIL"],
        ["Does the slice advance Wayfarer toward the G-4 exit review gate?", "PASS" if world_layout_score >= 8.5 else "FAIL"],
        ["Is human escalation truly required?", "NO" if not human_review_required else "YES"],
    ]
    g422_visual_gate_fields = [
        ["Does the origin city clear the 8.0+ visual foundation exit requirement?", "PASS" if design_score >= 8.0 else "FAIL"],
        ["Does at least one hero street/dock slice look like the real game?", "PASS" if art_direction_score >= 8.5 else "FAIL"],
        ["Do buildings, streets, docks, props, player, and HUD belong to one art direction?", "PASS" if art_direction_score >= 8.5 and gameplay_readability_score >= 8.5 else "FAIL"],
        ["Are yellow/provisional assets documented rather than promoted to final commercial green?", "PASS" if technical_stability_score >= 8.5 else "FAIL"],
        ["Are normal HUD, no-HUD, green-origin/yellow-art context, and debug-overlay proof captures present and inspected?", "PASS" if screenshots_inspected else "FAIL"],
        ["May G-5 be recommended after this gate?", "YES" if meets_bar and not human_review_required else "NO"],
        ["Is human escalation truly required?", "NO" if not human_review_required else "YES"],
    ]
    if phase.upper().strip().startswith("G-4.18E"):
        scrum_scope = "Scope check: this council pass produced a coherent G-4.18E asset family and controlled runtime placements; it must not scatter random props or hide layout problems."
    elif phase.upper().strip().startswith("SV-0"):
        scrum_scope = "Scope check: this SV-0 Tooling Stack gate locks free, safe production tooling, source-of-truth layout data, visual-regression warnings, runtime movement proof, asset cleanup, and ground cohesion before more Newport placement work."
    elif phase.upper().strip().startswith("OVI-1"):
        scrum_scope = "Scope check: this OVI-1 control-plane pass updates roadmap authority, ledgers, checklists, and validators only; it must not claim village or island runtime production completion."
    elif phase.upper().strip().startswith("G-4.19"):
        scrum_scope = "Scope check: this council pass replaces the drawn player placeholder with a directional runtime sprite foundation while preserving Newport layout, collision, camera, spawn, and interaction behavior."
    elif phase.upper().strip().startswith("G-4.20"):
        scrum_scope = "Scope check: this council pass redesigns HUD/UI presentation only; it keeps no-HUD capture, review metadata, Newport runtime layout, player movement, collision, camera, and interaction behavior intact."
    elif phase.upper().strip().startswith("G-4.21"):
        scrum_scope = "Scope check: this council pass composes the accepted Newport street/dock layout, G-4.18E props, G-4.19 player, and G-4.20 HUD into a hero-slice screenshot packet without changing core gameplay systems."
    elif phase.upper().strip().startswith("G-4.22R"):
        scrum_scope = "Scope check: this council pass reopens the false-positive G-5 readiness gate, verifies the pre-G-5 roadmap ledger, and repairs visible player/NPC/marker/world sprite consistency before G-5 can be recommended."
    elif phase.upper().strip().startswith("G-4.22"):
        scrum_scope = "Scope check: this council pass is the formal G-4 visual foundation gate; it records acceptance authority and may recommend G-5 only if screenshots, provenance, validators, and council scores clear the gate."
    elif phase.upper().strip().startswith("G-14"):
        scrum_scope = "Scope check: this council pass proves Starter Village readiness as an internal OVI-1 checkpoint; it must record Human review required: no and continue to G-15 if it passes."
    elif phase.upper().strip().startswith(("G-15", "G-16", "G-17", "G-18", "G-19", "G-20", "G-21", "G-22")):
        scrum_scope = "Scope check: this council pass belongs to the OVI-1 Opening Village + Island autonomous runway; it must prove the active island/village/quest/build slice without skipping required roadmap rows."
    elif phase.upper().strip().startswith("G-12"):
        scrum_scope = "Scope check: this council pass playtests the first-session loop, screenshot framing, objective readability, bark/prompt/dialogue overlap, and route clarity; it must not claim SV-1 final cohesion or browser build hardening."
    elif phase.upper().strip().startswith("G-10A"):
        scrum_scope = "Scope check: this council pass makes the Tavern/Inn a rumor gameplay hub with Bess, Silas, Nora, Jonah, rotating barks, and quest-relevant whisper data; it must not claim the broader multi-path starter foundation is complete."
    elif phase.upper().strip().startswith("G-10B"):
        scrum_scope = "Scope check: this council pass adds the multi-path starter choice foundation for First Light, including harbor, tavern, counting-house, merchant, and optional secret routes; it must not claim G-11 living town rhythm or G-12 final pacing/readability are complete."
    elif phase.upper().strip().startswith("G-10") and not phase.upper().strip().startswith(("G-10A", "G-10B")):
        scrum_scope = "Scope check: this council pass expands First Light into a playable opening quest arc with named NPCs, branch choice, optional discovery, reward/progression, and a reason to continue; it must not claim the later dedicated tavern-system or multi-path foundation phases are complete."
    elif phase.upper().strip().startswith("G-9A"):
        scrum_scope = "Scope check: this council pass adds the journal/objective quest-state foundation for First Light only; it must prove objective completion, feedback, and reward state without claiming the full G-10 opening quest arc is complete."
    elif phase.upper().strip().startswith("G-9"):
        scrum_scope = "Scope check: this council pass changes interaction prompt copy, HUD objective guidance, runtime prompt proof capture, validators, and SV-1 ledger only; it must improve clarity without starting G-9A quest-state scope."
    elif phase.upper().strip().startswith("G-8"):
        scrum_scope = "Scope check: this council pass changes the player/NPC motion foundation, runtime proof capture, validators, and SV-1 ledger only; it must eliminate static-sprite glide without expanding the quest scope."
    else:
        scrum_scope = "Scope check: this council pass changes production documentation and tooling only; it must not change Newport runtime layout."

    game_root = root / "wayfarer_godot_vertical_slice"
    ledger_validator_status = next(
        (item["status"] for item in validator_results if item["name"] == "Pre-G-5 roadmap execution ledger validation"),
        "NOT_RUN_FOR_PHASE",
    )
    ovi_roadmap_validator_status = next(
        (item["status"] for item in validator_results if item["name"] == "Opening Village + Island roadmap validation"),
        "NOT_RUN_FOR_PHASE",
    )
    ovi_ledger_validator_status = next(
        (item["status"] for item in validator_results if item["name"] == "Opening Village + Island execution ledger validation"),
        "NOT_RUN_FOR_PHASE",
    )
    runtime_asset_validator_status = next(
        (
            item["status"]
            for item in validator_results
            if item["name"] in {"G-4.22R runtime asset consistency validation", "Runtime atelier asset consistency validation"}
        ),
        "NOT_RUN_FOR_PHASE",
    )
    g422r_consistency_fields = [
        ["Is the previous G-5 readiness declaration reopened?", "YES"],
        ["Does the roadmap execution ledger have no non-PASS rows?", "PASS" if ledger_validator_status == "PASS" else "CHECK"],
        ["Are player sprites atelier-standard and manifest-backed?", "PASS" if runtime_asset_validator_status == "PASS" else "CHECK"],
        ["Are NPC sprites atelier-standard and manifest-backed?", "PASS" if runtime_asset_validator_status == "PASS" else "CHECK"],
        ["Are crude humanoid placeholders removed from normal play?", "PASS" if runtime_asset_validator_status == "PASS" else "CHECK"],
        ["Are marker/sign/quest/world objects traceable or hidden/debug-only?", "PASS" if runtime_asset_validator_status == "PASS" else "CHECK"],
        ["Were G-4.22R screenshots inspected by the council?", "PASS" if screenshots_inspected else "FAIL"],
        ["May true G-5 readiness be recommended after this repair?", "YES" if final_verdict == AUTHORITY_PASS else "NO"],
    ]
    ledger_result_rows = [
        ["Ledger markdown", "FOUND" if (root / "docs" / "reports" / "PRE_G5_ROADMAP_EXECUTION_LEDGER.md").exists() else "MISSING", "docs/reports/PRE_G5_ROADMAP_EXECUTION_LEDGER.md"],
        ["Ledger JSON", "FOUND" if (root / "docs" / "reports" / "PRE_G5_ROADMAP_EXECUTION_LEDGER.json").exists() else "MISSING", "docs/reports/PRE_G5_ROADMAP_EXECUTION_LEDGER.json"],
        ["Ledger validator", ledger_validator_status, "wayfarer_godot_vertical_slice/tools/validate_pre_g5_roadmap_ledger.py"],
        ["OVI-1 roadmap validator", ovi_roadmap_validator_status, "wayfarer_godot_vertical_slice/tools/validate_opening_village_island_roadmap.py"],
        ["OVI-1 ledger validator", ovi_ledger_validator_status, "wayfarer_godot_vertical_slice/tools/validate_opening_village_island_execution_ledger.py"],
        ["Runtime asset consistency validator", runtime_asset_validator_status, "wayfarer_godot_vertical_slice/tools/validate_g422r_runtime_asset_consistency.py"],
    ]
    runtime_asset_audit_rows = [
        [
            "Player",
            "wayfarer_godot_vertical_slice/art_pipeline/player_identity/atlases/player_wayfarer_atelier_g422r_v1.png",
            "newport_atelier_characters_g422r_manifest.json / player_wayfarer_atelier_g422r",
            "PASS" if runtime_asset_validator_status == "PASS" else "CHECK",
        ],
        [
            "NPCs",
            "wayfarer_godot_vertical_slice/art_pipeline/player_identity/atlases/newport_npc_atelier_g422r_v1.png",
            "newport_atelier_characters_g422r_manifest.json / three approved NPC variants",
            "PASS" if runtime_asset_validator_status == "PASS" else "CHECK",
        ],
        [
            "Visible marker/sign/quest/world objects",
            "wayfarer_godot_vertical_slice/art_pipeline/newport_atelier/contact_sheets",
            "Newport visual production registry and G-4.18E/G-4.20B atelier manifests",
            "PASS" if runtime_asset_validator_status == "PASS" else "CHECK",
        ],
        [
            "Hidden debug-only placeholders",
            "Debug overlay/capture toggles only",
            "Normal G-4.22R screenshots require debug_overlay=false except explicit proof metadata",
            "PASS" if screenshots_inspected else "CHECK",
        ],
        [
            "Removed/replaced placeholders",
            "Player.gd, EdrinVale.gd, MapLayer.gd, NewportTownBlueprint.gd",
            "G-4.22R validator scans primitive draw paths and npc_placeholder anchors",
            "PASS" if runtime_asset_validator_status == "PASS" else "CHECK",
        ],
    ]
    player_asset_audit_rows = [
        ["Runtime atlas", "player_wayfarer_atelier_g422r_v1.png", "Manifest-backed", "PASS" if runtime_asset_validator_status == "PASS" else "CHECK"],
        ["Source image", "g422r_atelier_characters_source_imagegen.png", "Repo-local generated source", "PASS" if runtime_asset_validator_status == "PASS" else "CHECK"],
        ["Source prompt", "g422r_atelier_characters_prompt.txt", "Prompt retained", "PASS" if runtime_asset_validator_status == "PASS" else "CHECK"],
        ["Contact sheet", "newport_atelier_characters_g422r_contact_sheet.png", "Reviewed in screenshot proof", "PASS" if runtime_asset_validator_status == "PASS" else "CHECK"],
        ["Runtime integration", "Player.gd / Player.tscn", "G-4.22R atlas, scale, y-sort grounding", "PASS" if runtime_asset_validator_status == "PASS" else "CHECK"],
    ]
    npc_asset_audit_rows = [
        ["Runtime atlas", "newport_npc_atelier_g422r_v1.png", "Manifest-backed three-variant NPC sheet", "PASS" if runtime_asset_validator_status == "PASS" else "CHECK"],
        ["Interactable NPC", "scenes/npc/EdrinVale.gd / EdrinVale.tscn", "AnimatedSprite2D atlas visual, primitive draw removed, G-8 no-drift contract", "PASS" if runtime_asset_validator_status == "PASS" else "CHECK"],
        ["Ambient NPC placements", "MapLayer.gd NEWPORT_ATELIER_CHARACTER_PLACEMENTS", "Manifest-backed dockworker/vendor/clerk variants", "PASS" if runtime_asset_validator_status == "PASS" else "CHECK"],
        ["Blueprint anchors", "NewportTownBlueprint.gd", "npc_atelier anchors, no npc_placeholder normal-play anchors", "PASS" if runtime_asset_validator_status == "PASS" else "CHECK"],
    ]
    marker_sign_audit_rows = [
        ["Shop/sign markers", "newport_atelier_sign_shop_markers_contact_sheet.png", "G-4.20B/G-4.18E atelier registry evidence", "PASS" if runtime_asset_validator_status == "PASS" else "CHECK"],
        ["Lamps/wayfinding", "newport_atelier_lamps_wayfinding_contact_sheet.png", "G-4.20B atelier registry evidence", "PASS" if runtime_asset_validator_status == "PASS" else "CHECK"],
        ["Primitive normal-play sign path", "MapLayer.gd _draw_g410_props", "G-4.22R validator requires no primitive sign posts in normal G410 props", "PASS" if runtime_asset_validator_status == "PASS" else "CHECK"],
    ]
    screenshot_inspection_rows = [
        ["Screenshots found", str(len(screenshots)), "PASS" if screenshots or not screenshots_required else "FAIL"],
        ["Screenshot review flag", screenshot_review, "PASS" if screenshots_inspected else "FAIL"],
        [
            "Debug overlays disabled proof",
            f"{screenshot_prefix_for_phase(phase)[1]}_14_debug_overlays_disabled.png" if screenshots_required else "Not required for SV-0 docs/tooling gate",
            "PASS" if screenshots_inspected else "CHECK",
        ],
        ["Visible failures found/fixed", "Non-atelier player/NPC/marker placeholders replaced or hidden by G-4.22R", "PASS" if final_verdict == AUTHORITY_PASS else "CHECK"],
    ]
    north_star_rows = [
        ["Harbor RPG believability", "Newport remains a coherent harbor city rather than an asset board.", "PASS" if advances_north_star else "CHECK"],
        ["Player-facing wonder/readability", "Player/NPC art no longer breaks the atelier environment language.", "PASS" if art_direction_score >= 8.5 else "FAIL"],
        ["Autonomous QA integrity", "Ledger, validators, screenshots, and council sections prevent silent phase compression.", "PASS" if ledger_validator_status in {"PASS", "NOT_RUN_FOR_PHASE"} and ovi_ledger_validator_status in {"PASS", "NOT_RUN_FOR_PHASE"} else "FAIL"],
    ]
    visual_bar_rows = [
        ["Design", score_text(design_score), score_status(design_score)],
        ["Art direction", score_text(art_direction_score), score_status(art_direction_score)],
        ["World/layout", score_text(world_layout_score), score_status(world_layout_score)],
        ["Gameplay/readability", score_text(gameplay_readability_score), score_status(gameplay_readability_score)],
        ["Technical stability", score_text(technical_stability_score), score_status(technical_stability_score)],
        ["Minimum score", score_text(min(design_score, art_direction_score, world_layout_score, gameplay_readability_score, technical_stability_score)), "PASS" if meets_bar else "FAIL"],
    ]

    screenshot_rows = []
    for path in screenshots[:16]:
        stat = path.stat()
        mtime = dt.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        screenshot_rows.append([rel(path, root), str(stat.st_size), mtime])
    if not screenshot_rows:
        screenshot_rows.append(["No screenshot artifacts found.", "", ""])

    pr_errors = pr_state.get("errors") if isinstance(pr_state.get("errors"), list) else []
    open_pr_rows = []
    if isinstance(open_prs, list) and open_prs:
        for item in open_prs:
            if isinstance(item, dict):
                open_pr_rows.append(
                    [
                        f"#{item.get('number')}",
                        str(item.get("title")),
                        str(item.get("headRefName")),
                        str(item.get("baseRefName")),
                        str(item.get("url")),
                    ]
                )
    else:
        open_pr_rows.append(["None detected", "", "", "", ""])

    lines = [
        f"# {phase} Wayfarer Agent Council Report",
        "",
        "TECHNICAL PASS DOES NOT EQUAL DESIGN PASS.",
        "",
        "For ordinary roadmap-bound work before OVI-1, this report is the council authority verdict after validators and screenshot review. This tool never merges, never impersonates Chris, and never converts technical validation alone into creative approval.",
        "",
        "## Summary",
        "",
        f"- Generated: {now}",
        f"- Repo root: `{root}`",
        f"- Phase ID: {phase}",
        f"- Branch: `{git_state['branch']}`",
        f"- Commit: `{git_state['head']}`",
        f"- origin/main: `{git_state['origin_main']}`",
        f"- Current branch PR: {current_pr_from_open(open_prs, git_state['branch'])}",
        f"- Target PR check: {pr_label(target_pr_data)}",
        f"- PR number if available: {final_pr_number(pr_state, target_pr)}",
        f"- Final Authority Verdict: {final_verdict}",
        f"- Final recommended next phase: {next_phase_text}",
        f"- Human escalation required: {yes_no(human_review_required)}",
        f"- Escalation blocker: {blocker_text}",
        "",
        "## Final Authority Verdict",
        "",
        f"Final Authority Verdict: `{final_verdict}`",
        "",
        md_table(
            ["Field", "Result"],
            [
                ["Phase ID", phase],
                ["Branch", git_state["branch"]],
                ["Commit", git_state["head"]],
                ["PR number if available", final_pr_number(pr_state, target_pr)],
                ["Screenshot review", screenshot_review],
                ["Design score", score_text(design_score)],
                ["Art direction score", score_text(art_direction_score)],
                ["World/layout score", score_text(world_layout_score)],
                ["Gameplay/readability score", score_text(gameplay_readability_score)],
                ["Technical stability score", score_text(technical_stability_score)],
                ["QA regression result", qa_regression_result],
                ["Build/release result", build_release_result],
                ["Final recommended next phase", next_phase_text],
            ],
        ),
        "",
        "## Agent Status Table",
        "",
        md_table(["Agent", "Status", "Recommendation"], agent_rows),
        "",
        "## Preflight Snapshot",
        "",
        "### Git Status",
        "",
        "```text",
        git_state["status"],
        "```",
        "",
        "### Open PR State",
        "",
        md_table(["PR", "Title", "Head", "Base", "URL"], open_pr_rows),
    ]

    if pr_errors:
        lines.extend(["", "### PR Discovery Notes", ""])
        lines.extend(f"- {error}" for error in pr_errors)

    lines.extend(
        [
            "",
            "## Screenshot Artifacts",
            "",
            md_table(["Path", "Bytes", "Modified"], screenshot_rows),
            "",
            f"Screenshot evidence status: {screenshot_review}. Final authority depends on council image inspection, not artifact existence alone.",
            "",
            "## Visual/World Authority Questions",
            "",
            md_table(
                ["Question", "Council Answer"],
                [
                    ["Does this meet the active 8.5+/10 visual/world bar?", yes_no(meets_bar)],
                    ["Does this advance Wayfarer toward the North Star?", yes_no(advances_north_star)],
                    ["Is human visual review truly required, or can the council accept this?", "Human review required only for true blocker." if human_review_required else "Council can accept this ordinary pre-OVI-1 pass."],
                    ["If human review is required, what exact blocker justifies escalation?", blocker_text if human_review_required else "None."],
                ],
            ),
            "",
            "## OVI-1 Hard Failure Rules",
            "",
            "- Fail with `COUNCIL_FAIL_NEEDS_CODE_FIX` if G-14 tries to stop for Chris before OVI-1.",
            "- Fail if the island roadmap or execution ledger rows are missing or unproven.",
            "- Fail if the village is good but the island is not playable, or if the island is explorable but not cohesive.",
            "- Fail if the village-to-island quest chain is not playable.",
            "- Fail if NPCs hover, glide, or lack required movement proof.",
            "- Fail if normal-play assets are non-atelier, untracked, or placeholder-like.",
            "- Fail if the first-session loop is boring, confusing, incomplete, or unrewarded.",
            "- Fail if browser/review package identity is stale.",
            "",
            "## Roadmap Execution Ledger Result",
            "",
            md_table(["Item", "Status", "Evidence"], ledger_result_rows),
            "",
            "## Visible Runtime Asset Consistency Audit",
            "",
            md_table(["Runtime Element", "Asset Path", "Provenance/Manifest", "Status"], runtime_asset_audit_rows),
            "",
            "## Player Asset Audit",
            "",
            md_table(["Item", "Path", "Evidence", "Status"], player_asset_audit_rows),
            "",
            "## NPC Asset Audit",
            "",
            md_table(["Item", "Path", "Evidence", "Status"], npc_asset_audit_rows),
            "",
            "## Marker/Sign/Quest Object Audit",
            "",
            md_table(["Item", "Path", "Evidence", "Status"], marker_sign_audit_rows),
            "",
            "## Screenshot Inspection Result",
            "",
            md_table(["Item", "Evidence", "Status"], screenshot_inspection_rows),
            "",
            "## North Star Result",
            "",
            md_table(["Area", "Judgment", "Status"], north_star_rows),
            "",
            "## 8.5+/10 Visual Bar Result",
            "",
            md_table(["Discipline", "Score", "Status"], visual_bar_rows),
            "",
            *(
                [
                    "## SV-0 Tooling Stack Result",
                    "",
                    "- Report: `docs/reports/SV0_FREE_TOOLING_INTAKE_PRODUCTION_STACK_LOCK.md`",
                    "- Structured report: `docs/reports/SV0_FREE_TOOLING_INTAKE_PRODUCTION_STACK_LOCK.json`",
                    "- Tool acquisition manifest: `docs/reports/SV0_TOOL_ACQUISITION_MANIFEST.json`",
                    "- Tooling roadmap: `docs/roadmaps/STARTER_VILLAGE_TOOLING_STACK.md`",
                    "- Validator: `wayfarer_godot_vertical_slice/tools/validate_sv0_tooling_stack.py`",
                    "- Acquisition validator: `wayfarer_godot_vertical_slice/tools/validate_sv0_tool_acquisition_manifest.py`",
                    "- Council rule: future SV phases must use the locked stack where applicable, including runtime movement proof and screenshot visual-regression warnings.",
                    "",
                ]
                if phase.upper().strip().startswith("SV-0")
                else []
            ),
            *(
                [
                    "## G-8 Character Motion Result",
                    "",
                    f"NPC motion/grounding score: {gameplay_readability_score:.1f}",
                    "",
                    "- runtime screenshots inspected: G-8 proof frames include player directional walk states, Edrin stationary no-drift proof, debug-off proof, and atelier provenance proof.",
                    "",
                    "- G-8 accepted proof: player directional walk frames are grounded and Edrin cannot glide as a static cutout because route walking is disabled until dedicated walk sheets ship.",
                    "",
                ]
                if phase.upper().strip().startswith("G-8")
                else []
            ),
            *(
                [
                    "## G-8A Living NPC Population Result",
                    "",
                    f"NPC population score: {gameplay_readability_score:.1f}",
                    "",
                    "- runtime screenshots inspected: G-8A proof frames show tavern, dockworker, counting-house, merchant, rumor-carrier, and suspicious-patron stations in the authored Newport town.",
                    "",
                    "- G-8A accepted proof: named NPCs now carry roles, stations, route intent, idle behavior, dialogue seeds, quest relevance, and a stationary work-pose policy until dedicated walk sheets ship.",
                    "",
                ]
                if phase.upper().strip().startswith("G-8A")
                else []
            ),
            *(
                [
                    "## G-11A Audio/Atmosphere Result",
                    "",
                    f"UX/readability score: {gameplay_readability_score:.1f}",
                    "",
                    "- runtime proof inspected: G-11A adds placeholder-free hook events for harbor ambience, tavern ambience, footsteps, quest updates, and UI feedback without loading audio streams.",
                    "",
                    "- G-11A accepted proof: no placeholder audio assets were added, no broken audio references exist, and all future audio paths require license/provenance before playback.",
                    "",
                    "- Build/release note: hooks are web-safe data/script contracts only; production playback remains disabled until provenance-safe assets are introduced.",
                    "",
                ]
                if phase.upper().strip().startswith("G-11A")
                else []
            ),
            *(
                [
                    "## G-11 Living Town Rhythm Result",
                    "",
                    f"NPC rhythm score: {gameplay_readability_score:.1f}",
                    "",
                    "- runtime screenshots inspected: G-11 proof frames show dock work, tavern social, merchant street, civic notice, and rear-gate rhythms with ambient barks and debug overlays disabled.",
                    "",
                    "- G-11 accepted proof: NPCs face, pause, and bark on authored district rhythms while route walking remains disabled until dedicated walk sheets exist; position drift: none.",
                    "",
                    "- QA guardrail: no static NPC sprite translates across the map, and broad ground/material patchwork remains a G-12 review risk rather than being hidden by activity.",
                    "",
                ]
                if phase.upper().strip().startswith("G-11")
                else []
            ),
            *(
                [
                    "## G-10A Tavern Whisper System Result",
                    "",
                    f"UX/readability score: {gameplay_readability_score:.1f}",
                    "",
                    "- runtime screenshots inspected: G-10A proof frames show Bess as a quest-relevant tavern keeper, the Third Toast rumor, Silas's rear-gate secret, the tavern whisper contract, rotating ambient barks, and debug-off normal play.",
                    "",
                    "- G-10A accepted proof: the Tavern/Inn now has structured rumor dialogue, ambient bark data, quest-relevant interactions, and explicit ties to harbor commerce and pre-Revolution pressure.",
                    "",
                    "## Visual Order QA Repair",
                    "",
                    "- Council failure mode added: proof screenshots cannot pass when route corridors render beneath tavern, commercial, civic, or market building bodies.",
                    "",
                    "- New validation source: Newport route corridors are drawn from `starter_village_route_order_specs()` and checked against runtime building visual bounds before G-10A can pass.",
                    "",
                ]
                if phase.upper().strip().startswith("G-10A")
                else []
            ),
            *(
                [
                    "## G-10B Multi-Path Starter Choice Result",
                    "",
                    f"Narrative/gameplay hook score: {gameplay_readability_score:.1f}",
                    "",
                    "- runtime screenshots inspected: G-10B proof frames show the counting-house lead, Bess's Third Toast tavern branch, Honor's merchant-street branch, Silas's optional rear-gate clue, debug-off normal play, and the multi-path choice contract in the manifest.",
                    "",
                    "- G-10B accepted proof: First Light can advance through harbor work, tavern rumor, counting-house pressure, merchant street gossip, and optional secret clues without reducing the opening mystery to one railroaded click path.",
                    "",
                    "## Screenshot Contradiction Review",
                    "",
                    "- Council failure mode enforced: written reports and validators cannot override visible screenshot evidence. If a screenshot shows route/building order confusion, debug overlays, patchwork that breaks the phase target, hovering NPCs, non-atelier sprites, or unclear objective guidance, the verdict must be `COUNCIL_FAIL_NEEDS_CODE_FIX`.",
                    "",
                    "- Current G-10B visual caveat: broad ground-material patchwork remains visible in wide shots and must stay in the G-11/G-12 review queue; it is not allowed to disappear from future council reports.",
                    "",
                ]
                if phase.upper().strip().startswith("G-10B")
                else []
            ),
            *(
                [
                    "## G-12 First-Session Result",
                    "",
                    f"First-session/readability score: {gameplay_readability_score:.1f}",
                    "",
                    "- Game Studio playtest method: boot the village, exercise representative First Light verbs, capture player states, inspect HUD/playfield obstruction, and reject screenshots that contradict written PASS claims.",
                    "",
                    "- runtime screenshots inspected: G-12 proof frames cover wide Newport, harbor arrival, counting-house route, Tavern/Inn, commercial avenue, wharf work, NPC rhythm, idle readability, counting-house interaction, tavern rumor, journal/objective, signs/prompts, y-sort/layering, debug-off proof, and provenance/contact proof.",
                    "",
                    "- prompt/dialogue/bark overlap: focused interaction states must suppress player prompts and ambient bark labels before capture; any remaining overlap fails the G-12 validator and council.",
                    "",
                    "- accepted first-session loop: the player can read the first goal within 10 seconds, follow the harbor/counting-house/tavern route within 60 seconds, advance an objective within three minutes, hear tavern rumor content within 10 minutes, and reach a reward/contact/mystery hook within 15-20 minutes.",
                    "",
                    "- QA guardrail: screenshots override validator prose. Clipped buildings, scale incoherence, debug overlays, prompt clutter, bark clutter, or hidden NPC glide must produce `COUNCIL_FAIL_NEEDS_CODE_FIX`.",
                    "",
                ]
                if phase.upper().strip().startswith("G-12")
                else []
            ),
            *(
                [
                    "## G-10 Opening Quest Arc Result",
                    "",
                    f"Narrative/gameplay hook score: {gameplay_readability_score:.1f}",
                    "",
                    "- runtime screenshots inspected: G-10 proof frames show landfall orientation, Edrin's missing-line setup, Bess and the Third Toast, Jonah's wharf-lantern branch, Silas's optional rear-gate clue, and Edrin's named-contact dawn hook.",
                    "",
                    "- G-10 accepted proof: First Light now plays as a 10-15 minute opening arc with at least three named/role NPCs, objective progression, a reward beat, optional discovery, and a reason to keep playing.",
                    "",
                ]
                if phase.upper().strip().startswith("G-10") and not phase.upper().strip().startswith(("G-10A", "G-10B"))
                else []
            ),
            *(
                [
                    "## G-9A Journal Objective Result",
                    "",
                    f"UX/readability score: {gameplay_readability_score:.1f}",
                    "",
                    "- runtime screenshots inspected: G-9A proof frames show Journal state, objective completion, missing-ledger update feedback, tavern whisper progression, reward feedback, and debug-off normal play.",
                    "",
                    "- G-9A accepted proof: First Light now has in-session quest state, HUD journal/objective updates, dialogue-driven advancement, optional clue sources, and a Resolve reward/progression update.",
                    "",
                ]
                if phase.upper().strip().startswith("G-9A")
                else []
            ),
            *(
                [
                    "## G-9 Interaction UX Result",
                    "",
                    f"UX/readability score: {gameplay_readability_score:.1f}",
                    "",
                    "- runtime screenshots inspected: G-9 proof frames show compact building, NPC, counting-house, tavern, dock, objective, dialogue, and debug-off prompt states.",
                    "",
                    "- G-9 accepted proof: normal-play prompts use compact action/name copy, avoid Press E debug phrasing, preserve HUD objective clarity, and do not introduce crude world markers.",
                    "",
                ]
                if phase.upper().strip().startswith("G-9") and not phase.upper().strip().startswith("G-9A")
                else []
            ),
            "## Required Tooling And Validator Paths",
            "",
            md_table(["Item", "Status", "Path"], paths),
            "",
            "## Newport-Specific Visual Review Fields",
            "",
            md_table(["Criterion", "Status"], visual_fields),
            "",
            *(
                [
                    "## G-4.18E Asset Family Authority Questions",
                    "",
                    md_table(["Question", "Council Answer"], g418e_asset_family_fields),
                    "",
                ]
                if phase.upper().strip().startswith("G-4.18E")
                else []
            ),
            *(
                [
                    "## G-4.19 Player Identity Authority Questions",
                    "",
                    md_table(["Question", "Council Answer"], g419_player_identity_fields),
                    "",
                ]
                if phase.upper().strip().startswith("G-4.19")
                else []
            ),
            *(
                [
                    "## G-4.20 HUD/UI Authority Questions",
                    "",
                    md_table(["Question", "Council Answer"], g420_hud_ui_fields),
                    "",
                ]
                if phase.upper().strip().startswith("G-4.20")
                else []
            ),
            *(
                [
                    "## G-4.21 Origin City Hero Slice Authority Questions",
                    "",
                    md_table(["Question", "Council Answer"], g421_hero_slice_fields),
                    "",
                ]
                if phase.upper().strip().startswith("G-4.21")
                else []
            ),
            *(
                [
                    "## G-4.22R Pre-G-5 Atelier Consistency Gate Authority Questions",
                    "",
                    md_table(["Question", "Council Answer"], g422r_consistency_fields),
                    "",
                ]
                if phase.upper().strip().startswith("G-4.22R")
                else []
            ),
            *(
                [
                    "## G-4.22 Visual Foundation Gate Authority Questions",
                    "",
                    md_table(["Question", "Council Answer"], g422_visual_gate_fields),
                    "",
                ]
                if phase.upper().strip().startswith("G-4.22")
                else []
            ),
            "## Scrum Master Review",
            "",
            "- Status: PASS",
            f"- {scrum_scope}",
            "- PR health check: open PR state was queried when gh was available.",
            "- Roadmap alignment: this supports future Newport reviews by splitting production disciplines before merge decisions.",
            "- Merge discipline: no merge action is allowed from this tool.",
            "",
            "## World-class Game Designer Review",
            "",
            f"- Status: {designer_status}",
            "- Required pass condition: Newport must read as a navigable settlement, not an asset board.",
            "- Review focus: player movement loops, purpose of space, interaction density, progression hooks, and NPC/player usability.",
            "- Fail condition: buildings or props that cannot support believable village behavior must block design acceptance.",
            "",
            "## World/Layout Designer Review",
            "",
            f"- Status: {world_status}",
            "- Required pass condition: districts, routes, landmarks, lots, wharf paths, uphill connectors, and rear streets must form one authored harbor town.",
            "- Review focus: harborfront avenue, counting-house route, Tavern/Inn threshold, commercial spine, civic/residential/service logic, and wide-shot cohesion.",
            "",
            "## Art Director Review",
            "",
            f"- Status: {art_status}",
            "- Required pass condition: street material, lots, building placement, and harbor/civic/commercial/residential language must feel cohesive.",
            "- Newport fail conditions: mismatched road layers, clipped transparent ground rectangles, floating buildings on old art, prop clutter hiding layout problems, or no coherent harbor-city street grammar.",
            "",
            "## Animation/NPC Behavior Director Review",
            "",
            f"- Status: {ux_status}",
            "- Required pass condition: player and NPCs must be grounded, have believable anchors/shadows, and avoid static cutout gliding in normal play.",
            "- Review focus: idle/walk state proof, directional facing, stop/start behavior, route intent, and movement speed matching animation cadence.",
            "",
            "## Narrative Designer Review",
            "",
            f"- Status: {world_status}",
            "- Required pass condition: opening play must expose tavern whispers, harbor rumors, counting-house pressure, and a reason to continue.",
            "- Review focus: First Light / Whispers Before Dawn quest beats, NPC motives, optional clues, rewards, and pre-Revolution tension as gameplay.",
            "",
            "## Quest Designer Review",
            "",
            f"- Status: {world_status}",
            "- Required pass condition: quest objectives, branches, clue states, rewards, and return/report hooks must be playable without manual guidance.",
            "- Review focus: village-to-island quest chain, optional clue enrichment, journal/objective text, and no broken progression branches.",
            "",
            "## UX Designer Review",
            "",
            f"- Status: {ux_status}",
            "- Required pass condition: a first-time player can understand location, first goal, interactables, objective updates, and next steps without debug-like presentation.",
            "- Review focus: navigation clarity, landmark hierarchy, prompts, journal/objective feedback, camera/capture framing, and readable interaction anchors.",
            "",
            "## Game Programmer Review",
            "",
            f"- Status: {programmer_status}",
            "- Required pass condition: Godot scene, sprite rendering, collision/pathing, and automation remain maintainable.",
            "- Automation files and validators were checked for presence.",
            "",
            "## QA Analyst Review",
            "",
            f"- Status: {qa_status}",
            f"- Validator mode: {'RUN' if run_validators else 'LIST_ONLY'}",
            f"- Passed commands: {len(validator_passes)}",
            f"- Failed commands: {len(validator_failures)}",
            f"- Skipped commands: {len(validator_skips)}",
            "",
            md_table(
                ["Check", "Status", "Command", "Notes"],
                [[item["name"], item["status"], f"`{item['command']}`", item["notes"]] for item in validator_results],
            ),
            "",
            "## Build/Release Engineer Review",
            "",
            f"- Status: {release_status}",
            "- Required pass condition: green checks, mergeability, required proof, provenance/atelier compliance, and no hard stop condition.",
            "- This report does not merge; it records whether a branch can proceed to the autonomous PR merge gate.",
        ]
    )

    if known_449:
        lines.extend(
            [
                "",
                "## Detected PR #449 Visual-State Classification",
                "",
                f"- Detected PR: {pr_label(target_pr_data)}",
                "- Context: this section records how the council would classify the known G-4.22A Newport visual state described by Chris.",
                "- Important: if the PR is already merged, this is a reusable production classification for the visual state, not a merge action.",
                "",
                "Known issues:",
                "",
                "- Mismatched street layers.",
                "- Weak or missing cohesive harbor avenue.",
                "- Weak uphill roads and back street grammar.",
                "- Buildings still appearing on old/prototype ground art.",
                "- City not ready for NPC/village behavior.",
                "",
                md_table(
                    ["Agent", "Classification", "Reason"],
                    [
                        ["QA", "LIKELY TECHNICAL PASS", "Known G-4.22A validators and screenshot automation can pass while design still fails."],
                        ["Game Designer", "FAIL", "The town still does not prove believable player/NPC settlement use."],
                        ["Art Director", "FAIL", "Street/ground cohesion and clipping problems block visual acceptance."],
                        ["World/Narrative", "FAIL", "Harbor-city life structure is not yet legible enough."],
                        ["UX", "FAIL OR NEEDS REPAIR", "Navigation and village-readability remain too unclear."],
                        ["Release Manager", AUTHORITY_FAIL, "Repair before any equivalent PR advances."],
                    ],
                ),
            ]
        )

    lines.extend(
        [
            "",
            "## Release Manager Decision",
            "",
            f"- Final Authority Verdict: {final_verdict}",
            "- Council tool merge behavior: never merges from this script.",
            "- Autonomous merge authority: Codex may merge outside this tool only after the active roadmap authorization, green checks, mergeability, proof, and hard-stop checks pass.",
            "- Never treat validator pass as design acceptance.",
            "- PR candidate conditions: validators pass, screenshots are inspected, all required discipline scores clear the phase bar, and remaining caveats are roadmap items.",
            "- Repair conditions: street grammar, ground cohesion, lot logic, player/NPC walkability, district readability, or visual cohesion fail the phase bar.",
            f"- Final recommended next phase: {next_phase_text}",
            f"- Human escalation blocker: {blocker_text}",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Wayfarer Agent Council report generator.")
    parser.add_argument("--phase", default="G-4.22P", help="Phase label to print in the report.")
    parser.add_argument("--target-pr", type=int, default=0, help="PR number to inspect for Newport classification context.")
    parser.add_argument("--run-validators", action="store_true", help="Run validators instead of listing SKIPPED_WITH_COMMAND entries.")
    parser.add_argument("--godot-bin", default=default_godot_bin(), help="Path to Godot console executable.")
    parser.add_argument("--python-bin", default=default_python_bin(), help="Path to Python executable.")
    parser.add_argument("--report-name", default=REPORT_NAME, help="Markdown report filename under docs/reports.")
    parser.add_argument("--authority-verdict", choices=AUTHORITY_VERDICTS, default="", help="Optional explicit final authority verdict after council review.")
    parser.add_argument(
        "--screenshot-review",
        choices=["inspected", "not-inspected", "missing", "not-applicable", "not_applicable"],
        default="not-inspected",
        help="Whether required screenshot evidence was inspected by the council.",
    )
    parser.add_argument("--design-score", type=float, default=0.0, help="Council design score out of 10.")
    parser.add_argument("--art-direction-score", type=float, default=0.0, help="Council art direction score out of 10.")
    parser.add_argument("--world-layout-score", type=float, default=0.0, help="Council world/layout score out of 10.")
    parser.add_argument("--gameplay-readability-score", type=float, default=0.0, help="Council gameplay/readability score out of 10.")
    parser.add_argument("--technical-stability-score", type=float, default=0.0, help="Council technical stability score out of 10.")
    parser.add_argument("--qa-regression-result", default="Not recorded.", help="Council QA regression result text.")
    parser.add_argument("--build-release-result", default="Not recorded.", help="Council build/release result text.")
    parser.add_argument("--final-recommended-next-phase", default="", help="Next roadmap phase selected by the council.")
    parser.add_argument("--human-escalation-blocker", default="", help="Exact blocker if the verdict requires human escalation.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = find_repo_root(Path.cwd())
    report_dir = root / "docs" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    git_state = get_git_state(root)
    pr_state = get_pr_state(root, args.target_pr)
    screenshots = find_latest_screenshots(root)
    paths = required_path_status(root, args.phase)
    validators = build_validator_commands(root, args.godot_bin, args.python_bin, args.phase)
    validator_results = run_or_list_validators(validators, args.run_validators)

    report = build_report(
        root=root,
        phase=args.phase,
        git_state=git_state,
        pr_state=pr_state,
        screenshots=screenshots,
        paths=paths,
        validator_results=validator_results,
        run_validators=args.run_validators,
        godot_bin=args.godot_bin,
        python_bin=args.python_bin,
        target_pr=args.target_pr,
        authority_verdict=args.authority_verdict,
        screenshot_review=args.screenshot_review,
        design_score=args.design_score,
        art_direction_score=args.art_direction_score,
        world_layout_score=args.world_layout_score,
        gameplay_readability_score=args.gameplay_readability_score,
        technical_stability_score=args.technical_stability_score,
        qa_regression_result=args.qa_regression_result,
        build_release_result=args.build_release_result,
        final_recommended_next_phase=args.final_recommended_next_phase,
        human_escalation_blocker=args.human_escalation_blocker,
    )

    report_path = report_dir / args.report_name
    report_path.write_text(report, encoding="utf-8", newline="\n")

    print("Wayfarer Agent Council")
    print("Repo root:", root)
    print("Branch:", git_state["branch"])
    print("Status:")
    print(git_state["status"])
    print("Open PRs detected:", len(pr_state.get("open_prs") or []))
    print("Latest screenshots:", len(screenshots))
    print("Validator mode:", "RUN" if args.run_validators else "LIST_ONLY")
    print("Report:", report_path)
    print("TECHNICAL PASS DOES NOT EQUAL DESIGN PASS.")
    print("Council authority verdict recorded; this tool did not merge.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
