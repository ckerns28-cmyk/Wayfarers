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
const PLAYER_HALF_WIDTH := 12.0
const VISUAL_BASE_TOLERANCE := 2.5
const COLLISION_BASE_TOLERANCE := 6.0
const FRONT_INTERACTION_TOLERANCE := 8.0

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
	var body_rects: Array[Rect2] = []
	for raw_building in buildings:
		var building := raw_building as Node2D
		if building == null:
			failures.append("building_is_not_node2d")
			continue
		seen.append(building.name)
		body_rects.append(_body_world_rect(building))
		_validate_building(building, camera_rect)

	for expected_id in EXPECTED_BUILDINGS:
		_expect(seen.has(expected_id), "building_present_" + expected_id)

	_validate_player_stand_clearance(player, buildings, body_rects)

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
	var debug_overlay := building.get_node_or_null("DebugOverlay") as Node2D

	_expect(sprite != null and sprite.texture != null, building.name + "_sprite_texture")
	_expect(body_shape != null and body_shape.shape is RectangleShape2D, building.name + "_body_collision")
	_expect(interaction_shape != null and interaction_shape.shape is RectangleShape2D, building.name + "_interaction_area")
	_expect(door_marker != null, building.name + "_door_marker")
	_expect(foot_anchor != null and foot_anchor.position == Vector2.ZERO, building.name + "_foot_anchor")
	_expect(debug_overlay != null, building.name + "_debug_overlay_node")

	if sprite and sprite.texture:
		_validate_atlas_region(building, sprite)
		_validate_foot_anchor_at_visual_base(building, sprite, foot_anchor)
		_expect(camera_rect.encloses(_sprite_world_rect(building, sprite)),
			building.name + "_fully_visible_in_initial_camera")

	if body_shape and body_shape.shape is RectangleShape2D:
		var body_size := (body_shape.shape as RectangleShape2D).size
		_expect(body_size.x >= 120.0 and body_size.y >= 40.0, building.name + "_nontrivial_footprint")
		_validate_collision_on_base(building, body_shape, sprite)

	if interaction_shape and interaction_shape.shape is RectangleShape2D:
		_expect(interaction_shape.position.y >= 14.0, building.name + "_frontage_interaction_south_of_base")
		_validate_interaction_at_door(building, interaction_shape, door_marker)

func _validate_atlas_region(building: Node2D, sprite: Sprite2D) -> void:
	if not (sprite.texture is AtlasTexture):
		failures.append(building.name + "_atlas_texture_missing")
		return
	var atlas_tex := sprite.texture as AtlasTexture
	_expect(atlas_tex.atlas != null, building.name + "_atlas_source_set")
	var region := atlas_tex.region
	_expect(region.size.x > 0 and region.size.y > 0,
		building.name + "_atlas_region_nonzero")
	if atlas_tex.atlas:
		var atlas_size := atlas_tex.atlas.get_size()
		var within := (region.position.x >= 0
			and region.position.y >= 0
			and region.position.x + region.size.x <= atlas_size.x
			and region.position.y + region.size.y <= atlas_size.y)
		_expect(within, building.name + "_atlas_region_within_source")

func _validate_foot_anchor_at_visual_base(building: Node2D, sprite: Sprite2D, foot_anchor: Marker2D) -> void:
	if foot_anchor == null or sprite == null or sprite.texture == null:
		return
	var region_size: Vector2 = _texture_region_size(sprite.texture)
	# Sprite is uncentered: its bottom in node-coord is sprite.position.y +
	# region.h * scale. With anchor at the visual base the sprite bottom sits
	# at FootAnchor (node y == 0).
	var sprite_bottom_y := sprite.position.y + region_size.y * sprite.scale.y
	var delta := absf(sprite_bottom_y - foot_anchor.position.y)
	_expect(delta <= VISUAL_BASE_TOLERANCE,
		building.name + "_foot_anchor_at_visual_base")

func _validate_collision_on_base(building: Node2D, body_shape: CollisionShape2D, sprite: Sprite2D) -> void:
	if sprite == null or sprite.texture == null:
		return
	var rect_shape := body_shape.shape as RectangleShape2D
	var half_h := rect_shape.size.y * 0.5
	var collision_top := body_shape.position.y - half_h
	var collision_bottom := body_shape.position.y + half_h
	var region_size: Vector2 = _texture_region_size(sprite.texture)
	var sprite_bottom_y := sprite.position.y + region_size.y * sprite.scale.y
	# Collision must overlap the lower portion of the visible sprite. The
	# lower 16px-ish slab of the visible building should sit inside the
	# collision rect.
	var visible_base_top := sprite_bottom_y - 16.0
	var overlaps_lower_visible := collision_top <= sprite_bottom_y \
		and collision_bottom >= visible_base_top - COLLISION_BASE_TOLERANCE
	_expect(overlaps_lower_visible, building.name + "_collision_overlaps_lower_visible")
	_expect(collision_bottom <= sprite_bottom_y + COLLISION_BASE_TOLERANCE,
		building.name + "_collision_stays_on_or_above_base")

func _validate_interaction_at_door(building: Node2D, interaction_shape: CollisionShape2D, door_marker: Marker2D) -> void:
	if door_marker == null:
		return
	var rect_shape := interaction_shape.shape as RectangleShape2D
	var rect := Rect2(interaction_shape.position - rect_shape.size * 0.5, rect_shape.size)
	# Door (or its projected ground position) should fall within the
	# interaction rect's X span, with the interaction rect ending south of
	# the door (in the player-facing direction).
	var door_x := door_marker.position.x
	_expect(door_x >= rect.position.x - FRONT_INTERACTION_TOLERANCE
		and door_x <= rect.position.x + rect.size.x + FRONT_INTERACTION_TOLERANCE,
		building.name + "_interaction_x_aligned_with_door")
	_expect(rect.position.y + rect.size.y > door_marker.position.y,
		building.name + "_interaction_south_of_door")

func _validate_player_stand_clearance(player: CharacterBody2D, buildings: Array, body_rects: Array[Rect2]) -> void:
	if player == null or buildings.is_empty():
		return
	var world_bounds := Rect2(Vector2.ZERO, WORLD_SIZE)
	var south_ok := 0
	var north_ok := 0
	for raw in buildings:
		var b := raw as Node2D
		if b == null:
			continue
		var sprite := b.get_node_or_null("Sprite2D") as Sprite2D
		if sprite == null or sprite.texture == null:
			continue
		var region_size: Vector2 = _texture_region_size(sprite.texture)
		var sprite_world_top := b.global_position.y + sprite.position.y
		var south_point := b.global_position + Vector2(0, PLAYER_HALF_WIDTH + 14.0)
		var north_point := Vector2(b.global_position.x, sprite_world_top - PLAYER_HALF_WIDTH - 4.0)
		if _player_can_stand(south_point, body_rects, world_bounds):
			south_ok += 1
		if _player_can_stand(north_point, body_rects, world_bounds):
			north_ok += 1
	_expect(south_ok >= 2, "player_can_stand_south_of_two_buildings")
	_expect(north_ok >= 2, "player_can_stand_north_of_two_buildings")

func _player_can_stand(point: Vector2, body_rects: Array[Rect2], world_bounds: Rect2) -> bool:
	if not world_bounds.has_point(point):
		return false
	for rect in body_rects:
		var grown: Rect2 = rect.grow(PLAYER_HALF_WIDTH)
		if grown.has_point(point):
			return false
	return true

func _body_world_rect(building: Node2D) -> Rect2:
	var body_shape := building.get_node_or_null("Body/CollisionShape2D") as CollisionShape2D
	if body_shape == null or not (body_shape.shape is RectangleShape2D):
		return Rect2()
	var size := (body_shape.shape as RectangleShape2D).size
	var center := building.global_position + body_shape.position
	return Rect2(center - size * 0.5, size)

func _camera_world_rect(player: Node2D) -> Rect2:
	if player == null:
		return Rect2(Vector2.ZERO, VIEWPORT_SIZE)
	var left: float = clampf(player.global_position.x - VIEWPORT_SIZE.x * 0.5, 0.0, WORLD_SIZE.x - VIEWPORT_SIZE.x)
	var top: float = clampf(player.global_position.y - VIEWPORT_SIZE.y * 0.5, 0.0, WORLD_SIZE.y - VIEWPORT_SIZE.y)
	return Rect2(Vector2(left, top), VIEWPORT_SIZE)

func _sprite_world_rect(building: Node2D, sprite: Sprite2D) -> Rect2:
	var region_size: Vector2 = _texture_region_size(sprite.texture)
	return Rect2(building.global_position + sprite.position, region_size * sprite.scale)

func _texture_region_size(texture: Texture2D) -> Vector2:
	if texture is AtlasTexture:
		return (texture as AtlasTexture).region.size
	return texture.get_size()

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
