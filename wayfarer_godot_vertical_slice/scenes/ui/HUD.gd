extends CanvasLayer

@onready var dialogue_panel: PanelContainer = $DialoguePanel
@onready var dialogue_label: Label = $DialoguePanel/MarginContainer/DialogueLabel

func _ready() -> void:
	dialogue_panel.visible = false

func show_dialogue(text: String) -> void:
	dialogue_label.text = text
	dialogue_panel.visible = true
	await get_tree().create_timer(4.0).timeout
	dialogue_panel.visible = false

