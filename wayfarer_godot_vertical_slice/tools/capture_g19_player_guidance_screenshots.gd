extends SceneTree

const MAIN_SCENE := preload("res://scenes/Main.tscn")

const OUT_DIR := "res://artifacts/review/g19_player_guidance_screenshots"
const MANIFEST_FILENAME := "g19_player_guidance_screenshot_manifest.json"
const VIEWPORT_SIZE := Vector2i(1600, 1000)
const INITIAL_WAIT_FRAMES := 36
const CAPTURE_WAIT_FRAMES := 12

const CAPTURES := [
	{
		"filename": "g19_01_arrival_journal_route.png",
		"viewpoint_id": "arrival_journal_route",
		"label": "arrival journal route / first objective names the harborfront route to the Counting House",
		"player_position": Vector2(430.0, 920.0),
		"camera_zoom": Vector2(1.38, 1.38),
		"player_direction": "up",
		"player_moving": false,
		"player_frame": 0,
		"target_id": "",
		"events": [],
		"dialogue": "",
		"suppress_prompt": true
	},
	{
		"filename": "g19_02_counting_house_route_prompt.png",
		"viewpoint_id": "counting_house_route_prompt",
		"label": "counting house route prompt / compact interaction prompt sits on the source-derived civic route",
		"player_position": Vector2(1080.0, 585.0),
		"camera_zoom": Vector2(1.38, 1.38),
		"player_direction": "up",
		"player_moving": false,
		"player_frame": 0,
		"target_id": "EdrinVale",
		"events": [],
		"dialogue": "",
		"suppress_prompt": false
	},
	{
		"filename": "g19_03_counting_house_journal_update.png",
		"viewpoint_id": "counting_house_journal_update",
		"label": "counting house journal update / objective advances toward wharf, merchant row, or notice board",
		"player_position": Vector2(1080.0, 585.0),
		"camera_zoom": Vector2(1.38, 1.38),
		"player_direction": "up",
		"player_moving": false,
		"player_frame": 0,
		"target_id": "EdrinVale",
		"events": ["edrin"],
		"dialogue": "Edrin Vale: The missing line is not a mistake. Ask the wharf, merchant row, or the notice board.",
		"suppress_prompt": false
	},
	{
		"filename": "g19_04_wharf_lantern_guidance.png",
		"viewpoint_id": "wharf_lantern_guidance",
		"label": "wharf lantern guidance / harbor work route reads without debug arrows",
		"player_position": Vector2(465.0, 1025.0),
		"camera_zoom": Vector2(1.34, 1.34),
		"player_direction": "down",
		"player_moving": false,
		"player_frame": 0,
		"target_id": "mara_pike_dockworker",
		"events": ["mara"],
		"dialogue": "Mara Pike: Cargo does not vanish from a pier this busy. Watch the lanterns.",
		"suppress_prompt": false
	},
	{
		"filename": "g19_05_tavern_whisper_route.png",
		"viewpoint_id": "tavern_whisper_route",
		"label": "tavern whisper route / route hint pulls the player to the Tavern Inn landmark",
		"player_position": Vector2(500.0, 585.0),
		"camera_zoom": Vector2(1.38, 1.38),
		"player_direction": "up",
		"player_moving": false,
		"player_frame": 0,
		"target_id": "bess_armitage_tavern_keeper",
		"events": ["bess"],
		"dialogue": "Bess Armitage: Third Toast, then no names.",
		"suppress_prompt": false
	},
	{
		"filename": "g19_06_commercial_branch_guidance.png",
		"viewpoint_id": "commercial_branch_guidance",
		"label": "commercial branch guidance / merchant-row path stays readable from the avenue",
		"player_position": Vector2(815.0, 585.0),
		"camera_zoom": Vector2(1.38, 1.38),
		"player_direction": "up",
		"player_moving": false,
		"player_frame": 0,
		"target_id": "honor_finch_merchant_shopkeeper",
		"events": ["honor"],
		"dialogue": "Honor Finch: If you ask who bought the silence, ask who could afford it twice.",
		"suppress_prompt": false
	},
	{
		"filename": "g19_07_rear_service_lane_secret.png",
		"viewpoint_id": "rear_service_lane_secret",
		"label": "rear service lane secret / location name and journal route expose the hidden path without crude markers",
		"player_position": Vector2(610.0, 365.0),
		"camera_zoom": Vector2(1.38, 1.38),
		"player_direction": "left",
		"player_moving": false,
		"player_frame": 0,
		"target_id": "silas_crowe_suspicious_patron",
		"events": ["silas"],
		"dialogue": "Silas Crowe: Watch the rear lane after the second lantern.",
		"suppress_prompt": false
	},
	{
		"filename": "g19_08_island_exit_guidance.png",
		"viewpoint_id": "island_exit_guidance",
		"label": "island exit guidance / east guidepost and journal route show how town continues",
		"player_position": Vector2(1880.0, 610.0),
		"camera_zoom": Vector2(1.25, 1.25),
		"player_direction": "right",
		"player_moving": true,
		"player_frame": 2,
		"target_id": "",
		"events": ["edrin", "isla"],
		"dialogue": "",
		"suppress_prompt": true
	},
	{
		"filename": "g19_09_journal_reward_return_route.png",
		"viewpoint_id": "journal_reward_return_route",
		"label": "journal reward return route / late quest guidance preserves return/report clarity",
		"player_position": Vector2(1100.0, 600.0),
		"camera_zoom": Vector2(1.38, 1.38),
		"player_direction": "up",
		"player_moving": false,
		"player_frame": 0,
		"target_id": "EdrinVale",
		"events": ["tomas", "annelise", "edrin"],
		"dialogue": "Edrin Vale: Keep that proof hidden until dawn.",
		"suppress_prompt": false
	},
	{
		"filename": "g19_10_debug_disabled_guidance_view.png",
		"viewpoint_id": "debug_disabled_guidance_view",
		"label": "debug disabled guidance view / HUD, journal, prompts, and route names are player-facing rather than debug labels",
		"player_position": Vector2(1045.0, 645.0),
		"camera_zoom": Vector2(1.38, 1.38),
		"player_direction": "up",
		"player_moving": true,
		"player_frame": 1,
		"target_id": "",
		"events": [],
		"dialogue": "",
		"suppress_prompt": true
	},
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
		_write_manifest(manifest)
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
	if main.has_method("set_starter_village_ambient_barks_enabled"):
		main.call("set_starter_village_ambient_barks_enabled", false)
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

	manifest["g19_player_guidance_contract_initial"] = _jsonify(main.call("player_guidance_polish_contract") if main.has_method("player_guidance_polish_contract") else {})
	manifest["quest_contract_initial"] = _jsonify(main.call("starter_village_quest_contract") if main.has_method("starter_village_quest_contract") else {})
	manifest["debug_overlays_disabled"] = true
	manifest["hud_visible_for_guidance_proof"] = true
	manifest["source_runtime_layout"] = "wayfarer_godot_vertical_slice/data/world_layout/g19s_newport_runtime_reconstruction_v1.json"
	manifest["guidance_source"] = "wayfarer_godot_vertical_slice/data/ux/g19_player_guidance_map_journal_interaction_v1.json"

	for capture in CAPTURES:
		var file_result := await _capture_one(capture, main, player, camera)
		manifest["screenshots"].append(file_result)
		if file_result.get("status", "") != "PASS":
			return _fail(manifest, String(file_result.get("failure", "Screenshot capture failed.")))

	manifest["g19_player_guidance_contract_final"] = _jsonify(main.call("player_guidance_polish_contract") if main.has_method("player_guidance_polish_contract") else {})
	manifest["quest_contract_final"] = _jsonify(main.call("starter_village_quest_contract") if main.has_method("starter_village_quest_contract") else {})
	manifest["hud_journal_contract_final"] = _jsonify(_journal_contract(main))
	manifest["status"] = "PASS"
	_write_manifest(manifest)
	print("PASS: G-19 player guidance screenshots -> ", ProjectSettings.globalize_path(OUT_DIR))
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
		"label": capture["label"],
		"path": output_path,
		"absolute_path": ProjectSettings.globalize_path(output_path),
		"player_position": _vector2_to_dict(player_position),
		"camera_zoom": _vector2_to_dict(capture["camera_zoom"]),
		"dimensions": {"w": image.get_width(), "h": image.get_height()},
		"prompt_visible": prompt_label != null and prompt_label.visible,
		"prompt_text": prompt_label.text if prompt_label != null else "",
		"journal_objective_contract": _jsonify(_journal_contract(main)),
		"player_guidance_contract": _jsonify(main.call("player_guidance_polish_contract") if main.has_method("player_guidance_polish_contract") else {}),
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
		"schema_id": "wayfarer.g19.player_guidance_screenshot_manifest.v1",
		"phase": "G-19",
		"out_dir": OUT_DIR,
		"viewport": {"w": VIEWPORT_SIZE.x, "h": VIEWPORT_SIZE.y},
		"screenshots": [],
		"status": "PENDING",
	}


func _fail(manifest: Dictionary, message: String) -> int:
	manifest["status"] = "FAIL"
	manifest["failure"] = message
	_write_manifest(manifest)
	push_error(message)
	return 1


func _write_manifest(manifest: Dictionary) -> void:
	var manifest_path := "%s/%s" % [OUT_DIR, MANIFEST_FILENAME]
	var file := FileAccess.open(manifest_path, FileAccess.WRITE)
	if file == null:
		push_error("Could not open manifest for writing: " + manifest_path)
		return
	file.store_string(JSON.stringify(_jsonify(manifest), "\t"))
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
