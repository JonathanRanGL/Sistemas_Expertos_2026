# Arquitectura — Tienda Inteligente

## Diagrama de flujo entre agentes

```
Usuario (Web)
    │
    ▼ mensaje de chat
┌─────────────────────┐
│     AGENTE 1        │  ← LangChain + Gemini API
│  Atención al        │
│     Cliente         │
│                     │
│ • Detecta intención │
│ • Extrae entidades  │
│ • Consulta BD       │
└────────┬────────────┘
         │ {intencion, productos, cliente_id}
         ▼
┌─────────────────────┐
│     AGENTE 2        │  ← Python + Motor de Inferencias
│  Generador de       │
│     Pedido          │
│                     │
│ • Valida stock      │  → IF stock < qty  THEN alerta
│ • Aplica reglas     │  → IF frecuente    THEN descuento
│ • Genera pedido     │  → IF total > 50k  THEN envío gratis
│ • Guarda en SQLite  │
└────────┬────────────┘
         │ {pedido, inferencias_disparadas}
         ▼
┌─────────────────────┐
│     AGENTE 3        │  ← LangChain + Gemini API
│    Supervisor /     │
│    Explicador       │
│                     │
│ • Resume la venta   │
│ • Explica decisiones│
│ • Lista inferencias │
│ • Pide confirmación │
└────────┬────────────┘
         │ respuesta final + explicación
         ▼
    Usuario (Web)
```

## Base de Datos

```
productos ──────────────────────┐
clientes ──────────────── pedidos ── detalle_pedido
reglas_inferencia               │
                                └── (inferencias JSON en pedidos.inferencias)
```

## Tecnologías

| Capa | Tecnología |
|------|-----------|
| Frontend | HTML/CSS/JS |
| API | FastAPI (Python) |
| Agentes | LangChain + Google Gemini 1.5 Flash |
| Base de datos | SQLite |
| Motor de inferencias | Python puro (reglas IF-THEN) |
