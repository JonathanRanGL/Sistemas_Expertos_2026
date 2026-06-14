"""
backend/api/pc_expert.py
Endpoint del Agente 2 (Generador de Pedido) para el configurador "Arma tu PC".

Valida compatibilidad de socket, potencia de la fuente y stock de cada
componente, usando producto_id reales de la base de datos.
"""
import json
from typing import Optional, Dict, Any, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.db.database import query

router = APIRouter()


class PCBuildRequest(BaseModel):
    cpu_id: int
    motherboard_id: int
    gpu_id: Optional[int] = None
    ram_id: Optional[int] = None
    ssd_id: Optional[int] = None
    fuente_id: Optional[int] = None
    cooler_id: Optional[int] = None
    gabinete_id: Optional[int] = None


def _get_product(product_id: int) -> Optional[Dict[str, Any]]:
    rows = query("SELECT * FROM productos WHERE id = ? AND activo = 1", (product_id,))
    return rows[0] if rows else None


def _parse_specs(product: Dict[str, Any]) -> Dict[str, Any]:
    specs = product.get("specs")
    if isinstance(specs, str):
        try:
            return json.loads(specs)
        except (json.JSONDecodeError, TypeError):
            return {}
    return specs or {}


@router.post("/pc-expert/validate")
def validar_compilado(build: PCBuildRequest):
    """
    Recibe los IDs de los componentes seleccionados en el configurador
    "Arma tu PC" y valida:
      1. Compatibilidad de socket (CPU <-> Motherboard)
      2. Suficiencia de la fuente de poder (TDP total vs wattage)
      3. Stock disponible de cada componente
      4. Advertencias de stock bajo (<3 unidades)

    Devuelve precio total, reglas disparadas y explicación del sistema experto.
    """
    cpu = _get_product(build.cpu_id)
    motherboard = _get_product(build.motherboard_id)

    if not cpu:
        raise HTTPException(status_code=404, detail=f"CPU con id={build.cpu_id} no encontrada.")
    if not motherboard:
        raise HTTPException(status_code=404, detail=f"Motherboard con id={build.motherboard_id} no encontrada.")

    cpu_specs = _parse_specs(cpu)
    mobo_specs = _parse_specs(motherboard)
    cpu_socket = cpu_specs.get("socket")
    mobo_socket = mobo_specs.get("socket")

    # Regla: incompatibilidad_socket
    if cpu_socket and mobo_socket and cpu_socket != mobo_socket:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Incompatibilidad de socket detectada. "
                f"'{cpu['nombre']}' usa {cpu_socket} pero "
                f"'{motherboard['nombre']}' usa {mobo_socket}. "
                f"Selecciona una tarjeta madre con socket {cpu_socket}."
            ),
        )

    # Recopilar todos los componentes seleccionados
    component_slots: List[tuple] = [
        ("CPU",        build.cpu_id),
        ("Motherboard", build.motherboard_id),
        ("GPU",        build.gpu_id),
        ("RAM",        build.ram_id),
        ("SSD",        build.ssd_id),
        ("Fuente",     build.fuente_id),
        ("Cooler",     build.cooler_id),
        ("Gabinete",   build.gabinete_id),
    ]

    components: Dict[str, Dict[str, Any]] = {}
    for label, pid in component_slots:
        if pid is not None:
            prod = _get_product(pid)
            if not prod:
                raise HTTPException(status_code=404, detail=f"{label} con id={pid} no encontrada en el catálogo.")
            components[label] = prod

    # Validación de stock (bloquea si algún componente está agotado)
    out_of_stock = [
        f"{lab}: {p['nombre']} (agotado)"
        for lab, p in components.items()
        if p.get("stock", 0) <= 0
    ]
    if out_of_stock:
        raise HTTPException(
            status_code=400,
            detail=f"Sin stock: {', '.join(out_of_stock)}. Selecciona una alternativa.",
        )

    warnings: List[str] = []
    rules_triggered: List[str] = []

    # Advertencia de stock bajo (no bloquea)
    low_stock = [
        f"{lab}: {p['nombre']} (solo {p['stock']} disponible{'s' if p['stock'] != 1 else ''})"
        for lab, p in components.items()
        if 0 < p.get("stock", 0) < 3
    ]
    if low_stock:
        warnings.append(f"Stock bajo — {', '.join(low_stock)}")
        rules_triggered.append("alerta_stock_bajo")

    # Regla: psu_insuficiente
    total_tdp = 0
    for lab, prod in components.items():
        specs = _parse_specs(prod)
        tdp_raw = specs.get("tdp") or specs.get("TDP") or "0"
        try:
            total_tdp += int(str(tdp_raw).replace("W", ""))
        except (ValueError, AttributeError):
            pass

    psu = components.get("Fuente")
    if psu:
        psu_specs = _parse_specs(psu)
        wattage_raw = psu_specs.get("wattage", "0W")
        try:
            psu_watts = int(str(wattage_raw).replace("W", ""))
        except (ValueError, AttributeError):
            psu_watts = 0
        if psu_watts > 0 and total_tdp > psu_watts * 0.8:
            warnings.append(
                f"TDP total estimado ({total_tdp}W) supera el 80% de la fuente "
                f"({psu_watts}W). Considera una fuente de mayor potencia."
            )
            rules_triggered.append("psu_insuficiente")

    precio_total = sum(p.get("precio", 0) for p in components.values())

    lines = [
        "Sistema Experto — Agente 2 (Generador de Pedido):",
        f"✓ Socket compatible: {cpu['nombre']} ({cpu_socket}) ↔ {motherboard['nombre']} ({mobo_socket}).",
    ]
    for lab, prod in components.items():
        lines.append(f"  • {lab}: {prod['nombre']} — ${prod['precio']:,.2f}")
    lines.append(f"Precio total estimado del ensamblado: ${precio_total:,.2f}")
    if warnings:
        lines.append("Advertencias: " + " | ".join(warnings))
    if not rules_triggered:
        rules_triggered.append("incompatibilidad_socket (no disparada — compatible)")

    return {
        "valido": True,
        "cpu_socket": cpu_socket,
        "motherboard_socket": mobo_socket,
        "precio_total": precio_total,
        "componentes": {
            lab: {"id": p["id"], "nombre": p["nombre"], "precio": p["precio"]}
            for lab, p in components.items()
        },
        "warnings": warnings,
        "rules_triggered": rules_triggered,
        "explanation": "\n".join(lines),
    }
