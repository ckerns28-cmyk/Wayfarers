extends CanvasLayer

const BUILD_INFO := preload("res://scripts/BuildInfo.gd")
const HUD_MARGIN := 12.0
const STATUS_MIN_WIDTH := 238.0
const STATUS_MAX_WIDTH := 304.0
const STATUS_EXPANDED_MAX_WIDTH := 348.0
const DIALOGUE_MAX_WIDTH := 780.0
const DIALOGUE_MIN_WIDTH := 340.0

@onready var status_panel: PanelContainer = $Panel
@onready var build_label: Label = $Panel/MarginContainer/VBoxContainer/BuildLabel
@onready var phase_host_label: Label = $Panel/MarginContainer/VBoxContainer/PhaseHost
@onready var green_origin_lab_label: Label = $Panel/MarginContainer/VBoxContainer/GreenOriginLab
@onready var channel_label: Label = $Panel/MarginContainer/VBoxContainer/Channel
@onready var branch_label: Label = $Panel/MarginContainer/VBoxContainer/Branch
@onready var objective_label: Label = $Panel/MarginContainer/VBoxContainer/Objective
@onready var zone_label: Label = $Panel/MarginContainer/VBoxContainer/Zone
@onready var stats_label: Label = $Panel/MarginContainer/VBoxContainer/Stats
@onready var dialogue_panel: PanelContainer = $DialoguePanel
@onready var dialogue_label: Label = $DialoguePanel/MarginContainer/DialogueLabel

var _metadata_expanded := false
var _review_screenshot_mode := false
var _green_origin_lab_enabled := false

func _ready() -> void:
	_apply_panel_styles()
	_apply_build_identity()
	_apply_metadata_visibility()
	dialogue_panel.visible = false
	_apply_layout()
	get_viewport().size_changed.connect(_apply_layout)

func show_dialogue(text: String) -> void:
	if _review_screenshot_mode:
		return
	dialogue_label.text = text
	dialogue_panel.visible = true
	await get_tree().create_timer(4.0).timeout
	if _review_screenshot_mode:
		return
	dialogue_panel.visible = false

func _apply_build_identity() -> void:
	build_label.text = "Build label: " + BUILD_INFO.BUILD_LABEL
	phase_host_label.text = "Phase: %s | Review host: %s" % [BUILD_INFO.BUILD_PHASE, BUILD_INFO.REVIEW_HOST]
	green_origin_lab_label.text = BUILD_INFO.GREEN_ORIGIN_LAB_LABEL
	channel_label.text = "Channel: " + BUILD_INFO.REVIEW_CHANNEL
	var branch := BUILD_INFO.SOURCE_BRANCH.replace("codex/", "")
	if branch.length() > 34:
		branch = branch.substr(0, 31) + "..."
	branch_label.text = "Branch: " + branch
	zone_label.text = "Newport Starter Harbor"
	stats_label.text = "Level 1  HP 52/52"
	objective_label.text = BUILD_INFO.PLAYER_STYLE_ROADMAP_NOTE

func toggle_review_metadata() -> void:
	if _review_screenshot_mode:
		return
	_metadata_expanded = not _metadata_expanded
	_apply_metadata_visibility()
	_apply_layout()

func set_review_screenshot_mode(enabled: bool) -> void:
	_review_screenshot_mode = enabled
	status_panel.visible = not enabled
	dialogue_panel.visible = false
	_apply_layout()

func set_green_origin_lab_mode(enabled: bool) -> void:
	_green_origin_lab_enabled = enabled
	green_origin_lab_label.visible = enabled
	_apply_layout()

func toggle_review_screenshot_mode() -> void:
	set_review_screenshot_mode(not _review_screenshot_mode)

func _apply_metadata_visibility() -> void:
	green_origin_lab_label.visible = _green_origin_lab_enabled
	channel_label.visible = _metadata_expanded
	branch_label.visible = _metadata_expanded
	objective_label.visible = _metadata_expanded

func _apply_panel_styles() -> void:
	var status_style := StyleBoxFlat.new()
	status_style.bg_color = Color(0.055, 0.075, 0.06, 0.46)
	status_style.border_color = Color(0.58, 0.66, 0.58, 0.22)
	status_style.set_border_width_all(1)
	status_style.corner_radius_top_left = 4
	status_style.corner_radius_top_right = 4
	status_style.corner_radius_bottom_left = 4
	status_style.corner_radius_bottom_right = 4
	status_panel.add_theme_stylebox_override("panel", status_style)

	var dialogue_style := StyleBoxFlat.new()
	dialogue_style.bg_color = Color(0.055, 0.07, 0.06, 0.78)
	dialogue_style.border_color = Color(0.62, 0.70, 0.62, 0.24)
	dialogue_style.set_border_width_all(1)
	dialogue_style.corner_radius_top_left = 4
	dialogue_style.corner_radius_top_right = 4
	dialogue_style.corner_radius_bottom_left = 4
	dialogue_style.corner_radius_bottom_right = 4
	dialogue_panel.add_theme_stylebox_override("panel", dialogue_style)

func _apply_layout() -> void:
	var viewport_size := get_viewport().get_visible_rect().size
	if viewport_size.x <= 0 or viewport_size.y <= 0:
		return
	if _review_screenshot_mode:
		return

	var max_width := STATUS_EXPANDED_MAX_WIDTH if _metadata_expanded else STATUS_MAX_WIDTH
	var status_width: float = clamp(viewport_size.x * 0.17, STATUS_MIN_WIDTH, max_width)
	status_panel.offset_left = HUD_MARGIN
	status_panel.offset_top = HUD_MARGIN
	status_panel.offset_right = HUD_MARGIN + status_width
	var status_height := 180.0 if _metadata_expanded else 108.0
	if _green_origin_lab_enabled:
		status_height += 34.0
	status_panel.offset_bottom = min(viewport_size.y - HUD_MARGIN, HUD_MARGIN + status_height)

	var dialogue_width: float = min(DIALOGUE_MAX_WIDTH, max(DIALOGUE_MIN_WIDTH, viewport_size.x - HUD_MARGIN * 2.0))
	var dialogue_left: float = clamp((viewport_size.x - dialogue_width) * 0.5, HUD_MARGIN, viewport_size.x - HUD_MARGIN - dialogue_width)
	var dialogue_bottom: float = viewport_size.y - 26.0
	var dialogue_height: float = min(112.0, max(84.0, viewport_size.y * 0.16))
	dialogue_panel.offset_left = dialogue_left
	dialogue_panel.offset_top = max(status_panel.offset_bottom + 16.0, dialogue_bottom - dialogue_height)
	dialogue_panel.offset_right = dialogue_left + dialogue_width
	dialogue_panel.offset_bottom = dialogue_bottom
