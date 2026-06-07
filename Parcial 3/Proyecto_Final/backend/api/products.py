from typing import Optional
from fastapi import APIRouter, Query
from backend.db.database import query

router = APIRouter(tags=["productos"])

@router.get("/products")
def list_products(
    q: Optional[str] = Query(None, description="Término de búsqueda para nombre, marca o categoría"),
    category: Optional[str] = Query(None, description="Filtrar por categoría"),
    brand: Optional[str] = Query(None, description="Filtrar por marca"),
    max_price: Optional[float] = Query(None, description="Precio máximo"),
):
    sql = "SELECT * FROM productos WHERE activo = 1"
    params = []

    if q:
        sql += " AND (nombre LIKE ? OR descripcion LIKE ? OR marca LIKE ? OR categoria LIKE ? )"
        term = f"%{q}%"
        params.extend([term, term, term, term])

    if category:
        sql += " AND categoria = ?"
        params.append(category)

    if brand:
        sql += " AND marca = ?"
        params.append(brand)

    if max_price is not None:
        sql += " AND precio <= ?"
        params.append(max_price)

    products = query(sql, tuple(params))
    return products
