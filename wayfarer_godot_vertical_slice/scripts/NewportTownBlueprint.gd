extends RefCounted
class_name NewportTownBlueprint

const TILE := 32
const MAP_TILES := Vector2i(50, 32)
const WORLD_SIZE := Vector2(MAP_TILES.x * TILE, MAP_TILES.y * TILE)
const PLAYER_SPAWN := Vector2(690, 590)
const EDRIN_SPAWN := Vector2(730, 560)

const BUILDING_IDS := [
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
	return [
		Rect2i(8, 18, 25, 1),
		Rect2i(20, 7, 1, 12),
		Rect2i(12, 7, 21, 1),
	]

static func secondary_roads() -> Array:
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
	return [
		{"id": "west_fish_pier", "rect": Rect2i(10, 18, 1, 8)},
		{"id": "west_commercial_pier", "rect": Rect2i(16, 18, 1, 7)},
		{"id": "central_civic_pier", "rect": Rect2i(19, 17, 1, 10)},
		{"id": "counting_house_pier", "rect": Rect2i(23, 18, 1, 7)},
		{"id": "east_market_pier", "rect": Rect2i(29, 18, 1, 7)},
	]

static func water_rects() -> Array:
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
	var rects: Array = [Rect2i(8, 18, 25, 1)]
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
	return {
		"waterfront_street": Vector2i(20, 18),
		"central_pier_frontage": Vector2i(19, 25),
		"civic_square": Vector2i(20, 12),
		"upper_residential": Vector2i(18, 7),
		"service_lane": Vector2i(37, 14),
	}

static func player_spawn_tile() -> Vector2i:
	return Vector2i(floori(PLAYER_SPAWN.x / TILE), floori(PLAYER_SPAWN.y / TILE))

static func building_specs() -> Array:
	return [
		_building("b_boathouse", "Boathouse", "newport_wharf_boathouse_large", "harbor_wharf", "harbor", Vector2(12, 21), 4.0, 1.0),
		_building("b_dock_storehouse", "Dock Storehouse", "newport_dockside_storehouse_long", "harbor_wharf", "harbor", Vector2(32, 21), 4.0, 1.0),
		_building("b_market_shed", "Market Shed", "newport_market_shed_stalls", "harbor_wharf", "harbor", Vector2(26, 21), 3.0, 1.0),
		_building("b_inn_tavern", "Inn & Tavern", "inn_tavern_v1", "waterfront_commercial", "commercial", Vector2(11, 16), 5.0, 1.4),
		_building("b_mercantile", "Mercantile", "mercantile_shop", "waterfront_commercial", "commercial", Vector2(17, 16), 3.5, 1.0),
		_building("b_counting_house", "Counting House", "newport_counting_house_civic_exchange", "waterfront_commercial", "commercial", Vector2(24, 16), 4.0, 1.0),
		_building("b_chandlery_front", "Chandlery", "newport_chandlery_outfitter_front", "waterfront_commercial", "commercial", Vector2(30, 16), 3.7, 1.0),
		_building("b_shop_house", "Shop House", "newport_shopfront_awning", "waterfront_commercial", "commercial", Vector2(37, 17), 3.5, 1.0),
		_building("b_custom_house", "Custom House", "newport_custom_house_civic_front", "civic_district", "civic", Vector2(30, 11), 3.8, 1.0),
		_building("b_village_hall", "Village Hall", "village_hall_meeting_house", "civic_district", "civic", Vector2(24, 11), 4.0, 1.0),
		_building("b_res_small", "Harbor Cottage", "residence_small", "service_outfitter_lane", "service", Vector2(6, 11), 2.3, 1.0),
		_building("b_townhouse_row_a", "Townhouse Row A", "newport_narrow_merchant_townhouse_a", "waterfront_commercial", "commercial", Vector2(39, 13), 2.1, 1.0),
		_building("b_townhouse_row_b", "Townhouse Row B", "newport_modest_clapboard_residence_a", "service_outfitter_lane", "service", Vector2(42, 10), 2.4, 1.0),
		_building("b_service_dependency", "Service Dependency", "service_dependency_shed", "service_outfitter_lane", "service", Vector2(42, 17), 2.1, 1.0),
		_building("b_hunter_lodge", "Hunter Lodge", "hunter_lodge_or_outfitter", "service_outfitter_lane", "rural", Vector2(5, 17), 2.4, 1.0),
		_building("b_res_large", "Large Residence", "residence_large", "upper_residential_terrace", "residential", Vector2(13, 5), 3.3, 1.0),
		_building("b_georgian_residence", "Georgian Residence", "newport_georgian_merchant_residence_a", "upper_residential_terrace", "residential", Vector2(18, 6), 3.4, 1.0),
		_building("b_elite_mansion", "Elite Mansion", "newport_elite_mansion_white", "upper_residential_terrace", "residential", Vector2(25, 5), 3.7, 1.0),
		_building("b_prestige_block", "Prestige Block", "newport_formal_townhouse_block_a", "upper_residential_terrace", "residential", Vector2(32, 6), 3.6, 1.0),
	]

static func substitution_notes() -> Dictionary:
	return {
		"b_market_shed": "Uses the closest market/frontage shed cell from Newport pack B.",
		"b_service_dependency": "Uses the compact service shed from the base Hearthvale atlas.",
		"b_prestige_block": "Uses the formal townhouse block from Newport pack B.",
	}

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
