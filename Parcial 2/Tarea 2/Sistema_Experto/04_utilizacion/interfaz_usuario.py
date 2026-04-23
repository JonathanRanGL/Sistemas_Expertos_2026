# Jonathan Rodrigo Sámchez Rangel - 23110179
# 04_utilizacion/interfaz_usuario.py
# Interfaz de consola del sistema experto automotriz

class InterfazUsuario:
    """
    Gestiona la interaccion entre el sistema experto y el técnico/usuario.
    En una aplicación real sería una UI web o de escritorio;
    aquí implementamos la versión de consola.
    """
    def __init__(self, motor, explicaciones):
        self.motor = motor
        self.exp = explicaciones
        self.sesion_activa = False

    def mostrar_bienvenida(self):
        print("\n" + "═" * 50)
        print("   SISTEMA EXPERTO DE DIAGNÓSTICO AUTOMOTRIZ")
        print("   Version 1.0 - Dominio: Mecánica Automotriz")
        print("═" * 50)
        print("  Ingrese datos del vehículo para obtener")
        print("  hipótesis de diagnóstico asistidas por reglas.")
        print("─" * 50)

    def solicitar_datos_vehiculo(self):
        """Recopila datos básicos del vehículo."""
        print("\n[1/3] DATOS DEL VEHÍCULO")
        datos = {}

        # En producción usarías input(); aquí simulamos
        campos = [
            ("placa", "Placa", "ABC-1234"),
            ("vehiculo", "Vehículo", "Toyota Hilux"),
            ("taller", "Taller", "Taller Central"),
        ]
        for key, etiqueta, valor_demo in campos:
            print(f"  {etiqueta}: {valor_demo}  [demo]")
            datos[key] = valor_demo

        return datos

    def solicitar_evidencias(self):
        """Recopila evidencias via teclado o sensores."""
        print("\n[2/3] DATOS DEL VEHÍCULO")
        evidencias = {
            "nivel_aceite": 12,
            "temperatura_motor": 110,
            "fugas_liquido": True,
            "luz_check_engine": True,
            "ruido_suspenso": True,
        }
        for k, v in evidencias.items():
            print(f"  {k:28s}: {v}  [demo]")

        print("\n[3/3] CONTEXTO DEL VEHÍCULO")
        contexto = {
            "ult_revision": "2025-11-10",
            "kilometraje": 124000,
            "estado_correa": "gastada",
        }
        for k, v in contexto.items():
            print(f"  {k:28s}: {v}  [demo]")

        return {**evidencias, **contexto}

    def mostrar_resultados(self):
        """Presenta los resultados del motor de inferencia al usuario."""
        conclusiones = self.motor.conclusiones

        print("\n" + "═" * 50)
        print("   RESULTADOS DEL ANÁLISIS")
        print("═" * 50)

        if not conclusiones:
            print("  ⚠ No fue posible establecer un diagnóstico claro.")
            print("  Por favor proporcione más datos del vehículo al sistema.")
            return

        top = sorted(conclusiones, key=lambda x: x["certeza"], reverse=True)

        for i, c in enumerate(top[:3], 1):
            pct = int(c["certeza"] * 100)
            barra = "█" * (pct // 5) + "░" * (20 - pct // 5)
            prioridad = "🔴 ALTA" if pct >= 90 else "🟡 MEDIA" if pct >= 75 else "🟢 BAJA"
            print(f"\n  {i}. {c['conclusion']}")
            print(f"     [{barra}] {pct}%  {prioridad}")

        print("\n" + "─" * 50)

    def menu_explicaciones(self):
        """Menu de opciones de explicacion para el técnico."""
        opciones = [
            "1. Ver explicación del diagnóstico principal",
            "2. Ver todas las reglas evaluadas",
            "3. Iniciar nuevo análisis",
            "4. Salir",
        ]
        print("\n¿Desea más información?")
        for op in opciones:
            print(f"  {op}")

        # Simulamos selección 1
        print("\n  Selección: 1")
        top = sorted(self.motor.conclusiones, key=lambda x: x["certeza"], reverse=True)
        if top:
            self.exp.por_que(top[0]["conclusion"])

    def ejecutar(self):
        """Flujo completo de una consulta."""
        self.mostrar_bienvenida()
        self.solicitar_datos_vehiculo()
        evidencias = self.solicitar_evidencias()

        # Cargar hechos en la Base de Hechos
        for k, v in evidencias.items():
            self.motor.bh.agregar_hecho(k, v, "interfaz")

        self.motor.inferir()
        self.mostrar_resultados()
        self.menu_explicaciones()


# ── Demo ──────────────────────────────────────────
if __name__ == "__main__":
    from pathlib import Path
    import sys

    raiz = Path(__file__).resolve().parents[1]
    for subdirectorio in [
        "02_representacion",
        "03_tratamiento",
        "04_utilizacion",
    ]:
        ruta = str(raiz / subdirectorio)
        if ruta not in sys.path:
            sys.path.insert(0, ruta)
    import importlib

    crear_bc_automotriz = importlib.import_module("base_conocimiento").crear_bc_automotriz
    BaseHechos = importlib.import_module("base_hechos").BaseHechos
    MotorInferencia = importlib.import_module("motor_inferencia").MotorInferencia
    ModuloExplicaciones = importlib.import_module("modulo_explicaciones").ModuloExplicaciones

    bc = crear_bc_automotriz()
    bh = BaseHechos("SESION-UI-001")
    motor_demo = MotorInferencia(bc, bh)
    exp = ModuloExplicaciones(motor_demo, bc)
    ui = InterfazUsuario(motor_demo, exp)
    ui.ejecutar()