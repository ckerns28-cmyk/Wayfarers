extends RefCounted
class_name BuildingCatalog

const ATLAS_V1 := "res://assets/buildings/hearthvale_buildings_atlas_v1.png"
const PACK_A := "res://assets/buildings/hearthvale_newport_structure_pack_v1_a.png"
const PACK_B := "res://assets/buildings/hearthvale_newport_structure_pack_v1_b.png"
const ISOLATED_BUILDINGS := "res://assets/sprites/buildings/isolated"
const ATELIER_BUILDINGS := "res://art_pipeline/newport_atelier/generated"

static func sprite_config(sprite_id: String) -> Dictionary:
	match sprite_id:
		"inn_tavern_v1":
			return _sprite(ISOLATED_BUILDINGS + "/inn_tavern_v1_isolated.png", Rect2(0, 0, 473, 468), 142.0, Rect2(55, 24, 379, 420))
		"atelier_newport_tavern_inn_hero_01":
			return _sprite(ATELIER_BUILDINGS + "/atelier_newport_tavern_inn_hero_01.png", Rect2(0, 0, 1475, 959), 224.0, Rect2(28, 28, 1419, 903))
		"mercantile_shop":
			return _sprite(ISOLATED_BUILDINGS + "/mercantile_shop_isolated.png", Rect2(0, 0, 398, 451), 150.0, Rect2(83, 24, 277, 403))
		"atelier_newport_mercantile_store_01":
			return _sprite(ATELIER_BUILDINGS + "/atelier_newport_mercantile_store_01.png", Rect2(0, 0, 1310, 875), 108.0, Rect2(28, 28, 1254, 819))
		"village_hall_meeting_house":
			return _sprite(ISOLATED_BUILDINGS + "/village_hall_meeting_house_isolated.png", Rect2(0, 0, 438, 498), 178.0)
		"residence_small":
			return _sprite(ISOLATED_BUILDINGS + "/residence_small_isolated.png", Rect2(0, 0, 393, 368), 126.0)
		"atelier_newport_harbor_cottage_gabled_01":
			return _sprite(ATELIER_BUILDINGS + "/atelier_newport_harbor_cottage_gabled_01.png", Rect2(0, 0, 1209, 901), 138.0, Rect2(28, 28, 1153, 845))
		"residence_large":
			return _sprite(ATLAS_V1, Rect2(836, 418, 381, 418), 184.0)
		"hunter_lodge_or_outfitter":
			return _sprite(ATLAS_V1, Rect2(44, 836, 367, 343), 150.0)
		"service_dependency_shed":
			return _sprite(ISOLATED_BUILDINGS + "/service_dependency_shed_isolated.png", Rect2(0, 0, 298, 293), 124.0)
		"atelier_newport_cooperage_workshop_01":
			return _sprite(ATELIER_BUILDINGS + "/atelier_newport_cooperage_workshop_01.png", Rect2(0, 0, 1454, 913), 132.0, Rect2(28, 28, 1398, 857))
		"newport_georgian_merchant_residence_a":
			return _sprite(PACK_A, Rect2(57, 57, 361, 361), 178.0)
		"newport_elite_garden_mansion_a":
			return _sprite(PACK_A, Rect2(418, 76, 410, 332), 190.0)
		"newport_waterfront_shop_house":
			return _sprite(PACK_A, Rect2(864, 86, 351, 315), 170.0)
		"newport_large_front_residence":
			return _sprite(ISOLATED_BUILDINGS + "/newport_large_front_residence_isolated.png", Rect2(0, 0, 435, 369), 200.0)
		"newport_shopfront_awning":
			return _sprite(ISOLATED_BUILDINGS + "/newport_shopfront_awning_isolated.png", Rect2(0, 0, 413, 448), 150.0, Rect2(42, 52, 321, 312))
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
			return _sprite(PACK_B, Rect2(444, 67, 371, 336), 168.0, Rect2(16, 0, 335, 336))
		"newport_formal_townhouse_single_bay":
			return _sprite(PACK_B, Rect2(568, 67, 124, 336), 64.0)
		"newport_narrow_clapboard_townhouse_b":
			return _sprite(PACK_B, Rect2(60, 450, 280, 380), 104.0)
		"newport_elite_mansion_white":
			return _sprite(PACK_B, Rect2(840, 60, 380, 348), 192.0)
		"newport_modest_clapboard_residence_a":
			return _sprite(ISOLATED_BUILDINGS + "/newport_modest_clapboard_residence_a_isolated.png", Rect2(0, 0, 247, 418), 126.0)
		"atelier_newport_harbor_cottage_dormer_01":
			return _sprite(ATELIER_BUILDINGS + "/atelier_newport_harbor_cottage_dormer_01.png", Rect2(0, 0, 1089, 884), 132.0, Rect2(28, 28, 1033, 828))
		"newport_counting_house_civic_exchange":
			return _sprite(ISOLATED_BUILDINGS + "/newport_counting_house_civic_exchange_isolated.png", Rect2(0, 0, 458, 370), 190.0, Rect2(32, 24, 394, 322))
		"newport_chandlery_outfitter_front":
			return _sprite(ISOLATED_BUILDINGS + "/newport_chandlery_outfitter_front_isolated.png", Rect2(0, 0, 435, 400), 181.0, Rect2(31, 24, 365, 352))
		"newport_dockside_storehouse":
			return _sprite(ISOLATED_BUILDINGS + "/newport_dockside_storehouse_isolated.png", Rect2(0, 0, 443, 448), 220.0)
		"atelier_newport_wharf_warehouse_01":
			return _sprite(ATELIER_BUILDINGS + "/atelier_newport_wharf_warehouse_01.png", Rect2(0, 0, 1505, 853), 224.0, Rect2(28, 28, 1449, 797))
		"newport_market_shed_stalls":
			return _sprite(ISOLATED_BUILDINGS + "/newport_market_shed_stalls_isolated.png", Rect2(0, 0, 434, 438), 210.0, Rect2(35, 36, 344, 353))
		"newport_market_frontage_row":
			return _sprite(PACK_B, Rect2(836, 842, 373, 355), 178.0)
		_:
			push_error("Unknown building sprite id: " + sprite_id)
			return {}

static func building_definition(building_id: String) -> Dictionary:
	match building_id:
		"b_inn_tavern":
			return _definition(building_id, "Inn & Tavern", "atelier_newport_tavern_inn_hero_01", "tavern", 224.0, Vector2(737.5, 931.0), Vector2(196.0, 28.0), Rect2(Vector2(-104.0, -188.0), Vector2(208.0, 200.0)), Vector2(0.0, 28.0), 176.0, false, ["harborfront_commercial", "tavern", "centerpiece", "hero_landmark"], "G-4.21A hero rebuild: brick coastal inn, two sets of large front/back bridged twin-stack chimneys, warm windows, clear entrance, strong foundation, Hotel Viking-inspired landmark presence without direct copy.")
		"b_mercantile":
			return _definition(building_id, "Mercantile", "atelier_newport_mercantile_store_01", "mercantile", 108.0, Vector2(655.0, 847.0), Vector2(112.0, 18.0), Rect2(Vector2(-54.0, -112.0), Vector2(108.0, 124.0)), Vector2(0.0, 22.0), 96.0, false, ["harborfront_commercial", "commercial", "mercantile", "market_spine"], "G-4.21A rebuild candidate: practical coastal mercantile with readable shopfront and sign/awning compatibility; scaled to the market-spine footprint so it supports the Tavern/Inn hero instead of competing with it.")
		"b_counting_house":
			return _definition(building_id, "Town Hall / Counting House", "newport_counting_house_civic_exchange", "town_hall_counting_house", 190.0, Vector2(229.0, 346.0), Vector2(166.0, 18.0), Rect2(Vector2(-104.0, -166.0), Vector2(208.0, 178.0)), Vector2(0.0, 25.0), 150.0, false, ["inland_residential_civic", "civic", "town_hall", "counting_house"], "G-4.22A uses the stronger dedicated civic exchange sprite as the provisional Town Hall anchor instead of reactivating the old meeting-house crop.")
		"b_chandlery_front":
			return _definition(building_id, "Chandlery", "newport_chandlery_outfitter_front", "chandlery", 181.0, Vector2(217.5, 376.0), Vector2(154.0, 18.0), Rect2(Vector2(-92.0, -168.0), Vector2(184.0, 180.0)), Vector2(0.0, 24.0), 132.0)
		"b_shop_house":
			return _definition(building_id, "Shop House", "newport_shopfront_awning", "shop", 190.0, Vector2(206.5, 364.0), Vector2(162.0, 20.0), Rect2(Vector2(-96.0, -174.0), Vector2(192.0, 186.0)), Vector2(0.0, 24.0), 146.0)
		"b_market_shed":
			return _definition(building_id, "Market Shed", "newport_market_shed_stalls", "dock_service", 210.0, Vector2(217.0, 389.0), Vector2(154.0, 18.0), Rect2(Vector2(-86.0, -92.0), Vector2(172.0, 102.0)), Vector2(0.0, 24.0), 132.0)
		"b_dock_storehouse":
			return _definition(building_id, "Dock Storehouse", "newport_dockside_storehouse_long", "warehouse", 220.0, Vector2(194.0, 318.0), Vector2(176.0, 18.0), Rect2(Vector2(-104.0, -122.0), Vector2(208.0, 128.0)), Vector2(0.0, 20.0), 156.0, true)
		"b_wharf_boathouse":
			return _definition(building_id, "Wharf Boathouse", "newport_wharf_boathouse_large", "dock_service", 280.0, Vector2(289.0, 378.0), Vector2(196.0, 20.0), Rect2(Vector2(-124.0, -138.0), Vector2(248.0, 146.0)), Vector2(0.0, 22.0), 190.0, true)
		"b_dock_warehouse":
			return _definition(building_id, "Dock Warehouse", "atelier_newport_wharf_warehouse_01", "warehouse", 224.0, Vector2(752.5, 610.0), Vector2(176.0, 22.0), Rect2(Vector2(-108.0, -134.0), Vector2(216.0, 146.0)), Vector2(0.0, 22.0), 164.0, true, ["working_wharf", "dock_service", "warehouse"], "G-4.21A rebuild candidate: working wharf warehouse/dock office with weathered wood, brick, stone foundation, and cargo-door readability.")
		"b_custom_house":
			return _definition(building_id, "Custom House", "newport_custom_house_civic_front", "customs_house", 176.0, Vector2(214.5, 409.0), Vector2(164.0, 20.0), Rect2(Vector2(-96.0, -146.0), Vector2(192.0, 156.0)), Vector2(0.0, 24.0), 146.0, false, ["inland_residential_civic", "harborfront_commercial", "civic", "customs"], "G-4.11 intentional civic/admin anchor; uses the dedicated custom house asset from the left side of Newport pack B.")
		"b_village_hall":
			return _definition(building_id, "Village Hall", "village_hall_meeting_house", "deferred_chapel", 178.0, Vector2(219.0, 454.0), Vector2(160.0, 20.0), Rect2(Vector2(-92.0, -152.0), Vector2(184.0, 164.0)), Vector2(0.0, 24.0), 142.0, false, ["deferred", "chapel"], "Deferred yellow meeting-house crop; G-4.22A does not use this as an active civic anchor.")
		"b_res_small":
			return _definition(building_id, "Harbor Cottage", "atelier_newport_harbor_cottage_gabled_01", "residence", 138.0, Vector2(604.5, 873.0), Vector2(112.0, 18.0), Rect2(Vector2(-68.0, -118.0), Vector2(136.0, 130.0)), Vector2(0.0, 22.0), 108.0, false, ["inland_residential_civic", "residential", "cottage"], "G-4.21A residence rebuild candidate: quiet gabled harbor cottage with Newport coastal clapboard language.")
		"b_large_residence":
			return _definition(building_id, "Harbor Residence", "newport_large_front_residence", "large_residence", 200.0, Vector2(217.5, 345.0), Vector2(156.0, 18.0), Rect2(Vector2(-92.0, -142.0), Vector2(184.0, 152.0)), Vector2(0.0, 23.0), 142.0, false, ["inland_residential_civic", "residential", "civic_residence"], "Integrated from Newport pack A with an isolated crop so the full residence and side dressing are visible.")
		"b_boarding_house":
			return _definition(building_id, "Boarding House", "atelier_newport_harbor_cottage_dormer_01", "boarding_house", 132.0, Vector2(544.5, 856.0), Vector2(112.0, 18.0), Rect2(Vector2(-66.0, -126.0), Vector2(132.0, 138.0)), Vector2(0.0, 21.0), 108.0, false, ["support_lane", "inland_residential_civic", "residential", "cottage"], "G-4.21A residence rebuild candidate: dormered coastal boarding cottage with a distinct quiet residential silhouette.")
		"b_cooperage_shed":
			return _definition(building_id, "Cooperage Shed", "atelier_newport_cooperage_workshop_01", "cooperage", 132.0, Vector2(727.0, 885.0), Vector2(98.0, 18.0), Rect2(Vector2(-60.0, -108.0), Vector2(120.0, 120.0)), Vector2(0.0, 20.0), 96.0, false, ["support_lane", "working_wharf", "dock_service", "service_building"], "G-4.21A service rebuild candidate: cooperage workshop with barrel repair and grounded service-lane utility.")
		"b_printer_rowhouse":
			return _definition(building_id, "Printer Rowhouse", "newport_narrow_merchant_townhouse_a", "printer_rowhouse", 118.0, Vector2(136.5, 385.0), Vector2(96.0, 16.0), Rect2(Vector2(-52.0, -154.0), Vector2(104.0, 166.0)), Vector2(0.0, 24.0), 92.0, false, ["harborfront_commercial", "commercial", "rowhouse", "future_printer"], "G-4.15 scales the narrow printer rowhouse at the asset's Newport default width so it reads as a real street-wall building beside the market shed instead of a prop-sized infill.")
		"b_clerk_townhouse":
			return _definition(building_id, "Clerk Townhouse", "newport_formal_townhouse_block_a", "clerk_lodging", 168.0, Vector2(185.5, 336.0), Vector2(136.0, 15.0), Rect2(Vector2(-78.0, -140.0), Vector2(156.0, 152.0)), Vector2(0.0, 24.0), 136.0, false, ["harborfront_commercial", "residential", "rowhouse", "future_clerk_lodging"], "G-4.13B.7 brick formal townhouse row restored at Newport scale and packed by street-wall art bounds rather than transparent or prop padding.")
		"b_dockworker_rowhouse":
			return _definition(building_id, "Dockworker Rowhouse", "newport_waterfront_shop_house", "dockworker_lodging", 154.0, Vector2(175.5, 300.0), Vector2(124.0, 15.0), Rect2(Vector2(-76.0, -112.0), Vector2(152.0, 124.0)), Vector2(0.0, 21.0), 124.0, false, ["support_lane", "residential", "rowhouse", "future_dockworker_lodging"], "G-4.13B.1 support-lane lodging infill using the four-unit clapboard rowhouse from Newport pack A, seated beside the boarding house with a hard visible gap.")
		_:
			push_error("Unknown building definition id: " + building_id)
			return {}

static func available_building_assets() -> Array:
	return [
		_asset("inn_tavern_v1", "tavern / inn", "integrated", "Accepted isolated tavern anchor."),
		_asset("atelier_newport_tavern_inn_hero_01", "tavern / inn", "integrated_g421a", "G-4.21A hero building rebuild: brick coastal inn with two twin-stack chimney sets."),
		_asset("mercantile_shop", "mercantile / general goods", "integrated", "Accepted isolated shop anchor."),
		_asset("atelier_newport_mercantile_store_01", "mercantile / general goods", "integrated_g421a", "G-4.21A coastal mercantile rebuild candidate."),
		_asset("newport_counting_house_civic_exchange", "counting house / civic exchange", "integrated", "Accepted isolated harborfront office."),
		_asset("newport_chandlery_outfitter_front", "chandlery / rope / sail shop", "integrated", "Accepted isolated working-harbor storefront."),
		_asset("newport_shopfront_awning", "shop house / general storefront", "integrated", "Accepted isolated harborfront shop."),
		_asset("newport_market_shed_stalls", "fishmonger / market shed", "integrated", "Accepted isolated market/fish stall."),
		_asset("newport_dockside_storehouse_long", "warehouse", "integrated", "Accepted isolated long dock storehouse."),
		_asset("newport_wharf_boathouse_large", "dock shack / boathouse", "integrated", "Accepted isolated wharf service building."),
		_asset("newport_dockside_storehouse", "warehouse / dock service", "integrated", "Accepted isolated dock warehouse."),
		_asset("atelier_newport_wharf_warehouse_01", "warehouse / dock service", "integrated_g421a", "G-4.21A wharf warehouse / dock office rebuild candidate."),
		_asset("newport_custom_house_civic_front", "customs house / civic", "integrated_g411", "Dedicated custom-house asset intentionally used as the starter civic/admin anchor."),
		_asset("residence_small", "small residence", "integrated", "Accepted isolated cottage."),
		_asset("atelier_newport_harbor_cottage_gabled_01", "small residence", "integrated_g421a", "G-4.21A quiet gabled harbor cottage variant."),
		_asset("newport_large_front_residence", "large residence / civic residence", "integrated_g411", "Adds inland residential depth using an isolated full-width crop."),
		_asset("newport_modest_clapboard_residence_a", "boarding house / small residence", "integrated_g411", "Adds support-lane housing using an isolated crop."),
		_asset("atelier_newport_harbor_cottage_dormer_01", "boarding house / small residence", "integrated_g421a", "G-4.21A dormered coastal cottage / boarding-house variant."),
		_asset("service_dependency_shed", "cooperage / barrel shop / dock shack", "integrated_g411", "Temporary support/service role using an isolated crop."),
		_asset("atelier_newport_cooperage_workshop_01", "cooperage / barrel shop / dock shack", "integrated_g421a", "G-4.21A cooperage workshop/service-lane rebuild candidate."),
		_asset("village_hall_meeting_house", "church / chapel", "deferred", "Demoted in G-4.11; not used as the starter civic anchor."),
		_asset("residence_large", "large residence", "available_deferred", "Base atlas residence; not active in starter pass."),
		_asset("hunter_lodge_or_outfitter", "outfitter / rural lodge", "available_deferred", "Less Newport-civic than current set."),
		_asset("newport_georgian_merchant_residence_a", "large residence / merchant residence", "available_deferred", "Possible G-4.12 composition candidate."),
		_asset("newport_elite_garden_mansion_a", "large residence / civic residence", "available_deferred", "Too grand for the starter harbor core right now."),
		_asset("newport_waterfront_shop_house", "dockworker rowhouse / attached housing", "integrated_g413b", "Used for the Dockworker Rowhouse four-unit clapboard street-wall infill beside the boarding-house/support lane."),
		_asset("newport_narrow_merchant_townhouse_a", "shop house / townhouse", "integrated_g413b", "Used for the Printer Rowhouse street-front infill east of the market shed."),
		_asset("newport_chandlery_cottage", "chandlery / cottage / service shop", "available_deferred", "Possible smaller service-lane shop."),
		_asset("newport_formal_townhouse_block_a", "formal townhouse row / residential row", "integrated_g413b", "Used for the Clerk Townhouse brick rowhouse after QA clarified the intended asset and placement against the mercantile."),
		_asset("newport_formal_townhouse_single_bay", "formal single-bay townhouse / clerk lodging", "rejected_g413b", "Rejected after QA because the crop reads like a sliced facade column rather than a complete building."),
		_asset("newport_narrow_clapboard_townhouse_b", "narrow clapboard townhouse / clerk lodging", "available_deferred", "Available for later residential infill, but not used for the Clerk Townhouse after QA requested the brick rowhouse asset."),
		_asset("newport_elite_mansion_white", "large residence / boarding house", "available_deferred", "Potential upper-town residence."),
		_asset("newport_market_frontage_row", "mercantile / market frontage", "available_deferred", "Duplicate commercial frontage for later dressing."),
	]

static func _sprite(atlas_path: String, region: Rect2, draw_width: float, visible_region := Rect2()) -> Dictionary:
	var normalized_visible_region := visible_region
	if normalized_visible_region.size.x <= 0.0 or normalized_visible_region.size.y <= 0.0:
		normalized_visible_region = Rect2(Vector2.ZERO, region.size)
	return {
		"atlas_path": atlas_path,
		"region": region,
		"source_size": region.size,
		"visible_region": normalized_visible_region,
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
	var door_anchor := frontage_offset
	var interaction_size := _interaction_size_for(building_id, collision_footprint)
	var interaction_zone := Rect2(door_anchor - interaction_size * 0.5, interaction_size)
	var visual_bounds := _visual_bounds(sprite, draw_width, visual_base_anchor)
	var review_lot_bounds := _review_lot_bounds(building_id, lot_bounds, visual_bounds)
	var entity_metadata := _entity_metadata_for(building_id, display_name, district_role)
	var projection_details := _projection_details_for(building_id)
	return {
		"id": building_id,
		"building_id": building_id,
		"display_name": display_name,
		"role": district_role,
		"building_type": entity_metadata.get("building_type", district_role),
		"access_rule": entity_metadata.get("access_rule", "locked"),
		"interior_scene": entity_metadata.get("interior_scene", "res://scenes/interiors/building_stub.tscn"),
		"owner_id": entity_metadata.get("owner_id", ""),
		"is_enterable": entity_metadata.get("is_enterable", false),
		"interaction_enabled": entity_metadata.get("interaction_enabled", false),
		"interaction_label": entity_metadata.get("interaction_label", ""),
		"locked_message": entity_metadata.get("locked_message", ""),
		"unavailable_message": entity_metadata.get("unavailable_message", ""),
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
		"door_anchor": door_anchor,
		"district_placement_tags": placement_tags,
		"notes": notes,
		"y_sort_offset": Vector2.ZERO,
		"y_sort_anchor": Vector2.ZERO,
		"shadow_offset": Vector2(0.0, -6.0),
		"shadow_size": shadow_size,
		"projection_details": projection_details,
		"lot_bounds": review_lot_bounds,
		"lot_rect": review_lot_bounds,
		"building_volume_rect": review_lot_bounds,
		"frontage_body_rect": Rect2(Vector2(-visual_base_width * 0.5, -maxf(34.0, collision_footprint.size.y)), Vector2(visual_base_width, maxf(34.0, collision_footprint.size.y))),
		"ground_contact_rect": Rect2(Vector2(-visual_base_width * 0.5, -4.0), Vector2(visual_base_width, 8.0)),
		"harbor_integrated": harbor_integrated,
		"definition_normalized": true,
	}

static func _projection_details_for(building_id: String) -> Array:
	match building_id:
		"b_mercantile":
			return [
				_projection_detail("mercantile_hanging_sign", Rect2(Vector2(1194.0, 418.0), Vector2(108.0, 172.0)), 12),
			]
		_:
			return []

static func _projection_detail(id: String, source_rect: Rect2, z_index: int) -> Dictionary:
	return {
		"id": id,
		"source_rect": source_rect,
		"z_index": z_index,
	}

static func _visual_bounds(sprite: Dictionary, draw_width: float, visual_base_anchor: Vector2, sprite_offset := Vector2.ZERO) -> Rect2:
	var source_size: Vector2 = sprite.get("source_size", Vector2(1.0, 1.0))
	var visible_region: Rect2 = sprite.get("visible_region", Rect2(Vector2.ZERO, source_size))
	var scale_factor := draw_width / maxf(1.0, source_size.x)
	return Rect2((visible_region.position - visual_base_anchor) * scale_factor + sprite_offset, visible_region.size * scale_factor)

static func _review_lot_bounds(building_id: String, declared_lot_bounds: Rect2, visual_bounds: Rect2) -> Rect2:
	match building_id:
		"b_inn_tavern", "b_clerk_townhouse", "b_mercantile", "b_counting_house", "b_chandlery_front", "b_shop_house", "b_market_shed", "b_printer_rowhouse", "b_boarding_house", "b_dockworker_rowhouse":
			return visual_bounds
		_:
			return declared_lot_bounds

static func _entity_metadata_for(building_id: String, display_name: String, district_role: String) -> Dictionary:
	match building_id:
		"b_inn_tavern":
			return _entity("tavern", "public", "res://scenes/interiors/tavern_stub.tscn", true, "Press E to enter Inn & Tavern", "", "Inn & Tavern will be enterable in G-4.15.")
		"b_mercantile":
			return _entity("mercantile", "public", "res://scenes/interiors/mercantile_stub.tscn", true, "Press E to enter Harbor Mercantile", "", "Harbor Mercantile will be enterable in G-4.15.")
		"b_counting_house":
			return _entity("civic", "public", "res://scenes/interiors/counting_house_stub.tscn", true, "Press E to enter Town Hall / Counting House", "", "Town Hall / Counting House will be enterable in G-4.15.")
		"b_chandlery_front":
			return _entity("shop", "public", "res://scenes/interiors/chandlery_stub.tscn", true, "Press E to enter Chandlery", "", "The Chandlery will be enterable in G-4.15.")
		"b_shop_house":
			return _entity("shop", "public", "res://scenes/interiors/shop_house_stub.tscn", true, "Press E to enter Shop House", "", "The Shop House will be enterable in G-4.15.")
		"b_custom_house":
			return _entity("civic", "locked", "res://scenes/interiors/customs_house_stub.tscn", false, "Press E to inspect Customs House", "", "The Customs House is not open yet.")
		"b_market_shed":
			return _entity("shop", "locked", "res://scenes/interiors/market_shed_stub.tscn", false, "Press E to inspect Market Shed", "", "The market shed is not staffed yet.")
		"b_printer_rowhouse":
			return _entity("rowhouse", "locked", "res://scenes/interiors/printer_rowhouse_stub.tscn", false, "Press E to inspect Printer Rowhouse", "", "The printer rowhouse is not open yet.")
		"b_clerk_townhouse":
			return _entity("rowhouse", "private", "res://scenes/interiors/residence_stub.tscn", false, "Press E to inspect Clerk Townhouse", "This rowhouse is private.", "")
		"b_res_small":
			return _entity("residence", "owner_only_future", "res://scenes/interiors/residence_stub.tscn", false, "Press E to inspect Harbor Cottage", "This residence is private.", "This cottage is reserved for future ownership.")
		"b_large_residence":
			return _entity("residence", "private", "res://scenes/interiors/residence_stub.tscn", false, "Press E to inspect Harbor Residence", "This residence is private.", "")
		"b_boarding_house":
			return _entity("boarding_house", "private", "res://scenes/interiors/boarding_house_stub.tscn", false, "Press E to inspect Boarding House", "The boarding house is private for now.", "")
		"b_dockworker_rowhouse":
			return _entity("rowhouse", "private", "res://scenes/interiors/residence_stub.tscn", false, "Press E to inspect Dockworker Rowhouse", "This rowhouse is private.", "")
		"b_dock_storehouse":
			return _entity("warehouse", "locked", "res://scenes/interiors/warehouse_stub.tscn", false, "Press E to inspect Dock Storehouse", "", "The dock storehouse is locked.")
		"b_dock_warehouse":
			return _entity("warehouse", "locked", "res://scenes/interiors/warehouse_stub.tscn", false, "Press E to inspect Dock Warehouse", "", "The dock warehouse is locked.")
		"b_wharf_boathouse":
			return _entity("dock_service", "locked", "res://scenes/interiors/boathouse_stub.tscn", false, "Press E to inspect Wharf Boathouse", "", "The wharf boathouse is locked.")
		"b_cooperage_shed":
			return _entity("dock_service", "locked", "res://scenes/interiors/cooperage_stub.tscn", false, "Press E to inspect Cooperage Shed", "", "The cooperage shed is not open yet.")
		"b_village_hall":
			return _entity("deferred_chapel", "locked", "res://scenes/interiors/building_stub.tscn", false, "Press E to inspect Village Hall", "", "The old Village Hall crop is deferred from normal review.")
		_:
			return _entity(district_role, "locked", "res://scenes/interiors/building_stub.tscn", false, "Press E to inspect " + display_name, "", display_name + " is not open yet.")

static func _entity(building_type: String, access_rule: String, interior_scene: String, is_enterable: bool, interaction_label: String, locked_message: String, unavailable_message: String, owner_id := "") -> Dictionary:
	return {
		"building_type": building_type,
		"access_rule": access_rule,
		"interior_scene": interior_scene,
		"owner_id": owner_id,
		"is_enterable": is_enterable,
		"interaction_enabled": true,
		"interaction_label": interaction_label,
		"locked_message": locked_message,
		"unavailable_message": unavailable_message,
	}

static func _collision_footprint_for(building_id: String, lot_bounds: Rect2, visual_base_width: float) -> Rect2:
	match building_id:
		"b_inn_tavern":
			return _base_footprint(148.0, 18.0, 12.0)
		"b_mercantile":
			return _base_footprint(108.0, 10.0, 18.0)
		"b_counting_house":
			return _base_footprint(140.0, 16.0, 12.0)
		"b_chandlery_front":
			return _base_footprint(154.0, 16.0, 12.0)
		"b_shop_house":
			return _base_footprint(150.0, 16.0, 12.0)
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
		"b_printer_rowhouse":
			return _base_footprint(92.0, 18.0, 12.0)
		"b_clerk_townhouse":
			return _base_footprint(132.0, 18.0, 12.0)
		"b_dockworker_rowhouse":
			return _base_footprint(124.0, 18.0, 12.0)
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

static func _interaction_size_for(building_id: String, _collision_footprint: Rect2) -> Vector2:
	match building_id:
		"b_dock_storehouse", "b_dock_warehouse", "b_wharf_boathouse":
			return Vector2(64.0, 36.0)
		"b_counting_house", "b_custom_house", "b_village_hall":
			return Vector2(58.0, 36.0)
		"b_inn_tavern", "b_mercantile", "b_chandlery_front", "b_shop_house":
			return Vector2(56.0, 34.0)
		"b_market_shed":
			return Vector2(60.0, 34.0)
		_:
			return Vector2(48.0, 32.0)
