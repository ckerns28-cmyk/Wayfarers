extends RefCounted
class_name NewportTownBlueprint

const TILE := 32
const MAP_TILES := Vector2i(50, 32)
const WORLD_SIZE := Vector2(MAP_TILES.x * TILE, MAP_TILES.y * TILE)
const G49_STREET_VIGNETTE := true
const G48_PROOF_STREET := false
const G46_PROOF_FRAME := false
const G47_CALIBRATION_MODE := false
const PLAYER_SPAWN := Vector2(675, 612)
const EDRIN_SPAWN := Vector2(-800, -800)

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

const BUILDING_IDS := PROOF_STREET_IDS

static func base_ground_rect() -> Rect2i:
	return Rect2i(0, 0, MAP_TILES.x, MAP_TILES.y)

static func district_rects() -> Array:
	return [
		{"id": "upper_residential_terrace", "rect": Rect2i(7, 0, 30, 8), "base": Color("#6e8d5d"), "alt": Color("#527449")},
		{"id": "civic_district", "rect": Rect2i(18, 6, 16, 8), "base": Color("#708b63"), "alt": Color("#58754f")},
		{"id": "waterfront_commercial", "rect": Rect2i(8, 11, 32, 8), "base": Color("#657f55"), "alt": Color("#506f49")},
		{"id": "service_outfitter_lane", "rect": Rect2i(3, 8, 43, 12), "base": Color("#5c784f"), "alt": Color("#486b43")},
		{"id": "harbor_wharf", "rect": Rect2i(7, 17, 34, 9), "base": Color("#626f55"), "alt": Color("#4b5e48")},
	]

static func primary_roads() -> Array:
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
	return [
		Rect2i(19, 10, 8, 4),
		Rect2i(18, 6, 15, 1),
		Rect2i(13, 8, 4, 2),
	]

static func waterfront_apron_rects() -> Array:
	return [
		Rect2i(8, 15, 25, 2),
		Rect2i(8, 17, 25, 1),
		Rect2i(8, 19, 25, 1),
	]

static func pier_rects() -> Array:
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
	return PROOF_STREET_IDS.duplicate()

static func proof_street_walk_targets() -> Dictionary:
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

static func lived_in_detail_count() -> int:
	if G49_STREET_VIGNETTE:
		return 30
	if G48_PROOF_STREET:
		return 24
	if G47_CALIBRATION_MODE:
		return 26
	if G46_PROOF_FRAME:
		return 12
	return 52

static func detail_blockers() -> Array:
	if G49_STREET_VIGNETTE:
		return [
			_blocker("mercantile_base_barrels", Rect2(430, 544, 26, 18)),
			_blocker("west_loading_crates", Rect2(526, 548, 28, 18)),
			_blocker("counting_house_left_goods", Rect2(602, 542, 32, 18)),
			_blocker("counting_house_right_barrels", Rect2(728, 546, 28, 18)),
			_blocker("east_alley_rope_stack", Rect2(786, 548, 30, 18)),
			_blocker("chandlery_side_crates", Rect2(900, 550, 28, 18)),
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
	if G49_STREET_VIGNETTE:
		return [
			_proof_street_building("b_mercantile", "Mercantile", "mercantile_shop", Vector2(15.0, 17.55), Vector2(193.0, 421.0), Vector2(88.0, 30.0), Vector2(0.0, 24.0), 122.0, Vector2(138.0, 17.0), 150.0, {
				"occupied_rect": Rect2(Vector2(-82.0, -160.0), Vector2(164.0, 172.0)),
			}),
			_proof_street_building("b_counting_house", "Counting House", "newport_counting_house_civic_exchange", Vector2(20.75, 17.55), Vector2(223.0, 340.0), Vector2(104.0, 32.0), Vector2(0.0, 25.0), 150.0, Vector2(166.0, 18.0), 190.0, {
				"occupied_rect": Rect2(Vector2(-104.0, -166.0), Vector2(208.0, 178.0)),
			}),
			_proof_street_building("b_chandlery_front", "Chandlery", "newport_chandlery_outfitter_front", Vector2(26.45, 17.55), Vector2(211.5, 370.0), Vector2(98.0, 31.0), Vector2(0.0, 24.0), 132.0, Vector2(154.0, 18.0), 181.0, {
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

static func substitution_notes() -> Dictionary:
	return {
		"b_market_shed": "Uses the closest market/frontage shed cell from Newport pack B.",
		"b_service_dependency": "Uses the compact service shed from the base Hearthvale atlas.",
		"b_prestige_block": "Uses the formal townhouse block from Newport pack B.",
	}

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
	var config := _building(id, display_name, sprite_id, "waterfront_commercial", "commercial", foot_tile, collision_size.x / TILE, collision_size.y / TILE)
	var occupied_rect := Rect2(Vector2(-collision_size.x * 0.5, -collision_size.y), collision_size)
	if seating_overrides.has("occupied_rect"):
		occupied_rect = seating_overrides["occupied_rect"]
	config["proof_street"] = true
	if draw_width_override > 0.0:
		config["draw_width_override"] = draw_width_override
	config["visual_base_anchor"] = visual_base_anchor
	config["sprite_offset"] = seating_overrides.get("sprite_offset", Vector2.ZERO)
	config["visual_base_width"] = base_width
	config["collision_rect"] = occupied_rect
	config["frontage_offset"] = frontage_offset
	config["interaction_size"] = Vector2(maxf(84.0, collision_size.x * 0.76), 42.0)
	config["interaction_offset"] = frontage_offset
	config["door_offset"] = frontage_offset
	config["y_sort_offset"] = Vector2.ZERO
	config["shadow_offset"] = Vector2(0.0, -6.0)
	config["shadow_size"] = shadow_size
	config["lot_rect"] = occupied_rect
	config["building_volume_rect"] = occupied_rect
	config["frontage_body_rect"] = Rect2(Vector2(-base_width * 0.5, -maxf(34.0, collision_size.y)), Vector2(base_width, maxf(34.0, collision_size.y)))
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
		"collision_size": Vector2(collision_tiles_w * TILE, collision_h),
		"collision_offset": Vector2(0.0, -collision_h * 0.5),
		"interaction_size": Vector2(max(72.0, collision_tiles_w * TILE * 0.72), 44.0),
		"interaction_offset": Vector2(0.0, 20.0),
		"door_offset": Vector2.ZERO,
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
