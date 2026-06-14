"""
backend/api/chat.py
Endpoint del Agente 1 (Atención al Cliente).

Usa Gemini 2.5 Flash Lite (SDK google-genai) si hay GEMINI_API_KEY en .env.
Si no hay key o la llamada falla, responde con el CustomerAgent basado en
reglas, para que el chat nunca se quede sin respuesta.
"""
import os
import logging
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv

from backend.agents.agent1_customer import CustomerAgent
from backend.db.database import query

load_dotenv()

router = APIRouter()
log = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = "gemini-2.5-flash-lite"

_customer_agent = CustomerAgent()

_SYSTEM_INSTRUCTION = (
    "Eres el Agente 1 de 'Tienda Inteligente', un sistema experto especializado "
    "en componentes de PC (GPU, CPU, RAM, SSD, Motherboard, Fuente de Poder, Cooler, Gabinete). "
    "Ayudas a los clientes a elegir componentes según su presupuesto y necesidades, "
    "explicas compatibilidad de hardware (sockets AM5/LGA1700, TDP vs. vatios de fuente), "
    "recomiendas configuraciones completas y diriges a la sección 'Arma tu PC' del sitio "
    "para ensamblar una build con validación automática de compatibilidad. "
    "Eres amable, técnico y conciso (máximo 4-5 líneas de respuesta). "
    "Cuando el contexto incluya una lista de 'Productos relevantes disponibles', MENCIONA "
    "productos ESPECÍFICOS por nombre y precio (ej: 'la AMD Radeon RX 7600 en $3,499') "
    "en lugar de descripciones genéricas ('una GPU de gama media'). "
    "No inventes productos ni precios que no estén en el catálogo provisto. "
    "Si te preguntan por stock exacto, sugiere revisar el catálogo en línea. "
    "Responde siempre en español. "
    "Al final de CADA respuesta agrega exactamente una línea con el siguiente formato: "
    "'SUGERENCIAS: pregunta 1 | pregunta 2 | pregunta 3' "
    "Las sugerencias deben estar redactadas en PRIMERA PERSONA desde la perspectiva del "
    "CLIENTE/USUARIO que le habla al asistente, como si fueran las próximas preguntas que "
    "el usuario querría hacer (ej: '¿Cuál me conviene más para gaming?' | "
    "'¿Hay algo más económico con specs similares?' | '¿Es compatible con mi placa madre?'). "
    "NO las redactes como instrucciones del asistente al usuario. "
    "Cada sugerencia debe ser máximo 8-10 palabras."
)

# Sinónimos de categorías y marcas para detectar términos en el mensaje del usuario
_CATEGORIA_SINONIMOS = {
    "gpu": "GPU", "grafica": "GPU", "gráfica": "GPU", "tarjeta grafica": "GPU",
    "tarjeta gráfica": "GPU", "video": "GPU", "rtx": "GPU", "rx": "GPU",
    "cpu": "CPU", "procesador": "CPU", "micro": "CPU", "ryzen": "CPU", "core i": "CPU",
    "ram": "RAM", "memoria": "RAM", "ddr": "RAM",
    "ssd": "SSD", "disco": "SSD", "almacenamiento": "SSD", "nvme": "SSD", "sata": "SSD",
    "motherboard": "Motherboard", "placa madre": "Motherboard", "mother": "Motherboard",
    "tarjeta madre": "Motherboard", "mobo": "Motherboard",
    "fuente": "Fuente", "psu": "Fuente", "power supply": "Fuente", "watts": "Fuente",
    "watt": "Fuente",
    "cooler": "Cooler", "ventilador": "Cooler", "refrigeracion": "Cooler",
    "refrigeración": "Cooler", "disipador": "Cooler", "aio": "Cooler",
    "gabinete": "Gabinete", "case": "Gabinete", "chasis": "Gabinete", "torre": "Gabinete",
}
_MARCAS = [
    "nvidia", "amd", "intel", "corsair", "samsung", "asus", "msi", "gigabyte",
    "western digital", "wd", "evga", "noctua", "nzxt", "lian li", "g.skill", "gskill",
    "kingston", "crucial", "seasonic", "arctic", "cooler master", "fractal",
    "be quiet", "bequiet",
]


def _get_catalog_summary() -> str:
    """Resumen breve del catálogo (categoría, rango de precio, cantidad en stock)."""
    rows = query(
        "SELECT categoria, MIN(precio) as min_p, MAX(precio) as max_p, COUNT(*) as total "
        "FROM productos WHERE activo=1 AND stock>0 GROUP BY categoria ORDER BY categoria"
    )
    if not rows:
        return "Catálogo: sin productos disponibles actualmente."
    lines = ["Catálogo disponible (productos en stock):"]
    for row in rows:
        lines.append(
            f"- {row['categoria']}: {row['total']} productos, "
            f"desde ${row['min_p']:,.0f} hasta ${row['max_p']:,.0f} MXN"
        )
    return "\n".join(lines)


def _get_relevant_products(message: str) -> str:
    """
    Busca hasta 8 productos relevantes según las palabras clave del mensaje.
    Devuelve cadena vacía si no hay coincidencias claras.
    """
    text = message.lower()
    categorias: set[str] = set()
    marcas: set[str] = set()

    for sinonimo, cat in _CATEGORIA_SINONIMOS.items():
        if sinonimo in text:
            categorias.add(cat)

    for marca in _MARCAS:
        if marca in text:
            marcas.add(marca)

    if not categorias and not marcas:
        return ""

    conditions = []
    params: list = []

    for cat in categorias:
        conditions.append("LOWER(categoria) = LOWER(?)")
        params.append(cat)

    for marca in marcas:
        conditions.append("LOWER(marca) LIKE LOWER(?)")
        params.append(f"%{marca}%")

    sql = (
        "SELECT nombre, marca, categoria, precio, stock "
        "FROM productos "
        "WHERE activo=1 AND stock>0 AND (" + " OR ".join(conditions) + ") "
        "ORDER BY rating DESC LIMIT 8"
    )
    rows = query(sql, tuple(params))

    if not rows:
        return ""

    lines = ["Productos relevantes disponibles para esta consulta:"]
    for row in rows:
        lines.append(
            f"- {row['nombre']} ({row['categoria']}) — "
            f"${row['precio']:,.0f} MXN — {row['stock']} en stock"
        )
    return "\n".join(lines)


class HistoryItem(BaseModel):
    role: str   # "user" | "model"
    text: str


class ChatMessage(BaseModel):
    message: str
    history: list[HistoryItem] = []


def _try_gemini(message: str, history: list[HistoryItem]) -> Optional[str]:
    """Intenta responder con Gemini 2.5 Flash Lite. Devuelve None si no está configurado o falla."""
    if not GEMINI_API_KEY:
        return None
    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=GEMINI_API_KEY)

        # Construir contexto: resumen del catálogo + productos relevantes al mensaje
        catalog_ctx = _get_catalog_summary()
        relevant_products = _get_relevant_products(message)

        context_parts = [_SYSTEM_INSTRUCTION, "", catalog_ctx]
        if relevant_products:
            context_parts += ["", relevant_products]
        system_with_context = "\n".join(context_parts)

        # Construir el array de Contents: historial previo + mensaje actual
        contents: list[types.Content] = []
        for turn in history:
            contents.append(
                types.Content(
                    role=turn.role,
                    parts=[types.Part(text=turn.text)]
                )
            )
        contents.append(
            types.Content(
                role="user",
                parts=[types.Part(text=message)]
            )
        )

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_with_context
            )
        )
        return response.text

    except Exception as exc:
        log.warning("Gemini error (%s): %s", type(exc).__name__, exc)
        return None


@router.post("/chat")
def chat_with_agent(chat: ChatMessage):
    reply = _try_gemini(chat.message, chat.history)

    if reply is None:
        fallback = _customer_agent.generate_response(chat.message)
        reply = fallback["respuesta"]

    return {"reply": reply}
