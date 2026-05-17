#!/usr/bin/env python3
"""Wayfarer Agent Council runner.

This script creates a repo-local production review report. It is deliberately
conservative: technical checks can pass, but visual/world/design fields stay
NEEDS_HUMAN_REVIEW unless a human reviewer or a more capable visual inspection
tool explicitly marks them otherwise.
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
    if normalized.startswith("G-4.23B"):
        return "G-4.23B", "g423b"
    if normalized.startswith("G-4.23A"):
        return "G-4.23A", "g423a"
    if normalized.startswith("G-4.22A"):
        return "G-4.22A", "g422a"
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
    extraction_text = (
        f"& {powershell_quote(python_bin)} "
        r"wayfarer_godot_vertical_slice\art_pipeline\newport_atelier\scripts\extract_g421a_core_building_assets.py "
        "--skip-registry --skip-building-provenance"
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

    return [
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
                "--skip-registry",
                "--skip-building-provenance",
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
) -> str:
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    target_pr_data = pr_state.get("target_pr")
    open_prs = pr_state.get("open_prs")
    known_449 = target_pr == 449 and isinstance(target_pr_data, dict)
    validator_failures = [item for item in validator_results if item["status"] == "FAIL"]
    validator_passes = [item for item in validator_results if item["status"] == "PASS"]
    validator_skips = [item for item in validator_results if item["status"] == "SKIPPED_WITH_COMMAND"]
    qa_status = "PASS" if run_validators and not validator_failures else "NEEDS_HUMAN_REVIEW"
    if validator_failures:
        qa_status = "FAIL"

    if known_449:
        release_recommendation = "REPAIR SAME PR / DO NOT MERGE for any Newport PR with this visual state"
        designer_status = "FAIL"
        art_status = "FAIL"
        world_status = "FAIL"
        ux_status = "FAIL"
    else:
        release_recommendation = "NEEDS_HUMAN_REVIEW"
        designer_status = "NEEDS_HUMAN_REVIEW"
        art_status = "NEEDS_HUMAN_REVIEW"
        world_status = "NEEDS_HUMAN_REVIEW"
        ux_status = "NEEDS_HUMAN_REVIEW"

    agent_rows = [
        ["Scrum Master", "PASS", "Branch/PR state gathered; no auto-merge allowed."],
        ["Game Designer", designer_status, "Newport layout must prove street grammar, loops, and NPC/player usability."],
        ["Art Director", art_status, "Ground/street cohesion and clipping must be visually reviewed."],
        ["Game Programmer", "PASS" if all(status == "FOUND" for _, status, _ in paths) else "FAIL", "Required automation and validator files checked."],
        ["QA", qa_status, "Validators listed or run; technical pass is not design approval."],
        ["World/Narrative", world_status, "Harbor economy, civic/commercial/residential logic need explicit review."],
        ["UX", ux_status, "Navigation clarity, landmarks, and player orientation need explicit review."],
        ["Technical Artist", "NEEDS_HUMAN_REVIEW", "Pipeline files found; layering/contact/provenance still need review."],
    ]

    visual_fields = [
        ["Does Newport read as a harbor city?", "NEEDS_HUMAN_REVIEW"],
        ["Is there a waterfront avenue parallel to the harbor?", "NEEDS_HUMAN_REVIEW"],
        ["Are there roads running uphill from harbor into town?", "NEEDS_HUMAN_REVIEW"],
        ["Is there a back street behind the first road?", "NEEDS_HUMAN_REVIEW"],
        ["Are buildings sitting on coherent lots?", "NEEDS_HUMAN_REVIEW"],
        ["Is the ground/street style unified?", "NEEDS_HUMAN_REVIEW"],
        ["Are old clipped/transparent road rectangles gone?", "NEEDS_HUMAN_REVIEW"],
        ["Is there believable player/NPC walkability?", "NEEDS_HUMAN_REVIEW"],
        ["Are civic, market, tavern, harbor, and residential districts legible?", "NEEDS_HUMAN_REVIEW"],
        ["Does the harbor economy read clearly?", "NEEDS_HUMAN_REVIEW"],
        ["Are props supporting function instead of hiding layout problems?", "NEEDS_HUMAN_REVIEW"],
        ["Does the scene support 90+ seconds of exploration in principle?", "NEEDS_HUMAN_REVIEW"],
        ["Does it approach the Newport 8.5+/10 bar?", "NEEDS_HUMAN_REVIEW"],
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
        "This report is a Recommendation for Chris. It never auto-merges, never impersonates Chris, and never converts technical validation into creative approval.",
        "",
        "## Summary",
        "",
        f"- Generated: {now}",
        f"- Repo root: `{root}`",
        f"- Phase: {phase}",
        f"- Branch: `{git_state['branch']}`",
        f"- HEAD: `{git_state['head']}`",
        f"- origin/main: `{git_state['origin_main']}`",
        f"- Current branch PR: {current_pr_from_open(open_prs, git_state['branch'])}",
        f"- Target PR check: {pr_label(target_pr_data)}",
        f"- Recommendation for Chris: {release_recommendation}",
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
            "Visual fields remain NEEDS_HUMAN_REVIEW because this script locates screenshot artifacts but does not judge image quality.",
            "",
            "## Required Tooling And Validator Paths",
            "",
            md_table(["Item", "Status", "Path"], paths),
            "",
            "## Newport-Specific Visual Review Fields",
            "",
            md_table(["Criterion", "Status"], visual_fields),
            "",
            "## Scrum Master Review",
            "",
            "- Status: PASS",
            "- Scope check: this council pass changes production documentation and tooling only; it must not change Newport runtime layout.",
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
            "- Status: NEEDS_HUMAN_REVIEW",
            "- Required pass condition: sprite provenance, atlas integrity, layering, shadows/contact, ground transitions, and asset pipeline compliance all hold together.",
            "- This script verifies pipeline paths but does not visually approve layering/contact quality.",
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
                        ["Release Manager", "REPAIR SAME PR / DO NOT MERGE", "Recommendation for Chris: repair before any equivalent PR is merged."],
                    ],
                ),
            ]
        )

    lines.extend(
        [
            "",
            "## Release Manager Decision",
            "",
            f"- Recommendation for Chris: {release_recommendation}",
            "- Never auto-merge.",
            "- Never treat validator pass as design acceptance.",
            "- Merge candidate conditions: all required agents pass, or remaining issues are explicitly marked acceptable for the phase.",
            "- Blockers to resolve before Newport layout acceptance: street grammar, ground cohesion, lot logic, player/NPC walkability, district readability, and visual cohesion.",
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
    print("Recommendation for Chris only; no auto-merge performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
