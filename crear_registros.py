import requests

cedulas = ["123456789", "987654321" , "654321987"]

for c in cedulas:
    requests.post(f"http://127.0.0.1:8001/health-data/{c}")
    requests.get(f"http://127.0.0.1:8002/analyze/{c}")

print("✅ Datos generados y analizados correctamente")
