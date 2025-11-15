FROM python:3.12-slim

# Establece el directorio de trabajo dentro del contenedor.
WORKDIR /app

# Copia el archivo de dependencias.
COPY requirements.txt .

# Instala las dependencias.
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos de la aplicación (código, templates, estáticos).
COPY . .

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

# Exponemos el puerto en el que la aplicación Flask se ejecutará.
EXPOSE 5000

# Flask se ejecutará en todas las interfaces de red (0.0.0.0) en el puerto 5000.
CMD ["python", "app.py"]  
