extends RefCounted
class_name FirstLightChoiceRouter

const G10B_MULTI_PATH_STARTER_CHOICE_PASS := "G-10B"
const DATA_PATH := "res://data/quests/first_light_multi_path_choices.json"

var _data: Dictionary = {}


func _init() -> void:
	_data = _load_data()


func choice_for_payload(payload: Dictionary, third_toast_heard: bool) -> Dictionary:
	var relevance := String(payload.get("quest_relevance", ""))
	for raw_path in _data.get("paths", []):
		var path := raw_path as Dictionary
		var relevances := path.get("quest_relevance", []) as Array
		if relevances.has(relevance):
			var result := path.duplicate(true)
			var always_available_relevances := [
				"first_light_counting_house",
				"missing_manifest_line",
				"optional_notice_clue",
				"tavern_whisper_hook",
			]
			result["available_after_third_toast"] = third_toast_heard or always_available_relevances.has(relevance)
			return result
	return {}


func path_response(path_id: String) -> String:
	for raw_path in _data.get("paths", []):
		var path := raw_path as Dictionary
		if String(path.get("id", "")) == path_id:
			return String(path.get("response", ""))
	return ""


func choice_contract() -> Dictionary:
	var paths := _data.get("paths", []) as Array
	var advancement_sources := {}
	var objectives := {}
	var optional_clues := []
	for raw_path in paths:
		var path := raw_path as Dictionary
		for npc in path.get("advancement_npcs", []):
			advancement_sources[String(npc)] = true
		for objective in path.get("advances_objectives", []):
			objectives[String(objective)] = true
		for clue in path.get("optional_clues", []):
			optional_clues.append(String(clue))
	var policy := _data.get("choice_policy", {}) as Dictionary
	return {
		"phase": G10B_MULTI_PATH_STARTER_CHOICE_PASS,
		"system_id": String(_data.get("system_id", "first_light_multi_path_choice_foundation")),
		"purpose": String(_data.get("purpose", "")),
		"path_count": paths.size(),
		"advancement_source_count": advancement_sources.keys().size(),
		"advancement_sources": advancement_sources.keys(),
		"advancable_objectives": objectives.keys(),
		"optional_clues": optional_clues,
		"branch_matrix_count": (_data.get("branch_matrix", []) as Array).size(),
		"minimum_advancement_sources": int(policy.get("minimum_advancement_sources", 0)),
		"supports_optional_clue": bool(policy.get("supports_optional_clue", false)),
		"supports_future_expansion": bool(policy.get("supports_future_expansion", false)),
		"not_single_railroad": bool(policy.get("not_single_railroad", false)),
		"required_paths": _path_ids(paths),
	}


func debug_branch_matrix() -> Array:
	return (_data.get("branch_matrix", []) as Array).duplicate(true)


func _path_ids(paths: Array) -> Array:
	var ids := []
	for raw_path in paths:
		var path := raw_path as Dictionary
		ids.append(String(path.get("id", "")))
	return ids


func _load_data() -> Dictionary:
	var raw_json := FileAccess.get_file_as_string(DATA_PATH)
	if raw_json.is_empty():
		return {}
	var parsed: Variant = JSON.parse_string(raw_json)
	if parsed is Dictionary:
		return parsed as Dictionary
	return {}
