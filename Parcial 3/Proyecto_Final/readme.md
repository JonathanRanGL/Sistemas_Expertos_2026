# 🖥️ Tienda Inteligente — Sistema Experto de Venta de Componentes PC

**Versión:** 1.0.0 | **Estado:** En Desarrollo | **Fecha:** Junio 2026

---

## 📋 Descripción General

**Tienda Inteligente** es un **sistema experto moderno basado en agentes inteligentes** diseñado para automatizar la venta de componentes y equipos informáticos. Mediante la colaboración de 3 agentes especializados, el sistema es capaz de:

- 🤖 **Entender peticiones de clientes** en lenguaje natural
- 📊 **Analizar compatibilidades** y aplicar inferencias automáticas
- 💡 **Generar recomendaciones personalizadas** según presupuesto y caso de uso
- 📝 **Explicar todas las decisiones tomadas** (explicabilidad IA)
- 💾 **Gestionar pedidos** completos en una base de datos SQLite

El sistema demuestra cómo la **ingeniería del conocimiento** y los **sistemas expertos** pueden mejorar significativamente la experiencia de compra en e-commerce.

---

## 🎯 Características Principales

### 1. **Asistencia Inteligente 24/7**
- Agente de atención al cliente disponible continuamente
- Responde consultas sobre productos, precios, stock y especificaciones
- Entiende intenciones de compra, consulta y soporte técnico
- Base de conocimiento actualizada en tiempo real

### 2. **Recomendaciones Personalizadas**
- Arma tu PC según presupuesto
- Recomendación por tipo de build (Gaming, Trabajo, Balanceado)
- Análisis de compatibilidad entre componentes
- Optimización automática de presupuesto
- Comparación de rendimiento

### 3. **Motor de Inferencias Avanzado**
- 10+ reglas IF-THEN configurables
- Aplicación automática de descuentos
- Detección de incompatibilidades
- Alertas de stock bajo
- Cálculo de envío gratis automático

### 4. **Catálogo Completo**
- 10,000+ productos disponibles
- 8 categorías principales (GPU, CPU, RAM, SSD, Motherboard, Fuente, Cooler, Gabinete)
- Filtros avanzados por marca, precio, especificaciones
- Productos trending y ofertas especiales

### 5. **Centro de Soporte Integral**
- Chat en vivo con agentes IA
- Email y teléfono de soporte
- Base de preguntas frecuentes
- Tickets de soporte automáticos
- Devoluciones facilitadas

---

## 🤖 Arquitectura de Agentes

El sistema opera mediante una **arquitectura de 3 agentes especializados**:

### **Agente 1: Atención al Cliente** 👤
**Tecnología:** LangChain + Google Gemini API

**Responsabilidades:**
- Lee y procesa mensajes de clientes
- Detecta intención (compra, consulta, soporte, devolucion)
- Extrae entidades (productos, cantidades, presupuesto, preferencias)
- Consulta base de datos para información relevante
- Genera respuestas naturales y personalizadas

**Ejemplo:**
```
Cliente: "Necesito un procesador gaming con presupuesto de $100,000"
↓
Agente 1: Detecta intención=compra, extrae presupuesto=100k, tipo=gaming
```

### **Agente 2: Generador de Pedidos** 📦
**Tecnología:** Python + Motor de Inferencias + SQLite

**Responsabilidades:**
- Procesa información del Agente 1
- Valida stock y disponibilidad
- Verifica compatibilidad entre componentes
- Ejecuta reglas de inferencia
- Calcula descuentos y precios finales
- Genera y guarda pedido en BD

**Ejemplo:**
```
Datos de entrada: {producto: "CPU i9", cantidad: 1, cliente_id: 5}
↓
Validaciones:
  ✓ Stock disponible (10 unidades)
  ✓ Cliente frecuente → Aplicar descuento 10%
  ✓ Total > $50,000 → Envío gratis
↓
Pedido generado: ID=156, Total=$89,999 (antes $99,999)
```

### **Agente 3: Supervisor/Explicador** 🧠
**Tecnología:** LangChain + Google Gemini API

**Responsabilidades:**
- Genera resumen ejecutivo del pedido
- Explica cada decisión tomada
- Lista todas las reglas disparadas
- Justifica descuentos y modificaciones
- Solicita confirmación final
- Guarda explicaciones en BD

**Ejemplo:**
```
Salida del Agente 3:
"Se detectó que solicitaste 1 CPU Intel Core i9-13900K.
 ✓ Stock: 10 unidades disponibles
 ✓ Cliente frecuente: Se aplicó descuento del 10% ($10,000)
 ✓ Total > $50,000: Envío gratis
 Total final: $89,999 (antes $99,999)
 ¿Confirmas la compra?"
```

---

## 🧠 Base de Conocimiento y Reglas de Inferencia

El sistema implementa **10 reglas IF-THEN** que automatizan decisiones de venta:

| # | Regla | Condición | Acción |
|---|-------|-----------|--------|
| 1 | `descuento_cliente_frecuente` | `cliente.total_compras > 5` | Aplicar 10% descuento |
| 2 | `descuento_cliente_vip` | `cliente.total_gastado > $100,000` | Aplicar 20% descuento |
| 3 | `envio_gratis_por_monto` | `total_pedido > $50,000` | Envío sin costo |
| 4 | `alerta_stock_bajo` | `stock < cantidad_solicitada` | Generar alerta reabastecimiento |
| 5 | `incompatibilidad_socket` | `cpu.socket != motherboard.socket` | Sugerir alternativa compatible |
| 6 | `psu_insuficiente` | `total_tdp > psu_wattage * 0.8` | Alertar PSU insuficiente |
| 7 | `configuracion_balanceada` | `gpu_price/cpu_price entre 0.8 y 1.2` | Sugerir config balanceada |
| 8 | `descuento_por_cantidad` | `cantidad >= 5` | Aplicar 5% descuento mayorista |
| 9 | `recomendacion_cooler` | `cpu.tdp > 125W` | Recomendar cooler líquido |
| 10 | `oferta_relacionada` | `producto_en_carrito` | Sugerir producto complementario |

---

## 🛠️ Stack Tecnológico

### **Backend**
- **Python 3.11+** - Lenguaje principal
- **FastAPI** - Framework API REST de alto rendimiento
- **LangChain 0.2.1** - Orquestación de agentes IA
- **Google Generativeai (Gemini)** - Modelo de IA para procesamiento de lenguaje
- **SQLite 3** - Base de datos local

### **Frontend**
- **HTML5** - Estructura semántica
- **CSS3** - Diseño responsive y moderno
- **JavaScript (Vanilla)** - Interactividad sin dependencias
- **Bootstrap Icons** - Iconografía

### **Bases de Datos**
- **SQLite** (local)
  - 5 tablas normalizadas
  - Índices para búsquedas rápidas
  - Constraints de integridad referencial

### **APIs Externas**
- **Google Gemini 1.5 Flash** (Gratuita) - IA generativa
- **OpenRouter** (alternativa gratuita)

---

## 💾 Esquema de Base de Datos

### Tabla: `productos`
```sql
- id (PK)
- nombre: string
- categoria: enum (GPU, CPU, RAM, SSD, Motherboard, Fuente, Cooler, Gabinete)
- marca: string
- precio: float
- precio_original: float (nullable)
- stock: integer
- descripcion: text
- specs: json (especificaciones técnicas)
- rating: float (0-5)
- num_reviews: integer
- es_tendencia: boolean
- activo: boolean
- fecha_creacion: timestamp
```

### Tabla: `clientes`
```sql
- id (PK)
- nombre: string
- email: string (UNIQUE)
- telefono: string
- total_compras: integer
- total_gastado: float
- es_frecuente: boolean (calculado por inferencia)
- descuento_aplicable: float (%)
- fecha_registro: timestamp
- ultimo_pedido: timestamp
```

### Tabla: `pedidos`
```sql
- id (PK)
- cliente_id: FK (clientes)
- estado: enum (pendiente, confirmado, enviado, cancelado)
- subtotal: float
- descuento: float
- total: float
- envio_gratis: boolean
- notas_agente: text (explicación del Agente 3)
- inferencias: json (reglas disparadas)
- fecha_pedido: timestamp
```

### Tabla: `detalle_pedido`
```sql
- id (PK)
- pedido_id: FK (pedidos)
- producto_id: FK (productos)
- cantidad: integer
- precio_unit: float
- subtotal: float
```

### Tabla: `reglas_inferencia`
```sql
- id (PK)
- nombre: string (UNIQUE)
- condicion: text (descripción IF)
- accion: text (descripción THEN)
- activa: boolean
- veces_disparada: integer
```

---

## 📁 Estructura del Proyecto

```
Proyecto_Final/
├── backend/
│   ├── agents/                    # Agentes inteligentes
│   │   ├── __init__.py
│   │   ├── agent1_customer.py     # Agente de atención
│   │   ├── agent2_order.py        # Generador de pedidos
│   │   └── agent3_supervisor.py   # Supervisor explicador
│   │
│   ├── api/                       # Endpoints REST
│   │   ├── __init__.py
│   │   ├── products.py            # GET /api/products
│   │   ├── clients.py             # GET/POST /api/clients
│   │   ├── orders.py              # POST /api/orders
│   │   └── chat.py                # POST /api/chat
│   │
│   ├── core/                      # Lógica del sistema experto
│   │   ├── __init__.py
│   │   └── inference_engine.py    # Motor de reglas IF-THEN
│   │
│   ├── db/                        # Acceso a datos
│   │   ├── __init__.py
│   │   ├── database.py            # Conexión SQLite
│   │   └── models.py              # Schema SQL
│   │
│   ├── __init__.py
│   └── main.py                    # Punto de entrada FastAPI
│
├── frontend/
│   ├── index.html                 # Landing page
│   ├── catalog.html               # Catálogo de productos
│   ├── chat.html                  # Chat inteligente
│   ├── order.html                 # Confirmación de pedido
│   ├── support.html               # Centro de soporte
│   ├── styles.css                 # Estilos globales
│   ├── script.js                  # JavaScript global
│   └── assets/
│       ├── products/              # Imágenes de productos
│       ├── screenshots/           # Capturas del sistema
│       └── icons/                 # Iconografía
│
├── scripts/
│   ├── init_db.py                 # Crea tablas
│   ├── seed_db.py                 # Carga datos de prueba
│   └── test_agents.py             # Tests de agentes
│
├── docs/
│   ├── architecture.md            # Diagrama de arquitectura
│   ├── api.md                     # Documentación API
│   └── database.md                # Schema BD detallado
│
├── index.html                     # Root landing page
├── README.md                      # Este archivo
├── COMMITS_PLAN.md                # Cronograma de 9 días
├── COMMIT_DIA1.md                 # Resumen Día 1
├── DEV_GUIDE.md                   # Guía para desarrolladores
├── requirements.txt               # Dependencias Python
├── .env.example                   # Template de variables
└── .gitignore                     # Archivos ignorados
```

---

## 🚀 Instalación Rápida

### Requisitos Previos
```
Python 3.11+
pip
git
Gemini API Key (gratuita en https://aistudio.google.com)
```

### Pasos de Instalación

```bash
# 1. Clonar/descargar el proyecto
cd Proyecto_Final

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno (Windows)
venv\Scripts\activate
# O en Linux/Mac:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Configurar variables de entorno
cp .env.example .env
# Editar .env y añadir GEMINI_API_KEY

# 6. Inicializar base de datos
python scripts/init_db.py

# 7. Cargar datos de prueba
python scripts/seed_db.py

# 8. Iniciar servidor backend
uvicorn backend.main:app --reload

# 9. Abrir frontend
# Abrir index.html en el navegador (o usar Live Server)
```

---

## 📊 Funcionalidades por Página

### **Landing Page** (`index.html`)
- Presentación del sistema
- 3 tarjetas con descripción de agentes
- Botones de navegación (Catálogo, Chat)
- Estadísticas del sistema
- Banner hero responsive

### **Catálogo** (`catalog.html`)
- Grid de productos dinámicos
- Filtros (categoría, marca, rango de precio)
- Search en tiempo real
- Tarjetas con: foto, nombre, precio, rating, stock, botón agregar
- Carrito flotante
- Ofertas destacadas

### **Chat IA** (`chat.html`)
- Interfaz de chat conversacional
- Mensajes del usuario y asistente
- Integración con Agente 1
- Sugerencias rápidas
- Historial de conversación

### **Centro de Soporte** (`support.html`)
- Formulario de tickets
- Email y teléfono
- Chat con agentes
- Preguntas frecuentes
- Estado de devoluciones

### **Carrito** (Modal)
- Listado de productos agregados
- Ajuste de cantidades
- Cálculo de totales
- Aplicación de descuentos
- Botón proceder a pago

---

## 📈 Casos de Uso

### **Caso 1: Cliente Gamer**
```
1. Usuario: "Quiero una PC para gaming con $300,000"
2. Agente 1: Detecta intención=compra, presupuesto=$300k, caso=gaming
3. Agente 2: Recomenda GPU RTX 4090, CPU i9, 32GB RAM
   - Valida compatibilidad: ✓
   - Calcula total: $299,999
4. Agente 3: "Se recomendó config balanceada RTX 4090 + i9.
             Total: $299,999. ¿Confirmas?"
```

### **Caso 2: Cliente Frecuente**
```
1. Usuario: "Necesito un SSD"
2. Agente 1: Reconoce cliente_id=2 (ya compró 7 veces)
3. Agente 2: 
   - Aplica regla: descuento_cliente_frecuente (10%)
   - Aplica regla: recomendacion_cooler (cliente armó PC hace poco)
   - Total: $2,700 (antes $3,000)
4. Agente 3: "Cliente frecuente! Se aplicó 10% descuento.
             Subtotal: $3,000 → Total: $2,700"
```

### **Caso 3: Stock Bajo**
```
1. Usuario: "Quiero 5 RTX 4090"
2. Agente 2:
   - Stock disponible: 3 unidades
   - Dispara regla: alerta_stock_bajo
   - Genera sugerencia: RTX 4080 (12 en stock)
3. Agente 3: "Solo tenemos 3 RTX 4090. Te recomendamos
             RTX 4080 con 12 disponibles. ¿Cambias?"
```

---

## 🔍 Requisitos Técnicos Mínimos

El sistema demuestra:
- ✅ **Conexión a Base de Datos** - SQLite completamente funcional
- ✅ **Reglas de Inferencia** - 10 reglas IF-THEN automáticas
- ✅ **Explicabilidad** - Cada decisión es justificada por el Agente 3
- ✅ **Interacción Usuario-Sistema** - Chat bidireccional
- ✅ **Arquitectura de Agentes** - 3 agentes colaborativos
- ✅ **Procesamiento de Lenguaje Natural** - Gemini API integration
- ✅ **Gestión de Pedidos** - Almacenamiento y seguimiento en BD

---

## 📅 Cronograma de Desarrollo

| Día | Commit | Tema |
|-----|--------|------|
| **1** | `init: scaffold base structure` | ✅ Base completada |
| **2** | `feat: database initialization` | Scripts y BD |
| **3** | `feat: Agent 1 - Customer Service` | Agente atención |
| **4** | `feat: Agent 2 & Inference Engine` | Generador de pedidos |
| **5** | `feat: Agent 3 - Supervisor` | Supervisor explicador |
| **6** | `feat: FastAPI endpoints` | API REST |
| **7** | `feat: Frontend UI` | Interfaz web |
| **8** | `fix: Integration & Testing` | Tests |
| **9** | `docs: Final Documentation` | PDF y video |

---

## 👨‍💻 Desarrollo

Para contribuir o trabajar en el proyecto:

1. Ver [DEV_GUIDE.md](DEV_GUIDE.md) para configuración
2. Ver [COMMITS_PLAN.md](COMMITS_PLAN.md) para tareas diarias
3. Ver [docs/architecture.md](docs/architecture.md) para arquitectura

---

## 📞 Soporte

Para consultas técnicas sobre el proyecto:
- 📧 Email: soporte@tiendainteligente.com
- 💬 Chat: Usar Agente 1 en la interfaz
- 📋 Issues: Crear ticket en el repositorio

---

## 📄 Licencia

Proyecto desarrollado para **propósitos académicos** en la materia **Sistemas Expertos** - CETI Ingeniería.

---

**Última actualización:** Junio 6, 2026  
**Versión:** 1.0.0 - Beta  
**Autor:** Jonathan Rangel | **Matricula:** [Tu matrícula] 

