#!/usr/bin/env python3
"""Validate Tavern/Inn whisper-system readiness."""

from __future__ import annotations

import sys

from starter_village_validator_common import PROJECT_ROOT, print_result


def main() -> int:
    failures: list[str] = []
    paths = [
        PROJECT_ROOT / "scripts" / "dialogue" / "TavernWhisperSystem.gd",
        PROJECT_ROOT / "data" / "dialogue" / "tavern_whispers.json",
    ]
    existing = [path for path in paths if path.exists()]
    if not existing:
        failures.append("G-10A not complete: tavern whisper system/data is missing")
    else:
        text = "\n".join(path.read_text(encoding="utf-8") for path in existing)
        for token in ["harbor", "ledger", "toast", "whisper", "rumor"]:
            if token not in text.lower():
                failures.append(f"G-10A not complete: tavern whisper content missing {token}")
    return print_result("tavern whisper system", failures)


if __name__ == "__main__":
    sys.exit(main())
