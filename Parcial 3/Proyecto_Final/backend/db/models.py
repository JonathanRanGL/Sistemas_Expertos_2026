"""
Modelos de la base de datos — Tienda Inteligente
Define el esquema SQLite con 5 tablas para el sistema experto.
"""

# DDL — Sentencias de creación de tablas
CREATE_TABLES = """

-- ─────────────────────────────────────────
-- TABLA: productos
-- Catálogo completo de componentes PC
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS productos (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre          TEXT NOT NULL,
    categoria       TEXT NOT NULL,         -- GPU, CPU, RAM, SSD, Motherboard, Gabinete, Fuente, Cooler
    marca           TEXT NOT NULL,
    precio          REAL NOT NULL,
    precio_original REAL,                  -- Precio antes de descuento (NULL si no hay oferta)
    stock           INTEGER NOT NULL DEFAULT 0,
    descripcion     TEXT,
    specs           TEXT,                  -- JSON con especificaciones técnicas
    rating          REAL DEFAULT 0.0,
    num_reviews     INTEGER DEFAULT 0,
    es_tendencia    INTEGER DEFAULT 0,     -- 0 = false, 1 = true
    activo          INTEGER DEFAULT 1,
    fecha_creacion  TEXT DEFAULT (datetime('now'))
);

-- ─────────────────────────────────────────
-- TABLA: clientes
-- Registro de clientes con historial
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS clientes (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre              TEXT NOT NULL,
    email               TEXT UNIQUE NOT NULL,
    telefono            TEXT,
    total_compras       INTEGER DEFAULT 0,   -- Número de pedidos realizados
    total_gastado       REAL DEFAULT 0.0,
    es_frecuente        INTEGER DEFAULT 0,   -- Se activa automáticamente con inferencia
    descuento_aplicable REAL DEFAULT 0.0,    -- % de descuento ganado
    fecha_registro      TEXT DEFAULT (datetime('now')),
    ultimo_pedido       TEXT
);

-- ─────────────────────────────────────────
-- TABLA: pedidos
-- Órdenes generadas por el Agente 2
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS pedidos (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id      INTEGER,
    estado          TEXT DEFAULT 'pendiente',  -- pendiente, confirmado, enviado, cancelado
    subtotal        REAL NOT NULL DEFAULT 0.0,
    descuento       REAL DEFAULT 0.0,
    total           REAL NOT NULL DEFAULT 0.0,
    envio_gratis    INTEGER DEFAULT 0,
    notas_agente    TEXT,                       -- Explicación del Agente 3
    inferencias     TEXT,                       -- JSON con reglas disparadas
    fecha_pedido    TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

-- ─────────────────────────────────────────
-- TABLA: detalle_pedido
-- Líneas de cada pedido
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS detalle_pedido (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id   INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad    INTEGER NOT NULL,
    precio_unit REAL NOT NULL,
    subtotal    REAL NOT NULL,
    FOREIGN KEY (pedido_id)   REFERENCES pedidos(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- ─────────────────────────────────────────
-- TABLA: reglas_inferencia
-- Base de conocimiento del sistema experto
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS reglas_inferencia (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre      TEXT NOT NULL UNIQUE,
    condicion   TEXT NOT NULL,   -- Descripción de la condición IF
    accion      TEXT NOT NULL,   -- Descripción de la acción THEN
    activa      INTEGER DEFAULT 1,
    veces_disparada INTEGER DEFAULT 0
);
"""

# Índices para búsquedas rápidas
CREATE_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_productos_categoria ON productos(categoria);
CREATE INDEX IF NOT EXISTS idx_productos_marca     ON productos(marca);
CREATE INDEX IF NOT EXISTS idx_pedidos_cliente     ON pedidos(cliente_id);
CREATE INDEX IF NOT EXISTS idx_pedidos_estado      ON pedidos(estado);
"""
