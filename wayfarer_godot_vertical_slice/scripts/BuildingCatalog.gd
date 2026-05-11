extends RefCounted
class_name BuildingCatalog

const ATLAS_V1 := "res://assets/buildings/hearthvale_buildings_atlas_v1.png"
const PACK_A := "res://assets/buildings/hearthvale_newport_structure_pack_v1_a.png"
const PACK_B := "res://assets/buildings/hearthvale_newport_structure_pack_v1_b.png"

static func sprite_config(sprite_id: String) -> Dictionary:
	match sprite_id:
		"inn_tavern_v1":
			return _sprite(ATLAS_V1, Rect2(33, 45, 385, 373), 218.0)
		"mercantile_shop":
			return _sprite(ATLAS_V1, Rect2(418, 67, 384, 351), 172.0)
		"village_hall_meeting_house":
			return _sprite(ATLAS_V1, Rect2(855, 10, 323, 408), 174.0)
		"residence_small":
			return _sprite(ATLAS_V1, Rect2(61, 418, 357, 418), 142.0)
		"residence_large":
			return _sprite(ATLAS_V1, Rect2(836, 418, 381, 418), 184.0)
		"hunter_lodge_or_outfitter":
			return _sprite(ATLAS_V1, Rect2(44, 836, 367, 343), 150.0)
		"service_dependency_shed":
			return _sprite(ATLAS_V1, Rect2(878, 836, 271, 348), 116.0)
		"newport_georgian_merchant_residence_a":
			return _sprite(PACK_A, Rect2(57, 57, 361, 361), 178.0)
		"newport_elite_garden_mansion_a":
			return _sprite(PACK_A, Rect2(418, 76, 410, 332), 190.0)
		"newport_waterfront_shop_house":
			return _sprite(PACK_A, Rect2(864, 86, 351, 315), 170.0)
		"newport_large_front_residence":
			return _sprite(PACK_A, Rect2(61, 418, 357, 372), 178.0)
		"newport_shopfront_awning":
			return _sprite(PACK_A, Rect2(418, 470, 418, 313), 178.0)
		"newport_narrow_merchant_townhouse_a":
			return _sprite(PACK_A, Rect2(836, 451, 273, 385), 118.0)
		"newport_chandlery_cottage":
			return _sprite(PACK_A, Rect2(68, 873, 350, 292), 156.0)
		"newport_dockside_storehouse_long":
			return _sprite(PACK_A, Rect2(418, 885, 418, 300), 212.0)
		"newport_wharf_boathouse_large":
			return _sprite(PACK_A, Rect2(836, 836, 370, 352), 224.0)
		"newport_custom_house_civic_front":
			return _sprite(PACK_B, Rect2(39, 19, 379, 385), 176.0)
		"newport_formal_townhouse_block_a":
			return _sprite(PACK_B, Rect2(418, 67, 397, 336), 188.0)
		"newport_elite_mansion_white":
			return _sprite(PACK_B, Rect2(840, 60, 380, 348), 192.0)
		"newport_modest_clapboard_residence_a":
			return _sprite(PACK_B, Rect2(105, 433, 313, 403), 126.0)
		"newport_counting_house_civic_exchange":
			return _sprite(PACK_B, Rect2(418, 475, 418, 322), 202.0)
		"newport_chandlery_outfitter_front":
			return _sprite(PACK_B, Rect2(836, 444, 366, 352), 184.0)
		"newport_dockside_storehouse":
			return _sprite(PACK_B, Rect2(51, 836, 361, 377), 196.0)
		"newport_market_shed_stalls":
			return _sprite(PACK_B, Rect2(430, 838, 406, 357), 170.0)
		"newport_market_frontage_row":
			return _sprite(PACK_B, Rect2(836, 842, 373, 355), 178.0)
		_:
			push_error("Unknown building sprite id: " + sprite_id)
			return {}

static func _sprite(atlas_path: String, region: Rect2, draw_width: float) -> Dictionary:
	return {
		"atlas_path": atlas_path,
		"region": region,
		"source_size": region.size,
		"draw_width": draw_width,
		"anchor": Vector2(region.size.x * 0.5, region.size.y)
	}
