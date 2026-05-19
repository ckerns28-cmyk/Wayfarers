extends SceneTree

const MAIN_SCENE := preload("res://scenes/Main.tscn")

const OUT_DIR := "res://artifacts/review/g19s_runtime_screenshots"
const MANIFEST_FILENAME := "g19s_runtime_screenshot_manifest.json"
const VIEWPORT_SIZE := Vector2i(1600, 1000)
const INITIAL_WAIT_FRAMES := 36
const CAPTURE_WAIT_FRAMES := 12

const CAPTURES := [
	{
		"filename": "g19s_01_wide_town_cohesion_view.png",
		"viewpoint_id": "wide_town_cohesion_view",
		"label": "wide town cohesion view / G-19R source blocks read as one human-scale harbor town",
		"camera_position": Vector2(1080.0, 710.0),
		"player_position": Vector2(1080.0, 710.0),
		"camera_zoom": Vector2(0.82, 0.82),
		"player_direction": "down",
		"player_moving": false,
		"player_frame": 0
	},
	{
		"filename": "g19s_02_arrival_harbor_view.png",
		"viewpoint_id": "arrival_harbor_view",
		"label": "arrival harbor view / player starts on a working wharf edge with the town spine readable uphill",
		"camera_position": Vector2(430.0, 920.0),
		"player_position": Vector2(430.0, 920.0),
		"camera_zoom": Vector2(1.38, 1.38),
		"player_direction": "up",
		"player_moving": false,
		"player_frame": 0
	},
	{
		"filename": "g19s_03_counting_house_route_view.png",
		"viewpoint_id": "counting_house_route_view",
		"label": "counting house route view / central official route is visible from harbor road to clerk target",
		"camera_position": Vector2(1045.0, 645.0),
		"player_position": Vector2(1045.0, 645.0),
		"camera_zoom": Vector2(1.38, 1.38),
		"player_direction": "up",
		"player_moving": true,
		"player_frame": 1
	},
	{
		"filename": "g19s_04_tavern_landmark_view.png",
		"viewpoint_id": "tavern_landmark_view",
		"label": "tavern landmark view / tavern lot anchors the west social/rumor district rather than floating as an asset",
		"camera_position": Vector2(500.0, 645.0),
		"player_position": Vector2(500.0, 645.0),
		"camera_zoom": Vector2(1.38, 1.38),
		"player_direction": "up",
		"player_moving": false,
		"player_frame": 0
	},
	{
		"filename": "g19s_05_commercial_avenue_view.png",
		"viewpoint_id": "commercial_avenue_view",
		"label": "commercial avenue view / shop row fronts a broad human-scale main street",
		"camera_position": Vector2(1260.0, 675.0),
		"player_position": Vector2(1260.0, 675.0),
		"camera_zoom": Vector2(1.38, 1.38),
		"player_direction": "right",
		"player_moving": true,
		"player_frame": 2
	},
	{
		"filename": "g19s_06_harbor_work_view.png",
		"viewpoint_id": "harbor_work_view",
		"label": "harbor work view / wharf apron, dock paths, cargo, rope, and waterline support a working harbor",
		"camera_position": Vector2(980.0, 1010.0),
		"player_position": Vector2(980.0, 1010.0),
		"camera_zoom": Vector2(1.34, 1.34),
		"player_direction": "down",
		"player_moving": false,
		"player_frame": 0
	},
	{
		"filename": "g19s_07_rear_service_lane_view.png",
		"viewpoint_id": "rear_service_lane_view",
		"label": "rear service lane view / back street and hidden rumor cutthrough exist behind the public frontage",
		"camera_position": Vector2(850.0, 380.0),
		"player_position": Vector2(850.0, 380.0),
		"camera_zoom": Vector2(1.38, 1.38),
		"player_direction": "right",
		"player_moving": true,
		"player_frame": 1
	},
	{
		"filename": "g19s_08_npc_route_proof_view.png",
		"viewpoint_id": "npc_route_proof_view",
		"label": "NPC route proof view / stationed NPCs sit on planned pause points until grounded walk animation exists",
		"camera_position": Vector2(735.0, 700.0),
		"player_position": Vector2(735.0, 700.0),
		"camera_zoom": Vector2(1.38, 1.38),
		"player_direction": "left",
		"player_moving": false,
		"player_frame": 0
	},
	{
		"filename": "g19s_09_village_exit_to_island_view.png",
		"viewpoint_id": "village_exit_to_island_view",
		"label": "village exit to island view / exit road and guidepost carry the player out of town without map-like ambiguity",
		"camera_position": Vector2(1880.0, 610.0),
		"player_position": Vector2(1880.0, 610.0),
		"camera_zoom": Vector2(1.25, 1.25),
		"player_direction": "right",
		"player_moving": true,
		"player_frame": 2
	},
	{
		"filename": "g19s_10_quest_interaction_view.png",
		"viewpoint_id": "quest_interaction_view",
		"label": "quest interaction view / counting house, notice board, and civic target sit in the first objective geography",
		"camera_position": Vector2(1100.0, 600.0),
		"player_position": Vector2(1100.0, 600.0),
		"camera_zoom": Vector2(1.38, 1.38),
		"player_direction": "up",
		"player_moving": false,
		"player_frame": 0
	},
	{
		"filename": "g19s_11_debug_disabled_view.png",
		"viewpoint_id": "debug_disabled_view",
		"label": "debug disabled view / normal review capture has no HUD, debug markers, or blockout overlays",
		"camera_position": Vector2(1080.0, 720.0),
		"player_position": Vector2(1080.0, 720.0),
		"camera_zoom": Vector2(1.38, 1.38),
		"player_direction": "down",
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
	if main.has_method("set_review_screenshot_mode"):
		main.call("set_review_screenshot_mode", true)
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
	if player.has_method("set_prompt_suppressed"):
		player.call("set_prompt_suppressed", true)

	var camera := player.get_node_or_null("Camera2D") as Camera2D
	if camera == null:
		return _fail(manifest, "Player Camera2D node not found.")
	camera.enabled = true
	camera.position_smoothing_enabled = false
	camera.limit_smoothed = false
	camera.make_current()

	manifest["g19s_runtime_reconstruction_contract"] = _jsonify(main.call("g19s_runtime_reconstruction_contract") if main.has_method("g19s_runtime_reconstruction_contract") else {})
	manifest["debug_overlays_disabled"] = true
	manifest["no_hud_capture"] = true
	manifest["canonical_camera_viewpoints_source"] = "wayfarer_godot_vertical_slice/artifacts/planning/g19r_newport_blockout/g19r_newport_camera_viewpoints.json"

	for capture in CAPTURES:
		var file_result := await _capture_one(capture, main, player, camera)
		manifest["screenshots"].append(file_result)
		if file_result.get("status", "") != "PASS":
			return _fail(manifest, String(file_result.get("failure", "Screenshot capture failed.")))

	manifest["status"] = "PASS"
	_write_manifest(manifest)
	print("PASS: G-19S runtime screenshots -> ", ProjectSettings.globalize_path(OUT_DIR))
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
	camera.offset = Vector2.ZERO
	camera.reset_smoothing()
	await _wait_for_render(CAPTURE_WAIT_FRAMES)

	var image := root.get_texture().get_image()
	var output_path := "%s/%s" % [OUT_DIR, capture["filename"]]
	var result := {
		"filename": capture["filename"],
		"viewpoint_id": capture["viewpoint_id"],
		"label": capture["label"],
		"path": output_path,
		"absolute_path": ProjectSettings.globalize_path(output_path),
		"player_position": _vector2_to_dict(player_position),
		"camera_position": _vector2_to_dict(capture["camera_position"]),
		"camera_zoom": _vector2_to_dict(capture["camera_zoom"]),
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
		"schema_id": "wayfarer.g19s.runtime_screenshot_manifest.v1",
		"phase": "G-19S",
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
