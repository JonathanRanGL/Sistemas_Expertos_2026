"""
backend/api/orders.py
Endpoint de checkout — conecta el carrito del frontend con el
Agente 2 (Generador de Pedido) y el Agente 3 (Supervisor/Explicador).
"""
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.agents.agent2_order import OrderAgent

router = APIRouter()


class CartItem(BaseModel):
    producto_id: int
    cantidad: int


class CheckoutRequest(BaseModel):
    cliente_id: Optional[int] = None
    items: List[CartItem]
    notas: str = ""


@router.post("/orders/checkout")
def checkout(payload: CheckoutRequest):
    """
    Recibe el carrito completo del frontend ({cliente_id, items}),
    lo procesa con el Agente 2 (valida stock, aplica reglas de inferencia,
    guarda el pedido) y devuelve el resumen + explicación del Agente 3.
    """
    if not payload.items:
        raise HTTPException(status_code=400, detail="El carrito está vacío.")

    agent = OrderAgent()
    try:
        items = [item.model_dump() for item in payload.items]
        result = agent.create_order(payload.cliente_id, items, notas=payload.notas)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el pedido: {str(e)}")

    return {
        "status": "success",
        "pedido_id": result["pedido_id"],
        "subtotal": result["subtotal"],
        "descuento": result["descuento"],
        "total": result["total"],
        "envio_gratis": result["envio_gratis"],
        "inferencias": result["inferencias"],
        "explicacion_agente3": result["notas_agente"],
    }


@router.get("/orders/{pedido_id}")
def get_order(pedido_id: int):
    """Consulta un pedido por ID, incluyendo su explicación del Agente 3."""
    from backend.db.database import query

    pedidos = query("SELECT * FROM pedidos WHERE id = ?", (pedido_id,))
    if not pedidos:
        raise HTTPException(status_code=404, detail="Pedido no encontrado.")

    detalle = query(
        """
        SELECT d.*, p.nombre AS producto_nombre
        FROM detalle_pedido d
        JOIN productos p ON p.id = d.producto_id
        WHERE d.pedido_id = ?
        """,
        (pedido_id,),
    )

    pedido = pedidos[0]
    pedido["items"] = detalle
    return pedido
