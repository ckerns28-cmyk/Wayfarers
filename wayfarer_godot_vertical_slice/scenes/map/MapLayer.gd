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
	var world_rect := Rect2(Vector2.ZERO, NEWPORT_TOWN.WORLD_SIZE)
	_draw_soft_rect(world_rect, Color("#587a4d"), Color("#496f45"), 1.0, 48)
	_draw_soft_rect(Rect2(190, 48, 1050, 245), Color("#6b8a5b"), Color("#55774d"), 0.56, 22)
	_draw_soft_rect(Rect2(465, 255, 465, 190), Color("#667e5b"), Color("#536f4f"), 0.48, 16)
	_draw_soft_rect(Rect2(210, 392, 1060, 270), Color("#5e774d"), Color("#4c6944"), 0.54, 28)
	_draw_soft_rect(Rect2(70, 300, 360, 330), Color("#59744a"), Color("#486741"), 0.42, 16)
	_draw_soft_rect(Rect2(1095, 300, 350, 330), Color("#5f744e"), Color("#4c6444"), 0.42, 16)
	_draw_planting_bed(Rect2(360, 82, 160, 64))
	_draw_planting_bed(Rect2(548, 80, 174, 66))
	_draw_planting_bed(Rect2(760, 78, 188, 68))
	_draw_planting_bed(Rect2(992, 88, 154, 58))
	_draw_planting_bed(Rect2(560, 286, 300, 70), Color("#718d64"), Color("#5b7b54"))
	_draw_planting_bed(Rect2(116, 452, 160, 88), Color("#668051"), Color("#4f6c46"))
	_draw_planting_bed(Rect2(1180, 430, 180, 100), Color("#697755"), Color("#566749"))

func _draw_roads() -> void:
	_draw_cobbled_world_rect(Rect2(545, 318, 345, 130), Color("#918a73"), Color("#6d715f"), 42)
	_draw_cobbled_world_rect(Rect2(230, 588, 910, 94), Color("#85775b"), Color("#635a45"), 78)
	_draw_path_line(Vector2(250, 580), Vector2(1130, 580), 48.0, Color("#a58a61"), Color("#726049"))
	_draw_path_line(Vector2(645, 350), Vector2(650, 660), 34.0, Color("#9b815d"), Color("#6f5d45"))
	_draw_path_line(Vector2(402, 330), Vector2(1080, 330), 36.0, Color("#9d865f"), Color("#726049"))
	_draw_path_line(Vector2(350, 530), Vector2(365, 645), 28.0, Color("#8d7353"), Color("#655541"), false)
	_draw_path_line(Vector2(1210, 350), Vector2(1210, 625), 28.0, Color("#836c4e"), Color("#5d513e"), false)
	_draw_path_line(Vector2(1340, 325), Vector2(1330, 590), 24.0, Color("#80694c"), Color("#5c4e3c"), false)
	_draw_path_line(Vector2(1088, 500), Vector2(1350, 500), 30.0, Color("#907755"), Color("#67563f"))
	_draw_path_line(Vector2(160, 515), Vector2(355, 520), 30.0, Color("#8f7655"), Color("#66553f"))
	_draw_cobbled_world_rect(Rect2(260, 680, 850, 46), Color("#766f57"), Color("#5a5542"), 54)
	for p in [Vector2(316, 552), Vector2(466, 548), Vector2(612, 548), Vector2(792, 548), Vector2(966, 548), Vector2(678, 376), Vector2(1230, 500)]:
		_draw_door_step(p)

func _draw_wharf_water() -> void:
	_draw_soft_rect(Rect2(0, 690, NEWPORT_TOWN.WORLD_SIZE.x, 334), Color("#2f7184"), Color("#1f5369"), 1.0, 36)
	draw_colored_polygon(PackedVector2Array([
		Vector2(0, 662), Vector2(255, 658), Vector2(330, 690), Vector2(470, 678),
		Vector2(610, 684), Vector2(760, 666), Vector2(950, 682), Vector2(1120, 668),
		Vector2(1245, 700), Vector2(1600, 690), Vector2(1600, 730), Vector2(0, 730)
	]), Color(0.30, 0.43, 0.36, 0.46))
	draw_polyline(PackedVector2Array([
		Vector2(0, 662), Vector2(255, 658), Vector2(330, 690), Vector2(470, 678),
		Vector2(610, 684), Vector2(760, 666), Vector2(950, 682), Vector2(1120, 668),
		Vector2(1245, 700), Vector2(1600, 690)
	]), Color(0.05, 0.12, 0.13, 0.42), 4.0)
	_draw_plank_world_rect(Rect2(248, 676, 895, 58), Color("#84765a"), Color("#625841"))
	_draw_plank_world_rect(Rect2(270, 720, 150, 140), Color("#7d6547"), Color("#5b4733"))
	_draw_plank_world_rect(Rect2(525, 708, 95, 170), Color("#856948"), Color("#5f4932"))
	_draw_plank_world_rect(Rect2(760, 704, 95, 200), Color("#8c6b47"), Color("#654b34"))
	_draw_plank_world_rect(Rect2(955, 715, 140, 150), Color("#7b6347"), Color("#5a4733"))
	_draw_post_line(Vector2(255, 680), Vector2(1125, 680), 58.0)
	_draw_post_line(Vector2(278, 728), Vector2(278, 846), 46.0)
	_draw_post_line(Vector2(410, 728), Vector2(410, 846), 46.0)
	_draw_post_line(Vector2(766, 714), Vector2(766, 894), 46.0)
	_draw_post_line(Vector2(846, 714), Vector2(846, 894), 46.0)
	for i in range(28):
		var x := 18.0 + float((i * 57) % 1510)
		var y := 760.0 + float((i * 43) % 235)
		draw_line(Vector2(x, y), Vector2(x + 22.0, y - 1.0), Color(0.75, 0.95, 1.0, 0.15), 2.0)
	for p in [Vector2(262, 666), Vector2(424, 690), Vector2(615, 680), Vector2(748, 668), Vector2(914, 680), Vector2(1120, 668), Vector2(1244, 700)]:
		_draw_shore_rocks(p)

func _draw_props() -> void:
	for pos in [Vector2(292, 612), Vector2(340, 628), Vector2(486, 544), Vector2(526, 556), Vector2(706, 544), Vector2(900, 542), Vector2(1038, 612), Vector2(1210, 534), Vector2(1318, 516)]:
		_draw_crate_stack(pos)
	for pos in [Vector2(322, 552), Vector2(552, 548), Vector2(760, 548), Vector2(935, 548), Vector2(1008, 634), Vector2(1240, 542)]:
		_draw_barrels(pos, 3)
	for pos in [Vector2(385, 636), Vector2(602, 626), Vector2(842, 625), Vector2(996, 646), Vector2(1082, 650), Vector2(762, 746)]:
		_draw_rope_coil(pos)
	_draw_market_table(Vector2(664, 620))
	_draw_market_table(Vector2(730, 622))
	_draw_fish_rack(Vector2(884, 590))
	_draw_net_bundle(Vector2(316, 672))
	_draw_net_bundle(Vector2(1004, 672))
	_draw_rowboat(Vector2(805, 900))
	_draw_rowboat(Vector2(370, 842))
	_draw_sign_post(Vector2(348, 548), Color("#9d4e38"))
	_draw_sign_post(Vector2(506, 535), Color("#4f6d48"))
	_draw_sign_post(Vector2(922, 535), Color("#90703d"))
	_draw_clothesline(Vector2(1182, 390), Vector2(1306, 368))
	_draw_fence_line(Vector2(372, 222), Vector2(516, 222), Color("#d9c89c"))
	_draw_fence_line(Vector2(720, 224), Vector2(892, 224), Color("#d9c89c"))
	_draw_fence_line(Vector2(1030, 232), Vector2(1185, 232), Color("#d9c89c"))
	_draw_woodpile(Vector2(154, 488))
	for pos in [Vector2(112, 438), Vector2(1360, 372), Vector2(1168, 300), Vector2(1320, 650), Vector2(252, 474), Vector2(1380, 530)]:
		draw_circle(pos, 13, Color("#2f5d35"))
		draw_circle(pos + Vector2(-8, -8), 8, Color("#3d7042"))
	for pos in [Vector2(620, 360), Vector2(805, 360), Vector2(486, 584), Vector2(1142, 584), Vector2(312, 698), Vector2(1118, 698)]:
		draw_circle(pos, 4, Color("#2f251b"))
		draw_circle(pos + Vector2(0, -6), 3, Color("#d8b56f"))

func _draw_soft_rect(rect: Rect2, base: Color, alt: Color, alpha := 1.0, detail_count := 12) -> void:
	var base_color := Color(base.r, base.g, base.b, alpha)
	draw_rect(rect, base_color, true)
	for i in range(detail_count):
		var x_unit := fmod(float(i * 73 + 17), 100.0) / 100.0
		var y_unit := fmod(float(i * 47 + 29), 100.0) / 100.0
		var patch_size := Vector2(56.0 + float((i % 4) * 22), 34.0 + float((i % 3) * 14))
		var patch_pos := rect.position + Vector2(x_unit * maxf(0.0, rect.size.x - patch_size.x), y_unit * maxf(0.0, rect.size.y - patch_size.y))
		var patch_color := Color(alt.r, alt.g, alt.b, alpha * 0.22)
		draw_rect(Rect2(patch_pos, patch_size), patch_color, true)

func _draw_planting_bed(rect: Rect2, base := Color("#789969"), alt := Color("#5f844f")) -> void:
	_draw_soft_rect(rect, base, alt, 0.76, 8)
	draw_rect(rect.grow(-5.0), Color(0.15, 0.25, 0.13, 0.18), false, 1.0)
	for i in range(12):
		var p := rect.position + Vector2(12.0 + fmod(float(i * 37), maxf(1.0, rect.size.x - 24.0)), 12.0 + fmod(float(i * 19), maxf(1.0, rect.size.y - 24.0)))
		draw_rect(Rect2(p, Vector2(4, 3)), Color("#d8c174"), true)

func _draw_path_line(a: Vector2, b: Vector2, width: float, base: Color, edge: Color, stone := true) -> void:
	draw_line(a, b, Color(edge.r, edge.g, edge.b, 0.50), width + 12.0, true)
	draw_line(a, b, base, width, true)
	draw_line(a, b, Color(0, 0, 0, 0.16), width + 1.0, true)
	draw_line(a, b, Color(base.r, base.g, base.b, 0.92), width - 4.0, true)
	if not stone:
		return
	var length := a.distance_to(b)
	var steps: int = maxi(1, int(length / 42.0))
	var dir := (b - a).normalized()
	var normal := Vector2(-dir.y, dir.x)
	for i in range(steps):
		var t := float(i) / float(maxi(1, steps - 1))
		var p := a.lerp(b, t)
		var side := (fmod(float(i * 37), 100.0) / 100.0 - 0.5) * width * 0.62
		draw_line(p + normal * side - dir * 8.0, p + normal * side + dir * 10.0, Color(1.0, 0.88, 0.62, 0.13), 1.0)

func _draw_cobbled_world_rect(rect: Rect2, base: Color, alt: Color, count: int) -> void:
	draw_rect(rect.grow(4.0), Color(0, 0, 0, 0.08), true)
	draw_rect(rect, base, true)
	for i in range(count):
		var w := 10.0 + float((i * 5) % 13)
		var h := 6.0 + float((i * 7) % 8)
		var x := rect.position.x + fmod(float(i * 41 + 13), maxf(1.0, rect.size.x - w))
		var y := rect.position.y + fmod(float(i * 29 + 23), maxf(1.0, rect.size.y - h))
		var color := alt.lerp(Color("#beb186"), fmod(float(i * 17), 100.0) / 420.0)
		draw_rect(Rect2(Vector2(x, y), Vector2(w, h)), Color(color.r, color.g, color.b, 0.26), true)
	draw_rect(rect, Color(0, 0, 0, 0.14), false, 1.0)

func _draw_door_step(pos: Vector2) -> void:
	draw_rect(Rect2(pos + Vector2(-13, -8), Vector2(26, 16)), Color("#9d7550"), true)
	draw_rect(Rect2(pos + Vector2(-13, -8), Vector2(26, 16)), Color(0, 0, 0, 0.25), false, 1.0)

func _draw_plank_world_rect(rect: Rect2, base: Color, alt: Color) -> void:
	draw_rect(rect.grow(3.0), Color(0.03, 0.04, 0.03, 0.18), true)
	draw_rect(rect, base, true)
	var vertical_lines := rect.size.x >= rect.size.y
	if vertical_lines:
		for x in range(int(rect.position.x) + 10, int(rect.position.x + rect.size.x), 24):
			draw_line(Vector2(x, rect.position.y + 5), Vector2(x, rect.position.y + rect.size.y - 5), Color(0, 0, 0, 0.18), 1.0)
	else:
		for y in range(int(rect.position.y) + 10, int(rect.position.y + rect.size.y), 24):
			draw_line(Vector2(rect.position.x + 5, y), Vector2(rect.position.x + rect.size.x - 5, y), Color(0, 0, 0, 0.18), 1.0)
	for i in range(12):
		var x_unit := fmod(float(i * 31 + 9), 100.0) / 100.0
		var y_unit := fmod(float(i * 53 + 21), 100.0) / 100.0
		draw_rect(Rect2(rect.position + Vector2(x_unit * rect.size.x, y_unit * rect.size.y), Vector2(30, 4)), Color(alt.r, alt.g, alt.b, 0.20), true)
	draw_rect(rect, Color(0, 0, 0, 0.20), false, 1.0)

func _draw_post_line(a: Vector2, b: Vector2, spacing: float) -> void:
	var distance := a.distance_to(b)
	var steps := int(distance / spacing)
	for i in range(steps + 1):
		var p := a.lerp(b, float(i) / maxf(1.0, float(steps)))
		_draw_post(p)

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
