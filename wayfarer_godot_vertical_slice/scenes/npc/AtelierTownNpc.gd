extends Node2D

const NPC_ATLAS_PATH := "res://art_pipeline/player_identity/atlases/newport_npc_atelier_g422r_v1.png"
const G8A_LIVING_NPC_POPULATION_PASS := "G-8A"
const G9_INTERACTION_UX_PASS := "G-9"
const G11_LIVING_TOWN_RHYTHM_PASS := "G-11"
const NPC_FRAME_SIZE := Vector2i(256, 256)
const NPC_VISUAL_SCALE := 0.32
const NPC_FOOT_ANCHOR := Vector2(128.0, 244.0)
const NPC_VISUAL_OFFSET := Vector2(0.0, -37.12)
const NPC_ROUTE_WALKING_ENABLED := false
const NPC_STATIONARY_UNTIL_WALK_SHEET := true
const NPC_MOVEMENT_SPEED := 0.0
const NPC_WALK_ANIMATION_FPS := 0.0
const NPC_PAUSE_BEHAVIOR := "stationary_work_pose_until_dedicated_walk_sheets"
const NPC_TOWN_RHYTHM_POLICY := "stationary_no_glide_rhythm_until_dedicated_walk_sheets"
const NPC_BARK_DISPLAY_SECONDS := 2.6
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
var _rhythm_config: Dictionary = {}
var _rhythm_elapsed := 0.0
var _rhythm_stage: Dictionary = {}
var _current_bark := ""
var _facing_direction := "down"
var _current_visual_animation := ""
var _ambient_bark_label: Label = null
var _ambient_barks_enabled := true


func _ready() -> void:
	add_to_group("interactable")
	add_to_group("starter_village_npc")
	add_to_group("starter_village_town_rhythm_actor")
	_configure_ground_shadow()
	_configure_visual_sprite()
	_configure_ambient_bark_label()
	_apply_config()


func _process(delta: float) -> void:
	if _rhythm_config.is_empty():
		return
	_rhythm_elapsed += delta
	apply_town_rhythm_tick(_rhythm_elapsed, false)


func configure(config: Dictionary) -> void:
	_config = config.duplicate(true)
	if _config.has("position"):
		global_position = _config["position"]
	if is_node_ready():
		_apply_config()


func get_interaction_label() -> String:
	return "Talk - " + String(_config.get("display_name", "Newporter"))


func get_prompt_text() -> String:
	return "E: " + get_interaction_label()


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


func configure_rhythm(config: Dictionary) -> void:
	_rhythm_config = config.duplicate(true)
	_rhythm_elapsed = 0.0
	if is_node_ready() and not _rhythm_config.is_empty():
		apply_town_rhythm_tick(0.0, false)


func apply_town_rhythm_tick(elapsed_seconds: float, force_bark := false) -> Dictionary:
	if _rhythm_config.is_empty():
		return town_rhythm_contract()
	var stage := _rhythm_stage_for_time(elapsed_seconds)
	_rhythm_stage = stage.duplicate(true)
	var facing := String(stage.get("facing", _facing_direction))
	set_review_motion_state(facing, false, 0)
	_current_bark = String(stage.get("bark", ""))
	var stage_age := _stage_age(elapsed_seconds, stage)
	var duration := maxf(float(stage.get("duration", NPC_BARK_DISPLAY_SECONDS)), NPC_BARK_DISPLAY_SECONDS)
	var should_show_bark := force_bark or (stage_age >= 0.0 and stage_age <= minf(NPC_BARK_DISPLAY_SECONDS, duration))
	_set_ambient_bark(_current_bark, should_show_bark and not _current_bark.is_empty())
	return town_rhythm_contract()


func set_town_rhythm_bark_visible(visible: bool) -> void:
	_set_ambient_bark(_current_bark, visible and not _current_bark.is_empty())


func set_town_rhythm_barks_enabled(enabled: bool) -> void:
	_ambient_barks_enabled = enabled
	if not enabled:
		_set_ambient_bark(_current_bark, false)


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


func town_rhythm_contract() -> Dictionary:
	var stages: Array = _rhythm_config.get("stages", [])
	var bark_count := 0
	for raw_stage in stages:
		var stage: Dictionary = raw_stage
		if not String(stage.get("bark", "")).is_empty():
			bark_count += 1
	return {
		"phase": G11_LIVING_TOWN_RHYTHM_PASS,
		"npc_id": String(_config.get("id", name)),
		"display_name": String(_config.get("display_name", "Newporter")),
		"role": String(_config.get("role", "")),
		"district": String(_config.get("district", "")),
		"station": String(_config.get("station", "")),
		"rhythm_id": String(_rhythm_config.get("id", "")),
		"behavior_tag": String(_rhythm_config.get("behavior_tag", "")),
		"station_points": (_rhythm_config.get("station_points", []) as Array).duplicate(),
		"stage_count": stages.size(),
		"ambient_bark_count": bark_count,
		"current_action": String(_rhythm_stage.get("action", "")),
		"current_bark": _current_bark,
		"facing_direction": _facing_direction,
		"route_walking_enabled": NPC_ROUTE_WALKING_ENABLED,
		"stationary_until_walk_sheet": NPC_STATIONARY_UNTIL_WALK_SHEET,
		"movement_speed": NPC_MOVEMENT_SPEED,
		"movement_policy": NPC_TOWN_RHYTHM_POLICY,
		"global_position": global_position,
		"ground_shadow_visible": ground_shadow != null and ground_shadow.visible,
		"ambient_barks_enabled": _ambient_barks_enabled,
		"no_static_sprite_translation": true,
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

func prompt_ux_contract() -> Dictionary:
	return {
		"phase": G9_INTERACTION_UX_PASS,
		"prompt_style": "compact_diegetic_action_name_no_debug_marker",
		"prompt_text": get_prompt_text(),
		"dialogue_seed": String(_config.get("dialogue_seed", "")),
		"quest_relevance": String(_config.get("quest_relevance", "")),
	}


func _apply_config() -> void:
	if _config.is_empty():
		return
	name = String(_config.get("id", name))
	if _config.has("position"):
		global_position = _config["position"]
	if visual_sprite != null:
		_configure_visual_sprite()
	if not _rhythm_config.is_empty():
		apply_town_rhythm_tick(_rhythm_elapsed, false)


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


func _configure_ambient_bark_label() -> void:
	if _ambient_bark_label != null:
		return
	_ambient_bark_label = Label.new()
	_ambient_bark_label.name = "AmbientBarkLabel"
	_ambient_bark_label.visible = false
	_ambient_bark_label.position = Vector2(-88.0, -106.0)
	_ambient_bark_label.custom_minimum_size = Vector2(176.0, 28.0)
	_ambient_bark_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_ambient_bark_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_ambient_bark_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_ambient_bark_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_ambient_bark_label.z_as_relative = true
	_ambient_bark_label.z_index = 4
	_ambient_bark_label.modulate = Color(1.0, 0.93, 0.70, 0.92)
	_ambient_bark_label.add_theme_font_size_override("font_size", 10)
	_ambient_bark_label.add_theme_color_override("font_outline_color", Color(0.05, 0.04, 0.02, 0.88))
	_ambient_bark_label.add_theme_constant_override("outline_size", 3)
	add_child(_ambient_bark_label)


func _set_ambient_bark(text: String, visible: bool) -> void:
	if _ambient_bark_label == null:
		return
	_ambient_bark_label.text = text
	_ambient_bark_label.visible = _ambient_barks_enabled and visible and not text.is_empty()


func _rhythm_stage_for_time(elapsed_seconds: float) -> Dictionary:
	var stages: Array = _rhythm_config.get("stages", [])
	if stages.is_empty():
		return {}
	var cycle_seconds := maxf(float(_rhythm_config.get("cycle_seconds", 1.0)), 1.0)
	var cycle_time := fposmod(elapsed_seconds, cycle_seconds)
	var selected: Dictionary = stages[0]
	for raw_stage in stages:
		var stage: Dictionary = raw_stage
		var start := float(stage.get("at", 0.0))
		var duration := maxf(float(stage.get("duration", 0.0)), 0.01)
		if cycle_time >= start and cycle_time < start + duration:
			return stage
		if cycle_time >= start:
			selected = stage
	return selected


func _stage_age(elapsed_seconds: float, stage: Dictionary) -> float:
	var cycle_seconds := maxf(float(_rhythm_config.get("cycle_seconds", 1.0)), 1.0)
	var cycle_time := fposmod(elapsed_seconds, cycle_seconds)
	return cycle_time - float(stage.get("at", 0.0))


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
