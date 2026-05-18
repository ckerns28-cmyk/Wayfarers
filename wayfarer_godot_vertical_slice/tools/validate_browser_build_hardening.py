#!/usr/bin/env python3
"""Validate G-13 browser build identity and package hardening gates."""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

from starter_village_validator_common import (
    LEDGER_JSON,
    PROJECT_ROOT,
    REPO_ROOT,
    load_json,
    phase_map,
    print_result,
    require_text,
)


PHASE = "G-13"
BRANCH = "codex/g-13-browser-build-hardening"
LABEL = "Godot G-13 Browser Build, Performance, and Regression Hardening"

BUILD_INFO = PROJECT_ROOT / "scripts" / "BuildInfo.gd"
VERTICAL_SLICE_VALIDATOR = PROJECT_ROOT / "tools" / "validate_vertical_slice.gd"
PACKAGE_SCRIPT = PROJECT_ROOT / "tools" / "package_itch_web.sh"
STABLE_ZIP = PROJECT_ROOT / "artifacts" / "wayfarers-tale-godot-web.zip"
VERSIONED_ZIP = PROJECT_ROOT / "artifacts" / "wayfarers-tale-godot-g-13-browser-build-performance-and-regression-hardening.zip"
G13_REPORT = REPO_ROOT / "docs" / "reports" / "G13_BROWSER_BUILD_PERFORMANCE_REGRESSION_HARDENING.md"
G13_COUNCIL_REPORT = REPO_ROOT / "docs" / "reports" / "G13_BROWSER_BUILD_AGENT_COUNCIL_REPORT.md"


def _read_build_info_constants(failures: list[str]) -> dict[str, str]:
    if not BUILD_INFO.exists():
        failures.append("missing BuildInfo.gd")
        return {}
    text = BUILD_INFO.read_text(encoding="utf-8")
    constants: dict[str, str] = {}
    for name in [
        "BUILD_PHASE",
        "BUILD_LABEL",
        "SOURCE_BRANCH",
        "REVIEW_HOST",
        "REVIEW_CHANNEL",
        "REVIEW_SCREENSHOT_FLAG",
        "PLAYER_STYLE_ROADMAP_NOTE",
    ]:
        match = re.search(rf'const {name} := "([^"]*)"', text)
        if not match:
            failures.append(f"BuildInfo.gd missing {name}")
            continue
        constants[name] = match.group(1)
    return constants


def _validate_zip(path: Path, failures: list[str]) -> None:
    if not path.exists():
        failures.append(f"missing review ZIP: {path.relative_to(REPO_ROOT).as_posix()}")
        return
    try:
        with zipfile.ZipFile(path, "r") as archive:
            names = set(archive.namelist())
    except zipfile.BadZipFile as exc:
        failures.append(f"invalid review ZIP {path.name}: {exc}")
        return
    for required in [
        "index.html",
        "index.js",
        "index.pck",
        "index.wasm",
        "index.audio.worklet.js",
        "index.audio.position.worklet.js",
    ]:
        if required not in names:
            failures.append(f"{path.name} missing ZIP root entry: {required}")
    if "web_build/index.html" in names:
        failures.append(f"{path.name} must not contain web_build/index.html")


def main() -> int:
    failures: list[str] = []
    constants = _read_build_info_constants(failures)
    if constants:
        expected = {
            "BUILD_PHASE": PHASE,
            "BUILD_LABEL": LABEL,
            "SOURCE_BRANCH": BRANCH,
            "REVIEW_HOST": "itch",
            "REVIEW_CHANNEL": "manual ZIP",
            "REVIEW_SCREENSHOT_FLAG": "--review-no-hud",
        }
        for key, value in expected.items():
            if constants.get(key) != value:
                failures.append(f"BuildInfo.gd {key} must be {value!r}, found {constants.get(key)!r}")
        note = constants.get("PLAYER_STYLE_ROADMAP_NOTE", "")
        for token in ["G-13", "G-4.22R", "atelier runtime asset gate", "browser review build"]:
            if token not in note:
                failures.append(f"BuildInfo.gd PLAYER_STYLE_ROADMAP_NOTE missing {token}")

    require_text(
        VERTICAL_SLICE_VALIDATOR,
        [
            'BUILD_INFO.BUILD_PHASE == "G-13"',
            "build_phase_g_13",
            'BUILD_INFO.SOURCE_BRANCH == "codex/g-13-browser-build-hardening"',
            "_validate_g422r_atelier_runtime_asset_consistency",
        ],
        failures,
    )
    require_text(
        PACKAGE_SCRIPT,
        [
            "WAYFARER_EXPECTED_BUILD_PHASE",
            "WAYFARER_EXPECTED_SOURCE_BRANCH",
            'Review build phase is',
            'Review build source branch is',
            'Review build label must include',
            "wayfarers-tale-godot-$version_slug.zip",
        ],
        failures,
    )

    _validate_zip(STABLE_ZIP, failures)
    _validate_zip(VERSIONED_ZIP, failures)

    ledger = load_json(LEDGER_JSON, failures)
    if isinstance(ledger, dict):
        phases = phase_map(ledger, failures)
        g12_status = str(phases.get("G-12", {}).get("current_status", ""))
        if g12_status != "PASS":
            failures.append(f"G-13 prerequisite not complete: G-12 is {g12_status or 'missing'}")
        g13 = phases.get("G-13", {})
        if str(g13.get("current_status", "")) == "PASS":
            for key in ["screenshot_paths", "validation_commands", "validation_results", "agent_council_report_path"]:
                if not g13.get(key):
                    failures.append(f"G-13 ledger missing {key}")
            if g13.get("agent_council_verdict") != "COUNCIL_PASS_READY_FOR_PR":
                failures.append("G-13 council verdict must be COUNCIL_PASS_READY_FOR_PR")
            require_text(
                G13_REPORT,
                [
                    "G-13 Browser Build, Performance, and Regression Hardening",
                    "Review Build Identity",
                    "Browser-Review ZIP",
                    "COUNCIL_PASS_READY_FOR_PR",
                ],
                failures,
            )
            require_text(
                G13_COUNCIL_REPORT,
                [
                    "G-13 Browser Build",
                    "COUNCIL_PASS_READY_FOR_PR",
                    "Build/Release Engineer",
                    "browser build",
                ],
                failures,
            )

    return print_result("browser build hardening", failures)


if __name__ == "__main__":
    sys.exit(main())
