extends SceneTree

const MAIN_SCENE := preload("res://scenes/Main.tscn")

const OUT_DIR := "res://artifacts/review/g22_ovi1_motion_proof"
const MANIFEST_FILENAME := "g22_player_motion_proof_manifest.json"
const CONTACT_SHEET_FILENAME := "g22_player_motion_contact_sheet.png"
const VIEWPORT_SIZE := Vector2i(1280, 720)
const INITIAL_WAIT_FRAMES := 36
const START_POSITION := Vector2(675.0, 612.0)
const CAMERA_ZOOM := Vector2(2.05, 2.05)
const CAMERA_OFFSET := Vector2(0.0, -30.0)
const WALK_KEY := KEY_D
const WALK_SAMPLE_STEPS := [6, 8, 8, 8, 8, 8, 8, 8]


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
		return _fail(manifest, "Refusing to capture player motion proof with the headless display driver.")

	var main := MAIN_SCENE.instantiate()
	root.add_child(main)
	await _wait_for_render(INITIAL_WAIT_FRAMES)
	_prepare_scene_for_motion_proof(main)

	var player := main.get_node_or_null("World/Player") as Node2D
	if player == null:
		return _fail(manifest, "Player node not found.")
	var camera := player.get_node_or_null("Camera2D") as Camera2D
	if camera == null:
		return _fail(manifest, "Player Camera2D node not found.")
	_set_key(WALK_KEY, false)
	_configure_player_camera(player, camera)
	await _wait_for_render(4)

	manifest["player_motion_contract"] = _jsonify(player.call("player_motion_corrective_contract") if player.has_method("player_motion_corrective_contract") else {})
	manifest["character_motion_contract"] = _jsonify(player.call("character_motion_contract") if player.has_method("character_motion_contract") else {})

	var frame_images := []
	var idle_result := await _capture_frame(player, 0, "idle_anchor_before_walk", frame_images)
	manifest["frame_sequence"].append(idle_result)
	if String(idle_result.get("status", "")) != "PASS":
		return _fail(manifest, String(idle_result.get("failure", "Idle frame capture failed.")))

	_set_key(WALK_KEY, true)
	var elapsed_frames := 0
	for sample_index in range(WALK_SAMPLE_STEPS.size()):
		var step_frames := int(WALK_SAMPLE_STEPS[sample_index])
		elapsed_frames += step_frames
		await _wait_physics_frames(step_frames)
		var frame_result := await _capture_frame(player, sample_index + 1, "walk_right_actual_displacement_%02d" % elapsed_frames, frame_images)
		manifest["frame_sequence"].append(frame_result)
		if String(frame_result.get("status", "")) != "PASS":
			_set_key(WALK_KEY, false)
			return _fail(manifest, String(frame_result.get("failure", "Walk frame capture failed.")))
	_set_key(WALK_KEY, false)
	await _wait_for_render(4)

	var evaluation := _evaluate_sequence(manifest["frame_sequence"])
	manifest["motion_evaluation"] = evaluation
	if String(evaluation.get("status", "")) != "PASS":
		return _fail(manifest, String(evaluation.get("failure", "Player motion evaluation failed.")))

	var contact_sheet := _write_contact_sheet(frame_images)
	manifest["contact_sheet"] = contact_sheet
	if String(contact_sheet.get("status", "")) != "PASS":
		return _fail(manifest, String(contact_sheet.get("failure", "Contact sheet failed.")))

	manifest["status"] = "PASS"
	_write_manifest(manifest)
	print("PASS: G-22 player motion proof -> ", ProjectSettings.globalize_path(OUT_DIR))
	return 0


func _prepare_scene_for_motion_proof(main: Node) -> void:
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
	var dialogue_panel := main.get_node_or_null("HUD/DialoguePanel") as Control
	if dialogue_panel != null:
		dialogue_panel.visible = false


func _configure_player_camera(player: Node2D, camera: Camera2D) -> void:
	player.global_position = START_POSITION
	if player.has_method("set_prompt_suppressed"):
		player.call("set_prompt_suppressed", true)
	if player.has_method("set_review_visual_state"):
		player.call("set_review_visual_state", "right", false, 0)
	camera.enabled = true
	camera.position_smoothing_enabled = false
	camera.limit_smoothed = false
	camera.limit_left = 0
	camera.limit_top = 0
	camera.limit_right = 2400
	camera.limit_bottom = 1600
	camera.zoom = CAMERA_ZOOM
	camera.offset = CAMERA_OFFSET
	camera.make_current()
	camera.reset_smoothing()


func _capture_frame(player: Node2D, sample_index: int, sample_id: String, frame_images: Array) -> Dictionary:
	await RenderingServer.frame_post_draw
	var image := root.get_texture().get_image()
	var filename := "g22_player_motion_frame_%02d.png" % sample_index
	var output_path := "%s/%s" % [OUT_DIR, filename]
	var state := _player_debug_state(player)
	var result := {
		"filename": filename,
		"sample_id": sample_id,
		"path": output_path,
		"absolute_path": ProjectSettings.globalize_path(output_path),
		"player_state": _jsonify(state),
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
	frame_images.append(image)
	result["status"] = "PASS"
	print("Wrote ", output_path)
	return result


func _player_debug_state(player: Node2D) -> Dictionary:
	if player.has_method("player_motion_debug_state"):
		return player.call("player_motion_debug_state") as Dictionary
	return {
		"global_position": player.global_position,
		"animation": "",
		"frame": -1,
		"visual_position": Vector2.ZERO,
		"visual_rotation": 0.0,
		"shadow_scale": Vector2.ONE,
		"shadow_alpha": 0.0,
		"actual_displacement": Vector2.ZERO,
	}


func _evaluate_sequence(sequence: Array) -> Dictionary:
	if sequence.size() < 6:
		return {"status": "FAIL", "failure": "Motion proof needs at least six frames."}
	var first_state: Dictionary = sequence[0].get("player_state", {})
	var last_state: Dictionary = sequence[sequence.size() - 1].get("player_state", {})
	var first_position := _dict_to_vector2(first_state.get("global_position", {}))
	var last_position := _dict_to_vector2(last_state.get("global_position", {}))
	var total_distance := first_position.distance_to(last_position)
	var animation_frames := {}
	var visual_offsets := {}
	var shadow_scales := {}
	var moving_animation_count := 0
	var nonzero_actual_displacement_count := 0
	for i in range(1, sequence.size()):
		var state: Dictionary = sequence[i].get("player_state", {})
		var animation := String(state.get("animation", ""))
		if animation.begins_with("walk_"):
			moving_animation_count += 1
		animation_frames[str(state.get("frame", ""))] = true
		visual_offsets[_vector_key(_dict_to_vector2(state.get("visual_position", {})))] = true
		shadow_scales[_vector_key(_dict_to_vector2(state.get("shadow_scale", {})))] = true
		if _dict_to_vector2(state.get("actual_displacement", {})).length() > 0.01:
			nonzero_actual_displacement_count += 1
	var result := {
		"status": "PASS",
		"total_position_delta_px": snappedf(total_distance, 0.001),
		"unique_animation_frames": animation_frames.size(),
		"unique_visual_offsets": visual_offsets.size(),
		"unique_shadow_scales": shadow_scales.size(),
		"moving_animation_samples": moving_animation_count,
		"nonzero_actual_displacement_samples": nonzero_actual_displacement_count,
		"no_static_sprite_translation": true,
	}
	if total_distance < 70.0:
		result["status"] = "FAIL"
		result["failure"] = "Player did not travel far enough for motion proof."
	elif animation_frames.size() < 3:
		result["status"] = "FAIL"
		result["failure"] = "Walk proof did not show enough distinct animation frames."
	elif visual_offsets.size() < 3:
		result["status"] = "FAIL"
		result["failure"] = "Walk proof did not show body bob/sway offsets."
	elif shadow_scales.size() < 2:
		result["status"] = "FAIL"
		result["failure"] = "Walk proof did not show shadow pulse."
	elif moving_animation_count < 5 or nonzero_actual_displacement_count < 5:
		result["status"] = "FAIL"
		result["failure"] = "Walk proof did not show sustained actual-displacement animation."
	return result


func _write_contact_sheet(frame_images: Array) -> Dictionary:
	if frame_images.is_empty():
		return {"status": "FAIL", "failure": "No frame images available for contact sheet."}
	var thumb_size := Vector2i(320, 180)
	var columns := 3
	var rows := int(ceil(float(frame_images.size()) / float(columns)))
	var sheet := Image.create_empty(columns * thumb_size.x, rows * thumb_size.y, false, Image.FORMAT_RGBA8)
	sheet.fill(Color(0.025, 0.022, 0.018, 1.0))
	for i in range(frame_images.size()):
		var thumb: Image = (frame_images[i] as Image).duplicate()
		thumb.convert(Image.FORMAT_RGBA8)
		thumb.resize(thumb_size.x, thumb_size.y, Image.INTERPOLATE_LANCZOS)
		var column := i % columns
		var row := int(i / columns)
		sheet.blit_rect(thumb, Rect2i(Vector2i.ZERO, thumb_size), Vector2i(column * thumb_size.x, row * thumb_size.y))
	var output_path := "%s/%s" % [OUT_DIR, CONTACT_SHEET_FILENAME]
	var save_error := sheet.save_png(output_path)
	if save_error != OK:
		return {"status": "FAIL", "failure": "Could not save contact sheet %s error=%s" % [output_path, save_error]}
	return {
		"status": "PASS",
		"filename": CONTACT_SHEET_FILENAME,
		"path": output_path,
		"absolute_path": ProjectSettings.globalize_path(output_path),
		"dimensions": {"w": sheet.get_width(), "h": sheet.get_height()},
		"png_verification": _verify_png_pixels(sheet),
	}


func _set_key(keycode: int, pressed: bool) -> void:
	var event := InputEventKey.new()
	event.keycode = keycode
	event.physical_keycode = keycode
	event.pressed = pressed
	Input.parse_input_event(event)
	Input.flush_buffered_events()


func _wait_for_render(frame_count: int) -> void:
	for _i in range(frame_count):
		await process_frame
	await RenderingServer.frame_post_draw


func _wait_physics_frames(frame_count: int) -> void:
	for _i in range(frame_count):
		await physics_frame
	await RenderingServer.frame_post_draw


func _base_manifest() -> Dictionary:
	return {
		"schema_id": "wayfarer.g22.player_motion_proof.v1",
		"phase": "G-22",
		"status": "PENDING",
		"created_at": Time.get_datetime_string_from_system(true),
		"command": OS.get_environment("G22_PLAYER_MOTION_CAPTURE_COMMAND"),
		"godot_version": Engine.get_version_info().get("string", ""),
		"os": OS.get_name(),
		"display_driver": DisplayServer.get_name(),
		"rendering_method": _project_setting("rendering/renderer/rendering_method"),
		"headless": DisplayServer.get_name().to_lower() == "headless",
		"output_dir": OUT_DIR,
		"absolute_output_dir": ProjectSettings.globalize_path(OUT_DIR),
		"viewport_size": {"w": VIEWPORT_SIZE.x, "h": VIEWPORT_SIZE.y},
		"proof_intent": "Demonstrate that the player is not a static sprite translating across the map: actual displacement advances frames, bob/sway, and shadow pulse on the clear waterfront avenue lane, not on a building roof.",
		"frame_sequence": [],
		"motion_evaluation": {},
		"contact_sheet": {},
	}


func _project_setting(setting_name: String) -> String:
	if ProjectSettings.has_setting(setting_name):
		return str(ProjectSettings.get_setting(setting_name))
	return ""


func _verify_png_pixels(image: Image) -> Dictionary:
	var samples := 0
	var color_buckets := {}
	var min_luminance := 10.0
	var max_luminance := -10.0
	for y_step in range(8):
		for x_step in range(10):
			var x := clampi(int((float(x_step) + 0.5) * float(image.get_width()) / 10.0), 0, image.get_width() - 1)
			var y := clampi(int((float(y_step) + 0.5) * float(image.get_height()) / 8.0), 0, image.get_height() - 1)
			var color := image.get_pixel(x, y)
			var luminance := color.r * 0.2126 + color.g * 0.7152 + color.b * 0.0722
			min_luminance = minf(min_luminance, luminance)
			max_luminance = maxf(max_luminance, luminance)
			color_buckets["%s_%s_%s" % [int(color.r * 31.0), int(color.g * 31.0), int(color.b * 31.0)]] = true
			samples += 1
	var luminance_range := max_luminance - min_luminance
	if color_buckets.size() < 10 or luminance_range < 0.08:
		return {"status": "FAIL", "failure": "PNG appeared blank or too uniform.", "sample_count": samples, "distinct_color_buckets": color_buckets.size(), "luminance_range": snappedf(luminance_range, 0.001)}
	return {"status": "PASS", "sample_count": samples, "distinct_color_buckets": color_buckets.size(), "luminance_range": snappedf(luminance_range, 0.001)}


func _dict_to_vector2(value: Variant) -> Vector2:
	if value is Vector2:
		return value
	if value is Dictionary:
		return Vector2(float(value.get("x", 0.0)), float(value.get("y", 0.0)))
	return Vector2.ZERO


func _vector_key(value: Vector2) -> String:
	return "%.2f,%.2f" % [snappedf(value.x, 0.01), snappedf(value.y, 0.01)]


func _jsonify(value: Variant) -> Variant:
	if value is Vector2:
		return {"x": snappedf(value.x, 0.001), "y": snappedf(value.y, 0.001)}
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


func _write_manifest(manifest: Dictionary) -> void:
	var output_path := "%s/%s" % [OUT_DIR, MANIFEST_FILENAME]
	var file := FileAccess.open(output_path, FileAccess.WRITE)
	if file == null:
		push_error("Could not write G-22 player motion manifest: " + output_path)
		return
	file.store_string(JSON.stringify(_jsonify(manifest), "\t"))
	file.store_line("")
	file.close()


func _fail(manifest: Dictionary, message: String) -> int:
	manifest["status"] = "FAIL"
	manifest["failure"] = message
	_write_manifest(manifest)
	push_error(message)
	return 1
