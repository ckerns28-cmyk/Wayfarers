extends SceneTree

const MAIN_SCENE := preload("res://scenes/Main.tscn")
const NEWPORT_TOWN := preload("res://scripts/NewportTownBlueprint.gd")
const BUILDING_CATALOG := preload("res://scripts/BuildingCatalog.gd")
const BUILD_INFO := preload("res://scripts/BuildInfo.gd")

var failures: Array[String] = []

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	var main := MAIN_SCENE.instantiate()
	root.add_child(main)
	await process_frame
	await physics_frame
	await process_frame

	_validate_scene(main)
	_print_report()
	quit(0 if failures.is_empty() else 1)

func _validate_scene(main: Node) -> void:
	var world := main.get_node_or_null("World") as Node2D
	var player := main.get_node_or_null("World/Player") as CharacterBody2D
	var hud := main.get_node_or_null("HUD") as CanvasLayer
	var map := main.get_node_or_null("World/TownMap") as Node2D

	_expect(BUILD_INFO.BUILD_PHASE == "G-4.13B", "build_phase_g_4_13b")
	_expect(BUILD_INFO.BUILD_LABEL == "Godot G-4.13B Rowhouse Infill Density", "build_label_g_4_13b")
	_expect(BUILD_INFO.DEBUG_OVERLAYS_DEFAULT == false, "debug_overlays_default_off")
	_expect(BUILD_INFO.DEBUG_OVERLAY_TOGGLE_ENABLED == true, "debug_overlay_toggle_available")
	_expect(world != null and world.y_sort_enabled, "world_y_sort_enabled")
	_expect(player != null, "player_exists")
	_expect(hud != null, "hud_exists")
	_expect(map != null, "map_exists")
	if not NEWPORT_TOWN.NPCS_ENABLED:
		_expect(main.get_node_or_null("World/EdrinVale") == null, "npcs_disabled_for_g_4_11")

	if player:
		_expect(player.get_node_or_null("Camera2D") != null, "player_camera_exists")
		_expect(root.get_camera_2d() == player.get_node("Camera2D"), "player_camera_is_current")
		_expect(player.get_node_or_null("CollisionShape2D") != null, "player_collision_exists")
		_expect(player.global_position.distance_to(NEWPORT_TOWN.PLAYER_SPAWN) < 1.0, "player_spawn_matches_blueprint")
		var camera := player.get_node_or_null("Camera2D") as Camera2D
		if camera:
			if NEWPORT_TOWN.G47_CALIBRATION_MODE:
				_expect(camera.zoom.x <= 1.0 and camera.zoom.y <= 1.0, "calibration_camera_shows_variants")
			else:
				_expect(camera.zoom.x >= 1.1 and camera.zoom.y >= 1.1, "spawn_camera_not_overview_zoom")
				_expect(camera.offset.length() > 20.0, "spawn_camera_intentional_offset")

	if map:
		for layer_name in ["GroundGrassLayer", "WharfWaterLayer", "RoadsPlazaLayer", "DecorativePropsLayer", "CollisionNavigationLayer"]:
			_expect(map.get_node_or_null(layer_name) != null, "map_layer_" + layer_name)
		var collision_layer := map.get_node_or_null("CollisionNavigationLayer")
		var minimum_collision_bodies := 3 if NEWPORT_TOWN.G47_CALIBRATION_MODE else (20 if (NEWPORT_TOWN.G46_PROOF_FRAME or NEWPORT_TOWN.G48_PROOF_STREET or NEWPORT_TOWN.G49_STREET_VIGNETTE) else 40)
		_expect(collision_layer != null and collision_layer.get_child_count() > minimum_collision_bodies, "collision_navigation_bodies")
		if collision_layer:
			_validate_detail_blockers(collision_layer)

	_validate_buildings()
	_validate_starter_harbor_plan()
	_validate_proof_street(main)
	_validate_lived_in_details()
	_validate_reachability()
	_validate_building_walkability_gate()
	_validate_route_debug_probes()

func _validate_detail_blockers(collision_layer: Node) -> void:
	var detail_count := 0
	for child in collision_layer.get_children():
		if child.name.begins_with("DetailBlocker_"):
			detail_count += 1
	_expect(detail_count == NEWPORT_TOWN.detail_blockers().size(), "detail_blocker_count")
	for blocker in NEWPORT_TOWN.detail_blockers():
		var id := String(blocker.get("id", ""))
		var rect: Rect2 = blocker.get("rect", Rect2())
		if id == "mercantile_front_crates":
			_expect(rect.position.y >= 570.0, "mercantile_front_crates_clear_rear_lane_throat")
		elif id == "west_alley_rope":
			_expect(rect.position.x >= 560.0 and rect.position.y >= 570.0, "west_alley_rope_clear_rear_lane_throat")
		elif id == "support_lane_woodpile":
			_expect(rect.position.y >= 460.0, "support_lane_woodpile_clear_rear_lane_road")

func _validate_lived_in_details() -> void:
	var minimum_detail_count := 118 if NEWPORT_TOWN.G410_STARTER_HARBOR_TOWN else (20 if NEWPORT_TOWN.G47_CALIBRATION_MODE else (24 if NEWPORT_TOWN.G49_STREET_VIGNETTE else (20 if NEWPORT_TOWN.G48_PROOF_STREET else (8 if NEWPORT_TOWN.G46_PROOF_FRAME else 40))))
	_expect(NEWPORT_TOWN.lived_in_detail_count() >= minimum_detail_count, "lived_in_detail_density")

func _validate_buildings() -> void:
	var buildings := get_nodes_in_group("buildings")
	var expected_ids: Array = NEWPORT_TOWN.BUILDING_IDS
	_expect(buildings.size() == expected_ids.size(), "newport_building_count")

	var seen := {}
	var district_counts := {}
	for raw_building in buildings:
		var building := raw_building as Node2D
		if building == null:
			failures.append("building_is_not_node2d")
			continue
		_expect(not seen.has(building.name), "unique_building_id_" + building.name)
		seen[building.name] = true
		_validate_building_node(building)

	for config in NEWPORT_TOWN.building_specs():
		var id: String = config["id"]
		var district: String = config["district"]
		district_counts[district] = district_counts.get(district, 0) + 1
		_expect(seen.has(id), "building_present_" + id)

	var expected_districts := ["harborfront_commercial", "working_wharf", "inland_residential_civic", "support_lane"] if NEWPORT_TOWN.G410_STARTER_HARBOR_TOWN else (["visual_calibration"] if NEWPORT_TOWN.G47_CALIBRATION_MODE else (["waterfront_commercial"] if (NEWPORT_TOWN.G46_PROOF_FRAME or NEWPORT_TOWN.G48_PROOF_STREET or NEWPORT_TOWN.G49_STREET_VIGNETTE) else ["harbor_wharf", "waterfront_commercial", "civic_district", "upper_residential_terrace", "service_outfitter_lane"]))
	for district_id in expected_districts:
		_expect(district_counts.get(district_id, 0) > 0, "district_has_building_" + district_id)

func _validate_starter_harbor_plan() -> void:
	if not NEWPORT_TOWN.G410_STARTER_HARBOR_TOWN:
		return

	var lots: Array = NEWPORT_TOWN.starter_lot_specs()
	var planned_lots: Array = NEWPORT_TOWN.planned_lot_specs()
	var total_lots := lots.size()
	_expect(total_lots >= 14 and total_lots <= 20, "starter_lot_count_14_to_20")
	_expect(planned_lots.size() == NEWPORT_TOWN.STARTER_HARBOR_PLANNED_LOT_IDS.size(), "planned_lot_manifest_count")
	_expect(NEWPORT_TOWN.STARTER_HARBOR_BUILDING_IDS.size() == NEWPORT_TOWN.BUILDING_IDS.size(), "starter_building_manifest_matches_active")

	var lot_ids := {}
	var actual_building_lots := {}
	var district_lots := {}
	for raw_lot in lots:
		var lot: Dictionary = raw_lot
		var id: String = lot["id"]
		_expect(not lot_ids.has(id), "unique_lot_id_" + id)
		lot_ids[id] = true
		var district: String = lot["district"]
		district_lots[district] = district_lots.get(district, 0) + 1
		var rect: Rect2i = lot["rect"]
		_expect(rect.size.x > 0 and rect.size.y > 0, "lot_has_area_" + id)
		if lot.get("status", "") == "actual":
			actual_building_lots[lot.get("building_id", "")] = true

	for building_id in NEWPORT_TOWN.STARTER_HARBOR_BUILDING_IDS:
		_expect(actual_building_lots.has(building_id), "actual_lot_for_" + building_id)
	_expect(not actual_building_lots.has("b_village_hall"), "chapel_coded_hall_not_active")
	_expect(actual_building_lots.has("b_custom_house"), "custom_house_replaces_civic_hall")
	for planned_id in NEWPORT_TOWN.STARTER_HARBOR_PLANNED_LOT_IDS:
		_expect(lot_ids.has(planned_id), "planned_lot_present_" + planned_id)
	for building_id in NEWPORT_TOWN.G413B_ACTIVE_INFILL_BUILDING_IDS:
		_expect(actual_building_lots.has(building_id), "g413b_active_infill_lot_for_" + building_id)
	for district_id in ["harborfront_commercial", "working_wharf", "inland_residential_civic", "support_lane"]:
		_expect(district_lots.get(district_id, 0) > 0, "starter_lots_cover_" + district_id)

	for building_id in ["b_dock_storehouse", "b_wharf_boathouse", "b_dock_warehouse"]:
		_expect(actual_building_lots.has(building_id), "harbor_water_asset_placed_" + building_id)
		for config in NEWPORT_TOWN.building_specs():
			if String(config.get("id", "")) == building_id:
				var water_position: Vector2 = config.get("position", Vector2.ZERO)
				var water_foot_tile_y := water_position.y / float(NEWPORT_TOWN.TILE)
				_expect(water_foot_tile_y >= 27.25 and water_foot_tile_y <= 28.25, "harbor_water_asset_in_wharf_edge_water_pocket_" + building_id)
				var water_foot_tile_x := water_position.x / float(NEWPORT_TOWN.TILE)
				if building_id == "b_dock_warehouse":
					_expect(water_foot_tile_x >= 14.5 and water_foot_tile_x <= 16.5, "harbor_water_asset_beside_west_pier_" + building_id)
				elif building_id == "b_wharf_boathouse":
					_expect(water_foot_tile_x >= 27.0 and water_foot_tile_x <= 29.5, "harbor_water_asset_beside_center_pier_" + building_id)
				else:
					_expect(water_foot_tile_x >= 40.0 and water_foot_tile_x <= 42.5, "harbor_water_asset_beside_east_pier_" + building_id)

	for config in NEWPORT_TOWN.building_specs():
		_expect(config.has("definition_id"), String(config["id"]) + "_has_reusable_definition_id")
		if config.has("definition_id"):
			var definition := BUILDING_CATALOG.building_definition(String(config["definition_id"]))
			for key in ["building_id", "display_name", "role", "texture_path", "sprite_region", "sprite_source_size", "visual_scale", "scale", "visual_bounds", "lot_bounds", "collision_footprint", "interaction_zone", "foot_anchor", "visual_base_anchor", "collision_shape", "collision_rect", "interaction_size", "interaction_offset", "interaction_zone_placeholder", "shadow_size", "district_role", "district_placement_tags", "notes"]:
				_expect(definition.has(key), String(config["id"]) + "_definition_has_" + key)
			var texture_path: String = definition.get("texture_path", "")
			_expect(texture_path.begins_with("res://assets/sprites/buildings/isolated/") or texture_path.begins_with("res://assets/buildings/"), String(config["id"]) + "_uses_project_building_sprite")
			var tags: Array = definition.get("district_placement_tags", [])
			_expect(not tags.is_empty(), String(config["id"]) + "_has_district_placement_tags")

	var manifest: Array = NEWPORT_TOWN.missing_asset_manifest()
	for needed in ["fishmonger storefront", "cooperage / barrel shop final art", "blacksmith / smithy", "small home variants", "dock shack", "carts", "dedicated crate/barrel/rope prop sprites", "sign variants", "fencing variants", "lantern variants", "chapel/church decision and final art if needed"]:
		_expect(manifest.has(needed), "missing_asset_manifest_" + needed.replace("/", "_").replace(" ", "_"))

	var plan: Dictionary = NEWPORT_TOWN.starter_district_plan()
	var plan_districts: Array = plan.get("districts", [])
	var plan_loop: Array = plan.get("movement_loop", [])
	_expect(plan.get("target_total_lots", "") == "14-20", "starter_plan_target_lot_range")
	_expect(plan.get("composition_pass", "") == "G-4.12B", "starter_plan_composition_pass_g_4_12b")
	_expect(plan.get("footprint_pass", "") == "G-4.13A", "starter_plan_footprint_pass_g_4_13a")
	_expect(plan.get("density_pass", "") == "G-4.13B", "starter_plan_density_pass_g_4_13b")
	_expect(int(plan.get("active_g413b_infill_count", 0)) >= 3, "starter_plan_active_g413b_infill_count")
	var plan_active_infill: Array = plan.get("active_g413b_infill_buildings", [])
	for building_id in NEWPORT_TOWN.G413B_ACTIVE_INFILL_BUILDING_IDS:
		_expect(plan_active_infill.has(building_id), "starter_plan_active_infill_" + building_id)
	_expect(String(plan.get("collision_model", "")).find("collision_footprint") >= 0, "starter_plan_collision_model_mentions_collision_footprint")
	_expect(plan.get("clean_review_default", false) == true, "starter_plan_clean_review_default")
	_expect(plan_districts.size() >= 4, "starter_plan_district_structure")
	_expect(plan_loop.has("commercial_rear_road"), "starter_plan_includes_commercial_rear_road")
	_expect(plan_loop.has("mercantile_counting_house_rear_road"), "starter_plan_includes_mercantile_counting_rear_road")
	_expect(plan_loop.size() >= 6, "starter_plan_movement_loop")
	_expect(NEWPORT_TOWN.g413b_rowhouse_infill_slots().size() == NEWPORT_TOWN.G413B_ROWHOUSE_INFILL_SLOT_IDS.size(), "g413b_rowhouse_infill_slot_manifest_count")
	var active_slots := 0
	var deferred_slots := 0
	for raw_slot in NEWPORT_TOWN.g413b_rowhouse_infill_slots():
		var slot: Dictionary = raw_slot
		var status := String(slot.get("status", ""))
		if status == "active_g413b":
			active_slots += 1
			_expect(NEWPORT_TOWN.G413B_ACTIVE_INFILL_BUILDING_IDS.has(String(slot.get("building_id", ""))), "g413b_slot_active_building_" + String(slot.get("id", "")))
		elif status == "deferred_g413b":
			deferred_slots += 1
			_expect(NEWPORT_TOWN.G413B_DEFERRED_INFILL_SLOT_IDS.has(String(slot.get("id", ""))), "g413b_slot_deferred_manifest_" + String(slot.get("id", "")))
		_expect(not String(slot.get("guardrail", "")).is_empty(), "g413b_slot_guardrail_" + String(slot.get("id", "")))
		_expect(not String(slot.get("future_hook", "")).is_empty(), "g413b_slot_future_hook_" + String(slot.get("id", "")))
	_expect(active_slots >= 3, "g413b_active_infill_slot_count")
	_expect(deferred_slots >= 2, "g413b_deferred_infill_slot_count")
	_expect(NEWPORT_TOWN.route_debug_probes().size() >= 13, "g413b_route_debug_probe_count")
	_expect(BUILDING_CATALOG.available_building_assets().size() >= 20, "asset_audit_catalog_populated")

func _validate_building_node(building: Node2D) -> void:
	var sprite := building.get_node_or_null("Sprite2D") as Sprite2D
	var body_shape := building.get_node_or_null("Body/CollisionShape2D") as CollisionShape2D
	var interaction_shape := building.get_node_or_null("InteractionArea/CollisionShape2D") as CollisionShape2D
	var door_marker := building.get_node_or_null("DoorMarker") as Marker2D
	var foot_anchor := building.get_node_or_null("FootAnchor") as Marker2D

	_expect(sprite != null and sprite.texture != null, building.name + "_sprite_texture")
	_expect(sprite == null or sprite.texture is AtlasTexture, building.name + "_atlas_texture")
	_expect(body_shape != null and body_shape.shape is RectangleShape2D, building.name + "_body_collision")
	_expect(interaction_shape != null and interaction_shape.shape is RectangleShape2D, building.name + "_interaction_area")
	_expect(door_marker != null, building.name + "_door_marker")
	_expect(foot_anchor != null and foot_anchor.position == Vector2.ZERO, building.name + "_foot_anchor")

	if sprite and sprite.texture:
		var region_size := _texture_region_size(sprite.texture)
		var sprite_bottom_y := sprite.position.y + region_size.y * sprite.scale.y
		var proof_street: bool = building.has_method("is_proof_street_building") and building.is_proof_street_building()
		var harbor_integrated: bool = building.has_method("is_harbor_integrated") and building.is_harbor_integrated()
		if harbor_integrated:
			_expect(sprite_bottom_y > 20.0 and sprite_bottom_y < 78.0, building.name + "_harbor_sprite_extends_into_water")
		elif proof_street:
			_expect(sprite_bottom_y > 3.0 and sprite_bottom_y < 28.0, building.name + "_painterly_base_padding_allowed")
		else:
			_expect(sprite_bottom_y >= -2.5 and sprite_bottom_y <= 22.0, building.name + "_foot_anchor_at_visual_base")

	if NEWPORT_TOWN.G410_STARTER_HARBOR_TOWN:
		_expect(building.has_method("uses_normalized_definition") and building.uses_normalized_definition(), building.name + "_uses_normalized_definition")

	if body_shape and body_shape.shape is RectangleShape2D:
		var body_size := (body_shape.shape as RectangleShape2D).size
		var body_rect := Rect2(body_shape.position - body_size * 0.5, body_size)
		_expect(body_size.x >= 60.0 and body_size.y >= 28.0, building.name + "_playable_collision_footprint")
		_expect(body_size.y <= 64.0, building.name + "_collision_footprint_not_visual_height")
		_expect(body_rect.position.y >= -42.0 and body_rect.end.y <= 18.0, building.name + "_collision_footprint_sits_on_ground_contact")
		var proof_street: bool = building.has_method("is_proof_street_building") and building.is_proof_street_building()
		if proof_street:
			_expect(body_size.y <= 48.0, building.name + "_proof_street_uses_tight_ground_footprint")
		if building.has_method("get_visual_bounds"):
			var visual_bounds: Rect2 = building.get_visual_bounds()
			_expect(visual_bounds.size.y > body_size.y * 2.0, building.name + "_visual_bounds_separate_from_collision_footprint")
		if building.has_method("get_lot_bounds"):
			var lot_bounds: Rect2 = building.get_lot_bounds()
			_expect(lot_bounds.size.y > body_size.y, building.name + "_lot_bounds_separate_from_collision_footprint")

	if interaction_shape and interaction_shape.shape is RectangleShape2D:
		_expect(interaction_shape.position.y > 0.0, building.name + "_frontage_interaction_south")
		if body_shape and body_shape.shape is RectangleShape2D:
			var interaction_size := (interaction_shape.shape as RectangleShape2D).size
			var interaction_rect := Rect2(interaction_shape.position - interaction_size * 0.5, interaction_size)
			var body_size := (body_shape.shape as RectangleShape2D).size
			var body_rect := Rect2(body_shape.position - body_size * 0.5, body_size)
			_expect(interaction_rect.position.y >= body_rect.position.y, building.name + "_interaction_zone_not_rear_blocker")

func _validate_proof_street(main: Node) -> void:
	var proof_ids: Array = NEWPORT_TOWN.proof_street_ids()
	if NEWPORT_TOWN.G47_CALIBRATION_MODE:
		_expect(proof_ids.size() == 8, "calibration_building_count_8")
		_expect(NEWPORT_TOWN.calibration_variants().size() == 4, "calibration_variant_count_4")
	elif NEWPORT_TOWN.G410_STARTER_HARBOR_TOWN:
		_expect(proof_ids.size() == 5, "starter_harborfront_building_count_5")
	elif NEWPORT_TOWN.G46_PROOF_FRAME:
		_expect(proof_ids.size() == 3, "proof_street_building_count_3")
	elif NEWPORT_TOWN.G48_PROOF_STREET or NEWPORT_TOWN.G49_STREET_VIGNETTE:
		_expect(proof_ids.size() >= 3 and proof_ids.size() <= 5, "proof_street_building_count_3_to_5")
	else:
		_expect(proof_ids.size() >= 5 and proof_ids.size() <= 7, "proof_street_building_count_5_to_7")

	var configs_by_id := {}
	for config in NEWPORT_TOWN.building_specs():
		var merged_config: Dictionary = config
		if config.has("definition_id"):
			merged_config = BUILDING_CATALOG.building_definition(String(config["definition_id"]))
			for key in config:
				merged_config[key] = config[key]
		configs_by_id[config["id"]] = merged_config

	for id in proof_ids:
		_expect(configs_by_id.has(id), "proof_street_config_present_" + id)
		if configs_by_id.has(id):
			var config: Dictionary = configs_by_id[id]
			_expect(config.get("proof_street", false), id + "_proof_street_flag")
			for key in ["visual_base_anchor", "frontage_offset", "visual_bounds", "collision_footprint", "collision_rect", "interaction_zone", "lot_bounds", "lot_rect", "building_volume_rect", "y_sort_offset", "shadow_size"]:
				_expect(config.has(key), id + "_seating_metadata_" + key)

	var proof_buildings := get_nodes_in_group("proof_street_buildings")
	_expect(proof_buildings.size() == proof_ids.size(), "proof_street_node_count")
	for raw_building in proof_buildings:
		var building := raw_building as Node2D
		if building == null:
			failures.append("proof_street_node_not_node2d")
			continue
		var overlay := building.get_node_or_null("DebugOverlay") as Node2D
		_expect(overlay != null and not overlay.visible, building.name + "_seating_debug_off_by_default")
		_expect(overlay == null or overlay.visible == false, building.name + "_debug_labels_hidden_in_review_mode")
		_expect(building.has_method("has_seating_metadata") and building.has_seating_metadata(), building.name + "_runtime_seating_metadata")
		_expect(building.get_node_or_null("FrontageMarker") != null, building.name + "_frontage_marker")
		_expect(building.get_node_or_null("YSortAnchor") != null, building.name + "_ysort_marker")

	if main.has_method("set_building_seating_overlay"):
		main.set_building_seating_overlay(true)
		for raw_building in get_nodes_in_group("buildings"):
			var building := raw_building as Node2D
			if building == null:
				continue
			var overlay := building.get_node_or_null("DebugOverlay") as Node2D
			if overlay == null:
				continue
			var is_proof: bool = building.has_method("is_proof_street_building") and building.is_proof_street_building()
			if NEWPORT_TOWN.G410_STARTER_HARBOR_TOWN:
				is_proof = true
			_expect(overlay.visible == is_proof, building.name + "_seating_debug_toggle_scope")
		main.set_building_seating_overlay(false)
	else:
		failures.append("main_set_building_seating_overlay_method")

func _validate_reachability() -> void:
	var route_tiles: Array = NEWPORT_TOWN.route_tiles()
	var route_set := {}
	for tile in route_tiles:
		route_set[_key(tile)] = true

	var start := NEWPORT_TOWN.player_spawn_tile()
	_expect(route_set.has(_key(start)), "spawn_on_route_tile")
	var reached := _flood_route_tiles(start, route_set)

	for target_name in NEWPORT_TOWN.reachability_targets().keys():
		var tile: Vector2i = NEWPORT_TOWN.reachability_targets()[target_name]
		_expect(reached.has(_key(tile)), "route_reachable_" + target_name)

	if not NEWPORT_TOWN.G47_CALIBRATION_MODE:
		for target_name in NEWPORT_TOWN.proof_street_walk_targets().keys():
			var tile: Vector2i = NEWPORT_TOWN.proof_street_walk_targets()[target_name]
			_expect(reached.has(_key(tile)), "proof_street_walk_reachable_" + target_name)

func _validate_building_walkability_gate() -> void:
	if not NEWPORT_TOWN.G410_STARTER_HARBOR_TOWN:
		return

	var walk_samples := {
		"road_behind_b_mercantile": Vector2(492.0, 526.0),
		"road_behind_b_counting_house": Vector2(680.0, 526.0),
		"harborfront_rear_commercial_row": Vector2(892.0, 526.0),
		"west_commercial_cross_lane": Vector2(392.0, 520.0),
		"central_inland_cross_lane": Vector2(672.0, 430.0),
		"central_front_cross_lane": Vector2(668.0, 592.0),
		"east_commercial_cross_lane": Vector2(1100.0, 520.0),
		"dock_layer_walk": Vector2(824.0, 710.0),
		"clerk_rowhouse_front_walk": Vector2(420.0, 604.0),
		"market_east_edge_front_walk": Vector2(1408.0, 604.0),
		"support_boarding_gap_walk": Vector2(1340.0, 462.0),
	}
	for sample_name in walk_samples.keys():
		var point: Vector2 = walk_samples[sample_name]
		_expect(_collision_owner_labels_at(point, 10.0).is_empty(), "walkability_" + sample_name)

	for raw_building in get_nodes_in_group("buildings"):
		var building := raw_building as Node2D
		if building == null:
			continue
		var rect := _building_collision_world_rect(building)
		if rect.size.x <= 0.0 or rect.size.y <= 0.0:
			continue
		_expect(rect.has_point(rect.get_center()), String(building.name) + "_obvious_building_body_blocks_center")

func _validate_route_debug_probes() -> void:
	if not NEWPORT_TOWN.G410_STARTER_HARBOR_TOWN:
		return
	for probe in NEWPORT_TOWN.route_debug_probes():
		var id := String(probe.get("id", ""))
		var position: Vector2 = probe.get("position", Vector2.ZERO)
		var owners := _collision_owner_labels_at(position, 10.0)
		if not owners.is_empty():
			failures.append("route_probe_" + id + "_blocked_by_" + ",".join(owners))

func _point_hits_building_collision(point: Vector2, player_radius: float) -> bool:
	for raw_building in get_nodes_in_group("buildings"):
		var building := raw_building as Node2D
		if building == null:
			continue
		var rect := _building_collision_world_rect(building).grow(player_radius)
		if rect.has_point(point):
			return true
	return false

func _collision_owner_labels_at(point: Vector2, player_radius: float) -> Array[String]:
	var owners: Array[String] = []
	var collision_layer := root.get_node_or_null("Main/World/TownMap/CollisionNavigationLayer")
	if collision_layer:
		for raw_body in collision_layer.get_children():
			var body := raw_body as StaticBody2D
			if body == null:
				continue
			for raw_shape in body.get_children():
				var shape := raw_shape as CollisionShape2D
				if shape == null or not (shape.shape is RectangleShape2D):
					continue
				var size := (shape.shape as RectangleShape2D).size
				var rect := Rect2(shape.global_position - size * 0.5, size).grow(player_radius)
				if rect.has_point(point):
					owners.append(_collision_body_owner_label(String(body.name)))
	for raw_building in get_nodes_in_group("buildings"):
		var building := raw_building as Node2D
		if building == null:
			continue
		var rect := _building_collision_world_rect(building).grow(player_radius)
		if rect.size.x > 0.0 and rect.size.y > 0.0 and rect.has_point(point):
			owners.append("building:" + String(building.name))
	return owners

func _collision_body_owner_label(body_name: String) -> String:
	if body_name.begins_with("DetailBlocker_"):
		return "prop:" + body_name.trim_prefix("DetailBlocker_")
	if body_name.begins_with("HarborWater_"):
		return "map_water:" + body_name.trim_prefix("HarborWater_")
	return "map:" + body_name

func _building_collision_world_rect(building: Node2D) -> Rect2:
	var body_shape := building.get_node_or_null("Body/CollisionShape2D") as CollisionShape2D
	if body_shape == null or not (body_shape.shape is RectangleShape2D):
		return Rect2()
	var body_size := (body_shape.shape as RectangleShape2D).size
	var local_rect := Rect2(body_shape.position - body_size * 0.5, body_size)
	return Rect2(building.global_position + local_rect.position, local_rect.size)

func _flood_route_tiles(start: Vector2i, route_set: Dictionary) -> Dictionary:
	var reached := {}
	var queue: Array[Vector2i] = [start]
	reached[_key(start)] = true
	var directions: Array[Vector2i] = [Vector2i.LEFT, Vector2i.RIGHT, Vector2i.UP, Vector2i.DOWN]
	while not queue.is_empty():
		var current := queue.pop_front() as Vector2i
		for direction: Vector2i in directions:
			var next_tile: Vector2i = current + direction
			var key: String = _key(next_tile)
			if route_set.has(key) and not reached.has(key):
				reached[key] = true
				queue.append(next_tile)
	return reached

func _texture_region_size(texture: Texture2D) -> Vector2:
	if texture is AtlasTexture:
		return (texture as AtlasTexture).region.size
	return texture.get_size()

func _key(tile: Vector2i) -> String:
	return "%d,%d" % [tile.x, tile.y]

func _expect(condition: bool, label: String) -> void:
	if not condition:
		failures.append(label)

func _print_report() -> void:
	var districts := {}
	for config in NEWPORT_TOWN.building_specs():
		var district: String = config["district"]
		districts[district] = districts.get(district, 0) + 1
	print("[Wayfarer Godot Newport Town QA]")
	print("godotVersion=", Engine.get_version_info()["string"])
	print("buildingCount=", get_nodes_in_group("buildings").size())
	print("expectedBuildings=", NEWPORT_TOWN.BUILDING_IDS)
	print("districtCounts=", districts)
	if NEWPORT_TOWN.G410_STARTER_HARBOR_TOWN:
		print("starterLotCount=", NEWPORT_TOWN.starter_lot_specs().size())
		print("plannedLots=", NEWPORT_TOWN.STARTER_HARBOR_PLANNED_LOT_IDS)
		print("missingAssets=", NEWPORT_TOWN.missing_asset_manifest())
		print("routeDebugProbes=", NEWPORT_TOWN.route_debug_probes())
	print("reachabilityTargets=", NEWPORT_TOWN.reachability_targets())
	print("failureCount=", failures.size())
	print("failures=", failures)
	print("status=", "PASS" if failures.is_empty() else "FAIL")
