extends SceneTree

const BUILD_INFO := preload("res://scripts/BuildInfo.gd")
const MAIN_SCENE := preload("res://scenes/Main.tscn")

const OUT_DIR := "res://artifacts/review/g421b_runtime_screenshots"
const MANIFEST_FILENAME := "g421b_runtime_screenshot_manifest.json"
const VIEWPORT_SIZE := Vector2i(1600, 1000)
const INITIAL_WAIT_FRAMES := 36
const CAPTURE_WAIT_FRAMES := 12

const CAPTURES := [
	{
		"filename": "g421b_01_whole_town.png",
		"label": "whole town / broad Newport view",
		"target": "whole_town",
		"player_position": Vector2(800.0, 575.0),
		"camera_zoom": Vector2(0.72, 0.72),
		"camera_offset": Vector2(0.0, -20.0),
	},
	{
		"filename": "g421b_02_tavern_inn_closeup.png",
		"label": "Tavern/Inn close-up near b_inn_tavern",
		"target": "b_inn_tavern",
		"player_position": Vector2(254.0, 616.0),
		"camera_zoom": Vector2(1.18, 1.18),
		"camera_offset": Vector2(0.0, -92.0),
	},
	{
		"filename": "g421b_03_market_spine.png",
		"label": "market spine near b_mercantile",
		"target": "b_mercantile",
		"player_position": Vector2(580.0, 616.0),
		"camera_zoom": Vector2(1.12, 1.12),
		"camera_offset": Vector2(0.0, -72.0),
	},
	{
		"filename": "g421b_04_wharf.png",
		"label": "wharf near b_dock_warehouse",
		"target": "b_dock_warehouse",
		"player_position": Vector2(486.0, 758.0),
		"camera_zoom": Vector2(1.04, 1.04),
		"camera_offset": Vector2(0.0, -64.0),
	},
	{
		"filename": "g421b_05_res_small.png",
		"label": "residential street near b_res_small",
		"target": "b_res_small",
		"player_position": Vector2(437.0, 432.0),
		"camera_zoom": Vector2(1.02, 1.02),
		"camera_offset": Vector2(0.0, -44.0),
	},
	{
		"filename": "g421b_06_cooperage_shed.png",
		"label": "service lane near b_cooperage_shed",
		"target": "b_cooperage_shed",
		"player_position": Vector2(264.0, 432.0),
		"camera_zoom": Vector2(1.08, 1.08),
		"camera_offset": Vector2(0.0, -44.0),
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
	print("PASS: G-4.21B runtime screenshots -> ", ProjectSettings.globalize_path(OUT_DIR))
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

	result["status"] = "PASS"
	print("Wrote ", output_path, " ", width, "x", height)
	return result


func _wait_for_render(frame_count: int) -> void:
	for _i in range(frame_count):
		await process_frame
	await RenderingServer.frame_post_draw


func _base_manifest() -> Dictionary:
	return {
		"schema_id": "wayfarer.g421b.runtime_screenshot_manifest.v1",
		"phase": "G-4.21B",
		"status": "PENDING",
		"created_at": Time.get_datetime_string_from_system(true),
		"command": OS.get_environment("G421B_CAPTURE_COMMAND"),
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
