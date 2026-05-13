extends Node2D
class_name WayfarerBuilding

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
var _y_sort_point := Vector2.ZERO

func configure(config: Dictionary) -> void:
	building_id = config.get("id", name)
	display_name = config.get("display_name", building_id)
	definition_id = config.get("definition_id", building_id)
	district_role = config.get("district_role", "")
	proof_street = config.get("proof_street", false)
	harbor_integrated = config.get("harbor_integrated", false)
	definition_normalized = config.get("definition_normalized", false)
	name = building_id
	add_to_group("buildings")
	if proof_street:
		add_to_group("proof_street_buildings")
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
	_visual_base_width = config.get("visual_base_width", draw_width * 0.86)
	_visual_bounds = Rect2(sprite.position, source_size * scale_factor)
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
	if config.has("interaction_zone"):
		_interaction_zone = config["interaction_zone"]
		interaction_shape.size = _interaction_zone.size
		interaction_collision.position = _interaction_zone.position + _interaction_zone.size * 0.5
	else:
		interaction_shape.size = config.get("interaction_size", Vector2(72.0, 40.0))
		interaction_collision.position = config.get("interaction_offset", frontage_offset)
		_interaction_zone = Rect2(interaction_collision.position - interaction_shape.size * 0.5, interaction_shape.size)
	interaction_collision.shape = interaction_shape
	door_marker.position = config.get("door_offset", frontage_offset)
	_foot_anchor_point = config.get("foot_anchor", Vector2.ZERO)
	foot_anchor.position = _foot_anchor_point
	frontage_marker.position = frontage_offset
	_y_sort_point = config.get("y_sort_offset", Vector2.ZERO)
	y_sort_anchor.position = _y_sort_point
	debug_overlay.refresh()
	queue_redraw()

func get_foot_anchor() -> Vector2:
	return global_position

func set_debug_overlay(enabled: bool) -> void:
	debug_overlay.visible = enabled

func is_proof_street_building() -> bool:
	return proof_street

func has_seating_metadata() -> bool:
	return proof_street and _visual_base_width > 0.0 and body_collision.shape is RectangleShape2D and _lot_bounds.size.x > 0.0 and _lot_bounds.size.y > 0.0 and _interaction_zone.size.x > 0.0 and _interaction_zone.size.y > 0.0 and frontage_marker != null and y_sort_anchor != null

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

func get_y_sort_anchor_local() -> Vector2:
	return _y_sort_point

func _draw() -> void:
	draw_set_transform(_ground_shadow_offset, 0.0, Vector2(_ground_shadow_size.x / 32.0, _ground_shadow_size.y / 32.0))
	draw_circle(Vector2.ZERO, 16.0, Color(0, 0, 0, 0.20))
	draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
