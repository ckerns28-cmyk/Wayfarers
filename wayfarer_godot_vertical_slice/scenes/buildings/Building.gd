extends Node2D
class_name WayfarerBuilding

const BUILD_INFO := preload("res://scripts/BuildInfo.gd")

@onready var sprite: Sprite2D = $Sprite2D
@onready var body_collision: CollisionShape2D = $Body/CollisionShape2D
@onready var interaction_collision: CollisionShape2D = $InteractionArea/CollisionShape2D
@onready var door_marker: Marker2D = $DoorMarker
@onready var foot_anchor: Marker2D = $FootAnchor
@onready var frontage_marker: Marker2D = $FrontageMarker
@onready var y_sort_anchor: Marker2D = $YSortAnchor
@onready var debug_overlay: Node2D = $DebugOverlay

var building_id := ""
var display_name := ""
var definition_id := ""
var district_role := ""
var building_type := ""
var access_rule := ""
var interior_scene := ""
var owner_id := ""
var is_enterable := false
var interaction_label := ""
var locked_message := ""
var unavailable_message := ""
var proof_street := false
var harbor_integrated := false
var definition_normalized := false
var _ground_shadow_size := Vector2(96.0, 22.0)
var _ground_shadow_offset := Vector2(0.0, -6.0)
var _visual_base_width := 96.0
var _visual_bounds := Rect2()
var _collision_footprint := Rect2()
var _interaction_zone := Rect2()
var _lot_bounds := Rect2()
var _foot_anchor_point := Vector2.ZERO
var _door_anchor_point := Vector2.ZERO
var _y_sort_point := Vector2.ZERO
var _ground_contact_rect := Rect2()
var _projection_detail_names: Array[String] = []

func configure(config: Dictionary) -> void:
	building_id = config.get("id", name)
	display_name = config.get("display_name", building_id)
	definition_id = config.get("definition_id", building_id)
	district_role = config.get("district_role", "")
	building_type = config.get("building_type", district_role)
	access_rule = config.get("access_rule", "locked")
	interior_scene = config.get("interior_scene", "")
	owner_id = config.get("owner_id", "")
	is_enterable = config.get("is_enterable", false)
	interaction_label = config.get("interaction_label", "")
	locked_message = config.get("locked_message", "")
	unavailable_message = config.get("unavailable_message", "")
	proof_street = config.get("proof_street", false)
	harbor_integrated = config.get("harbor_integrated", false)
	definition_normalized = config.get("definition_normalized", false)
	name = building_id
	add_to_group("buildings")
	if proof_street:
		add_to_group("proof_street_buildings")
	if is_enterable or config.get("interaction_enabled", false):
		add_to_group("interactable")
	position = config.get("position", position)

	var texture: Texture2D = config.get("texture")
	var source_size: Vector2 = config.get("source_size", Vector2(1.0, 1.0))
	var draw_width: float = config.get("draw_width", source_size.x)
	var default_anchor := Vector2(source_size.x * 0.5, source_size.y)
	var visual_base_anchor: Vector2 = config.get("visual_base_anchor", config.get("anchor", default_anchor))
	var sprite_offset: Vector2 = config.get("sprite_offset", Vector2.ZERO)
	var scale_factor: float = draw_width / max(1.0, source_size.x)

	sprite.texture = texture
	sprite.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	sprite.centered = false
	sprite.scale = Vector2(scale_factor, scale_factor)
	sprite.position = -visual_base_anchor * scale_factor + sprite_offset
	_configure_projection_details(config.get("projection_details", []), texture, visual_base_anchor, scale_factor, sprite_offset)
	_visual_base_width = config.get("visual_base_width", draw_width * 0.86)
	var default_visual_bounds := Rect2(sprite.position, source_size * scale_factor)
	_visual_bounds = config.get("visual_bounds", default_visual_bounds)
	_lot_bounds = config.get("lot_bounds", config.get("lot_rect", _visual_bounds))

	var collision_shape := RectangleShape2D.new()
	if config.has("collision_footprint") or config.has("collision_rect"):
		_collision_footprint = config.get("collision_footprint", config.get("collision_rect", Rect2(Vector2(-48.0, -32.0), Vector2(96.0, 32.0))))
		collision_shape.size = _collision_footprint.size
		body_collision.position = _collision_footprint.position + _collision_footprint.size * 0.5
	else:
		collision_shape.size = config.get("collision_size", Vector2(96.0, 32.0))
		body_collision.position = config.get("collision_offset", Vector2.ZERO)
		_collision_footprint = Rect2(body_collision.position - collision_shape.size * 0.5, collision_shape.size)
	body_collision.shape = collision_shape
	_ground_shadow_size = config.get("shadow_size", Vector2(max(collision_shape.size.x * 1.12, draw_width * 0.42), max(18.0, collision_shape.size.y * 0.58)))
	_ground_shadow_offset = config.get("shadow_offset", Vector2(0.0, -6.0))

	var interaction_shape := RectangleShape2D.new()
	var frontage_offset: Vector2 = config.get("frontage_offset", config.get("interaction_offset", Vector2(0.0, 22.0)))
	_door_anchor_point = config.get("door_anchor", config.get("door_offset", frontage_offset))
	if config.has("interaction_zone"):
		_interaction_zone = config["interaction_zone"]
		interaction_shape.size = _interaction_zone.size
		interaction_collision.position = _interaction_zone.position + _interaction_zone.size * 0.5
	else:
		interaction_shape.size = config.get("interaction_size", Vector2(72.0, 40.0))
		interaction_collision.position = config.get("interaction_offset", frontage_offset)
		_interaction_zone = Rect2(interaction_collision.position - interaction_shape.size * 0.5, interaction_shape.size)
	interaction_collision.shape = interaction_shape
	door_marker.position = _door_anchor_point
	_foot_anchor_point = config.get("foot_anchor", Vector2.ZERO)
	foot_anchor.position = _foot_anchor_point
	frontage_marker.position = frontage_offset
	_y_sort_point = config.get("y_sort_anchor", config.get("y_sort_offset", Vector2.ZERO))
	y_sort_anchor.position = _y_sort_point
	_ground_contact_rect = config.get("ground_contact_rect", Rect2(Vector2(-_visual_base_width * 0.5, -4.0), Vector2(_visual_base_width, 8.0)))
	debug_overlay.refresh()
	set_debug_overlay(BUILD_INFO.DEBUG_OVERLAYS_DEFAULT)
	queue_redraw()

func get_foot_anchor() -> Vector2:
	return global_position

func set_debug_overlay(enabled: bool) -> void:
	var effective_enabled := enabled and BUILD_INFO.DEBUG_OVERLAY_TOGGLE_ENABLED
	if debug_overlay.has_method("set_debug_enabled"):
		debug_overlay.set_debug_enabled(effective_enabled)
	else:
		debug_overlay.visible = effective_enabled

func set_debug_label_detail(enabled: bool) -> void:
	if debug_overlay.has_method("set_label_detail"):
		debug_overlay.set_label_detail(enabled)

func get_interaction_label() -> String:
	if not interaction_label.is_empty():
		return interaction_label
	return "Press E to inspect " + display_name

func get_interaction_position() -> Vector2:
	if door_marker:
		return door_marker.global_position
	return global_position

func get_prompt_text() -> String:
	var label := get_interaction_label()
	var enter_prefix := "Press E to enter "
	var inspect_prefix := "Press E to inspect "
	if label.begins_with(enter_prefix):
		return "E: Enter - " + label.substr(enter_prefix.length())
	if label.begins_with(inspect_prefix):
		return "E: Inspect - " + label.substr(inspect_prefix.length())
	return label

func prompt_ux_contract() -> Dictionary:
	return {
		"phase": "G-9",
		"prompt_style": "compact_diegetic_action_name_no_debug_marker",
		"get_interaction_label_keeps_validator_compatibility": get_interaction_label().begins_with("Press E"),
		"get_prompt_text_hides_press_e_copy": get_prompt_text().find("Press E") < 0,
		"prompt_text": get_prompt_text(),
	}

func is_player_in_interaction_area(world_position: Vector2) -> bool:
	if _interaction_zone.size.x <= 0.0 or _interaction_zone.size.y <= 0.0:
		return global_position.distance_to(world_position) <= 42.0
	var local_point := to_local(world_position)
	return _interaction_zone.grow(4.0).has_point(local_point)

func interact() -> String:
	if can_player_enter():
		if not unavailable_message.is_empty():
			return unavailable_message
		return "%s will be enterable in G-4.15." % display_name
	if access_rule == "private" or access_rule == "owner_only_future":
		if not locked_message.is_empty():
			return locked_message
		return "This residence is private."
	if not unavailable_message.is_empty():
		return unavailable_message
	if not locked_message.is_empty():
		return locked_message
	return "%s is not open yet." % display_name

func can_player_enter() -> bool:
	return is_enterable and access_rule == "public" and not interior_scene.is_empty()

func is_proof_street_building() -> bool:
	return proof_street

func has_seating_metadata() -> bool:
	return _visual_base_width > 0.0 and body_collision.shape is RectangleShape2D and _lot_bounds.size.x > 0.0 and _lot_bounds.size.y > 0.0 and _interaction_zone.size.x > 0.0 and _interaction_zone.size.y > 0.0 and _ground_contact_rect.size.x > 0.0 and _ground_contact_rect.size.y > 0.0 and frontage_marker != null and door_marker != null and y_sort_anchor != null

func uses_normalized_definition() -> bool:
	return definition_normalized and definition_id != "" and district_role != ""

func is_harbor_integrated() -> bool:
	return harbor_integrated

func get_visual_base_width() -> float:
	return _visual_base_width

func get_visual_bounds() -> Rect2:
	return _visual_bounds

func get_collision_footprint() -> Rect2:
	return _collision_footprint

func get_interaction_zone() -> Rect2:
	return _interaction_zone

func get_lot_bounds() -> Rect2:
	return _lot_bounds

func get_foot_anchor_local() -> Vector2:
	return _foot_anchor_point

func get_door_anchor_local() -> Vector2:
	return _door_anchor_point

func get_door_anchor() -> Vector2:
	return get_interaction_position()

func get_y_sort_anchor_local() -> Vector2:
	return _y_sort_point

func get_ground_contact_rect() -> Rect2:
	return _ground_contact_rect

func get_projection_detail_names() -> Array[String]:
	return _projection_detail_names.duplicate()

func _configure_projection_details(details: Array, source_texture: Texture2D, visual_base_anchor: Vector2, scale_factor: float, sprite_offset: Vector2) -> void:
	_projection_detail_names.clear()
	for child in get_children():
		if String(child.name).begins_with("Projection_"):
			remove_child(child)
			child.queue_free()

	var source_atlas := source_texture as AtlasTexture
	if source_atlas == null:
		return

	for raw_detail in details:
		if not raw_detail is Dictionary:
			continue
		var detail: Dictionary = raw_detail
		var source_rect: Rect2 = detail.get("source_rect", Rect2())
		if source_rect.size.x <= 0.0 or source_rect.size.y <= 0.0:
			continue

		var projection_texture := AtlasTexture.new()
		projection_texture.atlas = source_atlas.atlas
		projection_texture.region = Rect2(source_atlas.region.position + source_rect.position, source_rect.size)
		projection_texture.filter_clip = true

		var projection_sprite := Sprite2D.new()
		var detail_id := String(detail.get("id", "frontage_detail"))
		projection_sprite.name = "Projection_" + detail_id
		projection_sprite.texture = projection_texture
		projection_sprite.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		projection_sprite.centered = false
		projection_sprite.scale = Vector2(scale_factor, scale_factor)
		projection_sprite.position = (source_rect.position - visual_base_anchor) * scale_factor + sprite_offset
		projection_sprite.z_index = int(detail.get("z_index", 12))
		projection_sprite.z_as_relative = false
		add_child(projection_sprite)
		_projection_detail_names.append(detail_id)

func _draw() -> void:
	draw_set_transform(_ground_shadow_offset, 0.0, Vector2(_ground_shadow_size.x / 32.0, _ground_shadow_size.y / 32.0))
	draw_circle(Vector2.ZERO, 16.0, Color(0, 0, 0, 0.20))
	draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
