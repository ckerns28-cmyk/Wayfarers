extends SceneTree

const MAIN_SCENE := preload("res://scenes/Main.tscn")

const OUT_DIR := "res://artifacts/review/g17_runtime_screenshots"
const MOTION_OUT_DIR := "res://artifacts/review/g17_motion_proof"
const MANIFEST_FILENAME := "g17_runtime_screenshot_manifest.json"
const MOTION_TRACE_FILENAME := "g17_island_npc_motion_trace.json"
const VIEWPORT_SIZE := Vector2i(1600, 1000)
const INITIAL_WAIT_FRAMES := 36
const CAPTURE_WAIT_FRAMES := 12

const CAPTURES := [
	{
		"filename": "g17_01_island_life_wide.png",
		"label": "island life wide / farmhand, courier, patrol, dock runner, and return contact make the island feel inhabited",
		"target": "island_life_wide",
		"player_position": Vector2(2048.0, 574.0),
		"camera_zoom": Vector2(0.82, 0.82),
		"camera_offset": Vector2(-104.0, -86.0),
		"player_direction": "right",
		"player_moving": true,
		"player_frame": 1,
		"focus_npc_id": "isla_brooke_farmhand",
		"proof_time": 6.2
	},
	{
		"filename": "g17_02_farmhand_service_edge.png",
		"label": "farmhand service edge / farm life anchors the pasture crossing and points the player toward the signal rise",
		"target": "farmhand_service_edge",
		"player_position": Vector2(1886.0, 600.0),
		"camera_zoom": Vector2(1.12, 1.12),
		"camera_offset": Vector2(-116.0, -64.0),
		"player_direction": "up",
		"player_moving": false,
		"player_frame": 0,
		"focus_npc_id": "isla_brooke_farmhand",
		"proof_time": 6.4
	},
	{
		"filename": "g17_03_dock_runner_cove_watch.png",
		"label": "dock runner cove watch / harbor labor extends into the hidden landing and missing-manifest clue path",
		"target": "dock_runner_cove_watch",
		"player_position": Vector2(2220.0, 742.0),
		"camera_zoom": Vector2(1.35, 1.35),
		"camera_offset": Vector2(-100.0, -20.0),
		"player_direction": "up",
		"player_moving": false,
		"player_frame": 0,
		"focus_npc_id": "tomas_reed_dock_runner",
		"proof_time": 5.5
	},
	{
		"filename": "g17_04_suspicious_courier_old_road.png",
		"label": "suspicious courier old road / coded whisper energy carries from tavern rumor into island history",
		"target": "suspicious_courier_old_road",
		"player_position": Vector2(2140.0, 454.0),
		"camera_zoom": Vector2(1.35, 1.35),
		"camera_offset": Vector2(-120.0, 80.0),
		"player_direction": "up",
		"player_moving": false,
		"player_frame": 0,
		"focus_npc_id": "elias_ward_suspicious_courier",
		"proof_time": 8.4
	},
	{
		"filename": "g17_05_signal_patrol_overlook.png",
		"label": "signal patrol overlook / living coastal watch turns the signal point into threat and route memory",
		"target": "signal_patrol_overlook",
		"player_position": Vector2(2296.0, 378.0),
		"camera_zoom": Vector2(1.60, 1.60),
		"camera_offset": Vector2(-120.0, 80.0),
		"player_direction": "up",
		"player_moving": false,
		"player_frame": 0,
		"focus_npc_id": "mara_oren_coast_patrol",
		"proof_time": 8.8
	},
	{
		"filename": "g17_06_return_rumor_contact_debug_disabled.png",
		"label": "return rumor contact debug disabled / return path has a grounded social hook without HUD or debug overlays",
		"target": "return_rumor_contact_debug_disabled",
		"player_position": Vector2(1788.0, 674.0),
		"camera_zoom": Vector2(1.08, 1.08),
		"camera_offset": Vector2(-72.0, -76.0),
		"player_direction": "up",
		"player_moving": false,
		"player_frame": 0,
		"focus_npc_id": "",
		"proof_time": 13.2
	},
]

const REQUIRED_MOTION_FRAMES := [
	"g17_motion_frame_00.png",
	"g17_motion_frame_01.png",
	"g17_motion_frame_02.png",
	"g17_motion_frame_03.png",
	"g17_motion_frame_04.png",
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
	var motion_error := DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(MOTION_OUT_DIR))
	if motion_error != OK:
		return _fail(manifest, "Could not create motion proof directory: %s error=%s" % [MOTION_OUT_DIR, motion_error])
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
	if main.has_method("set_starter_village_ambient_barks_enabled"):
		main.call("set_starter_village_ambient_barks_enabled", false)
	if main.has_method("set_opening_island_ambient_barks_enabled"):
		main.call("set_opening_island_ambient_barks_enabled", false)
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
	camera.limit_left = 0
	camera.limit_top = 0
	camera.limit_right = 2400
	camera.limit_bottom = 1600
	camera.make_current()

	manifest["opening_island_npc_encounter_contract_initial"] = _jsonify(main.call("opening_island_npc_encounter_contract") if main.has_method("opening_island_npc_encounter_contract") else {})
	manifest["opening_island_atelier_asset_family_contract"] = _jsonify(main.call("opening_island_atelier_asset_family_contract") if main.has_method("opening_island_atelier_asset_family_contract") else {})
	manifest["debug_overlays_disabled"] = true
	manifest["no_hud_capture"] = true

	var motion_result: Dictionary = await _capture_motion_proof(main, player, camera)
	manifest["motion_proof_path"] = "%s/%s" % [MOTION_OUT_DIR, MOTION_TRACE_FILENAME]
	manifest["island_ambient_motion_proof_sequence"] = _jsonify(motion_result)
	if String(motion_result.get("status", "")) != "PASS":
		return _fail(manifest, String(motion_result.get("failure", "G-17 motion proof failed.")))

	for capture in CAPTURES:
		var file_result: Dictionary = await _capture_one(capture, main, player, camera)
		manifest["screenshots"].append(file_result)
		if file_result.get("status", "") != "PASS":
			return _fail(manifest, String(file_result.get("failure", "Screenshot capture failed.")))

	manifest["opening_island_npc_encounter_contract_final"] = _jsonify(main.call("opening_island_npc_encounter_contract") if main.has_method("opening_island_npc_encounter_contract") else {})
	manifest["status"] = "PASS"
	_write_manifest(manifest)
	print("PASS: G-17 runtime screenshots -> ", ProjectSettings.globalize_path(OUT_DIR))
	return 0


func _capture_motion_proof(main: Node, player: Node2D, camera: Camera2D) -> Dictionary:
	var timestamps := [0.0, 4.4, 8.8, 13.2, 17.6]
	var focus_ids := [
		"isla_brooke_farmhand",
		"tomas_reed_dock_runner",
		"elias_ward_suspicious_courier",
		"mara_oren_coast_patrol",
		"annelise_crow_rumor_contact",
	]
	var proof := {
		"schema_id": "wayfarer.g17.island_npc_motion_trace.v1",
		"phase": "G-17",
		"status": "PENDING",
		"motion_policy": "stationary_grounded_facing_bark_until_dedicated_walk_sheets",
		"no_hover_glide_slide": true,
		"route_walking_enabled": false,
		"frame_sequence": [],
		"snapshots": [],
		"position_drift_detected": false,
	}
	player.global_position = Vector2(2048.0, 602.0)
	if player.has_method("set_review_visual_state"):
		player.call("set_review_visual_state", "right", true, 1)
	if player.has_method("set_prompt_suppressed"):
		player.call("set_prompt_suppressed", true)
	_hide_dialogue(main)
	camera.zoom = Vector2(0.84, 0.84)
	camera.offset = Vector2(-90.0, -28.0)
	camera.reset_smoothing()
	for i in range(timestamps.size()):
		var timestamp := float(timestamps[i])
		var focus_id := String(focus_ids[i])
		var snapshot: Dictionary = {}
		if main.has_method("debug_apply_opening_island_ambient_tick"):
			snapshot = main.call("debug_apply_opening_island_ambient_tick", timestamp, true, focus_id) as Dictionary
		proof["snapshots"].append(_jsonify(snapshot))
		proof["position_drift_detected"] = bool(proof["position_drift_detected"]) or bool(snapshot.get("position_drift_detected", true))
		await _wait_for_render(CAPTURE_WAIT_FRAMES)
		var image: Image = root.get_texture().get_image()
		var filename: String = "g17_motion_frame_%02d.png" % i
		var output_path: String = "%s/%s" % [MOTION_OUT_DIR, filename]
		var save_error: Error = image.save_png(output_path)
		if save_error != OK:
			proof["status"] = "FAIL"
			proof["failure"] = "Could not save motion frame %s error=%s" % [output_path, save_error]
			_write_json(proof, "%s/%s" % [MOTION_OUT_DIR, MOTION_TRACE_FILENAME])
			return proof
		proof["frame_sequence"].append({
			"filename": filename,
			"path": output_path,
			"absolute_path": ProjectSettings.globalize_path(output_path),
			"timestamp_seconds": timestamp,
			"focus_npc_id": focus_id,
			"dimensions": {"w": image.get_width(), "h": image.get_height()},
			"png_verification": _verify_png_pixels(image),
		})
	var actor_count := 0
	if not proof["snapshots"].is_empty():
		var first_snapshot: Dictionary = proof["snapshots"][0]
		actor_count = int(first_snapshot.get("actor_count", 0))
	if bool(proof["position_drift_detected"]):
		proof["status"] = "FAIL"
		proof["failure"] = "Opening island NPC position drift detected."
	elif actor_count < 5:
		proof["status"] = "FAIL"
		proof["failure"] = "Expected at least five opening island ambient actors."
	else:
		proof["status"] = "PASS"
		proof["actor_count"] = actor_count
	_write_json(proof, "%s/%s" % [MOTION_OUT_DIR, MOTION_TRACE_FILENAME])
	return proof


func _capture_one(capture: Dictionary, main: Node, player: Node2D, camera: Camera2D) -> Dictionary:
	var player_position: Vector2 = capture["player_position"]
	player.global_position = player_position
	if player.has_method("set_review_visual_state"):
		player.call("set_review_visual_state", capture["player_direction"], capture["player_moving"], capture["player_frame"])
	if player.has_method("set_prompt_suppressed"):
		player.call("set_prompt_suppressed", true)
	_hide_dialogue(main)
	var focus_id := String(capture.get("focus_npc_id", ""))
	if focus_id.is_empty():
		if main.has_method("set_opening_island_ambient_barks_enabled"):
			main.call("set_opening_island_ambient_barks_enabled", false)
	else:
		if main.has_method("debug_apply_opening_island_ambient_tick"):
			main.call("debug_apply_opening_island_ambient_tick", float(capture.get("proof_time", 0.0)), true, focus_id)
	camera.zoom = capture["camera_zoom"]
	camera.offset = capture["camera_offset"]
	camera.reset_smoothing()
	await _wait_for_render(CAPTURE_WAIT_FRAMES)

	var image: Image = root.get_texture().get_image()
	var output_path: String = "%s/%s" % [OUT_DIR, capture["filename"]]
	var result := {
		"filename": capture["filename"],
		"label": capture["label"],
		"target": capture["target"],
		"path": output_path,
		"absolute_path": ProjectSettings.globalize_path(output_path),
		"player_position": _vector2_to_dict(player_position),
		"camera_zoom": _vector2_to_dict(capture["camera_zoom"]),
		"camera_offset": _vector2_to_dict(capture["camera_offset"]),
		"focus_npc_id": focus_id,
		"dimensions": {"w": image.get_width(), "h": image.get_height()},
		"png_verification": {},
		"status": "PENDING",
	}
	if image.get_width() < 640 or image.get_height() < 360:
		result["status"] = "FAIL"
		result["failure"] = "Viewport image dimensions were not sensible."
		return result
	var save_error: Error = image.save_png(output_path)
	if save_error != OK:
		result["status"] = "FAIL"
		result["failure"] = "Could not save %s error=%s" % [output_path, save_error]
		return result
	var png_verification: Dictionary = _verify_png_pixels(image)
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
		"schema_id": "wayfarer.g17.runtime_screenshot_manifest.v1",
		"phase": "G-17",
		"out_dir": OUT_DIR,
		"motion_out_dir": MOTION_OUT_DIR,
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
	_write_json(manifest, "%s/%s" % [OUT_DIR, MANIFEST_FILENAME])


func _write_json(data: Dictionary, path: String) -> void:
	var file := FileAccess.open(path, FileAccess.WRITE)
	if file == null:
		push_error("Could not open JSON for writing: " + path)
		return
	file.store_string(JSON.stringify(_jsonify(data), "\t"))
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
