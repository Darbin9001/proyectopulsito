import os
from dotenv import load_dotenv

# Carga las variables de entorno del archivo .env
# Esto asegura que las configuraciones se obtengan desde el entorno de ejecución,
# lo que es una buena práctica para entornos de desarrollo y producción.
load_dotenv()

# TODO: Define una clase para agrupar las configuraciones.
class Settings:
    """Clase para gestionar las configuraciones de la aplicación."""
    
    # URLs de los servicios
    # La URL del API Gateway se obtiene de las variables de entorno.
    API_GATEWAY_URL: str = os.getenv("API_GATEWAY_URL", "http://localhost:8000")
    
    # TODO: Agrega las URLs de los microservicios si son necesarias aquí.
    # Por ejemplo, para pruebas o scripts de utilidades.
    # AUTH_SERVICE_URL: str = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8001")
    # CATALOG_SERVICE_URL: str = os.getenv("CATALOG_SERVICE_URL", "http://catalog-service:8002")

    # TODO: Agrega otras configuraciones globales.
    # Por ejemplo, una clave secreta para la autenticación o el token JWT.
    # SECRET_KEY: str = os.getenv("SECRET_KEY", "tu-clave-secreta-muy-segura")
    # ALGORITHM: str = "HS256"

# Crea una instancia de la clase de configuración.
settings = Settings()

# --------------------------------------------------------------------------
# Los estudiantes pueden importar este objeto settings en cualquier parte 
# de su código para acceder a las configuraciones de manera consistente.
# 
# Ejemplo de uso en un microservicio
# from common.config import settings
# 
# Ahora puedes acceder a las variables de configuración
# api_url = settings.API_GATEWAY_URL
# 