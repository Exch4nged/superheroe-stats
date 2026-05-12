#!/bin/bash
# Script de automatización: genera Dockerfile, construye imagen Docker y ejecuta contenedor
# Autor: Axl Urrutia | DRY7122

mkdir -p evidencias/docker  # Crea la carpeta de evidencias si no existe

echo "Limpiando contenedor anterior si existe..."
docker stop samplerunning 2>/dev/null  # Detiene el contenedor si está corriendo (ignora error si no existe)
docker rm samplerunning 2>/dev/null    # Elimina el contenedor si existe (ignora error si no existe)

echo "Creando Dockerfile..."
cat > Dockerfile <<EOF
# Imagen base oficial de Python 3.11 versión slim (liviana)
FROM python:3.11-slim

# Define el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia e instala las dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el script principal de la aplicación
COPY app.py .

# Comando que se ejecuta al iniciar el contenedor
CMD ["python3", "app.py"]
EOF

echo "Construyendo imagen Docker..."
docker build -t superhero-app .  # Construye la imagen con el tag superhero-app

echo "Ejecutando contenedor..."
docker run --name samplerunning \
  -e SUPERHERO_TOKEN="${SUPERHERO_TOKEN}" \  # Token de API pasado como variable de entorno
  -e HERO_1="batman" \                       # Héroe 1 a buscar
  -e HERO_1_I="1" \                          # Índice del resultado para héroe 1
  -e HERO_2="superman" \                     # Héroe 2 a buscar
  -e HERO_2_I="2" \                          # Índice del resultado para héroe 2
  superhero-app > evidencias/docker/output.txt 2>&1  # Guarda toda la salida en output.txt

echo "" >> evidencias/docker/output.txt
echo "========== docker ps -a ==========" >> evidencias/docker/output.txt
docker ps -a >> evidencias/docker/output.txt  # Registra el estado final del contenedor

echo "Proceso finalizado. Revisar evidencias/docker/output.txt"
