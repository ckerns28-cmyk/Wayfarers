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
			return _sprite(ISOLATED_BUILDINGS + "/service_dependency_shed_isolated.png", Rect2(0, 0, 298, 293), 124.0)
		"newport_georgian_merchant_residence_a":
			return _sprite(PACK_A, Rect2(57, 57, 361, 361), 178.0)
		"newport_elite_garden_mansion_a":
			return _sprite(PACK_A, Rect2(418, 76, 410, 332), 190.0)
		"newport_waterfront_shop_house":
			return _sprite(PACK_A, Rect2(864, 86, 351, 315), 170.0)
		"newport_large_front_residence":
			return _sprite(ISOLATED_BUILDINGS + "/newport_large_front_residence_isolated.png", Rect2(0, 0, 435, 369), 200.0)
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
			return _sprite(ISOLATED_BUILDINGS + "/newport_custom_house_civic_front_isolated.png", Rect2(0, 0, 437, 433), 176.0)
		"newport_formal_townhouse_block_a":
			return _sprite(PACK_B, Rect2(444, 67, 371, 336), 188.0)
		"newport_elite_mansion_white":
			return _sprite(PACK_B, Rect2(840, 60, 380, 348), 192.0)
		"newport_modest_clapboard_residence_a":
			return _sprite(ISOLATED_BUILDINGS + "/newport_modest_clapboard_residence_a_isolated.png", Rect2(0, 0, 247, 418), 126.0)
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
		"b_custom_house":
			return _definition(building_id, "Custom House", "newport_custom_house_civic_front", "customs_house", 176.0, Vector2(214.5, 409.0), Vector2(164.0, 20.0), Rect2(Vector2(-96.0, -146.0), Vector2(192.0, 156.0)), Vector2(0.0, 24.0), 146.0, false, ["inland_residential_civic", "harborfront_commercial", "civic", "customs"], "G-4.11 intentional civic/admin anchor; uses the dedicated custom house asset from the left side of Newport pack B.")
		"b_village_hall":
			return _definition(building_id, "Meeting House Chapel", "village_hall_meeting_house", "chapel_deferred", 178.0, Vector2(219.0, 454.0), Vector2(160.0, 20.0), Rect2(Vector2(-92.0, -152.0), Vector2(184.0, 164.0)), Vector2(0.0, 24.0), 142.0, false, ["inland_residential_civic", "chapel"], "Church/chapel-coded asset demoted in G-4.11; not active as the starter town civic anchor.")
		"b_res_small":
			return _definition(building_id, "Harbor Cottage", "residence_small", "residence", 126.0, Vector2(196.5, 338.0), Vector2(112.0, 17.0), Rect2(Vector2(-66.0, -116.0), Vector2(132.0, 126.0)), Vector2(0.0, 22.0), 102.0)
		"b_large_residence":
			return _definition(building_id, "Harbor Residence", "newport_large_front_residence", "large_residence", 200.0, Vector2(217.5, 345.0), Vector2(156.0, 18.0), Rect2(Vector2(-92.0, -142.0), Vector2(184.0, 152.0)), Vector2(0.0, 23.0), 142.0, false, ["inland_residential_civic", "residential", "civic_residence"], "Integrated from Newport pack A with an isolated crop so the full residence and side dressing are visible.")
		"b_boarding_house":
			return _definition(building_id, "Boarding House", "newport_modest_clapboard_residence_a", "boarding_house", 126.0, Vector2(123.5, 394.0), Vector2(112.0, 17.0), Rect2(Vector2(-66.0, -126.0), Vector2(132.0, 136.0)), Vector2(0.0, 21.0), 104.0, false, ["support_lane", "inland_residential_civic", "residential"], "Tall clapboard residence reused as a boarding house with an isolated crop to remove neighboring sprite pixels.")
		"b_cooperage_shed":
			return _definition(building_id, "Cooperage Shed", "service_dependency_shed", "cooperage", 124.0, Vector2(149.0, 269.0), Vector2(98.0, 16.0), Rect2(Vector2(-58.0, -108.0), Vector2(116.0, 118.0)), Vector2(0.0, 20.0), 92.0, false, ["support_lane", "working_wharf", "dock_service"], "Compact service shed standing in for cooperage/barrel-shop support with an isolated crop to remove the building above it.")
		_:
			push_error("Unknown building definition id: " + building_id)
			return {}

static func available_building_assets() -> Array:
	return [
		_asset("inn_tavern_v1", "tavern / inn", "integrated", "Accepted isolated tavern anchor."),
		_asset("mercantile_shop", "mercantile / general goods", "integrated", "Accepted isolated shop anchor."),
		_asset("newport_counting_house_civic_exchange", "counting house / civic exchange", "integrated", "Accepted isolated harborfront office."),
		_asset("newport_chandlery_outfitter_front", "chandlery / rope / sail shop", "integrated", "Accepted isolated working-harbor storefront."),
		_asset("newport_shopfront_awning", "shop house / general storefront", "integrated", "Accepted isolated harborfront shop."),
		_asset("newport_market_shed_stalls", "fishmonger / market shed", "integrated", "Accepted isolated market/fish stall."),
		_asset("newport_dockside_storehouse_long", "warehouse", "integrated", "Accepted isolated long dock storehouse."),
		_asset("newport_wharf_boathouse_large", "dock shack / boathouse", "integrated", "Accepted isolated wharf service building."),
		_asset("newport_dockside_storehouse", "warehouse / dock service", "integrated", "Accepted isolated dock warehouse."),
		_asset("newport_custom_house_civic_front", "customs house / civic", "integrated_g411", "Dedicated custom-house asset intentionally used as the starter civic/admin anchor."),
		_asset("residence_small", "small residence", "integrated", "Accepted isolated cottage."),
		_asset("newport_large_front_residence", "large residence / civic residence", "integrated_g411", "Adds inland residential depth using an isolated full-width crop."),
		_asset("newport_modest_clapboard_residence_a", "boarding house / small residence", "integrated_g411", "Adds support-lane housing using an isolated crop."),
		_asset("service_dependency_shed", "cooperage / barrel shop / dock shack", "integrated_g411", "Temporary support/service role using an isolated crop."),
		_asset("village_hall_meeting_house", "church / chapel", "deferred", "Demoted in G-4.11; not used as the starter civic anchor."),
		_asset("residence_large", "large residence", "available_deferred", "Base atlas residence; not active in starter pass."),
		_asset("hunter_lodge_or_outfitter", "outfitter / rural lodge", "available_deferred", "Less Newport-civic than current set."),
		_asset("newport_georgian_merchant_residence_a", "large residence / merchant residence", "available_deferred", "Possible G-4.12 composition candidate."),
		_asset("newport_elite_garden_mansion_a", "large residence / civic residence", "available_deferred", "Too grand for the starter harbor core right now."),
		_asset("newport_waterfront_shop_house", "shop house / mercantile", "available_deferred", "Duplicate storefront role."),
		_asset("newport_narrow_merchant_townhouse_a", "shop house / townhouse", "available_deferred", "Possible row-house variant."),
		_asset("newport_chandlery_cottage", "chandlery / cottage / service shop", "available_deferred", "Possible smaller service-lane shop."),
		_asset("newport_formal_townhouse_block_a", "formal townhouse row / residential row", "available_deferred", "Deferred for a later row-house or residential purpose."),
		_asset("newport_elite_mansion_white", "large residence / boarding house", "available_deferred", "Potential upper-town residence."),
		_asset("newport_market_frontage_row", "mercantile / market frontage", "available_deferred", "Duplicate commercial frontage for later dressing."),
	]

static func _sprite(atlas_path: String, region: Rect2, draw_width: float) -> Dictionary:
	return {
		"atlas_path": atlas_path,
		"region": region,
		"source_size": region.size,
		"draw_width": draw_width,
		"anchor": Vector2(region.size.x * 0.5, region.size.y)
	}

static func _asset(sprite_id: String, role_candidates: String, status: String, notes: String) -> Dictionary:
	return {
		"sprite_id": sprite_id,
		"role_candidates": role_candidates,
		"status": status,
		"notes": notes,
	}

static func _definition(building_id: String, display_name: String, sprite_id: String, district_role: String, draw_width: float, visual_base_anchor: Vector2, shadow_size: Vector2, lot_bounds: Rect2, frontage_offset: Vector2, visual_base_width := 122.0, harbor_integrated := false, district_placement_tags := [], notes := "") -> Dictionary:
	var sprite := sprite_config(sprite_id)
	var placement_tags: Array = district_placement_tags.duplicate()
	if placement_tags.is_empty():
		placement_tags = [district_role]
	var collision_footprint := _collision_footprint_for(building_id, lot_bounds, visual_base_width)
	var interaction_size := Vector2(maxf(84.0, collision_footprint.size.x * 0.76), 42.0)
	var interaction_zone := Rect2(frontage_offset - interaction_size * 0.5, interaction_size)
	var visual_bounds := _visual_bounds(sprite, draw_width, visual_base_anchor)
	return {
		"id": building_id,
		"building_id": building_id,
		"display_name": display_name,
		"role": district_role,
		"sprite_id": sprite_id,
		"texture_path": sprite.get("atlas_path", ""),
		"sprite_region": sprite.get("region", Rect2()),
		"sprite_source_size": sprite.get("source_size", Vector2.ZERO),
		"district_role": district_role,
		"intended_district_role": district_role,
		"visual_scale": draw_width,
		"scale": draw_width,
		"draw_width_override": draw_width,
		"foot_anchor": Vector2.ZERO,
		"source_foot_anchor": visual_base_anchor,
		"visual_base_anchor": visual_base_anchor,
		"visual_base_width": visual_base_width,
		"visual_bounds": visual_bounds,
		"collision_shape": "rectangle",
		"collision_footprint": collision_footprint,
		"collision_rect": collision_footprint,
		"collision_size": collision_footprint.size,
		"collision_offset": collision_footprint.position + collision_footprint.size * 0.5,
		"interaction_zone": interaction_zone,
		"interaction_size": interaction_size,
		"interaction_offset": frontage_offset,
		"interaction_zone_placeholder": true,
		"frontage_offset": frontage_offset,
		"door_offset": frontage_offset,
		"district_placement_tags": placement_tags,
		"notes": notes,
		"y_sort_offset": Vector2.ZERO,
		"shadow_offset": Vector2(0.0, -6.0),
		"shadow_size": shadow_size,
		"lot_bounds": lot_bounds,
		"lot_rect": lot_bounds,
		"building_volume_rect": lot_bounds,
		"frontage_body_rect": Rect2(Vector2(-visual_base_width * 0.5, -maxf(34.0, collision_footprint.size.y)), Vector2(visual_base_width, maxf(34.0, collision_footprint.size.y))),
		"harbor_integrated": harbor_integrated,
		"definition_normalized": true,
	}

static func _visual_bounds(sprite: Dictionary, draw_width: float, visual_base_anchor: Vector2, sprite_offset := Vector2.ZERO) -> Rect2:
	var source_size: Vector2 = sprite.get("source_size", Vector2(1.0, 1.0))
	var scale_factor := draw_width / maxf(1.0, source_size.x)
	return Rect2(-visual_base_anchor * scale_factor + sprite_offset, source_size * scale_factor)

static func _collision_footprint_for(building_id: String, lot_bounds: Rect2, visual_base_width: float) -> Rect2:
	match building_id:
		"b_inn_tavern":
			return _base_footprint(148.0, 18.0, 12.0)
		"b_mercantile":
			return _base_footprint(116.0, 16.0, 12.0)
		"b_counting_house":
			return _base_footprint(140.0, 16.0, 12.0)
		"b_chandlery_front":
			return _base_footprint(154.0, 16.0, 12.0)
		"b_shop_house":
			return _base_footprint(126.0, 16.0, 12.0)
		"b_market_shed":
			return _base_footprint(164.0, 18.0, 14.0)
		"b_custom_house":
			return _base_footprint(148.0, 18.0, 12.0)
		"b_large_residence":
			return _base_footprint(150.0, 18.0, 12.0)
		"b_boarding_house":
			return _base_footprint(104.0, 18.0, 12.0)
		"b_res_small":
			return _base_footprint(104.0, 16.0, 12.0)
		"b_cooperage_shed":
			return _base_footprint(92.0, 16.0, 12.0)
		"b_dock_storehouse":
			return _base_footprint(178.0, 34.0, 14.0)
		"b_wharf_boathouse":
			return _base_footprint(196.0, 38.0, 14.0)
		"b_dock_warehouse":
			return _base_footprint(174.0, 34.0, 14.0)
		"b_village_hall":
			return _base_footprint(142.0, 18.0, 12.0)
		_:
			var width := minf(lot_bounds.size.x, maxf(72.0, visual_base_width))
			var rear_depth := minf(24.0, maxf(16.0, lot_bounds.size.y * 0.18))
			return _base_footprint(width, rear_depth, 12.0)

static func _base_footprint(width: float, rear_depth: float, front_depth: float) -> Rect2:
	return Rect2(Vector2(-width * 0.5, -rear_depth), Vector2(width, rear_depth + front_depth))
