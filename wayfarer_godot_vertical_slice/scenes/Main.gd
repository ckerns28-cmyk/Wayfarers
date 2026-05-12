extends Node2D

const BUILDING_SCENE := preload("res://scenes/buildings/Building.tscn")
const BUILDING_CATALOG := preload("res://scripts/BuildingCatalog.gd")
const NEWPORT_TOWN := preload("res://scripts/NewportTownBlueprint.gd")
const BUILD_INFO := preload("res://scripts/BuildInfo.gd")
const GAMEPLAY_KEYCODES := [
	KEY_W,
	KEY_A,
	KEY_S,
	KEY_D,
	KEY_UP,
	KEY_DOWN,
	KEY_LEFT,
	KEY_RIGHT,
	KEY_E,
	KEY_B,
]

@onready var world: Node2D = $World
@onready var player: CharacterBody2D = $World/Player
@onready var hud: CanvasLayer = $HUD

var _atlas_cache: Dictionary = {}
var _debug_overlay_enabled := BUILD_INFO.DEBUG_OVERLAYS_DEFAULT
var _seating_debug_enabled := BUILD_INFO.DEBUG_OVERLAYS_DEFAULT

func _ready() -> void:
	world.y_sort_enabled = true
	player.global_position = NEWPORT_TOWN.PLAYER_SPAWN
	if player.has_method("configure_world_limits"):
		player.configure_world_limits(Rect2(Vector2.ZERO, NEWPORT_TOWN.WORLD_SIZE))
	var edrin := world.get_node_or_null("EdrinVale") as Node2D
	if edrin and (NEWPORT_TOWN.G46_PROOF_FRAME or NEWPORT_TOWN.G47_CALIBRATION_MODE or NEWPORT_TOWN.G48_PROOF_STREET or NEWPORT_TOWN.G49_STREET_VIGNETTE):
		edrin.queue_free()
	elif edrin:
		edrin.global_position = NEWPORT_TOWN.EDRIN_SPAWN
	_place_buildings()
	_set_debug_overlay(BUILD_INFO.DEBUG_OVERLAYS_DEFAULT)
	_set_building_seating_overlay(BUILD_INFO.DEBUG_OVERLAYS_DEFAULT)
	player.dialogue_triggered.connect(hud.show_dialogue)

func _input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.pressed:
		get_viewport().set_input_as_handled()

func _unhandled_input(event: InputEvent) -> void:
	if not event is InputEventKey:
		return

	var key_event := event as InputEventKey
	if key_event.pressed and not key_event.echo and key_event.keycode == KEY_B:
		if BUILD_INFO.DEBUG_OVERLAY_TOGGLE_ENABLED:
			_set_building_seating_overlay(not _seating_debug_enabled)
		get_viewport().set_input_as_handled()
		return

	if key_event.pressed and not key_event.echo and key_event.keycode == KEY_F2:
		if hud.has_method("toggle_review_metadata"):
			hud.toggle_review_metadata()
		get_viewport().set_input_as_handled()
		return

	if key_event.pressed and not key_event.echo and key_event.keycode == KEY_F3:
		if BUILD_INFO.DEBUG_OVERLAY_TOGGLE_ENABLED:
			_set_debug_overlay(not _debug_overlay_enabled)
		get_viewport().set_input_as_handled()
		return

	if GAMEPLAY_KEYCODES.has(key_event.keycode):
		get_viewport().set_input_as_handled()

func set_debug_overlay(enabled: bool) -> void:
	_set_debug_overlay(enabled)

func set_building_seating_overlay(enabled: bool) -> void:
	_set_building_seating_overlay(enabled)

func _set_debug_overlay(enabled: bool) -> void:
	_debug_overlay_enabled = enabled
	for raw_building in get_tree().get_nodes_in_group("buildings"):
		var building := raw_building as Node2D
		if building and building.has_method("set_debug_overlay"):
			building.set_debug_overlay(enabled)

func _set_building_seating_overlay(enabled: bool) -> void:
	_seating_debug_enabled = enabled
	for raw_building in get_tree().get_nodes_in_group("buildings"):
		var building := raw_building as Node2D
		if building and building.has_method("set_debug_overlay"):
			var show_overlay: bool = enabled and building.has_method("is_proof_street_building") and building.is_proof_street_building()
			building.set_debug_overlay(show_overlay)

func _atlas(path: String, region: Rect2) -> AtlasTexture:
	var texture := AtlasTexture.new()
	texture.atlas = _atlas_image(path)
	texture.region = region
	texture.filter_clip = true
	return texture

func _atlas_image(path: String) -> Texture2D:
	if _atlas_cache.has(path):
		return _atlas_cache[path]

	var atlas_texture := ResourceLoader.load(path, "Texture2D") as Texture2D
	if atlas_texture == null:
		push_error("Failed to load atlas texture: " + path)
		return null

	_atlas_cache[path] = atlas_texture
	return atlas_texture

func _place_buildings() -> void:
	for blueprint_config in NEWPORT_TOWN.building_specs():
		var config := (blueprint_config as Dictionary).duplicate(true)
		var sprite_config := BUILDING_CATALOG.sprite_config(config["sprite_id"])
		for key in sprite_config:
			config[key] = sprite_config[key]
		if config.has("draw_width_override"):
			config["draw_width"] = config["draw_width_override"]
		var atlas_path: String = config["atlas_path"]
		var region: Rect2 = config["region"]
		config["texture"] = _atlas(atlas_path, region)
		var building := BUILDING_SCENE.instantiate()
		world.add_child(building)
		building.configure(config)
