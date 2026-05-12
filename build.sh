#!/bin/bash

mkdir -p evidencias/docker

echo "Limpiando contenedor anterior si existe..."
docker stop samplerunning 2>/dev/null
docker rm samplerunning 2>/dev/null

echo "Creando Dockerfile..."
cat > Dockerfile <<EOF
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
CMD ["python3", "app.py"]
EOF

echo "Construyendo imagen Docker..."
docker build -t superhero-app .

echo "Ejecutando contenedor..."
docker run --name samplerunning \
  -e SUPERHERO_TOKEN="${SUPERHERO_TOKEN}" \
  -e HERO_1="batman" \
  -e HERO_1_I="1" \
  -e HERO_2="superman" \
  -e HERO_2_I="2" \
  superhero-app > evidencias/docker/output.txt 2>&1

echo "" >> evidencias/docker/output.txt
echo "========== docker ps -a ==========" >> evidencias/docker/output.txt
docker ps -a >> evidencias/docker/output.txt

echo "Proceso finalizado. Revisar evidencias/docker/output.txt"
