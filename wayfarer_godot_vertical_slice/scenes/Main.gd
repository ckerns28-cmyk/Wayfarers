extends Node2D

const BUILDING_SCENE := preload("res://scenes/buildings/Building.tscn")

@onready var world: Node2D = $World
@onready var player: CharacterBody2D = $World/Player
@onready var hud: CanvasLayer = $HUD

var _atlas_cache: Dictionary = {}

func _ready() -> void:
	world.y_sort_enabled = true
	_place_buildings()
	player.dialogue_triggered.connect(hud.show_dialogue)

func _atlas(path: String, region: Rect2) -> AtlasTexture:
	var texture := AtlasTexture.new()
	texture.atlas = _atlas_image(path)
	texture.region = region
	return texture

func _atlas_image(path: String) -> Texture2D:
	if _atlas_cache.has(path):
		return _atlas_cache[path]

	var image := Image.load_from_file(path)
	if image == null or image.is_empty():
		push_error("Failed to load atlas image: " + path)
		return null

	var atlas_texture := ImageTexture.create_from_image(image)
	_atlas_cache[path] = atlas_texture
	return atlas_texture

func _place_buildings() -> void:
	var buildings := [
		{
			"id": "inn_tavern",
			"display_name": "Inn & Tavern",
			"texture": _atlas("res://assets/buildings/hearthvale_buildings_atlas_v1.png", Rect2(24, 36, 446, 436)),
			"source_size": Vector2(446, 436),
			"draw_width": 278.0,
			"anchor": Vector2(223, 405),
			"position": Vector2(430, 690),
			"collision_size": Vector2(216, 46),
			"collision_offset": Vector2(0, -23),
			"interaction_size": Vector2(92, 48),
			"interaction_offset": Vector2(4, 20),
			"door_offset": Vector2(4, 0)
		},
		{
			"id": "dock_storehouse",
			"display_name": "Dock Storehouse",
			"texture": _atlas("res://assets/buildings/hearthvale_newport_structure_pack_v1_b.png", Rect2(365, 865, 385, 350)),
			"source_size": Vector2(385, 350),
			"draw_width": 258.0,
			"anchor": Vector2(192.5, 350),
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
			"texture": _atlas("res://assets/buildings/hearthvale_newport_structure_pack_v1_a.png", Rect2(42, 824, 368, 357)),
			"source_size": Vector2(368, 357),
			"draw_width": 238.0,
			"anchor": Vector2(184, 324),
			"position": Vector2(930, 456),
			"collision_size": Vector2(160, 46),
			"collision_offset": Vector2(0, -23),
			"interaction_size": Vector2(86, 48),
			"interaction_offset": Vector2(0, 18),
			"door_offset": Vector2(0, 0)
		},
		{
			"id": "merchant_shop_house",
			"display_name": "Merchant Shop House",
			"texture": _atlas("res://assets/buildings/hearthvale_newport_structure_pack_v1_a.png", Rect2(434, 78, 398, 320)),
			"source_size": Vector2(398, 320),
			"draw_width": 236.0,
			"anchor": Vector2(199, 292),
			"position": Vector2(746, 610),
			"collision_size": Vector2(174, 42),
			"collision_offset": Vector2(0, -21),
			"interaction_size": Vector2(82, 48),
			"interaction_offset": Vector2(-16, 18),
			"door_offset": Vector2(-16, 0)
		},
		{
			"id": "large_residence",
			"display_name": "Large Residence",
			"texture": _atlas("res://assets/buildings/hearthvale_newport_structure_pack_v1_a.png", Rect2(841, 65, 372, 334)),
			"source_size": Vector2(372, 334),
			"draw_width": 240.0,
			"anchor": Vector2(186, 301),
			"position": Vector2(690, 420),
			"collision_size": Vector2(168, 42),
			"collision_offset": Vector2(0, -21),
			"interaction_size": Vector2(88, 48),
			"interaction_offset": Vector2(0, 18),
			"door_offset": Vector2(0, 0)
		}
	]

	for config in buildings:
		var building := BUILDING_SCENE.instantiate()
		world.add_child(building)
		building.configure(config)
