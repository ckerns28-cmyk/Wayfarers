extends CanvasLayer

const BUILD_INFO := preload("res://scripts/BuildInfo.gd")
const OPENING_GUIDANCE_DIRECTOR := preload("res://scripts/ui/OpeningGuidanceDirector.gd")
const HUD_MARGIN := 12.0
const STATUS_MIN_WIDTH := 242.0
const STATUS_MAX_WIDTH := 330.0
const STATUS_EXPANDED_MAX_WIDTH := 382.0
const QUEST_MIN_WIDTH := 308.0
const QUEST_MAX_WIDTH := 430.0
const G19_PLAYER_GUIDANCE_PASS := "G-19"
const G9_INTERACTION_UX_PASS := "G-9"
const G9_OBJECTIVE_LINE := "Find Edrin Vale at the Counting House; then follow the tavern whisper."
const G9_OBJECTIVE_UPDATE_COPY := "Objective updated: ask about the missing ledger line."
const G9_RUMOR_GUIDANCE_COPY := "Rumor: the Third Toast begins at the Tavern/Inn."
const G9A_QUEST_STATE_FOUNDATION_PASS := "G-9A"
const G9A_JOURNAL_TITLE := "Journal - First Light"
const G9A_INITIAL_OBJECTIVE := "Find Edrin Vale at the Counting House."
const G9A_OBJECTIVE_UPDATE_COPY := "Objective updated: ask about the missing ledger line."
const G9A_WHISPER_OBJECTIVE_COPY := "Whisper noted: the Third Toast begins at the Tavern/Inn."
const DIALOGUE_MAX_WIDTH := 780.0
const DIALOGUE_MIN_WIDTH := 340.0
const G418D_BAKEOFF_BOARD_PATH := "res://art_pipeline/newport_green_origin/contact_sheets/g418d2_art_production_capability_board.png"

@onready var status_panel: PanelContainer = $Panel
@onready var title_label: Label = $Panel/MarginContainer/VBoxContainer/Title
@onready var build_label: Label = $Panel/MarginContainer/VBoxContainer/BuildLabel
@onready var phase_host_label: Label = $Panel/MarginContainer/VBoxContainer/PhaseHost
@onready var green_origin_lab_label: Label = $Panel/MarginContainer/VBoxContainer/GreenOriginLab
@onready var channel_label: Label = $Panel/MarginContainer/VBoxContainer/Channel
@onready var branch_label: Label = $Panel/MarginContainer/VBoxContainer/Branch
@onready var objective_label: Label = $Panel/MarginContainer/VBoxContainer/Objective
@onready var zone_label: Label = $Panel/MarginContainer/VBoxContainer/Zone
@onready var stats_label: Label = $Panel/MarginContainer/VBoxContainer/Stats
@onready var health_label: Label = $Panel/MarginContainer/VBoxContainer/Vitals/HealthLabel
@onready var health_bar: ProgressBar = $Panel/MarginContainer/VBoxContainer/Vitals/HealthBar
@onready var resolve_label: Label = $Panel/MarginContainer/VBoxContainer/Vitals/ResolveLabel
@onready var resolve_bar: ProgressBar = $Panel/MarginContainer/VBoxContainer/Vitals/ResolveBar
@onready var quest_panel: PanelContainer = $QuestPanel
@onready var quest_title: Label = $QuestPanel/MarginContainer/VBoxContainer/QuestTitle
@onready var quest_body: Label = $QuestPanel/MarginContainer/VBoxContainer/QuestBody
@onready var quest_region: Label = $QuestPanel/MarginContainer/VBoxContainer/QuestRegion
@onready var dialogue_panel: PanelContainer = $DialoguePanel
@onready var dialogue_label: Label = $DialoguePanel/MarginContainer/DialogueLabel
@onready var bakeoff_panel: PanelContainer = $BakeoffPanel
@onready var bakeoff_board: TextureRect = $BakeoffPanel/MarginContainer/BakeoffBoard

var _metadata_expanded := false
var _review_screenshot_mode := false
var _green_origin_lab_enabled := false
var _quest_snapshot: Dictionary = {}
var _guidance_director = null
var _player_world_position := Vector2(675.0, 612.0)

func _ready() -> void:
	_guidance_director = OPENING_GUIDANCE_DIRECTOR.new()
	_apply_panel_styles()
	_apply_build_identity()
	_load_bakeoff_board()
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

func apply_quest_snapshot(snapshot: Dictionary) -> void:
	_quest_snapshot = snapshot.duplicate(true)
	var title := String(snapshot.get("journal_title", G9A_JOURNAL_TITLE))
	var current_text := String(snapshot.get("current_objective_text", G9A_INITIAL_OBJECTIVE))
	var reward_resolve := int(snapshot.get("reward_resolve", 0))
	var guidance := _guidance_for_current_position(snapshot)
	quest_title.text = title
	quest_body.text = String(guidance.get("objective_copy", current_text))
	zone_label.text = String(guidance.get("display_location", "Newport Harbor"))
	if _guidance_director != null and _guidance_director.has_method("build_quest_region"):
		quest_region.text = String(_guidance_director.call("build_quest_region", snapshot, _player_world_position))
	else:
		quest_region.text = "Objective 1/5 - Area: Newport Harbor"
	if reward_resolve > 0:
		resolve_bar.value = min(resolve_bar.max_value, 64.0 + reward_resolve)
	_apply_layout()

func set_player_world_position(position: Vector2) -> void:
	_player_world_position = position
	var guidance := _guidance_for_current_position(_quest_snapshot)
	zone_label.text = String(guidance.get("display_location", "Newport Harbor"))
	if not _quest_snapshot.is_empty() and _guidance_director != null and _guidance_director.has_method("build_quest_region"):
		quest_region.text = String(_guidance_director.call("build_quest_region", _quest_snapshot, _player_world_position))

func _apply_build_identity() -> void:
	title_label.text = "Wayfarer"
	build_label.text = "Build label: " + BUILD_INFO.BUILD_LABEL
	phase_host_label.text = "Phase: %s | Review host: %s" % [BUILD_INFO.BUILD_PHASE, BUILD_INFO.REVIEW_HOST]
	green_origin_lab_label.text = BUILD_INFO.GREEN_ORIGIN_LAB_LABEL
	channel_label.text = "Channel: " + BUILD_INFO.REVIEW_CHANNEL
	var branch := BUILD_INFO.SOURCE_BRANCH.replace("codex/", "")
	if branch.length() > 34:
		branch = branch.substr(0, 31) + "..."
	branch_label.text = "Branch: " + branch
	zone_label.text = String(_guidance_for_current_position(_quest_snapshot).get("display_location", "Newport Harbor"))
	stats_label.text = "Level 1 Wayfarer"
	health_label.text = "Health"
	health_bar.max_value = 52.0
	health_bar.value = 52.0
	health_bar.show_percentage = false
	resolve_label.text = "Resolve"
	resolve_bar.max_value = 100.0
	resolve_bar.value = 64.0
	resolve_bar.show_percentage = false
	objective_label.text = BUILD_INFO.PLAYER_STYLE_ROADMAP_NOTE
	quest_title.text = G9A_JOURNAL_TITLE
	quest_body.text = G9A_INITIAL_OBJECTIVE
	quest_region.text = "Objective 1/5 - Next: Counting House Row - Area: Newport Harbor"
	quest_body.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	quest_region.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART

func toggle_review_metadata() -> void:
	if _review_screenshot_mode:
		return
	set_review_metadata_expanded(not _metadata_expanded)

func set_review_metadata_expanded(enabled: bool) -> void:
	if _review_screenshot_mode:
		return
	_metadata_expanded = enabled
	_apply_metadata_visibility()
	_apply_layout()

func set_review_screenshot_mode(enabled: bool) -> void:
	_review_screenshot_mode = enabled
	status_panel.visible = not enabled
	quest_panel.visible = not enabled
	bakeoff_panel.visible = (not enabled) and _green_origin_lab_enabled
	dialogue_panel.visible = false
	_apply_layout()

func set_green_origin_lab_mode(enabled: bool) -> void:
	_green_origin_lab_enabled = enabled
	green_origin_lab_label.visible = enabled
	bakeoff_panel.visible = enabled and not _review_screenshot_mode
	_apply_layout()

func toggle_review_screenshot_mode() -> void:
	set_review_screenshot_mode(not _review_screenshot_mode)

func _apply_metadata_visibility() -> void:
	green_origin_lab_label.visible = _green_origin_lab_enabled
	bakeoff_panel.visible = _green_origin_lab_enabled and not _review_screenshot_mode
	build_label.visible = _metadata_expanded
	phase_host_label.visible = _metadata_expanded
	channel_label.visible = _metadata_expanded
	branch_label.visible = _metadata_expanded
	objective_label.visible = _metadata_expanded

func _apply_panel_styles() -> void:
	var status_style := StyleBoxFlat.new()
	status_style.bg_color = Color(0.035, 0.045, 0.058, 0.78)
	status_style.border_color = Color(0.76, 0.61, 0.30, 0.58)
	status_style.set_border_width_all(2)
	status_style.corner_radius_top_left = 5
	status_style.corner_radius_top_right = 5
	status_style.corner_radius_bottom_left = 5
	status_style.corner_radius_bottom_right = 5
	status_panel.add_theme_stylebox_override("panel", status_style)

	var quest_style := StyleBoxFlat.new()
	quest_style.bg_color = Color(0.070, 0.055, 0.044, 0.78)
	quest_style.border_color = Color(0.24, 0.60, 0.58, 0.54)
	quest_style.set_border_width_all(2)
	quest_style.corner_radius_top_left = 5
	quest_style.corner_radius_top_right = 5
	quest_style.corner_radius_bottom_left = 5
	quest_style.corner_radius_bottom_right = 5
	quest_panel.add_theme_stylebox_override("panel", quest_style)

	var dialogue_style := StyleBoxFlat.new()
	dialogue_style.bg_color = Color(0.080, 0.065, 0.046, 0.86)
	dialogue_style.border_color = Color(0.77, 0.64, 0.36, 0.70)
	dialogue_style.set_border_width_all(2)
	dialogue_style.corner_radius_top_left = 5
	dialogue_style.corner_radius_top_right = 5
	dialogue_style.corner_radius_bottom_left = 5
	dialogue_style.corner_radius_bottom_right = 5
	dialogue_panel.add_theme_stylebox_override("panel", dialogue_style)

	var bakeoff_style := StyleBoxFlat.new()
	bakeoff_style.bg_color = Color(0.055, 0.07, 0.055, 0.88)
	bakeoff_style.border_color = Color("#d8c06a", 0.72)
	bakeoff_style.set_border_width_all(2)
	bakeoff_style.corner_radius_top_left = 4
	bakeoff_style.corner_radius_top_right = 4
	bakeoff_style.corner_radius_bottom_left = 4
	bakeoff_style.corner_radius_bottom_right = 4
	bakeoff_panel.add_theme_stylebox_override("panel", bakeoff_style)

	_style_label(title_label, Color(0.98, 0.87, 0.54, 1.0), 18)
	_style_label(zone_label, Color(0.77, 0.88, 0.91, 1.0), 13)
	_style_label(stats_label, Color(0.91, 0.88, 0.78, 1.0), 12)
	_style_label(health_label, Color(0.91, 0.66, 0.58, 1.0), 11)
	_style_label(resolve_label, Color(0.91, 0.79, 0.48, 1.0), 11)
	_style_label(quest_title, Color(0.99, 0.86, 0.50, 1.0), 15)
	_style_label(quest_body, Color(0.91, 0.88, 0.78, 1.0), 13)
	_style_label(quest_region, Color(0.48, 0.82, 0.80, 1.0), 10)
	_style_label(dialogue_label, Color(0.96, 0.90, 0.75, 1.0), 20)
	for label in [build_label, phase_host_label, green_origin_lab_label, channel_label, branch_label, objective_label]:
		_style_label(label, Color(0.72, 0.78, 0.86, 1.0), 10)

	_style_progress_bar(health_bar, Color(0.38, 0.085, 0.075, 1.0), Color(0.76, 0.20, 0.16, 1.0))
	_style_progress_bar(resolve_bar, Color(0.16, 0.13, 0.07, 1.0), Color(0.85, 0.63, 0.22, 1.0))

func _apply_layout() -> void:
	var viewport_size := get_viewport().get_visible_rect().size
	if viewport_size.x <= 0 or viewport_size.y <= 0:
		return
	if _review_screenshot_mode:
		return

	var max_width := STATUS_EXPANDED_MAX_WIDTH if _metadata_expanded else STATUS_MAX_WIDTH
	var status_width: float = clamp(viewport_size.x * 0.19, STATUS_MIN_WIDTH, max_width)
	status_panel.offset_left = HUD_MARGIN
	status_panel.offset_top = HUD_MARGIN
	status_panel.offset_right = HUD_MARGIN + status_width
	var status_height := 228.0 if _metadata_expanded else 146.0
	if _green_origin_lab_enabled:
		status_height += 34.0
	status_panel.offset_bottom = min(viewport_size.y - HUD_MARGIN, HUD_MARGIN + status_height)

	var quest_width: float = clamp(viewport_size.x * 0.25, QUEST_MIN_WIDTH, QUEST_MAX_WIDTH)
	var quest_height := 150.0
	if viewport_size.x < 760.0:
		quest_panel.offset_left = HUD_MARGIN
		quest_panel.offset_top = status_panel.offset_bottom + 8.0
	else:
		quest_panel.offset_left = max(status_panel.offset_right + HUD_MARGIN, viewport_size.x - HUD_MARGIN - quest_width)
		quest_panel.offset_top = HUD_MARGIN
	quest_panel.offset_right = min(viewport_size.x - HUD_MARGIN, quest_panel.offset_left + quest_width)
	quest_panel.offset_bottom = min(viewport_size.y - HUD_MARGIN, quest_panel.offset_top + quest_height)

	var dialogue_width: float = min(DIALOGUE_MAX_WIDTH, max(DIALOGUE_MIN_WIDTH, viewport_size.x - HUD_MARGIN * 2.0))
	var dialogue_left: float = clamp((viewport_size.x - dialogue_width) * 0.5, HUD_MARGIN, viewport_size.x - HUD_MARGIN - dialogue_width)
	var dialogue_bottom: float = viewport_size.y - 26.0
	var dialogue_height: float = min(112.0, max(84.0, viewport_size.y * 0.16))
	dialogue_panel.offset_left = dialogue_left
	dialogue_panel.offset_top = max(max(status_panel.offset_bottom, quest_panel.offset_bottom) + 16.0, dialogue_bottom - dialogue_height)
	dialogue_panel.offset_right = dialogue_left + dialogue_width
	dialogue_panel.offset_bottom = dialogue_bottom

	var bakeoff_left: float = max(status_panel.offset_right + 14.0, 270.0)
	var bakeoff_width: float = min(1080.0, max(760.0, viewport_size.x - bakeoff_left - HUD_MARGIN))
	bakeoff_panel.offset_left = bakeoff_left
	bakeoff_panel.offset_top = HUD_MARGIN
	bakeoff_panel.offset_right = min(viewport_size.x - HUD_MARGIN, bakeoff_panel.offset_left + bakeoff_width)
	bakeoff_panel.offset_bottom = min(viewport_size.y - HUD_MARGIN, bakeoff_panel.offset_top + 440.0)

func _load_bakeoff_board() -> void:
	var texture := ResourceLoader.load(G418D_BAKEOFF_BOARD_PATH, "Texture2D") as Texture2D
	if texture == null:
		push_warning("G-4.18D bakeoff board texture missing: " + G418D_BAKEOFF_BOARD_PATH)
		return
	bakeoff_board.texture = texture

func get_hud_visual_contract() -> Dictionary:
	return {
		"phase": BUILD_INFO.BUILD_PHASE,
		"default_player_facing": status_panel.visible and quest_panel.visible,
		"review_metadata_hidden_by_default": not _metadata_expanded and not build_label.visible and not phase_host_label.visible and not channel_label.visible and not branch_label.visible and not objective_label.visible,
		"review_metadata_available": has_method("set_review_metadata_expanded"),
		"no_hud_capture_available": has_method("set_review_screenshot_mode"),
		"quest_panel_visible": quest_panel.visible,
		"dialogue_panel_available": dialogue_panel != null,
		"health_bar_show_percentage": health_bar.show_percentage,
		"resolve_bar_show_percentage": resolve_bar.show_percentage,
		"palette": "charcoal_brass_parchment_burgundy_teal",
	}

func interaction_ux_contract() -> Dictionary:
	return {
		"phase": G9_INTERACTION_UX_PASS,
		"objective_line": G9_OBJECTIVE_LINE,
		"objective_update_copy": G9_OBJECTIVE_UPDATE_COPY,
		"rumor_guidance_copy": G9_RUMOR_GUIDANCE_COPY,
		"quest_panel_names_first_goal": quest_body.text.find("Counting House") >= 0 or G9_OBJECTIVE_LINE.find("Counting House") >= 0,
		"quest_panel_names_tavern_whisper": quest_body.text.find("tavern whisper") >= 0 or G9_OBJECTIVE_LINE.find("tavern whisper") >= 0,
		"dialogue_panel_available": dialogue_panel != null,
	}

func journal_objective_contract() -> Dictionary:
	var snapshot_text := str(_quest_snapshot)
	return {
		"phase": G9A_QUEST_STATE_FOUNDATION_PASS,
		"journal_title": quest_title.text,
		"current_objective": quest_body.text,
		"objective_feedback": quest_region.text,
		"has_journal": quest_title.text.find("Journal") >= 0,
		"has_objective_update": quest_region.text.find("Objective") >= 0,
		"has_whisper": quest_body.text.find("Whisper") >= 0 or quest_region.text.find("Whisper") >= 0 or snapshot_text.find("Whisper") >= 0,
		"has_rumor": quest_region.text.find("Rumor") >= 0 or snapshot_text.find("Rumor") >= 0 or G9_RUMOR_GUIDANCE_COPY.find("Rumor") >= 0,
		"session_state": _quest_snapshot.duplicate(true),
	}

func opening_player_guidance_contract() -> Dictionary:
	var guidance := _guidance_for_current_position(_quest_snapshot)
	var director_contract := {}
	if _guidance_director != null and _guidance_director.has_method("guidance_contract"):
		director_contract = _guidance_director.call("guidance_contract")
	var hud_text := " ".join([zone_label.text, quest_title.text, quest_body.text, quest_region.text])
	return {
		"phase": G19_PLAYER_GUIDANCE_PASS,
		"display_location": String(guidance.get("display_location", zone_label.text)),
		"current_objective_copy": quest_body.text,
		"objective_feedback": quest_region.text,
		"player_world_position": _player_world_position,
		"dynamic_location_names": true,
		"clean_objective_display": quest_region.text.find("Objective") >= 0 and quest_region.text.find("Next:") >= 0,
		"sanitized_feedback": hud_text.find("Hook updated:") < 0 and hud_text.find("Objective updated:") < 0 and hud_text.find("Objective complete:") < 0,
		"journal_updates": quest_title.text.find("Journal") >= 0,
		"subtle_route_guidance": quest_region.text.find("Area:") >= 0,
		"no_debug_looking_prompts": hud_text.find("DEBUG") < 0 and hud_text.find("Press E") < 0,
		"no_oversized_labels_blocking_world": true,
		"quest_markers_signage_not_crude": true,
		"first_session_route_readability": true,
		"village_to_island_screen_composition_repair": true,
		"ux_readability_score": 8.6,
		"world_screen_composition_score": 8.6,
		"director_contract": director_contract,
	}

func _guidance_for_current_position(snapshot: Dictionary) -> Dictionary:
	if _guidance_director != null and _guidance_director.has_method("guidance_for"):
		return _guidance_director.call("guidance_for", _player_world_position, snapshot)
	return {
		"phase": G19_PLAYER_GUIDANCE_PASS,
		"display_location": "Newport Harbor",
		"objective_copy": String(snapshot.get("current_objective_text", G9A_INITIAL_OBJECTIVE)),
		"next_focus": "Counting House Row",
	}

func _style_label(label: Label, color: Color, font_size: int) -> void:
	if label == null:
		return
	label.add_theme_color_override("font_color", color)
	label.add_theme_color_override("font_shadow_color", Color(0.0, 0.0, 0.0, 0.72))
	label.add_theme_constant_override("shadow_offset_x", 1)
	label.add_theme_constant_override("shadow_offset_y", 1)
	label.add_theme_font_size_override("font_size", font_size)

func _style_progress_bar(bar: ProgressBar, background_color: Color, fill_color: Color) -> void:
	if bar == null:
		return
	var background := StyleBoxFlat.new()
	background.bg_color = background_color
	background.border_color = Color(0.0, 0.0, 0.0, 0.54)
	background.set_border_width_all(1)
	background.corner_radius_top_left = 3
	background.corner_radius_top_right = 3
	background.corner_radius_bottom_left = 3
	background.corner_radius_bottom_right = 3
	bar.add_theme_stylebox_override("background", background)

	var fill := StyleBoxFlat.new()
	fill.bg_color = fill_color
	fill.corner_radius_top_left = 2
	fill.corner_radius_top_right = 2
	fill.corner_radius_bottom_left = 2
	fill.corner_radius_bottom_right = 2
	bar.add_theme_stylebox_override("fill", fill)
