extends Node2D

@export_enum("ground", "roads", "wharf_water", "props") var layer_id := "ground"

const NEWPORT_TOWN := preload("res://scripts/NewportTownBlueprint.gd")
const BUILDING_CATALOG := preload("res://scripts/BuildingCatalog.gd")
const TILE := NEWPORT_TOWN.TILE
const MAP_W := NEWPORT_TOWN.MAP_TILES.x
const MAP_H := NEWPORT_TOWN.MAP_TILES.y
const NEWPORT_SURFACE_KIT_VERSION := "G-4.16"
const NEWPORT_HERO_ATLAS_VERSION := "G-4.18"
const NEWPORT_HERO_ATLAS_PATH := "res://art_pipeline/newport/atlases/newport_hero_street_atlas_v1.png"
const NEWPORT_GREEN_ORIGIN_VERSION := "G-4.18B"
const NEWPORT_GREEN_ORIGIN_ATLAS_PATH := "res://art_pipeline/newport_green_origin/atlases/newport_green_origin_dock_factory_v1.png"
const G418D1_M01B_PROOF_PATH := "res://art_pipeline/newport_green_origin/method_bakeoff/generated/method_01b_manual_paintover_proof.png"
const G418D2_CAPABILITY_ASSET_PATH := "res://art_pipeline/newport_green_origin/method_bakeoff/generated/g418d2_rope_crate_barrel_cluster.png"
const NEWPORT_ATELIER_CARGO_VERSION := "G-4.18D"
const NEWPORT_ATELIER_CARGO_ATLAS_PATH := "res://art_pipeline/newport_atelier/atlases/newport_atelier_cargo_v1.png"
const NEWPORT_ATELIER_DOCK_CLUTTER_VERSION := "G-4.19A"
const NEWPORT_ATELIER_DOCK_CLUTTER_ATLAS_PATH := "res://art_pipeline/newport_atelier/atlases/newport_atelier_dock_clutter_v1.png"
const NEWPORT_ENVIRONMENTAL_BELIEVABILITY_VERSION := "G-4.20A"
const NEWPORT_ATELIER_TERRAIN_EDGE_ATLAS_PATH := "res://art_pipeline/newport_atelier/atlases/newport_atelier_terrain_edge_dressing_v1.png"
const NEWPORT_ATELIER_COBBLE_PATH_ATLAS_PATH := "res://art_pipeline/newport_atelier/atlases/newport_atelier_cobble_path_transition_v1.png"
const NEWPORT_ATELIER_SHORELINE_ATLAS_PATH := "res://art_pipeline/newport_atelier/atlases/newport_atelier_shoreline_harbor_edge_v1.png"
const NEWPORT_ATELIER_BUILDING_GROUNDING_ATLAS_PATH := "res://art_pipeline/newport_atelier/atlases/newport_atelier_building_grounding_service_v1.png"
const NEWPORT_TOWN_IDENTITY_VERSION := "G-4.20B"
const NEWPORT_ATELIER_SIGN_SHOP_MARKERS_ATLAS_PATH := "res://art_pipeline/newport_atelier/atlases/newport_atelier_sign_shop_markers_v1.png"
const NEWPORT_ATELIER_LAMPS_WAYFINDING_ATLAS_PATH := "res://art_pipeline/newport_atelier/atlases/newport_atelier_lamps_wayfinding_v1.png"
const NEWPORT_ATELIER_CIVIC_MARKET_ATLAS_PATH := "res://art_pipeline/newport_atelier/atlases/newport_atelier_civic_market_identity_v1.png"
const NEWPORT_ATELIER_SHOPFRONT_SUPPORT_ATLAS_PATH := "res://art_pipeline/newport_atelier/atlases/newport_atelier_shopfront_support_accents_v1.png"
const NEWPORT_G418E_HERO_ASSET_FAMILY_VERSION := "G-4.18E"
const NEWPORT_G418E_TAVERN_INN_ATLAS_PATH := "res://art_pipeline/newport_atelier/atlases/newport_atelier_g418e_tavern_inn_district_v1.png"
const NEWPORT_G418E_COMMERCIAL_AVENUE_ATLAS_PATH := "res://art_pipeline/newport_atelier/atlases/newport_atelier_g418e_commercial_avenue_v1.png"
const NEWPORT_G418E_HARBOR_DOCK_EDGE_ATLAS_PATH := "res://art_pipeline/newport_atelier/atlases/newport_atelier_g418e_harbor_dock_edge_v1.png"
const NEWPORT_G418E_REAR_SERVICE_CONNECTOR_ATLAS_PATH := "res://art_pipeline/newport_atelier/atlases/newport_atelier_g418e_rear_service_connector_v1.png"
const NEWPORT_ATELIER_CHARACTER_VERSION := "G-4.22R"
const NEWPORT_ATELIER_CHARACTER_ATLAS_PATH := "res://art_pipeline/player_identity/atlases/newport_npc_atelier_g422r_v1.png"
const G422R_SUPPRESS_PRIMITIVE_WORLD_PROPS := true
const G422R_HIDE_NORMAL_PLAY_LAYOUT_GUIDES := true
const STARTER_VILLAGE_G7A_COHESION_PASS := "G-7A"
const G7A_TOWN_COHESION_PHASE_SCORE := 7.6
const STARTER_VILLAGE_G7B_HARBOR_SPINE_PASS := "G-7B"
const G7B_HARBOR_WORLD_SCORE := 8.5
const STARTER_VILLAGE_G7C_LANDMARK_IDENTITY_PASS := "G-7C"
const G7C_ART_WORLD_SCORE := 8.5
const STARTER_VILLAGE_G8A_LIVING_NPC_POPULATION_PASS := "G-8A"
const G8A_NPC_POPULATION_SCORE := 8.5
const G8A_RUNTIME_NPC_NODES_ENABLED := true
const G8A_NPC_MOVEMENT_POLICY := "stationary_work_pose_until_dedicated_walk_sheets"
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
const NEWPORT_ATELIER_CARGO_MATERIALS := [
	"atelier_newport_crate_01",
	"atelier_newport_barrel_01",
	"atelier_newport_rope_coil_01",
	"atelier_wharf_cargo_cluster_01",
]
const NEWPORT_ATELIER_DOCK_CLUTTER_MATERIALS := [
	"atelier_dock_bollards_01",
	"atelier_mooring_hardware_01",
	"atelier_fishing_net_bundle_01",
	"atelier_sacks_fish_baskets_01",
	"atelier_anchor_rope_01",
	"atelier_dock_repair_planks_01",
	"atelier_dock_lantern_01",
	"atelier_shoreline_debris_01",
]
const NEWPORT_ATELIER_TERRAIN_EDGE_MATERIALS := [
	"atelier_terrain_grass_road_edge_north_01",
	"atelier_terrain_grass_road_edge_south_01",
	"atelier_terrain_mud_cobble_feather_01",
	"atelier_terrain_dirt_path_border_01",
	"atelier_terrain_worn_corner_blend_01",
	"atelier_terrain_coastal_tuft_stone_cluster_01",
	"atelier_terrain_muddy_puddle_rut_01",
	"atelier_terrain_broken_grassy_shoulder_01",
]
const NEWPORT_ATELIER_COBBLE_PATH_MATERIALS := [
	"atelier_path_market_cobble_long_01",
	"atelier_path_broken_cobble_patch_01",
	"atelier_path_dirt_worn_section_01",
	"atelier_path_road_shoulder_earth_01",
	"atelier_path_curb_threshold_stones_01",
	"atelier_path_cobble_plank_seam_01",
	"atelier_path_sunken_gutter_stones_01",
	"atelier_path_loose_paving_fragments_01",
]
const NEWPORT_ATELIER_SHORELINE_MATERIALS := [
	"atelier_shore_seaweed_drift_line_01",
	"atelier_shore_shell_pebble_cluster_01",
	"atelier_shore_wet_rocks_sand_01",
	"atelier_shore_driftwood_log_cluster_01",
	"atelier_shore_wet_sand_mud_strip_01",
	"atelier_shore_harbor_debris_slats_rope_01",
	"atelier_shore_tide_puddle_mud_edge_01",
	"atelier_shore_eelgrass_reeds_cluster_01",
]
const NEWPORT_ATELIER_BUILDING_GROUNDING_MATERIALS := [
	"atelier_ground_doorstep_stones_01",
	"atelier_ground_foundation_shadow_strip_01",
	"atelier_ground_wall_weeds_stones_01",
	"atelier_ground_repair_boards_crate_scraps_01",
	"atelier_ground_barrel_crate_cluster_01",
	"atelier_ground_wash_tub_buckets_01",
	"atelier_ground_low_fence_weeds_01",
	"atelier_ground_firewood_chopping_block_01",
]
const NEWPORT_ATELIER_SIGN_SHOP_MARKER_MATERIALS := [
	"atelier_sign_tavern_inn_placeholder_01",
	"atelier_sign_mercantile_crate_marker_01",
	"atelier_sign_fishmonger_icon_board_01",
	"atelier_sign_dock_warehouse_barrel_anchor_01",
	"atelier_sign_inn_rooms_key_board_01",
	"atelier_sign_harbor_direction_arrows_01",
	"atelier_sign_hanging_bracket_iron_01",
	"atelier_sign_painted_shop_plaque_01",
]
const NEWPORT_ATELIER_LAMPS_WAYFINDING_MATERIALS := [
	"atelier_wayfinding_street_lamp_post_01",
	"atelier_wayfinding_dock_lantern_post_01",
	"atelier_wayfinding_multi_arrow_signpost_01",
	"atelier_wayfinding_bollard_lantern_01",
	"atelier_wayfinding_harbor_road_marker_01",
	"atelier_wayfinding_rope_rail_post_pair_01",
	"atelier_wayfinding_pier_lantern_stand_01",
	"atelier_wayfinding_coastal_waystone_01",
]
const NEWPORT_ATELIER_CIVIC_MARKET_MATERIALS := [
	"atelier_civic_town_notice_board_01",
	"atelier_civic_market_banner_strand_01",
	"atelier_civic_harbor_bulletin_board_01",
	"atelier_civic_flag_cluster_01",
	"atelier_civic_anchor_plaque_01",
	"atelier_civic_posting_pole_01",
	"atelier_civic_market_pennant_sign_01",
	"atelier_civic_dock_rules_board_01",
]
const NEWPORT_ATELIER_SHOPFRONT_SUPPORT_MATERIALS := [
	"atelier_shopfront_canvas_awning_segment_01",
	"atelier_shopfront_display_crates_slate_01",
	"atelier_shopfront_folded_cloth_bundle_01",
	"atelier_shopfront_chalk_slate_board_01",
	"atelier_shopfront_hanging_basket_01",
	"atelier_shopfront_coastal_planter_01",
	"atelier_shopfront_rope_pennant_rail_01",
	"atelier_shopfront_basket_parcel_display_01",
]
const NEWPORT_G418E_TAVERN_INN_MATERIALS := [
	"atelier_g418e_tavern_hanging_inn_sign_01",
	"atelier_g418e_tavern_entry_lantern_pair_01",
	"atelier_g418e_tavern_threshold_planters_01",
	"atelier_g418e_tavern_service_barrel_crate_01",
	"atelier_g418e_tavern_brick_threshold_01",
	"atelier_g418e_tavern_twin_stack_chimney_detail_01",
	"atelier_g418e_tavern_stable_tack_rack_01",
	"atelier_g418e_tavern_firewood_coal_scuttle_01",
]
const NEWPORT_G418E_COMMERCIAL_AVENUE_MATERIALS := [
	"atelier_g418e_commercial_mercantile_sign_01",
	"atelier_g418e_commercial_fishmonger_sign_01",
	"atelier_g418e_commercial_market_cart_01",
	"atelier_g418e_commercial_produce_crates_01",
	"atelier_g418e_commercial_basket_parcel_display_01",
	"atelier_g418e_commercial_canvas_awning_roll_01",
	"atelier_g418e_commercial_street_lamp_01",
	"atelier_g418e_commercial_directional_signpost_01",
]
const NEWPORT_G418E_HARBOR_DOCK_EDGE_MATERIALS := [
	"atelier_g418e_harbor_dock_barrel_row_01",
	"atelier_g418e_harbor_rope_coil_large_01",
	"atelier_g418e_harbor_fishing_crate_net_stack_01",
	"atelier_g418e_harbor_net_drying_frame_01",
	"atelier_g418e_harbor_bollard_pair_01",
	"atelier_g418e_harbor_cargo_stack_01",
	"atelier_g418e_harbor_service_post_lantern_01",
	"atelier_g418e_harbor_fish_baskets_tub_01",
]
const NEWPORT_G418E_REAR_SERVICE_CONNECTOR_MATERIALS := [
	"atelier_g418e_service_fence_gate_01",
	"atelier_g418e_service_utility_barrels_01",
	"atelier_g418e_service_alley_crates_01",
	"atelier_g418e_service_firewood_barrow_01",
	"atelier_g418e_service_stone_edge_01",
	"atelier_g418e_service_wash_tub_linen_01",
	"atelier_g418e_service_rain_barrel_01",
	"atelier_g418e_service_repair_sawhorse_01",
]
const NEWPORT_ATELIER_CHARACTER_MATERIALS := [
	"npc_dockworker_atelier_g422r",
	"npc_market_vendor_atelier_g422r",
	"npc_civic_clerk_atelier_g422r",
]
const G422R_HIDDEN_NORMAL_PLAY_MARKER_ASSETS := [
	"atelier_sign_tavern_inn_placeholder_01",
	"atelier_sign_mercantile_crate_marker_01",
	"atelier_sign_fishmonger_icon_board_01",
	"atelier_sign_dock_warehouse_barrel_anchor_01",
	"atelier_sign_harbor_direction_arrows_01",
	"atelier_sign_hanging_bracket_iron_01",
	"atelier_sign_painted_shop_plaque_01",
	"atelier_wayfinding_multi_arrow_signpost_01",
	"atelier_wayfinding_harbor_road_marker_01",
	"atelier_civic_town_notice_board_01",
	"atelier_civic_posting_pole_01",
	"atelier_civic_dock_rules_board_01",
	"atelier_shopfront_chalk_slate_board_01",
	"atelier_g418e_tavern_hanging_inn_sign_01",
	"atelier_g418e_commercial_mercantile_sign_01",
	"atelier_g418e_commercial_fishmonger_sign_01",
	"atelier_g418e_commercial_directional_signpost_01",
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
const NEWPORT_ATELIER_CARGO_ATLAS_REGIONS := {
	"atelier_newport_crate_01": Rect2(80, 36, 575, 486),
	"atelier_newport_barrel_01": Rect2(900, 38, 428, 488),
	"atelier_newport_rope_coil_01": Rect2(76, 574, 610, 374),
	"atelier_wharf_cargo_cluster_01": Rect2(710, 548, 758, 472),
}
const NEWPORT_ATELIER_DOCK_CLUTTER_ATLAS_REGIONS := {
	"atelier_dock_bollards_01": Rect2(38, 112, 347, 358),
	"atelier_mooring_hardware_01": Rect2(400, 140, 360, 350),
	"atelier_fishing_net_bundle_01": Rect2(752, 120, 381, 370),
	"atelier_sacks_fish_baskets_01": Rect2(1125, 120, 405, 370),
	"atelier_anchor_rope_01": Rect2(35, 520, 325, 380),
	"atelier_dock_repair_planks_01": Rect2(370, 560, 430, 340),
	"atelier_dock_lantern_01": Rect2(780, 520, 300, 395),
	"atelier_shoreline_debris_01": Rect2(1070, 560, 464, 360),
}
const NEWPORT_ATELIER_TERRAIN_EDGE_ATLAS_REGIONS := {
	"atelier_terrain_grass_road_edge_north_01": Rect2(85, 61, 750, 209),
	"atelier_terrain_grass_road_edge_south_01": Rect2(916, 72, 710, 198),
	"atelier_terrain_mud_cobble_feather_01": Rect2(80, 297, 761, 181),
	"atelier_terrain_dirt_path_border_01": Rect2(913, 316, 726, 153),
	"atelier_terrain_worn_corner_blend_01": Rect2(214, 502, 465, 190),
	"atelier_terrain_coastal_tuft_stone_cluster_01": Rect2(956, 502, 544, 171),
	"atelier_terrain_muddy_puddle_rut_01": Rect2(138, 704, 610, 178),
	"atelier_terrain_broken_grassy_shoulder_01": Rect2(905, 704, 729, 181),
}
const NEWPORT_ATELIER_COBBLE_PATH_ATLAS_REGIONS := {
	"atelier_path_market_cobble_long_01": Rect2(99, 96, 637, 182),
	"atelier_path_broken_cobble_patch_01": Rect2(845, 105, 583, 173),
	"atelier_path_dirt_worn_section_01": Rect2(113, 349, 606, 162),
	"atelier_path_road_shoulder_earth_01": Rect2(823, 347, 614, 164),
	"atelier_path_curb_threshold_stones_01": Rect2(108, 571, 613, 159),
	"atelier_path_cobble_plank_seam_01": Rect2(823, 577, 618, 148),
	"atelier_path_sunken_gutter_stones_01": Rect2(105, 797, 618, 136),
	"atelier_path_loose_paving_fragments_01": Rect2(810, 818, 621, 111),
}
const NEWPORT_ATELIER_SHORELINE_ATLAS_REGIONS := {
	"atelier_shore_seaweed_drift_line_01": Rect2(68, 88, 648, 184),
	"atelier_shore_shell_pebble_cluster_01": Rect2(795, 100, 642, 175),
	"atelier_shore_wet_rocks_sand_01": Rect2(71, 308, 636, 202),
	"atelier_shore_driftwood_log_cluster_01": Rect2(784, 308, 679, 202),
	"atelier_shore_wet_sand_mud_strip_01": Rect2(69, 560, 622, 158),
	"atelier_shore_harbor_debris_slats_rope_01": Rect2(785, 540, 649, 183),
	"atelier_shore_tide_puddle_mud_edge_01": Rect2(78, 767, 608, 186),
	"atelier_shore_eelgrass_reeds_cluster_01": Rect2(802, 761, 618, 192),
}
const NEWPORT_ATELIER_BUILDING_GROUNDING_ATLAS_REGIONS := {
	"atelier_ground_doorstep_stones_01": Rect2(187, 76, 491, 186),
	"atelier_ground_foundation_shadow_strip_01": Rect2(795, 100, 584, 153),
	"atelier_ground_wall_weeds_stones_01": Rect2(164, 293, 530, 186),
	"atelier_ground_repair_boards_crate_scraps_01": Rect2(824, 262, 498, 234),
	"atelier_ground_barrel_crate_cluster_01": Rect2(170, 498, 464, 214),
	"atelier_ground_wash_tub_buckets_01": Rect2(839, 512, 444, 200),
	"atelier_ground_low_fence_weeds_01": Rect2(142, 741, 549, 198),
	"atelier_ground_firewood_chopping_block_01": Rect2(813, 732, 540, 222),
}
const NEWPORT_ATELIER_SIGN_SHOP_MARKERS_ATLAS_REGIONS := {
	"atelier_sign_tavern_inn_placeholder_01": Rect2(329, 19, 312, 268),
	"atelier_sign_mercantile_crate_marker_01": Rect2(905, 32, 314, 240),
	"atelier_sign_fishmonger_icon_board_01": Rect2(329, 293, 311, 245),
	"atelier_sign_dock_warehouse_barrel_anchor_01": Rect2(909, 290, 301, 226),
	"atelier_sign_inn_rooms_key_board_01": Rect2(352, 546, 243, 192),
	"atelier_sign_harbor_direction_arrows_01": Rect2(929, 542, 267, 228),
	"atelier_sign_hanging_bracket_iron_01": Rect2(302, 737, 374, 261),
	"atelier_sign_painted_shop_plaque_01": Rect2(924, 774, 262, 209),
}
const NEWPORT_ATELIER_LAMPS_WAYFINDING_ATLAS_REGIONS := {
	"atelier_wayfinding_street_lamp_post_01": Rect2(440, 9, 120, 339),
	"atelier_wayfinding_dock_lantern_post_01": Rect2(897, 23, 203, 309),
	"atelier_wayfinding_multi_arrow_signpost_01": Rect2(383, 340, 232, 246),
	"atelier_wayfinding_bollard_lantern_01": Rect2(915, 344, 142, 246),
	"atelier_wayfinding_harbor_road_marker_01": Rect2(402, 579, 177, 196),
	"atelier_wayfinding_rope_rail_post_pair_01": Rect2(841, 587, 285, 196),
	"atelier_wayfinding_pier_lantern_stand_01": Rect2(402, 762, 178, 249),
	"atelier_wayfinding_coastal_waystone_01": Rect2(878, 796, 176, 204),
}
const NEWPORT_ATELIER_CIVIC_MARKET_ATLAS_REGIONS := {
	"atelier_civic_town_notice_board_01": Rect2(300, 8, 323, 267),
	"atelier_civic_market_banner_strand_01": Rect2(810, 58, 447, 178),
	"atelier_civic_harbor_bulletin_board_01": Rect2(265, 283, 382, 238),
	"atelier_civic_flag_cluster_01": Rect2(866, 292, 368, 209),
	"atelier_civic_anchor_plaque_01": Rect2(331, 523, 251, 222),
	"atelier_civic_posting_pole_01": Rect2(959, 510, 127, 254),
	"atelier_civic_market_pennant_sign_01": Rect2(281, 761, 337, 214),
	"atelier_civic_dock_rules_board_01": Rect2(861, 751, 309, 259),
}
const NEWPORT_ATELIER_SHOPFRONT_SUPPORT_ATLAS_REGIONS := {
	"atelier_shopfront_canvas_awning_segment_01": Rect2(276, 73, 370, 172),
	"atelier_shopfront_display_crates_slate_01": Rect2(853, 32, 355, 228),
	"atelier_shopfront_folded_cloth_bundle_01": Rect2(294, 318, 340, 169),
	"atelier_shopfront_chalk_slate_board_01": Rect2(927, 282, 206, 224),
	"atelier_shopfront_hanging_basket_01": Rect2(310, 550, 305, 171),
	"atelier_shopfront_coastal_planter_01": Rect2(894, 525, 269, 207),
	"atelier_shopfront_rope_pennant_rail_01": Rect2(276, 768, 381, 186),
	"atelier_shopfront_basket_parcel_display_01": Rect2(851, 739, 347, 249),
}
const NEWPORT_G418E_TAVERN_INN_ATLAS_REGIONS := {
	"atelier_g418e_tavern_hanging_inn_sign_01": Rect2(258, 10, 293, 270),
	"atelier_g418e_tavern_entry_lantern_pair_01": Rect2(915, 36, 421, 238),
	"atelier_g418e_tavern_threshold_planters_01": Rect2(189, 291, 401, 223),
	"atelier_g418e_tavern_service_barrel_crate_01": Rect2(939, 288, 392, 227),
	"atelier_g418e_tavern_brick_threshold_01": Rect2(133, 570, 505, 143),
	"atelier_g418e_tavern_twin_stack_chimney_detail_01": Rect2(925, 531, 397, 213),
	"atelier_g418e_tavern_stable_tack_rack_01": Rect2(171, 776, 440, 221),
	"atelier_g418e_tavern_firewood_coal_scuttle_01": Rect2(908, 780, 456, 210),
}
const NEWPORT_G418E_COMMERCIAL_AVENUE_ATLAS_REGIONS := {
	"atelier_g418e_commercial_mercantile_sign_01": Rect2(285, 17, 270, 237),
	"atelier_g418e_commercial_fishmonger_sign_01": Rect2(958, 24, 262, 240),
	"atelier_g418e_commercial_market_cart_01": Rect2(271, 275, 365, 253),
	"atelier_g418e_commercial_produce_crates_01": Rect2(917, 291, 337, 236),
	"atelier_g418e_commercial_basket_parcel_display_01": Rect2(284, 544, 302, 161),
	"atelier_g418e_commercial_canvas_awning_roll_01": Rect2(920, 569, 331, 150),
	"atelier_g418e_commercial_street_lamp_01": Rect2(360, 736, 105, 277),
	"atelier_g418e_commercial_directional_signpost_01": Rect2(971, 736, 197, 273),
}
const NEWPORT_G418E_HARBOR_DOCK_EDGE_ATLAS_REGIONS := {
	"atelier_g418e_harbor_dock_barrel_row_01": Rect2(179, 49, 471, 186),
	"atelier_g418e_harbor_rope_coil_large_01": Rect2(910, 30, 424, 199),
	"atelier_g418e_harbor_fishing_crate_net_stack_01": Rect2(197, 266, 402, 235),
	"atelier_g418e_harbor_net_drying_frame_01": Rect2(882, 263, 448, 245),
	"atelier_g418e_harbor_bollard_pair_01": Rect2(198, 523, 394, 216),
	"atelier_g418e_harbor_cargo_stack_01": Rect2(881, 516, 425, 222),
	"atelier_g418e_harbor_service_post_lantern_01": Rect2(244, 756, 226, 259),
	"atelier_g418e_harbor_fish_baskets_tub_01": Rect2(873, 774, 470, 221),
}
const NEWPORT_G418E_REAR_SERVICE_CONNECTOR_ATLAS_REGIONS := {
	"atelier_g418e_service_fence_gate_01": Rect2(188, 50, 477, 215),
	"atelier_g418e_service_utility_barrels_01": Rect2(852, 17, 446, 248),
	"atelier_g418e_service_alley_crates_01": Rect2(230, 285, 393, 223),
	"atelier_g418e_service_firewood_barrow_01": Rect2(891, 289, 381, 219),
	"atelier_g418e_service_stone_edge_01": Rect2(190, 580, 468, 139),
	"atelier_g418e_service_wash_tub_linen_01": Rect2(861, 516, 426, 203),
	"atelier_g418e_service_rain_barrel_01": Rect2(254, 727, 339, 280),
	"atelier_g418e_service_repair_sawhorse_01": Rect2(890, 727, 380, 280),
}
const NEWPORT_ATELIER_CHARACTER_ATLAS_REGIONS := {
	"npc_dockworker_atelier_g422r": Rect2(0, 0, 256, 256),
	"npc_market_vendor_atelier_g422r": Rect2(256, 0, 256, 256),
	"npc_civic_clerk_atelier_g422r": Rect2(512, 0, 256, 256),
}
const NEWPORT_ATELIER_CARGO_PLACEMENTS := [
	{
		"asset_id": "atelier_newport_crate_01",
		"dest": Rect2(494, 608, 108, 91),
		"pivot": Vector2(0.5, 0.94),
		"ground_y": 699.0,
		"scale": 0.20,
		"purpose": "commercial_row_front_cargo",
	},
	{
		"asset_id": "atelier_newport_barrel_01",
		"dest": Rect2(632, 617, 62, 71),
		"pivot": Vector2(0.5, 0.94),
		"ground_y": 688.0,
		"scale": 0.18,
		"purpose": "commercial_row_front_cargo",
	},
	{
		"asset_id": "atelier_wharf_cargo_cluster_01",
		"dest": Rect2(536, 692, 190, 118),
		"pivot": Vector2(0.5, 0.94),
		"ground_y": 810.0,
		"scale": 0.25,
		"purpose": "wharf_depth_cluster",
	},
	{
		"asset_id": "atelier_newport_rope_coil_01",
		"dest": Rect2(780, 706, 96, 59),
		"pivot": Vector2(0.5, 0.90),
		"ground_y": 765.0,
		"scale": 0.18,
		"purpose": "wharf_rope_accent",
	},
]
const NEWPORT_ATELIER_DOCK_CLUTTER_PLACEMENTS := [
	{
		"asset_id": "atelier_sacks_fish_baskets_01",
		"dest": Rect2(708, 618, 77, 70),
		"pivot": Vector2(0.5, 0.93),
		"ground_y": 688.0,
		"scale": 0.19,
		"purpose": "harbor_market_edge_cluster",
	},
	{
		"asset_id": "atelier_fishing_net_bundle_01",
		"dest": Rect2(882, 694, 76, 74),
		"pivot": Vector2(0.5, 0.92),
		"ground_y": 768.0,
		"scale": 0.20,
		"purpose": "wharf_net_cluster_near_rope_lane",
	},
	{
		"asset_id": "atelier_dock_bollards_01",
		"dest": Rect2(948, 642, 66, 68),
		"pivot": Vector2(0.5, 0.94),
		"ground_y": 710.0,
		"scale": 0.19,
		"purpose": "dock_edge_bollards",
	},
	{
		"asset_id": "atelier_mooring_hardware_01",
		"dest": Rect2(1024, 704, 68, 66),
		"pivot": Vector2(0.5, 0.93),
		"ground_y": 770.0,
		"scale": 0.19,
		"purpose": "mooring_service_path_edge",
	},
	{
		"asset_id": "atelier_dock_repair_planks_01",
		"dest": Rect2(338, 696, 86, 68),
		"pivot": Vector2(0.5, 0.93),
		"ground_y": 764.0,
		"scale": 0.20,
		"purpose": "dock_repair_boards_service_edge",
	},
	{
		"asset_id": "atelier_dock_lantern_01",
		"dest": Rect2(1122, 630, 51, 67),
		"pivot": Vector2(0.5, 0.95),
		"ground_y": 697.0,
		"scale": 0.17,
		"purpose": "harbor_edge_lantern_marker",
	},
]
const NEWPORT_G420A_TERRAIN_EDGE_PLACEMENTS := [
	{
		"asset_id": "atelier_terrain_grass_road_edge_north_01",
		"dest": Rect2(190, 542, 246, 42),
		"purpose": "waterfront_avenue_west_grass_curb_edge",
		"alpha": 0.46,
	},
	{
		"asset_id": "atelier_terrain_grass_road_edge_north_01",
		"dest": Rect2(956, 542, 330, 42),
		"purpose": "waterfront_avenue_east_grass_curb_edge",
		"alpha": 0.42,
	},
	{
		"asset_id": "atelier_terrain_mud_cobble_feather_01",
		"dest": Rect2(268, 662, 320, 48),
		"purpose": "wharf_to_waterfront_avenue_mud_cobble_feather",
		"alpha": 0.44,
	},
	{
		"asset_id": "atelier_terrain_broken_grassy_shoulder_01",
		"dest": Rect2(1218, 614, 238, 44),
		"purpose": "east_market_avenue_shoulder_breakup",
		"alpha": 0.38,
	},
]
const NEWPORT_G420A_COBBLE_PATH_PLACEMENTS := [
	{
		"asset_id": "atelier_path_market_cobble_long_01",
		"dest": Rect2(552, 592, 252, 44),
		"purpose": "waterfront_avenue_central_cobble_breakup",
		"alpha": 0.46,
	},
	{
		"asset_id": "atelier_path_broken_cobble_patch_01",
		"dest": Rect2(1228, 596, 190, 42),
		"purpose": "east_market_avenue_broken_cobble",
		"alpha": 0.38,
	},
	{
		"asset_id": "atelier_path_cobble_plank_seam_01",
		"dest": Rect2(628, 672, 286, 40),
		"purpose": "harbor_avenue_to_wharf_cobble_plank_seam",
		"alpha": 0.44,
	},
	{
		"asset_id": "atelier_path_curb_threshold_stones_01",
		"dest": Rect2(600, 548, 118, 28),
		"purpose": "mercantile_avenue_threshold_grounding",
		"alpha": 0.50,
	},
	{
		"asset_id": "atelier_path_curb_threshold_stones_01",
		"dest": Rect2(954, 548, 146, 28),
		"purpose": "chandlery_avenue_threshold_grounding",
		"alpha": 0.44,
	},
]
const NEWPORT_G420A_SHORELINE_PLACEMENTS := [
	{
		"asset_id": "atelier_shore_seaweed_drift_line_01",
		"dest": Rect2(300, 704, 220, 42),
		"purpose": "west_wharf_tide_edge_seaweed",
		"alpha": 0.88,
	},
	{
		"asset_id": "atelier_shore_wet_rocks_sand_01",
		"dest": Rect2(850, 704, 190, 52),
		"purpose": "central_dock_shoreline_rocks",
		"alpha": 0.82,
	},
	{
		"asset_id": "atelier_shore_driftwood_log_cluster_01",
		"dest": Rect2(1132, 714, 190, 56),
		"purpose": "east_shoreline_driftwood",
		"alpha": 0.82,
	},
	{
		"asset_id": "atelier_shore_harbor_debris_slats_rope_01",
		"dest": Rect2(1012, 812, 150, 44),
		"purpose": "east_pier_low_harbor_debris",
		"alpha": 0.78,
	},
]
const NEWPORT_G420A_BUILDING_GROUNDING_PLACEMENTS := [
	{
		"asset_id": "atelier_ground_foundation_shadow_strip_01",
		"dest": Rect2(592, 548, 150, 32),
		"purpose": "mercantile_avenue_foundation_grounding",
		"alpha": 0.38,
	},
	{
		"asset_id": "atelier_ground_foundation_shadow_strip_01",
		"dest": Rect2(940, 548, 220, 32),
		"purpose": "chandlery_shop_avenue_foundation_grounding",
		"alpha": 0.34,
	},
	{
		"asset_id": "atelier_ground_doorstep_stones_01",
		"dest": Rect2(626, 558, 72, 24),
		"purpose": "mercantile_doorstep_read_without_blocking",
		"alpha": 0.46,
	},
	{
		"asset_id": "atelier_ground_wall_weeds_stones_01",
		"dest": Rect2(1296, 548, 128, 30),
		"purpose": "market_printer_base_weeds",
		"alpha": 0.34,
	},
	{
		"asset_id": "atelier_ground_wash_tub_buckets_01",
		"dest": Rect2(1256, 408, 52, 26),
		"purpose": "support_lane_residential_life_accent",
		"alpha": 0.36,
	},
]
const NEWPORT_G420B_SIGN_SHOP_MARKER_PLACEMENTS := [
	{"asset_id": "atelier_sign_mercantile_crate_marker_01", "dest": Rect2(626, 508, 66, 50), "purpose": "mercantile_waterfront_avenue_shop_marker", "alpha": 0.94, "contact_shadow": true},
	{"asset_id": "atelier_sign_fishmonger_icon_board_01", "dest": Rect2(312, 604, 70, 56), "purpose": "west_fishmonger_future_lot_identity_marker", "alpha": 0.92, "contact_shadow": true},
	{"asset_id": "atelier_sign_dock_warehouse_barrel_anchor_01", "dest": Rect2(456, 704, 64, 48), "purpose": "west_dock_warehouse_wayfinding_marker", "alpha": 0.92, "contact_shadow": true},
	{"asset_id": "atelier_sign_harbor_direction_arrows_01", "dest": Rect2(694, 622, 50, 43), "purpose": "central_road_wharf_direction_marker", "alpha": 0.96, "contact_shadow": true},
	{"asset_id": "atelier_sign_hanging_bracket_iron_01", "dest": Rect2(1010, 508, 58, 43), "purpose": "chandlery_shopfront_sign_support_read", "alpha": 0.86},
]
const NEWPORT_G420B_LAMPS_WAYFINDING_PLACEMENTS := [
	{"asset_id": "atelier_wayfinding_street_lamp_post_01", "dest": Rect2(382, 500, 28, 79), "purpose": "west_upland_road_lamp_orientation", "alpha": 0.92, "contact_shadow": true},
	{"asset_id": "atelier_wayfinding_street_lamp_post_01", "dest": Rect2(1142, 500, 28, 79), "purpose": "east_upland_road_lamp_orientation", "alpha": 0.90, "contact_shadow": true},
	{"asset_id": "atelier_wayfinding_dock_lantern_post_01", "dest": Rect2(934, 640, 45, 68), "purpose": "central_wharf_lantern_wayfinding", "alpha": 0.94, "contact_shadow": true},
	{"asset_id": "atelier_wayfinding_multi_arrow_signpost_01", "dest": Rect2(1388, 590, 48, 50), "purpose": "east_market_road_to_harbor_direction_post", "alpha": 0.94, "contact_shadow": true},
	{"asset_id": "atelier_wayfinding_bollard_lantern_01", "dest": Rect2(704, 650, 38, 52), "purpose": "wharf_apron_low_lantern_read", "alpha": 0.95, "contact_shadow": true},
	{"asset_id": "atelier_wayfinding_harbor_road_marker_01", "dest": Rect2(840, 596, 36, 40), "purpose": "waterfront_avenue_road_marker_read", "alpha": 0.90, "contact_shadow": true},
	{"asset_id": "atelier_wayfinding_pier_lantern_stand_01", "dest": Rect2(1170, 707, 40, 54), "purpose": "east_pier_lantern_memory_anchor", "alpha": 0.92, "contact_shadow": true},
]
const NEWPORT_G420B_CIVIC_MARKET_PLACEMENTS := [
	{"asset_id": "atelier_civic_town_notice_board_01", "dest": Rect2(742, 368, 86, 72), "purpose": "town_hall_counting_house_public_notice_landmark", "alpha": 0.92, "contact_shadow": true},
	{"asset_id": "atelier_civic_market_banner_strand_01", "dest": Rect2(1314, 548, 116, 42), "purpose": "east_market_avenue_color_identity", "alpha": 0.84},
	{"asset_id": "atelier_civic_flag_cluster_01", "dest": Rect2(904, 374, 58, 42), "purpose": "custom_house_civic_identity_flags", "alpha": 0.88, "contact_shadow": true},
	{"asset_id": "atelier_civic_posting_pole_01", "dest": Rect2(820, 402, 32, 54), "purpose": "civic_square_to_avenue_posting_marker", "alpha": 0.90, "contact_shadow": true},
	{"asset_id": "atelier_civic_dock_rules_board_01", "dest": Rect2(1230, 688, 74, 62), "purpose": "dock_rules_board_harbor_orientation", "alpha": 0.86, "contact_shadow": true},
]
const NEWPORT_G420B_SHOPFRONT_SUPPORT_PLACEMENTS := [
	{"asset_id": "atelier_shopfront_display_crates_slate_01", "dest": Rect2(1142, 596, 76, 52), "purpose": "shop_house_avenue_display_read", "alpha": 0.94, "contact_shadow": true},
	{"asset_id": "atelier_shopfront_chalk_slate_board_01", "dest": Rect2(1000, 590, 34, 48), "purpose": "chandlery_front_blank_slate_marker", "alpha": 0.92, "contact_shadow": true},
	{"asset_id": "atelier_shopfront_hanging_basket_01", "dest": Rect2(724, 332, 48, 34), "purpose": "town_hall_counting_house_shopfront_warmth_accent", "alpha": 0.86},
	{"asset_id": "atelier_shopfront_rope_pennant_rail_01", "dest": Rect2(1320, 632, 94, 42), "purpose": "market_edge_low_pennant_boundary", "alpha": 0.88, "contact_shadow": true},
]
const NEWPORT_G418E_TAVERN_INN_PLACEMENTS := [
	{"asset_id": "atelier_g418e_tavern_hanging_inn_sign_01", "dest": Rect2(196, 508, 66, 61), "purpose": "tavern_frontage_hero_sign_read", "alpha": 0.98, "contact_shadow": true},
	{"asset_id": "atelier_g418e_tavern_entry_lantern_pair_01", "dest": Rect2(292, 536, 66, 37), "purpose": "tavern_entry_warm_lantern_threshold", "alpha": 0.98, "contact_shadow": true},
	{"asset_id": "atelier_g418e_tavern_threshold_planters_01", "dest": Rect2(160, 574, 72, 40), "purpose": "tavern_social_frontage_planters", "alpha": 0.97, "contact_shadow": true},
	{"asset_id": "atelier_g418e_tavern_service_barrel_crate_01", "dest": Rect2(332, 592, 68, 39), "purpose": "tavern_delivery_edge_service_cluster", "alpha": 0.96, "contact_shadow": true},
	{"asset_id": "atelier_g418e_tavern_brick_threshold_01", "dest": Rect2(184, 558, 126, 36), "purpose": "tavern_entry_brick_threshold_grounding", "alpha": 0.88},
]
const NEWPORT_G418E_COMMERCIAL_AVENUE_PLACEMENTS := [
	{"asset_id": "atelier_g418e_commercial_mercantile_sign_01", "dest": Rect2(616, 506, 60, 53), "purpose": "mercantile_avenue_hero_shop_sign", "alpha": 0.98, "contact_shadow": true},
	{"asset_id": "atelier_g418e_commercial_fishmonger_sign_01", "dest": Rect2(988, 506, 62, 57), "purpose": "fishmonger_chandlery_avenue_harbor_identity", "alpha": 0.98, "contact_shadow": true},
	{"asset_id": "atelier_g418e_commercial_market_cart_01", "dest": Rect2(1304, 596, 92, 64), "purpose": "market_spine_hero_cart_clear_of_route", "alpha": 0.96, "contact_shadow": true},
	{"asset_id": "atelier_g418e_commercial_produce_crates_01", "dest": Rect2(1138, 596, 76, 53), "purpose": "commercial_avenue_produce_frontage", "alpha": 0.95, "contact_shadow": true},
	{"asset_id": "atelier_g418e_commercial_basket_parcel_display_01", "dest": Rect2(1218, 618, 66, 35), "purpose": "commercial_avenue_compact_goods_display", "alpha": 0.95, "contact_shadow": true},
	{"asset_id": "atelier_g418e_commercial_canvas_awning_roll_01", "dest": Rect2(1036, 542, 76, 34), "purpose": "chandlery_shopfront_canvas_color_accent", "alpha": 0.86},
	{"asset_id": "atelier_g418e_commercial_street_lamp_01", "dest": Rect2(516, 506, 30, 79), "purpose": "commercial_spine_lamp_rhythm", "alpha": 0.94, "contact_shadow": true},
	{"asset_id": "atelier_g418e_commercial_directional_signpost_01", "dest": Rect2(1400, 580, 46, 64), "purpose": "market_to_harbor_blank_wayfinding", "alpha": 0.96, "contact_shadow": true},
]
const NEWPORT_G418E_HARBOR_DOCK_EDGE_PLACEMENTS := [
	{"asset_id": "atelier_g418e_harbor_dock_barrel_row_01", "dest": Rect2(304, 700, 88, 35), "purpose": "west_dock_barrel_row_working_edge", "alpha": 0.96, "contact_shadow": true},
	{"asset_id": "atelier_g418e_harbor_rope_coil_large_01", "dest": Rect2(742, 722, 72, 34), "purpose": "central_wharf_large_rope_coil", "alpha": 0.96, "contact_shadow": true},
	{"asset_id": "atelier_g418e_harbor_fishing_crate_net_stack_01", "dest": Rect2(1116, 700, 76, 45), "purpose": "east_dock_fishing_crate_net_stack", "alpha": 0.96, "contact_shadow": true},
	{"asset_id": "atelier_g418e_harbor_net_drying_frame_01", "dest": Rect2(1188, 770, 96, 53), "purpose": "dock_edge_net_drying_service_life", "alpha": 0.95, "contact_shadow": true},
	{"asset_id": "atelier_g418e_harbor_bollard_pair_01", "dest": Rect2(936, 704, 72, 39), "purpose": "central_mooring_bollard_pair", "alpha": 0.96, "contact_shadow": true},
	{"asset_id": "atelier_g418e_harbor_cargo_stack_01", "dest": Rect2(520, 700, 86, 45), "purpose": "wharf_cargo_stack_replacing_weak_cluster_language", "alpha": 0.95, "contact_shadow": true},
	{"asset_id": "atelier_g418e_harbor_service_post_lantern_01", "dest": Rect2(1012, 640, 48, 62), "purpose": "harbor_service_lantern_route_marker", "alpha": 0.96, "contact_shadow": true},
	{"asset_id": "atelier_g418e_harbor_fish_baskets_tub_01", "dest": Rect2(1250, 714, 86, 41), "purpose": "fish_market_dock_transition_goods", "alpha": 0.95, "contact_shadow": true},
]
const NEWPORT_G418E_REAR_SERVICE_CONNECTOR_PLACEMENTS := [
	{"asset_id": "atelier_g418e_service_fence_gate_01", "dest": Rect2(1076, 416, 112, 51), "purpose": "east_rear_service_connector_fence_gate", "alpha": 0.92, "contact_shadow": true},
	{"asset_id": "atelier_g418e_service_utility_barrels_01", "dest": Rect2(1248, 402, 80, 45), "purpose": "east_rear_service_utility_barrels", "alpha": 0.92, "contact_shadow": true},
	{"asset_id": "atelier_g418e_service_alley_crates_01", "dest": Rect2(462, 430, 76, 43), "purpose": "central_alley_storage_without_blocking_route", "alpha": 0.92, "contact_shadow": true},
	{"asset_id": "atelier_g418e_service_firewood_barrow_01", "dest": Rect2(1080, 416, 76, 44), "purpose": "rear_lane_firewood_service_motion", "alpha": 0.92, "contact_shadow": true},
	{"asset_id": "atelier_g418e_service_stone_edge_01", "dest": Rect2(592, 420, 112, 34), "purpose": "service_path_stone_edge_grounding", "alpha": 0.82},
	{"asset_id": "atelier_g418e_service_wash_tub_linen_01", "dest": Rect2(1268, 454, 74, 35), "purpose": "rear_yard_domestic_service_life", "alpha": 0.90, "contact_shadow": true},
	{"asset_id": "atelier_g418e_service_rain_barrel_01", "dest": Rect2(1438, 414, 58, 50), "purpose": "building_back_rain_barrel_grounding", "alpha": 0.90, "contact_shadow": true},
	{"asset_id": "atelier_g418e_service_repair_sawhorse_01", "dest": Rect2(1192, 646, 70, 52), "purpose": "cooperage_wharf_repair_sawhorse", "alpha": 0.90, "contact_shadow": true},
]
const NEWPORT_G7B_HARBOR_WORK_ZONE_PLACEMENTS := [
	{"family": "harbor", "asset_id": "atelier_g418e_harbor_fishing_crate_net_stack_01", "dest": Rect2(334, 690, 84, 49), "purpose": "g7b_west_fish_offload_zone_net_crates", "alpha": 0.98, "contact_shadow": true},
	{"family": "harbor", "asset_id": "atelier_g418e_harbor_fish_baskets_tub_01", "dest": Rect2(432, 706, 88, 42), "purpose": "g7b_west_fish_offload_zone_baskets", "alpha": 0.97, "contact_shadow": true},
	{"family": "harbor", "asset_id": "atelier_g418e_harbor_cargo_stack_01", "dest": Rect2(586, 684, 88, 46), "purpose": "g7b_central_manifest_cargo_waiting_for_counting_house", "alpha": 0.97, "contact_shadow": true},
	{"family": "commercial", "asset_id": "atelier_g418e_commercial_basket_parcel_display_01", "dest": Rect2(626, 622, 76, 40), "purpose": "g7b_manifest_goods_staged_between_mercantile_and_wharf", "alpha": 0.96, "contact_shadow": true},
	{"family": "harbor", "asset_id": "atelier_g418e_harbor_rope_coil_large_01", "dest": Rect2(792, 694, 76, 36), "purpose": "g7b_chandlery_rope_service_zone", "alpha": 0.97, "contact_shadow": true},
	{"family": "harbor", "asset_id": "atelier_g418e_harbor_bollard_pair_01", "dest": Rect2(892, 696, 72, 39), "purpose": "g7b_chandlery_mooring_service_zone", "alpha": 0.97, "contact_shadow": true},
	{"family": "harbor", "asset_id": "atelier_g418e_harbor_service_post_lantern_01", "dest": Rect2(1006, 640, 50, 64), "purpose": "g7b_counting_house_route_lantern_at_wharf_gate", "alpha": 0.98, "contact_shadow": true},
	{"family": "commercial", "asset_id": "atelier_g418e_commercial_produce_crates_01", "dest": Rect2(1194, 606, 82, 57), "purpose": "g7b_market_transfer_goods_linked_to_wharf", "alpha": 0.96, "contact_shadow": true},
	{"family": "commercial", "asset_id": "atelier_g418e_commercial_market_cart_01", "dest": Rect2(1320, 604, 94, 66), "purpose": "g7b_market_cart_clear_of_main_route", "alpha": 0.97, "contact_shadow": true},
	{"family": "harbor", "asset_id": "atelier_g418e_harbor_dock_barrel_row_01", "dest": Rect2(1220, 696, 92, 36), "purpose": "g7b_east_storehouse_barrel_row_work_queue", "alpha": 0.97, "contact_shadow": true},
	{"family": "harbor", "asset_id": "atelier_g418e_harbor_net_drying_frame_01", "dest": Rect2(1262, 764, 102, 56), "purpose": "g7b_east_net_drying_service_life", "alpha": 0.96, "contact_shadow": true},
]
const NEWPORT_G7C_LANDMARK_IDENTITY_PLACEMENTS := [
	{"family": "tavern", "asset_id": "atelier_g418e_tavern_entry_lantern_pair_01", "dest": Rect2(238, 530, 90, 51), "purpose": "g7c_tavern_inn_warm_entry_landmark", "alpha": 0.99, "contact_shadow": true},
	{"family": "tavern", "asset_id": "atelier_g418e_tavern_threshold_planters_01", "dest": Rect2(128, 578, 96, 53), "purpose": "g7c_tavern_inn_social_threshold_centerpiece", "alpha": 0.98, "contact_shadow": true},
	{"family": "tavern", "asset_id": "atelier_g418e_tavern_service_barrel_crate_01", "dest": Rect2(356, 582, 82, 47), "purpose": "g7c_tavern_service_lane_links_to_harbor_labor", "alpha": 0.97, "contact_shadow": true},
	{"family": "civic", "asset_id": "atelier_civic_harbor_bulletin_board_01", "dest": Rect2(800, 392, 86, 54), "purpose": "g7c_counting_house_civic_notice_board_landmark", "alpha": 0.94, "contact_shadow": true},
	{"family": "civic", "asset_id": "atelier_civic_flag_cluster_01", "dest": Rect2(884, 366, 72, 42), "purpose": "g7c_custom_house_civic_flag_landmark", "alpha": 0.90, "contact_shadow": true},
	{"family": "shopfront", "asset_id": "atelier_shopfront_canvas_awning_segment_01", "dest": Rect2(1082, 544, 92, 43), "purpose": "g7c_commercial_shop_row_colored_awning_identity", "alpha": 0.90, "contact_shadow": true},
	{"family": "shopfront", "asset_id": "atelier_shopfront_basket_parcel_display_01", "dest": Rect2(1136, 620, 74, 53), "purpose": "g7c_commercial_row_goods_below_shopfront", "alpha": 0.94, "contact_shadow": true},
	{"family": "lamps", "asset_id": "atelier_wayfinding_street_lamp_post_01", "dest": Rect2(894, 516, 30, 83), "purpose": "g7c_commercial_avenue_lamp_rhythm_landmark", "alpha": 0.94, "contact_shadow": true},
	{"family": "harbor", "asset_id": "atelier_g418e_harbor_service_post_lantern_01", "dest": Rect2(720, 660, 52, 66), "purpose": "g7c_harbor_work_lantern_landmark_at_manifest_route", "alpha": 0.98, "contact_shadow": true},
	{"family": "civic", "asset_id": "atelier_civic_anchor_plaque_01", "dest": Rect2(1136, 674, 46, 41), "purpose": "g7c_harbor_work_area_anchor_plaque_memory_point", "alpha": 0.88, "contact_shadow": true},
	{"family": "service", "asset_id": "atelier_g418e_service_fence_gate_01", "dest": Rect2(1088, 414, 118, 54), "purpose": "g7c_rear_service_lane_gate_identity_east_connector", "alpha": 0.93, "contact_shadow": true},
	{"family": "service", "asset_id": "atelier_g418e_service_wash_tub_linen_01", "dest": Rect2(1218, 454, 78, 37), "purpose": "g7c_rear_service_lane_domestic_work_identity", "alpha": 0.92, "contact_shadow": true},
	{"family": "grounding", "asset_id": "atelier_ground_low_fence_weeds_01", "dest": Rect2(116, 330, 148, 54), "purpose": "g7c_residential_edge_small_yard_landmark", "alpha": 0.42, "contact_shadow": true},
	{"family": "grounding", "asset_id": "atelier_ground_wash_tub_buckets_01", "dest": Rect2(1320, 386, 62, 31), "purpose": "g7c_residential_edge_lived_in_yard_identity", "alpha": 0.40, "contact_shadow": true},
]
const NEWPORT_ATELIER_CHARACTER_PLACEMENTS := [
	{"id": "mara_pike_dockworker", "asset_id": "npc_dockworker_atelier_g422r", "position": Vector2(420, 690), "size": Vector2(82, 82), "role": "dockworker", "district": "working_wharf", "station": "west_fish_offload", "route_intent": "harbor_loop", "movement_policy": G8A_NPC_MOVEMENT_POLICY, "idle_behavior": "checks rope and fish baskets", "dialogue_seed": "Crates do not forget hands. Ledgers do.", "quest_relevance": "missing_manifest_line", "purpose": "g8a_west_dockworker_station_supports_harbor_labor", "contact_shadow": true},
	{"id": "jonah_reed_dock_courier", "asset_id": "npc_dockworker_atelier_g422r", "position": Vector2(1218, 690), "size": Vector2(82, 82), "role": "dockworker_courier", "district": "working_wharf", "station": "east_storehouse_queue", "route_intent": "east_storehouse_to_counting_house", "movement_policy": G8A_NPC_MOVEMENT_POLICY, "idle_behavior": "waits by the storehouse barrels", "dialogue_seed": "A sealed cargo line went quiet before the tide turned.", "quest_relevance": "harbor_work_path", "purpose": "g8a_east_dock_courier_station_supports_storehouse_route", "contact_shadow": true},
	{"id": "honor_finch_merchant_shopkeeper", "asset_id": "npc_market_vendor_atelier_g422r", "position": Vector2(1364, 636), "size": Vector2(82, 82), "role": "merchant_shopkeeper", "district": "harborfront_commercial", "station": "east_market_cart", "route_intent": "market_loop", "movement_policy": G8A_NPC_MOVEMENT_POLICY, "idle_behavior": "counts parcels and watches the avenue", "dialogue_seed": "The missing line cost someone coin, and coin leaves footprints.", "quest_relevance": "merchant_or_street_path", "purpose": "g8a_merchant_shopkeeper_station_supports_commercial_spine", "contact_shadow": true},
	{"id": "bess_armitage_tavern_keeper", "asset_id": "npc_market_vendor_atelier_g422r", "position": Vector2(302, 604), "size": Vector2(80, 80), "role": "tavern_keeper", "district": "harborfront_commercial", "station": "tavern_front_threshold", "route_intent": "tavern_rumor_path", "movement_policy": G8A_NPC_MOVEMENT_POLICY, "idle_behavior": "keeps the door warm and hears the room before it speaks", "dialogue_seed": "Ask for the third toast only if you mean to hear the answer.", "quest_relevance": "tavern_whisper_hook", "purpose": "g8a_tavern_keeper_station_supports_rumor_hub", "contact_shadow": true},
	{"id": "silas_crowe_suspicious_patron", "asset_id": "npc_civic_clerk_atelier_g422r", "position": Vector2(386, 438), "size": Vector2(80, 80), "role": "suspicious_patron", "district": "support_lane", "station": "tavern_rear_service_gate", "route_intent": "secret_path_tavern_to_rear_lane", "movement_policy": G8A_NPC_MOVEMENT_POLICY, "idle_behavior": "lingers near the rear gate with sealed notes", "dialogue_seed": "Some whispers arrive by the back door, not the bar.", "quest_relevance": "optional_secret_path", "purpose": "g8a_suspicious_patron_station_supports_secret_path", "contact_shadow": true},
	{"id": "edrin_vale_counting_house_clerk", "asset_id": "npc_civic_clerk_atelier_g422r", "position": Vector2(792, 570), "size": Vector2(80, 80), "role": "counting_house_clerk", "district": "inland_residential_civic", "station": "counting_house_records_route", "route_intent": "counting_house_clerk_path", "movement_policy": G8A_NPC_MOVEMENT_POLICY, "idle_behavior": "holds the records route and watches the wharf", "dialogue_seed": "The ledger is missing a line, and no honest clerk misplaces ink by accident.", "quest_relevance": "first_light_counting_house", "purpose": "g8a_counting_house_clerk_station_supports_first_objective", "contact_shadow": true},
	{"id": "nora_vale_rumor_carrier", "asset_id": "npc_civic_clerk_atelier_g422r", "position": Vector2(748, 394), "size": Vector2(78, 78), "role": "rumor_carrier", "district": "inland_residential_civic", "station": "civic_notice_board", "route_intent": "notice_board_to_tavern", "movement_policy": G8A_NPC_MOVEMENT_POLICY, "idle_behavior": "reads the notices and folds one into a sleeve", "dialogue_seed": "One notice was posted for officials; one was posted for people who know where to look.", "quest_relevance": "optional_notice_clue", "purpose": "g8a_rumor_carrier_station_supports_civic_to_tavern_whisper", "contact_shadow": true},
]
const G417_HERO_PROP_REPLACEMENT_RECT := Rect2(240, 500, 1040, 280)

var _newport_hero_atlas: Texture2D
var _newport_green_origin_atlas: Texture2D
var _newport_atelier_cargo_atlas: Texture2D
var _newport_atelier_dock_clutter_atlas: Texture2D
var _newport_atelier_terrain_edge_atlas: Texture2D
var _newport_atelier_cobble_path_atlas: Texture2D
var _newport_atelier_shoreline_atlas: Texture2D
var _newport_atelier_building_grounding_atlas: Texture2D
var _newport_atelier_sign_shop_markers_atlas: Texture2D
var _newport_atelier_lamps_wayfinding_atlas: Texture2D
var _newport_atelier_civic_market_atlas: Texture2D
var _newport_atelier_shopfront_support_atlas: Texture2D
var _newport_g418e_tavern_inn_atlas: Texture2D
var _newport_g418e_commercial_avenue_atlas: Texture2D
var _newport_g418e_harbor_dock_edge_atlas: Texture2D
var _newport_g418e_rear_service_connector_atlas: Texture2D
var _newport_atelier_character_atlas: Texture2D
var _g418d1_m01b_proof: Texture2D
var _g418d2_capability_asset: Texture2D
var _green_origin_lab_enabled := false
var _building_texture_cache := {}

func _ready() -> void:
	_newport_hero_atlas = ResourceLoader.load(NEWPORT_HERO_ATLAS_PATH, "Texture2D") as Texture2D
	if _newport_hero_atlas == null:
		push_error("Failed to load Newport hero atlas: " + NEWPORT_HERO_ATLAS_PATH)
	_newport_green_origin_atlas = ResourceLoader.load(NEWPORT_GREEN_ORIGIN_ATLAS_PATH, "Texture2D") as Texture2D
	if _newport_green_origin_atlas == null:
		push_error("Failed to load Newport green-origin atlas: " + NEWPORT_GREEN_ORIGIN_ATLAS_PATH)
	_newport_atelier_cargo_atlas = ResourceLoader.load(NEWPORT_ATELIER_CARGO_ATLAS_PATH, "Texture2D") as Texture2D
	if _newport_atelier_cargo_atlas == null:
		push_error("Failed to load Newport atelier cargo atlas: " + NEWPORT_ATELIER_CARGO_ATLAS_PATH)
	_newport_atelier_dock_clutter_atlas = ResourceLoader.load(NEWPORT_ATELIER_DOCK_CLUTTER_ATLAS_PATH, "Texture2D") as Texture2D
	if _newport_atelier_dock_clutter_atlas == null:
		push_error("Failed to load Newport atelier dock clutter atlas: " + NEWPORT_ATELIER_DOCK_CLUTTER_ATLAS_PATH)
	_newport_atelier_terrain_edge_atlas = ResourceLoader.load(NEWPORT_ATELIER_TERRAIN_EDGE_ATLAS_PATH, "Texture2D") as Texture2D
	if _newport_atelier_terrain_edge_atlas == null:
		push_error("Failed to load Newport atelier terrain edge atlas: " + NEWPORT_ATELIER_TERRAIN_EDGE_ATLAS_PATH)
	_newport_atelier_cobble_path_atlas = ResourceLoader.load(NEWPORT_ATELIER_COBBLE_PATH_ATLAS_PATH, "Texture2D") as Texture2D
	if _newport_atelier_cobble_path_atlas == null:
		push_error("Failed to load Newport atelier cobble path atlas: " + NEWPORT_ATELIER_COBBLE_PATH_ATLAS_PATH)
	_newport_atelier_shoreline_atlas = ResourceLoader.load(NEWPORT_ATELIER_SHORELINE_ATLAS_PATH, "Texture2D") as Texture2D
	if _newport_atelier_shoreline_atlas == null:
		push_error("Failed to load Newport atelier shoreline atlas: " + NEWPORT_ATELIER_SHORELINE_ATLAS_PATH)
	_newport_atelier_building_grounding_atlas = ResourceLoader.load(NEWPORT_ATELIER_BUILDING_GROUNDING_ATLAS_PATH, "Texture2D") as Texture2D
	if _newport_atelier_building_grounding_atlas == null:
		push_error("Failed to load Newport atelier building grounding atlas: " + NEWPORT_ATELIER_BUILDING_GROUNDING_ATLAS_PATH)
	_newport_atelier_sign_shop_markers_atlas = ResourceLoader.load(NEWPORT_ATELIER_SIGN_SHOP_MARKERS_ATLAS_PATH, "Texture2D") as Texture2D
	if _newport_atelier_sign_shop_markers_atlas == null:
		push_error("Failed to load Newport atelier sign/shop marker atlas: " + NEWPORT_ATELIER_SIGN_SHOP_MARKERS_ATLAS_PATH)
	_newport_atelier_lamps_wayfinding_atlas = ResourceLoader.load(NEWPORT_ATELIER_LAMPS_WAYFINDING_ATLAS_PATH, "Texture2D") as Texture2D
	if _newport_atelier_lamps_wayfinding_atlas == null:
		push_error("Failed to load Newport atelier lamps/wayfinding atlas: " + NEWPORT_ATELIER_LAMPS_WAYFINDING_ATLAS_PATH)
	_newport_atelier_civic_market_atlas = ResourceLoader.load(NEWPORT_ATELIER_CIVIC_MARKET_ATLAS_PATH, "Texture2D") as Texture2D
	if _newport_atelier_civic_market_atlas == null:
		push_error("Failed to load Newport atelier civic/market atlas: " + NEWPORT_ATELIER_CIVIC_MARKET_ATLAS_PATH)
	_newport_atelier_shopfront_support_atlas = ResourceLoader.load(NEWPORT_ATELIER_SHOPFRONT_SUPPORT_ATLAS_PATH, "Texture2D") as Texture2D
	if _newport_atelier_shopfront_support_atlas == null:
		push_error("Failed to load Newport atelier shopfront support atlas: " + NEWPORT_ATELIER_SHOPFRONT_SUPPORT_ATLAS_PATH)
	_newport_g418e_tavern_inn_atlas = ResourceLoader.load(NEWPORT_G418E_TAVERN_INN_ATLAS_PATH, "Texture2D") as Texture2D
	if _newport_g418e_tavern_inn_atlas == null:
		push_error("Failed to load Newport G-4.18E tavern/inn atlas: " + NEWPORT_G418E_TAVERN_INN_ATLAS_PATH)
	_newport_g418e_commercial_avenue_atlas = ResourceLoader.load(NEWPORT_G418E_COMMERCIAL_AVENUE_ATLAS_PATH, "Texture2D") as Texture2D
	if _newport_g418e_commercial_avenue_atlas == null:
		push_error("Failed to load Newport G-4.18E commercial avenue atlas: " + NEWPORT_G418E_COMMERCIAL_AVENUE_ATLAS_PATH)
	_newport_g418e_harbor_dock_edge_atlas = ResourceLoader.load(NEWPORT_G418E_HARBOR_DOCK_EDGE_ATLAS_PATH, "Texture2D") as Texture2D
	if _newport_g418e_harbor_dock_edge_atlas == null:
		push_error("Failed to load Newport G-4.18E harbor dock edge atlas: " + NEWPORT_G418E_HARBOR_DOCK_EDGE_ATLAS_PATH)
	_newport_g418e_rear_service_connector_atlas = ResourceLoader.load(NEWPORT_G418E_REAR_SERVICE_CONNECTOR_ATLAS_PATH, "Texture2D") as Texture2D
	if _newport_g418e_rear_service_connector_atlas == null:
		push_error("Failed to load Newport G-4.18E rear service connector atlas: " + NEWPORT_G418E_REAR_SERVICE_CONNECTOR_ATLAS_PATH)
	_newport_atelier_character_atlas = ResourceLoader.load(NEWPORT_ATELIER_CHARACTER_ATLAS_PATH, "Texture2D") as Texture2D
	if _newport_atelier_character_atlas == null:
		push_error("Failed to load Newport G-4.22R atelier character atlas: " + NEWPORT_ATELIER_CHARACTER_ATLAS_PATH)
	_g418d1_m01b_proof = ResourceLoader.load(G418D1_M01B_PROOF_PATH, "Texture2D") as Texture2D
	if _g418d1_m01b_proof == null:
		push_warning("Failed to load G-4.18D.1 M01B lab proof: " + G418D1_M01B_PROOF_PATH)
	_g418d2_capability_asset = ResourceLoader.load(G418D2_CAPABILITY_ASSET_PATH, "Texture2D") as Texture2D
	if _g418d2_capability_asset == null:
		push_warning("Failed to load G-4.18D.2 capability asset: " + G418D2_CAPABILITY_ASSET_PATH)
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

func newport_atelier_cargo_version() -> String:
	return NEWPORT_ATELIER_CARGO_VERSION

func newport_atelier_cargo_materials() -> Array:
	return NEWPORT_ATELIER_CARGO_MATERIALS.duplicate()

func newport_atelier_cargo_placements() -> Array:
	return NEWPORT_ATELIER_CARGO_PLACEMENTS.duplicate(true)

func newport_atelier_dock_clutter_version() -> String:
	return NEWPORT_ATELIER_DOCK_CLUTTER_VERSION

func newport_atelier_dock_clutter_materials() -> Array:
	return NEWPORT_ATELIER_DOCK_CLUTTER_MATERIALS.duplicate()

func newport_atelier_dock_clutter_placements() -> Array:
	return NEWPORT_ATELIER_DOCK_CLUTTER_PLACEMENTS.duplicate(true)

func newport_environmental_believability_version() -> String:
	return NEWPORT_ENVIRONMENTAL_BELIEVABILITY_VERSION

func newport_environmental_believability_materials() -> Array:
	var materials: Array = []
	materials.append_array(NEWPORT_ATELIER_TERRAIN_EDGE_MATERIALS)
	materials.append_array(NEWPORT_ATELIER_COBBLE_PATH_MATERIALS)
	materials.append_array(NEWPORT_ATELIER_SHORELINE_MATERIALS)
	materials.append_array(NEWPORT_ATELIER_BUILDING_GROUNDING_MATERIALS)
	return materials

func newport_environmental_believability_placements() -> Array:
	var placements: Array = []
	placements.append_array(NEWPORT_G420A_TERRAIN_EDGE_PLACEMENTS)
	placements.append_array(NEWPORT_G420A_COBBLE_PATH_PLACEMENTS)
	placements.append_array(NEWPORT_G420A_SHORELINE_PLACEMENTS)
	placements.append_array(NEWPORT_G420A_BUILDING_GROUNDING_PLACEMENTS)
	return placements.duplicate(true)

func newport_town_identity_version() -> String:
	return NEWPORT_TOWN_IDENTITY_VERSION

func newport_town_identity_materials() -> Array:
	var materials: Array = []
	materials.append_array(NEWPORT_ATELIER_SIGN_SHOP_MARKER_MATERIALS)
	materials.append_array(NEWPORT_ATELIER_LAMPS_WAYFINDING_MATERIALS)
	materials.append_array(NEWPORT_ATELIER_CIVIC_MARKET_MATERIALS)
	materials.append_array(NEWPORT_ATELIER_SHOPFRONT_SUPPORT_MATERIALS)
	return materials

func newport_town_identity_placements() -> Array:
	var placements: Array = []
	placements.append_array(NEWPORT_G420B_SIGN_SHOP_MARKER_PLACEMENTS)
	placements.append_array(NEWPORT_G420B_LAMPS_WAYFINDING_PLACEMENTS)
	placements.append_array(NEWPORT_G420B_CIVIC_MARKET_PLACEMENTS)
	placements.append_array(NEWPORT_G420B_SHOPFRONT_SUPPORT_PLACEMENTS)
	return placements.duplicate(true)

func newport_g418e_hero_asset_family_version() -> String:
	return NEWPORT_G418E_HERO_ASSET_FAMILY_VERSION

func newport_g418e_hero_asset_family_materials() -> Array:
	var materials: Array = []
	materials.append_array(NEWPORT_G418E_TAVERN_INN_MATERIALS)
	materials.append_array(NEWPORT_G418E_COMMERCIAL_AVENUE_MATERIALS)
	materials.append_array(NEWPORT_G418E_HARBOR_DOCK_EDGE_MATERIALS)
	materials.append_array(NEWPORT_G418E_REAR_SERVICE_CONNECTOR_MATERIALS)
	return materials

func newport_g418e_hero_asset_family_placements() -> Array:
	var placements: Array = []
	placements.append_array(NEWPORT_G418E_TAVERN_INN_PLACEMENTS)
	placements.append_array(NEWPORT_G418E_COMMERCIAL_AVENUE_PLACEMENTS)
	placements.append_array(NEWPORT_G418E_HARBOR_DOCK_EDGE_PLACEMENTS)
	placements.append_array(NEWPORT_G418E_REAR_SERVICE_CONNECTOR_PLACEMENTS)
	return placements.duplicate(true)

func newport_atelier_character_version() -> String:
	return NEWPORT_ATELIER_CHARACTER_VERSION

func newport_atelier_character_materials() -> Array:
	return NEWPORT_ATELIER_CHARACTER_MATERIALS.duplicate()

func newport_atelier_character_placements() -> Array:
	return NEWPORT_ATELIER_CHARACTER_PLACEMENTS.duplicate(true)

func g422r_hidden_normal_play_marker_assets() -> Array:
	return G422R_HIDDEN_NORMAL_PLAY_MARKER_ASSETS.duplicate()

func _is_g422r_hidden_normal_play_marker(placement: Dictionary) -> bool:
	return G422R_HIDDEN_NORMAL_PLAY_MARKER_ASSETS.has(String(placement.get("asset_id", "")))

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

func _draw_atelier_cargo_piece(region_id: String, dest: Rect2, alpha := 1.0) -> void:
	if _newport_atelier_cargo_atlas == null:
		return
	if not NEWPORT_ATELIER_CARGO_ATLAS_REGIONS.has(region_id):
		push_error("Unknown Newport atelier cargo atlas region: " + region_id)
		return
	draw_texture_rect_region(_newport_atelier_cargo_atlas, dest, NEWPORT_ATELIER_CARGO_ATLAS_REGIONS[region_id], Color(1, 1, 1, alpha), false, true)

func _draw_atelier_cargo_placement(placement: Dictionary) -> void:
	var asset_id := String(placement.get("asset_id", ""))
	var dest: Rect2 = placement.get("dest", Rect2())
	if asset_id == "" or dest.size.x <= 0.0 or dest.size.y <= 0.0:
		return
	var ground_y := float(placement.get("ground_y", dest.end.y))
	_draw_contact_shadow(Vector2(dest.get_center().x, ground_y - 3.0), Vector2(dest.size.x * 0.34, max(5.0, dest.size.y * 0.075)), 0.16)
	_draw_atelier_cargo_piece(asset_id, dest, 1.0)

func _draw_atelier_dock_clutter_piece(region_id: String, dest: Rect2, alpha := 1.0) -> void:
	if _newport_atelier_dock_clutter_atlas == null:
		return
	if not NEWPORT_ATELIER_DOCK_CLUTTER_ATLAS_REGIONS.has(region_id):
		push_error("Unknown Newport atelier dock clutter atlas region: " + region_id)
		return
	draw_texture_rect_region(_newport_atelier_dock_clutter_atlas, dest, NEWPORT_ATELIER_DOCK_CLUTTER_ATLAS_REGIONS[region_id], Color(1, 1, 1, alpha), false, true)

func _draw_atelier_dock_clutter_placement(placement: Dictionary) -> void:
	var asset_id := String(placement.get("asset_id", ""))
	var dest: Rect2 = placement.get("dest", Rect2())
	if asset_id == "" or dest.size.x <= 0.0 or dest.size.y <= 0.0:
		return
	var ground_y := float(placement.get("ground_y", dest.end.y))
	_draw_contact_shadow(Vector2(dest.get_center().x, ground_y - 3.0), Vector2(dest.size.x * 0.34, max(5.0, dest.size.y * 0.075)), 0.15)
	_draw_atelier_dock_clutter_piece(asset_id, dest, 1.0)

func _draw_environmental_atelier_piece(atlas: Texture2D, regions: Dictionary, region_id: String, dest: Rect2, alpha := 1.0) -> void:
	if atlas == null:
		return
	if not regions.has(region_id):
		push_error("Unknown Newport environmental atelier region: " + region_id)
		return
	draw_texture_rect_region(atlas, dest, regions[region_id], Color(1, 1, 1, alpha), false, true)

func _draw_environmental_atelier_placement(atlas: Texture2D, regions: Dictionary, placement: Dictionary) -> void:
	var asset_id := String(placement.get("asset_id", ""))
	var dest: Rect2 = placement.get("dest", Rect2())
	if asset_id == "" or dest.size.x <= 0.0 or dest.size.y <= 0.0:
		return
	var alpha := float(placement.get("alpha", 1.0))
	if bool(placement.get("contact_shadow", false)):
		_draw_contact_shadow(Vector2(dest.get_center().x, dest.end.y - 2.0), Vector2(dest.size.x * 0.28, max(4.0, dest.size.y * 0.07)), 0.12)
	_draw_environmental_atelier_piece(atlas, regions, asset_id, dest, alpha)

func _draw_town_identity_atelier_piece(atlas: Texture2D, regions: Dictionary, region_id: String, dest: Rect2, alpha := 1.0) -> void:
	if atlas == null:
		return
	if not regions.has(region_id):
		push_error("Unknown Newport town identity atelier region: " + region_id)
		return
	draw_texture_rect_region(atlas, dest, regions[region_id], Color(1, 1, 1, alpha), false, true)

func _draw_town_identity_atelier_placement(atlas: Texture2D, regions: Dictionary, placement: Dictionary) -> void:
	var asset_id := String(placement.get("asset_id", ""))
	var dest: Rect2 = placement.get("dest", Rect2())
	if asset_id == "" or dest.size.x <= 0.0 or dest.size.y <= 0.0:
		return
	var alpha := float(placement.get("alpha", 1.0))
	if bool(placement.get("contact_shadow", false)):
		_draw_contact_shadow(Vector2(dest.get_center().x, dest.end.y - 2.0), Vector2(dest.size.x * 0.30, max(4.0, dest.size.y * 0.075)), 0.13)
	_draw_town_identity_atelier_piece(atlas, regions, asset_id, dest, alpha)

func _draw_g418e_hero_family_piece(atlas: Texture2D, regions: Dictionary, region_id: String, dest: Rect2, alpha := 1.0) -> void:
	if atlas == null:
		return
	if not regions.has(region_id):
		push_error("Unknown Newport G-4.18E hero family atelier region: " + region_id)
		return
	draw_texture_rect_region(atlas, dest, regions[region_id], Color(1, 1, 1, alpha), false, true)

func _draw_g418e_hero_family_placement(atlas: Texture2D, regions: Dictionary, placement: Dictionary) -> void:
	var asset_id := String(placement.get("asset_id", ""))
	var dest: Rect2 = placement.get("dest", Rect2())
	if asset_id == "" or dest.size.x <= 0.0 or dest.size.y <= 0.0:
		return
	var alpha := float(placement.get("alpha", 1.0))
	if bool(placement.get("contact_shadow", false)):
		_draw_contact_shadow(Vector2(dest.get_center().x, dest.end.y - 2.0), Vector2(dest.size.x * 0.31, max(4.0, dest.size.y * 0.078)), 0.14)
	_draw_g418e_hero_family_piece(atlas, regions, asset_id, dest, alpha)

func _draw_atelier_character_placement(placement: Dictionary) -> void:
	if _newport_atelier_character_atlas == null:
		return
	var asset_id := String(placement.get("asset_id", ""))
	if not NEWPORT_ATELIER_CHARACTER_ATLAS_REGIONS.has(asset_id):
		push_error("Unknown Newport G-4.22R atelier character region: " + asset_id)
		return
	var ground_pos: Vector2 = placement.get("position", Vector2.ZERO)
	var size: Vector2 = placement.get("size", Vector2(82, 82))
	if size.x <= 0.0 or size.y <= 0.0:
		return
	var dest := Rect2(ground_pos - Vector2(size.x * 0.5, size.y * 0.953), size)
	if bool(placement.get("contact_shadow", false)):
		_draw_contact_shadow(ground_pos + Vector2(0.0, 2.0), Vector2(size.x * 0.21, max(4.0, size.y * 0.045)), 0.14)
	draw_texture_rect_region(_newport_atelier_character_atlas, dest, NEWPORT_ATELIER_CHARACTER_ATLAS_REGIONS[asset_id], Color.WHITE, false, true)

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
	if not G422R_SUPPRESS_PRIMITIVE_WORLD_PROPS:
		for pos in [Vector2(620, 360), Vector2(805, 360), Vector2(486, 584), Vector2(1142, 584), Vector2(312, 698), Vector2(1118, 698), Vector2(610, 640), Vector2(856, 640)]:
			draw_circle(pos, 4, Color("#2f251b"))
			draw_circle(pos + Vector2(0, -6), 3, Color("#d8b56f"))

func _draw_g410_ground() -> void:
	_draw_newport_grass_rect(Rect2(Vector2.ZERO, NEWPORT_TOWN.WORLD_SIZE), Color("#4b6a42"), Color("#314d35"), 1.0, 64)
	_draw_newport_grass_swale(PackedVector2Array([
		Vector2(120, 206), Vector2(360, 178), Vector2(722, 188), Vector2(1078, 174),
		Vector2(1482, 202), Vector2(1464, 630), Vector2(1110, 620), Vector2(760, 648),
		Vector2(394, 618), Vector2(116, 650)
	]), Color("#5d7653", 0.12), Color("#425f43", 0.06), 54)
	_draw_newport_grass_swale(PackedVector2Array([
		Vector2(168, 636), Vector2(522, 628), Vector2(880, 646), Vector2(1410, 632),
		Vector2(1394, 744), Vector2(916, 754), Vector2(540, 736), Vector2(156, 758)
	]), Color("#5b6350", 0.10), Color("#454f3d", 0.06), 28)
	_draw_g7a_cohesive_ground_foundation()
	_draw_g423a_expanded_town_ground()
	_draw_g15a_transition_ground()
	_draw_g15b_island_world_ground()
	_draw_g410_background_depth()
	_draw_g422a_town_edge_boundaries()
	if NEWPORT_TOWN.G422A_SHOW_BLOCKOUT_GUIDES:
		_draw_g410_lot_plan()
	_draw_g415_parcel_grounding()
	# G-7A replaces the earlier translucent lot-wash stack with one subdued foundation layer.
	_draw_g7a_lot_foundation_overlays()
	_draw_shrub_cluster(Vector2(348, 322))
	_draw_shrub_cluster(Vector2(644, 332))
	_draw_shrub_cluster(Vector2(1084, 308))
	_draw_shrub_cluster(Vector2(1290, 358))
	_draw_low_wall(Vector2(588, 414), Vector2(790, 408), Color("#68715b", 0.34))
	_draw_low_wall(Vector2(870, 414), Vector2(1084, 408), Color("#68715b", 0.34))
	_draw_low_wall(Vector2(1220, 430), Vector2(1468, 424), Color("#68715b", 0.30))

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
	var pad_type := String(pad.get("type", ""))
	if not NEWPORT_TOWN.G422A_SHOW_LEGACY_PROOF_OVERLAYS and pad_type != "dock_plank":
		return

	match pad_type:
		"commercial_stone", "rowhouse_stone", "shop_stone":
			_draw_newport_frontage_threshold(rect, "commercial", 0.40)
		"market_stone":
			_draw_newport_frontage_threshold(rect, "market", 0.44)
		"civic_stone":
			_draw_newport_frontage_threshold(rect, "civic", 0.42)
		"civic_green":
			_draw_newport_grass_swale(_soft_rect_polygon(rect), Color("#6d865f", 0.12), Color("#4e6b4b", 0.07), 8)
			_draw_newport_grass_transition(Rect2(rect.position.x, rect.end.y - 10.0, rect.size.x, 10.0), "south", 0.10)
			_draw_shrub_cluster(rect.position + Vector2(20.0, rect.size.y - 20.0), 0.55)
			_draw_shrub_cluster(rect.position + Vector2(rect.size.x - 22.0, rect.size.y - 20.0), 0.55)
		"residential_yard":
			_draw_newport_grass_swale(_soft_rect_polygon(rect), Color("#6c875e", 0.11), Color("#4f6e4c", 0.07), 8)
			_draw_newport_grass_transition(Rect2(rect.position.x, rect.end.y - 10.0, rect.size.x, 10.0), "south", 0.09)
			_draw_shrub_cluster(rect.position + Vector2(18.0, rect.size.y - 18.0), 0.50)
			_draw_shrub_cluster(rect.position + Vector2(rect.size.x - 22.0, rect.size.y - 20.0), 0.50)
		"support_yard":
			_draw_newport_frontage_threshold(rect, "support", 0.34)
		"dock_plank":
			_draw_newport_dock_planks(rect, 20)
		_:
			_draw_newport_frontage_threshold(rect, "default", 0.26)

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
	if G422R_HIDE_NORMAL_PLAY_LAYOUT_GUIDES:
		return
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
	_draw_g423a_expanded_town_streets()
	_draw_g15a_transition_streets()
	_draw_g15b_island_world_routes()
	_draw_g7a_continuous_street_base()
	_draw_street_wear(Rect2(178, 580, 1328, 58), 58)
	_draw_street_wear(Rect2(250, 398, 1198, 42), 38)
	_draw_street_wear(Rect2(320, 276, 902, 34), 22)
	_draw_g7a_route_curbs_and_material_transitions()
	for p in [Vector2(386, 578), Vector2(820, 574), Vector2(1260, 576), Vector2(1458, 582), Vector2(704, 398), Vector2(1260, 430)]:
		_draw_edge_grime(p, 92.0)
	_draw_g420a_terrain_and_path_transitions()
	_draw_g423a_lot_threshold_overlays()
	_draw_g422a_block_boundaries()
	_draw_g415_lane_connections()

	_draw_newport_dock_planks(Rect2(238, 704, 1112, 34), 52)
	draw_line(Vector2(248, 704), Vector2(1338, 704), Color(0.04, 0.04, 0.03, 0.28), 2.0)
	for p in [Vector2(284, 704), Vector2(424, 704), Vector2(692, 704), Vector2(824, 704), Vector2(1010, 704), Vector2(1180, 704), Vector2(1318, 704)]:
		_draw_post(p)
	if NEWPORT_TOWN.G422A_SHOW_LEGACY_PROOF_OVERLAYS:
		_draw_g417_hero_street_atlas_proof()
	if not G422R_SUPPRESS_PRIMITIVE_WORLD_PROPS:
		for p in [Vector2(332, 596), Vector2(704, 592), Vector2(1010, 596), Vector2(1150, 594), Vector2(662, 408), Vector2(1094, 416), Vector2(390, 508), Vector2(1400, 590)]:
			draw_circle(p, 4, Color("#2f251b"))
			draw_circle(p + Vector2(0, -6), 3, Color("#d8b56f"))

func _draw_g7a_cohesive_ground_foundation() -> void:
	# G-7A-SV0: one authored town terrace sits under the lots and streets so
	# individual surfaces stop reading as loose editor slabs in wide screenshots.
	draw_rect(Rect2(70, 170, 1468, 574), Color("#4f6849", 0.055), true)
	draw_rect(Rect2(96, 314, 1410, 146), Color("#53664a", 0.050), true)
	draw_rect(Rect2(92, 500, 1438, 170), Color("#555f4a", 0.065), true)
	draw_rect(Rect2(206, 650, 1242, 94), Color("#5c5748", 0.055), true)
	_draw_newport_grass_swale(PackedVector2Array([
		Vector2(52, 302), Vector2(254, 286), Vector2(550, 300), Vector2(820, 288),
		Vector2(1120, 298), Vector2(1506, 306), Vector2(1538, 462), Vector2(1350, 486),
		Vector2(1078, 474), Vector2(830, 488), Vector2(550, 474), Vector2(274, 486),
		Vector2(74, 462)
	]), Color("#5e7653", 0.10), Color("#3f5f3e", 0.05), 50)
	_draw_newport_grass_swale(PackedVector2Array([
		Vector2(96, 482), Vector2(410, 462), Vector2(706, 474), Vector2(1014, 462),
		Vector2(1328, 476), Vector2(1532, 506), Vector2(1514, 662), Vector2(1268, 672),
		Vector2(960, 666), Vector2(664, 676), Vector2(350, 664), Vector2(110, 652)
	]), Color("#596a4f", 0.11), Color("#3f5640", 0.050), 52)
	_draw_newport_grass_swale(PackedVector2Array([
		Vector2(88, 650), Vector2(320, 642), Vector2(620, 654), Vector2(920, 644),
		Vector2(1224, 650), Vector2(1500, 660), Vector2(1510, 734), Vector2(1208, 746),
		Vector2(930, 740), Vector2(642, 750), Vector2(340, 738), Vector2(94, 728)
	]), Color("#5a604d", 0.12), Color("#3e493a", 0.050), 36)

	for raw_band in [
		{"rect": Rect2(132, 516, 1394, 22), "kind": "frontage", "alpha": 0.13},
		{"rect": Rect2(220, 456, 1258, 16), "kind": "support", "alpha": 0.10},
		{"rect": Rect2(294, 340, 970, 18), "kind": "civic", "alpha": 0.11},
		{"rect": Rect2(198, 652, 1252, 18), "kind": "support", "alpha": 0.13},
	]:
		var band: Dictionary = raw_band
		_draw_newport_frontage_threshold(band["rect"], String(band["kind"]), float(band["alpha"]))

	for raw_swale in [
		Rect2(120, 632, 234, 18),
		Rect2(458, 636, 284, 18),
		Rect2(846, 632, 300, 18),
		Rect2(1238, 638, 248, 18),
		Rect2(254, 440, 296, 16),
		Rect2(702, 438, 290, 16),
		Rect2(1148, 442, 292, 16),
	]:
		var swale: Rect2 = raw_swale
		_draw_newport_grass_transition(swale, "south", 0.12)

func _draw_g7a_lot_foundation_overlays() -> void:
	for raw_spec in [
		{"id": "g7a_tavern_lot_foundation", "rect": Rect2(120, 506, 292, 126), "kind": "tavern", "front": "south", "anchor": Vector2(244, 596)},
		{"id": "g7a_clerk_mercantile_lot_foundation", "rect": Rect2(420, 506, 332, 128), "kind": "commercial", "front": "south", "anchor": Vector2(650, 596)},
		{"id": "g7a_chandlery_shop_lot_foundation", "rect": Rect2(918, 504, 386, 130), "kind": "commercial", "front": "south", "anchor": Vector2(1018, 596)},
		{"id": "g7a_market_lot_foundation", "rect": Rect2(1274, 520, 236, 124), "kind": "market", "front": "south", "anchor": Vector2(1364, 636)},
		{"id": "g7a_counting_house_civic_lot_foundation", "rect": Rect2(574, 300, 280, 128), "kind": "civic", "front": "south", "anchor": Vector2(704, 392)},
		{"id": "g7a_custom_house_civic_lot_foundation", "rect": Rect2(846, 300, 292, 128), "kind": "civic", "front": "south", "anchor": Vector2(1010, 394)},
		{"id": "g7a_west_residential_lot_foundation", "rect": Rect2(204, 178, 230, 126), "kind": "residential", "front": "south", "anchor": Vector2(300, 275)},
		{"id": "g7a_east_residential_lot_foundation", "rect": Rect2(870, 176, 250, 124), "kind": "residential", "front": "south", "anchor": Vector2(980, 275)},
		{"id": "g7a_cooperage_service_lot_foundation", "rect": Rect2(1084, 626, 210, 96), "kind": "support", "front": "north", "anchor": Vector2(1165, 705)},
		{"id": "g7a_backstreet_service_lot_foundation", "rect": Rect2(1086, 350, 330, 126), "kind": "support", "front": "south", "anchor": Vector2(1240, 430)},
		{"id": "g7a_west_wharf_lot_foundation", "rect": Rect2(268, 682, 278, 62), "kind": "wharf", "front": "north", "anchor": Vector2(486, 736)},
		{"id": "g7a_central_wharf_lot_foundation", "rect": Rect2(668, 682, 262, 62), "kind": "wharf", "front": "north", "anchor": Vector2(824, 710)},
		{"id": "g7a_east_wharf_lot_foundation", "rect": Rect2(1104, 684, 276, 62), "kind": "wharf", "front": "north", "anchor": Vector2(1218, 708)},
	]:
		var spec: Dictionary = raw_spec
		_draw_g7a_named_lot_foundation(spec)

	for raw_path in [
		[Vector2(244, 596), Vector2(244, 570), 11.0],
		[Vector2(650, 596), Vector2(650, 570), 11.0],
		[Vector2(1018, 596), Vector2(1018, 570), 11.0],
		[Vector2(1364, 636), Vector2(1364, 612), 10.0],
		[Vector2(704, 392), Vector2(704, 424), 12.0],
		[Vector2(1010, 394), Vector2(1010, 424), 11.0],
		[Vector2(300, 275), Vector2(330, 334), 8.0],
		[Vector2(980, 275), Vector2(1010, 334), 8.0],
		[Vector2(1165, 705), Vector2(1165, 675), 9.0],
		[Vector2(1240, 430), Vector2(1240, 458), 9.0],
		[Vector2(486, 736), Vector2(486, 700), 10.0],
		[Vector2(824, 710), Vector2(824, 700), 10.0],
		[Vector2(1218, 708), Vector2(1218, 700), 10.0],
	]:
		var path: Array = raw_path
		_draw_g7a_soft_service_trace(path[0], path[1], path[2], 0.36)

func _draw_g7a_named_lot_foundation(spec: Dictionary) -> void:
	var rect: Rect2 = spec["rect"]
	var kind := String(spec.get("kind", "commercial"))
	var fill := Color("#5f7352", 0.075)
	var stroke := Color("#b8a46f", 0.035)
	if kind == "tavern":
		fill = Color("#596b4d", 0.090)
		stroke = Color("#d0b776", 0.045)
	elif kind == "commercial":
		fill = Color("#5d6750", 0.080)
		stroke = Color("#c6b275", 0.040)
	elif kind == "market":
		fill = Color("#6a604b", 0.090)
		stroke = Color("#d0b776", 0.045)
	elif kind == "civic":
		fill = Color("#666a5a", 0.085)
		stroke = Color("#d1c083", 0.040)
	elif kind == "residential":
		fill = Color("#647b57", 0.070)
		stroke = Color("#a8b677", 0.034)
	elif kind == "support":
		fill = Color("#5f674e", 0.075)
		stroke = Color("#c4ad78", 0.034)
	elif kind == "wharf":
		fill = Color("#665b48", 0.105)
		stroke = Color("#c6a66d", 0.045)

	_draw_g7a_soft_lot_patch(_soft_rect_polygon(rect), fill, stroke, kind)
	var frontage_height := 16.0 if kind != "wharf" else 12.0
	var frontage_rect := Rect2(rect.position.x + 10.0, rect.end.y - frontage_height - 2.0, maxf(28.0, rect.size.x - 20.0), frontage_height)
	if String(spec.get("front", "south")) == "north":
		frontage_rect = Rect2(rect.position.x + 10.0, rect.position.y + 3.0, maxf(28.0, rect.size.x - 20.0), frontage_height)
	var threshold_kind := "support" if kind == "wharf" else kind
	if kind == "residential":
		_draw_newport_grass_transition(frontage_rect, "south", 0.18)
	else:
		_draw_newport_frontage_threshold(frontage_rect, threshold_kind, 0.24)

	var anchor: Vector2 = spec.get("anchor", rect.get_center())
	_draw_surface_speckles(Rect2(anchor - Vector2(30.0, 10.0), Vector2(60.0, 20.0)), 8, Color(0.08, 0.06, 0.035, 0.10), Vector2(16, 3))

func _draw_g7a_soft_lot_patch(points: PackedVector2Array, fill: Color, stroke: Color, kind: String) -> void:
	if points.size() < 3:
		return
	draw_colored_polygon(points, fill)
	var bounds := _bounds_for_points(points)
	_draw_surface_speckles(bounds.grow(-8.0), maxi(6, int(bounds.size.x / 48.0)), stroke, Vector2(30, 3))
	if kind == "residential":
		for pos in [bounds.position + Vector2(26.0, bounds.size.y - 20.0), bounds.position + Vector2(bounds.size.x - 28.0, bounds.size.y - 18.0)]:
			_draw_shrub_cluster(pos, 0.42)

func _draw_g7a_soft_service_trace(a: Vector2, b: Vector2, width: float, alpha := 0.40) -> void:
	draw_line(a, b, Color("#463b2d", 0.12 * alpha), width + 8.0, true)
	draw_line(a, b, Color("#8b7858", 0.32 * alpha), width, true)
	draw_line(a, b, Color("#c9ad72", 0.12 * alpha), maxf(1.0, width - 5.0), true)
	var length := a.distance_to(b)
	var steps := maxi(1, int(length / 44.0))
	var dir := (b - a).normalized()
	var normal := Vector2(-dir.y, dir.x)
	for i in range(steps):
		var t := float(i) / float(maxi(1, steps - 1))
		var p := a.lerp(b, t)
		var side := (fmod(float(i * 37), 100.0) / 100.0 - 0.5) * width * 0.62
		draw_line(p + normal * side - dir * 6.0, p + normal * side + dir * 7.0, Color(0.10, 0.075, 0.045, 0.08 * alpha), 1.0)

func _draw_g7a_continuous_street_base() -> void:
	for raw_street in [
		{"rect": Rect2(118, 548, 1410, 98), "detail": 170, "alpha": 0.96},
		{"rect": Rect2(218, 378, 1260, 76), "detail": 116, "alpha": 0.90},
		{"rect": Rect2(176, 456, 1312, 54), "detail": 84, "alpha": 0.70},
		{"rect": Rect2(206, 648, 1242, 78), "detail": 108, "alpha": 0.82},
	]:
		var street: Dictionary = raw_street
		_draw_newport_commercial_street(street["rect"], int(street["detail"]), float(street["alpha"]))

	_draw_g7a_authored_visual_order_streets()

func _draw_g7a_authored_visual_order_streets() -> void:
	for raw_spec in NEWPORT_TOWN.starter_village_route_order_specs():
		var spec: Dictionary = raw_spec
		var width := float(spec.get("width", 32.0))
		var segments: Array = spec.get("segments", [])
		for raw_segment in segments:
			var segment: Rect2 = raw_segment
			if segment.size.x <= 0.0 or segment.size.y <= 0.0:
				continue
			var center := Vector2(segment.get_center().x, segment.get_center().y)
			var path_width := maxf(7.0, width * 0.58)
			_draw_g7a_soft_service_trace(Vector2(center.x, segment.position.y + 4.0), Vector2(center.x, segment.end.y - 4.0), path_width, 0.24)

func _draw_g7a_route_curbs_and_material_transitions() -> void:
	for raw_curb in [
		{"rect": Rect2(130, 548, 1390, 10), "kind": "curb", "alpha": 0.38},
		{"rect": Rect2(126, 638, 1400, 10), "kind": "curb_shadow", "alpha": 0.34},
		{"rect": Rect2(218, 378, 1252, 9), "kind": "curb", "alpha": 0.32},
		{"rect": Rect2(218, 448, 1248, 8), "kind": "curb_shadow", "alpha": 0.28},
		{"rect": Rect2(176, 454, 1310, 8), "kind": "street_patch", "alpha": 0.18},
		{"rect": Rect2(206, 724, 1232, 8), "kind": "curb_shadow", "alpha": 0.34},
	]:
		var curb: Dictionary = raw_curb
		_draw_newport_sidewalk_panel(curb["rect"], String(curb["kind"]), float(curb["alpha"]))

	for raw_transition in [
		{"rect": Rect2(124, 538, 1400, 14), "edge": "north", "alpha": 0.14},
		{"rect": Rect2(126, 648, 1394, 16), "edge": "south", "alpha": 0.14},
		{"rect": Rect2(216, 368, 1250, 14), "edge": "north", "alpha": 0.11},
		{"rect": Rect2(216, 456, 1250, 14), "edge": "south", "alpha": 0.11},
		{"rect": Rect2(206, 636, 1240, 14), "edge": "north", "alpha": 0.12},
		{"rect": Rect2(206, 732, 1240, 14), "edge": "south", "alpha": 0.12},
	]:
		var transition: Dictionary = raw_transition
		_draw_newport_grass_transition(transition["rect"], String(transition["edge"]), float(transition["alpha"]))

	for raw_lane in [
		[Vector2(386, 372), Vector2(386, 548), 13.0],
		[Vector2(820, 430), Vector2(820, 548), 14.0],
		[Vector2(820, 430), Vector2(704, 398), 9.0],
		[Vector2(1260, 426), Vector2(1260, 548), 11.0],
		[Vector2(1458, 500), Vector2(1458, 626), 9.0],
		[Vector2(588, 458), Vector2(588, 568), 8.0],
		[Vector2(926, 458), Vector2(926, 568), 9.0],
		[Vector2(1024, 604), Vector2(1024, 704), 10.0],
	]:
		var lane: Array = raw_lane
		_draw_g7a_soft_service_trace(lane[0], lane[1], lane[2], 0.18)

	for raw_rut in [
		[Vector2(154, 604), Vector2(1500, 596), 0.11],
		[Vector2(240, 422), Vector2(1444, 414), 0.09],
		[Vector2(230, 686), Vector2(1428, 684), 0.08],
		[Vector2(386, 324), Vector2(392, 630), 0.08],
		[Vector2(820, 430), Vector2(820, 686), 0.08],
		[Vector2(1260, 430), Vector2(1260, 688), 0.07],
		[Vector2(1458, 500), Vector2(1458, 688), 0.06],
	]:
		var rut: Array = raw_rut
		draw_line(rut[0], rut[1], Color(0.07, 0.055, 0.035, float(rut[2])), 2.0, true)

	_draw_newport_dock_planks(Rect2(248, 694, 1104, 28), 64)
	draw_line(Vector2(252, 694), Vector2(1344, 694), Color(0.03, 0.035, 0.025, 0.34), 2.0)
	draw_line(Vector2(252, 722), Vector2(1344, 722), Color("#d2b06e", 0.12), 1.0)

func _draw_g7b_functional_wharf_work_zones() -> void:
	for raw_zone in [
		{"rect": Rect2(300, 686, 242, 52), "kind": "fish_offload", "label": "west fish offload"},
		{"rect": Rect2(558, 676, 170, 54), "kind": "manifest_cargo", "label": "manifest cargo"},
		{"rect": Rect2(754, 684, 228, 52), "kind": "rope_chandlery", "label": "rope and mooring"},
		{"rect": Rect2(1114, 686, 236, 54), "kind": "storehouse_queue", "label": "storehouse queue"},
	]:
		var zone: Dictionary = raw_zone
		_draw_g7b_work_zone_surface(zone["rect"], String(zone["kind"]))

	for raw_route in [
		[Vector2(392, 710), Vector2(512, 650), 0.24],
		[Vector2(622, 702), Vector2(704, 600), 0.28],
		[Vector2(842, 704), Vector2(1018, 596), 0.22],
		[Vector2(1218, 704), Vector2(1364, 636), 0.26],
	]:
		var route: Array = raw_route
		_draw_g7b_trade_route_trace(route[0], route[1], float(route[2]))

	draw_line(Vector2(316, 690), Vector2(1330, 690), Color("#d0b06e", 0.16), 1.2, true)
	draw_line(Vector2(316, 738), Vector2(1330, 738), Color(0.03, 0.025, 0.018, 0.28), 1.6, true)

func _draw_g7b_work_zone_surface(rect: Rect2, kind: String) -> void:
	var base := Color("#6a5741", 0.32)
	var edge := Color("#c6a66d", 0.13)
	if kind == "fish_offload":
		base = Color("#665d48", 0.31)
		edge = Color("#c9b98c", 0.12)
	elif kind == "manifest_cargo":
		base = Color("#615844", 0.34)
		edge = Color("#d0b776", 0.14)
	elif kind == "rope_chandlery":
		base = Color("#625542", 0.30)
		edge = Color("#c0a36a", 0.12)
	elif kind == "storehouse_queue":
		base = Color("#695640", 0.32)
		edge = Color("#c8a66c", 0.13)
	_draw_newport_lot_variation(rect, Color(base.r, base.g, base.b), Color("#4d4031"), base.a, "working_wharf")
	draw_line(rect.position + Vector2(8.0, 4.0), Vector2(rect.end.x - 8.0, rect.position.y + 3.0), edge, 1.0)
	draw_line(Vector2(rect.position.x + 8.0, rect.end.y - 4.0), rect.end - Vector2(8.0, 5.0), Color(0.02, 0.025, 0.018, 0.22), 1.2)

func _draw_g7b_trade_route_trace(a: Vector2, b: Vector2, alpha: float) -> void:
	draw_line(a, b, Color("#3b3328", alpha * 0.42), 12.0, true)
	draw_line(a, b, Color("#c4a66c", alpha), 2.0, true)
	var length := a.distance_to(b)
	var steps := maxi(2, int(length / 38.0))
	var dir := (b - a).normalized()
	for i in range(steps):
		if i % 2 != 0:
			continue
		var p := a.lerp(b, float(i) / float(maxi(1, steps - 1)))
		draw_line(p - dir * 7.0, p + dir * 9.0, Color("#f0d08c", alpha * 0.28), 1.0, true)

func _draw_g7b_harbor_commercial_spine_dressing() -> void:
	for placement in NEWPORT_G7B_HARBOR_WORK_ZONE_PLACEMENTS:
		_draw_g7b_spine_placement(placement)

	for raw_marker in [
		{"pos": Vector2(622, 668), "size": Vector2(112, 10), "alpha": 0.18},
		{"pos": Vector2(1004, 668), "size": Vector2(92, 10), "alpha": 0.14},
		{"pos": Vector2(1210, 664), "size": Vector2(156, 10), "alpha": 0.16},
	]:
		var marker: Dictionary = raw_marker
		var rect := Rect2(marker["pos"], marker["size"])
		_draw_surface_speckles(rect, 8, Color("#d0b06e", float(marker["alpha"])), Vector2(18, 2))

func _draw_g7b_spine_placement(placement: Dictionary) -> void:
	var family := String(placement.get("family", "harbor"))
	if family == "commercial":
		_draw_g418e_hero_family_placement(_newport_g418e_commercial_avenue_atlas, NEWPORT_G418E_COMMERCIAL_AVENUE_ATLAS_REGIONS, placement)
	else:
		_draw_g418e_hero_family_placement(_newport_g418e_harbor_dock_edge_atlas, NEWPORT_G418E_HARBOR_DOCK_EDGE_ATLAS_REGIONS, placement)

func _draw_g7c_landmark_district_identity_pass() -> void:
	for placement in NEWPORT_G7C_LANDMARK_IDENTITY_PLACEMENTS:
		_draw_g7c_landmark_placement(placement)

func _draw_g7c_landmark_placement(placement: Dictionary) -> void:
	var family := String(placement.get("family", "civic"))
	match family:
		"tavern":
			_draw_g418e_hero_family_placement(_newport_g418e_tavern_inn_atlas, NEWPORT_G418E_TAVERN_INN_ATLAS_REGIONS, placement)
		"commercial":
			_draw_g418e_hero_family_placement(_newport_g418e_commercial_avenue_atlas, NEWPORT_G418E_COMMERCIAL_AVENUE_ATLAS_REGIONS, placement)
		"harbor":
			_draw_g418e_hero_family_placement(_newport_g418e_harbor_dock_edge_atlas, NEWPORT_G418E_HARBOR_DOCK_EDGE_ATLAS_REGIONS, placement)
		"service":
			_draw_g418e_hero_family_placement(_newport_g418e_rear_service_connector_atlas, NEWPORT_G418E_REAR_SERVICE_CONNECTOR_ATLAS_REGIONS, placement)
		"lamps":
			_draw_town_identity_atelier_placement(_newport_atelier_lamps_wayfinding_atlas, NEWPORT_ATELIER_LAMPS_WAYFINDING_ATLAS_REGIONS, placement)
		"shopfront":
			_draw_town_identity_atelier_placement(_newport_atelier_shopfront_support_atlas, NEWPORT_ATELIER_SHOPFRONT_SUPPORT_ATLAS_REGIONS, placement)
		"grounding":
			_draw_environmental_atelier_placement(_newport_atelier_building_grounding_atlas, NEWPORT_ATELIER_BUILDING_GROUNDING_ATLAS_REGIONS, placement)
		_:
			_draw_town_identity_atelier_placement(_newport_atelier_civic_market_atlas, NEWPORT_ATELIER_CIVIC_MARKET_ATLAS_REGIONS, placement)

func _draw_g422a_block_boundaries() -> void:
	for fence in [
		[Vector2(304, 356), Vector2(444, 354)],
		[Vector2(586, 418), Vector2(790, 412)],
		[Vector2(870, 418), Vector2(1086, 412)],
		[Vector2(1040, 342), Vector2(1186, 340)],
		[Vector2(1226, 434), Vector2(1368, 428)],
		[Vector2(1412, 434), Vector2(1540, 428)],
	]:
		_draw_fence_line(fence[0], fence[1], Color("#d7c894", 0.34))
	for wall in [
		[Vector2(512, 456), Vector2(512, 554)],
		[Vector2(918, 456), Vector2(918, 558)],
		[Vector2(1210, 450), Vector2(1210, 552)],
		[Vector2(1450, 452), Vector2(1450, 616)],
	]:
		_draw_low_wall(wall[0], wall[1], Color("#6f7d62", 0.20))
	for path in [
		[Vector2(552, 448), Vector2(552, 568), 8.0],
		[Vector2(834, 448), Vector2(834, 568), 8.0],
		[Vector2(1100, 342), Vector2(1100, 412), 8.0],
		[Vector2(1302, 424), Vector2(1302, 500), 8.0],
	]:
		_draw_g7a_soft_service_trace(path[0], path[1], path[2], 0.38)
	for gate in [Vector2(552, 448), Vector2(834, 448), Vector2(1100, 412), Vector2(1302, 500)]:
		_draw_door_step(gate)

func _draw_g417_hero_street_atlas_proof() -> void:
	if _newport_hero_atlas == null:
		return
	_draw_hero_atlas_piece("grass_edge_north", Rect2(186, 512, 300, 36), 0.22)
	_draw_hero_atlas_piece("grass_edge_north", Rect2(742, 506, 330, 38), 0.18)
	_draw_hero_atlas_piece("grass_edge_north", Rect2(1190, 512, 250, 34), 0.16)
	_draw_hero_atlas_piece("grass_cobble_feather", Rect2(184, 532, 318, 38), 0.22)
	_draw_hero_atlas_piece("grass_cobble_feather", Rect2(738, 528, 320, 36), 0.18)
	_draw_hero_atlas_piece("grass_cobble_feather", Rect2(1188, 532, 276, 34), 0.16)
	_draw_hero_atlas_tiled("building_contact_shadow_strip", Rect2(170, 536, 1340, 30), 0.34, 1.0)
	_draw_hero_atlas_piece("curb_sidewalk_stoop_strip", Rect2(194, 552, 288, 42), 0.28)
	_draw_hero_atlas_piece("curb_sidewalk_stoop_strip", Rect2(594, 548, 260, 44), 0.26)
	_draw_hero_atlas_piece("curb_sidewalk_stoop_strip", Rect2(936, 552, 300, 42), 0.24)
	_draw_hero_atlas_piece("curb_sidewalk_stoop_strip", Rect2(1288, 552, 220, 40), 0.20)
	_draw_hero_atlas_piece("curb_sidewalk_broken_edge", Rect2(288, 604, 246, 28), 0.24)
	_draw_hero_atlas_piece("curb_sidewalk_broken_edge", Rect2(704, 604, 284, 28), 0.22)
	_draw_hero_atlas_piece("curb_sidewalk_broken_edge", Rect2(1118, 604, 260, 28), 0.20)
	_draw_hero_atlas_piece("commercial_cobble_long_a", Rect2(246, 610, 290, 46), 0.26)
	_draw_hero_atlas_piece("commercial_cobble_patch_b", Rect2(536, 626, 214, 52), 0.24)
	_draw_hero_atlas_piece("commercial_cobble_patch_c", Rect2(704, 602, 178, 48), 0.22)
	_draw_hero_atlas_piece("commercial_cobble_long_a", Rect2(942, 614, 286, 46), 0.22)
	_draw_hero_atlas_piece("commercial_cobble_patch_b", Rect2(1208, 626, 218, 48), 0.20)
	_draw_hero_atlas_piece("dirt_wear_transition", Rect2(278, 656, 296, 34), 0.22)
	_draw_hero_atlas_piece("dirt_wear_transition", Rect2(650, 660, 316, 32), 0.20)
	_draw_hero_atlas_piece("dirt_wear_transition", Rect2(1060, 656, 260, 30), 0.18)
	_draw_hero_atlas_piece("grass_cobble_feather", Rect2(304, 680, 260, 28), 0.14)
	_draw_hero_atlas_piece("grass_cobble_feather", Rect2(760, 680, 310, 28), 0.12)

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
	if _g418d2_capability_asset != null:
		draw_texture_rect(_g418d2_capability_asset, Rect2(1036, 592, 160, 110), false, Color(1, 1, 1, 0.98))
		_draw_label("D2 DEFER - lab-only capability proof", Vector2(1038, 704), 11, Color("#f0cf7d"))
	_draw_lab_badge(Vector2(1008, 724))

func _draw_lab_badge(pos: Vector2) -> void:
	var rect := Rect2(pos, Vector2(316, 54))
	draw_rect(rect, Color(0.055, 0.075, 0.06, 0.82), true)
	draw_rect(rect, Color("#d8c06a", 0.72), false, 1.4)
	_draw_label("Green-Origin Lab: ON", pos + Vector2(12, 20), 13, Color("#f1df91"))
	_draw_label("Not normal review art", pos + Vector2(12, 40), 11, Color("#f0b1a3"))

func _draw_g410_wharf_water() -> void:
	_draw_newport_water_rect(Rect2(0, 742, NEWPORT_TOWN.WORLD_SIZE.x, maxf(282.0, NEWPORT_TOWN.WORLD_SIZE.y - 742.0)), 1.0)
	_draw_water_depth_bands()
	_draw_g15b_island_shoreline_water()
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
	_draw_g423b_harbor_working_surface()
	_draw_g7b_functional_wharf_work_zones()
	for p in [Vector2(266, 714), Vector2(358, 724), Vector2(526, 708), Vector2(716, 718), Vector2(934, 712), Vector2(1140, 716), Vector2(1322, 724)]:
		_draw_shore_rocks(p)
	for p in [Vector2(422, 846), Vector2(802, 846), Vector2(1252, 846)]:
		_draw_waterline_scum(p, 150.0)
	for i in range(46):
		var x := 28.0 + float((i * 67) % 1510)
		var y := 776.0 + float((i * 41) % 220)
		draw_line(Vector2(x, y), Vector2(x + 18.0 + float(i % 4) * 5.0, y - 1.0), Color(0.75, 0.95, 1.0, 0.10), 1.4)
	if NEWPORT_TOWN.G422A_SHOW_LEGACY_PROOF_OVERLAYS:
		_draw_g417_hero_wharf_atlas_proof()
	_draw_g420a_shoreline_edges()
	_draw_g418c_green_origin_lab_proof()

func _draw_g410_props() -> void:
	# G-4.23A keeps dressing subordinate to the town grammar: props mark jobs and thresholds, not empty space.
	_draw_g423a_expanded_town_fabric()
	_draw_g15a_transition_props()
	_draw_g15b_island_world_props()
	_draw_g16_island_poi_landmarks()
	_draw_g16a_island_atelier_asset_family()
	for pos in [Vector2(238, 612), Vector2(1028, 594), Vector2(1346, 624)]:
		_draw_barrels(pos, 2)
	for pos in [Vector2(454, 688), Vector2(1030, 688)]:
		_draw_crate_stack(pos)
	for pos in [Vector2(278, 474), Vector2(304, 474)]:
		_draw_hoop_stack(pos)
	for pos in [Vector2(1318, 622), Vector2(1382, 622)]:
		_draw_market_table(pos)
	for pos in [Vector2(326, 724), Vector2(1136, 716)]:
		_draw_fish_rack(pos)
	for pos in [Vector2(704, 724), Vector2(876, 724)]:
		_draw_net_bundle(pos)
	_draw_rowboat(Vector2(410, 884))
	_draw_rowboat(Vector2(792, 900))
	_draw_rowboat(Vector2(1120, 888))
	for pos in [Vector2(300, 520), Vector2(626, 520), Vector2(820, 388), Vector2(1008, 520), Vector2(1392, 520)]:
		_draw_lantern(pos)
	_draw_net_drying_line(Vector2(220, 442), Vector2(320, 426))
	for fence_config in [
		{"a": Vector2(308, 360), "b": Vector2(420, 360), "color": Color("#d9c89c")},
		{"a": Vector2(586, 412), "b": Vector2(760, 408), "color": Color("#d9c89c")},
		{"a": Vector2(880, 414), "b": Vector2(1040, 410), "color": Color("#d9c89c")},
	]:
		var fence_a: Vector2 = fence_config["a"]
		var fence_b: Vector2 = fence_config["b"]
		_draw_fence_line(fence_a, fence_b, fence_config["color"])
	for pos in [Vector2(396, 462), Vector2(278, 420)]:
		_draw_woodpile(pos)
	for pos in [Vector2(134, 438), Vector2(1452, 430), Vector2(1320, 332), Vector2(584, 356), Vector2(1018, 356)]:
		draw_circle(pos, 13, Color("#2f5d35"))
		draw_circle(pos + Vector2(-8, -8), 8, Color("#3d7042"))
	for bench in [Vector2(632, 408), Vector2(1048, 424), Vector2(832, 410), Vector2(342, 606)]:
		_draw_bench(bench)
	_draw_g423b_frontage_life_props()
	_draw_g423b_harbor_economy_props()
	for anchor in NEWPORT_TOWN.interaction_anchors():
		var anchor_pos: Vector2 = anchor.get("position", Vector2.ZERO)
		var anchor_type := String(anchor.get("type", ""))
		if anchor_type == "npc_atelier" and not G8A_RUNTIME_NPC_NODES_ENABLED:
			var asset_id := "npc_market_vendor_atelier_g422r" if String(anchor.get("id", "")) == "market_vendor" else "npc_dockworker_atelier_g422r"
			_draw_atelier_character_placement({"asset_id": asset_id, "position": anchor_pos, "size": Vector2(82, 82), "contact_shadow": true})
	for placement in NEWPORT_ATELIER_CHARACTER_PLACEMENTS:
		if not G8A_RUNTIME_NPC_NODES_ENABLED and String(placement.get("purpose", "")).find("_replaces_placeholder") < 0:
			_draw_atelier_character_placement(placement)
	if NEWPORT_TOWN.G422A_SHOW_LEGACY_PROOF_OVERLAYS:
		_draw_g418_hero_non_cargo_prop_clusters()
	_draw_g420a_building_grounding_accents()
	_draw_g420b_town_identity_accents()
	_draw_g418e_hero_asset_family_accents()
	_draw_g7b_harbor_commercial_spine_dressing()
	_draw_g7c_landmark_district_identity_pass()
	if NEWPORT_TOWN.G422A_SHOW_LEGACY_PROOF_OVERLAYS:
		_draw_g418d_atelier_cargo_clusters()
		_draw_g419a_atelier_dock_clutter_clusters()

func _draw_g423a_city_ground_washes() -> void:
	_draw_newport_grass_swale(PackedVector2Array([
		Vector2(252, 320), Vector2(470, 304), Vector2(602, 330), Vector2(586, 394),
		Vector2(388, 388), Vector2(250, 410)
	]), Color("#66815a", 0.08), Color("#456440", 0.045), 22)
	_draw_newport_grass_swale(PackedVector2Array([
		Vector2(856, 314), Vector2(1224, 302), Vector2(1378, 344), Vector2(1346, 410),
		Vector2(1080, 392), Vector2(888, 416)
	]), Color("#667f58", 0.08), Color("#496844", 0.045), 22)
	_draw_newport_grass_swale(PackedVector2Array([
		Vector2(170, 504), Vector2(430, 488), Vector2(660, 514), Vector2(656, 578),
		Vector2(422, 568), Vector2(170, 584)
	]), Color("#5e7352", 0.075), Color("#455e40", 0.04), 20)
	_draw_newport_grass_swale(PackedVector2Array([
		Vector2(930, 506), Vector2(1212, 492), Vector2(1488, 520), Vector2(1484, 580),
		Vector2(1220, 568), Vector2(930, 586)
	]), Color("#5e7352", 0.075), Color("#455e40", 0.04), 20)
	_draw_newport_frontage_threshold(Rect2(182, 560, 326, 20), "commercial", 0.10)
	_draw_newport_frontage_threshold(Rect2(566, 560, 172, 20), "commercial", 0.09)
	_draw_newport_frontage_threshold(Rect2(940, 560, 360, 20), "commercial", 0.09)
	_draw_newport_frontage_threshold(Rect2(1288, 560, 204, 20), "market", 0.10)
	_draw_newport_frontage_threshold(Rect2(604, 382, 500, 20), "civic", 0.08)
	_draw_newport_grass_transition(Rect2(258, 440, 1184, 12), "south", 0.06)
	_draw_newport_grass_transition(Rect2(176, 648, 1330, 12), "south", 0.06)

func _draw_g423a_enclosed_lot_cells() -> void:
	for raw_spec in [
		{"rect": Rect2(88, 320, 172, 74), "kind": "residential", "front": "south"},
		{"rect": Rect2(420, 322, 178, 70), "kind": "residential", "front": "south"},
		{"rect": Rect2(744, 316, 138, 72), "kind": "civic", "front": "south"},
		{"rect": Rect2(1130, 322, 150, 74), "kind": "civic", "front": "south"},
		{"rect": Rect2(1320, 326, 126, 76), "kind": "residential", "front": "south"},
		{"rect": Rect2(188, 452, 148, 104), "kind": "service", "front": "south"},
		{"rect": Rect2(430, 456, 166, 104), "kind": "residential", "front": "south"},
		{"rect": Rect2(604, 452, 118, 110), "kind": "civic", "front": "south"},
		{"rect": Rect2(724, 452, 206, 110), "kind": "civic", "front": "south"},
		{"rect": Rect2(1218, 454, 154, 108), "kind": "market", "front": "south"},
		{"rect": Rect2(1382, 458, 108, 102), "kind": "market", "front": "south"},
		{"rect": Rect2(196, 648, 278, 46), "kind": "service", "front": "north"},
		{"rect": Rect2(548, 648, 318, 46), "kind": "service", "front": "north"},
		{"rect": Rect2(944, 648, 340, 46), "kind": "service", "front": "north"},
	]:
		var spec: Dictionary = raw_spec
		var rect: Rect2 = spec["rect"]
		var kind := String(spec.get("kind", "residential"))
		var base := Color("#607a56")
		var alt := Color("#4c6849")
		var alpha := 0.26
		if kind == "civic":
			base = Color("#686a5a")
			alt = Color("#535848")
			alpha = 0.30
		elif kind == "market":
			base = Color("#6b6651")
			alt = Color("#554c3e")
			alpha = 0.30
		elif kind == "service":
			base = Color("#665f4c")
			alt = Color("#514837")
			alpha = 0.28
		_draw_newport_lot_variation(rect, base, alt, alpha, kind)
		var threshold_kind := "support" if kind == "service" else kind
		if kind == "residential":
			_draw_newport_grass_transition(Rect2(rect.position.x + 10.0, rect.end.y - 14.0, maxf(20.0, rect.size.x - 20.0), 10.0), "south", 0.18)
		else:
			_draw_newport_frontage_threshold(Rect2(rect.position.x + 8.0, rect.end.y - 18.0, maxf(20.0, rect.size.x - 16.0), 14.0), threshold_kind, 0.24)
		_draw_low_wall(rect.position + Vector2(4.0, 3.0), Vector2(rect.end.x - 6.0, rect.position.y + 1.0), Color("#5f6f58", 0.18))
		_draw_low_wall(rect.position + Vector2(4.0, rect.end.y - 1.0), rect.end - Vector2(6.0, 3.0), Color("#5f6f58", 0.14))
	for bed in [
		Rect2(108, 344, 62, 24),
		Rect2(476, 336, 72, 24),
		Rect2(1244, 482, 70, 24),
		Rect2(1406, 486, 54, 22),
	]:
		_draw_planting_bed(bed, Color("#6a845c"), Color("#506f4c"))

func _draw_g423b_authored_lot_grounding() -> void:
	for raw_spec in [
		{"points": PackedVector2Array([Vector2(118, 526), Vector2(370, 514), Vector2(414, 552), Vector2(392, 624), Vector2(172, 632), Vector2(120, 596)]), "kind": "tavern", "fill": Color("#566a49", 0.08), "stroke": Color("#b39c68", 0.06)},
		{"points": PackedVector2Array([Vector2(420, 522), Vector2(724, 510), Vector2(748, 554), Vector2(722, 626), Vector2(450, 626), Vector2(410, 582)]), "kind": "commercial", "fill": Color("#5c684e", 0.065), "stroke": Color("#bca96f", 0.055)},
		{"points": PackedVector2Array([Vector2(930, 520), Vector2(1296, 508), Vector2(1326, 552), Vector2(1288, 632), Vector2(950, 626), Vector2(918, 578)]), "kind": "commercial", "fill": Color("#5b674e", 0.065), "stroke": Color("#bca96f", 0.055)},
		{"points": PackedVector2Array([Vector2(1286, 522), Vector2(1516, 534), Vector2(1510, 626), Vector2(1338, 640), Vector2(1274, 606)]), "kind": "market", "fill": Color("#665d49", 0.08), "stroke": Color("#d0b776", 0.06)},
		{"points": PackedVector2Array([Vector2(578, 300), Vector2(1114, 292), Vector2(1152, 342), Vector2(1106, 422), Vector2(596, 422), Vector2(560, 356)]), "kind": "civic", "fill": Color("#64705a", 0.07), "stroke": Color("#c8b880", 0.05)},
		{"points": PackedVector2Array([Vector2(266, 304), Vector2(452, 296), Vector2(468, 360), Vector2(418, 408), Vector2(278, 396), Vector2(238, 346)]), "kind": "residential", "fill": Color("#647e59", 0.06), "stroke": Color("#9caf72", 0.05)},
		{"points": PackedVector2Array([Vector2(1012, 282), Vector2(1238, 288), Vector2(1248, 366), Vector2(1182, 402), Vector2(1014, 382), Vector2(982, 330)]), "kind": "residential", "fill": Color("#667e5a", 0.06), "stroke": Color("#9caf72", 0.05)},
		{"points": PackedVector2Array([Vector2(1384, 336), Vector2(1560, 346), Vector2(1552, 438), Vector2(1460, 458), Vector2(1370, 420)]), "kind": "support", "fill": Color("#5f6c4f", 0.06), "stroke": Color("#c4ad78", 0.045)},
		{"points": PackedVector2Array([Vector2(188, 408), Vector2(338, 400), Vector2(358, 472), Vector2(308, 536), Vector2(184, 520), Vector2(154, 456)]), "kind": "support", "fill": Color("#5f6a4e", 0.065), "stroke": Color("#c4ad78", 0.045)},
	]:
		var spec: Dictionary = raw_spec
		_draw_g423b_soft_ground_patch(spec["points"], spec["fill"], spec["stroke"], String(spec.get("kind", "")))

	for threshold in [
		{"rect": Rect2(146, 548, 218, 26), "kind": "market", "alpha": 0.32},
		{"rect": Rect2(426, 560, 286, 20), "kind": "commercial", "alpha": 0.24},
		{"rect": Rect2(944, 560, 342, 20), "kind": "commercial", "alpha": 0.24},
		{"rect": Rect2(1296, 588, 184, 28), "kind": "market", "alpha": 0.28},
		{"rect": Rect2(628, 384, 480, 22), "kind": "civic", "alpha": 0.26},
		{"rect": Rect2(272, 358, 154, 18), "kind": "support", "alpha": 0.22},
		{"rect": Rect2(1028, 340, 166, 18), "kind": "support", "alpha": 0.22},
	]:
		_draw_newport_frontage_threshold(threshold["rect"], String(threshold["kind"]), float(threshold["alpha"]))

	for raw_path in [
		[Vector2(244, 586), Vector2(244, 626), 13.0],
		[Vector2(650, 586), Vector2(650, 628), 12.0],
		[Vector2(1018, 586), Vector2(1018, 626), 12.0],
		[Vector2(704, 392), Vector2(704, 446), 15.0],
		[Vector2(362, 376), Vector2(386, 448), 10.0],
		[Vector2(1094, 362), Vector2(1154, 438), 10.0],
	]:
		var path: Array = raw_path
		_draw_g7a_soft_service_trace(path[0], path[1], path[2], 0.48)

	for fence in [
		[Vector2(126, 526), Vector2(206, 516)],
		[Vector2(330, 520), Vector2(396, 552)],
		[Vector2(266, 396), Vector2(420, 392)],
		[Vector2(1014, 382), Vector2(1182, 394)],
		[Vector2(1376, 420), Vector2(1518, 432)],
	]:
		_draw_fence_line(fence[0], fence[1], Color("#d7c894", 0.30))

func _draw_g423b_soft_ground_patch(points: PackedVector2Array, fill: Color, stroke: Color, kind: String) -> void:
	if points.size() < 3:
		return
	draw_colored_polygon(points, fill)
	var bounds := _bounds_for_points(points)
	_draw_surface_speckles(bounds.grow(-6.0), maxi(8, int(bounds.size.x / 36.0)), stroke, Vector2(26, 3))
	if kind == "market" or kind == "support":
		_draw_surface_speckles(bounds.grow(-10.0), 8, Color(0.08, 0.055, 0.035, fill.a * 0.50), Vector2(34, 4))
	elif kind == "residential":
		for pos in [bounds.position + Vector2(24.0, bounds.size.y - 20.0), bounds.position + Vector2(bounds.size.x - 24.0, bounds.size.y - 18.0)]:
			_draw_shrub_cluster(pos, 0.50)
	_draw_g423b_polyline(points, Color(stroke.r, stroke.g, stroke.b, minf(0.28, stroke.a * 1.5)), 1.0)

func _draw_g423b_authored_street_breakup() -> void:
	for raw_patch in [
		{"points": PackedVector2Array([Vector2(184, 586), Vector2(462, 580), Vector2(498, 616), Vector2(454, 638), Vector2(188, 628)]), "count": 22, "alpha": 0.28},
		{"points": PackedVector2Array([Vector2(548, 584), Vector2(840, 576), Vector2(884, 612), Vector2(826, 638), Vector2(560, 632)]), "count": 24, "alpha": 0.30},
		{"points": PackedVector2Array([Vector2(986, 584), Vector2(1280, 576), Vector2(1322, 616), Vector2(1270, 638), Vector2(996, 632)]), "count": 24, "alpha": 0.28},
		{"points": PackedVector2Array([Vector2(1288, 592), Vector2(1500, 596), Vector2(1492, 636), Vector2(1340, 644), Vector2(1280, 622)]), "count": 18, "alpha": 0.28},
		{"points": PackedVector2Array([Vector2(600, 398), Vector2(1108, 394), Vector2(1138, 424), Vector2(1086, 448), Vector2(620, 440)]), "count": 30, "alpha": 0.24},
		{"points": PackedVector2Array([Vector2(326, 278), Vector2(1220, 276), Vector2(1204, 304), Vector2(342, 312)]), "count": 28, "alpha": 0.18},
	]:
		var patch: Dictionary = raw_patch
		_draw_g423b_cobble_patch(patch["points"], int(patch["count"]), float(patch["alpha"]))

	for raw_feather in [
		{"points": PackedVector2Array([Vector2(168, 636), Vector2(506, 638), Vector2(470, 670), Vector2(188, 682)]), "alpha": 0.18},
		{"points": PackedVector2Array([Vector2(884, 638), Vector2(1300, 638), Vector2(1266, 672), Vector2(930, 680)]), "alpha": 0.18},
		{"points": PackedVector2Array([Vector2(250, 446), Vector2(478, 444), Vector2(456, 472), Vector2(254, 480)]), "alpha": 0.14},
		{"points": PackedVector2Array([Vector2(1102, 446), Vector2(1450, 444), Vector2(1424, 476), Vector2(1128, 472)]), "alpha": 0.14},
		{"points": PackedVector2Array([Vector2(220, 704), Vector2(530, 704), Vector2(500, 734), Vector2(244, 736)]), "alpha": 0.18},
		{"points": PackedVector2Array([Vector2(918, 704), Vector2(1350, 704), Vector2(1336, 734), Vector2(944, 738)]), "alpha": 0.18},
	]:
		var feather: Dictionary = raw_feather
		_draw_g423b_dirt_feather(feather["points"], float(feather["alpha"]))

	for raw_lane in [
		[Vector2(480, 452), Vector2(470, 584), 13.0],
		[Vector2(936, 452), Vector2(926, 584), 13.0],
		[Vector2(1240, 452), Vector2(1380, 586), 14.0],
		[Vector2(334, 638), Vector2(318, 704), 12.0],
		[Vector2(1116, 638), Vector2(1138, 704), 12.0],
	]:
		var lane: Array = raw_lane
		_draw_g7a_soft_service_trace(lane[0], lane[1], lane[2], 0.44)

	for raw_rut in [
		[Vector2(210, 612), Vector2(1480, 604), 0.10],
		[Vector2(270, 424), Vector2(1424, 416), 0.08],
		[Vector2(386, 326), Vector2(402, 568), 0.08],
		[Vector2(704, 312), Vector2(704, 680), 0.09],
		[Vector2(1156, 336), Vector2(1150, 682), 0.08],
	]:
		var rut: Array = raw_rut
		draw_line(rut[0], rut[1], Color(0.07, 0.055, 0.035, float(rut[2])), 2.0, true)

func _draw_g423b_cobble_patch(points: PackedVector2Array, detail_count: int, alpha: float) -> void:
	if points.size() < 3:
		return
	draw_colored_polygon(points, Color("#736b58", alpha))
	var bounds := _bounds_for_points(points)
	for i in range(detail_count):
		var w := 8.0 + float((i * 5) % 16)
		var h := 4.0 + float((i * 7) % 8)
		var x := bounds.position.x + fmod(float(i * 43 + 13), maxf(1.0, bounds.size.x - w))
		var y := bounds.position.y + fmod(float(i * 29 + 19), maxf(1.0, bounds.size.y - h))
		if not Geometry2D.is_point_in_polygon(Vector2(x + w * 0.5, y + h * 0.5), points):
			continue
		var n := fmod(float(i * 17), 100.0) / 100.0
		var stone := Color("#5e5a4c").lerp(Color("#b5a67a"), n * 0.45)
		draw_rect(Rect2(Vector2(x, y), Vector2(w, h)), Color(stone.r, stone.g, stone.b, alpha * 0.72), true)
	_draw_g423b_polyline(points, Color("#d4bd80", alpha * 0.35), 1.0)

func _draw_g423b_dirt_feather(points: PackedVector2Array, alpha: float) -> void:
	if points.size() < 3:
		return
	draw_colored_polygon(points, Color("#7a6848", alpha))
	var bounds := _bounds_for_points(points)
	_draw_surface_speckles(bounds.grow(-6.0), 14, Color(0.09, 0.065, 0.035, alpha * 0.70), Vector2(36, 4))
	_draw_g423b_polyline(points, Color("#263f2a", alpha * 0.45), 1.0)

func _draw_g423b_harbor_working_surface() -> void:
	for rect in [
		Rect2(300, 696, 132, 36),
		Rect2(454, 690, 86, 44),
		Rect2(760, 690, 132, 42),
		Rect2(1136, 694, 126, 40),
		Rect2(1266, 700, 86, 34),
		Rect2(312, 838, 126, 32),
		Rect2(748, 842, 144, 30),
		Rect2(1200, 838, 138, 30),
	]:
		_draw_newport_dock_planks(rect, 18)
		draw_line(rect.position + Vector2(4.0, 3.0), Vector2(rect.end.x - 4.0, rect.position.y + 2.0), Color("#d6bd7d", 0.12), 1.0)
		draw_line(Vector2(rect.position.x + 4.0, rect.end.y - 3.0), rect.end - Vector2(4.0, 3.0), Color(0.02, 0.025, 0.018, 0.22), 1.3)

	for raw_rope in [
		[Vector2(348, 734), Vector2(388, 836)],
		[Vector2(704, 734), Vector2(786, 844)],
		[Vector2(1188, 734), Vector2(1248, 840)],
	]:
		var rope: Array = raw_rope
		draw_line(rope[0], rope[1], Color("#c2a66d", 0.34), 1.3, true)
		draw_line(rope[0] + Vector2(0.0, 2.0), rope[1] + Vector2(0.0, 2.0), Color(0.05, 0.035, 0.02, 0.20), 1.0, true)

	for p in [
		Vector2(316, 704), Vector2(420, 704), Vector2(488, 696), Vector2(526, 696),
		Vector2(774, 698), Vector2(878, 698), Vector2(1152, 702), Vector2(1242, 702),
		Vector2(326, 844), Vector2(432, 844), Vector2(762, 846), Vector2(884, 846),
		Vector2(1214, 844), Vector2(1328, 844),
	]:
		_draw_mooring_bollard(p)

	for p in [Vector2(372, 870), Vector2(820, 872), Vector2(1260, 872)]:
		_draw_waterline_scum(p, 140.0)

func _draw_g423b_frontage_life_props() -> void:
	for pos in [Vector2(182, 594), Vector2(322, 594), Vector2(640, 590), Vector2(1004, 590), Vector2(1160, 590), Vector2(1384, 610)]:
		_draw_door_step(pos)
	for pos in [Vector2(202, 606), Vector2(356, 606), Vector2(768, 408), Vector2(1044, 410), Vector2(1358, 626)]:
		_draw_bench(pos)
	for pos in [Vector2(196, 580), Vector2(332, 582), Vector2(610, 574), Vector2(1028, 574), Vector2(1184, 574)]:
		_draw_lantern(pos)
	for pos in [Vector2(216, 618), Vector2(318, 620), Vector2(632, 612), Vector2(1040, 612), Vector2(1186, 612)]:
		_draw_barrels(pos, 2)
	for pos in [Vector2(272, 616), Vector2(684, 610), Vector2(1116, 612), Vector2(1328, 632)]:
		_draw_crate_stack(pos)
	for pos in [Vector2(410, 382), Vector2(1088, 372), Vector2(280, 462), Vector2(1450, 430)]:
		_draw_woodpile(pos)
	_draw_clothesline(Vector2(1042, 334), Vector2(1178, 340))
	_draw_net_drying_line(Vector2(226, 448), Vector2(326, 430))

func _draw_g423b_harbor_economy_props() -> void:
	for pos in [Vector2(326, 718), Vector2(384, 722), Vector2(1136, 710), Vector2(1216, 710)]:
		_draw_fish_rack(pos)
	for pos in [Vector2(350, 742), Vector2(704, 742), Vector2(842, 734), Vector2(1168, 736), Vector2(1260, 738)]:
		_draw_net_bundle(pos)
	for pos in [Vector2(462, 706), Vector2(802, 706), Vector2(1194, 706)]:
		_draw_sack_stack(pos)
	for pos in [Vector2(494, 712), Vector2(846, 708), Vector2(1224, 708), Vector2(1294, 716)]:
		_draw_crate_stack(pos)
	for pos in [Vector2(420, 716), Vector2(760, 716), Vector2(1160, 716), Vector2(1320, 716)]:
		_draw_rope_coil(pos)
	for pos in [Vector2(308, 690), Vector2(772, 686), Vector2(1128, 690), Vector2(1288, 694)]:
		_draw_lantern(pos)
	_draw_hoop_stack(Vector2(236, 620))
	_draw_hoop_stack(Vector2(1018, 674))

func _draw_mooring_bollard(pos: Vector2) -> void:
	if G422R_SUPPRESS_PRIMITIVE_WORLD_PROPS:
		return
	_draw_contact_shadow(pos + Vector2(0.0, 5.0), Vector2(8.0, 3.0), 0.12)
	draw_rect(Rect2(pos + Vector2(-3.0, -10.0), Vector2(6.0, 15.0)), Color("#33261b"), true)
	draw_rect(Rect2(pos + Vector2(-5.0, -12.0), Vector2(10.0, 4.0)), Color("#6f5134"), true)
	draw_line(pos + Vector2(-5.0, -8.0), pos + Vector2(5.0, -9.0), Color("#d0ad70", 0.22), 1.0)

func _draw_g423b_polyline(points: PackedVector2Array, color: Color, width: float) -> void:
	var closed := PackedVector2Array()
	for point in points:
		closed.append(point)
	if closed.size() > 0:
		closed.append(closed[0])
	draw_polyline(closed, color, width, true)

func _draw_g15a_transition_ground() -> void:
	_draw_newport_grass_swale(PackedVector2Array([
		Vector2(1450, 318), Vector2(1690, 292), Vector2(1948, 314), Vector2(2268, 360),
		Vector2(2318, 506), Vector2(2094, 548), Vector2(1808, 584), Vector2(1510, 634),
		Vector2(1442, 584)
	]), Color("#5e7653", 0.13), Color("#405d3d", 0.07), 44)
	_draw_newport_grass_swale(PackedVector2Array([
		Vector2(1608, 514), Vector2(1840, 486), Vector2(2100, 504), Vector2(2298, 552),
		Vector2(2292, 660), Vector2(2008, 684), Vector2(1740, 648), Vector2(1514, 626)
	]), Color("#586f50", 0.12), Color("#3e563c", 0.07), 38)
	for rect in [
		Rect2(1588, 332, 184, 104),
		Rect2(1808, 334, 198, 108),
		Rect2(1586, 574, 210, 78),
	]:
		_draw_newport_lot_variation(rect, Color("#627a55"), Color("#4f6b49"), 0.10, "opening_island_transition")
		_draw_newport_grass_transition(Rect2(rect.position.x + 10.0, rect.end.y - 13.0, rect.size.x - 20.0, 10.0), "south", 0.13)
	for rect in [
		Rect2(1508, 510, 96, 24),
		Rect2(1660, 482, 220, 18),
		Rect2(1968, 426, 214, 18),
	]:
		_draw_newport_frontage_threshold(rect, "support", 0.16)
	_draw_low_wall(Vector2(1506, 504), Vector2(1586, 498), Color("#6f7b60", 0.26))
	_draw_low_wall(Vector2(1578, 582), Vector2(1698, 570), Color("#6f7b60", 0.22))

func _draw_g15a_transition_streets() -> void:
	_draw_newport_dirt_path(Vector2(1412, 548), Vector2(1560, 548), 23.0, true)
	_draw_newport_dirt_path(Vector2(1560, 548), Vector2(1792, 492), 22.0, true)
	_draw_newport_dirt_path(Vector2(1792, 492), Vector2(2150, 420), 18.0, true)
	_draw_newport_dirt_path(Vector2(2150, 420), Vector2(2288, 394), 13.0, false)
	for raw_dest in [
		Rect2(1490, 536, 164, 34),
		Rect2(1666, 492, 230, 28),
		Rect2(1962, 430, 216, 24),
	]:
		var dest: Rect2 = raw_dest
		_draw_environmental_atelier_placement(_newport_atelier_cobble_path_atlas, NEWPORT_ATELIER_COBBLE_PATH_ATLAS_REGIONS, {
			"asset_id": "atelier_path_dirt_worn_section_01",
			"dest": dest,
			"purpose": "g15a_newport_to_island_road_wear",
			"alpha": 0.42,
		})
	for raw_dest in [
		Rect2(1542, 502, 148, 40),
		Rect2(1840, 452, 176, 38),
		Rect2(2128, 388, 128, 34),
	]:
		var dest: Rect2 = raw_dest
		_draw_environmental_atelier_placement(_newport_atelier_terrain_edge_atlas, NEWPORT_ATELIER_TERRAIN_EDGE_ATLAS_REGIONS, {
			"asset_id": "atelier_terrain_dirt_path_border_01",
			"dest": dest,
			"purpose": "g15a_trail_edge_no_random_green_blocks",
			"alpha": 0.30,
		})
	_draw_newport_grass_transition(Rect2(1508, 574, 276, 14), "south", 0.14)
	_draw_newport_grass_transition(Rect2(1800, 512, 280, 12), "south", 0.12)

func _draw_g15a_transition_props() -> void:
	for fence in [
		[Vector2(1598, 458), Vector2(1768, 450)],
		[Vector2(1660, 572), Vector2(1858, 560)],
		[Vector2(1878, 448), Vector2(2016, 426)],
	]:
		_draw_fence_line(fence[0], fence[1], Color("#d7c894", 0.34))
	_draw_town_identity_atelier_placement(_newport_atelier_lamps_wayfinding_atlas, NEWPORT_ATELIER_LAMPS_WAYFINDING_ATLAS_REGIONS, {
		"asset_id": "atelier_wayfinding_harbor_road_marker_01",
		"dest": Rect2(1496, 510, 40, 44),
		"purpose": "g15a_town_exit_wayfinding_marker",
		"alpha": 0.95,
		"contact_shadow": true,
	})
	_draw_town_identity_atelier_placement(_newport_atelier_lamps_wayfinding_atlas, NEWPORT_ATELIER_LAMPS_WAYFINDING_ATLAS_REGIONS, {
		"asset_id": "atelier_wayfinding_street_lamp_post_01",
		"dest": Rect2(1538, 482, 30, 82),
		"purpose": "g15a_last_village_lantern",
		"alpha": 0.93,
		"contact_shadow": true,
	})
	_draw_town_identity_atelier_placement(_newport_atelier_lamps_wayfinding_atlas, NEWPORT_ATELIER_LAMPS_WAYFINDING_ATLAS_REGIONS, {
		"asset_id": "atelier_wayfinding_coastal_waystone_01",
		"dest": Rect2(1770, 450, 42, 49),
		"purpose": "g15a_settlement_island_boundary_waystone",
		"alpha": 0.90,
		"contact_shadow": true,
	})
	_draw_g418e_hero_family_placement(_newport_g418e_rear_service_connector_atlas, NEWPORT_G418E_REAR_SERVICE_CONNECTOR_ATLAS_REGIONS, {
		"asset_id": "atelier_g418e_service_fence_gate_01",
		"dest": Rect2(1568, 504, 112, 50),
		"purpose": "g15a_fence_break_threshold",
		"alpha": 0.84,
		"contact_shadow": true,
	})
	_draw_g418e_hero_family_placement(_newport_g418e_harbor_dock_edge_atlas, NEWPORT_G418E_HARBOR_DOCK_EDGE_ATLAS_REGIONS, {
		"asset_id": "atelier_g418e_harbor_cargo_stack_01",
		"dest": Rect2(2064, 364, 66, 36),
		"purpose": "g15a_mysterious_roadside_cache",
		"alpha": 0.92,
		"contact_shadow": true,
	})
	for pos in [Vector2(1642, 430), Vector2(1748, 422), Vector2(1888, 398), Vector2(2058, 382), Vector2(2218, 370)]:
		_draw_shrub_cluster(pos, 0.62)
	for pos in [Vector2(1698, 540), Vector2(1868, 500), Vector2(2028, 458)]:
		_draw_shore_rocks(pos)

func _draw_g15b_island_world_ground() -> void:
	_draw_newport_grass_swale(PackedVector2Array([
		Vector2(1540, 360), Vector2(1850, 318), Vector2(2194, 266), Vector2(2378, 298),
		Vector2(2394, 706), Vector2(2228, 746), Vector2(1898, 690), Vector2(1562, 650)
	]), Color("#567252", 0.10), Color("#37583d", 0.05), 72)
	_draw_newport_grass_swale(PackedVector2Array([
		Vector2(1668, 558), Vector2(1900, 540), Vector2(2148, 588), Vector2(2352, 686),
		Vector2(2286, 740), Vector2(2016, 716), Vector2(1742, 674), Vector2(1588, 628)
	]), Color("#68764f", 0.08), Color("#495a37", 0.04), 54)
	_draw_newport_grass_swale(PackedVector2Array([
		Vector2(2068, 292), Vector2(2342, 230), Vector2(2396, 318), Vector2(2314, 404),
		Vector2(2168, 388), Vector2(2070, 346)
	]), Color("#66745a", 0.09), Color("#464e3f", 0.05), 30)
	for rect in [
		Rect2(1690, 592, 180, 74),
		Rect2(1850, 548, 190, 86),
		Rect2(2020, 618, 204, 66),
		Rect2(2190, 326, 162, 60),
	]:
		_draw_newport_lot_variation(rect, Color("#6d7d58"), Color("#526a47"), 0.06, "g15b_island_world")
		_draw_newport_grass_transition(Rect2(rect.position.x + 8.0, rect.end.y - 12.0, rect.size.x - 16.0, 10.0), "south", 0.08)
	for raw_dest in [
		Rect2(1600, 520, 190, 42),
		Rect2(1818, 590, 216, 44),
		Rect2(2048, 690, 222, 38),
		Rect2(2188, 346, 162, 36),
	]:
		var dest: Rect2 = raw_dest
		_draw_environmental_atelier_placement(_newport_atelier_terrain_edge_atlas, NEWPORT_ATELIER_TERRAIN_EDGE_ATLAS_REGIONS, {
			"asset_id": "atelier_terrain_broken_grassy_shoulder_01",
			"dest": dest,
			"purpose": "g15b_grass_stone_dirt_transition_logic",
			"alpha": 0.22,
		})

func _draw_g15b_island_world_routes() -> void:
	_draw_newport_dirt_path(Vector2(1792, 492), Vector2(1840, 626), 17.0, true)
	_draw_newport_dirt_path(Vector2(1840, 626), Vector2(2048, 574), 17.0, true)
	_draw_newport_dirt_path(Vector2(2048, 574), Vector2(2150, 420), 15.0, true)
	_draw_newport_dirt_path(Vector2(2150, 420), Vector2(2288, 332), 14.0, false)
	_draw_newport_dirt_path(Vector2(2048, 574), Vector2(2132, 714), 14.0, true)
	_draw_newport_dirt_path(Vector2(2132, 714), Vector2(1948, 690), 13.0, true)
	_draw_newport_dirt_path(Vector2(1948, 690), Vector2(1780, 642), 15.0, true)
	_draw_newport_dirt_path(Vector2(1780, 642), Vector2(1608, 548), 15.0, true)
	for raw_dest in [
		Rect2(1788, 602, 234, 34),
		Rect2(2008, 548, 184, 32),
		Rect2(2110, 390, 176, 30),
		Rect2(2040, 684, 246, 32),
		Rect2(1744, 626, 212, 30),
	]:
		var dest: Rect2 = raw_dest
		_draw_environmental_atelier_placement(_newport_atelier_cobble_path_atlas, NEWPORT_ATELIER_COBBLE_PATH_ATLAS_REGIONS, {
			"asset_id": "atelier_path_dirt_worn_section_01",
			"dest": dest,
			"purpose": "g15b_routes_lead_somewhere",
			"alpha": 0.30,
		})
	for raw_dest in [
		Rect2(1788, 668, 230, 25),
		Rect2(2032, 728, 238, 26),
		Rect2(2190, 302, 160, 24),
	]:
		var dest: Rect2 = raw_dest
		_draw_environmental_atelier_placement(_newport_atelier_terrain_edge_atlas, NEWPORT_ATELIER_TERRAIN_EDGE_ATLAS_REGIONS, {
			"asset_id": "atelier_terrain_dirt_path_border_01",
			"dest": dest,
			"purpose": "g15b_clear_walkable_edges",
			"alpha": 0.24,
		})

func _draw_g15b_island_world_props() -> void:
	for fence in [
		[Vector2(1698, 686), Vector2(1912, 696)],
		[Vector2(1852, 536), Vector2(1992, 512)],
		[Vector2(2178, 742), Vector2(2338, 748)],
	]:
		_draw_fence_line(fence[0], fence[1], Color("#d7c894", 0.28))
	_draw_town_identity_atelier_placement(_newport_atelier_lamps_wayfinding_atlas, NEWPORT_ATELIER_LAMPS_WAYFINDING_ATLAS_REGIONS, {
		"asset_id": "atelier_wayfinding_coastal_waystone_01",
		"dest": Rect2(2266, 292, 42, 49),
		"purpose": "g15b_signal_rise_visible_route_landmark",
		"alpha": 0.90,
		"contact_shadow": true,
	})
	_draw_g418e_hero_family_placement(_newport_g418e_harbor_dock_edge_atlas, NEWPORT_G418E_HARBOR_DOCK_EDGE_ATLAS_REGIONS, {
		"asset_id": "atelier_g418e_harbor_cargo_stack_01",
		"dest": Rect2(1874, 574, 62, 36),
		"purpose": "g15b_pasture_service_lands_not_empty_sprawl",
		"alpha": 0.86,
		"contact_shadow": true,
	})
	for pos in [Vector2(1968, 488), Vector2(2038, 494), Vector2(2108, 520), Vector2(2206, 282), Vector2(2316, 268)]:
		_draw_shrub_cluster(pos, 0.72)
	for pos in [Vector2(2188, 742), Vector2(2258, 750), Vector2(2326, 746), Vector2(2242, 268), Vector2(2294, 270)]:
		_draw_shore_rocks(pos)

func _draw_g15b_island_shoreline_water() -> void:
	var cove_shore := PackedVector2Array([
		Vector2(1700, 724), Vector2(1850, 704), Vector2(2020, 724), Vector2(2160, 742),
		Vector2(2396, 732), Vector2(2396, 790), Vector2(2188, 784), Vector2(1974, 764),
		Vector2(1780, 752), Vector2(1688, 764)
	])
	draw_colored_polygon(cove_shore, Color(0.31, 0.44, 0.35, 0.44))
	draw_polyline(PackedVector2Array([
		Vector2(1700, 724), Vector2(1850, 704), Vector2(2020, 724), Vector2(2160, 742), Vector2(2396, 732)
	]), Color(0.05, 0.12, 0.13, 0.34), 4.0)
	for raw_dest in [
		Rect2(1704, 708, 212, 42),
		Rect2(1968, 718, 250, 44),
		Rect2(2188, 716, 206, 46),
	]:
		var dest: Rect2 = raw_dest
		_draw_environmental_atelier_placement(_newport_atelier_shoreline_atlas, NEWPORT_ATELIER_SHORELINE_ATLAS_REGIONS, {
			"asset_id": "atelier_shore_wet_sand_mud_strip_01",
			"dest": dest,
			"purpose": "g15b_coastline_shoreline_treatment",
			"alpha": 0.28,
		})

func _draw_g16_island_poi_landmarks() -> void:
	_draw_town_identity_atelier_placement(_newport_atelier_lamps_wayfinding_atlas, NEWPORT_ATELIER_LAMPS_WAYFINDING_ATLAS_REGIONS, {
		"asset_id": "atelier_wayfinding_pier_lantern_stand_01",
		"dest": Rect2(2310, 286, 38, 62),
		"purpose": "g16_signal_overlook_lantern_destination",
		"alpha": 0.92,
		"contact_shadow": true,
	})
	_draw_town_identity_atelier_placement(_newport_atelier_civic_market_atlas, NEWPORT_ATELIER_CIVIC_MARKET_ATLAS_REGIONS, {
		"asset_id": "atelier_civic_anchor_plaque_01",
		"dest": Rect2(2238, 338, 46, 28),
		"purpose": "g16_signal_overlook_harbor_memory_marker",
		"alpha": 0.80,
		"contact_shadow": true,
	})
	_draw_town_identity_atelier_placement(_newport_atelier_lamps_wayfinding_atlas, NEWPORT_ATELIER_LAMPS_WAYFINDING_ATLAS_REGIONS, {
		"asset_id": "atelier_wayfinding_harbor_road_marker_01",
		"dest": Rect2(2104, 386, 42, 48),
		"purpose": "g16_old_road_marker_route_fork",
		"alpha": 0.90,
		"contact_shadow": true,
	})
	_draw_environmental_atelier_placement(_newport_atelier_cobble_path_atlas, NEWPORT_ATELIER_COBBLE_PATH_ATLAS_REGIONS, {
		"asset_id": "atelier_path_loose_paving_fragments_01",
		"dest": Rect2(2088, 430, 116, 28),
		"purpose": "g16_old_road_marker_not_debug_signage",
		"alpha": 0.30,
	})
	for pos in [Vector2(1992, 492), Vector2(2038, 476), Vector2(2098, 500), Vector2(2116, 548)]:
		_draw_shrub_cluster(pos, 0.86)
	for raw_dest in [
		Rect2(1988, 514, 116, 38),
		Rect2(2046, 546, 132, 32),
	]:
		var dest: Rect2 = raw_dest
		_draw_environmental_atelier_placement(_newport_atelier_terrain_edge_atlas, NEWPORT_ATELIER_TERRAIN_EDGE_ATLAS_REGIONS, {
			"asset_id": "atelier_terrain_coastal_tuft_stone_cluster_01",
			"dest": dest,
			"purpose": "g16_wooded_grove_path_natural_landmark",
			"alpha": 0.30,
		})
	_draw_g418e_hero_family_placement(_newport_g418e_rear_service_connector_atlas, NEWPORT_G418E_REAR_SERVICE_CONNECTOR_ATLAS_REGIONS, {
		"asset_id": "atelier_g418e_service_repair_sawhorse_01",
		"dest": Rect2(1818, 542, 66, 40),
		"purpose": "g16_farm_service_outbuilding_edge_settlement",
		"alpha": 0.88,
		"contact_shadow": true,
	})
	_draw_g418e_hero_family_placement(_newport_g418e_rear_service_connector_atlas, NEWPORT_G418E_REAR_SERVICE_CONNECTOR_ATLAS_REGIONS, {
		"asset_id": "atelier_g418e_service_firewood_barrow_01",
		"dest": Rect2(1924, 554, 58, 36),
		"purpose": "g16_farm_service_outbuilding_human_scale",
		"alpha": 0.86,
		"contact_shadow": true,
	})
	_draw_g418e_hero_family_placement(_newport_g418e_harbor_dock_edge_atlas, NEWPORT_G418E_HARBOR_DOCK_EDGE_ATLAS_REGIONS, {
		"asset_id": "atelier_g418e_harbor_bollard_pair_01",
		"dest": Rect2(2242, 698, 54, 32),
		"purpose": "g16_cove_hidden_landing_wharf_remnant",
		"alpha": 0.90,
		"contact_shadow": true,
	})
	_draw_g418e_hero_family_placement(_newport_g418e_harbor_dock_edge_atlas, NEWPORT_G418E_HARBOR_DOCK_EDGE_ATLAS_REGIONS, {
		"asset_id": "atelier_g418e_harbor_rope_coil_large_01",
		"dest": Rect2(2252, 700, 64, 34),
		"purpose": "g16_cove_hidden_landing_smuggling_read",
		"alpha": 0.88,
		"contact_shadow": true,
	})
	_draw_environmental_atelier_placement(_newport_atelier_shoreline_atlas, NEWPORT_ATELIER_SHORELINE_ATLAS_REGIONS, {
		"asset_id": "atelier_shore_driftwood_log_cluster_01",
		"dest": Rect2(2188, 732, 146, 34),
		"purpose": "g16_cove_hidden_landing_shore_story",
		"alpha": 0.34,
	})
	_draw_town_identity_atelier_placement(_newport_atelier_civic_market_atlas, NEWPORT_ATELIER_CIVIC_MARKET_ATLAS_REGIONS, {
		"asset_id": "atelier_civic_dock_rules_board_01",
		"dest": Rect2(2164, 614, 44, 54),
		"purpose": "g16_quest_clue_site_physical_evidence",
		"alpha": 0.86,
		"contact_shadow": true,
	})
	_draw_g418e_hero_family_placement(_newport_g418e_harbor_dock_edge_atlas, NEWPORT_G418E_HARBOR_DOCK_EDGE_ATLAS_REGIONS, {
		"asset_id": "atelier_g418e_harbor_cargo_stack_01",
		"dest": Rect2(2238, 624, 66, 36),
		"purpose": "g16_quest_clue_site_missing_manifest_cache",
		"alpha": 0.82,
		"contact_shadow": true,
	})
	_draw_g418e_hero_family_placement(_newport_g418e_rear_service_connector_atlas, NEWPORT_G418E_REAR_SERVICE_CONNECTOR_ATLAS_REGIONS, {
		"asset_id": "atelier_g418e_service_alley_crates_01",
		"dest": Rect2(2316, 248, 60, 36),
		"purpose": "g16_optional_secret_cache_off_route_discovery",
		"alpha": 0.84,
		"contact_shadow": true,
	})
	_draw_town_identity_atelier_placement(_newport_atelier_lamps_wayfinding_atlas, NEWPORT_ATELIER_LAMPS_WAYFINDING_ATLAS_REGIONS, {
		"asset_id": "atelier_wayfinding_bollard_lantern_01",
		"dest": Rect2(1868, 612, 38, 60),
		"purpose": "g16_return_landmark_visible_from_multiple_routes",
		"alpha": 0.90,
		"contact_shadow": true,
	})

func _draw_g16a_island_atelier_asset_family() -> void:
	for placement in [
		{"asset_id": "atelier_terrain_dirt_path_border_01", "dest": Rect2(1748, 588, 190, 34), "purpose": "g16a_trail_edge_clutter_pasture_lane", "alpha": 0.24},
		{"asset_id": "atelier_terrain_broken_grassy_shoulder_01", "dest": Rect2(1948, 512, 214, 38), "purpose": "g16a_wooded_path_ground_cohesion", "alpha": 0.24},
		{"asset_id": "atelier_terrain_dirt_path_border_01", "dest": Rect2(2128, 654, 210, 34), "purpose": "g16a_clue_site_trail_edge", "alpha": 0.22},
	]:
		_draw_environmental_atelier_placement(_newport_atelier_terrain_edge_atlas, NEWPORT_ATELIER_TERRAIN_EDGE_ATLAS_REGIONS, placement)
	for placement in [
		{"asset_id": "atelier_path_dirt_worn_section_01", "dest": Rect2(2068, 416, 180, 36), "purpose": "g16a_old_road_worn_path_surface", "alpha": 0.22},
		{"asset_id": "atelier_path_loose_paving_fragments_01", "dest": Rect2(2124, 442, 122, 26), "purpose": "g16a_old_road_path_fragments_source_proof", "alpha": 0.24},
	]:
		_draw_environmental_atelier_placement(_newport_atelier_cobble_path_atlas, NEWPORT_ATELIER_COBBLE_PATH_ATLAS_REGIONS, placement)
	for placement in [
		{"asset_id": "atelier_shore_shell_pebble_cluster_01", "dest": Rect2(2104, 734, 148, 30), "purpose": "g16a_coastal_rocks_cove_threshold", "alpha": 0.34},
		{"asset_id": "atelier_shore_wet_rocks_sand_01", "dest": Rect2(2238, 742, 160, 34), "purpose": "g16a_coastal_rocks_hidden_landing_edge", "alpha": 0.34},
		{"asset_id": "atelier_shore_harbor_debris_slats_rope_01", "dest": Rect2(2294, 704, 122, 32), "purpose": "g16a_shore_debris_hidden_landing", "alpha": 0.38},
		{"asset_id": "atelier_shore_eelgrass_reeds_cluster_01", "dest": Rect2(2008, 718, 140, 32), "purpose": "g16a_shore_debris_cove_life", "alpha": 0.30},
		{"asset_id": "atelier_shore_driftwood_log_cluster_01", "dest": Rect2(2168, 760, 152, 32), "purpose": "g16a_shore_debris_coastal_story", "alpha": 0.26},
	]:
		_draw_environmental_atelier_placement(_newport_atelier_shoreline_atlas, NEWPORT_ATELIER_SHORELINE_ATLAS_REGIONS, placement)
	for placement in [
		{"asset_id": "atelier_wayfinding_multi_arrow_signpost_01", "dest": Rect2(2026, 448, 42, 54), "purpose": "g16a_signposts_old_road_choice_without_debug_ui", "alpha": 0.88, "contact_shadow": true},
		{"asset_id": "atelier_wayfinding_coastal_waystone_01", "dest": Rect2(2324, 704, 38, 46), "purpose": "g16a_signposts_cove_waystone", "alpha": 0.86, "contact_shadow": true},
	]:
		_draw_town_identity_atelier_placement(_newport_atelier_lamps_wayfinding_atlas, NEWPORT_ATELIER_LAMPS_WAYFINDING_ATLAS_REGIONS, placement)
	for placement in [
		{"asset_id": "atelier_g418e_service_fence_gate_01", "dest": Rect2(1736, 528, 82, 38), "purpose": "g16a_fences_farm_service_threshold", "alpha": 0.84, "contact_shadow": true},
		{"asset_id": "atelier_g418e_service_utility_barrels_01", "dest": Rect2(1872, 594, 62, 34), "purpose": "g16a_farm_service_props_worked_edge", "alpha": 0.84, "contact_shadow": true},
		{"asset_id": "atelier_g418e_service_stone_edge_01", "dest": Rect2(1818, 628, 108, 24), "purpose": "g16a_farm_service_props_lot_edge", "alpha": 0.72, "contact_shadow": true},
	]:
		_draw_g418e_hero_family_placement(_newport_g418e_rear_service_connector_atlas, NEWPORT_G418E_REAR_SERVICE_CONNECTOR_ATLAS_REGIONS, placement)
	for placement in [
		{"asset_id": "atelier_g418e_harbor_fishing_crate_net_stack_01", "dest": Rect2(2166, 696, 78, 44), "purpose": "g16a_cove_objects_harbor_work_read", "alpha": 0.86, "contact_shadow": true},
		{"asset_id": "atelier_g418e_harbor_service_post_lantern_01", "dest": Rect2(2274, 662, 40, 58), "purpose": "g16a_lantern_posts_hidden_landing_orientation", "alpha": 0.88, "contact_shadow": true},
		{"asset_id": "atelier_g418e_harbor_fish_baskets_tub_01", "dest": Rect2(2306, 622, 82, 40), "purpose": "g16a_small_carts_crates_clue_site_work_props", "alpha": 0.82, "contact_shadow": true},
	]:
		_draw_g418e_hero_family_placement(_newport_g418e_harbor_dock_edge_atlas, NEWPORT_G418E_HARBOR_DOCK_EDGE_ATLAS_REGIONS, placement)

func _draw_g423a_expanded_town_ground() -> void:
	_draw_newport_grass_swale(PackedVector2Array([
		Vector2(28, 124), Vector2(286, 88), Vector2(648, 96), Vector2(962, 88),
		Vector2(1328, 98), Vector2(1572, 132), Vector2(1546, 296), Vector2(1180, 294),
		Vector2(820, 306), Vector2(444, 294), Vector2(54, 304)
	]), Color("#5e7852", 0.14), Color("#415f40", 0.08), 46)
	for rect in [
		Rect2(64, 144, 152, 116),
		Rect2(236, 144, 184, 116),
		Rect2(444, 144, 166, 116),
		Rect2(644, 140, 178, 120),
		Rect2(850, 140, 178, 120),
		Rect2(1054, 144, 170, 116),
		Rect2(1250, 144, 166, 116),
		Rect2(1432, 144, 136, 116),
		Rect2(42, 334, 142, 162),
		Rect2(1450, 334, 124, 174),
	]:
		_draw_newport_lot_variation(rect, Color("#607a56"), Color("#4c6849"), 0.018, "outer_town")
	for rect in [
		Rect2(92, 58, 210, 38),
		Rect2(366, 58, 238, 38),
		Rect2(684, 58, 252, 38),
		Rect2(1038, 58, 232, 38),
		Rect2(1322, 60, 160, 36),
	]:
		_draw_planting_bed(rect, Color("#6a845c"), Color("#506f4c"))
	for rect in [
		Rect2(56, 260, 154, 16),
		Rect2(234, 260, 186, 16),
		Rect2(444, 260, 170, 16),
		Rect2(642, 260, 184, 16),
		Rect2(846, 260, 186, 16),
		Rect2(1052, 260, 174, 16),
		Rect2(1248, 260, 170, 16),
		Rect2(1430, 260, 138, 16),
	]:
		_draw_newport_frontage_threshold(rect, "residential", 0.08)
	for wall in [
		[Vector2(44, 300), Vector2(1558, 300)],
		[Vector2(62, 132), Vector2(1510, 136)],
		[Vector2(58, 516), Vector2(196, 594)],
		[Vector2(1430, 518), Vector2(1558, 590)],
	]:
		_draw_low_wall(wall[0], wall[1], Color("#5f6f58", 0.16))

func _draw_g423a_expanded_town_streets() -> void:
	_draw_newport_street_polygon(PackedVector2Array([
		Vector2(34, 274), Vector2(296, 270), Vector2(548, 274), Vector2(812, 268),
		Vector2(1080, 272), Vector2(1344, 272), Vector2(1566, 278), Vector2(1560, 306),
		Vector2(1342, 302), Vector2(1080, 300), Vector2(814, 298), Vector2(550, 304),
		Vector2(296, 300), Vector2(36, 306)
	]), 54, 0.50)
	_draw_newport_street_polygon(PackedVector2Array([
		Vector2(34, 126), Vector2(336, 118), Vector2(646, 122), Vector2(948, 118),
		Vector2(1260, 122), Vector2(1564, 130), Vector2(1558, 150), Vector2(1258, 144),
		Vector2(948, 144), Vector2(646, 148), Vector2(338, 144), Vector2(36, 150)
	]), 32, 0.24)
	for spec in [
		{"center": Vector2(210, 268), "width": 24.0, "top": 144.0, "bottom": 384.0, "count": 28, "alpha": 0.32},
		{"center": Vector2(552, 276), "width": 24.0, "top": 146.0, "bottom": 316.0, "count": 26, "alpha": 0.30},
		{"center": Vector2(892, 274), "width": 24.0, "top": 144.0, "bottom": 324.0, "count": 28, "alpha": 0.30},
		{"center": Vector2(1268, 276), "width": 24.0, "top": 148.0, "bottom": 410.0, "count": 32, "alpha": 0.31},
	]:
		_draw_g7a_soft_service_trace(Vector2(spec["center"].x, spec["top"]), Vector2(spec["center"].x, spec["bottom"]), float(spec["width"]) * 0.70, 0.16)
	_draw_g7a_soft_service_trace(Vector2(70, 430), Vector2(206, 596), 12.0, 0.16)
	_draw_g7a_soft_service_trace(Vector2(1518, 420), Vector2(1428, 622), 12.0, 0.16)
	for rect in [
		Rect2(36, 306, 1518, 8),
		Rect2(40, 152, 1518, 6),
	]:
		_draw_newport_grass_transition(rect, "south", 0.07)

func _draw_g423a_expanded_town_fabric() -> void:
	for config in [
		{"sprite_id": "newport_narrow_clapboard_townhouse_b", "foot": Vector2(136, 260), "width": 84.0, "alpha": 0.76},
		{"sprite_id": "atelier_newport_harbor_cottage_gabled_01", "foot": Vector2(318, 260), "width": 104.0, "alpha": 0.78},
		{"sprite_id": "newport_formal_townhouse_block_a", "foot": Vector2(528, 260), "width": 126.0, "alpha": 0.78},
		{"sprite_id": "newport_elite_mansion_white", "foot": Vector2(734, 260), "width": 138.0, "alpha": 0.74},
		{"sprite_id": "newport_georgian_merchant_residence_a", "foot": Vector2(940, 260), "width": 124.0, "alpha": 0.76},
		{"sprite_id": "atelier_newport_harbor_cottage_dormer_01", "foot": Vector2(1140, 260), "width": 104.0, "alpha": 0.78},
		{"sprite_id": "newport_chandlery_cottage", "foot": Vector2(1318, 260), "width": 108.0, "alpha": 0.76},
		{"sprite_id": "newport_narrow_clapboard_townhouse_b", "foot": Vector2(1500, 260), "width": 86.0, "alpha": 0.76},
		{"sprite_id": "newport_chandlery_cottage", "foot": Vector2(96, 430), "width": 112.0, "alpha": 0.70},
		{"sprite_id": "newport_market_frontage_row", "foot": Vector2(1518, 444), "width": 120.0, "alpha": 0.70},
		{"sprite_id": "atelier_newport_harbor_cottage_gabled_01", "foot": Vector2(70, 604), "width": 92.0, "alpha": 0.64},
		{"sprite_id": "newport_narrow_merchant_townhouse_a", "foot": Vector2(1540, 612), "width": 82.0, "alpha": 0.64},
	]:
		_draw_g423a_visual_building(config)
	for fence in [
		[Vector2(70, 276), Vector2(196, 276)],
		[Vector2(242, 276), Vector2(396, 276)],
		[Vector2(456, 276), Vector2(600, 276)],
		[Vector2(654, 276), Vector2(810, 276)],
		[Vector2(862, 276), Vector2(1016, 276)],
		[Vector2(1066, 276), Vector2(1210, 276)],
		[Vector2(1260, 276), Vector2(1390, 276)],
		[Vector2(1440, 276), Vector2(1548, 276)],
	]:
		_draw_fence_line(fence[0], fence[1], Color("#d7c894", 0.30))
	for pos in [
		Vector2(92, 76), Vector2(146, 72), Vector2(212, 78), Vector2(384, 72),
		Vector2(452, 70), Vector2(560, 74), Vector2(702, 70), Vector2(782, 72),
		Vector2(910, 70), Vector2(1064, 74), Vector2(1140, 70), Vector2(1246, 76),
		Vector2(1360, 78), Vector2(1450, 82), Vector2(1540, 168)
	]:
		draw_circle(pos, 11, Color("#2f5d35", 0.92))
		draw_circle(pos + Vector2(-7, -7), 7, Color("#3d7042", 0.88))
	for pos in [Vector2(220, 252), Vector2(552, 258), Vector2(892, 252), Vector2(1268, 260)]:
		_draw_lantern(pos)

func _draw_g423a_visual_building(config: Dictionary) -> void:
	var sprite_id := String(config.get("sprite_id", ""))
	var sprite := BUILDING_CATALOG.sprite_config(sprite_id)
	if sprite.is_empty():
		return
	var atlas_path := String(sprite.get("atlas_path", ""))
	var texture := _g423a_building_texture(atlas_path)
	if texture == null:
		return
	var region: Rect2 = sprite.get("region", Rect2())
	var source_size: Vector2 = sprite.get("source_size", region.size)
	var draw_width := float(config.get("width", source_size.x))
	var scale := draw_width / maxf(1.0, source_size.x)
	var dest_size := source_size * scale
	var foot: Vector2 = config.get("foot", Vector2.ZERO)
	var alpha := float(config.get("alpha", 1.0))
	var dest := Rect2(foot - Vector2(dest_size.x * 0.5, dest_size.y), dest_size)
	_draw_contact_shadow(foot + Vector2(0.0, -4.0), Vector2(draw_width * 0.42, 8.0), 0.09 * alpha)
	draw_texture_rect_region(texture, dest, region, Color(1.0, 1.0, 1.0, alpha), false, true)

func _g423a_building_texture(path: String) -> Texture2D:
	if path.is_empty():
		return null
	if _building_texture_cache.has(path):
		return _building_texture_cache[path] as Texture2D
	var texture := ResourceLoader.load(path, "Texture2D") as Texture2D
	if texture == null:
		push_warning("Failed to load Newport outer town building texture: " + path)
		return null
	_building_texture_cache[path] = texture
	return texture

func _draw_g423a_lot_threshold_overlays() -> void:
	if G422R_HIDE_NORMAL_PLAY_LAYOUT_GUIDES:
		return
	var rules: Dictionary = NEWPORT_TOWN.g415_layout_rules()
	for raw_id in rules.keys():
		var rule: Dictionary = rules[raw_id]
		var band := String(rule.get("district_band", ""))
		if band == "dock":
			continue
		var pad: Dictionary = rule.get("ground_pad", {})
		var rect: Rect2 = pad.get("rect", Rect2())
		if rect.size.x <= 0.0 or rect.size.y <= 0.0:
			continue
		if ["commercial", "market"].has(band):
			var threshold := Rect2(rect.position.x + 8.0, rect.end.y - 28.0, maxf(24.0, rect.size.x - 16.0), 24.0)
			_draw_newport_frontage_threshold(threshold, "market" if band == "market" else "commercial", 0.34)
		elif band == "civic":
			var civic_threshold := Rect2(rect.position.x + 12.0, rect.end.y - 26.0, maxf(32.0, rect.size.x - 24.0), 22.0)
			_draw_newport_frontage_threshold(civic_threshold, "civic", 0.28)
		elif band == "support":
			var support_threshold := Rect2(rect.position.x + 10.0, rect.end.y - 24.0, maxf(30.0, rect.size.x - 20.0), 20.0)
			_draw_newport_frontage_threshold(support_threshold, "support", 0.26)
		elif band == "residential":
			var yard_edge := Rect2(rect.position.x + 10.0, rect.end.y - 18.0, maxf(30.0, rect.size.x - 20.0), 12.0)
			_draw_newport_grass_transition(yard_edge, "south", 0.14)

func _draw_g418_hero_non_cargo_prop_clusters() -> void:
	if _newport_hero_atlas == null:
		return
	_draw_hero_atlas_piece("fence_sign_market_cluster", Rect2(1324, 610, 118, 87), 0.92)
	_draw_hero_atlas_piece("market_sign_cluster", Rect2(790, 708, 92, 64), 0.88)

func _draw_g418d_atelier_cargo_clusters() -> void:
	if _newport_atelier_cargo_atlas == null:
		return
	for placement in NEWPORT_ATELIER_CARGO_PLACEMENTS:
		_draw_atelier_cargo_placement(placement)

func _draw_g419a_atelier_dock_clutter_clusters() -> void:
	if _newport_atelier_dock_clutter_atlas == null:
		return
	for placement in NEWPORT_ATELIER_DOCK_CLUTTER_PLACEMENTS:
		_draw_atelier_dock_clutter_placement(placement)

func _draw_g420a_terrain_and_path_transitions() -> void:
	for placement in NEWPORT_G420A_TERRAIN_EDGE_PLACEMENTS:
		_draw_environmental_atelier_placement(_newport_atelier_terrain_edge_atlas, NEWPORT_ATELIER_TERRAIN_EDGE_ATLAS_REGIONS, placement)
	for placement in NEWPORT_G420A_COBBLE_PATH_PLACEMENTS:
		_draw_environmental_atelier_placement(_newport_atelier_cobble_path_atlas, NEWPORT_ATELIER_COBBLE_PATH_ATLAS_REGIONS, placement)

func _draw_g420a_shoreline_edges() -> void:
	for placement in NEWPORT_G420A_SHORELINE_PLACEMENTS:
		_draw_environmental_atelier_placement(_newport_atelier_shoreline_atlas, NEWPORT_ATELIER_SHORELINE_ATLAS_REGIONS, placement)

func _draw_g420a_building_grounding_accents() -> void:
	for placement in NEWPORT_G420A_BUILDING_GROUNDING_PLACEMENTS:
		_draw_environmental_atelier_placement(_newport_atelier_building_grounding_atlas, NEWPORT_ATELIER_BUILDING_GROUNDING_ATLAS_REGIONS, placement)

func _draw_g420b_town_identity_accents() -> void:
	for placement in NEWPORT_G420B_SIGN_SHOP_MARKER_PLACEMENTS:
		if _is_g422r_hidden_normal_play_marker(placement):
			continue
		_draw_town_identity_atelier_placement(_newport_atelier_sign_shop_markers_atlas, NEWPORT_ATELIER_SIGN_SHOP_MARKERS_ATLAS_REGIONS, placement)
	for placement in NEWPORT_G420B_LAMPS_WAYFINDING_PLACEMENTS:
		if _is_g422r_hidden_normal_play_marker(placement):
			continue
		_draw_town_identity_atelier_placement(_newport_atelier_lamps_wayfinding_atlas, NEWPORT_ATELIER_LAMPS_WAYFINDING_ATLAS_REGIONS, placement)
	for placement in NEWPORT_G420B_CIVIC_MARKET_PLACEMENTS:
		if _is_g422r_hidden_normal_play_marker(placement):
			continue
		_draw_town_identity_atelier_placement(_newport_atelier_civic_market_atlas, NEWPORT_ATELIER_CIVIC_MARKET_ATLAS_REGIONS, placement)
	for placement in NEWPORT_G420B_SHOPFRONT_SUPPORT_PLACEMENTS:
		if _is_g422r_hidden_normal_play_marker(placement):
			continue
		_draw_town_identity_atelier_placement(_newport_atelier_shopfront_support_atlas, NEWPORT_ATELIER_SHOPFRONT_SUPPORT_ATLAS_REGIONS, placement)

func _draw_g418e_hero_asset_family_accents() -> void:
	for placement in NEWPORT_G418E_TAVERN_INN_PLACEMENTS:
		_draw_g418e_hero_family_placement(_newport_g418e_tavern_inn_atlas, NEWPORT_G418E_TAVERN_INN_ATLAS_REGIONS, placement)
	for placement in NEWPORT_G418E_COMMERCIAL_AVENUE_PLACEMENTS:
		if _is_g422r_hidden_normal_play_marker(placement):
			continue
		_draw_g418e_hero_family_placement(_newport_g418e_commercial_avenue_atlas, NEWPORT_G418E_COMMERCIAL_AVENUE_ATLAS_REGIONS, placement)
	for placement in NEWPORT_G418E_HARBOR_DOCK_EDGE_PLACEMENTS:
		_draw_g418e_hero_family_placement(_newport_g418e_harbor_dock_edge_atlas, NEWPORT_G418E_HARBOR_DOCK_EDGE_ATLAS_REGIONS, placement)
	for placement in NEWPORT_G418E_REAR_SERVICE_CONNECTOR_PLACEMENTS:
		_draw_g418e_hero_family_placement(_newport_g418e_rear_service_connector_atlas, NEWPORT_G418E_REAR_SERVICE_CONNECTOR_ATLAS_REGIONS, placement)

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
	draw_rect(rect, Color(base.r, base.g, base.b, alpha), true)
	for i in range(detail_count):
		var x := rect.position.x + fmod(float(i * 71 + 17), maxf(1.0, rect.size.x - 18.0))
		var y := rect.position.y + fmod(float(i * 43 + 29), maxf(1.0, rect.size.y - 8.0))
		var p := Vector2(x, y)
		var stroke_alpha := alpha * (0.08 + float(i % 4) * 0.012)
		draw_line(p, p + Vector2(18.0 + float(i % 5) * 4.0, -2.0), Color(alt.r, alt.g, alt.b, stroke_alpha), 1.0)
		if i % 3 == 0:
			draw_line(p + Vector2(2.0, 5.0), p + Vector2(15.0 + float(i % 4) * 3.0, 4.0), Color("#9aac72", stroke_alpha * 0.70), 1.0)
		if i % 7 == 0:
			draw_rect(Rect2(p + Vector2(3.0, 8.0), Vector2(18.0, 2.0)), Color(0.06, 0.08, 0.04, alpha * 0.035), true)
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

func _draw_newport_grass_swale(points: PackedVector2Array, fill: Color, stroke: Color, detail_count: int) -> void:
	if points.size() < 3:
		return
	draw_colored_polygon(points, fill)
	var bounds := _bounds_for_points(points)
	for i in range(detail_count):
		var x := bounds.position.x + fmod(float(i * 71 + 17), maxf(1.0, bounds.size.x - 24.0))
		var y := bounds.position.y + fmod(float(i * 43 + 29), maxf(1.0, bounds.size.y - 8.0))
		var p := Vector2(x, y)
		draw_line(p, p + Vector2(18.0 + float(i % 5) * 4.0, -2.0), stroke, 1.0)
		if i % 4 == 0:
			draw_line(p + Vector2(3.0, 5.0), p + Vector2(16.0, 4.0), Color("#a7b675", stroke.a * 0.58), 1.0)

func _soft_rect_polygon(rect: Rect2) -> PackedVector2Array:
	return PackedVector2Array([
		rect.position + Vector2(3.0, 5.0),
		rect.position + Vector2(rect.size.x * 0.47, -3.0),
		rect.position + Vector2(rect.size.x - 4.0, 4.0),
		rect.position + Vector2(rect.size.x - 2.0, rect.size.y - 7.0),
		rect.position + Vector2(rect.size.x * 0.52, rect.size.y + 2.0),
		rect.position + Vector2(4.0, rect.size.y - 4.0),
	])

func _draw_newport_lot_variation(rect: Rect2, base: Color, alt: Color, alpha: float, district: String) -> void:
	draw_rect(rect, Color(base.r, base.g, base.b, alpha), true)
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

func _draw_newport_frontage_threshold(rect: Rect2, kind: String, alpha := 0.40) -> void:
	var base := Color("#756e5b", alpha)
	if kind == "market":
		base = Color("#796d55", alpha)
	elif kind == "civic":
		base = Color("#777264", alpha)
	elif kind == "support":
		base = Color("#6b604d", alpha)
	var slab := Rect2(rect.position.x, rect.end.y - minf(22.0, rect.size.y), rect.size.x, minf(22.0, rect.size.y))
	var points := PackedVector2Array([
		slab.position + Vector2(2.0, 1.0),
		slab.position + Vector2(slab.size.x - 3.0, -1.0),
		slab.position + Vector2(slab.size.x - 1.0, slab.size.y - 3.0),
		slab.position + Vector2(slab.size.x * 0.48, slab.size.y + 1.0),
		slab.position + Vector2(3.0, slab.size.y - 2.0),
	])
	draw_colored_polygon(points, Color(0.02, 0.025, 0.018, alpha * 0.18))
	draw_colored_polygon(points, base)
	for i in range(maxi(3, int(slab.size.x / 30.0))):
		var x := slab.position.x + 8.0 + fmod(float(i * 37 + 9), maxf(1.0, slab.size.x - 18.0))
		draw_line(Vector2(x, slab.position.y + 4.0), Vector2(x - 4.0, slab.end.y - 4.0), Color(0.03, 0.03, 0.025, alpha * 0.24), 1.0)
	draw_line(slab.position + Vector2(6.0, 2.0), slab.position + Vector2(slab.size.x - 8.0, 1.0), Color("#d5c28c", alpha * 0.18), 1.0)
	draw_line(slab.position + Vector2(5.0, slab.size.y - 2.0), slab.position + Vector2(slab.size.x - 7.0, slab.size.y - 3.0), Color("#3f382d", alpha * 0.54), 1.0)

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

func _draw_newport_street_polygon(points: PackedVector2Array, detail_count: int, alpha := 1.0) -> void:
	if points.size() < 3:
		return
	var shadow_points := PackedVector2Array()
	for point in points:
		shadow_points.append(point + Vector2(0.0, 4.0))
	draw_colored_polygon(shadow_points, Color(0.02, 0.022, 0.018, 0.12 * alpha))
	draw_colored_polygon(points, Color("#635d50", alpha))
	var bounds := _bounds_for_points(points)
	for i in range(detail_count):
		var w := 12.0 + float((i * 7) % 17)
		var h := 5.0 + float((i * 5) % 9)
		var x := bounds.position.x + fmod(float(i * 43 + 17), maxf(1.0, bounds.size.x - w))
		var y := bounds.position.y + fmod(float(i * 31 + 11), maxf(1.0, bounds.size.y - h))
		if not Geometry2D.is_point_in_polygon(Vector2(x + w * 0.5, y + h * 0.5), points):
			continue
		var n := fmod(float(i * 19), 100.0) / 100.0
		var stone := Color("#6f6958").lerp(Color("#a69a75"), n * 0.34)
		draw_rect(Rect2(Vector2(x, y), Vector2(w, h)), Color(stone.r, stone.g, stone.b, 0.18 * alpha), true)
	draw_polyline(points, Color("#d0bd85", 0.10 * alpha), 1.0, true)

func _draw_newport_uphill_street(center: Vector2, width: float, top: float, bottom: float, detail_count: int, alpha := 1.0) -> void:
	var half := width * 0.5
	var points := PackedVector2Array([
		Vector2(center.x - half - 5.0, top + 4.0),
		Vector2(center.x + half - 2.0, top - 2.0),
		Vector2(center.x + half + 6.0, bottom - 8.0),
		Vector2(center.x + half * 0.30, bottom + 2.0),
		Vector2(center.x - half - 3.0, bottom - 4.0),
	])
	_draw_newport_street_polygon(points, detail_count, alpha)

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
	draw_rect(rect, Color("#635d50", alpha), true)
	_draw_surface_speckles(rect.grow(-5.0), maxi(6, int(rect.size.y / 18.0)), Color(0.10, 0.075, 0.045, alpha * 0.18), Vector2(24, 3))
	for x in range(int(rect.position.x + 10.0), int(rect.end.x - 8.0), 26):
		var y := rect.position.y + 8.0 + fmod(float(x * 5), maxf(1.0, rect.size.y - 12.0))
		draw_line(Vector2(x, y), Vector2(x + 13.0, y - 1.0), Color("#d0bd85", alpha * 0.24), 1.0)
		if x % 3 == 0:
			draw_circle(Vector2(x + 5.0, y + 4.0), 1.5, Color(0.10, 0.07, 0.04, alpha * 0.32))

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
	draw_rect(rect, Color("#2e7183", alpha), true)
	for i in range(54):
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
	if G422R_SUPPRESS_PRIMITIVE_WORLD_PROPS:
		return
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
	if G422R_SUPPRESS_PRIMITIVE_WORLD_PROPS:
		return
	draw_circle(pos, 8, Color("#75543a"))
	draw_arc(pos, 8, 0, TAU, 18, Color("#c09b62"), 1.5)
	draw_arc(pos, 4.5, 0, TAU, 14, Color("#d5b574"), 1.2)

func _draw_crate_stack(pos: Vector2) -> void:
	if G422R_SUPPRESS_PRIMITIVE_WORLD_PROPS:
		return
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
	if G422R_SUPPRESS_PRIMITIVE_WORLD_PROPS:
		return
	for i in range(count):
		var barrel_pos := pos + Vector2(i * 9, 0)
		_draw_ellipse(barrel_pos + Vector2(1.0, 6.0), Vector2(6, 2.2), Color(0.02, 0.018, 0.012, 0.15))
		_draw_ellipse(barrel_pos, Vector2(4.8, 7.4), Color("#7f5631"))
		_draw_ellipse(barrel_pos + Vector2(-1.2, -1.8), Vector2(2.0, 4.5), Color("#a46e3c", 0.36))
		draw_rect(Rect2(barrel_pos + Vector2(-4.5, -2.0), Vector2(9.0, 2.0)), Color("#3f2c1d"), true)
		draw_rect(Rect2(barrel_pos + Vector2(-4.5, 2.0), Vector2(9.0, 2.0)), Color("#3f2c1d"), true)
		draw_arc(barrel_pos, 6.0, 0, TAU, 16, Color("#c2965a"), 1.1)

func _draw_market_table(pos: Vector2) -> void:
	if G422R_SUPPRESS_PRIMITIVE_WORLD_PROPS:
		return
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
	if G422R_SUPPRESS_PRIMITIVE_WORLD_PROPS:
		return
	draw_line(pos + Vector2(1.0, 18.0), pos + Vector2(39.0, 18.0), Color(0.02, 0.018, 0.012, 0.16), 3.0)
	draw_line(pos, pos + Vector2(38, 0), Color("#6c4b30"), 2.0)
	draw_line(pos + Vector2(3, 0), pos + Vector2(3, 18), Color("#6c4b30"), 2.0)
	draw_line(pos + Vector2(35, 0), pos + Vector2(35, 18), Color("#6c4b30"), 2.0)
	draw_line(pos + Vector2(0, -1), pos + Vector2(38, -1), Color("#c29a62", 0.24), 1.0)
	for i in range(7):
		draw_rect(Rect2(pos + Vector2(6 + i * 5, 2), Vector2(2, 9)), Color("#c9b98c"), true)
		draw_line(pos + Vector2(7 + i * 5, 2), pos + Vector2(7 + i * 5, 11), Color("#4b4538", 0.22), 1.0)

func _draw_net_bundle(pos: Vector2) -> void:
	if G422R_SUPPRESS_PRIMITIVE_WORLD_PROPS:
		return
	draw_arc(pos, 14, 0.15, PI - 0.15, 16, Color("#c8b277"), 1.0)
	draw_arc(pos + Vector2(4, 2), 11, 0.15, PI - 0.15, 16, Color("#a98e58"), 1.0)
	for i in range(4):
		draw_line(pos + Vector2(-10 + i * 6, 0), pos + Vector2(-6 + i * 7, 12), Color("#c8b277"), 1.0)

func _draw_rowboat(pos: Vector2) -> void:
	if G422R_SUPPRESS_PRIMITIVE_WORLD_PROPS:
		return
	_draw_ellipse(pos, Vector2(32, 8), Color(0.18, 0.12, 0.07, 0.48))
	_draw_ellipse(pos, Vector2(26, 7), Color("#65452c"))
	_draw_ellipse(pos, Vector2(18, 4), Color("#2c4f5b"))
	draw_line(pos + Vector2(-18, -2), pos + Vector2(18, -2), Color("#a67c4c"), 1.5)

func _draw_sign_post(pos: Vector2, color: Color) -> void:
	if G422R_SUPPRESS_PRIMITIVE_WORLD_PROPS:
		return
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
	if G422R_SUPPRESS_PRIMITIVE_WORLD_PROPS:
		return
	_draw_contact_shadow(pos + Vector2(16.0, 8.0), Vector2(22.0, 5.0), 0.12)
	for i in range(5):
		var p := pos + Vector2(i * 7, (i % 2) * 4)
		draw_rect(Rect2(p, Vector2(10, 3)), Color("#775032"), true)
		draw_circle(p + Vector2(1, 1.5), 1.5, Color("#b98750"))

func _draw_g410_background_depth() -> void:
	if NEWPORT_TOWN.G422A_SHOW_LEGACY_PROOF_OVERLAYS:
		for spec in [
			{"base": Rect2(112, 210, 90, 54), "roof": Color("#2f3e35", 0.08), "wall": Color("#6f8065", 0.045)},
			{"base": Rect2(474, 140, 128, 58), "roof": Color("#2e3d36", 0.075), "wall": Color("#6b7f62", 0.04)},
			{"base": Rect2(1012, 142, 112, 54), "roof": Color("#2e3a34", 0.075), "wall": Color("#708163", 0.04)},
			{"base": Rect2(1316, 214, 116, 58), "roof": Color("#2c3932", 0.07), "wall": Color("#6a7c5f", 0.038)},
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
		_draw_low_wall(wall[0], wall[1], Color("#67735d", 0.18))

func _draw_g422a_town_edge_boundaries() -> void:
	for wall in [
		[Vector2(178, 246), Vector2(378, 232)],
		[Vector2(402, 232), Vector2(640, 230)],
		[Vector2(760, 230), Vector2(982, 228)],
		[Vector2(1016, 230), Vector2(1238, 236)],
		[Vector2(1264, 248), Vector2(1450, 266)],
		[Vector2(144, 356), Vector2(222, 524)],
		[Vector2(1472, 332), Vector2(1488, 604)],
	]:
		_draw_low_wall(wall[0], wall[1], Color("#73815f", 0.32))
	for fence in [
		[Vector2(300, 346), Vector2(432, 350)],
		[Vector2(584, 348), Vector2(742, 350)],
		[Vector2(1018, 338), Vector2(1178, 344)],
		[Vector2(1228, 382), Vector2(1374, 392)],
		[Vector2(1386, 432), Vector2(1540, 432)],
	]:
		_draw_fence_line(fence[0], fence[1], Color("#cdbb86", 0.42))
	for pos in [
		Vector2(208, 250), Vector2(258, 236), Vector2(342, 232), Vector2(440, 224),
		Vector2(646, 232), Vector2(944, 226), Vector2(1210, 242), Vector2(1392, 282),
		Vector2(154, 356), Vector2(150, 510), Vector2(1466, 356), Vector2(1480, 548),
	]:
		draw_circle(pos, 12.0, Color("#2f5d35", 0.62))
		draw_circle(pos + Vector2(-7.0, -6.0), 7.0, Color("#3d7042", 0.54))

func _draw_surface_speckles(rect: Rect2, count: int, color: Color, max_size: Vector2) -> void:
	for i in range(count):
		var x := rect.position.x + fmod(float(i * 37 + 11), maxf(1.0, rect.size.x - max_size.x))
		var y := rect.position.y + fmod(float(i * 19 + 7), maxf(1.0, rect.size.y - max_size.y))
		var w := 4.0 + float((i * 5) % int(maxf(5.0, max_size.x)))
		var h := 1.0 + float((i * 3) % int(maxf(2.0, max_size.y)))
		draw_rect(Rect2(Vector2(x, y), Vector2(w, h)), color, true)

func _bounds_for_points(points: PackedVector2Array) -> Rect2:
	if points.is_empty():
		return Rect2()
	var min_x := points[0].x
	var max_x := points[0].x
	var min_y := points[0].y
	var max_y := points[0].y
	for point in points:
		min_x = minf(min_x, point.x)
		max_x = maxf(max_x, point.x)
		min_y = minf(min_y, point.y)
		max_y = maxf(max_y, point.y)
	return Rect2(Vector2(min_x, min_y), Vector2(max_x - min_x, max_y - min_y))

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
	if G422R_SUPPRESS_PRIMITIVE_WORLD_PROPS:
		return
	_draw_ellipse(pos + Vector2(8.0, 6.0), Vector2(10.0, 6.0), Color("#b69a68", 0.92))
	_draw_ellipse(pos + Vector2(20.0, 7.0), Vector2(9.0, 6.0), Color("#9e8458", 0.92))
	_draw_ellipse(pos + Vector2(14.0, -1.0), Vector2(11.0, 6.0), Color("#c0a873", 0.92))
	draw_line(pos + Vector2(8.0, 1.0), pos + Vector2(20.0, 0.0), Color("#6a5232", 0.35), 1.0)

func _draw_lantern(pos: Vector2) -> void:
	if G422R_SUPPRESS_PRIMITIVE_WORLD_PROPS:
		return
	draw_rect(Rect2(pos + Vector2(-1.0, 0.0), Vector2(2.0, 18.0)), Color("#3e2c1d"), true)
	draw_rect(Rect2(pos + Vector2(-5.0, -9.0), Vector2(10.0, 11.0)), Color("#4a3320"), true)
	draw_rect(Rect2(pos + Vector2(-3.0, -7.0), Vector2(6.0, 7.0)), Color("#d2a956", 0.72), true)
	draw_circle(pos + Vector2(0.0, -3.0), 8.0, Color("#d2a956", 0.08))

func _draw_hoop_stack(pos: Vector2) -> void:
	if G422R_SUPPRESS_PRIMITIVE_WORLD_PROPS:
		return
	for i in range(3):
		var center := pos + Vector2(i * 8.0, float(i % 2) * 2.0)
		draw_arc(center, 8.0, 0.0, TAU, 18, Color("#b48750", 0.88), 1.4)
		draw_arc(center, 5.0, 0.0, TAU, 14, Color("#5f4025", 0.72), 1.0)

func _draw_bench(pos: Vector2) -> void:
	if G422R_SUPPRESS_PRIMITIVE_WORLD_PROPS:
		return
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
