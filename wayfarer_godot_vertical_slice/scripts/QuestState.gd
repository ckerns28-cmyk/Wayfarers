extends RefCounted
class_name WayfarerQuestState

const G9A_QUEST_STATE_FOUNDATION_PASS := "G-9A"

var quest_id := ""
var quest_title := ""
var objectives: Array = []
var started_objectives: Array[String] = []
var completed_objectives: Array[String] = []
var current_objective_id := ""
var flags := {}
var progress_updates: Array[String] = []
var reward_log: Array[String] = []
var reward_resolve := 0
var last_feedback := ""
var last_response := ""


func configure(id: String, title: String, objective_rows: Array) -> void:
	quest_id = id
	quest_title = title
	objectives = objective_rows.duplicate(true)
	if not objectives.is_empty():
		current_objective_id = String((objectives[0] as Dictionary).get("id", ""))


func start_objective(objective_id: String, feedback := "") -> Dictionary:
	if objective_id.is_empty():
		return snapshot()
	if not started_objectives.has(objective_id):
		started_objectives.append(objective_id)
	current_objective_id = objective_id
	_record_feedback(feedback)
	return snapshot()


func complete_objective(objective_id: String, feedback := "") -> Dictionary:
	if objective_id.is_empty():
		return snapshot()
	if not completed_objectives.has(objective_id):
		completed_objectives.append(objective_id)
	_record_feedback(feedback)
	return snapshot()


func set_flag(flag_id: String, value: Variant = true, feedback := "") -> Dictionary:
	if not flag_id.is_empty():
		flags[flag_id] = value
	_record_feedback(feedback)
	return snapshot()


func add_reward(label: String, resolve_amount := 0) -> Dictionary:
	var is_new_reward := not label.is_empty() and not reward_log.has(label)
	if is_new_reward:
		reward_log.append(label)
	if is_new_reward:
		reward_resolve += max(0, resolve_amount)
	if is_new_reward and resolve_amount > 0:
		_record_feedback("Reward: +" + str(resolve_amount) + " Resolve")
	return snapshot()


func set_response(text: String) -> Dictionary:
	last_response = text
	return snapshot()


func is_objective_complete(objective_id: String) -> bool:
	return completed_objectives.has(objective_id)


func objective_text(objective_id: String) -> String:
	for raw_objective in objectives:
		var objective := raw_objective as Dictionary
		if String(objective.get("id", "")) == objective_id:
			return String(objective.get("text", ""))
	return ""


func current_objective_text() -> String:
	return objective_text(current_objective_id)


func snapshot() -> Dictionary:
	return {
		"phase": G9A_QUEST_STATE_FOUNDATION_PASS,
		"quest_id": quest_id,
		"quest_title": quest_title,
		"journal_title": "Journal - " + quest_title,
		"current_objective_id": current_objective_id,
		"current_objective_text": current_objective_text(),
		"started_objectives": started_objectives.duplicate(),
		"completed_objectives": completed_objectives.duplicate(),
		"objective_count": objectives.size(),
		"completed_count": completed_objectives.size(),
		"flags": flags.duplicate(true),
		"progress_updates": progress_updates.duplicate(),
		"reward_log": reward_log.duplicate(),
		"reward_resolve": reward_resolve,
		"feedback": last_feedback,
		"response_text": last_response,
		"session_persistence": "in_memory_runtime_state_for_current_session",
	}


func _record_feedback(feedback: String) -> void:
	if feedback.is_empty():
		return
	last_feedback = feedback
	progress_updates.append(feedback)
