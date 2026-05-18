extends SceneTree

const BUILD_INFO := preload("res://scripts/BuildInfo.gd")
const MAIN_SCENE := preload("res://scenes/Main.tscn")

const OUT_DIR := "res://artifacts/review/g8_runtime_screenshots"
const MANIFEST_FILENAME := "g8_runtime_screenshot_manifest.json"
const VIEWPORT_SIZE := Vector2i(1600, 1000)
const INITIAL_WAIT_FRAMES := 36
const CAPTURE_WAIT_FRAMES := 12

const CAPTURES := [
	{"filename": "g8_01_wide_newport_normal_gameplay_view.png", "label": "wide Newport normal gameplay view / G-8 grounded player and stationary NPC motion foundation in the authored town", "target": "wide_newport_normal_gameplay_view", "player_position": Vector2(800.0, 512.0), "camera_zoom": Vector2(1.0, 1.0), "camera_offset": Vector2(0.0, 0.0), "player_direction": "down", "player_moving": false, "player_frame": 0, "edrin_position": Vector2(418.0, 666.0), "edrin_direction": "down", "edrin_moving": false, "edrin_frame": 0},
	{"filename": "g8_02_player_arrival_at_harbor.png", "label": "player arrival at harbor / grounded idle state at landfall with foot anchor and shadow", "target": "player_arrival_at_harbor", "player_position": Vector2(805.0, 710.0), "camera_zoom": Vector2(1.32, 1.32), "camera_offset": Vector2(12.0, 10.0), "player_direction": "up", "player_moving": false, "player_frame": 0, "edrin_position": Vector2(418.0, 666.0), "edrin_direction": "down", "edrin_moving": false, "edrin_frame": 0},
	{"filename": "g8_03_player_route_to_counting_house_walk_up.png", "label": "route to counting house / player walk_up animation proof on uphill town route", "target": "route_to_counting_house", "player_position": Vector2(704.0, 520.0), "camera_zoom": Vector2(1.36, 1.36), "camera_offset": Vector2(38.0, -66.0), "player_direction": "up", "player_moving": true, "player_frame": 1, "edrin_position": Vector2(418.0, 666.0), "edrin_direction": "down", "edrin_moving": false, "edrin_frame": 0},
	{"filename": "g8_04_player_walk_down_grounded.png", "label": "player walk_down proof / grounded feet and cadence-aligned frame", "target": "player_walk_down_grounded", "player_position": Vector2(342.0, 606.0), "camera_zoom": Vector2(1.50, 1.50), "camera_offset": Vector2(42.0, -62.0), "player_direction": "down", "player_moving": true, "player_frame": 2, "edrin_position": Vector2(418.0, 666.0), "edrin_direction": "down", "edrin_moving": false, "edrin_frame": 0},
	{"filename": "g8_05_player_walk_left_commercial_avenue.png", "label": "commercial avenue / player walk_left state remains foot-anchored against lot frontages", "target": "commercial_avenue", "player_position": Vector2(1010.0, 608.0), "camera_zoom": Vector2(1.30, 1.30), "camera_offset": Vector2(20.0, -38.0), "player_direction": "left", "player_moving": true, "player_frame": 1, "edrin_position": Vector2(418.0, 666.0), "edrin_direction": "down", "edrin_moving": false, "edrin_frame": 0},
	{"filename": "g8_06_player_walk_right_dock_work_area.png", "label": "dock and wharf work area / player walk_right state on working waterfront", "target": "dock_wharf_work_area", "player_position": Vector2(1030.0, 704.0), "camera_zoom": Vector2(1.34, 1.34), "camera_offset": Vector2(20.0, -6.0), "player_direction": "right", "player_moving": true, "player_frame": 3, "edrin_position": Vector2(418.0, 666.0), "edrin_direction": "down", "edrin_moving": false, "edrin_frame": 0},
	{"filename": "g8_07_npc_movement_path_stationary_no_drift.png", "label": "NPC movement path area / Edrin is grounded and stationary until a dedicated walk sheet ships", "target": "npc_movement_path_area", "player_position": Vector2(420.0, 690.0), "camera_zoom": Vector2(1.42, 1.42), "camera_offset": Vector2(32.0, -22.0), "player_direction": "right", "player_moving": false, "player_frame": 0, "edrin_position": Vector2(480.0, 660.0), "edrin_direction": "down", "edrin_moving": false, "edrin_frame": 0},
	{"filename": "g8_08_npc_idle_and_stationary_walk_request_proof.png", "label": "NPC idle and walking proof / walk request resolves to grounded idle because route walking is disabled, preventing static-sprite glide", "target": "npc_idle_and_walking_proof", "player_position": Vector2(1218.0, 690.0), "camera_zoom": Vector2(1.42, 1.42), "camera_offset": Vector2(0.0, -20.0), "player_direction": "left", "player_moving": false, "player_frame": 0, "edrin_position": Vector2(1238.0, 664.0), "edrin_direction": "left", "edrin_moving": true, "edrin_frame": 0},
	{"filename": "g8_09_counting_house_interaction_grounding.png", "label": "counting house interaction area / player idle_up state is grounded at the civic frontage", "target": "counting_house_interaction_area", "player_position": Vector2(704.0, 392.0), "camera_zoom": Vector2(1.42, 1.42), "camera_offset": Vector2(24.0, -34.0), "player_direction": "up", "player_moving": false, "player_frame": 0, "edrin_position": Vector2(418.0, 666.0), "edrin_direction": "down", "edrin_moving": false, "edrin_frame": 0},
	{"filename": "g8_10_tavern_rumor_location_grounding.png", "label": "tavern rumor location area / player idle_down state reads at the warm rumor hub threshold", "target": "tavern_rumor_location_area", "player_position": Vector2(342.0, 606.0), "camera_zoom": Vector2(1.50, 1.50), "camera_offset": Vector2(42.0, -62.0), "player_direction": "down", "player_moving": false, "player_frame": 0, "edrin_position": Vector2(418.0, 666.0), "edrin_direction": "down", "edrin_moving": false, "edrin_frame": 0},
	{"filename": "g8_11_objective_route_readability_motion.png", "label": "objective route readability area / player walk_up proof keeps the counting-house route readable", "target": "objective_route_readability_area", "player_position": Vector2(675.0, 600.0), "camera_zoom": Vector2(1.44, 1.44), "camera_offset": Vector2(42.0, -54.0), "player_direction": "up", "player_moving": true, "player_frame": 2, "edrin_position": Vector2(418.0, 666.0), "edrin_direction": "down", "edrin_moving": false, "edrin_frame": 0},
	{"filename": "g8_12_signs_markers_interaction_ux_grounded.png", "label": "signs and interaction UX area / no crude motion markers or debug placeholders in normal play", "target": "signs_markers_interaction_ux_area", "player_position": Vector2(800.0, 392.0), "camera_zoom": Vector2(1.46, 1.46), "camera_offset": Vector2(-8.0, -44.0), "player_direction": "left", "player_moving": false, "player_frame": 0, "edrin_position": Vector2(418.0, 666.0), "edrin_direction": "down", "edrin_moving": false, "edrin_frame": 0},
	{"filename": "g8_13_y_sort_layering_character_feet.png", "label": "y-sort and layering near buildings / player feet remain grounded against shop-row props", "target": "y_sort_layering_near_buildings", "player_position": Vector2(1018.0, 596.0), "camera_zoom": Vector2(1.46, 1.46), "camera_offset": Vector2(0.0, -54.0), "player_direction": "down", "player_moving": false, "player_frame": 0, "edrin_position": Vector2(418.0, 666.0), "edrin_direction": "down", "edrin_moving": false, "edrin_frame": 0},
	{"filename": "g8_14_debug_overlays_disabled.png", "label": "debug overlays disabled / normal-play proof has no route labels, boxes, or primitive motion placeholders", "target": "debug_overlays_disabled", "player_position": Vector2(800.0, 512.0), "camera_zoom": Vector2(1.18, 1.18), "camera_offset": Vector2(0.0, -8.0), "player_direction": "down", "player_moving": false, "player_frame": 0, "edrin_position": Vector2(418.0, 666.0), "edrin_direction": "down", "edrin_moving": false, "edrin_frame": 0},
	{"filename": "g8_15_provenance_character_motion_contract.png", "label": "provenance proof / character motion uses accepted G-4.22R atelier atlases plus G-8 grounded movement contracts", "target": "provenance_character_motion_contract", "player_position": Vector2(704.0, 654.0), "camera_zoom": Vector2(1.20, 1.20), "camera_offset": Vector2(0.0, -8.0), "player_direction": "right", "player_moving": true, "player_frame": 1, "edrin_position": Vector2(418.0, 666.0), "edrin_direction": "right", "edrin_moving": false, "edrin_frame": 0},
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
		main.call("set_review_screenshot_mode", true)
		manifest["hud_hidden"] = true
	else:
		manifest["warnings"].append("Main scene did not expose set_review_screenshot_mode.")

	var player := main.get_node_or_null("World/Player") as Node2D
	if player == null:
		player = main.get_node_or_null("Player") as Node2D
	if player == null:
		return _fail(manifest, "Player node not found.")
	player.set_physics_process(false)
	player.set_process(false)
	var prompt_label := player.get_node_or_null("PromptLabel") as CanvasItem
	if prompt_label != null:
		prompt_label.visible = false
	var camera := player.get_node_or_null("Camera2D") as Camera2D
	if camera == null:
		return _fail(manifest, "Player Camera2D node not found.")
	camera.enabled = true
	camera.position_smoothing_enabled = false
	camera.limit_smoothed = false
	camera.make_current()

	var edrin := main.get_node_or_null("World/EdrinVale") as Node2D
	if edrin != null:
		edrin.set_process(false)
		edrin.set_physics_process(false)
	manifest["player_motion_contract"] = _jsonify(player.call("character_motion_contract") if player.has_method("character_motion_contract") else {})
	manifest["npc_motion_contract"] = _jsonify(edrin.call("motion_foundation_contract") if edrin != null and edrin.has_method("motion_foundation_contract") else {})
	manifest["npc_route_walking_enabled"] = bool(edrin.call("is_route_walking_enabled")) if edrin != null and edrin.has_method("is_route_walking_enabled") else false

	for capture in CAPTURES:
		var file_result := await _capture_one(capture, player, edrin, camera)
		if file_result.get("status", "") != "PASS":
			manifest["screenshots"].append(file_result)
			return _fail(manifest, String(file_result.get("failure", "Screenshot capture failed.")))
		manifest["screenshots"].append(file_result)

	manifest["status"] = "PASS"
	_write_manifest(manifest)
	print("PASS: G-8 runtime screenshots -> ", ProjectSettings.globalize_path(OUT_DIR))
	return 0


func _capture_one(capture: Dictionary, player: Node2D, edrin: Node2D, camera: Camera2D) -> Dictionary:
	player.global_position = capture["player_position"]
	if player.has_method("set_review_visual_state"):
		player.call("set_review_visual_state", capture["player_direction"], capture["player_moving"], capture["player_frame"])
	if edrin != null:
		edrin.global_position = capture["edrin_position"]
		if edrin.has_method("set_review_motion_state"):
			edrin.call("set_review_motion_state", capture["edrin_direction"], capture["edrin_moving"], capture["edrin_frame"])
	camera.zoom = capture["camera_zoom"]
	camera.offset = capture["camera_offset"]
	camera.reset_smoothing()
	await _wait_for_render(CAPTURE_WAIT_FRAMES)

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
		"player_position": _vector2_to_dict(capture["player_position"]),
		"player_motion_state": _motion_state(capture["player_direction"], capture["player_moving"], capture["player_frame"]),
		"edrin_position": _vector2_to_dict(capture["edrin_position"]),
		"edrin_motion_state": _motion_state(capture["edrin_direction"], capture["edrin_moving"], capture["edrin_frame"]),
		"edrin_route_walking_expected": false,
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


func _wait_for_render(frame_count: int) -> void:
	for _i in range(frame_count):
		await process_frame
	await RenderingServer.frame_post_draw


func _base_manifest() -> Dictionary:
	return {
		"schema_id": "wayfarer.g8.runtime_screenshot_manifest.v1",
		"phase": "G-8",
		"status": "PENDING",
		"created_at": Time.get_datetime_string_from_system(true),
		"command": OS.get_environment("G8_CAPTURE_COMMAND"),
		"godot_version": Engine.get_version_info().get("string", ""),
		"os": OS.get_name(),
		"display_driver": DisplayServer.get_name(),
		"rendering_method": _project_setting("rendering/renderer/rendering_method"),
		"headless": DisplayServer.get_name().to_lower() == "headless",
		"user_data_dir": OS.get_user_data_dir(),
		"output_dir": OUT_DIR,
		"absolute_output_dir": ProjectSettings.globalize_path(OUT_DIR),
		"viewport_size": {"w": VIEWPORT_SIZE.x, "h": VIEWPORT_SIZE.y},
		"hud_hidden": false,
		"review_screenshot_flag": BUILD_INFO.REVIEW_SCREENSHOT_FLAG,
		"required_recurring_screenshot_set_count": CAPTURES.size(),
		"movement_proof": "Player directional walk-frame screenshots plus NPC stationary-no-drift proof until dedicated walk sheets ship.",
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
