extends SceneTree

const OUTPUT_DIR := "res://assets/sprites/buildings/isolated"
const PADDING := 18

const CROPS := [
	{
		"id": "mercantile_shop",
		"source": "res://assets/buildings/hearthvale_buildings_atlas_v1.png",
		"rect": Rect2i(452, 67, 350, 403),
		"output": "mercantile_shop_isolated.png",
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
		"rect": Rect2i(452, 470, 360, 360),
		"output": "newport_shopfront_awning_isolated.png",
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
