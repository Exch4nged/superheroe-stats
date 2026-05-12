import os       # Para leer variables de entorno del sistema
import sys      # Para salir del programa con códigos de error
import requests # Para hacer peticiones HTTP a la API

# =============================================
# ZONA AZUL — Construcción de la solicitud
# =============================================
TOKEN    = os.getenv("SUPERHERO_TOKEN")   # Lee el token desde variable de entorno (nunca hardcodeado)
HERO_1   = os.getenv("HERO_1")            # Nombre del héroe 1 (modo automático Docker/Jenkins)
HERO_1_I = os.getenv("HERO_1_I")          # Índice del resultado a elegir para héroe 1
HERO_2   = os.getenv("HERO_2")            # Nombre del héroe 2 (modo automático Docker/Jenkins)
HERO_2_I = os.getenv("HERO_2_I")          # Índice del resultado a elegir para héroe 2


def buscar_heroe(nombre):
    """Busca héroes por nombre en la SuperHero API y retorna lista de resultados."""

    if not TOKEN: # Verifica que el token esté definido antes de hacer la petición
        raise ValueError("No se encontró la variable de entorno SUPERHERO_TOKEN.")

    url = f"https://superheroapi.com/api/{TOKEN}/search/{nombre}" # Construye la URL con el token y nombre

    # =============================================
    # ZONA VERDE — Llamada HTTP (GET)
    # =============================================
    try:
        respuesta = requests.get(url, timeout=5) # Realiza la petición GET con timeout de 5 segundos

        # =============================================
        # ZONA ROJA — Manejo de errores HTTP
        # =============================================
        if respuesta.status_code == 401: # Token inválido o sin permisos
            raise PermissionError("Error 401: Token inválido o no autorizado.")
        if respuesta.status_code == 404: # Endpoint no existe
            raise FileNotFoundError("Error 404: Endpoint no encontrado.")
        if respuesta.status_code != 200: # Cualquier otro error HTTP inesperado
            raise Exception(f"Error HTTP inesperado: {respuesta.status_code}")

        # =============================================
        # ZONA MORADA — Parseo JSON
        # =============================================
        try:
            datos = respuesta.json() # Convierte la respuesta a diccionario Python
        except ValueError:
            raise ValueError("La respuesta no es un JSON válido.")

        if datos.get("response") == "error": # La API retorna "error" si no encuentra el héroe
            raise LookupError(f"'{nombre}' no fue encontrado. Intenta en inglés.")

        return datos["results"] # Retorna la lista de héroes encontrados

    # =============================================
    # ZONA NARANJA — Errores de red
    # =============================================
    except requests.exceptions.ConnectionError: # Sin internet o API caída
        raise ConnectionError("Sin conexión a internet. Revisa tu red.")
    except requests.exceptions.Timeout: # La API no respondió en 5 segundos
        raise TimeoutError("El servidor tardó más de 5 segundos. Intenta de nuevo.")


def elegir_de_lista(resultados, nombre_buscado, indice_auto=None):
    """Muestra lista numerada y permite elegir. En modo automático usa indice_auto."""

    if len(resultados) > 1: # Si hay más de un resultado muestra la lista
        print(f"\n  Se encontraron {len(resultados)} resultados para '{nombre_buscado}':")
        for i, r in enumerate(resultados): # Itera e imprime cada resultado numerado
            publisher = r["biography"].get("publisher", "Desconocido")
            print(f"    {i+1}. {r['name']} ({publisher})")

        if indice_auto is not None: # Modo automático: usa el índice de la variable de entorno
            eleccion = str(indice_auto)
            print(f"  Selección automática: {eleccion}")
        else: # Modo interactivo: el usuario escribe el número
            eleccion = input("\n  Elige un número: ").strip()

        if not eleccion.isdigit() or int(eleccion) < 1 or int(eleccion) > len(resultados):
            raise ValueError("Opción no válida.") # Valida que la elección esté en rango

        return resultados[int(eleccion) - 1] # Retorna el héroe elegido (índice base 0)
    else:
        return resultados[0] # Si hay solo un resultado lo retorna directamente


def extraer_datos(personaje):
    """Extrae los 6 campos relevantes del personaje desde el JSON de la API."""
    try:
        nombre        = personaje["name"]                              # Nombre del héroe
        nombre_real   = personaje["biography"].get("full-name", "N/A") # Identidad secreta
        publisher     = personaje["biography"].get("publisher", "N/A") # Editorial (DC, Marvel, etc)
        alineacion    = personaje["biography"].get("alignment", "N/A") # Bueno, malo o neutral
        fuerza        = personaje["powerstats"]["strength"]             # Campo 1: fuerza física
        velocidad     = personaje["powerstats"]["speed"]                # Campo 2: velocidad
        combate       = personaje["powerstats"]["combat"]               # Campo 3: habilidad de combate
        inteligencia  = personaje["powerstats"]["intelligence"]         # Campo 4: inteligencia
        poder         = personaje["powerstats"]["power"]                # Campo 5: poder especial
        durabilidad   = personaje["powerstats"]["durability"]           # Campo 6: resistencia al daño
    except KeyError as e:
        raise KeyError(f"Falta una clave esperada en el JSON: {e}")

    return { # Retorna diccionario con todos los datos extraídos
        "nombre":       nombre,
        "nombre_real":  nombre_real,
        "publisher":    publisher,
        "alineacion":   alineacion,
        "fuerza":       fuerza,
        "velocidad":    velocidad,
        "combate":      combate,
        "inteligencia": inteligencia,
        "poder":        poder,
        "durabilidad":  durabilidad,
    }


def comparar_stat(etiqueta, v1, v2, n1, n2):
    """Compara un stat entre dos héroes y retorna 1 si gana h1, -1 si gana h2, 0 si empatan."""
    try:
        i1 = int(v1) # Convierte a entero para comparar numéricamente
        i2 = int(v2)
    except (TypeError, ValueError):
        i1 = i2 = 0 # Si el valor es null o inválido, trata como 0

    print(f"\n  {etiqueta}:")
    print(f"    {n1}: {v1}/100")
    print(f"    {n2}: {v2}/100")

    if i1 > i2: # Héroe 1 tiene mayor stat
        print(f"    >> Ganador: {n1}")
        return 1
    elif i2 > i1: # Héroe 2 tiene mayor stat
        print(f"    >> Ganador: {n2}")
        return -1
    else: # Ambos tienen el mismo valor
        print(f"    >> Empate")
        return 0


def flujo_heroe(numero, nombre_auto, indice_auto):
    """Maneja el flujo completo de búsqueda y selección de un héroe."""
    if nombre_auto: # Modo automático (Docker/Jenkins): usa variables de entorno
        nombre = nombre_auto
        print(f"\n  [Modo automático] Héroe {numero}: '{nombre}'")
    else: # Modo interactivo: pide input al usuario
        nombre = input(f"\nBuscar héroe {numero} (en inglés): ").strip()
        if not nombre:
            raise ValueError("El nombre no puede estar vacío.")

    resultados = buscar_heroe(nombre)          # Consulta la API
    personaje  = elegir_de_lista(resultados, nombre, indice_auto) # Usuario o auto elige
    return extraer_datos(personaje)            # Extrae y retorna los datos


def mostrar_comparacion(h1, h2):
    """Muestra la comparación completa entre dos héroes y determina el ganador general."""
    print("\n" + "=" * 45)
    print(f"  {h1['nombre']} vs {h2['nombre']}") # Título del enfrentamiento
    print("=" * 45)
    # Muestra datos biográficos de cada héroe
    print(f"  {h1['nombre']}: {h1['nombre_real']} | {h1['publisher']} | {h1['alineacion']}")
    print(f"  {h2['nombre']}: {h2['nombre_real']} | {h2['publisher']} | {h2['alineacion']}")
    print("\n  COMPARACIÓN DE STATS:")

    puntos  = 0 # Acumulador de puntos para determinar ganador general
    # Compara cada stat y acumula puntos (+ = gana h1, - = gana h2)
    puntos += comparar_stat("Inteligencia", h1["inteligencia"], h2["inteligencia"], h1["nombre"], h2["nombre"])
    puntos += comparar_stat("Fuerza",       h1["fuerza"],       h2["fuerza"],       h1["nombre"], h2["nombre"])
    puntos += comparar_stat("Velocidad",    h1["velocidad"],    h2["velocidad"],     h1["nombre"], h2["nombre"])
    puntos += comparar_stat("Durabilidad",  h1["durabilidad"],  h2["durabilidad"],  h1["nombre"], h2["nombre"])
    puntos += comparar_stat("Poder",        h1["poder"],        h2["poder"],         h1["nombre"], h2["nombre"])
    puntos += comparar_stat("Combate",      h1["combate"],      h2["combate"],       h1["nombre"], h2["nombre"])

    print("\n" + "=" * 45)
    if puntos > 0:      # h1 ganó más stats
        print(f"  GANADOR GENERAL: {h1['nombre']} 🏆")
    elif puntos < 0:    # h2 ganó más stats
        print(f"  GANADOR GENERAL: {h2['nombre']} 🏆")
    else:               # Misma cantidad de stats ganados
        print("  RESULTADO: Empate total")
    print("=" * 45)
    print("\nComparación completada correctamente.")


def main():
    """Función principal — punto de entrada del programa."""
    print("\n" + "=" * 45)
    print("  SUPERHERO STATS ANALYZER")
    print("  Comparador profesional de superhéroes")
    print("  Axl Urrutia | DRY7122")
    print("=" * 45)

    # Detecta si está en modo automático (variables de entorno definidas)
    modo_auto = HERO_1 and HERO_2

    try:
        if modo_auto: # Docker/Jenkins: usa variables de entorno para seleccionar héroes
            print("\n  Modo automático activado (Docker/Jenkins)")
            h1 = flujo_heroe(1, HERO_1, HERO_1_I)
            h2 = flujo_heroe(2, HERO_2, HERO_2_I)
            mostrar_comparacion(h1, h2) # Muestra resultado y termina
            sys.exit(0) # Salida exitosa — contenedor termina con código 0

        else: # Modo interactivo: loop para múltiples comparaciones
            print("\n  Modo interactivo — escribe 'salir' para terminar")
            while True:
                entrada = input("\n¿Deseas comparar dos héroes? (s/salir): ").strip().lower()
                if entrada == "salir": # El usuario puede salir cuando quiera
                    print("¡Hasta la próxima!")
                    sys.exit(0)

                h1 = flujo_heroe(1, None, None)
                h2 = flujo_heroe(2, None, None)

                if h1["nombre"] == h2["nombre"]: # No permite comparar un héroe consigo mismo
                    print("  Elige dos héroes diferentes.")
                    continue

                mostrar_comparacion(h1, h2) # Muestra comparación y vuelve al inicio del loop

    # Captura cada tipo de error con mensaje descriptivo para el usuario
    except ValueError as e:
        print(f"\nERROR - Entrada/Configuración: {e}")
        sys.exit(1)
    except ConnectionError as e:
        print(f"\nERROR - Conexión: {e}")
        sys.exit(1)
    except TimeoutError as e:
        print(f"\nERROR - Timeout: {e}")
        sys.exit(1)
    except PermissionError as e:
        print(f"\nERROR - Autenticación 401: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"\nERROR - 404: {e}")
        sys.exit(1)
    except LookupError as e:
        print(f"\nERROR - Búsqueda: {e}")
        sys.exit(1)
    except KeyError as e:
        print(f"\nERROR - Parseo JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR - Inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() # Ejecuta el programa solo si se llama directamente (no si se importa)
