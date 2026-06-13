"""
Agente 2 — Generador de Pedido
Procesa pedidos, valida stock, aplica reglas y persiste la orden.
"""
import json
from typing import Any, Dict, List, Optional

from backend.agents.agent3_supervisor import SupervisorAgent
from backend.core.inference_engine import InferenceEngine
from backend.db.database import query, execute, execute_many


class OrderAgent:
    def __init__(self) -> None:
        self.engine = InferenceEngine()
        self.supervisor = SupervisorAgent()

    def _fetch_client(self, cliente_id: int) -> Dict[str, Any]:
        result = query("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
        return result[0] if result else {}

    def _fetch_products(self, product_ids: List[int]) -> List[Dict[str, Any]]:
        placeholders = ",".join(["?" for _ in product_ids])
        return query(
            f"SELECT id, nombre, precio, stock, categoria, specs FROM productos WHERE id IN ({placeholders}) AND activo = 1",
            tuple(product_ids),
        )

    def _decrement_stock(self, items: List[Dict[str, Any]]) -> None:
        for item in items:
            execute(
                "UPDATE productos SET stock = stock - ? WHERE id = ?",
                (item["cantidad"], item["producto_id"]),
            )

    def create_order(self, cliente_id: Optional[int], items: List[Dict[str, Any]], notas: str = "") -> Dict[str, Any]:
        if not items:
            raise ValueError("El pedido debe contener al menos un artículo.")
        cliente_id = cliente_id or None

        product_ids = list({item["producto_id"] for item in items})
        products = self._fetch_products(product_ids)
        if len(products) != len(product_ids):
            raise ValueError("Algunos productos no existen o no están activos.")

        products_by_id = {product["id"]: product for product in products}
        subtotal = 0.0

        for item in items:
            product = products_by_id.get(item["producto_id"])
            if not product:
                raise ValueError(f"Producto {item['producto_id']} no encontrado.")
            if item["cantidad"] < 1:
                raise ValueError("La cantidad debe ser como mínimo 1.")
            if item["cantidad"] > product["stock"]:
                raise ValueError(f"Stock insuficiente para el producto {product['nombre']}.")
            subtotal += product["precio"] * item["cantidad"]

        cliente = self._fetch_client(cliente_id) if cliente_id is not None else {}
        if cliente_id is not None and not cliente:
            raise ValueError("Cliente no encontrado.")

        inference = self.engine.evaluate(
            {
                "cliente": cliente,
                "items": items,
                "products": products,
                "subtotal": subtotal,
            }
        )

        descuento = inference["discount"]
        envio_gratis = 1 if inference["envio_gratis"] else 0
        total = subtotal - descuento

        detalle_items = [
            {
                "producto_id": item["producto_id"],
                "cantidad": item["cantidad"],
                "precio_unit": products_by_id[item["producto_id"]]["precio"],
                "subtotal": products_by_id[item["producto_id"]]["precio"] * item["cantidad"],
            }
            for item in items
        ]

        inferencias_json = json.dumps(
            {
                "rules_triggered": inference["rules_triggered"],
                "warnings": inference["warnings"],
                "recommendations": inference["recommendations"],
            },
            ensure_ascii=False,
        )

        pedido_id = execute(
            """
            INSERT INTO pedidos (cliente_id, subtotal, descuento, total, envio_gratis, notas_cliente, notas_agente, inferencias)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (cliente_id, subtotal, descuento, total, envio_gratis, notas, "", inferencias_json),
        )

        detalle_params = [
            (
                pedido_id,
                item["producto_id"],
                item["cantidad"],
                item["precio_unit"],
                item["subtotal"],
            )
            for item in detalle_items
        ]
        execute_many(
            """
            INSERT INTO detalle_pedido (pedido_id, producto_id, cantidad, precio_unit, subtotal)
            VALUES (?, ?, ?, ?, ?)
            """,
            detalle_params,
        )

        self._decrement_stock(items)

        if cliente:
            nuevos_compras = cliente.get("total_compras", 0) + 1
            nuevos_gastado = cliente.get("total_gastado", 0.0) + total
            es_frecuente = 1 if nuevos_compras > 5 else cliente.get("es_frecuente", 0)
            descuento_aplicable = 0.2 if nuevos_gastado > 100000 else 0.1 if nuevos_compras > 5 else 0.0
            execute(
                "UPDATE clientes SET total_compras = ?, total_gastado = ?, es_frecuente = ?, descuento_aplicable = ? WHERE id = ?",
                (nuevos_compras, nuevos_gastado, es_frecuente, descuento_aplicable, cliente_id),
            )

        order_summary = {
            "pedido_id": pedido_id,
            "cliente_id": cliente_id,
            "subtotal": subtotal,
            "descuento": descuento,
            "total": total,
            "envio_gratis": bool(envio_gratis),
        }

        explanation = self.supervisor.explain(order_summary, detalle_items, inference)
        notas_agente = f"Notas del cliente: {notas}. {explanation}" if notas else explanation
        execute(
            "UPDATE pedidos SET notas_agente = ? WHERE id = ?",
            (notas_agente, pedido_id),
        )

        return {
            "pedido_id": pedido_id,
            "cliente_id": cliente_id,
            "subtotal": subtotal,
            "descuento": descuento,
            "total": total,
            "envio_gratis": bool(envio_gratis),
            "inferencias": inference,
            "notas_cliente": notas,
            "notas_agente": notas_agente,
        }
