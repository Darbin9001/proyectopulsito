FROM python:3.12-slim

WORKDIR /app

# Copiar requirements desde api-gateway
COPY api-gateway/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código del api-gateway
COPY api-gateway/ .

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]