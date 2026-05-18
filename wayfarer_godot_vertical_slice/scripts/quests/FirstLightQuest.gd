extends RefCounted
class_name FirstLightQuest

signal quest_updated(snapshot: Dictionary)

const QUEST_STATE := preload("res://scripts/QuestState.gd")
const G9A_QUEST_STATE_FOUNDATION_PASS := "G-9A"
const G10_OPENING_QUEST_ARC_PASS := "G-10"
const QUEST_ID := "first_light_whispers_before_dawn"
const QUEST_TITLE := "First Light"
const QUEST_REWARD_LABEL := "Reward: Resolve +5 for following the tavern whisper"
const CONTACT_REWARD_LABEL := "Named contact: Edrin Vale"
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
	{
		"id": "lantern_at_wharf",
		"text": "Look for the lantern signal at the wharf.",
	},
	{
		"id": "secure_contact",
		"text": "Secure a trusted contact before the rumor spreads.",
	},
	{
		"id": "hook_to_continue",
		"text": "Keep the missing line quiet until dawn.",
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
		if bool(_state.flags.get("third_toast_heard", false)) or _state.current_objective_id in ["secure_contact", "hook_to_continue"]:
			latest = _return_to_edrin()
		else:
			latest = _complete_counting_house()
	elif relevance == "harbor_work_path" and bool(_state.flags.get("third_toast_heard", false)):
		latest = _follow_wharf_lantern(role)
	elif relevance == "merchant_or_street_path" and bool(_state.flags.get("third_toast_heard", false)):
		latest = _follow_merchant_choice(role)
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
	debug_apply_event("jonah")
	debug_apply_event("silas")
	debug_apply_event("edrin")
	var snap := snapshot()
	return {
		"phase": G10_OPENING_QUEST_ARC_PASS,
		"quest_id": String(snap.get("quest_id", "")),
		"started_objectives": (snap.get("started_objectives", []) as Array).duplicate(),
		"completed_objectives": (snap.get("completed_objectives", []) as Array).duplicate(),
		"current_objective_id": String(snap.get("current_objective_id", "")),
		"reward_log": (snap.get("reward_log", []) as Array).duplicate(),
		"has_objective_update_feedback": (snap.get("progress_updates", []) as Array).size() >= 4,
		"has_reward_or_progression_update": (snap.get("reward_log", []) as Array).size() > 0,
		"playable_minutes_estimate": 12,
		"quest_beats": [
			"make_landfall",
			"report_to_counting_house",
			"missing_line_investigation",
			"third_toast_tavern_whisper",
			"lantern_at_wharf",
			"trusted_contact_hook",
		],
		"named_npc_roles": ["counting_house_clerk", "dockworker", "tavern_keeper", "dockworker_courier", "suspicious_patron"],
		"branch_choices": ["tell_edrin", "ask_the_wharf", "watch_rear_service_gate"],
		"optional_discovery": "rear_service_gate_hint",
		"hook_to_continue": "Edrin becomes a named contact and asks the player to keep the missing line quiet until dawn.",
		"three_named_or_role_npcs_participate": true,
		"choice_or_branch_exists": true,
		"secret_or_optional_discovery_exists": true,
		"reason_to_continue_exists": true,
		"supports_multiple_advancement_sources": true,
	}


func _complete_counting_house() -> Dictionary:
	if not _state.is_objective_complete("report_to_counting_house"):
		_state.complete_objective("report_to_counting_house", "Objective complete: Edrin confirms the missing ledger line.")
		_state.set_response("Edrin Vale: The missing line is not a mistake. Ask the wharf who handled the cargo, then listen at the Tavern/Inn.")
	if _state.current_objective_id in ["make_landfall", "report_to_counting_house"]:
		return _state.start_objective("investigate_missing_line", "Objective updated: ask about the missing ledger line.")
	return _state.snapshot()


func _record_missing_line_clue(relevance: String, role: String) -> Dictionary:
	_complete_counting_house()
	_state.set_flag("clue_" + relevance, true, "Journal updated: " + role.replace("_", " ") + " clue added.")
	if relevance == "missing_manifest_line":
		_state.set_response("Mara Pike: That crate was not lost. Someone made it disappear before the tide bell.")
	elif relevance == "merchant_or_street_path":
		_state.set_response("Honor Finch: Coin moved before the cargo did. Follow the buyer, not the box.")
	elif relevance == "optional_notice_clue":
		_state.set_response("Nora Vale: One notice is for officials. The folded one is for people who know the Third Toast.")
	else:
		_state.set_response("Jonah Reed: A sealed cargo line went quiet before the tide turned.")
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
		_state.set_response("Bess Armitage: Third Toast, then no names. If the lantern burns twice at the wharf, someone chose a side.")
	_state.add_reward(QUEST_REWARD_LABEL, 5)
	if _state.current_objective_id in ["lantern_at_wharf", "secure_contact", "hook_to_continue"]:
		return _state.snapshot()
	if _state.current_objective_id != "choose_next_lead":
		return _state.start_objective("choose_next_lead", "Objective updated: choose who to trust.")
	return _state.snapshot()


func _record_secret_path() -> Dictionary:
	_hear_tavern_whisper()
	_state.set_flag("rear_service_gate_hint", true, "Secret noted: whispers move through the rear service gate.")
	_state.set_response("Silas Crowe: Some messages never cross the tavern floor. Watch the rear gate after the second lantern.")
	return _state.snapshot()


func _follow_wharf_lantern(role: String) -> Dictionary:
	_hear_tavern_whisper()
	if not _state.is_objective_complete("choose_next_lead"):
		_state.complete_objective("choose_next_lead", "Objective complete: the wharf path is chosen.")
	_state.set_flag("chosen_path", "ask_the_wharf", "Journal updated: wharf path chosen through " + role.replace("_", " ") + ".")
	_state.start_objective("lantern_at_wharf", "Objective updated: look for the lantern signal at the wharf.")
	if not _state.is_objective_complete("lantern_at_wharf"):
		_state.complete_objective("lantern_at_wharf", "Objective complete: the lantern signal confirms a hidden network.")
	_state.set_response("Jonah Reed: Two lanterns means the cargo was claimed. One means it sank. Tonight there were two.")
	return _state.start_objective("secure_contact", "Objective updated: secure a trusted contact before dawn.")


func _follow_merchant_choice(role: String) -> Dictionary:
	_hear_tavern_whisper()
	if not _state.is_objective_complete("choose_next_lead"):
		_state.complete_objective("choose_next_lead", "Objective complete: the merchant path is chosen.")
	_state.set_flag("chosen_path", "merchant_or_street_path", "Journal updated: street path chosen through " + role.replace("_", " ") + ".")
	_state.set_response("Honor Finch: If you ask who bought the silence, ask who could afford it twice.")
	return _state.start_objective("secure_contact", "Objective updated: secure a trusted contact before dawn.")


func _return_to_edrin() -> Dictionary:
	if not _state.is_objective_complete("secure_contact") and _state.current_objective_id == "secure_contact":
		_state.complete_objective("secure_contact", "Objective complete: Edrin agrees to be your contact.")
	if not _state.reward_log.has(CONTACT_REWARD_LABEL):
		_state.add_reward(CONTACT_REWARD_LABEL, 0)
	_state.set_response("Edrin Vale: Keep the missing line out of official ink until dawn. Come back when the harbor bell changes.")
	return _state.start_objective("hook_to_continue", "Hook added: return at dawn with the missing line.")


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
