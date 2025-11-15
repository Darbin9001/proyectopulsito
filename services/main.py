from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime
import random

# Cargar variables de entorno
load_dotenv()

app = FastAPI(title="Microservicio de Monitoreo de Salud")

# Conexión con MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
collection = db["lecturas"]

try:
    client.admin.command('ping')
    print("✅ Conectado correctamente a MongoDB Atlas")
except Exception as e:
    print("❌ Error conectando a MongoDB:", e)


# CORS para permitir conexión con el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📤 Endpoint de simulación (genera datos aleatorios)
@app.get("/api/simular")
def simular_datos():
    lectura = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "datos": {
            "ritmo_cardiaco": random.randint(55, 110),
            "temperatura": round(random.uniform(35.5, 38.5), 1)
        }
    }
    # Guardar en MongoDB
    collection.insert_one(lectura)
    return {"status": "ok", "inserted": True, "lectura": lectura}

# 📥 Endpoint para obtener los últimos datos
@app.get("/api/data")
def obtener_datos():
    registros = list(collection.find().sort("_id", -1).limit(20))
    # Convertir ObjectId a string y limpiar formato
    for r in registros:
        r["_id"] = str(r["_id"])
    return registros
