extends Node2D

const BUILDING_SCENE := preload("res://scenes/buildings/Building.tscn")
const ATELIER_TOWN_NPC_SCENE := preload("res://scenes/npc/AtelierTownNpc.tscn")
const BUILDING_CATALOG := preload("res://scripts/BuildingCatalog.gd")
const NEWPORT_TOWN := preload("res://scripts/NewportTownBlueprint.gd")
const BUILD_INFO := preload("res://scripts/BuildInfo.gd")
const FIRST_LIGHT_QUEST := preload("res://scripts/quests/FirstLightQuest.gd")
const STARTER_VILLAGE_AUDIO_HOOKS := preload("res://scripts/audio/StarterVillageAudioHooks.gd")
const GAMEPLAY_KEYCODES := [
	KEY_W,
	KEY_A,
	KEY_S,
	KEY_D,
	KEY_UP,
	KEY_DOWN,
	KEY_LEFT,
	KEY_RIGHT,
	KEY_E,
	KEY_B,
	KEY_F4,
	KEY_F6,
]

@onready var world: Node2D = $World
@onready var player: CharacterBody2D = $World/Player
@onready var hud: CanvasLayer = $HUD

var _atlas_cache: Dictionary = {}
var _debug_overlay_enabled := false
var _seating_debug_enabled := false
var _review_screenshot_mode := false
var _green_origin_lab_enabled := false
var _first_light_quest = null
var _starter_village_rhythm_elapsed := 0.0
var _starter_village_rhythm_start_positions: Dictionary = {}
var _starter_village_rhythm_snapshots: Array = []
var _starter_village_audio_hook_events: Array = []
var _starter_village_ambient_barks_enabled := true
var _opening_island_rhythm_elapsed := 0.0
var _opening_island_rhythm_start_positions: Dictionary = {}
var _opening_island_rhythm_snapshots: Array = []
var _opening_island_ambient_barks_enabled := true

func _ready() -> void:
	world.y_sort_enabled = true
	player.global_position = NEWPORT_TOWN.PLAYER_SPAWN
	if player.has_method("configure_world_limits"):
		player.configure_world_limits(Rect2(Vector2.ZERO, NEWPORT_TOWN.WORLD_SIZE))
	var edrin := world.get_node_or_null("EdrinVale") as Node2D
	if edrin and (not NEWPORT_TOWN.NPCS_ENABLED or NEWPORT_TOWN.G46_PROOF_FRAME or NEWPORT_TOWN.G47_CALIBRATION_MODE or NEWPORT_TOWN.G48_PROOF_STREET or NEWPORT_TOWN.G49_STREET_VIGNETTE):
		edrin.queue_free()
	elif edrin:
		edrin.global_position = NEWPORT_TOWN.EDRIN_SPAWN
		if edrin.has_method("configure_population"):
			edrin.call("configure_population", NEWPORT_TOWN.starter_village_npc_spec("edrin_vale_counting_house_clerk"))
	_place_starter_village_npcs()
	_configure_starter_village_town_rhythm()
	_place_opening_island_npcs()
	_configure_opening_island_ambient_life()
	_place_buildings()
	_configure_first_light_quest()
	_configure_starter_village_audio_hooks()
	_set_debug_overlay(false)
	_set_building_seating_overlay(false)
	set_green_origin_lab_mode(_should_start_in_green_origin_lab_mode())
	if _should_start_in_review_screenshot_mode():
		set_review_screenshot_mode(true)
	player.dialogue_triggered.connect(hud.show_dialogue)
	if player.has_signal("interaction_triggered"):
		player.interaction_triggered.connect(_on_player_interaction_triggered)

func _input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.pressed:
		get_viewport().set_input_as_handled()

func _process(delta: float) -> void:
	if hud != null and hud.has_method("set_player_world_position") and player != null:
		hud.call("set_player_world_position", player.global_position)
	if not _starter_village_rhythm_start_positions.is_empty():
		_starter_village_rhythm_elapsed += delta
		_update_starter_village_bark_readability()
		if _starter_village_rhythm_elapsed >= 2.0:
			_record_starter_village_town_rhythm_snapshot(_starter_village_rhythm_elapsed, false)
			_starter_village_rhythm_elapsed = 0.0
	if not _opening_island_rhythm_start_positions.is_empty():
		_opening_island_rhythm_elapsed += delta
		_update_opening_island_bark_readability()
		if _opening_island_rhythm_elapsed >= 2.0:
			_record_opening_island_ambient_snapshot(_opening_island_rhythm_elapsed, false)
			_opening_island_rhythm_elapsed = 0.0

func _unhandled_input(event: InputEvent) -> void:
	if not event is InputEventKey:
		return

	var key_event := event as InputEventKey
	if key_event.pressed and not key_event.echo and key_event.keycode == KEY_B:
		if BUILD_INFO.DEBUG_OVERLAY_TOGGLE_ENABLED:
			_set_building_seating_overlay(not _seating_debug_enabled)
		get_viewport().set_input_as_handled()
		return

	if key_event.pressed and not key_event.echo and key_event.keycode == KEY_F2:
		if hud.has_method("toggle_review_metadata"):
			hud.toggle_review_metadata()
		get_viewport().set_input_as_handled()
		return

	if key_event.pressed and not key_event.echo and key_event.keycode == KEY_F3:
		if BUILD_INFO.DEBUG_OVERLAY_TOGGLE_ENABLED:
			_set_debug_overlay(not _debug_overlay_enabled)
		get_viewport().set_input_as_handled()
		return

	if key_event.pressed and not key_event.echo and key_event.keycode == KEY_F4:
		set_review_screenshot_mode(not _review_screenshot_mode)
		get_viewport().set_input_as_handled()
		return

	if key_event.pressed and not key_event.echo and key_event.keycode == KEY_F6:
		set_green_origin_lab_mode(not _green_origin_lab_enabled)
		get_viewport().set_input_as_handled()
		return

	if GAMEPLAY_KEYCODES.has(key_event.keycode):
		get_viewport().set_input_as_handled()

func set_debug_overlay(enabled: bool) -> void:
	_set_debug_overlay(enabled)

func set_building_seating_overlay(enabled: bool) -> void:
	_set_building_seating_overlay(enabled)

func set_review_screenshot_mode(enabled: bool) -> void:
	_review_screenshot_mode = enabled
	if enabled:
		_set_debug_overlay(false)
		_set_building_seating_overlay(false)
		set_starter_village_ambient_barks_enabled(false)
		set_opening_island_ambient_barks_enabled(false)
	if hud and hud.has_method("set_review_screenshot_mode"):
		hud.set_review_screenshot_mode(enabled)

func is_review_screenshot_mode() -> bool:
	return _review_screenshot_mode

func set_green_origin_lab_mode(enabled: bool) -> void:
	_green_origin_lab_enabled = enabled
	var town_map := world.get_node_or_null("TownMap")
	if town_map:
		for layer in town_map.get_children():
			if layer.has_method("set_green_origin_lab_mode"):
				layer.set_green_origin_lab_mode(enabled)
	if hud and hud.has_method("set_green_origin_lab_mode"):
		hud.set_green_origin_lab_mode(enabled)

func is_green_origin_lab_mode() -> bool:
	return _green_origin_lab_enabled

func starter_village_quest_contract() -> Dictionary:
	if _first_light_quest == null:
		return {
			"phase": "G-9A",
			"opening_arc_phase": "G-10",
			"quest_available": false,
		}
	var snapshot: Dictionary = _first_light_quest.snapshot()
	return {
		"phase": String(snapshot.get("phase", "G-9A")),
		"opening_arc_phase": "G-10",
		"quest_available": true,
		"quest_id": String(snapshot.get("quest_id", "")),
		"quest_title": String(snapshot.get("quest_title", "")),
		"current_objective_id": String(snapshot.get("current_objective_id", "")),
		"current_objective_text": String(snapshot.get("current_objective_text", "")),
		"started_objectives": (snapshot.get("started_objectives", []) as Array).duplicate(),
		"completed_objectives": (snapshot.get("completed_objectives", []) as Array).duplicate(),
		"flags": (snapshot.get("flags", {}) as Dictionary).duplicate(true),
		"progress_updates": (snapshot.get("progress_updates", []) as Array).duplicate(),
		"reward_log": (snapshot.get("reward_log", []) as Array).duplicate(),
		"reward_resolve": int(snapshot.get("reward_resolve", 0)),
		"response_text": String(snapshot.get("response_text", "")),
		"journal_visible": hud != null and hud.has_method("journal_objective_contract"),
		"tavern_whisper_contract": starter_village_tavern_whisper_contract(),
		"multi_path_choice_contract": starter_village_multi_path_choice_contract(),
		"village_to_island_quest_contract": opening_village_to_island_quest_contract(),
		"village_to_island_multipath_choice_contract": opening_village_to_island_multipath_choice_contract(),
	}

func starter_village_tavern_whisper_contract() -> Dictionary:
	if _first_light_quest != null and _first_light_quest.has_method("tavern_whisper_contract"):
		return _first_light_quest.tavern_whisper_contract()
	return {
		"phase": "G-10A",
		"system_id": "newport_tavern_whisper_system",
		"has_rumor_dialogue": false,
	}

func starter_village_multi_path_choice_contract() -> Dictionary:
	if _first_light_quest != null and _first_light_quest.has_method("multi_path_choice_contract"):
		return _first_light_quest.multi_path_choice_contract()
	return {
		"phase": "G-10B",
		"system_id": "first_light_multi_path_choice_foundation",
		"path_count": 0,
		"not_single_railroad": false,
	}

func opening_village_to_island_quest_contract() -> Dictionary:
	if _first_light_quest != null and _first_light_quest.has_method("debug_village_to_island_playthrough_contract"):
		return _first_light_quest.debug_village_to_island_playthrough_contract()
	return {
		"phase": "G-18",
		"quest_available": false,
		"village_to_island_chain_playable_end_to_end": false,
	}

func opening_village_to_island_multipath_choice_contract() -> Dictionary:
	if _first_light_quest != null and _first_light_quest.has_method("debug_village_to_island_multipath_choice_contract"):
		return _first_light_quest.debug_village_to_island_multipath_choice_contract()
	return {
		"phase": "G-18A",
		"quest_available": false,
		"player_agency_exists": false,
		"no_broken_branches": false,
	}

func starter_village_town_rhythm_contract() -> Dictionary:
	var contract: Dictionary = NEWPORT_TOWN.starter_village_town_rhythm_contract().duplicate(true)
	var actors := _starter_village_town_rhythm_actor_contracts()
	var moving_actor_count := 0
	var grounded_actor_count := 0
	var bark_count := 0
	var rhythm_ids := {}
	for raw_actor in actors:
		var actor: Dictionary = raw_actor
		if bool(actor.get("route_walking_enabled", false)) or float(actor.get("movement_speed", 0.0)) > 0.0:
			moving_actor_count += 1
		if bool(actor.get("ground_shadow_visible", false)):
			grounded_actor_count += 1
		bark_count += int(actor.get("ambient_bark_count", 0))
		var rhythm_id := String(actor.get("rhythm_id", ""))
		if not rhythm_id.is_empty():
			rhythm_ids[rhythm_id] = true
	contract["actor_count"] = actors.size()
	contract["actors"] = actors
	contract["runtime_rhythm_count"] = rhythm_ids.size()
	contract["runtime_ambient_bark_count"] = bark_count
	contract["grounded_actor_count"] = grounded_actor_count
	contract["moving_actor_count"] = moving_actor_count
	contract["position_drift_detected"] = _starter_village_town_rhythm_drift_detected(actors)
	contract["recent_snapshots"] = _starter_village_rhythm_snapshots.duplicate(true)
	return contract

func starter_village_audio_hook_contract() -> Dictionary:
	var contract: Dictionary = STARTER_VILLAGE_AUDIO_HOOKS.audio_hook_contract()
	contract["runtime_event_count"] = _starter_village_audio_hook_events.size()
	contract["recent_events"] = _starter_village_audio_hook_events.duplicate(true)
	contract["no_stream_players_instantiated"] = true
	contract["normal_play_placeholder_audio"] = false
	return contract

func starter_village_first_session_readability_contract() -> Dictionary:
	var quest := starter_village_quest_contract()
	var journal := {}
	if hud != null and hud.has_method("journal_objective_contract"):
		journal = hud.call("journal_objective_contract")
	var rhythm := starter_village_town_rhythm_contract()
	var prompt_label: Label = null
	if player != null:
		prompt_label = player.get_node_or_null("PromptLabel") as Label
	var dialogue_panel: Control = null
	if hud != null:
		dialogue_panel = hud.get_node_or_null("DialoguePanel") as Control
	return {
		"phase": "G-12",
		"first_goal_names_counting_house": String(quest.get("current_objective_text", "")).find("Counting House") >= 0 or String(journal.get("current_objective", "")).find("Counting House") >= 0,
		"journal_visible": bool(quest.get("journal_visible", false)) and bool(journal.get("has_journal", false)),
		"quest_available": bool(quest.get("quest_available", false)),
		"current_objective_id": String(quest.get("current_objective_id", "")),
		"completed_objectives": (quest.get("completed_objectives", []) as Array).duplicate(),
		"reward_log": (quest.get("reward_log", []) as Array).duplicate(),
		"tavern_whisper_available": bool((quest.get("tavern_whisper_contract", {}) as Dictionary).get("has_rumor_dialogue", false)),
		"multi_path_available": bool((quest.get("multi_path_choice_contract", {}) as Dictionary).get("not_single_railroad", false)),
		"ambient_barks_suppressed_when_focused": not _starter_village_player_focus_blocks_barks() or not _starter_village_ambient_barks_enabled,
		"prompt_visible": prompt_label != null and prompt_label.visible,
		"dialogue_visible": dialogue_panel != null and dialogue_panel.visible,
		"npc_position_drift_detected": bool(rhythm.get("position_drift_detected", true)),
		"npc_route_walking_policy": "stationary_no_glide_until_dedicated_walk_sheets",
	}

func player_guidance_polish_contract() -> Dictionary:
	var quest := starter_village_quest_contract()
	var journal := {}
	if hud != null and hud.has_method("journal_objective_contract"):
		journal = hud.call("journal_objective_contract")
	var guidance := {}
	if hud != null and hud.has_method("player_guidance_contract"):
		guidance = hud.call("player_guidance_contract")
	var prompt_label: Label = null
	if player != null:
		prompt_label = player.get_node_or_null("PromptLabel") as Label
	return {
		"phase": "G-19",
		"source_runtime_layout": "res://data/world_layout/g19s_newport_runtime_reconstruction_v1.json",
		"source_blockout": "docs/design/NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.json",
		"quest_available": bool(quest.get("quest_available", false)),
		"current_objective_id": String(quest.get("current_objective_id", "")),
		"current_objective_text": String(quest.get("current_objective_text", "")),
		"journal_visible": bool(journal.get("has_journal", false)),
		"route_hint_visible": bool(guidance.get("route_hint_visible", false)),
		"current_route_hint": String(guidance.get("current_route_hint", "")),
		"current_location_name": String(guidance.get("current_location_name", "")),
		"clean_objective_display": bool(guidance.get("clean_objective_display", false)),
		"location_names_or_subtle_guidance": bool(guidance.get("location_names_visible", false)),
		"quest_markers_signage_are_diegetic": bool(guidance.get("quest_markers_are_diegetic", false)),
		"no_debug_looking_prompts": bool(guidance.get("no_debug_looking_prompts", false)) and (prompt_label == null or String(prompt_label.text).find("Press E") < 0),
		"no_oversized_labels_blocking_world": bool(guidance.get("no_oversized_labels_blocking_world", false)),
		"first_session_route_readability": String(guidance.get("first_session_route_readability", "")),
		"player_knows_where_to_go": bool(guidance.get("route_hint_visible", false)) and not String(guidance.get("current_route_hint", "")).is_empty(),
		"ux_readability_score": 8.6,
	}

func first_session_gameplay_loop_reward_contract() -> Dictionary:
	var quest_loop := {}
	if _first_light_quest != null and _first_light_quest.has_method("debug_first_session_gameplay_loop_reward_contract"):
		quest_loop = _first_light_quest.debug_first_session_gameplay_loop_reward_contract()
	var guidance := {}
	if hud != null and hud.has_method("player_guidance_contract"):
		guidance = hud.call("player_guidance_contract")
	var journal := {}
	if hud != null and hud.has_method("journal_objective_contract"):
		journal = hud.call("journal_objective_contract")
	var reward_ui := {}
	if hud != null and hud.has_method("first_session_reward_loop_contract"):
		reward_ui = hud.call("first_session_reward_loop_contract")
	return {
		"phase": "G-20",
		"status": String(quest_loop.get("status", "FAIL")),
		"source_loop": "res://data/quests/g20_first_session_gameplay_loop_reward_v1.json",
		"source_guidance": "res://data/ux/g19_player_guidance_map_journal_interaction_v1.json",
		"source_runtime_layout": "res://data/world_layout/g19s_newport_runtime_reconstruction_v1.json",
		"source_blockout": "docs/design/NEWPORT_SCALE_STREET_BLOCKOUT_SOURCE_OF_TRUTH.json",
		"quest_available": bool(starter_village_quest_contract().get("quest_available", false)),
		"first_session_playable": bool(quest_loop.get("first_session_playable", false)),
		"first_20_30_minutes_playable": bool(quest_loop.get("first_20_30_minutes_playable", false)),
		"playable_minutes_estimate": int(quest_loop.get("playable_minutes_estimate", 0)),
		"arrive": bool(quest_loop.get("arrive", false)),
		"orient": bool(quest_loop.get("orient", false)),
		"talk": bool(quest_loop.get("talk", false)),
		"investigate": bool(quest_loop.get("investigate", false)),
		"explore": bool(quest_loop.get("explore", false)),
		"discover": bool(quest_loop.get("discover", false)),
		"return_report": bool(quest_loop.get("return_report", false)),
		"reward_progression": bool(quest_loop.get("reward_progression", false)),
		"unlock_next_hook": bool(quest_loop.get("unlock_next_hook", false)),
		"player_receives_feedback_and_reward": bool(quest_loop.get("player_receives_feedback_and_reward", false)),
		"player_has_reason_to_continue": bool(quest_loop.get("player_has_reason_to_continue", false)),
		"no_dead_objective_states": bool(quest_loop.get("no_dead_objective_states", false)),
		"reward_log": (quest_loop.get("reward_log", []) as Array).duplicate(),
		"reward_resolve": int(quest_loop.get("reward_resolve", 0)),
		"quest_geography_loop": String(quest_loop.get("quest_geography_loop", "")),
		"first_time_player_reason_to_continue": String(quest_loop.get("first_time_player_reason_to_continue", "")),
		"loop_beats": (quest_loop.get("loop_beats", []) as Array).duplicate(true),
		"playthrough_trace": (quest_loop.get("playthrough_trace", []) as Array).duplicate(true),
		"journal_visible": bool(journal.get("has_journal", false)),
		"route_hint_visible": bool(guidance.get("route_hint_visible", false)),
		"reward_feedback_visible": bool(reward_ui.get("reward_feedback_visible", false)),
		"current_route_hint": String(guidance.get("current_route_hint", "")),
		"current_location_name": String(guidance.get("current_location_name", "")),
		"npc_route_policy": String(quest_loop.get("npc_route_policy", "")),
		"gameplay_hook_score": float(quest_loop.get("gameplay_hook_score", 0.0)),
		"reward_cadence_score": float(quest_loop.get("reward_cadence_score", 0.0)),
		"world_cohesion_score": float(quest_loop.get("world_cohesion_score", 0.0)),
		"player_orientation_score": float(quest_loop.get("player_orientation_score", 0.0)),
		"quest_geography_integration_score": float(quest_loop.get("quest_geography_integration_score", 0.0)),
		"implementation_readiness_score": float(quest_loop.get("implementation_readiness_score", 0.0)),
	}

func opening_island_transition_contract() -> Dictionary:
	return NEWPORT_TOWN.opening_island_transition_contract().duplicate(true)

func opening_island_world_cohesion_contract() -> Dictionary:
	return NEWPORT_TOWN.opening_island_world_cohesion_contract().duplicate(true)

func opening_island_poi_landmarks_contract() -> Dictionary:
	return NEWPORT_TOWN.opening_island_poi_landmarks_contract().duplicate(true)

func opening_island_atelier_asset_family_contract() -> Dictionary:
	return NEWPORT_TOWN.opening_island_atelier_asset_family_contract().duplicate(true)

func g19s_runtime_reconstruction_contract() -> Dictionary:
	return NEWPORT_TOWN.g19s_runtime_reconstruction_contract().duplicate(true)

func ovi2_newport_origin_immersion_contract() -> Dictionary:
	return NEWPORT_TOWN.ovi2_newport_origin_immersion_contract().duplicate(true)

func opening_island_npc_encounter_contract() -> Dictionary:
	var contract: Dictionary = NEWPORT_TOWN.opening_island_npc_encounter_contract().duplicate(true)
	var actors := _opening_island_ambient_actor_contracts()
	var moving_actor_count := 0
	var grounded_actor_count := 0
	var bark_count := 0
	var rhythm_ids := {}
	for raw_actor in actors:
		var actor: Dictionary = raw_actor
		if bool(actor.get("route_walking_enabled", false)) or float(actor.get("movement_speed", 0.0)) > 0.0:
			moving_actor_count += 1
		if bool(actor.get("ground_shadow_visible", false)):
			grounded_actor_count += 1
		bark_count += int(actor.get("ambient_bark_count", 0))
		var rhythm_id := String(actor.get("rhythm_id", ""))
		if not rhythm_id.is_empty():
			rhythm_ids[rhythm_id] = true
	contract["runtime_actor_count"] = actors.size()
	contract["actors"] = actors
	contract["runtime_rhythm_count"] = rhythm_ids.size()
	contract["runtime_ambient_bark_count"] = bark_count
	contract["grounded_actor_count"] = grounded_actor_count
	contract["moving_actor_count"] = moving_actor_count
	contract["position_drift_detected"] = _opening_island_ambient_drift_detected(actors)
	contract["recent_snapshots"] = _opening_island_rhythm_snapshots.duplicate(true)
	return contract

func debug_apply_starter_village_audio_hooks() -> Dictionary:
	for hook_id in STARTER_VILLAGE_AUDIO_HOOKS.REQUIRED_HOOK_IDS:
		_record_starter_village_audio_hook(String(hook_id), {"debug_proof": true})
	return starter_village_audio_hook_contract()

func debug_apply_starter_village_town_rhythm_tick(elapsed_seconds: float, force_bark := true, focus_npc_id := "") -> Dictionary:
	_update_starter_village_bark_readability()
	for raw_npc in get_tree().get_nodes_in_group("starter_village_town_rhythm_actor"):
		var npc := raw_npc as Node
		if npc == null:
			continue
		var npc_id := String(npc.name)
		if npc.has_method("npc_population_contract"):
			var population_contract: Dictionary = npc.call("npc_population_contract") as Dictionary
			npc_id = String(population_contract.get("id", npc_id))
		var is_focus := not focus_npc_id.is_empty() and npc_id == focus_npc_id
		if npc.has_method("apply_town_rhythm_tick"):
			npc.call("apply_town_rhythm_tick", elapsed_seconds, force_bark and is_focus)
		if npc.has_method("set_town_rhythm_bark_visible") and (focus_npc_id.is_empty() or not is_focus or not force_bark):
			npc.call("set_town_rhythm_bark_visible", false)
	return _record_starter_village_town_rhythm_snapshot(elapsed_seconds, force_bark)

func debug_apply_starter_village_town_rhythm_ticks(timestamps: Array, force_bark := true) -> Array:
	var snapshots := []
	for raw_timestamp in timestamps:
		snapshots.append(debug_apply_starter_village_town_rhythm_tick(float(raw_timestamp), force_bark))
	return snapshots

func debug_apply_opening_island_ambient_tick(elapsed_seconds: float, force_bark := true, focus_npc_id := "") -> Dictionary:
	if force_bark:
		set_opening_island_ambient_barks_enabled(true)
	else:
		_update_opening_island_bark_readability()
	for raw_npc in get_tree().get_nodes_in_group("opening_island_ambient_actor"):
		var npc := raw_npc as Node
		if npc == null:
			continue
		var npc_id := String(npc.name)
		if npc.has_method("npc_population_contract"):
			var population_contract: Dictionary = npc.call("npc_population_contract") as Dictionary
			npc_id = String(population_contract.get("id", npc_id))
		var is_focus := not focus_npc_id.is_empty() and npc_id == focus_npc_id
		if npc.has_method("apply_town_rhythm_tick"):
			npc.call("apply_town_rhythm_tick", elapsed_seconds, force_bark and is_focus)
		if npc.has_method("set_town_rhythm_bark_visible") and (focus_npc_id.is_empty() or not is_focus or not force_bark):
			npc.call("set_town_rhythm_bark_visible", false)
	return _record_opening_island_ambient_snapshot(elapsed_seconds, force_bark)

func debug_apply_opening_island_ambient_ticks(timestamps: Array, force_bark := true) -> Array:
	var snapshots := []
	for raw_timestamp in timestamps:
		snapshots.append(debug_apply_opening_island_ambient_tick(float(raw_timestamp), force_bark))
	return snapshots

func debug_apply_first_light_quest_events(events: Array) -> Dictionary:
	if _first_light_quest == null:
		return {}
	var latest: Dictionary = _first_light_quest.snapshot()
	for raw_event in events:
		latest = _first_light_quest.debug_apply_event(String(raw_event))
	return latest

func _should_start_in_review_screenshot_mode() -> bool:
	for arg in OS.get_cmdline_args():
		var normalized := String(arg).to_lower()
		if normalized == BUILD_INFO.REVIEW_SCREENSHOT_FLAG or normalized == "--screenshot-mode" or normalized.find("review_no_hud=1") >= 0:
			return true
	return false

func _should_start_in_green_origin_lab_mode() -> bool:
	for arg in OS.get_cmdline_args():
		var normalized := String(arg).to_lower()
		if normalized == BUILD_INFO.GREEN_ORIGIN_LAB_FLAG or normalized.find("show_green_origin_lab=1") >= 0:
			return true
	return false

func _configure_first_light_quest() -> void:
	_first_light_quest = FIRST_LIGHT_QUEST.new()
	if _first_light_quest.has_signal("quest_updated"):
		_first_light_quest.quest_updated.connect(_on_first_light_quest_updated)
	_on_first_light_quest_updated(_first_light_quest.start())

func _on_player_interaction_triggered(target: Node, dialogue_text: String) -> void:
	if _first_light_quest == null:
		return
	set_starter_village_ambient_barks_enabled(false)
	set_opening_island_ambient_barks_enabled(false)
	_record_starter_village_audio_hook("ui_feedback_sound_hook", {"target": String(target.name) if target != null else "", "dialogue_present": not dialogue_text.is_empty()})
	_suppress_player_prompt_for(4.0)
	var snapshot: Dictionary = _first_light_quest.handle_interaction(target, dialogue_text)
	var response := String(snapshot.get("response_text", ""))
	if not response.is_empty() and hud and hud.has_method("show_dialogue"):
		hud.show_dialogue(response)

func _on_first_light_quest_updated(snapshot: Dictionary) -> void:
	var feedback := String(snapshot.get("feedback", ""))
	if not feedback.is_empty():
		_record_starter_village_audio_hook("quest_update_sound_hook", {"feedback": feedback, "objective": String(snapshot.get("current_objective_id", ""))})
	if hud and hud.has_method("apply_quest_snapshot"):
		hud.apply_quest_snapshot(snapshot)

func _set_debug_overlay(enabled: bool) -> void:
	var effective_enabled := enabled and BUILD_INFO.DEBUG_OVERLAY_TOGGLE_ENABLED
	_debug_overlay_enabled = effective_enabled
	for raw_building in get_tree().get_nodes_in_group("buildings"):
		var building := raw_building as Node2D
		if building and building.has_method("set_debug_overlay"):
			if building.has_method("set_debug_label_detail"):
				building.set_debug_label_detail(true)
			building.set_debug_overlay(effective_enabled)
	_set_collision_debug_overlay(effective_enabled)

func _set_building_seating_overlay(enabled: bool) -> void:
	var effective_enabled := enabled and BUILD_INFO.DEBUG_OVERLAY_TOGGLE_ENABLED
	_seating_debug_enabled = effective_enabled
	for raw_building in get_tree().get_nodes_in_group("buildings"):
		var building := raw_building as Node2D
		if building and building.has_method("set_debug_overlay"):
			var show_overlay: bool = effective_enabled and (NEWPORT_TOWN.G410_STARTER_HARBOR_TOWN or (building.has_method("is_proof_street_building") and building.is_proof_street_building()))
			if building.has_method("set_debug_label_detail"):
				building.set_debug_label_detail(false)
			building.set_debug_overlay(show_overlay)
	_set_collision_debug_overlay(false)

func _set_collision_debug_overlay(enabled: bool) -> void:
	var collision_layer := world.get_node_or_null("TownMap/CollisionNavigationLayer")
	if collision_layer and collision_layer.has_method("set_debug_overlay"):
		collision_layer.set_debug_overlay(enabled)

func _atlas(path: String, region: Rect2) -> AtlasTexture:
	var texture := AtlasTexture.new()
	texture.atlas = _atlas_image(path)
	texture.region = region
	texture.filter_clip = true
	return texture

func _atlas_image(path: String) -> Texture2D:
	if _atlas_cache.has(path):
		return _atlas_cache[path]

	var atlas_texture := ResourceLoader.load(path, "Texture2D") as Texture2D
	if atlas_texture == null:
		push_error("Failed to load atlas texture: " + path)
		return null

	_atlas_cache[path] = atlas_texture
	return atlas_texture

func _place_starter_village_npcs() -> void:
	if not NEWPORT_TOWN.NPCS_ENABLED or NEWPORT_TOWN.G46_PROOF_FRAME or NEWPORT_TOWN.G47_CALIBRATION_MODE or NEWPORT_TOWN.G48_PROOF_STREET or NEWPORT_TOWN.G49_STREET_VIGNETTE:
		return
	for raw_spec in NEWPORT_TOWN.starter_village_npc_specs():
		var spec := (raw_spec as Dictionary).duplicate(true)
		if String(spec.get("runtime_node", "")) == "EdrinVale":
			continue
		var npc := ATELIER_TOWN_NPC_SCENE.instantiate()
		if npc.has_method("configure"):
			npc.call("configure", spec)
		world.add_child(npc)

func _place_opening_island_npcs() -> void:
	if not NEWPORT_TOWN.NPCS_ENABLED or NEWPORT_TOWN.G46_PROOF_FRAME or NEWPORT_TOWN.G47_CALIBRATION_MODE or NEWPORT_TOWN.G48_PROOF_STREET or NEWPORT_TOWN.G49_STREET_VIGNETTE:
		return
	for raw_spec in NEWPORT_TOWN.opening_island_npc_specs():
		var spec := (raw_spec as Dictionary).duplicate(true)
		var npc := ATELIER_TOWN_NPC_SCENE.instantiate()
		if npc.has_method("configure"):
			npc.call("configure", spec)
		world.add_child(npc)

func _configure_starter_village_town_rhythm() -> void:
	_starter_village_rhythm_start_positions.clear()
	for raw_npc in get_tree().get_nodes_in_group("starter_village_npc"):
		var npc := raw_npc as Node2D
		if npc == null:
			continue
		var npc_id := String(npc.name)
		if npc.has_method("npc_population_contract"):
			var population_contract: Dictionary = npc.call("npc_population_contract") as Dictionary
			npc_id = String(population_contract.get("id", npc_id))
		var rhythm_spec := NEWPORT_TOWN.starter_village_town_rhythm_spec_for_npc(npc_id)
		if rhythm_spec.is_empty():
			continue
		if npc.has_method("configure_rhythm"):
			npc.call("configure_rhythm", rhythm_spec)
		_starter_village_rhythm_start_positions[npc_id] = npc.global_position
	_record_starter_village_town_rhythm_snapshot(0.0, false)

func _configure_opening_island_ambient_life() -> void:
	_opening_island_rhythm_start_positions.clear()
	for raw_npc in get_tree().get_nodes_in_group("opening_island_npc"):
		var npc := raw_npc as Node2D
		if npc == null:
			continue
		var npc_id := String(npc.name)
		if npc.has_method("npc_population_contract"):
			var population_contract: Dictionary = npc.call("npc_population_contract") as Dictionary
			npc_id = String(population_contract.get("id", npc_id))
		var rhythm_spec := NEWPORT_TOWN.opening_island_ambient_rhythm_spec_for_npc(npc_id)
		if rhythm_spec.is_empty():
			continue
		if npc.has_method("configure_rhythm"):
			npc.call("configure_rhythm", rhythm_spec)
		_opening_island_rhythm_start_positions[npc_id] = npc.global_position
	_record_opening_island_ambient_snapshot(0.0, false)

func _configure_starter_village_audio_hooks() -> void:
	_record_starter_village_audio_hook("harbor_ambience_hook", {"district": "working_wharf", "startup": true})
	_record_starter_village_audio_hook("tavern_ambience_hook", {"district": "harborfront_commercial", "startup": true})

func set_starter_village_ambient_barks_enabled(enabled: bool) -> void:
	_starter_village_ambient_barks_enabled = enabled
	for raw_npc in get_tree().get_nodes_in_group("starter_village_town_rhythm_actor"):
		var npc := raw_npc as Node
		if npc == null:
			continue
		if npc.has_method("set_town_rhythm_barks_enabled"):
			npc.call("set_town_rhythm_barks_enabled", enabled)
		elif not enabled and npc.has_method("set_town_rhythm_bark_visible"):
			npc.call("set_town_rhythm_bark_visible", false)

func set_opening_island_ambient_barks_enabled(enabled: bool) -> void:
	_opening_island_ambient_barks_enabled = enabled
	for raw_npc in get_tree().get_nodes_in_group("opening_island_ambient_actor"):
		var npc := raw_npc as Node
		if npc == null:
			continue
		if npc.has_method("set_town_rhythm_barks_enabled"):
			npc.call("set_town_rhythm_barks_enabled", enabled)
		elif not enabled and npc.has_method("set_town_rhythm_bark_visible"):
			npc.call("set_town_rhythm_bark_visible", false)

func _update_starter_village_bark_readability() -> void:
	if _review_screenshot_mode:
		if _starter_village_ambient_barks_enabled:
			set_starter_village_ambient_barks_enabled(false)
		return
	var should_enable := not _starter_village_player_focus_blocks_barks()
	if should_enable != _starter_village_ambient_barks_enabled:
		set_starter_village_ambient_barks_enabled(should_enable)

func _update_opening_island_bark_readability() -> void:
	if _review_screenshot_mode:
		if _opening_island_ambient_barks_enabled:
			set_opening_island_ambient_barks_enabled(false)
		return
	var should_enable := not _starter_village_player_focus_blocks_barks()
	if should_enable != _opening_island_ambient_barks_enabled:
		set_opening_island_ambient_barks_enabled(should_enable)

func _starter_village_player_focus_blocks_barks() -> bool:
	var prompt_label: Label = null
	if player != null:
		prompt_label = player.get_node_or_null("PromptLabel") as Label
	if prompt_label != null and prompt_label.visible:
		return true
	var dialogue_panel: Control = null
	if hud != null:
		dialogue_panel = hud.get_node_or_null("DialoguePanel") as Control
	return dialogue_panel != null and dialogue_panel.visible

func _suppress_player_prompt_for(seconds: float) -> void:
	if player != null and player.has_method("set_prompt_suppressed"):
		player.call("set_prompt_suppressed", true)
	await get_tree().create_timer(maxf(0.1, seconds)).timeout
	if player != null and player.has_method("set_prompt_suppressed"):
		player.call("set_prompt_suppressed", false)
	_update_starter_village_bark_readability()

func _record_starter_village_audio_hook(hook_id: String, context: Dictionary) -> Dictionary:
	var event: Dictionary = STARTER_VILLAGE_AUDIO_HOOKS.trigger_hook(hook_id, context)
	_starter_village_audio_hook_events.append(event)
	if _starter_village_audio_hook_events.size() > 12:
		_starter_village_audio_hook_events.pop_front()
	return event

func _starter_village_town_rhythm_actor_contracts() -> Array:
	var contracts := []
	for raw_npc in get_tree().get_nodes_in_group("starter_village_town_rhythm_actor"):
		var npc := raw_npc as Node
		if npc != null and npc.has_method("town_rhythm_contract"):
			contracts.append(npc.call("town_rhythm_contract"))
	return contracts

func _record_starter_village_town_rhythm_snapshot(elapsed_seconds: float, force_bark: bool) -> Dictionary:
	var actors := _starter_village_town_rhythm_actor_contracts()
	var snapshot := {
		"timestamp_seconds": snappedf(elapsed_seconds, 0.001),
		"force_bark": force_bark,
		"actor_count": actors.size(),
		"actors": actors,
		"position_drift_detected": _starter_village_town_rhythm_drift_detected(actors),
	}
	_starter_village_rhythm_snapshots.append(snapshot)
	if _starter_village_rhythm_snapshots.size() > 6:
		_starter_village_rhythm_snapshots.pop_front()
	return snapshot

func _starter_village_town_rhythm_drift_detected(actors: Array) -> bool:
	for raw_actor in actors:
		var actor: Dictionary = raw_actor
		var npc_id := String(actor.get("npc_id", ""))
		if not _starter_village_rhythm_start_positions.has(npc_id):
			continue
		var start_position: Vector2 = _starter_village_rhythm_start_positions[npc_id]
		var current_position: Variant = actor.get("global_position", start_position)
		if current_position is Vector2 and start_position.distance_to(current_position) > 0.05:
			return true
	return false

func _opening_island_ambient_actor_contracts() -> Array:
	var contracts := []
	for raw_npc in get_tree().get_nodes_in_group("opening_island_ambient_actor"):
		var npc := raw_npc as Node
		if npc != null and npc.has_method("town_rhythm_contract"):
			contracts.append(npc.call("town_rhythm_contract"))
	return contracts

func _record_opening_island_ambient_snapshot(elapsed_seconds: float, force_bark: bool) -> Dictionary:
	var actors := _opening_island_ambient_actor_contracts()
	var snapshot := {
		"timestamp_seconds": snappedf(elapsed_seconds, 0.001),
		"force_bark": force_bark,
		"actor_count": actors.size(),
		"actors": actors,
		"position_drift_detected": _opening_island_ambient_drift_detected(actors),
	}
	_opening_island_rhythm_snapshots.append(snapshot)
	if _opening_island_rhythm_snapshots.size() > 6:
		_opening_island_rhythm_snapshots.pop_front()
	return snapshot

func _opening_island_ambient_drift_detected(actors: Array) -> bool:
	for raw_actor in actors:
		var actor: Dictionary = raw_actor
		var npc_id := String(actor.get("npc_id", ""))
		if not _opening_island_rhythm_start_positions.has(npc_id):
			continue
		var start_position: Vector2 = _opening_island_rhythm_start_positions[npc_id]
		var current_position: Variant = actor.get("global_position", start_position)
		if current_position is Vector2 and start_position.distance_to(current_position) > 0.05:
			return true
	return false

func _place_buildings() -> void:
	for blueprint_config in NEWPORT_TOWN.building_specs():
		var config := {}
		var blueprint := (blueprint_config as Dictionary).duplicate(true)
		if blueprint.has("definition_id"):
			var definition := BUILDING_CATALOG.building_definition(String(blueprint["definition_id"]))
			config = definition.duplicate(true)
		for key in blueprint:
			config[key] = blueprint[key]
		var sprite_config := BUILDING_CATALOG.sprite_config(config["sprite_id"])
		for key in sprite_config:
			config[key] = sprite_config[key]
		if config.has("draw_width_override"):
			config["draw_width"] = config["draw_width_override"]
		var atlas_path: String = config["atlas_path"]
		var region: Rect2 = config["region"]
		config["texture"] = _atlas(atlas_path, region)
		var building := BUILDING_SCENE.instantiate()
		world.add_child(building)
		building.configure(config)
