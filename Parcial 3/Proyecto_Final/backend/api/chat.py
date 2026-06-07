from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter(tags=["chat"])

class ChatRequest(BaseModel):
    cliente_id: Optional[int] = None
    mensaje: str

class ChatResponse(BaseModel):
    respuesta: str
    origen: str

@router.post("/chat", response_model=ChatResponse)
def chat_message(payload: ChatRequest):
    respuesta = (
        f"¡Hola! He recibido tu mensaje: '{payload.mensaje}'. "
        "En esta etapa, la respuesta se simula localmente para validar la conexión entre frontend y backend."
    )
    return {
        "respuesta": respuesta,
        "origen": "Agente 1 (simulado)"
    }
