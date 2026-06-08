import json
from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.agents.agent2_order import OrderAgent
from backend.agents.agent3_supervisor import SupervisorAgent
from backend.db.database import query

router = APIRouter(tags=["pedidos"])
order_agent = OrderAgent()
supervisor = SupervisorAgent()

class OrderItem(BaseModel):
    producto_id: int
    cantidad: int

class OrderRequest(BaseModel):
    cliente_id: int
    items: List[OrderItem]
    notas: str = ""

class OrderResponse(BaseModel):
    pedido_id: int
    subtotal: float
    descuento: float
    total: float
    envio_gratis: bool
    inferencias: dict
    resumen: dict
    estado: str

@router.post("/orders", response_model=OrderResponse)
def create_order(payload: OrderRequest):
    try:
        result = order_agent.create_order(
            payload.cliente_id,
            [item.dict() for item in payload.items],
            payload.notas,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    details = query(
        "SELECT producto_id, cantidad, precio_unit, subtotal FROM detalle_pedido WHERE pedido_id = ?",
        (result["pedido_id"],),
    )

    summary = supervisor.summarize(result, details, result["inferencias"])

    return {
        "pedido_id": result["pedido_id"],
        "subtotal": result["subtotal"],
        "descuento": result["descuento"],
        "total": result["total"],
        "envio_gratis": result["envio_gratis"],
        "inferencias": result["inferencias"],
        "resumen": summary,
        "estado": "pendiente",
    }
