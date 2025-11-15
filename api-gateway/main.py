from fastapi import FastAPI, APIRouter, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

# Define la instancia de la aplicación FastAPI.
app = FastAPI(title="API Gateway Taller Microservicios")

# Configura CORS (Cross-Origin Resource Sharing).
# Esto es esencial para permitir que el frontend se comunique con el gateway.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite peticiones desde cualquier origen (ajustar en producción)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crea un enrutador para las peticiones de los microservicios.
router = APIRouter(prefix="/api/v1")

# Define los microservicios y sus URLs.
# La URL debe coincidir con el nombre del servicio definido en docker-compose.yml.
# El puerto debe ser el del contenedor (ej. auth-service:8001).
SERVICES = {
    "auth": os.getenv("AUTH_SERVICE_URL", "http://auth-service:8000"),
    "service1": os.getenv("NAME1_SERVICE_URL", "http://127.0.0.1:8001"),
    "service2": os.getenv("NAME2_SERVICE_URL", "http://127.0.0.1:8002"),
    "service3": os.getenv("NAME3_SERVICE_URL", "http://127.0.0.1:8003"),
}

# TODO: Implementa una ruta genérica para redirigir peticiones GET.
@router.get("/{service_name}/{path:path}")
async def forward_get(service_name: str, path: str, request: Request):
    if service_name not in SERVICES:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found.")
    
    service_url = f"{SERVICES[service_name]}/{path}"
    
    try:
        response = requests.get(service_url, params=request.query_params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error forwarding request to {service_name}: {e}")

# TODO: Implementa una ruta genérica para redirigir peticiones POST.
@router.post("/{service_name}/{path:path}")
async def forward_post(service_name: str, path: str, request: Request):
    if service_name not in SERVICES:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found.")
    
    service_url = f"{SERVICES[service_name]}/{path}"
    
    try:
        # Pasa los datos JSON del cuerpo de la petición.
        response = requests.post(service_url, json=await request.json())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error forwarding request to {service_name}: {e}")

# TODO: Agrega más rutas para otros métodos HTTP (PUT, DELETE, etc.).

# Incluye el router en la aplicación principal.
app.include_router(router)

# Endpoint de salud para verificar el estado del gateway.
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API Gateway is running."}
