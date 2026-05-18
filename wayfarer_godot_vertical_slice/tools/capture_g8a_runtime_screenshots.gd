extends SceneTree

const BUILD_INFO := preload("res://scripts/BuildInfo.gd")
const MAIN_SCENE := preload("res://scenes/Main.tscn")

const OUT_DIR := "res://artifacts/review/g8a_runtime_screenshots"
const MANIFEST_FILENAME := "g8a_runtime_screenshot_manifest.json"
const VIEWPORT_SIZE := Vector2i(1600, 1000)
const INITIAL_WAIT_FRAMES := 36
const CAPTURE_WAIT_FRAMES := 12

const CAPTURES := [
	{"filename": "g8a_01_wide_newport_normal_gameplay_view.png", "label": "wide Newport normal gameplay view / living NPC stations across harbor, tavern, market, civic, and service districts", "target": "wide_newport_normal_gameplay_view", "player_position": Vector2(800.0, 512.0), "camera_zoom": Vector2(1.0, 1.0), "camera_offset": Vector2(0.0, 0.0), "player_direction": "down", "player_moving": false, "player_frame": 0, "npc_states": []},
	{"filename": "g8a_02_player_arrival_at_harbor.png", "label": "player arrival at harbor / dockworkers establish work life immediately at landfall", "target": "player_arrival_at_harbor", "player_position": Vector2(805.0, 710.0), "camera_zoom": Vector2(1.32, 1.32), "camera_offset": Vector2(12.0, 10.0), "player_direction": "up", "player_moving": false, "player_frame": 0, "npc_states": [{"id": "mara_pike_dockworker", "direction": "down", "moving": false, "frame": 0}, {"id": "jonah_reed_dock_courier", "direction": "left", "moving": false, "frame": 0}]},
	{"filename": "g8a_03_player_route_to_counting_house.png", "label": "route to counting house / Edrin Vale anchors the records path without drifting", "target": "route_to_counting_house", "player_position": Vector2(704.0, 520.0), "camera_zoom": Vector2(1.36, 1.36), "camera_offset": Vector2(38.0, -66.0), "player_direction": "up", "player_moving": true, "player_frame": 1, "npc_states": [{"id": "edrin_vale_counting_house_clerk", "direction": "down", "moving": false, "frame": 0}]},
	{"filename": "g8a_04_player_near_tavern_inn.png", "label": "player near Tavern/Inn / Bess and Silas make the inn read as a rumor hub", "target": "player_near_tavern_inn", "player_position": Vector2(342.0, 606.0), "camera_zoom": Vector2(1.50, 1.50), "camera_offset": Vector2(42.0, -62.0), "player_direction": "down", "player_moving": false, "player_frame": 0, "npc_states": [{"id": "bess_armitage_tavern_keeper", "direction": "down", "moving": false, "frame": 0}, {"id": "silas_crowe_suspicious_patron", "direction": "right", "moving": false, "frame": 0}]},
	{"filename": "g8a_05_player_on_commercial_avenue.png", "label": "commercial avenue / Honor Finch gives the shop row a merchant station and quest-relevant motive", "target": "commercial_avenue", "player_position": Vector2(1010.0, 608.0), "camera_zoom": Vector2(1.30, 1.30), "camera_offset": Vector2(20.0, -38.0), "player_direction": "left", "player_moving": true, "player_frame": 1, "npc_states": [{"id": "honor_finch_merchant_shopkeeper", "direction": "left", "moving": false, "frame": 0}]},
	{"filename": "g8a_06_player_at_dock_wharf_work_area.png", "label": "dock and wharf work area / dock labor NPCs reinforce harbor function without blocking route flow", "target": "dock_wharf_work_area", "player_position": Vector2(1030.0, 704.0), "camera_zoom": Vector2(1.34, 1.34), "camera_offset": Vector2(20.0, -6.0), "player_direction": "right", "player_moving": true, "player_frame": 3, "npc_states": [{"id": "mara_pike_dockworker", "direction": "right", "moving": false, "frame": 0}, {"id": "jonah_reed_dock_courier", "direction": "left", "moving": false, "frame": 0}]},
	{"filename": "g8a_07_player_near_npc_route_intent.png", "label": "player near NPC route intent / stations point toward future harbor, tavern, and counting-house loops", "target": "npc_route_intent", "player_position": Vector2(748.0, 394.0), "camera_zoom": Vector2(1.42, 1.42), "camera_offset": Vector2(0.0, -38.0), "player_direction": "right", "player_moving": false, "player_frame": 0, "npc_states": [{"id": "nora_vale_rumor_carrier", "direction": "down", "moving": false, "frame": 0}, {"id": "edrin_vale_counting_house_clerk", "direction": "left", "moving": false, "frame": 0}]},
	{"filename": "g8a_08_npc_idle_and_walking_proof.png", "label": "NPC idle and walking proof / a walk request resolves to grounded idle because no dedicated walk sheet exists yet", "target": "npc_idle_and_walking_proof", "player_position": Vector2(302.0, 604.0), "camera_zoom": Vector2(1.52, 1.52), "camera_offset": Vector2(40.0, -60.0), "player_direction": "up", "player_moving": false, "player_frame": 0, "npc_states": [{"id": "bess_armitage_tavern_keeper", "direction": "down", "moving": true, "frame": 0}, {"id": "silas_crowe_suspicious_patron", "direction": "right", "moving": true, "frame": 0}]},
	{"filename": "g8a_09_player_interacting_with_counting_house_clerk.png", "label": "counting house interaction / clerk role and missing-ledger dialogue seed are present", "target": "counting_house_interaction", "player_position": Vector2(704.0, 392.0), "camera_zoom": Vector2(1.42, 1.42), "camera_offset": Vector2(24.0, -34.0), "player_direction": "up", "player_moving": false, "player_frame": 0, "npc_states": [{"id": "edrin_vale_counting_house_clerk", "direction": "down", "moving": false, "frame": 0}]},
	{"filename": "g8a_10_player_interacting_at_tavern_rumor_location.png", "label": "tavern rumor interaction / tavern keeper and suspicious patron make whispers player-facing", "target": "tavern_rumor_interaction", "player_position": Vector2(342.0, 606.0), "camera_zoom": Vector2(1.50, 1.50), "camera_offset": Vector2(42.0, -62.0), "player_direction": "down", "player_moving": false, "player_frame": 0, "npc_states": [{"id": "bess_armitage_tavern_keeper", "direction": "down", "moving": false, "frame": 0}, {"id": "silas_crowe_suspicious_patron", "direction": "right", "moving": false, "frame": 0}]},
	{"filename": "g8a_11_quest_prompt_journal_objective_proof.png", "label": "quest prompt and objective proof / NPC dialogue seeds connect First Light, tavern whisper, and optional clue paths", "target": "quest_prompt_journal_objective_proof", "player_position": Vector2(675.0, 600.0), "camera_zoom": Vector2(1.44, 1.44), "camera_offset": Vector2(42.0, -54.0), "player_direction": "up", "player_moving": true, "player_frame": 2, "npc_states": [{"id": "edrin_vale_counting_house_clerk", "direction": "down", "moving": false, "frame": 0}, {"id": "nora_vale_rumor_carrier", "direction": "down", "moving": false, "frame": 0}]},
	{"filename": "g8a_12_signs_markers_interaction_ux_proof.png", "label": "signs and interaction UX proof / living NPC stations add guidance without crude debug markers", "target": "signs_markers_interaction_ux_proof", "player_position": Vector2(800.0, 392.0), "camera_zoom": Vector2(1.46, 1.46), "camera_offset": Vector2(-8.0, -44.0), "player_direction": "left", "player_moving": false, "player_frame": 0, "npc_states": [{"id": "nora_vale_rumor_carrier", "direction": "down", "moving": false, "frame": 0}]},
	{"filename": "g8a_13_y_sort_layering_near_buildings_props.png", "label": "y-sort and layering proof / NPC feet and shadows sit with buildings and props", "target": "y_sort_layering_near_buildings_props", "player_position": Vector2(1018.0, 596.0), "camera_zoom": Vector2(1.46, 1.46), "camera_offset": Vector2(0.0, -54.0), "player_direction": "down", "player_moving": false, "player_frame": 0, "npc_states": [{"id": "honor_finch_merchant_shopkeeper", "direction": "left", "moving": false, "frame": 0}]},
	{"filename": "g8a_14_debug_overlays_disabled.png", "label": "debug overlays disabled / no primitive route boxes, debug signs, or placeholder NPC markers in normal play", "target": "debug_overlays_disabled", "player_position": Vector2(800.0, 512.0), "camera_zoom": Vector2(1.18, 1.18), "camera_offset": Vector2(0.0, -8.0), "player_direction": "down", "player_moving": false, "player_frame": 0, "npc_states": []},
	{"filename": "g8a_15_contact_sheet_provenance_proof.png", "label": "contact sheet and provenance proof / all visible NPCs use the accepted G-4.22R atelier NPC atlas and population contracts", "target": "contact_sheet_provenance_proof", "player_position": Vector2(704.0, 654.0), "camera_zoom": Vector2(1.20, 1.20), "camera_offset": Vector2(0.0, -8.0), "player_direction": "right", "player_moving": true, "player_frame": 1, "npc_states": [{"id": "mara_pike_dockworker", "direction": "right", "moving": false, "frame": 0}, {"id": "bess_armitage_tavern_keeper", "direction": "down", "moving": false, "frame": 0}, {"id": "edrin_vale_counting_house_clerk", "direction": "down", "moving": false, "frame": 0}]},
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
	player.set_process(false)
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

	var npc_nodes := _starter_village_npc_nodes(main)
	for npc in npc_nodes.values():
		var npc_node := npc as Node
		npc_node.set_process(false)
		npc_node.set_physics_process(false)
	manifest["player_motion_contract"] = _jsonify(player.call("character_motion_contract") if player.has_method("character_motion_contract") else {})
	manifest["npc_population_contracts"] = _jsonify(_npc_contracts(npc_nodes))
	manifest["npc_population_count"] = npc_nodes.size()
	manifest["npc_role_count"] = _npc_roles(npc_nodes).size()
	manifest["npc_roles"] = _npc_roles(npc_nodes)
	manifest["movement_policy"] = "stationary_work_pose_until_dedicated_walk_sheets"

	if npc_nodes.size() < 6:
		return _fail(manifest, "Expected at least six starter_village_npc nodes; found %s" % npc_nodes.size())

	for capture in CAPTURES:
		var file_result := await _capture_one(capture, player, npc_nodes, camera)
		if file_result.get("status", "") != "PASS":
			manifest["screenshots"].append(file_result)
			return _fail(manifest, String(file_result.get("failure", "Screenshot capture failed.")))
		manifest["screenshots"].append(file_result)

	manifest["status"] = "PASS"
	_write_manifest(manifest)
	print("PASS: G-8A runtime screenshots -> ", ProjectSettings.globalize_path(OUT_DIR))
	return 0


func _capture_one(capture: Dictionary, player: Node2D, npc_nodes: Dictionary, camera: Camera2D) -> Dictionary:
	player.global_position = capture["player_position"]
	if player.has_method("set_review_visual_state"):
		player.call("set_review_visual_state", capture["player_direction"], capture["player_moving"], capture["player_frame"])
	_reset_npc_review_states(npc_nodes)
	for raw_state in capture.get("npc_states", []):
		var state := raw_state as Dictionary
		var npc_id := String(state.get("id", ""))
		var npc := _npc_by_id(npc_nodes, npc_id)
		if npc != null and npc.has_method("set_review_motion_state"):
			npc.call("set_review_motion_state", String(state.get("direction", "down")), bool(state.get("moving", false)), int(state.get("frame", 0)))
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
		"player_motion_state": _motion_state(capture["player_direction"], capture["player_moving"], capture["player_frame"]),
		"npc_states": _jsonify(capture.get("npc_states", [])),
		"npc_route_walking_expected": false,
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


func _starter_village_npc_nodes(main: Node) -> Dictionary:
	var npc_nodes := {}
	for raw_npc in main.get_tree().get_nodes_in_group("starter_village_npc"):
		var npc := raw_npc as Node2D
		if npc == null:
			continue
		var contract: Dictionary = {}
		if npc.has_method("npc_population_contract"):
			contract = npc.call("npc_population_contract")
		var contract_id := String(contract.get("id", npc.name))
		npc_nodes[contract_id] = npc
	return npc_nodes


func _npc_by_id(npc_nodes: Dictionary, npc_id: String) -> Node2D:
	if npc_nodes.has(npc_id):
		return npc_nodes[npc_id] as Node2D
	if npc_id == "edrin_vale_counting_house_clerk" and npc_nodes.has("EdrinVale"):
		return npc_nodes["EdrinVale"] as Node2D
	return null


func _reset_npc_review_states(npc_nodes: Dictionary) -> void:
	for npc in npc_nodes.values():
		var npc_node := npc as Node
		if npc_node != null and npc_node.has_method("set_review_motion_state"):
			npc_node.call("set_review_motion_state", "down", false, 0)


func _npc_contracts(npc_nodes: Dictionary) -> Array:
	var contracts := []
	for npc in npc_nodes.values():
		var npc_node := npc as Node
		if npc_node != null and npc_node.has_method("npc_population_contract"):
			contracts.append(npc_node.call("npc_population_contract"))
	return contracts


func _npc_roles(npc_nodes: Dictionary) -> Array:
	var roles := []
	for contract in _npc_contracts(npc_nodes):
		if contract is Dictionary:
			var role := String(contract.get("role", ""))
			if not role.is_empty() and not roles.has(role):
				roles.append(role)
	return roles


func _wait_for_render(frame_count: int) -> void:
	for _i in range(frame_count):
		await process_frame
	await RenderingServer.frame_post_draw


func _base_manifest() -> Dictionary:
	return {
		"schema_id": "wayfarer.g8a.runtime_screenshot_manifest.v1",
		"phase": "G-8A",
		"status": "PENDING",
		"created_at": Time.get_datetime_string_from_system(true),
		"command": OS.get_environment("G8A_CAPTURE_COMMAND"),
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
		"required_recurring_screenshot_set_count": CAPTURES.size(),
		"movement_proof": "Named NPCs are grounded with route-walking disabled; station, role, dialogue, and quest relevance contracts prove living-town placement without static glide.",
		"warnings": [],
		"screenshots": [],
	}


func _project_setting(setting_name: String) -> String:
	if ProjectSettings.has_setting(setting_name):
		return str(ProjectSettings.get_setting(setting_name))
	return ""


func _motion_state(direction: String, moving: bool, frame_index: int) -> Dictionary:
	return {
		"direction": direction,
		"moving_requested": moving,
		"animation": ("walk_" if moving else "idle_") + direction,
		"frame_index": frame_index,
	}


func _vector2_to_dict(value: Vector2) -> Dictionary:
	return {"x": snappedf(value.x, 0.001), "y": snappedf(value.y, 0.001)}


func _jsonify(value: Variant) -> Variant:
	if value is Vector2:
		return _vector2_to_dict(value)
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
		push_error("Could not open manifest for writing: " + manifest_path)
		return
	file.store_string(JSON.stringify(manifest, "\t"))
	file.store_line("")
