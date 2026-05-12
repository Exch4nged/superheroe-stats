import os
import sys
import requests

# =============================================
# ZONA AZUL — Construcción de la solicitud
# =============================================
TOKEN    = os.getenv("SUPERHERO_TOKEN")   # NUNCA hardcodeado
HERO_1   = os.getenv("HERO_1")            # Modo automático: nombre héroe 1
HERO_1_I = os.getenv("HERO_1_I")          # Modo automático: índice resultado 1
HERO_2   = os.getenv("HERO_2")            # Modo automático: nombre héroe 2
HERO_2_I = os.getenv("HERO_2_I")          # Modo automático: índice resultado 2


def buscar_heroe(nombre):
    """Busca héroes por nombre y retorna lista de resultados."""

    if not TOKEN:
        raise ValueError("No se encontró la variable de entorno SUPERHERO_TOKEN.")

    url = f"https://superheroapi.com/api/{TOKEN}/search/{nombre}"

    # =============================================
    # ZONA VERDE — Llamada HTTP (GET)
    # =============================================
    try:
        respuesta = requests.get(url, timeout=5)

        # =============================================
        # ZONA ROJA — Manejo de errores HTTP
        # =============================================
        if respuesta.status_code == 401:
            raise PermissionError("Error 401: Token inválido o no autorizado.")
        if respuesta.status_code == 404:
            raise FileNotFoundError("Error 404: Endpoint no encontrado.")
        if respuesta.status_code != 200:
            raise Exception(f"Error HTTP inesperado: {respuesta.status_code}")

        # =============================================
        # ZONA MORADA — Parseo JSON
        # =============================================
        try:
            datos = respuesta.json()
        except ValueError:
            raise ValueError("La respuesta no es un JSON válido.")

        if datos.get("response") == "error":
            raise LookupError(f"'{nombre}' no fue encontrado. Intenta en inglés.")

        return datos["results"]

    # =============================================
    # ZONA NARANJA — Errores de red
    # =============================================
    except requests.exceptions.ConnectionError:
        raise ConnectionError("Sin conexión a internet. Revisa tu red.")
    except requests.exceptions.Timeout:
        raise TimeoutError("El servidor tardó más de 5 segundos. Intenta de nuevo.")


def elegir_de_lista(resultados, nombre_buscado, indice_auto=None):
    """Muestra lista y permite elegir. En modo auto usa indice_auto."""

    if len(resultados) > 1:
        print(f"\n  Se encontraron {len(resultados)} resultados para '{nombre_buscado}':")
        for i, r in enumerate(resultados):
            publisher = r["biography"].get("publisher", "Desconocido")
            print(f"    {i+1}. {r['name']} ({publisher})")

        if indice_auto is not None:
            eleccion = str(indice_auto)
            print(f"  Selección automática: {eleccion}")
        else:
            eleccion = input("\n  Elige un número: ").strip()

        if not eleccion.isdigit() or int(eleccion) < 1 or int(eleccion) > len(resultados):
            raise ValueError("Opción no válida.")

        return resultados[int(eleccion) - 1]
    else:
        return resultados[0]


def extraer_datos(personaje):
    """Extrae los campos relevantes del personaje."""
    try:
        nombre        = personaje["name"]
        nombre_real   = personaje["biography"].get("full-name", "N/A")
        publisher     = personaje["biography"].get("publisher", "N/A")
        alineacion    = personaje["biography"].get("alignment", "N/A")
        fuerza        = personaje["powerstats"]["strength"]      # Campo 1
        velocidad     = personaje["powerstats"]["speed"]         # Campo 2
        combate       = personaje["powerstats"]["combat"]        # Campo 3
        inteligencia  = personaje["powerstats"]["intelligence"]  # Campo 4
        poder         = personaje["powerstats"]["power"]         # Campo 5
        durabilidad   = personaje["powerstats"]["durability"]    # Campo 6
    except KeyError as e:
        raise KeyError(f"Falta una clave esperada en el JSON: {e}")

    return {
        "nombre":      nombre,
        "nombre_real": nombre_real,
        "publisher":   publisher,
        "alineacion":  alineacion,
        "fuerza":      fuerza,
        "velocidad":   velocidad,
        "combate":     combate,
        "inteligencia":inteligencia,
        "poder":       poder,
        "durabilidad": durabilidad,
    }


def comparar_stat(etiqueta, v1, v2, n1, n2):
    """Muestra comparación de un stat y retorna 1, -1 o 0."""
    try:
        i1 = int(v1)
        i2 = int(v2)
    except (TypeError, ValueError):
        i1 = i2 = 0

    print(f"\n  {etiqueta}:")
    print(f"    {n1}: {v1}/100")
    print(f"    {n2}: {v2}/100")

    if i1 > i2:
        print(f"    >> Ganador: {n1}")
        return 1
    elif i2 > i1:
        print(f"    >> Ganador: {n2}")
        return -1
    else:
        print(f"    >> Empate")
        return 0


def flujo_heroe(numero, nombre_auto, indice_auto):
    """Maneja búsqueda y selección de un héroe (manual o automático)."""
    if nombre_auto:
        nombre = nombre_auto
        print(f"\n  [Modo automático] Héroe {numero}: '{nombre}'")
    else:
        nombre = input(f"\nBuscar héroe {numero} (en inglés): ").strip()
        if not nombre:
            raise ValueError("El nombre no puede estar vacío.")

    resultados = buscar_heroe(nombre)
    personaje  = elegir_de_lista(resultados, nombre, indice_auto)
    return extraer_datos(personaje)


def main():
    print("\n" + "=" * 45)
    print("  SUPERHERO STATS ANALYZER")
    print("  Comparador profesional de superhéroes")
    print("  Axl Urrutia | DRY7122")
    print("=" * 45)

    modo_auto = HERO_1 and HERO_2

    try:
        if modo_auto:
            print("\n  Modo automático activado (Docker/Jenkins)")
            h1 = flujo_heroe(1, HERO_1, HERO_1_I)
            h2 = flujo_heroe(2, HERO_2, HERO_2_I)

        else:
            # Modo interactivo: permite múltiples comparaciones
            print("\n  Modo interactivo — escribe 'salir' para terminar")
            while True:
                entrada = input("\n¿Deseas comparar dos héroes? (s/salir): ").strip().lower()
                if entrada == "salir":
                    print("¡Hasta la próxima!")
                    sys.exit(0)

                h1 = flujo_heroe(1, None, None)
                h2 = flujo_heroe(2, None, None)

                if h1["nombre"] == h2["nombre"]:
                    print("  Elige dos héroes diferentes.")
                    continue

                mostrar_comparacion(h1, h2)

        if modo_auto:
            mostrar_comparacion(h1, h2)

        sys.exit(0)

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


def mostrar_comparacion(h1, h2):
    print("\n" + "=" * 45)
    print(f"  {h1['nombre']} vs {h2['nombre']}")
    print("=" * 45)
    print(f"  {h1['nombre']}: {h1['nombre_real']} | {h1['publisher']} | {h1['alineacion']}")
    print(f"  {h2['nombre']}: {h2['nombre_real']} | {h2['publisher']} | {h2['alineacion']}")
    print("\n  COMPARACIÓN DE STATS:")

    puntos  = 0
    puntos += comparar_stat("Inteligencia", h1["inteligencia"], h2["inteligencia"], h1["nombre"], h2["nombre"])
    puntos += comparar_stat("Fuerza",       h1["fuerza"],       h2["fuerza"],       h1["nombre"], h2["nombre"])
    puntos += comparar_stat("Velocidad",    h1["velocidad"],    h2["velocidad"],     h1["nombre"], h2["nombre"])
    puntos += comparar_stat("Durabilidad",  h1["durabilidad"],  h2["durabilidad"],  h1["nombre"], h2["nombre"])
    puntos += comparar_stat("Poder",        h1["poder"],        h2["poder"],         h1["nombre"], h2["nombre"])
    puntos += comparar_stat("Combate",      h1["combate"],      h2["combate"],       h1["nombre"], h2["nombre"])

    print("\n" + "=" * 45)
    if puntos > 0:
        print(f"  GANADOR GENERAL: {h1['nombre']} 🏆")
    elif puntos < 0:
        print(f"  GANADOR GENERAL: {h2['nombre']} 🏆")
    else:
        print("  RESULTADO: Empate total")
    print("=" * 45)
    print("\nComparación completada correctamente.")


if __name__ == "__main__":
    main()
