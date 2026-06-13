from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import sqlite3
import os

router = APIRouter()
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tienda.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Permite acceder a las columnas por nombre
    return conn

@router.get("/products")
def get_products(
    q: Optional[str] = None,
    category: Optional[str] = None,
    brand: Optional[str] = None,
    max_price: Optional[float] = None
):
    conn = get_db_connection()
    try:
        query = "SELECT * FROM productos WHERE activo = 1"
        params = []
        
        if q:
            query += " AND nombre LIKE ?"
            params.append(f"%{q}%")
        if category:
            query += " AND categoria = ?"
            params.append(category)
        if brand:
            query += " AND marca = ?"
            params.append(brand)
        if max_price is not None:
            query += " AND precio <= ?"
            params.append(max_price)
            
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # Convertimos sqlite3.Row a diccionarios
        return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {str(e)}")
    finally:
        conn.close()