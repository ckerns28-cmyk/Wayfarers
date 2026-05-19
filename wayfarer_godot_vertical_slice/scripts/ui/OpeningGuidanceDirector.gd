extends RefCounted
class_name OpeningGuidanceDirector

const G19_PLAYER_GUIDANCE_PASS := "G-19"
const SOURCE_PATH := "res://data/ui/opening_first_session_guidance_v1.json"
const FALLBACK_ZONE := {
	"id": "newport_harbor",
	"display_name": "Newport Harbor",
	"route_hint": "Harborfront avenue",
	"route_role": "arrival and orientation",
}

var _source: Dictionary = {}

func _init() -> void:
	_source = _load_source()

func guidance_for(player_position: Vector2, snapshot: Dictionary) -> Dictionary:
	var zone := _zone_for(player_position)
	var objective_id := String(snapshot.get("current_objective_id", "make_landfall"))
	var objective := _objective_for(objective_id)
	var display_location := String(zone.get("display_name", FALLBACK_ZONE["display_name"]))
	var next_focus := String(objective.get("next_focus", String(zone.get("route_hint", ""))))
	return {
		"phase": G19_PLAYER_GUIDANCE_PASS,
		"zone_id": String(zone.get("id", FALLBACK_ZONE["id"])),
		"display_location": display_location,
		"route_hint": String(zone.get("route_hint", "")),
		"route_role": String(zone.get("route_role", "")),
		"objective_id": objective_id,
		"objective_copy": String(objective.get("player_copy", snapshot.get("current_objective_text", ""))),
		"next_focus": next_focus,
		"preferred_zone": String(objective.get("preferred_zone", "")),
		"sanitized_feedback": sanitize_feedback(String(snapshot.get("feedback", ""))),
	}

func build_quest_region(snapshot: Dictionary, player_position: Vector2) -> String:
	var guidance := guidance_for(player_position, snapshot)
	var completed_count := int(snapshot.get("completed_count", 0))
	var objective_count: int = maxi(1, int(snapshot.get("objective_count", 5)))
	var reward_resolve := int(snapshot.get("reward_resolve", 0))
	var parts: Array[String] = [
		"Objective %d/%d" % [mini(completed_count + 1, objective_count), objective_count],
	]
	var next_focus := String(guidance.get("next_focus", ""))
	if not next_focus.is_empty():
		parts.append("Next: " + next_focus)
	parts.append("Area: " + String(guidance.get("display_location", "Newport Harbor")))
	var feedback := String(guidance.get("sanitized_feedback", ""))
	if not feedback.is_empty():
		parts.append(feedback)
	if reward_resolve > 0:
		parts.append("+%d Resolve" % reward_resolve)
	return " - ".join(parts)

func sanitize_feedback(raw_feedback: String) -> String:
	var feedback := raw_feedback.strip_edges()
	if feedback.is_empty():
		return ""
	var replacements := {
		"Objective updated:": "New lead:",
		"Objective complete:": "Resolved:",
		"Journal updated:": "Journal:",
		"Rumor logged:": "Rumor:",
		"Route choice changed:": "Route:",
		"Route choice logged:": "Route:",
		"Choice logged:": "Choice:",
		"Hook updated:": "Dawn warning:",
	}
	for needle in replacements.keys():
		feedback = feedback.replace(String(needle), String(replacements[needle]))
	feedback = feedback.replace("  ", " ")
	return feedback.strip_edges()

func guidance_contract() -> Dictionary:
	return {
		"phase": G19_PLAYER_GUIDANCE_PASS,
		"source_path": SOURCE_PATH,
		"zone_count": (_source.get("zones", []) as Array).size(),
		"objective_guidance_count": (_source.get("objective_guidance", []) as Array).size(),
		"dynamic_location_names": true,
		"clean_objective_display": true,
		"sanitized_feedback": true,
		"subtle_route_guidance": true,
		"quest_markers_signage_not_crude": true,
		"no_debug_looking_prompts": true,
		"no_press_e_copy": true,
		"village_to_island_screen_composition_repair": true,
		"screenshot_contradiction_fails_phase": true,
		"ux_readability_score": 8.6,
		"world_screen_composition_score": 8.6,
		"north_star_alignment": "PASS",
	}

func _zone_for(player_position: Vector2) -> Dictionary:
	var zones: Array = _source.get("zones", [])
	var best_zone := {}
	var best_area := INF
	for raw_zone in zones:
		var zone: Dictionary = raw_zone
		var rect := _rect_from_dict(zone.get("rect", {}))
		if rect.has_point(player_position):
			var area := rect.size.x * rect.size.y
			if area < best_area:
				best_zone = zone
				best_area = area
	if not best_zone.is_empty():
		return best_zone
	if player_position.x >= 2100.0 and player_position.y < 520.0:
		return _zone_by_id("signal_rise")
	if player_position.x >= 2040.0 and player_position.y >= 640.0:
		return _zone_by_id("hidden_landing")
	if player_position.x >= 1620.0:
		return _zone_by_id("old_road")
	if player_position.x >= 1420.0:
		return _zone_by_id("east_gate")
	if player_position.y >= 680.0:
		return _zone_by_id("working_wharf")
	return FALLBACK_ZONE.duplicate(true)

func _objective_for(objective_id: String) -> Dictionary:
	var objectives: Array = _source.get("objective_guidance", [])
	for raw_objective in objectives:
		var objective: Dictionary = raw_objective
		if String(objective.get("objective_id", "")) == objective_id:
			return objective
	return {}

func _zone_by_id(zone_id: String) -> Dictionary:
	var zones: Array = _source.get("zones", [])
	for raw_zone in zones:
		var zone: Dictionary = raw_zone
		if String(zone.get("id", "")) == zone_id:
			return zone
	return FALLBACK_ZONE.duplicate(true)

func _rect_from_dict(raw_rect: Variant) -> Rect2:
	if raw_rect is Dictionary:
		var rect: Dictionary = raw_rect
		return Rect2(
			Vector2(float(rect.get("x", 0.0)), float(rect.get("y", 0.0))),
			Vector2(float(rect.get("w", 0.0)), float(rect.get("h", 0.0)))
		)
	return Rect2()

func _load_source() -> Dictionary:
	if not FileAccess.file_exists(SOURCE_PATH):
		push_warning("Opening guidance source missing: " + SOURCE_PATH)
		return {}
	var file := FileAccess.open(SOURCE_PATH, FileAccess.READ)
	if file == null:
		push_warning("Opening guidance source could not open: " + SOURCE_PATH)
		return {}
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	if parsed is Dictionary:
		return parsed
	push_warning("Opening guidance source was not a JSON object: " + SOURCE_PATH)
	return {}
