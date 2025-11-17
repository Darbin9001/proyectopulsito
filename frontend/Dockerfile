# Crear el Dockerfile correct
FROM python:3.12-slim

WORKDIR /app

# Copiar requirements desde frontend
COPY frontend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar módulos compartidos desde services/
COPY services/data_base_mongo.py services/utils.py ./

# Copiar código del frontend
COPY frontend/ .

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

EXPOSE 5000

CMD ["python", "app.py"]
