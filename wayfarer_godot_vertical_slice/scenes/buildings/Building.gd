extends Node2D
class_name WayfarerBuilding

@onready var sprite: Sprite2D = $Sprite2D
@onready var body_collision: CollisionShape2D = $Body/CollisionShape2D
@onready var interaction_collision: CollisionShape2D = $InteractionArea/CollisionShape2D
@onready var door_marker: Marker2D = $DoorMarker
@onready var foot_anchor: Marker2D = $FootAnchor
@onready var debug_overlay: Node2D = $DebugOverlay

var building_id := ""
var display_name := ""
var _ground_shadow_width := 96.0
var _ground_shadow_depth := 22.0

func configure(config: Dictionary) -> void:
	building_id = config.get("id", name)
	display_name = config.get("display_name", building_id)
	name = building_id
	add_to_group("buildings")
	position = config.get("position", position)

	var texture: Texture2D = config.get("texture")
	var source_size: Vector2 = config.get("source_size", Vector2(1.0, 1.0))
	var draw_width: float = config.get("draw_width", source_size.x)
	var anchor: Vector2 = config.get("anchor", Vector2(source_size.x * 0.5, source_size.y))
	var scale_factor: float = draw_width / max(1.0, source_size.x)

	sprite.texture = texture
	sprite.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	sprite.centered = false
	sprite.scale = Vector2(scale_factor, scale_factor)
	sprite.position = -anchor * scale_factor

	var collision_shape := RectangleShape2D.new()
	collision_shape.size = config.get("collision_size", Vector2(96.0, 32.0))
	body_collision.shape = collision_shape
	body_collision.position = config.get("collision_offset", Vector2.ZERO)
	_ground_shadow_width = max(collision_shape.size.x * 1.12, draw_width * 0.42)
	_ground_shadow_depth = max(18.0, collision_shape.size.y * 0.58)

	var interaction_shape := RectangleShape2D.new()
	interaction_shape.size = config.get("interaction_size", Vector2(72.0, 40.0))
	interaction_collision.shape = interaction_shape
	interaction_collision.position = config.get("interaction_offset", Vector2(0.0, 16.0))
	door_marker.position = config.get("door_offset", Vector2.ZERO)
	foot_anchor.position = Vector2.ZERO
	debug_overlay.refresh()
	queue_redraw()

func get_foot_anchor() -> Vector2:
	return global_position

func set_debug_overlay(enabled: bool) -> void:
	debug_overlay.visible = enabled

func _draw() -> void:
	draw_set_transform(Vector2(0, -6), 0.0, Vector2(_ground_shadow_width / 32.0, _ground_shadow_depth / 32.0))
	draw_circle(Vector2.ZERO, 16.0, Color(0, 0, 0, 0.20))
	draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
