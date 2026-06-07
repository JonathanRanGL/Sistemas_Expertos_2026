"""
backend/main.py
Punto de entrada de la API FastAPI — Tienda Inteligente
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Tienda Inteligente API",
    description="Sistema experto de venta de componentes PC con agentes inteligentes",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

from backend.api.products import router as products_router
from backend.api.clients import router as clients_router
from backend.api.orders import router as orders_router
from backend.api.chat import router as chat_router

app.include_router(products_router, prefix="/api")
app.include_router(clients_router, prefix="/api")
app.include_router(orders_router, prefix="/api")
app.include_router(chat_router, prefix="/api")


@app.get("/")
def root():
    return {
        "sistema": "Tienda Inteligente",
        "version": "1.0.0",
        "agentes": ["Agente1-AtencionCliente", "Agente2-GeneradorPedido", "Agente3-Supervisor"],
        "status": "online",
    }


@app.get("/health")
def health():
    return {"status": "ok"}
