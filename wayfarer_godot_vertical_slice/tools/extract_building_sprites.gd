extends SceneTree

const OUTPUT_DIR := "res://assets/sprites/buildings/isolated"
const PADDING := 24

const CROPS := [
	{
		"id": "inn_tavern_v1",
		"source": "res://assets/buildings/hearthvale_buildings_atlas_v1.png",
		"rect": Rect2i(36, 45, 425, 420),
		"output": "inn_tavern_v1_isolated.png",
	},
	{
		"id": "mercantile_shop",
		"source": "res://assets/buildings/hearthvale_buildings_atlas_v1.png",
		"rect": Rect2i(452, 67, 350, 403),
		"output": "mercantile_shop_isolated.png",
		"erase_rects": [
			Rect2i(18, 328, 6, 96),
		],
	},
	{
		"id": "newport_counting_house_civic_exchange",
		"source": "res://assets/buildings/hearthvale_newport_structure_pack_v1_b.png",
		"rect": Rect2i(378, 475, 410, 322),
		"output": "newport_counting_house_civic_exchange_isolated.png",
	},
	{
		"id": "newport_chandlery_outfitter_front",
		"source": "res://assets/buildings/hearthvale_newport_structure_pack_v1_b.png",
		"rect": Rect2i(815, 444, 387, 352),
		"output": "newport_chandlery_outfitter_front_isolated.png",
	},
	{
		"id": "newport_shopfront_awning",
		"source": "res://assets/buildings/hearthvale_newport_structure_pack_v1_a.png",
		"rect": Rect2i(486, 442, 365, 400),
		"output": "newport_shopfront_awning_isolated.png",
		"erase_rects": [
			Rect2i(0, 0, 30, 448),
		],
	},
	{
		"id": "newport_dockside_storehouse_long",
		"source": "res://assets/buildings/hearthvale_newport_structure_pack_v1_a.png",
		"rect": Rect2i(386, 870, 340, 350),
		"output": "newport_dockside_storehouse_long_isolated.png",
	},
	{
		"id": "newport_wharf_boathouse_large",
		"source": "res://assets/buildings/hearthvale_newport_structure_pack_v1_a.png",
		"rect": Rect2i(724, 796, 530, 430),
		"output": "newport_wharf_boathouse_large_isolated.png",
	},
	{
		"id": "newport_dockside_storehouse",
		"source": "res://assets/buildings/hearthvale_newport_structure_pack_v1_b.png",
		"rect": Rect2i(40, 826, 395, 400),
		"output": "newport_dockside_storehouse_isolated.png",
		"erase_rects": [
			Rect2i(410, 0, 33, 448),
		],
	},
	{
		"id": "village_hall_meeting_house",
		"source": "res://assets/buildings/hearthvale_buildings_atlas_v1.png",
		"rect": Rect2i(850, 10, 390, 450),
		"output": "village_hall_meeting_house_isolated.png",
	},
	{
		"id": "residence_small",
		"source": "res://assets/buildings/hearthvale_buildings_atlas_v1.png",
		"rect": Rect2i(58, 520, 345, 320),
		"output": "residence_small_isolated.png",
	},
	{
		"id": "newport_market_shed_stalls",
		"source": "res://assets/buildings/hearthvale_newport_structure_pack_v1_b.png",
		"rect": Rect2i(430, 826, 386, 390),
		"output": "newport_market_shed_stalls_isolated.png",
	},
	{
		"id": "newport_custom_house_civic_front",
		"source": "res://assets/buildings/hearthvale_newport_structure_pack_v1_b.png",
		"rect": Rect2i(38, 19, 389, 385),
		"output": "newport_custom_house_civic_front_isolated.png",
	},
	{
		"id": "newport_large_front_residence",
		"source": "res://assets/buildings/hearthvale_newport_structure_pack_v1_a.png",
		"rect": Rect2i(61, 469, 387, 321),
		"output": "newport_large_front_residence_isolated.png",
	},
	{
		"id": "newport_modest_clapboard_residence_a",
		"source": "res://assets/buildings/hearthvale_newport_structure_pack_v1_b.png",
		"rect": Rect2i(104, 433, 199, 370),
		"output": "newport_modest_clapboard_residence_a_isolated.png",
	},
	{
		"id": "service_dependency_shed",
		"source": "res://assets/buildings/hearthvale_buildings_atlas_v1.png",
		"rect": Rect2i(899, 939, 250, 245),
		"output": "service_dependency_shed_isolated.png",
	},
]

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	var output_abs := ProjectSettings.globalize_path(OUTPUT_DIR)
	var make_dir_error := DirAccess.make_dir_recursive_absolute(output_abs)
	if make_dir_error != OK:
		push_error("Failed to create isolated sprite output dir: %s" % output_abs)
		quit(1)
		return

	for crop_config in CROPS:
		var source_path: String = crop_config["source"]
		var crop_rect: Rect2i = crop_config["rect"]
		var output_path := OUTPUT_DIR + "/" + String(crop_config["output"])
		var source_image := Image.load_from_file(source_path)
		if source_image == null:
			push_error("Failed to load source atlas: %s" % source_path)
			quit(1)
			return

		var output_size := crop_rect.size + Vector2i(PADDING * 2, PADDING * 2)
		var output_image := Image.create_empty(output_size.x, output_size.y, false, Image.FORMAT_RGBA8)
		output_image.fill(Color(0, 0, 0, 0))
		output_image.blit_rect(source_image, crop_rect, Vector2i(PADDING, PADDING))
		for erase_rect in crop_config.get("erase_rects", []):
			output_image.fill_rect(erase_rect, Color(0, 0, 0, 0))

		var save_error := output_image.save_png(ProjectSettings.globalize_path(output_path))
		if save_error != OK:
			push_error("Failed to save isolated sprite: %s" % output_path)
			quit(1)
			return

		print("%s -> %s rect=%s padded_size=%s" % [
			crop_config["id"],
			output_path,
			crop_rect,
			output_size,
		])

	quit(0)
