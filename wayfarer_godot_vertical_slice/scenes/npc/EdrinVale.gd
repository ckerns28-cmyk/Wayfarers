extends Node2D

@export var npc_name := "Edrin Vale"
@export_multiline var dialogue := "Edrin Vale: Newport has a waterfront, a civic spine, and streets worth walking now."

const NPC_ATLAS_PATH := "res://art_pipeline/player_identity/atlases/newport_npc_atelier_g422r_v1.png"
const NPC_FRAME_SIZE := Vector2i(256, 256)
const EDRIN_FRAME_INDEX := 2
const NPC_VISUAL_SCALE := 0.32
const NPC_VISUAL_OFFSET := Vector2(0.0, -33.0)

@onready var visual_sprite: Sprite2D = $Visual

func _ready() -> void:
	add_to_group("interactable")
	_configure_visual_sprite()

func get_interaction_label() -> String:
	return "E: Speak with " + npc_name

func interact() -> String:
	return dialogue

func _configure_visual_sprite() -> void:
	if visual_sprite == null:
		push_error("EdrinVale Visual Sprite2D is missing.")
		return
	var atlas := ResourceLoader.load(NPC_ATLAS_PATH, "Texture2D") as Texture2D
	if atlas == null:
		push_error("Failed to load G-4.22R Newport NPC atlas: " + NPC_ATLAS_PATH)
		return
	var frame := AtlasTexture.new()
	frame.atlas = atlas
	frame.region = Rect2(EDRIN_FRAME_INDEX * NPC_FRAME_SIZE.x, 0, NPC_FRAME_SIZE.x, NPC_FRAME_SIZE.y)
	frame.filter_clip = true
	visual_sprite.texture = frame
	visual_sprite.centered = true
	visual_sprite.position = NPC_VISUAL_OFFSET
	visual_sprite.scale = Vector2.ONE * NPC_VISUAL_SCALE
	visual_sprite.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	visual_sprite.z_as_relative = true
	visual_sprite.z_index = 1
