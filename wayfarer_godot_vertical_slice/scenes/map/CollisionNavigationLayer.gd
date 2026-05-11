extends Node2D

const NEWPORT_TOWN := preload("res://scripts/NewportTownBlueprint.gd")
const TILE := NEWPORT_TOWN.TILE

func _ready() -> void:
	_add_world_edge_collision()
	_add_water_collision()
	_add_detail_blockers()

func _add_body(rect: Rect2, label: String) -> void:
	var body := StaticBody2D.new()
	body.name = label
	body.collision_layer = 1
	body.collision_mask = 0
	add_child(body)

	var shape := CollisionShape2D.new()
	var rectangle := RectangleShape2D.new()
	rectangle.size = rect.size
	shape.shape = rectangle
	shape.position = rect.position + rect.size * 0.5
	body.add_child(shape)

func _add_world_edge_collision() -> void:
	var world_size := NEWPORT_TOWN.WORLD_SIZE
	_add_body(Rect2(-TILE, -TILE, TILE, world_size.y + TILE * 2), "WestBoundary")
	_add_body(Rect2(world_size.x, -TILE, TILE, world_size.y + TILE * 2), "EastBoundary")
	_add_body(Rect2(-TILE, -TILE, world_size.x + TILE * 2, TILE), "NorthBoundary")
	_add_body(Rect2(-TILE, world_size.y, world_size.x + TILE * 2, TILE), "SouthBoundary")

func _add_water_collision() -> void:
	for tile in NEWPORT_TOWN.water_collision_tiles():
		_add_body(Rect2(tile.x * TILE, tile.y * TILE, TILE, TILE), "HarborWater_%d_%d" % [tile.x, tile.y])

func _add_detail_blockers() -> void:
	for blocker_config in NEWPORT_TOWN.detail_blockers():
		var blocker: Dictionary = blocker_config
		_add_body(blocker["rect"], "DetailBlocker_" + String(blocker["id"]))
