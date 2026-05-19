#!/usr/bin/env python3
"""Validate G-21 browser build identity and package hardening gates."""

from __future__ import annotations

import re
import sys
import json
import zipfile
from pathlib import Path

from opening_village_island_validator_common import (
    LEDGER_JSON,
    PROJECT_ROOT,
    REPO_ROOT,
    load_json,
    phase_map,
    print_result,
    require_text,
)


PHASE = "G-21"
BRANCH = "codex/g-21-opening-island-performance-browser-build-regression-hardening"
LABEL = "Godot G-21 Opening Island Performance, Browser Build, and Regression Hardening"

BUILD_INFO = PROJECT_ROOT / "scripts" / "BuildInfo.gd"
VERTICAL_SLICE_VALIDATOR = PROJECT_ROOT / "tools" / "validate_vertical_slice.gd"
PACKAGE_SCRIPT = PROJECT_ROOT / "tools" / "package_itch_web.sh"
STABLE_ZIP = PROJECT_ROOT / "artifacts" / "wayfarers-tale-godot-web.zip"
VERSIONED_ZIP = PROJECT_ROOT / "artifacts" / "wayfarers-tale-godot-g-21-opening-island-performance-browser-build-and-regression-hardening.zip"
G21_REPORT = REPO_ROOT / "docs" / "reports" / "G21_OPENING_ISLAND_BROWSER_BUILD_REGRESSION_HARDENING.md"
G21_COUNCIL_REPORT = REPO_ROOT / "docs" / "reports" / "G21_OPENING_ISLAND_BROWSER_BUILD_AGENT_COUNCIL_REPORT.md"
G21_REVIEW_DIR = PROJECT_ROOT / "artifacts" / "review" / "g21_browser_build_hardening"
G21_MANIFEST = G21_REVIEW_DIR / "g21_browser_build_hardening_manifest.json"
G21_BROWSER_LOADER_SCREENSHOT = G21_REVIEW_DIR / "g21_browser_review_identity_proof.jpg"
G21_BROWSER_LOADED_SCREENSHOT = G21_REVIEW_DIR / "g21_browser_review_loaded_surface.jpg"
G21_BROWSER_CONSOLE_LOG = G21_REVIEW_DIR / "g21_browser_review_loaded_console_log.json"


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


def _validate_manifest(failures: list[str]) -> None:
    if not G21_MANIFEST.exists():
        failures.append(f"missing G-21 browser proof manifest: {G21_MANIFEST.relative_to(REPO_ROOT).as_posix()}")
        return
    try:
        manifest = json.loads(G21_MANIFEST.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        failures.append(f"invalid G-21 browser proof manifest: {exc}")
        return
    if manifest.get("phase_id") != PHASE:
        failures.append("G-21 browser proof manifest phase_id mismatch")
    if manifest.get("branch") != BRANCH:
        failures.append("G-21 browser proof manifest branch mismatch")
    build_identity = manifest.get("build_identity", {})
    if not isinstance(build_identity, dict):
        failures.append("G-21 browser proof manifest build_identity must be an object")
    else:
        for key, value in {"BUILD_PHASE": PHASE, "BUILD_LABEL": LABEL, "SOURCE_BRANCH": BRANCH}.items():
            if build_identity.get(key) != value:
                failures.append(f"G-21 browser proof manifest build_identity {key} mismatch")

    zip_artifacts = manifest.get("zip_artifacts", {})
    if not isinstance(zip_artifacts, dict):
        failures.append("G-21 browser proof manifest zip_artifacts must be an object")
    else:
        for key in ["stable", "versioned"]:
            zip_info = zip_artifacts.get(key, {})
            if not isinstance(zip_info, dict):
                failures.append(f"G-21 browser proof manifest {key} zip info must be an object")
                continue
            if zip_info.get("index_html_at_zip_root") is not True:
                failures.append(f"G-21 browser proof manifest {key} ZIP must record root index.html")
            if zip_info.get("contains_web_build_index_html") is not False:
                failures.append(f"G-21 browser proof manifest {key} ZIP must record no web_build/index.html nesting")
            if int(zip_info.get("size_bytes", 0)) <= 0:
                failures.append(f"G-21 browser proof manifest {key} ZIP missing positive size_bytes")
            entries = zip_info.get("entries", [])
            for required in ["index.html", "index.js", "index.pck", "index.wasm"]:
                if required not in entries:
                    failures.append(f"G-21 browser proof manifest {key} ZIP entries missing {required}")

    browser_proof = manifest.get("browser_proof", {})
    if not isinstance(browser_proof, dict):
        failures.append("G-21 browser proof manifest browser_proof must be an object")
    else:
        if browser_proof.get("local_url") != "http://127.0.0.1:8766/index.html":
            failures.append("G-21 browser proof manifest local_url mismatch")
        if browser_proof.get("console_warning_error_count") != 0:
            failures.append("G-21 browser proof manifest must record zero warning/error console entries")
        page_info = browser_proof.get("page_info", {})
        if not isinstance(page_info, dict):
            failures.append("G-21 browser proof manifest page_info must be an object")
        else:
            if page_info.get("title") != "Wayfarer Godot Vertical Slice":
                failures.append("G-21 browser proof manifest page title mismatch")
            if int(page_info.get("canvas_count", 0)) < 1:
                failures.append("G-21 browser proof manifest must record at least one canvas")

    for path in [G21_BROWSER_LOADER_SCREENSHOT, G21_BROWSER_LOADED_SCREENSHOT, G21_BROWSER_CONSOLE_LOG]:
        if not path.exists():
            failures.append(f"missing G-21 browser proof artifact: {path.relative_to(REPO_ROOT).as_posix()}")
    if G21_BROWSER_CONSOLE_LOG.exists():
        try:
            console_log = json.loads(G21_BROWSER_CONSOLE_LOG.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"invalid G-21 browser console log: {exc}")
        else:
            if console_log != []:
                failures.append("G-21 browser warning/error console log must be empty")


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
        for token in ["G-21", "G-19R", "G-20", "browser review build", "OVI-1"]:
            if token not in note:
                failures.append(f"BuildInfo.gd PLAYER_STYLE_ROADMAP_NOTE missing {token}")

    require_text(
        VERTICAL_SLICE_VALIDATOR,
        [
            'BUILD_INFO.BUILD_PHASE == "G-21"',
            "build_phase_g_21",
            'BUILD_INFO.SOURCE_BRANCH == "codex/g-21-opening-island-performance-browser-build-regression-hardening"',
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
    _validate_manifest(failures)

    ledger = load_json(LEDGER_JSON, failures)
    if isinstance(ledger, dict):
        phases = phase_map(ledger, failures)
        g20_status = str(phases.get("G-20", {}).get("current_status", ""))
        if g20_status != "PASS":
            failures.append(f"G-21 prerequisite not complete: G-20 is {g20_status or 'missing'}")
        g21 = phases.get("G-21", {})
        if str(g21.get("current_status", "")) == "PASS":
            for key in ["screenshot_paths", "validation_commands", "validation_results", "agent_council_report_path"]:
                if not g21.get(key):
                    failures.append(f"G-21 ledger missing {key}")
            if g21.get("agent_council_verdict") != "COUNCIL_PASS_READY_FOR_PR":
                failures.append("G-21 council verdict must be COUNCIL_PASS_READY_FOR_PR")
            require_text(
                G21_REPORT,
                [
                    "G-21 Opening Island Performance, Browser Build, and Regression Hardening",
                    "Review Build Identity",
                    "Browser-Review ZIP",
                    "COUNCIL_PASS_READY_FOR_PR",
                ],
                failures,
            )
            require_text(
                G21_COUNCIL_REPORT,
                [
                    "G-21 Browser Build",
                    "COUNCIL_PASS_READY_FOR_PR",
                    "Build/Release Engineer",
                    "browser build",
                ],
                failures,
            )

    return print_result("browser build hardening", failures)


if __name__ == "__main__":
    sys.exit(main())
