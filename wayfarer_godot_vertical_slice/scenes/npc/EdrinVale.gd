extends Node2D

@export var npc_name := "Edrin Vale"
@export_multiline var dialogue := "Edrin Vale: Newport has a waterfront, a civic spine, and streets worth walking now."

const NPC_ATLAS_PATH := "res://art_pipeline/player_identity/atlases/newport_npc_atelier_g422r_v1.png"
const G8_CHARACTER_MOTION_FOUNDATION_PASS := "G-8"
const NPC_FRAME_SIZE := Vector2i(256, 256)
const EDRIN_FRAME_INDEX := 2
const NPC_VISUAL_SCALE := 0.32
const NPC_FOOT_ANCHOR := Vector2(128.0, 244.0)
const NPC_VISUAL_OFFSET := Vector2(0.0, -37.12)
const NPC_ROUTE_WALKING_ENABLED := false
const NPC_STATIONARY_UNTIL_WALK_SHEET := true
const NPC_MOVEMENT_SPEED := 0.0
const NPC_WALK_ANIMATION_FPS := 0.0
const NPC_PAUSE_BEHAVIOR := "stationary_idle_until_dedicated_walk_sheet_no_static_drift"
const NPC_DIRECTIONS := ["down", "up", "left", "right"]
const NPC_MOTION_STATE_NAMES := [
	"idle_down",
	"idle_up",
	"idle_left",
	"idle_right",
	"walk_down",
	"walk_up",
	"walk_left",
	"walk_right",
]

@onready var ground_shadow: Polygon2D = $GroundShadow
@onready var visual_sprite: AnimatedSprite2D = $Visual

var _facing_direction := "down"
var _current_visual_animation := ""

func _ready() -> void:
	add_to_group("interactable")
	_configure_ground_shadow()
	_configure_visual_sprite()

func get_interaction_label() -> String:
	return "E: Speak with " + npc_name

func interact() -> String:
	return dialogue

func set_review_motion_state(direction: String, moving: bool, frame_index := 0) -> void:
	if NPC_DIRECTIONS.has(direction):
		_facing_direction = direction
	var should_walk := moving and NPC_ROUTE_WALKING_ENABLED
	var animation_name := ("walk_" if should_walk else "idle_") + _facing_direction
	_play_visual_animation(animation_name)
	if visual_sprite and visual_sprite.sprite_frames and visual_sprite.sprite_frames.has_animation(animation_name):
		var frame_count := visual_sprite.sprite_frames.get_frame_count(animation_name)
		visual_sprite.frame = clampi(frame_index, 0, maxi(0, frame_count - 1))
		if should_walk:
			visual_sprite.pause()

func is_route_walking_enabled() -> bool:
	return NPC_ROUTE_WALKING_ENABLED

func motion_foundation_contract() -> Dictionary:
	return {
		"phase": G8_CHARACTER_MOTION_FOUNDATION_PASS,
		"states": NPC_MOTION_STATE_NAMES.duplicate(),
		"foot_anchor": NPC_FOOT_ANCHOR,
		"visual_offset": NPC_VISUAL_OFFSET,
		"route_walking_enabled": NPC_ROUTE_WALKING_ENABLED,
		"stationary_until_walk_sheet": NPC_STATIONARY_UNTIL_WALK_SHEET,
		"movement_speed": NPC_MOVEMENT_SPEED,
		"walk_animation_fps": NPC_WALK_ANIMATION_FPS,
		"pause_behavior": NPC_PAUSE_BEHAVIOR,
	}

func get_interaction_position() -> Vector2:
	return global_position

func _configure_ground_shadow() -> void:
	if ground_shadow == null:
		push_error("EdrinVale GroundShadow Polygon2D is missing.")
		return
	ground_shadow.position = Vector2(0.0, 1.0)
	ground_shadow.color = Color(0.0, 0.0, 0.0, 0.16)
	ground_shadow.z_as_relative = true
	ground_shadow.z_index = 0

func _configure_visual_sprite() -> void:
	if visual_sprite == null:
		push_error("EdrinVale Visual AnimatedSprite2D is missing.")
		return
	var atlas := ResourceLoader.load(NPC_ATLAS_PATH, "Texture2D") as Texture2D
	if atlas == null:
		push_error("Failed to load G-4.22R Newport NPC atlas: " + NPC_ATLAS_PATH)
		return
	var sprite_frames := SpriteFrames.new()
	if sprite_frames.has_animation("default"):
		sprite_frames.remove_animation("default")
	var frame := _atlas_frame(atlas)
	for raw_direction in NPC_DIRECTIONS:
		var direction := String(raw_direction)
		var idle_animation := "idle_" + direction
		sprite_frames.add_animation(idle_animation)
		sprite_frames.set_animation_loop(idle_animation, true)
		sprite_frames.set_animation_speed(idle_animation, 1.0)
		sprite_frames.add_frame(idle_animation, frame, 1.0)
		var walk_animation := "walk_" + direction
		sprite_frames.add_animation(walk_animation)
		sprite_frames.set_animation_loop(walk_animation, true)
		sprite_frames.set_animation_speed(walk_animation, 1.0)
		sprite_frames.add_frame(walk_animation, frame, 1.0)
	visual_sprite.sprite_frames = sprite_frames
	visual_sprite.centered = true
	visual_sprite.position = NPC_VISUAL_OFFSET
	visual_sprite.scale = Vector2.ONE * NPC_VISUAL_SCALE
	visual_sprite.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	visual_sprite.z_as_relative = true
	visual_sprite.z_index = 1
	_play_visual_animation("idle_down")

func _atlas_frame(atlas: Texture2D) -> AtlasTexture:
	var frame := AtlasTexture.new()
	frame.atlas = atlas
	frame.region = Rect2(EDRIN_FRAME_INDEX * NPC_FRAME_SIZE.x, 0, NPC_FRAME_SIZE.x, NPC_FRAME_SIZE.y)
	frame.filter_clip = true
	return frame

func _play_visual_animation(animation_name: String) -> void:
	if visual_sprite == null or visual_sprite.sprite_frames == null:
		return
	if not visual_sprite.sprite_frames.has_animation(animation_name):
		return
	if _current_visual_animation == animation_name and visual_sprite.is_playing():
		return
	_current_visual_animation = animation_name
	visual_sprite.play(animation_name)
	if NPC_STATIONARY_UNTIL_WALK_SHEET:
		visual_sprite.pause()
