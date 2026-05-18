extends CharacterBody2D

signal dialogue_triggered(text: String)

const NEWPORT_TOWN := preload("res://scripts/NewportTownBlueprint.gd")
const WORLD_LIMIT_LEFT := 0
const WORLD_LIMIT_TOP := 0
const WORLD_LIMIT_RIGHT := 1600
const WORLD_LIMIT_BOTTOM := 1024
const PLAYER_SPRITE_ATLAS_PATH := "res://art_pipeline/player_identity/atlases/player_wayfarer_atelier_g422r_v1.png"
const G8_CHARACTER_MOTION_FOUNDATION_PASS := "G-8"
const PLAYER_FRAME_SIZE := Vector2i(256, 256)
const PLAYER_FOOT_ANCHOR := Vector2(128.0, 244.0)
const PLAYER_VISUAL_SCALE := 0.32
const PLAYER_VISUAL_OFFSET := Vector2(0.0, -37.12)
const PLAYER_GROUND_SHADOW_SIZE := Vector2(34.0, 8.0)
const PLAYER_GROUND_SHADOW_ALPHA := 0.17
const PLAYER_WALK_ANIMATION_FPS := 7.0
const PLAYER_MOVEMENT_SPEED_SYNC := 185.0
const G9_INTERACTION_UX_PASS := "G-9"
const PROMPT_MAX_WIDTH := 160.0
const PROMPT_FONT_SIZE := 12
const PROMPT_STYLE := "compact_diegetic_action_name_no_debug_marker"
const PLAYER_DIRECTIONS := ["down", "up", "left", "right"]
const PLAYER_FRAME_VARIANTS := ["idle", "walk_a", "walk_b"]
const PLAYER_MOTION_STATE_NAMES := [
	"idle_down",
	"idle_up",
	"idle_left",
	"idle_right",
	"walk_down",
	"walk_up",
	"walk_left",
	"walk_right",
]

@export var speed := 185.0
@export var interaction_radius := 44.0

@onready var ground_shadow: Polygon2D = $GroundShadow
@onready var visual_sprite: AnimatedSprite2D = $Visual
@onready var camera: Camera2D = $Camera2D
@onready var prompt_label: Label = $PromptLabel

var _current_target: Node = null
var _interact_was_down := false
var _world_limits := Rect2(Vector2(WORLD_LIMIT_LEFT, WORLD_LIMIT_TOP), Vector2(WORLD_LIMIT_RIGHT, WORLD_LIMIT_BOTTOM))
var _facing_direction := "down"
var _current_visual_animation := ""

func _ready() -> void:
	add_to_group("player")
	_configure_ground_shadow()
	_configure_visual_sprite()
	_configure_camera()
	prompt_label.z_as_relative = false
	prompt_label.z_index = 100
	prompt_label.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	prompt_label.offset_left = -PROMPT_MAX_WIDTH * 0.5
	prompt_label.offset_top = -66.0
	prompt_label.offset_right = PROMPT_MAX_WIDTH * 0.5
	prompt_label.offset_bottom = -50.0
	prompt_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	prompt_label.clip_text = false
	prompt_label.add_theme_font_size_override("font_size", PROMPT_FONT_SIZE)
	prompt_label.add_theme_color_override("font_color", Color(0.98, 0.86, 0.58, 0.96))
	prompt_label.add_theme_color_override("font_outline_color", Color(0.055, 0.035, 0.018, 0.94))
	prompt_label.add_theme_constant_override("outline_size", 2)

func _physics_process(_delta: float) -> void:
	var input := _movement_axis()
	velocity = input.normalized() * speed
	_update_visual_animation(input)
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

func set_review_visual_state(direction: String, moving: bool, frame_index := 0) -> void:
	if PLAYER_DIRECTIONS.has(direction):
		_facing_direction = direction
	var animation_name := ("walk_" if moving else "idle_") + _facing_direction
	_play_visual_animation(animation_name)
	if visual_sprite and visual_sprite.sprite_frames and visual_sprite.sprite_frames.has_animation(animation_name):
		var frame_count := visual_sprite.sprite_frames.get_frame_count(animation_name)
		visual_sprite.frame = clampi(frame_index, 0, maxi(0, frame_count - 1))
		if moving:
			visual_sprite.pause()

func character_motion_contract() -> Dictionary:
	return {
		"phase": G8_CHARACTER_MOTION_FOUNDATION_PASS,
		"states": PLAYER_MOTION_STATE_NAMES.duplicate(),
		"foot_anchor": PLAYER_FOOT_ANCHOR,
		"visual_offset": PLAYER_VISUAL_OFFSET,
		"ground_shadow_size": PLAYER_GROUND_SHADOW_SIZE,
		"movement_speed": speed,
		"movement_speed_synced_to_animation": absf(speed - PLAYER_MOVEMENT_SPEED_SYNC) < 0.01,
		"walk_animation_fps": PLAYER_WALK_ANIMATION_FPS,
		"pause_behavior": "idle state holds the last facing direction when movement input stops",
	}

func prompt_ux_contract() -> Dictionary:
	return {
		"phase": G9_INTERACTION_UX_PASS,
		"style": PROMPT_STYLE,
		"max_width": PROMPT_MAX_WIDTH,
		"font_size": PROMPT_FONT_SIZE,
		"forbidden_prefix": "Press E",
		"normal_play_debug_marker_free": true,
		"targeting_rule": "nearest_interactable_with_compact_action_name_copy",
	}

func _configure_ground_shadow() -> void:
	if ground_shadow == null:
		push_error("Player GroundShadow Polygon2D is missing.")
		return
	var half_w := PLAYER_GROUND_SHADOW_SIZE.x * 0.5
	var half_h := PLAYER_GROUND_SHADOW_SIZE.y * 0.5
	ground_shadow.polygon = PackedVector2Array([
		Vector2(-half_w, -1.0),
		Vector2(-half_w * 0.55, -half_h),
		Vector2(0.0, -half_h - 1.0),
		Vector2(half_w * 0.55, -half_h),
		Vector2(half_w, -1.0),
		Vector2(half_w * 0.55, half_h),
		Vector2(0.0, half_h + 1.0),
		Vector2(-half_w * 0.55, half_h),
	])
	ground_shadow.position = Vector2(0.0, 1.0)
	ground_shadow.color = Color(0.0, 0.0, 0.0, PLAYER_GROUND_SHADOW_ALPHA)
	ground_shadow.z_as_relative = true
	ground_shadow.z_index = 0

func _configure_visual_sprite() -> void:
	if visual_sprite == null:
		push_error("Player Visual AnimatedSprite2D is missing.")
		return

	var atlas := ResourceLoader.load(PLAYER_SPRITE_ATLAS_PATH, "Texture2D") as Texture2D
	if atlas == null:
		push_error("Failed to load G-4.22R player sprite atlas: " + PLAYER_SPRITE_ATLAS_PATH)
		return

	var sprite_frames := SpriteFrames.new()
	if sprite_frames.has_animation("default"):
		sprite_frames.remove_animation("default")
	for raw_direction in PLAYER_DIRECTIONS:
		var direction := String(raw_direction)
		var idle_animation := "idle_" + direction
		sprite_frames.add_animation(idle_animation)
		sprite_frames.set_animation_loop(idle_animation, true)
		sprite_frames.set_animation_speed(idle_animation, 1.0)
		sprite_frames.add_frame(idle_animation, _atlas_frame(atlas, direction, "idle"), 1.0)

		var walk_animation := "walk_" + direction
		sprite_frames.add_animation(walk_animation)
		sprite_frames.set_animation_loop(walk_animation, true)
		sprite_frames.set_animation_speed(walk_animation, PLAYER_WALK_ANIMATION_FPS)
		for raw_variant in ["idle", "walk_a", "idle", "walk_b"]:
			var variant := String(raw_variant)
			sprite_frames.add_frame(walk_animation, _atlas_frame(atlas, direction, variant), 1.0)

	visual_sprite.sprite_frames = sprite_frames
	visual_sprite.position = PLAYER_VISUAL_OFFSET
	visual_sprite.scale = Vector2.ONE * PLAYER_VISUAL_SCALE
	visual_sprite.centered = true
	visual_sprite.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	visual_sprite.z_as_relative = true
	visual_sprite.z_index = 1
	_play_visual_animation("idle_down")

func _atlas_frame(atlas: Texture2D, direction: String, variant: String) -> AtlasTexture:
	var direction_index := PLAYER_DIRECTIONS.find(direction)
	var variant_index := PLAYER_FRAME_VARIANTS.find(variant)
	if direction_index < 0:
		direction_index = 0
	if variant_index < 0:
		variant_index = 0
	var frame := AtlasTexture.new()
	frame.atlas = atlas
	frame.region = Rect2(
		variant_index * PLAYER_FRAME_SIZE.x,
		direction_index * PLAYER_FRAME_SIZE.y,
		PLAYER_FRAME_SIZE.x,
		PLAYER_FRAME_SIZE.y
	)
	frame.filter_clip = true
	return frame

func _update_visual_animation(input: Vector2) -> void:
	if input.length_squared() > 0.01:
		_update_facing_direction(input)
		_play_visual_animation("walk_" + _facing_direction)
	else:
		_play_visual_animation("idle_" + _facing_direction)

func _update_facing_direction(input: Vector2) -> void:
	if absf(input.x) > absf(input.y):
		_facing_direction = "right" if input.x > 0.0 else "left"
	else:
		_facing_direction = "down" if input.y > 0.0 else "up"

func _play_visual_animation(animation_name: String) -> void:
	if visual_sprite == null or visual_sprite.sprite_frames == null:
		return
	if not visual_sprite.sprite_frames.has_animation(animation_name):
		return
	if _current_visual_animation == animation_name and visual_sprite.is_playing():
		return
	_current_visual_animation = animation_name
	visual_sprite.play(animation_name)

func _configure_camera() -> void:
	camera.enabled = true
	if NEWPORT_TOWN.G410_STARTER_HARBOR_TOWN:
		camera.zoom = Vector2(1.38, 1.38)
	elif NEWPORT_TOWN.G49_STREET_VIGNETTE:
		camera.zoom = Vector2(1.58, 1.58)
	elif NEWPORT_TOWN.G48_PROOF_STREET:
		camera.zoom = Vector2(1.34, 1.34)
	elif NEWPORT_TOWN.G47_CALIBRATION_MODE:
		camera.zoom = Vector2(0.88, 0.88)
	elif NEWPORT_TOWN.G46_PROOF_FRAME:
		camera.zoom = Vector2(1.82, 1.82)
	else:
		camera.zoom = Vector2(1.48, 1.48)
	camera.position = Vector2.ZERO
	if NEWPORT_TOWN.G410_STARTER_HARBOR_TOWN:
		camera.offset = Vector2(0, -70)
	elif NEWPORT_TOWN.G49_STREET_VIGNETTE:
		camera.offset = Vector2(0, -70)
	elif NEWPORT_TOWN.G48_PROOF_STREET:
		camera.offset = Vector2(0, -76)
	elif NEWPORT_TOWN.G47_CALIBRATION_MODE:
		camera.offset = Vector2(-130, -110)
	elif NEWPORT_TOWN.G46_PROOF_FRAME:
		camera.offset = Vector2(0, -86)
	else:
		camera.offset = Vector2(72, -26)
	camera.position_smoothing_enabled = true
	camera.position_smoothing_speed = 9.5 if (NEWPORT_TOWN.G410_STARTER_HARBOR_TOWN or NEWPORT_TOWN.G46_PROOF_FRAME or NEWPORT_TOWN.G47_CALIBRATION_MODE or NEWPORT_TOWN.G48_PROOF_STREET or NEWPORT_TOWN.G49_STREET_VIGNETTE) else 8.5
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
	var nearest_dist := 1.0e20
	for candidate in get_tree().get_nodes_in_group("interactable"):
		if not candidate is Node2D:
			continue
		var candidate_node := candidate as Node2D
		var dist := global_position.distance_to(_candidate_interaction_position(candidate_node))
		var is_in_zone := dist <= interaction_radius
		if candidate_node.has_method("is_player_in_interaction_area"):
			is_in_zone = bool(candidate_node.call("is_player_in_interaction_area", global_position))
		if is_in_zone and dist < nearest_dist:
			nearest = candidate
			nearest_dist = dist

	_current_target = nearest
	prompt_label.visible = _current_target != null
	if _current_target and _current_target.has_method("get_prompt_text"):
		prompt_label.text = _current_target.call("get_prompt_text")
	elif _current_target and _current_target.has_method("get_interaction_label"):
		prompt_label.text = _current_target.get_interaction_label()
	else:
		prompt_label.text = ""

func _candidate_interaction_position(candidate: Node2D) -> Vector2:
	if candidate.has_method("get_interaction_position"):
		return candidate.get_interaction_position()
	return candidate.global_position
