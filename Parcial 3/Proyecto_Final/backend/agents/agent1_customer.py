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

    # Vocabulario de categorías y marcas conocidas para extraer palabras clave del mensaje
    CATEGORIAS = ["GPU", "CPU", "RAM", "SSD", "Motherboard", "Fuente", "Cooler", "Gabinete"]
    MARCAS = ["NVIDIA", "AMD", "Intel", "Corsair", "Samsung", "ASUS", "MSI", "Gigabyte",
              "Western Digital", "EVGA", "Noctua", "NZXT", "Lian Li", "G.Skill"]

    CATEGORIA_SINONIMOS = {
        "gpu": "GPU", "grafica": "GPU", "gráfica": "GPU", "tarjeta grafica": "GPU", "video": "GPU",
        "cpu": "CPU", "procesador": "CPU", "micro": "CPU",
        "ram": "RAM", "memoria": "RAM",
        "ssd": "SSD", "disco": "SSD", "almacenamiento": "SSD",
        "motherboard": "Motherboard", "placa madre": "Motherboard", "mother": "Motherboard", "tarjeta madre": "Motherboard",
        "fuente": "Fuente", "psu": "Fuente", "power supply": "Fuente",
        "cooler": "Cooler", "ventilador": "Cooler", "refrigeracion": "Cooler", "refrigeración": "Cooler",
        "gabinete": "Gabinete", "case": "Gabinete", "chasis": "Gabinete",
    }

    def _extract_keywords(self, mensaje: str) -> List[str]:
        """Extrae categorías/marcas mencionadas en el mensaje para buscar en el catálogo."""
        text = mensaje.lower()
        encontrados = set()

        for sinonimo, categoria in self.CATEGORIA_SINONIMOS.items():
            if sinonimo in text:
                encontrados.add(categoria)

        for marca in self.MARCAS:
            if marca.lower() in text:
                encontrados.add(marca)

        return list(encontrados)

    def search_products(self, mensaje: str) -> List[Dict[str, Any]]:
        keywords = self._extract_keywords(mensaje)

        if not keywords:
            return []

        conditions = []
        params: List[str] = []
        for kw in keywords:
            conditions.append("LOWER(categoria) = LOWER(?) OR LOWER(marca) = LOWER(?) OR LOWER(nombre) LIKE LOWER(?)")
            params.extend([kw, kw, f"%{kw}%"])

        sql = (
            "SELECT id, nombre, categoria, marca, precio FROM productos "
            "WHERE activo = 1 AND (" + " OR ".join(conditions) + ") "
            "ORDER BY es_tendencia DESC, rating DESC LIMIT 5"
        )
        return query(sql, tuple(params))

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
