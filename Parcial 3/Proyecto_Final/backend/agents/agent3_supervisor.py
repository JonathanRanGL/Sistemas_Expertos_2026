"""
Agente 3 — Supervisor / Explicador
Genera resúmenes de pedido y explica las inferencias aplicadas.
"""
import json
from typing import Any, Dict, List


class SupervisorAgent:
    def summarize(self, order: Dict[str, Any], details: List[Dict[str, Any]], inferencias: Dict[str, Any]) -> Dict[str, Any]:
        reglas = inferencias.get("rules_triggered", [])
        warnings = inferencias.get("warnings", [])
        recommendations = inferencias.get("recommendations", [])

        linea_items = [f"{item['cantidad']}x {item['producto_id']}" for item in details]
        summary = {
            "titulo": f"Pedido #{order.get('pedido_id')} - Cliente {order.get('cliente_id')}",
            "subtotal": order.get("subtotal"),
            "descuento": order.get("descuento"),
            "total": order.get("total"),
            "envio_gratis": order.get("envio_gratis"),
            "items": linea_items,
            "advertencias": warnings,
            "recomendaciones": recommendations,
            "reglas_aplicadas": [rule.get("nombre") for rule in reglas],
        }

        return summary

    def parse_inferencias(self, inferencias_raw: str) -> Dict[str, Any]:
        try:
            return json.loads(inferencias_raw)
        except (ValueError, TypeError):
            return {"rules_triggered": [], "warnings": [], "recommendations": []}
