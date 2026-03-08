import customtkinter as ctk
import ctypes  
import math 
import pywinstyles 
from database import buscar_respuesta, guardar_nuevo_conocimiento, inicializar_db

# Parche para que Windows muestre nuestro logo en la barra de tareas en lugar del logo de Python
try:
    mi_app_id = 'mintcondition.chatbot.detailing.1.0'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(mi_app_id)
except Exception:
    pass

# Setup general de la UI
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# --- Clase para la animación de "escribiendo..." (los 3 puntitos) ---
class IndicadorEscribiendo(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        # Usamos radio de 8 para evitar el aliasing/escalonado feo en monitores de alta resolución
        super().__init__(master, fg_color="#1e1e1e", corner_radius=8, width=70, height=40, **kwargs)
        self.pack_propagate(False) # Evita que el frame se encoja al tamaño del texto
        
        self.puntos = []
        for i in range(3):
            lbl = ctk.CTkLabel(self, text="•", font=("Arial", 30), text_color="#555555")
            lbl.place(x=12 + i*15, y=5) 
            self.puntos.append(lbl)
            
        self.animando = True
        self.tiempo = 0
        self.animar() 

    def animar(self):
        if not self.animando:
            return
        
        self.tiempo += 0.3 
        for i, punto in enumerate(self.puntos):
            # Usamos seno para crear un desfase y dar el efecto de ola en cascada
            desfase = math.sin(self.tiempo - i * 1.0) * 5 
            punto.place(x=12 + i*15, y=3 + desfase) 
            
        self.after(30, self.animar) # Refresco a 30ms para que se vea smooth

    def detener_y_destruir(self):
        # Matamos el loop de la animación antes de borrar el widget para no dejar basura en memoria
        self.animando = False
        self.destroy()
# --------------------------------------------------------------------

class ChatBotGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        inicializar_db() # Carga la BD de SQLite o la crea si no existe
        
        self.title("Mint-Condition® - Auto Detailing Assistant")
        self.geometry("450x600")
        
        # Le damos un delay de 200ms para asegurar que el ícono cargue bien en Tkinter
        self.after(200, lambda: self.iconbitmap(r'D:\CETI\Ingeniería\7. Séptimo\Sistemas Expertos\Repositorio\Sistemas_Expertos_2026\Parcial 1\Práctica 2\ChatBot\assets\logo.ico'))

        # --- EFECTO CRISTAL DE WINDOWS ---
        pywinstyles.apply_style(self, "aero") 
        
        # Hack: Hacemos que el color base de la app sea el transparente de Windows 
        # para que el efecto Aero se pueda ver por debajo sin que los colores internos lo tapen
        color_fondo = self._apply_appearance_mode(self._fg_color)
        self.wm_attributes("-transparentcolor", color_fondo)
        # ---------------------------------

        # Frame con scroll para los mensajes
        self.chat_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.chat_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.burbujas = []
        self.ancho_anterior = 0  
        self.chat_frame.bind("<Configure>", self.recalcular_ancho) # Escucha si el usuario cambia el tamaño de la ventana

        # Input de texto
        self.entrada = ctk.CTkEntry(self, placeholder_text="Escribe aquí...", height=40, corner_radius=8)
        self.entrada.pack(fill="x", padx=10, pady=(0, 10))
        self.entrada.bind("<Return>", self.procesar_mensaje)

        # Variables para controlar si el bot está esperando a que le enseñemos algo
        self.esperando_respuesta = False
        self.pregunta_pendiente = ""

        # Mensaje de arranque
        self.simular_escritura_bot("¡Hola! Soy Mint-Condition®.  ¿En qué te puedo ayudar?")

    def recalcular_ancho(self, event):
        # Solo recalcula si cambió el ancho (ignora los cambios de altura para evitar lag)
        if event.width != self.ancho_anterior:
            self.ancho_anterior = event.width
            ancho_disponible = event.width - 50
            if ancho_disponible > 10:
                for burbuja in self.burbujas:
                    if isinstance(burbuja, ctk.CTkLabel):
                        burbuja.configure(wraplength=ancho_disponible)

    def agregar_burbuja(self, texto, color, alineacion):
        burbuja = ctk.CTkLabel(
            self.chat_frame, 
            text=texto, 
            fg_color=color, 
            text_color="white",
            corner_radius=8,
            padx=10, pady=10,
            justify="left"
        )
        burbuja.pack(padx=10, pady=5, anchor=alineacion)
        
        self.burbujas.append(burbuja)

        # Forzamos a la UI a calcular el espacio real que va a ocupar la burbuja nueva
        self.chat_frame.update_idletasks()
        ancho_actual = self.chat_frame.winfo_width() - 50
        if ancho_actual > 10:
            burbuja.configure(wraplength=ancho_actual)

        # Pequeño retardo para asegurar que el canvas se actualizó antes de bajar el scroll
        self.after(50, self._actualizar_scroll)

    def _actualizar_scroll(self):
        # Mueve la vista al 100% (hasta abajo)
        self.chat_frame._parent_canvas.configure(scrollregion=self.chat_frame._parent_canvas.bbox("all"))
        self.chat_frame._parent_canvas.yview_moveto(1.0)

    def simular_escritura_bot(self, texto_final):
        self.entrada.configure(state="disabled") # Bloqueamos el input para evitar spam

        burbuja_temp = IndicadorEscribiendo(self.chat_frame)
        burbuja_temp.pack(padx=10, pady=5, anchor="w")
        
        self.burbujas.append(burbuja_temp)
        self.after(50, self._actualizar_scroll)

        # Le damos 1.5 seg de "tiempo de pensar" antes de soltar la respuesta
        self.after(1500, lambda: self.reemplazar_respuesta(burbuja_temp, texto_final))

    def reemplazar_respuesta(self, burbuja_temp, texto_final):
        burbuja_temp.detener_y_destruir()
        if burbuja_temp in self.burbujas:
            self.burbujas.remove(burbuja_temp)

        self.entrada.configure(state="normal")
        self.entrada.focus() # Regresamos el cursor al input

        self.agregar_burbuja(texto_final, "#1e1e1e", "w")

    def procesar_mensaje(self, event):
        msg = self.entrada.get().strip()
        if not msg: return
        
        # Burbuja del usuario
        self.agregar_burbuja(msg, "#153d6b", "e")
        self.entrada.delete(0, "end")

        # Comando maestro oculto para limpiar la BD rápido mientras hago pruebas
        if msg.lower() == "/borrar":
            try:
                from database import borrar_memoria
                borrar_memoria()
                self.simular_escritura_bot("Memoria formateada. He vuelto a mi estado de fábrica.")
            except ImportError:
                self.simular_escritura_bot("Error: La función borrar_memoria no existe en database.py")
            return

        # MODO APRENDIZAJE: Si en el turno anterior el bot nos pidió la respuesta
        if self.esperando_respuesta:
            guardar_nuevo_conocimiento(self.pregunta_pendiente, msg)
            self.simular_escritura_bot("¡Anotado! Ya lo guardé en mi base de datos.")
            
            # Reseteamos los estados
            self.esperando_respuesta = False
            self.pregunta_pendiente = ""
            return

        # FLUJO NORMAL: Buscar en la BD
        respuesta = buscar_respuesta(msg.lower())

        if respuesta:
            self.simular_escritura_bot(respuesta)
        else:
            # No sabe la respuesta, pasa al modo aprendizaje
            self.simular_escritura_bot("No sé que responder a eso. ¿Qué debería decir?")
            self.esperando_respuesta = True
            self.pregunta_pendiente = msg.lower()

if __name__ == "__main__":
    app = ChatBotGUI()
    app.mainloop()