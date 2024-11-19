import requests
from armarBase import levantarArchivosDataSet



# Tu clave de API de OpenRouteService
ORS_API_KEY = "5b3ce3597851110001cf6248eeb850562bc34d329aca00efb8694718"

def obtener_matriz_distancias_y_tiempos(puntos):
    url = "https://api.openrouteservice.org/v2/matrix/driving-car"
    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "locations": puntos,  # Lista de puntos
        "metrics": ["distance"],  # Obtener distancias y tiempos
        "units": "km",  # Resultados en kilómetros
        "radius": 500
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Lanza un error para códigos de estado HTTP 4xx o 5xx

        data = response.json()
        if "distances" in data:
            return data["distances"]
        else:
            print(f"Respuesta inesperada: {data}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
        return None

def obtenerDistancias():
    datos = levantarArchivosDataSet()
    puntos = []

    for ciudad in datos:
        puntos.append([float(ciudad[6]), float(ciudad[5])])

    return obtener_matriz_distancias_y_tiempos(puntos)
