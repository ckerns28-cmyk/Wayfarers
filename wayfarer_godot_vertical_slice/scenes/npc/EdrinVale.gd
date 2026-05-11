extends Node2D

@export var npc_name := "Edrin Vale"
@export_multiline var dialogue := "Edrin Vale: Newport has a waterfront, a civic spine, and streets worth walking now."

func _ready() -> void:
	add_to_group("interactable")
	queue_redraw()

func get_interaction_label() -> String:
	return "E: Speak with " + npc_name

func interact() -> String:
	return dialogue

func _draw() -> void:
	draw_set_transform(Vector2(0, 8), 0.0, Vector2(1.35, 0.42))
	draw_circle(Vector2.ZERO, 10.0, Color(0, 0, 0, 0.22))
	draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
	draw_circle(Vector2(0, -28), 11.0, Color("#d5b384"))
	draw_rect(Rect2(Vector2(-9, -20), Vector2(18, 28)), Color("#6c4b7f"), true)
	draw_rect(Rect2(Vector2(-12, 4), Vector2(24, 8)), Color("#47345a"), true)
	draw_line(Vector2(-13, -21), Vector2(13, -21), Color("#251b25"), 4.0)
