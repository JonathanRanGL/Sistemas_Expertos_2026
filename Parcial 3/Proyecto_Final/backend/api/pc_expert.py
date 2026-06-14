"""
backend/api/pc_expert.py
Endpoint del Agente 2 (Generador de Pedido) para el configurador "Arma tu PC".

Valida la compatibilidad de socket entre CPU y Motherboard, y entrega
una explicación generada por el motor de inferencias (sistema experto).
"""
import json
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.db.database import query

router = APIRouter()


class PCBuildRequest(BaseModel):
    cpu: str
    motherboard: str
    gpu: str


def _socket_from_text(texto: str) -> Optional[str]:
    """Detecta el socket (AM5 / LGA1700) a partir del texto visible del <option>."""
    texto_upper = texto.upper()
    if "AM5" in texto_upper:
        return "AM5"
    if "LGA 1700" in texto_upper or "LGA1700" in texto_upper:
        return "LGA1700"
    return None


def _buscar_producto_por_nombre(fragmento: str):
    """Busca en la tabla productos uno cuyo nombre contenga el fragmento dado."""
    rows = query("SELECT * FROM productos WHERE nombre LIKE ?", (f"%{fragmento}%",))
    return rows[0] if rows else None


@router.post("/pc-expert/validate")
def validar_compilado(build: PCBuildRequest):
    """
    Recibe los textos seleccionados de CPU, Motherboard y GPU
    desde el configurador "Arma tu PC" y valida:
      1. Compatibilidad de socket (CPU <-> Motherboard)
      2. Disponibilidad en catálogo (si existe un producto similar)

    Devuelve una explicación estilo "Agente 3 - Supervisor".
    """
    cpu_socket = _socket_from_text(build.cpu)
    mobo_socket = _socket_from_text(build.motherboard)

    # ── Regla de inferencia: incompatibilidad_socket ──
    if cpu_socket and mobo_socket and cpu_socket != mobo_socket:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Incompatibilidad de socket detectada. El procesador usa socket "
                f"{cpu_socket} pero la tarjeta madre seleccionada usa {mobo_socket}. "
                f"Selecciona una tarjeta madre con socket {cpu_socket}."
            ),
        )

    if not cpu_socket or not mobo_socket:
        raise HTTPException(
            status_code=400,
            detail="No se pudo determinar el socket del procesador o la tarjeta madre seleccionados.",
        )

    # ── Intentar enriquecer con datos reales del catálogo ──
    cpu_part = build.cpu.split("(")[0].strip()
    gpu_part = build.gpu.strip()

    cpu_producto = _buscar_producto_por_nombre(cpu_part) or _buscar_producto_por_nombre(cpu_part.split(" ")[-1])
    gpu_producto = _buscar_producto_por_nombre(gpu_part)

    precio_total = 0.0
    detalles_precio = []

    for prod, etiqueta in ((cpu_producto, "CPU"), (gpu_producto, "GPU")):
        if prod:
            precio_total += prod["precio"]
            detalles_precio.append(f"{etiqueta}: {prod['nombre']} (${prod['precio']:,.2f})")

    explicacion = (
        f"Sistema Experto — Agente 2 (Generador de Pedido): "
        f"Procesador con socket {cpu_socket} y tarjeta madre con socket {mobo_socket} "
        f"son compatibles. "
    )
    if detalles_precio:
        explicacion += "Componentes identificados en catálogo: " + "; ".join(detalles_precio) + ". "
        explicacion += f"Precio estimado del ensamblado (CPU + GPU): ${precio_total:,.2f}."
    else:
        explicacion += "No se encontraron coincidencias exactas en el catálogo para calcular precio, pero la combinación es válida."

    return {
        "valido": True,
        "cpu_socket": cpu_socket,
        "motherboard_socket": mobo_socket,
        "precio_estimado": precio_total if detalles_precio else None,
        "explanation": explicacion,
        "rules_triggered": ["incompatibilidad_socket (no disparada - compatible)"],
    }
