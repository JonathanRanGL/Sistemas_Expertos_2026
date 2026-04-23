# Sistema Experto Automotriz

Proyecto académico de sistema experto orientado a diagnóstico y mantenimiento automotriz.

## Qué es
Es una aplicación en Python que implementa un sistema experto basado en reglas de producción para el dominio automotriz.

## Para qué sirve
Sirve para apoyar el diagnóstico de fallas en vehículos:
- procesa datos de sensores y contexto del vehículo,
- aplica reglas de conocimiento técnico,
- entrega hipótesis con nivel de certeza,
- explica por qué y cómo llegó a cada conclusión.

## Cómo funciona
1. Adquisición de conocimiento: se capturan reglas desde un experto automotriz.
2. Representación del conocimiento: reglas y hechos se estructuran en memoria.
3. Tratamiento del conocimiento: el motor de inferencia evalúa reglas con forward chaining.
4. Utilización del conocimiento: la interfaz de consola muestra resultados y explicaciones.

## Estructura del proyecto
- 01_adquisicion: captura y validación de reglas
- 02_representacion: base de conocimiento y base de hechos
- 03_tratamiento: inferencia y explicaciones
- 04_utilizacion: interfaz de usuario
- diagnostico_automotriz.py: ejecución integrada del sistema

## Ejecución
Desde la raíz del proyecto:

```powershell
python diagnostico_automotriz.py
```

## Nota
El sistema corre en modo demostración con datos simulados para mostrar el flujo completo de diagnóstico automotriz.
