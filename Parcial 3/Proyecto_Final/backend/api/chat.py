import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

router = APIRouter()

class ChatMessage(BaseModel):
    message: str

# Llave directa sin validaciones confusas
GEMINI_API_KEY = "TU_LLAVE_DE_API_AQUI"
genai.configure(api_key=GEMINI_API_KEY)

@router.post("/chat")
async def chat_with_agent(chat: ChatMessage):
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        prompt_contexto = (
            "Eres el Agente 1 de 'Tienda Inteligente', un sistema experto de venta de componentes de PC. "
            "Eres amable, técnico y conciso. Ayudas a los usuarios a saber qué comprar, explicas cuellos de botella "
            "y recomiendas usar la herramienta 'Arma tu PC'. Responde a este mensaje del cliente: "
        )
        
        response = model.generate_content(prompt_contexto + chat.message)
        return {"reply": response.text}
        
    except Exception as e:
        # Si la API falla, te mandamos el error real a la pantalla para saber qué pasa
        return {"reply": f"Error interno del Agente: {str(e)}"}