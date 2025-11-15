import random
import datetime

def generar_datos_vitales():
    """Simula la generación de signos vitales de un paciente"""
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "frecuencia_cardiaca": random.randint(60, 110),   # bpm
        "presion_sistolica": random.randint(100, 160),    # mmHg
        "presion_diastolica": random.randint(60, 100),    # mmHg
        "temperatura": round(random.uniform(36.0, 38.5), 1),  # °C
        "oxigeno": random.randint(90, 100)                # %
    }
