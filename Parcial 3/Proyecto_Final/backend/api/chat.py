"""
backend/api/chat.py
Endpoint del Agente 1 (Atención al Cliente).

Usa Gemini API si hay una GEMINI_API_KEY configurada en el archivo .env.
Si no hay key, o si la llamada a Gemini falla, responde usando el
agente basado en reglas (CustomerAgent) como respaldo, para que el
chat NUNCA se quede sin respuesta.
"""
import os

from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv

from backend.agents.agent1_customer import CustomerAgent

load_dotenv()

router = APIRouter()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = "gemini-1.5-flash"

_customer_agent = CustomerAgent()

_PROMPT_CONTEXTO = (
    "Eres el Agente 1 de 'Tienda Inteligente', un sistema experto de venta de "
    "componentes de PC (GPU, CPU, RAM, SSD, motherboards, fuentes, gabinetes y coolers). "
    "Eres amable, técnico y conciso (máximo 4-5 líneas). Ayudas a los usuarios a elegir "
    "componentes, explicas compatibilidad básica (sockets, cuellos de botella) y "
    "recomiendas usar la herramienta 'Arma tu PC' para configuraciones completas. "
    "No inventes precios ni stock exactos; si te preguntan por disponibilidad, sugiere "
    "revisar el catálogo. Responde siempre en español. "
    "Mensaje del cliente: "
)


class ChatMessage(BaseModel):
    message: str


def _try_gemini(message: str) -> str | None:
    """Intenta responder con Gemini. Devuelve None si no está disponible o falla."""
    if not GEMINI_API_KEY:
        return None
    try:
        import google.generativeai as genai

        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(_PROMPT_CONTEXTO + message)
        return response.text
    except Exception:
        # Cualquier error de Gemini (key inválida, cuota, modelo, red, etc.)
        # cae al agente basado en reglas, sin romper el chat.
        return None


@router.post("/chat")
def chat_with_agent(chat: ChatMessage):
    reply = _try_gemini(chat.message)

    if reply is None:
        # Respaldo: Agente 1 basado en reglas (sin IA generativa)
        fallback = _customer_agent.generate_response(chat.message)
        reply = fallback["respuesta"]

    return {"reply": reply}
