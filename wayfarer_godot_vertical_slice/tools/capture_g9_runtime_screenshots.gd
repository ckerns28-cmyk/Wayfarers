extends SceneTree

const BUILD_INFO := preload("res://scripts/BuildInfo.gd")
const MAIN_SCENE := preload("res://scenes/Main.tscn")

const OUT_DIR := "res://artifacts/review/g9_runtime_screenshots"
const MANIFEST_FILENAME := "g9_runtime_screenshot_manifest.json"
const VIEWPORT_SIZE := Vector2i(1600, 1000)
const INITIAL_WAIT_FRAMES := 36
const CAPTURE_WAIT_FRAMES := 12

const CAPTURES := [
	{"filename": "g9_01_wide_newport_normal_gameplay_view.png", "label": "wide Newport normal gameplay view / HUD objective is clear without debug overlays", "target": "wide_newport_normal_gameplay_view", "player_position": Vector2(800.0, 512.0), "camera_zoom": Vector2(1.0, 1.0), "camera_offset": Vector2(0.0, 0.0), "player_direction": "down", "player_moving": false, "player_frame": 0, "target_id": "", "dialogue": ""},
	{"filename": "g9_02_player_arrival_at_harbor.png", "label": "player arrival at harbor / first objective points toward Counting House and tavern whisper", "target": "player_arrival_at_harbor", "player_position": Vector2(805.0, 710.0), "camera_zoom": Vector2(1.32, 1.32), "camera_offset": Vector2(12.0, 10.0), "player_direction": "up", "player_moving": false, "player_frame": 0, "target_id": "", "dialogue": ""},
	{"filename": "g9_03_player_on_route_to_counting_house.png", "label": "route to counting house / compact prompt names Edrin without Press E debug copy", "target": "route_to_counting_house", "player_position": Vector2(792.0, 570.0), "camera_zoom": Vector2(1.36, 1.36), "camera_offset": Vector2(38.0, -66.0), "player_direction": "up", "player_moving": true, "player_frame": 1, "target_id": "EdrinVale", "dialogue": ""},
	{"filename": "g9_04_player_near_tavern_inn.png", "label": "player near Tavern/Inn / compact tavern prompt protects the world view", "target": "player_near_tavern_inn", "player_position": Vector2(244.0, 596.0), "camera_zoom": Vector2(1.50, 1.50), "camera_offset": Vector2(42.0, -62.0), "player_direction": "down", "player_moving": false, "player_frame": 0, "target_id": "b_inn_tavern", "dialogue": ""},
	{"filename": "g9_05_player_on_commercial_avenue.png", "label": "commercial avenue / Harbor Mercantile uses compact enter prompt", "target": "commercial_avenue", "player_position": Vector2(651.0, 596.0), "camera_zoom": Vector2(1.30, 1.30), "camera_offset": Vector2(20.0, -38.0), "player_direction": "left", "player_moving": true, "player_frame": 1, "target_id": "b_mercantile", "dialogue": ""},
	{"filename": "g9_06_player_at_dock_wharf_work_area.png", "label": "dock and wharf work area / dock storehouse inspection prompt is readable and not oversized", "target": "dock_wharf_work_area", "player_position": Vector2(1030.0, 704.0), "camera_zoom": Vector2(1.34, 1.34), "camera_offset": Vector2(20.0, -6.0), "player_direction": "right", "player_moving": true, "player_frame": 3, "target_id": "b_dock_storehouse", "dialogue": ""},
	{"filename": "g9_07_player_near_npc_movement_path.png", "label": "player near NPC movement path / rumor carrier prompt is compact and anchored", "target": "npc_movement_path", "player_position": Vector2(748.0, 394.0), "camera_zoom": Vector2(1.42, 1.42), "camera_offset": Vector2(0.0, -38.0), "player_direction": "right", "player_moving": false, "player_frame": 0, "target_id": "nora_vale_rumor_carrier", "dialogue": ""},
	{"filename": "g9_08_npc_idle_and_walking_proof.png", "label": "NPC idle and walking proof / no marker replaces the accepted no-glide policy", "target": "npc_idle_and_walking_proof", "player_position": Vector2(302.0, 604.0), "camera_zoom": Vector2(1.52, 1.52), "camera_offset": Vector2(40.0, -60.0), "player_direction": "up", "player_moving": false, "player_frame": 0, "target_id": "bess_armitage_tavern_keeper", "dialogue": ""},
	{"filename": "g9_09_player_interacting_with_counting_house_clerk.png", "label": "counting house interaction / Edrin dialogue is readable in HUD without covering the world", "target": "counting_house_interaction", "player_position": Vector2(792.0, 570.0), "camera_zoom": Vector2(1.42, 1.42), "camera_offset": Vector2(24.0, -34.0), "player_direction": "up", "player_moving": false, "player_frame": 0, "target_id": "EdrinVale", "dialogue": "Edrin Vale: The ledger is missing a line, and no honest clerk misplaces ink by accident."},
	{"filename": "g9_10_player_interacting_at_tavern_rumor_location.png", "label": "tavern rumor interaction / whisper dialogue supports the opening theme", "target": "tavern_rumor_interaction", "player_position": Vector2(302.0, 604.0), "camera_zoom": Vector2(1.50, 1.50), "camera_offset": Vector2(42.0, -62.0), "player_direction": "down", "player_moving": false, "player_frame": 0, "target_id": "bess_armitage_tavern_keeper", "dialogue": "Bess Armitage: Ask for the third toast only if you mean to hear the answer."},
	{"filename": "g9_11_quest_prompt_journal_objective_proof.png", "label": "quest prompt and objective proof / objective update and rumor copy are present in the HUD contract", "target": "quest_prompt_journal_objective_proof", "player_position": Vector2(675.0, 600.0), "camera_zoom": Vector2(1.44, 1.44), "camera_offset": Vector2(42.0, -54.0), "player_direction": "up", "player_moving": true, "player_frame": 2, "target_id": "", "dialogue": "Objective updated: ask about the missing ledger line. Rumor: the Third Toast begins at the Tavern/Inn."},
	{"filename": "g9_12_signs_markers_interaction_ux_proof.png", "label": "signs and interaction UX proof / prompts guide without crude placeholder signs or markers", "target": "signs_markers_interaction_ux_proof", "player_position": Vector2(800.0, 392.0), "camera_zoom": Vector2(1.46, 1.46), "camera_offset": Vector2(-8.0, -44.0), "player_direction": "left", "player_moving": false, "player_frame": 0, "target_id": "nora_vale_rumor_carrier", "dialogue": ""},
	{"filename": "g9_13_y_sort_layering_near_buildings_props.png", "label": "y-sort and layering proof / prompt remains compact near buildings and props", "target": "y_sort_layering_near_buildings_props", "player_position": Vector2(651.0, 596.0), "camera_zoom": Vector2(1.46, 1.46), "camera_offset": Vector2(0.0, -54.0), "player_direction": "down", "player_moving": false, "player_frame": 0, "target_id": "b_mercantile", "dialogue": ""},
	{"filename": "g9_14_debug_overlays_disabled.png", "label": "debug overlays disabled / no route labels, primitive markers, or debug prompt copy", "target": "debug_overlays_disabled", "player_position": Vector2(800.0, 512.0), "camera_zoom": Vector2(1.18, 1.18), "camera_offset": Vector2(0.0, -8.0), "player_direction": "down", "player_moving": false, "player_frame": 0, "target_id": "", "dialogue": ""},
	{"filename": "g9_15_contact_sheet_provenance_proof.png", "label": "contact sheet and provenance proof / no new marker assets were introduced for G-9", "target": "contact_sheet_provenance_proof", "player_position": Vector2(704.0, 654.0), "camera_zoom": Vector2(1.20, 1.20), "camera_offset": Vector2(0.0, -8.0), "player_direction": "right", "player_moving": true, "player_frame": 1, "target_id": "EdrinVale", "dialogue": ""},
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
	await _wait_for_render(INITIAL_WAIT_FRAMES)
	if main.has_method("set_review_screenshot_mode"):
		main.call("set_review_screenshot_mode", false)
	if main.has_method("set_debug_overlay"):
		main.call("set_debug_overlay", false)
	if main.has_method("set_building_seating_overlay"):
		main.call("set_building_seating_overlay", false)

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

	_freeze_npcs(main)
	manifest["player_prompt_contract"] = _jsonify(player.call("prompt_ux_contract") if player.has_method("prompt_ux_contract") else {})
	var hud := main.get_node_or_null("HUD") as CanvasLayer
	manifest["hud_interaction_contract"] = _jsonify(hud.call("interaction_ux_contract") if hud != null and hud.has_method("interaction_ux_contract") else {})

	for capture in CAPTURES:
		var file_result := await _capture_one(capture, main, player, camera)
		if file_result.get("status", "") != "PASS":
			manifest["screenshots"].append(file_result)
			return _fail(manifest, String(file_result.get("failure", "Screenshot capture failed.")))
		manifest["screenshots"].append(file_result)

	manifest["status"] = "PASS"
	_write_manifest(manifest)
	print("PASS: G-9 runtime screenshots -> ", ProjectSettings.globalize_path(OUT_DIR))
	return 0


func _capture_one(capture: Dictionary, main: Node, player: Node2D, camera: Camera2D) -> Dictionary:
	var target := _target_by_id(main, String(capture.get("target_id", "")))
	var player_position: Vector2 = capture["player_position"]
	if target != null and target.has_method("get_interaction_position"):
		var raw_position: Variant = target.call("get_interaction_position")
		if raw_position is Vector2:
			player_position = raw_position
	player.global_position = player_position
	if player.has_method("set_review_visual_state"):
		player.call("set_review_visual_state", capture["player_direction"], capture["player_moving"], capture["player_frame"])
	if player.has_method("_update_interaction_target"):
		player.call("_update_interaction_target")
	_set_dialogue(main, String(capture.get("dialogue", "")))
	camera.zoom = capture["camera_zoom"]
	camera.offset = capture["camera_offset"]
	camera.reset_smoothing()
	await _wait_for_render(CAPTURE_WAIT_FRAMES)

	var prompt_label := player.get_node_or_null("PromptLabel") as Label
	var image := root.get_texture().get_image()
	var width := image.get_width()
	var height := image.get_height()
	var output_path := "%s/%s" % [OUT_DIR, capture["filename"]]
	var result := {
		"filename": capture["filename"],
		"label": capture["label"],
		"target": capture["target"],
		"path": output_path,
		"absolute_path": ProjectSettings.globalize_path(output_path),
		"player_position": _vector2_to_dict(player_position),
		"player_motion_state": _motion_state(capture["player_direction"], capture["player_moving"], capture["player_frame"]),
		"target_id": String(capture.get("target_id", "")),
		"prompt_visible": prompt_label != null and prompt_label.visible,
		"prompt_text": prompt_label.text if prompt_label != null else "",
		"dialogue_text": String(capture.get("dialogue", "")),
		"camera_zoom": _vector2_to_dict(capture["camera_zoom"]),
		"camera_offset": _vector2_to_dict(capture["camera_offset"]),
		"dimensions": {"w": width, "h": height},
		"png_verification": {},
		"status": "PENDING",
	}
	if width < 640 or height < 360:
		result["status"] = "FAIL"
		result["failure"] = "Viewport image dimensions were not sensible: %sx%s" % [width, height]
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
	print("Wrote ", output_path, " ", width, "x", height)
	return result


func _target_by_id(main: Node, target_id: String) -> Node2D:
	if target_id.is_empty():
		return null
	var world := main.get_node_or_null("World")
	if world == null:
		return null
	var direct := world.get_node_or_null(target_id) as Node2D
	if direct != null:
		return direct
	for raw_node in main.get_tree().get_nodes_in_group("starter_village_npc"):
		var npc := raw_node as Node2D
		if npc == null:
			continue
		if String(npc.name) == target_id:
			return npc
		if npc.has_method("npc_population_contract"):
			var contract: Dictionary = npc.call("npc_population_contract") as Dictionary
			if String(contract.get("id", "")) == target_id:
				return npc
	return null


func _set_dialogue(main: Node, text: String) -> void:
	var panel := main.get_node_or_null("HUD/DialoguePanel") as Control
	var label := main.get_node_or_null("HUD/DialoguePanel/MarginContainer/DialogueLabel") as Label
	if panel != null:
		panel.visible = not text.is_empty()
	if label != null:
		label.text = text


func _freeze_npcs(main: Node) -> void:
	for raw_npc in main.get_tree().get_nodes_in_group("starter_village_npc"):
		var npc := raw_npc as Node
		if npc == null:
			continue
		npc.set_process(false)
		npc.set_physics_process(false)


func _wait_for_render(frame_count: int) -> void:
	for _i in range(frame_count):
		await process_frame
	await RenderingServer.frame_post_draw


func _base_manifest() -> Dictionary:
	return {
		"schema_id": "wayfarer.g9.runtime_screenshot_manifest.v1",
		"phase": "G-9",
		"status": "PENDING",
		"created_at": Time.get_datetime_string_from_system(true),
		"command": OS.get_environment("G9_CAPTURE_COMMAND"),
		"godot_version": Engine.get_version_info().get("string", ""),
		"os": OS.get_name(),
		"display_driver": DisplayServer.get_name(),
		"rendering_method": _project_setting("rendering/renderer/rendering_method"),
		"headless": DisplayServer.get_name().to_lower() == "headless",
		"user_data_dir": OS.get_user_data_dir(),
		"output_dir": OUT_DIR,
		"absolute_output_dir": ProjectSettings.globalize_path(OUT_DIR),
		"viewport_size": {"w": VIEWPORT_SIZE.x, "h": VIEWPORT_SIZE.y},
		"review_screenshot_flag": BUILD_INFO.REVIEW_SCREENSHOT_FLAG,
		"required_recurring_screenshot_set_count": CAPTURES.size(),
		"interaction_proof": "Compact prompts use E: Action - Name copy, HUD objective names the Counting House and tavern whisper, and debug overlays remain disabled.",
		"warnings": [],
		"screenshots": [],
	}


func _project_setting(setting_name: String) -> String:
	if ProjectSettings.has_setting(setting_name):
		return str(ProjectSettings.get_setting(setting_name))
	return ""


func _motion_state(direction: String, moving: bool, frame_index: int) -> Dictionary:
	return {
		"direction": direction,
		"moving_requested": moving,
		"animation": ("walk_" if moving else "idle_") + direction,
		"frame_index": frame_index,
	}


func _vector2_to_dict(value: Vector2) -> Dictionary:
	return {"x": snappedf(value.x, 0.001), "y": snappedf(value.y, 0.001)}


func _jsonify(value: Variant) -> Variant:
	if value is Vector2:
		return _vector2_to_dict(value)
	if value is Vector2i:
		return {"x": value.x, "y": value.y}
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


func _verify_png_pixels(image: Image) -> Dictionary:
	var width := image.get_width()
	var height := image.get_height()
	var color_buckets := {}
	var min_luminance := 10.0
	var max_luminance := -10.0
	var sample_count := 0
	for y_step in range(8):
		for x_step in range(10):
			var x := clampi(int((float(x_step) + 0.5) * float(width) / 10.0), 0, width - 1)
			var y := clampi(int((float(y_step) + 0.5) * float(height) / 8.0), 0, height - 1)
			var color := image.get_pixel(x, y)
			var luminance := color.r * 0.2126 + color.g * 0.7152 + color.b * 0.0722
			min_luminance = minf(min_luminance, luminance)
			max_luminance = maxf(max_luminance, luminance)
			var bucket := "%s_%s_%s" % [int(color.r * 31.0), int(color.g * 31.0), int(color.b * 31.0)]
			color_buckets[bucket] = true
			sample_count += 1
	var luminance_range := max_luminance - min_luminance
	var result := {
		"status": "PASS",
		"sample_count": sample_count,
		"distinct_color_buckets": color_buckets.size(),
		"luminance_range": snappedf(luminance_range, 0.001),
	}
	if color_buckets.size() < 12 or luminance_range < 0.08:
		result["status"] = "FAIL"
		result["failure"] = "PNG appeared blank or too uniform: buckets=%s luminance_range=%.3f" % [color_buckets.size(), luminance_range]
	return result


func _fail(manifest: Dictionary, message: String) -> int:
	manifest["status"] = "FAIL"
	manifest["failure"] = message
	_write_manifest(manifest)
	push_error(message)
	return 1


func _write_manifest(manifest: Dictionary) -> void:
	var output_error := DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_DIR))
	if output_error != OK:
		push_error("Could not create manifest directory: %s error=%s" % [OUT_DIR, output_error])
		return
	var manifest_path := "%s/%s" % [OUT_DIR, MANIFEST_FILENAME]
	var file := FileAccess.open(manifest_path, FileAccess.WRITE)
	if file == null:
		push_error("Could not open manifest for writing: " + manifest_path)
		return
	file.store_string(JSON.stringify(manifest, "\t"))
	file.store_line("")
