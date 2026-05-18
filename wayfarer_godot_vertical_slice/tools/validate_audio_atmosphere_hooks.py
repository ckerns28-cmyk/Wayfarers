#!/usr/bin/env python3
"""Validate G-11A placeholder-free audio/atmosphere hooks."""

from __future__ import annotations

import sys
from typing import Any

from starter_village_validator_common import (
    G11A_AUDIO_HOOKS_GD,
    G11A_AUDIO_HOOKS_JSON,
    G11A_COUNCIL_REPORT,
    G11A_REPORT,
    LEDGER_JSON,
    MAIN_GD,
    load_json,
    phase_map,
    print_result,
    require_text,
)


REQUIRED_HOOK_IDS = [
    "harbor_ambience_hook",
    "tavern_ambience_hook",
    "footstep_event_hook",
    "quest_update_sound_hook",
    "ui_feedback_sound_hook",
]


def _validate_registry(data: dict[str, Any], failures: list[str]) -> None:
    if data.get("schema_id") != "wayfarer.starter_village.audio_atmosphere_hooks.v1":
        failures.append("G-11A audio hook registry schema mismatch")
    if data.get("phase") != "G-11A":
        failures.append("G-11A audio hook registry phase mismatch")
    for key in ["no_audio_assets_loaded", "no_broken_audio_references", "no_licensing_unsafe_audio", "web_export_safe"]:
        if data.get(key) is not True:
            failures.append(f"G-11A audio registry must set {key}=true")
    hooks = data.get("hooks")
    if not isinstance(hooks, list) or len(hooks) < len(REQUIRED_HOOK_IDS):
        failures.append("G-11A audio registry must include all required hook rows")
        return
    by_id: dict[str, dict[str, Any]] = {}
    for hook in hooks:
        if not isinstance(hook, dict):
            failures.append("G-11A hook row must be an object")
            continue
        hook_id = str(hook.get("id", ""))
        by_id[hook_id] = hook
        if str(hook.get("asset_reference", "")):
            failures.append(f"G-11A hook {hook_id} must not reference placeholder or unlicensed audio assets")
        if str(hook.get("license_status", "")) != "none_needed_hook_only":
            failures.append(f"G-11A hook {hook_id} license_status must be none_needed_hook_only")
        for required_key in ["hook_type", "district", "event", "future_bus", "purpose"]:
            if not str(hook.get(required_key, "")).strip():
                failures.append(f"G-11A hook {hook_id} missing {required_key}")
    for hook_id in REQUIRED_HOOK_IDS:
        if hook_id not in by_id:
            failures.append(f"G-11A missing required hook: {hook_id}")


def main() -> int:
    failures: list[str] = []
    registry = load_json(G11A_AUDIO_HOOKS_JSON, failures)
    if isinstance(registry, dict):
        _validate_registry(registry, failures)
    hooks_source = require_text(
        G11A_AUDIO_HOOKS_GD,
        [
            "G11A_AUDIO_ATMOSPHERE_PASS",
            "HOOK_REGISTRY_PATH",
            "audio_hook_contract",
            "trigger_hook",
            "runtime_playback_enabled",
            "hook_only_no_license_safe_audio_asset_loaded",
        ]
        + REQUIRED_HOOK_IDS,
        failures,
    )
    main_source = require_text(
        MAIN_GD,
        [
            "STARTER_VILLAGE_AUDIO_HOOKS",
            "starter_village_audio_hook_contract",
            "debug_apply_starter_village_audio_hooks",
            "_record_starter_village_audio_hook",
            "harbor_ambience_hook",
            "tavern_ambience_hook",
            "quest_update_sound_hook",
            "ui_feedback_sound_hook",
        ],
        failures,
    )
    for forbidden in [
        "AudioStreamPlayer",
        "AudioStreamWAV",
        "AudioStreamOggVorbis",
        "load(\"res://",
        "preload(\"res://audio",
        ".ogg",
        ".wav",
        ".mp3",
    ]:
        if forbidden in hooks_source:
            failures.append(f"G-11A audio hook script must not load placeholder audio: {forbidden}")
    if "AudioStreamPlayer" in main_source:
        failures.append("G-11A Main must not instantiate AudioStreamPlayer without license-safe assets")

    ledger = load_json(LEDGER_JSON, failures)
    if isinstance(ledger, dict):
        phases = phase_map(ledger, failures)
        if phases.get("G-11A", {}).get("current_status") == "PASS":
            require_text(
                G11A_REPORT,
                [
                    "G-11A Audio/Atmosphere Placeholder-Free Foundation",
                    "harbor_ambience_hook",
                    "tavern_ambience_hook",
                    "footstep_event_hook",
                    "quest_update_sound_hook",
                    "ui_feedback_sound_hook",
                    "No placeholder audio assets were added",
                    "no broken audio references",
                ],
                failures,
            )
            require_text(
                G11A_COUNCIL_REPORT,
                [
                    "COUNCIL_PASS_READY_FOR_PR",
                    "Build/Release Engineer",
                    "G-11A Audio/Atmosphere Result",
                    "placeholder-free",
                    "no broken audio references",
                ],
                failures,
            )
    return print_result("audio atmosphere hooks", failures)


if __name__ == "__main__":
    sys.exit(main())
