# Jonathan Rodrigo Sámchez Rangel - 23110179
# 01_adquisicion/modulo_adquisicion.py
# Controla la integración de nuevo conocimiento

class ModuloAdquisicion:
    """
    Valida que el nuevo conocimiento sea consistente
    con la base existente antes de incorporarlo.
    """
    def __init__(self, base_conocimiento):
        self.base = base_conocimiento  # lista de reglas existentes
        self.log = []

    def integrar_regla(self, nueva_regla):
        """
        Intenta integrar una nueva regla.
        Devuelve True si fue aceptada, False si fue rechazada.
        """
        print(f"\n[Adquisición] Evaluando regla {nueva_regla['id']}...")

        if self._es_duplicada(nueva_regla):
            self._registrar("RECHAZADA", nueva_regla, "Regla duplicada o muy similar")
            return False

        conflicto = self._detectar_conflicto(nueva_regla)
        if conflicto:
            self._registrar("CONFLICTO", nueva_regla, f"Conflicto con {conflicto['id']}")
            print(f"  ⚠ Conflicto detectado con regla {conflicto['id']}")
            print("     Ambas tienen mismas condiciones pero conclusiones distintas.")
            return False

        self.base.append(nueva_regla)
        self._registrar("ACEPTADA", nueva_regla, "Conocimiento consistente")
        print(f"  ✓ Regla {nueva_regla['id']} integrada correctamente.")
        return True

    def _es_duplicada(self, nueva):
        for existente in self.base:
            if (existente["condiciones"] == nueva["condiciones"] and
                    existente["conclusion"] == nueva["conclusion"]):
                return True
        return False

    def _detectar_conflicto(self, nueva):
        """Detecta si mismas condiciones llevan a conclusiones opuestas."""
        for existente in self.base:
            if (existente["condiciones"] == nueva["condiciones"] and
                    existente["conclusion"] != nueva["conclusion"]):
                return existente
        return None

    def _registrar(self, estado, regla, motivo):
        entrada = {"estado": estado, "regla_id": regla["id"], "motivo": motivo}
        self.log.append(entrada)
        simbolo = {"ACEPTADA": "✓", "RECHAZADA": "✗", "CONFLICTO": "⚠"}.get(estado, "?")
        print(f"  {simbolo} [{estado}] {regla['id']}: {motivo}")

    def reporte(self):
        print("\n── Reporte del Módulo de Adquisición ──")
        for entrada in self.log:
            print(f"  {entrada['estado']:12s} {entrada['regla_id']}: {entrada['motivo']}")


# ── Demo ──────────────────────────────────────────
if __name__ == "__main__":
    base = [
        {
            "id": "R001",
            "condiciones": [("temperatura", ">", 38.5)],
            "conclusion": "Fiebre",
            "certeza": 0.98,
        }
    ]

    modulo = ModuloAdquisicion(base)

    # Regla nueva válida
    modulo.integrar_regla({
        "id": "R002",
        "condiciones": [("frecuencia_cardiaca", ">", 100), ("onda_p", "==", "ausente")],
        "conclusion": "Fibrilación Auricular",
        "certeza": 0.92,
    })

    # Regla duplicada
    modulo.integrar_regla({
        "id": "R003",
        "condiciones": [("temperatura", ">", 38.5)],
        "conclusion": "Fiebre",
        "certeza": 0.98,
    })

    # Regla en conflicto
    modulo.integrar_regla({
        "id": "R004",
        "condiciones": [("temperatura", ">", 38.5)],
        "conclusion": "Hipotermia",  # contradice R001!
        "certeza": 0.50,
    })

    modulo.reporte()
    print(f"\nReglas en base: {len(base)}")