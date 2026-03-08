import sqlite3

def inicializar_db():
    # Conexión a la DB local. Si el archivo no existe, SQLite lo crea de jalón.
    conexion = sqlite3.connect("memoria_bot.db")
    cursor = conexion.cursor()
    
    # Armamos la tabla principal para guardar el conocimiento
    # El ID es autoincrementable para no pelearnos con los índices manuales
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conocimiento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pregunta TEXT UNIQUE, -- UNIQUE para que no haya preguntas duplicadas rompiendo el script
            respuesta TEXT
        )
    ''')
    
    # Las 3 frases base que pide la rúbrica de la práctica
    respuestas_iniciales = [
        ("hola", "Hola, soy Mint-Condition®, tu asistente en detallado automotriz profesional. ¿Tienes alguna pregunta?"),
        ("¿lavar mi auto es importante?", "Lavar regularmente un auto es una tarea sumamente importante por que de esta manera remueves todo tipo de contaminante incrustado en la pintura, que con el tiempo puede dañar de manera permanente la capa de transparente (clearcoat) de la pintura de tu auto. Además el estado de la pintura es uno de los primeros factores que un comprador potencial o una agencia evalúan. Un auto con una pintura bien cuidada, brillante y sin manchas de oxidación mantiene un valor de mercado significativamente más alto que uno descuidado."),
        ("¿qué necesito para lavar mi auto?", "Para empezar a lavar tu auto de la manera correcta y minimizar el riesgo de arañar la pintura, es recomendable emplear el método del las dos cubetas, para este necesitaras un guante de microfibra, un jabón para auto de pH neutro, un cepillo de cerda suave para los rines, dos cubetas, un paño de secado de microfibra y de preferencia una manguera para enjuagar el auto. Con esto deberías tener suficiente para lavarlo de forma segura, aunque es recomendable adquirir más herramientas y productos limpieza si quieres llevar tu lavado al siguiente nivel.")
    ]
    
    try:
        # INSERT OR IGNORE nos salva la vida si corremos el script varias veces,
        # así no intenta duplicar estas frases iniciales y no crashea.
        cursor.executemany("INSERT OR IGNORE INTO conocimiento (pregunta, respuesta) VALUES (?, ?)", respuestas_iniciales)
    except sqlite3.Error:
        pass # Si falla por algo interno de la BD, lo ignoramos de momento

    conexion.commit() # Guardar cambios (fundamental, si no, se pierde al cerrar la app)
    conexion.close()

def buscar_respuesta(pregunta_usuario):
    conexion = sqlite3.connect("memoria_bot.db")
    cursor = conexion.cursor()
    
    # Hacemos el query forzando la pregunta a minúsculas para que el match sea exacto
    cursor.execute("SELECT respuesta FROM conocimiento WHERE pregunta = ?", (pregunta_usuario.lower(),))
    resultado = cursor.fetchone()
    
    conexion.close()
    
    # Si encontró algo, devolvemos el string (índice 0 de la tupla), si no, soltamos un None
    return resultado[0] if resultado else None

def guardar_nuevo_conocimiento(pregunta, respuesta):
    conexion = sqlite3.connect("memoria_bot.db")
    cursor = conexion.cursor()
    
    # Inyectamos la nueva data a la BD (El modo aprendizaje)
    # Ojo: Siempre pasar la pregunta a .lower() para estandarizar la memoria
    cursor.execute("INSERT INTO conocimiento (pregunta, respuesta) VALUES (?, ?)", (pregunta.lower(), respuesta))
    
    conexion.commit()
    conexion.close()

def borrar_memoria():
    conexion = sqlite3.connect("memoria_bot.db")
    cursor = conexion.cursor()
    
    # Comando maestro para resetear la memoria completa (formateo de emergencia)
    cursor.execute("DELETE FROM conocimiento") 
    conexion.commit()
    conexion.close()
    
    # Volvemos a cargar las 3 frases base para no dejar al bot totalmente en blanco
    inicializar_db()