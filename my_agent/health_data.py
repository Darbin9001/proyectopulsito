# my_agent/health_data.py
import requests

SERVICE2_URL = "http://127.0.0.1:8002/analyze"  # endpoint del último registro

def get_latest_health_data():
    try:
        response = requests.get(SERVICE2_URL)
        if response.status_code == 200:
            data = response.json()
            if "datos" in data:
                return data["datos"]  # Retorna solo los datos de salud
        return None
    except Exception as e:
        print("⚠️ Error al obtener datos de salud:", e)
        return None
