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

# Los routers de productos, clientes y chat se añaden en commits posteriores
