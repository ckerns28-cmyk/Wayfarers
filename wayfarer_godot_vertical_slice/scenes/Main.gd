extends Node2D

const BUILDING_SCENE := preload("res://scenes/buildings/Building.tscn")

@onready var world: Node2D = $World
@onready var player: CharacterBody2D = $World/Player
@onready var hud: CanvasLayer = $HUD

var _atlas_cache: Dictionary = {}
var _debug_overlay_enabled := false

func _ready() -> void:
	world.y_sort_enabled = true
	_place_buildings()
	player.dialogue_triggered.connect(hud.show_dialogue)

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_F3:
			_set_debug_overlay(not _debug_overlay_enabled)

func set_debug_overlay(enabled: bool) -> void:
	_set_debug_overlay(enabled)

func _set_debug_overlay(enabled: bool) -> void:
	_debug_overlay_enabled = enabled
	for raw_building in get_tree().get_nodes_in_group("buildings"):
		var building := raw_building as Node2D
		if building and building.has_method("set_debug_overlay"):
			building.set_debug_overlay(enabled)

func _atlas(path: String, region: Rect2) -> AtlasTexture:
	var texture := AtlasTexture.new()
	texture.atlas = _atlas_image(path)
	texture.region = region
	return texture

func _atlas_image(path: String) -> Texture2D:
	if _atlas_cache.has(path):
		return _atlas_cache[path]

	var atlas_texture := ResourceLoader.load(path, "Texture2D") as Texture2D
	if atlas_texture == null:
		push_error("Failed to load atlas texture: " + path)
		return null

	_atlas_cache[path] = atlas_texture
	return atlas_texture

func _place_buildings() -> void:
	# Atlas regions below are TIGHT bounding boxes for a single building cell.
	# Each atlas PNG is a 3x3 grid of 418px cells with zero gutter between
	# adjacent sprites, so any rect that crosses a cell boundary will pull in
	# a sliver of a neighbor. See SPRITE_ATLAS_GODOT.md.
	var buildings := [
		{
			"id": "inn_tavern",
			"display_name": "Inn & Tavern",
			"atlas_path": "res://assets/buildings/hearthvale_buildings_atlas_v1.png",
			"region": Rect2(33, 45, 385, 373),
			"source_size": Vector2(385, 373),
			"draw_width": 240.0,
			"anchor": Vector2(192.5, 373),
			"position": Vector2(417, 676),
			"collision_size": Vector2(216, 46),
			"collision_offset": Vector2(0, -23),
			"interaction_size": Vector2(92, 48),
			"interaction_offset": Vector2(4, 20),
			"door_offset": Vector2(4, 0)
		},
		{
			"id": "dock_storehouse",
			"display_name": "Dock Storehouse",
			"atlas_path": "res://assets/buildings/hearthvale_newport_structure_pack_v1_b.png",
			"region": Rect2(51, 836, 361, 377),
			"source_size": Vector2(361, 377),
			"draw_width": 242.0,
			"anchor": Vector2(180.5, 377),
			"position": Vector2(1060, 704),
			"collision_size": Vector2(186, 54),
			"collision_offset": Vector2(0, -27),
			"interaction_size": Vector2(120, 52),
			"interaction_offset": Vector2(0, 20),
			"door_offset": Vector2(0, 0)
		},
		{
			"id": "custom_house",
			"display_name": "Custom House",
			"atlas_path": "res://assets/buildings/hearthvale_newport_structure_pack_v1_a.png",
			"region": Rect2(68, 873, 350, 292),
			"source_size": Vector2(350, 292),
			"draw_width": 226.0,
			"anchor": Vector2(175, 292),
			"position": Vector2(941, 467),
			"collision_size": Vector2(160, 46),
			"collision_offset": Vector2(0, -23),
			"interaction_size": Vector2(86, 48),
			"interaction_offset": Vector2(0, 18),
			"door_offset": Vector2(0, 0)
		},
		{
			"id": "merchant_shop_house",
			"display_name": "Merchant Shop House",
			"atlas_path": "res://assets/buildings/hearthvale_newport_structure_pack_v1_a.png",
			"region": Rect2(418, 76, 410, 332),
			"source_size": Vector2(410, 332),
			"draw_width": 243.0,
			"anchor": Vector2(205, 332),
			"position": Vector2(740, 633),
			"collision_size": Vector2(174, 42),
			"collision_offset": Vector2(0, -21),
			"interaction_size": Vector2(82, 48),
			"interaction_offset": Vector2(-16, 18),
			"door_offset": Vector2(-16, 0)
		},
		{
			"id": "large_residence",
			"display_name": "Large Residence",
			"atlas_path": "res://assets/buildings/hearthvale_newport_structure_pack_v1_a.png",
			"region": Rect2(864, 86, 351, 315),
			"source_size": Vector2(351, 315),
			"draw_width": 227.0,
			"anchor": Vector2(175.5, 315),
			"position": Vector2(698, 443),
			"collision_size": Vector2(168, 42),
			"collision_offset": Vector2(0, -21),
			"interaction_size": Vector2(88, 48),
			"interaction_offset": Vector2(0, 18),
			"door_offset": Vector2(0, 0)
		}
	]

	for config in buildings:
		var atlas_path: String = config["atlas_path"]
		var region: Rect2 = config["region"]
		config["texture"] = _atlas(atlas_path, region)
		var building := BUILDING_SCENE.instantiate()
		world.add_child(building)
		building.configure(config)
