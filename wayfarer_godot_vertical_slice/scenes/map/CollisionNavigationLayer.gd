extends Node2D

const TILE := 32

func _ready() -> void:
	_add_world_edge_collision()
	_add_water_collision()

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
	_add_body(Rect2(-32, -32, 32, 1120), "WestBoundary")
	_add_body(Rect2(1600, -32, 32, 1120), "EastBoundary")
	_add_body(Rect2(-32, -32, 1664, 32), "NorthBoundary")
	_add_body(Rect2(-32, 1024, 1664, 32), "SouthBoundary")

func _add_water_collision() -> void:
	var y := 26 * TILE
	var h := 6 * TILE
	_add_body(Rect2(0, y, 9 * TILE, h), "HarborWaterWest")
	_add_body(Rect2(12 * TILE, y, 8 * TILE, h), "HarborWaterBetweenWest")
	_add_body(Rect2(23 * TILE, y, 8 * TILE, h), "HarborWaterBetweenCenter")
	_add_body(Rect2(34 * TILE, y, 16 * TILE, h), "HarborWaterEast")

