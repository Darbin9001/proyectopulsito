import json
import requests
from typing import Any

# TODO: Define funciones de ayuda que puedan ser útiles en varios microservicios.

def send_request_to_service(url: str, method: str = "GET", data: Any = None):
    """
    Envía una petición HTTP a otro microservicio.
    
    Args:
        url (str): La URL completa del endpoint.
        method (str): El método HTTP (GET, POST, PUT, DELETE).
        data (Any): Los datos a enviar en el cuerpo de la petición (para POST/PUT).
    
    Returns:
        dict: La respuesta del servicio en formato JSON.
    
    Raises:
        requests.exceptions.RequestException: Si la petición falla.
    """
    try:
        response = requests.request(method, url, json=data)
        response.raise_for_status()  # Lanza una excepción si la respuesta es un error
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error en la petición: {e}")
        raise e


def format_date(dt_object: datetime):
    """Formatea un objeto datetime a una cadena de texto."""
    return dt_object.strftime("%Y-%m-%d %H:%M:%S")

# TODO: Agrega más funciones de utilidad según sea necesario.

# ------------------------------------------------------------------------------
# Ejemplo de uso en un microservicio
# from common.helpers.utils import send_request_to_service
# from common.config import settings
# 
# URL del servicio de autenticación
# auth_url = f"{settings.AUTH_SERVICE_URL}/users"
# 
# try:
#     # Envía una petición para obtener todos los usuarios del servicio de autenticación
#     users = send_request_to_service(auth_url)
#     print("Usuarios obtenidos:", users)
# except requests.exceptions.RequestException:
#     print("No se pudo obtener la lista de usuarios.")
#