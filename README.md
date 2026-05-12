# Hero Scout CLI
## Descripción del proyecto
Hero Scout CLI es una solución de software profesional orientada a la comparación de estadísticas de superhéroes mediante una API externa. La aplicación realiza una consulta puntual a la SuperHero API, procesa los datos y entrega un resultado por consola de forma clara, rápida y automatizable.

## Autor
- **Nombre:** Axl Urrutia
- **Correo:** ax.urrutia@duocuc.cl
- **Carrera:** Ingeniería en Conectividad y Redes
- **Asignatura:** Programación y Redes Virtualizadas (DRY7122)

## Stakeholder
El stakeholder es un analista gamer, creador de contenido geek o estudiante que necesita comparar rápidamente dos superhéroes para tomar decisiones, generar contenido o analizar estadísticas sin buscar manualmente en múltiples páginas.

## Problema
Comparar superhéroes manualmente en distintos sitios web consume tiempo, genera distracciones y puede llevar a errores o datos inconsistentes.

## Solución / Propuesta de valor
La aplicación busca héroes por nombre, muestra una lista de resultados para elegir con precisión y compara 6 estadísticas:
- Inteligencia
- Fuerza
- Velocidad
- Durabilidad
- Poder
- Combate

Además entrega información complementaria: nombre real, editorial y alineación.

## Variables de entorno
| Variable | Descripción |
|---|---|
| `SUPERHERO_TOKEN` | Token de acceso a la SuperHero API |
| `HERO_1` | Nombre del primer héroe a buscar |
| `HERO_1_I` | Índice del resultado a elegir para héroe 1 |
| `HERO_2` | Nombre del segundo héroe a buscar |
| `HERO_2_I` | Índice del resultado a elegir para héroe 2 |

### Configurar variables (Linux/Bash)
```bash
export SUPERHERO_TOKEN="tu_token_aqui"
export HERO_1="batman"
export HERO_1_I="1"
export HERO_2="superman"
export HERO_2_I="2"
```

## Ejecución local
```bash
pip install -r requirements.txt
export SUPERHERO_TOKEN="tu_token_aqui"
python3 app.py
```

## Ejecución con Docker
```bash
# Construir y ejecutar automáticamente
export SUPERHERO_TOKEN="tu_token_aqui"
chmod +x build.sh
./build.sh

# Ver resultado
cat evidencias/docker/output.txt
```

## Estructura del proyecto
```
superheroe-stats/
├── app.py              # Script principal que consulta la API
├── build.sh            # Script de automatización Docker
├── requirements.txt    # Dependencias Python
├── .gitignore
├── README.md
└── evidencias/
    ├── docker/
    │   ├── output.txt      # docker ps -a + logs con datos reales
    │   └── screenshot.png  # Captura de salida en consola
    └── jenkins/
        ├── stage_view.png
        ├── console_output_build.png
        ├── credentials.png
        └── pipeline_script.txt
```
