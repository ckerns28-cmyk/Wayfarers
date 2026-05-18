extends Node2D

const NPC_ATLAS_PATH := "res://art_pipeline/player_identity/atlases/newport_npc_atelier_g422r_v1.png"
const G8A_LIVING_NPC_POPULATION_PASS := "G-8A"
const NPC_FRAME_SIZE := Vector2i(256, 256)
const NPC_VISUAL_SCALE := 0.32
const NPC_FOOT_ANCHOR := Vector2(128.0, 244.0)
const NPC_VISUAL_OFFSET := Vector2(0.0, -37.12)
const NPC_ROUTE_WALKING_ENABLED := false
const NPC_STATIONARY_UNTIL_WALK_SHEET := true
const NPC_MOVEMENT_SPEED := 0.0
const NPC_WALK_ANIMATION_FPS := 0.0
const NPC_PAUSE_BEHAVIOR := "stationary_work_pose_until_dedicated_walk_sheets"
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
const NPC_FRAME_INDEX_BY_ASSET := {
	"npc_dockworker_atelier_g422r": 0,
	"npc_market_vendor_atelier_g422r": 1,
	"npc_civic_clerk_atelier_g422r": 2,
}

@onready var ground_shadow: Polygon2D = $GroundShadow
@onready var visual_sprite: AnimatedSprite2D = $Visual

var _config: Dictionary = {}
var _facing_direction := "down"
var _current_visual_animation := ""


func _ready() -> void:
	add_to_group("interactable")
	add_to_group("starter_village_npc")
	_configure_ground_shadow()
	_configure_visual_sprite()
	_apply_config()


func configure(config: Dictionary) -> void:
	_config = config.duplicate(true)
	if _config.has("position"):
		global_position = _config["position"]
	if is_node_ready():
		_apply_config()


func get_interaction_label() -> String:
	return "E: " + String(_config.get("display_name", "Newporter"))


func get_prompt_text() -> String:
	return get_interaction_label()


func interact() -> String:
	var speaker := String(_config.get("display_name", "Newporter"))
	var line := String(_config.get("dialogue_seed", "Keep your ears open by the harbor."))
	return "%s: %s" % [speaker, line]


func get_interaction_position() -> Vector2:
	return global_position


func is_player_in_interaction_area(player_position: Vector2) -> bool:
	return player_position.distance_to(global_position) <= 50.0


func set_review_motion_state(direction: String, moving: bool, frame_index := 0) -> void:
	if NPC_DIRECTIONS.has(direction):
		_facing_direction = direction
	var animation_name := ("walk_" if moving and NPC_ROUTE_WALKING_ENABLED else "idle_") + _facing_direction
	_play_visual_animation(animation_name)
	if visual_sprite and visual_sprite.sprite_frames and visual_sprite.sprite_frames.has_animation(animation_name):
		var frame_count := visual_sprite.sprite_frames.get_frame_count(animation_name)
		visual_sprite.frame = clampi(frame_index, 0, maxi(0, frame_count - 1))


func is_route_walking_enabled() -> bool:
	return NPC_ROUTE_WALKING_ENABLED


func npc_population_contract() -> Dictionary:
	return {
		"phase": G8A_LIVING_NPC_POPULATION_PASS,
		"id": String(_config.get("id", "")),
		"display_name": String(_config.get("display_name", "")),
		"role": String(_config.get("role", "")),
		"district": String(_config.get("district", "")),
		"station": String(_config.get("station", "")),
		"route_intent": String(_config.get("route_intent", "")),
		"idle_behavior": String(_config.get("idle_behavior", "")),
		"dialogue_seed": String(_config.get("dialogue_seed", "")),
		"quest_relevance": String(_config.get("quest_relevance", "")),
		"movement_policy": String(_config.get("movement_policy", NPC_PAUSE_BEHAVIOR)),
		"atelier_asset_id": String(_config.get("asset_id", "")),
	}


func motion_foundation_contract() -> Dictionary:
	return {
		"phase": G8A_LIVING_NPC_POPULATION_PASS,
		"states": NPC_MOTION_STATE_NAMES.duplicate(),
		"foot_anchor": NPC_FOOT_ANCHOR,
		"visual_offset": NPC_VISUAL_OFFSET,
		"route_walking_enabled": NPC_ROUTE_WALKING_ENABLED,
		"stationary_until_walk_sheet": NPC_STATIONARY_UNTIL_WALK_SHEET,
		"movement_speed": NPC_MOVEMENT_SPEED,
		"walk_animation_fps": NPC_WALK_ANIMATION_FPS,
		"pause_behavior": NPC_PAUSE_BEHAVIOR,
	}


func _apply_config() -> void:
	if _config.is_empty():
		return
	name = String(_config.get("id", name))
	if _config.has("position"):
		global_position = _config["position"]
	if visual_sprite != null:
		_configure_visual_sprite()


func _configure_ground_shadow() -> void:
	if ground_shadow == null:
		push_error("AtelierTownNpc GroundShadow Polygon2D is missing.")
		return
	ground_shadow.position = Vector2(0.0, 1.0)
	ground_shadow.color = Color(0.0, 0.0, 0.0, 0.16)
	ground_shadow.z_as_relative = true
	ground_shadow.z_index = 0


func _configure_visual_sprite() -> void:
	if visual_sprite == null:
		push_error("AtelierTownNpc Visual AnimatedSprite2D is missing.")
		return
	var atlas := ResourceLoader.load(NPC_ATLAS_PATH, "Texture2D") as Texture2D
	if atlas == null:
		push_error("Failed to load G-4.22R Newport NPC atlas: " + NPC_ATLAS_PATH)
		return
	var asset_id := String(_config.get("asset_id", "npc_market_vendor_atelier_g422r"))
	var frame_index := int(NPC_FRAME_INDEX_BY_ASSET.get(asset_id, 1))
	var sprite_frames := SpriteFrames.new()
	if sprite_frames.has_animation("default"):
		sprite_frames.remove_animation("default")
	var frame := _atlas_frame(atlas, frame_index)
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


func _atlas_frame(atlas: Texture2D, frame_index: int) -> AtlasTexture:
	var frame := AtlasTexture.new()
	frame.atlas = atlas
	frame.region = Rect2(frame_index * NPC_FRAME_SIZE.x, 0, NPC_FRAME_SIZE.x, NPC_FRAME_SIZE.y)
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
