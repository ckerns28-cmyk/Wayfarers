#!/usr/bin/env python3
"""Wayfarer Agent Council runner.

This script creates a repo-local production review report. For ordinary pre-G-5
work, the council is the acceptance authority after screenshots are inspected
and validators pass. It still never merges, never impersonates Chris, and never
treats a technical pass by itself as design approval.
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
        if candidate.exists():
            return str(candidate)
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


def build_validator_commands(root: Path, godot_bin: str, python_bin: str, phase: str) -> list[ValidatorCommand]:
    game_root = root / "wayfarer_godot_vertical_slice"
    capture_label, capture_prefix = screenshot_prefix_for_phase(phase)
    capture_ps1 = game_root / "tools" / f"capture_{capture_prefix}_runtime_screenshots.ps1"
    capture_log = game_root / "artifacts" / "review" / f"{capture_prefix}_runtime_screenshots" / "godot_capture.log"

    godot_import_text = f"& {powershell_quote(godot_bin)} --headless --path wayfarer_godot_vertical_slice --import"
    vertical_text = (
        "Push-Location wayfarer_godot_vertical_slice; "
        f"& {powershell_quote(godot_bin)} --headless --path . --script res://tools/validate_vertical_slice.gd; "
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
            args=[godot_bin, "--headless", "--path", str(game_root), "--import"],
            cwd=root,
            required_paths=[game_root],
        ),
        ValidatorCommand(
            name="validate_vertical_slice.gd",
            command_text=vertical_text,
            args=[godot_bin, "--headless", "--path", ".", "--script", "res://tools/validate_vertical_slice.gd"],
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
    required = [
        ("Vertical slice validator", game_root / "tools" / "validate_vertical_slice.gd"),
        ("G-4.22A runtime screenshot wrapper", game_root / "tools" / "capture_g422a_runtime_screenshots.ps1"),
        ("G-4.22A runtime screenshot script", game_root / "tools" / "capture_g422a_runtime_screenshots.gd"),
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
    if capture_prefix != "g422a":
        required.extend(
            [
                (f"{capture_label} runtime screenshot wrapper", game_root / "tools" / f"capture_{capture_prefix}_runtime_screenshots.ps1"),
                (f"{capture_label} runtime screenshot script", game_root / "tools" / f"capture_{capture_prefix}_runtime_screenshots.gd"),
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
    if not screenshots or screenshot_review != "inspected":
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

    screenshots_inspected = bool(screenshots) and screenshot_review == "inspected"
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

    agent_rows = [
        ["Scrum Master", "PASS", "Branch/PR state gathered; no auto-merge allowed."],
        ["Game Designer", designer_status, "Newport layout must prove street grammar, loops, and NPC/player usability."],
        ["Art Director", art_status, "Ground/street cohesion and clipping must clear council visual review."],
        ["Game Programmer", "PASS" if all(status == "FOUND" for _, status, _ in paths) else "FAIL", "Required automation and validator files checked."],
        ["QA", qa_status, "Validators must pass, but technical pass is not design approval."],
        ["World/Narrative", world_status, "Harbor economy, civic/commercial/residential logic must clear council review."],
        ["UX", ux_status, "Navigation clarity, landmarks, and player orientation must clear council review."],
        ["Technical Artist", technical_artist_status, "Pipeline files, layering/contact/provenance, and screenshot evidence were considered."],
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
    elif phase.upper().strip().startswith("G-4.19"):
        scrum_scope = "Scope check: this council pass replaces the drawn player placeholder with a directional runtime sprite foundation while preserving Newport layout, collision, camera, spawn, and interaction behavior."
    elif phase.upper().strip().startswith("G-4.20"):
        scrum_scope = "Scope check: this council pass redesigns HUD/UI presentation only; it keeps no-HUD capture, review metadata, Newport runtime layout, player movement, collision, camera, and interaction behavior intact."
    elif phase.upper().strip().startswith("G-4.21"):
        scrum_scope = "Scope check: this council pass composes the accepted Newport street/dock layout, G-4.18E props, G-4.19 player, and G-4.20 HUD into a hero-slice screenshot packet without changing core gameplay systems."
    elif phase.upper().strip().startswith("G-4.22"):
        scrum_scope = "Scope check: this council pass is the formal G-4 visual foundation gate; it records acceptance authority and may recommend G-5 only if screenshots, provenance, validators, and council scores clear the gate."
    else:
        scrum_scope = "Scope check: this council pass changes production documentation and tooling only; it must not change Newport runtime layout."

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
        "For ordinary pre-G-5 work, this report is the council authority verdict after validators and screenshot review. It never auto-merges, never impersonates Chris, and never converts technical validation alone into creative approval.",
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
                    ["Does this meet the 8.5+/10 pre-G-5 visual/world bar?", yes_no(meets_bar)],
                    ["Does this advance Wayfarer toward the North Star?", yes_no(advances_north_star)],
                    ["Is human visual review truly required, or can the council accept this?", "Human review required only for true blocker." if human_review_required else "Council can accept this ordinary pre-G-5 pass."],
                    ["If human review is required, what exact blocker justifies escalation?", blocker_text if human_review_required else "None."],
                ],
            ),
            "",
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
            "## Game Designer Review",
            "",
            f"- Status: {designer_status}",
            "- Required pass condition: Newport must read as a navigable settlement, not an asset board.",
            "- Review focus: player movement loops, purpose of space, interaction density, progression hooks, and NPC/player usability.",
            "- Fail condition: buildings or props that cannot support believable village behavior must block design acceptance.",
            "",
            "## Art Director Review",
            "",
            f"- Status: {art_status}",
            "- Required pass condition: street material, lots, building placement, and harbor/civic/commercial/residential language must feel cohesive.",
            "- Newport fail conditions: mismatched road layers, clipped transparent ground rectangles, floating buildings on old art, prop clutter hiding layout problems, or no coherent harbor-city street grammar.",
            "",
            "## Game Programmer Review",
            "",
            f"- Status: {'PASS' if all(status == 'FOUND' for _, status, _ in paths) else 'FAIL'}",
            "- Required pass condition: Godot scene, sprite rendering, collision/pathing, and automation remain maintainable.",
            "- Automation files and validators were checked for presence.",
            "",
            "## QA Review",
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
            "## World/Narrative Review",
            "",
            f"- Status: {world_status}",
            "- Required pass condition: Newport must express a lived-in harbor city with civic, commercial, residential, tavern, and working waterfront logic.",
            "- Review focus: work/life structure, harbor economy, story hooks, class/civic relationships, and the Tavern/Inn as a social anchor.",
            "",
            "## UX Review",
            "",
            f"- Status: {ux_status}",
            "- Required pass condition: a player can orient by landmarks, understand where paths lead, and see why spaces exist.",
            "- Review focus: navigation clarity, landmark hierarchy, camera/capture framing, and readable interaction anchors.",
            "",
            "## Technical Artist Review",
            "",
            f"- Status: {technical_artist_status}",
            "- Required pass condition: sprite provenance, atlas integrity, layering, shadows/contact, ground transitions, and asset pipeline compliance all hold together.",
            "- Council authority requires screenshot inspection for layering/contact quality.",
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
            "- Never auto-merge.",
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
    parser.add_argument("--target-pr", type=int, default=449, help="PR number to inspect for Newport classification context.")
    parser.add_argument("--run-validators", action="store_true", help="Run validators instead of listing SKIPPED_WITH_COMMAND entries.")
    parser.add_argument("--godot-bin", default=default_godot_bin(), help="Path to Godot console executable.")
    parser.add_argument("--python-bin", default=default_python_bin(), help="Path to Python executable.")
    parser.add_argument("--report-name", default=REPORT_NAME, help="Markdown report filename under docs/reports.")
    parser.add_argument("--authority-verdict", choices=AUTHORITY_VERDICTS, default="", help="Optional explicit final authority verdict after council review.")
    parser.add_argument(
        "--screenshot-review",
        choices=["inspected", "not-inspected", "missing"],
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
    print("Council authority verdict recorded; no auto-merge performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
