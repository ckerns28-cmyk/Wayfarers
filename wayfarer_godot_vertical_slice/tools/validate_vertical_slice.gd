extends SceneTree

const MAIN_SCENE := preload("res://scenes/Main.tscn")
const NEWPORT_TOWN := preload("res://scripts/NewportTownBlueprint.gd")
const BUILDING_CATALOG := preload("res://scripts/BuildingCatalog.gd")
const BUILD_INFO := preload("res://scripts/BuildInfo.gd")

const G414A_PUBLIC_BUILDING_IDS := [
	"b_inn_tavern",
	"b_mercantile",
	"b_counting_house",
	"b_chandlery_front",
	"b_shop_house",
]

const G414A_PRIVATE_OR_FUTURE_HOME_IDS := [
	"b_res_small",
	"b_large_residence",
	"b_boarding_house",
	"b_clerk_townhouse",
	"b_dockworker_rowhouse",
]

const G414A_CURB_DATUM_BUILDING_IDS := [
	"b_inn_tavern",
	"b_clerk_townhouse",
	"b_mercantile",
	"b_counting_house",
	"b_chandlery_front",
	"b_shop_house",
	"b_market_shed",
	"b_printer_rowhouse",
]

var failures: Array[String] = []

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	var main := MAIN_SCENE.instantiate()
	root.add_child(main)
	await process_frame
	await physics_frame
	await process_frame

	_validate_scene(main)
	_print_report()
	quit(0 if failures.is_empty() else 1)

func _validate_scene(main: Node) -> void:
	var world := main.get_node_or_null("World") as Node2D
	var player := main.get_node_or_null("World/Player") as CharacterBody2D
	var hud := main.get_node_or_null("HUD") as CanvasLayer
	var map := main.get_node_or_null("World/TownMap") as Node2D

	_expect(BUILD_INFO.BUILD_PHASE == "G-4.18D.1", "build_phase_g_4_18d_1")
	_expect(BUILD_INFO.BUILD_LABEL == "Godot G-4.18D.1 Bakeoff Verdict Correction", "build_label_g_4_18d_1")
	_expect(BUILD_INFO.DEBUG_OVERLAYS_DEFAULT == false, "debug_overlays_default_off")
	_expect(BUILD_INFO.DEBUG_OVERLAY_TOGGLE_ENABLED == true, "debug_overlay_toggle_available")
	_expect(BUILD_INFO.REVIEW_SCREENSHOT_FLAG == "--review-no-hud", "review_screenshot_flag_declared")
	_expect(BUILD_INFO.GREEN_ORIGIN_LAB_FLAG == "--show-green-origin-lab", "green_origin_lab_flag_declared")
	_expect(world != null and world.y_sort_enabled, "world_y_sort_enabled")
	_expect(player != null, "player_exists")
	_expect(hud != null, "hud_exists")
	_expect(map != null, "map_exists")
	if not NEWPORT_TOWN.NPCS_ENABLED:
		_expect(main.get_node_or_null("World/EdrinVale") == null, "npcs_disabled_for_g_4_11")

	if player:
		_expect(player.get_node_or_null("Camera2D") != null, "player_camera_exists")
		_expect(root.get_camera_2d() == player.get_node("Camera2D"), "player_camera_is_current")
		_expect(player.get_node_or_null("CollisionShape2D") != null, "player_collision_exists")
		_expect(player.global_position.distance_to(NEWPORT_TOWN.PLAYER_SPAWN) < 1.0, "player_spawn_matches_blueprint")
		var camera := player.get_node_or_null("Camera2D") as Camera2D
		if camera:
			if NEWPORT_TOWN.G47_CALIBRATION_MODE:
				_expect(camera.zoom.x <= 1.0 and camera.zoom.y <= 1.0, "calibration_camera_shows_variants")
			else:
				_expect(camera.zoom.x >= 1.1 and camera.zoom.y >= 1.1, "spawn_camera_not_overview_zoom")
				_expect(camera.offset.length() > 20.0, "spawn_camera_intentional_offset")

	if map:
		for layer_name in ["GroundGrassLayer", "WharfWaterLayer", "RoadsPlazaLayer", "DecorativePropsLayer", "CollisionNavigationLayer"]:
			_expect(map.get_node_or_null(layer_name) != null, "map_layer_" + layer_name)
		_validate_g416_surface_kit(map)
		_validate_g418_asset_factory(map)
		_validate_g418c_green_origin_lab_quarantine(main, map, hud)
		var collision_layer := map.get_node_or_null("CollisionNavigationLayer")
		var minimum_collision_bodies := 3 if NEWPORT_TOWN.G47_CALIBRATION_MODE else (20 if (NEWPORT_TOWN.G46_PROOF_FRAME or NEWPORT_TOWN.G48_PROOF_STREET or NEWPORT_TOWN.G49_STREET_VIGNETTE) else 40)
		_expect(collision_layer != null and collision_layer.get_child_count() > minimum_collision_bodies, "collision_navigation_bodies")
		if collision_layer:
			_expect(not collision_layer.visible, "collision_probe_debug_layer_hidden_by_default")
			_expect(collision_layer.get("_debug_overlay_enabled") == false, "collision_probe_debug_flag_off_by_default")
			_validate_detail_blockers(collision_layer)

	_validate_buildings()
	_validate_review_screenshot_mode(main, hud)
	_validate_building_entity_contract(player, hud)
	_validate_g414a_street_wall_curb_datum()
	_validate_starter_harbor_plan()
	_validate_g415_layout_rules()
	_validate_proof_street(main)
	_validate_visual_composition_spacing()
	_validate_lived_in_details()
	_validate_reachability()
	_validate_building_walkability_gate()
	_validate_route_debug_probes()

func _validate_detail_blockers(collision_layer: Node) -> void:
	var detail_count := 0
	for child in collision_layer.get_children():
		if child.name.begins_with("DetailBlocker_"):
			detail_count += 1
	_expect(detail_count == NEWPORT_TOWN.detail_blockers().size(), "detail_blocker_count")
	for blocker in NEWPORT_TOWN.detail_blockers():
		var id := String(blocker.get("id", ""))
		var rect: Rect2 = blocker.get("rect", Rect2())
		if id == "mercantile_front_crates":
			_expect(rect.position.y >= 570.0, "mercantile_front_crates_clear_rear_lane_throat")
		elif id == "west_alley_rope":
			_expect(rect.position.x >= 560.0 and rect.position.y >= 570.0, "west_alley_rope_clear_rear_lane_throat")
		elif id == "support_lane_woodpile":
			_expect(rect.position.y >= 460.0, "support_lane_woodpile_clear_rear_lane_road")

func _validate_g416_surface_kit(map: Node) -> void:
	if not NEWPORT_TOWN.G410_STARTER_HARBOR_TOWN:
		return

	for layer_name in ["GroundGrassLayer", "WharfWaterLayer", "RoadsPlazaLayer", "DecorativePropsLayer"]:
		var layer := map.get_node_or_null(layer_name)
		_expect(layer != null and layer.has_method("newport_surface_kit_version"), "g416_surface_kit_api_" + layer_name)
		if layer and layer.has_method("newport_surface_kit_version"):
			_expect(String(layer.call("newport_surface_kit_version")) == "G-4.16", "g416_surface_kit_version_" + layer_name)

	var ground_layer := map.get_node_or_null("GroundGrassLayer")
	if ground_layer and ground_layer.has_method("newport_surface_kit_materials"):
		var materials: Array = ground_layer.call("newport_surface_kit_materials")
		for material in ["commercial_street", "curb_sidewalk", "dirt_path", "grass_road_transition", "dock_plank", "pier_edge", "building_base_shadow", "service_lane"]:
			_expect(materials.has(material), "g416_surface_kit_material_" + material)
	else:
		failures.append("g416_surface_kit_material_manifest")

func _validate_g418_asset_factory(map: Node) -> void:
	if not NEWPORT_TOWN.G410_STARTER_HARBOR_TOWN:
		return

	for dir_path in [
		"res://art_pipeline/newport/source_refs",
		"res://art_pipeline/newport/blender",
		"res://art_pipeline/newport/generated_assets",
		"res://art_pipeline/newport/generated_contact_sheets",
		"res://art_pipeline/newport/manifests",
		"res://art_pipeline/newport/atlases",
		"res://art_pipeline/newport/reports",
		"res://art_pipeline/newport/scripts",
		"res://art_pipeline/newport_green_origin/source_authored",
		"res://art_pipeline/newport_green_origin/generated",
		"res://art_pipeline/newport_green_origin/method_bakeoff",
		"res://art_pipeline/newport_green_origin/contact_sheets",
		"res://art_pipeline/newport_green_origin/atlases",
		"res://art_pipeline/newport_green_origin/manifests",
		"res://art_pipeline/newport_green_origin/reports",
		"res://art_pipeline/newport_green_origin/scripts",
	]:
		_expect(DirAccess.dir_exists_absolute(dir_path), "g418_pipeline_dir_" + dir_path.get_file())

	for file_path in [
		"res://art_pipeline/newport/scripts/extract_building_style_refs.py",
		"res://art_pipeline/newport/scripts/generate_hero_street_atlas.py",
		"res://art_pipeline/newport/scripts/generate_newport_asset_factory.py",
		"res://art_pipeline/newport/scripts/validate_newport_asset_provenance.py",
		"res://art_pipeline/newport/blender/render_newport_components.py",
		"res://art_pipeline/newport/reports/newport_building_style_reference.md",
		"res://art_pipeline/newport/reports/G417_G418_ASSET_PROVENANCE_AUDIT.md",
		"res://art_pipeline/newport/generated_contact_sheets/newport_building_palette_contact_sheet.png",
		"res://art_pipeline/newport/generated_contact_sheets/newport_hero_street_atlas_contact_sheet.png",
		"res://art_pipeline/newport/generated_contact_sheets/newport_g418_provenance_safe_hero_asset_proof.png",
		"res://art_pipeline/newport/manifests/newport_building_style_values.json",
		"res://art_pipeline/newport/manifests/newport_asset_manifest.schema.json",
		"res://art_pipeline/newport/manifests/newport_asset_manifest.json",
		"res://art_pipeline/newport/manifests/newport_hero_street_assets.json",
		"res://art_pipeline/newport/atlases/newport_hero_street_atlas_v1.png",
		"res://art_pipeline/newport_green_origin/source_authored/newport_green_origin_style_tokens.json",
		"res://art_pipeline/newport_green_origin/scripts/generate_green_origin_assets.py",
		"res://art_pipeline/newport_green_origin/scripts/generate_green_origin_method_bakeoff.py",
		"res://art_pipeline/newport_green_origin/scripts/validate_green_origin_assets.py",
		"res://art_pipeline/newport_green_origin/manifests/green_origin_asset_manifest.json",
		"res://art_pipeline/newport_green_origin/manifests/green_origin_method_bakeoff_manifest.json",
		"res://art_pipeline/newport_green_origin/atlases/newport_green_origin_dock_factory_v1.png",
		"res://art_pipeline/newport_green_origin/contact_sheets/green_origin_asset_contact_sheet.png",
		"res://art_pipeline/newport_green_origin/contact_sheets/green_origin_palette_shadow_sheet.png",
		"res://art_pipeline/newport_green_origin/contact_sheets/g418d_method_bakeoff_board.png",
		"res://art_pipeline/newport_green_origin/contact_sheets/g418d_candidate_comparison_strip.png",
		"res://art_pipeline/newport_green_origin/contact_sheets/g418d1_corrected_bakeoff_board.png",
		"res://art_pipeline/newport_green_origin/contact_sheets/g418d1_candidate_comparison_strip.png",
		"res://art_pipeline/newport_green_origin/contact_sheets/g418d1_m01b_isolated_proof.png",
		"res://art_pipeline/newport_green_origin/contact_sheets/g418d1_m01b_in_world_comparison_frame.png",
		"res://art_pipeline/newport_green_origin/reports/G418B_GREEN_ORIGIN_ASSET_FACTORY.md",
		"res://art_pipeline/newport_green_origin/reports/G418C_GREEN_ORIGIN_VISUAL_RETROSPECTIVE.md",
		"res://art_pipeline/newport_green_origin/reports/G418D_GREEN_ORIGIN_METHOD_BAKEOFF.md",
		"res://art_pipeline/newport_green_origin/reports/G418D1_BAKEOFF_VERDICT_CORRECTION_MANUAL_PAINTOVER.md",
		"res://tools/capture_g418c_review_screenshots.mjs",
		"res://tools/capture_g418d_review_screenshots.mjs",
	]:
		_expect(FileAccess.file_exists(file_path), "g418_pipeline_file_" + file_path.get_file())

	for layer_name in ["GroundGrassLayer", "WharfWaterLayer", "RoadsPlazaLayer", "DecorativePropsLayer"]:
		var layer := map.get_node_or_null(layer_name)
		_expect(layer != null and layer.has_method("newport_hero_atlas_version"), "g418_hero_atlas_api_" + layer_name)
		if layer and layer.has_method("newport_hero_atlas_version"):
			_expect(String(layer.call("newport_hero_atlas_version")) == "G-4.18", "g418_hero_atlas_version_" + layer_name)
		if layer and layer.has_method("newport_hero_atlas_materials"):
			var materials: Array = layer.call("newport_hero_atlas_materials")
			for material in ["commercial_cobble_long_a", "commercial_cobble_patch_b", "commercial_cobble_patch_c", "curb_sidewalk_stoop_strip", "curb_sidewalk_broken_edge", "building_contact_shadow_strip", "dirt_wear_transition", "grass_edge_north", "grass_cobble_feather", "dock_market_transition", "dock_pier_vertical", "dock_edge_feather", "pier_shadow_post_strip", "crate_barrel_table_cluster", "fence_sign_market_cluster", "small_crate_barrel_cluster", "market_sign_cluster", "wharf_crate_pile_cluster", "chandlery_base_cluster"]:
				_expect(materials.has(material), "g418_hero_atlas_material_" + material + "_" + layer_name)
		_expect(layer != null and layer.has_method("newport_green_origin_version"), "g418b_green_origin_api_" + layer_name)
		if layer and layer.has_method("newport_green_origin_version"):
			_expect(String(layer.call("newport_green_origin_version")) == "G-4.18B", "g418b_green_origin_version_" + layer_name)
		if layer and layer.has_method("newport_green_origin_materials"):
			var green_materials: Array = layer.call("newport_green_origin_materials")
			for material in ["green_dock_plank_strip", "green_dock_plank_patch", "green_dock_edge_shadow", "green_pier_post_pair", "green_rope_coil_small", "green_plank_contact_shadow"]:
				_expect(green_materials.has(material), "g418b_green_origin_material_" + material + "_" + layer_name)

	var manifest := _load_json_dictionary("res://art_pipeline/newport/manifests/newport_asset_manifest.json")
	_expect(not manifest.is_empty(), "g418_asset_manifest_json")
	_expect(String(manifest.get("schema_id", "")) == "wayfarer.newport.asset_manifest.v2", "g418_asset_manifest_schema")
	_expect(String(manifest.get("phase", "")) == "G-4.18-temporary-yellow", "g418_asset_manifest_phase_temporary_yellow")
	_expect(String(manifest.get("source_policy", "")).find("Temporary yellow review art") >= 0 and String(manifest.get("source_policy", "")).find("green-origin assets") >= 0, "g418_asset_manifest_yellow_green_gate")
	var legacy_manifest := _load_json_dictionary("res://art_pipeline/newport/manifests/newport_hero_street_assets.json")
	_expect(not legacy_manifest.is_empty(), "g418_legacy_asset_manifest_json")
	if not manifest.is_empty() and not legacy_manifest.is_empty():
		_expect(JSON.stringify(manifest.get("assets", [])) == JSON.stringify(legacy_manifest.get("assets", [])), "g418_legacy_manifest_mirrors_assets")
	var assets: Array = manifest.get("assets", [])
	_expect(assets.size() >= 16, "g418_asset_manifest_asset_count")
	var review_ready_assets := 0
	for raw_asset in assets:
		if not raw_asset is Dictionary:
			failures.append("g418_asset_manifest_asset_not_dictionary")
			continue
		var asset: Dictionary = raw_asset
		for key in ["asset_id", "material_category", "source_file", "generated_piece_file", "atlas_region", "intended_scale", "collision_behavior", "y_sort_behavior", "contact_shadow_required", "visual_cohesion_status", "visual_quality_status", "provenance_status", "placeholder", "final", "review_eligible", "normal_review_eligible", "lab_only", "license_ownership_status", "source_pixels_from_project_owned_wayfarer_assets", "source_pixels_from_third_party_material", "origin_classification", "commercial_use_status", "final_commercial_candidate", "final_commercial_eligible", "source_pixels_from_yellow_uncertain_assets"]:
			_expect(asset.has(key), "g418_asset_manifest_field_" + String(asset.get("asset_id", "unknown")) + "_" + key)
		if bool(asset.get("review_eligible", false)) and not bool(asset.get("placeholder", true)):
			review_ready_assets += 1
			_expect(String(asset.get("visual_cohesion_status", "")) == "g418_review_candidate", "g418_review_asset_visual_status_" + String(asset.get("asset_id", "unknown")))
			_expect(String(asset.get("visual_quality_status", "")) == "temporary_review_visual_accepted", "g418_review_asset_visual_quality_" + String(asset.get("asset_id", "unknown")))
			_expect(String(asset.get("provenance_status", "")) == "temporary_review_yellow", "g418_review_asset_provenance_status_" + String(asset.get("asset_id", "unknown")))
			_expect(String(asset.get("origin_classification", "")) == "temporary_review_yellow", "g418_review_asset_origin_classification_" + String(asset.get("asset_id", "unknown")))
			_expect(String(asset.get("commercial_use_status", "")) == "temporary_review_yellow", "g418_review_asset_commercial_status_" + String(asset.get("asset_id", "unknown")))
			_expect(bool(asset.get("normal_review_eligible", false)) == true, "g418_review_asset_normal_review_eligible_" + String(asset.get("asset_id", "unknown")))
			_expect(bool(asset.get("lab_only", true)) == false, "g418_review_asset_not_lab_only_" + String(asset.get("asset_id", "unknown")))
			_expect(bool(asset.get("final_commercial_candidate", true)) == false, "g418_review_asset_not_final_commercial_" + String(asset.get("asset_id", "unknown")))
			_expect(bool(asset.get("final_commercial_eligible", true)) == false, "g418_review_asset_final_commercial_blocked_" + String(asset.get("asset_id", "unknown")))
			_expect(bool(asset.get("source_pixels_from_yellow_uncertain_assets", false)) == true, "g418_review_asset_yellow_source_declared_" + String(asset.get("asset_id", "unknown")))
			_expect(bool(asset.get("contact_shadow_required", false)), "g418_review_asset_contact_shadow_" + String(asset.get("asset_id", "unknown")))
			_expect(bool(asset.get("source_pixels_from_third_party_material", true)) == false, "g418_review_asset_no_third_party_source_pixels_" + String(asset.get("asset_id", "unknown")))
		var source: Dictionary = asset.get("source", {})
		_expect(String(source.get("ownership", "")).find("project-owned") >= 0, "g418_asset_source_owned_" + String(asset.get("asset_id", "unknown")))
		_expect(String(source.get("license", "")).to_lower().find("no third-party") >= 0, "g418_asset_source_license_no_third_party_" + String(asset.get("asset_id", "unknown")))
		_expect(String(source.get("license", "")).to_lower().find("prior prop-sheet") >= 0, "g418_asset_source_license_no_prior_prop_sheet_" + String(asset.get("asset_id", "unknown")))
		_expect(String(source.get("license", "")).to_lower().find("temporary yellow review") >= 0, "g418_asset_source_license_temporary_yellow_" + String(asset.get("asset_id", "unknown")))
		_expect(source.has("material_sources"), "g418_asset_source_material_refs_" + String(asset.get("asset_id", "unknown")))
		_expect(source.has("blender_component_sources"), "g418_asset_source_blender_refs_" + String(asset.get("asset_id", "unknown")))
		_expect(source.has("prior_project_prop_sources") and source.get("prior_project_prop_sources", []) == [], "g418_asset_source_prior_prop_refs_empty_" + String(asset.get("asset_id", "unknown")))
		_expect(bool(source.get("source_pixels_from_third_party_material", true)) == false, "g418_asset_source_no_third_party_pixels_" + String(asset.get("asset_id", "unknown")))
		_expect(bool(source.get("web_scraped_source_pixels", true)) == false, "g418_asset_source_no_web_scraped_pixels_" + String(asset.get("asset_id", "unknown")))
		_expect(bool(source.get("source_pixels_from_yellow_uncertain_assets", false)) == true, "g418_asset_source_yellow_influence_declared_" + String(asset.get("asset_id", "unknown")))
		_expect(bool(source.get("green_origin_candidate", true)) == false, "g418_asset_source_not_green_origin_" + String(asset.get("asset_id", "unknown")))
		for raw_crop in source.get("material_sources", []):
			if raw_crop is Dictionary:
				var crop: Dictionary = raw_crop
				_expect(String(crop.get("ownership", "")).find("project-owned") >= 0, "g418_asset_crop_owned_" + String(asset.get("asset_id", "unknown")) + "_" + String(crop.get("source_crop_id", "unknown")))
				_expect(bool(crop.get("third_party_pixels", true)) == false, "g418_asset_crop_no_third_party_" + String(asset.get("asset_id", "unknown")) + "_" + String(crop.get("source_crop_id", "unknown")))
	_expect(review_ready_assets >= 16, "g418_asset_manifest_review_ready_assets")
	_validate_g418b_green_origin_manifest()
	_validate_g418d_green_origin_bakeoff_manifest()

func _validate_g418b_green_origin_manifest() -> void:
	var manifest := _load_json_dictionary("res://art_pipeline/newport_green_origin/manifests/green_origin_asset_manifest.json")
	_expect(not manifest.is_empty(), "g418b_green_origin_manifest_json")
	_expect(String(manifest.get("schema_id", "")) == "wayfarer.newport_green_origin.asset_manifest.v1", "g418b_green_origin_manifest_schema")
	_expect(String(manifest.get("phase", "")) == "G-4.18B", "g418b_green_origin_manifest_phase")
	var taxonomy: Array = manifest.get("origin_taxonomy", [])
	for status in ["temporary_review_yellow", "green_origin_candidate", "final_commercial_green", "red_unsafe"]:
		_expect(taxonomy.has(status), "g418b_origin_taxonomy_" + status)
	var assets: Array = manifest.get("assets", [])
	_expect(assets.size() >= 4, "g418b_green_origin_asset_family_count")
	for raw_asset in assets:
		if not raw_asset is Dictionary:
			failures.append("g418b_green_origin_asset_not_dictionary")
			continue
		var asset: Dictionary = raw_asset
		var asset_id := String(asset.get("asset_id", "unknown"))
		for key in ["asset_id", "asset_type", "source_type", "generation_script", "input_sources", "license", "ownership", "commercial_use_status", "provenance_status", "origin_classification", "visual_quality_status", "review_eligible", "normal_review_eligible", "lab_only", "final_commercial_candidate", "final_commercial_eligible", "notes"]:
			_expect(asset.has(key), "g418b_green_origin_field_" + asset_id + "_" + key)
		_expect(String(asset.get("source_type", "")) == "deterministic_python_pillow", "g418b_green_origin_source_type_" + asset_id)
		_expect(String(asset.get("ownership", "")) == "project-owned", "g418b_green_origin_owned_" + asset_id)
		_expect(String(asset.get("commercial_use_status", "")) == "green_origin_candidate" or String(asset.get("commercial_use_status", "")) == "final_commercial_green", "g418b_green_origin_status_" + asset_id)
		_expect(String(asset.get("provenance_status", "")) == "green_origin_candidate", "g418b_green_origin_provenance_" + asset_id)
		_expect(String(asset.get("origin_classification", "")) == "green_origin_candidate", "g418b_green_origin_classification_" + asset_id)
		_expect(String(asset.get("visual_quality_status", "")) == "visual_failed_g418b_proof", "g418c_green_origin_visual_failed_" + asset_id)
		_expect(bool(asset.get("review_eligible", true)) == false, "g418c_green_origin_review_ineligible_" + asset_id)
		_expect(bool(asset.get("normal_review_eligible", true)) == false, "g418c_green_origin_normal_review_ineligible_" + asset_id)
		_expect(bool(asset.get("lab_only", false)) == true, "g418c_green_origin_lab_only_" + asset_id)
		_expect(bool(asset.get("final_commercial_candidate", true)) == false, "g418c_green_origin_not_final_candidate_" + asset_id)
		_expect(bool(asset.get("final_commercial_eligible", true)) == false, "g418c_green_origin_not_final_eligible_" + asset_id)
		_expect(bool(asset.get("source_pixels_from_yellow_uncertain_assets", true)) == false, "g418b_green_origin_no_yellow_pixels_" + asset_id)
		_expect(bool(asset.get("source_pixels_from_third_party_material", true)) == false, "g418b_green_origin_no_third_party_pixels_" + asset_id)
		_expect(bool(asset.get("web_scraped_source_pixels", true)) == false, "g418b_green_origin_no_web_pixels_" + asset_id)
		for raw_source in asset.get("input_sources", []):
			if raw_source is Dictionary:
				var source: Dictionary = raw_source
				var source_text := JSON.stringify(source).to_lower()
				for forbidden in ["assets/sprites/buildings/isolated", "assets/buildings", "hearthvale", "yellow", "uncertain", "marketplace", "web-scraped", "ripped"]:
					_expect(source_text.find(forbidden) < 0, "g418b_green_origin_input_not_" + forbidden.replace("/", "_").replace("-", "_") + "_" + asset_id)
				_expect(bool(source.get("source_pixels_used", true)) == false, "g418b_green_origin_input_no_source_pixels_" + asset_id)

func _validate_g418d_green_origin_bakeoff_manifest() -> void:
	var manifest := _load_json_dictionary("res://art_pipeline/newport_green_origin/manifests/green_origin_method_bakeoff_manifest.json")
	_expect(not manifest.is_empty(), "g418d_bakeoff_manifest_json")
	_expect(String(manifest.get("schema_id", "")) == "wayfarer.newport_green_origin.method_bakeoff.v1", "g418d_bakeoff_manifest_schema")
	_expect(String(manifest.get("phase", "")) == "G-4.18D.1", "g418d1_bakeoff_manifest_phase")
	_expect(manifest.has("recommended_method_for_g418e") and manifest.get("recommended_method_for_g418e") == null, "g418d1_bakeoff_no_recommendation")
	_expect(String(manifest.get("normal_review_policy", "")).find("No G-4.18D or G-4.18D.1 bakeoff candidate is normal-review eligible") >= 0, "g418d1_bakeoff_normal_review_blocked")
	_expect(String(manifest.get("visual_quality_gate", "")).find("8.5") >= 0, "g418d1_visual_pass_gate_8_5")
	var candidates: Array = manifest.get("candidates", [])
	_expect(candidates.size() == 6, "g418d1_bakeoff_candidate_count")
	var pass_count := 0
	for raw_candidate in candidates:
		if not raw_candidate is Dictionary:
			failures.append("g418d_bakeoff_candidate_not_dictionary")
			continue
		var candidate: Dictionary = raw_candidate
		var candidate_id := String(candidate.get("candidate_id", "unknown"))
		for key in ["candidate_id", "method_name", "sample_path", "provenance_status", "origin_classification", "visual_quality_status", "visual_rating", "visual_pass_gate", "review_eligible", "normal_review_eligible", "lab_only", "final_commercial_candidate", "final_commercial_eligible", "recommendation", "input_sources", "source_pixels_from_yellow_uncertain_assets", "source_pixels_from_third_party_material", "web_scraped_source_pixels"]:
			_expect(candidate.has(key), "g418d_bakeoff_field_" + candidate_id + "_" + key)
		_expect(FileAccess.file_exists("res://" + String(candidate.get("sample_path", ""))), "g418d_bakeoff_sample_" + candidate_id)
		_expect(String(candidate.get("provenance_status", "")) == "green_origin_candidate", "g418d_bakeoff_provenance_" + candidate_id)
		_expect(String(candidate.get("origin_classification", "")) == "green_origin_candidate", "g418d_bakeoff_origin_" + candidate_id)
		_expect(bool(candidate.get("review_eligible", true)) == false, "g418d_bakeoff_review_blocked_" + candidate_id)
		_expect(bool(candidate.get("normal_review_eligible", true)) == false, "g418d_bakeoff_normal_review_blocked_" + candidate_id)
		_expect(bool(candidate.get("lab_only", false)) == true, "g418d_bakeoff_lab_only_" + candidate_id)
		_expect(bool(candidate.get("final_commercial_eligible", true)) == false, "g418d_bakeoff_not_final_eligible_" + candidate_id)
		_expect(bool(candidate.get("source_pixels_from_yellow_uncertain_assets", true)) == false, "g418d_bakeoff_no_yellow_pixels_" + candidate_id)
		_expect(bool(candidate.get("source_pixels_from_third_party_material", true)) == false, "g418d_bakeoff_no_third_party_pixels_" + candidate_id)
		_expect(bool(candidate.get("web_scraped_source_pixels", true)) == false, "g418d_bakeoff_no_web_pixels_" + candidate_id)
		if String(candidate.get("recommendation", "")) == "PASS":
			pass_count += 1
			_expect(float(candidate.get("visual_rating", 0.0)) >= 8.5, "g418d1_pass_requires_8_5_" + candidate_id)
		else:
			_expect(float(candidate.get("visual_rating", 0.0)) < 8.5, "g418d1_non_pass_below_gate_" + candidate_id)
			_expect(bool(candidate.get("final_commercial_candidate", true)) == false, "g418d1_non_pass_not_final_candidate_" + candidate_id)
	_expect(pass_count == 0, "g418d1_bakeoff_zero_pass")

func _validate_g418c_green_origin_lab_quarantine(main: Node, map: Node, hud: CanvasLayer) -> void:
	_expect(main.has_method("set_green_origin_lab_mode"), "g418c_lab_main_set_api")
	_expect(main.has_method("is_green_origin_lab_mode"), "g418c_lab_main_query_api")
	_expect(hud != null and hud.has_method("set_green_origin_lab_mode"), "g418c_lab_hud_api")

	var lab_capable_layers := 0
	for layer_name in ["GroundGrassLayer", "WharfWaterLayer", "RoadsPlazaLayer", "DecorativePropsLayer"]:
		var layer := map.get_node_or_null(layer_name)
		_expect(layer != null and layer.has_method("set_green_origin_lab_mode"), "g418c_lab_layer_set_api_" + layer_name)
		_expect(layer != null and layer.has_method("is_green_origin_lab_mode"), "g418c_lab_layer_query_api_" + layer_name)
		if layer and layer.has_method("is_green_origin_lab_mode"):
			lab_capable_layers += 1
			_expect(not bool(layer.call("is_green_origin_lab_mode")), "g418c_lab_layer_default_off_" + layer_name)
	_expect(lab_capable_layers == 4, "g418c_lab_all_map_layers_capable")
	_expect(not bool(main.call("is_green_origin_lab_mode")), "g418c_lab_default_off_main")
	if main.has_method("set_green_origin_lab_mode"):
		main.call("set_green_origin_lab_mode", true)
		_expect(bool(main.call("is_green_origin_lab_mode")), "g418c_lab_can_enable_main")
		var wharf := map.get_node_or_null("WharfWaterLayer")
		_expect(wharf != null and bool(wharf.call("is_green_origin_lab_mode")), "g418c_lab_enables_wharf_layer")
		var bakeoff_panel := hud.get_node_or_null("BakeoffPanel") if hud else null
		_expect(bakeoff_panel != null and bakeoff_panel.visible, "g418d_lab_bakeoff_panel_visible")
		var bakeoff_board := hud.get_node_or_null("BakeoffPanel/MarginContainer/BakeoffBoard") if hud else null
		_expect(bakeoff_board != null and bakeoff_board.get("texture") != null, "g418d_lab_bakeoff_board_texture")
		main.call("set_green_origin_lab_mode", false)
		_expect(not bool(main.call("is_green_origin_lab_mode")), "g418c_lab_can_disable_main")
		_expect(bakeoff_panel == null or not bakeoff_panel.visible, "g418d_lab_bakeoff_panel_hidden_after_disable")

func _load_json_dictionary(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		return {}
	var parsed = JSON.parse_string(FileAccess.get_file_as_string(path))
	if parsed is Dictionary:
		return parsed
	return {}

func _validate_review_screenshot_mode(main: Node, hud: CanvasLayer) -> void:
	_expect(main.has_method("set_review_screenshot_mode"), "review_screenshot_mode_main_api")
	_expect(main.has_method("is_review_screenshot_mode"), "review_screenshot_mode_query_api")
	_expect(hud != null and hud.has_method("set_review_screenshot_mode"), "review_screenshot_mode_hud_api")
	if not main.has_method("set_review_screenshot_mode") or hud == null:
		return

	var status_panel := hud.get_node_or_null("Panel") as Control
	var dialogue_panel := hud.get_node_or_null("DialoguePanel") as Control
	main.call("set_review_screenshot_mode", true)
	_expect(bool(main.call("is_review_screenshot_mode")), "review_screenshot_mode_enabled")
	_expect(status_panel == null or not status_panel.visible, "review_screenshot_mode_hides_status_panel")
	_expect(dialogue_panel == null or not dialogue_panel.visible, "review_screenshot_mode_hides_dialogue_panel")
	main.call("set_review_screenshot_mode", false)
	_expect(not bool(main.call("is_review_screenshot_mode")), "review_screenshot_mode_disabled")
	_expect(status_panel == null or status_panel.visible, "review_screenshot_mode_restores_status_panel")

func _validate_lived_in_details() -> void:
	var minimum_detail_count := 150 if NEWPORT_TOWN.G410_STARTER_HARBOR_TOWN else (20 if NEWPORT_TOWN.G47_CALIBRATION_MODE else (24 if NEWPORT_TOWN.G49_STREET_VIGNETTE else (20 if NEWPORT_TOWN.G48_PROOF_STREET else (8 if NEWPORT_TOWN.G46_PROOF_FRAME else 40))))
	_expect(NEWPORT_TOWN.lived_in_detail_count() >= minimum_detail_count, "lived_in_detail_density")

func _validate_buildings() -> void:
	var buildings := get_nodes_in_group("buildings")
	var expected_ids: Array = NEWPORT_TOWN.BUILDING_IDS
	_expect(buildings.size() == expected_ids.size(), "newport_building_count")

	var seen := {}
	var district_counts := {}
	for raw_building in buildings:
		var building := raw_building as Node2D
		if building == null:
			failures.append("building_is_not_node2d")
			continue
		_expect(not seen.has(building.name), "unique_building_id_" + building.name)
		seen[building.name] = true
		_validate_building_node(building)

	for config in NEWPORT_TOWN.building_specs():
		var id: String = config["id"]
		var district: String = config["district"]
		district_counts[district] = district_counts.get(district, 0) + 1
		_expect(seen.has(id), "building_present_" + id)

	var expected_districts := ["harborfront_commercial", "working_wharf", "inland_residential_civic", "support_lane"] if NEWPORT_TOWN.G410_STARTER_HARBOR_TOWN else (["visual_calibration"] if NEWPORT_TOWN.G47_CALIBRATION_MODE else (["waterfront_commercial"] if (NEWPORT_TOWN.G46_PROOF_FRAME or NEWPORT_TOWN.G48_PROOF_STREET or NEWPORT_TOWN.G49_STREET_VIGNETTE) else ["harbor_wharf", "waterfront_commercial", "civic_district", "upper_residential_terrace", "service_outfitter_lane"]))
	for district_id in expected_districts:
		_expect(district_counts.get(district_id, 0) > 0, "district_has_building_" + district_id)

func _validate_building_entity_contract(player: Node, hud: CanvasLayer) -> void:
	var public_runtime_count := 0
	var interactable_names := {}
	for raw_interactable in get_nodes_in_group("interactable"):
		var interactable := raw_interactable as Node
		if interactable:
			interactable_names[String(interactable.name)] = true

	for config in NEWPORT_TOWN.building_specs():
		var id: String = config["id"]
		_expect(config.has("definition_id"), id + "_entity_has_definition_id")
		if not config.has("definition_id"):
			continue

		var definition := BUILDING_CATALOG.building_definition(String(config["definition_id"]))
		_validate_building_definition_entity_metadata(id, definition)

		var runtime_building := _building_by_name(id)
		_expect(runtime_building != null, id + "_entity_runtime_node")
		if runtime_building == null:
			continue

		for method in ["get_interaction_label", "get_interaction_position", "get_prompt_text", "is_player_in_interaction_area", "interact", "can_player_enter", "get_door_anchor_local", "get_ground_contact_rect", "get_y_sort_anchor_local", "set_debug_label_detail"]:
			_expect(runtime_building.has_method(method), id + "_entity_method_" + method)

		if bool(definition.get("is_enterable", false)) or bool(definition.get("interaction_enabled", false)):
			_expect(interactable_names.has(id), id + "_entity_in_interactable_group")

		if runtime_building.has_method("get_interaction_position"):
			var door_marker := runtime_building.get_node_or_null("DoorMarker") as Marker2D
			var interaction_position: Vector2 = runtime_building.get_interaction_position()
			_expect(door_marker != null and interaction_position.distance_to(door_marker.global_position) <= 1.0, id + "_entity_interaction_position_uses_door")
			if door_marker and runtime_building.has_method("get_door_anchor_local"):
				var door_anchor_local: Vector2 = runtime_building.get_door_anchor_local()
				_expect(door_anchor_local.distance_to(door_marker.position) <= 1.0, id + "_entity_door_anchor_matches_marker")
			if runtime_building.has_method("is_player_in_interaction_area"):
				_expect(bool(runtime_building.call("is_player_in_interaction_area", interaction_position)), id + "_entity_door_anchor_inside_interaction_area")
				_expect(not bool(runtime_building.call("is_player_in_interaction_area", interaction_position + Vector2(0.0, 72.0))), id + "_entity_interaction_not_middle_of_street")
			if runtime_building.has_method("get_ground_contact_rect"):
				var ground_contact: Rect2 = runtime_building.get_ground_contact_rect()
				_expect(ground_contact.size.x > 0.0 and ground_contact.size.y > 0.0 and absf(ground_contact.get_center().y) <= 4.0, id + "_entity_ground_contact_at_base")

		if G414A_PUBLIC_BUILDING_IDS.has(id):
			public_runtime_count += 1
			_expect(runtime_building.has_method("can_player_enter") and runtime_building.can_player_enter(), id + "_public_building_can_enter_future_stub")
			if runtime_building.has_method("get_interaction_label"):
				_expect(String(runtime_building.get_interaction_label()).begins_with("Press E to enter "), id + "_public_building_enter_prompt")
			if runtime_building.has_method("interact"):
				var message := String(runtime_building.interact())
				_expect(message.find("G-4.15") >= 0, id + "_public_building_stub_mentions_g_4_15")
		elif G414A_PRIVATE_OR_FUTURE_HOME_IDS.has(id):
			_expect(runtime_building.has_method("can_player_enter") and not runtime_building.can_player_enter(), id + "_private_building_cannot_enter")
			if runtime_building.has_method("interact"):
				var private_message := String(runtime_building.interact())
				_expect(private_message.find("private") >= 0 or private_message.find("future ownership") >= 0, id + "_private_building_stub_message")

	_expect(public_runtime_count >= 5, "g414a_public_door_stub_count")
	_validate_g414b_minimum_conversion_scope()
	if player:
		_expect(player.has_signal("dialogue_triggered"), "player_dialogue_signal_for_building_interaction")
		_validate_player_uses_building_door_target(player)
		if hud and player is Node2D:
			_validate_player_interaction_message(player as Node2D, hud, "b_counting_house", "Counting House", "G-4.15", "player_public_counting_house_hud_stub")
			_validate_player_interaction_message(player as Node2D, hud, "b_res_small", "Harbor Cottage", "private", "player_private_harbor_cottage_hud_stub")

func _validate_g414b_minimum_conversion_scope() -> void:
	var scoped_buildings := {
		"b_counting_house": "civic",
		"b_large_residence": "large_residence",
		"b_mercantile": "shopfront",
		"b_dock_storehouse": "warehouse",
	}
	for id in scoped_buildings.keys():
		var building := _building_by_name(id)
		_expect(building != null, "g414b_scope_" + id + "_present")
		if building == null:
			continue
		_expect(building.has_method("uses_normalized_definition") and building.uses_normalized_definition(), "g414b_scope_" + id + "_normalized_entity")
		_expect(building.has_method("has_seating_metadata") and building.has_seating_metadata(), "g414b_scope_" + id + "_grounding_metadata")
		_expect(building.get_node_or_null("DebugOverlay") != null, "g414b_scope_" + id + "_debug_overlay")

func _validate_player_uses_building_door_target(player: Node) -> void:
	var mercantile := _building_by_name("b_mercantile")
	if mercantile == null or not mercantile.has_method("get_interaction_position"):
		failures.append("player_door_targeting_missing_mercantile")
		return
	if not player is Node2D:
		failures.append("player_door_targeting_player_not_node2d")
		return

	var player_node := player as Node2D
	var original_position := player_node.global_position
	player_node.global_position = mercantile.get_interaction_position()
	if player.has_method("_update_interaction_target"):
		player.call("_update_interaction_target")
	else:
		failures.append("player_door_targeting_update_method")

	var prompt_label := player.get_node_or_null("PromptLabel") as Label
	_expect(prompt_label != null and prompt_label.visible, "player_door_targeting_prompt_visible")
	if prompt_label:
		_expect(prompt_label.text.find("Harbor Mercantile") >= 0, "player_door_targeting_prompt_identifies_building")
		_expect(prompt_label.text.length() <= 28, "player_door_targeting_prompt_less_intrusive")
		_expect(prompt_label.get_theme_font_size("font_size") <= 16, "player_door_targeting_prompt_font_smaller")
		_expect((prompt_label.offset_right - prompt_label.offset_left) <= 200.0, "player_door_targeting_prompt_width_controlled")
	if mercantile.has_method("interact"):
		_expect(String(mercantile.interact()) == "Harbor Mercantile will be enterable in G-4.15.", "player_door_targeting_interact_stub")
	player_node.global_position = mercantile.get_interaction_position() + Vector2(0.0, 72.0)
	if player.has_method("_update_interaction_target"):
		player.call("_update_interaction_target")
	if prompt_label:
		_expect(not prompt_label.visible, "player_door_targeting_no_prompt_from_street")
	player_node.global_position = original_position

func _validate_player_interaction_message(player: Node2D, hud: CanvasLayer, building_id: String, expected_prompt_fragment: String, expected_message_fragment: String, label: String) -> void:
	var building := _building_by_name(building_id)
	if building == null or not building.has_method("get_interaction_position"):
		failures.append(label + "_building_missing")
		return

	var prompt_label := player.get_node_or_null("PromptLabel") as Label
	var dialogue_label := hud.get_node_or_null("DialoguePanel/MarginContainer/DialogueLabel") as Label
	var dialogue_panel := hud.get_node_or_null("DialoguePanel") as PanelContainer
	var original_position := player.global_position

	if dialogue_label:
		dialogue_label.text = ""
	if dialogue_panel:
		dialogue_panel.visible = false

	player.global_position = building.get_interaction_position()
	if player.has_method("_update_interaction_target"):
		player.call("_update_interaction_target")
	_expect(prompt_label != null and prompt_label.visible, label + "_prompt_visible")
	if prompt_label:
		_expect(prompt_label.text.find(expected_prompt_fragment) >= 0, label + "_prompt_identifies_building")

	if building.has_method("interact") and player.has_signal("dialogue_triggered"):
		player.emit_signal("dialogue_triggered", building.interact())

	var message := String(dialogue_label.text) if dialogue_label else ""
	_expect(dialogue_panel != null and dialogue_panel.visible, label + "_dialogue_panel_visible")
	_expect(message.find(expected_message_fragment) >= 0, label + "_dialogue_message")
	player.global_position = original_position

func _validate_building_definition_entity_metadata(id: String, definition: Dictionary) -> void:
	for key in ["building_type", "access_rule", "interior_scene", "owner_id", "is_enterable", "interaction_label", "locked_message", "unavailable_message", "collision_footprint", "interaction_zone", "door_anchor", "ground_contact_rect", "y_sort_anchor", "projection_details"]:
		_expect(definition.has(key), id + "_entity_definition_has_" + key)
	_expect(definition.has("door_offset") or definition.has("frontage_offset"), id + "_entity_definition_has_door_or_frontage_offset")

	var building_type := String(definition.get("building_type", ""))
	var access_rule := String(definition.get("access_rule", ""))
	var interior_scene := String(definition.get("interior_scene", ""))
	_expect(not building_type.is_empty(), id + "_entity_building_type_present")
	_expect(["public", "private", "locked", "owner_only_future"].has(access_rule), id + "_entity_access_rule_known")
	_expect(interior_scene.begins_with("res://scenes/interiors/") and interior_scene.ends_with("_stub.tscn"), id + "_entity_interior_stub_path")
	_expect((definition.get("collision_footprint", Rect2()) as Rect2).size.x > 0.0, id + "_entity_collision_footprint_present")
	_expect((definition.get("interaction_zone", Rect2()) as Rect2).size.x > 0.0, id + "_entity_interaction_zone_present")
	var interaction_zone: Rect2 = definition.get("interaction_zone", Rect2())
	_expect(interaction_zone.size.x <= 64.0 and interaction_zone.size.y <= 36.0, id + "_entity_interaction_zone_tight_to_door")
	_expect(not String(definition.get("interaction_label", "")).is_empty(), id + "_entity_interaction_label_present")

	if G414A_PUBLIC_BUILDING_IDS.has(id):
		_expect(access_rule == "public", id + "_entity_public_access_rule")
		_expect(bool(definition.get("is_enterable", false)), id + "_entity_public_is_enterable")
	elif G414A_PRIVATE_OR_FUTURE_HOME_IDS.has(id):
		_expect(["private", "owner_only_future"].has(access_rule), id + "_entity_private_or_owner_future_access")
		_expect(not bool(definition.get("is_enterable", false)), id + "_entity_private_not_enterable")

	if id == "b_mercantile":
		var projection_details: Array = definition.get("projection_details", [])
		_expect(projection_details.size() == 1, "mercantile_hanging_sign_projection_declared")
		if not projection_details.is_empty():
			var sign_projection: Dictionary = projection_details[0]
			var source_rect: Rect2 = sign_projection.get("source_rect", Rect2())
			_expect(String(sign_projection.get("id", "")) == "mercantile_hanging_sign", "mercantile_hanging_sign_projection_id")
			_expect(source_rect.size.x > 0.0 and source_rect.size.y > 0.0, "mercantile_hanging_sign_projection_source_rect")
			_expect(int(sign_projection.get("z_index", 0)) > 0, "mercantile_hanging_sign_projection_foreground_z")

func _validate_g414a_street_wall_curb_datum() -> void:
	if not NEWPORT_TOWN.G410_STARTER_HARBOR_TOWN:
		return

	var target_y := NEWPORT_TOWN.G414A_STREET_WALL_CURB_DATUM_Y * NEWPORT_TOWN.TILE
	for id in G414A_CURB_DATUM_BUILDING_IDS:
		var building := _building_by_name(id)
		_expect(building != null, id + "_curb_datum_building_present")
		if building == null:
			continue
		_expect(absf(building.global_position.y - target_y) <= 0.5, id + "_curb_datum_global_y")

func _validate_starter_harbor_plan() -> void:
	if not NEWPORT_TOWN.G410_STARTER_HARBOR_TOWN:
		return

	var lots: Array = NEWPORT_TOWN.starter_lot_specs()
	var planned_lots: Array = NEWPORT_TOWN.planned_lot_specs()
	var total_lots := lots.size()
	_expect(total_lots >= 14 and total_lots <= 20, "starter_lot_count_14_to_20")
	_expect(planned_lots.size() == NEWPORT_TOWN.STARTER_HARBOR_PLANNED_LOT_IDS.size(), "planned_lot_manifest_count")
	_expect(NEWPORT_TOWN.STARTER_HARBOR_BUILDING_IDS.size() == NEWPORT_TOWN.BUILDING_IDS.size(), "starter_building_manifest_matches_active")

	var lot_ids := {}
	var actual_building_lots := {}
	var district_lots := {}
	for raw_lot in lots:
		var lot: Dictionary = raw_lot
		var id: String = lot["id"]
		_expect(not lot_ids.has(id), "unique_lot_id_" + id)
		lot_ids[id] = true
		var district: String = lot["district"]
		district_lots[district] = district_lots.get(district, 0) + 1
		var rect: Rect2i = lot["rect"]
		_expect(rect.size.x > 0 and rect.size.y > 0, "lot_has_area_" + id)
		if lot.get("status", "") == "actual":
			actual_building_lots[lot.get("building_id", "")] = true

	for building_id in NEWPORT_TOWN.STARTER_HARBOR_BUILDING_IDS:
		_expect(actual_building_lots.has(building_id), "actual_lot_for_" + building_id)
	_expect(not actual_building_lots.has("b_village_hall"), "chapel_coded_hall_not_active")
	_expect(actual_building_lots.has("b_custom_house"), "custom_house_replaces_civic_hall")
	for planned_id in NEWPORT_TOWN.STARTER_HARBOR_PLANNED_LOT_IDS:
		_expect(lot_ids.has(planned_id), "planned_lot_present_" + planned_id)
	for building_id in NEWPORT_TOWN.G413B_ACTIVE_INFILL_BUILDING_IDS:
		_expect(actual_building_lots.has(building_id), "g413b_active_infill_lot_for_" + building_id)
	for district_id in ["harborfront_commercial", "working_wharf", "inland_residential_civic", "support_lane"]:
		_expect(district_lots.get(district_id, 0) > 0, "starter_lots_cover_" + district_id)

	for building_id in ["b_dock_storehouse", "b_wharf_boathouse", "b_dock_warehouse"]:
		_expect(actual_building_lots.has(building_id), "harbor_water_asset_placed_" + building_id)
		for config in NEWPORT_TOWN.building_specs():
			if String(config.get("id", "")) == building_id:
				var water_position: Vector2 = config.get("position", Vector2.ZERO)
				var water_foot_tile_y := water_position.y / float(NEWPORT_TOWN.TILE)
				_expect(water_foot_tile_y >= 27.25 and water_foot_tile_y <= 28.25, "harbor_water_asset_in_wharf_edge_water_pocket_" + building_id)
				var water_foot_tile_x := water_position.x / float(NEWPORT_TOWN.TILE)
				if building_id == "b_dock_warehouse":
					_expect(water_foot_tile_x >= 14.5 and water_foot_tile_x <= 16.5, "harbor_water_asset_beside_west_pier_" + building_id)
				elif building_id == "b_wharf_boathouse":
					_expect(water_foot_tile_x >= 27.0 and water_foot_tile_x <= 29.5, "harbor_water_asset_beside_center_pier_" + building_id)
				else:
					_expect(water_foot_tile_x >= 40.0 and water_foot_tile_x <= 42.5, "harbor_water_asset_beside_east_pier_" + building_id)

	for config in NEWPORT_TOWN.building_specs():
		_expect(config.has("definition_id"), String(config["id"]) + "_has_reusable_definition_id")
		if config.has("definition_id"):
			var definition := BUILDING_CATALOG.building_definition(String(config["definition_id"]))
			for key in ["building_id", "display_name", "role", "building_type", "access_rule", "interior_scene", "owner_id", "is_enterable", "interaction_enabled", "interaction_label", "locked_message", "unavailable_message", "texture_path", "sprite_region", "sprite_source_size", "visual_scale", "scale", "visual_bounds", "lot_bounds", "collision_footprint", "interaction_zone", "foot_anchor", "visual_base_anchor", "collision_shape", "collision_rect", "interaction_size", "interaction_offset", "interaction_zone_placeholder", "frontage_offset", "door_offset", "door_anchor", "ground_contact_rect", "y_sort_anchor", "shadow_size", "projection_details", "district_role", "district_placement_tags", "notes"]:
				_expect(definition.has(key), String(config["id"]) + "_definition_has_" + key)
			var texture_path: String = definition.get("texture_path", "")
			_expect(texture_path.begins_with("res://assets/sprites/buildings/isolated/") or texture_path.begins_with("res://assets/buildings/"), String(config["id"]) + "_uses_project_building_sprite")
			var tags: Array = definition.get("district_placement_tags", [])
			_expect(not tags.is_empty(), String(config["id"]) + "_has_district_placement_tags")
			if String(config["id"]) == "b_clerk_townhouse":
				var clerk_visual: Rect2 = definition.get("visual_bounds", Rect2())
				var clerk_region: Rect2 = definition.get("sprite_region", Rect2())
				_expect(definition.get("sprite_id", "") == "newport_formal_townhouse_block_a", "clerk_townhouse_uses_brick_rowhouse_asset")
				_expect(clerk_region.size.x >= 360.0 and clerk_region.size.y >= 330.0, "clerk_townhouse_uses_uncut_brick_block_region")
				_expect(clerk_visual.size.x >= 145.0 and clerk_visual.size.y >= 150.0, "clerk_townhouse_not_under_scaled_or_cropped")
				_expect(float(definition.get("visual_scale", 0.0)) >= 160.0, "clerk_townhouse_newport_rowhouse_scale")
			if String(config["id"]) == "b_shop_house":
				var shop_visual: Rect2 = definition.get("visual_bounds", Rect2())
				_expect(definition.get("sprite_id", "") == "newport_shopfront_awning", "shop_house_uses_awning_storefront_asset")
				_expect(shop_visual.size.x >= 145.0 and shop_visual.size.y >= 140.0, "shop_house_not_under_scaled_or_cropped")
				_expect(float(definition.get("visual_scale", 0.0)) >= 185.0, "shop_house_newport_storefront_scale")

	var manifest: Array = NEWPORT_TOWN.missing_asset_manifest()
	for needed in ["fishmonger storefront", "cooperage / barrel shop final art", "blacksmith / smithy", "small home variants", "dock shack", "carts", "dedicated crate/barrel/rope prop sprites", "sign variants", "fencing variants", "lantern variants", "Newport-detail player character sprite sheet", "Newport-detail NPC sprite sheets", "Newport-detail monster sprite sheets", "Newport-detail equipment, weapons, armor, and combat VFX", "chapel/church decision and final art if needed"]:
		_expect(manifest.has(needed), "missing_asset_manifest_" + needed.replace("/", "_").replace(" ", "_"))

	var plan: Dictionary = NEWPORT_TOWN.starter_district_plan()
	var plan_districts: Array = plan.get("districts", [])
	var plan_loop: Array = plan.get("movement_loop", [])
	_expect(plan.get("target_total_lots", "") == "14-20", "starter_plan_target_lot_range")
	_expect(plan.get("composition_pass", "") == "G-4.13B.1", "starter_plan_composition_pass_g_4_13b_1")
	_expect(plan.get("footprint_pass", "") == "G-4.13A", "starter_plan_footprint_pass_g_4_13a")
	_expect(plan.get("density_pass", "") == "G-4.13B", "starter_plan_density_pass_g_4_13b")
	_expect(plan.get("layout_rules_pass", "") == "G-4.15", "starter_plan_layout_rules_pass_g_4_15")
	_expect(plan.get("surface_kit_pass", "") == "G-4.16", "starter_plan_surface_kit_pass_g_4_16")
	_expect(plan.get("asset_pipeline_pass", "") == "G-4.18B", "starter_plan_asset_pipeline_pass_g_4_18b")
	_expect(String(plan.get("hero_street_atlas_proof", "")).find("atlas") >= 0, "starter_plan_hero_street_atlas_proof")
	_expect(plan.get("green_origin_pipeline_pass", "") == "G-4.18B", "starter_plan_green_origin_pipeline_pass")
	_expect(String(plan.get("yellow_review_art_policy", "")).find("yellow pixels cannot source final-commercial green assets") >= 0, "starter_plan_yellow_review_art_policy")
	_expect(int(plan.get("layout_rule_count", 0)) == NEWPORT_TOWN.STARTER_HARBOR_BUILDING_IDS.size(), "starter_plan_g415_layout_rule_count")
	_expect(float(plan.get("visual_acceptance_score_target", 0.0)) >= 8.5, "starter_plan_g415_visual_acceptance_target")
	_expect(int(plan.get("active_g413b_infill_count", 0)) >= 3, "starter_plan_active_g413b_infill_count")
	var plan_active_infill: Array = plan.get("active_g413b_infill_buildings", [])
	for building_id in NEWPORT_TOWN.G413B_ACTIVE_INFILL_BUILDING_IDS:
		_expect(plan_active_infill.has(building_id), "starter_plan_active_infill_" + building_id)
	_expect(String(plan.get("collision_model", "")).find("collision_footprint") >= 0, "starter_plan_collision_model_mentions_collision_footprint")
	_expect(plan.get("clean_review_default", false) == true, "starter_plan_clean_review_default")
	_expect(plan.get("newport_visual_cohesion_gate", false) == true, "starter_plan_newport_visual_cohesion_gate")
	_expect(plan.get("asset_provenance_gate", false) == true, "starter_plan_asset_provenance_gate")
	_expect(String(plan.get("review_screenshot_mode", "")).find("F4") >= 0, "starter_plan_review_screenshot_mode")
	_expect(plan_districts.size() >= 4, "starter_plan_district_structure")
	_expect(plan_loop.has("commercial_rear_road"), "starter_plan_includes_commercial_rear_road")
	_expect(plan_loop.has("mercantile_counting_house_rear_road"), "starter_plan_includes_mercantile_counting_rear_road")
	_expect(plan_loop.size() >= 6, "starter_plan_movement_loop")
	_expect(NEWPORT_TOWN.g413b_rowhouse_infill_slots().size() == NEWPORT_TOWN.G413B_ROWHOUSE_INFILL_SLOT_IDS.size(), "g413b_rowhouse_infill_slot_manifest_count")
	var active_slots := 0
	var deferred_slots := 0
	for raw_slot in NEWPORT_TOWN.g413b_rowhouse_infill_slots():
		var slot: Dictionary = raw_slot
		var status := String(slot.get("status", ""))
		if status == "active_g413b":
			active_slots += 1
			_expect(NEWPORT_TOWN.G413B_ACTIVE_INFILL_BUILDING_IDS.has(String(slot.get("building_id", ""))), "g413b_slot_active_building_" + String(slot.get("id", "")))
		elif status == "deferred_g413b":
			deferred_slots += 1
			_expect(NEWPORT_TOWN.G413B_DEFERRED_INFILL_SLOT_IDS.has(String(slot.get("id", ""))), "g413b_slot_deferred_manifest_" + String(slot.get("id", "")))
		_expect(not String(slot.get("guardrail", "")).is_empty(), "g413b_slot_guardrail_" + String(slot.get("id", "")))
		_expect(not String(slot.get("future_hook", "")).is_empty(), "g413b_slot_future_hook_" + String(slot.get("id", "")))
	_expect(active_slots >= 3, "g413b_active_infill_slot_count")
	_expect(deferred_slots >= 2, "g413b_deferred_infill_slot_count")
	_expect(NEWPORT_TOWN.route_debug_probes().size() >= 13, "g413b_route_debug_probe_count")
	_expect(BUILDING_CATALOG.available_building_assets().size() >= 20, "asset_audit_catalog_populated")

func _validate_g415_layout_rules() -> void:
	if not NEWPORT_TOWN.G410_STARTER_HARBOR_TOWN:
		return

	var rules: Dictionary = NEWPORT_TOWN.g415_layout_rules()
	_expect(rules.size() == NEWPORT_TOWN.STARTER_HARBOR_BUILDING_IDS.size(), "g415_layout_rule_count_matches_buildings")

	var configs_by_id := {}
	for config in NEWPORT_TOWN.building_specs():
		configs_by_id[String(config.get("id", ""))] = config

	for building_id in NEWPORT_TOWN.STARTER_HARBOR_BUILDING_IDS:
		var id := String(building_id)
		_expect(rules.has(id), "g415_layout_rule_present_" + id)
		if not rules.has(id):
			continue
		var rule: Dictionary = rules[id]
		for key in ["parcel_id", "district_band", "frontage_line_y", "setback_from_road", "side_gap_minimum", "door_path_target", "prop_band", "ground_pad", "lot_type"]:
			_expect(rule.has(key), "g415_layout_rule_" + id + "_has_" + key)

		var ground_pad: Dictionary = rule.get("ground_pad", {})
		var ground_rect: Rect2 = ground_pad.get("rect", Rect2())
		var prop_band: Rect2 = rule.get("prop_band", Rect2())
		var door_path_target: Vector2 = rule.get("door_path_target", Vector2.ZERO)
		_expect(not String(rule.get("parcel_id", "")).is_empty(), "g415_layout_rule_" + id + "_parcel_id_named")
		_expect(["commercial", "market", "civic", "residential", "support", "dock"].has(String(rule.get("district_band", ""))), "g415_layout_rule_" + id + "_district_band_known")
		_expect(float(rule.get("frontage_line_y", 0.0)) > 0.0, "g415_layout_rule_" + id + "_frontage_line_y_authored")
		_expect(float(rule.get("setback_from_road", 0.0)) >= 0.0, "g415_layout_rule_" + id + "_setback_authored")
		_expect(float(rule.get("side_gap_minimum", 0.0)) >= 0.0, "g415_layout_rule_" + id + "_side_gap_authored")
		_expect(door_path_target.x > 0.0 and door_path_target.y > 0.0, "g415_layout_rule_" + id + "_door_path_target_authored")
		_expect(prop_band.size.x > 0.0 and prop_band.size.y > 0.0, "g415_layout_rule_" + id + "_prop_band_authored")
		_expect(ground_rect.size.x > 0.0 and ground_rect.size.y > 0.0, "g415_layout_rule_" + id + "_ground_pad_authored")
		_expect(not String(ground_pad.get("type", "")).is_empty(), "g415_layout_rule_" + id + "_ground_pad_type")

		var config: Dictionary = configs_by_id.get(id, {})
		for key in ["parcel_id", "district_band", "frontage_line_y", "setback_from_road", "side_gap_minimum", "door_path_target", "prop_band", "ground_pad", "lot_type", "layout_rule"]:
			_expect(config.has(key), "g415_building_spec_" + id + "_carries_" + key)

	var rubric: Dictionary = NEWPORT_TOWN.g415_visual_qa_rubric()
	var target := float(rubric.get("target_score", 0.0))
	_expect(target >= 8.5, "g415_visual_target_8_5")
	for key in ["building_grounding", "readable_doors", "believable_spacing", "prop_purposefulness", "walkable_roads", "harbor_identity", "depth_y_sort_believability", "screenshot_beauty", "not_pasted_feel"]:
		_expect(float(rubric.get(key, 0.0)) >= target, "g415_visual_rubric_" + key + "_meets_target")

func _validate_visual_composition_spacing() -> void:
	if not NEWPORT_TOWN.G410_STARTER_HARBOR_TOWN:
		return

	_validate_visual_sequence_has_tight_seams("harborfront_parceled_street_wall", [
		"b_inn_tavern",
		"b_clerk_townhouse",
		"b_mercantile",
		"b_counting_house",
		"b_chandlery_front",
		"b_shop_house",
		"b_market_shed",
		"b_printer_rowhouse",
	], 0.0, 32.0)
	_validate_harborfront_visual_bottom_datum()
	_validate_harborfront_parcel_rhythm()
	_validate_review_bounds_track_art_body("harborfront_street_wall", [
		"b_inn_tavern",
		"b_clerk_townhouse",
		"b_mercantile",
		"b_counting_house",
		"b_chandlery_front",
		"b_shop_house",
		"b_market_shed",
		"b_printer_rowhouse",
	])
	_validate_visual_sequence_has_tight_seams("support_lane_row", [
		"b_boarding_house",
		"b_dockworker_rowhouse",
	], 0.0, 8.0)
	_validate_review_bounds_track_art_body("support_lane_row", [
		"b_boarding_house",
		"b_dockworker_rowhouse",
	])

	var clerk := _building_by_name("b_clerk_townhouse")
	if clerk:
		var clerk_rect := _building_visual_world_rect(clerk)
		_expect(clerk_rect.size.x >= 145.0 and clerk_rect.size.y >= 150.0, "clerk_townhouse_world_full_brick_block")
		var mercantile := _building_by_name("b_mercantile")
		if mercantile:
			var mercantile_rect := _building_visual_world_rect(mercantile)
			var clerk_to_mercantile_gap := mercantile_rect.position.x - clerk_rect.end.x
			_expect(clerk_to_mercantile_gap >= 8.0, "clerk_townhouse_not_cut_off_by_mercantile")
			_expect(clerk_to_mercantile_gap <= 12.0, "clerk_townhouse_keeps_tight_mercantile_gutter")

func _validate_harborfront_parcel_rhythm() -> void:
	var chandlery_to_shop_gap := _visual_gap_between("b_chandlery_front", "b_shop_house")
	var shop_to_market_gap := _visual_gap_between("b_shop_house", "b_market_shed")
	var market_to_printer_gap := _visual_gap_between("b_market_shed", "b_printer_rowhouse")
	_expect(chandlery_to_shop_gap >= 10.0 and chandlery_to_shop_gap <= 18.0, "g415_shop_house_has_chandlery_service_slit")
	_expect(shop_to_market_gap >= 18.0 and shop_to_market_gap <= 32.0, "g415_shop_house_has_market_breathing_room")
	_expect(market_to_printer_gap >= 10.0 and market_to_printer_gap <= 26.0, "g415_market_to_printer_has_east_gutter")

	var chandlery := _building_by_name("b_chandlery_front")
	var shop := _building_by_name("b_shop_house")
	var market := _building_by_name("b_market_shed")
	var printer := _building_by_name("b_printer_rowhouse")
	if chandlery and shop and market and printer:
		_expect(chandlery.global_position.x < shop.global_position.x and shop.global_position.x < market.global_position.x and market.global_position.x < printer.global_position.x, "g415_parcel_order_chandlery_shop_market_printer")

func _validate_harborfront_visual_bottom_datum() -> void:
	var street_bottom_y := NEWPORT_TOWN.G414A_STREET_WALL_CURB_DATUM_Y * float(NEWPORT_TOWN.TILE)
	for id in G414A_CURB_DATUM_BUILDING_IDS:
		var building := _building_by_name(String(id))
		if building == null:
			failures.append("harborfront_bottom_datum_missing_" + String(id))
			continue
		var rect := _building_visual_world_rect(building)
		_expect(absf(rect.end.y - street_bottom_y) <= 1.0, "harborfront_visual_bottom_on_curb_datum_" + String(id))

func _validate_review_bounds_track_art_body(label: String, ids: Array) -> void:
	for id in ids:
		var building := _building_by_name(String(id))
		if building == null or not building.has_method("get_visual_bounds") or not building.has_method("get_lot_bounds"):
			failures.append("review_bounds_missing_" + label + "_" + String(id))
			continue
		var visual_rect: Rect2 = building.get_visual_bounds()
		var lot_rect: Rect2 = building.get_lot_bounds()
		_expect(absf(lot_rect.position.x - visual_rect.position.x) <= 1.0, "review_bounds_left_tracks_art_" + label + "_" + String(id))
		_expect(absf(lot_rect.end.x - visual_rect.end.x) <= 1.0, "review_bounds_right_tracks_art_" + label + "_" + String(id))
		_expect(absf(lot_rect.position.y - visual_rect.position.y) <= 1.0, "review_bounds_top_tracks_art_" + label + "_" + String(id))
		_expect(absf(lot_rect.end.y - visual_rect.end.y) <= 1.0, "review_bounds_bottom_tracks_art_" + label + "_" + String(id))

func _validate_visual_sequence_has_tight_seams(label: String, ids: Array, min_gap: float, max_gap: float) -> void:
	var entries: Array = []
	for id in ids:
		var building := _building_by_name(String(id))
		if building == null:
			failures.append("visual_sequence_missing_" + label + "_" + String(id))
			continue
		var rect := _building_visual_world_rect(building)
		_expect(rect.size.x > 0.0 and rect.size.y > 0.0, "visual_sequence_rect_" + label + "_" + String(id))
		entries.append({"id": String(id), "rect": rect})

	for i in range(entries.size() - 1):
		var left: Dictionary = entries[i]
		var right: Dictionary = entries[i + 1]
		var left_rect: Rect2 = left["rect"]
		var right_rect: Rect2 = right["rect"]
		var gap := right_rect.position.x - left_rect.end.x
		_expect(gap >= min_gap, "visual_seam_not_overlapping_" + label + "_" + String(left["id"]) + "_to_" + String(right["id"]))
		_expect(gap <= max_gap, "visual_seam_not_detached_" + label + "_" + String(left["id"]) + "_to_" + String(right["id"]))

func _visual_gap_between(left_id: String, right_id: String) -> float:
	var left := _building_by_name(left_id)
	var right := _building_by_name(right_id)
	if left == null or right == null:
		failures.append("visual_gap_missing_" + left_id + "_to_" + right_id)
		return -INF
	var left_rect := _building_visual_world_rect(left)
	var right_rect := _building_visual_world_rect(right)
	return right_rect.position.x - left_rect.end.x

func _validate_building_node(building: Node2D) -> void:
	var sprite := building.get_node_or_null("Sprite2D") as Sprite2D
	var body_shape := building.get_node_or_null("Body/CollisionShape2D") as CollisionShape2D
	var interaction_shape := building.get_node_or_null("InteractionArea/CollisionShape2D") as CollisionShape2D
	var door_marker := building.get_node_or_null("DoorMarker") as Marker2D
	var foot_anchor := building.get_node_or_null("FootAnchor") as Marker2D

	_expect(sprite != null and sprite.texture != null, building.name + "_sprite_texture")
	_expect(sprite == null or sprite.texture is AtlasTexture, building.name + "_atlas_texture")
	_expect(body_shape != null and body_shape.shape is RectangleShape2D, building.name + "_body_collision")
	_expect(interaction_shape != null and interaction_shape.shape is RectangleShape2D, building.name + "_interaction_area")
	_expect(door_marker != null, building.name + "_door_marker")
	_expect(foot_anchor != null and foot_anchor.position == Vector2.ZERO, building.name + "_foot_anchor")

	if sprite and sprite.texture:
		var region_size := _texture_region_size(sprite.texture)
		var sprite_bottom_y := sprite.position.y + region_size.y * sprite.scale.y
		var visual_bottom_y := sprite_bottom_y
		if building.has_method("get_visual_bounds"):
			var visual_bounds: Rect2 = building.get_visual_bounds()
			visual_bottom_y = visual_bounds.end.y
		var proof_street: bool = building.has_method("is_proof_street_building") and building.is_proof_street_building()
		var harbor_integrated: bool = building.has_method("is_harbor_integrated") and building.is_harbor_integrated()
		if harbor_integrated:
			_expect(sprite_bottom_y > 20.0 and sprite_bottom_y < 78.0, building.name + "_harbor_sprite_extends_into_water")
		elif proof_street:
			_expect(visual_bottom_y >= -2.5 and visual_bottom_y <= 22.0, building.name + "_foot_anchor_at_visual_base")
			_expect(sprite_bottom_y > -2.5 and sprite_bottom_y < 44.0, building.name + "_painterly_base_padding_allowed")
		else:
			_expect(visual_bottom_y >= -2.5 and visual_bottom_y <= 22.0, building.name + "_foot_anchor_at_visual_base")

	if String(building.name) == "b_mercantile":
		var projection := building.get_node_or_null("Projection_mercantile_hanging_sign") as Sprite2D
		_expect(projection != null and projection.texture is AtlasTexture, "mercantile_hanging_sign_projection_runtime_sprite")
		_expect(projection == null or projection.z_index > 0, "mercantile_hanging_sign_projection_draws_foreground")
		_expect(projection == null or projection.z_as_relative == false, "mercantile_hanging_sign_projection_uses_absolute_z")
		if building.has_method("get_projection_detail_names"):
			_expect(building.get_projection_detail_names().has("mercantile_hanging_sign"), "mercantile_hanging_sign_projection_registered")

	if NEWPORT_TOWN.G410_STARTER_HARBOR_TOWN:
		_expect(building.has_method("uses_normalized_definition") and building.uses_normalized_definition(), building.name + "_uses_normalized_definition")

	if body_shape and body_shape.shape is RectangleShape2D:
		var body_size := (body_shape.shape as RectangleShape2D).size
		var body_rect := Rect2(body_shape.position - body_size * 0.5, body_size)
		_expect(body_size.x >= 60.0 and body_size.y >= 28.0, building.name + "_playable_collision_footprint")
		_expect(body_size.y <= 64.0, building.name + "_collision_footprint_not_visual_height")
		_expect(body_rect.position.y >= -42.0 and body_rect.end.y <= 18.0, building.name + "_collision_footprint_sits_on_ground_contact")
		var proof_street: bool = building.has_method("is_proof_street_building") and building.is_proof_street_building()
		if proof_street:
			_expect(body_size.y <= 48.0, building.name + "_proof_street_uses_tight_ground_footprint")
		if building.has_method("get_visual_bounds"):
			var visual_bounds: Rect2 = building.get_visual_bounds()
			_expect(visual_bounds.size.y > body_size.y * 2.0, building.name + "_visual_bounds_separate_from_collision_footprint")
		if building.has_method("get_lot_bounds"):
			var lot_bounds: Rect2 = building.get_lot_bounds()
			_expect(lot_bounds.size.y > body_size.y, building.name + "_lot_bounds_separate_from_collision_footprint")

	if interaction_shape and interaction_shape.shape is RectangleShape2D:
		_expect(interaction_shape.position.y > 0.0, building.name + "_frontage_interaction_south")
		if body_shape and body_shape.shape is RectangleShape2D:
			var interaction_size := (interaction_shape.shape as RectangleShape2D).size
			var interaction_rect := Rect2(interaction_shape.position - interaction_size * 0.5, interaction_size)
			var body_size := (body_shape.shape as RectangleShape2D).size
			var body_rect := Rect2(body_shape.position - body_size * 0.5, body_size)
			_expect(interaction_rect.position.y >= body_rect.position.y, building.name + "_interaction_zone_not_rear_blocker")

func _validate_proof_street(main: Node) -> void:
	var proof_ids: Array = NEWPORT_TOWN.proof_street_ids()
	if NEWPORT_TOWN.G47_CALIBRATION_MODE:
		_expect(proof_ids.size() == 8, "calibration_building_count_8")
		_expect(NEWPORT_TOWN.calibration_variants().size() == 4, "calibration_variant_count_4")
	elif NEWPORT_TOWN.G410_STARTER_HARBOR_TOWN:
		_expect(proof_ids.size() == 5, "starter_harborfront_building_count_5")
	elif NEWPORT_TOWN.G46_PROOF_FRAME:
		_expect(proof_ids.size() == 3, "proof_street_building_count_3")
	elif NEWPORT_TOWN.G48_PROOF_STREET or NEWPORT_TOWN.G49_STREET_VIGNETTE:
		_expect(proof_ids.size() >= 3 and proof_ids.size() <= 5, "proof_street_building_count_3_to_5")
	else:
		_expect(proof_ids.size() >= 5 and proof_ids.size() <= 7, "proof_street_building_count_5_to_7")

	var configs_by_id := {}
	for config in NEWPORT_TOWN.building_specs():
		var merged_config: Dictionary = config
		if config.has("definition_id"):
			merged_config = BUILDING_CATALOG.building_definition(String(config["definition_id"]))
			for key in config:
				merged_config[key] = config[key]
		configs_by_id[config["id"]] = merged_config

	for id in proof_ids:
		_expect(configs_by_id.has(id), "proof_street_config_present_" + id)
		if configs_by_id.has(id):
			var config: Dictionary = configs_by_id[id]
			_expect(config.get("proof_street", false), id + "_proof_street_flag")
			for key in ["visual_base_anchor", "frontage_offset", "visual_bounds", "collision_footprint", "collision_rect", "interaction_zone", "lot_bounds", "lot_rect", "building_volume_rect", "y_sort_offset", "shadow_size"]:
				_expect(config.has(key), id + "_seating_metadata_" + key)

	var proof_buildings := get_nodes_in_group("proof_street_buildings")
	_expect(proof_buildings.size() == proof_ids.size(), "proof_street_node_count")
	for raw_building in proof_buildings:
		var building := raw_building as Node2D
		if building == null:
			failures.append("proof_street_node_not_node2d")
			continue
		var overlay := building.get_node_or_null("DebugOverlay") as Node2D
		_expect(overlay != null and not overlay.visible, building.name + "_seating_debug_off_by_default")
		_expect(overlay == null or overlay.visible == false, building.name + "_debug_labels_hidden_in_review_mode")
		_expect(overlay == null or overlay.get("_debug_enabled") == false, building.name + "_debug_overlay_not_armed_in_review_mode")
		_expect(building.has_method("has_seating_metadata") and building.has_seating_metadata(), building.name + "_runtime_seating_metadata")
		_expect(building.get_node_or_null("FrontageMarker") != null, building.name + "_frontage_marker")
		_expect(building.get_node_or_null("YSortAnchor") != null, building.name + "_ysort_marker")

	if main.has_method("set_building_seating_overlay"):
		main.set_building_seating_overlay(true)
		var collision_layer := main.get_node_or_null("World/TownMap/CollisionNavigationLayer")
		_expect(collision_layer == null or collision_layer.get("_debug_overlay_enabled") == false, "g415_building_seating_overlay_keeps_route_collision_labels_off")
		for raw_building in get_nodes_in_group("buildings"):
			var building := raw_building as Node2D
			if building == null:
				continue
			var overlay := building.get_node_or_null("DebugOverlay") as Node2D
			if overlay == null:
				continue
			var is_proof: bool = building.has_method("is_proof_street_building") and building.is_proof_street_building()
			if NEWPORT_TOWN.G410_STARTER_HARBOR_TOWN:
				is_proof = true
			_expect(overlay.visible == is_proof, building.name + "_seating_debug_toggle_scope")
			if is_proof:
				_expect(overlay.get("_label_detail") == false, building.name + "_seating_debug_uses_compact_labels")
		main.set_building_seating_overlay(false)
	else:
		failures.append("main_set_building_seating_overlay_method")

	if main.has_method("set_debug_overlay"):
		main.set_debug_overlay(true)
		for raw_building in get_nodes_in_group("buildings"):
			var building := raw_building as Node2D
			if building == null:
				continue
			var overlay := building.get_node_or_null("DebugOverlay") as Node2D
			if overlay:
				_expect(overlay.visible, building.name + "_full_debug_overlay_scope")
				_expect(overlay.get("_label_detail") == true, building.name + "_full_debug_overlay_detailed_labels")
		main.set_debug_overlay(false)
	else:
		failures.append("main_set_debug_overlay_method")

func _validate_reachability() -> void:
	var route_tiles: Array = NEWPORT_TOWN.route_tiles()
	var route_set := {}
	for tile in route_tiles:
		route_set[_key(tile)] = true

	var start := NEWPORT_TOWN.player_spawn_tile()
	_expect(route_set.has(_key(start)), "spawn_on_route_tile")
	var reached := _flood_route_tiles(start, route_set)

	for target_name in NEWPORT_TOWN.reachability_targets().keys():
		var tile: Vector2i = NEWPORT_TOWN.reachability_targets()[target_name]
		_expect(reached.has(_key(tile)), "route_reachable_" + target_name)

	if not NEWPORT_TOWN.G47_CALIBRATION_MODE:
		for target_name in NEWPORT_TOWN.proof_street_walk_targets().keys():
			var tile: Vector2i = NEWPORT_TOWN.proof_street_walk_targets()[target_name]
			_expect(reached.has(_key(tile)), "proof_street_walk_reachable_" + target_name)

func _validate_building_walkability_gate() -> void:
	if not NEWPORT_TOWN.G410_STARTER_HARBOR_TOWN:
		return

	var walk_samples := {
		"road_behind_b_mercantile": Vector2(492.0, 526.0),
		"road_behind_b_counting_house": Vector2(680.0, 526.0),
		"harborfront_rear_commercial_row": Vector2(892.0, 526.0),
		"west_commercial_cross_lane": Vector2(392.0, 520.0),
		"central_inland_cross_lane": Vector2(672.0, 430.0),
		"central_front_cross_lane": Vector2(752.0, 604.0),
		"east_commercial_cross_lane": Vector2(1100.0, 520.0),
		"dock_layer_walk": Vector2(824.0, 710.0),
		"clerk_rowhouse_front_walk": Vector2(420.0, 604.0),
		"market_east_edge_front_walk": Vector2(1430.0, 604.0),
		"support_boarding_gap_walk": Vector2(1380.0, 418.0),
	}
	for sample_name in walk_samples.keys():
		var point: Vector2 = walk_samples[sample_name]
		_expect(_collision_owner_labels_at(point, 10.0).is_empty(), "walkability_" + sample_name)

	for raw_building in get_nodes_in_group("buildings"):
		var building := raw_building as Node2D
		if building == null:
			continue
		var rect := _building_collision_world_rect(building)
		if rect.size.x <= 0.0 or rect.size.y <= 0.0:
			continue
		_expect(rect.has_point(rect.get_center()), String(building.name) + "_obvious_building_body_blocks_center")

func _validate_route_debug_probes() -> void:
	if not NEWPORT_TOWN.G410_STARTER_HARBOR_TOWN:
		return
	for probe in NEWPORT_TOWN.route_debug_probes():
		var id := String(probe.get("id", ""))
		var position: Vector2 = probe.get("position", Vector2.ZERO)
		var owners := _collision_owner_labels_at(position, 10.0)
		if not owners.is_empty():
			failures.append("route_probe_" + id + "_blocked_by_" + ",".join(owners))

func _point_hits_building_collision(point: Vector2, player_radius: float) -> bool:
	for raw_building in get_nodes_in_group("buildings"):
		var building := raw_building as Node2D
		if building == null:
			continue
		var rect := _building_collision_world_rect(building).grow(player_radius)
		if rect.has_point(point):
			return true
	return false

func _collision_owner_labels_at(point: Vector2, player_radius: float) -> Array[String]:
	var owners: Array[String] = []
	var collision_layer := root.get_node_or_null("Main/World/TownMap/CollisionNavigationLayer")
	if collision_layer:
		for raw_body in collision_layer.get_children():
			var body := raw_body as StaticBody2D
			if body == null:
				continue
			for raw_shape in body.get_children():
				var shape := raw_shape as CollisionShape2D
				if shape == null or not (shape.shape is RectangleShape2D):
					continue
				var size := (shape.shape as RectangleShape2D).size
				var rect := Rect2(shape.global_position - size * 0.5, size).grow(player_radius)
				if rect.has_point(point):
					owners.append(_collision_body_owner_label(String(body.name)))
	for raw_building in get_nodes_in_group("buildings"):
		var building := raw_building as Node2D
		if building == null:
			continue
		var rect := _building_collision_world_rect(building).grow(player_radius)
		if rect.size.x > 0.0 and rect.size.y > 0.0 and rect.has_point(point):
			owners.append("building:" + String(building.name))
	return owners

func _collision_body_owner_label(body_name: String) -> String:
	if body_name.begins_with("DetailBlocker_"):
		return "prop:" + body_name.trim_prefix("DetailBlocker_")
	if body_name.begins_with("HarborWater_"):
		return "map_water:" + body_name.trim_prefix("HarborWater_")
	return "map:" + body_name

func _building_collision_world_rect(building: Node2D) -> Rect2:
	var body_shape := building.get_node_or_null("Body/CollisionShape2D") as CollisionShape2D
	if body_shape == null or not (body_shape.shape is RectangleShape2D):
		return Rect2()
	var body_size := (body_shape.shape as RectangleShape2D).size
	var local_rect := Rect2(body_shape.position - body_size * 0.5, body_size)
	return Rect2(building.global_position + local_rect.position, local_rect.size)

func _building_by_name(building_name: String) -> Node2D:
	for raw_building in get_nodes_in_group("buildings"):
		var building := raw_building as Node2D
		if building and String(building.name) == building_name:
			return building
	return null

func _building_visual_world_rect(building: Node2D) -> Rect2:
	if building == null or not building.has_method("get_visual_bounds"):
		return Rect2()
	var local_rect: Rect2 = building.get_visual_bounds()
	return Rect2(building.global_position + local_rect.position, local_rect.size)

func _flood_route_tiles(start: Vector2i, route_set: Dictionary) -> Dictionary:
	var reached := {}
	var queue: Array[Vector2i] = [start]
	reached[_key(start)] = true
	var directions: Array[Vector2i] = [Vector2i.LEFT, Vector2i.RIGHT, Vector2i.UP, Vector2i.DOWN]
	while not queue.is_empty():
		var current := queue.pop_front() as Vector2i
		for direction: Vector2i in directions:
			var next_tile: Vector2i = current + direction
			var key: String = _key(next_tile)
			if route_set.has(key) and not reached.has(key):
				reached[key] = true
				queue.append(next_tile)
	return reached

func _texture_region_size(texture: Texture2D) -> Vector2:
	if texture is AtlasTexture:
		return (texture as AtlasTexture).region.size
	return texture.get_size()

func _key(tile: Vector2i) -> String:
	return "%d,%d" % [tile.x, tile.y]

func _expect(condition: bool, label: String) -> void:
	if not condition:
		failures.append(label)

func _print_report() -> void:
	var districts := {}
	for config in NEWPORT_TOWN.building_specs():
		var district: String = config["district"]
		districts[district] = districts.get(district, 0) + 1
	print("[Wayfarer Godot Newport Town QA]")
	print("godotVersion=", Engine.get_version_info()["string"])
	print("buildingCount=", get_nodes_in_group("buildings").size())
	print("expectedBuildings=", NEWPORT_TOWN.BUILDING_IDS)
	print("districtCounts=", districts)
	if NEWPORT_TOWN.G410_STARTER_HARBOR_TOWN:
		print("starterLotCount=", NEWPORT_TOWN.starter_lot_specs().size())
		print("plannedLots=", NEWPORT_TOWN.STARTER_HARBOR_PLANNED_LOT_IDS)
		print("missingAssets=", NEWPORT_TOWN.missing_asset_manifest())
		print("routeDebugProbes=", NEWPORT_TOWN.route_debug_probes())
		print("surfaceKitPass=", NEWPORT_TOWN.starter_district_plan().get("surface_kit_pass", ""))
		print("assetPipelinePass=", NEWPORT_TOWN.starter_district_plan().get("asset_pipeline_pass", ""))
	print("reachabilityTargets=", NEWPORT_TOWN.reachability_targets())
	print("failureCount=", failures.size())
	print("failures=", failures)
	print("status=", "PASS" if failures.is_empty() else "FAIL")
