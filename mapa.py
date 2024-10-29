import folium
import requests

# Coordenadas del centro de Uruguay
uruguay_coords = [-32.5228, -55.7658]

# Crear un mapa centrado en Uruguay
mapa_uruguay = folium.Map(location=uruguay_coords, zoom_start=7)

# Puntos de interés (Montevideo -> Punta del Este)
origen = [-34.9011, -56.1645]  # Montevideo
destino = [-34.9687, -54.9505]  # Punta del Este

# API Key de OpenRouteService (reemplazar con tu clave)
ORS_API_KEY = "5b3ce3597851110001cf6248eeb850562bc34d329aca00efb8694718y"

# Hacer la solicitud a la API de ORS para obtener la ruta entre los puntos
url = "https://api.openrouteservice.org/v2/directions/driving-car"
params = {
    "api_key": ORS_API_KEY,
    "start": f"{origen[1]},{origen[0]}",  # Longitud, Latitud
    "end": f"{destino[1]},{destino[0]}"
}
response = requests.get(url, params=params)
data = response.json()

# Extraer las coordenadas de la ruta
ruta = [(coord[1], coord[0]) for coord in data["features"][0]["geometry"]["coordinates"]]

# Dibujar la ruta en el mapa
folium.PolyLine(ruta, color="blue", weight=5, opacity=0.6).add_to(mapa_uruguay)

# Inyectar JavaScript para animación del marcador
animated_marker_js = f"""
var animatedMarker = L.Marker.movingMarker(
    {ruta},
    [5000] * {len(ruta)},  // Asigna 5 segundos para cada segmento
    {{autostart: true}}
).addTo(map);
"""

# Añadir JavaScript personalizado al mapa
folium.Element(f"<script>{animated_marker_js}</script>").add_to(mapa_uruguay)

# Guardar el mapa como HTML
mapa_uruguay.save("mapa_uruguay_ruta_real.html")
print("Mapa guardado como mapa_uruguay_ruta_real.html")
