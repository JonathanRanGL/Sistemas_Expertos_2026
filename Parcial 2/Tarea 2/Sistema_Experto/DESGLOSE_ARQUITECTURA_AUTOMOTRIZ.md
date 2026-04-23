## Portada

**Materia:** Sistemas Expertos  
**Tema:** Desglose de la Arquitectura de un Sistema Experto Automotriz  
**Estudiante:** Kenya Gabriela Frutos Gonzalez  
**Fecha:** 23 de abril de 2026

---

# Desglose de la Arquitectura del Sistema Experto Automotriz

## Introducción
La arquitectura del sistema experto se organiza en cuatro fases principales:

1. Adquisición de conocimiento
2. Representación del conocimiento
3. Tratamiento del conocimiento
4. Utilización del conocimiento

Cada fase tiene componentes con una función específica. A continuación se explica cada elemento con el formato solicitado:
- Qué es
- Para qué sirve
- Cómo funciona

También se incluyen ejemplos prácticos orientados al diagnóstico automotriz implementado.

---

## 1) Adquisición de conocimiento

### 1.1 Experto automotriz
Qué es:
Es la persona especialista del dominio (por ejemplo, un ingeniero automotriz) que aporta conocimiento técnico sobre fallas de vehículos.

Para qué sirve:
Sirve para transformar conocimiento humano en reglas formales que el sistema pueda usar.

Cómo funciona:
El experto define reglas del tipo:
SI condición(es) ENTONCES conclusión con cierta certeza.

Ejemplo:
SI nivel_aceite < 20 Y temperatura_motor > 95 Y ruido_suspenso == True
ENTONCES Falla probable en junta de culata (certeza 0.97)

---

### 1.2 Cognimatic
Qué es:
Es una herramienta de elicitación de conocimiento. En el proyecto, se simula como módulo que ayuda a estructurar reglas.

Para qué sirve:
Sirve para guiar al experto en la captura ordenada y consistente de reglas.

Cómo funciona:
Presenta una estructura para registrar:
- variable
- operador
- valor
- conclusión
- certeza
Con esto genera reglas listas para integrar en la base de conocimiento.

Ejemplo:
Variable: nivel_aceite
Operador: <
Valor: 20
Conclusión: Inspeccionar fuga de aceite
Certeza: 0.98

---

### 1.3 Sensores/Fuentes de datos
Qué es:
Son fuentes automáticas de datos del vehículo (simulados en el proyecto).

Para qué sirve:
Sirven para alimentar la base de hechos con información en tiempo real del vehículo.

Cómo funciona:
Capturan o registran variables como nivel de aceite, temperatura del motor, fugas o indicadores de tablero.

Ejemplo:
- nivel_aceite: 12
- temperatura_motor: 110
- fugas_liquido: True

---

### 1.4 Base de datos automotriz
Qué es:
Es la fuente histórica de información del vehículo y su mantenimiento.

Para qué sirve:
Sirve para complementar los datos del sensor con contexto previo del vehículo.

Cómo funciona:
Se consulta por ID de vehículo para recuperar antecedentes, kilometraje y mantenimientos previos.

Ejemplo:
Vehículo V001:
- vehiculo: Toyota Hilux
- placa: ABC-1234
- historico_mantenimientos: [cambio_aceite, reparacion_radiador]

---

### 1.5 Módulo de adquisición de conocimiento
Qué es:
Es el filtro de calidad entre el conocimiento nuevo y el conocimiento existente.

Para qué sirve:
Sirve para validar reglas antes de incorporarlas:
- evita duplicados
- detecta conflictos
- registra trazabilidad de aceptación/rechazo

Cómo funciona:
Compara cada nueva regla con las ya registradas.
Si hay mismas condiciones y distinta conclusión, marca conflicto.

Ejemplo:
Regla existente:
SI humedad_refrigerante == True ENTONCES Posible fuga en el sistema de refrigeración
Regla nueva conflictiva:
SI humedad_refrigerante == True ENTONCES Sistema de frenos con fuga
Resultado: conflicto y rechazo.

---

## 2) Representación del conocimiento

### 2.1 Base de conocimiento
Qué es:
Es el repositorio permanente de reglas del sistema experto.

Para qué sirve:
Sirve para almacenar conocimiento automotriz de forma estable y reutilizable.

Cómo funciona:
Guarda reglas estructuradas con:
- id
- condiciones
- conclusión
- certeza
Estas reglas son consumidas por el motor de inferencia.

Ejemplo:
R004:
SI luz_check_engine == True Y vibracion_rpm == True
ENTONCES Sensor de motor o convertidor catalítico defectuoso (0.89)

---

### 2.2 Base de hechos
Qué es:
Es la memoria temporal del vehículo en revisión.

Para qué sirve:
Sirve para almacenar el estado del vehículo en tiempo real y compararlo con las reglas.

Cómo funciona:
Registra hechos como pares variable-valor y permite evaluar condiciones.
Se limpia al terminar la sesión.

Ejemplo:
Hechos del vehículo actual:
- nivel_aceite = 12
- temperatura_motor = 110
- fugas_liquido = True

---

## 3) Tratamiento del conocimiento

### 3.1 Motor de inferencia
Qué es:
Es el núcleo lógico del sistema experto.

Para qué sirve:
Sirve para derivar hipótesis a partir de:
- reglas (base de conocimiento)
- hechos (base de hechos)

Cómo funciona:
Usa encadenamiento hacia adelante (forward chaining):
1. toma los hechos conocidos
2. evalúa cada regla
3. dispara reglas cuyas condiciones se cumplen
4. genera conclusiones con su certeza

Ejemplo:
Si los hechos contienen:
- nivel_aceite < 20
- temperatura_motor > 95
- ruido_suspenso == True
Se dispara la regla de Falla probable en junta de culata.

---

### 3.2 Módulo de explicaciones
Qué es:
Es el componente que traduce el razonamiento técnico a lenguaje comprensible.

Para qué sirve:
Sirve para justificar resultados y generar confianza en el diagnóstico.

Cómo funciona:
Muestra:
- por qué se llegó a una conclusión
- qué datos se usaron
- qué reglas se activaron o no

Ejemplo:
Conclusión: Falla probable en junta de culata
Explicación: nivel_aceite bajo, temperatura de motor alta y ruido sospechoso se cumplieron.

---

## 4) Utilización del conocimiento

### 4.1 Interfaz de usuario
Qué es:
Es la capa de interacción entre el sistema experto y el técnico o usuario.

Para qué sirve:
Sirve para presentar resultados y permitir consultar explicaciones.

Cómo funciona:
Recibe datos, muestra hipótesis priorizadas por certeza y despliega explicaciones detalladas.

Ejemplo:
Top de resultados:
1. Falla probable en junta de culata - 97%
2. Riesgo de sobrecalentamiento del motor - 93%
3. Posible fuga en el sistema de refrigeración - 91%

---

### 4.2 Usuario
Qué es:
Es quien consulta y consume la salida del sistema (técnico o conductor).

Para qué sirve:
Su función es tomar decisiones informadas usando el apoyo del sistema, sin reemplazar criterio profesional.

Cómo funciona:
Interpreta conclusiones, revisa explicaciones y decide siguientes acciones de mantenimiento.

Ejemplo:
El técnico prioriza revisar el sistema de refrigeración y verificar el nivel de aceite.

---

## Flujo integrado de extremo a extremo
1. El experto aporta reglas.
2. Cognimatic ayuda a formalizarlas.
3. El módulo de adquisición valida e integra reglas.
4. La base de conocimiento las almacena.
5. Sensores/fuentes y base de datos llenan la base de hechos del vehículo.
6. El motor de inferencia evalúa reglas con forward chaining.
7. El módulo de explicaciones justifica resultados.
8. La interfaz muestra conclusiones al técnico.
9. El usuario toma decisiones con apoyo del sistema.

---
