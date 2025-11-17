FROM python:3.11-slim

WORKDIR /app

# Mejorar compatibilidad con requests
RUN apt-get update && apt-get install -y curl && apt-get clean

COPY services/pacientes/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/pacientes/generate_auto_data.py .

ENV PYTHONUNBUFFERED=1

CMD ["python", "generate_auto_data.py"]
