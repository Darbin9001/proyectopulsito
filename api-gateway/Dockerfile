FROM python:3.12-slim

# Establece el directorio de trabajo.
WORKDIR /app

# Copia el archivo de dependencias.
COPY requirements.txt .

# Instala las dependencias.
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código.
COPY . .

# Define el comando para ejecutar la aplicación.
# El puerto debe ser el mismo que se expone en docker-compose.yml (8000).
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
