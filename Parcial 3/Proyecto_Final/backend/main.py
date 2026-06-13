import sqlite3
import os
import sys
import os
# Esto fuerza a Python a buscar dentro de la carpeta 'backend'
sys.path.append(os.path.join(os.path.dirname(__file__)))


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Asegúrate de que las rutas 'api.products' existan en tu estructura
from api.products import router as products_router
from api.orders import router as orders_router
from api.chat import router as chat_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def init_db():
    # Esto crea tienda.db en la misma carpeta que main.py
    db_path = os.path.join(os.path.dirname(__file__), 'tienda.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Crear tablas
    c.execute('''CREATE TABLE IF NOT EXISTS productos 
                 (id INTEGER PRIMARY KEY, nombre TEXT, categoria TEXT, precio REAL)''')
    
    # Insertar datos de prueba si no existen
    c.execute("INSERT OR IGNORE INTO productos VALUES (1, 'Ryzen 7 7800X3D', 'CPU', 8500)")
    c.execute("INSERT OR IGNORE INTO productos VALUES (2, 'RTX 4070', 'GPU', 14000)")
    c.execute("INSERT OR IGNORE INTO productos VALUES (3, 'ASUS B650E', 'Motherboard', 4500)")
    
    conn.commit()
    conn.close()

# Inicializar DB
init_db()

# Registrar Routers
app.include_router(products_router, prefix="/api", tags=["Catálogo"])
app.include_router(orders_router, prefix="/api", tags=["Pedidos"])
app.include_router(chat_router, prefix="/api", tags=["Chat"])

@app.get("/")
def read_root():
    return {"status": "Servidor backend activo"}