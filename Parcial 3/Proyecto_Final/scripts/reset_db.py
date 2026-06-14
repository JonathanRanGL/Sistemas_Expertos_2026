"""
scripts/reset_db.py
Reinicia la tienda a su estado inicial sin borrar el esquema.

- Restaura el stock original de los 47 productos
- Borra todos los pedidos y detalles de pedido
- Restaura los datos originales de los 3 clientes de prueba

Ejecutar: python scripts/reset_db.py
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db.database import execute, query
from scripts.seed_db import PRODUCTOS, CLIENTES


def reset_db() -> dict:
    # 1. Restaurar stock original de cada producto
    productos_actualizados = 0
    for prod in PRODUCTOS:
        prod_id = prod[0]
        stock_original = prod[6]
        execute(
            "UPDATE productos SET stock = ? WHERE id = ?",
            (stock_original, prod_id)
        )
        productos_actualizados += 1

    # 2. Borrar detalle_pedido primero (FK), luego pedidos; resetear autoincrement
    detalles = query("SELECT COUNT(*) as n FROM detalle_pedido")[0]["n"]
    pedidos = query("SELECT COUNT(*) as n FROM pedidos")[0]["n"]
    execute("DELETE FROM detalle_pedido")
    execute("DELETE FROM pedidos")
    # Resetear contadores de AUTOINCREMENT para que el siguiente pedido sea #1
    execute("DELETE FROM sqlite_sequence WHERE name='pedidos'")
    execute("DELETE FROM sqlite_sequence WHERE name='detalle_pedido'")

    # 3. Resetear clientes a valores iniciales del seed
    clientes_actualizados = 0
    for cliente in CLIENTES:
        cid, nombre, email, telefono, total_compras, total_gastado, es_frecuente, descuento = cliente
        execute(
            """UPDATE clientes SET
                total_compras = ?,
                total_gastado = ?,
                es_frecuente = ?,
                descuento_aplicable = ?
               WHERE id = ?""",
            (total_compras, total_gastado, es_frecuente, descuento, cid)
        )
        clientes_actualizados += 1

    return {
        "productos_restaurados": productos_actualizados,
        "pedidos_eliminados": pedidos,
        "detalles_eliminados": detalles,
        "clientes_reseteados": clientes_actualizados,
    }


if __name__ == "__main__":
    print("🔄 Reiniciando base de datos de la Tienda Inteligente...")
    resultado = reset_db()
    print(f"✅ Reset completado:")
    print(f"   • {resultado['productos_restaurados']} productos con stock restaurado")
    print(f"   • {resultado['pedidos_eliminados']} pedidos eliminados")
    print(f"   • {resultado['detalles_eliminados']} líneas de detalle eliminadas")
    print(f"   • {resultado['clientes_reseteados']} clientes reseteados")
