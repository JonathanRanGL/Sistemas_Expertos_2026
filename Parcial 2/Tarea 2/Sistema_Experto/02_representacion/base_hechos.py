# Jonathan Rodrigo Sámchez Rangel - 23110179
# 02_representacion/base_hechos.py
# Memoria de trabajo del sistema experto (efímera por sesión)

class BaseHechos:
    """
    Almacén TEMPORAL de datos del caso en proceso.
    Se crea al inicio de cada consulta y se destruye al terminar.
    Diferencia clave: la Base de Conocimiento es permanente;
    la Base de Hechos es específica de cada caso.
    """
    def __init__(self, caso_id):
        self.caso_id = caso_id
        self.hechos = {}
        self.historial_cambios = []

    def agregar_hecho(self, variable, valor, fuente="usuario"):
        """Registra un dato del caso actual."""
        anterior = self.hechos.get(variable)
        self.hechos[variable] = valor
        self.historial_cambios.append({
            "variable": variable,
            "valor_anterior": anterior,
            "valor_nuevo": valor,
            "fuente": fuente,
        })
        print(f"  [Hecho] {variable} = {valor}  (fuente: {fuente})")

    def obtener(self, variable):
        return self.hechos.get(variable)

    def evaluar_condicion(self, condicion):
        """
        Evalúa una condición de regla contra los hechos actuales.
        condicion: (variable, operador, valor_umbral)
        """
        variable, operador, umbral = condicion
        valor_actual = self.hechos.get(variable)

        if valor_actual is None:
            return None  # Hecho desconocido

        ops = {
            ">": lambda a, b: a > b,
            "<": lambda a, b: a < b,
            ">=": lambda a, b: a >= b,
            "<=": lambda a, b: a <= b,
            "==": lambda a, b: a == b,
            "!=": lambda a, b: a != b,
        }
        fn = ops.get(operador)
        if not fn:
            return False

        try:
            return fn(valor_actual, umbral)
        except TypeError:
            # Evita romper la inferencia cuando hay tipos incompatibles.
            return False

    def limpiar(self):
        """Limpia la memoria al finalizar la sesión."""
        print(f"  [Base de Hechos] Sesión {self.caso_id} cerrada. Memoria limpiada.")
        self.hechos.clear()

    def resumen(self):
        print(f"\n── Caso {self.caso_id} — Hechos registrados ──")
        for k, v in self.hechos.items():
            print(f"   {k:30s} = {v}")


# ── Demo ──────────────────────────────────────────
if __name__ == "__main__":
    # Caso de un vehículo en revisión
    caso = BaseHechos("VEHICULO-2024-001")

    print("Registrando datos del vehículo:")
    caso.agregar_hecho("vehiculo", "Toyota Hilux", fuente="registro")
    caso.agregar_hecho("placa", "ABC-1234", fuente="registro")
    caso.agregar_hecho("nivel_aceite", 14, fuente="sensor")
    caso.agregar_hecho("temperatura_motor", 112, fuente="sensor")
    caso.agregar_hecho("fugas_liquido", True, fuente="sensor")
    caso.agregar_hecho("luz_check_engine", True, fuente="sensor")
    caso.agregar_hecho("ruido_suspenso", True, fuente="usuario")
    caso.agregar_hecho("historico_mantenimientos", ["cambio_aceite", "reparacion_radiador"], fuente="registro")

    caso.resumen()

    # Evaluación de condiciones
    print("\nEvaluando condiciones de reglas:")
    conds = [
        ("temperatura", ">", 38.5),
        ("frecuencia_cardiaca", ">", 100),
        ("infiltrado_pulmonar", "==", True),
    ]
    for c in conds:
        resultado = caso.evaluar_condicion(c)
        estado = "✓ VERDADERA" if resultado else "✗ FALSA"
        print(f"  {c[0]} {c[1]} {c[2]:>6} → {estado}")

    caso.limpiar()