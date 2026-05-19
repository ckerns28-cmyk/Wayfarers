extends SceneTree

const MAIN_SCENE := preload("res://scenes/Main.tscn")

const OUT_DIR := "res://artifacts/review/g20_first_session_gameplay_loop"
const MANIFEST_FILENAME := "g20_first_session_screenshot_manifest.json"
const TRACE_FILENAME := "g20_first_session_trace.json"
const PLAYTEST_LOG_FILENAME := "g20_first_session_playtest_log.md"
const VIEWPORT_SIZE := Vector2i(1600, 1000)
const INITIAL_WAIT_FRAMES := 36
const CAPTURE_WAIT_FRAMES := 12

const CAPTURES := [
	{
		"filename": "g20_01_arrival_goal.png",
		"viewpoint_id": "arrival_goal",
		"beat_id": "arrive",
		"label": "arrival goal / Newport Harbor opens the first-session loop",
		"events": [],
		"player_position": Vector2(430.0, 920.0),
		"camera_zoom": Vector2(1.34, 1.34),
		"player_direction": "up",
		"player_moving": false,
		"player_frame": 0,
		"target_id": "",
		"dialogue": "",
		"suppress_prompt": true
	},
	{
		"filename": "g20_02_counting_house_first_talk.png",
		"viewpoint_id": "counting_house_first_talk",
		"beat_id": "orient_talk",
		"label": "counting house first talk / Edrin turns arrival into a missing-manifest problem",
		"events": ["edrin"],
		"player_position": Vector2(1080.0, 585.0),
		"camera_zoom": Vector2(1.38, 1.38),
		"player_direction": "up",
		"player_moving": false,
		"player_frame": 0,
		"target_id": "EdrinVale",
		"dialogue": "Edrin Vale: The missing line is not a mistake. Ask the wharf who handled the cargo, then listen at the Tavern/Inn.",
		"suppress_prompt": false
	},
	{
		"filename": "g20_03_wharf_investigation_reward.png",
		"viewpoint_id": "wharf_investigation_reward",
		"beat_id": "investigate",
		"label": "wharf investigation / harbor work gives the mystery a physical place",
		"events": ["mara"],
		"player_position": Vector2(465.0, 1025.0),
		"camera_zoom": Vector2(1.34, 1.34),
		"player_direction": "right",
		"player_moving": true,
		"player_frame": 1,
		"target_id": "mara_pike_dockworker",
		"dialogue": "Mara Pike: That crate was not lost. Someone made it disappear before the tide bell.",
		"suppress_prompt": false
	},
	{
		"filename": "g20_04_tavern_whisper_social_hook.png",
		"viewpoint_id": "tavern_whisper_social_hook",
		"beat_id": "tavern_whisper",
		"label": "tavern whisper / the Third Toast creates the social hook and first Resolve reward",
		"events": ["bess"],
		"player_position": Vector2(500.0, 585.0),
		"camera_zoom": Vector2(1.38, 1.38),
		"player_direction": "up",
		"player_moving": false,
		"player_frame": 0,
		"target_id": "bess_armitage_tavern_keeper",
		"dialogue": "Bess Armitage: Third Toast, then no names. If the lantern burns twice at the wharf, someone chose a side.",
		"suppress_prompt": false
	},
	{
		"filename": "g20_05_choice_branch_next_lead.png",
		"viewpoint_id": "choice_branch_next_lead",
		"beat_id": "choose",
		"label": "choice branch / wharf lanterns show player agency before the island opens",
		"events": ["jonah"],
		"player_position": Vector2(465.0, 1025.0),
		"camera_zoom": Vector2(1.34, 1.34),
		"player_direction": "down",
		"player_moving": true,
		"player_frame": 2,
		"target_id": "jonah_reed_dock_courier",
		"dialogue": "Jonah Reed: Two lanterns means the cargo was claimed. One means it sank. Tonight there were two.",
		"suppress_prompt": false
	},
	{
		"filename": "g20_06_island_exit_reward_hook.png",
		"viewpoint_id": "island_exit_reward_hook",
		"beat_id": "explore",
		"label": "island exit / Edrin contact plus Isla turn the village edge into a route unlock",
		"events": ["edrin", "isla"],
		"player_position": Vector2(1880.0, 610.0),
		"camera_zoom": Vector2(1.18, 1.18),
		"player_direction": "right",
		"player_moving": true,
		"player_frame": 2,
		"target_id": "isla_brooke_farmhand",
		"dialogue": "Isla Brooke: The hill lantern was not farmer's work. Follow the old road, but keep the harbor at your back.",
		"suppress_prompt": false
	},
	{
		"filename": "g20_07_old_road_explore.png",
		"viewpoint_id": "old_road_explore",
		"beat_id": "old_road",
		"label": "old road / tavern code travels beyond Newport into island exploration",
		"events": ["elias"],
		"player_position": Vector2(2140.0, 454.0),
		"camera_zoom": Vector2(1.35, 1.35),
		"player_direction": "up",
		"player_moving": false,
		"player_frame": 0,
		"target_id": "elias_ward_suspicious_courier",
		"dialogue": "Elias Ward: The old road remembers kings better than clerks remember cargo. Look where the road stops pretending.",
		"suppress_prompt": false
	},
	{
		"filename": "g20_08_hidden_landing_discovery.png",
		"viewpoint_id": "hidden_landing_discovery",
		"beat_id": "discover",
		"label": "hidden landing discovery / optional signal clue and rope evidence make exploration pay off",
		"events": ["mara_oren", "tomas"],
		"player_position": Vector2(2220.0, 742.0),
		"camera_zoom": Vector2(1.32, 1.32),
		"player_direction": "up",
		"player_moving": false,
		"player_frame": 0,
		"target_id": "tomas_reed_dock_runner",
		"dialogue": "Tomas Reed: If the manifest lost a line, the cove kept the ink. That rope was cut after midnight.",
		"suppress_prompt": false
	},
	{
		"filename": "g20_09_return_report_choice.png",
		"viewpoint_id": "return_report_choice",
		"beat_id": "return_report",
		"label": "return report choice / Annelise gives the proof a social route home",
		"events": ["annelise"],
		"player_position": Vector2(1788.0, 674.0),
		"camera_zoom": Vector2(1.08, 1.08),
		"player_direction": "up",
		"player_moving": false,
		"player_frame": 0,
		"target_id": "annelise_crow_rumor_contact",
		"dialogue": "Annelise Crow: Bring the rope mark to Edrin. I will make sure the tavern hears the safer half of the truth.",
		"suppress_prompt": false
	},
	{
		"filename": "g20_10_final_reward_next_hook.png",
		"viewpoint_id": "final_reward_next_hook",
		"beat_id": "continue",
		"label": "final reward next hook / Edrin accepts proof and names the dawn threat",
		"events": ["edrin"],
		"player_position": Vector2(1080.0, 585.0),
		"camera_zoom": Vector2(1.38, 1.38),
		"player_direction": "up",
		"player_moving": false,
		"player_frame": 0,
		"target_id": "EdrinVale",
		"dialogue": "Edrin Vale: This tar mark is not Newport work. At first light, the Governor's men will ask the wrong questions. We ask first.",
		"suppress_prompt": false
	},
	{
		"filename": "g20_11_debug_disabled_first_session.png",
		"viewpoint_id": "debug_disabled_first_session",
		"beat_id": "debug_disabled",
		"label": "debug disabled / first-session proof uses player-facing HUD and no debug overlays",
		"events": [],
		"player_position": Vector2(1045.0, 645.0),
		"camera_zoom": Vector2(1.38, 1.38),
		"player_direction": "up",
		"player_moving": true,
		"player_frame": 1,
		"target_id": "",
		"dialogue": "",
		"suppress_prompt": true
	}
]


func _initialize() -> void:
	root.size = VIEWPORT_SIZE
	call_deferred("_run")


func _run() -> void:
	var exit_code := await _capture_all()
	quit(exit_code)


func _capture_all() -> int:
	var manifest := _base_manifest()
	var output_error := DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_DIR))
	if output_error != OK:
		manifest["status"] = "FAIL"
		manifest["failure"] = "Could not create output directory: %s error=%s" % [OUT_DIR, output_error]
		_write_json(manifest, "%s/%s" % [OUT_DIR, MANIFEST_FILENAME])
		return 1
	if DisplayServer.get_name().to_lower() == "headless":
		return _fail(manifest, "Refusing to capture visual proof with the headless display driver.")

	var main := MAIN_SCENE.instantiate()
	root.add_child(main)
	if main.has_method("set_review_screenshot_mode"):
		main.call("set_review_screenshot_mode", false)
	if main.has_method("set_debug_overlay"):
		main.call("set_debug_overlay", false)
	if main.has_method("set_building_seating_overlay"):
		main.call("set_building_seating_overlay", false)
	if main.has_method("set_green_origin_lab_mode"):
		main.call("set_green_origin_lab_mode", false)
	_set_ambient_barks(main, false)
	await _wait_for_render(INITIAL_WAIT_FRAMES)

	var player := main.get_node_or_null("World/Player") as Node2D
	if player == null:
		return _fail(manifest, "Player node not found.")
	player.set_physics_process(false)
	player.set_process(false)

	var camera := player.get_node_or_null("Camera2D") as Camera2D
	if camera == null:
		return _fail(manifest, "Player Camera2D node not found.")
	camera.enabled = true
	camera.position_smoothing_enabled = false
	camera.limit_smoothed = false
	camera.make_current()

	manifest["first_session_contract_initial"] = _jsonify(main.call("first_session_gameplay_loop_reward_contract") if main.has_method("first_session_gameplay_loop_reward_contract") else {})
	manifest["quest_contract_initial"] = _jsonify(main.call("starter_village_quest_contract") if main.has_method("starter_village_quest_contract") else {})
	manifest["debug_overlays_disabled"] = true
	manifest["hud_visible_for_reward_proof"] = true
	manifest["source_loop"] = "wayfarer_godot_vertical_slice/data/quests/g20_first_session_gameplay_loop_reward_v1.json"
	manifest["source_guidance"] = "wayfarer_godot_vertical_slice/data/ux/g19_player_guidance_map_journal_interaction_v1.json"
	manifest["source_runtime_layout"] = "wayfarer_godot_vertical_slice/data/world_layout/g19s_newport_runtime_reconstruction_v1.json"

	for capture in CAPTURES:
		var file_result := await _capture_one(capture, main, player, camera)
		manifest["screenshots"].append(file_result)
		if file_result.get("status", "") != "PASS":
			return _fail(manifest, String(file_result.get("failure", "Screenshot capture failed.")))

	var final_contract := _jsonify(main.call("first_session_gameplay_loop_reward_contract") if main.has_method("first_session_gameplay_loop_reward_contract") else {}) as Dictionary
	manifest["first_session_contract_final"] = final_contract
	manifest["quest_contract_final"] = _jsonify(main.call("starter_village_quest_contract") if main.has_method("starter_village_quest_contract") else {})
	manifest["hud_journal_contract_final"] = _jsonify(_journal_contract(main))
	manifest["status"] = "PASS"
	_write_json(final_contract, "%s/%s" % [OUT_DIR, TRACE_FILENAME])
	_write_playtest_log(final_contract)
	_write_json(manifest, "%s/%s" % [OUT_DIR, MANIFEST_FILENAME])
	print("PASS: G-20 first-session gameplay-loop screenshots -> ", ProjectSettings.globalize_path(OUT_DIR))
	return 0


func _capture_one(capture: Dictionary, main: Node, player: Node2D, camera: Camera2D) -> Dictionary:
	if main.has_method("debug_apply_first_light_quest_events"):
		main.call("debug_apply_first_light_quest_events", capture.get("events", []))
	await _wait_for_render(2)

	var target := _target_node(main, String(capture.get("target_id", "")))
	var player_position: Vector2 = capture["player_position"]
	if target != null and target.has_method("get_interaction_position"):
		player_position = target.call("get_interaction_position") + Vector2(0.0, 30.0)
	player.global_position = player_position
	if player.has_method("set_review_visual_state"):
		player.call("set_review_visual_state", capture["player_direction"], capture["player_moving"], capture["player_frame"])
	if player.has_method("set_prompt_suppressed"):
		player.call("set_prompt_suppressed", bool(capture.get("suppress_prompt", true)))
	if player.has_method("_update_interaction_target"):
		player.call("_update_interaction_target")
	_update_hud_location(main, player_position)
	_show_dialogue(main, String(capture.get("dialogue", "")))
	_set_ambient_barks(main, false)
	camera.zoom = capture["camera_zoom"]
	camera.offset = Vector2.ZERO
	camera.reset_smoothing()
	await _wait_for_render(CAPTURE_WAIT_FRAMES)
	_set_ambient_barks(main, false)

	var image := root.get_texture().get_image()
	var output_path := "%s/%s" % [OUT_DIR, capture["filename"]]
	var prompt_label := player.get_node_or_null("PromptLabel") as Label
	var result := {
		"filename": capture["filename"],
		"viewpoint_id": capture["viewpoint_id"],
		"beat_id": capture["beat_id"],
		"label": capture["label"],
		"path": output_path,
		"absolute_path": ProjectSettings.globalize_path(output_path),
		"player_position": _vector2_to_dict(player_position),
		"camera_zoom": _vector2_to_dict(capture["camera_zoom"]),
		"dimensions": {"w": image.get_width(), "h": image.get_height()},
		"prompt_visible": prompt_label != null and prompt_label.visible,
		"prompt_text": prompt_label.text if prompt_label != null else "",
		"journal_objective_contract": _jsonify(_journal_contract(main)),
		"reward_loop_contract": _jsonify(_reward_loop_contract(main)),
		"first_session_contract": _jsonify(main.call("first_session_gameplay_loop_reward_contract") if main.has_method("first_session_gameplay_loop_reward_contract") else {}),
		"png_verification": {},
		"status": "PENDING",
	}
	if image.get_width() < 640 or image.get_height() < 360:
		result["status"] = "FAIL"
		result["failure"] = "Viewport image dimensions were not sensible."
		return result
	var save_error := image.save_png(output_path)
	if save_error != OK:
		result["status"] = "FAIL"
		result["failure"] = "Could not save %s error=%s" % [output_path, save_error]
		return result
	var png_verification := _verify_png_pixels(image)
	result["png_verification"] = png_verification
	if String(png_verification.get("status", "")) != "PASS":
		result["status"] = "FAIL"
		result["failure"] = String(png_verification.get("failure", "PNG verification failed."))
		return result
	result["status"] = "PASS"
	print("Wrote ", output_path, " ", image.get_width(), "x", image.get_height())
	return result


func _target_node(main: Node, target_id: String) -> Node:
	if target_id.is_empty():
		return null
	return main.get_node_or_null("World/" + target_id)


func _update_hud_location(main: Node, player_position: Vector2) -> void:
	var hud := main.get_node_or_null("HUD")
	if hud != null and hud.has_method("set_player_world_position"):
		hud.call("set_player_world_position", player_position)


func _show_dialogue(main: Node, text: String) -> void:
	var hud := main.get_node_or_null("HUD")
	if hud == null:
		return
	var dialogue_panel := hud.get_node_or_null("DialoguePanel") as Control
	var dialogue_label := hud.get_node_or_null("DialoguePanel/MarginContainer/DialogueLabel") as Label
	if dialogue_panel == null or dialogue_label == null:
		return
	dialogue_label.text = text
	dialogue_panel.visible = not text.is_empty()


func _set_ambient_barks(main: Node, enabled: bool) -> void:
	if main.has_method("set_starter_village_ambient_barks_enabled"):
		main.call("set_starter_village_ambient_barks_enabled", enabled)
	if main.has_method("set_opening_island_ambient_barks_enabled"):
		main.call("set_opening_island_ambient_barks_enabled", enabled)


func _journal_contract(main: Node) -> Dictionary:
	var hud := main.get_node_or_null("HUD")
	if hud != null and hud.has_method("journal_objective_contract"):
		return _jsonify(hud.call("journal_objective_contract")) as Dictionary
	return {}


func _reward_loop_contract(main: Node) -> Dictionary:
	var hud := main.get_node_or_null("HUD")
	if hud != null and hud.has_method("first_session_reward_loop_contract"):
		return _jsonify(hud.call("first_session_reward_loop_contract")) as Dictionary
	return {}


func _write_playtest_log(contract: Dictionary) -> void:
	var lines := [
		"# G-20 First-Session Gameplay Loop Playtest Log",
		"",
		"Phase: G-20 First-Session Gameplay Loop and Reward Pass",
		"Playthrough result: " + String(contract.get("status", "UNKNOWN")),
		"Playable minutes estimate: " + str(contract.get("playable_minutes_estimate", 0)),
		"Reward Resolve total: " + str(contract.get("reward_resolve", 0)),
		"Reason to continue: " + String(contract.get("first_time_player_reason_to_continue", "")),
		"",
		"## Loop Beats",
	]
	for raw_beat in contract.get("loop_beats", []):
		var beat: Dictionary = raw_beat
		lines.append("- %s (%s): %s -> %s" % [
			String(beat.get("beat_id", "")),
			String(beat.get("minute_target", "")),
			String(beat.get("location", "")),
			String(beat.get("reward_feedback", "")),
		])
	lines.append("")
	lines.append("## Rewards")
	for reward in contract.get("reward_log", []):
		lines.append("- " + String(reward))
	lines.append("")
	lines.append("## Scores")
	for score_key in ["gameplay_hook_score", "reward_cadence_score", "world_cohesion_score", "player_orientation_score", "quest_geography_integration_score", "implementation_readiness_score"]:
		lines.append("- %s: %s" % [score_key, str(contract.get(score_key, 0.0))])
	var file := FileAccess.open("%s/%s" % [OUT_DIR, PLAYTEST_LOG_FILENAME], FileAccess.WRITE)
	if file == null:
		push_error("Could not open G-20 playtest log for writing.")
		return
	file.store_string("\n".join(lines) + "\n")
	file.close()


func _wait_for_render(frames: int) -> void:
	for _i in range(frames):
		await process_frame


func _verify_png_pixels(image: Image) -> Dictionary:
	var samples := 0
	var color_sum := 0.0
	for y in range(0, image.get_height(), 80):
		for x in range(0, image.get_width(), 80):
			var color := image.get_pixel(x, y)
			color_sum += color.r + color.g + color.b
			samples += 1
	if samples <= 0:
		return {"status": "FAIL", "failure": "No sampled pixels."}
	var average := color_sum / float(samples)
	if average <= 0.03:
		return {"status": "FAIL", "failure": "Screenshot appears blank or black.", "average_rgb": average}
	return {"status": "PASS", "average_rgb": average, "sample_count": samples}


func _base_manifest() -> Dictionary:
	return {
		"schema_id": "wayfarer.g20.first_session_screenshot_manifest.v1",
		"phase": "G-20",
		"out_dir": OUT_DIR,
		"viewport": {"w": VIEWPORT_SIZE.x, "h": VIEWPORT_SIZE.y},
		"screenshots": [],
		"status": "PENDING",
	}


func _fail(manifest: Dictionary, message: String) -> int:
	manifest["status"] = "FAIL"
	manifest["failure"] = message
	_write_json(manifest, "%s/%s" % [OUT_DIR, MANIFEST_FILENAME])
	push_error(message)
	return 1


func _write_json(value: Variant, path: String) -> void:
	var file := FileAccess.open(path, FileAccess.WRITE)
	if file == null:
		push_error("Could not open JSON for writing: " + path)
		return
	file.store_string(JSON.stringify(_jsonify(value), "\t"))
	file.close()


func _jsonify(value: Variant) -> Variant:
	if value is Vector2:
		return _vector2_to_dict(value)
	if value is Vector2i:
		return {"x": value.x, "y": value.y}
	if value is Rect2:
		return {
			"x": value.position.x,
			"y": value.position.y,
			"w": value.size.x,
			"h": value.size.y,
		}
	if value is Rect2i:
		return {
			"x": value.position.x,
			"y": value.position.y,
			"w": value.size.x,
			"h": value.size.y,
		}
	if value is Array:
		var array: Array = []
		for item in value:
			array.append(_jsonify(item))
		return array
	if value is Dictionary:
		var dict := {}
		for key in value.keys():
			dict[String(key)] = _jsonify(value[key])
		return dict
	return value


func _vector2_to_dict(value: Vector2) -> Dictionary:
	return {"x": value.x, "y": value.y}
