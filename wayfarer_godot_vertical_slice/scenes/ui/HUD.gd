extends CanvasLayer

const BUILD_INFO := preload("res://scripts/BuildInfo.gd")
const HUD_MARGIN := 18.0
const STATUS_MIN_WIDTH := 360.0
const STATUS_MAX_WIDTH := 520.0
const DIALOGUE_MAX_WIDTH := 780.0
const DIALOGUE_MIN_WIDTH := 340.0

@onready var status_panel: PanelContainer = $Panel
@onready var build_label: Label = $Panel/MarginContainer/VBoxContainer/BuildLabel
@onready var phase_host_label: Label = $Panel/MarginContainer/VBoxContainer/PhaseHost
@onready var channel_label: Label = $Panel/MarginContainer/VBoxContainer/Channel
@onready var branch_label: Label = $Panel/MarginContainer/VBoxContainer/Branch
@onready var dialogue_panel: PanelContainer = $DialoguePanel
@onready var dialogue_label: Label = $DialoguePanel/MarginContainer/DialogueLabel

func _ready() -> void:
	_apply_build_identity()
	dialogue_panel.visible = false
	_apply_layout()
	get_viewport().size_changed.connect(_apply_layout)

func show_dialogue(text: String) -> void:
	dialogue_label.text = text
	dialogue_panel.visible = true
	await get_tree().create_timer(4.0).timeout
	dialogue_panel.visible = false

func _apply_build_identity() -> void:
	build_label.text = "Build label: " + BUILD_INFO.BUILD_LABEL
	phase_host_label.text = "Phase: %s | Review host: %s" % [BUILD_INFO.BUILD_PHASE, BUILD_INFO.REVIEW_HOST]
	channel_label.text = "Channel: " + BUILD_INFO.REVIEW_CHANNEL
	branch_label.text = "Branch: " + BUILD_INFO.SOURCE_BRANCH

func _apply_layout() -> void:
	var viewport_size := get_viewport().get_visible_rect().size
	if viewport_size.x <= 0 or viewport_size.y <= 0:
		return

	var status_width: float = clamp(viewport_size.x * 0.36, STATUS_MIN_WIDTH, STATUS_MAX_WIDTH)
	status_panel.offset_left = HUD_MARGIN
	status_panel.offset_top = HUD_MARGIN
	status_panel.offset_right = HUD_MARGIN + status_width
	status_panel.offset_bottom = min(viewport_size.y - HUD_MARGIN, HUD_MARGIN + 282.0)

	var dialogue_width: float = min(DIALOGUE_MAX_WIDTH, max(DIALOGUE_MIN_WIDTH, viewport_size.x - HUD_MARGIN * 2.0))
	var dialogue_left: float = clamp((viewport_size.x - dialogue_width) * 0.5, HUD_MARGIN, viewport_size.x - HUD_MARGIN - dialogue_width)
	var dialogue_bottom: float = viewport_size.y - 26.0
	var dialogue_height: float = min(112.0, max(84.0, viewport_size.y * 0.16))
	dialogue_panel.offset_left = dialogue_left
	dialogue_panel.offset_top = max(status_panel.offset_bottom + 16.0, dialogue_bottom - dialogue_height)
	dialogue_panel.offset_right = dialogue_left + dialogue_width
	dialogue_panel.offset_bottom = dialogue_bottom
