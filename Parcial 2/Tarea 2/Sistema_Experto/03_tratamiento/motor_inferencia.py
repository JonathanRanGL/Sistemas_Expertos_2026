# Jonathan Rodrigo Sámchez Rangel - 23110179
# 03_tratamiento/motor_inferencia.py
# Motor de Inferencia con encadenamiento hacia adelante

class MotorInferencia:
    """
    Corazón del sistema experto.
    Aplica reglas de la Base de Conocimiento sobre los
    hechos de la Base de Hechos para derivar conclusiones.
    
    Estrategia: Forward Chaining (encadenamiento hacia adelante)
    Parte de los hechos conocidos → aplica reglas → obtiene conclusiones.
    """
    def __init__(self, base_conocimiento, base_hechos):
        self.bc = base_conocimiento
        self.bh = base_hechos
        self.conclusiones = []
        self.traza = []  # Para el módulo de explicaciones

    def inferir(self):
        """
        Ciclo principal de inferencia.
        Evalúa cada regla contra los hechos actuales.
        """
        print("\n=== Motor de Inferencia: iniciando ciclo ===")
        self.conclusiones.clear()
        self.traza.clear()

        for regla in self.bc.reglas:
            resultado = self._evaluar_regla(regla)
            if resultado["disparada"]:
                self.conclusiones.append({
                    "conclusion": regla["conclusion"],
                    "certeza": regla["certeza"],
                    "regla_id": regla["id"],
                })
                print(f"  ✓ {regla['id']} disparada → {regla['conclusion']} "
                      f"(certeza: {regla['certeza']*100:.0f}%)")

        if not self.conclusiones:
            print("  ⚠ No se pudieron derivar conclusiones con los hechos actuales.")

        return self.conclusiones

    def _evaluar_regla(self, regla):
        """Evalúa si TODAS las condiciones de una regla se cumplen."""
        evaluaciones = []
        todas_ciertas = True

        for condicion in regla["condiciones"]:
            cumplida = self.bh.evaluar_condicion(condicion)
            if cumplida is None:
                cumplida = False  # Hecho desconocido = no cumple
            evaluaciones.append({
                "condicion": condicion,
                "cumplida": cumplida,
            })
            if not cumplida:
                todas_ciertas = False

        resultado = {
            "regla_id": regla["id"],
            "disparada": todas_ciertas,
            "evaluaciones": evaluaciones,
        }
        self.traza.append(resultado)
        return resultado

    def top_conclusiones(self, n=3):
        """Retorna las N conclusiones con mayor certeza."""
        return sorted(self.conclusiones, key=lambda x: x["certeza"], reverse=True)[:n]

    def obtener_traza(self):
        """Devuelve la traza de razonamiento para el módulo de explicaciones."""
        return self.traza


# ── Demo ──────────────────────────────────────────
if __name__ == "__main__":
    # Importar los módulos anteriores desde rutas del proyecto.
    from pathlib import Path
    import sys

    raiz = Path(__file__).resolve().parents[1]
    for subdirectorio in ["02_representacion", "03_tratamiento"]:
        ruta = str(raiz / subdirectorio)
        if ruta not in sys.path:
            sys.path.insert(0, ruta)

    import importlib

    crear_bc_automotriz = importlib.import_module("base_conocimiento").crear_bc_automotriz
    BaseHechos = importlib.import_module("base_hechos").BaseHechos

    bc = crear_bc_automotriz()
    bh = BaseHechos("DEMO-001")

    # Cargar hechos del vehículo demo
    bh.agregar_hecho("nivel_aceite", 12, "sensor")
    bh.agregar_hecho("temperatura_motor", 112, "sensor")
    bh.agregar_hecho("fugas_liquido", True, "inspeccion")
    bh.agregar_hecho("luz_check_engine", True, "sensor")
    bh.agregar_hecho("ruido_suspenso", True, "usuario")
    bh.agregar_hecho("ult_revision", "2025-11-10", "registro")
    bh.agregar_hecho("kilometraje", 124000, "registro")

    motor_demo = MotorInferencia(bc, bh)
    conclusiones = motor_demo.inferir()

    print("\n── Top conclusiones ──")
    for c in motor_demo.top_conclusiones():
        print(f"  {c['conclusion']:40s}  certeza: {c['certeza']*100:.0f}%")