#!/usr/bin/env python3
"""Validate Tavern/Inn whisper-system readiness."""

from __future__ import annotations

import sys

from starter_village_validator_common import (
    BLUEPRINT,
    FIRST_LIGHT_QUEST_GD,
    G10A_COUNCIL_REPORT,
    G10A_REPORT,
    G10A_SCREENSHOT_MANIFEST,
    LEDGER_JSON,
    MAIN_GD,
    TAVERN_WHISPER_GD,
    TAVERN_WHISPER_JSON,
    load_json,
    phase_map,
    print_result,
    repo_path,
    require_text,
)


def main() -> int:
    failures: list[str] = []
    ledger = load_json(LEDGER_JSON, failures)
    system_source = require_text(
        TAVERN_WHISPER_GD,
        [
            "class_name TavernWhisperSystem",
            "G10A_TAVERN_WHISPER_SYSTEM_PASS",
            "opening_rumor_response",
            "next_ambient_bark",
            "rumor_contract",
            "debug_whisper_contract",
        ],
        failures,
    )
    data = load_json(TAVERN_WHISPER_JSON, failures)
    require_text(
        FIRST_LIGHT_QUEST_GD,
        [
            "TAVERN_WHISPER_SYSTEM",
            "tavern_whisper_contract",
            "opening_rumor_response",
            "optional_secret_response",
        ],
        failures,
    )
    require_text(MAIN_GD, ["starter_village_tavern_whisper_contract", "tavern_whisper_contract"], failures)
    require_text(
        BLUEPRINT,
        [
            "STARTER_VILLAGE_G10A_TAVERN_WHISPER_SYSTEM_PASS",
            "g10a_tavern_whisper_system_contract",
            "Third Toast",
            "rotating ambient barks",
        ],
        failures,
    )
    if isinstance(data, dict):
        if data.get("phase") != "G-10A":
            failures.append("G-10A tavern whisper data phase must be G-10A")
        interactions = data.get("quest_relevant_interactions")
        barks = data.get("ambient_barks")
        hub = data.get("hub_contract")
        if not isinstance(interactions, list) or len(interactions) < 4:
            failures.append("G-10A requires at least four quest-relevant tavern/rumor interactions")
        if not isinstance(barks, list) or len(barks) < 5:
            failures.append("G-10A requires at least five ambient rumor barks")
        if not isinstance(hub, dict):
            failures.append("G-10A data missing hub_contract")
        else:
            for key in [
                "has_tavern_npcs",
                "has_rumor_dialogue",
                "has_quest_relevant_interaction",
                "has_rotating_rumor_lines",
                "ties_to_harbor_commerce",
                "ties_to_political_tension",
                "normal_play_debug_marker_free",
            ]:
                if hub.get(key) is not True:
                    failures.append(f"G-10A hub_contract must set {key}=true")
        text = "\n".join([system_source, str(data)])
        for token in ["harbor", "ledger", "toast", "whisper", "rumor", "lantern", "rear gate"]:
            if token not in text.lower():
                failures.append(f"G-10A not complete: tavern whisper content missing {token}")
    if isinstance(ledger, dict):
        phases = phase_map(ledger, failures)
        if phases.get("G-10A", {}).get("current_status") == "PASS":
            row = phases.get("G-10A", {})
            if row.get("agent_council_verdict") != "COUNCIL_PASS_READY_FOR_PR":
                failures.append("G-10A council verdict must be COUNCIL_PASS_READY_FOR_PR")
            for key in ["screenshot_paths", "validation_commands", "validation_results"]:
                if not row.get(key):
                    failures.append(f"G-10A ledger missing {key}")
            require_text(
                G10A_REPORT,
                ["G-10A Tavern Whisper System", "Third Toast", "ambient barks", "rumor gameplay hub"],
                failures,
            )
            if G10A_COUNCIL_REPORT.exists():
                require_text(
                    G10A_COUNCIL_REPORT,
                    ["COUNCIL_PASS_READY_FOR_PR", "G-10A Tavern Whisper System Result", "runtime screenshots"],
                    failures,
                )
            manifest = load_json(G10A_SCREENSHOT_MANIFEST, failures)
            if isinstance(manifest, dict):
                screenshots = manifest.get("screenshots")
                if manifest.get("status") != "PASS":
                    failures.append("G-10A screenshot manifest must be PASS")
                if manifest.get("phase") != "G-10A":
                    failures.append("G-10A screenshot manifest phase mismatch")
                tavern_contract = manifest.get("tavern_whisper_contract", {})
                if not isinstance(tavern_contract, dict) or tavern_contract.get("phase") != "G-10A":
                    failures.append("G-10A manifest missing tavern whisper contract")
                elif not tavern_contract.get("has_rotating_rumor_lines"):
                    failures.append("G-10A manifest must prove rotating rumor lines")
                if not isinstance(screenshots, list) or len(screenshots) < 15:
                    failures.append("G-10A screenshot manifest must include 15 proof views")
                else:
                    for shot in screenshots:
                        if isinstance(shot, dict):
                            raw_path = str(shot.get("path", ""))
                            if raw_path and not repo_path(raw_path).exists():
                                failures.append(f"G-10A screenshot path missing: {raw_path}")
    return print_result("tavern whisper system", failures)


if __name__ == "__main__":
    sys.exit(main())
