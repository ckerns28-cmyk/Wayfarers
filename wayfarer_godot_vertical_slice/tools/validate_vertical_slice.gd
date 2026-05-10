extends SceneTree

const MAIN_SCENE := preload("res://scenes/Main.tscn")
const EXPECTED_BUILDINGS := [
	"inn_tavern",
	"dock_storehouse",
	"custom_house",
	"merchant_shop_house",
	"large_residence"
]
const VIEWPORT_SIZE := Vector2(1280, 720)
const WORLD_SIZE := Vector2(1600, 1024)

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

	if map:
		for layer_name in ["GroundGrassLayer", "WharfWaterLayer", "RoadsPlazaLayer", "DecorativePropsLayer", "CollisionNavigationLayer"]:
			_expect(map.get_node_or_null(layer_name) != null, "map_layer_" + layer_name)
		var collision_layer := map.get_node_or_null("CollisionNavigationLayer")
		_expect(collision_layer != null and collision_layer.get_child_count() >= 6, "collision_navigation_bodies")

	var buildings := get_nodes_in_group("buildings")
	_expect(buildings.size() == EXPECTED_BUILDINGS.size(), "five_buildings_only")
	var seen: Array[String] = []
	var camera_rect := _camera_world_rect(player)
	for raw_building in buildings:
		var building := raw_building as Node2D
		if building == null:
			failures.append("building_is_not_node2d")
			continue
		seen.append(building.name)
		_validate_building(building, camera_rect)

	for expected_id in EXPECTED_BUILDINGS:
		_expect(seen.has(expected_id), "building_present_" + expected_id)

	var interactables := get_nodes_in_group("interactable")
	_expect(interactables.size() == 1, "one_interactable")
	if player and interactables.size() == 1 and interactables[0] is Node2D:
		var distance := player.global_position.distance_to(interactables[0].global_position)
		var prompt_label := player.get_node_or_null("PromptLabel") as Label
		_expect(distance <= player.interaction_radius, "objective_npc_in_prompt_range")
		_expect(prompt_label != null and prompt_label.visible, "interaction_prompt_visible")

func _validate_building(building: Node2D, camera_rect: Rect2) -> void:
	var sprite := building.get_node_or_null("Sprite2D") as Sprite2D
	var body_shape := building.get_node_or_null("Body/CollisionShape2D") as CollisionShape2D
	var interaction_shape := building.get_node_or_null("InteractionArea/CollisionShape2D") as CollisionShape2D
	var door_marker := building.get_node_or_null("DoorMarker") as Marker2D
	var foot_anchor := building.get_node_or_null("FootAnchor") as Marker2D

	_expect(sprite != null and sprite.texture != null, building.name + "_sprite_texture")
	_expect(body_shape != null and body_shape.shape is RectangleShape2D, building.name + "_body_collision")
	_expect(interaction_shape != null and interaction_shape.shape is RectangleShape2D, building.name + "_interaction_area")
	_expect(door_marker != null, building.name + "_door_marker")
	_expect(foot_anchor != null and foot_anchor.position == Vector2.ZERO, building.name + "_foot_anchor")

	if body_shape and body_shape.shape is RectangleShape2D:
		var body_size := (body_shape.shape as RectangleShape2D).size
		_expect(body_size.x >= 120.0 and body_size.y >= 40.0, building.name + "_nontrivial_footprint")
	if interaction_shape and interaction_shape.shape is RectangleShape2D:
		_expect(interaction_shape.position.y >= 14.0, building.name + "_frontage_interaction_south_of_base")
	if sprite and sprite.texture:
		_expect(camera_rect.encloses(_sprite_world_rect(building, sprite)), building.name + "_fully_visible_in_initial_camera")

func _camera_world_rect(player: Node2D) -> Rect2:
	if player == null:
		return Rect2(Vector2.ZERO, VIEWPORT_SIZE)
	var left: float = clampf(player.global_position.x - VIEWPORT_SIZE.x * 0.5, 0.0, WORLD_SIZE.x - VIEWPORT_SIZE.x)
	var top: float = clampf(player.global_position.y - VIEWPORT_SIZE.y * 0.5, 0.0, WORLD_SIZE.y - VIEWPORT_SIZE.y)
	return Rect2(Vector2(left, top), VIEWPORT_SIZE)

func _sprite_world_rect(building: Node2D, sprite: Sprite2D) -> Rect2:
	var source_size: Vector2 = sprite.texture.get_size()
	if sprite.texture is AtlasTexture:
		source_size = (sprite.texture as AtlasTexture).region.size
	return Rect2(building.global_position + sprite.position, source_size * sprite.scale)

func _expect(condition: bool, label: String) -> void:
	if not condition:
		failures.append(label)

func _print_report() -> void:
	print("[Wayfarer Godot Vertical Slice QA]")
	print("godotVersion=", Engine.get_version_info()["string"])
	print("buildingCount=", get_nodes_in_group("buildings").size())
	print("expectedBuildings=", EXPECTED_BUILDINGS)
	print("failureCount=", failures.size())
	print("failures=", failures)
	print("status=", "PASS" if failures.is_empty() else "FAIL")
