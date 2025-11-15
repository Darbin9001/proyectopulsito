import redis
import os

# Obtén la URL de la base de datos de las variables de entorno
REDIS_URL = os.getenv("REDIS_URL", "redis://redis-db:6379/0")

# Crea el cliente de Redis
def get_redis_client():
    return redis.from_url(REDIS_URL)

# Ejemplo de uso:
# redis_client = get_redis_client()
# redis_client.set("my_key", "my_value")
# value = redis_client.get("my_key")
