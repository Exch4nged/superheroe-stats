# Hero Scout CLI

## Descripción del proyecto
Hero Scout CLI es una solución de software profesional orientada a la comparación de estadísticas de superhéroes mediante una API externa. La aplicación realiza una consulta puntual a la SuperHero API, procesa los datos y entrega un resultado por consola de forma clara, rápida y automatizable.

## Autor
- **Nombre:** Axl Urrutia
- **Carrera:** Ingeniería en Conectividad y Redes

## Stakeholder
El stakeholder de esta herramienta es un analista gamer, creador de contenido geek o estudiante que necesita comparar rápidamente dos superhéroes para tomar decisiones, generar contenido o analizar sus estadísticas sin buscar manualmente en múltiples páginas.

## Problema
Comparar superhéroes manualmente en distintos sitios web consume tiempo, genera distracciones y puede llevar a errores o datos inconsistentes.

## Solución / Propuesta de valor
La aplicación permite comparar dos superhéroes automáticamente y mostrar en consola tres métricas principales:
- Fuerza
- Velocidad
- Combate

Además entrega información complementaria:
- Nombre
- Nombre real
- Publisher

## Variables de entorno
La aplicación requiere las siguientes variables de entorno:

- `SUPERHERO_TOKEN`: token de acceso a la SuperHero API
- `HERO_1`: nombre del primer héroe
- `HERO_2`: nombre del segundo héroe

### Linux / Bash
```bash
export SUPERHERO_TOKEN="49161a06b6a6cf05bc4bc8fe747f047f"
export HERO_1="batman"
export HERO_2="superman"
