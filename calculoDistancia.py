import requests

# Tu clave de API de OpenRouteService
ORS_API_KEY = "5b3ce3597851110001cf6248eeb850562bc34d329aca00efb8694718"

def obtener_matriz_distancias_y_tiempos(puntos):
    url = "https://api.openrouteservice.org/v2/matrix"
    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "locations": puntos,  # Lista de puntos
        "metrics": ["distance", "duration"],  # Obtener distancias y tiempos
        "units": "km"  # Resultados en kilómetros
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Lanza un error para códigos de estado HTTP 4xx o 5xx

        data = response.json()
        if "distances" in data and "durations" in data:
            return data["distances"], data["durations"]
        else:
            print(f"Respuesta inesperada: {data}")
            return None, None

    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
        return None, None

# Ejemplo de uso
# Coordenadas: [latitud, longitud]
puntos = [
    [-34.9011, -56.1645],  # Montevideo
    [-34.94747, -54.93382],  # Punta del Este
    [-34.79123, -54.91824],  # San Carlos
    [-33.11651, -58.31067],  # Fray Bentos
    [-30.90534, -55.55076],  # Rivera
    # Agrega más puntos según sea necesario
]

matriz_distancias, matriz_tiempos = obtener_matriz_distancias_y_tiempos(puntos)

# Verificar si se obtuvieron resultados válidos
if matriz_distancias is not None and matriz_tiempos is not None:
    for i, fila in enumerate(matriz_distancias):
        print(f"Distancias desde el punto {i + 1}: {fila}")
        print(f"Tiempos desde el punto {i + 1} (en segundos): {matriz_tiempos[i]}")
else:
    print("No se pudo obtener la matriz de distancias y tiempos.")
