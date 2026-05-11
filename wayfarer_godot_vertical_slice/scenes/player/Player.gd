extends CharacterBody2D

signal dialogue_triggered(text: String)

@export var speed := 185.0
@export var interaction_radius := 86.0

@onready var camera: Camera2D = $Camera2D
@onready var prompt_label: Label = $PromptLabel

var _current_target: Node = null
var _interact_was_down := false

func _ready() -> void:
	add_to_group("player")
	camera.make_current()
	queue_redraw()

func _physics_process(_delta: float) -> void:
	var input := Vector2.ZERO
	if Input.is_key_pressed(KEY_A) or Input.is_key_pressed(KEY_LEFT):
		input.x -= 1.0
	if Input.is_key_pressed(KEY_D) or Input.is_key_pressed(KEY_RIGHT):
		input.x += 1.0
	if Input.is_key_pressed(KEY_W) or Input.is_key_pressed(KEY_UP):
		input.y -= 1.0
	if Input.is_key_pressed(KEY_S) or Input.is_key_pressed(KEY_DOWN):
		input.y += 1.0

	velocity = input.normalized() * speed
	move_and_slide()
	_update_interaction_target()

	var interact_down := Input.is_key_pressed(KEY_E)
	if interact_down and not _interact_was_down and _current_target and _current_target.has_method("interact"):
		dialogue_triggered.emit(_current_target.interact())
	_interact_was_down = interact_down

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
	draw_circle(Vector2(0, -31), 12.0, Color("#f3d6a0"))
	draw_rect(Rect2(Vector2(-9, -20), Vector2(18, 26)), Color("#4a6fa3"), true)
	draw_rect(Rect2(Vector2(-11, 4), Vector2(22, 8)), Color("#2f4769"), true)
	draw_line(Vector2(-15, -10), Vector2(15, -10), Color("#d2b978"), 3.0)
