"""
scripts/seed_db.py
Carga datos de prueba realistas en la base de datos.
Ejecutar después de init_db.py: python scripts/seed_db.py
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db.database import execute, execute_many
import json

# ─────────────────────────────────────────
# PRODUCTOS — Componentes PC reales
# ─────────────────────────────────────────

PRODUCTOS = [
    # GPUs
    (1, "NVIDIA RTX 4090", "GPU", "NVIDIA", 16999.00, 18999.00, 5, "Tarjeta gráfica profesional", json.dumps({"vram": "24GB GDDR6X", "vram_bandwidth": "1440GB/s", "tdp": "450W"}), 4.9, 250, 1, 1),
    (2, "AMD Radeon RX 7900 XTX", "GPU", "AMD", 12999.00, None, 8, "GPU RDNA 3 high-end", json.dumps({"vram": "24GB GDDR6", "vram_bandwidth": "576GB/s", "tdp": "420W"}), 4.7, 180, 1, 1),
    (17, "NVIDIA RTX 4060 8GB", "GPU", "NVIDIA", 5499.00, 5999.00, 22, "GPU ideal para 1080p", json.dumps({"vram": "8GB GDDR6", "tdp": "115W"}), 4.5, 310, 0, 1),
    (18, "NVIDIA RTX 4070 12GB", "GPU", "NVIDIA", 8999.00, None, 14, "GPU balanceada 1440p", json.dumps({"vram": "12GB GDDR6X", "tdp": "200W"}), 4.7, 240, 1, 1),
    (19, "AMD Radeon RX 7800 XT 16GB", "GPU", "AMD", 7499.00, None, 10, "GPU AMD para 1440p alto", json.dumps({"vram": "16GB GDDR6", "tdp": "263W"}), 4.6, 175, 0, 1),

    # CPUs
    (3, "Intel Core i9-13900K", "CPU", "Intel", 7999.00, None, 10, "CPU flagship 13ª gen", json.dumps({"cores": 24, "threads": 32, "tdp": "253W", "socket": "LGA1700"}), 4.8, 320, 1, 1),
    (4, "AMD Ryzen 9 7950X", "CPU", "AMD", 7499.00, None, 12, "CPU top-tier Zen 4", json.dumps({"cores": 16, "threads": 32, "tdp": "162W", "socket": "AM5"}), 4.8, 280, 1, 1),
    (20, "AMD Ryzen 5 7600X", "CPU", "AMD", 3299.00, 3699.00, 18, "CPU gama media Zen 4", json.dumps({"cores": 6, "threads": 12, "tdp": "105W", "socket": "AM5"}), 4.6, 210, 0, 1),
    (21, "AMD Ryzen 7 7800X3D", "CPU", "AMD", 4999.00, None, 9, "CPU gaming Zen 4 3D V-Cache", json.dumps({"cores": 8, "threads": 16, "tdp": "120W", "socket": "AM5"}), 4.9, 260, 1, 1),
    (22, "Intel Core i5-13600K", "CPU", "Intel", 4499.00, None, 16, "CPU gama media 13ª gen", json.dumps({"cores": 14, "threads": 20, "tdp": "181W", "socket": "LGA1700"}), 4.7, 230, 0, 1),

    # RAM
    (5, "Corsair Vengeance 32GB (2x16GB) DDR5", "RAM", "Corsair", 1899.00, None, 20, "RAM DDR5 high-speed", json.dumps({"capacity": "32GB", "type": "DDR5", "speed": "5600MHz"}), 4.6, 150, 0, 1),
    (6, "G.Skill Trident Z5 64GB (2x32GB) DDR5", "RAM", "G.Skill", 3999.00, None, 15, "RAM ultra-capacity", json.dumps({"capacity": "64GB", "type": "DDR5", "speed": "6000MHz"}), 4.7, 120, 0, 1),

    # SSDs
    (7, "Samsung 990 Pro 2TB NVMe", "SSD", "Samsung", 2999.00, 3499.00, 18, "SSD ultra-fast NVMe", json.dumps({"capacity": "2TB", "type": "NVMe M.2", "speed": "7100MB/s"}), 4.8, 200, 1, 1),
    (8, "WD Black SN850X 4TB NVMe", "SSD", "Western Digital", 4499.00, None, 12, "SSD premium 4TB", json.dumps({"capacity": "4TB", "type": "NVMe M.2", "speed": "7100MB/s"}), 4.7, 180, 0, 1),

    # Motherboards
    (9, "ASUS ROG MAXIMUS Z790", "Motherboard", "ASUS", 3299.00, None, 8, "Placa madre Intel top-tier", json.dumps({"socket": "LGA1700", "chipset": "Z790", "memory": "DDR5"}), 4.7, 140, 0, 1),
    (10, "MSI MPG B850 EDGE WIFI", "Motherboard", "MSI", 2899.00, None, 10, "Placa madre AMD B850", json.dumps({"socket": "AM5", "chipset": "B850", "memory": "DDR5"}), 4.6, 110, 0, 1),
    (23, "ASUS ROG Strix B650E-F", "Motherboard", "ASUS", 2499.00, None, 12, "Placa madre AMD B650E", json.dumps({"socket": "AM5", "chipset": "B650E", "memory": "DDR5"}), 4.6, 95, 0, 1),
    (24, "MSI MAG X670E Tomahawk", "Motherboard", "MSI", 3199.00, None, 7, "Placa madre AMD X670E", json.dumps({"socket": "AM5", "chipset": "X670E", "memory": "DDR5"}), 4.7, 88, 0, 1),
    (25, "Gigabyte Z790 AORUS ELITE", "Motherboard", "Gigabyte", 2999.00, None, 9, "Placa madre Intel Z790", json.dumps({"socket": "LGA1700", "chipset": "Z790", "memory": "DDR5"}), 4.5, 102, 0, 1),
    (26, "ASUS TUF Gaming B760-PLUS", "Motherboard", "ASUS", 2199.00, None, 14, "Placa madre Intel B760", json.dumps({"socket": "LGA1700", "chipset": "B760", "memory": "DDR5"}), 4.5, 121, 0, 1),

    # Fuentes
    (11, "Corsair HX1000 80+ Platinum", "Fuente", "Corsair", 2299.00, None, 15, "PSU modular 1000W", json.dumps({"wattage": "1000W", "efficiency": "80+ Platinum", "modular": "full"}), 4.8, 190, 0, 1),
    (12, "EVGA SuperNOVA 750 G6", "Fuente", "EVGA", 1299.00, 1499.00, 20, "PSU confiable 750W", json.dumps({"wattage": "750W", "efficiency": "80+ Gold", "modular": "full"}), 4.6, 160, 0, 1),

    # Coolers
    (13, "Noctua NH-D15 chromax", "Cooler", "Noctua", 999.00, None, 25, "Cooler aire premium", json.dumps({"type": "air", "socket": "universal", "tdp": "250W"}), 4.9, 210, 0, 1),
    (14, "NZXT Kraken X93 RGB", "Cooler", "NZXT", 1899.00, None, 18, "Cooler líquido 360mm", json.dumps({"type": "liquid", "size": "360mm", "tdp": "300W"}), 4.7, 170, 1, 1),

    # Gabinetes
    (15, "Lian Li Lancool 303", "Gabinete", "Lian Li", 899.00, None, 12, "Gabinete moderno", json.dumps({"form_factor": "ATX", "airflow": "excellent", "tempered_glass": True}), 4.6, 130, 0, 1),
    (16, "NZXT H7 Flow RGB", "Gabinete", "NZXT", 1199.00, 1399.00, 10, "Gabinete gaming", json.dumps({"form_factor": "ATX", "fans": "2x120mm", "tempered_glass": True}), 4.5, 100, 0, 1),
]

print("📊 Cargando productos de prueba...")
for prod in PRODUCTOS:
    execute(
        """
        INSERT INTO productos (id, nombre, categoria, marca, precio, precio_original, stock, 
                               descripcion, specs, rating, num_reviews, es_tendencia, activo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        prod
    )

# ─────────────────────────────────────────
# CLIENTES — Datos de prueba
# ─────────────────────────────────────────

CLIENTES = [
    (1, "Juan Pérez", "juan@example.com", "555-1234", 0, 0.0, 0, 0.0),
    (2, "María García", "maria@example.com", "555-5678", 3, 15000.0, 1, 10.0),
    (3, "Carlos López", "carlos@example.com", "555-9012", 1, 8500.0, 0, 0.0),
]

print("👥 Cargando clientes de prueba...")
for cliente in CLIENTES:
    execute(
        """
        INSERT INTO clientes (id, nombre, email, telefono, total_compras, total_gastado, 
                              es_frecuente, descuento_aplicable)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        cliente
    )

# ─────────────────────────────────────────
# REGLAS DE INFERENCIA
# ─────────────────────────────────────────

REGLAS = [
    (1, "descuento_cliente_frecuente", "cliente.total_compras > 5", "aplicar_descuento(10%)", 1, 0),
    (2, "descuento_cliente_vip", "cliente.total_gastado > 100000", "aplicar_descuento(20%)", 1, 0),
    (3, "envio_gratis_por_monto", "total_pedido > 50000", "aplicar_envio_gratis()", 1, 0),
    (4, "alerta_stock_bajo", "stock < cantidad_solicitada", "generar_alerta_reabastecimiento()", 1, 0),
    (5, "incompatibilidad_socket", "cpu.socket != motherboard.socket", "sugerir_alternativa()", 1, 0),
    (6, "psu_insuficiente", "total_tdp > psu_wattage * 0.8", "alertar_psu_insuficiente()", 1, 0),
    (7, "configuracion_balanceada", "gpu_price/cpu_price entre 0.8 y 1.2", "sugerir_configuracion_balanceada()", 1, 0),
]

print("📋 Cargando reglas de inferencia...")
for regla in REGLAS:
    execute(
        """
        INSERT INTO reglas_inferencia (id, nombre, condicion, accion, activa, veces_disparada)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        regla
    )

print("\n✅ Base de datos inicializada correctamente.")
print("📊 Datos cargados:")
print(f"   • {len(PRODUCTOS)} productos")
print(f"   • {len(CLIENTES)} clientes")
print(f"   • {len(REGLAS)} reglas de inferencia")
