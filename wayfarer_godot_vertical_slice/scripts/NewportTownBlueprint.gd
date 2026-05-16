extends RefCounted
class_name NewportTownBlueprint

const TILE := 32
const MAP_TILES := Vector2i(50, 32)
const WORLD_SIZE := Vector2(MAP_TILES.x * TILE, MAP_TILES.y * TILE)
const G410_STARTER_HARBOR_TOWN := true
const G49_STREET_VIGNETTE := false
const G48_PROOF_STREET := false
const G46_PROOF_FRAME := false
const G47_CALIBRATION_MODE := false
const NPCS_ENABLED := false
const PLAYER_SPAWN := Vector2(675, 612)
const EDRIN_SPAWN := Vector2(-800, -800)
const G414A_STREET_WALL_CURB_DATUM_Y := 17.77
const G415_VISUAL_ACCEPTANCE_SCORE_TARGET := 8.5
const G416_SURFACE_KIT_PASS := "G-4.16"
const G418_ASSET_FACTORY_PASS := "G-4.18B"
const G418C_GREEN_ORIGIN_QUARANTINE_PASS := "G-4.18C"
const G418D_ATELIER_CARGO_PASS := "G-4.18D"
const G419A_DOCK_CLUTTER_ATELIER_PASS := "G-4.19A"
const G419B_VISUAL_PRODUCTION_AUDIT_PASS := "G-4.19B"
const G420A_ENVIRONMENTAL_BELIEVABILITY_PASS := "G-4.20A"
const G420B_TOWN_IDENTITY_PASS := "G-4.20B"

const HARBORFRONT_BUILDING_IDS := [
	"b_inn_tavern",
	"b_mercantile",
	"b_counting_house",
	"b_chandlery_front",
	"b_shop_house",
]

const STARTER_HARBOR_BUILDING_IDS := [
	"b_inn_tavern",
	"b_mercantile",
	"b_counting_house",
	"b_chandlery_front",
	"b_shop_house",
	"b_printer_rowhouse",
	"b_dock_storehouse",
	"b_wharf_boathouse",
	"b_dock_warehouse",
	"b_market_shed",
	"b_custom_house",
	"b_clerk_townhouse",
	"b_res_small",
	"b_large_residence",
	"b_boarding_house",
	"b_dockworker_rowhouse",
	"b_cooperage_shed",
]

const G413B_ACTIVE_INFILL_BUILDING_IDS := [
	"b_printer_rowhouse",
	"b_clerk_townhouse",
	"b_dockworker_rowhouse",
]

const G413B_DEFERRED_INFILL_SLOT_IDS := [
	"slot_counting_chandlery_lane_edge_shop",
	"slot_shop_market_townhouse_pair",
	"slot_cottage_customs_inland_townhouse",
]

const STARTER_HARBOR_PLANNED_LOT_IDS := [
	"lot_west_fishmonger_future",
]

const G413B_ROWHOUSE_INFILL_SLOT_IDS := [
	"slot_tavern_mercantile_brick_rowhouse",
	"slot_counting_chandlery_lane_edge_shop",
	"slot_shop_market_townhouse_pair",
	"slot_cottage_customs_inland_townhouse",
	"slot_support_lane_boarding_gap",
	"slot_market_east_edge_narrow_shop",
]

const FULL_TOWN_BUILDING_IDS := [
	"b_boathouse",
	"b_dock_storehouse",
	"b_market_shed",
	"b_inn_tavern",
	"b_mercantile",
	"b_counting_house",
	"b_chandlery_front",
	"b_shop_house",
	"b_custom_house",
	"b_village_hall",
	"b_res_small",
	"b_townhouse_row_a",
	"b_townhouse_row_b",
	"b_service_dependency",
	"b_hunter_lodge",
	"b_res_large",
	"b_georgian_residence",
	"b_elite_mansion",
	"b_prestige_block",
]

const PROOF_STREET_IDS := [
	"b_mercantile",
	"b_counting_house",
	"b_chandlery_front",
]

const BUILDING_IDS := STARTER_HARBOR_BUILDING_IDS

static func base_ground_rect() -> Rect2i:
	return Rect2i(0, 0, MAP_TILES.x, MAP_TILES.y)

static func district_rects() -> Array:
	if G410_STARTER_HARBOR_TOWN:
		return [
			{"id": "inland_residential_civic", "rect": Rect2i(6, 5, 42, 8), "base": Color("#617a55"), "alt": Color("#4d6848")},
			{"id": "support_lane", "rect": Rect2i(7, 11, 41, 5), "base": Color("#5a744f"), "alt": Color("#486743")},
			{"id": "harborfront_commercial", "rect": Rect2i(6, 15, 42, 6), "base": Color("#596f50"), "alt": Color("#465f43")},
			{"id": "working_wharf", "rect": Rect2i(6, 20, 42, 5), "base": Color("#5f6750"), "alt": Color("#4d5944")},
			{"id": "harbor_water", "rect": Rect2i(0, 24, MAP_TILES.x, 8), "base": Color("#2f7184"), "alt": Color("#1f5369")},
		]
	return [
		{"id": "upper_residential_terrace", "rect": Rect2i(7, 0, 30, 8), "base": Color("#6e8d5d"), "alt": Color("#527449")},
		{"id": "civic_district", "rect": Rect2i(18, 6, 16, 8), "base": Color("#708b63"), "alt": Color("#58754f")},
		{"id": "waterfront_commercial", "rect": Rect2i(8, 11, 32, 8), "base": Color("#657f55"), "alt": Color("#506f49")},
		{"id": "service_outfitter_lane", "rect": Rect2i(3, 8, 43, 12), "base": Color("#5c784f"), "alt": Color("#486b43")},
		{"id": "harbor_wharf", "rect": Rect2i(7, 17, 34, 9), "base": Color("#626f55"), "alt": Color("#4b5e48")},
	]

static func primary_roads() -> Array:
	if G410_STARTER_HARBOR_TOWN:
		return [
			Rect2i(7, 18, 42, 3),
			Rect2i(10, 13, 30, 2),
			Rect2i(20, 11, 3, 10),
		]
	if G49_STREET_VIGNETTE:
		return [
			Rect2i(10, 18, 27, 3),
		]
	if G48_PROOF_STREET:
		return [
			Rect2i(8, 18, 34, 4),
		]
	if G47_CALIBRATION_MODE:
		return [
			Rect2i(3, 11, 18, 3),
			Rect2i(28, 11, 18, 3),
			Rect2i(3, 25, 18, 3),
			Rect2i(28, 25, 18, 3),
		]
	if G46_PROOF_FRAME:
		return [
			Rect2i(10, 16, 28, 1),
			Rect2i(10, 17, 28, 1),
			Rect2i(10, 18, 28, 1),
			Rect2i(10, 19, 28, 1),
		]
	return [
		Rect2i(8, 18, 28, 1),
		Rect2i(8, 19, 28, 1),
		Rect2i(20, 7, 1, 12),
		Rect2i(12, 7, 21, 1),
	]

static func secondary_roads() -> Array:
	if G410_STARTER_HARBOR_TOWN:
		return [
			Rect2i(8, 16, 40, 2),
			Rect2i(8, 21, 40, 3),
			Rect2i(12, 13, 2, 11),
			Rect2i(34, 13, 2, 11),
		]
	if G49_STREET_VIGNETTE:
		return [
			Rect2i(13, 17, 21, 1),
		]
	if G48_PROOF_STREET:
		return [
			Rect2i(11, 17, 28, 1),
		]
	if G47_CALIBRATION_MODE:
		return []
	if G46_PROOF_FRAME:
		return []
	return [
		Rect2i(8, 14, 25, 1),
		Rect2i(20, 12, 13, 1),
		Rect2i(12, 7, 1, 12),
		Rect2i(17, 7, 1, 12),
		Rect2i(27, 7, 1, 12),
		Rect2i(32, 9, 1, 10),
		Rect2i(33, 14, 8, 1),
	]

static func service_lanes() -> Array:
	if G410_STARTER_HARBOR_TOWN:
		return [
			Rect2i(8, 12, 9, 1),
			Rect2i(26, 12, 22, 1),
			Rect2i(9, 15, 7, 1),
			Rect2i(36, 15, 12, 1),
			Rect2i(21, 21, 3, 5),
			Rect2i(32, 22, 2, 4),
		]
	if G49_STREET_VIGNETTE:
		return []
	if G48_PROOF_STREET:
		return []
	if G47_CALIBRATION_MODE:
		return []
	if G46_PROOF_FRAME:
		return []
	return [
		Rect2i(5, 10, 1, 9),
		Rect2i(37, 10, 1, 9),
		Rect2i(42, 10, 1, 9),
	]

static func civic_square_rects() -> Array:
	if G410_STARTER_HARBOR_TOWN:
		return [
			Rect2i(18, 10, 8, 4),
			Rect2i(12, 11, 4, 2),
			Rect2i(31, 11, 5, 2),
		]
	return [
		Rect2i(19, 10, 8, 4),
		Rect2i(18, 6, 15, 1),
		Rect2i(13, 8, 4, 2),
	]

static func waterfront_apron_rects() -> Array:
	if G410_STARTER_HARBOR_TOWN:
		return [
			Rect2i(7, 16, 36, 2),
			Rect2i(7, 20, 36, 1),
			Rect2i(8, 21, 34, 3),
		]
	return [
		Rect2i(8, 15, 25, 2),
		Rect2i(8, 17, 25, 1),
		Rect2i(8, 19, 25, 1),
	]

static func pier_rects() -> Array:
	if G410_STARTER_HARBOR_TOWN:
		return [
			{"id": "west_service_pier", "rect": Rect2i(11, 22, 1, 4)},
			{"id": "west_dock_warehouse_landing", "rect": Rect2i(11, 25, 5, 1)},
			{"id": "central_market_pier", "rect": Rect2i(22, 22, 1, 4)},
			{"id": "central_boathouse_landing", "rect": Rect2i(22, 25, 6, 1)},
			{"id": "east_storehouse_pier", "rect": Rect2i(37, 22, 1, 4)},
			{"id": "east_storehouse_landing", "rect": Rect2i(37, 25, 5, 1)},
		]
	if G49_STREET_VIGNETTE:
		return [
			{"id": "street_vignette_short_pier", "rect": Rect2i(20, 21, 3, 5)},
		]
	if G48_PROOF_STREET:
		return [
			{"id": "variant_d_center_pier", "rect": Rect2i(24, 22, 3, 6)},
		]
	if G47_CALIBRATION_MODE:
		return []
	if G46_PROOF_FRAME:
		return [
			{"id": "proof_wharf_hint", "rect": Rect2i(23, 20, 3, 5)},
		]
	return [
		{"id": "west_fish_pier", "rect": Rect2i(10, 18, 1, 8)},
		{"id": "west_commercial_pier", "rect": Rect2i(16, 18, 1, 7)},
		{"id": "central_civic_pier", "rect": Rect2i(19, 17, 1, 10)},
		{"id": "counting_house_pier", "rect": Rect2i(23, 18, 1, 7)},
		{"id": "east_market_pier", "rect": Rect2i(29, 18, 1, 7)},
	]

static func water_rects() -> Array:
	if G410_STARTER_HARBOR_TOWN:
		return [
			Rect2i(0, 24, MAP_TILES.x, 8),
		]
	if G49_STREET_VIGNETTE:
		return [
			Rect2i(0, 24, MAP_TILES.x, 8),
		]
	if G48_PROOF_STREET:
		return [
			Rect2i(0, 23, MAP_TILES.x, 9),
		]
	if G47_CALIBRATION_MODE:
		return []
	if G46_PROOF_FRAME:
		return [
			Rect2i(0, 22, MAP_TILES.x, 10),
		]
	return [
		Rect2i(0, 20, MAP_TILES.x, 12),
	]

static func wharf_support_rects() -> Array:
	if G410_STARTER_HARBOR_TOWN:
		return [
			Rect2i(8, 21, 8, 3),
			Rect2i(20, 21, 9, 3),
			Rect2i(32, 21, 8, 3),
		]
	return [
		Rect2i(9, 20, 5, 4),
		Rect2i(17, 20, 6, 4),
		Rect2i(24, 20, 5, 4),
	]

static func route_rects() -> Array:
	var rects: Array = []
	rects.append_array(primary_roads())
	rects.append_array(secondary_roads())
	rects.append_array(service_lanes())
	for pier in pier_rects():
		rects.append(pier["rect"])
	return rects

static func route_tiles() -> Array:
	return _tiles_from_rects(route_rects())

static func wharf_walkable_tiles() -> Array:
	if G410_STARTER_HARBOR_TOWN:
		var starter_rects: Array = [Rect2i(8, 21, 34, 3)]
		for pier in pier_rects():
			starter_rects.append(pier["rect"])
		return _tiles_from_rects(starter_rects)
	var rects: Array = [Rect2i(8, 18, 25, 2)]
	for pier in pier_rects():
		rects.append(pier["rect"])
	return _tiles_from_rects(rects)

static func water_collision_tiles() -> Array:
	var passable := _tile_key_set(wharf_walkable_tiles())
	var blocked: Array = []
	for tile in _tiles_from_rects(water_rects()):
		if not passable.has(_key(tile)):
			blocked.append(tile)
	return blocked

static func reachability_targets() -> Dictionary:
	if G410_STARTER_HARBOR_TOWN:
		return {
			"harborfront_main_street": Vector2i(21, 19),
			"west_tavern_frontage": Vector2i(10, 18),
			"mercantile_frontage": Vector2i(17, 18),
			"counting_house_frontage": Vector2i(22, 18),
			"chandlery_frontage": Vector2i(27, 18),
			"east_storefront_frontage": Vector2i(32, 18),
			"working_wharf_edge": Vector2i(22, 22),
			"west_service_pier": Vector2i(11, 25),
			"west_dock_warehouse_landing": Vector2i(13, 25),
			"central_market_pier": Vector2i(22, 25),
			"central_boathouse_landing": Vector2i(24, 25),
			"east_storehouse_pier": Vector2i(37, 25),
			"east_storehouse_landing": Vector2i(39, 25),
			"inland_cross_lane": Vector2i(21, 13),
			"west_support_lane": Vector2i(13, 13),
			"east_support_lane": Vector2i(35, 13),
		}
	if G49_STREET_VIGNETTE:
		return {
			"mercantile_frontage": Vector2i(16, 18),
			"counting_house_frontage": Vector2i(21, 18),
			"chandlery_frontage": Vector2i(26, 18),
			"street_walking_lane": Vector2i(21, 19),
			"harbor_edge_context": Vector2i(21, 21),
		}
	if G48_PROOF_STREET:
		return {
			"left_storefront": Vector2i(12, 18),
			"center_storefront": Vector2i(24, 18),
			"right_storefront": Vector2i(36, 18),
			"narrow_street_lane": Vector2i(24, 20),
			"wharf_frontage": Vector2i(25, 22),
		}
	if G47_CALIBRATION_MODE:
		return {
			"variant_d_left_frontage": Vector2i(33, 26),
			"variant_d_center_walk": Vector2i(37, 26),
			"variant_d_right_frontage": Vector2i(41, 26),
		}
	if G46_PROOF_FRAME:
		return {
			"left_storefront": Vector2i(17, 18),
			"center_storefront": Vector2i(23, 18),
			"right_storefront": Vector2i(29, 18),
			"wharf_edge": Vector2i(23, 20),
		}
	return {
		"harbor_wharf_start": Vector2i(23, 19),
		"dockside_working_area": Vector2i(29, 19),
		"commercial_frontage": Vector2i(22, 18),
		"central_pier_frontage": Vector2i(19, 25),
		"civic_landmark": Vector2i(20, 12),
		"residential_edge": Vector2i(18, 7),
		"service_lane": Vector2i(37, 14),
	}

static func proof_street_ids() -> Array:
	if G410_STARTER_HARBOR_TOWN:
		return HARBORFRONT_BUILDING_IDS.duplicate()
	return PROOF_STREET_IDS.duplicate()

static func proof_street_walk_targets() -> Dictionary:
	if G410_STARTER_HARBOR_TOWN:
		return {
			"tavern_door": Vector2i(10, 18),
			"mercantile_door": Vector2i(17, 18),
			"counting_house_door": Vector2i(22, 18),
			"chandlery_door": Vector2i(27, 18),
			"shop_house_door": Vector2i(32, 18),
			"harborfront_walk": Vector2i(22, 19),
			"dock_access": Vector2i(23, 22),
			"inland_return_lane": Vector2i(21, 13),
		}
	if G49_STREET_VIGNETTE:
		return {
			"mercantile_door": Vector2i(16, 18),
			"counting_house_door": Vector2i(21, 18),
			"chandlery_door": Vector2i(26, 18),
			"storefront_walk": Vector2i(21, 19),
		}
	if G48_PROOF_STREET:
		return {
			"mercantile_frontage": Vector2i(13, 18),
			"counting_house_frontage": Vector2i(20, 18),
			"chandlery_frontage": Vector2i(27, 18),
			"shop_house_frontage": Vector2i(34, 18),
			"street_lane": Vector2i(24, 20),
		}
	if G47_CALIBRATION_MODE:
		return {
			"variant_a_reference": Vector2i(12, 12),
			"variant_b_smaller_player": Vector2i(37, 12),
			"variant_c_camera_vignette": Vector2i(12, 26),
			"variant_d_integrated_stoop": Vector2i(37, 26),
		}
	if G46_PROOF_FRAME:
		return {
			"mercantile_frontage": Vector2i(17, 17),
			"counting_house_frontage": Vector2i(23, 17),
			"chandlery_frontage": Vector2i(29, 17),
		}
	return {
		"west_frontage": Vector2i(11, 18),
		"center_frontage": Vector2i(22, 18),
		"east_frontage": Vector2i(34, 18),
	}

static func route_debug_probes() -> Array:
	if G410_STARTER_HARBOR_TOWN:
		return [
			_route_probe("black_box_marked_lane", Vector2(500.0, 536.0), "G-4.13A.1 marked lane throat north of mercantile", "black-box"),
			_route_probe("tavern_mercantile_rear_lane", Vector2(500.0, 528.0), "rear lane between tavern, mercantile, and small residence", "tav/merc"),
			_route_probe("tavern_mercantile_east_throat", Vector2(562.0, 548.0), "east edge of the tavern/mercantile connector", "east throat"),
			_route_probe("road_behind_b_mercantile", Vector2(492.0, 526.0), "road behind b_mercantile", "merc rear"),
			_route_probe("road_behind_b_counting_house", Vector2(680.0, 526.0), "road behind b_counting_house", "count rear"),
			_route_probe("lane_near_b_res_small", Vector2(492.0, 500.0), "lane near b_res_small", "res lane"),
			_route_probe("central_rear_road", Vector2(748.0, 526.0), "central rear road", "rear C"),
			_route_probe("east_rear_road", Vector2(1040.0, 526.0), "east rear road", "rear E"),
			_route_probe("commercial_street", Vector2(824.0, 600.0), "commercial street", "comm street"),
			_route_probe("commercial_to_dock_access", Vector2(672.0, 652.0), "commercial row to dock layer access", "dock access"),
			_route_probe("dock_boardwalk", Vector2(824.0, 710.0), "dock boardwalk", "dock walk"),
			_route_probe("central_cross_lane", Vector2(672.0, 430.0), "inland road to commercial row access", "cross C"),
			_route_probe("support_lane_woodpile_road", Vector2(424.0, 430.0), "old support-lane woodpile road position", "wood road"),
			_route_probe("clerk_rowhouse_front_walk", Vector2(420.0, 604.0), "commercial street approach below the tavern/mercantile clerk-rowhouse infill", "clerk row"),
			_route_probe("market_east_edge_front_walk", Vector2(1430.0, 604.0), "commercial street approach below the east market-edge printer rowhouse", "market edge"),
			_route_probe("support_boarding_gap_walk", Vector2(1380.0, 418.0), "east support-lane return below the dockworker rowhouse street wall", "dockworker"),
		]
	return []

static func lived_in_detail_count() -> int:
	if G410_STARTER_HARBOR_TOWN:
		return 168
	if G49_STREET_VIGNETTE:
		return 38
	if G48_PROOF_STREET:
		return 24
	if G47_CALIBRATION_MODE:
		return 26
	if G46_PROOF_FRAME:
		return 12
	return 52

static func detail_blockers() -> Array:
	if G410_STARTER_HARBOR_TOWN:
		return [
			_blocker("tavern_loading_barrels", Rect2(334, 582, 30, 16)),
			_blocker("mercantile_front_crates", Rect2(506, 586, 28, 14)),
			_blocker("west_alley_rope", Rect2(616, 586, 22, 14)),
			_blocker("counting_house_goods_left", Rect2(604, 582, 34, 16)),
			_blocker("counting_house_goods_right", Rect2(774, 584, 30, 16)),
			_blocker("chandlery_rope_stack", Rect2(930, 586, 30, 14)),
			_blocker("shop_house_crates", Rect2(1062, 584, 32, 16)),
			_blocker("wharf_west_cargo", Rect2(370, 666, 36, 20)),
			_blocker("wharf_market_table", Rect2(706, 656, 62, 20)),
			_blocker("wharf_east_barrels", Rect2(1024, 666, 34, 22)),
			_blocker("west_pier_posts", Rect2(374, 758, 34, 18)),
			_blocker("central_pier_cargo", Rect2(746, 742, 36, 20)),
			_blocker("east_pier_net", Rect2(1070, 746, 34, 20)),
			_blocker("inland_civic_bench", Rect2(628, 374, 42, 16)),
			_blocker("support_lane_woodpile", Rect2(404, 462, 40, 18)),
		]
	if G49_STREET_VIGNETTE:
		return [
			_blocker("mercantile_base_barrels", Rect2(428, 544, 26, 18)),
			_blocker("west_loading_crates", Rect2(522, 548, 28, 18)),
			_blocker("counting_house_left_goods", Rect2(592, 542, 32, 18)),
			_blocker("counting_house_right_barrels", Rect2(730, 546, 28, 18)),
			_blocker("east_alley_rope_stack", Rect2(786, 548, 30, 18)),
			_blocker("chandlery_side_crates", Rect2(890, 550, 28, 18)),
			_blocker("foreground_post_stack", Rect2(398, 678, 24, 16)),
		]
	if G48_PROOF_STREET:
		return [
			_blocker("street_barrels_left", Rect2(332, 548, 28, 18)),
			_blocker("counting_house_crates", Rect2(650, 548, 34, 18)),
			_blocker("chandlery_rope_stack", Rect2(882, 550, 30, 18)),
			_blocker("shop_house_barrels", Rect2(1128, 548, 30, 18)),
			_blocker("wharf_post_stack", Rect2(456, 704, 28, 18)),
		]
	if G47_CALIBRATION_MODE:
		return []
	if G46_PROOF_FRAME:
		return []
	return [
		_blocker("inn_barrels", Rect2(330, 534, 34, 18)),
		_blocker("mercantile_crates", Rect2(488, 536, 38, 20)),
		_blocker("counting_house_crates", Rect2(690, 536, 40, 20)),
		_blocker("chandlery_rope_stack", Rect2(900, 536, 34, 20)),
		_blocker("market_table_west", Rect2(622, 650, 62, 20)),
		_blocker("market_table_east", Rect2(756, 650, 62, 20)),
		_blocker("dock_storehouse_barrels", Rect2(984, 626, 34, 22)),
		_blocker("boathouse_crates", Rect2(304, 626, 42, 22)),
		_blocker("central_pier_posts", Rect2(616, 790, 34, 18)),
		_blocker("civic_bench_west", Rect2(600, 366, 38, 16)),
		_blocker("civic_bench_east", Rect2(792, 366, 38, 16)),
		_blocker("residential_planter", Rect2(414, 230, 40, 18)),
		_blocker("service_yard_barrels", Rect2(1208, 532, 34, 22)),
		_blocker("harbor_cottage_woodpile", Rect2(166, 486, 38, 18)),
		_blocker("wharf_north_post_stack", Rect2(560, 648, 26, 18)),
		_blocker("pier_cargo_stack", Rect2(840, 730, 34, 20)),
	]

static func player_spawn_tile() -> Vector2i:
	return Vector2i(floori(PLAYER_SPAWN.x / TILE), floori(PLAYER_SPAWN.y / TILE))

static func building_specs() -> Array:
	if G410_STARTER_HARBOR_TOWN:
		return [
			_catalog_building("b_inn_tavern", "harborfront_commercial", "commercial", Vector2(8.95, G414A_STREET_WALL_CURB_DATUM_Y), true),
			_catalog_building("b_mercantile", "harborfront_commercial", "commercial", Vector2(17.86, G414A_STREET_WALL_CURB_DATUM_Y), true),
			_catalog_building("b_counting_house", "harborfront_commercial", "commercial", Vector2(22.40, G414A_STREET_WALL_CURB_DATUM_Y), true),
			_catalog_building("b_chandlery_front", "harborfront_commercial", "commercial", Vector2(27.47, G414A_STREET_WALL_CURB_DATUM_Y), true),
			_catalog_building("b_shop_house", "harborfront_commercial", "commercial", Vector2(32.52, G414A_STREET_WALL_CURB_DATUM_Y), true),
			_catalog_building("b_printer_rowhouse", "harborfront_commercial", "rowhouse_printer", Vector2(42.72, G414A_STREET_WALL_CURB_DATUM_Y)),
			_catalog_building("b_market_shed", "harborfront_commercial", "market", Vector2(38.10, G414A_STREET_WALL_CURB_DATUM_Y)),
			_catalog_building("b_dock_storehouse", "working_wharf", "dock_services", Vector2(41.35, 27.55)),
			_catalog_building("b_wharf_boathouse", "working_wharf", "dock_services", Vector2(28.05, 27.65)),
			_catalog_building("b_dock_warehouse", "working_wharf", "dock_services", Vector2(15.20, 27.55)),
			_catalog_building("b_custom_house", "inland_residential_civic", "customs_house", Vector2(25.10, 11.70)),
			_catalog_building("b_clerk_townhouse", "harborfront_commercial", "rowhouse_clerk_lodging", Vector2(13.85, G414A_STREET_WALL_CURB_DATUM_Y)),
			_catalog_building("b_res_small", "inland_residential_civic", "residential", Vector2(13.65, 11.45)),
			_catalog_building("b_large_residence", "inland_residential_civic", "civic_residence", Vector2(31.80, 11.55)),
			_catalog_building("b_boarding_house", "support_lane", "boarding_house", Vector2(38.35, 11.70)),
			_catalog_building("b_dockworker_rowhouse", "support_lane", "rowhouse_dockworker_lodging", Vector2(42.79, 12.10)),
			_catalog_building("b_cooperage_shed", "support_lane", "cooperage", Vector2(8.25, 11.85)),
		]
	if G49_STREET_VIGNETTE:
		return [
			_proof_street_building("b_mercantile", "Mercantile", "mercantile_shop", Vector2(14.9, 17.55), Vector2(193.0, 421.0), Vector2(88.0, 30.0), Vector2(0.0, 24.0), 122.0, Vector2(138.0, 17.0), 150.0, {
				"occupied_rect": Rect2(Vector2(-82.0, -160.0), Vector2(164.0, 172.0)),
			}),
			_proof_street_building("b_counting_house", "Counting House", "newport_counting_house_civic_exchange", Vector2(20.55, 17.55), Vector2(223.0, 340.0), Vector2(104.0, 32.0), Vector2(0.0, 25.0), 150.0, Vector2(166.0, 18.0), 190.0, {
				"occupied_rect": Rect2(Vector2(-104.0, -166.0), Vector2(208.0, 178.0)),
			}),
			_proof_street_building("b_chandlery_front", "Chandlery", "newport_chandlery_outfitter_front", Vector2(25.95, 17.55), Vector2(211.5, 370.0), Vector2(98.0, 31.0), Vector2(0.0, 24.0), 132.0, Vector2(154.0, 18.0), 181.0, {
				"occupied_rect": Rect2(Vector2(-92.0, -168.0), Vector2(184.0, 180.0)),
			}),
		]
	if G48_PROOF_STREET:
		return [
			_proof_street_building("b_mercantile", "Mercantile", "mercantile_shop", Vector2(13.1, 17.75), Vector2(218.0, 427.0), Vector2(88.0, 30.0), Vector2(0.0, 20.0), 118.0, Vector2(132.0, 17.0), 146.0),
			_proof_street_building("b_counting_house", "Counting House", "newport_counting_house_civic_exchange", Vector2(20.2, 17.75), Vector2(224.0, 382.0), Vector2(104.0, 32.0), Vector2(0.0, 21.0), 142.0, Vector2(156.0, 18.0), 174.0),
			_proof_street_building("b_chandlery_front", "Chandlery", "newport_chandlery_outfitter_front", Vector2(27.3, 17.75), Vector2(196.0, 430.0), Vector2(98.0, 31.0), Vector2(0.0, 21.0), 126.0, Vector2(148.0, 18.0), 152.0),
			_proof_street_building("b_shop_house", "Shop House", "newport_shopfront_awning", Vector2(34.3, 17.75), Vector2(230.0, 436.0), Vector2(92.0, 30.0), Vector2(0.0, 20.0), 118.0, Vector2(136.0, 17.0), 150.0),
		]
	if G47_CALIBRATION_MODE:
		return [
			_calibration_building("g47_a_mercantile", "A Mercantile", "mercantile_shop", Vector2(8.0, 9.7), Vector2(218.0, 427.0), 138.0, Vector2(96.0, 34.0), Vector2(0.0, 29.0), 116.0, Vector2(120.0, 20.0), "A"),
			_calibration_building("g47_a_counting_house", "A Counting House", "newport_counting_house_civic_exchange", Vector2(14.2, 9.7), Vector2(224.0, 382.0), 166.0, Vector2(112.0, 36.0), Vector2(0.0, 30.0), 138.0, Vector2(140.0, 22.0), "A"),
			_calibration_building("g47_b_mercantile", "B Mercantile", "mercantile_shop", Vector2(33.0, 9.7), Vector2(218.0, 427.0), 150.0, Vector2(96.0, 34.0), Vector2(0.0, 26.0), 118.0, Vector2(122.0, 20.0), "B"),
			_calibration_building("g47_b_counting_house", "B Counting House", "newport_counting_house_civic_exchange", Vector2(39.2, 9.7), Vector2(224.0, 382.0), 178.0, Vector2(112.0, 36.0), Vector2(0.0, 28.0), 142.0, Vector2(146.0, 22.0), "B"),
			_calibration_building("g47_c_mercantile", "C Mercantile", "mercantile_shop", Vector2(8.0, 23.9), Vector2(218.0, 427.0), 148.0, Vector2(92.0, 32.0), Vector2(0.0, 24.0), 116.0, Vector2(124.0, 18.0), "C"),
			_calibration_building("g47_c_counting_house", "C Counting House", "newport_counting_house_civic_exchange", Vector2(14.2, 23.9), Vector2(224.0, 382.0), 176.0, Vector2(108.0, 34.0), Vector2(0.0, 25.0), 140.0, Vector2(148.0, 20.0), "C"),
			_calibration_building("g47_d_mercantile", "D Mercantile", "mercantile_shop", Vector2(33.2, 23.75), Vector2(218.0, 427.0), 146.0, Vector2(88.0, 30.0), Vector2(0.0, 20.0), 118.0, Vector2(132.0, 17.0), "D"),
			_calibration_building("g47_d_counting_house", "D Counting House", "newport_counting_house_civic_exchange", Vector2(39.4, 23.75), Vector2(224.0, 382.0), 174.0, Vector2(104.0, 32.0), Vector2(0.0, 21.0), 142.0, Vector2(156.0, 18.0), "D"),
		]
	if G46_PROOF_FRAME:
		return [
			_proof_street_building("b_mercantile", "Mercantile", "mercantile_shop", Vector2(17.2, 15.95), Vector2(218.0, 427.0), Vector2(92.0, 32.0), Vector2(0.0, 26.0), 112.0, Vector2(116.0, 19.0), 138.0),
			_proof_street_building("b_counting_house", "Counting House", "newport_counting_house_civic_exchange", Vector2(23.0, 15.95), Vector2(224.0, 382.0), Vector2(104.0, 34.0), Vector2(0.0, 28.0), 126.0, Vector2(128.0, 20.0), 166.0),
			_proof_street_building("b_chandlery_front", "Chandlery", "newport_chandlery_outfitter_front", Vector2(29.1, 15.95), Vector2(196.0, 430.0), Vector2(98.0, 34.0), Vector2(0.0, 27.0), 118.0, Vector2(120.0, 20.0), 152.0),
		]
	return [
		_building("b_boathouse", "Boathouse", "newport_wharf_boathouse_large", "harbor_wharf", "harbor", Vector2(10.7, 21.2), 4.0, 1.0),
		_building("b_dock_storehouse", "Dock Storehouse", "newport_dockside_storehouse_long", "harbor_wharf", "harbor", Vector2(30.3, 21.1), 4.0, 1.0),
		_building("b_market_shed", "Market Shed", "newport_market_shed_stalls", "harbor_wharf", "harbor", Vector2(21.4, 21.0), 3.0, 1.0),
		_proof_street_building("b_inn_tavern", "Inn & Tavern", "inn_tavern_v1", Vector2(11.0, 17.05), Vector2(192.5, 350.0), Vector2(154.0, 42.0), Vector2(0.0, 34.0), 184.0, Vector2(184.0, 28.0)),
		_proof_street_building("b_mercantile", "Mercantile", "mercantile_shop", Vector2(16.3, 17.05), Vector2(218.0, 427.0), Vector2(110.0, 34.0), Vector2(0.0, 32.0), 136.0, Vector2(132.0, 23.0)),
		_proof_street_building("b_counting_house", "Counting House", "newport_counting_house_civic_exchange", Vector2(22.1, 17.05), Vector2(224.0, 382.0), Vector2(132.0, 36.0), Vector2(0.0, 34.0), 162.0, Vector2(156.0, 24.0)),
		_proof_street_building("b_chandlery_front", "Chandlery", "newport_chandlery_outfitter_front", Vector2(28.1, 17.05), Vector2(196.0, 430.0), Vector2(124.0, 36.0), Vector2(0.0, 34.0), 148.0, Vector2(148.0, 24.0)),
		_proof_street_building("b_shop_house", "Shop House", "newport_shopfront_awning", Vector2(33.7, 17.05), Vector2(230.0, 436.0), Vector2(116.0, 34.0), Vector2(0.0, 32.0), 136.0, Vector2(140.0, 22.0)),
		_building("b_custom_house", "Custom House", "newport_custom_house_civic_front", "civic_district", "civic", Vector2(25.2, 11.7), 3.8, 1.0),
		_building("b_village_hall", "Village Hall", "village_hall_meeting_house", "civic_district", "civic", Vector2(20.0, 11.6), 4.0, 1.0),
		_building("b_res_small", "Harbor Cottage", "residence_small", "service_outfitter_lane", "service", Vector2(6.2, 15.6), 2.3, 1.0),
		_building("b_townhouse_row_a", "Townhouse Row A", "newport_narrow_merchant_townhouse_a", "waterfront_commercial", "commercial", Vector2(34.8, 12.4), 2.1, 1.0),
		_building("b_townhouse_row_b", "Townhouse Row B", "newport_modest_clapboard_residence_a", "service_outfitter_lane", "service", Vector2(37.8, 10.1), 2.4, 1.0),
		_building("b_service_dependency", "Service Dependency", "service_dependency_shed", "service_outfitter_lane", "service", Vector2(38.4, 17.1), 2.1, 1.0),
		_building("b_hunter_lodge", "Hunter Lodge", "hunter_lodge_or_outfitter", "service_outfitter_lane", "rural", Vector2(5.8, 18.5), 2.4, 1.0),
		_building("b_res_large", "Large Residence", "residence_large", "upper_residential_terrace", "residential", Vector2(13.2, 7.0), 3.3, 1.0),
		_building("b_georgian_residence", "Georgian Residence", "newport_georgian_merchant_residence_a", "upper_residential_terrace", "residential", Vector2(18.0, 7.3), 3.4, 1.0),
		_building("b_elite_mansion", "Elite Mansion", "newport_elite_mansion_white", "upper_residential_terrace", "residential", Vector2(24.7, 7.0), 3.7, 1.0),
		_building("b_prestige_block", "Prestige Block", "newport_formal_townhouse_block_a", "upper_residential_terrace", "residential", Vector2(31.2, 7.3), 3.6, 1.0),
	]

static func g415_layout_rules() -> Dictionary:
	if not G410_STARTER_HARBOR_TOWN:
		return {}
	return {
		"b_inn_tavern": _layout_rule("parcel_tavern_anchor", "commercial", 584.0, 24.0, 12.0, Vector2(286.0, 616.0), Rect2(314, 578, 58, 26), Rect2(220, 548, 176, 70), "commercial_stone", "tavern loading stays on the west apron while the front door stays clear"),
		"b_clerk_townhouse": _layout_rule("parcel_clerk_rowhouse", "commercial", 584.0, 22.0, 4.0, Vector2(443.0, 616.0), Rect2(410, 580, 48, 20), Rect2(386, 550, 116, 68), "rowhouse_stone", "brick rowhouse remains attached to the tavern/mercantile run but keeps a distinct stoop"),
		"b_mercantile": _layout_rule("parcel_harbor_mercantile", "commercial", 584.0, 22.0, 10.0, Vector2(565.0, 616.0), Rect2(502, 582, 78, 24), Rect2(498, 550, 136, 68), "commercial_stone", "trade crates sit on the side apron; the doorway prompt zone remains open"),
		"b_counting_house": _layout_rule("parcel_counting_house", "commercial", 584.0, 22.0, 12.0, Vector2(710.0, 616.0), Rect2(604, 580, 205, 24), Rect2(612, 548, 196, 70), "civic_stone", "ledger crates flank a formal front walk without crossing the central entry"),
		"b_chandlery_front": _layout_rule("parcel_chandlery", "commercial", 584.0, 22.0, 12.0, Vector2(873.0, 616.0), Rect2(912, 582, 58, 24), Rect2(806, 550, 154, 68), "commercial_stone", "rope work belongs to the east service slit, not the doorway"),
		"b_shop_house": _layout_rule("parcel_shop_house", "commercial", 584.0, 22.0, 16.0, Vector2(1019.0, 616.0), Rect2(1058, 580, 58, 24), Rect2(960, 550, 126, 68), "shop_stone", "the shop house gets a wider east gutter before the market parcel"),
		"b_market_shed": _layout_rule("parcel_market_shed", "market", 584.0, 32.0, 18.0, Vector2(1189.0, 620.0), Rect2(1128, 642, 142, 36), Rect2(1096, 548, 178, 72), "market_stone", "market tables sit in the wharf-facing trade band instead of pinching the shop facade"),
		"b_printer_rowhouse": _layout_rule("parcel_printer_rowhouse", "commercial", 584.0, 22.0, 12.0, Vector2(1340.0, 616.0), Rect2(1309, 580, 52, 24), Rect2(1284, 540, 124, 80), "rowhouse_stone", "printer frontage keeps the east-edge parcel spacing while the rowhouse now reads at full Newport scale"),
		"b_custom_house": _layout_rule("parcel_custom_house_green", "civic", 424.0, 44.0, 28.0, Vector2(803.0, 432.0), Rect2(744, 390, 120, 26), Rect2(692, 326, 224, 96), "civic_green", "customs house sits on a formal green with a road-facing walk"),
		"b_res_small": _layout_rule("parcel_harbor_cottage_yard", "residential", 424.0, 42.0, 24.0, Vector2(437.0, 432.0), Rect2(392, 394, 92, 24), Rect2(360, 326, 154, 88), "residential_yard", "small residence gets a visible yard and path instead of floating on grass"),
		"b_large_residence": _layout_rule("parcel_harbor_residence_yard", "residential", 424.0, 42.0, 28.0, Vector2(1018.0, 432.0), Rect2(964, 394, 126, 24), Rect2(910, 326, 224, 92), "residential_yard", "large residence has a broad green parcel and walk down to the support road"),
		"b_boarding_house": _layout_rule("parcel_boarding_house_lane", "support", 424.0, 34.0, 12.0, Vector2(1227.0, 432.0), Rect2(1188, 392, 104, 26), Rect2(1160, 334, 146, 86), "support_yard", "boarding props stay in a lane-side yard"),
		"b_dockworker_rowhouse": _layout_rule("parcel_dockworker_rowhouse_lane", "support", 424.0, 34.0, 8.0, Vector2(1369.0, 432.0), Rect2(1330, 396, 100, 24), Rect2(1298, 346, 152, 78), "support_yard", "dockworker rowhouse keeps a hard support-lane frontage"),
		"b_cooperage_shed": _layout_rule("parcel_cooperage_yard", "support", 424.0, 30.0, 18.0, Vector2(264.0, 432.0), Rect2(232, 398, 76, 26), Rect2(204, 338, 128, 78), "support_yard", "cooperage barrels sit in a small work yard beside the support lane"),
		"b_dock_warehouse": _layout_rule("parcel_west_dock_warehouse", "dock", 708.0, 24.0, 28.0, Vector2(486.0, 758.0), Rect2(398, 716, 154, 48), Rect2(360, 704, 248, 154), "dock_plank", "warehouse cargo belongs on the west pier apron"),
		"b_wharf_boathouse": _layout_rule("parcel_wharf_boathouse", "dock", 708.0, 24.0, 30.0, Vector2(898.0, 758.0), Rect2(812, 716, 164, 48), Rect2(752, 704, 292, 162), "dock_plank", "boathouse work zone connects directly to the center pier"),
		"b_dock_storehouse": _layout_rule("parcel_east_dock_storehouse", "dock", 708.0, 24.0, 28.0, Vector2(1323.0, 758.0), Rect2(1238, 716, 154, 48), Rect2(1206, 704, 248, 154), "dock_plank", "east storehouse cargo stays on the wharf apron"),
	}

static func g415_layout_rule(building_id: String) -> Dictionary:
	return g415_layout_rules().get(building_id, {})

static func g415_visual_qa_rubric() -> Dictionary:
	return {
		"target_score": G415_VISUAL_ACCEPTANCE_SCORE_TARGET,
		"building_grounding": 8.6,
		"readable_doors": 8.7,
		"believable_spacing": 8.5,
		"prop_purposefulness": 8.6,
		"walkable_roads": 8.7,
		"harbor_identity": 8.6,
		"depth_y_sort_believability": 8.5,
		"screenshot_beauty": 8.5,
		"not_pasted_feel": 8.5,
	}

static func substitution_notes() -> Dictionary:
	return {
		"b_market_shed": "Uses the closest market/frontage shed cell from Newport pack B.",
		"b_service_dependency": "Uses the compact service shed from the base Hearthvale atlas.",
		"b_prestige_block": "Uses the formal townhouse block from Newport pack B.",
	}

static func starter_district_plan() -> Dictionary:
	return {
		"target_total_lots": "14-20",
		"active_building_count": STARTER_HARBOR_BUILDING_IDS.size(),
		"active_g413b_infill_count": G413B_ACTIVE_INFILL_BUILDING_IDS.size(),
		"active_g413b_infill_buildings": G413B_ACTIVE_INFILL_BUILDING_IDS,
		"deferred_g413b_infill_slots": G413B_DEFERRED_INFILL_SLOT_IDS,
		"planned_lot_count": STARTER_HARBOR_PLANNED_LOT_IDS.size(),
		"composition_pass": "G-4.13B.1",
		"footprint_pass": "G-4.13A",
		"density_pass": "G-4.13B",
		"layout_rules_pass": "G-4.15",
		"surface_kit_pass": G416_SURFACE_KIT_PASS,
		"asset_pipeline_pass": G418_ASSET_FACTORY_PASS,
		"green_origin_quarantine_pass": G418C_GREEN_ORIGIN_QUARANTINE_PASS,
		"atelier_cargo_pipeline_pass": G418D_ATELIER_CARGO_PASS,
		"dock_clutter_atelier_pack_pass": G419A_DOCK_CLUTTER_ATELIER_PASS,
		"visual_production_audit_pass": G419B_VISUAL_PRODUCTION_AUDIT_PASS,
		"environmental_believability_wave_pass": G420A_ENVIRONMENTAL_BELIEVABILITY_PASS,
		"town_identity_wave_pass": G420B_TOWN_IDENTITY_PASS,
		"hero_street_atlas_proof": "central commercial row uses G-4.18 temporary yellow generated atlas pieces for review composition; cargo proof placement uses the G-4.18D Newport atelier cargo sprites; dock clutter proof placement uses the G-4.19A atelier pack as the first city rollout pack from that standard; G-4.19B audits all current visual targets and moves future work to production waves; G-4.20A is the first mass environmental believability atelier wave for terrain edges, path transitions, shoreline dressing, and non-centerpiece building grounding; G-4.20B is the Town Identity atelier wave for signage, lamps, wayfinding, civic markers, market identity, and shopfront support; the failed G-4.18B green-origin dock proof is lab-only after G-4.18C",
		"green_origin_pipeline_pass": "G-4.18B",
		"green_origin_lab_mode": "F6 or --show-green-origin-lab; lab-only provenance proof, not normal review art",
		"yellow_review_art_policy": "temporary yellow review art may support prototype composition, scale, and gameplay only; yellow pixels cannot source final-commercial green assets",
		"layout_rule_count": g415_layout_rules().size(),
		"visual_acceptance_score_target": G415_VISUAL_ACCEPTANCE_SCORE_TARGET,
		"collision_model": "visual_bounds and lot_bounds are review/planning data; collision_footprint is the only blocking building body.",
		"clean_review_default": true,
		"surface_cohesion_gate": true,
		"newport_visual_cohesion_gate": true,
		"asset_provenance_gate": true,
		"player_style_deferred_note": "current player is temporary scale/debug art; after G-4.20B town identity and wayfinding, player/NPC sprite style still waits until the town environment has enough visual context",
		"tavern_inn_centerpiece_lock": "current Tavern/Inn remains REBUILD_REQUIRED_CENTERPIECE for a future brick Hotel Viking-inspired twin-stack chimney rebuild; G-4.20B may register temporary sign candidates but does not patch or rebuild it",
		"review_screenshot_mode": "F4 or --review-no-hud",
		"districts": [
			"harborfront_commercial",
			"working_wharf",
			"inland_residential_civic",
			"support_lane",
		],
		"district_identity": {
			"harborfront_commercial": "main working street with tavern, shops, exchange, chandlery, and market frontage",
			"working_wharf": "goods move from waterline platforms through pier fingers to the wharf apron and street",
			"inland_residential_civic": "customs administration and higher-status houses sit behind the commercial frontage",
			"support_lane": "cooperage and boarding-house support the harbor labor loop",
		},
		"movement_loop": [
			"harborfront_main_street",
			"commercial_rear_road",
			"mercantile_counting_house_rear_road",
			"dock_access",
			"working_wharf_edge",
			"inland_cross_lane",
			"support_lane_return",
		],
		"planned_g413b_infill_slots": G413B_ROWHOUSE_INFILL_SLOT_IDS,
		"future_story_hooks": [
			"printer_rowhouse_revolutionary_pamphlet_or_apprentice_errand",
			"clerk_townhouse_customs_lodging_family_dispute_or_artifact_hook",
			"dockworker_rowhouse_missing_person_neighbor_or_wharf_job_hook",
		],
	}

static func starter_lot_specs() -> Array:
	return [
		_lot("lot_tavern_anchor", "actual", "harborfront_commercial", "tavern", Rect2i(6, 13, 6, 5), "b_inn_tavern"),
		_lot("lot_mercantile_anchor", "actual", "harborfront_commercial", "mercantile", Rect2i(16, 13, 5, 5), "b_mercantile"),
		_lot("lot_counting_house_anchor", "actual", "harborfront_commercial", "civic_exchange", Rect2i(20, 12, 7, 6), "b_counting_house"),
		_lot("lot_chandlery_anchor", "actual", "harborfront_commercial", "chandlery", Rect2i(25, 13, 6, 5), "b_chandlery_front"),
		_lot("lot_shop_house_anchor", "actual", "harborfront_commercial", "future_storefront_pattern", Rect2i(30, 13, 5, 5), "b_shop_house"),
		_lot("lot_printer_rowhouse_infill", "actual", "harborfront_commercial", "printer_rowhouse", Rect2i(40, 13, 4, 5), "b_printer_rowhouse"),
		_lot("lot_market_shed_anchor", "actual", "harborfront_commercial", "market_stall", Rect2i(35, 13, 5, 5), "b_market_shed"),
		_lot("lot_storehouse_anchor", "actual", "working_wharf", "waterline_warehouse", Rect2i(39, 24, 7, 5), "b_dock_storehouse"),
		_lot("lot_wharf_boathouse_anchor", "actual", "working_wharf", "waterline_dock_service", Rect2i(25, 24, 8, 5), "b_wharf_boathouse"),
		_lot("lot_dock_warehouse_anchor", "actual", "working_wharf", "waterline_warehouse", Rect2i(12, 24, 7, 5), "b_dock_warehouse"),
		_lot("lot_customs_house_anchor", "actual", "inland_residential_civic", "customs_house", Rect2i(22, 8, 8, 5), "b_custom_house"),
		_lot("lot_clerk_townhouse_infill", "actual", "harborfront_commercial", "clerk_lodging", Rect2i(11, 13, 6, 5), "b_clerk_townhouse"),
		_lot("lot_cottage_anchor", "actual", "inland_residential_civic", "home", Rect2i(11, 8, 5, 4), "b_res_small"),
		_lot("lot_civic_residence_anchor", "actual", "inland_residential_civic", "civic_residence", Rect2i(29, 7, 7, 5), "b_large_residence"),
		_lot("lot_lane_boarding_house_anchor", "actual", "support_lane", "boarding_house", Rect2i(36, 8, 5, 4), "b_boarding_house"),
		_lot("lot_dockworker_rowhouse_infill", "actual", "support_lane", "dockworker_lodging", Rect2i(41, 9, 5, 4), "b_dockworker_rowhouse"),
		_lot("lot_lane_cooperage_anchor", "actual", "support_lane", "cooperage_or_barrel_shop", Rect2i(6, 8, 4, 4), "b_cooperage_shed"),
		_lot("lot_west_fishmonger_future", "planned", "harborfront_commercial", "fishmonger_or_service_shop", Rect2i(3, 14, 4, 4)),
	]

static func planned_lot_specs() -> Array:
	var planned: Array = []
	for lot in starter_lot_specs():
		if lot.get("status", "") == "planned":
			planned.append(lot)
	return planned

static func g413b_rowhouse_infill_slots() -> Array:
	return [
		_infill_slot(
			"slot_tavern_mercantile_brick_rowhouse",
			"harborfront_commercial",
			"brick clerk townhouse row seated directly against the mercantile",
			Rect2i(12, 14, 6, 4),
			"Uses the full brick formal townhouse block and packs it directly against the mercantile without cropping or asset swapping.",
			"active_g413b",
			"b_clerk_townhouse",
			"future clerk lodging, tavern rumor, rented-room lead, or suspicious-neighbor hook"
		),
		_infill_slot(
			"slot_counting_chandlery_lane_edge_shop",
			"harborfront_commercial",
			"skinny lane-edge shop face east of counting house",
			Rect2i(24, 14, 1, 4),
			"Deferred to preserve the commercial rear road and the central cross-lane sightline.",
			"deferred_g413b",
			"",
			"future lane-edge shop or apothecary frontage after prop dressing confirms the lane remains clear"
		),
		_infill_slot(
			"slot_shop_market_townhouse_pair",
			"harborfront_commercial",
			"narrow shop-house gap between chandlery/shop-house and market frontage",
			Rect2i(30, 14, 3, 4),
			"Deferred after visual review: the shop-house bounds and storefront dressing make this gap too tight for a readable rowhouse without crowding the shop facade.",
			"deferred_g413b",
			"",
			"future small signboard shop or alley-width storefront after the shop-house crop/bounds are revisited"
		),
		_infill_slot(
			"slot_cottage_customs_inland_townhouse",
			"inland_residential_civic",
			"small inland townhouse fronting the inland/support road west of the custom house",
			Rect2i(16, 10, 4, 4),
			"Deferred after visual review: this read as an orphaned yard object instead of village street fabric.",
			"deferred_g413b",
			"",
			"future customs-clerk lodging, family dispute, or quiet artifact-discovery hook once an inland street edge exists"
		),
		_infill_slot(
			"slot_support_lane_boarding_gap",
			"support_lane",
			"four-unit dockworker rowhouse fronting the support-lane return beside boarding",
			Rect2i(41, 9, 5, 4),
			"Uses the attached clapboard rowhouse sprite and sits directly off the support road with a tight street-wall seam from the boarding house.",
			"active_g413b",
			"b_dockworker_rowhouse",
			"future missing-person, dockworker connection, or suspicious-neighbor hook"
		),
		_infill_slot(
			"slot_market_east_edge_narrow_shop",
			"harborfront_commercial",
			"narrow printer rowhouse on the east market street edge",
			Rect2i(43, 14, 3, 4),
			"Moved out of the shop-house gap and packed to a tight street-wall seam east of the market shed while keeping the dock access and market approach clear.",
			"active_g413b",
			"b_printer_rowhouse",
			"future revolutionary pamphlet, apprentice errand, rented-room rumor, or suspicious printing job"
		),
	]

static func missing_asset_manifest() -> Array:
	return [
		"fishmonger storefront",
		"cooperage / barrel shop final art",
		"blacksmith / smithy",
		"small home variants",
		"dock shack",
		"carts",
		"additional dock clutter atelier variants beyond the G-4.19A first rollout pack",
		"sign variants",
		"fencing variants",
		"lantern variants",
		"Newport-detail player character sprite sheet",
		"Newport-detail NPC sprite sheets",
		"Newport-detail monster sprite sheets",
		"Newport-detail equipment, weapons, armor, and combat VFX",
		"UI-world objects that match Newport material and outline rules",
		"chapel/church decision and final art if needed",
	]

static func calibration_variants() -> Array:
	return [
		{"id": "A", "label": "A Current scale reference - likely failing", "rect": Rect2(58, 72, 650, 345), "player_scale": 1.12, "recommendation": "baseline"},
		{"id": "B", "label": "B Smaller player / human scale", "rect": Rect2(858, 72, 650, 345), "player_scale": 0.76, "recommendation": "scale test"},
		{"id": "C", "label": "C Lower camera street vignette", "rect": Rect2(58, 522, 650, 345), "player_scale": 0.90, "recommendation": "framing test"},
		{"id": "D", "label": "D Integrated sidewalk + stoops - recommended", "rect": Rect2(858, 522, 650, 345), "player_scale": 0.78, "recommendation": "candidate"},
	]

static func _calibration_building(id: String, display_name: String, sprite_id: String, foot_tile: Vector2, visual_base_anchor: Vector2, draw_width: float, collision_size: Vector2, frontage_offset: Vector2, base_width: float, shadow_size: Vector2, variant_id: String) -> Dictionary:
	var config := _proof_street_building(id, display_name, sprite_id, foot_tile, visual_base_anchor, collision_size, frontage_offset, base_width, shadow_size, draw_width)
	config["district"] = "visual_calibration"
	config["district_tag"] = "calibration_" + variant_id.to_lower()
	config["calibration_variant"] = variant_id
	return config

static func _proof_street_building(id: String, display_name: String, sprite_id: String, foot_tile: Vector2, visual_base_anchor: Vector2, collision_size: Vector2, frontage_offset: Vector2, base_width: float, shadow_size: Vector2, draw_width_override := 0.0, seating_overrides := {}) -> Dictionary:
	var district_id := "harborfront_commercial" if G410_STARTER_HARBOR_TOWN else "waterfront_commercial"
	var config := _building(id, display_name, sprite_id, district_id, "commercial", foot_tile, collision_size.x / TILE, collision_size.y / TILE)
	var collision_footprint := Rect2(Vector2(-collision_size.x * 0.5, -collision_size.y), collision_size)
	var occupied_rect := collision_footprint
	if seating_overrides.has("occupied_rect"):
		occupied_rect = seating_overrides["occupied_rect"]
	config["proof_street"] = true
	if draw_width_override > 0.0:
		config["draw_width_override"] = draw_width_override
	config["visual_base_anchor"] = visual_base_anchor
	config["sprite_offset"] = seating_overrides.get("sprite_offset", Vector2.ZERO)
	config["visual_base_width"] = base_width
	config["collision_footprint"] = collision_footprint
	config["collision_rect"] = collision_footprint
	config["collision_size"] = collision_footprint.size
	config["collision_offset"] = collision_footprint.position + collision_footprint.size * 0.5
	config["frontage_offset"] = frontage_offset
	config["interaction_size"] = Vector2(maxf(84.0, collision_size.x * 0.76), 42.0)
	config["interaction_offset"] = frontage_offset
	config["interaction_zone"] = Rect2(frontage_offset - config["interaction_size"] * 0.5, config["interaction_size"])
	config["door_offset"] = frontage_offset
	config["y_sort_offset"] = Vector2.ZERO
	config["shadow_offset"] = Vector2(0.0, -6.0)
	config["shadow_size"] = shadow_size
	config["lot_bounds"] = occupied_rect
	config["lot_rect"] = occupied_rect
	config["building_volume_rect"] = occupied_rect
	config["frontage_body_rect"] = Rect2(Vector2(-base_width * 0.5, -maxf(34.0, collision_footprint.size.y)), Vector2(base_width, maxf(34.0, collision_footprint.size.y)))
	config["street_edge"] = Vector2(foot_tile.x * TILE, foot_tile.y * TILE + frontage_offset.y)
	return config

static func _building(id: String, display_name: String, sprite_id: String, district: String, district_tag: String, foot_tile: Vector2, collision_tiles_w: float, collision_tiles_h: float) -> Dictionary:
	var collision_h: float = maxf(30.0, collision_tiles_h * TILE)
	return {
		"id": id,
		"display_name": display_name,
		"sprite_id": sprite_id,
		"district": district,
		"district_tag": district_tag,
		"position": foot_tile * TILE,
		"foot_tile": Vector2i(roundi(foot_tile.x), roundi(foot_tile.y)),
		"foot_anchor": Vector2.ZERO,
		"collision_size": Vector2(collision_tiles_w * TILE, collision_h),
		"collision_offset": Vector2(0.0, -collision_h * 0.5),
		"collision_footprint": Rect2(Vector2(-collision_tiles_w * TILE * 0.5, -collision_h), Vector2(collision_tiles_w * TILE, collision_h)),
		"collision_rect": Rect2(Vector2(-collision_tiles_w * TILE * 0.5, -collision_h), Vector2(collision_tiles_w * TILE, collision_h)),
		"interaction_size": Vector2(max(72.0, collision_tiles_w * TILE * 0.72), 44.0),
		"interaction_offset": Vector2(0.0, 20.0),
		"interaction_zone": Rect2(Vector2(-max(72.0, collision_tiles_w * TILE * 0.72) * 0.5, -2.0), Vector2(max(72.0, collision_tiles_w * TILE * 0.72), 44.0)),
		"door_offset": Vector2.ZERO,
		"lot_bounds": Rect2(Vector2(-collision_tiles_w * TILE * 0.5, -collision_h), Vector2(collision_tiles_w * TILE, collision_h)),
		"lot_rect": Rect2(Vector2(-collision_tiles_w * TILE * 0.5, -collision_h), Vector2(collision_tiles_w * TILE, collision_h)),
		"building_volume_rect": Rect2(Vector2(-collision_tiles_w * TILE * 0.5, -collision_h), Vector2(collision_tiles_w * TILE, collision_h)),
		"y_sort_offset": Vector2.ZERO,
	}

static func _catalog_building(id: String, district: String, district_tag: String, foot_tile: Vector2, proof_street := false) -> Dictionary:
	var layout_rule := g415_layout_rule(id)
	var config := {
		"id": id,
		"definition_id": id,
		"district": district,
		"district_tag": district_tag,
		"position": foot_tile * TILE,
		"foot_tile": Vector2i(roundi(foot_tile.x), roundi(foot_tile.y)),
		"proof_street": proof_street,
		"street_edge": foot_tile * TILE,
	}
	if not layout_rule.is_empty():
		config["parcel_id"] = layout_rule.get("parcel_id", "")
		config["district_band"] = layout_rule.get("district_band", "")
		config["frontage_line_y"] = layout_rule.get("frontage_line_y", 0.0)
		config["setback_from_road"] = layout_rule.get("setback_from_road", 0.0)
		config["side_gap_minimum"] = layout_rule.get("side_gap_minimum", 0.0)
		config["door_path_target"] = layout_rule.get("door_path_target", Vector2.ZERO)
		config["prop_band"] = layout_rule.get("prop_band", Rect2())
		config["ground_pad"] = layout_rule.get("ground_pad", {})
		config["lot_type"] = layout_rule.get("lot_type", "")
		config["layout_rule"] = layout_rule
	return config

static func _layout_rule(parcel_id: String, district_band: String, frontage_line_y: float, setback_from_road: float, side_gap_minimum: float, door_path_target: Vector2, prop_band: Rect2, ground_pad_rect: Rect2, ground_pad_type: String, notes := "") -> Dictionary:
	return {
		"parcel_id": parcel_id,
		"district_band": district_band,
		"frontage_line_y": frontage_line_y,
		"setback_from_road": setback_from_road,
		"side_gap_minimum": side_gap_minimum,
		"door_path_target": door_path_target,
		"prop_band": prop_band,
		"ground_pad": {
			"rect": ground_pad_rect,
			"type": ground_pad_type,
		},
		"lot_type": ground_pad_type,
		"notes": notes,
	}

static func _lot(id: String, status: String, district: String, role: String, rect: Rect2i, building_id := "") -> Dictionary:
	return {
		"id": id,
		"status": status,
		"district": district,
		"role": role,
		"rect": rect,
		"building_id": building_id,
	}

static func _infill_slot(id: String, district: String, role: String, rect: Rect2i, guardrail: String, status := "planned_g413b", building_id := "", future_hook := "") -> Dictionary:
	return {
		"id": id,
		"status": status,
		"district": district,
		"role": role,
		"rect": rect,
		"guardrail": guardrail,
		"building_id": building_id,
		"future_hook": future_hook,
	}

static func _route_probe(id: String, position: Vector2, notes: String, label: String = "") -> Dictionary:
	return {
		"id": id,
		"label": label if not label.is_empty() else id,
		"position": position,
		"notes": notes,
	}

static func _blocker(id: String, rect: Rect2) -> Dictionary:
	return {"id": id, "rect": rect}

static func _tiles_from_rects(rects: Array) -> Array:
	var tiles: Array = []
	var seen := {}
	for rect in rects:
		for y in range(rect.position.y, rect.position.y + rect.size.y):
			for x in range(rect.position.x, rect.position.x + rect.size.x):
				var tile := Vector2i(x, y)
				var key := _key(tile)
				if not seen.has(key):
					seen[key] = true
					tiles.append(tile)
	return tiles

static func _tile_key_set(tiles: Array) -> Dictionary:
	var result := {}
	for tile in tiles:
		result[_key(tile)] = true
	return result

static func _key(tile: Vector2i) -> String:
	return "%d,%d" % [tile.x, tile.y]
