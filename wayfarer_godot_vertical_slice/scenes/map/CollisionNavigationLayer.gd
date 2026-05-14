extends Node2D

const NEWPORT_TOWN := preload("res://scripts/NewportTownBlueprint.gd")
const TILE := NEWPORT_TOWN.TILE

const DETAIL_FILL := Color(1.0, 0.42, 0.16, 0.24)
const DETAIL_OUTLINE := Color(1.0, 0.42, 0.16, 0.95)
const WATER_FILL := Color(0.25, 0.55, 1.0, 0.12)
const WATER_OUTLINE := Color(0.25, 0.55, 1.0, 0.58)
const BOUNDARY_OUTLINE := Color(1.0, 0.15, 0.15, 0.35)
const PROBE_COLOR := Color(0.20, 1.0, 0.70, 1.0)
const LABEL_COLOR := Color(1.0, 0.96, 0.70, 0.95)
const OWNER_LABEL_SIZE := 8
const PROBE_LABEL_SIZE := 8
const MAX_OWNER_LABEL_CHARS := 28

var _debug_overlay_enabled := false
var _debug_bodies: Array = []

func _ready() -> void:
	set_debug_overlay(false)
	_add_world_edge_collision()
	_add_water_collision()
	_add_detail_blockers()

func _add_body(rect: Rect2, label: String) -> void:
	var body := StaticBody2D.new()
	body.name = label
	body.collision_layer = 1
	body.collision_mask = 0
	add_child(body)

	var shape := CollisionShape2D.new()
	var rectangle := RectangleShape2D.new()
	rectangle.size = rect.size
	shape.shape = rectangle
	shape.position = rect.position + rect.size * 0.5
	body.add_child(shape)
	_debug_bodies.append({"rect": rect, "label": label})

func set_debug_overlay(enabled: bool) -> void:
	_debug_overlay_enabled = enabled
	visible = enabled
	queue_redraw()

func _draw() -> void:
	if not _debug_overlay_enabled:
		return
	for entry in _debug_bodies:
		var rect: Rect2 = entry["rect"]
		var label := String(entry["label"])
		var fill := DETAIL_FILL
		var outline := DETAIL_OUTLINE
		if label.begins_with("HarborWater_"):
			fill = WATER_FILL
			outline = WATER_OUTLINE
		elif label.ends_with("Boundary"):
			fill = Color.TRANSPARENT
			outline = BOUNDARY_OUTLINE
		if fill.a > 0.0:
			draw_rect(rect, fill, true)
		draw_rect(rect, outline, false, 1.4)
		if label.begins_with("DetailBlocker_"):
			_draw_text_tag(_owner_label(label), rect.position + Vector2(2.0, -2.0), DETAIL_OUTLINE, OWNER_LABEL_SIZE)
	for probe in NEWPORT_TOWN.route_debug_probes():
		var position: Vector2 = probe["position"]
		draw_circle(position, 5.0, PROBE_COLOR)
		draw_arc(position, 10.0, 0.0, TAU, 24, PROBE_COLOR, 1.5)
		_draw_text_tag("probe:" + _probe_label(probe), position + Vector2(8.0, -8.0), PROBE_COLOR, PROBE_LABEL_SIZE)

func _add_world_edge_collision() -> void:
	var world_size := NEWPORT_TOWN.WORLD_SIZE
	_add_body(Rect2(-TILE, -TILE, TILE, world_size.y + TILE * 2), "WestBoundary")
	_add_body(Rect2(world_size.x, -TILE, TILE, world_size.y + TILE * 2), "EastBoundary")
	_add_body(Rect2(-TILE, -TILE, world_size.x + TILE * 2, TILE), "NorthBoundary")
	_add_body(Rect2(-TILE, world_size.y, world_size.x + TILE * 2, TILE), "SouthBoundary")

func _add_water_collision() -> void:
	for tile in NEWPORT_TOWN.water_collision_tiles():
		_add_body(Rect2(tile.x * TILE, tile.y * TILE, TILE, TILE), "HarborWater_%d_%d" % [tile.x, tile.y])

func _add_detail_blockers() -> void:
	for blocker_config in NEWPORT_TOWN.detail_blockers():
		var blocker: Dictionary = blocker_config
		_add_body(blocker["rect"], "DetailBlocker_" + String(blocker["id"]))

func _draw_text_tag(text: String, at: Vector2, color: Color, font_size: int) -> void:
	var font := ThemeDB.fallback_font
	if font == null:
		return
	draw_string(font, at + Vector2(1.0, 1.0), text, HORIZONTAL_ALIGNMENT_LEFT,
		-1, font_size, Color(0, 0, 0, 0.84))
	draw_string(font, at, text, HORIZONTAL_ALIGNMENT_LEFT,
		-1, font_size, color.lightened(0.25) if color != Color.TRANSPARENT else LABEL_COLOR)

func _owner_label(label: String) -> String:
	var owner := "prop:" + label.trim_prefix("DetailBlocker_")
	if owner.length() <= MAX_OWNER_LABEL_CHARS:
		return owner
	return owner.left(MAX_OWNER_LABEL_CHARS - 3) + "..."

func _probe_label(probe: Dictionary) -> String:
	return String(probe.get("label", probe.get("id", "")))
