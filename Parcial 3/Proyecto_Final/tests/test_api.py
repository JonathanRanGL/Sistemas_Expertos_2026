import os
import sys
import tempfile
import sqlite3
import unittest
import importlib
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
        INSERT INTO productos (id, nombre, categoria, marca, precio, stock, descripcion, specs, rating, num_reviews, es_tendencia, activo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            1,
            "NVIDIA GTX 1660",
            "GPU",
            "NVIDIA",
            12000.0,
            3,
            "Tarjeta gráfica de alto rendimiento",
            '{"tdp": "130W"}',
            4.5,
            50,
            0,
            1,
        ),
    )

    cursor.execute(
        """
        INSERT INTO productos (id, nombre, categoria, marca, precio, stock, descripcion, specs, rating, num_reviews, es_tendencia, activo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            2,
            "Intel Core i5-13600K",
            "CPU",
            "Intel",
            9500.0,
            5,
            "Procesador de 13ª generación",
            '{"socket": "LGA1700", "tdp": "125W"}',
            4.6,
            95,
            0,
            1,
        ),
    )

    cursor.execute(
        """
        INSERT INTO productos (id, nombre, categoria, marca, precio, stock, descripcion, specs, rating, num_reviews, es_tendencia, activo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            3,
            "ASUS PRIME Z790",
            "Motherboard",
            "ASUS",
            6800.0,
            2,
            "Placa madre Intel compatible DDR5",
            '{"socket": "LGA1700"}',
            4.4,
            40,
            0,
            1,
        ),
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

        # Reload backend modules after setting the database path environment variable.
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

    def test_list_products(self) -> None:
        response = self.client.get("/api/products")
        self.assertEqual(response.status_code, 200)
        products = response.json()
        self.assertTrue(isinstance(products, list))
        self.assertGreaterEqual(len(products), 3)

    def test_create_order_success(self) -> None:
        payload = {
            "cliente_id": 1,
            "items": [{"producto_id": 1, "cantidad": 1}],
            "notas": "Prueba de pedido",
        }
        response = self.client.post("/api/orders", json=payload)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["pedido_id"], 1)
        self.assertEqual(data["subtotal"], 12000.0)
        self.assertEqual(data["total"], 12000.0)
        self.assertIsInstance(data["inferencias"], dict)
        self.assertIsInstance(data["resumen"], dict)
        self.assertIn("notas_agente", data)

    def test_create_order_insufficient_stock(self) -> None:
        payload = {
            "cliente_id": 1,
            "items": [{"producto_id": 1, "cantidad": 10}],
            "notas": "Stock insuficiente",
        }
        response = self.client.post("/api/orders", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Stock insuficiente", response.json().get("detail", ""))

    def test_get_order_details(self) -> None:
        payload = {
            "cliente_id": 1,
            "items": [{"producto_id": 2, "cantidad": 1}, {"producto_id": 3, "cantidad": 1}],
            "notas": "Pedido con compatibilidad",
        }
        create_resp = self.client.post("/api/orders", json=payload)
        self.assertEqual(create_resp.status_code, 200)

        pedido_id = create_resp.json()["pedido_id"]
        get_resp = self.client.get(f"/api/orders/{pedido_id}")
        self.assertEqual(get_resp.status_code, 200)

        order_data = get_resp.json()
        self.assertEqual(order_data["pedido_id"], pedido_id)
        self.assertTrue(order_data["envio_gratis"] in (True, False))
        self.assertIsInstance(order_data["resumen"], dict)
        self.assertEqual(order_data["estado"], "pendiente")

    def test_chat_endpoint(self) -> None:
        response = self.client.post("/api/chat", json={"mensaje": "Hola"})
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIn("respuesta", body)
        self.assertEqual(body["origen"], "Agente 1 - Atención al Cliente")


if __name__ == "__main__":
    unittest.main()
