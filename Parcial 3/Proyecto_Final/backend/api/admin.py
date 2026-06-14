"""
backend/api/admin.py
Endpoints administrativos — solo para uso en desarrollo/demo.
"""
from fastapi import APIRouter
from scripts.reset_db import reset_db

router = APIRouter()


@router.post("/admin/reset")
def reset_store():
    """Reinicia el stock y borra los pedidos de prueba."""
    resultado = reset_db()
    return {
        "ok": True,
        "mensaje": (
            f"Tienda reiniciada: {resultado['productos_restaurados']} productos restaurados, "
            f"{resultado['pedidos_eliminados']} pedidos eliminados."
        ),
        **resultado,
    }
