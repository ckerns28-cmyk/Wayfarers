#!/usr/bin/env python3
"""Validate the playable opening quest arc."""

from __future__ import annotations

import sys

from starter_village_validator_common import (
    FIRST_LIGHT_QUEST_GD,
    FIRST_LIGHT_QUEST_JSON,
    HUD_GD,
    LEDGER_JSON,
    MAIN_GD,
    PROJECT_ROOT,
    QUEST_STATE_GD,
    load_json,
    phase_map,
    print_result,
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
            "missing ledger line",
            "Third Toast",
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
            "interaction_triggered",
        ],
        failures,
    )
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
    return print_result("opening quest arc", failures)


if __name__ == "__main__":
    sys.exit(main())
