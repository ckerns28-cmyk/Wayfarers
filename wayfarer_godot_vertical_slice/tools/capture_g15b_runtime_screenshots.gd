extends SceneTree

const MAIN_SCENE := preload("res://scenes/Main.tscn")

const OUT_DIR := "res://artifacts/review/g15b_runtime_screenshots"
const MANIFEST_FILENAME := "g15b_runtime_screenshot_manifest.json"
const VIEWPORT_SIZE := Vector2i(1600, 1000)
const INITIAL_WAIT_FRAMES := 36
const CAPTURE_WAIT_FRAMES := 12

const CAPTURES := [
	{
		"filename": "g15b_01_island_wide_cohesion.png",
		"label": "island wide cohesion / town exit, loop, shore, and return lane read as one authored place",
		"target": "island_wide_cohesion",
		"player_position": Vector2(1840.0, 626.0),
		"camera_zoom": Vector2(0.98, 0.98),
		"camera_offset": Vector2(-120.0, -34.0),
		"player_direction": "right",
		"player_moving": true,
		"player_frame": 1
	},
	{
		"filename": "g15b_02_main_trail_ground_transition.png",
		"label": "main trail ground transition / grass, dirt, and wooded shoulder stay readable at gameplay zoom",
		"target": "main_trail_ground_transition",
		"player_position": Vector2(2048.0, 574.0),
		"camera_zoom": Vector2(1.20, 1.20),
		"camera_offset": Vector2(-180.0, -48.0),
		"player_direction": "right",
		"player_moving": true,
		"player_frame": 2
	},
	{
		"filename": "g15b_03_coastline_route_cohesion.png",
		"label": "coastline route cohesion / blocked water and walkable shore path are visually separated",
		"target": "coastline_route_cohesion",
		"player_position": Vector2(2132.0, 714.0),
		"camera_zoom": Vector2(1.16, 1.16),
		"camera_offset": Vector2(-210.0, -92.0),
		"player_direction": "down",
		"player_moving": false,
		"player_frame": 0
	},
	{
		"filename": "g15b_04_route_loop_return_path.png",
		"label": "route loop return path / the island path returns toward Newport rather than dead-ending",
		"target": "route_loop_return_path",
		"player_position": Vector2(1780.0, 642.0),
		"camera_zoom": Vector2(1.12, 1.12),
		"camera_offset": Vector2(-60.0, -60.0),
		"player_direction": "left",
		"player_moving": true,
		"player_frame": 1
	},
	{
		"filename": "g15b_05_debug_overlays_disabled.png",
		"label": "debug overlays disabled / terrain cohesion proof uses authored world art only",
		"target": "debug_overlays_disabled",
		"player_position": Vector2(1840.0, 626.0),
		"camera_zoom": Vector2(1.04, 1.04),
		"camera_offset": Vector2(-90.0, -54.0),
		"player_direction": "right",
		"player_moving": false,
		"player_frame": 0
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
	await _wait_for_render(INITIAL_WAIT_FRAMES)
	if main.has_method("set_review_screenshot_mode"):
		main.call("set_review_screenshot_mode", true)
	if main.has_method("set_debug_overlay"):
		main.call("set_debug_overlay", false)
	if main.has_method("set_building_seating_overlay"):
		main.call("set_building_seating_overlay", false)
	if main.has_method("set_starter_village_ambient_barks_enabled"):
		main.call("set_starter_village_ambient_barks_enabled", false)

	var player := main.get_node_or_null("World/Player") as Node2D
	if player == null:
		return _fail(manifest, "Player node not found.")
	player.set_physics_process(false)
	player.set_process(false)
	if player.has_method("set_prompt_suppressed"):
		player.call("set_prompt_suppressed", true)

	var camera := player.get_node_or_null("Camera2D") as Camera2D
	if camera == null:
		return _fail(manifest, "Player Camera2D node not found.")
	camera.enabled = true
	camera.position_smoothing_enabled = false
	camera.limit_smoothed = false
	camera.make_current()

	manifest["opening_island_world_cohesion_contract"] = _jsonify(main.call("opening_island_world_cohesion_contract") if main.has_method("opening_island_world_cohesion_contract") else {})
	manifest["debug_overlays_disabled"] = true
	manifest["no_hud_capture"] = true

	for capture in CAPTURES:
		var file_result := await _capture_one(capture, main, player, camera)
		manifest["screenshots"].append(file_result)
		if file_result.get("status", "") != "PASS":
			return _fail(manifest, String(file_result.get("failure", "Screenshot capture failed.")))

	manifest["status"] = "PASS"
	_write_manifest(manifest)
	print("PASS: G-15B runtime screenshots -> ", ProjectSettings.globalize_path(OUT_DIR))
	return 0


func _capture_one(capture: Dictionary, main: Node, player: Node2D, camera: Camera2D) -> Dictionary:
	var player_position: Vector2 = capture["player_position"]
	player.global_position = player_position
	if player.has_method("set_review_visual_state"):
		player.call("set_review_visual_state", capture["player_direction"], capture["player_moving"], capture["player_frame"])
	if player.has_method("set_prompt_suppressed"):
		player.call("set_prompt_suppressed", true)
	_hide_dialogue(main)
	camera.zoom = capture["camera_zoom"]
	camera.offset = capture["camera_offset"]
	camera.reset_smoothing()
	await _wait_for_render(CAPTURE_WAIT_FRAMES)

	var image := root.get_texture().get_image()
	var output_path := "%s/%s" % [OUT_DIR, capture["filename"]]
	var result := {
		"filename": capture["filename"],
		"label": capture["label"],
		"target": capture["target"],
		"path": output_path,
		"absolute_path": ProjectSettings.globalize_path(output_path),
		"player_position": _vector2_to_dict(player_position),
		"camera_zoom": _vector2_to_dict(capture["camera_zoom"]),
		"camera_offset": _vector2_to_dict(capture["camera_offset"]),
		"dimensions": {"w": image.get_width(), "h": image.get_height()},
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


func _hide_dialogue(main: Node) -> void:
	var hud := main.get_node_or_null("HUD")
	if hud == null:
		return
	var dialogue_panel := hud.get_node_or_null("DialoguePanel") as Control
	if dialogue_panel != null:
		dialogue_panel.visible = false


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
		"schema_id": "wayfarer.g15b.runtime_screenshot_manifest.v1",
		"phase": "G-15B",
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
	if value is Dictionary:
		var result := {}
		for key in value.keys():
			result[str(key)] = _jsonify(value[key])
		return result
	if value is Array:
		var result := []
		for item in value:
			result.append(_jsonify(item))
		return result
	return value


func _vector2_to_dict(value: Vector2) -> Dictionary:
	return {"x": snappedf(value.x, 0.001), "y": snappedf(value.y, 0.001)}
