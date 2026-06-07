import json
from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.core.inference_engine import InferenceEngine
from backend.db.database import query, execute, execute_many

router = APIRouter(tags=["pedidos"])

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
    estado: str

@router.post("/orders", response_model=OrderResponse)
def create_order(payload: OrderRequest):
    if not payload.items:
        raise HTTPException(status_code=400, detail="El pedido debe contener al menos un artículo.")

    unique_ids = []
    for item in payload.items:
        if item.producto_id not in unique_ids:
            unique_ids.append(item.producto_id)
    product_ids = tuple(unique_ids)

    placeholders = ",".join(["?"] * len(product_ids))
    products = query(
        f"SELECT id, nombre, precio, stock, categoria, specs FROM productos WHERE id IN ({placeholders}) AND activo = 1",
        product_ids,
    )

    if len(products) != len(product_ids):
        raise HTTPException(status_code=404, detail="Algunos productos no existen o no están activos.")

    products_by_id = {product["id"]: product for product in products}
    subtotal = 0.0

    for item in payload.items:
        product = products_by_id.get(item.producto_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Producto {item.producto_id} no encontrado.")
        if item.cantidad < 1:
            raise HTTPException(status_code=400, detail="La cantidad debe ser como mínimo 1.")
        if item.cantidad > product["stock"]:
            raise HTTPException(status_code=400, detail=f"Stock insuficiente para el producto {product['nombre']}.")
        subtotal += product["precio"] * item.cantidad

    cliente = query("SELECT * FROM clientes WHERE id = ?", (payload.cliente_id,))
    cliente_data = cliente[0] if cliente else {}

    engine = InferenceEngine()
    inference = engine.evaluate({
        "cliente": cliente_data,
        "items": [item.dict() for item in payload.items],
        "products": products,
        "subtotal": subtotal,
    })

    descuento = inference["discount"]
    envio_gratis = 1 if inference["envio_gratis"] else 0
    total = subtotal - descuento

    inferencias_json = json.dumps(
        {
            "rules_triggered": inference["rules_triggered"],
            "warnings": inference["warnings"],
            "recommendations": inference["recommendations"],
        },
        ensure_ascii=False,
    )

    pedido_id = execute(
        """
        INSERT INTO pedidos (cliente_id, subtotal, descuento, total, envio_gratis, notas_agente, inferencias)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (payload.cliente_id, subtotal, descuento, total, envio_gratis, payload.notas, inferencias_json),
    )

    detalle_params = [
        (
            pedido_id,
            item.producto_id,
            item.cantidad,
            products_by_id[item.producto_id]["precio"],
            products_by_id[item.producto_id]["precio"] * item.cantidad,
        )
        for item in payload.items
    ]

    execute_many(
        """
        INSERT INTO detalle_pedido (pedido_id, producto_id, cantidad, precio_unit, subtotal)
        VALUES (?, ?, ?, ?, ?)
        """,
        detalle_params,
    )

    return {
        "pedido_id": pedido_id,
        "subtotal": subtotal,
        "descuento": descuento,
        "total": total,
        "envio_gratis": bool(envio_gratis),
        "estado": "pendiente",
    }
