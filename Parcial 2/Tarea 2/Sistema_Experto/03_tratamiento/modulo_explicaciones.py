# Jonathan Rodrigo Sámchez Rangel - 23110179
# 03_tratamiento/modulo_explicaciones.py
# Genera explicaciones del razonamiento del motor de inferencia

class ModuloExplicaciones:
    """
    Transforma la traza técnica del Motor de Inferencia
    en explicaciones comprensibles para el usuario.
    
    Responde preguntas como:
    - ¿Por qué concluiste X?
    - ¿Como llegaste a esa hipotesis?
    - ¿Qué reglas se activaron?
    """
    def __init__(self, motor, base_conocimiento):
        self.motor = motor
        self.bc = base_conocimiento

    def que_para_que_como(self):
        """Presenta una explicación breve y clara del sistema."""
        print("\n╔════════════════════════════════════════════════════════════╗")
        print("║                  GUÍA RÁPIDA DEL SISTEMA                 ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print("  ¿Qué es?")
        print("  Un sistema experto automotriz basado en reglas de produccion.")
        print("\n  ¿Para qué sirve?")
        print("  Para apoyar el diagnóstico de fallas con hipótesis y niveles")
        print("  de certeza a partir de datos del vehículo.")
        print("\n  ¿Cómo funciona?")
        print("  1) Carga conocimiento experto (reglas SI... ENTONCES...).")
        print("  2) Registra hechos y evidencias del caso actual.")
        print("  3) Evalúa condiciones con encadenamiento hacia adelante.")
        print("  4) Muestra diagnósticos/hipótesis y explicación del razonamiento.")

    def por_que(self, conclusion_objetivo):
        """
        Explica por qué el sistema llegó a una conclusión particular.
        """
        print(f"\n=== EXPLICACIÓN: ¿Por qué '{conclusion_objetivo}'? ===")

        # Buscar la conclusión en las derivadas
        encontrada = None
        for c in self.motor.conclusiones:
            if conclusion_objetivo.lower() in c["conclusion"].lower():
                encontrada = c
                break

        if not encontrada:
            print(f"  El sistema NO concluyó '{conclusion_objetivo}'.")
            print("  Posibles razones: falta de datos o condiciones no cumplidas.")
            return

        # Buscar la regla que la disparó
        regla = next((r for r in self.bc.reglas if r["id"] == encontrada["regla_id"]), None)
        if not regla:
            return

        print(f"\n  Conclusión: {encontrada['conclusion']}")
        print(f"  Certeza   : {encontrada['certeza'] * 100:.0f}%")
        print(f"  Regla     : {regla['id']} — {regla.get('nombre', '')}")
        print("\n  Evidencia que soporta la hipotesis:")

        for i, cond in enumerate(regla["condiciones"], 1):
            variable, op, umbral = cond
            valor_real = self.motor.bh.hechos.get(variable, "desconocido")
            print(f"    {i}. {variable} = {valor_real}  "
                  f"(condición: {variable} {op} {umbral} ✓)")

    def como_funcione(self):
        """Muestra todas las reglas evaluadas y su resultado."""
        print("\n=== CÓMO RAZONÓ EL SISTEMA ===")
        disparadas = [t for t in self.motor.traza if t["disparada"]]
        no_disparadas = [t for t in self.motor.traza if not t["disparada"]]

        print(f"  Reglas evaluadas : {len(self.motor.traza)}")
        print(f"  Reglas disparadas: {len(disparadas)}")

        if disparadas:
            print("\n  Reglas que SÍ se activaron:")
            for t in disparadas:
                regla = next((r for r in self.bc.reglas if r["id"] == t["regla_id"]), None)
                nombre = regla.get("nombre", "") if regla else ""
                print(f"    ✓ {t['regla_id']} — {nombre}")

        if no_disparadas:
            print("\n  Reglas que NO se activaron (primera condición fallida):")
            for t in no_disparadas[:3]:  # Solo primeras 3
                fallo = next((e for e in t["evaluaciones"] if not e["cumplida"]), None)
                if fallo:
                    c = fallo["condicion"]
                    v = self.motor.bh.hechos.get(c[0], "sin dato")
                    print(f"    ✗ {t['regla_id']}: {c[0]} = {v} (requería {c[0]} {c[1]} {c[2]})")

    def resumen_para_usuario(self):
        """Genera el resumen final para el diagnóstico automotriz."""
        print("\n╔══════════════════════════════════════════╗")
        print("║       INFORME DEL SISTEMA EXPERTO        ║")
        print("╚══════════════════════════════════════════╝")

        top = sorted(self.motor.conclusiones, key=lambda x: x["certeza"], reverse=True)
        for i, c in enumerate(top[:3], 1):
            barra = "█" * int(c["certeza"] * 20)
            print(f"  {i}. {c['conclusion']}")
            print(f"     Certeza: {c['certeza']*100:.0f}% [{barra:<20}]")
        print()


# ── Demo ──────────────────────────────────────────
if __name__ == "__main__":
    from pathlib import Path
    import sys
    import importlib

    raiz = Path(__file__).resolve().parents[1]
    for subdirectorio in ["02_representacion", "03_tratamiento"]:
        ruta = str(raiz / subdirectorio)
        if ruta not in sys.path:
            sys.path.insert(0, ruta)

    crear_bc_automotriz = importlib.import_module("base_conocimiento").crear_bc_automotriz
    BaseHechos = importlib.import_module("base_hechos").BaseHechos
    MotorInferencia = importlib.import_module("motor_inferencia").MotorInferencia

    bc = crear_bc_automotriz()
    bh = BaseHechos("DEMO-EXP-001")
    bh.agregar_hecho("nivel_aceite", 12, "sensor")
    bh.agregar_hecho("temperatura_motor", 110, "sensor")
    bh.agregar_hecho("fugas_liquido", True, "inspeccion")
    bh.agregar_hecho("luz_check_engine", True, "sensor")
    bh.agregar_hecho("ruido_suspenso", True, "diagnostico")
    bh.agregar_hecho("ult_revision", "2025-11-10", "registro")
    bh.agregar_hecho("kilometraje", 124000, "registro")
    bh.agregar_hecho("estado_correa", "gastada", "inspeccion")

    motor_demo = MotorInferencia(bc, bh)
    motor_demo.inferir()

    exp = ModuloExplicaciones(motor_demo, bc)
    exp.resumen_para_usuario()
    exp.por_que("Falla")
    exp.como_funcione()