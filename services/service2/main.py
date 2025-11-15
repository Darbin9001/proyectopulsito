from fastapi import FastAPI, HTTPException
import httpx
import asyncio
import datetime
import json
import os

app = FastAPI(title="Servicio 2 - Análisis de Datos de Salud")

SERVICE1_URL = os.getenv("NAME1_SERVICE_URL", "http://127.0.0.1:8001")
DATA_FILE = "data_history.json"
data_history = {}  # Cambiar a diccionario para organizar por cédula


# --- Cargar historial previo si existe ---
def load_data():
    global data_history
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                data_history = json.load(f)
                print(f"✅ Historial cargado ({sum(len(v) for v in data_history.values())} registros).")
            except json.JSONDecodeError:
                print("⚠️ Archivo JSON vacío o dañado, iniciando nuevo historial.")
                data_history = {}
    else:
        print("📁 No se encontró historial previo, iniciando nuevo archivo.")


# --- Guardar historial en archivo ---
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data_history, f, indent=4, ensure_ascii=False)


# --- Analizar datos recibidos ---
def analyze(data):
    bpm = data.get("ritmo_cardiaco", 0)
    temp = data.get("temperatura", 0)
    oxigeno = data.get("oxigeno", 100)
    alertas = []

    if bpm > 100:
        alertas.append("⚠️ Ritmo cardíaco alto (posible taquicardia)")
    elif bpm < 60:
        alertas.append("⚠️ Ritmo cardíaco bajo (posible bradicardia)")
    
    if temp > 38:
        alertas.append("🌡️ Fiebre detectada")
    elif temp < 36:
        alertas.append("❄️ Hipotermia detectada")
    
    if oxigeno < 95:
        alertas.append("🫁 Saturación de oxígeno baja")

    return alertas if alertas else ["✅ Todo en rangos normales"]


# --- Endpoints ---
@app.get("/")
def root():
    return {"message": "Servicio 2 activo - Análisis por paciente"}


@app.get("/analyze/{cedula}")
def analizar_por_cedula(cedula: str):
    """Obtener el último análisis de signos vitales de un paciente"""
    try:
        # Obtener datos del service1
        import requests
        response = requests.get(f"{SERVICE1_URL}/health-data/{cedula}?limit=1")
        
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"No hay datos para la cédula {cedula}")
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error al consultar signos vitales")
        
        data = response.json()
        
        if "signos_vitales" not in data or not data["signos_vitales"]:
            raise HTTPException(status_code=404, detail="No hay signos vitales disponibles")
        
        ultimo_signo = data["signos_vitales"][0]
        alertas = analyze(ultimo_signo)
        
        resultado = {
            "paciente": data["paciente"],
            "timestamp": ultimo_signo.get("timestamp"),
            "datos": {
                "ritmo_cardiaco": ultimo_signo.get("ritmo_cardiaco"),
                "temperatura": ultimo_signo.get("temperatura"),
                "presion": ultimo_signo.get("presion"),
                "oxigeno": ultimo_signo.get("oxigeno")
            },
            "alertas": alertas
        }
        
        # Guardar en historial
        if cedula not in data_history:
            data_history[cedula] = []
        
        data_history[cedula].append(resultado)
        
        # Mantener solo últimos 50 registros por paciente
        if len(data_history[cedula]) > 50:
            data_history[cedula] = data_history[cedula][-50:]
        
        save_data()
        
        return resultado
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/historial/{cedula}")
def obtener_historial(cedula: str, limit: int = 20):
    """Obtener el historial de análisis de un paciente"""
    if cedula not in data_history or not data_history[cedula]:
        raise HTTPException(
            status_code=404, 
            detail=f"No hay historial para la cédula {cedula}"
        )
    
    registros = data_history[cedula][-limit:] if len(data_history[cedula]) > limit else data_history[cedula]
    
    return {
        "cedula": cedula,
        "total_registros": len(data_history[cedula]),
        "registros_mostrados": len(registros),
        "historial": registros
    }


@app.get("/pacientes")
def listar_pacientes_con_datos():
    """Listar todos los pacientes que tienen datos registrados"""
    if not data_history:
        return {"mensaje": "No hay datos almacenados", "pacientes": []}
    
    resumen = []
    for cedula, registros in data_history.items():
        if registros:
            ultimo = registros[-1]
            resumen.append({
                "cedula": cedula,
                "nombre": ultimo.get("paciente", {}).get("nombre", "Desconocido"),
                "total_registros": len(registros),
                "ultimo_registro": ultimo.get("timestamp"),
                "ultima_alerta": ultimo.get("alertas", [])
            })
    
    return {"total_pacientes": len(resumen), "pacientes": resumen}


# --- Al iniciar el servicio ---
@app.on_event("startup")
async def startup_event():
    load_data()
    print("✅ Servicio 2 iniciado")