# Jonathan Rodrigo Sámchez Rangel - 23110179
# diagnostico_automotriz.py — Sistema Experto Automotriz Completo
# Integra las 4 fases del diagnóstico automotriz.

from pathlib import Path
import importlib
import sys


def _configurar_rutas_importacion():
    """Permite ejecutar el proyecto desde la carpeta raíz sin errores de importación."""
    raiz = Path(__file__).resolve().parent
    subdirectorios = [
        "01_adquisicion",
        "02_representacion",
        "03_tratamiento",
        "04_utilizacion",
    ]
    for subdirectorio in subdirectorios:
        ruta = str(raiz / subdirectorio)
        if ruta not in sys.path:
            sys.path.insert(0, ruta)


_configurar_rutas_importacion()

ExpertoAutomotriz = importlib.import_module("experto").ExpertoAutomotriz
SensorAutomotriz = importlib.import_module("sensores").SensorAutomotriz
BaseDatosAutomotriz = importlib.import_module("sensores").BaseDatosAutomotriz
ModuloAdquisicion = importlib.import_module("modulo_adquisicion").ModuloAdquisicion
BaseConocimiento = importlib.import_module("base_conocimiento").BaseConocimiento
BaseHechos = importlib.import_module("base_hechos").BaseHechos
MotorInferencia = importlib.import_module("motor_inferencia").MotorInferencia
ModuloExplicaciones = importlib.import_module("modulo_explicaciones").ModuloExplicaciones
InterfazUsuario = importlib.import_module("interfaz_usuario").InterfazUsuario


def construir_base_conocimiento():
    """Fase 1+2: Adquirir y representar el conocimiento."""
    print("\n📥 FASE 1: Adquisición del Conocimiento")
    print("─" * 45)

    # Experto aporta reglas
    experto = ExpertoAutomotriz("Ing. Rojas", "Mecánica Automotriz")
    experto.aportar_regla(
        [("nivel_aceite", "<", 20), ("temperatura_motor", ">", 95),
         ("ruido_suspenso", "==", True)],
        "Falla probable en junta de culata", certeza=0.97
    )
    experto.aportar_regla(
        [("nivel_anticongelante", "<", 30), ("temperatura_motor", ">", 105)],
        "Riesgo de sobrecalentamiento del motor", certeza=0.93
    )
    experto.aportar_regla(
        [("fugas_liquido", "==", True), ("olor_quemado", "==", True)],
        "Posible fuga en el sistema de refrigeración", certeza=0.91
    )
    experto.aportar_regla(
        [("luz_check_engine", "==", True), ("vibracion_rpm", "==", True)],
        "Sensor de motor o convertidor catalítico defectuoso", certeza=0.89
    )
    experto.aportar_regla(
        [("nivel_aceite", "<", 20), ("fugas_liquido", "==", True)],
        "Alto riesgo de daño grave en el motor", certeza=0.99
    )

    # Módulo de adquisición valida e integra
    print("\n🔍 Módulo de Adquisición validando reglas...")
    bc_lista = []
    modulo_adq = ModuloAdquisicion(bc_lista)
    for regla in experto.reglas_conocidas:
        modulo_adq.integrar_regla(regla)

    # Construir Base de Conocimiento oficial
    print("\n🧠 FASE 2: Representación del Conocimiento")
    print("─" * 45)
    bc = BaseConocimiento("Diagnóstico Automotriz")
    for regla in bc_lista:
        bc.reglas.append(regla)
    print(f"  Base de Conocimiento: {len(bc.reglas)} reglas cargadas.")

    return bc


def adquirir_datos_caso(caso_id):
    """Fase 1: Recopilar datos del vehículo actual."""
    sensor = SensorAutomotriz(caso_id, modo_demo=True)
    bd = BaseDatosAutomotriz()

    evidencias = sensor.leer_evidencias()
    historial = bd.obtener_historial(caso_id)

    # Hechos adicionales del vehículo
    hechos_extra = {
        "nivel_aceite": 15,
        "fugas_liquido": True,
        "temperatura_motor": 110,
        "luz_check_engine": True,
    }
    return {**evidencias, **hechos_extra, **(historial or {})}


def main():
    print("╔══════════════════════════════════════════════╗")
    print("║   SISTEMA EXPERTO AUTOMOTRIZ — Arranque      ║")
    print("╚══════════════════════════════════════════════╝")

    # ── FASE 1 + 2: Adquisición y Representación ──
    bc = construir_base_conocimiento()

    # ── FASE 1: Recopilar datos del vehículo ──
    print("\n📡 Adquiriendo datos del vehículo V001...")
    datos_caso = adquirir_datos_caso("V001")

    # ── FASE 2: Base de Hechos ──
    bh = BaseHechos("VEHICULO-V001")
    print("\n📋 FASE 2: Cargando Base de Hechos...")
    for k, v in datos_caso.items():
        if isinstance(v, (int, float, str, bool)):
            bh.agregar_hecho(k, v, "sistema")

    # ── FASE 3: Tratamiento del Conocimiento ──
    print("\n⚙️  FASE 3: Tratamiento del Conocimiento")
    print("─" * 45)
    motor = MotorInferencia(bc, bh)
    motor.inferir()

    exp = ModuloExplicaciones(motor, bc)
    exp.que_para_que_como()
    exp.resumen_para_usuario()

    # ── FASE 4: Utilización del Conocimiento ──
    print("\n🖥️  FASE 4: Utilización del Conocimiento")
    print("─" * 45)
    ui = InterfazUsuario(motor, exp)
    ui.mostrar_resultados()
    ui.menu_explicaciones()

    # Explicación detallada
    top = sorted(motor.conclusiones, key=lambda x: x["certeza"], reverse=True)
    if top:
        exp.por_que(top[0]["conclusion"])
    exp.como_funcione()

    # Limpieza de memoria de trabajo
    bh.limpiar()
    print("\n✓ Sesión finalizada correctamente.\n")


if __name__ == "__main__":
    main()