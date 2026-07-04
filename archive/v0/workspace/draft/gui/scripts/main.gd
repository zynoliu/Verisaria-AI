extends Control

const VIEW_W := 1672.0
const VIEW_H := 941.0

const BG := preload("res://assets/backgrounds/frostgate_gatehouse_base.png")
const STANDEES := preload("res://assets/characters/character_standee_atlas_alpha.png")
const PORTRAITS := preload("res://assets/characters/portrait_expression_atlas_alpha.png")
const UI_FRAMES := preload("res://assets/ui/ui_frame_atlas_alpha.png")
const ICONS := preload("res://assets/icons/icon_emblem_atlas_alpha.png")
const OVERLAYS := preload("res://assets/overlays/frostgate_overlay_atlas_alpha.png")

const C_BG := Color("#07090c")
const C_PANEL := Color(0.03, 0.045, 0.06, 0.88)
const C_PANEL_SOFT := Color(0.05, 0.065, 0.08, 0.90)
const C_BORDER := Color("#75654f")
const C_AMBER := Color("#d7a86e")
const C_PARCHMENT := Color("#d8cbbb")
const C_RED := Color("#c0504d")
const C_GREEN := Color("#8fbd7b")
const C_DIM := Color("#8b8580")

var tick := 127
var hp := 32
var stamina := 18
var refugees_admitted := false
var brann_trust := 24
var voss_tension := 15
var pressure := 72

var log_box: RichTextLabel
var command_input: LineEdit
var world_panel: VBoxContainer
var npc_panel: VBoxContainer
var status_label: Label
var dialogue_name: Label
var dialogue_text: RichTextLabel
var brann_relation: ProgressBar
var voss_relation: ProgressBar
var pressure_bar: ProgressBar
var world_change_label: Label


func _ready() -> void:
	get_window().title = "Verisaria GUI Draft"
	_build_scene()
	_seed_log()
	_refresh_all()


func _build_scene() -> void:
	custom_minimum_size = Vector2(VIEW_W, VIEW_H)
	_add_base_background()
	_add_scene_overlays()
	_add_character_standees()
	_add_top_hud()
	_add_right_sidebar()
	_add_dialogue_panel()
	_add_input_panel()


func _add_base_background() -> void:
	var bg := TextureRect.new()
	bg.name = "FrostgateBackground"
	bg.texture = BG
	bg.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	bg.stretch_mode = TextureRect.STRETCH_SCALE
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(bg)

	var shade := ColorRect.new()
	shade.name = "SceneShade"
	shade.color = Color(0, 0, 0, 0.10)
	shade.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(shade)


func _add_scene_overlays() -> void:
	# Snow and speech marker crops from the overlay atlas. These are decorative
	# prototype uses; later slicing can turn the atlas into named sprites.
	_add_texture_crop(OVERLAYS, Rect2(60, 40, 880, 190), Vector2(168, 126), Vector2(450, 92), 0.24)
	_add_texture_crop(OVERLAYS, Rect2(1210, 710, 110, 130), Vector2(624, 190), Vector2(34, 40), 0.95)
	_add_texture_crop(OVERLAYS, Rect2(1210, 710, 110, 130), Vector2(876, 232), Vector2(28, 34), 0.80)


func _add_character_standees() -> void:
	# Approximate atlas crops. The atlas is intentionally kept whole in assets/;
	# these prototype regions document the first pass of sprite slicing.
	_add_texture_crop(STANDEES, Rect2(55, 42, 290, 330), Vector2(362, 322), Vector2(180, 242), 1.0)
	_add_texture_crop(STANDEES, Rect2(500, 38, 260, 330), Vector2(555, 250), Vector2(244, 318), 1.0)
	_add_texture_crop(STANDEES, Rect2(860, 38, 205, 340), Vector2(818, 292), Vector2(168, 278), 1.0)
	_add_texture_crop(STANDEES, Rect2(1228, 42, 250, 320), Vector2(1045, 306), Vector2(178, 240), 0.85)

	var name_a := _label("队长布兰", 22, C_AMBER, true)
	name_a.position = Vector2(624, 226)
	add_child(name_a)
	var name_b := _label("哨兵沃斯", 20, C_PARCHMENT, true)
	name_b.position = Vector2(842, 268)
	add_child(name_b)


func _add_top_hud() -> void:
	var hud := _panel(Vector2(8, 8), Vector2(1656, 62), C_PANEL, C_BORDER)
	add_child(hud)

	status_label = _label("", 22, C_PARCHMENT, true)
	status_label.position = Vector2(42, 24)
	add_child(status_label)


func _add_right_sidebar() -> void:
	var side_x := 1288.0
	var panel_w := 366.0
	_add_panel_title("附近人物", Vector2(side_x, 86), Vector2(panel_w, 38))
	var npc_bg := _panel(Vector2(side_x, 124), Vector2(panel_w, 286), C_PANEL_SOFT, C_BORDER)
	add_child(npc_bg)
	npc_panel = VBoxContainer.new()
	npc_panel.position = Vector2(side_x + 18, 140)
	npc_panel.size = Vector2(panel_w - 36, 250)
	npc_panel.add_theme_constant_override("separation", 10)
	add_child(npc_panel)

	_add_panel_title("世界状态", Vector2(side_x, 428), Vector2(panel_w, 38))
	var world_bg := _panel(Vector2(side_x, 466), Vector2(panel_w, 170), C_PANEL_SOFT, C_BORDER)
	add_child(world_bg)
	world_panel = VBoxContainer.new()
	world_panel.position = Vector2(side_x + 18, 482)
	world_panel.size = Vector2(panel_w - 36, 136)
	world_panel.add_theme_constant_override("separation", 8)
	add_child(world_panel)

	_add_panel_title("事件日志", Vector2(side_x, 652), Vector2(panel_w, 38))
	var log_bg := _panel(Vector2(side_x, 690), Vector2(panel_w, 146), C_PANEL_SOFT, C_BORDER)
	add_child(log_bg)
	log_box = RichTextLabel.new()
	log_box.bbcode_enabled = true
	log_box.scroll_active = true
	log_box.fit_content = false
	log_box.position = Vector2(side_x + 18, 704)
	log_box.size = Vector2(panel_w - 36, 116)
	add_child(log_box)

	var consequence := _panel(Vector2(side_x, 850), Vector2(panel_w, 76), Color(0.04, 0.06, 0.055, 0.92), C_BORDER)
	add_child(consequence)
	pressure_bar = _progress(Vector2(side_x + 24, 882), Vector2(130, 18), C_RED)
	add_child(pressure_bar)
	world_change_label = _label("", 18, C_GREEN, true)
	world_change_label.position = Vector2(side_x + 175, 872)
	add_child(world_change_label)


func _add_dialogue_panel() -> void:
	# Use the generated frame atlas as a visual frame, with live Godot labels above.
	var backing := _panel(Vector2(20, 610), Vector2(1248, 186), Color(0.025, 0.032, 0.04, 0.92), C_BORDER)
	add_child(backing)
	_add_texture_crop(UI_FRAMES, Rect2(20, 40, 930, 300), Vector2(20, 610), Vector2(1248, 186), 0.82)
	_add_texture_crop(PORTRAITS, Rect2(0, 0, 310, 250), Vector2(48, 640), Vector2(124, 124), 1.0)

	dialogue_name = _label("队长布兰", 28, C_AMBER, true)
	dialogue_name.position = Vector2(190, 632)
	add_child(dialogue_name)

	dialogue_text = RichTextLabel.new()
	dialogue_text.bbcode_enabled = true
	dialogue_text.fit_content = false
	dialogue_text.position = Vector2(190, 674)
	dialogue_text.size = Vector2(780, 78)
	dialogue_text.text = "这里是霜门，无关人员不得入内。说明来意。"
	add_child(dialogue_text)

	var tones := ["平和", "诚恳", "强硬", "威胁", "试探"]
	for i in tones.size():
		var b := Button.new()
		b.text = tones[i]
		b.position = Vector2(190 + i * 96, 746)
		b.size = Vector2(84, 36)
		b.add_theme_stylebox_override("normal", _button_style(Color("#403526")))
		b.add_theme_stylebox_override("hover", _button_style(Color("#5a4630")))
		b.add_theme_color_override("font_color", C_PARCHMENT)
		add_child(b)


func _add_input_panel() -> void:
	var input_bg := _panel(Vector2(20, 808), Vector2(1248, 116), C_PANEL, C_BORDER)
	add_child(input_bg)
	var label := _label("输入", 34, C_PARCHMENT, true)
	label.position = Vector2(50, 848)
	add_child(label)

	command_input = LineEdit.new()
	command_input.placeholder_text = "告诉他这些难民是被北境风暴迫使南下的平民，请求暂时收容。"
	command_input.text = "告诉他这些难民是被北境风暴迫使南下的平民，请求暂时收容。"
	command_input.position = Vector2(150, 838)
	command_input.size = Vector2(820, 54)
	command_input.add_theme_stylebox_override("normal", _line_edit_style())
	command_input.text_submitted.connect(_on_text_submitted)
	add_child(command_input)

	var execute := Button.new()
	execute.text = "执行\n(Enter)"
	execute.position = Vector2(1080, 828)
	execute.size = Vector2(150, 72)
	execute.pressed.connect(_submit_command)
	execute.add_theme_stylebox_override("normal", _button_style(Color("#5b3f23")))
	execute.add_theme_stylebox_override("hover", _button_style(Color("#765333")))
	execute.add_theme_color_override("font_color", C_AMBER)
	add_child(execute)


func _refresh_all() -> void:
	status_label.text = "生命 %d/32      耐力 %d/24      Tick %04d 夜晚      位置：霜门哨所 · 门楼      节奏：紧张" % [hp, stamina, tick]
	_refresh_npcs()
	_refresh_world()
	pressure_bar.value = pressure
	world_change_label.text = "世界变化\n难民入营  %s" % ("true" if refugees_admitted else "false")


func _refresh_npcs() -> void:
	for child in npc_panel.get_children():
		child.queue_free()
	npc_panel.add_child(_npc_card("队长布兰", "谨慎但公正。", "信任", brann_trust, C_GREEN, Rect2(0, 0, 310, 250)))
	npc_panel.add_child(_npc_card("哨兵沃斯", "害怕出错。", "紧张", voss_tension, C_RED, Rect2(313, 250, 313, 250)))


func _refresh_world() -> void:
	for child in world_panel.get_children():
		child.queue_free()
	world_panel.add_child(_world_row("难民入营", "true" if refugees_admitted else "false", C_GREEN if refugees_admitted else C_RED))
	world_panel.add_child(_world_row("霜门戒备等级", "高", C_RED))
	world_panel.add_child(_world_row("补给状况", "吃紧", C_AMBER))
	world_panel.add_child(_world_row("队长的压力", "中", C_AMBER))


func _npc_card(npc_name: String, note: String, metric: String, value: int, color: Color, portrait_region: Rect2) -> Control:
	var card := HBoxContainer.new()
	card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	card.add_theme_constant_override("separation", 10)

	var portrait := TextureRect.new()
	portrait.texture = _atlas(PORTRAITS, portrait_region)
	portrait.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	portrait.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	portrait.custom_minimum_size = Vector2(72, 72)
	card.add_child(portrait)

	var box := VBoxContainer.new()
	box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	var name := _label(npc_name, 22, C_AMBER, true)
	box.add_child(name)
	box.add_child(_label("关系：%s  %d/100" % [metric, value], 16, C_PARCHMENT, false))
	var bar := _progress(Vector2.ZERO, Vector2(210, 12), color)
	bar.value = value
	box.add_child(bar)
	box.add_child(_label(note, 15, C_DIM, false))
	card.add_child(box)
	return card


func _world_row(label_text: String, value_text: String, color: Color) -> Label:
	var row := _label("%-10s  %s" % [label_text, value_text], 20, color, true)
	return row


func _seed_log() -> void:
	_log("0125 夜晚  你抵达霜门哨所。", C_DIM)
	_log("0126 夜晚  与哨兵沃斯交谈。", C_PARCHMENT)
	_log("0126 夜晚  布兰对你的态度有所保留。", C_RED)
	_log("0127 夜晚  难民在门外聚集，气氛紧张。", C_AMBER)


func _on_text_submitted(_text: String) -> void:
	_submit_command()


func _submit_command() -> void:
	var text := command_input.text.strip_edges()
	if text.is_empty():
		text = "等待片刻，观察门楼里的动静。"
	command_input.text = ""
	tick += 1
	stamina = max(stamina - 1, 0)
	brann_trust = min(brann_trust + 12, 100)
	voss_tension = min(voss_tension + 6, 100)
	pressure = min(pressure + 3, 100)
	_log("你：%s" % text, C_AMBER)

	if brann_trust >= 48 and not refugees_admitted:
		refugees_admitted = true
		dialogue_name.text = "队长布兰"
		dialogue_text.text = "[color=#d8cbbb]好吧。先让孩子和伤者进来，其他人等我的命令。[/color]"
		_log("世界变化：难民入营 false → true", C_GREEN)
		_log("压力：补给压力上升，兵营里传来压低的争吵声。", C_RED)
	else:
		dialogue_name.text = "队长布兰"
		dialogue_text.text = "[color=#d8cbbb]你的话听起来慷慨，但我要守的是整座哨站。继续说。[/color]"
		_log("关系：队长布兰 信任 +0.12；哨兵沃斯 紧张 +0.06", C_GREEN)

	_refresh_all()


func _log(text: String, color: Color) -> void:
	if log_box == null:
		return
	log_box.append_text("[color=%s]%s[/color]\n" % [color.to_html(false), text])
	log_box.scroll_to_line(log_box.get_line_count())


func _add_panel_title(text: String, pos: Vector2, size: Vector2) -> void:
	var title := _panel(pos, size, Color(0.025, 0.032, 0.04, 0.95), C_BORDER)
	add_child(title)
	var label := _label(text, 22, C_PARCHMENT, true)
	label.position = pos + Vector2(18, 7)
	add_child(label)


func _add_icon(region: Rect2, pos: Vector2, size: Vector2) -> void:
	_add_texture_crop(ICONS, region, pos, size, 1.0)


func _add_texture_crop(texture: Texture2D, region: Rect2, pos: Vector2, size: Vector2, alpha: float) -> TextureRect:
	var tr := TextureRect.new()
	tr.texture = _atlas(texture, region)
	tr.position = pos
	tr.size = size
	tr.modulate = Color(1, 1, 1, alpha)
	tr.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	tr.stretch_mode = TextureRect.STRETCH_SCALE
	add_child(tr)
	return tr


func _atlas(texture: Texture2D, region: Rect2) -> AtlasTexture:
	var atlas := AtlasTexture.new()
	atlas.atlas = texture
	atlas.region = region
	return atlas


func _panel(pos: Vector2, size: Vector2, bg: Color, border: Color) -> Panel:
	var p := Panel.new()
	p.position = pos
	p.size = size
	p.add_theme_stylebox_override("panel", _panel_style(bg, border))
	return p


func _panel_style(bg: Color, border: Color) -> StyleBoxFlat:
	var s := StyleBoxFlat.new()
	s.bg_color = bg
	s.border_color = border
	s.border_width_left = 2
	s.border_width_top = 2
	s.border_width_right = 2
	s.border_width_bottom = 2
	s.corner_radius_top_left = 6
	s.corner_radius_top_right = 6
	s.corner_radius_bottom_left = 6
	s.corner_radius_bottom_right = 6
	s.content_margin_left = 10
	s.content_margin_right = 10
	s.content_margin_top = 8
	s.content_margin_bottom = 8
	return s


func _button_style(bg: Color) -> StyleBoxFlat:
	return _panel_style(bg, Color("#9b7a4b"))


func _line_edit_style() -> StyleBoxFlat:
	var s := _panel_style(Color("#080b0f"), Color("#5c5245"))
	s.content_margin_left = 18
	s.content_margin_right = 18
	return s


func _label(text: String, size: int, color: Color, bold: bool) -> Label:
	var label := Label.new()
	label.text = text
	label.add_theme_font_size_override("font_size", size)
	label.add_theme_color_override("font_color", color)
	if bold:
		label.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.75))
		label.add_theme_constant_override("shadow_offset_x", 1)
		label.add_theme_constant_override("shadow_offset_y", 1)
	return label


func _progress(pos: Vector2, size: Vector2, fill: Color) -> ProgressBar:
	var bar := ProgressBar.new()
	bar.position = pos
	bar.size = size
	bar.min_value = 0
	bar.max_value = 100
	bar.show_percentage = false
	var bg := StyleBoxFlat.new()
	bg.bg_color = Color("#181817")
	bg.corner_radius_top_left = 6
	bg.corner_radius_top_right = 6
	bg.corner_radius_bottom_left = 6
	bg.corner_radius_bottom_right = 6
	bar.add_theme_stylebox_override("background", bg)
	var fg := StyleBoxFlat.new()
	fg.bg_color = fill
	fg.corner_radius_top_left = 6
	fg.corner_radius_top_right = 6
	fg.corner_radius_bottom_left = 6
	fg.corner_radius_bottom_right = 6
	bar.add_theme_stylebox_override("fill", fg)
	return bar
