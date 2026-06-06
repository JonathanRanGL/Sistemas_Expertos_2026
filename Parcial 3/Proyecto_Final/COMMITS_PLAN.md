# 📋 PLAN DE COMMITS — Tienda Inteligente

## Cronograma de Desarrollo (9 días)

Este archivo contiene el plan de commits detallados para cada día del desarrollo del proyecto.

### ✅ DÍA 1 — HECHO: `init: scaffold base structure`

**Fecha:** 6 de Junio, 2026

**Descripción:** Estructura base del proyecto, configuración inicial y organización de carpetas.

**Commits del Día:**
```bash
git add .
git commit -m "init: scaffold base structure

- Crear estructura de carpetas (backend, frontend, scripts, docs)
- Añadir archivos __init__.py para los módulos
- Crear modelos de base de datos (models.py)
- Configurar conexión a SQLite (database.py)
- Crear archivos de agentes vacíos (agent1, agent2, agent3)
- Motor de inferencias (infrastructure_engine.py)
- Punto de entrada FastAPI (main.py)
- HTML landing page responsive
- requirements.txt con dependencias
- .env.example para configuración
- docs/architecture.md con diagrama de agentes
- README.md con instrucciones"
```

**Archivos Creados:**
- ✅ `backend/agents/` (agent1_customer.py, agent2_order.py, agent3_supervisor.py)
- ✅ `backend/db/` (database.py, models.py)
- ✅ `backend/core/` (inference_engine.py)
- ✅ `backend/api/` (vacío, estructura reservada)
- ✅ `backend/main.py`
- ✅ `frontend/` (index.html, catalog.html, chat.html)
- ✅ `scripts/` (init_db.py, seed_db.py)
- ✅ `docs/architecture.md`
- ✅ Archivos de configuración (.env.example, requirements.txt)

---

### 🔄 DÍA 2 — `feat: database initialization`

**Fecha:** 7 de Junio, 2026

**Descripción:** Completar scripts de inicialización y seeding de base de datos.

**Tareas:**
- [ ] Mejorar script `init_db.py` con validaciones
- [ ] Ejecutar y probar creación de tablas
- [ ] Completar `seed_db.py` con más datos realistas
- [ ] Crear tabla de historial de inferencias
- [ ] Crear índices y constraints
- [ ] Documentar schema de DB

**Commit:**
```
feat: database initialization and seeding

- Mejorar scripts de inicialización
- Añadir más productos de prueba (50+)
- Añadir clientes de prueba con historial
- Crear índices en DB para mejor performance
- Documentar schema SQLite
- Validar integridad referencial
```

---

### 🤖 DÍA 3 — `feat: Agent 1 - Customer Service`

**Fecha:** 8 de Junio, 2026

**Descripción:** Implementar Agente 1 - Atención al Cliente con LangChain + Gemini.

**Tareas:**
- [ ] Configurar LangChain y Google Gemini API
- [ ] Implementar clase CustomerAgent
- [ ] Crear método de detección de intención (NLU)
- [ ] Extracción de entidades (productos, cantidades, presupuesto)
- [ ] Consultas a BD para obtener información relevante
- [ ] Generación de respuestas con Gemini

**Commit:**
```
feat: Agent 1 - Customer Service

- Implementar CustomerAgent con LangChain
- Detector de intención (compra, consulta, soporte)
- Extractor de entidades usando LLM
- Consultas a BD (productos, clientes)
- Respuestas personalizadas con Gemini API
- Manejo de múltiples idiomas
- Tests básicos del agente
```

---

### 🧠 DÍA 4 — `feat: Agent 2 - Order Generation & Inference Engine`

**Fecha:** 9 de Junio, 2026

**Descripción:** Implementar Agente 2 y Motor de Inferencias.

**Tareas:**
- [ ] Implementar clase OrderAgent
- [ ] Crear motor de inferencias (InferenceEngine)
- [ ] Implementar 7-10 reglas IF-THEN
- [ ] Validar stock
- [ ] Detectar incompatibilidades
- [ ] Aplicar descuentos automáticos
- [ ] Generar pedidos en SQLite

**Commit:**
```
feat: Agent 2 - Order Generation & Inference Engine

- Implementar OrderAgent
- Crear InferenceEngine con reglas IF-THEN
- Regla: descuento_cliente_frecuente
- Regla: envio_gratis_por_monto
- Regla: alerta_stock_bajo
- Regla: incompatibilidad_socket
- Regla: psu_insuficiente
- Validación de compatibilidad
- Generación de pedidos en BD
- Registro de inferencias disparadas
```

---

### 📝 DÍA 5 — `feat: Agent 3 - Supervisor & Explainability`

**Fecha:** 10 de Junio, 2026

**Descripción:** Implementar Agente 3 - Supervisor y Explicabilidad.

**Tareas:**
- [ ] Implementar clase SupervisorAgent
- [ ] Generar resumen de venta
- [ ] Explicar decisiones tomadas
- [ ] Mostrar reglas disparadas
- [ ] Solicitar validación final
- [ ] Guardar explicaciones en BD

**Commit:**
```
feat: Agent 3 - Supervisor & Explainability

- Implementar SupervisorAgent
- Generar resumen ejecutivo de venta
- Explicar cada decisión tomada
- Mostrar reglas de inferencia disparadas
- Explicabilidad en lenguaje natural
- Solicitar confirmación del usuario
- Guardar notas de agente en pedidos
```

---

### 🔌 DÍA 6 — `feat: FastAPI endpoints`

**Fecha:** 11 de Junio, 2026

**Descripción:** Crear endpoints REST para conectar frontend con backend.

**Tareas:**
- [ ] Endpoint GET `/api/products` - listar productos
- [ ] Endpoint POST `/api/chat` - enviar mensaje al Agente 1
- [ ] Endpoint POST `/api/orders` - crear pedido
- [ ] Endpoint GET `/api/orders/{id}` - obtener pedido con explicaciones
- [ ] Middleware CORS
- [ ] Validación de Pydantic
- [ ] Manejo de errores

**Commit:**
```
feat: FastAPI endpoints

- Crear api/products.py - listar y filtrar productos
- Crear api/chat.py - endpoint chat con Agente 1
- Crear api/orders.py - generador de pedidos
- Crear api/clients.py - gestión de clientes
- Middleware CORS configurado
- Validación con Pydantic
- Manejo de excepciones
- Documentación automática Swagger
```

---

### 🎨 DÍA 7 — `feat: Frontend UI`

**Fecha:** 12 de Junio, 2026

**Descripción:** Mejorar y completar la interfaz web.

**Tareas:**
- [ ] Conectar catálogo HTML con API
- [ ] Implementar chat funcional con WebSocket/HTTP
- [ ] Carrito de compras (localStorage)
- [ ] Formulario de checkout
- [ ] Mostrar explicaciones del sistema
- [ ] Responsive design completo

**Commit:**
```
feat: Frontend UI - Product Catalog & Chat

- Cargar productos dinámicamente desde API
- Filtros funcionales (categoría, marca, precio)
- Carrito de compras con localStorage
- Chat en tiempo real con Agente 1
- Mostrar explicaciones y reglas disparadas
- Checkout funcional
- Responsive design (móvil, tablet, desktop)
```

---

### 🐛 DÍA 8 — `fix: Integration & Testing`

**Fecha:** 13 de Junio, 2026

**Descripción:** Pruebas, integración y corrección de bugs.

**Tareas:**
- [ ] Tests unitarios
- [ ] Tests de integración
- [ ] Validar flujo completo usuario-sistema
- [ ] Performance testing
- [ ] Corrección de bugs encontrados
- [ ] Documentación de API

**Commit:**
```
fix: Integration Testing & Bug Fixes

- Tests unitarios para agentes
- Tests de integración BD-API-Frontend
- Validar flujo completo de venta
- Performance optimization
- Corrección de bugs encontrados
- Documentación de API (Swagger)
- README actualizado con instrucciones
```

---

### 📚 DÍA 9 — `docs: Final Documentation & PDF`

**Fecha:** 14 de Junio, 2026

**Descripción:** Documentación final, PDF y video.

**Tareas:**
- [ ] Crear PDF: GG_registro_Proy.pdf
- [ ] Incluir: portada, objetivo, descripción, arquitectura
- [ ] Documentar base de conocimiento y reglas
- [ ] Incluir capturas de pantalla
- [ ] Manual de usuario paso a paso
- [ ] Grabación y upload de video a YouTube
- [ ] README final actualizado

**Commit:**
```
docs: Final Documentation & Video

- GG_registro_Proy.pdf con:
  - Portada profesional
  - Objetivo del proyecto
  - Descripción del sistema
  - Arquitectura de agentes
  - Base de conocimiento (7-10 reglas)
  - Explicación técnica
  - Capturas de pantalla del sistema
  - Manual de usuario
  - Video demostrativo
- README.md con instrucciones finales
- Links a documentación y video
```

---

## 🎯 Checkpoints Diarios

Cada día deberás:

1. ✅ **Planificar:** Qué vas a hacer ese día
2. 🔨 **Implementar:** Escribir el código
3. 🧪 **Probar:** Verificar que funciona
4. 📝 **Documentar:** Actualizar README/comentarios
5. 🚀 **Commit:** Hacer commit con mensaje descriptivo
6. 📤 **Push:** Subir a GitHub

---

## 📊 Rúbricas de Evaluación

- **Funcionamiento de agentes (20%):** ¿Cumplen sus funciones?
- **Explicabilidad (20%):** ¿El sistema puede justificar decisiones?
- **GitHub commits (20%):** ¿Hay commits diarios?
- **Manual de usuario (20%):** ¿Es claro y reproducible?
- **Video demostrativo (20%):** ¿Muestra el sistema funcionando?

---

## 🚨 Recordatorios Importantes

- ⚠️ **NO hacer commits masivos el último día**
- ⚠️ **Commits diarios son OBLIGATORIOS** (2 puntos menos por día sin commits)
- ⚠️ **Todo debe estar en GitHub** (código, PDFs, enlaces a video)
- ⚠️ **El sistema debe funcionar en máquina local**
- ⚠️ **Estar preparado para explicar técnicamente todo**

---

**Fecha de inicio:** 6 de Junio, 2026
**Fecha de entrega:** 14 de Junio, 2026
**Duración total:** 9 días

¡Éxito en el proyecto! 🎉
