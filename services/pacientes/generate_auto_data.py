import os
import requests
import time
import random

# Lista de cédulas simuladas
cedulas = ["123456789", "987654321", "456789123", "1060872570"]

# URL de los servicios
SERVICE1_URL = os.getenv("SERVICE1_URL", "http://service1-service:8002/health-data")
SERVICE2_URL = os.getenv("SERVICE2_URL", "http://service2-service:8003/analyze")

def generar_signos_vitales(cedula):
    """Envía datos aleatorios de signos vitales al microservicio 1 y los analiza en el 2"""
    try:
        # Crear signos vitales aleatorios
        data = {
            "ritmo_cardiaco": random.randint(60, 100),
            "temperatura": round(random.uniform(36.0, 38.0), 1),
            "presion": f"{random.randint(110, 130)}/{random.randint(70, 90)}",
            "oxigeno": random.randint(94, 100)
        }

        # Enviar al servicio 1
        r1 = requests.post(f"{SERVICE1_URL}/{cedula}", json=data, timeout=5)

        # Analizar en servicio 2
        r2 = requests.get(f"{SERVICE2_URL}/{cedula}", timeout=5)

        if r1.status_code == 200 and r2.status_code == 200:
            print(f"✅ Datos generados y analizados correctamente para cédula {cedula}")
        else:
            print(f"⚠️ Error con cédula {cedula}: "
                  f"Service1 {r1.status_code}, Service2 {r2.status_code}")

    except Exception as e:
        print(f"❌ Error procesando {cedula}: {e}")

if __name__ == "__main__":
    print("🩺 Generando signos vitales automáticamente cada 10 segundos...")
    while True:
        for c in cedulas:
            generar_signos_vitales(c)
        print("⏱️ Esperando 10 segundos para la siguiente ronda...\n")
        time.sleep(10)
