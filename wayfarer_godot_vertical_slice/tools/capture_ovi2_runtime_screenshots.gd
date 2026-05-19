extends SceneTree

const MAIN_SCENE := preload("res://scenes/Main.tscn")

const OUT_DIR := "res://artifacts/review/ovi2_newport_origin_immersion"
const MANIFEST_FILENAME := "ovi2_newport_origin_immersion_screenshot_manifest.json"
const VIEWPORT_SIZE := Vector2i(1600, 1000)
const INITIAL_WAIT_FRAMES := 36
const CAPTURE_WAIT_FRAMES := 12

const CAPTURES := [
	{
		"filename": "ovi2_01_player_spawn_first_impression_hud.png",
		"viewpoint_id": "player_spawn_first_impression_hud",
		"label": "Player spawn first impression with HUD; harbor goods, lanterns, wharf route, and town avenue must read before the UI explains anything.",
		"camera_position": Vector2(430.0, 920.0),
		"player_position": Vector2(430.0, 920.0),
		"camera_zoom": Vector2(1.25, 1.25),
		"player_direction": "up",
		"player_moving": false,
		"player_frame": 0,
		"hide_hud": false
	},
	{
		"filename": "ovi2_02_player_spawn_first_impression_no_hud.png",
		"viewpoint_id": "player_spawn_first_impression_no_hud",
		"label": "Player spawn first impression with HUD hidden; world must carry origin-town identity on its own.",
		"camera_position": Vector2(430.0, 920.0),
		"player_position": Vector2(430.0, 920.0),
		"camera_zoom": Vector2(1.25, 1.25),
		"player_direction": "up",
		"player_moving": false,
		"player_frame": 0,
		"hide_hud": true
	},
	{
		"filename": "ovi2_03_harborfront_avenue.png",
		"viewpoint_id": "harborfront_avenue",
		"label": "Harborfront avenue: segmented street surfaces, shopfronts, civic approach, and wharf link replace the old giant slab read.",
		"camera_position": Vector2(1100.0, 710.0),
		"player_position": Vector2(1100.0, 710.0),
		"camera_zoom": Vector2(1.10, 1.10),
		"player_direction": "up",
		"player_moving": true,
		"player_frame": 1,
		"hide_hud": true
	},
	{
		"filename": "ovi2_04_tavern_inn_district.png",
		"viewpoint_id": "tavern_inn_district",
		"label": "Tavern/Inn district: warm entry, parcel frontage, rear lane, and service goods make it a social anchor rather than an isolated sprite.",
		"camera_position": Vector2(505.0, 640.0),
		"player_position": Vector2(505.0, 640.0),
		"camera_zoom": Vector2(1.28, 1.28),
		"player_direction": "up",
		"player_moving": false,
		"player_frame": 0,
		"hide_hud": true
	},
	{
		"filename": "ovi2_05_counting_house_civic_district.png",
		"viewpoint_id": "counting_house_civic_district",
		"label": "Counting House / civic district: notice boards, flags, posting pole, and plaza route integrate the first objective with the road plan.",
		"camera_position": Vector2(1120.0, 610.0),
		"player_position": Vector2(1120.0, 610.0),
		"camera_zoom": Vector2(1.24, 1.24),
		"player_direction": "up",
		"player_moving": false,
		"player_frame": 0,
		"hide_hud": true
	},
	{
		"filename": "ovi2_06_shopfront_commercial_street.png",
		"viewpoint_id": "shopfront_commercial_street",
		"label": "Shopfront/commercial street: signs, awnings, market goods, lamps, and route openings align to storefronts.",
		"camera_position": Vector2(1510.0, 675.0),
		"player_position": Vector2(1510.0, 675.0),
		"camera_zoom": Vector2(1.18, 1.18),
		"player_direction": "right",
		"player_moving": true,
		"player_frame": 2,
		"hide_hud": true
	},
	{
		"filename": "ovi2_07_wharf_dock_service_district.png",
		"viewpoint_id": "wharf_dock_service_district",
		"label": "Wharf/dock/service district: cargo, rope, bollards, dock rules, fish baskets, and plank seams show a working harbor economy.",
		"camera_position": Vector2(1110.0, 1000.0),
		"player_position": Vector2(1110.0, 1000.0),
		"camera_zoom": Vector2(1.18, 1.18),
		"player_direction": "down",
		"player_moving": false,
		"player_frame": 0,
		"hide_hud": true
	},
	{
		"filename": "ovi2_08_wide_town_composition.png",
		"viewpoint_id": "wide_town_composition",
		"label": "Wide town composition: the origin city must read as authored blocks, lanes, waterfront, civic anchor, tavern, shops, and wharf.",
		"camera_position": Vector2(1080.0, 720.0),
		"player_position": Vector2(1080.0, 720.0),
		"camera_zoom": Vector2(0.78, 0.78),
		"player_direction": "down",
		"player_moving": false,
		"player_frame": 0,
		"hide_hud": true
	},
	{
		"filename": "ovi2_09_movement_route_through_town.png",
		"viewpoint_id": "movement_route_through_town",
		"label": "Movement proof through town: authored lanes remain playable without flattening Newport into an empty test track.",
		"camera_position": Vector2(815.0, 735.0),
		"player_position": Vector2(815.0, 735.0),
		"camera_zoom": Vector2(1.20, 1.20),
		"player_direction": "right",
		"player_moving": true,
		"player_frame": 2,
		"hide_hud": true
	},
	{
		"filename": "ovi2_10_before_after_reference_current_failure.png",
		"viewpoint_id": "before_after_reference_current_failure",
		"label": "Current branch wide review angle captured against the baseline OVI-1 failure reference recorded in the manifest.",
		"camera_position": Vector2(1080.0, 720.0),
		"player_position": Vector2(1080.0, 720.0),
		"camera_zoom": Vector2(0.82, 0.82),
		"player_direction": "down",
		"player_moving": false,
		"player_frame": 0,
		"hide_hud": true
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

	manifest["ovi2_newport_origin_immersion_contract"] = _jsonify(main.call("ovi2_newport_origin_immersion_contract") if main.has_method("ovi2_newport_origin_immersion_contract") else {})
	manifest["baseline_failure_reference"] = "wayfarer_godot_vertical_slice/artifacts/review/g22_ovi1_review_screenshots/01_village_wide_cohesion.png"
	manifest["debug_overlays_disabled"] = true
	manifest["representative_human_review_angles"] = true
	manifest["not_outward_gameplay_expansion"] = true

	for capture in CAPTURES:
		var file_result := await _capture_one(capture, main, player, camera)
		manifest["screenshots"].append(file_result)
		if file_result.get("status", "") != "PASS":
			return _fail(manifest, String(file_result.get("failure", "Screenshot capture failed.")))

	manifest["status"] = "PASS"
	_write_manifest(manifest)
	print("PASS: OVI-2 runtime screenshots -> ", ProjectSettings.globalize_path(OUT_DIR))
	return 0


func _capture_one(capture: Dictionary, main: Node, player: Node2D, camera: Camera2D) -> Dictionary:
	var player_position: Vector2 = capture["player_position"]
	player.global_position = player_position
	if main.has_method("set_review_screenshot_mode"):
		main.call("set_review_screenshot_mode", bool(capture.get("hide_hud", true)))
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
		"hide_hud": bool(capture.get("hide_hud", true)),
		"dimensions": {"w": image.get_width(), "h": image.get_height()},
		"png_verification": {},
		"status": "PENDING",
	}
	if image.get_width() < 1200 or image.get_height() < 800:
		result["status"] = "FAIL"
		result["failure"] = "Viewport image dimensions were too small for OVI-2 review."
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
	var bright_samples := 0
	for y in range(0, image.get_height(), 80):
		for x in range(0, image.get_width(), 80):
			var color := image.get_pixel(x, y)
			var total := color.r + color.g + color.b
			color_sum += total
			if total > 0.20:
				bright_samples += 1
			samples += 1
	if samples <= 0:
		return {"status": "FAIL", "failure": "No sampled pixels."}
	var average := color_sum / float(samples)
	if average <= 0.03 or bright_samples < 8:
		return {"status": "FAIL", "failure": "Screenshot appears blank or under-rendered.", "average_rgb": average, "bright_samples": bright_samples}
	return {"status": "PASS", "average_rgb": average, "sample_count": samples, "bright_samples": bright_samples}


func _base_manifest() -> Dictionary:
	return {
		"schema_id": "wayfarer.ovi2.newport_origin_immersion_screenshot_manifest.v1",
		"phase": "OVI-2",
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
