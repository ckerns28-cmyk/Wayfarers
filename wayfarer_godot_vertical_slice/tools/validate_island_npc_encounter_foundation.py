#!/usr/bin/env python3
"""Validate the G-17 island NPC/encounter/ambient life contract."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from opening_village_island_validator_common import PROJECT_ROOT, REPO_ROOT, load_json, print_result, require_text, repo_path, validate_phase_contract


SOURCE_JSON = PROJECT_ROOT / "data" / "world_layout" / "island_npc_encounter_foundation_v1.json"
TOPOLOGY_JSON = PROJECT_ROOT / "data" / "world_layout" / "opening_island_world_topology_v1.json"
SCREENSHOT_MANIFEST = PROJECT_ROOT / "artifacts" / "review" / "g17_runtime_screenshots" / "g17_runtime_screenshot_manifest.json"
MOTION_TRACE = PROJECT_ROOT / "artifacts" / "review" / "g17_motion_proof" / "g17_island_npc_motion_trace.json"
G17_REPORT = REPO_ROOT / "docs" / "reports" / "G17_ISLAND_NPC_ENCOUNTER_FOUNDATION.md"
G17_REPORT_JSON = REPO_ROOT / "docs" / "reports" / "G17_ISLAND_NPC_ENCOUNTER_FOUNDATION.json"
BLUEPRINT_GD = PROJECT_ROOT / "scripts" / "NewportTownBlueprint.gd"
MAIN_GD = PROJECT_ROOT / "scenes" / "Main.gd"
ATELIER_NPC_GD = PROJECT_ROOT / "scenes" / "npc" / "AtelierTownNpc.gd"
CAPTURE_GD = PROJECT_ROOT / "tools" / "capture_g17_runtime_screenshots.gd"
CAPTURE_PS1 = PROJECT_ROOT / "tools" / "capture_g17_runtime_screenshots.ps1"
CHARACTER_MANIFEST = PROJECT_ROOT / "art_pipeline" / "player_identity" / "manifests" / "newport_atelier_characters_g422r_manifest.json"

REQUIRED_NPC_IDS = [
    "isla_brooke_farmhand",
    "tomas_reed_dock_runner",
    "elias_ward_suspicious_courier",
    "mara_oren_coast_patrol",
    "annelise_crow_rumor_contact",
]

REQUIRED_ROLES = [
    "farmhand",
    "dock_runner",
    "suspicious_courier",
    "coast_patrol",
    "rumor_contact",
]

ALLOWED_ASSET_IDS = {
    "npc_dockworker_atelier_g422r",
    "npc_market_vendor_atelier_g422r",
    "npc_civic_clerk_atelier_g422r",
}

REQUIRED_SCREENSHOTS = [
    "g17_01_island_life_wide.png",
    "g17_02_farmhand_service_edge.png",
    "g17_03_dock_runner_cove_watch.png",
    "g17_04_suspicious_courier_old_road.png",
    "g17_05_signal_patrol_overlook.png",
    "g17_06_return_rumor_contact_debug_disabled.png",
]

REQUIRED_MOTION_FRAMES = [
    "g17_motion_frame_00.png",
    "g17_motion_frame_01.png",
    "g17_motion_frame_02.png",
    "g17_motion_frame_03.png",
    "g17_motion_frame_04.png",
]


def project_path(raw_path: str) -> Path:
    normalized = raw_path.replace("\\", "/")
    if normalized.startswith("res://"):
        return PROJECT_ROOT / normalized.removeprefix("res://")
    if normalized.startswith("wayfarer_godot_vertical_slice/"):
        return REPO_ROOT / normalized
    if normalized.startswith("art_pipeline/"):
        return PROJECT_ROOT / normalized
    return repo_path(normalized)


def main() -> int:
    failures: list[str] = []
    validate_phase_contract("G-17", failures)
    source = load_json(SOURCE_JSON, failures)
    topology = load_json(TOPOLOGY_JSON, failures)
    report_json = load_json(G17_REPORT_JSON, failures)
    screenshot_manifest = load_json(SCREENSHOT_MANIFEST, failures)
    motion_trace = load_json(MOTION_TRACE, failures)
    character_manifest = load_json(CHARACTER_MANIFEST, failures)
    require_text(
        G17_REPORT,
        [
            "G-17 Island NPC / Encounter / Ambient Life Foundation",
            "Human review required: no",
            "grounded, no-glide",
            "COUNCIL_PASS_READY_FOR_PR",
            "Next phase: G-18 Opening Quest Extension: From Whispers to the Island",
        ],
        failures,
    )
    require_text(
        BLUEPRINT_GD,
        [
            "G17_ISLAND_NPC_ENCOUNTER_PASS",
            "opening_island_npc_specs",
            "opening_island_ambient_rhythm_specs",
            "opening_island_npc_encounter_contract",
            "stationary_grounded_facing_bark_until_dedicated_walk_sheets",
            "isla_brooke_farmhand",
            "mara_oren_coast_patrol",
        ],
        failures,
    )
    require_text(
        MAIN_GD,
        [
            "_place_opening_island_npcs",
            "_configure_opening_island_ambient_life",
            "opening_island_npc_encounter_contract",
            "debug_apply_opening_island_ambient_tick",
            "_opening_island_ambient_drift_detected",
        ],
        failures,
    )
    require_text(
        ATELIER_NPC_GD,
        [
            "opening_island_npc",
            "opening_island_ambient_actor",
            "group_namespace",
            "atelier_standard_sprite",
            "no_static_sprite_translation",
        ],
        failures,
    )
    require_text(CAPTURE_GD, REQUIRED_SCREENSHOTS + REQUIRED_MOTION_FRAMES + ["g17_island_npc_motion_trace.json"], failures)
    require_text(CAPTURE_PS1, ["capture_g17_runtime_screenshots.gd"], failures)
    if isinstance(source, dict):
        validate_source(source, failures)
    if isinstance(topology, dict):
        implementation = topology.get("g17_npc_encounter_implementation", {})
        if not isinstance(implementation, dict) or implementation.get("status") != "PASS":
            failures.append("topology missing PASS g17_npc_encounter_implementation")
    if isinstance(report_json, dict):
        validate_report_json(report_json, failures)
    if isinstance(screenshot_manifest, dict):
        validate_screenshot_manifest(screenshot_manifest, failures)
    if isinstance(motion_trace, dict):
        validate_motion_trace(motion_trace, failures)
    if isinstance(character_manifest, dict):
        validate_character_manifest(character_manifest, failures)
    return print_result("island NPC encounter foundation", failures)


def validate_source(data: dict[str, Any], failures: list[str]) -> None:
    if data.get("schema_id") != "wayfarer.g17.island_npc_encounter_foundation.v1":
        failures.append("G-17 source schema mismatch")
    if data.get("phase") != "G-17":
        failures.append("G-17 source phase mismatch")
    if data.get("route_walking_enabled") is not False:
        failures.append("G-17 source route_walking_enabled must be false until dedicated walk sheets exist")
    if data.get("no_static_sprite_translation") is not True:
        failures.append("G-17 source must assert no_static_sprite_translation")
    if data.get("motion_proof_manifest") != "wayfarer_godot_vertical_slice/artifacts/review/g17_motion_proof/g17_island_npc_motion_trace.json":
        failures.append("G-17 source motion proof manifest mismatch")
    npc_rows = data.get("npc_encounters", [])
    if not isinstance(npc_rows, list) or len(npc_rows) < 5:
        failures.append("G-17 source must define at least five island NPC encounters")
        npc_rows = []
    seen_ids = set()
    seen_roles = set()
    for raw_npc in npc_rows:
        if not isinstance(raw_npc, dict):
            failures.append("G-17 npc_encounters rows must be objects")
            continue
        npc_id = str(raw_npc.get("id", "")).strip()
        seen_ids.add(npc_id)
        seen_roles.add(str(raw_npc.get("role", "")).strip())
        for key in ["display_name", "role", "encounter_type", "station", "route_or_station", "route_intent", "dialogue_seed", "quest_relevance", "world_flavor", "movement_policy", "provenance"]:
            if not str(raw_npc.get(key, "")).strip():
                failures.append(f"G-17 NPC {npc_id or '<unknown>'} missing {key}")
        asset_id = str(raw_npc.get("asset_id", "")).strip()
        if asset_id not in ALLOWED_ASSET_IDS:
            failures.append(f"G-17 NPC {npc_id} uses unapproved atelier NPC asset: {asset_id}")
        if raw_npc.get("atelier_standard_sprite") is not True:
            failures.append(f"G-17 NPC {npc_id} must record atelier_standard_sprite=true")
        if raw_npc.get("grounded_movement") is not True:
            failures.append(f"G-17 NPC {npc_id} must record grounded_movement=true")
        if str(raw_npc.get("movement_policy", "")) != "stationary_grounded_facing_bark_until_dedicated_walk_sheets":
            failures.append(f"G-17 NPC {npc_id} movement policy mismatch")
    for npc_id in REQUIRED_NPC_IDS:
        if npc_id not in seen_ids:
            failures.append(f"G-17 missing required NPC id: {npc_id}")
    for role in REQUIRED_ROLES:
        if role not in seen_roles:
            failures.append(f"G-17 missing required role: {role}")
    screenshots = set(str(item) for item in data.get("required_screenshots", []))
    for filename in REQUIRED_SCREENSHOTS:
        if filename not in screenshots:
            failures.append(f"G-17 source missing required screenshot: {filename}")
    motion_frames = set(str(item) for item in data.get("required_motion_frames", []))
    for filename in REQUIRED_MOTION_FRAMES:
        if filename not in motion_frames:
            failures.append(f"G-17 source missing required motion frame: {filename}")
    acceptance = data.get("acceptance", {})
    for flag in [
        "island_does_not_feel_empty",
        "npcs_do_not_hover_or_glide",
        "npcs_reinforce_opening_mystery",
        "movement_proof_exists_where_applicable",
        "all_visible_npcs_atelier_standard",
        "quest_or_world_relevance_for_each_npc",
    ]:
        if not isinstance(acceptance, dict) or acceptance.get(flag) is not True:
            failures.append(f"G-17 acceptance missing true flag: {flag}")
    for score_key in ["npc_ambient_score", "npc_motion_grounding_score", "art_direction_score", "world_layout_score"]:
        if not isinstance(acceptance, dict) or float(acceptance.get(score_key, 0.0)) < 8.5:
            failures.append(f"G-17 acceptance {score_key} must be at least 8.5")


def validate_report_json(data: dict[str, Any], failures: list[str]) -> None:
    if data.get("status") != "PASS":
        failures.append("G-17 report JSON status must be PASS")
    if data.get("human_review_required") is not False:
        failures.append("G-17 report JSON must record human_review_required=false")
    if data.get("screenshot_manifest") != "wayfarer_godot_vertical_slice/artifacts/review/g17_runtime_screenshots/g17_runtime_screenshot_manifest.json":
        failures.append("G-17 report JSON screenshot manifest mismatch")
    if data.get("motion_proof") != "wayfarer_godot_vertical_slice/artifacts/review/g17_motion_proof/g17_island_npc_motion_trace.json":
        failures.append("G-17 report JSON motion proof mismatch")
    if data.get("agent_council_verdict") != "COUNCIL_PASS_READY_FOR_PR":
        failures.append("G-17 report JSON council verdict mismatch")
    for score_key in ["npc_ambient_score", "npc_motion_grounding_score", "world_layout_score", "art_direction_score", "technical_stability_score"]:
        if float(data.get(score_key, 0.0)) < 8.5:
            failures.append(f"G-17 report JSON {score_key} must be at least 8.5")
    if data.get("provenance_atelier_result") != "PASS":
        failures.append("G-17 report JSON provenance_atelier_result must be PASS")


def validate_screenshot_manifest(manifest: dict[str, Any], failures: list[str]) -> None:
    if manifest.get("phase") != "G-17":
        failures.append("G-17 screenshot manifest phase mismatch")
    if manifest.get("status") != "PASS":
        failures.append("G-17 screenshot manifest status must be PASS")
    if manifest.get("no_hud_capture") is not True:
        failures.append("G-17 screenshot manifest must record no_hud_capture=true")
    if manifest.get("debug_overlays_disabled") is not True:
        failures.append("G-17 screenshot manifest must record debug_overlays_disabled=true")
    if manifest.get("motion_proof_path") != "res://artifacts/review/g17_motion_proof/g17_island_npc_motion_trace.json":
        failures.append("G-17 screenshot manifest motion_proof_path mismatch")
    filenames = {
        str(item.get("filename", ""))
        for item in manifest.get("screenshots", [])
        if isinstance(item, dict)
    }
    for filename in REQUIRED_SCREENSHOTS:
        if filename not in filenames:
            failures.append(f"G-17 screenshot manifest missing {filename}")
    for item in manifest.get("screenshots", []):
        if isinstance(item, dict):
            if item.get("status") != "PASS":
                failures.append(f"G-17 screenshot did not PASS: {item.get('filename', '<unknown>')}")
            raw_path = str(item.get("path", ""))
            if raw_path and not project_path(raw_path).exists():
                failures.append(f"G-17 screenshot path missing: {raw_path}")
    for key in ["opening_island_npc_encounter_contract_initial", "opening_island_npc_encounter_contract_final"]:
        contract = manifest.get(key, {})
        if not isinstance(contract, dict) or contract.get("phase") != "G-17":
            failures.append(f"G-17 screenshot manifest missing {key}")
        else:
            if int(contract.get("runtime_actor_count", 0)) < 5:
                failures.append(f"G-17 {key} runtime_actor_count is too low")
            if int(contract.get("grounded_actor_count", 0)) < 5:
                failures.append(f"G-17 {key} grounded_actor_count is too low")
            if int(contract.get("moving_actor_count", 0)) != 0:
                failures.append(f"G-17 {key} moving_actor_count must remain 0 until walk sheets exist")
            if bool(contract.get("position_drift_detected", True)):
                failures.append(f"G-17 {key} detected position drift")
    sequence = manifest.get("island_ambient_motion_proof_sequence", {})
    if not isinstance(sequence, dict) or sequence.get("status") != "PASS":
        failures.append("G-17 manifest missing PASS island ambient motion proof sequence")


def validate_motion_trace(trace: dict[str, Any], failures: list[str]) -> None:
    if trace.get("phase") != "G-17":
        failures.append("G-17 motion trace phase mismatch")
    if trace.get("status") != "PASS":
        failures.append("G-17 motion trace status must be PASS")
    if trace.get("route_walking_enabled") is not False:
        failures.append("G-17 motion trace must keep route_walking_enabled=false")
    if trace.get("no_hover_glide_slide") is not True:
        failures.append("G-17 motion trace must assert no_hover_glide_slide=true")
    if bool(trace.get("position_drift_detected", True)):
        failures.append("G-17 motion trace detected position drift")
    frames = trace.get("frame_sequence", [])
    if not isinstance(frames, list) or len(frames) < len(REQUIRED_MOTION_FRAMES):
        failures.append("G-17 motion trace must include timestamped frame sequence")
        frames = []
    frame_names = {
        str(item.get("filename", ""))
        for item in frames
        if isinstance(item, dict)
    }
    for filename in REQUIRED_MOTION_FRAMES:
        if filename not in frame_names:
            failures.append(f"G-17 motion trace missing frame: {filename}")
    for frame in frames:
        if isinstance(frame, dict):
            raw_path = str(frame.get("path", ""))
            if raw_path and not project_path(raw_path).exists():
                failures.append(f"G-17 motion frame path missing: {raw_path}")
            png = frame.get("png_verification", {})
            if not isinstance(png, dict) or png.get("status") != "PASS":
                failures.append(f"G-17 motion frame PNG verification failed: {frame.get('filename', '<unknown>')}")
    snapshots = trace.get("snapshots", [])
    if not isinstance(snapshots, list) or len(snapshots) < 5:
        failures.append("G-17 motion trace must include at least five rhythm snapshots")
        snapshots = []
    for snapshot in snapshots:
        if not isinstance(snapshot, dict):
            continue
        if int(snapshot.get("actor_count", 0)) < 5:
            failures.append("G-17 motion snapshot actor_count is too low")
        if bool(snapshot.get("position_drift_detected", True)):
            failures.append("G-17 motion snapshot detected position drift")
        for raw_actor in snapshot.get("actors", []):
            if not isinstance(raw_actor, dict):
                continue
            if raw_actor.get("route_walking_enabled") is not False:
                failures.append(f"G-17 actor {raw_actor.get('npc_id', '<unknown>')} route_walking_enabled must be false")
            if raw_actor.get("ground_shadow_visible") is not True:
                failures.append(f"G-17 actor {raw_actor.get('npc_id', '<unknown>')} missing visible ground shadow")
            if raw_actor.get("no_static_sprite_translation") is not True:
                failures.append(f"G-17 actor {raw_actor.get('npc_id', '<unknown>')} must assert no static sprite translation")


def validate_character_manifest(manifest: dict[str, Any], failures: list[str]) -> None:
    serialized = json.dumps(manifest, sort_keys=True)
    for asset_id in ALLOWED_ASSET_IDS:
        if asset_id not in serialized:
            failures.append(f"G-17 character manifest missing atelier NPC asset id: {asset_id}")
    assertions = manifest.get("provenance_assertions", {})
    if not isinstance(assertions, dict) or assertions.get("placeholder") is not False:
        failures.append("G-17 character manifest provenance must reject placeholder NPCs")
    if not isinstance(assertions, dict) or assertions.get("normal_review_eligible") is not True:
        failures.append("G-17 character manifest must remain normal_review_eligible")
    npc_motion = manifest.get("motion_contract", {}).get("npc", {}) if isinstance(manifest.get("motion_contract", {}), dict) else {}
    if not isinstance(npc_motion, dict) or npc_motion.get("route_walking_enabled") is not False:
        failures.append("G-17 character manifest NPC route walking must remain disabled until dedicated walk sheets")


if __name__ == "__main__":
    sys.exit(main())
