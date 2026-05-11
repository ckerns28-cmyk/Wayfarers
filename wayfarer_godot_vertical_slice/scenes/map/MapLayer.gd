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
	if NEWPORT_TOWN.G49_STREET_VIGNETTE:
		_draw_g49_ground()
		return

	if NEWPORT_TOWN.G48_PROOF_STREET:
		_draw_g48_ground()
		return

	if NEWPORT_TOWN.G47_CALIBRATION_MODE:
		_draw_g47_ground()
		return

	if NEWPORT_TOWN.G46_PROOF_FRAME:
		_draw_g46_ground()
		return

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
	_draw_planting_bed(Rect2(438, 360, 70, 52), Color("#617d52"), Color("#4f6f49"))
	_draw_planting_bed(Rect2(914, 360, 76, 52), Color("#617d52"), Color("#4f6f49"))
	_draw_planting_bed(Rect2(116, 452, 160, 88), Color("#668051"), Color("#4f6c46"))
	_draw_planting_bed(Rect2(1180, 430, 180, 100), Color("#697755"), Color("#566749"))

func _draw_roads() -> void:
	if NEWPORT_TOWN.G49_STREET_VIGNETTE:
		_draw_g49_street_plane()
		return

	if NEWPORT_TOWN.G48_PROOF_STREET:
		_draw_g48_street_plane()
		return

	if NEWPORT_TOWN.G47_CALIBRATION_MODE:
		_draw_g47_street_planes()
		return

	if NEWPORT_TOWN.G46_PROOF_FRAME:
		_draw_g46_street_plane()
		return

	_draw_cobbled_world_rect(Rect2(545, 318, 345, 130), Color("#918a73"), Color("#6d715f"), 42)
	_draw_cobbled_world_rect(Rect2(286, 526, 850, 56), Color("#8d826a"), Color("#6e6653"), 74)
	draw_line(Vector2(286, 546), Vector2(1136, 546), Color(0.05, 0.06, 0.04, 0.24), 2.0)
	draw_line(Vector2(286, 582), Vector2(1136, 582), Color("#c0ad82"), 1.2)
	_draw_cobbled_world_rect(Rect2(255, 596, 855, 70), Color("#85775b"), Color("#635a45"), 74)
	_draw_cobbled_world_rect(Rect2(594, 636, 260, 42), Color("#8d7958"), Color("#66573f"), 30)
	_draw_path_line(Vector2(250, 572), Vector2(1130, 572), 42.0, Color("#a58a61"), Color("#726049"))
	_draw_path_line(Vector2(280, 625), Vector2(1100, 625), 34.0, Color("#8f7959"), Color("#655841"))
	_draw_path_line(Vector2(645, 350), Vector2(650, 660), 34.0, Color("#9b815d"), Color("#6f5d45"))
	_draw_path_line(Vector2(402, 330), Vector2(1080, 330), 36.0, Color("#9d865f"), Color("#726049"))
	_draw_path_line(Vector2(440, 430), Vector2(986, 430), 24.0, Color("#8d7656"), Color("#65533d"), false)
	_draw_path_line(Vector2(350, 530), Vector2(365, 645), 28.0, Color("#8d7353"), Color("#655541"), false)
	_draw_path_line(Vector2(1210, 350), Vector2(1210, 625), 28.0, Color("#836c4e"), Color("#5d513e"), false)
	_draw_path_line(Vector2(1340, 325), Vector2(1330, 590), 24.0, Color("#80694c"), Color("#5c4e3c"), false)
	_draw_path_line(Vector2(1088, 500), Vector2(1350, 500), 30.0, Color("#907755"), Color("#67563f"))
	_draw_path_line(Vector2(160, 515), Vector2(355, 520), 30.0, Color("#8f7655"), Color("#66553f"))
	_draw_cobbled_world_rect(Rect2(260, 680, 850, 46), Color("#766f57"), Color("#5a5542"), 54)
	for p in [Vector2(352, 573), Vector2(522, 572), Vector2(707, 573), Vector2(899, 573), Vector2(1078, 572), Vector2(678, 376), Vector2(1230, 500), Vector2(735, 628)]:
		_draw_door_step(p)

func _draw_wharf_water() -> void:
	if NEWPORT_TOWN.G49_STREET_VIGNETTE:
		_draw_g49_wharf_water()
		return

	if NEWPORT_TOWN.G48_PROOF_STREET:
		_draw_g48_wharf_water()
		return

	if NEWPORT_TOWN.G47_CALIBRATION_MODE:
		_draw_g47_water_hints()
		return

	if NEWPORT_TOWN.G46_PROOF_FRAME:
		_draw_g46_wharf_hint()
		return

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
	_draw_plank_world_rect(Rect2(600, 672, 270, 34), Color("#8b7a5a"), Color("#665b43"))
	_draw_plank_world_rect(Rect2(270, 720, 150, 140), Color("#7d6547"), Color("#5b4733"))
	_draw_plank_world_rect(Rect2(525, 708, 95, 170), Color("#856948"), Color("#5f4932"))
	_draw_plank_world_rect(Rect2(760, 704, 95, 200), Color("#8c6b47"), Color("#654b34"))
	_draw_plank_world_rect(Rect2(955, 715, 140, 150), Color("#7b6347"), Color("#5a4733"))
	_draw_post_line(Vector2(255, 680), Vector2(1125, 680), 58.0)
	_draw_post_line(Vector2(604, 704), Vector2(866, 704), 44.0)
	_draw_post_line(Vector2(278, 728), Vector2(278, 846), 46.0)
	_draw_post_line(Vector2(410, 728), Vector2(410, 846), 46.0)
	_draw_post_line(Vector2(532, 718), Vector2(532, 866), 46.0)
	_draw_post_line(Vector2(612, 718), Vector2(612, 866), 46.0)
	_draw_post_line(Vector2(766, 714), Vector2(766, 894), 46.0)
	_draw_post_line(Vector2(846, 714), Vector2(846, 894), 46.0)
	_draw_post_line(Vector2(962, 728), Vector2(962, 850), 46.0)
	_draw_post_line(Vector2(1086, 728), Vector2(1086, 850), 46.0)
	for i in range(28):
		var x := 18.0 + float((i * 57) % 1510)
		var y := 760.0 + float((i * 43) % 235)
		draw_line(Vector2(x, y), Vector2(x + 22.0, y - 1.0), Color(0.75, 0.95, 1.0, 0.15), 2.0)
	for p in [Vector2(262, 666), Vector2(424, 690), Vector2(615, 680), Vector2(748, 668), Vector2(914, 680), Vector2(1120, 668), Vector2(1244, 700)]:
		_draw_shore_rocks(p)

func _draw_props() -> void:
	if NEWPORT_TOWN.G49_STREET_VIGNETTE:
		_draw_g49_props()
		return

	if NEWPORT_TOWN.G48_PROOF_STREET:
		_draw_g48_props()
		return

	if NEWPORT_TOWN.G47_CALIBRATION_MODE:
		_draw_g47_props()
		return

	if NEWPORT_TOWN.G46_PROOF_FRAME:
		_draw_g46_props()
		return

	for pos in [Vector2(292, 612), Vector2(340, 628), Vector2(486, 536), Vector2(526, 552), Vector2(690, 536), Vector2(900, 536), Vector2(1038, 612), Vector2(1210, 534), Vector2(1318, 516), Vector2(558, 650), Vector2(840, 730)]:
		_draw_crate_stack(pos)
	for pos in [Vector2(322, 552), Vector2(552, 548), Vector2(760, 548), Vector2(935, 548), Vector2(1008, 634), Vector2(1240, 542), Vector2(814, 666)]:
		_draw_barrels(pos, 3)
	for pos in [Vector2(385, 636), Vector2(590, 640), Vector2(870, 640), Vector2(996, 646), Vector2(1082, 650), Vector2(762, 746), Vector2(672, 690), Vector2(804, 690)]:
		_draw_rope_coil(pos)
	_draw_market_table(Vector2(622, 648))
	_draw_market_table(Vector2(756, 648))
	_draw_fish_rack(Vector2(838, 628))
	_draw_fish_rack(Vector2(310, 652))
	_draw_net_bundle(Vector2(316, 672))
	_draw_net_bundle(Vector2(1004, 672))
	_draw_net_bundle(Vector2(710, 700))
	_draw_rowboat(Vector2(805, 900))
	_draw_rowboat(Vector2(370, 842))
	_draw_rowboat(Vector2(1030, 850))
	_draw_sign_post(Vector2(348, 540), Color("#9d4e38"))
	_draw_sign_post(Vector2(506, 532), Color("#4f6d48"))
	_draw_sign_post(Vector2(922, 532), Color("#90703d"))
	_draw_sign_post(Vector2(720, 626), Color("#7e6240"))
	_draw_clothesline(Vector2(1182, 390), Vector2(1306, 368))
	_draw_fence_line(Vector2(372, 222), Vector2(516, 222), Color("#d9c89c"))
	_draw_fence_line(Vector2(720, 224), Vector2(892, 224), Color("#d9c89c"))
	_draw_fence_line(Vector2(1030, 232), Vector2(1185, 232), Color("#d9c89c"))
	_draw_woodpile(Vector2(154, 488))
	for pos in [Vector2(112, 438), Vector2(1360, 372), Vector2(1168, 300), Vector2(1320, 650), Vector2(252, 474), Vector2(1380, 530), Vector2(430, 356), Vector2(1004, 356)]:
		draw_circle(pos, 13, Color("#2f5d35"))
		draw_circle(pos + Vector2(-8, -8), 8, Color("#3d7042"))
	for pos in [Vector2(620, 360), Vector2(805, 360), Vector2(486, 584), Vector2(1142, 584), Vector2(312, 698), Vector2(1118, 698), Vector2(610, 640), Vector2(856, 640)]:
		draw_circle(pos, 4, Color("#2f251b"))
		draw_circle(pos + Vector2(0, -6), 3, Color("#d8b56f"))

func _draw_g49_ground() -> void:
	_draw_soft_rect(Rect2(Vector2.ZERO, NEWPORT_TOWN.WORLD_SIZE), Color("#435f3f"), Color("#334c35"), 1.0, 34)
	_draw_soft_rect(Rect2(280, 268, 830, 330), Color("#516d49"), Color("#405a3f"), 0.80, 18)
	_draw_soft_rect(Rect2(330, 392, 690, 118), Color("#5e7353"), Color("#4e6648"), 0.72, 10)
	_draw_g49_building_lots()
	_draw_planting_bed(Rect2(300, 430, 72, 58), Color("#637a55"), Color("#4f6848"))
	_draw_planting_bed(Rect2(940, 404, 96, 72), Color("#637a55"), Color("#4f6848"))
	_draw_planting_bed(Rect2(550, 338, 96, 42), Color("#617650"), Color("#4e6648"))

func _draw_g49_building_lots() -> void:
	for raw_config in NEWPORT_TOWN.building_specs():
		var config: Dictionary = raw_config
		if not config.get("proof_street", false) or not config.has("lot_rect"):
			continue
		var origin: Vector2 = config["position"]
		var local_lot: Rect2 = config["lot_rect"]
		var lot := Rect2(origin + local_lot.position, local_lot.size)
		draw_rect(lot.grow(8.0), Color(0.05, 0.07, 0.04, 0.14), true)
		draw_rect(lot, Color("#586c50").lerp(Color("#384c39"), 0.38), true)
		draw_rect(lot, Color(0.04, 0.05, 0.03, 0.24), false, 1.0)
		var frontage_y := lot.position.y + lot.size.y
		draw_line(Vector2(lot.position.x + 8.0, frontage_y), Vector2(lot.position.x + lot.size.x - 8.0, frontage_y), Color("#c2b17b"), 1.4)
		for x in range(int(lot.position.x + 12.0), int(lot.position.x + lot.size.x - 12.0), 34):
			draw_line(Vector2(x, frontage_y - 10.0), Vector2(x + 18.0, frontage_y - 10.0), Color(0.86, 0.80, 0.58, 0.10), 1.0)

func _draw_g49_street_plane() -> void:
	_draw_cobbled_world_rect(Rect2(326, 538, 705, 36), Color("#9b9278"), Color("#746d5a"), 46)
	for p in [Vector2(468, 566), Vector2(658, 562), Vector2(850, 568)]:
		_draw_g47_threshold(p, 58)
	draw_rect(Rect2(326, 574, 705, 7), Color("#3d372d"), true)
	draw_line(Vector2(332, 576), Vector2(1025, 576), Color("#d6c48e"), 1.2)
	_draw_cobbled_world_rect(Rect2(306, 586, 746, 48), Color("#655f52"), Color("#4b473e"), 72)
	draw_line(Vector2(316, 608), Vector2(1044, 604), Color(0.96, 0.86, 0.62, 0.10), 1.0)
	draw_line(Vector2(318, 630), Vector2(1040, 626), Color(0.04, 0.04, 0.03, 0.18), 1.0)
	_draw_plank_world_rect(Rect2(315, 646, 718, 36), Color("#766950"), Color("#5b503d"))
	draw_line(Vector2(320, 644), Vector2(1028, 644), Color(0.04, 0.04, 0.03, 0.30), 2.0)
	for p in [Vector2(344, 646), Vector2(414, 646), Vector2(548, 646), Vector2(692, 646), Vector2(828, 646), Vector2(998, 646)]:
		_draw_post(p)
	for p in [Vector2(372, 574), Vector2(536, 574), Vector2(746, 574), Vector2(918, 574)]:
		draw_circle(p, 3.5, Color("#30271d"))
		draw_circle(p + Vector2(0, -5), 2.8, Color("#d8b56f"))

func _draw_g49_wharf_water() -> void:
	_draw_soft_rect(Rect2(0, 704, NEWPORT_TOWN.WORLD_SIZE.x, 320), Color("#2f7184"), Color("#1f5369"), 1.0, 24)
	draw_colored_polygon(PackedVector2Array([
		Vector2(0, 676), Vector2(310, 672), Vector2(430, 682), Vector2(600, 674),
		Vector2(760, 682), Vector2(930, 674), Vector2(1120, 684), Vector2(1600, 676),
		Vector2(1600, 724), Vector2(0, 724)
	]), Color(0.28, 0.38, 0.32, 0.38))
	_draw_plank_world_rect(Rect2(640, 676, 86, 154), Color("#846849"), Color("#604a35"))
	_draw_post_line(Vector2(318, 684), Vector2(1030, 684), 72.0)
	_draw_post_line(Vector2(648, 686), Vector2(648, 818), 48.0)
	_draw_post_line(Vector2(718, 686), Vector2(718, 818), 48.0)
	for p in [Vector2(324, 678), Vector2(480, 684), Vector2(640, 676), Vector2(820, 682), Vector2(1020, 678)]:
		_draw_shore_rocks(p)
	for i in range(16):
		var x := 72.0 + float((i * 83) % 1420)
		var y := 746.0 + float((i * 39) % 220)
		draw_line(Vector2(x, y), Vector2(x + 22.0, y - 1.0), Color(0.75, 0.95, 1.0, 0.13), 2.0)

func _draw_g49_props() -> void:
	for pos in [Vector2(404, 544), Vector2(512, 548), Vector2(598, 542), Vector2(930, 550)]:
		_draw_crate_stack(pos)
	for pos in [Vector2(438, 548), Vector2(714, 546), Vector2(966, 548)]:
		_draw_barrels(pos, 2)
	for pos in [Vector2(804, 548), Vector2(462, 636), Vector2(918, 636)]:
		_draw_rope_coil(pos)
	_draw_sign_post(Vector2(540, 536), Color("#4f6d48"))
	_draw_sign_post(Vector2(908, 536), Color("#90703d"))
	_draw_market_table(Vector2(742, 636))
	_draw_net_bundle(Vector2(336, 674))
	_draw_net_bundle(Vector2(1000, 676))
	_draw_rowboat(Vector2(684, 852))
	for p in [Vector2(376, 562), Vector2(786, 560), Vector2(1010, 565)]:
		draw_rect(Rect2(p + Vector2(-3, -10), Vector2(6, 20)), Color("#3f2e20"), true)
		draw_circle(p + Vector2(0, -14), 4, Color("#d6b36e"))
	for pos in [Vector2(354, 530), Vector2(988, 528)]:
		draw_rect(Rect2(pos, Vector2(5, 12)), Color("#4a5f39"), true)
		draw_circle(pos + Vector2(2, -2), 5, Color("#6f8b55"))

func _draw_g48_ground() -> void:
	_draw_soft_rect(Rect2(Vector2.ZERO, NEWPORT_TOWN.WORLD_SIZE), Color("#496743"), Color("#3b5538"), 1.0, 36)
	_draw_soft_rect(Rect2(230, 244, 1135, 340), Color("#536e4b"), Color("#465f41"), 0.72, 18)
	_draw_soft_rect(Rect2(260, 330, 1020, 165), Color("#5c7250"), Color("#4b6446"), 0.64, 12)
	for rect in [Rect2(272, 348, 118, 82), Rect2(742, 332, 150, 74), Rect2(1178, 346, 124, 78)]:
		_draw_planting_bed(rect, Color("#617a54"), Color("#4e6a49"))

func _draw_g48_street_plane() -> void:
	_draw_cobbled_world_rect(Rect2(248, 544, 1092, 42), Color("#9a9076"), Color("#746d5a"), 54)
	draw_line(Vector2(252, 548), Vector2(1336, 548), Color(1.0, 0.92, 0.66, 0.13), 1.0)
	draw_rect(Rect2(248, 586, 1092, 8), Color("#3d372d"), true)
	draw_line(Vector2(252, 588), Vector2(1336, 588), Color("#d6c48e"), 1.2)
	_draw_cobbled_world_rect(Rect2(236, 598, 1118, 70), Color("#655f52"), Color("#4b473e"), 86)
	draw_line(Vector2(242, 618), Vector2(1348, 618), Color(0.96, 0.86, 0.62, 0.10), 1.0)
	draw_line(Vector2(242, 650), Vector2(1348, 650), Color(0.04, 0.04, 0.03, 0.18), 1.0)
	_draw_plank_world_rect(Rect2(236, 678, 1118, 38), Color("#766950"), Color("#5b503d"))
	draw_line(Vector2(242, 676), Vector2(1348, 676), Color(0.04, 0.04, 0.03, 0.30), 2.0)
	for p in [Vector2(420, 574), Vector2(646, 575), Vector2(874, 575), Vector2(1098, 574)]:
		_draw_g47_threshold(p, 64)
	for p in [Vector2(296, 678), Vector2(372, 678), Vector2(548, 678), Vector2(725, 678), Vector2(910, 678), Vector2(1088, 678), Vector2(1280, 678)]:
		_draw_post(p)

func _draw_g48_wharf_water() -> void:
	_draw_soft_rect(Rect2(0, 720, NEWPORT_TOWN.WORLD_SIZE.x, 304), Color("#2f7184"), Color("#1f5369"), 1.0, 28)
	draw_colored_polygon(PackedVector2Array([
		Vector2(0, 694), Vector2(238, 690), Vector2(360, 704), Vector2(532, 696),
		Vector2(735, 704), Vector2(930, 696), Vector2(1140, 704), Vector2(1352, 692),
		Vector2(1600, 700), Vector2(1600, 738), Vector2(0, 738)
	]), Color(0.28, 0.38, 0.32, 0.42))
	_draw_plank_world_rect(Rect2(768, 704, 96, 190), Color("#846849"), Color("#604a35"))
	_draw_post_line(Vector2(240, 712), Vector2(1352, 712), 74.0)
	_draw_post_line(Vector2(776, 718), Vector2(776, 884), 52.0)
	_draw_post_line(Vector2(856, 718), Vector2(856, 884), 52.0)
	for p in [Vector2(248, 698), Vector2(410, 704), Vector2(640, 696), Vector2(900, 702), Vector2(1130, 698), Vector2(1345, 696)]:
		_draw_shore_rocks(p)
	for i in range(20):
		var x := 34.0 + float((i * 73) % 1500)
		var y := 748.0 + float((i * 41) % 240)
		draw_line(Vector2(x, y), Vector2(x + 24.0, y - 1.0), Color(0.75, 0.95, 1.0, 0.14), 2.0)

func _draw_g48_props() -> void:
	for pos in [Vector2(332, 548), Vector2(650, 548), Vector2(1128, 548), Vector2(1244, 628)]:
		_draw_crate_stack(pos)
	for pos in [Vector2(384, 552), Vector2(712, 550), Vector2(1166, 548)]:
		_draw_barrels(pos, 2)
	for pos in [Vector2(882, 552), Vector2(1030, 676), Vector2(492, 676)]:
		_draw_rope_coil(pos)
	_draw_sign_post(Vector2(524, 540), Color("#4f6d48"))
	_draw_sign_post(Vector2(944, 540), Color("#90703d"))
	_draw_market_table(Vector2(1208, 618))
	_draw_net_bundle(Vector2(310, 690))
	_draw_net_bundle(Vector2(1320, 692))
	_draw_rowboat(Vector2(820, 906))
	for pos in [Vector2(468, 586), Vector2(632, 586), Vector2(838, 586), Vector2(1048, 586), Vector2(1232, 586)]:
		draw_circle(pos, 4, Color("#2f251b"))
		draw_circle(pos + Vector2(0, -6), 3, Color("#d8b56f"))

func _draw_g47_ground() -> void:
	_draw_soft_rect(Rect2(Vector2.ZERO, NEWPORT_TOWN.WORLD_SIZE), Color("#435f46"), Color("#334d39"), 1.0, 28)
	for variant in NEWPORT_TOWN.calibration_variants():
		var panel: Rect2 = variant["rect"]
		var is_candidate := String(variant["id"]) == "D"
		var panel_base := Color("#536b50") if not is_candidate else Color("#5b7357")
		var panel_alt := Color("#41573f") if not is_candidate else Color("#475f45")
		_draw_soft_rect(panel, panel_base, panel_alt, 0.96, 12)
		draw_rect(panel, Color(0.03, 0.04, 0.03, 0.34), false, 2.0)
		if is_candidate:
			draw_rect(panel.grow(-4.0), Color("#d0ba7a"), false, 2.0)
		_draw_label(String(variant["label"]), panel.position + Vector2(14, 22), 15, Color("#f0e8ce"))
		_draw_label("player scale " + str(variant["player_scale"]), panel.position + Vector2(14, 43), 11, Color("#c7d4c4"))

func _draw_g47_street_planes() -> void:
	_draw_g47_variant_a()
	_draw_g47_variant_b()
	_draw_g47_variant_c()
	_draw_g47_variant_d()

func _draw_g47_variant_a() -> void:
	# A deliberately preserves the failed broad-slab grammar for comparison.
	_draw_cobbled_world_rect(Rect2(98, 298, 555, 100), Color("#a99265"), Color("#746349"), 42)
	draw_line(Vector2(100, 310), Vector2(650, 310), Color(0.04, 0.04, 0.03, 0.22), 2.0)
	draw_line(Vector2(100, 376), Vector2(650, 376), Color("#c1ad7e"), 1.0)

func _draw_g47_variant_b() -> void:
	_draw_cobbled_world_rect(Rect2(894, 300, 540, 34), Color("#978c73"), Color("#6f6654"), 24)
	draw_rect(Rect2(894, 334, 540, 6), Color("#4c4538"), true)
	_draw_cobbled_world_rect(Rect2(882, 342, 566, 62), Color("#766e5c"), Color("#5a5448"), 42)
	for p in [Vector2(1056, 315), Vector2(1256, 315)]:
		_draw_g46_stoop(p)

func _draw_g47_variant_c() -> void:
	_draw_cobbled_world_rect(Rect2(94, 742, 555, 30), Color("#90876f"), Color("#6d6654"), 22)
	draw_rect(Rect2(94, 770, 555, 6), Color("#413b31"), true)
	_draw_cobbled_world_rect(Rect2(70, 778, 605, 72), Color("#6a6252"), Color("#4f4a40"), 48)
	draw_rect(Rect2(70, 832, 605, 62), Color(0.13, 0.11, 0.08, 0.22), true)
	for p in [Vector2(257, 755), Vector2(454, 755)]:
		_draw_g47_threshold(p, 52)

func _draw_g47_variant_d() -> void:
	_draw_cobbled_world_rect(Rect2(890, 736, 560, 26), Color("#9a9076"), Color("#726a57"), 24)
	for p in [Vector2(1062, 748), Vector2(1261, 748)]:
		_draw_g47_threshold(p, 64)
	draw_rect(Rect2(890, 762, 560, 8), Color("#3e382e"), true)
	draw_line(Vector2(894, 764), Vector2(1446, 764), Color("#d7c48f"), 1.2)
	_draw_cobbled_world_rect(Rect2(878, 774, 585, 58), Color("#655f52"), Color("#4c493f"), 50)
	_draw_plank_world_rect(Rect2(878, 838, 585, 34), Color("#766950"), Color("#5b503d"))
	for x in [910, 964, 1030, 1154, 1350, 1424]:
		_draw_post(Vector2(x, 838))

func _draw_g47_threshold(pos: Vector2, width: float) -> void:
	draw_rect(Rect2(pos + Vector2(-width * 0.5, -8), Vector2(width, 24)), Color("#88775b"), true)
	draw_rect(Rect2(pos + Vector2(-width * 0.5, -8), Vector2(width, 24)), Color(0, 0, 0, 0.25), false, 1.0)
	draw_line(pos + Vector2(-width * 0.42, 2), pos + Vector2(width * 0.42, 2), Color("#c6b686"), 1.2)

func _draw_g47_water_hints() -> void:
	for raw_rect in [Rect2(72, 390, 620, 42), Rect2(872, 390, 620, 42), Rect2(72, 842, 620, 52), Rect2(872, 842, 620, 52)]:
		var rect: Rect2 = raw_rect
		_draw_soft_rect(rect, Color("#2f7184"), Color("#1f5369"), 0.82, 7)
		draw_line(rect.position + Vector2(0, 2), rect.position + Vector2(rect.size.x, 2), Color(0.05, 0.10, 0.12, 0.34), 3.0)
		for i in range(6):
			var p: Vector2 = rect.position + Vector2(38 + i * 96, 24 + float((i * 11) % 12))
			draw_line(p, p + Vector2(28, -1), Color(0.78, 0.95, 1.0, 0.14), 2.0)

func _draw_g47_props() -> void:
	_draw_label("A repeats the failing G-4.6 grammar", Vector2(98, 410), 11, Color("#e4b89a"))
	_draw_label("B tests a smaller human figure", Vector2(898, 410), 11, Color("#d9dec1"))
	_draw_label("C tests a lower, tighter street vignette", Vector2(98, 860), 11, Color("#d9dec1"))
	_draw_label("D candidate: stoop + curb + narrower lane", Vector2(898, 878), 11, Color("#f0dc9e"))

	_draw_player_reference(Vector2(360, 352), 1.12, "current player")
	_draw_player_reference(Vector2(1160, 358), 0.76, "smaller player")
	_draw_player_reference(Vector2(360, 812), 0.90, "lower-frame player")
	_draw_label("actual player uses 0.78 scale", Vector2(1160, 884), 10, Color("#c7d4c4"))

	for pos in [Vector2(1038, 742), Vector2(1304, 742), Vector2(1440, 812)]:
		_draw_crate_stack(pos)
	for pos in [Vector2(936, 744), Vector2(1398, 746)]:
		_draw_barrels(pos, 2)
	for pos in [Vector2(990, 826), Vector2(1372, 826)]:
		_draw_rope_coil(pos)
	_draw_sign_post(Vector2(1120, 740), Color("#7a7047"))
	_draw_sign_post(Vector2(1328, 740), Color("#8c6a3f"))

func _draw_player_reference(pos: Vector2, scale: float, label: String) -> void:
	draw_set_transform(pos + Vector2(0, 8 * scale), 0.0, Vector2(1.45 * scale, 0.42 * scale))
	draw_circle(Vector2.ZERO, 10.0, Color(0, 0, 0, 0.22))
	draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
	draw_circle(pos + Vector2(0, -31 * scale), 12.0 * scale, Color("#f3d6a0"))
	draw_rect(Rect2(pos + Vector2(-9, -20) * scale, Vector2(18, 26) * scale), Color("#4a6fa3"), true)
	draw_rect(Rect2(pos + Vector2(-11, 4) * scale, Vector2(22, 8) * scale), Color("#2f4769"), true)
	draw_line(pos + Vector2(-15, -10) * scale, pos + Vector2(15, -10) * scale, Color("#d2b978"), maxf(1.0, 3.0 * scale))
	_draw_label(label, pos + Vector2(-38, 30), 9, Color("#d8e0ce"))

func _draw_label(text: String, pos: Vector2, size: int, color: Color) -> void:
	var font := ThemeDB.fallback_font
	if font:
		draw_string(font, pos + Vector2(1, 1), text, HORIZONTAL_ALIGNMENT_LEFT, -1, size, Color(0, 0, 0, 0.55))
		draw_string(font, pos, text, HORIZONTAL_ALIGNMENT_LEFT, -1, size, color)

func _draw_g46_ground() -> void:
	var world_rect := Rect2(Vector2.ZERO, NEWPORT_TOWN.WORLD_SIZE)
	_draw_soft_rect(world_rect, Color("#506c4c"), Color("#435f42"), 1.0, 36)
	_draw_soft_rect(Rect2(318, 330, 842, 370), Color("#526d4d"), Color("#435e42"), 0.72, 18)
	_draw_soft_rect(Rect2(350, 424, 760, 92), Color("#5d7356"), Color("#4d684a"), 0.74, 10)
	draw_rect(Rect2(350, 508, 760, 10), Color(0.05, 0.08, 0.05, 0.18), true)
	for rect in [Rect2(400, 385, 96, 82), Rect2(670, 386, 126, 80), Rect2(870, 382, 118, 84)]:
		_draw_planting_bed(rect, Color("#617b55"), Color("#4f6a4a"))

func _draw_g46_street_plane() -> void:
	_draw_cobbled_world_rect(Rect2(346, 510, 778, 38), Color("#9b9278"), Color("#756d58"), 34)
	draw_rect(Rect2(346, 546, 778, 7), Color("#4a4437"), true)
	draw_line(Vector2(350, 548), Vector2(1120, 548), Color("#d0c090"), 1.4)

	_draw_cobbled_world_rect(Rect2(328, 553, 814, 68), Color("#766e5b"), Color("#5b5547"), 58)
	draw_line(Vector2(332, 554), Vector2(1138, 554), Color(0.04, 0.04, 0.03, 0.28), 2.0)
	draw_line(Vector2(332, 618), Vector2(1138, 618), Color("#b7a67e"), 1.3)

	_draw_plank_world_rect(Rect2(340, 630, 790, 34), Color("#76684f"), Color("#5a4f3b"))
	draw_line(Vector2(344, 628), Vector2(1128, 628), Color(0.04, 0.04, 0.03, 0.30), 2.0)

	for p in [Vector2(550, 523), Vector2(736, 523), Vector2(932, 523)]:
		_draw_g46_stoop(p)

	for x in [390, 454, 642, 836, 1032, 1100]:
		_draw_post(Vector2(x, 628))

func _draw_g46_wharf_hint() -> void:
	_draw_soft_rect(Rect2(0, 704, NEWPORT_TOWN.WORLD_SIZE.x, 320), Color("#2f7184"), Color("#1f5369"), 1.0, 24)
	draw_colored_polygon(PackedVector2Array([
		Vector2(0, 676), Vector2(350, 672), Vector2(470, 688), Vector2(680, 674),
		Vector2(850, 688), Vector2(1110, 672), Vector2(1600, 682), Vector2(1600, 724),
		Vector2(0, 724)
	]), Color(0.28, 0.38, 0.32, 0.44))
	_draw_plank_world_rect(Rect2(686, 660, 100, 178), Color("#836848"), Color("#5f4a34"))
	_draw_post_line(Vector2(346, 668), Vector2(1122, 668), 64.0)
	for p in [Vector2(352, 676), Vector2(510, 682), Vector2(720, 674), Vector2(940, 682), Vector2(1120, 674)]:
		_draw_shore_rocks(p)
	for i in range(14):
		var x := 80.0 + float((i * 113) % 1420)
		var y := 760.0 + float((i * 47) % 210)
		draw_line(Vector2(x, y), Vector2(x + 22.0, y - 1.0), Color(0.75, 0.95, 1.0, 0.13), 2.0)

func _draw_g46_props() -> void:
	_draw_barrels(Vector2(478, 526), 2)
	_draw_crate_stack(Vector2(998, 526))
	_draw_rope_coil(Vector2(414, 624))
	_draw_rope_coil(Vector2(1054, 624))
	_draw_sign_post(Vector2(620, 523), Color("#6b7d52"))
	_draw_sign_post(Vector2(864, 522), Color("#8c6a3f"))
	for pos in [Vector2(394, 606), Vector2(1072, 606), Vector2(650, 622), Vector2(836, 622)]:
		draw_circle(pos, 4, Color("#2f251b"))
		draw_circle(pos + Vector2(0, -6), 3, Color("#d8b56f"))

func _draw_g46_stoop(pos: Vector2) -> void:
	draw_rect(Rect2(pos + Vector2(-28, -10), Vector2(56, 25)), Color("#8f8064"), true)
	draw_rect(Rect2(pos + Vector2(-28, -10), Vector2(56, 25)), Color(0, 0, 0, 0.26), false, 1.0)
	draw_line(pos + Vector2(-24, 2), pos + Vector2(24, 2), Color("#c8b98a"), 1.2)

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
