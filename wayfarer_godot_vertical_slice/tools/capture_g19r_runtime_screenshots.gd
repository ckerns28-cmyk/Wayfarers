extends SceneTree

const MAIN_SCENE := preload("res://scenes/Main.tscn")

const OUT_DIR := "res://artifacts/review/g19r_newport_reconstruction_screenshots"
const MANIFEST_FILENAME := "g19r_runtime_screenshot_manifest.json"
const VIEWPORT_SIZE := Vector2i(1600, 1000)
const INITIAL_WAIT_FRAMES := 30
const CAPTURE_WAIT_FRAMES := 12

const CAPTURES := [
	{
		"filename": "g19r_01_village_wide_city_structure.png",
		"step_id": "village_wide_city_structure",
		"label": "wide village composition / districts, streets, wharf, and lots read before UI",
		"player_position": Vector2(800.0, 560.0),
		"camera_zoom": Vector2(1.16, 1.16),
		"camera_offset": Vector2(0.0, -42.0),
		"player_direction": "down"
	},
	{
		"filename": "g19r_02_harborfront_avenue_width.png",
		"step_id": "harborfront_avenue_width",
		"label": "harborfront avenue / primary road has walkable RPG breathing room",
		"player_position": Vector2(675.0, 612.0),
		"camera_zoom": Vector2(1.42, 1.42),
		"camera_offset": Vector2(-18.0, -34.0),
		"player_direction": "right"
	},
	{
		"filename": "g19r_03_counting_house_civic_climb.png",
		"step_id": "counting_house_civic_climb",
		"label": "counting house climb / harbor work leads into civic pressure",
		"player_position": Vector2(770.0, 500.0),
		"camera_zoom": Vector2(1.42, 1.42),
		"camera_offset": Vector2(0.0, -44.0),
		"player_direction": "up"
	},
	{
		"filename": "g19r_04_wharf_work_apron.png",
		"step_id": "wharf_work_apron",
		"label": "wharf work apron / harbor labor edge is continuous and walkable",
		"player_position": Vector2(824.0, 812.0),
		"camera_zoom": Vector2(1.38, 1.38),
		"camera_offset": Vector2(-18.0, -28.0),
		"player_direction": "down"
	},
	{
		"filename": "g19r_05_east_gate_settlement_edge.png",
		"step_id": "east_gate_settlement_edge",
		"label": "east gate / Newport exits into the island from a coherent town edge",
		"player_position": Vector2(1518.0, 555.0),
		"camera_zoom": Vector2(1.28, 1.28),
		"camera_offset": Vector2(-82.0, -42.0),
		"player_direction": "right"
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
	manifest["status"] = "PASS"
	_write_json(manifest, "%s/%s" % [OUT_DIR, MANIFEST_FILENAME])
	print("PASS: G-19R Newport reconstruction screenshots -> ", ProjectSettings.globalize_path(OUT_DIR))
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
	player.global_position = capture["player_position"]
	if player.has_method("set_review_visual_state"):
		player.call("set_review_visual_state", capture["player_direction"], false, 0)
	if player.has_method("set_prompt_suppressed"):
		player.call("set_prompt_suppressed", true)
	camera.zoom = capture["camera_zoom"]
	camera.offset = capture["camera_offset"]
	camera.reset_smoothing()
	await _wait_for_render(CAPTURE_WAIT_FRAMES)

	var image := root.get_texture().get_image()
	var output_path := "%s/%s" % [OUT_DIR, capture["filename"]]
	var result := {
		"filename": capture["filename"],
		"step_id": capture["step_id"],
		"label": capture["label"],
		"path": output_path,
		"absolute_path": ProjectSettings.globalize_path(output_path),
		"player_position": _vector2_to_dict(capture["player_position"]),
		"camera_zoom": _vector2_to_dict(capture["camera_zoom"]),
		"newport_reconstruction_contract": _jsonify(main.call("newport_reconstruction_contract") if main.has_method("newport_reconstruction_contract") else {}),
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
		main.call("set_review_screenshot_mode", true)
	if main.has_method("set_debug_overlay"):
		main.call("set_debug_overlay", false)
	if main.has_method("set_building_seating_overlay"):
		main.call("set_building_seating_overlay", false)
	if main.has_method("set_starter_village_ambient_barks_enabled"):
		main.call("set_starter_village_ambient_barks_enabled", false)
	if main.has_method("set_opening_island_ambient_barks_enabled"):
		main.call("set_opening_island_ambient_barks_enabled", false)
	var hud := main.get_node_or_null("HUD") as CanvasLayer
	if hud != null:
		hud.visible = false
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

func _freeze_npcs(main: Node) -> void:
	for npc in main.get_tree().get_nodes_in_group("npcs"):
		if npc is Node:
			(npc as Node).set_process(false)
			(npc as Node).set_physics_process(false)
			if (npc as Node).has_method("set_ambient_barks_enabled"):
				(npc as Node).call("set_ambient_barks_enabled", false)

func _wait_for_render(frame_count: int) -> void:
	for _i in range(frame_count):
		await process_frame

func _verify_png_pixels(image: Image) -> Dictionary:
	var width := image.get_width()
	var height := image.get_height()
	var nontransparent := 0
	var varied := {}
	for y in range(0, height, max(1, int(height / 18))):
		for x in range(0, width, max(1, int(width / 24))):
			var c := image.get_pixel(x, y)
			if c.a > 0.05:
				nontransparent += 1
			var key := "%02d-%02d-%02d" % [int(c.r * 32.0), int(c.g * 32.0), int(c.b * 32.0)]
			varied[key] = true
	if nontransparent < 20 or varied.size() < 8:
		return {"status": "FAIL", "failure": "Image appears blank or too visually uniform.", "sample_count": nontransparent, "color_bucket_count": varied.size()}
	return {"status": "PASS", "sample_count": nontransparent, "color_bucket_count": varied.size()}

func _base_manifest() -> Dictionary:
	return {
		"schema_id": "wayfarer.g19r.runtime_screenshot_manifest.v1",
		"phase": "G-19R",
		"status": "PENDING",
		"source": "res://data/world_layout/newport_harbor_town_reconstruction_v1.json",
		"debug_overlays_disabled": true,
		"hud_hidden_for_world_structure_review": true,
		"city_structure_review": {
			"districts_first": true,
			"road_hierarchy_first": true,
			"road_widths_authored": true,
			"wharf_dimensions_authored": true,
			"props_last": true,
			"screenshot_contradiction_fails_phase": true
		},
		"screenshots": []
	}

func _fail(manifest: Dictionary, message: String) -> int:
	manifest["status"] = "FAIL"
	manifest["failure"] = message
	_write_json(manifest, "%s/%s" % [OUT_DIR, MANIFEST_FILENAME])
	push_error(message)
	return 1

func _write_json(data: Dictionary, path: String) -> void:
	var file := FileAccess.open(path, FileAccess.WRITE)
	if file == null:
		push_error("Could not write JSON: " + path)
		return
	file.store_string(JSON.stringify(_jsonify(data), "\t"))

func _jsonify(value: Variant) -> Variant:
	if value is Vector2:
		return _vector2_to_dict(value)
	if value is Rect2:
		return {"x": value.position.x, "y": value.position.y, "w": value.size.x, "h": value.size.y}
	if value is Dictionary:
		var result := {}
		for key in value.keys():
			result[str(key)] = _jsonify(value[key])
		return result
	if value is Array:
		var result_array := []
		for item in value:
			result_array.append(_jsonify(item))
		return result_array
	return value

func _vector2_to_dict(value: Vector2) -> Dictionary:
	return {"x": value.x, "y": value.y}
