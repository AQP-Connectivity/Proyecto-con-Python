FROM python:3-slim
# Usa una imagen ligera de Python 3 como base del contenedor

ENV PYTHONDONTWRITEBYTECODE=1
# Evita que Python genere archivos .pyc dentro del contenedor

ENV PYTHONUNBUFFERED=1
# Muestra los logs de Python en tiempo real sin usar buffers

COPY requirements.txt .
# Copia el archivo de dependencias al sistema de archivos del contenedor

RUN python -m pip install -r requirements.txt
# Instala las dependencias listadas en requirements.txt

WORKDIR /app
# Define /app como el directorio de trabajo dentro del contenedor

COPY . /app
# Copia todos los archivos del proyecto al directorio /app

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# Crea un usuario no-root llamado appuser y asigna permisos sobre /app

USER appuser
# A partir de aquí, todos los comandos se ejecutan como appuser

CMD ["python", "Estructura del Proyecto/app.py"]
# Comando que se ejecuta al iniciar el contenedor (arranca tu aplicación)
