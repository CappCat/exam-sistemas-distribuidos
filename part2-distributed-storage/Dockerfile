FROM python:3.11-slim

# Información de la imagen:
# - copia el código de la app
# - instala dependencias desde requirements.txt
# - ejecuta storage_system.py

WORKDIR /app

# Evitar buffers en salida para ver logs inmediatamente
ENV PYTHONUNBUFFERED=1

# Copiar requirements (si existe) e instalar dependencias
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . /app

# Por defecto ejecutamos el script principal
CMD ["python", "storage_system.py"]

