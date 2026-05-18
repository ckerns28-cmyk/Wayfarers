#!/usr/bin/env python3
"""Validate the playable opening quest arc."""

from __future__ import annotations

import sys

from starter_village_validator_common import PROJECT_ROOT, print_result


def main() -> int:
    failures: list[str] = []
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
    return print_result("opening quest arc", failures)


if __name__ == "__main__":
    sys.exit(main())
