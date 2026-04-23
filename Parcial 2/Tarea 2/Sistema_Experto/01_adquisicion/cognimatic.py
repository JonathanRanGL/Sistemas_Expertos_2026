# Jonathan Rodrigo Sámchez Rangel - 23110179
# 01_adquisicion/cognimatic.py
# Simula la herramienta Cognimatic de elicitación de conocimiento automotriz

class Cognimatic:
    """
    Herramienta que guía al experto para estructurar
    su conocimiento en reglas formales procesables.
    """
    OPERADORES = [">", "<", ">=", "<=", "==", "!="]

    def __init__(self):
        self.sesiones = []
        self.reglas_generadas = []

    def iniciar_sesion(self, experto_nombre):
        print("\n=== COGNIMATIC - Sesión de Elicitación ===")
        print(f"Experto: {experto_nombre}")
        sesion = {"experto": experto_nombre, "reglas": []}
        self.sesiones.append(sesion)
        return sesion

    def elicitar_regla_interactiva(self, sesion):
        """
        Guía paso a paso al experto para definir una regla.
        (En producción usaría input(); aquí simulamos el diálogo)
        """
        print("\n-- Definición de nueva regla --")

        # Simularemos una interacción típica
        ejemplo_dialogo = {
            "variable": "nivel_aceite",
            "operador": "<",
            "valor": 20,
            "conclusion": "Inspeccionar fuga de aceite",
            "certeza": 0.98,
        }

        regla = self._construir_regla(ejemplo_dialogo)
        sesion["reglas"].append(regla)
        self.reglas_generadas.append(regla)
        return regla

    def _construir_regla(self, dialogo):
        condicion = (dialogo["variable"], dialogo["operador"], dialogo["valor"])
        regla = {
            "id": f"CG{len(self.reglas_generadas) + 1:03d}",
            "condiciones": [condicion],
            "conclusion": dialogo["conclusion"],
            "certeza": dialogo["certeza"],
        }
        print(f"  → Regla generada: SI {condicion[0]} {condicion[1]} {condicion[2]}")
        print(f"     ENTONCES {regla['conclusion']} (certeza={regla['certeza']})")
        return regla

    def exportar_a_base(self):
        """Exporta todas las reglas generadas para importarlas a la Base de Conocimiento."""
        print(f"\n[Cognimatic] Exportando {len(self.reglas_generadas)} reglas...")
        return self.reglas_generadas


# ── Demo ──────────────────────────────────────────
if __name__ == "__main__":
    cog = Cognimatic()
    sesion_demo = cog.iniciar_sesion("Lic. Vega")

    # Simula varias rondas de elicitación
    cog.elicitar_regla_interactiva(sesion_demo)

    # Regla manual adicional
    sesion_demo["reglas"].append({
        "id": "CG002",
        "condiciones": [("temperatura_motor", ">", 105), ("fugas_liquido", "==", True)],
        "conclusion": "Enfriamiento insuficiente por fuga",
        "certeza": 0.90,
    })
    cog.reglas_generadas.append(sesion_demo["reglas"][-1])

    reglas = cog.exportar_a_base()
    print(f"\nTotal reglas listas para la Base de Conocimiento: {len(reglas)}")