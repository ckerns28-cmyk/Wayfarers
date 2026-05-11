extends SceneTree

const MAIN_SCENE := preload("res://scenes/Main.tscn")
const NEWPORT_TOWN := preload("res://scripts/NewportTownBlueprint.gd")

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

	_expect(world != null and world.y_sort_enabled, "world_y_sort_enabled")
	_expect(player != null, "player_exists")
	_expect(hud != null, "hud_exists")
	_expect(map != null, "map_exists")

	if player:
		_expect(player.get_node_or_null("Camera2D") != null, "player_camera_exists")
		_expect(root.get_camera_2d() == player.get_node("Camera2D"), "player_camera_is_current")
		_expect(player.get_node_or_null("CollisionShape2D") != null, "player_collision_exists")
		_expect(player.global_position.distance_to(NEWPORT_TOWN.PLAYER_SPAWN) < 1.0, "player_spawn_matches_blueprint")

	if map:
		for layer_name in ["GroundGrassLayer", "WharfWaterLayer", "RoadsPlazaLayer", "DecorativePropsLayer", "CollisionNavigationLayer"]:
			_expect(map.get_node_or_null(layer_name) != null, "map_layer_" + layer_name)
		var collision_layer := map.get_node_or_null("CollisionNavigationLayer")
		_expect(collision_layer != null and collision_layer.get_child_count() > 40, "collision_navigation_bodies")

	_validate_buildings()
	_validate_reachability()

func _validate_buildings() -> void:
	var buildings := get_nodes_in_group("buildings")
	var expected_ids: Array = NEWPORT_TOWN.BUILDING_IDS
	_expect(buildings.size() == expected_ids.size(), "newport_building_count_19")

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

	for district_id in ["harbor_wharf", "waterfront_commercial", "civic_district", "upper_residential_terrace", "service_outfitter_lane"]:
		_expect(district_counts.get(district_id, 0) > 0, "district_has_building_" + district_id)

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
		_expect(absf(sprite_bottom_y) <= 2.5, building.name + "_foot_anchor_at_visual_base")

	if body_shape and body_shape.shape is RectangleShape2D:
		var body_size := (body_shape.shape as RectangleShape2D).size
		_expect(body_size.x >= 60.0 and body_size.y >= 28.0, building.name + "_playable_collision_footprint")

	if interaction_shape and interaction_shape.shape is RectangleShape2D:
		_expect(interaction_shape.position.y > 0.0, building.name + "_frontage_interaction_south")

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
	print("reachabilityTargets=", NEWPORT_TOWN.reachability_targets())
	print("failureCount=", failures.size())
	print("failures=", failures)
	print("status=", "PASS" if failures.is_empty() else "FAIL")
