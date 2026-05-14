extends Node2D
class_name BuildingDebugOverlay

const VISUAL_OUTLINE := Color(0.95, 0.95, 0.30, 0.64)
const LOT_FILL := Color(1.0, 0.68, 0.24, 0.10)
const LOT_OUTLINE := Color(1.0, 0.68, 0.24, 0.78)
const COLLISION_FILL := Color(1.0, 0.35, 0.35, 0.22)
const COLLISION_OUTLINE := Color(1.0, 0.20, 0.20, 0.95)
const INTERACTION_FILL := Color(0.35, 0.85, 1.0, 0.25)
const INTERACTION_OUTLINE := Color(0.25, 0.70, 1.0, 0.95)
const ANCHOR_COLOR := Color(0.10, 1.0, 0.45, 1.0)
const DOOR_COLOR := Color(1.0, 0.85, 0.30, 1.0)
const FRONTAGE_COLOR := Color(0.15, 0.85, 1.0, 1.0)
const YSORT_COLOR := Color(1.0, 0.35, 1.0, 1.0)
const LABEL_COLOR := Color(1, 1, 1, 0.95)

var _debug_enabled := false

func _ready() -> void:
	z_index = 100
	set_debug_enabled(false)

func refresh() -> void:
	if _debug_enabled:
		queue_redraw()

func set_debug_enabled(enabled: bool) -> void:
	_debug_enabled = enabled
	visible = enabled
	queue_redraw()

func _draw() -> void:
	if not _debug_enabled:
		return

	var building := get_parent()
	if not (building is Node2D):
		return

	var visual_rect := Rect2()
	if building.has_method("get_visual_bounds"):
		visual_rect = building.get_visual_bounds()
	else:
		var sprite := building.get_node_or_null("Sprite2D") as Sprite2D
		if sprite and sprite.texture:
			var region_size: Vector2
			if sprite.texture is AtlasTexture:
				region_size = (sprite.texture as AtlasTexture).region.size
			else:
				region_size = sprite.texture.get_size()
			visual_rect = Rect2(sprite.position, region_size * sprite.scale)
	if visual_rect.size.x > 0.0 and visual_rect.size.y > 0.0:
		_draw_rect_outline(visual_rect, VISUAL_OUTLINE, 1.0)
		_draw_text_tag("visual_bounds", visual_rect.position + Vector2(4.0, 14.0), VISUAL_OUTLINE)

	if building.has_method("get_lot_bounds"):
		var lot_rect: Rect2 = building.get_lot_bounds()
		if lot_rect.size.x > 0.0 and lot_rect.size.y > 0.0:
			draw_rect(lot_rect, LOT_FILL, true)
			_draw_rect_outline(lot_rect, LOT_OUTLINE, 1.2)
			_draw_text_tag("lot_bounds", lot_rect.position + Vector2(4.0, 14.0), LOT_OUTLINE)

	var body_collision := building.get_node_or_null("Body/CollisionShape2D") as CollisionShape2D
	if body_collision and body_collision.shape is RectangleShape2D:
		var rect_shape := body_collision.shape as RectangleShape2D
		var rect := Rect2(body_collision.position - rect_shape.size * 0.5, rect_shape.size)
		draw_rect(rect, COLLISION_FILL, true)
		_draw_rect_outline(rect, COLLISION_OUTLINE, 2.0)
		_draw_text_tag("collision_footprint", rect.position + Vector2(4.0, 13.0), COLLISION_OUTLINE)

	var interaction_collision := building.get_node_or_null("InteractionArea/CollisionShape2D") as CollisionShape2D
	if interaction_collision and interaction_collision.shape is RectangleShape2D:
		var rect_shape := interaction_collision.shape as RectangleShape2D
		var rect := Rect2(interaction_collision.position - rect_shape.size * 0.5, rect_shape.size)
		draw_rect(rect, INTERACTION_FILL, true)
		_draw_rect_outline(rect, INTERACTION_OUTLINE, 2.0)
		_draw_text_tag("interaction_zone", rect.position + Vector2(4.0, 13.0), INTERACTION_OUTLINE)

	var foot_anchor := building.get_node_or_null("FootAnchor") as Marker2D
	if foot_anchor:
		var visual_base_width := 96.0
		if building.has_method("get_visual_base_width"):
			visual_base_width = building.get_visual_base_width()
		draw_line(Vector2(-visual_base_width * 0.5, 0.0), Vector2(visual_base_width * 0.5, 0.0), ANCHOR_COLOR, 2.0)
		_draw_cross(foot_anchor.position, 8.0, ANCHOR_COLOR, 2.0)
		draw_circle(foot_anchor.position, 3.0, ANCHOR_COLOR)
		_draw_text_tag("foot_anchor", foot_anchor.position + Vector2(8.0, -7.0), ANCHOR_COLOR)

	var door_marker := building.get_node_or_null("DoorMarker") as Marker2D
	if door_marker:
		draw_circle(door_marker.position, 4.0, DOOR_COLOR)

	var frontage_marker := building.get_node_or_null("FrontageMarker") as Marker2D
	if frontage_marker:
		_draw_diamond(frontage_marker.position, 6.0, FRONTAGE_COLOR)
		draw_line(Vector2(frontage_marker.position.x - 18.0, frontage_marker.position.y), Vector2(frontage_marker.position.x + 18.0, frontage_marker.position.y), FRONTAGE_COLOR, 1.5)

	var y_sort_anchor := building.get_node_or_null("YSortAnchor") as Marker2D
	if y_sort_anchor:
		_draw_diamond(y_sort_anchor.position, 5.0, YSORT_COLOR)
		_draw_cross(y_sort_anchor.position, 10.0, YSORT_COLOR, 1.5)
		_draw_text_tag("y_sort", y_sort_anchor.position + Vector2(8.0, 13.0), YSORT_COLOR)

	var label := ""
	if building is Node:
		label = String(building.name)
	if label != "":
		var font := ThemeDB.fallback_font
		if font:
			draw_string(font, Vector2(-58, -8), label, HORIZONTAL_ALIGNMENT_LEFT,
				-1, 12, LABEL_COLOR)

func _draw_rect_outline(rect: Rect2, color: Color, width: float) -> void:
	var tl := rect.position
	var tr := rect.position + Vector2(rect.size.x, 0)
	var br := rect.position + rect.size
	var bl := rect.position + Vector2(0, rect.size.y)
	draw_line(tl, tr, color, width)
	draw_line(tr, br, color, width)
	draw_line(br, bl, color, width)
	draw_line(bl, tl, color, width)

func _draw_text_tag(text: String, at: Vector2, color: Color) -> void:
	var font := ThemeDB.fallback_font
	if font == null:
		return
	draw_string(font, at + Vector2(1.0, 1.0), text, HORIZONTAL_ALIGNMENT_LEFT,
		-1, 10, Color(0, 0, 0, 0.82))
	draw_string(font, at, text, HORIZONTAL_ALIGNMENT_LEFT,
		-1, 10, color.lightened(0.25))

func _draw_cross(at: Vector2, half: float, color: Color, width: float) -> void:
	draw_line(at + Vector2(-half, 0), at + Vector2(half, 0), color, width)
	draw_line(at + Vector2(0, -half), at + Vector2(0, half), color, width)

func _draw_diamond(at: Vector2, radius: float, color: Color) -> void:
	draw_colored_polygon(PackedVector2Array([
		at + Vector2(0, -radius),
		at + Vector2(radius, 0),
		at + Vector2(0, radius),
		at + Vector2(-radius, 0),
	]), color)
