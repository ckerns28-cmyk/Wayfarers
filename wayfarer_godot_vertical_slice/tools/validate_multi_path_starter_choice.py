#!/usr/bin/env python3
"""Validate G-10B multi-path starter-choice foundation."""

from __future__ import annotations

import sys

from starter_village_validator_common import (
    BLUEPRINT,
    FIRST_LIGHT_CHOICE_ROUTER_GD,
    FIRST_LIGHT_MULTI_PATH_JSON,
    FIRST_LIGHT_QUEST_GD,
    FIRST_LIGHT_QUEST_JSON,
    G10B_COUNCIL_REPORT,
    G10B_REPORT,
    G10B_SCREENSHOT_MANIFEST,
    LEDGER_JSON,
    MAIN_GD,
    load_json,
    phase_map,
    print_result,
    repo_path,
    require_text,
)


REQUIRED_PATHS = {
    "counting_house_clerk_path",
    "harbor_work_path",
    "tavern_rumor_path",
    "merchant_street_path",
    "optional_secret_path",
}


def main() -> int:
    failures: list[str] = []
    ledger = load_json(LEDGER_JSON, failures)
    router_source = require_text(
        FIRST_LIGHT_CHOICE_ROUTER_GD,
        [
            "class_name FirstLightChoiceRouter",
            "G10B_MULTI_PATH_STARTER_CHOICE_PASS",
            "choice_for_payload",
            "choice_contract",
            "debug_branch_matrix",
        ],
        failures,
    )
    data = load_json(FIRST_LIGHT_MULTI_PATH_JSON, failures)
    require_text(
        FIRST_LIGHT_QUEST_GD,
        [
            "CHOICE_ROUTER",
            "multi_path_choice_contract",
            "debug_multi_path_branch_contract",
            "merchant_first",
            "secret_first",
            "harbor_first",
        ],
        failures,
    )
    require_text(
        MAIN_GD,
        ["starter_village_multi_path_choice_contract", "multi_path_choice_contract"],
        failures,
    )
    require_text(
        BLUEPRINT,
        [
            "STARTER_VILLAGE_G10B_MULTI_PATH_CHOICE_PASS",
            "g10b_multi_path_starter_choice_contract",
            "harbor_work_path",
            "optional_secret_path",
            "not_single_railroad",
        ],
        failures,
    )
    require_text(
        FIRST_LIGHT_QUEST_JSON,
        ["G-10B", "multi_path_choice_foundation", "not_single_railroad", "optional_clue_paths"],
        failures,
    )

    if isinstance(data, dict):
        if data.get("phase") != "G-10B":
            failures.append("G-10B multi-path data phase must be G-10B")
        paths = data.get("paths")
        matrix = data.get("branch_matrix")
        policy = data.get("choice_policy")
        if not isinstance(paths, list) or len(paths) < 5:
            failures.append("G-10B requires at least five approach paths")
        else:
            path_ids = {str(path.get("id", "")) for path in paths if isinstance(path, dict)}
            missing = sorted(REQUIRED_PATHS - path_ids)
            if missing:
                failures.append("G-10B missing required path ids: " + ", ".join(missing))
            advancement_npcs: set[str] = set()
            optional_clues: set[str] = set()
            objective_advancers: dict[str, set[str]] = {}
            for path in paths:
                if not isinstance(path, dict):
                    failures.append("G-10B path row must be an object")
                    continue
                path_id = str(path.get("id", ""))
                for npc in path.get("advancement_npcs", []):
                    advancement_npcs.add(str(npc))
                for clue in path.get("optional_clues", []):
                    optional_clues.add(str(clue))
                for objective in path.get("advances_objectives", []):
                    objective_advancers.setdefault(str(objective), set()).add(path_id)
            if len(advancement_npcs) < 6:
                failures.append("G-10B requires at least six named/role advancement NPCs")
            if len(objective_advancers.get("investigate_missing_line", set())) < 2:
                failures.append("G-10B requires multiple NPC/path sources for investigate_missing_line")
            if len(objective_advancers.get("choose_next_lead", set())) < 2:
                failures.append("G-10B requires multiple NPC/path sources for choose_next_lead")
            if not {"folded_notice", "rear_service_gate_hint"}.issubset(optional_clues):
                failures.append("G-10B optional clues must include folded_notice and rear_service_gate_hint")
        if not isinstance(matrix, list) or len(matrix) < 3:
            failures.append("G-10B branch_matrix must prove at least three approach sequences")
        if not isinstance(policy, dict) or policy.get("not_single_railroad") is not True:
            failures.append("G-10B choice policy must declare not_single_railroad=true")
        text = "\n".join([router_source, str(data)])
        for token in ["harbor", "tavern", "counting", "merchant", "optional", "secret", "future"]:
            if token not in text.lower():
                failures.append(f"G-10B content missing {token}")

    if isinstance(ledger, dict):
        phases = phase_map(ledger, failures)
        if phases.get("G-10B", {}).get("current_status") == "PASS":
            row = phases.get("G-10B", {})
            if row.get("agent_council_verdict") != "COUNCIL_PASS_READY_FOR_PR":
                failures.append("G-10B council verdict must be COUNCIL_PASS_READY_FOR_PR")
            for key in ["screenshot_paths", "validation_commands", "validation_results"]:
                if not row.get(key):
                    failures.append(f"G-10B ledger missing {key}")
            require_text(
                G10B_REPORT,
                ["G-10B Multi-Path Starter Choice Foundation", "harbor_work_path", "merchant_street_path", "optional_secret_path"],
                failures,
            )
            if G10B_COUNCIL_REPORT.exists():
                require_text(
                    G10B_COUNCIL_REPORT,
                    ["COUNCIL_PASS_READY_FOR_PR", "G-10B Multi-Path Starter Choice Result", "runtime screenshots"],
                    failures,
                )
            manifest = load_json(G10B_SCREENSHOT_MANIFEST, failures)
            if isinstance(manifest, dict):
                if manifest.get("status") != "PASS":
                    failures.append("G-10B screenshot manifest must be PASS")
                if manifest.get("phase") != "G-10B":
                    failures.append("G-10B screenshot manifest phase mismatch")
                choice_contract = manifest.get("multi_path_choice_contract", {})
                if not isinstance(choice_contract, dict) or choice_contract.get("phase") != "G-10B":
                    failures.append("G-10B manifest missing multi-path choice contract")
                elif choice_contract.get("path_count", 0) < 5:
                    failures.append("G-10B manifest must prove at least five paths")
                screenshots = manifest.get("screenshots")
                if not isinstance(screenshots, list) or len(screenshots) < 15:
                    failures.append("G-10B screenshot manifest must include 15 proof views")
                else:
                    for shot in screenshots:
                        if isinstance(shot, dict):
                            raw_path = str(shot.get("path", ""))
                            if raw_path and not repo_path(raw_path).exists():
                                failures.append(f"G-10B screenshot path missing: {raw_path}")
    return print_result("multi-path starter choice", failures)


if __name__ == "__main__":
    sys.exit(main())
