extends Control

# --- BASE DE DATOS TÉCNICA (50 Tanques - Firma Digital Única) ---
var base_tanques = {
	# --- SUECIA ---
	"Strv 103B": {"nacion": "Suecia", "clase": "TD", "tier_alto": true, "cal_100_110": true, "peso_25_60": true, "vel_50": true, "dep_10": true, "modo_esp": true, "vision_390": false, "potencia_20": true, "torreta_360": false, "ruedas": false, "cargador": false, "autoreloader": false, "autocannon": false, "blindaje_200": false},
	"UDES 03": {"nacion": "Suecia", "clase": "TD", "tier_alto": false, "cal_100_110": true, "peso_25": true, "vel_50": true, "dep_10": true, "modo_esp": true, "vision_390": false, "potencia_20": true, "torreta_360": false, "ruedas": false, "cargador": false, "autoreloader": false, "autocannon": false, "blindaje_200": false},
	"Strv 74": {"nacion": "Suecia", "clase": "Mediano", "tier_alto": false, "cal_75_90": true, "peso_25_60": true, "vel_50": false, "dep_10": true, "torreta_360": true, "ruedas": false, "cargador": false, "autoreloader": false, "autocannon": false, "blindaje_200": false},
	"Strv 81": {"nacion": "Suecia", "clase": "Mediano", "tier_alto": false, "cal_75_90": true, "peso_25_60": true, "vel_50": false, "dep_10": true, "torreta_360": true, "blindaje_200": true, "ruedas": false, "cargador": false, "autoreloader": false, "autocannon": false},
	"Kranvagn": {"nacion": "Suecia", "clase": "Pesado", "tier_alto": true, "cal_120_130": true, "peso_25_60": true, "dep_10": true, "modo_esp": true, "cargador": true, "blindaje_200": true, "torreta_360": true, "ruedas": false, "vision_390": false},

	# --- URSS ---
	"IS-7": {"nacion": "URSS", "clase": "Pesado", "tier_alto": true, "cal_120_130": true, "peso_60_100": true, "vel_50": true, "blindaje_200": true, "torreta_360": true, "dep_5": true, "ruedas": false, "cargador": false, "autoreloader": false, "autocannon": false},
	"T-34": {"nacion": "URSS", "clase": "Mediano", "tier_alto": false, "cal_75_90": true, "peso_25_60": true, "vel_50": true, "torreta_360": true, "dep_5": true, "ruedas": false, "cargador": false, "autoreloader": false, "autocannon": false},
	"KV-2": {"nacion": "URSS", "clase": "Pesado", "tier_alto": false, "cal_150_mas": true, "peso_60_100": true, "torreta_360": true, "dep_7": true, "vel_50": false, "ruedas": false, "cargador": false},
	"KV-1": {"nacion": "URSS", "clase": "Pesado", "tier_alto": false, "cal_75_90": true, "peso_25_60": true, "torreta_360": true, "dep_5": true, "vel_50": false, "ruedas": false},
	"ISU-152": {"nacion": "URSS", "clase": "TD", "tier_alto": false, "cal_150_mas": true, "peso_25_60": true, "torreta_360": false, "dep_5": true, "vel_50": false, "ruedas": false},
	"IS": {"nacion": "URSS", "clase": "Pesado", "tier_alto": false, "cal_120_130": true, "peso_25_60": true, "torreta_360": true, "dep_5": true, "ruedas": false},
	"Obj 704": {"nacion": "URSS", "clase": "TD", "tier_alto": true, "cal_150_mas": true, "peso_60_100": true, "torreta_360": false, "dep_5": true, "ruedas": false},
	"T-100-LT": {"nacion": "URSS", "clase": "Ligero", "tier_alto": true, "cal_100_110": true, "peso_25": true, "vel_50": true, "vision_390": true, "torreta_360": true, "ruedas": false},

	# --- ALEMANIA ---
	"Maus": {"nacion": "Alemania", "clase": "Pesado", "tier_alto": true, "cal_120_130": true, "peso_100_mas": true, "blindaje_200": true, "torreta_360": true, "vision_390": true, "vel_50": false, "ruedas": false},
	"E100": {"nacion": "Alemania", "clase": "Pesado", "tier_alto": true, "cal_150_mas": true, "peso_100_mas": true, "blindaje_200": true, "torreta_360": true, "vision_390": true, "ruedas": false},
	"Tiger I": {"nacion": "Alemania", "clase": "Pesado", "tier_alto": false, "cal_75_90": true, "peso_25_60": true, "torreta_360": true, "dep_7": true, "vision_390": true, "vel_50": false},
	"Leopard 1": {"nacion": "Alemania", "clase": "Mediano", "tier_alto": true, "cal_100_110": true, "peso_25_60": true, "vel_50": true, "vision_390": true, "torreta_360": true, "potencia_20": true},
	"E50": {"nacion": "Alemania", "clase": "Mediano", "tier_alto": true, "cal_75_90": true, "peso_60_100": true, "vel_50": true, "torreta_360": true, "blindaje_200": false},

	# --- FRANCIA ---
	"Bourrasque": {"nacion": "Francia", "clase": "Mediano", "tier_alto": false, "cal_100_110": true, "peso_25": true, "vel_50": true, "cargador": true, "vision_390": true, "torreta_360": true, "dep_5": true, "ruedas": false, "potencia_20": true},
	"Projet Louis": {"nacion": "Francia", "clase": "Ligero", "tier_alto": true, "cal_100_110": true, "peso_25": true, "vel_50": true, "cargador": true, "vision_390": true, "torreta_360": true, "dep_5": true, "ruedas": false, "potencia_20": true},
	"EBR 105": {"nacion": "Francia", "clase": "Ligero", "tier_alto": true, "cal_100_110": true, "peso_25": true, "vel_50": true, "ruedas": true, "modo_esp": true, "torreta_360": true, "vision_390": false},
	"Foch 155": {"nacion": "Francia", "clase": "TD", "tier_alto": true, "cal_150_mas": true, "peso_25_60": true, "cargador": true, "torreta_360": false, "vel_50": true},
	"AMX M4 51": {"nacion": "Francia", "clase": "Pesado", "tier_alto": true, "cal_120_130": true, "peso_60_100": true, "dep_7": true, "blindaje_200": true, "torreta_360": true},
	"Char Futur 4": {"nacion": "Francia", "clase": "Mediano", "tier_alto": true, "cal_100_110": true, "peso_25_60": true, "cargador": true, "vel_50": true, "torreta_360": true},
	"Lorr. 40t": {"nacion": "Francia", "clase": "Mediano", "tier_alto": false, "cal_100_110": true, "peso_25_60": true, "cargador": true, "vel_50": true, "torreta_360": true},

	# --- EEUU ---
	"Ares 75": {"nacion": "EEUU", "clase": "Mediano", "tier_alto": false, "cal_75_90": true, "autocannon": true, "peso_25_60": true, "vel_50": true, "dep_10": true, "torreta_360": true},
	"E8 Sherman": {"nacion": "EEUU", "clase": "Mediano", "tier_alto": false, "cal_75_90": true, "peso_25_60": true, "dep_10": true, "torreta_360": true, "vision_390": true},
	"Hellcat": {"nacion": "EEUU", "clase": "TD", "tier_alto": false, "cal_75_90": true, "peso_25": true, "vel_50": true, "torreta_360": true, "dep_10": true},
	"T57 Heavy": {"nacion": "EEUU", "clase": "Pesado", "tier_alto": true, "cal_120_130": true, "peso_25_60": true, "cargador": true, "torreta_360": true, "dep_7": true},
	"M48 Patton": {"nacion": "EEUU", "clase": "Mediano", "tier_alto": true, "cal_100_110": true, "peso_25_60": true, "dep_10": true, "torreta_360": true, "vision_390": true},
	"T49": {"nacion": "EEUU", "clase": "Ligero", "tier_alto": true, "cal_150_mas": true, "peso_25": true, "vel_50": true, "dep_10": true, "torreta_360": true},
	"T20": {"nacion": "EEUU", "clase": "Mediano", "tier_alto": false, "cal_75_90": true, "peso_25_60": true, "vel_50": true, "dep_10": true, "torreta_360": true},
	"T95": {"nacion": "EEUU", "clase": "TD", "tier_alto": true, "cal_150_mas": true, "peso_60_100": true, "torreta_360": false, "dep_5": true, "blindaje_200": true},

	# --- REINO UNIDO ---
	"Cromwell": {"nacion": "Reino Unido", "clase": "Mediano", "tier_alto": false, "cal_75_90": true, "peso_25_60": true, "vel_50": true, "dep_10": true, "torreta_360": true},
	"Concept 5": {"nacion": "Reino Unido", "clase": "Mediano", "tier_alto": true, "cal_100_110": true, "peso_25_60": true, "ruedas": true, "torreta_360": true, "vel_50": true},
	"FSV Sch. A": {"nacion": "Reino Unido", "clase": "Mediano", "tier_alto": false, "cal_75_90": true, "peso_25": true, "ruedas": true, "dep_10": true, "torreta_360": true},
	"Centurion I": {"nacion": "Reino Unido", "clase": "Mediano", "tier_alto": false, "cal_75_90": true, "peso_25_60": true, "dep_10": true, "torreta_360": true, "blindaje_200": true},
	"Manticore": {"nacion": "Reino Unido", "clase": "Ligero", "tier_alto": true, "cal_100_110": true, "peso_25": true, "vel_50": true, "torreta_360": true, "vision_390": true},
	"LHMTV": {"nacion": "Reino Unido", "clase": "Ligero", "tier_alto": false, "cal_75_90": true, "peso_25": true, "vel_50": true, "dep_10": true, "torreta_360": true},
	"Charioteer": {"nacion": "Reino Unido", "clase": "TD", "tier_alto": false, "cal_100_110": true, "peso_25_60": true, "torreta_360": true, "dep_10": true, "vel_50": true},
	"Staghound": {"nacion": "Reino Unido", "clase": "Mediano", "tier_alto": false, "cal_75_90": true, "peso_25": true, "ruedas": true, "torreta_360": true, "dep_5": true},
	"Churchill I": {"nacion": "Reino Unido", "clase": "Pesado", "tier_alto": false, "cal_75_90": true, "peso_25_60": true, "torreta_360": true, "dep_menor_5": true},
	"FV4005": {"nacion": "Reino Unido", "clase": "TD", "tier_alto": true, "cal_150_mas": true, "peso_25_60": true, "torreta_360": false, "dep_10": true, "vision_390": true},

	# --- JAPÓN ---
	"STB-1": {"nacion": "Japón", "clase": "Mediano", "tier_alto": true, "cal_100_110": true, "peso_25_60": true, "modo_esp": true, "dep_10": true, "torreta_360": true},
	"Type 5 Heavy": {"nacion": "Japón", "clase": "Pesado", "tier_alto": true, "cal_150_mas": true, "peso_100_mas": true, "blindaje_200": true, "torreta_360": true},
	"Type 71": {"nacion": "Japón", "clase": "Pesado", "tier_alto": true, "cal_120_130": true, "peso_60_100": true, "modo_esp": true, "dep_10": true, "torreta_360": true},
	"Ka-Ri": {"nacion": "Japón", "clase": "TD", "tier_alto": false, "cal_120_130": true, "peso_60_100": true, "torreta_360": false, "dep_7": true},

	# --- CHECOSLOVAQUIA, POLONIA e ITALIA ---
	"Skoda T40": {"nacion": "Checoslovaquia", "clase": "Mediano", "tier_alto": false, "cal_75_90": true, "peso_25_60": true, "vel_50": true, "torreta_360": true},
	"Skoda T17": {"nacion": "Checoslovaquia", "clase": "Ligero", "tier_alto": false, "cal_75_90": true, "peso_25": true, "cargador": true, "torreta_360": true},
	"60TP": {"nacion": "Polonia", "clase": "Pesado", "tier_alto": true, "cal_150_mas": true, "peso_60_100": true, "blindaje_200": true, "torreta_360": true},
	"Minotauro": {"nacion": "Italia", "clase": "TD", "tier_alto": true, "cal_120_130": true, "peso_60_100": true, "cargador": true, "autoreloader": true, "torreta_360": false}
}

# --- LÓGICA DE JUEGO ---
var candidatos = []
var preguntas_disponibles = []
var pregunta_actual = {}
var juego_activo = false
var esperando_inicio = false
var tanque_propuesto = ""

@onready var video = $VideoStreamPlayer
@onready var interfaz_capa = $CanvasLayer
@onready var chasis_radio = $CanvasLayer/TextureRect
@onready var label_texto = $CanvasLayer/TextureRect/VBoxContainer/RichTextLabel
@onready var btn_si = $CanvasLayer/TextureRect/Boton_SI
@onready var btn_no = $CanvasLayer/TextureRect/Boton_NO
@onready var luz_verde = $CanvasLayer/TextureRect/LuzVerde
@onready var luz_roja = $CanvasLayer/TextureRect/LuzRoja
@onready var fade_final = $CanvasLayer/FadeFinal
@onready var ventana_aprendizaje = $CanvasLayer/VentanaAprendizaje

# Audio
@onready var musica_1 = $CanvasLayer/Soundtrack
@onready var musica_2 = $CanvasLayer/WarAmbience
@onready var audio_beep = $CanvasLayer/AudioBeep
@onready var audio_morse = $CanvasLayer/AudioMorse

func _ready():
	interfaz_capa.hide()
	ventana_aprendizaje.hide()
	fade_final.hide()
	fade_final.modulate.a = 0.0
	chasis_radio.modulate = Color(0, 0, 0, 1)
	btn_si.disabled = true; btn_no.disabled = true
	btn_si.pressed.connect(func(): _on_respuesta_usuario(true))
	btn_no.pressed.connect(func(): _on_respuesta_usuario(false))
	video.play()

func _process(_delta):
	if Input.is_action_just_pressed("ui_cancel"): get_tree().quit()
	if Input.is_key_pressed(KEY_F11) or Input.is_action_just_pressed("f11_toggle"):
		toggle_fullscreen()

func toggle_fullscreen():
	var mode = DisplayServer.window_get_mode()
	if mode != DisplayServer.WINDOW_MODE_EXCLUSIVE_FULLSCREEN:
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_EXCLUSIVE_FULLSCREEN)
	else:
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)

func _on_respuesta_usuario(valor: bool):
	if esperando_inicio:
		parpadear_foco("SI" if valor else "NO")
		if valor:
			esperando_inicio = false
			inicializar_preguntas()
		return

	if tanque_propuesto != "":
		parpadear_foco("SI" if valor else "NO")
		if valor: confirmar_victoria()
		else: modo_aprendizaje()
		return

	if juego_activo:
		parpadear_foco("SI" if valor else "NO")
		procesar_respuesta(valor)

# --- MOTOR DE INFERENCIA DETERMINÍSTICO ---

func inicializar_preguntas():
	candidatos = base_tanques.keys()
	preguntas_disponibles = [
		{"id": "tier_alto", "texto": "¿Es un vehículo de Tier IX o X?"},
		{"id": "cal_150_mas", "texto": "¿Su calibre es de 150mm o superior?"},
		{"id": "cal_120_130", "texto": "¿Su calibre está entre los 120mm y 130mm?"},
		{"id": "cal_100_110", "texto": "¿Su calibre principal es de 100mm a 110mm?"},
		{"id": "cal_75_90", "texto": "¿Es un calibre pequeño (75mm a 90mm)?"},
		{"id": "peso_100_mas", "texto": "¿Es un superpesado de 100 toneladas o más?"},
		{"id": "peso_60_100", "texto": "¿Su peso bruto está entre 60 y 100 toneladas?"},
		{"id": "peso_25_60", "texto": "¿El peso está en el rango medio de 25 a 60 toneladas?"},
		{"id": "ruedas", "texto": "¿Utiliza neumáticos en lugar de orugas?"},
		{"id": "dep_10", "texto": "¿Tiene una depresión de cañón de 10 grados o más?"},
		{"id": "dep_7", "texto": "¿Tiene una depresión de cañón de al menos 7 grados?"},
		{"id": "modo_esp", "texto": "¿Cuenta con mecánicas especiales (Asedio/Turbos)?"},
		{"id": "cargador", "texto": "¿Utiliza sistema de Autocargador?"},
		{"id": "autoreloader", "texto": "¿Utiliza sistema de Autorecarga secuencial?"},
		{"id": "autocannon", "texto": "¿Su armamento es un auto-cañón de ráfaga rápida?"},
		{"id": "vision_390", "texto": "¿Su rango de visión base supera los 390m?"},
		{"id": "potencia_20", "texto": "¿Su relación potencia/peso es mayor a 20hp/t?"},
		{"id": "blindaje_200", "texto": "¿Tiene más de 200mm de blindaje frontal?"},
		{"id": "torreta_360", "texto": "¿Su torreta gira los 360 grados?"}
	]
	
	for c in ["Pesado", "Mediano", "Ligero", "TD"]:
		preguntas_disponibles.append({"id": "clase", "valor": c, "texto": "¿Es un vehículo de clase: " + c + "?"})
	for n in ["Alemania", "URSS", "EEUU", "Francia", "Reino Unido", "Suecia", "Japón", "Italia", "Polonia", "Checoslovaquia"]:
		preguntas_disponibles.append({"id": "nacion", "valor": n, "texto": "¿Pertenece a la nación de " + n + "?"})
	
	preguntas_disponibles.shuffle()
	juego_activo = true
	siguiente_pregunta()

func siguiente_pregunta():
	if candidatos.size() == 1:
		tanque_propuesto = candidatos[0]
		mostrar_dialogo("Radio: Identificación 100% positiva: " + tanque_propuesto + ". ¿Es correcto?")
		return
	
	if candidatos.size() == 0 or preguntas_disponibles.size() == 0:
		modo_aprendizaje()
		return

	pregunta_actual = preguntas_disponibles.pop_back()
	mostrar_dialogo("Radio: " + pregunta_actual["texto"])

func procesar_respuesta(respuesta: bool):
	btn_si.disabled = true; btn_no.disabled = true
	var id = pregunta_actual["id"]
	
	if (id == "nacion" or id == "clase") and respuesta:
		preguntas_disponibles = preguntas_disponibles.filter(func(q): return q["id"] != id)
	
	if id in ["cal_150_mas", "cal_120_130", "cal_100_110", "cal_75_90"] and respuesta:
		preguntas_disponibles = preguntas_disponibles.filter(func(q): return q["id"] not in ["cal_150_mas", "cal_120_130", "cal_100_110", "cal_75_90"])

	var nuevos = []
	for t in candidatos:
		var cumple = false
		if id == "nacion" or id == "clase":
			cumple = (base_tanques[t].get(id) == pregunta_actual["valor"])
		else:
			cumple = (base_tanques[t].get(id, false) == respuesta)
		
		if id == "nacion" or id == "clase":
			if (respuesta and cumple) or (not respuesta and not cumple): nuevos.append(t)
		else:
			if cumple: nuevos.append(t)
	
	candidatos = nuevos
	await pausa(2.2)
	btn_si.disabled = false; btn_no.disabled = false
	siguiente_pregunta()

# --- PROTOCOLOS DE CIERRE ---

func confirmar_victoria():
	juego_activo = false
	await mostrar_dialogo("Radio: Muy bien soldado, en este momento enviamos refuerzos y piezas para su tanque.")
	await pausa(3.0)
	protocolo_salida()

func modo_aprendizaje():
	juego_activo = false
	tanque_propuesto = ""
	await mostrar_dialogo("Radio: Lo siento soldado, no pudimos identificar su tanque, buena suerte.")
	await pausa(2.5)
	ventana_aprendizaje.show()

func protocolo_salida():
	fade_final.show()
	var t = create_tween()
	t.parallel().tween_property(chasis_radio, "modulate:a", 0.0, 2.0)
	t.parallel().tween_property(fade_final, "modulate:a", 1.0, 2.0)
	await t.finished
	label_texto.text = "Gracias por jugar a Tank Intelligence"
	label_texto.visible_ratio = 1.0
	label_texto.modulate = Color(1,1,1,1)
	await pausa(4.0)
	get_tree().change_scene_to_file("res://menu_inicio.tscn")

# --- SOPORTE TÉCNICO ---

func mostrar_dialogo(texto: String):
	label_texto.text = texto; label_texto.visible_ratio = 0.0
	audio_morse.play()
	var t = create_tween()
	t.tween_property(label_texto, "visible_ratio", 1.0, 2.0)
	await t.finished
	audio_morse.stop()

func parpadear_foco(tipo: String):
	var luz = luz_verde if tipo == "SI" else luz_roja
	audio_beep.play()
	for i in 2:
		luz.enabled = true
		await get_tree().create_timer(0.15).timeout
		luz.enabled = false
		await get_tree().create_timer(0.15).timeout

func pausa(segundos: float):
	await get_tree().create_timer(segundos).timeout

func _on_video_stream_player_finished():
	$VideoStreamPlayer.hide(); interfaz_capa.show()
	gestionar_entrada_atmosferica()

func gestionar_entrada_atmosferica():
	musica_1.volume_db = -60; musica_2.volume_db = -60
	musica_1.play(); musica_2.play()
	var at = create_tween()
	at.parallel().tween_property(musica_1, "volume_db", 0.0, 30.0)
	at.parallel().tween_property(musica_2, "volume_db", 10.0, 5.0)
	var rt = create_tween()
	rt.tween_property(chasis_radio, "modulate", Color(1,1,1,1), 3.0)
	await rt.finished
	secuencia_narrativa()

func secuencia_narrativa():
	await mostrar_dialogo("Radio: *bzztt* Unidad 7-A reporten su estado, ¿fueron impactados?")
	await pausa(1.5)
	await mostrar_dialogo("Radio: ¿La tripulación se encuentra bien?"); await pausa(0.8); await parpadear_foco("SI"); await pausa(1.5)
	await mostrar_dialogo("Radio: ¿Siguen expuestos a fuego enemigo?"); await pausa(0.8); await parpadear_foco("NO"); await pausa(1.5)
	await mostrar_dialogo("Radio: Entendido, continuaremos comunicándonos mediante comandos de afirmativo y negativo, pero necesito saber lo antes posible qué tanque llevan para enviarles refuerzos...")
	await pausa(3.0)
	await mostrar_dialogo("Radio: Le haré unas preguntas para determinar qué tanque lleva, ¿está listo?")
	esperando_inicio = true
	btn_si.disabled = false; btn_no.disabled = false
	label_texto.modulate = Color(1.4, 1.4, 1.4)
