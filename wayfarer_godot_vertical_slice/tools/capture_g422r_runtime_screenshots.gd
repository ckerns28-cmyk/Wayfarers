extends SceneTree

const BUILD_INFO := preload("res://scripts/BuildInfo.gd")
const MAIN_SCENE := preload("res://scenes/Main.tscn")

const OUT_DIR := "res://artifacts/review/g422r_runtime_screenshots"
const MANIFEST_FILENAME := "g422r_runtime_screenshot_manifest.json"
const VIEWPORT_SIZE := Vector2i(1600, 1000)
const INITIAL_WAIT_FRAMES := 36
const CAPTURE_WAIT_FRAMES := 12

const CAPTURES := [
	{"filename": "g422r_01_wide_newport_normal_gameplay_view.png", "target": "wide_newport_normal_gameplay_view", "label": "G-4.22R wide Newport normal gameplay view with HUD, player, NPCs, buildings, streets, and harbor.", "player_position": Vector2(760, 604), "camera_zoom": Vector2(1.16, 1.16), "camera_offset": Vector2(20, -22), "direction": "down", "moving": false, "frame_index": 0},
	{"filename": "g422r_02_player_near_tavern_inn_district.png", "target": "player_near_tavern_inn_district", "label": "G-4.22R player near Tavern/Inn district.", "player_position": Vector2(276, 600), "camera_zoom": Vector2(1.58, 1.58), "camera_offset": Vector2(-20, -34), "direction": "left", "moving": false, "frame_index": 0, "no_hud": true},
	{"filename": "g422r_03_player_near_commercial_avenue.png", "target": "player_near_commercial_avenue", "label": "G-4.22R player near commercial avenue and shopfront signs.", "player_position": Vector2(1070, 574), "camera_zoom": Vector2(1.52, 1.52), "camera_offset": Vector2(12, -20), "direction": "right", "moving": true, "frame_index": 1, "no_hud": true},
	{"filename": "g422r_04_player_at_harbor_dock_edge.png", "target": "player_at_harbor_dock_edge", "label": "G-4.22R player at harbor/dock edge beside atelier harbor props.", "player_position": Vector2(824, 710), "camera_zoom": Vector2(1.36, 1.36), "camera_offset": Vector2(0, -38), "direction": "down", "moving": false, "frame_index": 0, "no_hud": true},
	{"filename": "g422r_05_player_near_npcs.png", "target": "player_near_npcs", "label": "G-4.22R player near manifest-backed NPCs.", "player_position": Vector2(392, 676), "camera_zoom": Vector2(1.70, 1.70), "camera_offset": Vector2(-14, -54), "direction": "right", "moving": false, "frame_index": 0, "no_hud": true},
	{"filename": "g422r_06_player_near_props_signs_markers.png", "target": "player_near_props_signs_markers", "label": "G-4.22R player near props, signs, markers, and wayfinding proof.", "player_position": Vector2(1010, 594), "camera_zoom": Vector2(1.70, 1.70), "camera_offset": Vector2(24, -44), "direction": "down", "moving": false, "frame_index": 0, "no_hud": true},
	{"filename": "g422r_07_player_near_layered_y_sort_objects.png", "target": "player_near_layered_y_sort_objects", "label": "G-4.22R player near layered buildings and objects for y-sort proof.", "player_position": Vector2(704, 392), "camera_zoom": Vector2(1.30, 1.30), "camera_offset": Vector2(112, -44), "direction": "down", "moving": false, "frame_index": 0, "no_hud": true},
	{"filename": "g422r_08_gameplay_zoom_readability_proof.png", "target": "gameplay_zoom_readability_proof", "label": "G-4.22R gameplay zoom readability proof.", "player_position": Vector2(736, 620), "camera_zoom": Vector2(1.86, 1.86), "camera_offset": Vector2(18, -58), "direction": "down", "moving": false, "frame_index": 0, "no_hud": true},
	{"filename": "g422r_09_debug_overlays_disabled_proof.png", "target": "debug_overlays_disabled_proof", "label": "G-4.22R debug overlays disabled proof.", "player_position": Vector2(800, 560), "camera_zoom": Vector2(1.02, 1.02), "camera_offset": Vector2(0, -16), "direction": "down", "moving": false, "frame_index": 0, "no_hud": true, "debug_overlay": false},
	{"filename": "g422r_12_wider_town_cohesion_no_placeholder_mix.png", "target": "wider_town_cohesion_no_placeholder_mix", "label": "G-4.22R wider town cohesion proof without mixed atelier/placeholder character styles.", "player_position": Vector2(800, 560), "camera_zoom": Vector2(0.82, 0.82), "camera_offset": Vector2(0, -32), "direction": "down", "moving": false, "frame_index": 0, "no_hud": true},
]

const ASSET_PROOFS := [
	{"source": "res://art_pipeline/player_identity/contact_sheets/newport_atelier_characters_g422r_contact_sheet.png", "filename": "g422r_10_player_npc_contact_sheet_proof.png", "target": "player_npc_contact_sheet_proof", "label": "G-4.22R player/NPC contact sheet proof."},
	{"source": "res://art_pipeline/newport_atelier/contact_sheets/newport_atelier_sign_shop_markers_contact_sheet.png", "filename": "g422r_11_marker_sign_world_object_contact_sheet_proof.png", "target": "marker_sign_world_object_contact_sheet_proof", "label": "G-4.22R marker/sign/world-object contact sheet proof."},
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

	var main := MAIN_SCENE.instantiate()
	root.add_child(main)
	await _wait_for_render(INITIAL_WAIT_FRAMES)

	var player := main.get_node_or_null("World/Player") as Node2D
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

	for proof in ASSET_PROOFS:
		var proof_result := _copy_asset_proof(proof)
		manifest["screenshots"].append(proof_result)
		if proof_result.get("status", "") != "PASS":
			return _fail(manifest, String(proof_result.get("failure", "Asset proof capture failed.")))

	manifest["status"] = "PASS"
	_write_manifest(manifest)
	print("PASS: G-4.22R runtime screenshots -> ", ProjectSettings.globalize_path(OUT_DIR))
	return 0


func _capture_one(capture: Dictionary, main: Node, player: Node2D, camera: Camera2D) -> Dictionary:
	var no_hud := bool(capture.get("no_hud", false))
	var debug_overlay := bool(capture.get("debug_overlay", false))
	if main.has_method("set_review_screenshot_mode"):
		main.call("set_review_screenshot_mode", no_hud)
	if main.has_method("set_debug_overlay"):
		main.call("set_debug_overlay", debug_overlay)
	if main.has_method("set_green_origin_lab_mode"):
		main.call("set_green_origin_lab_mode", false)
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
	var output_path := "%s/%s" % [OUT_DIR, capture["filename"]]
	var result := _base_screenshot_result(capture, output_path, image.get_width(), image.get_height())
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
	print("Wrote ", output_path)
	return result


func _copy_asset_proof(proof: Dictionary) -> Dictionary:
	var source_path := String(proof["source"])
	var output_path := "%s/%s" % [OUT_DIR, proof["filename"]]
	var image := Image.new()
	var load_error := image.load(ProjectSettings.globalize_path(source_path))
	var result := _base_screenshot_result(proof, output_path, 0, 0)
	if load_error != OK:
		result["status"] = "FAIL"
		result["failure"] = "Could not load asset proof %s error=%s" % [source_path, load_error]
		return result
	result["dimensions"] = {"w": image.get_width(), "h": image.get_height()}
	var save_error := image.save_png(output_path)
	if save_error != OK:
		result["status"] = "FAIL"
		result["failure"] = "Could not save asset proof %s error=%s" % [output_path, save_error]
		return result
	result["png_verification"] = _verify_png_pixels(image)
	result["status"] = "PASS"
	print("Wrote ", output_path)
	return result


func _base_screenshot_result(capture: Dictionary, output_path: String, width: int, height: int) -> Dictionary:
	return {
		"filename": capture["filename"],
		"label": capture["label"],
		"target": capture["target"],
		"path": output_path,
		"absolute_path": ProjectSettings.globalize_path(output_path),
		"hud_visible": not bool(capture.get("no_hud", false)),
		"debug_overlay": bool(capture.get("debug_overlay", false)),
		"green_origin_lab": false,
		"dimensions": {"w": width, "h": height},
		"png_verification": {},
		"status": "PENDING",
	}


func _wait_for_render(frame_count: int) -> void:
	for _i in range(frame_count):
		await process_frame
	await RenderingServer.frame_post_draw


func _base_manifest() -> Dictionary:
	return {
		"schema_id": "wayfarer.g422r.runtime_screenshot_manifest.v1",
		"phase": "G-4.22R",
		"status": "PENDING",
		"created_at": Time.get_datetime_string_from_system(true),
		"command": OS.get_environment("G422R_CAPTURE_COMMAND"),
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
			"wide_newport_normal_gameplay_view",
			"player_near_tavern_inn_district",
			"player_near_commercial_avenue",
			"player_at_harbor_dock_edge",
			"player_near_npcs",
			"player_near_props_signs_markers",
			"player_near_layered_y_sort_objects",
			"gameplay_zoom_readability_proof",
			"debug_overlays_disabled_proof",
			"player_npc_contact_sheet_proof",
			"marker_sign_world_object_contact_sheet_proof",
			"wider_town_cohesion_no_placeholder_mix",
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
	for y_step in range(12):
		for x_step in range(16):
			var x := clampi(int((float(x_step) + 0.5) * float(width) / 16.0), 0, width - 1)
			var y := clampi(int((float(y_step) + 0.5) * float(height) / 12.0), 0, height - 1)
			var color := image.get_pixel(x, y)
			var luminance := color.r * 0.2126 + color.g * 0.7152 + color.b * 0.0722
			min_luminance = minf(min_luminance, luminance)
			max_luminance = maxf(max_luminance, luminance)
			var bucket := "%s_%s_%s" % [int(color.r * 31.0), int(color.g * 31.0), int(color.b * 31.0)]
			color_buckets[bucket] = true
			sample_count += 1
	var luminance_range := max_luminance - min_luminance
	var result := {"status": "PASS", "sample_count": sample_count, "distinct_color_buckets": color_buckets.size(), "luminance_range": snappedf(luminance_range, 0.001)}
	if color_buckets.size() < 8 or luminance_range < 0.08:
		result["status"] = "FAIL"
		result["failure"] = "PNG appeared blank or too uniform: buckets=%s luminance_range=%.3f" % [color_buckets.size(), luminance_range]
	return result


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
