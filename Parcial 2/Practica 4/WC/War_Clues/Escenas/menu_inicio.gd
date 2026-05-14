extends Control

# Esta función se ejecuta al iniciar el menú
func _ready():
	# Esto ayuda a que puedas usar las flechas del teclado para elegir
	$VBoxContainer/Button.grab_focus()

# Función para el botón JUGAR
func _on_jugar_pressed():
	print("Intentando cambiar a la escena de juego...") # Esto aparecerá en la consola de Godot
	get_tree().change_scene_to_file("res://war_clues_game.tscn")

# Función para el botón CERRAR
func _on_cerrar_pressed():
	# Cierra el juego por completo
	get_tree().quit()

func _process(_delta):
	# Cerrar con ESC
	if Input.is_action_just_pressed("ui_cancel"):
		get_tree().quit()
		
	# Alternar pantalla completa con F11
	if Input.is_key_pressed(KEY_F11):
		# Solo ejecutamos el cambio si acabamos de presionar la tecla (evita rebotes)
		if Input.is_action_just_pressed("f11_toggle"): 
			toggle_fullscreen()

# Función auxiliar para el cambio de modo
func toggle_fullscreen():
	var current_mode = DisplayServer.window_get_mode()
	
	# Verificamos si NO es modo ventana (0)
	if current_mode != DisplayServer.WINDOW_MODE_WINDOWED:
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
	else:
		# Si estaba en ventana, lo mandamos a pantalla completa
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_EXCLUSIVE_FULLSCREEN)
