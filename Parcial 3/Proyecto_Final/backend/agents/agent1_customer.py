"""
Agente 1 — Atención al Cliente
Responde preguntas, sugiere productos y detecta intención básica.
"""
from typing import Any, Dict, List, Optional

from backend.db.database import query


class CustomerAgent:
    def __init__(self) -> None:
        self.greeting_keywords = ["hola", "buenos", "buenas", "saludos"]
        self.buy_keywords = ["comprar", "pedido", "orden", "adquirir", "cotiza", "cotización"]
        self.compatibility_keywords = ["compatible", "compatibilidad", "socket", "ram", "plca madre", "motherboard"]

    def detect_intent(self, mensaje: str) -> str:
        text = mensaje.lower()
        if any(word in text for word in self.greeting_keywords):
            return "saludo"
        if any(word in text for word in self.buy_keywords):
            return "compra"
        if any(word in text for word in self.compatibility_keywords):
            return "compatibilidad"
        return "consulta"

    def search_products(self, mensaje: str) -> List[Dict[str, Any]]:
        term = f"%{mensaje.strip().lower()}%"
        return query(
            "SELECT id, nombre, categoria, marca, precio FROM productos WHERE activo = 1 AND (LOWER(nombre) LIKE ? OR LOWER(categoria) LIKE ? OR LOWER(marca) LIKE ?) LIMIT 5",
            (term, term, term),
        )

    def generate_response(self, mensaje: str, cliente_id: Optional[int] = None) -> Dict[str, Any]:
        intent = self.detect_intent(mensaje)
        productos = self.search_products(mensaje)
        respuesta = ""

        if intent == "saludo":
            respuesta = (
                "¡Hola! Soy tu asistente de Tienda Inteligente. "
                "Puedo recomendarte componentes, responder dudas de compatibilidad o ayudarte a crear un pedido."
            )
        elif intent == "compra":
            respuesta = (
                "Veo que quieres comprar. "
                "Dime qué componentes necesitas o usa el carrito para generar tu pedido. "
                "Puedo ayudarte a validar stock y compatibilidad."
            )
        elif intent == "compatibilidad":
            if productos:
                respuesta = (
                    "Para comprobar compatibilidad, selecciona los productos que quieres combinar. "
                    "He encontrado algunos componentes relacionados: "
                    + "; ".join([f"{p['nombre']} ({p['categoria']})" for p in productos])
                    + "."
                )
            else:
                respuesta = (
                    "Cuéntame qué CPU, motherboard o memoria estás evaluando, "
                    "y te ayudo a ver si son compatibles."
                )
        else:
            if productos:
                respuesta = (
                    "He encontrado estos productos que pueden ayudarte: "
                    + "; ".join([f"{p['nombre']} - ${p['precio']}" for p in productos])
                    + ". "
                    + "Si quieres, puedo generar un pedido con cualquiera de ellos."
                )
            else:
                respuesta = (
                    "Lo siento, no encontré productos exactos con esa descripción. "
                    "Puedes preguntar por GPU, CPU, RAM, SSD, motherboard, fuente o gabinete."
                )

        metadata = {
            "intent": intent,
            "cliente_id": cliente_id,
            "productos_sugeridos": [p["id"] for p in productos],
        }
        return {"respuesta": respuesta, "metadata": metadata}
