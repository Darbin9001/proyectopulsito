FROM python:3.11-slim

WORKDIR /app

# Copiar requirements primero (mejor cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar archivos del servicio
COPY . .

# Copiar módulos compartidos
COPY ../data_base_mongo.py /app/services/
COPY ../utils.py /app/services/

# Variables de entorno por defecto
ENV PYTHONUNBUFFERED=1

# Exponer puerto
EXPOSE 8003

# Comando de inicio
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]