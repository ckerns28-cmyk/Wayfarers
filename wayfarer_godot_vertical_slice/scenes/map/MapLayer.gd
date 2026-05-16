extends Node2D

@export_enum("ground", "roads", "wharf_water", "props") var layer_id := "ground"

const NEWPORT_TOWN := preload("res://scripts/NewportTownBlueprint.gd")
const TILE := NEWPORT_TOWN.TILE
const MAP_W := NEWPORT_TOWN.MAP_TILES.x
const MAP_H := NEWPORT_TOWN.MAP_TILES.y
const NEWPORT_SURFACE_KIT_VERSION := "G-4.16"
const NEWPORT_HERO_ATLAS_VERSION := "G-4.18"
const NEWPORT_HERO_ATLAS_PATH := "res://art_pipeline/newport/atlases/newport_hero_street_atlas_v1.png"
const NEWPORT_GREEN_ORIGIN_VERSION := "G-4.18B"
const NEWPORT_GREEN_ORIGIN_ATLAS_PATH := "res://art_pipeline/newport_green_origin/atlases/newport_green_origin_dock_factory_v1.png"
const G418D1_M01B_PROOF_PATH := "res://art_pipeline/newport_green_origin/method_bakeoff/generated/method_01b_manual_paintover_proof.png"
const G418D3_PIXEL_ATELIER_ASSET_PATH := "res://art_pipeline/newport_green_origin/method_bakeoff/generated/g418d3_dockside_rope_crate_barrel_cluster.png"
const NEWPORT_SURFACE_KIT_MATERIALS := [
	"commercial_street",
	"curb_sidewalk",
	"dirt_path",
	"grass_road_transition",
	"dock_plank",
	"pier_edge",
	"building_base_shadow",
	"service_lane",
]
const NEWPORT_HERO_ATLAS_MATERIALS := [
	"commercial_cobble_long_a",
	"commercial_cobble_patch_b",
	"commercial_cobble_patch_c",
	"curb_sidewalk_stoop_strip",
	"curb_sidewalk_broken_edge",
	"building_contact_shadow_strip",
	"dirt_wear_transition",
	"grass_edge_north",
	"grass_cobble_feather",
	"dock_market_transition",
	"dock_pier_vertical",
	"dock_edge_feather",
	"pier_shadow_post_strip",
	"crate_barrel_table_cluster",
	"fence_sign_market_cluster",
	"small_crate_barrel_cluster",
	"market_sign_cluster",
	"wharf_crate_pile_cluster",
	"chandlery_base_cluster",
]
const NEWPORT_GREEN_ORIGIN_MATERIALS := [
	"green_dock_plank_strip",
	"green_dock_plank_patch",
	"green_dock_edge_shadow",
	"green_pier_post_pair",
	"green_rope_coil_small",
	"green_plank_contact_shadow",
]
const NEWPORT_HERO_ATLAS_REGIONS := {
	"commercial_cobble_long_a": Rect2(0, 0, 320, 96),
	"commercial_cobble_patch_b": Rect2(0, 104, 220, 72),
	"commercial_cobble_patch_c": Rect2(0, 184, 180, 64),
	"curb_sidewalk_stoop_strip": Rect2(0, 256, 320, 72),
	"curb_sidewalk_broken_edge": Rect2(0, 336, 320, 56),
	"building_contact_shadow_strip": Rect2(0, 400, 320, 48),
	"dirt_wear_transition": Rect2(0, 456, 320, 64),
	"grass_edge_north": Rect2(0, 528, 320, 64),
	"grass_cobble_feather": Rect2(0, 600, 320, 56),
	"dock_market_transition": Rect2(0, 664, 320, 96),
	"dock_pier_vertical": Rect2(336, 0, 96, 224),
	"dock_edge_feather": Rect2(448, 0, 320, 64),
	"pier_shadow_post_strip": Rect2(448, 72, 224, 56),
	"crate_barrel_table_cluster": Rect2(448, 144, 184, 136),
	"fence_sign_market_cluster": Rect2(648, 144, 184, 136),
	"small_crate_barrel_cluster": Rect2(448, 296, 160, 112),
	"market_sign_cluster": Rect2(624, 296, 160, 112),
	"wharf_crate_pile_cluster": Rect2(448, 424, 220, 146),
	"chandlery_base_cluster": Rect2(684, 424, 220, 146),
}
const NEWPORT_GREEN_ORIGIN_ATLAS_REGIONS := {
	"green_dock_plank_strip": Rect2(0, 0, 320, 72),
	"green_dock_plank_patch": Rect2(0, 84, 180, 72),
	"green_dock_edge_shadow": Rect2(0, 168, 320, 42),
	"green_pier_post_pair": Rect2(336, 0, 112, 92),
	"green_rope_coil_small": Rect2(336, 104, 80, 56),
	"green_plank_contact_shadow": Rect2(336, 172, 144, 36),
}
const G417_HERO_PROP_REPLACEMENT_RECT := Rect2(240, 500, 1040, 280)

var _newport_hero_atlas: Texture2D
var _newport_green_origin_atlas: Texture2D
var _g418d1_m01b_proof: Texture2D
var _g418d3_pixel_atelier_asset: Texture2D
var _green_origin_lab_enabled := false

func _ready() -> void:
	_newport_hero_atlas = ResourceLoader.load(NEWPORT_HERO_ATLAS_PATH, "Texture2D") as Texture2D
	if _newport_hero_atlas == null:
		push_error("Failed to load Newport hero atlas: " + NEWPORT_HERO_ATLAS_PATH)
	_newport_green_origin_atlas = ResourceLoader.load(NEWPORT_GREEN_ORIGIN_ATLAS_PATH, "Texture2D") as Texture2D
	if _newport_green_origin_atlas == null:
		push_error("Failed to load Newport green-origin atlas: " + NEWPORT_GREEN_ORIGIN_ATLAS_PATH)
	_g418d1_m01b_proof = ResourceLoader.load(G418D1_M01B_PROOF_PATH, "Texture2D") as Texture2D
	if _g418d1_m01b_proof == null:
		push_warning("Failed to load G-4.18D.1 M01B lab proof: " + G418D1_M01B_PROOF_PATH)
	_g418d3_pixel_atelier_asset = ResourceLoader.load(G418D3_PIXEL_ATELIER_ASSET_PATH, "Texture2D") as Texture2D
	if _g418d3_pixel_atelier_asset == null:
		push_warning("Failed to load G-4.18D.3 pixel atelier asset: " + G418D3_PIXEL_ATELIER_ASSET_PATH)
	queue_redraw()

func newport_surface_kit_version() -> String:
	return NEWPORT_SURFACE_KIT_VERSION

func newport_surface_kit_materials() -> Array:
	return NEWPORT_SURFACE_KIT_MATERIALS.duplicate()

func newport_hero_atlas_version() -> String:
	return NEWPORT_HERO_ATLAS_VERSION

func newport_hero_atlas_materials() -> Array:
	return NEWPORT_HERO_ATLAS_MATERIALS.duplicate()

func newport_green_origin_version() -> String:
	return NEWPORT_GREEN_ORIGIN_VERSION

func newport_green_origin_materials() -> Array:
	return NEWPORT_GREEN_ORIGIN_MATERIALS.duplicate()

func set_green_origin_lab_mode(enabled: bool) -> void:
	_green_origin_lab_enabled = enabled
	queue_redraw()

func is_green_origin_lab_mode() -> bool:
	return _green_origin_lab_enabled

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

func _draw_hero_atlas_piece(region_id: String, dest: Rect2, alpha := 1.0) -> void:
	if _newport_hero_atlas == null:
		return
	if not NEWPORT_HERO_ATLAS_REGIONS.has(region_id):
		push_error("Unknown Newport hero atlas region: " + region_id)
		return
	draw_texture_rect_region(_newport_hero_atlas, dest, NEWPORT_HERO_ATLAS_REGIONS[region_id], Color(1, 1, 1, alpha), false, true)

func _draw_hero_atlas_tiled(region_id: String, dest: Rect2, alpha := 1.0, scale := 1.0) -> void:
	if _newport_hero_atlas == null:
		return
	if not NEWPORT_HERO_ATLAS_REGIONS.has(region_id):
		push_error("Unknown Newport hero atlas region: " + region_id)
		return
	var source: Rect2 = NEWPORT_HERO_ATLAS_REGIONS[region_id]
	var tile_size := source.size * scale
	var y := dest.position.y
	while y < dest.end.y:
		var x := dest.position.x
		while x < dest.end.x:
			var size := Vector2(min(tile_size.x, dest.end.x - x), min(tile_size.y, dest.end.y - y))
			draw_texture_rect_region(_newport_hero_atlas, Rect2(Vector2(x, y), size), source, Color(1, 1, 1, alpha), false, true)
			x += tile_size.x
		y += tile_size.y

func _draw_green_origin_piece(region_id: String, dest: Rect2, alpha := 1.0) -> void:
	if _newport_green_origin_atlas == null:
		return
	if not NEWPORT_GREEN_ORIGIN_ATLAS_REGIONS.has(region_id):
		push_error("Unknown Newport green-origin atlas region: " + region_id)
		return
	draw_texture_rect_region(_newport_green_origin_atlas, dest, NEWPORT_GREEN_ORIGIN_ATLAS_REGIONS[region_id], Color(1, 1, 1, alpha), false, true)

func _is_g417_hero_prop_placeholder(pos: Vector2) -> bool:
	return G417_HERO_PROP_REPLACEMENT_RECT.has_point(pos)

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
	if NEWPORT_TOWN.G410_STARTER_HARBOR_TOWN:
		_draw_g410_ground()
		return

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
	if NEWPORT_TOWN.G410_STARTER_HARBOR_TOWN:
		_draw_g410_street_plan()
		return

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
	if NEWPORT_TOWN.G410_STARTER_HARBOR_TOWN:
		_draw_g410_wharf_water()
		return

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
	if NEWPORT_TOWN.G410_STARTER_HARBOR_TOWN:
		_draw_g410_props()
		return

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

func _draw_g410_ground() -> void:
	_draw_newport_grass_rect(Rect2(Vector2.ZERO, NEWPORT_TOWN.WORLD_SIZE), Color("#4a6a42"), Color("#314d35"), 1.0, 64)
	_draw_newport_grass_rect(Rect2(150, 160, 1240, 270), Color("#647f57"), Color("#496744"), 0.76, 42)
	_draw_newport_grass_rect(Rect2(208, 372, 1192, 224), Color("#5b7251"), Color("#405c41"), 0.72, 38)
	_draw_newport_grass_rect(Rect2(198, 606, 1190, 170), Color("#5d6650"), Color("#454f3d"), 0.50, 28)
	_draw_newport_grass_rect(Rect2(42, 392, 178, 178), Color("#526b49"), Color("#36543a"), 0.42, 18)
	_draw_newport_grass_rect(Rect2(1384, 398, 98, 172), Color("#536b4a"), Color("#36543a"), 0.40, 14)
	for rect in [Rect2(184, 206, 174, 86), Rect2(426, 176, 256, 92), Rect2(742, 186, 218, 82), Rect2(1044, 174, 240, 98), Rect2(1288, 314, 180, 96)]:
		_draw_newport_lot_variation(rect, Color("#4f6849"), Color("#40583e"), 0.12, "distant")
	_draw_g410_background_depth()
	_draw_g410_lot_plan()
	_draw_g415_parcel_grounding()
	_draw_planting_bed(Rect2(190, 260, 112, 52), Color("#718c62"), Color("#5c7a53"))
	_draw_planting_bed(Rect2(844, 238, 134, 58), Color("#718c62"), Color("#5c7a53"))
	_draw_planting_bed(Rect2(1122, 248, 122, 54), Color("#718c62"), Color("#5c7a53"))
	_draw_planting_bed(Rect2(1210, 338, 106, 46), Color("#647d55"), Color("#4e6b49"))
	_draw_shrub_cluster(Vector2(248, 272))
	_draw_shrub_cluster(Vector2(905, 260))
	_draw_shrub_cluster(Vector2(1180, 270))
	_draw_low_wall(Vector2(790, 420), Vector2(990, 414), Color("#68715b", 0.42))
	_draw_low_wall(Vector2(1100, 424), Vector2(1280, 418), Color("#68715b", 0.38))

func _draw_g410_lot_plan() -> void:
	for raw_lot in NEWPORT_TOWN.starter_lot_specs():
		var lot: Dictionary = raw_lot
		var rect: Rect2i = lot["rect"]
		var world_rect := _tile_rect(rect.position.x, rect.position.y, rect.size.x, rect.size.y).grow(-5.0)
		if lot.get("status", "") == "planned":
			_draw_g410_planned_lot(world_rect, String(lot.get("district", "")), String(lot.get("role", "")))
		else:
			_draw_g410_active_lot(world_rect, String(lot.get("district", "")), String(lot.get("role", "")))

func _draw_g410_active_lot(rect: Rect2, district: String, role := "") -> void:
	var base := Color("#5f7554")
	var alt := Color("#4c6649")
	var alpha := 0.12
	if role.begins_with("waterline_"):
		base = Color("#2f7184")
		alt = Color("#1f5369")
		alpha = 0.06
	elif district == "working_wharf":
		base = Color("#6b6049")
		alt = Color("#534936")
		alpha = 0.08
	elif district == "harborfront_commercial":
		base = Color("#647157")
		alt = Color("#4d5f49")
		alpha = 0.10
	elif district == "inland_residential_civic":
		base = Color("#69835d")
		alt = Color("#54724f")
		alpha = 0.10
	elif district == "support_lane":
		base = Color("#5d724f")
		alt = Color("#486442")
		alpha = 0.09
	_draw_newport_lot_variation(rect, base, alt, alpha, district)
	if district == "harborfront_commercial":
		var frontage := Rect2(rect.position.x + 8.0, rect.position.y + rect.size.y - 24.0, maxf(0.0, rect.size.x - 16.0), 18.0)
		_draw_newport_sidewalk_panel(frontage, "frontage", 0.38)
	elif district == "inland_residential_civic":
		var yard := rect.grow(-14.0)
		_draw_newport_grass_rect(yard, Color("#789365"), Color("#56784f"), 0.14, 8)
		_draw_newport_dirt_path(yard.position + Vector2(yard.size.x * 0.5, yard.size.y - 6.0), rect.position + Vector2(rect.size.x * 0.5, rect.size.y + 8.0), 12.0, true)
		_draw_shrub_cluster(yard.position + Vector2(18.0, yard.size.y - 18.0))
		_draw_shrub_cluster(yard.position + Vector2(yard.size.x - 22.0, yard.size.y - 20.0))
		_draw_fence_line(rect.position + Vector2(10.0, rect.size.y - 10.0), rect.position + Vector2(rect.size.x - 10.0, rect.size.y - 8.0), Color("#c9b781", 0.42))
	elif district == "support_lane":
		var work_yard := Rect2(rect.position + Vector2(10.0, rect.size.y - 34.0), Vector2(maxf(0.0, rect.size.x - 20.0), 24.0))
		_draw_newport_service_lane_rect(work_yard, 0.34)
	elif role.begins_with("waterline_"):
		draw_line(rect.position + Vector2(10.0, rect.size.y - 12.0), rect.position + Vector2(rect.size.x - 10.0, rect.size.y - 8.0), Color(0.75, 0.95, 1.0, 0.08), 1.0)

func _draw_g410_planned_lot(rect: Rect2, district: String, role: String) -> void:
	var fill := Color("#53624e", 0.08)
	if district == "working_wharf":
		fill = Color("#66563f", 0.08)
	elif district == "harborfront_commercial":
		fill = Color("#5c6652", 0.075)
	elif district == "support_lane":
		fill = Color("#52634d", 0.07)
	_draw_newport_lot_variation(rect, Color(fill.r, fill.g, fill.b), Color(fill.r * 0.78, fill.g * 0.82, fill.b * 0.78), fill.a, district)
	var inset := rect.grow(-14.0)
	_draw_surface_speckles(inset, 6, Color(0.09, 0.075, 0.045, 0.045), Vector2(22, 3))
	if role.contains("home") or role.contains("residence"):
		_draw_fence_line(rect.position + Vector2(6, rect.size.y - 8), rect.position + Vector2(rect.size.x - 8, rect.size.y - 7), Color("#c9b781", 0.28))
	elif role.contains("dock") or role.contains("chandler"):
		_draw_post_line(rect.position + Vector2(14, rect.size.y - 9), rect.position + Vector2(rect.size.x - 14, rect.size.y - 8), 42.0)
	else:
		for x in range(int(inset.position.x + 16.0), int(inset.position.x + inset.size.x - 10.0), 34):
			draw_line(Vector2(x, inset.position.y + 8), Vector2(x + 12, inset.position.y + 8), Color(0.94, 0.86, 0.61, 0.045), 1.0)
	_draw_shrub_cluster(rect.position + Vector2(rect.size.x - 20.0, rect.size.y - 16.0), 0.55)

func _draw_g415_parcel_grounding() -> void:
	var rules: Dictionary = NEWPORT_TOWN.g415_layout_rules()
	for raw_id in rules.keys():
		var rule: Dictionary = rules[raw_id]
		var band := String(rule.get("district_band", ""))
		if band == "dock":
			continue
		_draw_g415_ground_pad(rule)
		_draw_g415_prop_band(rule)
		if ["commercial", "market"].has(band):
			_draw_g415_commercial_gutters(rule)

func _draw_g415_dock_grounding() -> void:
	var rules: Dictionary = NEWPORT_TOWN.g415_layout_rules()
	for raw_id in rules.keys():
		var rule: Dictionary = rules[raw_id]
		if String(rule.get("district_band", "")) != "dock":
			continue
		_draw_g415_ground_pad(rule)
		_draw_g415_prop_band(rule)

func _draw_g415_ground_pad(rule: Dictionary) -> void:
	var pad: Dictionary = rule.get("ground_pad", {})
	var rect: Rect2 = pad.get("rect", Rect2())
	if rect.size.x <= 0.0 or rect.size.y <= 0.0:
		return

	match String(pad.get("type", "")):
		"commercial_stone", "rowhouse_stone", "shop_stone":
			_draw_newport_sidewalk_panel(rect, "commercial", 0.58)
		"market_stone":
			_draw_newport_sidewalk_panel(rect, "market", 0.62)
		"civic_stone":
			_draw_newport_sidewalk_panel(rect, "civic", 0.60)
		"civic_green":
			_draw_newport_grass_rect(rect, Color("#6d865f"), Color("#4e6b4b"), 0.34, 16)
			_draw_newport_grass_transition(Rect2(rect.position.x, rect.end.y - 16.0, rect.size.x, 16.0), "south", 0.24)
			_draw_shrub_cluster(rect.position + Vector2(20.0, rect.size.y - 20.0), 0.55)
			_draw_shrub_cluster(rect.position + Vector2(rect.size.x - 22.0, rect.size.y - 20.0), 0.55)
		"residential_yard":
			_draw_newport_grass_rect(rect, Color("#6c875e"), Color("#4f6e4c"), 0.30, 14)
			_draw_newport_grass_transition(Rect2(rect.position.x, rect.end.y - 14.0, rect.size.x, 14.0), "south", 0.20)
			_draw_shrub_cluster(rect.position + Vector2(18.0, rect.size.y - 18.0), 0.50)
			_draw_shrub_cluster(rect.position + Vector2(rect.size.x - 22.0, rect.size.y - 20.0), 0.50)
		"support_yard":
			_draw_newport_service_lane_rect(rect, 0.40)
		"dock_plank":
			_draw_newport_dock_planks(rect, 20)
		_:
			_draw_newport_lot_variation(rect, Color("#6a765d"), Color("#4f6048"), 0.12, "default")

func _draw_g415_prop_band(rule: Dictionary) -> void:
	var rect: Rect2 = rule.get("prop_band", Rect2())
	if rect.size.x <= 0.0 or rect.size.y <= 0.0:
		return

	var band := String(rule.get("district_band", ""))
	var fill := Color(0.12, 0.09, 0.05, 0.11)
	if band == "residential" or band == "civic":
		fill = Color(0.11, 0.16, 0.08, 0.08)
	elif band == "dock":
		fill = Color(0.10, 0.07, 0.04, 0.14)
	elif band == "market":
		fill = Color(0.13, 0.09, 0.045, 0.13)
	_draw_surface_speckles(rect, maxi(5, int(rect.size.x / 18.0)), fill, Vector2(18, 4))
	for x in range(int(rect.position.x + 8.0), int(rect.end.x - 8.0), 34):
		var y := rect.position.y + 5.0 + fmod(float(x * 3), maxf(1.0, rect.size.y - 10.0))
		draw_line(Vector2(x, y), Vector2(x + 13.0, y - 1.0), Color(0.94, 0.82, 0.55, fill.a * 0.55), 1.0)

func _draw_g415_commercial_gutters(rule: Dictionary) -> void:
	var pad: Dictionary = rule.get("ground_pad", {})
	var rect: Rect2 = pad.get("rect", Rect2())
	if rect.size.x <= 0.0 or rect.size.y <= 0.0:
		return
	var side_gap := float(rule.get("side_gap_minimum", 0.0))
	if side_gap < 10.0:
		return
	var gutter_alpha: float = clamp(side_gap / 80.0, 0.10, 0.28)
	draw_rect(Rect2(rect.position.x - 3.0, rect.position.y + 8.0, 4.0, rect.size.y - 14.0), Color(0.06, 0.06, 0.045, gutter_alpha), true)
	draw_rect(Rect2(rect.end.x - 1.0, rect.position.y + 8.0, 4.0, rect.size.y - 14.0), Color(0.06, 0.06, 0.045, gutter_alpha * 0.84), true)

func _draw_g415_lane_connections() -> void:
	var rules: Dictionary = NEWPORT_TOWN.g415_layout_rules()
	for raw_id in rules.keys():
		var id := String(raw_id)
		var rule: Dictionary = rules[id]
		var band := String(rule.get("district_band", ""))
		if band == "dock":
			continue

		var target: Vector2 = rule.get("door_path_target", Vector2.ZERO)
		var frontage_y := float(rule.get("frontage_line_y", target.y))
		if ["commercial", "market"].has(band):
			var threshold_center := Vector2(target.x, frontage_y)
			_draw_g47_threshold(threshold_center, _g415_threshold_width_for(id, band))
			_draw_newport_dirt_path(threshold_center + Vector2(0.0, 12.0), target, 14.0, true)
			continue

		var pad: Dictionary = rule.get("ground_pad", {})
		var rect: Rect2 = pad.get("rect", Rect2())
		if rect.size.x <= 0.0 or rect.size.y <= 0.0:
			continue
		var path_start := Vector2(clamp(target.x, rect.position.x + 18.0, rect.end.x - 18.0), rect.end.y - 8.0)
		var path_width := 14.0 if band == "civic" else 11.0
		_draw_newport_dirt_path(path_start, target, path_width, band == "civic")
		_draw_door_step(path_start)

func _g415_threshold_width_for(id: String, band: String) -> float:
	match id:
		"b_counting_house":
			return 58.0
		"b_inn_tavern", "b_market_shed":
			return 56.0
		"b_clerk_townhouse", "b_printer_rowhouse":
			return 38.0
		_:
			return 46.0 if band == "commercial" else 52.0

func _draw_g410_street_plan() -> void:
	_draw_newport_dirt_path(Vector2(392, 414), Vector2(384, 680), 30.0, false)
	_draw_newport_service_lane_path(Vector2(676, 350), Vector2(664, 682), 34.0)
	_draw_newport_dirt_path(Vector2(1110, 420), Vector2(1090, 690), 30.0, false)
	_draw_newport_service_lane_path(Vector2(318, 430), Vector2(1268, 424), 34.0)
	_draw_newport_dirt_path(Vector2(438, 484), Vector2(1140, 476), 22.0, false)

	for rect in [Rect2(232, 504, 312, 34), Rect2(544, 512, 286, 30), Rect2(818, 506, 284, 36), Rect2(1090, 516, 258, 30)]:
		_draw_newport_commercial_street(rect, 38, 0.62)
	draw_polyline(PackedVector2Array([
		Vector2(240, 512), Vector2(466, 506), Vector2(612, 516), Vector2(824, 510),
		Vector2(1032, 516), Vector2(1338, 520)
	]), Color(1.0, 0.93, 0.68, 0.10), 1.0)
	_draw_street_wear(Rect2(232, 504, 1116, 42), 34)

	var main_street_poly := PackedVector2Array([
		Vector2(232, 544), Vector2(546, 548), Vector2(826, 542), Vector2(1090, 550),
		Vector2(1354, 546), Vector2(1354, 634), Vector2(1092, 626), Vector2(842, 632),
		Vector2(560, 624), Vector2(226, 632)
	])
	draw_colored_polygon(main_street_poly, Color("#5f594c"))
	_draw_newport_grass_transition(Rect2(218, 532, 1148, 18), "north", 0.18)
	_draw_newport_sidewalk_panel(Rect2(218, 540, 1148, 20), "curb", 0.62)
	_draw_newport_commercial_street(Rect2(226, 558, 1134, 68), 168, 0.98)
	_draw_newport_sidewalk_panel(Rect2(226, 624, 1130, 18), "curb_shadow", 0.46)
	draw_polyline(PackedVector2Array([
		Vector2(238, 548), Vector2(544, 550), Vector2(824, 544), Vector2(1090, 552),
		Vector2(1348, 548)
	]), Color("#d6c48e", 0.62), 1.4)
	draw_polyline(PackedVector2Array([
		Vector2(238, 626), Vector2(560, 622), Vector2(842, 628), Vector2(1090, 622),
		Vector2(1348, 626)
	]), Color(0.04, 0.04, 0.03, 0.20), 1.0)
	for rect in [Rect2(368, 586, 120, 18), Rect2(720, 570, 92, 16), Rect2(988, 592, 150, 18), Rect2(1190, 562, 72, 14)]:
		_draw_newport_sidewalk_panel(rect, "street_patch", 0.34)
	_draw_street_wear(Rect2(226, 552, 1134, 78), 64)
	for p in [Vector2(380, 548), Vector2(664, 542), Vector2(1088, 550)]:
		_draw_edge_grime(p, 112.0)
	_draw_g415_lane_connections()

	_draw_newport_commercial_street(Rect2(232, 642, 1116, 58), 118, 0.80)
	draw_polyline(PackedVector2Array([
		Vector2(240, 644), Vector2(530, 640), Vector2(812, 648), Vector2(1084, 642),
		Vector2(1338, 646)
	]), Color("#b9aa80", 0.26), 1.2)
	_draw_street_wear(Rect2(232, 642, 1116, 58), 48)
	_draw_newport_dock_planks(Rect2(238, 696, 1112, 46), 74)
	draw_line(Vector2(248, 696), Vector2(1338, 696), Color(0.04, 0.04, 0.03, 0.32), 2.0)
	for p in [Vector2(284, 696), Vector2(392, 696), Vector2(548, 696), Vector2(692, 696), Vector2(824, 696), Vector2(1008, 696), Vector2(1180, 696), Vector2(1318, 696)]:
		_draw_post(p)
	_draw_g417_hero_street_atlas_proof()
	for p in [Vector2(332, 580), Vector2(520, 582), Vector2(746, 578), Vector2(930, 584), Vector2(1136, 582), Vector2(662, 420), Vector2(1094, 504), Vector2(390, 506), Vector2(1250, 580)]:
		draw_circle(p, 4, Color("#2f251b"))
		draw_circle(p + Vector2(0, -6), 3, Color("#d8b56f"))

func _draw_g417_hero_street_atlas_proof() -> void:
	if _newport_hero_atlas == null:
		return
	_draw_hero_atlas_piece("grass_edge_north", Rect2(268, 504, 262, 38), 0.26)
	_draw_hero_atlas_piece("grass_edge_north", Rect2(622, 498, 316, 42), 0.22)
	_draw_hero_atlas_piece("grass_edge_north", Rect2(964, 506, 226, 36), 0.18)
	_draw_hero_atlas_piece("grass_cobble_feather", Rect2(248, 530, 286, 40), 0.24)
	_draw_hero_atlas_piece("grass_cobble_feather", Rect2(612, 526, 320, 38), 0.22)
	_draw_hero_atlas_piece("grass_cobble_feather", Rect2(930, 532, 274, 36), 0.18)
	_draw_hero_atlas_tiled("building_contact_shadow_strip", Rect2(242, 536, 906, 30), 0.42, 1.0)
	_draw_hero_atlas_piece("curb_sidewalk_stoop_strip", Rect2(266, 552, 286, 42), 0.32)
	_draw_hero_atlas_piece("curb_sidewalk_stoop_strip", Rect2(574, 548, 304, 44), 0.30)
	_draw_hero_atlas_piece("curb_sidewalk_stoop_strip", Rect2(902, 554, 246, 40), 0.24)
	_draw_hero_atlas_piece("curb_sidewalk_broken_edge", Rect2(324, 586, 246, 28), 0.28)
	_draw_hero_atlas_piece("curb_sidewalk_broken_edge", Rect2(704, 590, 284, 28), 0.24)
	_draw_hero_atlas_piece("commercial_cobble_long_a", Rect2(300, 610, 268, 46), 0.30)
	_draw_hero_atlas_piece("commercial_cobble_patch_b", Rect2(486, 630, 214, 52), 0.30)
	_draw_hero_atlas_piece("commercial_cobble_patch_c", Rect2(618, 602, 178, 48), 0.24)
	_draw_hero_atlas_piece("commercial_cobble_long_a", Rect2(776, 614, 286, 46), 0.24)
	_draw_hero_atlas_piece("commercial_cobble_patch_b", Rect2(958, 632, 196, 48), 0.20)
	_draw_hero_atlas_piece("dirt_wear_transition", Rect2(278, 654, 296, 34), 0.28)
	_draw_hero_atlas_piece("dirt_wear_transition", Rect2(602, 660, 316, 32), 0.24)
	_draw_hero_atlas_piece("dirt_wear_transition", Rect2(918, 656, 240, 30), 0.20)
	_draw_hero_atlas_piece("grass_cobble_feather", Rect2(304, 676, 260, 28), 0.16)
	_draw_hero_atlas_piece("grass_cobble_feather", Rect2(728, 674, 310, 28), 0.14)

func _draw_g417_hero_wharf_atlas_proof() -> void:
	if _newport_hero_atlas == null:
		return
	_draw_hero_atlas_piece("dock_edge_feather", Rect2(266, 684, 318, 34), 0.24)
	_draw_hero_atlas_piece("dock_edge_feather", Rect2(594, 686, 302, 32), 0.22)
	_draw_hero_atlas_piece("dock_edge_feather", Rect2(906, 684, 228, 32), 0.18)
	_draw_hero_atlas_piece("dock_market_transition", Rect2(284, 708, 286, 54), 0.26)
	_draw_hero_atlas_piece("dock_market_transition", Rect2(616, 714, 294, 52), 0.22)
	_draw_hero_atlas_piece("dock_market_transition", Rect2(902, 710, 220, 50), 0.18)
	_draw_hero_atlas_piece("pier_shadow_post_strip", Rect2(278, 696, 224, 46), 0.30)
	_draw_hero_atlas_piece("pier_shadow_post_strip", Rect2(666, 696, 224, 46), 0.26)
	_draw_hero_atlas_piece("pier_shadow_post_strip", Rect2(934, 698, 184, 44), 0.20)
	_draw_hero_atlas_piece("dock_market_transition", Rect2(328, 774, 274, 48), 0.22)
	_draw_hero_atlas_piece("dock_market_transition", Rect2(718, 778, 270, 48), 0.18)
	_draw_hero_atlas_piece("dock_edge_feather", Rect2(304, 834, 292, 30), 0.18)
	_draw_hero_atlas_piece("dock_edge_feather", Rect2(722, 834, 300, 30), 0.16)
	_draw_hero_atlas_piece("dock_pier_vertical", Rect2(392, 730, 58, 122), 0.32)
	_draw_hero_atlas_piece("dock_pier_vertical", Rect2(734, 724, 58, 128), 0.30)
	draw_line(Vector2(252, 690), Vector2(1126, 690), Color("#d6bd7d", 0.20), 1.0)
	draw_line(Vector2(252, 770), Vector2(1126, 770), Color("#0f0a06", 0.34), 1.4)
	draw_line(Vector2(252, 854), Vector2(1126, 854), Color("#0f0a06", 0.38), 1.4)

func _draw_g418c_green_origin_lab_proof() -> void:
	if not _green_origin_lab_enabled:
		return
	if _newport_green_origin_atlas == null:
		return
	_draw_green_origin_piece("green_plank_contact_shadow", Rect2(1010, 772, 178, 32), 0.82)
	_draw_green_origin_piece("green_dock_plank_strip", Rect2(1014, 728, 256, 58), 0.96)
	_draw_green_origin_piece("green_dock_edge_shadow", Rect2(1014, 780, 256, 28), 0.76)
	_draw_green_origin_piece("green_dock_plank_patch", Rect2(1076, 800, 144, 48), 0.92)
	_draw_green_origin_piece("green_pier_post_pair", Rect2(1018, 714, 74, 62), 0.95)
	_draw_green_origin_piece("green_rope_coil_small", Rect2(1188, 770, 54, 38), 0.98)

func _draw_g418d3_pixel_atelier_lab_sprite() -> void:
	if not _green_origin_lab_enabled:
		return
	if _g418d3_pixel_atelier_asset != null:
		draw_texture_rect(_g418d3_pixel_atelier_asset, Rect2(1114, 594, 96, 64), false, Color(1, 1, 1, 1.0))

func _draw_lab_badge(pos: Vector2) -> void:
	var rect := Rect2(pos, Vector2(316, 54))
	draw_rect(rect, Color(0.055, 0.075, 0.06, 0.82), true)
	draw_rect(rect, Color("#d8c06a", 0.72), false, 1.4)
	_draw_label("Green-Origin Lab: ON", pos + Vector2(12, 20), 13, Color("#f1df91"))
	_draw_label("Not normal review art", pos + Vector2(12, 40), 11, Color("#f0b1a3"))

func _draw_g410_wharf_water() -> void:
	_draw_newport_water_rect(Rect2(0, 742, NEWPORT_TOWN.WORLD_SIZE.x, 282), 1.0)
	_draw_water_depth_bands()
	var shore_poly := PackedVector2Array([
		Vector2(0, 712), Vector2(240, 706), Vector2(352, 724), Vector2(500, 708),
		Vector2(642, 718), Vector2(792, 706), Vector2(972, 720), Vector2(1140, 708),
		Vector2(1324, 724), Vector2(1600, 714), Vector2(1600, 752), Vector2(0, 752)
	])
	draw_colored_polygon(shore_poly, Color(0.30, 0.43, 0.36, 0.46))
	draw_polyline(PackedVector2Array([
		Vector2(0, 712), Vector2(240, 706), Vector2(352, 724), Vector2(500, 708),
		Vector2(642, 718), Vector2(792, 706), Vector2(972, 720), Vector2(1140, 708),
		Vector2(1324, 724), Vector2(1600, 714)
	]), Color(0.05, 0.12, 0.13, 0.42), 4.0)
	_draw_newport_pier_edge(PackedVector2Array([
		Vector2(0, 712), Vector2(240, 706), Vector2(352, 724), Vector2(500, 708),
		Vector2(642, 718), Vector2(792, 706), Vector2(972, 720), Vector2(1140, 708),
		Vector2(1324, 724), Vector2(1600, 714)
	]))
	_draw_newport_dock_planks(Rect2(260, 704, 1110, 54), 112)
	_draw_g415_dock_grounding()
	_draw_newport_dock_planks(Rect2(342, 724, 46, 118), 22)
	_draw_newport_dock_planks(Rect2(372, 808, 92, 30), 18)
	_draw_newport_dock_planks(Rect2(452, 816, 46, 18), 10)
	_draw_newport_dock_planks(Rect2(686, 718, 54, 124), 24)
	_draw_newport_dock_planks(Rect2(730, 808, 112, 30), 22)
	_draw_newport_dock_planks(Rect2(826, 816, 58, 18), 12)
	_draw_newport_dock_planks(Rect2(1168, 724, 46, 118), 22)
	_draw_newport_dock_planks(Rect2(1204, 808, 98, 30), 20)
	_draw_newport_dock_planks(Rect2(1288, 816, 52, 18), 10)
	for rect in [Rect2(342, 724, 46, 118), Rect2(372, 808, 126, 30), Rect2(686, 718, 54, 124), Rect2(730, 808, 154, 30), Rect2(1168, 724, 46, 118), Rect2(1204, 808, 136, 30)]:
		draw_rect(Rect2(rect.position.x, rect.position.y + rect.size.y - 3.0, rect.size.x, 5.0), Color(0.02, 0.035, 0.025, 0.24), true)
	_draw_post_line(Vector2(270, 708), Vector2(1360, 708), 68.0)
	_draw_post_line(Vector2(348, 738), Vector2(382, 738), 34.0)
	_draw_post_line(Vector2(694, 730), Vector2(734, 730), 36.0)
	_draw_post_line(Vector2(1174, 738), Vector2(1208, 738), 34.0)
	_draw_post_line(Vector2(346, 742), Vector2(346, 834), 44.0)
	_draw_post_line(Vector2(386, 742), Vector2(386, 834), 44.0)
	_draw_post_line(Vector2(690, 728), Vector2(690, 834), 46.0)
	_draw_post_line(Vector2(738, 728), Vector2(738, 834), 46.0)
	_draw_post_line(Vector2(1172, 742), Vector2(1172, 834), 44.0)
	_draw_post_line(Vector2(1212, 742), Vector2(1212, 834), 44.0)
	_draw_post_line(Vector2(382, 812), Vector2(490, 812), 36.0)
	_draw_post_line(Vector2(740, 812), Vector2(874, 812), 38.0)
	_draw_post_line(Vector2(1214, 812), Vector2(1334, 812), 38.0)
	for p in [Vector2(266, 714), Vector2(358, 724), Vector2(526, 708), Vector2(716, 718), Vector2(934, 712), Vector2(1140, 716), Vector2(1322, 724)]:
		_draw_shore_rocks(p)
	for p in [Vector2(422, 846), Vector2(802, 846), Vector2(1252, 846)]:
		_draw_waterline_scum(p, 150.0)
	for i in range(46):
		var x := 28.0 + float((i * 67) % 1510)
		var y := 776.0 + float((i * 41) % 220)
		draw_line(Vector2(x, y), Vector2(x + 18.0 + float(i % 4) * 5.0, y - 1.0), Color(0.75, 0.95, 1.0, 0.10), 1.4)
	_draw_g417_hero_wharf_atlas_proof()
	_draw_g418c_green_origin_lab_proof()

func _draw_g410_props() -> void:
	for pos in [Vector2(250, 386), Vector2(334, 582), Vector2(506, 586), Vector2(604, 582), Vector2(812, 388), Vector2(986, 386), Vector2(1062, 584), Vector2(1234, 392), Vector2(368, 666), Vector2(1024, 666), Vector2(742, 742), Vector2(1102, 748), Vector2(1268, 672)]:
		if _is_g417_hero_prop_placeholder(pos):
			continue
		_draw_contact_shadow(pos + Vector2(14, 11), Vector2(20, 7), 0.15)
		_draw_crate_stack(pos)
	for pos in [Vector2(286, 394), Vector2(348, 584), Vector2(774, 584), Vector2(850, 390), Vector2(938, 584), Vector2(1182, 392), Vector2(1058, 668), Vector2(418, 728), Vector2(1160, 728), Vector2(254, 410), Vector2(1222, 418)]:
		if _is_g417_hero_prop_placeholder(pos):
			continue
		_draw_contact_shadow(pos + Vector2(8, 6), Vector2(17, 6), 0.16)
		_draw_barrels(pos, 3)
	for pos in [Vector2(298, 408), Vector2(616, 586), Vector2(930, 586), Vector2(552, 688), Vector2(872, 684), Vector2(1256, 408), Vector2(1070, 746), Vector2(664, 694), Vector2(904, 586), Vector2(1286, 812)]:
		if _is_g417_hero_prop_placeholder(pos):
			continue
		_draw_contact_shadow(pos + Vector2(3, 5), Vector2(15, 5), 0.13)
		_draw_rope_coil(pos)
	for pos in [Vector2(476, 592), Vector2(526, 592), Vector2(1052, 592), Vector2(1194, 682)]:
		if _is_g417_hero_prop_placeholder(pos):
			continue
		_draw_contact_shadow(pos + Vector2(10, 9), Vector2(17, 6), 0.13)
		_draw_sack_stack(pos)
	for pos in [Vector2(252, 432), Vector2(290, 432), Vector2(326, 432)]:
		_draw_hoop_stack(pos)
	for pos in [Vector2(706, 656), Vector2(800, 650), Vector2(1174, 660)]:
		if not _is_g417_hero_prop_placeholder(pos):
			_draw_market_table(pos)
	for pos in [Vector2(396, 690), Vector2(1136, 690), Vector2(1228, 684)]:
		if not _is_g417_hero_prop_placeholder(pos):
			_draw_fish_rack(pos)
	for pos in [Vector2(316, 712), Vector2(1004, 714), Vector2(754, 718), Vector2(816, 716)]:
		if not _is_g417_hero_prop_placeholder(pos):
			_draw_net_bundle(pos)
	_draw_rowboat(Vector2(410, 884))
	_draw_rowboat(Vector2(792, 900))
	_draw_rowboat(Vector2(1120, 888))
	_draw_rowboat(Vector2(1370, 868))
	for sign_config in [
		{"pos": Vector2(300, 536), "color": Color("#9d4e38")},
		{"pos": Vector2(506, 536), "color": Color("#4f6d48")},
		{"pos": Vector2(770, 536), "color": Color("#7a7047")},
		{"pos": Vector2(820, 390), "color": Color("#4f6275")},
		{"pos": Vector2(920, 536), "color": Color("#90703d")},
		{"pos": Vector2(1092, 536), "color": Color("#7e6240")},
		{"pos": Vector2(1218, 392), "color": Color("#6c5c43")},
		{"pos": Vector2(1246, 536), "color": Color("#8c6a3f")},
	]:
		var sign_pos: Vector2 = sign_config["pos"]
		if not _is_g417_hero_prop_placeholder(sign_pos):
			_draw_sign_post(sign_pos, sign_config["color"])
	for pos in [Vector2(300, 520), Vector2(510, 520), Vector2(770, 520), Vector2(920, 520), Vector2(1088, 520), Vector2(820, 374), Vector2(1218, 376)]:
		if _is_g417_hero_prop_placeholder(pos):
			continue
		_draw_lantern(pos)
	_draw_net_drying_line(Vector2(1118, 350), Vector2(1238, 330))
	_draw_net_drying_line(Vector2(220, 356), Vector2(320, 338))
	_draw_net_drying_line(Vector2(1164, 398), Vector2(1258, 384))
	for fence_config in [
		{"a": Vector2(210, 410), "b": Vector2(330, 410), "color": Color("#d9c89c")},
		{"a": Vector2(196, 380), "b": Vector2(310, 380), "color": Color("#d9c89c")},
		{"a": Vector2(828, 374), "b": Vector2(966, 374), "color": Color("#d9c89c")},
		{"a": Vector2(1118, 382), "b": Vector2(1262, 382), "color": Color("#d9c89c")},
		{"a": Vector2(1000, 410), "b": Vector2(1090, 410), "color": Color("#d9c89c")},
		{"a": Vector2(406, 442), "b": Vector2(530, 442), "color": Color("#cdbb86")},
	]:
		var fence_a: Vector2 = fence_config["a"]
		var fence_b: Vector2 = fence_config["b"]
		if not _is_g417_hero_prop_placeholder(fence_a) and not _is_g417_hero_prop_placeholder(fence_b):
			_draw_fence_line(fence_a, fence_b, fence_config["color"])
	for pos in [Vector2(396, 462), Vector2(278, 420), Vector2(534, 592)]:
		if not _is_g417_hero_prop_placeholder(pos):
			_draw_woodpile(pos)
	for pos in [Vector2(134, 438), Vector2(1452, 430), Vector2(1320, 332), Vector2(150, 612), Vector2(1368, 642), Vector2(584, 356), Vector2(1018, 356), Vector2(1190, 326)]:
		draw_circle(pos, 13, Color("#2f5d35"))
		draw_circle(pos + Vector2(-8, -8), 8, Color("#3d7042"))
	for bench in [Vector2(792, 404), Vector2(952, 404), Vector2(1178, 410), Vector2(342, 596)]:
		if not _is_g417_hero_prop_placeholder(bench):
			_draw_bench(bench)
	_draw_g417_hero_prop_clusters()
	_draw_g418d3_pixel_atelier_lab_sprite()

func _draw_g417_hero_prop_clusters() -> void:
	if _newport_hero_atlas == null:
		return
	_draw_hero_atlas_piece("crate_barrel_table_cluster", Rect2(494, 614, 118, 87), 0.94)
	_draw_hero_atlas_piece("small_crate_barrel_cluster", Rect2(648, 628, 92, 64), 0.92)
	_draw_hero_atlas_piece("fence_sign_market_cluster", Rect2(862, 610, 118, 87), 0.92)
	_draw_hero_atlas_piece("chandlery_base_cluster", Rect2(966, 586, 128, 85), 0.92)
	_draw_hero_atlas_piece("wharf_crate_pile_cluster", Rect2(552, 708, 132, 88), 0.92)
	_draw_hero_atlas_piece("market_sign_cluster", Rect2(790, 700, 92, 64), 0.88)

func _draw_g49_ground() -> void:
	_draw_soft_rect(Rect2(Vector2.ZERO, NEWPORT_TOWN.WORLD_SIZE), Color("#435f3f"), Color("#334c35"), 1.0, 34)
	_draw_soft_rect(Rect2(280, 268, 830, 330), Color("#516d49"), Color("#405a3f"), 0.80, 18)
	_draw_soft_rect(Rect2(324, 386, 700, 128), Color("#607854"), Color("#4e6849"), 0.64, 10)
	_draw_g49_building_lots()
	_draw_planting_bed(Rect2(286, 430, 70, 54), Color("#637a55"), Color("#4f6848"))
	_draw_planting_bed(Rect2(930, 404, 92, 70), Color("#637a55"), Color("#4f6848"))
	_draw_planting_bed(Rect2(548, 338, 92, 40), Color("#617650"), Color("#4e6648"))

func _draw_g49_building_lots() -> void:
	for raw_config in NEWPORT_TOWN.building_specs():
		var config: Dictionary = raw_config
		if not config.get("proof_street", false) or not config.has("lot_rect"):
			continue
		var origin: Vector2 = config["position"]
		var local_lot: Rect2 = config["lot_rect"]
		var lot := Rect2(origin + local_lot.position, local_lot.size)
		var frontage_y := lot.position.y + lot.size.y

		var rear_rect := Rect2(lot.position + Vector2(10.0, 14.0), Vector2(maxf(0.0, lot.size.x - 20.0), maxf(0.0, lot.size.y - 54.0)))
		var frontage_rect := Rect2(lot.position.x + 4.0, frontage_y - 32.0, maxf(0.0, lot.size.x - 8.0), 32.0)
		draw_rect(lot.grow(10.0), Color(0.02, 0.03, 0.02, 0.12), true)
		_draw_soft_rect(rear_rect, Color("#40523f"), Color("#2f3f32"), 0.22, 5)
		draw_rect(Rect2(rear_rect.position.x + 8.0, rear_rect.position.y + 8.0, maxf(0.0, rear_rect.size.x - 16.0), maxf(0.0, rear_rect.size.y - 18.0)), Color(0.53, 0.60, 0.45, 0.055), true)
		draw_rect(frontage_rect, Color(0.57, 0.55, 0.44, 0.42), true)
		draw_line(Vector2(frontage_rect.position.x, frontage_rect.position.y + 2.0), Vector2(frontage_rect.position.x + frontage_rect.size.x, frontage_rect.position.y + 2.0), Color(0.04, 0.04, 0.03, 0.22), 1.6)
		draw_line(Vector2(frontage_rect.position.x + 6.0, frontage_y - 1.0), Vector2(frontage_rect.position.x + frontage_rect.size.x - 6.0, frontage_y - 1.0), Color("#c8b985"), 1.2)
		for x in range(int(frontage_rect.position.x + 14.0), int(frontage_rect.position.x + frontage_rect.size.x - 12.0), 38):
			draw_line(Vector2(x, frontage_y - 13.0), Vector2(x + 16.0, frontage_y - 13.0), Color(0.90, 0.82, 0.58, 0.10), 1.0)

func _draw_g49_street_plane() -> void:
	_draw_cobbled_world_rect(Rect2(312, 538, 724, 36), Color("#9b9278"), Color("#746d5a"), 54)
	draw_line(Vector2(318, 541), Vector2(1030, 541), Color(1.0, 0.93, 0.68, 0.10), 1.0)
	draw_line(Vector2(318, 573), Vector2(1030, 573), Color(0.05, 0.04, 0.03, 0.20), 1.0)
	for p in [Vector2(477, 566), Vector2(658, 562), Vector2(831, 568)]:
		_draw_g47_threshold(p, 58)
	for p in [Vector2(548, 566), Vector2(760, 566)]:
		draw_rect(Rect2(p + Vector2(-20, -10), Vector2(40, 24)), Color("#6b624f"), true)
		draw_rect(Rect2(p + Vector2(-20, -10), Vector2(40, 24)), Color(0, 0, 0, 0.20), false, 1.0)
	draw_rect(Rect2(312, 574, 724, 7), Color("#3d372d"), true)
	draw_line(Vector2(318, 576), Vector2(1030, 576), Color("#d6c48e"), 1.2)
	draw_rect(Rect2(312, 581, 724, 3), Color(0.06, 0.05, 0.04, 0.26), true)
	_draw_cobbled_world_rect(Rect2(292, 586, 764, 48), Color("#655f52"), Color("#4b473e"), 86)
	draw_line(Vector2(302, 608), Vector2(1048, 604), Color(0.96, 0.86, 0.62, 0.10), 1.0)
	draw_line(Vector2(304, 630), Vector2(1044, 626), Color(0.04, 0.04, 0.03, 0.18), 1.0)
	draw_rect(Rect2(296, 634, 756, 4), Color(0.03, 0.035, 0.03, 0.28), true)
	_draw_plank_world_rect(Rect2(300, 646, 742, 38), Color("#766950"), Color("#5b503d"))
	draw_line(Vector2(306, 644), Vector2(1036, 644), Color(0.04, 0.04, 0.03, 0.30), 2.0)
	draw_line(Vector2(306, 684), Vector2(1036, 684), Color(0.02, 0.03, 0.025, 0.24), 2.0)
	for p in [Vector2(334, 646), Vector2(414, 646), Vector2(548, 646), Vector2(692, 646), Vector2(828, 646), Vector2(1008, 646)]:
		_draw_post(p)
	for p in [Vector2(372, 574), Vector2(536, 574), Vector2(746, 574), Vector2(916, 574)]:
		draw_circle(p, 3.5, Color("#30271d"))
		draw_circle(p + Vector2(0, -5), 2.8, Color("#d8b56f"))

func _draw_g49_wharf_water() -> void:
	_draw_soft_rect(Rect2(0, 704, NEWPORT_TOWN.WORLD_SIZE.x, 320), Color("#2f7184"), Color("#1f5369"), 1.0, 24)
	draw_colored_polygon(PackedVector2Array([
		Vector2(0, 678), Vector2(310, 674), Vector2(430, 682), Vector2(600, 676),
		Vector2(760, 682), Vector2(930, 676), Vector2(1120, 684), Vector2(1600, 678),
		Vector2(1600, 724), Vector2(0, 724)
	]), Color(0.28, 0.38, 0.32, 0.44))
	draw_polyline(PackedVector2Array([
		Vector2(0, 678), Vector2(310, 674), Vector2(430, 682), Vector2(600, 676),
		Vector2(760, 682), Vector2(930, 676), Vector2(1120, 684), Vector2(1600, 678)
	]), Color(0.04, 0.10, 0.10, 0.36), 3.0)
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
	for pos in [Vector2(428, 544), Vector2(522, 548), Vector2(592, 542), Vector2(890, 550)]:
		_draw_contact_shadow(pos + Vector2(14, 11), Vector2(20, 7), 0.15)
		_draw_crate_stack(pos)
	for pos in [Vector2(456, 548), Vector2(730, 546), Vector2(928, 548)]:
		_draw_contact_shadow(pos + Vector2(8, 6), Vector2(17, 6), 0.16)
		_draw_barrels(pos, 2)
	for pos in [Vector2(786, 548), Vector2(462, 636), Vector2(918, 636)]:
		_draw_contact_shadow(pos + Vector2(3, 5), Vector2(15, 5), 0.13)
		_draw_rope_coil(pos)
	_draw_sign_post(Vector2(552, 536), Color("#4f6d48"))
	_draw_sign_post(Vector2(770, 536), Color("#7a7047"))
	_draw_sign_post(Vector2(908, 536), Color("#90703d"))
	_draw_contact_shadow(Vector2(1014, 561), Vector2(20, 7), 0.14)
	_draw_crate_stack(Vector2(1000, 550))
	_draw_contact_shadow(Vector2(771, 656), Vector2(34, 8), 0.14)
	_draw_market_table(Vector2(742, 636))
	_draw_net_bundle(Vector2(336, 674))
	_draw_net_bundle(Vector2(1000, 676))
	_draw_rowboat(Vector2(684, 852))
	for p in [Vector2(376, 562), Vector2(786, 560), Vector2(1010, 565)]:
		_draw_contact_shadow(p + Vector2(0, 9), Vector2(9, 4), 0.12)
		draw_rect(Rect2(p + Vector2(-3, -10), Vector2(6, 20)), Color("#3f2e20"), true)
		draw_circle(p + Vector2(0, -14), 4, Color("#d6b36e"))
	for pos in [Vector2(354, 530), Vector2(988, 528)]:
		_draw_contact_shadow(pos + Vector2(4, 10), Vector2(10, 4), 0.10)
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

func _draw_newport_grass_rect(rect: Rect2, base: Color, alt: Color, alpha := 1.0, detail_count := 24) -> void:
	_draw_soft_rect(rect, base, alt, alpha, detail_count)
	var tuft_count := maxi(8, int(rect.size.x * rect.size.y / 12500.0))
	for i in range(tuft_count):
		var x := rect.position.x + fmod(float(i * 67 + 19), maxf(1.0, rect.size.x - 12.0))
		var y := rect.position.y + fmod(float(i * 43 + 31), maxf(1.0, rect.size.y - 8.0))
		var p := Vector2(x, y)
		var grass_alpha := alpha * (0.11 + float(i % 3) * 0.025)
		draw_line(p, p + Vector2(5.0, -2.0), Color("#9fb071", grass_alpha), 1.0)
		draw_line(p + Vector2(6.0, 1.0), p + Vector2(10.0, -1.0), Color("#2f4d31", grass_alpha * 0.78), 1.0)
		if i % 5 == 0:
			draw_rect(Rect2(p + Vector2(2.0, 3.0), Vector2(11.0, 2.0)), Color(0.06, 0.08, 0.04, alpha * 0.055), true)

func _draw_newport_lot_variation(rect: Rect2, base: Color, alt: Color, alpha: float, district: String) -> void:
	_draw_soft_rect(rect, base, alt, alpha, 5)
	var edge_color := Color(0.05, 0.065, 0.035, alpha * 0.34)
	if district == "working_wharf":
		edge_color = Color(0.05, 0.04, 0.025, alpha * 0.45)
	for i in range(6):
		var y := rect.position.y + 8.0 + fmod(float(i * 17 + 5), maxf(1.0, rect.size.y - 18.0))
		draw_line(Vector2(rect.position.x + 10.0, y), Vector2(rect.end.x - 12.0, y - 2.0), edge_color, 1.0)
	_draw_surface_speckles(rect.grow(-8.0), 8, Color(0.09, 0.075, 0.045, alpha * 0.52), Vector2(18, 3))

func _draw_newport_grass_transition(rect: Rect2, edge: String, alpha: float) -> void:
	_draw_surface_speckles(rect, 16, Color(0.05, 0.07, 0.035, alpha), Vector2(28, 4))
	var step := 18
	var start_x := int(rect.position.x + 4.0)
	var end_x := int(rect.end.x - 4.0)
	for x in range(start_x, end_x, step):
		var t := fmod(float(x * 11), 100.0) / 100.0
		var y := rect.position.y + (rect.size.y * t if edge == "south" else rect.size.y * (1.0 - t))
		draw_line(Vector2(x, y), Vector2(x + 12.0, y - 1.0), Color("#a79a66", alpha * 0.42), 1.0)
		draw_line(Vector2(x + 3.0, y + 3.0), Vector2(x + 14.0, y + 2.0), Color("#263f2a", alpha * 0.32), 1.0)

func _draw_newport_sidewalk_panel(rect: Rect2, kind: String, alpha := 0.55) -> void:
	var base := Color("#756e5b", alpha)
	var edge := Color("#4d4638", alpha * 0.74)
	var hi := Color("#d5c28c", alpha * 0.26)
	if kind == "market":
		base = Color("#796d55", alpha)
	elif kind == "civic":
		base = Color("#777264", alpha)
	elif kind == "curb" or kind == "curb_shadow":
		base = Color("#81775f", alpha)
		edge = Color("#3f382d", alpha * 0.80)
	elif kind == "frontage":
		base = Color("#7d7159", alpha)
	elif kind == "street_patch":
		base = Color("#746e5c", alpha)
	draw_rect(Rect2(rect.position - Vector2(2.0, 3.0), rect.size + Vector2(4.0, 6.0)), Color(0.02, 0.025, 0.018, alpha * 0.26), true)
	draw_rect(rect, base, true)
	var seams := maxi(2, int(rect.size.x / 34.0))
	for i in range(seams + 1):
		var x := rect.position.x + fmod(float(i * 37 + 9), maxf(1.0, rect.size.x))
		draw_line(Vector2(x, rect.position.y + 3.0), Vector2(x - 4.0, rect.end.y - 4.0), Color(0.03, 0.03, 0.025, alpha * 0.34), 1.0)
	for y in range(int(rect.position.y + 6.0), int(rect.end.y - 3.0), 13):
		draw_line(Vector2(rect.position.x + 6.0, y), Vector2(rect.end.x - 8.0, y - 1.0), Color(0.03, 0.03, 0.025, alpha * 0.18), 1.0)
	draw_line(rect.position + Vector2(6.0, 3.0), rect.position + Vector2(rect.size.x - 8.0, 2.0), hi, 1.0)
	draw_line(rect.position + Vector2(4.0, rect.size.y - 2.0), rect.position + Vector2(rect.size.x - 6.0, rect.size.y - 3.0), edge, 1.3)
	_draw_surface_speckles(rect.grow(-4.0), maxi(4, int(rect.size.x / 24.0)), Color(0.10, 0.08, 0.05, alpha * 0.16), Vector2(14, 3))

func _draw_newport_commercial_street(rect: Rect2, detail_count: int, alpha := 1.0) -> void:
	draw_rect(rect.grow(5.0), Color(0.02, 0.022, 0.018, 0.12 * alpha), true)
	draw_rect(rect, Color("#635d50", alpha), true)
	for i in range(detail_count):
		var w := 12.0 + float((i * 7) % 17)
		var h := 5.0 + float((i * 5) % 9)
		var x := rect.position.x + fmod(float(i * 43 + 17), maxf(1.0, rect.size.x - w))
		var y := rect.position.y + fmod(float(i * 31 + 11), maxf(1.0, rect.size.y - h))
		var n := fmod(float(i * 19), 100.0) / 100.0
		var stone := Color("#6f6958").lerp(Color("#a69a75"), n * 0.34)
		draw_rect(Rect2(Vector2(x, y), Vector2(w, h)), Color(stone.r, stone.g, stone.b, 0.22 * alpha), true)
		if i % 3 == 0:
			draw_line(Vector2(x + 2.0, y + 1.0), Vector2(x + w - 2.0, y), Color("#d6c28b", 0.08 * alpha), 1.0)
		if i % 4 == 0:
			draw_line(Vector2(x + 2.0, y + h - 1.0), Vector2(x + w - 2.0, y + h - 2.0), Color(0.04, 0.035, 0.025, 0.10 * alpha), 1.0)
	draw_line(rect.position + Vector2(4.0, 3.0), rect.position + Vector2(rect.size.x - 5.0, 2.0), Color("#d0bd85", 0.10 * alpha), 1.0)
	draw_line(rect.position + Vector2(3.0, rect.size.y - 2.0), rect.position + Vector2(rect.size.x - 4.0, rect.size.y - 4.0), Color(0.025, 0.025, 0.02, 0.20 * alpha), 1.4)

func _draw_newport_dirt_path(a: Vector2, b: Vector2, width: float, stone := true) -> void:
	draw_line(a, b, Color("#514432", 0.38), width + 12.0, true)
	draw_line(a, b, Color("#8d7656", 0.92), width, true)
	draw_line(a, b, Color("#b19569", 0.26), maxf(2.0, width - 7.0), true)
	var length := a.distance_to(b)
	var steps: int = maxi(1, int(length / 28.0))
	var dir := (b - a).normalized()
	var normal := Vector2(-dir.y, dir.x)
	for i in range(steps):
		var t := float(i) / float(maxi(1, steps - 1))
		var p := a.lerp(b, t)
		var side := (fmod(float(i * 37), 100.0) / 100.0 - 0.5) * width * 0.70
		draw_line(p + normal * side - dir * 7.0, p + normal * side + dir * (8.0 + float(i % 3) * 2.0), Color(0.10, 0.075, 0.045, 0.16), 1.0)
		if stone and i % 2 == 0:
			draw_line(p - normal * side * 0.3 - dir * 4.0, p - normal * side * 0.3 + dir * 5.0, Color("#d7c28a", 0.12), 1.0)

func _draw_newport_service_lane_path(a: Vector2, b: Vector2, width: float) -> void:
	_draw_newport_dirt_path(a, b, width, true)
	var dir := (b - a).normalized()
	var normal := Vector2(-dir.y, dir.x)
	draw_line(a + normal * width * 0.42, b + normal * width * 0.42, Color(0.04, 0.035, 0.025, 0.18), 1.0, true)
	draw_line(a - normal * width * 0.42, b - normal * width * 0.42, Color("#cfba82", 0.12), 1.0, true)

func _draw_newport_service_lane_rect(rect: Rect2, alpha := 0.40) -> void:
	draw_rect(rect.grow(4.0), Color(0.02, 0.025, 0.018, alpha * 0.28), true)
	_draw_soft_rect(rect, Color("#675f49"), Color("#4a503b"), alpha, 5)
	for x in range(int(rect.position.x + 10.0), int(rect.end.x - 8.0), 26):
		var y := rect.position.y + 8.0 + fmod(float(x * 5), maxf(1.0, rect.size.y - 12.0))
		draw_line(Vector2(x, y), Vector2(x + 13.0, y - 1.0), Color("#d2b675", alpha * 0.36), 1.0)
		if x % 3 == 0:
			draw_circle(Vector2(x + 5.0, y + 4.0), 1.5, Color(0.10, 0.07, 0.04, alpha * 0.45))

func _draw_newport_dock_planks(rect: Rect2, weather_count := 24) -> void:
	draw_rect(rect.grow(4.0), Color(0.02, 0.025, 0.018, 0.18), true)
	draw_rect(rect, Color("#6f5940"), true)
	var along_x := rect.size.x >= rect.size.y
	if along_x:
		var plank_index := 0
		for y in range(int(rect.position.y), int(rect.end.y), 8):
			var plank_h := 7.0 + float(plank_index % 3)
			var row := Rect2(rect.position.x, float(y), rect.size.x, minf(plank_h, rect.end.y - float(y)))
			var shade := Color("#7a5f40").lerp(Color("#55402c"), float(plank_index % 6) / 10.0)
			draw_rect(row, shade, true)
			draw_line(Vector2(row.position.x + 4.0, row.position.y), Vector2(row.end.x - 6.0, row.position.y - 1.0), Color("#c5a66b", 0.10), 1.0)
			draw_line(Vector2(row.position.x + 3.0, row.end.y - 1.0), Vector2(row.end.x - 5.0, row.end.y - 2.0), Color(0.03, 0.025, 0.018, 0.13), 1.0)
			plank_index += 1
		for x in range(int(rect.position.x) + 18, int(rect.end.x), 52):
			draw_line(Vector2(x, rect.position.y + 3.0), Vector2(x - 3.0, rect.end.y - 4.0), Color(0.03, 0.025, 0.018, 0.11), 1.0)
	else:
		var plank_index := 0
		for x in range(int(rect.position.x), int(rect.end.x), 8):
			var plank_w := 7.0 + float(plank_index % 3)
			var col := Rect2(float(x), rect.position.y, minf(plank_w, rect.end.x - float(x)), rect.size.y)
			var shade := Color("#785d3e").lerp(Color("#513c29"), float(plank_index % 6) / 10.0)
			draw_rect(col, shade, true)
			draw_line(Vector2(col.position.x, col.position.y + 4.0), Vector2(col.position.x - 1.0, col.end.y - 6.0), Color("#c5a66b", 0.09), 1.0)
			draw_line(Vector2(col.end.x - 1.0, col.position.y + 3.0), Vector2(col.end.x - 2.0, col.end.y - 5.0), Color(0.03, 0.025, 0.018, 0.13), 1.0)
			plank_index += 1
		for y in range(int(rect.position.y) + 20, int(rect.end.y), 52):
			draw_line(Vector2(rect.position.x + 3.0, y), Vector2(rect.end.x - 4.0, y - 2.0), Color(0.03, 0.025, 0.018, 0.11), 1.0)
	_draw_plank_weathering(rect, weather_count)
	draw_rect(rect, Color(0.0, 0.0, 0.0, 0.10), false, 1.0)

func _draw_newport_water_rect(rect: Rect2, alpha := 1.0) -> void:
	_draw_soft_rect(rect, Color("#2e7183"), Color("#1d5267"), alpha, 36)
	for i in range(30):
		var x := rect.position.x + fmod(float(i * 71 + 23), maxf(1.0, rect.size.x - 40.0))
		var y := rect.position.y + fmod(float(i * 47 + 13), maxf(1.0, rect.size.y - 10.0))
		draw_line(Vector2(x, y), Vector2(x + 24.0 + float(i % 5) * 4.0, y - 1.0), Color("#9ed1d8", 0.06 * alpha), 1.0)
		if i % 4 == 0:
			draw_line(Vector2(x + 4.0, y + 5.0), Vector2(x + 36.0, y + 3.0), Color("#123a4d", 0.07 * alpha), 1.0)

func _draw_newport_pier_edge(points: PackedVector2Array) -> void:
	draw_polyline(points, Color(0.018, 0.025, 0.018, 0.42), 6.0, true)
	draw_polyline(points, Color("#bfa873", 0.16), 1.4, true)
	for i in range(points.size()):
		if i == points.size() - 1:
			continue
		var a := points[i]
		var b := points[i + 1]
		var length := a.distance_to(b)
		var steps := maxi(1, int(length / 58.0))
		for j in range(steps):
			var p := a.lerp(b, float(j) / float(maxi(1, steps)))
			draw_line(p + Vector2(4.0, 6.0), p + Vector2(22.0, 4.0), Color("#88a98c", 0.13), 1.0)

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
	_draw_contact_shadow(pos + Vector2(14.0, 12.0), Vector2(18.0, 5.0), 0.12)
	_draw_crate(pos, Vector2(18, 16), Color("#9b7042"))
	_draw_crate(pos + Vector2(14, -7), Vector2(14, 13), Color("#ad7d49"))

func _draw_crate(pos: Vector2, size: Vector2, color: Color) -> void:
	draw_rect(Rect2(pos, size), color, true)
	draw_rect(Rect2(pos, size), Color("#2e2117"), false, 1.2)
	draw_line(pos + Vector2(2.0, 3.0), pos + Vector2(size.x - 2.0, size.y - 3.0), Color(0.16, 0.09, 0.05, 0.62), 1.0)
	draw_line(pos + Vector2(2.0, size.y - 4.0), pos + Vector2(size.x - 3.0, 3.0), Color("#d1a36a", 0.24), 1.0)
	draw_line(pos + Vector2(3.0, 4.0), pos + Vector2(size.x - 4.0, 4.0), Color("#d4a66a", 0.20), 1.0)
	draw_line(pos + Vector2(3.0, size.y - 3.0), pos + Vector2(size.x - 4.0, size.y - 4.0), Color(0.08, 0.05, 0.03, 0.30), 1.0)

func _draw_barrels(pos: Vector2, count: int) -> void:
	for i in range(count):
		var barrel_pos := pos + Vector2(i * 9, 0)
		_draw_ellipse(barrel_pos + Vector2(1.0, 6.0), Vector2(6, 2.2), Color(0.02, 0.018, 0.012, 0.15))
		_draw_ellipse(barrel_pos, Vector2(4.8, 7.4), Color("#7f5631"))
		_draw_ellipse(barrel_pos + Vector2(-1.2, -1.8), Vector2(2.0, 4.5), Color("#a46e3c", 0.36))
		draw_rect(Rect2(barrel_pos + Vector2(-4.5, -2.0), Vector2(9.0, 2.0)), Color("#3f2c1d"), true)
		draw_rect(Rect2(barrel_pos + Vector2(-4.5, 2.0), Vector2(9.0, 2.0)), Color("#3f2c1d"), true)
		draw_arc(barrel_pos, 6.0, 0, TAU, 16, Color("#c2965a"), 1.1)

func _draw_market_table(pos: Vector2) -> void:
	_draw_contact_shadow(pos + Vector2(29.0, 22.0), Vector2(32.0, 6.0), 0.12)
	draw_rect(Rect2(pos + Vector2(-2.0, -2.0), Vector2(62, 20)), Color("#3b2a1c"), true)
	draw_rect(Rect2(pos, Vector2(58, 17)), Color("#80603c"), true)
	for y in [3, 8, 13]:
		draw_line(pos + Vector2(4, y), pos + Vector2(54, y - 1), Color(0.15, 0.09, 0.05, 0.34), 1.0)
	draw_rect(Rect2(pos + Vector2(2, 2), Vector2(54, 4)), Color("#d2b06e", 0.76), true)
	for i in range(7):
		var color := Color("#d9c37a") if i % 2 == 0 else Color("#a95e45")
		draw_circle(pos + Vector2(8 + i * 7, 11), 2.4, color)
	draw_rect(Rect2(pos + Vector2(4, 17), Vector2(3, 8)), Color("#4d3824"), true)
	draw_rect(Rect2(pos + Vector2(50, 17), Vector2(3, 8)), Color("#4d3824"), true)

func _draw_fish_rack(pos: Vector2) -> void:
	draw_line(pos + Vector2(1.0, 18.0), pos + Vector2(39.0, 18.0), Color(0.02, 0.018, 0.012, 0.16), 3.0)
	draw_line(pos, pos + Vector2(38, 0), Color("#6c4b30"), 2.0)
	draw_line(pos + Vector2(3, 0), pos + Vector2(3, 18), Color("#6c4b30"), 2.0)
	draw_line(pos + Vector2(35, 0), pos + Vector2(35, 18), Color("#6c4b30"), 2.0)
	draw_line(pos + Vector2(0, -1), pos + Vector2(38, -1), Color("#c29a62", 0.24), 1.0)
	for i in range(7):
		draw_rect(Rect2(pos + Vector2(6 + i * 5, 2), Vector2(2, 9)), Color("#c9b98c"), true)
		draw_line(pos + Vector2(7 + i * 5, 2), pos + Vector2(7 + i * 5, 11), Color("#4b4538", 0.22), 1.0)

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
	_draw_contact_shadow(pos + Vector2(0.0, 18.0), Vector2(8.0, 3.0), 0.10)
	draw_rect(Rect2(pos + Vector2(-1.5, -1.0), Vector2(3, 20)), Color("#3e2c1d"), true)
	draw_rect(Rect2(pos + Vector2(-9, 1), Vector2(18, 9)), color, true)
	draw_rect(Rect2(pos + Vector2(-9, 1), Vector2(18, 9)), Color(0, 0, 0, 0.36), false, 1.0)
	draw_line(pos + Vector2(-7.0, 3.0), pos + Vector2(7.0, 3.0), Color("#d3b06c", 0.20), 1.0)
	draw_line(pos + Vector2(-6.0, 8.0), pos + Vector2(6.0, 8.0), Color(0.07, 0.045, 0.025, 0.22), 1.0)

func _draw_net_drying_line(a: Vector2, b: Vector2) -> void:
	draw_line(a, b, Color("#6f5a38", 0.72), 1.4)
	for i in range(3):
		var t := float(i + 1) / 4.0
		var p := a.lerp(b, t)
		draw_line(p + Vector2(-8.0, 1.0), p + Vector2(8.0, -1.0), Color("#b9a66f", 0.54), 1.0)
		draw_line(p + Vector2(-6.0, 4.0), p + Vector2(6.0, 2.0), Color("#8e7b50", 0.42), 1.0)
		draw_line(p + Vector2(-5.0, 1.0), p + Vector2(-3.0, 9.0), Color("#b9a66f", 0.34), 1.0)
		draw_line(p + Vector2(4.0, 0.0), p + Vector2(5.0, 8.0), Color("#b9a66f", 0.34), 1.0)

func _draw_clothesline(a: Vector2, b: Vector2) -> void:
	draw_line(a, b, Color("#d6c49c"), 1.0)
	for i in range(4):
		var t := float(i + 1) / 5.0
		var p := a.lerp(b, t)
		draw_rect(Rect2(p + Vector2(-5, 1), Vector2(10, 9)), Color("#d8d2b6") if i % 2 == 0 else Color("#7b8c9c"), true)

func _draw_fence_line(a: Vector2, b: Vector2, color: Color) -> void:
	draw_line(a + Vector2(0, 3), b + Vector2(0, 3), Color(0.02, 0.02, 0.014, color.a * 0.22), 2.0)
	draw_line(a, b, color, 2.0)
	var distance := a.distance_to(b)
	var steps := int(distance / 12.0)
	for i in range(steps + 1):
		var p := a.lerp(b, float(i) / maxf(1.0, steps))
		draw_rect(Rect2(p + Vector2(-1.5, -7), Vector2(3, 14)), color.darkened(0.32), true)
		draw_rect(Rect2(p + Vector2(-1.0, -7), Vector2(2, 3)), color.lightened(0.18), true)

func _draw_woodpile(pos: Vector2) -> void:
	_draw_contact_shadow(pos + Vector2(16.0, 8.0), Vector2(22.0, 5.0), 0.12)
	for i in range(5):
		var p := pos + Vector2(i * 7, (i % 2) * 4)
		draw_rect(Rect2(p, Vector2(10, 3)), Color("#775032"), true)
		draw_circle(p + Vector2(1, 1.5), 1.5, Color("#b98750"))

func _draw_g410_background_depth() -> void:
	for spec in [
		{"base": Rect2(112, 210, 90, 54), "roof": Color("#2f3e35", 0.18), "wall": Color("#6f8065", 0.13)},
		{"base": Rect2(474, 140, 128, 58), "roof": Color("#2e3d36", 0.16), "wall": Color("#6b7f62", 0.12)},
		{"base": Rect2(1012, 142, 112, 54), "roof": Color("#2e3a34", 0.16), "wall": Color("#708163", 0.12)},
		{"base": Rect2(1316, 214, 116, 58), "roof": Color("#2c3932", 0.15), "wall": Color("#6a7c5f", 0.11)},
	]:
		var base: Rect2 = spec["base"]
		draw_rect(base, spec["wall"], true)
		draw_colored_polygon(PackedVector2Array([
			base.position + Vector2(-8.0, 6.0),
			base.position + Vector2(base.size.x * 0.5, -22.0),
			base.position + Vector2(base.size.x + 8.0, 6.0),
		]), spec["roof"])
		draw_line(base.position + Vector2(8.0, base.size.y - 7.0), base.position + Vector2(base.size.x - 8.0, base.size.y - 7.0), Color("#d0bf87", 0.08), 1.0)
	for wall in [
		[Vector2(150, 318), Vector2(324, 304)],
		[Vector2(466, 300), Vector2(620, 294)],
		[Vector2(1068, 314), Vector2(1248, 306)],
		[Vector2(1300, 430), Vector2(1440, 420)],
	]:
		_draw_low_wall(wall[0], wall[1], Color("#67735d", 0.30))

func _draw_surface_speckles(rect: Rect2, count: int, color: Color, max_size: Vector2) -> void:
	for i in range(count):
		var x := rect.position.x + fmod(float(i * 37 + 11), maxf(1.0, rect.size.x - max_size.x))
		var y := rect.position.y + fmod(float(i * 19 + 7), maxf(1.0, rect.size.y - max_size.y))
		var w := 4.0 + float((i * 5) % int(maxf(5.0, max_size.x)))
		var h := 1.0 + float((i * 3) % int(maxf(2.0, max_size.y)))
		draw_rect(Rect2(Vector2(x, y), Vector2(w, h)), color, true)

func _draw_residential_path(a: Vector2, b: Vector2, width: float) -> void:
	draw_line(a, b, Color("#8b7657", 0.22), width + 4.0, true)
	draw_line(a, b, Color("#b0996d", 0.18), width, true)
	draw_line(a, b, Color(0.08, 0.07, 0.04, 0.10), width + 1.0, true)
	for i in range(4):
		var t := float(i + 1) / 5.0
		var p := a.lerp(b, t)
		draw_line(p + Vector2(-8.0, 2.0), p + Vector2(8.0, -1.0), Color("#d9c28a", 0.12), 1.0)

func _draw_shrub_cluster(pos: Vector2, scale := 1.0) -> void:
	draw_circle(pos, 7.0 * scale, Color("#2f5d35", 0.86))
	draw_circle(pos + Vector2(-6.0, -5.0) * scale, 5.0 * scale, Color("#3d7042", 0.86))
	draw_circle(pos + Vector2(7.0, -3.0) * scale, 4.5 * scale, Color("#486f3f", 0.72))
	draw_rect(Rect2(pos + Vector2(-2.0, 4.0) * scale, Vector2(4.0, 4.0) * scale), Color("#2b3f28", 0.45), true)

func _draw_low_wall(a: Vector2, b: Vector2, color: Color) -> void:
	draw_line(a, b, Color(0.03, 0.035, 0.025, color.a * 0.45), 5.0, true)
	draw_line(a, b, color, 3.0, true)
	var distance := a.distance_to(b)
	var steps := int(distance / 20.0)
	for i in range(steps + 1):
		var p := a.lerp(b, float(i) / maxf(1.0, float(steps)))
		draw_line(p + Vector2(-5.0, 1.0), p + Vector2(5.0, -1.0), Color("#d0c28d", color.a * 0.34), 1.0)

func _draw_street_wear(rect: Rect2, count: int) -> void:
	for i in range(count):
		var x := rect.position.x + fmod(float(i * 43 + 17), maxf(1.0, rect.size.x - 38.0))
		var y := rect.position.y + fmod(float(i * 29 + 13), maxf(1.0, rect.size.y - 8.0))
		var w := 14.0 + float((i * 7) % 32)
		var alpha := 0.05 + float(i % 4) * 0.012
		draw_rect(Rect2(Vector2(x, y), Vector2(w, 3.0)), Color(0.10, 0.08, 0.05, alpha), true)
		if i % 5 == 0:
			draw_line(Vector2(x + 2.0, y + 5.0), Vector2(x + w - 2.0, y + 3.0), Color("#d7c58e", 0.07), 1.0)

func _draw_edge_grime(pos: Vector2, width: float) -> void:
	draw_line(pos + Vector2(-width * 0.5, 0.0), pos + Vector2(width * 0.5, -4.0), Color(0.05, 0.04, 0.025, 0.16), 8.0, true)
	draw_line(pos + Vector2(-width * 0.45, 2.0), pos + Vector2(width * 0.45, -2.0), Color("#bfa774", 0.08), 2.0, true)

func _draw_plank_weathering(rect: Rect2, count: int) -> void:
	for i in range(count):
		var x := rect.position.x + fmod(float(i * 31 + 9), maxf(1.0, rect.size.x - 26.0))
		var y := rect.position.y + fmod(float(i * 47 + 15), maxf(1.0, rect.size.y - 8.0))
		var w := 10.0 + float((i * 5) % 24)
		draw_line(Vector2(x, y), Vector2(x + w, y - 1.0), Color(0.05, 0.035, 0.025, 0.16), 1.0)
		if i % 4 == 0:
			draw_circle(Vector2(x + 3.0, y + 2.0), 1.2, Color("#2b2118", 0.26))

func _draw_water_depth_bands() -> void:
	_draw_soft_rect(Rect2(0, 792, NEWPORT_TOWN.WORLD_SIZE.x, 64), Color("#28687b"), Color("#1d4d62"), 0.18, 12)
	_draw_soft_rect(Rect2(0, 896, NEWPORT_TOWN.WORLD_SIZE.x, 80), Color("#225c70"), Color("#193f55"), 0.20, 12)
	draw_line(Vector2(0, 744), Vector2(1600, 736), Color("#86b6bf", 0.08), 2.0)
	for i in range(18):
		var p := Vector2(50.0 + float((i * 83) % 1500), 756.0 + float((i * 31) % 90))
		draw_line(p, p + Vector2(42.0, -2.0), Color("#9ed1d8", 0.075), 1.0)

func _draw_waterline_scum(pos: Vector2, width: float) -> void:
	draw_line(pos + Vector2(-width * 0.5, 0.0), pos + Vector2(width * 0.5, -3.0), Color("#83a98d", 0.20), 4.0, true)
	draw_line(pos + Vector2(-width * 0.42, 5.0), pos + Vector2(width * 0.42, 2.0), Color("#d4c790", 0.10), 1.4, true)

func _draw_sack_stack(pos: Vector2) -> void:
	_draw_ellipse(pos + Vector2(8.0, 6.0), Vector2(10.0, 6.0), Color("#b69a68", 0.92))
	_draw_ellipse(pos + Vector2(20.0, 7.0), Vector2(9.0, 6.0), Color("#9e8458", 0.92))
	_draw_ellipse(pos + Vector2(14.0, -1.0), Vector2(11.0, 6.0), Color("#c0a873", 0.92))
	draw_line(pos + Vector2(8.0, 1.0), pos + Vector2(20.0, 0.0), Color("#6a5232", 0.35), 1.0)

func _draw_lantern(pos: Vector2) -> void:
	draw_rect(Rect2(pos + Vector2(-1.0, 0.0), Vector2(2.0, 18.0)), Color("#3e2c1d"), true)
	draw_rect(Rect2(pos + Vector2(-5.0, -9.0), Vector2(10.0, 11.0)), Color("#4a3320"), true)
	draw_rect(Rect2(pos + Vector2(-3.0, -7.0), Vector2(6.0, 7.0)), Color("#d2a956", 0.72), true)
	draw_circle(pos + Vector2(0.0, -3.0), 8.0, Color("#d2a956", 0.08))

func _draw_hoop_stack(pos: Vector2) -> void:
	for i in range(3):
		var center := pos + Vector2(i * 8.0, float(i % 2) * 2.0)
		draw_arc(center, 8.0, 0.0, TAU, 18, Color("#b48750", 0.88), 1.4)
		draw_arc(center, 5.0, 0.0, TAU, 14, Color("#5f4025", 0.72), 1.0)

func _draw_bench(pos: Vector2) -> void:
	draw_rect(Rect2(pos + Vector2(-18, -3), Vector2(36, 6)), Color("#6f4b2f"), true)
	draw_rect(Rect2(pos + Vector2(-16, -9), Vector2(32, 5)), Color("#8a6139"), true)
	draw_rect(Rect2(pos + Vector2(-14, 3), Vector2(3, 10)), Color("#3d2b1f"), true)
	draw_rect(Rect2(pos + Vector2(11, 3), Vector2(3, 10)), Color("#3d2b1f"), true)

func _draw_ellipse(center: Vector2, radii: Vector2, color: Color) -> void:
	draw_set_transform(center, 0.0, Vector2(radii.x / 16.0, radii.y / 16.0))
	draw_circle(Vector2.ZERO, 16.0, color)
	draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)

func _draw_contact_shadow(center: Vector2, radii: Vector2, alpha := 0.14) -> void:
	_draw_ellipse(center, radii, Color(0.02, 0.02, 0.015, alpha))
