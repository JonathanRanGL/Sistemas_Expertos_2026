"""
Agente 2 — Generador de Pedido
Procesa pedidos, valida stock, aplica reglas y persiste la orden.
"""
import json
from typing import Any, Dict, List

from backend.core.inference_engine import InferenceEngine
from backend.db.database import query, execute, execute_many


class OrderAgent:
    def __init__(self) -> None:
        self.engine = InferenceEngine()

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

    def create_order(self, cliente_id: int, items: List[Dict[str, Any]], notas: str = "") -> Dict[str, Any]:
        if not items:
            raise ValueError("El pedido debe contener al menos un artículo.")

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

        cliente = self._fetch_client(cliente_id)
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
            INSERT INTO pedidos (cliente_id, subtotal, descuento, total, envio_gratis, notas_agente, inferencias)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (cliente_id, subtotal, descuento, total, envio_gratis, notas, inferencias_json),
        )

        detalle_params = [
            (
                pedido_id,
                item["producto_id"],
                item["cantidad"],
                products_by_id[item["producto_id"]]["precio"],
                products_by_id[item["producto_id"]]["precio"] * item["cantidad"],
            )
            for item in items
        ]
        execute_many(
            """
            INSERT INTO detalle_pedido (pedido_id, producto_id, cantidad, precio_unit, subtotal)
            VALUES (?, ?, ?, ?, ?)
            """,
            detalle_params,
        )

        self._decrement_stock(items)

        return {
            "pedido_id": pedido_id,
            "cliente_id": cliente_id,
            "subtotal": subtotal,
            "descuento": descuento,
            "total": total,
            "envio_gratis": bool(envio_gratis),
            "inferencias": inference,
        }
