@app.get("/predict")
def predict_risk():
    data = requests.get("http://127.0.0.1:8002/historial").json()
    # Analiza últimos 10 registros y genera una recomendación
    riesgo = modelo.predict(data)
    return {"riesgo": riesgo, "recomendacion": "Visitar al médico si los valores persisten"}
