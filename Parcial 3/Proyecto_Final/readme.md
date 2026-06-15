# Tienda Inteligente

Sistema experto de venta de componentes de PC construido con FastAPI, SQLite y una arquitectura de tres agentes inteligentes. El sistema integra un motor de inferencias basado en reglas IF-THEN con IA generativa (Gemini) para atención al cliente, validación de compatibilidad de hardware y gestión de pedidos.

El proyecto demuestra los principios centrales de la ingeniería del conocimiento: representación del conocimiento en reglas declarativas, encadenamiento hacia adelante (forward chaining), explicabilidad de decisiones y colaboración entre agentes especializados.

---

## Arquitectura del sistema

```
Usuario (navegador)
        |
        v
  Frontend estático
  (HTML / CSS / JS)
        |
        v
  FastAPI  (puerto 8080)
        |
   _____|_______________________________
  |             |             |         |
  v             v             v         v
Agente 1    Agente 2      Agente 3   Motor de
Atención    Generador     Supervisor inferencias
al cliente  de pedidos    Explicador
  |             |             |         |
  v             v             v         v
              SQLite  <-----------  reglas_inferencia
              tienda.db
```

**Agente 1 — Atención al cliente** (`agent1_customer.py`): Recibe mensajes del usuario, detecta la categoría o marca consultada y genera una respuesta. Delega a Gemini API cuando hay una clave configurada; en caso contrario responde con el motor de reglas del propio agente.

**Agente 2 — Generador de pedidos** (`agent2_order.py`): Recibe el carrito desde el frontend, valida stock, invoca el motor de inferencias para calcular descuentos y envío gratis, y persiste el pedido en la base de datos.

**Agente 3 — Supervisor / Explicador** (`agent3_supervisor.py`): Genera la explicación en lenguaje natural del pedido: qué reglas se dispararon, qué descuentos se aplicaron y cuál es el total final. Su salida se guarda en el campo `notas_agente` de cada pedido.

El motor de inferencias (`InferenceEngine`) evalúa un conjunto de reglas IF-THEN sobre el contexto del pedido (cliente, items, subtotal, especificaciones de los componentes) y devuelve descuentos, advertencias, recomendaciones y la lista de reglas disparadas.

---

## Características principales

- Catálogo de **47 productos** reales distribuidos en 8 categorías: GPU, CPU, RAM, SSD, Motherboard, Fuente, Cooler y Gabinete.
- Configurador **Arma tu PC** en 8 pasos con validación automática de compatibilidad de socket (AM5 / LGA1700) y suficiencia de la fuente de poder (TDP total vs. wattage).
- Sistema de **ofertas**: productos con `precio_original` mayor al precio actual aparecen en la sección de deals con el porcentaje de descuento calculado.
- **Carrito** con cálculo de envío y aplicación automática de descuentos según reglas de inferencia.
- **Chat con IA**: usa `gemini-2.5-flash-lite` con memoria de conversación y contexto del catálogo; si la API key no está configurada o la cuota se agota, el `CustomerAgent` basado en reglas responde automáticamente.
- **Motor de inferencias** con 9 reglas de negocio (ver sección dedicada más adelante).

---

## Stack tecnológico

| Capa | Tecnología | Version minima |
|------|-----------|----------------|
| Backend | Python + FastAPI | fastapi >= 0.115.0 |
| Servidor ASGI | Uvicorn | uvicorn[standard] >= 0.30.0 |
| Validacion | Pydantic | >= 2.9.0 |
| Base de datos | SQLite (aiosqlite) | aiosqlite >= 0.20.0 |
| IA generativa | Google Gemini (google-genai) | >= 1.0.0 |
| Variables de entorno | python-dotenv | >= 1.0.1 |
| Cliente HTTP | httpx | >= 0.27.0 |
| Frontend | HTML5 / CSS3 / JavaScript vanilla | — |

El modelo de Gemini configurado en produccion es `gemini-2.5-flash-lite` (definido en `backend/api/chat.py`).

---

## Estructura del proyecto

```
Proyecto_Final/
├── .env                        # Variables de entorno (no versionado)
├── .env.example                # Plantilla de configuracion
├── requirements.txt
├── backend/
│   ├── main.py                 # Punto de entrada FastAPI; registra todos los routers
│   ├── agents/
│   │   ├── agent1_customer.py  # Agente 1: respuesta al cliente basada en reglas
│   │   ├── agent2_order.py     # Agente 2: creacion y validacion de pedidos
│   │   └── agent3_supervisor.py# Agente 3: explicacion del pedido en lenguaje natural
│   ├── api/
│   │   ├── products.py         # Endpoints del catalogo
│   │   ├── orders.py           # Endpoint de checkout y consulta de pedidos
│   │   ├── chat.py             # Endpoint de chat (Gemini + fallback)
│   │   ├── pc_expert.py        # Endpoint del configurador Arma tu PC
│   │   ├── clients.py          # CRUD de clientes
│   │   └── admin.py            # Endpoint de reset para demos
│   ├── core/
│   │   └── inference_engine.py # Motor de inferencias IF-THEN
│   └── db/
│       ├── database.py         # Conexion SQLite y helpers query/execute
│       └── models.py           # Esquema de tablas y creacion de indices
├── frontend/
│   ├── index.html              # Pagina principal
│   ├── catalog.html            # Catalogo con filtros
│   ├── armatupc.html           # Configurador de 8 pasos
│   ├── checkout.html           # Carrito y checkout
│   ├── chat.html               # Chat con IA
│   ├── ofertas.html            # Productos en oferta
│   ├── soporte.html            # Pagina de soporte
│   └── assets/
│       └── products/           # 47 imagenes de productos (1.png ... 47.png)
├── scripts/
│   ├── init_db.py              # Crea las tablas del esquema
│   ├── seed_db.py              # Carga 47 productos, 3 clientes y 7 reglas
│   └── reset_db.py             # Restaura el estado inicial para demostraciones
├── docs/
│   └── architecture.md
├── tests/
│   └── test_api.py
└── assets/
    └── 7E_23110179_prototipoSE.pdf
```

---

## Requisitos previos

- Python 3.10 o superior
- pip
- API key de Google Gemini (gratuita en https://aistudio.google.com/app/apikey)

La API key es opcional: el sistema responde con el motor de reglas integrado si no esta configurada.

---

## Instalacion y configuracion (Windows / PowerShell)

**1. Posicionarse en el directorio del proyecto**

```powershell
cd "Proyecto_Final"
```

**2. Crear y activar el entorno virtual**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

**3. Instalar dependencias**

```powershell
pip install -r requirements.txt
```

Todos los paquetes de `requirements.txt` disponen de wheels precompilados para Windows, por lo que no se requiere compilador de C.

**4. Configurar variables de entorno**

```powershell
Copy-Item .env.example .env
```

Abrir `.env` y reemplazar `your_api_key_here` con la clave de Gemini:

```
GEMINI_API_KEY=AIza...
```

**5. Inicializar la base de datos**

```powershell
python scripts/init_db.py
python scripts/seed_db.py
```

`seed_db.py` carga: **47 productos**, **3 clientes** de prueba y **7 reglas de inferencia** en la tabla `reglas_inferencia`.

---

## Ejecucion

**Levantar el backend:**

```powershell
python -m uvicorn backend.main:app --reload --port 8080
```

**Abrir el frontend:** abrir `frontend/index.html` directamente en el navegador.

**Verificar que el backend responde:**

- Pagina de documentacion interactiva: http://127.0.0.1:8080/docs
- Health check: http://127.0.0.1:8080/health

---

## Reinicio de datos de demostracion

Para restaurar el catalogo al estado original (stock completo, sin pedidos de prueba, contadores de ID reiniciados) hay dos formas equivalentes:

**Por linea de comandos:**

```powershell
python scripts/reset_db.py
```

**Por endpoint HTTP (mientras el servidor esta corriendo):**

```
POST http://127.0.0.1:8080/api/admin/reset
```

Ambas opciones restauran el stock original de los 47 productos, eliminan todos los pedidos y lineas de detalle, reinician los contadores AUTOINCREMENT de SQLite y devuelven los 3 clientes a sus valores iniciales del seed.

---

## Motor de inferencias y reglas

El `InferenceEngine` evalua 9 reglas sobre el contexto de cada operacion. Siete de ellas estan ademas registradas en la tabla `reglas_inferencia` de la base de datos (para trazabilidad y auditoria); las dos restantes se evaluan exclusivamente en codigo.

| Nombre | Condicion | Accion |
|--------|-----------|--------|
| `descuento_cliente_frecuente` | `cliente.total_compras > 5` | Aplica 10% de descuento sobre el subtotal |
| `descuento_cliente_vip` | `cliente.total_gastado > 100 000` | Aplica 20% de descuento (toma el mayor entre ambos descuentos) |
| `envio_gratis_por_monto` | `subtotal > 50 000` | Activa envio gratis |
| `alerta_stock_bajo` | `cantidad_solicitada > stock_disponible` | Genera advertencia; bloquea el pedido si algun item esta agotado |
| `sugerir_reabastecimiento` | `stock_producto < 3` | Agrega recomendacion de reabastecimiento al resultado |
| `incompatibilidad_socket` | `cpu.socket != motherboard.socket` | Bloquea el pedido / configuracion y explica la incompatibilidad |
| `psu_insuficiente` | `total_tdp > psu_wattage * 0.8` | Genera advertencia sobre la fuente de poder |
| `configuracion_balanceada` | `0.8 <= gpu_precio / cpu_precio <= 1.2` | Agrega recomendacion de configuracion balanceada |
| `presupuesto_excedido` | `subtotal > 150 000` | Genera advertencia de presupuesto alto |

Las reglas `sugerir_reabastecimiento` y `presupuesto_excedido` se evaluan en el motor pero no tienen entrada en la tabla `reglas_inferencia` del seed actual.

---

## Endpoints principales de la API

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | `/api/products` | Lista el catalogo; soporta `q`, `category`, `brand`, `max_price` como parametros opcionales |
| GET | `/api/products/deals` | Productos con descuento activo (`precio_original > precio`), ordenados por porcentaje de descuento |
| GET | `/api/products/{id}` | Detalle de un producto por ID |
| POST | `/api/orders/checkout` | Procesa el carrito: valida stock, aplica inferencias, persiste el pedido; devuelve resumen + explicacion del Agente 3 |
| GET | `/api/orders/{id}` | Consulta un pedido con sus lineas de detalle y la explicacion del Agente 3 |
| POST | `/api/chat` | Envia un mensaje al Agente 1; acepta historial de conversacion para mantener contexto |
| POST | `/api/pc-expert/validate` | Valida la configuracion del configurador Arma tu PC (socket, PSU, stock) |
| GET | `/api/clients` | Lista todos los clientes registrados |
| GET | `/api/clients/{id}` | Detalle de un cliente |
| POST | `/api/clients` | Registra un nuevo cliente |
| POST | `/api/admin/reset` | Reinicia stock, pedidos y clientes al estado del seed (uso en demos) |
| GET | `/` | Estado general del sistema (version, agentes activos) |
| GET | `/health` | Health check |

La documentacion interactiva completa (Swagger UI) esta disponible en `/docs` mientras el servidor esta corriendo.

---

## Notas sobre el chat con IA

El endpoint `POST /api/chat` implementa una estrategia de degradacion elegante:

1. Si `GEMINI_API_KEY` esta configurada, el mensaje se envia a `gemini-2.5-flash-lite` con un `system_instruction` que incluye el rol del agente, el resumen del catalogo actual y hasta 8 productos relevantes filtrados por categoria y marca mencionadas en el mensaje. El historial de conversacion se pasa completo para mantener el contexto.

2. Si la clave no esta configurada, la cuota de Gemini se ha agotado, o la llamada falla por cualquier razon, el sistema responde automaticamente usando el `CustomerAgent` basado en reglas (`agent1_customer.py`). Este agente detecta palabras clave del mensaje, consulta la base de datos y genera una respuesta estructurada.

El chat **nunca deja de responder**: el mecanismo de respaldo garantiza disponibilidad aunque no haya acceso a la API de Gemini.

---

## Solucion de problemas comunes

**Error al instalar dependencias en Windows**

Si aparece `error: linker 'link.exe' not found` durante `pip install`, significa que pip esta intentando compilar un paquete desde codigo fuente. Esto no deberia ocurrir con las versiones especificadas en `requirements.txt`, que tienen wheels precompilados para Windows. Verificar que pip este actualizado:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Puerto 8080 ocupado**

```powershell
# Ver que proceso usa el puerto
netstat -ano | findstr :8080

# Terminar el proceso (reemplazar PID con el numero obtenido)
taskkill /PID <PID> /F
```

Alternativamente, iniciar uvicorn en otro puerto:

```powershell
python -m uvicorn backend.main:app --reload --port 8090
```

**El chat responde con mensajes genericos o de respaldo**

Esto indica que Gemini no esta disponible (cuota agotada, clave incorrecta o ausente). El sistema sigue funcionando: el `CustomerAgent` interno responde con informacion del catalogo. Para restaurar Gemini, verificar que `GEMINI_API_KEY` en `.env` sea valida y que la cuenta no haya excedido la cuota gratuita diaria.

**La base de datos no existe al iniciar el servidor**

El servidor arranca sin error pero las consultas fallaran. Ejecutar los scripts en orden:

```powershell
python scripts/init_db.py
python scripts/seed_db.py
```

---

## Pruebas

```powershell
python -m unittest tests.test_api -v
```

---

## Contexto academico

Proyecto academico — Materia: Sistemas Expertos, 2026.
