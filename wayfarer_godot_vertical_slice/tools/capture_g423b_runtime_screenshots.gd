extends SceneTree

const BUILD_INFO := preload("res://scripts/BuildInfo.gd")
const MAIN_SCENE := preload("res://scenes/Main.tscn")

const OUT_DIR := "res://artifacts/review/g423b_runtime_screenshots"
const MANIFEST_FILENAME := "g423b_runtime_screenshot_manifest.json"
const VIEWPORT_SIZE := Vector2i(1600, 1000)
const INITIAL_WAIT_FRAMES := 36
const CAPTURE_WAIT_FRAMES := 12

const CAPTURES := [
	{
		"filename": "g423b_01_whole_town.png",
		"label": "whole town / harbor at bottom, waterfront avenue, uphill city fabric, back street",
		"target": "whole_town",
		"player_position": Vector2(800.0, 512.0),
		"camera_zoom": Vector2(1.0, 1.0),
		"camera_offset": Vector2(0.0, 0.0),
	},
	{
		"filename": "g423b_02_working_harborfront_avenue.png",
		"label": "harborfront avenue / working harbor, piers, loading points, and clear route",
		"target": "harborfront_working_harbor",
		"player_position": Vector2(805.0, 654.0),
		"camera_zoom": Vector2(1.28, 1.28),
		"camera_offset": Vector2(20.0, -12.0),
	},
	{
		"filename": "g423b_03_tavern_inn_social_anchor.png",
		"label": "Tavern/Inn social anchor / street threshold, market pocket, and west avenue",
		"target": "tavern_inn_social_anchor",
		"player_position": Vector2(300.0, 604.0),
		"camera_zoom": Vector2(1.44, 1.44),
		"camera_offset": Vector2(50.0, -58.0),
	},
	{
		"filename": "g423b_04_uphill_connector_road.png",
		"label": "uphill connector road / avenue to civic buildings and back street",
		"target": "uphill_connector_road",
		"player_position": Vector2(704.0, 520.0),
		"camera_zoom": Vector2(1.36, 1.36),
		"camera_offset": Vector2(38.0, -66.0),
	},
	{
		"filename": "g423b_05_backstreet_service_lane.png",
		"label": "back street and service lane / rear street behind first road",
		"target": "backstreet_service_lane",
		"player_position": Vector2(960.0, 418.0),
		"camera_zoom": Vector2(1.32, 1.32),
		"camera_offset": Vector2(36.0, -10.0),
	},
	{
		"filename": "g423b_06_building_frontage_grounding.png",
		"label": "building frontage and lot grounding / thresholds, yards, civic frontage",
		"target": "building_frontage_grounding",
		"player_position": Vector2(675.0, 590.0),
		"camera_zoom": Vector2(1.36, 1.36),
		"camera_offset": Vector2(12.0, -64.0),
	},
	{
		"filename": "g423b_07_player_walkability_proof.png",
		"label": "player walkability proof / avenue to wharf, civic road, and back street",
		"target": "player_walkability_proof",
		"player_position": Vector2(675.0, 600.0),
		"camera_zoom": Vector2(1.44, 1.44),
		"camera_offset": Vector2(42.0, -54.0),
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
		manifest["status"] = "FAIL"
		manifest["failure"] = "Refusing to capture visual proof with the headless display driver."
		_write_manifest(manifest)
		push_error(manifest["failure"])
		return 1

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

	for capture in CAPTURES:
		var file_result := await _capture_one(capture, player, camera)
		if file_result.get("status", "") != "PASS":
			manifest["screenshots"].append(file_result)
			return _fail(manifest, String(file_result.get("failure", "Screenshot capture failed.")))
		manifest["screenshots"].append(file_result)

	manifest["status"] = "PASS"
	_write_manifest(manifest)
	print("PASS: G-4.23B runtime screenshots -> ", ProjectSettings.globalize_path(OUT_DIR))
	return 0


func _capture_one(capture: Dictionary, player: Node2D, camera: Camera2D) -> Dictionary:
	player.global_position = capture["player_position"]
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
		"schema_id": "wayfarer.g423b.runtime_screenshot_manifest.v1",
		"phase": "G-4.23B",
		"status": "PENDING",
		"created_at": Time.get_datetime_string_from_system(true),
		"command": OS.get_environment("G423B_CAPTURE_COMMAND"),
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
		"warnings": [],
		"screenshots": [],
	}


func _project_setting(setting_name: String) -> String:
	if ProjectSettings.has_setting(setting_name):
		return str(ProjectSettings.get_setting(setting_name))
	return ""


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
		push_error("Could not write manifest: %s error=%s" % [manifest_path, FileAccess.get_open_error()])
		return
	file.store_string(JSON.stringify(manifest, "\t"))
	file.store_string("\n")
	file.close()


func _vector2_to_dict(value: Vector2) -> Dictionary:
	return {"x": value.x, "y": value.y}
