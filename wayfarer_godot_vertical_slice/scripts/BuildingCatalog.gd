extends RefCounted
class_name BuildingCatalog

const ATLAS_V1 := "res://assets/buildings/hearthvale_buildings_atlas_v1.png"
const PACK_A := "res://assets/buildings/hearthvale_newport_structure_pack_v1_a.png"
const PACK_B := "res://assets/buildings/hearthvale_newport_structure_pack_v1_b.png"
const ISOLATED_BUILDINGS := "res://assets/sprites/buildings/isolated"

static func sprite_config(sprite_id: String) -> Dictionary:
	match sprite_id:
		"inn_tavern_v1":
			return _sprite(ISOLATED_BUILDINGS + "/inn_tavern_v1_isolated.png", Rect2(0, 0, 473, 468), 142.0)
		"mercantile_shop":
			return _sprite(ISOLATED_BUILDINGS + "/mercantile_shop_isolated.png", Rect2(0, 0, 398, 451), 150.0)
		"village_hall_meeting_house":
			return _sprite(ISOLATED_BUILDINGS + "/village_hall_meeting_house_isolated.png", Rect2(0, 0, 438, 498), 178.0)
		"residence_small":
			return _sprite(ISOLATED_BUILDINGS + "/residence_small_isolated.png", Rect2(0, 0, 393, 368), 126.0)
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
			return _sprite(ISOLATED_BUILDINGS + "/newport_shopfront_awning_isolated.png", Rect2(0, 0, 413, 448), 150.0)
		"newport_narrow_merchant_townhouse_a":
			return _sprite(PACK_A, Rect2(836, 451, 273, 385), 118.0)
		"newport_chandlery_cottage":
			return _sprite(PACK_A, Rect2(68, 873, 350, 292), 156.0)
		"newport_dockside_storehouse_long":
			return _sprite(ISOLATED_BUILDINGS + "/newport_dockside_storehouse_long_isolated.png", Rect2(0, 0, 388, 398), 220.0)
		"newport_wharf_boathouse_large":
			return _sprite(ISOLATED_BUILDINGS + "/newport_wharf_boathouse_large_isolated.png", Rect2(0, 0, 578, 478), 280.0)
		"newport_custom_house_civic_front":
			return _sprite(PACK_B, Rect2(39, 19, 379, 385), 176.0)
		"newport_formal_townhouse_block_a":
			return _sprite(PACK_B, Rect2(418, 67, 397, 336), 188.0)
		"newport_elite_mansion_white":
			return _sprite(PACK_B, Rect2(840, 60, 380, 348), 192.0)
		"newport_modest_clapboard_residence_a":
			return _sprite(PACK_B, Rect2(105, 433, 313, 403), 126.0)
		"newport_counting_house_civic_exchange":
			return _sprite(ISOLATED_BUILDINGS + "/newport_counting_house_civic_exchange_isolated.png", Rect2(0, 0, 458, 370), 190.0)
		"newport_chandlery_outfitter_front":
			return _sprite(ISOLATED_BUILDINGS + "/newport_chandlery_outfitter_front_isolated.png", Rect2(0, 0, 435, 400), 181.0)
		"newport_dockside_storehouse":
			return _sprite(ISOLATED_BUILDINGS + "/newport_dockside_storehouse_isolated.png", Rect2(0, 0, 443, 448), 220.0)
		"newport_market_shed_stalls":
			return _sprite(ISOLATED_BUILDINGS + "/newport_market_shed_stalls_isolated.png", Rect2(0, 0, 434, 438), 210.0)
		"newport_market_frontage_row":
			return _sprite(PACK_B, Rect2(836, 842, 373, 355), 178.0)
		_:
			push_error("Unknown building sprite id: " + sprite_id)
			return {}

static func building_definition(building_id: String) -> Dictionary:
	match building_id:
		"b_inn_tavern":
			return _definition(building_id, "Inn & Tavern", "inn_tavern_v1", "tavern", 166.0, Vector2(214.0, 392.0), Vector2(154.0, 22.0), Rect2(Vector2(-86.0, -164.0), Vector2(172.0, 176.0)), Vector2(0.0, 26.0), 146.0)
		"b_mercantile":
			return _definition(building_id, "Mercantile", "mercantile_shop", "mercantile", 150.0, Vector2(199.0, 427.0), Vector2(138.0, 17.0), Rect2(Vector2(-82.0, -160.0), Vector2(164.0, 172.0)), Vector2(0.0, 24.0))
		"b_counting_house":
			return _definition(building_id, "Counting House", "newport_counting_house_civic_exchange", "counting_house", 190.0, Vector2(229.0, 346.0), Vector2(166.0, 18.0), Rect2(Vector2(-104.0, -166.0), Vector2(208.0, 178.0)), Vector2(0.0, 25.0), 150.0)
		"b_chandlery_front":
			return _definition(building_id, "Chandlery", "newport_chandlery_outfitter_front", "chandlery", 181.0, Vector2(217.5, 376.0), Vector2(154.0, 18.0), Rect2(Vector2(-92.0, -168.0), Vector2(184.0, 180.0)), Vector2(0.0, 24.0), 132.0)
		"b_shop_house":
			return _definition(building_id, "Shop House", "newport_shopfront_awning", "shop", 150.0, Vector2(206.5, 402.0), Vector2(138.0, 17.0), Rect2(Vector2(-82.0, -158.0), Vector2(164.0, 170.0)), Vector2(0.0, 24.0))
		"b_market_shed":
			return _definition(building_id, "Market Shed", "newport_market_shed_stalls", "dock_service", 210.0, Vector2(217.0, 394.0), Vector2(154.0, 18.0), Rect2(Vector2(-86.0, -92.0), Vector2(172.0, 102.0)), Vector2(0.0, 24.0), 132.0)
		"b_dock_storehouse":
			return _definition(building_id, "Dock Storehouse", "newport_dockside_storehouse_long", "warehouse", 220.0, Vector2(194.0, 318.0), Vector2(176.0, 18.0), Rect2(Vector2(-104.0, -122.0), Vector2(208.0, 128.0)), Vector2(0.0, 20.0), 156.0, true)
		"b_wharf_boathouse":
			return _definition(building_id, "Wharf Boathouse", "newport_wharf_boathouse_large", "dock_service", 280.0, Vector2(289.0, 378.0), Vector2(196.0, 20.0), Rect2(Vector2(-124.0, -138.0), Vector2(248.0, 146.0)), Vector2(0.0, 22.0), 190.0, true)
		"b_dock_warehouse":
			return _definition(building_id, "Dock Warehouse", "newport_dockside_storehouse", "warehouse", 220.0, Vector2(221.5, 351.0), Vector2(176.0, 20.0), Rect2(Vector2(-106.0, -136.0), Vector2(212.0, 144.0)), Vector2(0.0, 22.0), 160.0, true)
		"b_village_hall":
			return _definition(building_id, "Village Hall", "village_hall_meeting_house", "civic", 178.0, Vector2(219.0, 454.0), Vector2(160.0, 20.0), Rect2(Vector2(-92.0, -152.0), Vector2(184.0, 164.0)), Vector2(0.0, 24.0), 142.0)
		"b_res_small":
			return _definition(building_id, "Harbor Cottage", "residence_small", "residence", 126.0, Vector2(196.5, 338.0), Vector2(112.0, 17.0), Rect2(Vector2(-66.0, -116.0), Vector2(132.0, 126.0)), Vector2(0.0, 22.0), 102.0)
		_:
			push_error("Unknown building definition id: " + building_id)
			return {}

static func _sprite(atlas_path: String, region: Rect2, draw_width: float) -> Dictionary:
	return {
		"atlas_path": atlas_path,
		"region": region,
		"source_size": region.size,
		"draw_width": draw_width,
		"anchor": Vector2(region.size.x * 0.5, region.size.y)
	}

static func _definition(building_id: String, display_name: String, sprite_id: String, district_role: String, draw_width: float, visual_base_anchor: Vector2, shadow_size: Vector2, collision_rect: Rect2, frontage_offset: Vector2, visual_base_width := 122.0, harbor_integrated := false) -> Dictionary:
	var sprite := sprite_config(sprite_id)
	return {
		"id": building_id,
		"building_id": building_id,
		"display_name": display_name,
		"sprite_id": sprite_id,
		"texture_path": sprite.get("atlas_path", ""),
		"sprite_region": sprite.get("region", Rect2()),
		"sprite_source_size": sprite.get("source_size", Vector2.ZERO),
		"district_role": district_role,
		"intended_district_role": district_role,
		"visual_scale": draw_width,
		"draw_width_override": draw_width,
		"foot_anchor": visual_base_anchor,
		"visual_base_anchor": visual_base_anchor,
		"visual_base_width": visual_base_width,
		"collision_rect": collision_rect,
		"collision_size": collision_rect.size,
		"collision_offset": collision_rect.position + collision_rect.size * 0.5,
		"interaction_size": Vector2(maxf(84.0, collision_rect.size.x * 0.76), 42.0),
		"interaction_offset": frontage_offset,
		"frontage_offset": frontage_offset,
		"door_offset": frontage_offset,
		"y_sort_offset": Vector2.ZERO,
		"shadow_offset": Vector2(0.0, -6.0),
		"shadow_size": shadow_size,
		"lot_rect": collision_rect,
		"building_volume_rect": collision_rect,
		"frontage_body_rect": Rect2(Vector2(-visual_base_width * 0.5, -maxf(34.0, collision_rect.size.y)), Vector2(visual_base_width, maxf(34.0, collision_rect.size.y))),
		"harbor_integrated": harbor_integrated,
		"definition_normalized": true,
	}
