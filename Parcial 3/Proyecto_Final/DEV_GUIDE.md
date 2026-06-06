# Guía rápida para desarrolladores

## Configuración inicial

```bash
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno (Windows)
venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar .env
cp .env.example .env
# Luego editar .env y añadir tu GEMINI_API_KEY
```

## Inicializar base de datos

```bash
# 1. Crear tablas
python scripts/init_db.py

# 2. Cargar datos de prueba
python scripts/seed_db.py
```

## Ejecutar el servidor

```bash
uvicorn backend.main:app --reload
```

Luego abre `frontend/index.html` en el navegador.

## Estructura de desarrollo

```
Día 1-2: Base de datos
Día 3-5: Agentes inteligentes
Día 6: API endpoints
Día 7: Frontend
Día 8: Testing
Día 9: Documentación
```

## Archivos importantes

- `README.md` - Documentación del proyecto
- `COMMITS_PLAN.md` - Plan de commits diarios
- `docs/architecture.md` - Diagrama de arquitectura
- `backend/main.py` - Punto de entrada FastAPI
- `frontend/index.html` - Landing page

## Comandos útiles

```bash
# Ver estado del git
git status

# Ver commit log
git log --oneline

# Ver cambios
git diff

# Hacer commit
git commit -m "mensaje descriptivo"

# Subir cambios
git push origin main
```

¡Buena suerte! 🚀
