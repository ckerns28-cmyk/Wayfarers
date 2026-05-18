#!/usr/bin/env python3
"""Validate the SV-0 free tool acquisition manifest."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[1]
REPO_ROOT = PROJECT_ROOT.parent

MANIFEST_MD = REPO_ROOT / "docs" / "reports" / "SV0_TOOL_ACQUISITION_MANIFEST.md"
MANIFEST_JSON = REPO_ROOT / "docs" / "reports" / "SV0_TOOL_ACQUISITION_MANIFEST.json"
AGENTS_MD = REPO_ROOT / "AGENTS.md"
TOOLING_STACK_MD = REPO_ROOT / "docs" / "roadmaps" / "STARTER_VILLAGE_TOOLING_STACK.md"
PROTOCOL_MD = REPO_ROOT / "docs" / "PRE_G5_AUTONOMOUS_PRODUCTION_PROTOCOL.md"
PR_CHECKLIST_MD = REPO_ROOT / "docs" / "checklists" / "WAYFARER_PR_REVIEW_CHECKLIST.md"
COUNCIL_TOOL = REPO_ROOT / "tools" / "wayfarer_agent_council.py"

ALLOWED_DECISIONS = {"ADOPT_NOW", "SPIKE_ONLY", "DEFER", "REJECT", "ALREADY_COVERED"}
REQUIRED_CATEGORY_IDS = {str(index) for index in range(1, 10)}
REQUIRED_TOOL_NAMES = {
    "Tiled",
    "LDtk",
    "Wayfarer Godot-native StarterVillageWorldLayout schema",
    "Current NewportTownBlueprint runtime approach",
    "Dialogue Manager",
    "Dialogic",
    "Wayfarer data-driven quest/dialogue JSON",
    "Current custom quest/dialogue approach",
    "Godot NavigationAgent2D, NavigationRegion2D, AnimationPlayer, AnimationTree",
    "Wayfarer custom NPC route/path data",
    "LimboAI",
    "Playwright",
    "pixelmatch or pixelmatch-py",
    "SSIM / scikit-image comparison",
    "Godot screenshot wrappers and Python screenshot validators",
    "Godot frame-sequence movement proof",
    "FFmpeg",
    "GIF or video creation from screenshot frames",
    "OBS Studio",
    "Godot command-line and Python integration validators",
    "GUT for Godot 4",
    "Python/Pillow extraction and contact-sheet pipeline",
    "Pixelorama",
    "LibreSprite",
    "Krita",
    "Wayfarer ground material taxonomy and atelier ground sheets",
    "Material Maker",
    "Godot TileSet / TileMapLayer",
    "Godot-native Camera2D and authored viewpoints",
    "Godot-native camera smoothing/framing",
    "Phantom Camera",
}
REQUIRED_TOOL_FIELDS = [
    "tool_name",
    "category_id",
    "category_name",
    "decision",
    "version",
    "source_url_or_description",
    "license",
    "free_status",
    "installation_path",
    "files_added_to_repo",
    "files_added_outside_repo",
    "why_needed",
    "validation_method",
    "rollback_steps",
    "affects_godot_export",
    "affects_web_review_route",
    "requires_google_or_browser_credentials",
    "credentials_or_secrets_stored",
    "requires_payment",
    "downloaded_or_installed_this_run",
    "installed_outside_approved_folders",
    "used_by_later_validators",
]


def rel(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def read_json(path: Path, failures: list[str]) -> dict[str, Any] | None:
    if not path.exists():
        failures.append(f"missing json: {rel(path)}")
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        failures.append(f"invalid json {rel(path)}: {exc}")
        return None
    if not isinstance(data, dict):
        failures.append(f"{rel(path)} root must be an object")
        return None
    return data


def require_path(path: Path, failures: list[str], label: str) -> None:
    if not path.exists():
        failures.append(f"missing {label}: {rel(path)}")


def require_text(path: Path, tokens: list[str], failures: list[str]) -> None:
    if not path.exists():
        failures.append(f"missing text file: {rel(path)}")
        return
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        if token not in text:
            failures.append(f"{rel(path)} missing token: {token}")


def is_empty(value: Any) -> bool:
    return value is None or value == "" or value == {}


def validate_policy(data: dict[str, Any], failures: list[str]) -> None:
    if data.get("schema_id") != "wayfarer.sv0.tool_acquisition_manifest.v1":
        failures.append("tool acquisition manifest schema_id mismatch")
    if data.get("phase_id") != "SV-0":
        failures.append("tool acquisition manifest phase_id must be SV-0")
    policy = data.get("policy")
    if not isinstance(policy, dict):
        failures.append("policy must be an object")
        return
    for key in [
        "free_only",
        "no_payment",
        "no_paid_trials",
        "no_marketplace_purchases",
        "no_credentials_or_secrets_stored",
    ]:
        if policy.get(key) is not True:
            failures.append(f"policy.{key} must be true")
    if policy.get("google_or_browser_credentials_used_this_run") is not False:
        failures.append("Google/browser credentials must not be used by this addendum pass")
    if policy.get("downloads_or_installations_performed_this_run") is not False:
        failures.append("manifest says downloads/installations happened; add per-tool outside-file proof before passing")


def validate_categories(data: dict[str, Any], failures: list[str]) -> None:
    categories = data.get("required_categories")
    if not isinstance(categories, list):
        failures.append("required_categories must be a list")
        return
    seen: set[str] = set()
    for index, category in enumerate(categories):
        if not isinstance(category, dict):
            failures.append(f"required_categories[{index}] must be an object")
            continue
        category_id = str(category.get("category_id", ""))
        seen.add(category_id)
        if category.get("decision") not in ALLOWED_DECISIONS:
            failures.append(f"category {category_id} has invalid decision: {category.get('decision')}")
        for field in ["category_name", "locked_choice"]:
            if is_empty(category.get(field)):
                failures.append(f"category {category_id} missing {field}")
    missing = REQUIRED_CATEGORY_IDS - seen
    if missing:
        failures.append("missing required tool category decision(s): " + ", ".join(sorted(missing)))


def validate_tool(tool: dict[str, Any], index: int, failures: list[str]) -> None:
    path = f"tools[{index}]"
    for field in REQUIRED_TOOL_FIELDS:
        if field in {"files_added_to_repo", "files_added_outside_repo"}:
            if field not in tool or not isinstance(tool[field], list):
                failures.append(f"{path}.{field} must be a list")
            continue
        if is_empty(tool.get(field)):
            failures.append(f"{path}.{field} is required")
    decision = str(tool.get("decision", ""))
    if decision not in ALLOWED_DECISIONS:
        failures.append(f"{path}.decision invalid: {decision}")
    if str(tool.get("category_id", "")) not in REQUIRED_CATEGORY_IDS:
        failures.append(f"{path}.category_id must be 1-9")
    if tool.get("requires_payment") is not False:
        failures.append(f"{path} requires payment or lacks explicit no-payment proof")
    if tool.get("credentials_or_secrets_stored") is not False:
        failures.append(f"{path} stores credentials/secrets")
    if tool.get("installed_outside_approved_folders") is True and not str(tool.get("outside_install_justification", "")).strip():
        failures.append(f"{path} installed outside approved folders without justification")
    if decision == "ADOPT_NOW":
        for field in ["license", "free_status", "installation_path", "rollback_steps", "source_url_or_description", "validation_method"]:
            value = str(tool.get(field, "")).strip().lower()
            if not value or value in {"unknown", "n/a", "tbd"}:
                failures.append(f"{path}.{field} must be known for adopted tools")
        if "paid" in str(tool.get("free_status", "")).lower():
            failures.append(f"{path}.free_status cannot imply paid access for adopted tools")
    if decision not in {"ADOPT_NOW", "ALREADY_COVERED"} and tool.get("used_by_later_validators") is not False:
        failures.append(f"{path} is {decision} but marked required by later validators")


def validate_tools(data: dict[str, Any], failures: list[str]) -> None:
    tools = data.get("tools")
    if not isinstance(tools, list):
        failures.append("tools must be a list")
        return
    seen_names: set[str] = set()
    category_decisions: dict[str, set[str]] = {category_id: set() for category_id in REQUIRED_CATEGORY_IDS}
    for index, tool in enumerate(tools):
        if not isinstance(tool, dict):
            failures.append(f"tools[{index}] must be an object")
            continue
        seen_names.add(str(tool.get("tool_name", "")))
        category_id = str(tool.get("category_id", ""))
        if category_id in category_decisions:
            category_decisions[category_id].add(str(tool.get("decision", "")))
        validate_tool(tool, index, failures)
    missing_tools = REQUIRED_TOOL_NAMES - seen_names
    if missing_tools:
        failures.append("missing evaluated tool(s): " + ", ".join(sorted(missing_tools)))
    for category_id in REQUIRED_CATEGORY_IDS:
        if "ADOPT_NOW" not in category_decisions.get(category_id, set()):
            failures.append(f"category {category_id} must have at least one ADOPT_NOW tool")


def main() -> int:
    failures: list[str] = []
    for path, label in [
        (MANIFEST_MD, "SV-0 tool acquisition markdown manifest"),
        (MANIFEST_JSON, "SV-0 tool acquisition json manifest"),
        (AGENTS_MD, "AGENTS.md"),
        (TOOLING_STACK_MD, "Starter Village tooling stack"),
        (PROTOCOL_MD, "autonomous production protocol"),
        (PR_CHECKLIST_MD, "PR review checklist"),
        (COUNCIL_TOOL, "Agent Council tool"),
    ]:
        require_path(path, failures, label)
    require_text(MANIFEST_MD, ["No paid tools", "No Google/browser credentials", "Deferred Or Spike-Only Tools"], failures)
    require_text(AGENTS_MD, ["SV-0 Tool Acquisition Manifest", "free, license-safe, reversible tools"], failures)
    require_text(TOOLING_STACK_MD, ["Tool Acquisition Manifest", "free, license-safe, reversible"], failures)
    require_text(PROTOCOL_MD, ["SV-0 Tool Acquisition Manifest", "free, license-safe, reversible tools"], failures)
    require_text(PR_CHECKLIST_MD, ["SV-0 tool acquisition manifest"], failures)
    require_text(COUNCIL_TOOL, ["validate_sv0_tool_acquisition_manifest.py", "SV-0 Tool Acquisition Manifest"], failures)

    data = read_json(MANIFEST_JSON, failures)
    if isinstance(data, dict):
        validate_policy(data, failures)
        validate_categories(data, failures)
        validate_tools(data, failures)
        if data.get("final_status") != "COUNCIL_PASS_READY_FOR_PR":
            failures.append("final_status must be COUNCIL_PASS_READY_FOR_PR")

    if failures:
        print("FAIL: SV-0 tool acquisition manifest")
        for failure in failures:
            print(" - " + failure)
        return 1
    print("PASS: SV-0 tool acquisition manifest")
    print("Categories audited: 9")
    print("Downloads/installations performed this run: false")
    print("Google/browser credentials used: false")
    print(f"Manifest: {rel(MANIFEST_JSON)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
