"""
backend/api/products.py
Endpoints del catálogo de productos.
Usa la base de datos unificada (backend/db/database.py + models.py).
"""
from typing import Optional
from fastapi import APIRouter, HTTPException

from backend.db.database import query

router = APIRouter()


@router.get("/products")
def get_products(
    q: Optional[str] = None,
    category: Optional[str] = None,
    brand: Optional[str] = None,
    max_price: Optional[float] = None,
):
    """Lista productos del catálogo con filtros opcionales."""
    try:
        sql = "SELECT * FROM productos WHERE activo = 1"
        params: list = []

        if q:
            sql += " AND nombre LIKE ?"
            params.append(f"%{q}%")
        if category:
            sql += " AND categoria = ?"
            params.append(category)
        if brand:
            sql += " AND marca = ?"
            params.append(brand)
        if max_price is not None:
            sql += " AND precio <= ?"
            params.append(max_price)

        sql += " ORDER BY id"
        return query(sql, tuple(params))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {str(e)}")


@router.get("/products/deals")
def get_deals():
    """
    Productos en oferta: aquellos que tienen precio_original
    (es decir, tienen un descuento activo).
    """
    try:
        sql = """
            SELECT *,
                   ROUND((1 - precio * 1.0 / precio_original) * 100) AS porcentaje_descuento
            FROM productos
            WHERE activo = 1
              AND precio_original IS NOT NULL
              AND precio_original > precio
            ORDER BY porcentaje_descuento DESC
        """
        return query(sql)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {str(e)}")


@router.get("/products/{product_id}")
def get_product(product_id: int):
    """Detalle de un producto específico."""
    rows = query("SELECT * FROM productos WHERE id = ? AND activo = 1", (product_id,))
    if not rows:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")
    return rows[0]
