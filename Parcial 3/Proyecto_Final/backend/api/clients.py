from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.db.database import query, execute

router = APIRouter(tags=["clientes"])

class ClientCreateRequest(BaseModel):
    nombre: str
    email: str
    telefono: Optional[str] = None

@router.get("/clients")
def list_clients():
    return query("SELECT * FROM clientes")

@router.get("/clients/{client_id}")
def get_client(client_id: int):
    result = query("SELECT * FROM clientes WHERE id = ?", (client_id,))
    if not result:
        raise HTTPException(status_code=404, detail="Cliente no encontrado.")
    return result[0]

@router.post("/clients")
def create_client(payload: ClientCreateRequest):
    existing = query("SELECT id FROM clientes WHERE email = ?", (payload.email,))
    if existing:
        raise HTTPException(status_code=400, detail="Cliente con este email ya existe.")

    client_id = execute(
        "INSERT INTO clientes (nombre, email, telefono) VALUES (?, ?, ?)",
        (payload.nombre, payload.email, payload.telefono),
    )
    return {
        "id": client_id,
        "nombre": payload.nombre,
        "email": payload.email,
        "telefono": payload.telefono,
    }
