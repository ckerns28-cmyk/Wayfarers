#!/usr/bin/env python3
"""Validate the playable opening quest arc."""

from __future__ import annotations

import sys

from starter_village_validator_common import (
    FIRST_LIGHT_QUEST_GD,
    FIRST_LIGHT_QUEST_JSON,
    G10_COUNCIL_REPORT,
    G10_REPORT,
    G10_SCREENSHOT_MANIFEST,
    HUD_GD,
    LEDGER_JSON,
    MAIN_GD,
    PROJECT_ROOT,
    QUEST_STATE_GD,
    load_json,
    phase_map,
    print_result,
    repo_path,
    require_text,
)


def main() -> int:
    failures: list[str] = []
    ledger = load_json(LEDGER_JSON, failures)
    require_text(
        QUEST_STATE_GD,
        [
            "class_name WayfarerQuestState",
            "start_objective",
            "complete_objective",
            "add_reward",
            "session_persistence",
        ],
        failures,
    )
    require_text(
        FIRST_LIGHT_QUEST_GD,
        [
            "class_name FirstLightQuest",
            "handle_interaction",
            "handle_interaction_payload",
            "debug_playthrough_contract",
            "G10_OPENING_QUEST_ARC_PASS",
            "missing ledger line",
            "Third Toast",
            "lantern_at_wharf",
            "secure_contact",
            "hook_to_continue",
            "branch_choices",
            "optional_discovery",
            "Reward",
        ],
        failures,
    )
    require_text(
        FIRST_LIGHT_QUEST_JSON,
        [
            "first_light_whispers_before_dawn",
            "missing ledger line",
            "tavern",
            "rumor",
            "reward",
            "opening_arc",
            "playable_minutes_estimate",
            "branch_choices",
            "optional_discovery",
            "hook_to_continue",
            "multiple_advancement_sources",
        ],
        failures,
    )
    require_text(
        HUD_GD,
        [
            "apply_quest_snapshot",
            "journal_objective_contract",
            "Journal - First Light",
            "Objective updated",
            "Reward",
        ],
        failures,
    )
    require_text(
        MAIN_GD,
        [
            "FIRST_LIGHT_QUEST",
            "starter_village_quest_contract",
            "debug_apply_first_light_quest_events",
            "opening_arc_phase",
            "interaction_triggered",
        ],
        failures,
    )
    quest_data = load_json(FIRST_LIGHT_QUEST_JSON, failures)
    if isinstance(quest_data, dict):
        objectives = quest_data.get("objectives", [])
        if quest_data.get("phase") != "G-10":
            failures.append("G-10 quest data phase must be G-10")
        if not isinstance(objectives, list) or len(objectives) < 8:
            failures.append("G-10 quest data must include at least eight objective beats")
        opening_arc = quest_data.get("opening_arc")
        if not isinstance(opening_arc, dict):
            failures.append("G-10 quest data missing opening_arc contract")
        else:
            if int(opening_arc.get("playable_minutes_estimate", 0)) < 10:
                failures.append("G-10 opening_arc must estimate at least 10 meaningful minutes")
            if len(opening_arc.get("named_or_role_npcs", [])) < 3:
                failures.append("G-10 opening_arc must include at least three named/role NPCs")
            if len(opening_arc.get("branch_choices", [])) < 2:
                failures.append("G-10 opening_arc must include at least two branch choices")
            if not str(opening_arc.get("optional_discovery", "")).strip():
                failures.append("G-10 opening_arc missing optional discovery")
            if not str(opening_arc.get("hook_to_continue", "")).strip():
                failures.append("G-10 opening_arc missing reason-to-continue hook")
    candidate_paths = [
        PROJECT_ROOT / "scripts" / "quests" / "FirstLightQuest.gd",
        PROJECT_ROOT / "scripts" / "QuestState.gd",
        PROJECT_ROOT / "data" / "quests" / "first_light_whispers_before_dawn.json",
    ]
    existing = [path for path in candidate_paths if path.exists()]
    if len(existing) < 2:
        failures.append("G-10 not complete: opening quest state/data files are not implemented")
    if existing:
        text = "\n".join(path.read_text(encoding="utf-8") for path in existing if path.is_file())
        for token in ["missing line", "tavern", "rumor", "counting", "reward"]:
            if token.lower() not in text.lower():
                failures.append(f"G-10 not complete: quest data missing concept {token}")
    if isinstance(ledger, dict):
        phases = phase_map(ledger, failures)
        if phases.get("G-9A", {}).get("current_status") == "PASS":
            row = phases.get("G-9A", {})
            if row.get("agent_council_verdict") != "COUNCIL_PASS_READY_FOR_PR":
                failures.append("G-9A council verdict must be COUNCIL_PASS_READY_FOR_PR")
            for key in ["screenshot_paths", "validation_commands", "validation_results"]:
                if not row.get(key):
                    failures.append(f"G-9A ledger missing {key}")
        if phases.get("G-10", {}).get("current_status") == "PASS":
            row = phases.get("G-10", {})
            if row.get("agent_council_verdict") != "COUNCIL_PASS_READY_FOR_PR":
                failures.append("G-10 council verdict must be COUNCIL_PASS_READY_FOR_PR")
            for key in ["screenshot_paths", "validation_commands", "validation_results"]:
                if not row.get(key):
                    failures.append(f"G-10 ledger missing {key}")
            require_text(
                G10_REPORT,
                [
                    "G-10 Opening Quest Arc",
                    "First Light / Whispers Before Dawn",
                    "lantern signal",
                    "Edrin Vale",
                    "reason to continue",
                ],
                failures,
            )
            if G10_COUNCIL_REPORT.exists():
                require_text(
                    G10_COUNCIL_REPORT,
                    [
                        "COUNCIL_PASS_READY_FOR_PR",
                        "Narrative Designer",
                        "G-10 Opening Quest Arc Result",
                        "runtime screenshots",
                    ],
                    failures,
                )
            manifest = load_json(G10_SCREENSHOT_MANIFEST, failures)
            if isinstance(manifest, dict):
                screenshots = manifest.get("screenshots")
                if manifest.get("status") != "PASS":
                    failures.append("G-10 screenshot manifest must be PASS")
                if manifest.get("phase") != "G-10":
                    failures.append("G-10 screenshot manifest phase mismatch")
                final_contract = manifest.get("quest_contract_final", {})
                if not isinstance(final_contract, dict):
                    failures.append("G-10 manifest missing final quest contract")
                else:
                    if final_contract.get("opening_arc_phase") != "G-10":
                        failures.append("G-10 manifest final contract must expose opening_arc_phase")
                    if final_contract.get("current_objective_id") != "hook_to_continue":
                        failures.append("G-10 manifest final objective must hook the player to continue")
                    reward_log = final_contract.get("reward_log", [])
                    if not isinstance(reward_log, list) or len(reward_log) < 2:
                        failures.append("G-10 manifest must prove reward and named-contact progression")
                if not isinstance(screenshots, list) or len(screenshots) < 15:
                    failures.append("G-10 screenshot manifest must include 15 proof views")
                else:
                    for shot in screenshots:
                        if isinstance(shot, dict):
                            raw_path = str(shot.get("path", ""))
                            if raw_path and not repo_path(raw_path).exists():
                                failures.append(f"G-10 screenshot path missing: {raw_path}")
    return print_result("opening quest arc", failures)


if __name__ == "__main__":
    sys.exit(main())
