import folium
import requests
import time

# Tu clave de API de OpenRouteService
ORS_API_KEY = "5b3ce3597851110001cf6248eeb850562bc34d329aca00efb8694718"

# Coordenadas de Montevideo
origen = [-34.9011, -56.1645]  # (Latitud, Longitud)

# Coordenadas de las capitales departamentales de Uruguay
destinos = {
    "Punta del Este": [-34.94747, -54.93382],
    "San Carlos": [-34.79123, -54.91824],
    "Aires Puros": [-34.852, -56.183],
    "Estación Porvenir": [-32.37085, -57.85371],
    "Fray Bentos": [-33.11651, -58.31067],
    "Rivera": [-30.90534, -55.55076],
    "Castillos": [-34.19871, -53.85919],
    "Belén": [-30.78716, -57.77577],
    "Mercedes": [-33.2524, -58.03047],
    "Palmitas": [-33.50719, -57.80079],
    "Santa Catalina": [-33.791, -57.48824],
    "Villa Soriano": [-33.39811, -58.32177],
    "Curtina": [-32.15, -56.11667],
    "Paso de los Toros": [-32.81667, -56.51667],
    "Tacuarembó": [-31.71694, -55.98111],
    "Santa Clara de Olimar": [-32.92254, -54.94447],
    "Treinta y Tres": [-33.23333, -54.38333],
    "Vergara": [-32.94419, -53.9381],
    "Villa Sara": [-33.2534, -54.41947]
}

# Función para obtener ruta entre origen y destino
def obtener_ruta(origen, destino):
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    params = {
        "api_key": ORS_API_KEY,
        "start": f"{origen[1]},{origen[0]}",  # Longitud, Latitud
        "end": f"{destino[1]},{destino[0]}",
        "radiuses": "-1;-1",  # Sin límites de búsqueda
        "optimize_waypoints": "false"  # Deshabilitar optimización
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error al obtener ruta: {response.status_code} - {response.text}")
        return []

    data = response.json()

    if "features" not in data or not data["features"]:
        print(f"Respuesta inesperada: {data}")
        return []

    return [(coord[1], coord[0]) for coord in data["features"][0]["geometry"]["coordinates"]]

# Crear el mapa
mapa = folium.Map(location=origen, zoom_start=6)

# Añadir marcador de origen
folium.Marker(location=origen, popup='Montevideo', icon=folium.Icon(color='blue')).add_to(mapa)

# Iterar sobre destinos y trazar rutas
for departamento, coords in destinos.items():
    print(f"Obteniendo ruta a {departamento}...")
    ruta = obtener_ruta(origen, coords)

    if ruta:
        # Trazar la ruta en el mapa
        folium.PolyLine(locations=ruta, color='red', weight=5).add_to(mapa)

        # Añadir marcador de destino
        folium.Marker(location=coords, popup=departamento, icon=folium.Icon(color='green')).add_to(mapa)

    # Pausar para evitar sobrecarga en la API
    time.sleep(1)
    origen = coords

# Guardar el mapa en un archivo HTML
mapa.save("mapa_rutas_uruguay2.html")
print("Mapa generado: mapa_rutas_uruguay2.html")

