# Jonathan Rodrigo Sámchez Rangel - 23110179
# 02_representacion/base_conocimiento.py
# Implementación de la Base de Conocimiento con reglas de producción para diagnóstico automotriz

class BaseConocimiento:
    """
    Repositorio permanente del conocimiento experto.
    Almacena reglas de producción: SI [cond] ENTONCES [conclusión] (certeza).
    """
    def __init__(self, dominio="General"):
        self.dominio = dominio
        self.reglas = []

    def agregar_regla(self, condiciones, conclusion, certeza=1.0, nombre=None):
        """
        condiciones: lista de tuplas (variable, operador, valor)
                     operadores: '>', '<', '>=', '<=', '==', '!='
        conclusion : string — diagnóstico, acción o recomendación
        certeza    : float 0.0-1.0
        """
        regla = {
            "id": f"R{len(self.reglas) + 1:03d}",
            "nombre": nombre or f"Regla {len(self.reglas) + 1}",
            "condiciones": condiciones,
            "conclusion": conclusion,
            "certeza": certeza,
        }
        self.reglas.append(regla)
        return regla

    def buscar_por_conclusion(self, conclusion):
        return [r for r in self.reglas if conclusion.lower() in r["conclusion"].lower()]

    def listar(self):
        print(f"\n── Base de Conocimiento: {self.dominio} ──")
        print(f"   Total de reglas: {len(self.reglas)}")
        for regla in self.reglas:
            conds = " Y ".join([f"{c[0]} {c[1]} {c[2]}" for c in regla["condiciones"]])
            print(f"   {regla['id']}: SI {conds}")
            print(f"         ENTONCES {regla['conclusion']} (certeza: {regla['certeza']*100:.0f}%)")


# ── Construccion de una BC automotriz completa ─────────
def crear_bc_automotriz():
    bc = BaseConocimiento("Diagnóstico Automotriz")

    bc.agregar_regla(
        [("nivel_aceite", "<", 20), ("temperatura_motor", ">", 95), ("ruido_suspenso", "==", True)],
        "Falla probable en junta de culata", certeza=0.97, nombre="Junta de culata"
    )
    bc.agregar_regla(
        [("nivel_anticongelante", "<", 30), ("temperatura_motor", ">", 105)],
        "Riesgo de sobrecalentamiento del motor", certeza=0.93, nombre="Sobrecalentamiento"
    )
    bc.agregar_regla(
        [("fugas_liquido", "==", True), ("olor_quemado", "==", True)],
        "Posible fuga en el sistema de refrigeración", certeza=0.91, nombre="Fuga refrigerante"
    )
    bc.agregar_regla(
        [("luz_check_engine", "==", True), ("vibracion_rpm", "==", True)],
        "Sensor de motor o convertidor catalítico defectuoso", certeza=0.89, nombre="Sensor defectuoso"
    )
    bc.agregar_regla(
        [("nivel_aceite", "<", 20), ("fugas_liquido", "==", True)],
        "Alto riesgo de daño grave en el motor",
        certeza=0.99, nombre="Riesgo motor"
    )
    return bc


# Alias de compatibilidad para demos o imports previos.
crear_bc_medica = crear_bc_automotriz


if __name__ == "__main__":
    bc_demo = crear_bc_automotriz()
    bc_demo.listar()

    print("\n── Busqueda de reglas sobre diagnóstico ──")
    resultados = bc_demo.buscar_por_conclusion("Falla")
    for regla_demo in resultados:
        print(f"   Encontrada: {regla_demo['id']} — {regla_demo['nombre']}")