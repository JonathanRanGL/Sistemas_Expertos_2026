from database import inicializar_db, buscar_respuesta, guardar_nuevo_conocimiento

def ejecutar_bot():
    # 1. Levantamos la base de datos
    # (Si el archivo .db no existe, la función lo crea "on the fly" con las 3 frases de la rúbrica)
    inicializar_db()
    
    print("--- Chatbot Mint-Condition® Activado ---")
    print("(Escribe 'END' para terminar)\n")

    # Loop infinito para mantener la consola escuchando hasta que le mandemos el kill switch
    while True:
        # Atrapamos el input, le quitamos espacios fantasma (strip) 
        # y lo pasamos a minúsculas para no pelear con la case sensitivity en SQLite
        entrada = input("Tú: ").strip().lower()

        # Kill switch para salir del loop de forma limpia y no a la fuerza (Ctrl+C)
        if entrada == "end":
            print("Bot: ¡Hasta luego! ")
            break

        # 2. Mandamos la query a la DB a ver si hace match exacto con algo conocido
        respuesta = buscar_respuesta(entrada)

        if respuesta:
            # Si la DB escupió algo, lo printeamos
            print(f"Bot: {respuesta}")
        else:
            # 3. MODO APRENDIZAJE (Fallback)
            # Aquí es donde ocurre la "adquisición de conocimiento" que pide la práctica
            print("Bot: No tengo una respuesta para eso.")
            
            # Le pedimos al usuario que funcione como maestro/entrenador
            nueva_respuesta = input(f"¿Qué debería responder cuando alguien diga '{entrada}'?: ")
            
            # Validamos que el usuario no nos haya pasado un string vacío (puro enter)
            if nueva_respuesta.strip():
                # Disparamos el guardado a SQLite
                guardar_nuevo_conocimiento(entrada, nueva_respuesta)
                print("Bot: ¡Entendido! Base de conocimientos actualizada.")
            else:
                # Por si el usuario se arrepiente y solo da Enter sin escribir nada
                print("Bot: Muy bien, lo dejamos para otro día.")

# Entry point clásico de Python. 
# Asegura que el bot solo arranque si ejecutamos ESTE script directamente.
if __name__ == "__main__":
    ejecutar_bot()