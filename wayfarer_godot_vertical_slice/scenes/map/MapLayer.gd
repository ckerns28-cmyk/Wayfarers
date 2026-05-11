extends Node2D

@export_enum("ground", "roads", "wharf_water", "props") var layer_id := "ground"

const TILE := 32
const MAP_W := 50
const MAP_H := 32

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

func _draw_ground() -> void:
	_draw_tiled_rect(Rect2i(0, 0, MAP_W, MAP_H), Color("#5f8052"), Color("#456b45"))
	_draw_tiled_rect(Rect2i(4, 5, 7, 5), Color("#6f8c5d"), Color("#53774a"), Color(0, 0, 0, 0.03))
	_draw_tiled_rect(Rect2i(35, 4, 9, 7), Color("#6a8959"), Color("#506f4c"), Color(0, 0, 0, 0.03))
	_draw_tiled_rect(Rect2i(5, 23, 11, 5), Color("#587747"), Color("#45683f"), Color(0, 0, 0, 0.03))

func _draw_roads() -> void:
	_draw_tiled_rect(Rect2i(4, 18, 40, 2), Color("#a9926a"), Color("#8b7653"))
	_draw_tiled_rect(Rect2i(6, 14, 32, 2), Color("#a38d69"), Color("#857355"))
	_draw_tiled_rect(Rect2i(18, 9, 12, 6), Color("#9a9a85"), Color("#777b6f"))
	_draw_tiled_rect(Rect2i(15, 6, 2, 14), Color("#a9926a"), Color("#887452"))
	_draw_tiled_rect(Rect2i(24, 6, 2, 14), Color("#a9926a"), Color("#887452"))
	_draw_tiled_rect(Rect2i(33, 8, 2, 12), Color("#a9926a"), Color("#887452"))
	_draw_tiled_rect(Rect2i(10, 6, 28, 2), Color("#9f8964"), Color("#806d50"))
	for p in [Vector2i(13, 12), Vector2i(27, 10), Vector2i(37, 16), Vector2i(8, 17), Vector2i(43, 18)]:
		draw_rect(_tile_rect(p.x, p.y, 1, 1).grow(-11), Color("#b7754d"), true)

func _draw_wharf_water() -> void:
	_draw_tiled_rect(Rect2i(0, 22, MAP_W, 10), Color("#346c7f"), Color("#1f5165"), Color(0, 0, 0, 0.04))
	_draw_tiled_rect(Rect2i(4, 21, 40, 1), Color("#7c7258"), Color("#5d5644"))
	for pier in [Rect2i(9, 18, 3, 8), Rect2i(20, 18, 3, 8), Rect2i(31, 18, 3, 8)]:
		_draw_tiled_rect(pier, Color("#8f6d48"), Color("#654b34"))
		for y in range(pier.position.y, pier.position.y + pier.size.y):
			draw_line(Vector2(pier.position.x * TILE, y * TILE), Vector2((pier.position.x + pier.size.x) * TILE, y * TILE), Color(0, 0, 0, 0.16), 2.0)
	for x in range(0, MAP_W):
		var wave_y := 23 * TILE + ((x % 3) * 3)
		draw_line(Vector2(x * TILE + 8, wave_y), Vector2(x * TILE + 24, wave_y), Color(0.75, 0.95, 1.0, 0.18), 2.0)

func _draw_props() -> void:
	for pos in [Vector2i(11, 18), Vector2i(22, 18), Vector2i(32, 18), Vector2i(35, 18), Vector2i(8, 12), Vector2i(42, 14)]:
		draw_circle(Vector2(pos.x * TILE + 16, pos.y * TILE + 18), 8, Color("#75543a"))
		draw_arc(Vector2(pos.x * TILE + 16, pos.y * TILE + 18), 8, 0, TAU, 16, Color("#c09b62"), 1.5)
	for pos in [Vector2i(5, 20), Vector2i(14, 21), Vector2i(28, 19), Vector2i(45, 21)]:
		draw_rect(_tile_rect(pos.x, pos.y).grow(-7), Color("#9b7042"), true)
		draw_rect(_tile_rect(pos.x, pos.y).grow(-7), Color("#392819"), false, 1.5)
	for pos in [Vector2i(7, 7), Vector2i(41, 7), Vector2i(5, 15), Vector2i(45, 12)]:
		draw_circle(Vector2(pos.x * TILE + 16, pos.y * TILE + 20), 12, Color("#2f5d35"))
		draw_circle(Vector2(pos.x * TILE + 9, pos.y * TILE + 13), 8, Color("#3d7042"))

