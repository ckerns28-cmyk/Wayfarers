extends RefCounted
class_name TavernWhisperSystem

const G10A_TAVERN_WHISPER_SYSTEM_PASS := "G-10A"
const DATA_PATH := "res://data/dialogue/tavern_whispers.json"

var _data: Dictionary = {}
var _ambient_index := 0


func _init() -> void:
	_data = _load_data()


func opening_rumor_response() -> String:
	return _interaction_line("third_toast", "Bess Armitage: Third Toast, then no names. If the lantern burns twice at the wharf, someone chose a side.")


func optional_secret_response() -> String:
	return _interaction_line("rear_service_gate", "Silas Crowe: Some messages never cross the tavern floor. Watch the rear gate after the second lantern.")


func notice_response() -> String:
	return _interaction_line("folded_notice", "Nora Vale: The folded notice is for people who know what the Third Toast means.")


func next_ambient_bark() -> String:
	var barks := _data.get("ambient_barks", []) as Array
	if barks.is_empty():
		return ""
	var line := String(barks[_ambient_index % barks.size()])
	_ambient_index += 1
	return line


func rumor_contract() -> Dictionary:
	var interactions := _data.get("quest_relevant_interactions", []) as Array
	var barks := _data.get("ambient_barks", []) as Array
	var hub_contract := (_data.get("hub_contract", {}) as Dictionary).duplicate(true)
	return {
		"phase": G10A_TAVERN_WHISPER_SYSTEM_PASS,
		"system_id": String(_data.get("system_id", "newport_tavern_whisper_system")),
		"location": String(_data.get("location", "Inn & Tavern")),
		"purpose": String(_data.get("purpose", "")),
		"rumor_cycle_policy": String(_data.get("rumor_cycle_policy", "")),
		"quest_relevant_npcs": (_data.get("quest_relevant_npcs", []) as Array).duplicate(),
		"quest_relevant_interaction_count": interactions.size(),
		"ambient_bark_count": barks.size(),
		"has_tavern_npcs": bool(hub_contract.get("has_tavern_npcs", false)),
		"has_rumor_dialogue": bool(hub_contract.get("has_rumor_dialogue", false)),
		"has_quest_relevant_interaction": bool(hub_contract.get("has_quest_relevant_interaction", false)),
		"has_rotating_rumor_lines": bool(hub_contract.get("has_rotating_rumor_lines", false)),
		"ties_to_harbor_commerce": bool(hub_contract.get("ties_to_harbor_commerce", false)),
		"ties_to_political_tension": bool(hub_contract.get("ties_to_political_tension", false)),
		"normal_play_debug_marker_free": bool(hub_contract.get("normal_play_debug_marker_free", false)),
		"sample_ambient_bark": String(barks[0]) if not barks.is_empty() else "",
		"third_toast_line": opening_rumor_response(),
		"rear_gate_line": optional_secret_response(),
	}


func debug_whisper_contract() -> Dictionary:
	var contract := rumor_contract()
	var sample_cycle := []
	for _i in range(3):
		sample_cycle.append(next_ambient_bark())
	contract["sample_cycle"] = sample_cycle
	contract["sample_cycle_count"] = sample_cycle.size()
	return contract


func _interaction_line(interaction_id: String, fallback: String) -> String:
	for raw_interaction in _data.get("quest_relevant_interactions", []):
		var interaction := raw_interaction as Dictionary
		if String(interaction.get("id", "")) == interaction_id:
			return String(interaction.get("line", fallback))
	return fallback


func _load_data() -> Dictionary:
	var raw_json := FileAccess.get_file_as_string(DATA_PATH)
	if raw_json.is_empty():
		return {}
	var parsed: Variant = JSON.parse_string(raw_json)
	if parsed is Dictionary:
		return parsed as Dictionary
	return {}
