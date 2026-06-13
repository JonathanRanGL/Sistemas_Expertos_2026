from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sqlite3
import os

router = APIRouter()

class Order(BaseModel):
    componente_id: int
    cantidad: int

@router.post("/orders/checkout")
async def checkout(order: Order):
    try:
        db_path = os.path.join(os.path.dirname(__file__), '../tienda.db')
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("INSERT INTO pedidos (componente_id, cantidad, status) VALUES (?, ?, ?)", 
                  (order.componente_id, order.cantidad, "Aprobado"))
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Pedido procesado por el Agente Supervisor"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))