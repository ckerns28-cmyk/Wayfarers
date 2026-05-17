extends SceneTree

const BUILD_INFO := preload("res://scripts/BuildInfo.gd")
const MAIN_SCENE := preload("res://scenes/Main.tscn")

const OUT_DIR := "res://artifacts/review/g422_runtime_screenshots"
const MANIFEST_FILENAME := "g422_runtime_screenshot_manifest.json"
const VIEWPORT_SIZE := Vector2i(1600, 1000)
const INITIAL_WAIT_FRAMES := 36
const CAPTURE_WAIT_FRAMES := 12

const CAPTURES := [
	{
		"filename": "g422_01_visual_gate_normal_hud.png",
		"label": "G-4.22 gate: normal HUD, player, Newport harbor city, and hero-slice composition",
		"target": "normal_hud_gate",
		"player_position": Vector2(760.0, 604.0),
		"camera_zoom": Vector2(1.16, 1.16),
		"camera_offset": Vector2(20.0, -22.0),
		"direction": "down",
		"moving": false,
		"frame_index": 0,
	},
	{
		"filename": "g422_02_visual_gate_clean_no_hud.png",
		"label": "G-4.22 gate: clean no-HUD world review of harbor avenue, docks, buildings, and player",
		"target": "clean_no_hud_gate",
		"player_position": Vector2(800.0, 560.0),
		"camera_zoom": Vector2(1.02, 1.02),
		"camera_offset": Vector2(0.0, -16.0),
		"direction": "down",
		"moving": false,
		"frame_index": 0,
		"no_hud": true,
	},
	{
		"filename": "g422_03_hero_street_dock_slice.png",
		"label": "G-4.22 gate: hero street/dock close-up with buildings, player scale, props, and walkable avenue",
		"target": "hero_street_dock_slice",
		"player_position": Vector2(1070.0, 574.0),
		"camera_zoom": Vector2(1.52, 1.52),
		"camera_offset": Vector2(12.0, -20.0),
		"direction": "right",
		"moving": true,
		"frame_index": 1,
		"no_hud": true,
	},
	{
		"filename": "g422_04_ui_world_cohesion.png",
		"label": "G-4.22 gate: HUD/UI, player, road grammar, buildings, and harbor-town readability",
		"target": "ui_world_cohesion",
		"player_position": Vector2(676.0, 604.0),
		"camera_zoom": Vector2(1.58, 1.58),
		"camera_offset": Vector2(28.0, -40.0),
		"direction": "down",
		"moving": false,
		"frame_index": 0,
	},
	{
		"filename": "g422_05_green_origin_lab_and_yellow_art_proof.png",
		"label": "G-4.22 gate: green-origin lab/provenance context remains explicit and separate from normal review art",
		"target": "green_origin_yellow_art_proof",
		"player_position": Vector2(824.0, 710.0),
		"camera_zoom": Vector2(0.92, 0.92),
		"camera_offset": Vector2(0.0, -38.0),
		"direction": "up",
		"moving": false,
		"frame_index": 0,
		"no_hud": true,
		"green_origin_lab": true,
	},
	{
		"filename": "g422_06_debug_overlay_proof.png",
		"label": "G-4.22 gate: debug overlay proof is available only when explicitly toggled",
		"target": "debug_overlay_proof",
		"player_position": Vector2(704.0, 392.0),
		"camera_zoom": Vector2(1.0, 1.0),
		"camera_offset": Vector2(112.0, -44.0),
		"direction": "down",
		"moving": false,
		"frame_index": 0,
		"no_hud": true,
		"debug_overlay": true,
	},
	{
		"filename": "g422_07_wide_origin_city_readability.png",
		"label": "G-4.22 gate: wide origin-city readability, harbor, uphill roads, back street, and home-base scale",
		"target": "wide_origin_city_readability",
		"player_position": Vector2(800.0, 560.0),
		"camera_zoom": Vector2(0.82, 0.82),
		"camera_offset": Vector2(0.0, -32.0),
		"direction": "down",
		"moving": false,
		"frame_index": 0,
		"no_hud": true,
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
		var file_result := await _capture_one(capture, main, player, camera)
		manifest["screenshots"].append(file_result)
		if file_result.get("status", "") != "PASS":
			return _fail(manifest, String(file_result.get("failure", "Screenshot capture failed.")))

	manifest["status"] = "PASS"
	_write_manifest(manifest)
	print("PASS: G-4.22 runtime screenshots -> ", ProjectSettings.globalize_path(OUT_DIR))
	return 0


func _capture_one(capture: Dictionary, main: Node, player: Node2D, camera: Camera2D) -> Dictionary:
	var no_hud := bool(capture.get("no_hud", false))
	var debug_overlay := bool(capture.get("debug_overlay", false))
	var green_origin_lab := bool(capture.get("green_origin_lab", false))

	if main.has_method("set_review_screenshot_mode"):
		main.call("set_review_screenshot_mode", no_hud)
	if main.has_method("set_debug_overlay"):
		main.call("set_debug_overlay", debug_overlay)
	if main.has_method("set_green_origin_lab_mode"):
		main.call("set_green_origin_lab_mode", green_origin_lab)

	var hud := main.get_node_or_null("HUD") as CanvasLayer
	if hud != null and hud.has_method("set_review_metadata_expanded"):
		hud.call("set_review_metadata_expanded", false)

	player.global_position = capture["player_position"]
	if player.has_method("set_review_visual_state"):
		player.call("set_review_visual_state", capture["direction"], capture["moving"], capture["frame_index"])
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
		"hud_visible": not no_hud,
		"debug_overlay": debug_overlay,
		"green_origin_lab": green_origin_lab,
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
		"schema_id": "wayfarer.g422.runtime_screenshot_manifest.v1",
		"phase": "G-4.22",
		"status": "PENDING",
		"created_at": Time.get_datetime_string_from_system(true),
		"command": OS.get_environment("G422_CAPTURE_COMMAND"),
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
		"required_views": [
			"normal_hud_gate",
			"clean_no_hud_gate",
			"hero_street_dock_slice",
			"ui_world_cohesion",
			"green_origin_yellow_art_proof",
			"debug_overlay_proof",
			"wide_origin_city_readability",
		],
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


func _vector2_to_dict(value: Vector2) -> Dictionary:
	return {"x": snappedf(value.x, 0.001), "y": snappedf(value.y, 0.001)}


func _write_manifest(manifest: Dictionary) -> void:
	var output_path := "%s/%s" % [OUT_DIR, MANIFEST_FILENAME]
	var file := FileAccess.open(output_path, FileAccess.WRITE)
	if file == null:
		push_error("Could not write screenshot manifest: " + output_path)
		return
	file.store_string(JSON.stringify(manifest, "\t"))
	file.store_string("\n")


func _fail(manifest: Dictionary, message: String) -> int:
	manifest["status"] = "FAIL"
	manifest["failure"] = message
	_write_manifest(manifest)
	push_error(message)
	return 1
