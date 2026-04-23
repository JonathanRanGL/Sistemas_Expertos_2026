# Jonathan Rodrigo Sámchez Rangel - 23110179
# 01_adquisicion/experto.py
# Simula la captura de conocimiento desde un experto automotriz

class ExpertoAutomotriz:
    """
    Representa al experto humano cuyo conocimiento
    se extrae para construir el sistema experto automotriz.
    """
    def __init__(self, nombre, especialidad):
        self.nombre = nombre
        self.especialidad = especialidad
        # Conocimiento que el experto aporta al sistema
        self.reglas_conocidas = []

    def aportar_regla(self, condiciones, conclusion, certeza=1.0):
        """
        El experto define una regla de su conocimiento.
        condiciones : lista de tuplas (variable, operador, valor)
        conclusion  : string con la hipotesis/accion
        certeza     : float 0.0 - 1.0
        """
        regla = {
            "id": f"R{len(self.reglas_conocidas) + 1:03d}",
            "condiciones": condiciones,
            "conclusion": conclusion,
            "certeza": certeza,
            "autor": self.nombre,
        }
        self.reglas_conocidas.append(regla)
        print(f"[Experto] Regla {regla['id']} registrada por {self.nombre}")
        return regla

    def revisar_base(self, base_conocimiento):
        """El experto valida reglas ya capturadas."""
        print(f"\n[{self.nombre}] Revisando base de conocimiento...")
        for regla in base_conocimiento:
            print(f"  Regla {regla['id']}: {regla['conclusion']} — OK")


# ── Demo ──────────────────────────────────────────
if __name__ == "__main__":
    experto = ExpertoAutomotriz("Ing. Rojas", "Mecánica Automotriz")

    experto.aportar_regla(
        condiciones=[
            ("nivel_aceite", "<", 20),
            ("temperatura_motor", ">", 95),
            ("ruido_suspenso", "==", True),
        ],
        conclusion="Falla probable en junta de culata",
        certeza=0.92,
    )

    experto.aportar_regla(
        condiciones=[
            ("luz_check_engine", "==", True),
            ("vibracion_rpm", "==", True),
        ],
        conclusion="Problema en sensor de motor o catalizador",
        certeza=0.95,
    )

    print("\nReglas aportadas por el experto:")
    for regla_demo in experto.reglas_conocidas:
        print(
            f"  {regla_demo['id']}: SI {regla_demo['condiciones']} "
            f"→ {regla_demo['conclusion']} ({regla_demo['certeza']*100:.0f}%)"
        )


# Alias de compatibilidad para no romper imports previos.
ExpertoLegacy = ExpertoAutomotriz