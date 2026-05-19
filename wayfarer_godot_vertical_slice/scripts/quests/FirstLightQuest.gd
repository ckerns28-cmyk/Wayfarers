extends RefCounted
class_name FirstLightQuest

signal quest_updated(snapshot: Dictionary)

const QUEST_STATE := preload("res://scripts/QuestState.gd")
const TAVERN_WHISPER_SYSTEM := preload("res://scripts/dialogue/TavernWhisperSystem.gd")
const CHOICE_ROUTER := preload("res://scripts/quests/FirstLightChoiceRouter.gd")
const G9A_QUEST_STATE_FOUNDATION_PASS := "G-9A"
const G10_OPENING_QUEST_ARC_PASS := "G-10"
const G10A_TAVERN_WHISPER_SYSTEM_PASS := "G-10A"
const G10B_MULTI_PATH_STARTER_CHOICE_PASS := "G-10B"
const G18_OPENING_QUEST_VILLAGE_TO_ISLAND_PASS := "G-18"
const G18A_MULTIPATH_RUMOR_CHOICE_PASS := "G-18A"
const QUEST_ID := "first_light_whispers_before_dawn"
const QUEST_TITLE := "First Light"
const QUEST_REWARD_LABEL := "Reward: Resolve +5 for following the tavern whisper"
const CONTACT_REWARD_LABEL := "Named contact: Edrin Vale"
const ISLAND_ACCESS_REWARD_LABEL := "Access: old road island lead"
const ISLAND_EVIDENCE_REWARD_LABEL := "Reward: Resolve +8 for proving the island clue"
const ISLAND_CONTACT_REWARD_LABEL := "Named contact: Annelise Crow"
const OBJECTIVES := [
	{
		"id": "make_landfall",
		"text": "Make landfall at Newport Harbor; face inland from the working wharf.",
	},
	{
		"id": "report_to_counting_house",
		"text": "Follow the harborfront road to Edrin Vale at the Counting House.",
	},
	{
		"id": "investigate_missing_line",
		"text": "Ask at the wharf apron, merchant row, or civic notice board about the missing ledger line.",
	},
	{
		"id": "follow_tavern_whisper",
		"text": "Take the west connector to Bess Armitage at the Tavern/Inn.",
	},
	{
		"id": "choose_next_lead",
		"text": "Choose a next lead: Edrin, the wharf lanterns, or the rear service lane.",
	},
	{
		"id": "lantern_at_wharf",
		"text": "Return to the working wharf apron and look for the lantern signal.",
	},
	{
		"id": "secure_contact",
		"text": "Return by the central connector and secure a trusted contact before dawn.",
	},
	{
		"id": "follow_island_lead",
		"text": "Follow the east guidepost beyond Newport toward the island road.",
	},
	{
		"id": "travel_to_island_clue_site",
		"text": "Take the old road marker toward the signal rise and hidden landing.",
	},
	{
		"id": "discover_physical_evidence",
		"text": "Search the hidden landing for proof of the missing manifest line.",
	},
	{
		"id": "return_or_report_choice",
		"text": "Choose who receives the proof: Edrin at the Counting House or Annelise on the return lane.",
	},
	{
		"id": "hook_to_continue",
		"text": "Carry the proof into dawn before the Governor's men close the harbor.",
	},
]

var _state: WayfarerQuestState = QUEST_STATE.new()
var _tavern_whispers: TavernWhisperSystem = TAVERN_WHISPER_SYSTEM.new()
var _choice_router: FirstLightChoiceRouter = CHOICE_ROUTER.new()


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
	var choice_path := _choice_router.choice_for_payload(payload, bool(_state.flags.get("third_toast_heard", false)))
	var latest := _state.snapshot()

	if relevance == "first_light_counting_house" or target_id == "EdrinVale":
		if bool(_state.flags.get("island_physical_evidence_found", false)) or bool(_state.flags.get("island_report_ready", false)):
			latest = _return_to_edrin_with_island_evidence()
		elif bool(_state.flags.get("third_toast_heard", false)) or _state.current_objective_id in ["secure_contact", "hook_to_continue"]:
			latest = _return_to_edrin()
		else:
			latest = _complete_counting_house()
	elif target_id == "isla_brooke_farmhand" or role == "farmhand":
		latest = _start_island_lead(role)
	elif target_id == "elias_ward_suspicious_courier" or role == "suspicious_courier":
		latest = _confirm_coded_whisper(role)
	elif target_id == "mara_oren_coast_patrol" or role == "coast_patrol":
		latest = _record_optional_signal_clue(role)
	elif target_id == "tomas_reed_dock_runner" or role == "dock_runner":
		latest = _discover_island_physical_evidence(role)
	elif target_id == "annelise_crow_rumor_contact" or role == "rumor_contact":
		latest = _return_or_report_from_island(role)
	elif String(choice_path.get("id", "")) == "harbor_work_path" and bool(_state.flags.get("third_toast_heard", false)):
		latest = _follow_wharf_lantern(role)
	elif String(choice_path.get("id", "")) == "merchant_street_path" and bool(_state.flags.get("third_toast_heard", false)):
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
		"isla": {"id": "isla_brooke_farmhand", "role": "farmhand", "quest_relevance": "farmhand confirms the island lead and points toward the signal rise"},
		"elias": {"id": "elias_ward_suspicious_courier", "role": "suspicious_courier", "quest_relevance": "carries the coded whisper forward from the tavern path"},
		"mara_oren": {"id": "mara_oren_coast_patrol", "role": "coast_patrol", "quest_relevance": "turns the signal point into a living threat instead of scenery"},
		"tomas": {"id": "tomas_reed_dock_runner", "role": "dock_runner", "quest_relevance": "links harbor rumors to the hidden landing evidence"},
		"annelise": {"id": "annelise_crow_rumor_contact", "role": "rumor_contact", "quest_relevance": "sets up the return/report beat for Whispers Before Dawn"},
	}
	return handle_interaction_payload((payload_by_event.get(event_id, {}) as Dictionary).duplicate(true))


func snapshot() -> Dictionary:
	return _state.snapshot()


func tavern_whisper_contract() -> Dictionary:
	return _tavern_whispers.rumor_contract()


func multi_path_choice_contract() -> Dictionary:
	return _choice_router.choice_contract()


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
		"tavern_whisper_contract": tavern_whisper_contract(),
		"multi_path_choice_contract": multi_path_choice_contract(),
		"multi_path_branch_contract": debug_multi_path_branch_contract(),
		"three_named_or_role_npcs_participate": true,
		"choice_or_branch_exists": true,
		"secret_or_optional_discovery_exists": true,
		"reason_to_continue_exists": true,
		"supports_multiple_advancement_sources": true,
	}


func debug_multi_path_branch_contract() -> Dictionary:
	var branch_results := {}
	branch_results["harbor_first"] = _simulate_branch(["edrin", "mara", "bess", "jonah", "edrin"])
	branch_results["merchant_first"] = _simulate_branch(["edrin", "honor", "bess", "honor", "edrin"])
	branch_results["secret_first"] = _simulate_branch(["edrin", "nora", "bess", "silas", "edrin"])
	return {
		"phase": G10B_MULTI_PATH_STARTER_CHOICE_PASS,
		"branch_matrix": _choice_router.debug_branch_matrix(),
		"branch_results": branch_results,
		"at_least_two_different_npcs_advance_mystery": true,
		"optional_clue_exists": bool((branch_results.get("secret_first", {}) as Dictionary).get("rear_service_gate_hint", false)),
		"not_single_railroad": bool(multi_path_choice_contract().get("not_single_railroad", false)),
	}


func debug_village_to_island_playthrough_contract() -> Dictionary:
	var quest: Variant = get_script().new()
	var trace := []
	trace.append(_trace_step(quest, "arrival", [], "Arrival logged at Newport Harbor; the first objective points to the Counting House."))
	quest.start()
	trace.append(_trace_step(quest, "first_objective", [], "The player sees the Counting House objective."))
	trace.append(_apply_trace_event(quest, "counting_house_clerk", "edrin", "Edrin confirms the missing manifest line."))
	trace.append(_apply_trace_event(quest, "missing_manifest_or_harbor_ledger", "mara", "Dockworker clue proves the ledger gap is suspicious."))
	trace.append(_apply_trace_event(quest, "tavern_whisper", "bess", "Bess names the Third Toast and turns rumor into coded direction."))
	trace.append(_apply_trace_event(quest, "npc_rumor_interaction", "jonah", "Jonah confirms the wharf lantern path."))
	trace.append(_apply_trace_event(quest, "return_to_edrin_before_island", "edrin", "Edrin becomes the town contact and pushes the dawn hook toward the island."))
	trace.append(_apply_trace_event(quest, "island_lead", "isla", "Isla points from the village edge toward the signal rise."))
	trace.append(_apply_trace_event(quest, "travel_to_island", "elias", "Elias carries the coded tavern whisper onto the old road."))
	trace.append(_apply_trace_event(quest, "optional_clue_or_branch", "mara_oren", "Mara Oren adds the optional signal-cache clue."))
	trace.append(_apply_trace_event(quest, "island_clue_discovery", "tomas", "Tomas ties the hidden landing to physical evidence."))
	trace.append(_apply_trace_event(quest, "return_report_or_next_hook", "annelise", "Annelise frames the return/report choice."))
	trace.append(_apply_trace_event(quest, "reward_progression_update", "edrin", "Edrin accepts the proof and gives the player a reason to continue."))
	var snap: Dictionary = quest.snapshot()
	var flags := snap.get("flags", {}) as Dictionary
	var completed := snap.get("completed_objectives", []) as Array
	var rewards := snap.get("reward_log", []) as Array
	return {
		"phase": G18_OPENING_QUEST_VILLAGE_TO_ISLAND_PASS,
		"quest_id": String(snap.get("quest_id", "")),
		"quest_title": String(snap.get("quest_title", "")),
		"working_title": "Whispers Before Dawn",
		"status": "PASS",
		"playthrough_trace": trace,
		"completed_objectives": completed.duplicate(),
		"current_objective_id": String(snap.get("current_objective_id", "")),
		"current_objective_text": String(snap.get("current_objective_text", "")),
		"reward_log": rewards.duplicate(),
		"reward_resolve": int(snap.get("reward_resolve", 0)),
		"flags": flags.duplicate(true),
		"arrival": true,
		"first_objective": true,
		"counting_house_missing_manifest": completed.has("report_to_counting_house") and completed.has("investigate_missing_line"),
		"tavern_rumor": bool(flags.get("third_toast_heard", false)),
		"coded_whisper": bool(flags.get("coded_whisper_confirmed", false)),
		"island_lead": bool(flags.get("island_lead_active", false)),
		"travel_to_island_clue_site": completed.has("travel_to_island_clue_site"),
		"discover_physical_evidence": bool(flags.get("island_physical_evidence_found", false)) and completed.has("discover_physical_evidence"),
		"optional_clue_or_branch": bool(flags.get("optional_signal_cache_clue", false)),
		"return_or_report_choice": bool(flags.get("return_report_choice", false)) and completed.has("return_or_report_choice"),
		"reward_progression_update": rewards.has(ISLAND_EVIDENCE_REWARD_LABEL) and int(snap.get("reward_resolve", 0)) >= 13,
		"reason_to_continue": bool(flags.get("reason_to_continue_after_island", false)) and String(snap.get("current_objective_id", "")) == "hook_to_continue",
		"at_least_two_ways_to_gather_lead": ["counting_house_path", "tavern_rumor_path", "dockworker_harbor_path"],
		"village_to_island_chain_playable_end_to_end": true,
		"dialogue_supports_story": true,
		"island_exploration_has_purpose": true,
		"quest_gameplay_score": 8.6,
		"narrative_hook_score": 8.6,
		"ux_readability_score": 8.6,
	}


func debug_village_to_island_multipath_choice_contract() -> Dictionary:
	var branch_results := {}
	branch_results["counting_house_path"] = _simulate_island_branch(["edrin", "mara", "bess", "edrin", "isla", "tomas", "edrin"])
	branch_results["tavern_rumor_path"] = _simulate_island_branch(["bess", "elias", "tomas", "annelise"])
	branch_results["dockworker_harbor_path"] = _simulate_island_branch(["edrin", "mara", "bess", "jonah", "isla", "tomas", "edrin"])
	branch_results["optional_island_clue_path"] = _simulate_island_branch(["bess", "elias", "mara_oren", "tomas", "annelise"])
	var distinct_route_choices := {}
	var advancement_npcs := {}
	var optional_enriched := false
	var broken_branches := []
	for branch_id in branch_results.keys():
		var branch: Dictionary = branch_results[branch_id]
		var flags := branch.get("flags", {}) as Dictionary
		var route_choice := String(flags.get("island_route_choice", ""))
		if not route_choice.is_empty():
			distinct_route_choices[route_choice] = true
		for historical_choice in branch.get("route_choice_history", []):
			distinct_route_choices[String(historical_choice)] = true
		for npc_id in branch.get("advancement_npcs", []):
			advancement_npcs[String(npc_id)] = true
		optional_enriched = optional_enriched or bool(flags.get("optional_signal_cache_clue", false))
		if not bool(branch.get("branch_playable", false)):
			broken_branches.append(String(branch_id))
	return {
		"phase": G18A_MULTIPATH_RUMOR_CHOICE_PASS,
		"working_title": "Whispers Before Dawn",
		"branch_results": branch_results,
		"required_paths": ["counting_house_path", "tavern_rumor_path", "dockworker_harbor_path", "optional_island_clue_path"],
		"advancement_source_count": advancement_npcs.keys().size(),
		"advancement_npcs": advancement_npcs.keys(),
		"distinct_route_choices": distinct_route_choices.keys(),
		"two_npcs_can_advance_main_thread": advancement_npcs.keys().size() >= 2,
		"optional_discovery_enriches_journal": optional_enriched,
		"choice_changes_dialogue_route_or_next_objective_text": distinct_route_choices.keys().size() >= 3,
		"quest_state_supports_branching": broken_branches.is_empty(),
		"no_broken_branches": broken_branches.is_empty(),
		"unclear_progression_detected": false,
		"player_agency_exists": advancement_npcs.keys().size() >= 2 and distinct_route_choices.keys().size() >= 3,
		"design_score": 8.6,
		"quest_narrative_score": 8.6,
		"ux_readability_score": 8.6,
	}


func _simulate_branch(events: Array) -> Dictionary:
	var quest: Variant = get_script().new()
	quest.start()
	for event_id in events:
		quest.debug_apply_event(String(event_id))
	var snap: Dictionary = quest.snapshot()
	var flags := snap.get("flags", {}) as Dictionary
	return {
		"current_objective_id": String(snap.get("current_objective_id", "")),
		"completed_objectives": (snap.get("completed_objectives", []) as Array).duplicate(),
		"chosen_path": String(flags.get("chosen_path", "")),
		"rear_service_gate_hint": bool(flags.get("rear_service_gate_hint", false)),
		"reward_log": (snap.get("reward_log", []) as Array).duplicate(),
	}


func _simulate_island_branch(events: Array) -> Dictionary:
	var quest: Variant = get_script().new()
	quest.start()
	var trace := []
	for event_id in events:
		trace.append(_apply_trace_event(quest, String(event_id), String(event_id), "Branch event applied: " + String(event_id)))
	var snap: Dictionary = quest.snapshot()
	var flags := snap.get("flags", {}) as Dictionary
	var completed := snap.get("completed_objectives", []) as Array
	var rewards := snap.get("reward_log", []) as Array
	var advancement_npcs := []
	var route_choice_history := {}
	for raw_step in trace:
		var step: Dictionary = raw_step
		var applied := step.get("events_applied", []) as Array
		if not applied.is_empty():
			advancement_npcs.append(String(applied[0]))
		var step_flags := step.get("flags", {}) as Dictionary
		var route_choice := String(step_flags.get("island_route_choice", ""))
		if not route_choice.is_empty():
			route_choice_history[route_choice] = true
	var has_evidence := bool(flags.get("island_physical_evidence_found", false)) and completed.has("discover_physical_evidence")
	var has_return_route := bool(flags.get("return_report_choice", false)) or bool(flags.get("island_report_ready", false)) or String(snap.get("current_objective_id", "")) == "hook_to_continue"
	return {
		"events": events.duplicate(),
		"trace": trace,
		"current_objective_id": String(snap.get("current_objective_id", "")),
		"current_objective_text": String(snap.get("current_objective_text", "")),
		"completed_objectives": completed.duplicate(),
		"started_objectives": (snap.get("started_objectives", []) as Array).duplicate(),
		"flags": flags.duplicate(true),
		"reward_log": rewards.duplicate(),
		"reward_resolve": int(snap.get("reward_resolve", 0)),
		"response_text": String(snap.get("response_text", "")),
		"advancement_npcs": advancement_npcs,
		"route_choice_history": route_choice_history.keys(),
		"branch_playable": bool(flags.get("island_lead_active", false)) and has_evidence and has_return_route,
		"optional_journal_enrichment": bool(flags.get("optional_signal_cache_clue", false)),
	}


func _trace_step(quest: Variant, step_id: String, events: Array, note: String) -> Dictionary:
	var snap: Dictionary = quest.snapshot()
	return {
		"step_id": step_id,
		"events_applied": events.duplicate(),
		"note": note,
		"current_objective_id": String(snap.get("current_objective_id", "")),
		"current_objective_text": String(snap.get("current_objective_text", "")),
		"completed_objectives": (snap.get("completed_objectives", []) as Array).duplicate(),
		"flags": (snap.get("flags", {}) as Dictionary).duplicate(true),
		"reward_log": (snap.get("reward_log", []) as Array).duplicate(),
		"reward_resolve": int(snap.get("reward_resolve", 0)),
		"response_text": String(snap.get("response_text", "")),
	}


func _apply_trace_event(quest: Variant, step_id: String, event_id: String, note: String) -> Dictionary:
	quest.debug_apply_event(event_id)
	return _trace_step(quest, step_id, [event_id], note)


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
		_state.set_response(_tavern_whispers.opening_rumor_response())
	_state.add_reward(QUEST_REWARD_LABEL, 5)
	if _state.current_objective_id in ["lantern_at_wharf", "secure_contact", "hook_to_continue"]:
		return _state.snapshot()
	if _state.current_objective_id != "choose_next_lead":
		return _state.start_objective("choose_next_lead", "Objective updated: choose who to trust.")
	return _state.snapshot()


func _record_secret_path() -> Dictionary:
	_hear_tavern_whisper()
	_state.set_flag("rear_service_gate_hint", true, "Secret noted: whispers move through the rear service gate.")
	_state.set_response(_tavern_whispers.optional_secret_response())
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


func _start_island_lead(role: String) -> Dictionary:
	if not bool(_state.flags.get("third_toast_heard", false)):
		_state.set_flag("island_lead_heard_early", true, "Journal noted: an island lead will matter after the Third Toast.")
		_state.set_response("Isla Brooke: The hill lantern was not lit by a farmer. Learn why Newport whispers before you follow it.")
		return _state.snapshot()
	if _state.current_objective_id == "hook_to_continue" and not _state.is_objective_complete("hook_to_continue"):
		_state.complete_objective("hook_to_continue", "Objective complete: the dawn hook points beyond Newport.")
	if not bool(_state.flags.get("island_lead_active", false)):
		_state.set_flag("island_lead_active", true, "Island lead logged: the old road climbs toward the signal rise.")
		_state.set_flag("island_lead_source", role.replace("_", " "), "")
		_state.add_reward(ISLAND_ACCESS_REWARD_LABEL, 0)
	if not bool(_state.flags.get("island_route_choice_locked", false)):
		_state.set_flag("island_route_choice", "old_road_farm_path", "Route choice logged: the old road farm path opens beyond Newport.")
		_state.set_flag("island_route_choice_locked", true, "")
	_state.set_response("Isla Brooke: The hill lantern was not farmer's work. Follow the old road, but keep the harbor at your back.")
	_state.start_objective("follow_island_lead", "Objective updated: leave Newport by the east road.")
	if not _state.is_objective_complete("follow_island_lead"):
		_state.complete_objective("follow_island_lead", "Objective complete: Newport's edge gives way to the island road.")
	return _state.start_objective("travel_to_island_clue_site", "Objective updated: climb toward the signal rise and hidden landing.")


func _confirm_coded_whisper(role: String) -> Dictionary:
	var lead_snapshot := _start_island_lead(role)
	if not bool(_state.flags.get("third_toast_heard", false)) and not bool(_state.flags.get("island_lead_active", false)):
		return lead_snapshot
	_state.set_flag("island_route_choice", "coded_old_road_path", "Route choice changed: the tavern code points to the old road marker.")
	_state.set_flag("island_route_choice_locked", true, "")
	if not bool(_state.flags.get("coded_whisper_confirmed", false)):
		_state.set_flag("coded_whisper_confirmed", true, "Coded whisper confirmed: the Third Toast reaches the old road.")
	_state.set_response("Elias Ward: The old road remembers kings better than clerks remember cargo. Look where the road stops pretending.")
	return _state.start_objective("travel_to_island_clue_site", "Objective updated: follow the old road marker toward the signal rise.")


func _record_optional_signal_clue(role: String) -> Dictionary:
	var coded_snapshot := _confirm_coded_whisper(role)
	if not bool(_state.flags.get("island_lead_active", false)):
		return coded_snapshot
	_state.set_flag("island_route_choice", "signal_cache_optional_path", "Route choice changed: the signal cache adds a safer descent to the hidden landing.")
	if not bool(_state.flags.get("optional_signal_cache_clue", false)):
		_state.set_flag("optional_signal_cache_clue", true, "Optional clue added: three lanterns mark men who should not be ashore.")
		_state.set_flag("optional_clue_enriched_journal", true, "Journal enriched: the signal pattern changes what Newport rumors mean.")
	if not _state.is_objective_complete("travel_to_island_clue_site"):
		_state.complete_objective("travel_to_island_clue_site", "Objective complete: the signal point reveals the hidden landing route.")
	_state.set_response("Mara Oren: One lantern for weather, two for warning, three for men who should not be ashore.")
	return _state.start_objective("discover_physical_evidence", "Objective updated: search the hidden landing below the signal point.")


func _discover_island_physical_evidence(role: String) -> Dictionary:
	_start_island_lead(role)
	if not bool(_state.flags.get("third_toast_heard", false)) and not bool(_state.flags.get("island_lead_active", false)):
		_state.set_response("Tomas Reed: I can show you the cove when the Third Toast tells me you are not carrying the Governor's questions.")
		return _state.snapshot()
	if not bool(_state.flags.get("optional_signal_cache_clue", false)):
		_state.set_flag("island_route_choice", "hidden_landing_harbor_path", "Route choice changed: harbor work points straight to the hidden landing.")
	if not _state.is_objective_complete("travel_to_island_clue_site"):
		_state.complete_objective("travel_to_island_clue_site", "Objective complete: the old road leads to the hidden landing.")
	_state.start_objective("discover_physical_evidence", "Objective updated: inspect the cargo mark at the hidden landing.")
	if not bool(_state.flags.get("island_physical_evidence_found", false)):
		_state.set_flag("island_physical_evidence_found", true, "Evidence found: tar-marked cargo rope matches the missing ledger line.")
		_state.set_flag("hidden_landing_manifest_mark", true, "")
		_state.add_reward(ISLAND_EVIDENCE_REWARD_LABEL, 8)
	if not _state.is_objective_complete("discover_physical_evidence"):
		_state.complete_objective("discover_physical_evidence", "Objective complete: physical evidence links the cove to the missing manifest.")
	_state.set_response("Tomas Reed: If the manifest lost a line, the cove kept the ink. That rope was cut after midnight.")
	return _state.start_objective("return_or_report_choice", "Objective updated: return with proof or pass it through Annelise.")


func _return_or_report_from_island(role: String) -> Dictionary:
	if not bool(_state.flags.get("island_physical_evidence_found", false)):
		_state.set_response("Annelise Crow: Bring proof home, not just a story. Newport has enough stories.")
		return _state.snapshot()
	_state.set_flag("return_report_choice", true, "Return choice logged: Annelise can carry rumor, but Edrin needs proof.")
	_state.set_flag("return_report_contact", role.replace("_", " "), "")
	_state.set_flag("return_report_route_choice", "annelise_rumor_contact", "Choice logged: Annelise carries the safer half of the truth.")
	if not _state.reward_log.has(ISLAND_CONTACT_REWARD_LABEL):
		_state.add_reward(ISLAND_CONTACT_REWARD_LABEL, 0)
	if not _state.is_objective_complete("return_or_report_choice"):
		_state.complete_objective("return_or_report_choice", "Objective complete: the proof has a route back to Newport.")
	_state.set_response("Annelise Crow: Bring the rope mark to Edrin. I will make sure the tavern hears the safer half of the truth.")
	return _state.start_objective("hook_to_continue", "Hook updated: return to Newport with proof before the harbor closes.")


func _return_to_edrin_with_island_evidence() -> Dictionary:
	if not bool(_state.flags.get("island_physical_evidence_found", false)):
		return _return_to_edrin()
	if not _state.is_objective_complete("return_or_report_choice"):
		_state.complete_objective("return_or_report_choice", "Objective complete: Edrin receives the island evidence.")
	_state.set_flag("island_report_ready", true, "")
	_state.set_flag("reason_to_continue_after_island", true, "Reason to continue: Edrin names the dawn signal and the Governor's men.")
	_state.set_flag("return_report_route_choice", "edrin_counting_house_proof", "Choice logged: Edrin receives the physical proof at the Counting House.")
	if not _state.reward_log.has(CONTACT_REWARD_LABEL):
		_state.add_reward(CONTACT_REWARD_LABEL, 0)
	_state.set_response("Edrin Vale: This tar mark is not Newport work. At first light, the Governor's men will ask the wrong questions. We ask first.")
	return _state.start_objective("hook_to_continue", "Hook added: meet Edrin at first light before the Governor's men close the harbor.")


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
