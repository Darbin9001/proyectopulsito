from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import random
from datetime import datetime
from services.data_base_mongo import db
from services.utils import serialize_mongo
from typing import Optional

app = FastAPI(title="Servicio 1 - Generador de Datos de Salud")

# --- HABILITAR CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ENDPOINTS DE PACIENTES ---

@app.post("/pacientes")
def crear_paciente(cedula: str, nombre: str, apellido: str, edad: Optional[int] = None):
    """Crear o actualizar un paciente"""
    if db is None:
        raise HTTPException(status_code=500, detail="Base de datos no disponible")
    
    # Verificar si ya existe
    paciente_existente = db["pacientes"].find_one({"cedula": cedula})
    
    paciente_data = {
        "cedula": cedula,
        "nombre": nombre,
        "apellido": apellido,
        "edad": edad,
        "fecha_registro": datetime.now()
    }
    
    if paciente_existente:
        db["pacientes"].update_one(
            {"cedula": cedula},
            {"$set": paciente_data}
        )
        return {"mensaje": "Paciente actualizado", "cedula": cedula}
    else:
        db["pacientes"].insert_one(paciente_data)
        return {"mensaje": "Paciente creado", "cedula": cedula}


@app.get("/pacientes/{cedula}")
def obtener_paciente(cedula: str):
    """Obtener información de un paciente por cédula"""
    if db is None:
        raise HTTPException(status_code=500, detail="Base de datos no disponible")
    
    paciente = db["pacientes"].find_one({"cedula": cedula})
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    return serialize_mongo(paciente)


@app.get("/pacientes")
def listar_pacientes():
    """Listar todos los pacientes"""
    if db is None:
        raise HTTPException(status_code=500, detail="Base de datos no disponible")
    
    pacientes = list(db["pacientes"].find())
    return serialize_mongo(pacientes)


# --- ENDPOINTS DE SIGNOS VITALES ---

@app.get("/")
def root():
    return {"message": "Servicio 1 activo"}


@app.post("/health-data/{cedula}")
def generar_signos_vitales(cedula: str):
    """Generar signos vitales para un paciente específico"""
    if db is None:
        raise HTTPException(status_code=500, detail="Base de datos no disponible")
    
    # Verificar que el paciente existe
    paciente = db["pacientes"].find_one({"cedula": cedula})
    if not paciente:
        raise HTTPException(
            status_code=404, 
            detail=f"Paciente con cédula {cedula} no encontrado. Debe registrarlo primero."
        )
    
    # Generar datos aleatorios simulados
    lectura = {
        "cedula": cedula,
        "nombre": f"{paciente['nombre']} {paciente['apellido']}",
        "ritmo_cardiaco": random.randint(60, 120),
        "temperatura": round(random.uniform(36, 39), 1),
        "presion": f"{random.randint(100,130)}/{random.randint(70,90)}",
        "oxigeno": random.randint(90, 100),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Guardar en MongoDB en colección "signos_vitales"
    try:
        db["signos_vitales"].insert_one(lectura.copy())
        print(f"📥 Signos vitales guardados para {lectura['nombre']} (Cédula: {cedula})")
    except Exception as e:
        print(f"⚠️ Error guardando en MongoDB: {e}")
        raise HTTPException(status_code=500, detail="Error al guardar signos vitales")

    return {"status": "ok", "lectura": serialize_mongo(lectura)}


@app.get("/health-data/{cedula}")
def obtener_signos_por_cedula(cedula: str, limit: int = 10):
    """Obtener los últimos signos vitales de un paciente por cédula"""
    if db is None:
        raise HTTPException(status_code=500, detail="Base de datos no disponible")
    
    # Verificar que el paciente existe
    paciente = db["pacientes"].find_one({"cedula": cedula})
    if not paciente:
        raise HTTPException(status_code=404, detail=f"Paciente con cédula {cedula} no encontrado")
    
    # Obtener los últimos registros
    signos = list(
        db["signos_vitales"]
        .find({"cedula": cedula})
        .sort("timestamp", -1)
        .limit(limit)
    )
    
    if not signos:
        return {
            "mensaje": f"No hay signos vitales registrados para {paciente['nombre']} {paciente['apellido']}",
            "cedula": cedula
        }
    
    return {
        "paciente": {
            "cedula": cedula,
            "nombre": f"{paciente['nombre']} {paciente['apellido']}"
        },
        "signos_vitales": serialize_mongo(signos)
    }


@app.get("/health-data")
def obtener_ultimo_signo():
    """Obtener el último signo vital registrado (para compatibilidad)"""
    if db is None:
        raise HTTPException(status_code=500, detail="Base de datos no disponible")
    
    ultimo = db["signos_vitales"].find_one(sort=[("timestamp", -1)])
    if not ultimo:
        raise HTTPException(status_code=404, detail="No hay signos vitales registrados")
    
    return {"status": "ok", "lectura": serialize_mongo(ultimo)}