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
        pedido_id = order.get("pedido_id") or order.get("id")
        cliente_id = order.get("cliente_id")
        summary = {
            "titulo": f"Pedido #{pedido_id} - Cliente {cliente_id}",
            "subtotal": order.get("subtotal"),
            "descuento": order.get("descuento"),
            "total": order.get("total"),
            "envio_gratis": bool(order.get("envio_gratis")),
            "items": linea_items,
            "advertencias": warnings,
            "recomendaciones": recommendations,
            "reglas_aplicadas": [rule.get("nombre") for rule in reglas],
            "confirmacion_requerida": True,
        }

        return summary

    def explain(self, order: Dict[str, Any], details: List[Dict[str, Any]], inferencias: Dict[str, Any]) -> str:
        reglas = inferencias.get("rules_triggered", [])
        warnings = inferencias.get("warnings", [])
        recommendations = inferencias.get("recommendations", [])

        lineas = [
            f"El pedido #{order.get('pedido_id')} para cliente {order.get('cliente_id')} tiene un subtotal de ${order.get('subtotal'):.2f}.",
        ]

        if order.get("descuento"):
            lineas.append(f"Se aplica un descuento de ${order.get('descuento'):.2f}.")
        else:
            lineas.append("No se aplica descuento adicional.")

        if order.get("envio_gratis"):
            lineas.append("El envío gratuito se activa por las políticas de compra.")

        if reglas:
            nombres = ", ".join([rule.get("nombre", "regla") for rule in reglas])
            lineas.append(f"Reglas inferidas: {nombres}.")
        else:
            lineas.append("No se han disparado reglas específicas.")

        if warnings:
            lineas.append(f"Avisos: {'; '.join(warnings)}.")

        if recommendations:
            lineas.append(f"Recomendaciones: {'; '.join(recommendations)}.")

        lineas.append("Se solicita validación final del cliente antes de confirmar el envío.")
        return " ".join(lineas)

    def parse_inferencias(self, inferencias_raw: str) -> Dict[str, Any]:
        try:
            return json.loads(inferencias_raw)
        except (ValueError, TypeError):
            return {"rules_triggered": [], "warnings": [], "recommendations": []}
