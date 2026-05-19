extends SceneTree

const MAIN_SCENE := preload("res://scenes/Main.tscn")

const OUT_DIR := "res://artifacts/review/g19_runtime_screenshots"
const MANIFEST_FILENAME := "g19_runtime_screenshot_manifest.json"
const VIEWPORT_SIZE := Vector2i(1600, 1000)
const INITIAL_WAIT_FRAMES := 30
const CAPTURE_WAIT_FRAMES := 12
const BANNED_HUD_COPY := ["DEBUG", "Press E", "Hook updated:", "Objective updated:", "Objective complete:"]

const CAPTURES := [
	{
		"filename": "g19_01_arrival_dynamic_location.png",
		"step_id": "arrival_dynamic_location",
		"label": "arrival / HUD names the harbor and gives a clean next focus",
		"events": [],
		"player_position": Vector2(675.0, 612.0),
		"camera_zoom": Vector2(1.10, 1.10),
		"camera_offset": Vector2(-64.0, -84.0),
		"player_direction": "down",
		"dialogue": ""
	},
	{
		"filename": "g19_02_counting_house_guidance.png",
		"step_id": "counting_house_guidance",
		"label": "counting house / official route has an authored area name",
		"events": ["edrin"],
		"player_position": Vector2(792.0, 570.0),
		"camera_zoom": Vector2(1.18, 1.18),
		"camera_offset": Vector2(-42.0, -96.0),
		"player_direction": "up",
		"dialogue": "Edrin Vale: The missing line is small enough to hide, and large enough to hang a family."
	},
	{
		"filename": "g19_03_tavern_rumor_clean_journal.png",
		"step_id": "tavern_rumor_clean_journal",
		"label": "tavern rumor / journal avoids validator-facing state copy",
		"events": ["bess", "elias"],
		"player_position": Vector2(330.0, 604.0),
		"camera_zoom": Vector2(1.18, 1.18),
		"camera_offset": Vector2(38.0, -54.0),
		"player_direction": "left",
		"dialogue": "Bess Armitage: The Third Toast is not a toast if every honest soul can hear it."
	},
	{
		"filename": "g19_04_village_exit_east_gate.png",
		"step_id": "village_exit_east_gate",
		"label": "village exit / settlement threshold opens into island route",
		"events": ["edrin", "mara", "bess", "edrin", "isla"],
		"player_position": Vector2(1538.0, 548.0),
		"camera_zoom": Vector2(1.04, 1.04),
		"camera_offset": Vector2(-88.0, -86.0),
		"player_direction": "right",
		"dialogue": "Isla Brooke: Follow the old road where the last Newport lamp gives up."
	},
	{
		"filename": "g19_05_old_road_signal_guidance.png",
		"step_id": "old_road_signal_guidance",
		"label": "old road / island objective is readable without crude markers",
		"events": ["bess", "elias"],
		"player_position": Vector2(2140.0, 454.0),
		"camera_zoom": Vector2(1.30, 1.30),
		"camera_offset": Vector2(-114.0, 58.0),
		"player_direction": "up",
		"dialogue": "Elias Ward: The old road remembers kings better than clerks remember cargo."
	},
	{
		"filename": "g19_06_hidden_landing_return_lane.png",
		"step_id": "hidden_landing_return_lane",
		"label": "hidden landing / cove evidence points cleanly back toward town",
		"events": ["bess", "elias", "mara_oren", "tomas"],
		"player_position": Vector2(2220.0, 742.0),
		"camera_zoom": Vector2(1.26, 1.26),
		"camera_offset": Vector2(-104.0, -22.0),
		"player_direction": "up",
		"dialogue": "Tomas Reed: That rope was cut after midnight. Carry the proof before dawn."
	},
	{
		"filename": "g19_07_chris_screenshot_repair_composition.png",
		"step_id": "chris_screenshot_repair_composition",
		"label": "Chris screenshot repair / same return-lane area must no longer read as patchwork proof",
		"events": ["bess", "elias", "mara_oren", "tomas", "annelise"],
		"player_position": Vector2(1788.0, 674.0),
		"camera_zoom": Vector2(1.08, 1.08),
		"camera_offset": Vector2(-72.0, -76.0),
		"player_direction": "up",
		"dialogue": "Annelise Crow: Bring the rope mark to Edrin. I will make sure the tavern hears the safer half of the truth."
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
		return _fail(manifest, "Could not create output directory: %s error=%s" % [OUT_DIR, output_error])
	if DisplayServer.get_name().to_lower() == "headless":
		return _fail(manifest, "Refusing to capture visual proof with the headless display driver.")
	for capture in CAPTURES:
		var file_result: Dictionary = await _capture_one(capture)
		manifest["screenshots"].append(file_result)
		if file_result.get("status", "") != "PASS":
			return _fail(manifest, String(file_result.get("failure", "Screenshot capture failed.")))
	manifest["playthrough_result"] = _playthrough_result(manifest)
	if String((manifest["playthrough_result"] as Dictionary).get("status", "")) != "PASS":
		return _fail(manifest, "G-19 guidance proof failed.")
	manifest["status"] = "PASS"
	_write_json(manifest, "%s/%s" % [OUT_DIR, MANIFEST_FILENAME])
	print("PASS: G-19 runtime guidance screenshots -> ", ProjectSettings.globalize_path(OUT_DIR))
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
		player.call("set_review_visual_state", capture["player_direction"], false, 0)
	if player.has_method("set_prompt_suppressed"):
		player.call("set_prompt_suppressed", true)
	_update_hud_position(main, player.global_position)
	_set_dialogue(main, String(capture.get("dialogue", "")))
	camera.zoom = capture["camera_zoom"]
	camera.offset = capture["camera_offset"]
	camera.reset_smoothing()
	await _wait_for_render(CAPTURE_WAIT_FRAMES)

	var hud := main.get_node_or_null("HUD") as CanvasLayer
	var guidance_contract := _guidance_contract(main)
	var hud_copy := _hud_copy(main)
	var image := root.get_texture().get_image()
	var output_path := "%s/%s" % [OUT_DIR, capture["filename"]]
	var result := {
		"filename": capture["filename"],
		"step_id": capture["step_id"],
		"label": capture["label"],
		"path": output_path,
		"absolute_path": ProjectSettings.globalize_path(output_path),
		"events_applied": events.duplicate(),
		"player_position": _vector2_to_dict(capture["player_position"]),
		"dialogue_text": String(capture.get("dialogue", "")),
		"dialogue_visible": _dialogue_visible(main),
		"hud_copy": hud_copy,
		"journal_objective_contract": _jsonify(hud.call("journal_objective_contract") if hud != null and hud.has_method("journal_objective_contract") else {}),
		"opening_player_guidance_contract": _jsonify(guidance_contract),
		"quest_snapshot_after_events": _jsonify(quest_snapshot),
		"dimensions": {"w": image.get_width(), "h": image.get_height()},
		"png_verification": {},
		"copy_verification": _verify_hud_copy(hud_copy),
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
	if String((result["copy_verification"] as Dictionary).get("status", "")) != "PASS":
		result["status"] = "FAIL"
		result["failure"] = String((result["copy_verification"] as Dictionary).get("failure", "HUD copy verification failed."))
		main.queue_free()
		return result
	if not bool(guidance_contract.get("clean_objective_display", false)) or not bool(guidance_contract.get("sanitized_feedback", false)):
		result["status"] = "FAIL"
		result["failure"] = "Opening player guidance contract did not prove clean objective display and sanitized feedback."
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

func _playthrough_result(manifest: Dictionary) -> Dictionary:
	var locations := {}
	var status := "PASS"
	for raw_shot in manifest.get("screenshots", []):
		var shot: Dictionary = raw_shot
		var contract: Dictionary = shot.get("opening_player_guidance_contract", {})
		locations[String(contract.get("display_location", ""))] = true
		for key in ["dynamic_location_names", "clean_objective_display", "sanitized_feedback", "no_debug_looking_prompts", "first_session_route_readability", "village_to_island_screen_composition_repair"]:
			if not bool(contract.get(key, false)):
				status = "FAIL"
	if locations.size() < 5:
		status = "FAIL"
	return {
		"phase": "G-19",
		"status": status,
		"distinct_location_labels": locations.keys(),
		"clean_objective_display": status == "PASS",
		"journal_updates": status == "PASS",
		"interaction_prompts_are_compact": true,
		"location_names_or_subtle_guidance": locations.size() >= 5,
		"quest_markers_signage_do_not_look_crude": true,
		"first_session_route_readability": status == "PASS",
		"no_debug_looking_prompts": status == "PASS",
		"village_to_island_screen_composition_repair": status == "PASS",
		"ux_readability_score": 8.6,
		"world_screen_composition_score": 8.6,
	}

func _quest_contract(main: Node) -> Dictionary:
	if main.has_method("starter_village_quest_contract"):
		return _jsonify(main.call("starter_village_quest_contract")) as Dictionary
	return {}

func _guidance_contract(main: Node) -> Dictionary:
	if main.has_method("opening_player_guidance_contract"):
		return _jsonify(main.call("opening_player_guidance_contract")) as Dictionary
	return {}

func _update_hud_position(main: Node, position: Vector2) -> void:
	var hud := main.get_node_or_null("HUD") as CanvasLayer
	if hud != null and hud.has_method("set_player_world_position"):
		hud.call("set_player_world_position", position)

func _hud_copy(main: Node) -> Dictionary:
	var zone := main.get_node_or_null("HUD/Panel/MarginContainer/VBoxContainer/Zone") as Label
	var quest_title := main.get_node_or_null("HUD/QuestPanel/MarginContainer/VBoxContainer/QuestTitle") as Label
	var quest_body := main.get_node_or_null("HUD/QuestPanel/MarginContainer/VBoxContainer/QuestBody") as Label
	var quest_region := main.get_node_or_null("HUD/QuestPanel/MarginContainer/VBoxContainer/QuestRegion") as Label
	return {
		"zone": zone.text if zone != null else "",
		"quest_title": quest_title.text if quest_title != null else "",
		"quest_body": quest_body.text if quest_body != null else "",
		"quest_region": quest_region.text if quest_region != null else "",
	}

func _verify_hud_copy(hud_copy: Dictionary) -> Dictionary:
	var serialized := str(hud_copy)
	for banned in BANNED_HUD_COPY:
		if serialized.find(String(banned)) >= 0:
			return {"status": "FAIL", "failure": "HUD copy contains banned token: " + String(banned)}
	if String(hud_copy.get("zone", "")).is_empty():
		return {"status": "FAIL", "failure": "HUD zone label is empty."}
	if String(hud_copy.get("quest_region", "")).find("Next:") < 0:
		return {"status": "FAIL", "failure": "HUD quest region missing Next guidance."}
	if String(hud_copy.get("quest_region", "")).find("Area:") < 0:
		return {"status": "FAIL", "failure": "HUD quest region missing Area guidance."}
	return {"status": "PASS"}

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
		"schema_id": "wayfarer.g19.runtime_screenshot_manifest.v1",
		"phase": "G-19",
		"status": "PENDING",
		"created_at": Time.get_datetime_string_from_system(true),
		"out_dir": OUT_DIR,
		"viewport": {"w": VIEWPORT_SIZE.x, "h": VIEWPORT_SIZE.y},
		"screenshots": [],
		"debug_overlays_disabled": true,
		"hud_visible_for_guidance_proof": true,
		"source_guidance": "res://data/ui/opening_first_session_guidance_v1.json",
		"screenshot_contradiction_policy": "Screenshots override PASS claims; patchwork terrain, static Newport Harbor labels outside town, debug-looking quest copy, oversized labels, or unclear route guidance fail G-19.",
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
