FROM python:3.11-slim

WORKDIR /app

# Copiar requirements del agente
COPY my_agent/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del agente
COPY my_agent/ ./my_agent/

# Copiar el archivo .env si existe (para las variables de entorno)
COPY .env* ./

ENV PYTHONUNBUFFERED=1

# El bot de Telegram no expone un puerto, solo escucha eventos
CMD ["python", "-m", "my_agent.telegram_bot"]