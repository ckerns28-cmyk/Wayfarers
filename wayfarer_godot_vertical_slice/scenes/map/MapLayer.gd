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

func _draw_tiled_rect(rect: Rect2i, base: Color, alt: Color, line := Color(0, 0, 0, 0.035)) -> void:
	for y in range(rect.position.y, rect.position.y + rect.size.y):
		for x in range(rect.position.x, rect.position.x + rect.size.x):
			var n := float((x * 19 + y * 31) % 100) / 100.0
			draw_rect(_tile_rect(x, y), base.lerp(alt, n * 0.35), true)
			if line.a > 0.0:
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
		_draw_walk_rect(segment, Color("#a58c64"), Color("#7d6a4d"), 5.0, "primary")
	for segment in NEWPORT_TOWN.secondary_roads():
		_draw_walk_rect(segment, Color("#9a805a"), Color("#766247"), 8.0, "secondary")
	for segment in NEWPORT_TOWN.service_lanes():
		_draw_walk_rect(segment, Color("#806f51"), Color("#64543d"), 10.0, "service")
	for plaza in NEWPORT_TOWN.civic_square_rects():
		_draw_cobble_rect(plaza, Color("#96927b"), Color("#727568"), 5.0)
	for apron in NEWPORT_TOWN.waterfront_apron_rects():
		_draw_cobble_rect(apron, Color("#84775b"), Color("#625a45"), 3.0)
	for p in [Vector2i(11, 17), Vector2i(17, 17), Vector2i(23, 17), Vector2i(29, 17), Vector2i(20, 11), Vector2i(37, 14), Vector2i(42, 14)]:
		draw_rect(_tile_rect(p.x, p.y, 1, 1).grow(-12), Color("#b7754d"), true)
		draw_rect(_tile_rect(p.x, p.y, 1, 1).grow(-12), Color(0, 0, 0, 0.22), false, 1.0)

func _draw_wharf_water() -> void:
	for water in NEWPORT_TOWN.water_rects():
		_draw_tiled_rect(water, Color("#346f83"), Color("#1f5268"), Color(0, 0, 0, 0.04))
	for support in NEWPORT_TOWN.wharf_support_rects():
		_draw_plank_rect(support, Color("#786a50"), Color("#5b523f"))
	_draw_plank_rect(Rect2i(8, 19, 25, 1), Color("#877a5b"), Color("#655d48"))
	draw_line(Vector2(8 * TILE, 20 * TILE), Vector2(39 * TILE, 20 * TILE), Color(0.05, 0.12, 0.13, 0.36), 3.0)
	for pier_config in NEWPORT_TOWN.pier_rects():
		var pier: Rect2i = pier_config["rect"]
		_draw_plank_rect(pier, Color("#8f6d48"), Color("#654b34"))
		for y in range(pier.position.y, pier.position.y + pier.size.y):
			draw_line(Vector2(pier.position.x * TILE + 4, y * TILE), Vector2((pier.position.x + pier.size.x) * TILE - 4, y * TILE), Color(0, 0, 0, 0.16), 2.0)
			_draw_post(Vector2(pier.position.x * TILE + 5, y * TILE + 25))
			if y % 2 == 0:
				_draw_post(Vector2((pier.position.x + pier.size.x) * TILE - 5, y * TILE + 25))
	for x in range(0, MAP_W):
		var wave_y := 22 * TILE + ((x % 3) * 3)
		draw_line(Vector2(x * TILE + 8, wave_y), Vector2(x * TILE + 24, wave_y), Color(0.75, 0.95, 1.0, 0.18), 2.0)
		if x % 2 == 0:
			draw_line(Vector2(x * TILE + 4, wave_y + 92), Vector2(x * TILE + 20, wave_y + 92), Color(0.75, 0.95, 1.0, 0.12), 2.0)
	for p in [Vector2i(8, 20), Vector2i(14, 20), Vector2i(21, 20), Vector2i(28, 20), Vector2i(34, 20), Vector2i(38, 21)]:
		_draw_shore_rocks(Vector2(p.x * TILE + 12, p.y * TILE + 8))

func _draw_props() -> void:
	for pos in [Vector2i(11, 18), Vector2i(16, 18), Vector2i(19, 18), Vector2i(23, 18), Vector2i(29, 18), Vector2i(32, 18), Vector2i(5, 14), Vector2i(42, 15), Vector2i(27, 18), Vector2i(37, 15)]:
		_draw_rope_coil(Vector2(pos.x * TILE + 16, pos.y * TILE + 18))
	for pos in [Vector2i(9, 17), Vector2i(14, 17), Vector2i(21, 17), Vector2i(26, 17), Vector2i(31, 17), Vector2i(40, 16), Vector2i(44, 17), Vector2i(15, 18), Vector2i(24, 18)]:
		_draw_crate_stack(Vector2(pos.x * TILE + 10, pos.y * TILE + 15))
	for pos in [Vector2i(7, 6), Vector2i(34, 6), Vector2i(5, 15), Vector2i(45, 12), Vector2i(14, 2), Vector2i(25, 2), Vector2i(30, 3)]:
		draw_circle(Vector2(pos.x * TILE + 16, pos.y * TILE + 20), 12, Color("#2f5d35"))
		draw_circle(Vector2(pos.x * TILE + 9, pos.y * TILE + 13), 8, Color("#3d7042"))
	for pos in [Vector2i(13, 7), Vector2i(18, 7), Vector2i(24, 7), Vector2i(32, 7), Vector2i(20, 12)]:
		draw_circle(Vector2(pos.x * TILE + 16, pos.y * TILE + 18), 4, Color("#2f251b"))
		draw_circle(Vector2(pos.x * TILE + 16, pos.y * TILE + 12), 3, Color("#d8b56f"))
	_draw_barrels(Vector2(354, 548), 3)
	_draw_barrels(Vector2(850, 548), 2)
	_draw_barrels(Vector2(1304, 524), 3)
	_draw_market_table(Vector2(808, 592))
	_draw_fish_rack(Vector2(882, 570))
	_draw_net_bundle(Vector2(395, 646))
	_draw_net_bundle(Vector2(990, 652))
	_draw_rowboat(Vector2(626, 836))
	_draw_sign_post(Vector2(352, 386), Color("#9d4e38"))
	_draw_sign_post(Vector2(536, 388), Color("#4f6d48"))
	_draw_sign_post(Vector2(920, 386), Color("#90703d"))
	_draw_clothesline(Vector2(1200, 368), Vector2(1320, 344))
	_draw_fence_line(Vector2(374, 229), Vector2(515, 229), Color("#d9c89c"))
	_draw_fence_line(Vector2(728, 229), Vector2(884, 229), Color("#d9c89c"))
	_draw_fence_line(Vector2(1040, 229), Vector2(1176, 229), Color("#d9c89c"))
	_draw_woodpile(Vector2(150, 446))

func _draw_garden_rect(rect: Rect2i, base := Color("#789969"), alt := Color("#5f844f")) -> void:
	_draw_tiled_rect(rect, base, alt, Color(0, 0, 0, 0.025))
	draw_rect(_tile_rect(rect.position.x, rect.position.y, rect.size.x, rect.size.y).grow(-6), Color(0.15, 0.25, 0.13, 0.18), false, 1.0)
	for y in range(rect.position.y, rect.position.y + rect.size.y):
		for x in range(rect.position.x, rect.position.x + rect.size.x):
			if (x * 11 + y * 7) % 3 == 0:
				draw_rect(Rect2(Vector2(x * TILE + 10, y * TILE + 12), Vector2(4, 3)), Color("#d8c174"), true)

func _draw_walk_rect(rect: Rect2i, base: Color, alt: Color, inset: float, kind: String) -> void:
	var world_rect := _tile_rect(rect.position.x, rect.position.y, rect.size.x, rect.size.y).grow(-inset)
	draw_rect(world_rect.grow(4.0), Color(0, 0, 0, 0.08), true)
	draw_rect(world_rect, base, true)
	for y in range(rect.position.y, rect.position.y + rect.size.y):
		for x in range(rect.position.x, rect.position.x + rect.size.x):
			var tile := _tile_rect(x, y).grow(-inset)
			var n := float((x * 23 + y * 17) % 100) / 100.0
			draw_rect(tile, base.lerp(alt, n * 0.45), true)
			if kind != "service":
				draw_line(Vector2(tile.position.x + 6, tile.position.y + 8 + int(n * 9.0)), Vector2(tile.position.x + tile.size.x - 7, tile.position.y + 9 + int(n * 9.0)), Color(0.96, 0.86, 0.62, 0.14), 1.0)
			else:
				draw_circle(tile.position + Vector2(9 + int(n * 8.0), 10 + int(n * 7.0)), 1.4, Color(0.18, 0.12, 0.08, 0.18))
	draw_rect(world_rect, Color(0, 0, 0, 0.16), false, 1.0)

func _draw_cobble_rect(rect: Rect2i, base: Color, alt: Color, inset: float) -> void:
	var world_rect := _tile_rect(rect.position.x, rect.position.y, rect.size.x, rect.size.y).grow(-inset)
	draw_rect(world_rect.grow(3.0), Color(0, 0, 0, 0.08), true)
	for y in range(rect.position.y, rect.position.y + rect.size.y):
		for x in range(rect.position.x, rect.position.x + rect.size.x):
			var tile := _tile_rect(x, y).grow(-inset)
			var n := float((x * 31 + y * 13) % 100) / 100.0
			draw_rect(tile, base.lerp(alt, n * 0.36), true)
			draw_rect(tile.grow(-6.0), Color(1, 0.94, 0.76, 0.08), false, 1.0)
	draw_rect(world_rect, Color(0, 0, 0, 0.14), false, 1.0)

func _draw_plank_rect(rect: Rect2i, base: Color, alt: Color) -> void:
	for y in range(rect.position.y, rect.position.y + rect.size.y):
		for x in range(rect.position.x, rect.position.x + rect.size.x):
			var tile := _tile_rect(x, y).grow(-2.0)
			var n := float((x * 29 + y * 43) % 100) / 100.0
			draw_rect(tile, base.lerp(alt, n * 0.40), true)
			draw_line(Vector2(tile.position.x + 3, tile.position.y + 8), Vector2(tile.position.x + tile.size.x - 3, tile.position.y + 8), Color(0, 0, 0, 0.20), 1.0)
			draw_line(Vector2(tile.position.x + 4, tile.position.y + 20), Vector2(tile.position.x + tile.size.x - 4, tile.position.y + 20), Color(1, 0.88, 0.58, 0.10), 1.0)
			draw_rect(tile, Color(0, 0, 0, 0.14), false, 1.0)

func _draw_post(pos: Vector2) -> void:
	draw_rect(Rect2(pos + Vector2(-2, -8), Vector2(4, 12)), Color("#382a1f"), true)
	draw_rect(Rect2(pos + Vector2(-2, -8), Vector2(4, 2)), Color("#7d6144"), true)

func _draw_shore_rocks(pos: Vector2) -> void:
	draw_circle(pos, 4, Color("#5e5849"))
	draw_circle(pos + Vector2(9, 4), 3, Color("#4f4c43"))
	draw_circle(pos + Vector2(17, -1), 2.5, Color("#7a7059"))

func _draw_rope_coil(pos: Vector2) -> void:
	draw_circle(pos, 8, Color("#75543a"))
	draw_arc(pos, 8, 0, TAU, 18, Color("#c09b62"), 1.5)
	draw_arc(pos, 4.5, 0, TAU, 14, Color("#d5b574"), 1.2)

func _draw_crate_stack(pos: Vector2) -> void:
	draw_rect(Rect2(pos, Vector2(17, 15)), Color("#9b7042"), true)
	draw_rect(Rect2(pos, Vector2(17, 15)), Color("#392819"), false, 1.3)
	draw_line(pos + Vector2(2, 3), pos + Vector2(15, 13), Color(0.18, 0.11, 0.06, 0.55), 1.0)
	draw_rect(Rect2(pos + Vector2(14, -7), Vector2(13, 12)), Color("#ad7d49"), true)
	draw_rect(Rect2(pos + Vector2(14, -7), Vector2(13, 12)), Color("#392819"), false, 1.0)

func _draw_barrels(pos: Vector2, count: int) -> void:
	for i in range(count):
		var barrel_pos := pos + Vector2(i * 9, 0)
		_draw_ellipse(barrel_pos, Vector2(4, 7), Color("#7f5631"))
		draw_rect(Rect2(barrel_pos + Vector2(-4, -1), Vector2(8, 2)), Color("#3f2c1d"), true)
		draw_arc(barrel_pos, 6, 0, TAU, 12, Color("#b48750"), 1.0)

func _draw_market_table(pos: Vector2) -> void:
	draw_rect(Rect2(pos, Vector2(58, 17)), Color("#80603c"), true)
	draw_rect(Rect2(pos + Vector2(2, 2), Vector2(54, 4)), Color("#d2b06e"), true)
	for i in range(7):
		var color := Color("#d9c37a") if i % 2 == 0 else Color("#a95e45")
		draw_circle(pos + Vector2(8 + i * 7, 11), 2.4, color)
	draw_rect(Rect2(pos + Vector2(4, 17), Vector2(3, 8)), Color("#4d3824"), true)
	draw_rect(Rect2(pos + Vector2(50, 17), Vector2(3, 8)), Color("#4d3824"), true)

func _draw_fish_rack(pos: Vector2) -> void:
	draw_line(pos, pos + Vector2(38, 0), Color("#6c4b30"), 2.0)
	draw_line(pos + Vector2(3, 0), pos + Vector2(3, 18), Color("#6c4b30"), 2.0)
	draw_line(pos + Vector2(35, 0), pos + Vector2(35, 18), Color("#6c4b30"), 2.0)
	for i in range(7):
		draw_rect(Rect2(pos + Vector2(6 + i * 5, 2), Vector2(2, 9)), Color("#c9b98c"), true)

func _draw_net_bundle(pos: Vector2) -> void:
	draw_arc(pos, 14, 0.15, PI - 0.15, 16, Color("#c8b277"), 1.0)
	draw_arc(pos + Vector2(4, 2), 11, 0.15, PI - 0.15, 16, Color("#a98e58"), 1.0)
	for i in range(4):
		draw_line(pos + Vector2(-10 + i * 6, 0), pos + Vector2(-6 + i * 7, 12), Color("#c8b277"), 1.0)

func _draw_rowboat(pos: Vector2) -> void:
	_draw_ellipse(pos, Vector2(32, 8), Color(0.18, 0.12, 0.07, 0.48))
	_draw_ellipse(pos, Vector2(26, 7), Color("#65452c"))
	_draw_ellipse(pos, Vector2(18, 4), Color("#2c4f5b"))
	draw_line(pos + Vector2(-18, -2), pos + Vector2(18, -2), Color("#a67c4c"), 1.5)

func _draw_sign_post(pos: Vector2, color: Color) -> void:
	draw_rect(Rect2(pos + Vector2(-1, 0), Vector2(2, 18)), Color("#3e2c1d"), true)
	draw_rect(Rect2(pos + Vector2(-8, 1), Vector2(16, 8)), color, true)
	draw_rect(Rect2(pos + Vector2(-8, 1), Vector2(16, 8)), Color(0, 0, 0, 0.35), false, 1.0)

func _draw_clothesline(a: Vector2, b: Vector2) -> void:
	draw_line(a, b, Color("#d6c49c"), 1.0)
	for i in range(4):
		var t := float(i + 1) / 5.0
		var p := a.lerp(b, t)
		draw_rect(Rect2(p + Vector2(-5, 1), Vector2(10, 9)), Color("#d8d2b6") if i % 2 == 0 else Color("#7b8c9c"), true)

func _draw_fence_line(a: Vector2, b: Vector2, color: Color) -> void:
	draw_line(a, b, color, 1.5)
	var distance := a.distance_to(b)
	var steps := int(distance / 12.0)
	for i in range(steps + 1):
		var p := a.lerp(b, float(i) / maxf(1.0, steps))
		draw_rect(Rect2(p + Vector2(-1, -6), Vector2(2, 12)), color.darkened(0.25), true)

func _draw_woodpile(pos: Vector2) -> void:
	for i in range(5):
		var p := pos + Vector2(i * 7, (i % 2) * 4)
		draw_rect(Rect2(p, Vector2(10, 3)), Color("#775032"), true)
		draw_circle(p + Vector2(1, 1.5), 1.5, Color("#b98750"))

func _draw_ellipse(center: Vector2, radii: Vector2, color: Color) -> void:
	draw_set_transform(center, 0.0, Vector2(radii.x / 16.0, radii.y / 16.0))
	draw_circle(Vector2.ZERO, 16.0, color)
	draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
