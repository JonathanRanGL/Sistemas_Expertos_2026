from fastapi import APIRouter, HTTPException
from backend.db.database import query

router = APIRouter(tags=["clientes"])

@router.get("/clients")
def list_clients():
    return query("SELECT * FROM clientes")

@router.get("/clients/{client_id}")
def get_client(client_id: int):
    result = query("SELECT * FROM clientes WHERE id = ?", (client_id,))
    if not result:
        raise HTTPException(status_code=404, detail="Cliente no encontrado.")
    return result[0]
