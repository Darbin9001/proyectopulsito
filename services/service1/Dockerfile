# services/service1/Dockerfile
# ==========================================
FROM python:3.11-slim

WORKDIR /app

# Copiar requirements desde el servicio
COPY services/service1/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar módulos compartidos desde services/
COPY services/data_base_mongo.py services/utils.py ./

# Copiar código del servicio
COPY services/service1/ .

ENV PYTHONUNBUFFERED=1

EXPOSE 8002

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
