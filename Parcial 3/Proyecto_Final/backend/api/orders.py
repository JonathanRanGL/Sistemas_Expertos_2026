import json
from typing import List, Optional
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
    cliente_id: Optional[int] = None
    items: List[OrderItem]
    notas: str = ""

class OrderResponse(BaseModel):
    pedido_id: int
    subtotal: float
    descuento: float
    total: float
    envio_gratis: bool
    notas_agente: str
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
        "notas_agente": result["notas_agente"],
        "inferencias": result["inferencias"],
        "resumen": summary,
        "estado": "pendiente",
    }

@router.get("/orders/{pedido_id}", response_model=OrderResponse)
def get_order(pedido_id: int):
    order_result = query("SELECT * FROM pedidos WHERE id = ?", (pedido_id,))
    if not order_result:
        raise HTTPException(status_code=404, detail="Pedido no encontrado.")

    order_data = order_result[0]
    details = query(
        "SELECT producto_id, cantidad, precio_unit, subtotal FROM detalle_pedido WHERE pedido_id = ?",
        (pedido_id,),
    )

    inferencias = supervisor.parse_inferencias(order_data.get("inferencias"))
    summary = supervisor.summarize(order_data, details, inferencias)

    return {
        "pedido_id": order_data["id"],
        "subtotal": order_data["subtotal"],
        "descuento": order_data["descuento"],
        "total": order_data["total"],
        "envio_gratis": bool(order_data["envio_gratis"]),
        "notas_agente": order_data.get("notas_agente", ""),
        "inferencias": inferencias,
        "resumen": summary,
        "estado": order_data.get("estado", "pendiente"),
    }
