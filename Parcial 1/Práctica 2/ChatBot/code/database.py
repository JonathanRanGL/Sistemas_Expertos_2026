import sqlite3

def inicializar_db():
    # Creamos (o abrimos) el archivo de la base de datos
    conexion = sqlite3.connect("memoria_bot.db")
    cursor = conexion.cursor()
    
    # Creamos la tabla
    # Guardamos la pregunta y la respuesta sugerida
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conocimiento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pregunta TEXT UNIQUE,
            respuesta TEXT
        )
    ''')
    
    # Insertamos las 3 líneas base si la tabla está vacía
    respuestas_iniciales = [
        ("hola", "Hola, soy Mint-Condition®, tu asistente en detallado automotriz profesional. ¿Tienes alguna pregunta?"),
        ("que tan importante es lavar mi auto", "es muy importante lavar el auto correctamente porque..."),
        ("que necesito para lavar mi auto", "para empezar, vas a necesitar...")
    ]
    
    try:
        cursor.executemany("INSERT OR IGNORE INTO conocimiento (pregunta, respuesta) VALUES (?, ?)", respuestas_iniciales)
    except sqlite3.Error:
        pass

    conexion.commit()
    conexion.close()

def buscar_respuesta(pregunta_usuario):
    conexion = sqlite3.connect("memoria_bot.db")
    cursor = conexion.cursor()
    
    # Buscamos si existe la pregunta exacta (en minúsculas)
    cursor.execute("SELECT respuesta FROM conocimiento WHERE pregunta = ?", (pregunta_usuario.lower(),))
    resultado = cursor.fetchone()
    
    conexion.close()
    return resultado[0] if resultado else None

def guardar_nuevo_conocimiento(pregunta, respuesta):
    conexion = sqlite3.connect("memoria_bot.db")
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO conocimiento (pregunta, respuesta) VALUES (?, ?)", (pregunta.lower(), respuesta))
    conexion.commit()
    conexion.close()