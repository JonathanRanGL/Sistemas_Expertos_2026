import sqlite3
import json
import os

# Guardar la base de datos de manera uniforme en la raíz de 'backend/'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "tienda.db")

def crear_tablas(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            marca TEXT,
            precio REAL NOT NULL,
            precio_original REAL,
            stock INTEGER NOT NULL,
            descripcion TEXT,
            specs TEXT,
            rating REAL DEFAULT 0,
            num_reviews INTEGER DEFAULT 0,
            es_tendencia BOOLEAN DEFAULT 0,
            activo BOOLEAN DEFAULT 1,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            email TEXT UNIQUE,
            telefono TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            estado TEXT,
            subtotal REAL,
            descuento REAL,
            total REAL,
            envio_gratis BOOLEAN,
            notas_agente TEXT,
            inferencias TEXT,
            fecha_pedido TIMESTAMP,
            FOREIGN KEY(cliente_id) REFERENCES clientes(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detalle_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER,
            producto_id INTEGER,
            cantidad INTEGER,
            precio_unit REAL,
            subtotal REAL,
            FOREIGN KEY(pedido_id) REFERENCES pedidos(id),
            FOREIGN KEY(producto_id) REFERENCES productos(id)
        )
    ''')

def poblar_datos(cursor):
    cursor.execute("INSERT OR IGNORE INTO clientes (id, nombre, email, telefono) VALUES (1, 'Cliente Prueba', 'cliente@test.com', '555-0000')")

    cursor.execute("SELECT COUNT(*) FROM productos")
    if cursor.fetchone()[0] >= 10:
        print("La base de datos ya contiene 10 o más productos. Saltando la inserción de prueba.")
        return

    productos_prueba = [
        ("NVIDIA GeForce RTX 4090", "GPU", "NVIDIA", 35000.0, 38000.0, 5, "Gráfica tope de gama.", json.dumps({"vram": "24GB"}), 4.9, 120, True),
        ("Intel Core i9-13900K", "CPU", "Intel", 12500.0, 14000.0, 10, "Procesador de 24 núcleos.", json.dumps({"socket": "LGA1700"}), 4.8, 85, True),
        ("Corsair Vengeance RGB 32GB DDR5", "RAM", "Corsair", 3200.0, 3500.0, 30, "Memoria DDR5.", json.dumps({"speed": "6000MHz"}), 4.7, 200, False),
        ("Samsung 990 PRO 2TB PCIe 4.0", "SSD", "Samsung", 4100.0, 4800.0, 20, "Almacenamiento NVMe.", json.dumps({"read": "7450MB/s"}), 4.9, 150, True),
        ("ASUS ROG Maximus Z790 Hero", "Motherboard", "ASUS", 11500.0, 12500.0, 8, "Placa base premium.", json.dumps({"socket": "LGA1700"}), 4.6, 45, False),
        ("AMD Ryzen 9 7950X3D", "CPU", "AMD", 13000.0, 14500.0, 15, "Procesador AMD con 3D V-Cache.", json.dumps({"socket": "AM5"}), 4.9, 310, True),
        ("Radeon RX 7900 XTX", "GPU", "AMD", 21000.0, 23000.0, 5, "Excelente relación calidad-precio en 4K.", json.dumps({"vram": "24GB"}), 4.7, 90, False),
        ("Corsair RM1000x", "Fuente", "Corsair", 3500.0, 4000.0, 25, "Fuente de poder de 1000W 80+ Gold.", json.dumps({"wattage": "1000W"}), 4.8, 410, False),
        ("NZXT H7 Flow", "Gabinete", "NZXT", 2800.0, 3200.0, 12, "Gabinete con flujo de aire optimizado.", json.dumps({"form_factor": "ATX"}), 4.8, 150, True),
        ("Noctua NH-D15", "Cooler", "Noctua", 2200.0, 2500.0, 40, "Disipación por aire de la más alta calidad.", json.dumps({"type": "Air"}), 4.9, 500, False)
    ]

    cursor.execute("DELETE FROM productos")
    cursor.executemany('''
        INSERT INTO productos (nombre, categoria, marca, precio, precio_original, stock, descripcion, specs, rating, num_reviews, es_tendencia)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', productos_prueba)
    print("✅ Seeding completado exitosamente con 10 componentes de hardware variados.")

def main():
    conn = sqlite3.connect(DB_PATH)
    crear_tablas(conn.cursor())
    poblar_datos(conn.cursor())
    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada y lista en tienda.db")

if __name__ == "__main__":
    main()