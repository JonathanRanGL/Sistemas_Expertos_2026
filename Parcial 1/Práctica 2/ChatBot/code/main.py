from database import inicializar_db, buscar_respuesta, guardar_nuevo_conocimiento

def ejecutar_bot():
    # 1. Preparamos la base de datos
    inicializar_db()
    print("--- Chatbot Mint-Condition® Activado ---")
    print("(Escribe 'END' para terminar)\n")

    while True:
        entrada = input("Tú: ").strip().lower()

        if entrada == "END":
            print("Bot: ¡Hasta luego! ")
            break

        # 2. Intentamos buscar la respuesta
        respuesta = buscar_respuesta(entrada)

        if respuesta:
            print(f"Bot: {respuesta}")
        else:
            # 3. MODO APRENDIZAJE
            print("Bot: No tengo una respuesta para eso.")
            nueva_respuesta = input(f"¿Qué debería responder cuando alguien diga '{entrada}'?: ")
            
            if nueva_respuesta.strip():
                guardar_nuevo_conocimiento(entrada, nueva_respuesta)
                print("Bot: ¡Entendido! Base de conocimientos actualizada.")
            else:
                print("Bot: Muy bien, lo dejamos para otro día.")

if __name__ == "__main__":
    ejecutar_bot()