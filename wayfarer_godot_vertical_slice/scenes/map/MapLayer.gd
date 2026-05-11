extends Node2D

@export_enum("ground", "roads", "wharf_water", "props") var layer_id := "ground"

const NEWPORT_TOWN := preload("res://scripts/NewportTownBlueprint.gd")
const TILE := NEWPORT_TOWN.TILE
const MAP_W := NEWPORT_TOWN.MAP_TILES.x
const MAP_H := NEWPORT_TOWN.MAP_TILES.y

func _ready() -> void:
	queue_redraw()

func _draw() -> void:
	match layer_id:
		"ground":
			_draw_ground()
		"roads":
			_draw_roads()
		"wharf_water":
			_draw_wharf_water()
		"props":
			_draw_props()

func _tile_rect(x: int, y: int, w: int = 1, h: int = 1) -> Rect2:
	return Rect2(x * TILE, y * TILE, w * TILE, h * TILE)

func _draw_tiled_rect(rect: Rect2i, base: Color, alt: Color, line := Color(0, 0, 0, 0.08)) -> void:
	for y in range(rect.position.y, rect.position.y + rect.size.y):
		for x in range(rect.position.x, rect.position.x + rect.size.x):
			var n := float((x * 19 + y * 31) % 100) / 100.0
			draw_rect(_tile_rect(x, y), base.lerp(alt, n * 0.35), true)
			draw_rect(_tile_rect(x, y), line, false, 1.0)

func _draw_tile_rect_outline(rect: Rect2i, color: Color, width := 2.0) -> void:
	draw_rect(_tile_rect(rect.position.x, rect.position.y, rect.size.x, rect.size.y), color, false, width)

func _draw_ground() -> void:
	_draw_tiled_rect(NEWPORT_TOWN.base_ground_rect(), Color("#5f8052"), Color("#456b45"))
	for district in NEWPORT_TOWN.district_rects():
		_draw_tiled_rect(district["rect"], district["base"], district["alt"], Color(0, 0, 0, 0.025))
	_draw_garden_rect(Rect2i(11, 1, 5, 3))
	_draw_garden_rect(Rect2i(17, 1, 5, 3))
	_draw_garden_rect(Rect2i(23, 1, 5, 3))
	_draw_garden_rect(Rect2i(29, 1, 5, 3))
	_draw_garden_rect(Rect2i(19, 8, 8, 2), Color("#769569"), Color("#587c54"))
	_draw_garden_rect(Rect2i(4, 15, 5, 3), Color("#668452"), Color("#4c7047"))
	_draw_garden_rect(Rect2i(38, 15, 7, 3), Color("#6f7654"), Color("#5a654a"))

func _draw_roads() -> void:
	for segment in NEWPORT_TOWN.primary_roads():
		_draw_tiled_rect(segment, Color("#ad9265"), Color("#8b7754"), Color(0, 0, 0, 0.075))
	for segment in NEWPORT_TOWN.secondary_roads():
		_draw_tiled_rect(segment, Color("#a28a63"), Color("#806f51"), Color(0, 0, 0, 0.07))
	for segment in NEWPORT_TOWN.service_lanes():
		_draw_tiled_rect(segment, Color("#8c7958"), Color("#6e6048"), Color(0, 0, 0, 0.07))
	for plaza in NEWPORT_TOWN.civic_square_rects():
		_draw_tiled_rect(plaza, Color("#9c9a83"), Color("#777c70"), Color(0, 0, 0, 0.065))
	for apron in NEWPORT_TOWN.waterfront_apron_rects():
		_draw_tiled_rect(apron, Color("#8b8062"), Color("#68614c"), Color(0, 0, 0, 0.07))
	for segment in NEWPORT_TOWN.route_rects():
		_draw_tile_rect_outline(segment, Color(0, 0, 0, 0.12), 1.5)
	for p in [Vector2i(11, 17), Vector2i(17, 17), Vector2i(23, 17), Vector2i(29, 17), Vector2i(20, 11), Vector2i(37, 14), Vector2i(42, 14)]:
		draw_rect(_tile_rect(p.x, p.y, 1, 1).grow(-11), Color("#b7754d"), true)

func _draw_wharf_water() -> void:
	for water in NEWPORT_TOWN.water_rects():
		_draw_tiled_rect(water, Color("#346f83"), Color("#1f5268"), Color(0, 0, 0, 0.04))
	for support in NEWPORT_TOWN.wharf_support_rects():
		_draw_tiled_rect(support, Color("#786a50"), Color("#5b523f"), Color(0, 0, 0, 0.07))
	_draw_tiled_rect(Rect2i(8, 19, 25, 1), Color("#877a5b"), Color("#655d48"), Color(0, 0, 0, 0.08))
	draw_line(Vector2(8 * TILE, 20 * TILE), Vector2(39 * TILE, 20 * TILE), Color(0.05, 0.12, 0.13, 0.36), 3.0)
	for pier_config in NEWPORT_TOWN.pier_rects():
		var pier: Rect2i = pier_config["rect"]
		_draw_tiled_rect(pier, Color("#8f6d48"), Color("#654b34"), Color(0, 0, 0, 0.08))
		for y in range(pier.position.y, pier.position.y + pier.size.y):
			draw_line(Vector2(pier.position.x * TILE, y * TILE), Vector2((pier.position.x + pier.size.x) * TILE, y * TILE), Color(0, 0, 0, 0.16), 2.0)
	for x in range(0, MAP_W):
		var wave_y := 22 * TILE + ((x % 3) * 3)
		draw_line(Vector2(x * TILE + 8, wave_y), Vector2(x * TILE + 24, wave_y), Color(0.75, 0.95, 1.0, 0.18), 2.0)
		if x % 2 == 0:
			draw_line(Vector2(x * TILE + 4, wave_y + 92), Vector2(x * TILE + 20, wave_y + 92), Color(0.75, 0.95, 1.0, 0.12), 2.0)

func _draw_props() -> void:
	for pos in [Vector2i(11, 18), Vector2i(16, 18), Vector2i(19, 18), Vector2i(23, 18), Vector2i(29, 18), Vector2i(32, 18), Vector2i(5, 14), Vector2i(42, 15)]:
		draw_circle(Vector2(pos.x * TILE + 16, pos.y * TILE + 18), 8, Color("#75543a"))
		draw_arc(Vector2(pos.x * TILE + 16, pos.y * TILE + 18), 8, 0, TAU, 16, Color("#c09b62"), 1.5)
	for pos in [Vector2i(9, 17), Vector2i(14, 17), Vector2i(21, 17), Vector2i(26, 17), Vector2i(31, 17), Vector2i(40, 16), Vector2i(44, 17)]:
		draw_rect(_tile_rect(pos.x, pos.y).grow(-7), Color("#9b7042"), true)
		draw_rect(_tile_rect(pos.x, pos.y).grow(-7), Color("#392819"), false, 1.5)
	for pos in [Vector2i(7, 6), Vector2i(34, 6), Vector2i(5, 15), Vector2i(45, 12), Vector2i(14, 2), Vector2i(25, 2), Vector2i(30, 3)]:
		draw_circle(Vector2(pos.x * TILE + 16, pos.y * TILE + 20), 12, Color("#2f5d35"))
		draw_circle(Vector2(pos.x * TILE + 9, pos.y * TILE + 13), 8, Color("#3d7042"))
	for pos in [Vector2i(13, 7), Vector2i(18, 7), Vector2i(24, 7), Vector2i(32, 7), Vector2i(20, 12)]:
		draw_circle(Vector2(pos.x * TILE + 16, pos.y * TILE + 18), 4, Color("#2f251b"))
		draw_circle(Vector2(pos.x * TILE + 16, pos.y * TILE + 12), 3, Color("#d8b56f"))

func _draw_garden_rect(rect: Rect2i, base := Color("#789969"), alt := Color("#5f844f")) -> void:
	_draw_tiled_rect(rect, base, alt, Color(0, 0, 0, 0.025))
	draw_rect(_tile_rect(rect.position.x, rect.position.y, rect.size.x, rect.size.y).grow(-6), Color(0.15, 0.25, 0.13, 0.18), false, 1.0)
	for y in range(rect.position.y, rect.position.y + rect.size.y):
		for x in range(rect.position.x, rect.position.x + rect.size.x):
			if (x * 11 + y * 7) % 3 == 0:
				draw_rect(Rect2(Vector2(x * TILE + 10, y * TILE + 12), Vector2(4, 3)), Color("#d8c174"), true)
