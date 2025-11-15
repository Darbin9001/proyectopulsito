from pymongo import MongoClient
from dotenv import load_dotenv

import os

load_dotenv()  # Carga variables del .env

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    print("✅ Conectado correctamente a MongoDB Atlas")
except Exception as e:
    print("❌ Error al conectar a MongoDB Atlas:", e)
    db = None
