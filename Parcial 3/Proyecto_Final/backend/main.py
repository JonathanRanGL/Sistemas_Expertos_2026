"""
backend/main.py
Punto de entrada de la API FastAPI — Tienda Inteligente

Se ejecuta desde la raíz del proyecto (Proyecto_Final/) con:
    python -m uvicorn backend.main:app --reload

La base de datos (backend/tienda.db) se crea y se llena por separado con:
    python scripts/init_db.py
    python scripts/seed_db.py

Este archivo NO crea ni modifica el esquema de la base de datos;
solo registra los routers y arranca el servidor.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.products import router as products_router
from backend.api.orders import router as orders_router
from backend.api.chat import router as chat_router
from backend.api.pc_expert import router as pc_expert_router
from backend.api.clients import router as clients_router
from backend.api.admin import router as admin_router

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

# ─────────────────────────────────────────
# Registrar Routers
# ─────────────────────────────────────────
app.include_router(products_router, prefix="/api", tags=["Catálogo"])
app.include_router(orders_router, prefix="/api", tags=["Pedidos"])
app.include_router(chat_router, prefix="/api", tags=["Chat - Agente 1"])
app.include_router(pc_expert_router, prefix="/api", tags=["Arma tu PC - Agente 2"])
app.include_router(clients_router, prefix="/api", tags=["Clientes"])
app.include_router(admin_router, prefix="/api", tags=["Admin"])


@app.get("/")
def read_root():
    return {
        "sistema": "Tienda Inteligente",
        "version": "1.0.0",
        "agentes": ["Agente1-AtencionCliente", "Agente2-GeneradorPedido", "Agente3-Supervisor"],
        "status": "online",
    }


@app.get("/health")
def health():
    return {"status": "ok"}
