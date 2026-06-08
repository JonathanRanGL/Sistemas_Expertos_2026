from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from backend.agents.agent1_customer import CustomerAgent

router = APIRouter(tags=["chat"])

class ChatRequest(BaseModel):
    cliente_id: Optional[int] = None
    mensaje: str

class ChatResponse(BaseModel):
    respuesta: str
    origen: str
    metadata: Optional[dict] = None

agent = CustomerAgent()

@router.post("/chat", response_model=ChatResponse)
def chat_message(payload: ChatRequest):
    result = agent.generate_response(payload.mensaje, payload.cliente_id)
    return {
        "respuesta": result["respuesta"],
        "origen": "Agente 1 - Atención al Cliente",
        "metadata": result.get("metadata"),
    }
