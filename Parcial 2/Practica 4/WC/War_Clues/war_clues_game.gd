extends Control

# --- BASE DE DATOS ENCICLOPÉDICA (Para el Panel de Información) ---
var info_personajes = {
	"USA": "USA: En la gran guerra nuestro país organizó un ataque a estados unidos por cielo mar y tierra en febrero de 1946 finalizando en noviembre de ese mismo año.",
	"Alemania": "ALEMANIA: Como parte de los eventos sucedidos en la gran guerra la extensa invasión a tierras germanas fue llevada a cabo de abril de 1947 a octubre de 1949.",
	"Francia": "FRANCIA: A mediados de la guerra, Francia organizó un feroz ataque a nuestro país que sacudió nuestras fronteras a inicios de 1950.",
	"Reino Unido": "REINO UNIDO: Después de algunos años en relativa paz, un explosivo avance por parte de nuestras tropas logró que los británicos se retiraran de todo territorio ocupado fuera de su isla de enero de 1951 hasta abril de ese mismo año, sin embargo su retirada no fue pacífica, sufrimos muchas bajas en el proceso.",
	"Italia": "ITALIA: A finales de la guerra, en 1952 nuestro país ejecutó un ataque relámpago a Italia en respuesta a los bombardeos sufridos en nuestra capital, sin embargo debido a el gran avance tecnológico con el que contaba Italia en ese momento lograron repeler nuestro avance."
}

var info_lugares = {
	"Desierto": "DESIERTO: Un área extremadamente calurosa y seca, de difícil acceso, la arena se mete en todos lados, el metal del tanque te cocina como lo haría una sartén en pleno fuego, la pesadilla de cualquier tanquista e ingeniero.",
	"Bosque": "BOSQUE: Baja visibilidad, avance lento y mucha vegetación que en ocasiones era amarrada a los tanques en forma de camuflaje con la esperanza no ser detectados por el enemigo tan fácilmente.",
	"Nevado": "NIEVE: Temperaturas que llevan al extremo a cada mecanismo y ser vivo, debido a la alta humedad del ambiente y a pasar constantemente sobre recientes nevadas, la nieve se metía en cada recoveco del tanque generando así gruesas capas de óxido.",
	"Pantano": "PANTANO: Uno de los entornos más desafiantes incluso para el conductor de tanques más experimentado, llegando a sumergirse en resbaladizo y espeso lodo a profundidades de hasta metro y medio, donde el lodo queda atrapado en cada engrane, rueda y hueco que el tanque tenga.",
	"Ciudad": "CIUDAD: Pareciera ser uno de los entornos menos desafiantes, quizá no lo sea con el tanque en sí, pero lo es con la tripulación; estrechas calles, no saber que puedes encontrar al girar en la siguiente esquina, sortear nubes de polvo y escombros, además de la constante posibilidad de ser flanqueado, lo convierten en la peor pesadilla, incluso de las mejores tripulaciones."
}

var info_armas = {
	"Bomba": "BOMBA: Una de las primeras armas implementadas después de empezar a usar aviones con intenciones bélicas, usada exclusivamente en ataques aire a tierra, su intención es caer desde el cielo al objetivo y mediante una carga explosiva de gran tamaño causar un daño devastador.",
	"Mina": "MINA ANTI TANQUE: Las minas anti tanque son elementos explosivos colocados usualmente en caminos de vehículos pesados, estas se activan con la presión ejercida por el vehículo una vez este la pisa, están diseñadas para dirigir la explosión hacia arriba maximizando el daño y así perforar el blindaje inferior del tanque para destruirlo o como mínimo inmovilizarlo.",
	"Cazatanques": "CAZATANQUES: Una categoría de vehículos blindados con potentes cañones cuyo objetivo principal es destruir vehículos blindados enemigos a largas distancias, generalmente tienen un solo cañón de gran calibre con el que al disparar a su objetivo atraviesan el grueso blindaje logrando destruirlo de un solo impacto.",
	"Misil": "MISIL ANTI TANQUE: Conocidos generalmente por las siglas ATGM, esta es un arma de más alta tecnología; ojivas tipo HEAT propulsadas por un cohete guiadas generalmente a láser o por calor a su objetivo, al impactar sueltan un chorro de metal líquido a altísima temperatura con el que perfora el blindaje principal, destruyendo o matando a todo módulo o tripulante a su paso. Debido a la forma en que opera la ojiva, el orificio de impacto resultante es pequeño y deja marcas radiales alrededor del impacto.",
	"Granada": "GRANADA: Este es un explosivo de mano operado por infantería, una carga pequeña de TNT explota después de unos segundos de haber liberado el mecanismo, esto expulsa fragmentos de metal a alta velocidad que pueden ser letales a corta distancia, son usadas principalmente como arma antipersona o contra vehículos sin blindaje. No son efectivas contra el blindaje de un tanque puesto que no pueden dañarlo y mucho menos perforarlo, sin embargo, cuando un tanque era emboscado, un soldado podía abrir una de las escotillas del tanque y arrojar una o varias granadas a su interior con el objetivo de matar a toda la tripulación."
}

# --- BASE DE DATOS DE PISTAS (Generación de Casos) ---
var pistas_personajes = {
	"USA": "Los datos del reporte indican que el tanque fue recuperado en mayo de 1946.",
	"Alemania": "El reporte del tanque tiene poca información pero indica que su recuperación se dio en septiembre de 1948.",
	"Francia": "Este tanque no tiene registro exacto de cuando fue recuperado, aunque en su lateral parece tener una inscripción que dice R - 120850 que indica la fecha que se recuperó el 12 de agosto de 1950.",
	"Reino Unido": "Este tanque cuenta un informe detallado, aunque no indica la fecha de su recuperación indica que perteneció a la brigada de acorazados S76 desplegada únicamente desde enero de 1951 hasta abril de ese mismo año.",
	"Italia": "El reporte no indica mucho, pero este tanque es una variante más moderna cuyas unidades fueron desplegadas hasta finales de 1952."
}

var pistas_lugares = {
	"Desierto": "El tanque parece estar limpio y libre de óxido a excepción de toda la arena fina que tiene esparcida en cada recoveco de este.",
	"Bosque": "El exterior del tanque parece tener un poco de tierra seca, ramas secas de árbol amarradas como camuflaje y hojas secas por todo el frente y las orugas.",
	"Nevado": "El tanque está mayormente limpio de no ser por una excesiva cantidad de óxido en todo el sistema de tracción del tanque, sobre todo en las orugas.",
	"Pantano": "El tanque está muy sucio, lleno de montones de lo que parece ser lodo seco, tiene una presencia ligera de óxido y algunas hojas en las orugas.",
	"Ciudad": "El tanque está mayormente limpio, no presenta residuos de ningún tipo en su exterior, solo un poco de polvo."
}

var pistas_armas = {
	"Bomba": "El tanque presenta severo daño en la parte superior, donde presenta pronunciadas abolladuras y una gran perforación en el techo de la torreta.",
	"Mina": "El tanque presenta un gran daño en su sistema de tracción con gran parte de este destruido de un lado, el otro lado presenta daños considerables, el suelo del tanque presenta una perforación leve.",
	"Cazatanques": "El tanque presenta un gran impacto con perforación en la parte frontal del chasis, es un solo impacto limpio en forma de círculo de unos 25cm de diámetro.",
	"Misil": "El blindaje lateral del tanque presenta una perforación de pequeño diámetro con marcas en forma de estrella que marcan alrededor de la zona del impacto con un poco de restos de pólvora quemada en esa misma zona.",
	"Granada": "El exterior del tanque está intacto, no presenta ningún daño, sin embargo el interior del tanque está en mal estado, con instrumentos dañados, controles quemados, ópticas destruidas y mecanismos severamente deteriorados, lo que parece producto de una explosión y un incendio."
}

var casos_predefinidos = [
	{"personaje": "USA", "lugar": "Pantano", "arma": "Mina"},
	{"personaje": "Alemania", "lugar": "Ciudad", "arma": "Granada"},
	{"personaje": "Francia", "lugar": "Bosque", "arma": "Bomba"},
	{"personaje": "Reino Unido", "lugar": "Nevado", "arma": "Cazatanques"},
	{"personaje": "Italia", "lugar": "Desierto", "arma": "Misil"}
]

# --- VARIABLES DE ESTADO ---
var caso_actual = {}
var seleccion_jugador = {"personaje": "", "lugar": "", "arma": ""}

# --- REFERENCIAS A NODOS ---
@onready var panel_lore = $PanelLore
@onready var panel_info = $PanelInfo
@onready var panel_pistas = $PanelPistas
@onready var panel_acusacion = $PanelAcusacion
@onready var panel_resultado = $PanelResultado

@onready var txt_detalle_info = $PanelInfo/TextoDetalle
@onready var txt_pistas = $PanelPistas/TextoPistas
@onready var txt_resumen_acusacion = $PanelAcusacion/ResumenSeleccion
@onready var txt_resultado = $PanelResultado/TextoResultado
@onready var musica = $MusicaFondo

func _ready():
	randomize()
	if musica and not musica.playing:
		musica.play()
		
	mostrar_panel(panel_lore)
	conectar_botones_navegacion()
	conectar_botones_info()
	conectar_botones_acusacion()

func _process(_delta):
	if Input.is_action_just_pressed("ui_cancel"): 
		get_tree().quit()
	if Input.is_key_pressed(KEY_F11) or Input.is_action_just_pressed("f11_toggle"):
		toggle_fullscreen()

func toggle_fullscreen():
	var mode = DisplayServer.window_get_mode()
	if mode != DisplayServer.WINDOW_MODE_EXCLUSIVE_FULLSCREEN:
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_EXCLUSIVE_FULLSCREEN)
	else:
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)

# --- MÁQUINA DE ESTADOS (PANELES) ---
func mostrar_panel(panel_activo):
	panel_lore.hide()
	panel_info.hide()
	panel_pistas.hide()
	panel_acusacion.hide()
	panel_resultado.hide()
	panel_activo.show()

# --- NAVEGACIÓN PRINCIPAL ---
func conectar_botones_navegacion():
	$PanelLore/BotonIniciar.pressed.connect(func(): mostrar_panel(panel_info))
	$PanelInfo/BotonSiguiente.pressed.connect(_generar_caso)
	$PanelPistas/BotonRegresarInfo.pressed.connect(func(): mostrar_panel(panel_info))
	$PanelPistas/BotonContinuar.pressed.connect(func(): mostrar_panel(panel_acusacion))
	$PanelAcusacion/BotonRegresarPistas.pressed.connect(func(): mostrar_panel(panel_pistas))
	$PanelAcusacion/BotonContinuar.pressed.connect(_verificar_reporte) 
	
	$PanelResultado/BotonFinalizar.pressed.connect(func(): 
		if ResourceLoader.exists("res://menu_inicio.tscn"):
			get_tree().change_scene_to_file("res://menu_inicio.tscn")
		elif ResourceLoader.exists("res://Escenas/menu_inicio.tscn"):
			get_tree().change_scene_to_file("res://Escenas/menu_inicio.tscn")
		else:
			print("Error: No se encontró la escena menu_inicio.tscn")
			get_tree().quit() 
	)

# --- LÓGICA DE JUEGO ---
func _generar_caso():
	# CANDADO LÓGICO: Solo elige un caso nuevo si está vacío.
	if caso_actual.is_empty():
		caso_actual = casos_predefinidos.pick_random()
		$PanelInfo/BotonSiguiente.text = "REVISAR PISTAS" # Cambio de UX
	
	var texto = "[color=#ffd3b6]Pista del Origen:[/color]\n" + pistas_personajes[caso_actual["personaje"]] + "\n\n"
	texto += "[color=#a8e6cf]Pista del Entorno:[/color]\n" + pistas_lugares[caso_actual["lugar"]] + "\n\n"
	texto += "[color=#ff8b94]Pista del Armamento:[/color]\n" + pistas_armas[caso_actual["arma"]]
	
	txt_pistas.text = texto
	mostrar_panel(panel_pistas)

func _verificar_reporte():
	var aciertos = 0
	var reporte_final = ""
	
	if seleccion_jugador["personaje"] == "": return 
	
	if seleccion_jugador["personaje"] == caso_actual["personaje"]:
		aciertos += 1
		reporte_final += "[color=green]✓ Nación correcta:[/color] " + seleccion_jugador["personaje"] + "\n"
	else:
		reporte_final += "[color=red]✗ Nación incorrecta.[/color] (Seleccionó " + seleccion_jugador["personaje"] + ")\n"
		
	if seleccion_jugador["lugar"] == caso_actual["lugar"]:
		aciertos += 1
		reporte_final += "[color=green]✓ Entorno correcto:[/color] " + seleccion_jugador["lugar"] + "\n"
	else:
		reporte_final += "[color=red]✗ Entorno incorrecto.[/color] (Seleccionó " + seleccion_jugador["lugar"] + ")\n"
		
	if seleccion_jugador["arma"] == caso_actual["arma"]:
		aciertos += 1
		reporte_final += "[color=green]✓ Armamento correcto:[/color] " + seleccion_jugador["arma"] + "\n"
	else:
		reporte_final += "[color=red]✗ Armamento incorrecto.[/color] (Seleccionó " + seleccion_jugador["arma"] + ")\n"
	
	if aciertos == 3:
		reporte_final = "[center][b]¡MISIÓN EXITOSA, INGENIERO![/b][/center]\n\n" + reporte_final
	else:
		reporte_final = "[center][b]REPORTE DENEGADO. ANÁLISIS FALLIDO.[/b][/center]\n\n" + reporte_final
		
	txt_resultado.text = reporte_final
	txt_resultado.bbcode_enabled = true
	mostrar_panel(panel_resultado)

# --- CONEXIÓN AUTOMÁTICA DE BOTONES ---
func conectar_botones_info():
	var btn_paths = {
		"USA": $PanelInfo/ContenedorColumnas/ColPersonajes/BotonUSA,
		"Alemania": $PanelInfo/ContenedorColumnas/ColPersonajes/BotonALE,
		"Francia": $PanelInfo/ContenedorColumnas/ColPersonajes/BotonFRA,
		"Reino Unido": $PanelInfo/ContenedorColumnas/ColPersonajes/BotonUK,
		"Italia": $PanelInfo/ContenedorColumnas/ColPersonajes/BotonITA,
		
		"Desierto": $PanelInfo/ContenedorColumnas/ColLugares/BotonDesierto,
		"Bosque": $PanelInfo/ContenedorColumnas/ColLugares/BotonBosque,
		"Nevado": $PanelInfo/ContenedorColumnas/ColLugares/BotonNieve,
		"Pantano": $PanelInfo/ContenedorColumnas/ColLugares/BotonPantano,
		"Ciudad": $PanelInfo/ContenedorColumnas/ColLugares/BotonCiudad,
		
		"Bomba": $PanelInfo/ContenedorColumnas/ColArmas/BotonBomba,
		"Mina": $PanelInfo/ContenedorColumnas/ColArmas/BotonMina,
		"Cazatanques": $PanelInfo/ContenedorColumnas/ColArmas/BotonCazatanques,
		"Misil": $PanelInfo/ContenedorColumnas/ColArmas/BotonMisil,
		"Granada": $PanelInfo/ContenedorColumnas/ColArmas/BotonGranada
	}
	
	for key in btn_paths:
		var btn = btn_paths[key]
		btn.pressed.connect(func(): _mostrar_info_detalle(key))

func _mostrar_info_detalle(clave: String):
	if info_personajes.has(clave): txt_detalle_info.text = info_personajes[clave]
	elif info_lugares.has(clave): txt_detalle_info.text = info_lugares[clave]
	elif info_armas.has(clave): txt_detalle_info.text = info_armas[clave]

func conectar_botones_acusacion():
	var btn_paths = {
		"personaje": {
			"USA": $PanelAcusacion/ContenedorOpciones/GrupoPersonajes/BotonUSA,
			"Alemania": $PanelAcusacion/ContenedorOpciones/GrupoPersonajes/BotonALE,
			"Francia": $PanelAcusacion/ContenedorOpciones/GrupoPersonajes/BotonFRA,
			"Reino Unido": $PanelAcusacion/ContenedorOpciones/GrupoPersonajes/BotonUK,
			"Italia": $PanelAcusacion/ContenedorOpciones/GrupoPersonajes/BotonITA
		},
		"lugar": {
			"Desierto": $PanelAcusacion/ContenedorOpciones/GrupoLugares/BotonDesierto,
			"Bosque": $PanelAcusacion/ContenedorOpciones/GrupoLugares/BotonBosque,
			"Nevado": $PanelAcusacion/ContenedorOpciones/GrupoLugares/BotonNieve,
			"Pantano": $PanelAcusacion/ContenedorOpciones/GrupoLugares/BotonPantano,
			"Ciudad": $PanelAcusacion/ContenedorOpciones/GrupoLugares/BotonCiudad
		},
		"arma": {
			"Bomba": $PanelAcusacion/ContenedorOpciones/GrupoArmas/BotonBomba,
			"Mina": $PanelAcusacion/ContenedorOpciones/GrupoArmas/BotonMina,
			"Cazatanques": $PanelAcusacion/ContenedorOpciones/GrupoArmas/BotonCazatanques,
			"Misil": $PanelAcusacion/ContenedorOpciones/GrupoArmas/BotonMisil,
			"Granada": $PanelAcusacion/ContenedorOpciones/GrupoArmas/BotonGranada
		}
	}
	
	for categoria in btn_paths:
		for clave in btn_paths[categoria]:
			var btn = btn_paths[categoria][clave]
			btn.pressed.connect(func(): _actualizar_seleccion(categoria, clave))

func _actualizar_seleccion(categoria: String, valor: String):
	seleccion_jugador[categoria] = valor
	txt_resumen_acusacion.text = "Ha seleccionado: " + seleccion_jugador["personaje"] + " | " + seleccion_jugador["lugar"] + " | " + seleccion_jugador["arma"]
