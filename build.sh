#!/bin/bash
# Script de automatización: genera Dockerfile, construye imagen Docker y ejecuta contenedor
# Autor: Axl Urrutia | DRY7122

# Crea la carpeta de evidencias si no existe
mkdir -p evidencias/docker

echo "Limpiando contenedor anterior si existe..."
# Detiene el contenedor si está corriendo (ignora error si no existe)
docker stop samplerunning 2>/dev/null
# Elimina el contenedor si existe (ignora error si no existe)
docker rm samplerunning 2>/dev/null

echo "Creando Dockerfile..."
# Genera el Dockerfile automáticamente con heredoc
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
# Construye la imagen con el tag superhero-app
docker build -t superhero-app .

echo "Ejecutando contenedor..."
# Ejecuta el contenedor pasando variables de entorno para modo automático
# La salida completa se guarda en output.txt como evidencia
docker run --name samplerunning \
  -e SUPERHERO_TOKEN="${SUPERHERO_TOKEN}" \
  -e HERO_1="batman" \
  -e HERO_1_I="1" \
  -e HERO_2="superman" \
  -e HERO_2_I="2" \
  superhero-app 2>&1 | tee evidencias/docker/output.txt

# Agrega el estado del contenedor al archivo de evidencias
echo "" >> evidencias/docker/output.txt
echo "========== docker ps -a ==========" >> evidencias/docker/output.txt
docker ps -a >> evidencias/docker/output.txt

echo "Proceso finalizado. Revisar evidencias/docker/output.txt"
