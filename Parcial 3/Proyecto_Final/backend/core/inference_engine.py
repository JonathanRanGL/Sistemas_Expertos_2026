import json
from typing import Any, Dict, List

from backend.db.database import query


def _parse_specs(product: Dict[str, Any]) -> Dict[str, Any]:
    specs = product.get("specs")
    if isinstance(specs, str):
        try:
            return json.loads(specs)
        except json.JSONDecodeError:
            return {}
    return specs or {}


def _find_by_category(products: List[Dict[str, Any]], category: str):
    return next((p for p in products if p.get("categoria") == category), None)


class InferenceEngine:
    """
    Motor de inferencias del sistema experto.
    Evalúa reglas IF-THEN sobre los datos del pedido.

    Reglas implementadas:
      - descuento_cliente_frecuente
      - descuento_cliente_vip
      - envio_gratis_por_monto
      - alerta_stock_bajo
      - sugerir_reabastecimiento
      - incompatibilidad_socket
      - psu_insuficiente
      - presupuesto_excedido
      - configuracion_balanceada
    """

    def __init__(self) -> None:
        self.rules = self._load_rules()

    def _load_rules(self) -> Dict[str, Dict[str, Any]]:
        rows = query("SELECT id, nombre, condicion, accion FROM reglas_inferencia WHERE activa = 1")
        return {row["nombre"]: row for row in rows}

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        products = context.get("products", [])
        cliente = context.get("cliente", {})
        items = context.get("items", [])
        subtotal = context.get("subtotal", 0.0)

        products_info = [dict(product, specs=_parse_specs(product)) for product in products]
        cpu = _find_by_category(products_info, "CPU")
        motherboard = _find_by_category(products_info, "Motherboard")
        psu = _find_by_category(products_info, "Fuente")
        gpu = _find_by_category(products_info, "GPU")

        gpu_price = gpu.get("precio", 0.0) if gpu else 0.0
        cpu_price = cpu.get("precio", 0.0) if cpu else 0.0
        psu_wattage = 0
        if psu:
            psu_spec = psu.get("specs", {})
            psu_wattage = int(str(psu_spec.get("wattage", "0W")).replace("W", "") or 0)

        total_tdp = 0
        for item in items:
            product = next((p for p in products_info if p.get("id") == item.get("producto_id")), None)
            if product:
                specs = product.get("specs", {})
                tdp = specs.get("tdp") or specs.get("TDP") or 0
                try:
                    total_tdp += int(str(tdp).replace("W", "")) * int(item.get("cantidad", 1))
                except ValueError:
                    total_tdp += 0

        rule_results: List[Dict[str, Any]] = []
        warnings: List[str] = []
        recommendations: List[str] = []
        discount = 0.0
        envio_gratis = False

        def add_trigger(rule_name: str, reason: str) -> None:
            rule = self.rules.get(rule_name, {})
            rule_results.append({
                "id": rule.get("id"),
                "nombre": rule_name,
                "condicion": rule.get("condicion"),
                "accion": rule.get("accion"),
                "motivo": reason,
            })

        if cliente.get("total_compras", 0) > 5:
            discount = max(discount, subtotal * 0.10)
            add_trigger("descuento_cliente_frecuente", "Cliente con más de 5 compras frecuentes")

        if cliente.get("total_gastado", 0.0) > 100000:
            discount = max(discount, subtotal * 0.20)
            add_trigger("descuento_cliente_vip", "Cliente VIP con gasto acumulado mayor a 100000")

        if subtotal > 50000:
            envio_gratis = True
            add_trigger("envio_gratis_por_monto", "Pedido supera el umbral de envío gratis")

        low_stock_items = [item for item in items if next((p for p in products_info if p.get("id") == item.get("producto_id") and item.get("cantidad", 0) > p.get("stock", 0)), None)]
        if low_stock_items:
            warnings.append("Stock insuficiente para uno o más artículos del pedido.")
            add_trigger("alerta_stock_bajo", "Uno o más artículos exceden el stock disponible")

        low_stock_products = [p.get("nombre") for p in products_info if p.get("stock", 0) < 3]
        if low_stock_products:
            recommendations.append(f"Reabastecer productos: {', '.join(low_stock_products)}")
            add_trigger("sugerir_reabastecimiento", "Productos con stock bajo detectados")

        if cpu and motherboard and cpu.get("socket") != motherboard.get("socket"):
            warnings.append("Incompatibilidad de socket entre CPU y motherboard.")
            add_trigger("incompatibilidad_socket", "Los sockets del CPU y la motherboard no coinciden")

        if psu_wattage and total_tdp and total_tdp > psu_wattage * 0.8:
            warnings.append("La potencia de la fuente podría no ser suficiente para la configuración.")
            add_trigger("psu_insuficiente", "La carga térmica supera el 80% de la potencia de la fuente")

        if gpu_price and cpu_price:
            ratio = gpu_price / cpu_price
            if 0.8 <= ratio <= 1.2:
                recommendations.append("La relación GPU/CPU está balanceada para un buen desempeño.")
                add_trigger("configuracion_balanceada", "GPU y CPU tienen un balance de precio adecuado")

        if subtotal > 150000:
            warnings.append("El pedido supera el presupuesto medio recomendado.")
            add_trigger("presupuesto_excedido", "Subtotal mayor a 150000")

        return {
            "discount": round(discount, 2),
            "envio_gratis": envio_gratis,
            "warnings": warnings,
            "recommendations": recommendations,
            "rules_triggered": rule_results,
        }
