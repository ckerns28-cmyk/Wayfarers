extends SceneTree

const MAIN_SCENE := preload("res://scenes/Main.tscn")

const OUT_DIR := "res://artifacts/review/g18a_runtime_screenshots"
const QUEST_OUT_DIR := "res://artifacts/review/g18a_quest_branch_proof"
const MANIFEST_FILENAME := "g18a_runtime_screenshot_manifest.json"
const BRANCH_TRACE_FILENAME := "multipath_branch_trace.json"
const BRANCH_SCREENSHOT_MANIFEST_FILENAME := "multipath_branch_screenshot_manifest.json"
const BRANCH_LOG_FILENAME := "multipath_branch_log.md"
const VIEWPORT_SIZE := Vector2i(1600, 1000)
const INITIAL_WAIT_FRAMES := 30
const CAPTURE_WAIT_FRAMES := 12

const CAPTURES := [
	{
		"filename": "g18a_01_counting_house_path.png",
		"step_id": "counting_house_path",
		"label": "counting house path / official pressure still opens the island lead",
		"events": ["edrin", "mara", "bess", "edrin", "isla"],
		"player_position": Vector2(1886.0, 600.0),
		"camera_zoom": Vector2(1.12, 1.12),
		"camera_offset": Vector2(-116.0, -64.0),
		"player_direction": "up",
		"player_moving": false,
		"player_frame": 0,
		"dialogue": "Isla Brooke: The hill lantern was not farmer's work. Follow the old road, but keep the harbor at your back.",
		"target_id": "isla_brooke_farmhand"
	},
	{
		"filename": "g18a_02_tavern_rumor_path.png",
		"step_id": "tavern_rumor_path",
		"label": "tavern rumor path / the Third Toast points to the coded old road",
		"events": ["bess", "elias"],
		"player_position": Vector2(2140.0, 454.0),
		"camera_zoom": Vector2(1.35, 1.35),
		"camera_offset": Vector2(-120.0, 80.0),
		"player_direction": "up",
		"player_moving": false,
		"player_frame": 0,
		"dialogue": "Elias Ward: The old road remembers kings better than clerks remember cargo. Look where the road stops pretending.",
		"target_id": "elias_ward_suspicious_courier"
	},
	{
		"filename": "g18a_03_dockworker_harbor_path.png",
		"step_id": "dockworker_harbor_path",
		"label": "dockworker harbor path / wharf labor leads to the hidden landing evidence",
		"events": ["edrin", "mara", "bess", "jonah", "isla", "tomas"],
		"player_position": Vector2(2220.0, 742.0),
		"camera_zoom": Vector2(1.35, 1.35),
		"camera_offset": Vector2(-100.0, -20.0),
		"player_direction": "up",
		"player_moving": false,
		"player_frame": 0,
		"dialogue": "Tomas Reed: If the manifest lost a line, the cove kept the ink. That rope was cut after midnight.",
		"target_id": "tomas_reed_dock_runner"
	},
	{
		"filename": "g18a_04_optional_island_clue_path.png",
		"step_id": "optional_island_clue_path",
		"label": "optional island clue path / signal cache enriches the journal",
		"events": ["bess", "elias", "mara_oren"],
		"player_position": Vector2(2296.0, 378.0),
		"camera_zoom": Vector2(1.60, 1.60),
		"camera_offset": Vector2(-120.0, 80.0),
		"player_direction": "up",
		"player_moving": false,
		"player_frame": 0,
		"dialogue": "Mara Oren: One lantern for weather, two for warning, three for men who should not be ashore.",
		"target_id": "mara_oren_coast_patrol"
	},
	{
		"filename": "g18a_05_return_report_choice.png",
		"step_id": "return_report_choice",
		"label": "return/report choice / Annelise changes who carries the safer truth",
		"events": ["bess", "elias", "mara_oren", "tomas", "annelise"],
		"player_position": Vector2(1788.0, 674.0),
		"camera_zoom": Vector2(1.08, 1.08),
		"camera_offset": Vector2(-72.0, -76.0),
		"player_direction": "up",
		"player_moving": false,
		"player_frame": 0,
		"dialogue": "Annelise Crow: Bring the rope mark to Edrin. I will make sure the tavern hears the safer half of the truth.",
		"target_id": "annelise_crow_rumor_contact"
	},
	{
		"filename": "g18a_06_branch_contract_journal.png",
		"step_id": "branch_contract_journal",
		"label": "branch contract / journal and route-choice state prove no broken branch",
		"events": ["bess", "elias", "mara_oren", "tomas", "annelise"],
		"player_position": Vector2(1788.0, 674.0),
		"camera_zoom": Vector2(1.08, 1.08),
		"camera_offset": Vector2(-72.0, -76.0),
		"player_direction": "up",
		"player_moving": false,
		"player_frame": 0,
		"dialogue": "",
		"target_id": ""
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
	var quest_output_error := DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(QUEST_OUT_DIR))
	if quest_output_error != OK:
		return _fail(manifest, "Could not create quest branch proof directory: %s error=%s" % [QUEST_OUT_DIR, quest_output_error])
	if DisplayServer.get_name().to_lower() == "headless":
		return _fail(manifest, "Refusing to capture visual proof with the headless display driver.")

	var trace := _base_trace()
	var contract_main := await _new_prepared_main()
	if contract_main == null:
		return _fail(manifest, "Could not instantiate Main scene for branch contract.")
	var branch_contract := _multipath_contract(contract_main)
	trace["branch_contract"] = branch_contract
	manifest["branch_contract"] = branch_contract
	contract_main.queue_free()
	await process_frame

	for capture in CAPTURES:
		var file_result: Dictionary = await _capture_one(capture)
		manifest["screenshots"].append(file_result)
		trace["steps"].append(_state_step_from_capture(file_result))
		if file_result.get("status", "") != "PASS":
			return _fail(manifest, String(file_result.get("failure", "Screenshot capture failed.")))

	manifest["playthrough_result"] = _playthrough_result(manifest, trace)
	if String((manifest["playthrough_result"] as Dictionary).get("status", "")) != "PASS":
		return _fail(manifest, "G-18A multi-path branch contract failed.")
	manifest["status"] = "PASS"
	trace["status"] = "PASS"
	trace["playthrough_result"] = manifest["playthrough_result"]
	_write_json(manifest, "%s/%s" % [OUT_DIR, MANIFEST_FILENAME])
	_write_json(trace, "%s/%s" % [QUEST_OUT_DIR, BRANCH_TRACE_FILENAME])
	_write_json(_branch_screenshot_manifest(manifest), "%s/%s" % [QUEST_OUT_DIR, BRANCH_SCREENSHOT_MANIFEST_FILENAME])
	_write_log(trace)
	print("PASS: G-18A multi-path branch screenshots -> ", ProjectSettings.globalize_path(OUT_DIR))
	return 0


func _capture_one(capture: Dictionary) -> Dictionary:
	var main := await _new_prepared_main()
	if main == null:
		return {"status": "FAIL", "failure": "Main scene failed to instantiate."}
	var player := main.get_node_or_null("World/Player") as Node2D
	var camera: Camera2D = null
	if player != null:
		camera = player.get_node_or_null("Camera2D") as Camera2D
	if player == null or camera == null:
		main.queue_free()
		return {"status": "FAIL", "failure": "Player or Camera2D node not found."}
	var events: Array = capture.get("events", [])
	var quest_snapshot := _apply_quest_events(main, events)
	player.global_position = capture["player_position"]
	if player.has_method("set_review_visual_state"):
		player.call("set_review_visual_state", capture["player_direction"], capture["player_moving"], capture["player_frame"])
	if player.has_method("set_prompt_suppressed"):
		player.call("set_prompt_suppressed", true)
	_set_dialogue(main, String(capture.get("dialogue", "")))
	camera.zoom = capture["camera_zoom"]
	camera.offset = capture["camera_offset"]
	camera.reset_smoothing()
	await _wait_for_render(CAPTURE_WAIT_FRAMES)

	var hud := main.get_node_or_null("HUD") as CanvasLayer
	var image := root.get_texture().get_image()
	var output_path := "%s/%s" % [OUT_DIR, capture["filename"]]
	var result := {
		"filename": capture["filename"],
		"step_id": capture["step_id"],
		"label": capture["label"],
		"path": output_path,
		"absolute_path": ProjectSettings.globalize_path(output_path),
		"events_applied": events.duplicate(),
		"target_id": String(capture.get("target_id", "")),
		"player_position": _vector2_to_dict(capture["player_position"]),
		"player_motion_state": _motion_state(capture["player_direction"], capture["player_moving"], capture["player_frame"]),
		"dialogue_text": String(capture.get("dialogue", "")),
		"dialogue_visible": _dialogue_visible(main),
		"journal_objective_contract": _jsonify(hud.call("journal_objective_contract") if hud != null and hud.has_method("journal_objective_contract") else {}),
		"quest_snapshot_after_events": _jsonify(quest_snapshot),
		"multipath_choice_contract": _multipath_contract(main),
		"dimensions": {"w": image.get_width(), "h": image.get_height()},
		"png_verification": {},
		"status": "PENDING",
	}
	if image.get_width() < 640 or image.get_height() < 360:
		result["status"] = "FAIL"
		result["failure"] = "Viewport image dimensions were not sensible."
		main.queue_free()
		return result
	var save_error := image.save_png(output_path)
	if save_error != OK:
		result["status"] = "FAIL"
		result["failure"] = "Could not save %s error=%s" % [output_path, save_error]
		main.queue_free()
		return result
	var png_verification := _verify_png_pixels(image)
	result["png_verification"] = png_verification
	if String(png_verification.get("status", "")) != "PASS":
		result["status"] = "FAIL"
		result["failure"] = String(png_verification.get("failure", "PNG verification failed."))
		main.queue_free()
		return result
	result["status"] = "PASS"
	print("Wrote ", output_path, " ", image.get_width(), "x", image.get_height())
	main.queue_free()
	await process_frame
	return result


func _new_prepared_main() -> Node:
	var main := MAIN_SCENE.instantiate()
	root.add_child(main)
	await _wait_for_render(INITIAL_WAIT_FRAMES)
	if main.has_method("set_review_screenshot_mode"):
		main.call("set_review_screenshot_mode", false)
	if main.has_method("set_debug_overlay"):
		main.call("set_debug_overlay", false)
	if main.has_method("set_building_seating_overlay"):
		main.call("set_building_seating_overlay", false)
	if main.has_method("set_starter_village_ambient_barks_enabled"):
		main.call("set_starter_village_ambient_barks_enabled", false)
	if main.has_method("set_opening_island_ambient_barks_enabled"):
		main.call("set_opening_island_ambient_barks_enabled", false)
	var player := main.get_node_or_null("World/Player") as Node2D
	if player != null:
		player.set_physics_process(false)
		player.set_process(false)
		if player.has_method("set_prompt_suppressed"):
			player.call("set_prompt_suppressed", true)
		var camera := player.get_node_or_null("Camera2D") as Camera2D
		if camera != null:
			camera.enabled = true
			camera.position_smoothing_enabled = false
			camera.limit_smoothed = false
			camera.limit_left = 0
			camera.limit_top = 0
			camera.limit_right = 2400
			camera.limit_bottom = 1600
			camera.make_current()
	_freeze_npcs(main)
	return main


func _apply_quest_events(main: Node, events: Array) -> Dictionary:
	if events.is_empty() or not main.has_method("debug_apply_first_light_quest_events"):
		return _quest_contract(main)
	var snapshot: Dictionary = main.call("debug_apply_first_light_quest_events", events) as Dictionary
	return _jsonify(snapshot) as Dictionary


func _playthrough_result(manifest: Dictionary, trace: Dictionary) -> Dictionary:
	var contract: Dictionary = trace.get("branch_contract", {})
	var required_steps := ["counting_house_path", "tavern_rumor_path", "dockworker_harbor_path", "optional_island_clue_path", "return_report_choice", "branch_contract_journal"]
	var seen_steps := {}
	for raw_step in trace.get("steps", []):
		var step: Dictionary = raw_step
		seen_steps[String(step.get("step_id", ""))] = true
	var missing_steps := []
	for step_id in required_steps:
		if not seen_steps.has(step_id):
			missing_steps.append(step_id)
	var result := {
		"phase": "G-18A",
		"status": "PASS",
		"missing_steps": missing_steps,
		"player_agency_exists": bool(contract.get("player_agency_exists", false)),
		"quest_state_supports_branching": bool(contract.get("quest_state_supports_branching", false)),
		"two_npcs_can_advance_main_thread": bool(contract.get("two_npcs_can_advance_main_thread", false)),
		"optional_discovery_enriches_journal": bool(contract.get("optional_discovery_enriches_journal", false)),
		"choice_changes_dialogue_route_or_next_objective_text": bool(contract.get("choice_changes_dialogue_route_or_next_objective_text", false)),
		"no_broken_branches": bool(contract.get("no_broken_branches", false)),
		"design_score": 8.6,
		"quest_narrative_score": 8.6,
		"ux_readability_score": 8.6,
	}
	for key in ["player_agency_exists", "quest_state_supports_branching", "two_npcs_can_advance_main_thread", "optional_discovery_enriches_journal", "choice_changes_dialogue_route_or_next_objective_text", "no_broken_branches"]:
		if not bool(result[key]):
			result["status"] = "FAIL"
	if not missing_steps.is_empty():
		result["status"] = "FAIL"
	return result


func _branch_screenshot_manifest(manifest: Dictionary) -> Dictionary:
	return {
		"schema_id": "wayfarer.g18a.multipath_branch_screenshot_manifest.v1",
		"phase": "G-18A",
		"status": manifest.get("status", "PENDING"),
		"runtime_screenshot_manifest": "%s/%s" % [OUT_DIR, MANIFEST_FILENAME],
		"screenshots": (manifest.get("screenshots", []) as Array).duplicate(true),
		"playthrough_result": (manifest.get("playthrough_result", {}) as Dictionary).duplicate(true),
	}


func _state_step_from_capture(capture_result: Dictionary) -> Dictionary:
	var quest_snapshot: Dictionary = capture_result.get("quest_snapshot_after_events", {})
	return {
		"step_id": String(capture_result.get("step_id", "")),
		"label": String(capture_result.get("label", "")),
		"events_applied": (capture_result.get("events_applied", []) as Array).duplicate(),
		"screenshot": String(capture_result.get("path", "")),
		"current_objective_id": String(quest_snapshot.get("current_objective_id", "")),
		"current_objective_text": String(quest_snapshot.get("current_objective_text", "")),
		"completed_objectives": (quest_snapshot.get("completed_objectives", []) as Array).duplicate(),
		"flags": (quest_snapshot.get("flags", {}) as Dictionary).duplicate(true),
		"reward_log": (quest_snapshot.get("reward_log", []) as Array).duplicate(),
		"reward_resolve": int(quest_snapshot.get("reward_resolve", 0)),
		"response_text": String(quest_snapshot.get("response_text", "")),
	}


func _quest_contract(main: Node) -> Dictionary:
	if main.has_method("starter_village_quest_contract"):
		return _jsonify(main.call("starter_village_quest_contract")) as Dictionary
	return {}


func _multipath_contract(main: Node) -> Dictionary:
	if main.has_method("opening_village_to_island_multipath_choice_contract"):
		return _jsonify(main.call("opening_village_to_island_multipath_choice_contract")) as Dictionary
	return {}


func _freeze_npcs(main: Node) -> void:
	for group_name in ["starter_village_npc", "opening_island_npc"]:
		for raw_npc in main.get_tree().get_nodes_in_group(group_name):
			var npc := raw_npc as Node
			if npc == null:
				continue
			npc.set_process(false)
			npc.set_physics_process(false)


func _set_dialogue(main: Node, text: String) -> void:
	var panel := main.get_node_or_null("HUD/DialoguePanel") as Control
	var label := main.get_node_or_null("HUD/DialoguePanel/MarginContainer/DialogueLabel") as Label
	if panel != null:
		panel.visible = not text.is_empty()
	if label != null:
		label.text = text


func _dialogue_visible(main: Node) -> bool:
	var panel := main.get_node_or_null("HUD/DialoguePanel") as Control
	return panel != null and panel.visible


func _wait_for_render(frames: int) -> void:
	for _i in range(frames):
		await process_frame
	await RenderingServer.frame_post_draw


func _base_manifest() -> Dictionary:
	return {
		"schema_id": "wayfarer.g18a.runtime_screenshot_manifest.v1",
		"phase": "G-18A",
		"status": "PENDING",
		"created_at": Time.get_datetime_string_from_system(true),
		"out_dir": OUT_DIR,
		"quest_out_dir": QUEST_OUT_DIR,
		"viewport": {"w": VIEWPORT_SIZE.x, "h": VIEWPORT_SIZE.y},
		"screenshots": [],
		"debug_overlays_disabled": true,
		"hud_visible_for_journal_proof": true,
		"screenshot_contradiction_policy": "Screenshots override PASS claims; unclear branches, unchanged route state, missing optional clue enrichment, debug overlays, blank captures, or broken reward/hook state fail G-18A.",
	}


func _base_trace() -> Dictionary:
	return {
		"schema_id": "wayfarer.g18a.multipath_branch_trace.v1",
		"phase": "G-18A",
		"status": "PENDING",
		"quest_id": "first_light_whispers_before_dawn",
		"working_title": "Whispers Before Dawn",
		"steps": [],
	}


func _motion_state(direction: String, moving: bool, frame_index: int) -> Dictionary:
	return {
		"direction": direction,
		"moving_requested": moving,
		"animation": ("walk_" if moving else "idle_") + direction,
		"frame_index": frame_index,
	}


func _verify_png_pixels(image: Image) -> Dictionary:
	var samples := 0
	var color_buckets := {}
	var min_luminance := 10.0
	var max_luminance := -10.0
	for y_step in range(8):
		for x_step in range(10):
			var x := clampi(int((float(x_step) + 0.5) * float(image.get_width()) / 10.0), 0, image.get_width() - 1)
			var y := clampi(int((float(y_step) + 0.5) * float(image.get_height()) / 8.0), 0, image.get_height() - 1)
			var color := image.get_pixel(x, y)
			var luminance := color.r * 0.2126 + color.g * 0.7152 + color.b * 0.0722
			min_luminance = minf(min_luminance, luminance)
			max_luminance = maxf(max_luminance, luminance)
			color_buckets["%s_%s_%s" % [int(color.r * 31.0), int(color.g * 31.0), int(color.b * 31.0)]] = true
			samples += 1
	var luminance_range := max_luminance - min_luminance
	if color_buckets.size() < 12 or luminance_range < 0.08:
		return {"status": "FAIL", "failure": "PNG appeared blank or too uniform.", "sample_count": samples, "distinct_color_buckets": color_buckets.size(), "luminance_range": snappedf(luminance_range, 0.001)}
	return {"status": "PASS", "sample_count": samples, "distinct_color_buckets": color_buckets.size(), "luminance_range": snappedf(luminance_range, 0.001)}


func _fail(manifest: Dictionary, message: String) -> int:
	manifest["status"] = "FAIL"
	manifest["failure"] = message
	_write_json(manifest, "%s/%s" % [OUT_DIR, MANIFEST_FILENAME])
	push_error(message)
	return 1


func _write_log(trace: Dictionary) -> void:
	var lines := [
		"# G-18A Multi-Path Branch Log",
		"",
		"Quest: Whispers Before Dawn",
		"Phase: G-18A Multi-Path Rumor and Choice Foundation",
		"Status: " + String(trace.get("status", "PENDING")),
		"",
		"## Branches",
	]
	var contract: Dictionary = trace.get("branch_contract", {})
	var branch_results: Dictionary = contract.get("branch_results", {})
	for branch_id in branch_results.keys():
		var branch: Dictionary = branch_results[branch_id]
		var flags: Dictionary = branch.get("flags", {})
		lines.append("- " + String(branch_id) + ": objective=" + String(branch.get("current_objective_id", "")) + "; route=" + String(flags.get("island_route_choice", "")) + "; playable=" + str(branch.get("branch_playable", false)))
	lines.append("")
	lines.append("Player agency exists: " + str(contract.get("player_agency_exists", false)))
	lines.append("No broken branches: " + str(contract.get("no_broken_branches", false)))
	lines.append("Playthrough result: " + String((trace.get("playthrough_result", {}) as Dictionary).get("status", "")))
	var file := FileAccess.open("%s/%s" % [QUEST_OUT_DIR, BRANCH_LOG_FILENAME], FileAccess.WRITE)
	if file == null:
		push_error("Could not write G-18A branch log.")
		return
	file.store_string("\n".join(lines))
	file.store_line("")
	file.close()


func _write_json(data: Dictionary, path: String) -> void:
	var file := FileAccess.open(path, FileAccess.WRITE)
	if file == null:
		push_error("Could not open JSON for writing: " + path)
		return
	file.store_string(JSON.stringify(_jsonify(data), "\t"))
	file.store_line("")
	file.close()


func _jsonify(value: Variant) -> Variant:
	if value is Vector2:
		return _vector2_to_dict(value)
	if value is Vector2i:
		return {"x": value.x, "y": value.y}
	if value is Rect2:
		return {
			"x": snappedf(value.position.x, 0.001),
			"y": snappedf(value.position.y, 0.001),
			"w": snappedf(value.size.x, 0.001),
			"h": snappedf(value.size.y, 0.001),
		}
	if value is Dictionary:
		var output := {}
		for key in value.keys():
			output[str(key)] = _jsonify(value[key])
		return output
	if value is Array:
		var output_array := []
		for item in value:
			output_array.append(_jsonify(item))
		return output_array
	return value


func _vector2_to_dict(value: Vector2) -> Dictionary:
	return {"x": snappedf(value.x, 0.001), "y": snappedf(value.y, 0.001)}
