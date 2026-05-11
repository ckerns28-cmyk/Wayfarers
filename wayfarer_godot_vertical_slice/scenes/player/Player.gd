extends CharacterBody2D

signal dialogue_triggered(text: String)

const NEWPORT_TOWN := preload("res://scripts/NewportTownBlueprint.gd")
const WORLD_LIMIT_LEFT := 0
const WORLD_LIMIT_TOP := 0
const WORLD_LIMIT_RIGHT := 1600
const WORLD_LIMIT_BOTTOM := 1024

@export var speed := 185.0
@export var interaction_radius := 86.0

@onready var camera: Camera2D = $Camera2D
@onready var prompt_label: Label = $PromptLabel

var _current_target: Node = null
var _interact_was_down := false
var _world_limits := Rect2(Vector2(WORLD_LIMIT_LEFT, WORLD_LIMIT_TOP), Vector2(WORLD_LIMIT_RIGHT, WORLD_LIMIT_BOTTOM))

func _ready() -> void:
	add_to_group("player")
	_configure_camera()
	prompt_label.z_as_relative = false
	prompt_label.z_index = 100
	prompt_label.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	queue_redraw()

func _physics_process(_delta: float) -> void:
	var input := _movement_axis()
	velocity = input.normalized() * speed
	move_and_slide()
	_update_interaction_target()

	var interact_down := Input.is_key_pressed(KEY_E)
	if interact_down and not _interact_was_down and _current_target and _current_target.has_method("interact"):
		dialogue_triggered.emit(_current_target.interact())
	_interact_was_down = interact_down

func _notification(what: int) -> void:
	if what == NOTIFICATION_APPLICATION_FOCUS_OUT:
		velocity = Vector2.ZERO
		_interact_was_down = false

func configure_world_limits(world_rect: Rect2) -> void:
	_world_limits = world_rect
	if is_node_ready():
		_apply_camera_limits()
		camera.reset_smoothing()

func _configure_camera() -> void:
	camera.enabled = true
	if NEWPORT_TOWN.G47_CALIBRATION_MODE:
		camera.zoom = Vector2(0.88, 0.88)
	elif NEWPORT_TOWN.G46_PROOF_FRAME:
		camera.zoom = Vector2(1.82, 1.82)
	else:
		camera.zoom = Vector2(1.48, 1.48)
	camera.position = Vector2.ZERO
	if NEWPORT_TOWN.G47_CALIBRATION_MODE:
		camera.offset = Vector2(-130, -110)
	elif NEWPORT_TOWN.G46_PROOF_FRAME:
		camera.offset = Vector2(0, -86)
	else:
		camera.offset = Vector2(72, -26)
	camera.position_smoothing_enabled = true
	camera.position_smoothing_speed = 9.5 if (NEWPORT_TOWN.G46_PROOF_FRAME or NEWPORT_TOWN.G47_CALIBRATION_MODE) else 8.5
	_apply_camera_limits()
	camera.limit_smoothed = true
	camera.make_current()
	camera.reset_smoothing()

func _apply_camera_limits() -> void:
	camera.limit_left = int(_world_limits.position.x)
	camera.limit_top = int(_world_limits.position.y)
	camera.limit_right = int(_world_limits.position.x + _world_limits.size.x)
	camera.limit_bottom = int(_world_limits.position.y + _world_limits.size.y)

func _movement_axis() -> Vector2:
	var input := Vector2.ZERO
	if Input.is_key_pressed(KEY_A) or Input.is_key_pressed(KEY_LEFT):
		input.x -= 1.0
	if Input.is_key_pressed(KEY_D) or Input.is_key_pressed(KEY_RIGHT):
		input.x += 1.0
	if Input.is_key_pressed(KEY_W) or Input.is_key_pressed(KEY_UP):
		input.y -= 1.0
	if Input.is_key_pressed(KEY_S) or Input.is_key_pressed(KEY_DOWN):
		input.y += 1.0
	return input

func _update_interaction_target() -> void:
	var nearest: Node = null
	var nearest_dist := interaction_radius
	for candidate in get_tree().get_nodes_in_group("interactable"):
		if not candidate is Node2D:
			continue
		var dist := global_position.distance_to(candidate.global_position)
		if dist < nearest_dist:
			nearest = candidate
			nearest_dist = dist

	_current_target = nearest
	prompt_label.visible = _current_target != null
	if _current_target and _current_target.has_method("get_interaction_label"):
		prompt_label.text = _current_target.get_interaction_label()

func _draw() -> void:
	var visual_scale := 0.78 if NEWPORT_TOWN.G47_CALIBRATION_MODE else (1.12 if NEWPORT_TOWN.G46_PROOF_FRAME else 1.0)
	draw_set_transform(Vector2(0, 8 * visual_scale), 0.0, Vector2(1.45 * visual_scale, 0.42 * visual_scale))
	draw_circle(Vector2.ZERO, 10.0, Color(0, 0, 0, 0.24))
	draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
	draw_circle(Vector2(0, -31 * visual_scale), 12.0 * visual_scale, Color("#f3d6a0"))
	draw_rect(Rect2(Vector2(-9, -20) * visual_scale, Vector2(18, 26) * visual_scale), Color("#4a6fa3"), true)
	draw_rect(Rect2(Vector2(-11, 4) * visual_scale, Vector2(22, 8) * visual_scale), Color("#2f4769"), true)
	draw_line(Vector2(-15, -10) * visual_scale, Vector2(15, -10) * visual_scale, Color("#d2b978"), 3.0)
