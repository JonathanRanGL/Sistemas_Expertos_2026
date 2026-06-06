"""
scripts/init_db.py
Crea las tablas de la base de datos SQLite.
Ejecutar una sola vez: python scripts/init_db.py
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sqlite3
from pathlib import Path
from backend.db.models import CREATE_TABLES, CREATE_INDEXES
from backend.db.database import DB_PATH


def init_database():
    print(f"📦 Inicializando base de datos en: {DB_PATH}")

    if DB_PATH.exists():
        print("⚠️  La base de datos ya existe. ¿Deseas recrearla? (s/n): ", end="")
        resp = input().strip().lower()
        if resp != "s":
            print("✅ Sin cambios.")
            return
        DB_PATH.unlink()
        print("🗑️  Base de datos anterior eliminada.")

    conn = sqlite3.connect(str(DB_PATH))
    conn.executescript(CREATE_TABLES)
    conn.executescript(CREATE_INDEXES)
    conn.close()

    print("✅ Tablas creadas:")
    print("   • productos")
    print("   • clientes")
    print("   • pedidos")
    print("   • detalle_pedido")
    print("   • reglas_inferencia")
    print("\n👉 Ahora ejecuta: python scripts/seed_db.py")


if __name__ == "__main__":
    init_database()
