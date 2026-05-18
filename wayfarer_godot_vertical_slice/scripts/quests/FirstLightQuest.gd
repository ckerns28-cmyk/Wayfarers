extends RefCounted
class_name FirstLightQuest

signal quest_updated(snapshot: Dictionary)

const QUEST_STATE := preload("res://scripts/QuestState.gd")
const G9A_QUEST_STATE_FOUNDATION_PASS := "G-9A"
const QUEST_ID := "first_light_whispers_before_dawn"
const QUEST_TITLE := "First Light"
const QUEST_REWARD_LABEL := "Reward: Resolve +5 for following the tavern whisper"
const OBJECTIVES := [
	{
		"id": "make_landfall",
		"text": "Make landfall at Newport Harbor and get your bearings.",
	},
	{
		"id": "report_to_counting_house",
		"text": "Find Edrin Vale at the Counting House.",
	},
	{
		"id": "investigate_missing_line",
		"text": "Ask the dockworkers, merchant row, or notice board about the missing ledger line.",
	},
	{
		"id": "follow_tavern_whisper",
		"text": "Bring the missing-line rumor to Bess Armitage at the Tavern/Inn.",
	},
	{
		"id": "choose_next_lead",
		"text": "Choose a next lead: Edrin, the wharf, or the rear gate.",
	},
]

var _state: WayfarerQuestState = QUEST_STATE.new()


func _init() -> void:
	_state.configure(QUEST_ID, QUEST_TITLE, OBJECTIVES)


func start() -> Dictionary:
	_state.start_objective("make_landfall", "Journal updated: landfall logged at Newport Harbor.")
	_state.complete_objective("make_landfall", "Objective complete: Newport Harbor reached.")
	var snapshot := _state.start_objective("report_to_counting_house", "Objective updated: find Edrin Vale at the Counting House.")
	quest_updated.emit(snapshot)
	return snapshot


func handle_interaction(target: Node, dialogue_text: String) -> Dictionary:
	return handle_interaction_payload(_payload_from_target(target, dialogue_text))


func handle_interaction_payload(payload: Dictionary) -> Dictionary:
	var relevance := String(payload.get("quest_relevance", ""))
	var role := String(payload.get("role", ""))
	var target_id := String(payload.get("id", payload.get("target_id", "")))
	var latest := _state.snapshot()

	if relevance == "first_light_counting_house" or target_id == "EdrinVale":
		latest = _complete_counting_house()
	elif relevance in ["missing_manifest_line", "harbor_work_path", "merchant_or_street_path", "optional_notice_clue"]:
		latest = _record_missing_line_clue(relevance, role)
	elif relevance == "tavern_whisper_hook":
		latest = _hear_tavern_whisper()
	elif relevance == "optional_secret_path":
		latest = _record_secret_path()

	quest_updated.emit(latest)
	return latest


func debug_apply_event(event_id: String) -> Dictionary:
	var payload_by_event := {
		"edrin": {"id": "EdrinVale", "role": "counting_house_clerk", "quest_relevance": "first_light_counting_house"},
		"mara": {"id": "mara_pike_dockworker", "role": "dockworker", "quest_relevance": "missing_manifest_line"},
		"jonah": {"id": "jonah_reed_dock_courier", "role": "dockworker_courier", "quest_relevance": "harbor_work_path"},
		"honor": {"id": "honor_finch_merchant_shopkeeper", "role": "merchant_shopkeeper", "quest_relevance": "merchant_or_street_path"},
		"nora": {"id": "nora_vale_rumor_carrier", "role": "rumor_carrier", "quest_relevance": "optional_notice_clue"},
		"bess": {"id": "bess_armitage_tavern_keeper", "role": "tavern_keeper", "quest_relevance": "tavern_whisper_hook"},
		"silas": {"id": "silas_crowe_suspicious_patron", "role": "suspicious_patron", "quest_relevance": "optional_secret_path"},
	}
	return handle_interaction_payload((payload_by_event.get(event_id, {}) as Dictionary).duplicate(true))


func snapshot() -> Dictionary:
	return _state.snapshot()


func debug_playthrough_contract() -> Dictionary:
	start()
	debug_apply_event("edrin")
	debug_apply_event("mara")
	debug_apply_event("bess")
	debug_apply_event("silas")
	var snap := snapshot()
	return {
		"phase": G9A_QUEST_STATE_FOUNDATION_PASS,
		"quest_id": String(snap.get("quest_id", "")),
		"started_objectives": (snap.get("started_objectives", []) as Array).duplicate(),
		"completed_objectives": (snap.get("completed_objectives", []) as Array).duplicate(),
		"current_objective_id": String(snap.get("current_objective_id", "")),
		"reward_log": (snap.get("reward_log", []) as Array).duplicate(),
		"has_objective_update_feedback": (snap.get("progress_updates", []) as Array).size() >= 4,
		"has_reward_or_progression_update": (snap.get("reward_log", []) as Array).size() > 0,
		"supports_multiple_advancement_sources": true,
	}


func _complete_counting_house() -> Dictionary:
	if not _state.is_objective_complete("report_to_counting_house"):
		_state.complete_objective("report_to_counting_house", "Objective complete: Edrin confirms the missing ledger line.")
	if _state.current_objective_id in ["make_landfall", "report_to_counting_house"]:
		return _state.start_objective("investigate_missing_line", "Objective updated: ask about the missing ledger line.")
	return _state.snapshot()


func _record_missing_line_clue(relevance: String, role: String) -> Dictionary:
	_complete_counting_house()
	_state.set_flag("clue_" + relevance, true, "Journal updated: " + role.replace("_", " ") + " clue added.")
	if not _state.is_objective_complete("investigate_missing_line"):
		_state.complete_objective("investigate_missing_line", "Objective complete: the missing line is not clerical error.")
	return _state.start_objective("follow_tavern_whisper", "Whisper noted: the Third Toast begins at the Tavern/Inn.")


func _hear_tavern_whisper() -> Dictionary:
	if not _state.is_objective_complete("investigate_missing_line"):
		_state.complete_objective("investigate_missing_line", "Objective complete: tavern rumor confirms the missing line matters.")
	if not _state.is_objective_complete("follow_tavern_whisper"):
		_state.complete_objective("follow_tavern_whisper", "Objective complete: Bess names the Third Toast.")
	if not bool(_state.flags.get("third_toast_heard", false)):
		_state.set_flag("third_toast_heard", true, "Rumor logged: The Third Toast is real.")
	_state.add_reward(QUEST_REWARD_LABEL, 5)
	if _state.current_objective_id != "choose_next_lead":
		return _state.start_objective("choose_next_lead", "Objective updated: choose who to trust.")
	return _state.snapshot()


func _record_secret_path() -> Dictionary:
	_hear_tavern_whisper()
	_state.set_flag("rear_service_gate_hint", true, "Secret noted: whispers move through the rear service gate.")
	return _state.snapshot()


func _payload_from_target(target: Node, dialogue_text: String) -> Dictionary:
	var payload := {
		"id": "",
		"role": "",
		"quest_relevance": "",
		"dialogue_text": dialogue_text,
	}
	if target == null:
		return payload
	payload["target_id"] = String(target.name)
	if target.has_method("npc_population_contract"):
		var npc_contract := target.call("npc_population_contract") as Dictionary
		payload["id"] = String(npc_contract.get("id", String(target.name)))
		payload["role"] = String(npc_contract.get("role", ""))
		payload["quest_relevance"] = String(npc_contract.get("quest_relevance", ""))
	elif target.has_method("prompt_ux_contract"):
		var prompt_contract := target.call("prompt_ux_contract") as Dictionary
		payload["id"] = String(prompt_contract.get("prompt_text", String(target.name)))
	return payload
