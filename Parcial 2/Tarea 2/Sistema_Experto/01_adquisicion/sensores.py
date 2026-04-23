# Jonathan Rodrigo Sámchez Rangel - 23110179
# 01_adquisicion/sensores.py
# Módulo de lectura de datos automotrices y bases de datos

import random
import datetime

class SensorAutomotriz:
    """
    Simula una unidad de captura que lee datos del vehículo
    y los pone a disposición del sistema experto automotriz.
    """
    def __init__(self, caso_id, modo_demo=False):
        self.caso_id = caso_id
        self.modo_demo = modo_demo
        self.lecturas = []

    def leer_evidencias(self):
        """Simula lectura de evidencias en tiempo real."""
        lectura = {
            "timestamp": datetime.datetime.now().isoformat(),
            "caso_id": self.caso_id,
        }

        if self.modo_demo:
            lectura.update({
                "nivel_aceite": 12,
                "temperatura_motor": 110,
                "fugas_liquido": True,
                "luz_check_engine": True,
                "ruido_suspenso": True,
            })
        else:
            lectura.update({
                "nivel_aceite": random.randint(5, 80),
                "temperatura_motor": random.randint(70, 120),
                "fugas_liquido": random.choice([True, False]),
                "luz_check_engine": random.choice([True, False]),
                "ruido_suspenso": random.choice([True, False]),
            })
        self.lecturas.append(lectura)
        print(
            "[Sensor] Lectura automotriz: "
            f"Aceite={lectura['nivel_aceite']}%  "
            f"TempMotor={lectura['temperatura_motor']}°C  "
            f"Fugas={lectura['fugas_liquido']}  "
            f"CheckEngine={lectura['luz_check_engine']}  "
            f"Ruido={lectura['ruido_suspenso']}"
        )
        return lectura

    # Alias para compatibilidad con codigo previo.
    def leer_signos_vitales(self):
        return self.leer_evidencias()


class BaseDatosAutomotriz:
    """
    Simula la base de datos automotriz con historial de mantenimiento.
    """
    def __init__(self):
        # Datos simulados
        self._db = {
            "V001": {
                "vehiculo": "Toyota Hilux",
                "placa": "ABC-1234",
                "kilometraje": 124000,
                "ult_revision": "2025-11-10",
                "historico_mantenimientos": ["cambio_aceite", "reparacion_radiador"],
                "estado_correa": "gastada",
            },
            "V002": {
                "vehiculo": "Nissan Frontier",
                "placa": "DEF-5678",
                "kilometraje": 98000,
                "ult_revision": "2025-07-15",
                "historico_mantenimientos": ["reemplazo_bomba_agua", "alineacion"],
                "estado_correa": "bueno",
            },
        }

    def obtener_historial(self, caso_id):
        datos = self._db.get(caso_id)
        if datos:
            print(f"[BD] Historial de {datos['vehiculo']} recuperado.")
        else:
            print(f"[BD] Vehículo {caso_id} no encontrado.")
        return datos


# ── Demo ──────────────────────────────────────────
if __name__ == "__main__":
    sensor = SensorAutomotriz("V001")
    bd = BaseDatosAutomotriz()

    evidencias = sensor.leer_evidencias()
    historial = bd.obtener_historial("V001")

    print("\n── Datos del vehículo listos para el motor de inferencia ──")
    print(f"Vehículo: {historial['vehiculo']}, placa {historial['placa']}")
    print(f"Kilometraje: {historial['kilometraje']}")
    print(f"Nivel de aceite: {evidencias['nivel_aceite']}%")
    print(f"Fugas de líquido: {evidencias['fugas_liquido']}")


# Alias de compatibilidad para no romper imports previos.
SensorLegacy = SensorAutomotriz
BaseDatosLegacy = BaseDatosAutomotriz