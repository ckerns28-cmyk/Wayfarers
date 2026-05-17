extends SceneTree

const BUILD_INFO := preload("res://scripts/BuildInfo.gd")
const MAIN_SCENE := preload("res://scenes/Main.tscn")

const OUT_DIR := "res://artifacts/review/g419_runtime_screenshots"
const MANIFEST_FILENAME := "g419_runtime_screenshot_manifest.json"
const CONTACT_SHEET_PATH := "res://art_pipeline/player_identity/contact_sheets/player_wayfarer_foundation_g419_contact_sheet.png"
const VIEWPORT_SIZE := Vector2i(1600, 1000)
const INITIAL_WAIT_FRAMES := 36
const CAPTURE_WAIT_FRAMES := 12

const CAPTURES := [
	{
		"filename": "g419_01_tavern_inn_player_grounding.png",
		"label": "Player in Tavern/Inn district, human-scale and grounded beside social-frontage props",
		"target": "tavern_inn_district",
		"player_position": Vector2(280.0, 548.0),
		"camera_zoom": Vector2(1.72, 1.72),
		"camera_offset": Vector2(16.0, -30.0),
		"direction": "down",
		"moving": false,
		"frame_index": 0,
	},
	{
		"filename": "g419_02_commercial_avenue_player_scale.png",
		"label": "Player on commercial avenue against shops, road width, and market dressing",
		"target": "commercial_avenue",
		"player_position": Vector2(1070.0, 574.0),
		"camera_zoom": Vector2(1.54, 1.54),
		"camera_offset": Vector2(10.0, -24.0),
		"direction": "right",
		"moving": true,
		"frame_index": 1,
	},
	{
		"filename": "g419_03_harbor_dock_edge_player_read.png",
		"label": "Player at harbor/dock edge with water, dock clutter, and G-4.18E harbor props",
		"target": "harbor_dock_edge",
		"player_position": Vector2(940.0, 704.0),
		"camera_zoom": Vector2(1.48, 1.48),
		"camera_offset": Vector2(20.0, 4.0),
		"direction": "left",
		"moving": true,
		"frame_index": 3,
	},
	{
		"filename": "g419_04_rear_service_connector_player_fit.png",
		"label": "Player in rear service connector, readable without overpowering narrow utility space",
		"target": "rear_service_connector",
		"player_position": Vector2(1005.0, 424.0),
		"camera_zoom": Vector2(1.44, 1.44),
		"camera_offset": Vector2(0.0, -10.0),
		"direction": "up",
		"moving": true,
		"frame_index": 1,
	},
	{
		"filename": "g419_05_player_near_g418e_props.png",
		"label": "Player near G-4.18E controlled prop family for palette, scale, and grounding proof",
		"target": "near_g418e_props",
		"player_position": Vector2(1062.0, 586.0),
		"camera_zoom": Vector2(1.82, 1.82),
		"camera_offset": Vector2(0.0, -22.0),
		"direction": "down",
		"moving": false,
		"frame_index": 0,
	},
	{
		"filename": "g419_06_player_near_buildings_scale_grounding.png",
		"label": "Player near buildings for doorway, street, and contact-scale proof",
		"target": "near_buildings_for_scale_grounding",
		"player_position": Vector2(676.0, 604.0),
		"camera_zoom": Vector2(1.72, 1.72),
		"camera_offset": Vector2(28.0, -40.0),
		"direction": "down",
		"moving": false,
		"frame_index": 0,
	},
	{
		"filename": "g419_07_player_layering_y_sort_proof.png",
		"label": "Player near layered objects/buildings for y-sort and depth proof",
		"target": "layered_objects_y_sort",
		"player_position": Vector2(780.0, 570.0),
		"camera_zoom": Vector2(1.82, 1.82),
		"camera_offset": Vector2(8.0, -46.0),
		"direction": "up",
		"moving": false,
		"frame_index": 0,
	},
	{
		"filename": "g419_08_facing_down_idle_proof.png",
		"label": "Facing proof: idle_down",
		"target": "facing_down_idle",
		"player_position": Vector2(804.0, 612.0),
		"camera_zoom": Vector2(2.08, 2.08),
		"camera_offset": Vector2(0.0, -34.0),
		"direction": "down",
		"moving": false,
		"frame_index": 0,
	},
	{
		"filename": "g419_09_facing_up_walk_proof.png",
		"label": "Facing/movement proof: walk_up",
		"target": "facing_up_walk",
		"player_position": Vector2(804.0, 612.0),
		"camera_zoom": Vector2(2.08, 2.08),
		"camera_offset": Vector2(0.0, -34.0),
		"direction": "up",
		"moving": true,
		"frame_index": 1,
	},
	{
		"filename": "g419_10_facing_left_walk_proof.png",
		"label": "Facing/movement proof: walk_left",
		"target": "facing_left_walk",
		"player_position": Vector2(804.0, 612.0),
		"camera_zoom": Vector2(2.08, 2.08),
		"camera_offset": Vector2(0.0, -34.0),
		"direction": "left",
		"moving": true,
		"frame_index": 1,
	},
	{
		"filename": "g419_11_facing_right_walk_proof.png",
		"label": "Facing/movement proof: walk_right",
		"target": "facing_right_walk",
		"player_position": Vector2(804.0, 612.0),
		"camera_zoom": Vector2(2.08, 2.08),
		"camera_offset": Vector2(0.0, -34.0),
		"direction": "right",
		"moving": true,
		"frame_index": 3,
	},
	{
		"filename": "g419_12_gameplay_zoom_player_readability.png",
		"label": "Gameplay zoom proof: player remains readable in normal play composition",
		"target": "gameplay_zoom_player_readability",
		"player_position": Vector2(676.0, 604.0),
		"camera_zoom": Vector2(1.66, 1.66),
		"camera_offset": Vector2(28.0, -40.0),
		"direction": "down",
		"moving": false,
		"frame_index": 0,
	},
	{
		"filename": "g419_13_wide_newport_player_readability.png",
		"label": "Wider Newport proof: player readable without dominating the harbor-city view",
		"target": "wide_newport_player_readability",
		"player_position": Vector2(800.0, 560.0),
		"camera_zoom": Vector2(1.06, 1.06),
		"camera_offset": Vector2(0.0, -16.0),
		"direction": "down",
		"moving": false,
		"frame_index": 0,
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

	var contact_sheet_result := _verify_contact_sheet()
	manifest["contact_sheet_proof"] = contact_sheet_result
	if String(contact_sheet_result.get("status", "")) != "PASS":
		return _fail(manifest, String(contact_sheet_result.get("failure", "Contact-sheet verification failed.")))

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
		manifest["screenshots"].append(file_result)
		if file_result.get("status", "") != "PASS":
			return _fail(manifest, String(file_result.get("failure", "Screenshot capture failed.")))

	manifest["status"] = "PASS"
	_write_manifest(manifest)
	print("PASS: G-4.19 runtime screenshots -> ", ProjectSettings.globalize_path(OUT_DIR))
	return 0


func _capture_one(capture: Dictionary, player: Node2D, camera: Camera2D) -> Dictionary:
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
		"direction": capture["direction"],
		"moving": capture["moving"],
		"frame_index": capture["frame_index"],
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
		"schema_id": "wayfarer.g419.runtime_screenshot_manifest.v1",
		"phase": "G-4.19",
		"status": "PENDING",
		"created_at": Time.get_datetime_string_from_system(true),
		"command": OS.get_environment("G419_CAPTURE_COMMAND"),
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
		"player_family": "player_wayfarer_foundation_g419",
		"contact_sheet_path": CONTACT_SHEET_PATH,
		"contact_sheet_absolute_path": ProjectSettings.globalize_path(CONTACT_SHEET_PATH),
		"required_views": [
			"tavern_inn_district",
			"commercial_avenue",
			"harbor_dock_edge",
			"rear_service_connector",
			"near_g418e_props",
			"near_buildings_for_scale_grounding",
			"layered_objects_y_sort",
			"facing_down_idle",
			"facing_up_walk",
			"facing_left_walk",
			"facing_right_walk",
			"gameplay_zoom_player_readability",
			"wide_newport_player_readability",
			"player_frame_contact_sheet",
		],
		"contact_sheet_proof": {},
		"warnings": [],
		"screenshots": [],
	}


func _project_setting(setting_name: String) -> String:
	if ProjectSettings.has_setting(setting_name):
		return str(ProjectSettings.get_setting(setting_name))
	return ""


func _verify_contact_sheet() -> Dictionary:
	var path := ProjectSettings.globalize_path(CONTACT_SHEET_PATH)
	var image := Image.new()
	var error := image.load(path)
	var result := {
		"status": "PENDING",
		"path": CONTACT_SHEET_PATH,
		"absolute_path": path,
		"dimensions": {},
		"png_verification": {},
	}
	if error != OK:
		result["status"] = "FAIL"
		result["failure"] = "Could not load contact sheet: %s error=%s" % [CONTACT_SHEET_PATH, error]
		return result
	result["dimensions"] = {"w": image.get_width(), "h": image.get_height()}
	var verification := {
		"status": "PASS",
		"width": image.get_width(),
		"height": image.get_height(),
	}
	if image.get_width() < 500 or image.get_height() < 500:
		result["status"] = "FAIL"
		result["failure"] = "Contact sheet dimensions were too small for review proof."
		return result
	result["png_verification"] = verification
	result["status"] = "PASS"
	return result


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
