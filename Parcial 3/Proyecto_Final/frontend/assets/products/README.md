# Imágenes de Productos

Carpeta para las imágenes del catálogo de la Tienda Inteligente.

## Convención de nombres

Cada imagen se llama `{producto_id}.png`, donde `{producto_id}` es el ID
numérico del producto en la base de datos (campo `id` de la tabla `productos`).

Ejemplos:
- `1.png`  → NVIDIA RTX 4090 (id=1)
- `2.png`  → AMD Radeon RX 7900 XTX (id=2)
- `47.png` → Corsair 4000D Airflow (id=47)

## Rango actual de IDs

La base de datos tiene productos con IDs del 1 al 47. Los 47 archivos están
presentes en esta carpeta.

## Origen

Los archivos originales en `img_productos/` siguen la convención
`{categoria}_{marca}_{modelo}.png`. Al copiarlos aquí se renombran a
`{producto_id}.png` según el mapeo establecido en la sesión de setup.

## Fallback

Si la imagen de un producto no existe, el frontend muestra automáticamente
un ícono genérico (📦 en catalog.html, 🔥 en ofertas.html) sin romper el layout.
