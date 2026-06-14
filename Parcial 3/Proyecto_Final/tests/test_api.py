"""
tests/test_api.py
Pruebas de integración de la API — Tienda Inteligente.

Ejecutar con:  python -m unittest tests.test_api -v
(desde la raíz del proyecto, con el entorno virtual activado)
"""
import os
import sys
import tempfile
import sqlite3
import unittest
import importlib
import json
from pathlib import Path
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.db.models import CREATE_TABLES, CREATE_INDEXES


def init_test_db(path: Path) -> None:
    conn = sqlite3.connect(path)
    conn.executescript(CREATE_TABLES)
    conn.executescript(CREATE_INDEXES)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO productos (id, nombre, categoria, marca, precio, precio_original, stock,
                               descripcion, specs, rating, num_reviews, es_tendencia, activo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (1, "NVIDIA GTX 1660", "GPU", "NVIDIA", 12000.0, None, 3,
         "Tarjeta gráfica de alto rendimiento", json.dumps({"tdp": "130W"}), 4.5, 50, 0, 1),
    )

    cursor.execute(
        """
        INSERT INTO productos (id, nombre, categoria, marca, precio, precio_original, stock,
                               descripcion, specs, rating, num_reviews, es_tendencia, activo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (2, "Intel Core i5-13600K", "CPU", "Intel", 9500.0, None, 5,
         "Procesador de 13ª generación", json.dumps({"socket": "LGA1700", "tdp": "125W"}), 4.6, 95, 0, 1),
    )

    cursor.execute(
        """
        INSERT INTO productos (id, nombre, categoria, marca, precio, precio_original, stock,
                               descripcion, specs, rating, num_reviews, es_tendencia, activo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (3, "ASUS PRIME Z790", "Motherboard", "ASUS", 6800.0, None, 2,
         "Placa madre Intel compatible DDR5", json.dumps({"socket": "LGA1700"}), 4.4, 40, 0, 1),
    )

    # Producto con stock bajo y precio en oferta, para probar /products/deals
    cursor.execute(
        """
        INSERT INTO productos (id, nombre, categoria, marca, precio, precio_original, stock,
                               descripcion, specs, rating, num_reviews, es_tendencia, activo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (4, "Corsair RM850x", "Fuente", "Corsair", 1500.0, 1800.0, 4,
         "Fuente modular 850W", json.dumps({"wattage": "850W"}), 4.7, 60, 0, 1),
    )

    cursor.execute(
        """
        INSERT INTO clientes (id, nombre, email, telefono, total_compras, total_gastado, es_frecuente, descuento_aplicable)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (1, "Prueba Cliente", "prueba@example.com", "555-0000", 2, 25000.0, 0, 0.0),
    )

    cursor.execute(
        """
        INSERT INTO reglas_inferencia (id, nombre, condicion, accion, activa, veces_disparada)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (1, "descuento_cliente_frecuente", "cliente.total_compras > 5", "aplicar_descuento(10%)", 1, 0),
    )

    cursor.execute(
        """
        INSERT INTO reglas_inferencia (id, nombre, condicion, accion, activa, veces_disparada)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (2, "envio_gratis_por_monto", "total_pedido > 50000", "aplicar_envio_gratis()", 1, 0),
    )

    cursor.execute(
        """
        INSERT INTO reglas_inferencia (id, nombre, condicion, accion, activa, veces_disparada)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (3, "incompatibilidad_socket", "cpu.socket != motherboard.socket", "sugerir_alternativa()", 1, 0),
    )

    conn.commit()
    conn.close()


class BackendAPITestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_file = Path(self.temp_dir.name) / "tienda_test.db"
        os.environ["TIENDA_DB_PATH"] = str(self.db_file)
        init_test_db(self.db_file)

        # Recargar los módulos del backend para que tomen la nueva ruta de BD.
        for module_name in list(sys.modules):
            if module_name.startswith("backend"):
                del sys.modules[module_name]

        import backend.main
        self.app = importlib.reload(backend.main).app
        self.client = TestClient(self.app)

    def tearDown(self) -> None:
        if self.client is not None:
            self.client.close()
            self.client = None
        try:
            self.temp_dir.cleanup()
        except PermissionError:
            pass
        if "TIENDA_DB_PATH" in os.environ:
            del os.environ["TIENDA_DB_PATH"]

    # ── Catálogo ──────────────────────────────────────────
    def test_list_products(self) -> None:
        response = self.client.get("/api/products")
        self.assertEqual(response.status_code, 200)
        products = response.json()
        self.assertIsInstance(products, list)
        self.assertGreaterEqual(len(products), 4)

    def test_get_product_detail(self) -> None:
        response = self.client.get("/api/products/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["nombre"], "NVIDIA GTX 1660")

    def test_get_product_not_found(self) -> None:
        response = self.client.get("/api/products/999")
        self.assertEqual(response.status_code, 404)

    def test_products_deals(self) -> None:
        response = self.client.get("/api/products/deals")
        self.assertEqual(response.status_code, 200)
        deals = response.json()
        self.assertTrue(any(p["id"] == 4 for p in deals))

    # ── Pedidos (Agente 2 + Agente 3) ─────────────────────
    def test_create_order_success(self) -> None:
        payload = {
            "cliente_id": 1,
            "items": [{"producto_id": 1, "cantidad": 1}],
            "notas": "Prueba de pedido",
        }
        response = self.client.post("/api/orders/checkout", json=payload)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["pedido_id"], 1)
        self.assertEqual(data["subtotal"], 12000.0)
        self.assertEqual(data["total"], 12000.0)
        self.assertIsInstance(data["inferencias"], dict)
        self.assertIn("explicacion_agente3", data)

    def test_create_order_insufficient_stock(self) -> None:
        payload = {
            "cliente_id": 1,
            "items": [{"producto_id": 1, "cantidad": 10}],
            "notas": "Stock insuficiente",
        }
        response = self.client.post("/api/orders/checkout", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Stock insuficiente", response.json().get("detail", ""))

    def test_get_order_details(self) -> None:
        payload = {
            "cliente_id": 1,
            "items": [{"producto_id": 2, "cantidad": 1}, {"producto_id": 3, "cantidad": 1}],
            "notas": "Pedido con compatibilidad",
        }
        create_resp = self.client.post("/api/orders/checkout", json=payload)
        self.assertEqual(create_resp.status_code, 200)

        pedido_id = create_resp.json()["pedido_id"]
        get_resp = self.client.get(f"/api/orders/{pedido_id}")
        self.assertEqual(get_resp.status_code, 200)

        order_data = get_resp.json()
        self.assertEqual(order_data["id"], pedido_id)
        self.assertIn(order_data["envio_gratis"], (0, 1))
        self.assertEqual(len(order_data["items"]), 2)

    # ── Chat (Agente 1) ────────────────────────────────────
    def test_chat_endpoint(self) -> None:
        response = self.client.post("/api/chat", json={"message": "Hola"})
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIn("reply", body)
        self.assertTrue(len(body["reply"]) > 0)

    # ── Clientes ────────────────────────────────────────────
    def test_create_client(self) -> None:
        payload = {
            "nombre": "Cliente Test",
            "email": "cliente_test@example.com",
            "telefono": "555-1234",
        }
        response = self.client.post("/api/clients", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["nombre"], payload["nombre"])
        self.assertEqual(data["email"], payload["email"])

        list_response = self.client.get("/api/clients")
        self.assertEqual(list_response.status_code, 200)
        clients = list_response.json()
        self.assertTrue(any(c["email"] == payload["email"] for c in clients))

    # ── Arma tu PC (Agente 2 - validación de compatibilidad) ──
    def test_pc_expert_compatible(self) -> None:
        payload = {
            "cpu": "Intel Core i5-13600K (Socket LGA 1700)",
            "motherboard": "ASUS TUF Gaming B760-PLUS (LGA 1700)",
            "gpu": "NVIDIA RTX 4060 8GB",
        }
        response = self.client.post("/api/pc-expert/validate", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["valido"])

    def test_pc_expert_incompatible(self) -> None:
        payload = {
            "cpu": "AMD Ryzen 5 7600X (Socket AM5)",
            "motherboard": "ASUS TUF Gaming B760-PLUS (LGA 1700)",
            "gpu": "NVIDIA RTX 4060 8GB",
        }
        response = self.client.post("/api/pc-expert/validate", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Incompatibilidad", response.json()["detail"])


if __name__ == "__main__":
    unittest.main()
