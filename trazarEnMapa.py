import folium
import requests
import time

# Tu clave de API de OpenRouteService
ORS_API_KEY = "5b3ce3597851110001cf6248eeb850562bc34d329aca00efb8694718"

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


def trazaMapa(tour, ciudades, origen, nombres, nombreArchivo):
    # Crear el mapa
    mapa = folium.Map(location=ciudades[origen], zoom_start=6)

    nombreOrigen = nombres[origen]

    # Añadir marcador de origen con número 1
    folium.Marker(
        location=ciudades[origen],
        popup=f"{nombreOrigen} (1)",
        icon=folium.DivIcon(html=f"<div style='font-size: 12pt; color: blue;'>{1}</div>")
    ).add_to(mapa)

    # Inicializar lista para guardar las rutas para la animación
    rutas_animadas = []

    for i in range(1, len(tour)):
        origin = tour[i - 1]
        destiny = tour[i]

        ruta = obtener_ruta(ciudades[origin], ciudades[destiny])

        if ruta:
            # Trazar la ruta en el mapa y guardar las coordenadas para animación
            folium.PolyLine(locations=ruta, color='red', weight=5).add_to(mapa)
            rutas_animadas.append(ruta)

            # Añadir marcador con número de parada correspondiente
            folium.Marker(
                location=ciudades[destiny],
                popup=f"{nombres[destiny]} ({i + 1})",
                icon=folium.DivIcon(html=f"<div style='font-size: 12pt; color: green;'>{i + 1}</div>")
            ).add_to(mapa)

        # Pausar para evitar sobrecarga en la API
        time.sleep(1)

    # Guardar el mapa en un archivo HTML
    mapa.save(nombreArchivo + ".html")

    # Agregar la animación al HTML generado
    agregar_animacion_html(nombreArchivo, rutas_animadas, tour, ciudades, origen, nombres)

def agregar_animacion_html(nombreArchivo, rutas, tour, ciudades, origen, nombres):
    # Leer el contenido del archivo HTML generado
    with open(nombreArchivo + ".html", "r", encoding="utf-8") as file:
        contenido = file.read()

    # Agregar el script de animación usando Leaflet y JavaScript
    animacion_script = f"""
    <script>
        var rutas = {rutas};  // Lista de rutas para la animación

        // Función para animar una línea en el mapa
        function animarLinea(mapa, coordenadas) {{
            var polyline = L.polyline([], {{ color: 'blue', weight: 4 }}).addTo(mapa);
            var i = 0;

            function dibujarSegmento() {{
                if (i < coordenadas.length) {{
                    polyline.addLatLng(L.latLng(coordenadas[i]));
                    i++;
                    setTimeout(dibujarSegmento, 100);  // Velocidad de animación
                }}
            }}
            dibujarSegmento();
        }}

        // Ejecutar la animación para cada ruta
        rutas.forEach(ruta => animarLinea(mymap, ruta));
    </script>
    """

    # Insertar el script al final del archivo HTML
    contenido = contenido.replace("</body>", animacion_script + "\n</body>")

    # Guardar el archivo modificado
    with open(nombreArchivo + ".html", "w", encoding="utf-8") as file:
        file.write(contenido)

    # Crear el mapa
    mapa = folium.Map(location=ciudades[origen], zoom_start=6)

    nombreOrigen = nombres[origen]

    # Añadir marcador de origen
    folium.Marker(location=ciudades[origen], popup=nombreOrigen, icon=folium.Icon(color='blue')).add_to(mapa)

    for i in range(1, len(tour), 1):
        origin = tour[i - 1]
        destiny = tour[i]

        ruta = obtener_ruta(ciudades[origin], ciudades[destiny])

        if ruta:
            # Trazar la ruta en el mapa
            folium.PolyLine(locations=ruta, color='red', weight=5).add_to(mapa)

            # Añadir marcador de destino
            folium.Marker(location=ciudades[destiny], popup=nombres[destiny], icon=folium.Icon(color='green')).add_to(mapa)

        # Pausar para evitar sobrecarga en la API
        time.sleep(1)

    # Guardar el mapa en un archivo HTML
    mapa.save(nombreArchivo + ".html")