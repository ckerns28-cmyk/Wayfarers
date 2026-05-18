extends RefCounted
class_name StarterVillageAudioHooks

const G11A_AUDIO_ATMOSPHERE_PASS := "G-11A"
const HOOK_REGISTRY_PATH := "res://data/audio/starter_village_atmosphere_hooks.json"
const REQUIRED_HOOK_IDS := [
	"harbor_ambience_hook",
	"tavern_ambience_hook",
	"footstep_event_hook",
	"quest_update_sound_hook",
	"ui_feedback_sound_hook",
]

static func hook_registry() -> Dictionary:
	var file := FileAccess.open(HOOK_REGISTRY_PATH, FileAccess.READ)
	if file == null:
		return _fallback_registry("missing_registry_file")
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	if parsed is Dictionary:
		return parsed
	return _fallback_registry("invalid_registry_json")

static func audio_hook_contract() -> Dictionary:
	var registry := hook_registry()
	var hooks: Array = registry.get("hooks", [])
	var hook_ids := []
	var missing_required := []
	var hooks_with_asset_references := []
	for raw_hook in hooks:
		var hook: Dictionary = raw_hook
		var hook_id := String(hook.get("id", ""))
		hook_ids.append(hook_id)
		if not String(hook.get("asset_reference", "")).is_empty():
			hooks_with_asset_references.append(hook_id)
	for required_id in REQUIRED_HOOK_IDS:
		if not hook_ids.has(required_id):
			missing_required.append(required_id)
	return {
		"phase": G11A_AUDIO_ATMOSPHERE_PASS,
		"registry_path": HOOK_REGISTRY_PATH,
		"schema_id": String(registry.get("schema_id", "")),
		"hook_count": hooks.size(),
		"hook_ids": hook_ids,
		"required_hook_ids": REQUIRED_HOOK_IDS.duplicate(),
		"missing_required_hook_ids": missing_required,
		"hooks_with_asset_references": hooks_with_asset_references,
		"no_audio_assets_loaded": bool(registry.get("no_audio_assets_loaded", false)),
		"no_broken_audio_references": bool(registry.get("no_broken_audio_references", false)),
		"no_licensing_unsafe_audio": bool(registry.get("no_licensing_unsafe_audio", false)),
		"web_export_safe": bool(registry.get("web_export_safe", false)),
		"placeholder_free": hooks_with_asset_references.is_empty(),
		"runtime_playback_enabled": false,
		"future_asset_requirements": (registry.get("future_asset_requirements", []) as Array).duplicate(),
	}

static func trigger_hook(hook_id: String, context := {}) -> Dictionary:
	var registry := hook_registry()
	for raw_hook in registry.get("hooks", []):
		var hook: Dictionary = raw_hook
		if String(hook.get("id", "")) == hook_id:
			return {
				"phase": G11A_AUDIO_ATMOSPHERE_PASS,
				"hook_id": hook_id,
				"event": String(hook.get("event", "")),
				"future_bus": String(hook.get("future_bus", "")),
				"asset_reference": String(hook.get("asset_reference", "")),
				"playback_started": false,
				"reason": "hook_only_no_license_safe_audio_asset_loaded",
				"context": context.duplicate(true) if context is Dictionary else {},
			}
	return {
		"phase": G11A_AUDIO_ATMOSPHERE_PASS,
		"hook_id": hook_id,
		"playback_started": false,
		"reason": "unknown_hook_id",
		"context": context.duplicate(true) if context is Dictionary else {},
	}

static func _fallback_registry(reason: String) -> Dictionary:
	return {
		"schema_id": "wayfarer.starter_village.audio_atmosphere_hooks.v1",
		"phase": G11A_AUDIO_ATMOSPHERE_PASS,
		"policy": "fallback_registry_" + reason,
		"no_audio_assets_loaded": true,
		"no_broken_audio_references": false,
		"no_licensing_unsafe_audio": true,
		"web_export_safe": true,
		"hooks": [],
		"future_asset_requirements": [],
	}
