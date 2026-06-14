# 🔧 Fixes del Día 8 — Integración Backend ↔ Frontend

Este documento explica, problema por problema, qué estaba roto y cómo se corrigió.
Útil para responder preguntas técnicas durante la presentación.

---

## 1. `/api/products` devolvía 500 Internal Server Error

**Causa raíz:** existían **tres definiciones distintas del esquema de `productos`**:

1. `backend/main.py` tenía una función `init_db()` que se ejecutaba en cada arranque
   del servidor y creaba una tabla `productos` mínima: `(id, nombre, categoria, precio)`.
2. `backend/db/models.py` define el esquema completo y correcto: `(id, nombre, categoria,
   marca, precio, precio_original, stock, descripcion, specs, rating, num_reviews,
   es_tendencia, activo, fecha_creacion)`.
3. `backend/api/products.py` hacía `SELECT * FROM productos WHERE activo = 1`, columna
   que **no existía** en la tabla creada por `main.py`.

**Solución:**
- Se eliminó `init_db()` de `main.py`. La base de datos ahora se crea **una sola vez**
  con `python scripts/init_db.py` (usa el esquema de `models.py`) y se llena con
  `python scripts/seed_db.py`.
- `main.py` ya **no toca el esquema**, solo registra routers.

---

## 2. `/api/products/deals` → 404 Not Found

**Causa raíz:** el endpoint nunca se implementó; `ofertas.html` lo llamaba pero no existía
en `products.py`.

**Solución:** se agregó:
```python
@router.get("/products/deals")
def get_deals():
    # Productos donde precio_original > precio
```

---

## 3. `/api/pc-expert/validate` → 404 Not Found

**Causa raíz:** el configurador "Arma tu PC" (`armatupc.html`) llamaba este endpoint,
pero no existía ningún router para él.

**Solución:** se creó `backend/api/pc_expert.py` con el endpoint `POST /api/pc-expert/validate`,
que:
1. Extrae el socket (AM5 / LGA1700) del texto de CPU y Motherboard seleccionados.
2. Aplica la **regla de inferencia `incompatibilidad_socket`**: si los sockets no
   coinciden, responde `400` con una explicación clara.
3. Si son compatibles, busca los productos reales en el catálogo para calcular un
   precio estimado y genera una explicación en estilo "Agente 2 / Sistema Experto".

---

## 4. El carrito no reconocía las PCs armadas

**Causa raíz:** `armatupc.html` guardaba el ensamblado en `localStorage` bajo la clave
`"tienda_cart"` (singular), mientras que `catalog.html`, `ofertas.html` y `checkout.html`
usaban `"tienda_cart_v1"`. Además, el formato del objeto guardado era distinto
(`{id, nombre, precio, cantidad}` vs `{producto_id, cantidad}`).

**Solución:**
- Se unificó todo a la clave `tienda_cart_v1`.
- Los ensamblados ahora se guardan con un flag `es_build: true` y una `descripcion_build`,
  para que `checkout.html` los pueda mostrar de forma diferenciada (no son un producto
  individual del catálogo).

---

## 5. El checkout no procesaba el carrito completo

**Causa raíz:** `backend/api/orders.py` tenía un modelo `Order` que aceptaba **un solo
item** (`{componente_id, cantidad}`) e insertaba directamente en una tabla `pedidos`
con columnas que ni siquiera coincidían con `models.py`. El frontend (`checkout.html`)
en cambio mandaba `{cliente_id, items: [...]}` y esperaba `{pedido_id, explicacion_agente3}`.

**Solución:** se reescribió `orders.py` para usar el **Agente 2 (`OrderAgent`)**, que:
1. Valida que cada producto exista, esté activo y tenga stock suficiente.
2. Calcula subtotal y ejecuta el **motor de inferencias** (`InferenceEngine`) con
   los datos del cliente, productos y carrito.
3. Aplica descuentos (`descuento_cliente_frecuente`, `descuento_cliente_vip`),
   envío gratis (`envio_gratis_por_monto`), advertencias de stock/compatibilidad, etc.
4. Guarda el pedido y su detalle en `pedidos` / `detalle_pedido`.
5. Llama al **Agente 3 (`SupervisorAgent`)** para generar la explicación en
   lenguaje natural (`explicacion_agente3`).
6. Actualiza el historial del cliente (`total_compras`, `total_gastado`, `es_frecuente`).

`checkout.html` se reescribió para mostrar nombre y precio real de cada producto
(vía `/api/products/{id}`), permitir cambiar cantidades o eliminar items, mostrar
subtotal/total, y renderizar la explicación del Agente 3 incluyendo advertencias
y recomendaciones del motor de inferencias.

---

## 6. API Key de Gemini filtrada / chat roto

**Causa raíz:** `backend/api/chat.py` tenía la API Key de Gemini **hardcodeada
directamente en el código** (un archivo versionado en Git), y usaba el modelo
`gemini-pro`, que ya está descontinuado.

**Solución:**
- La key ahora se lee desde el archivo `.env` (`GEMINI_API_KEY`), que está en
  `.gitignore` y nunca se sube a GitHub.
- Se actualizó el modelo a `gemini-1.5-flash`.
- Se agregó un **fallback automático**: si no hay key configurada, o si la llamada
  a Gemini falla por cualquier motivo (key inválida, cuota, sin red, etc.), el chat
  responde usando el **Agente 1 basado en reglas** (`CustomerAgent`), que detecta
  intención (saludo / compra / compatibilidad / consulta) y busca productos por
  categoría o marca mencionada. Así el chat **nunca se queda sin respuesta**.
- Se agregaron **preguntas sugeridas** en `chat.html` para guiar la conversación.

⚠️ **Importante:** la key que se filtró ya fue invalidada automáticamente por Google.
Genera una nueva en https://aistudio.google.com/app/apikey y agrégala **solo** en tu
archivo `.env` local (nunca en el código).

---

## 7. Imports inconsistentes (`backend.db.database` vs `db.database`)

**Causa raíz:** algunos archivos usaban `from backend.db.database import ...` y otros
intentaban `sys.path.append` para usar imports relativos sin el prefijo `backend.`,
generando `ModuleNotFoundError` dependiendo de cómo se ejecutara el servidor.

**Solución:** como el servidor se ejecuta desde la raíz del proyecto con
`python -m uvicorn backend.main:app --reload`, **todos los imports usan el prefijo
`backend.`** de forma consistente (`from backend.db.database import query`, etc.).
Se quitó el `sys.path.append` de `main.py`.

---

## 8. Enlaces rotos de navegación

**Causa raíz:** el logo en `catalog.html` y `ofertas.html` usaba
`onclick="window.location.href='../index.html'"`, una ruta que sube un directorio
fuera de `frontend/`, donde `index.html` no existe.

**Solución:** se corrigió a `'index.html'` (mismo directorio).

---

## 9. Archivos duplicados/obsoletos eliminados

- `backend/api/seed_db.py` — duplicado de `scripts/seed_db.py` con un esquema antiguo
  e incompatible.
- `index.html` en la raíz del proyecto — duplicado de `frontend/index.html`.
- `tests/tienda_test.db` — base de datos de prueba generada por una corrida anterior,
  no debe versionarse (los tests crean su propia BD temporal).

---

## 10. `requirements.txt` con dependencias conflictivas

**Causa raíz:** `langchain` y `langchain-google-genai` generaban conflictos de
resolución de dependencias con `google-generativeai`, y **no se usaban en ningún
archivo del proyecto**.

**Solución:** se eliminaron ambas dependencias. El proyecto usa `google-generativeai`
directamente (sin LangChain) para el Agente 1.

---

## ✅ Verificación

Se corrieron pruebas de integración (`tests/test_api.py`, 11 tests) que cubren:
catálogo, detalle de producto, ofertas, checkout (éxito, stock insuficiente, detalle
de pedido), chat, clientes y el configurador "Arma tu PC" (casos compatible e
incompatible). **Resultado: 11/11 OK.**
