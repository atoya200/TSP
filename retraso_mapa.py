import tkinter
import tkintermapview
import math
import csv
from haversine import haversine, Unit 

# Función para levantar los datos del archivo ciudades.txt
def levantarArchivosDataSet():
    ciudades = []
    with open("ciudades.txt", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Saltar la cabecera
        for row in reader:
            id_ciudad = int(row[0])
            nombre = row[1]
            latitud = float(row[8])
            longitud = float(row[9])
            ciudades.append((nombre, latitud, longitud))
    return ciudades

def calcularDistancias(ciudades):
    n = len(ciudades)
    matriz_distancias = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            puntoInicial = (ciudades[i][1], ciudades[i][2])  # Índices para latitud y longitud
            puntoActual = (ciudades[j][1], ciudades[j][2])    # Índices para latitud y longitud
            
            # Calcular la distancia usando Haversine
            distancia = haversine(puntoInicial, puntoActual, unit=Unit.KILOMETERS)

            # Asignar la distancia en ambas posiciones de la matriz (simétrica)
            matriz_distancias[i][j] = distancia
            matriz_distancias[j][i] = distancia

    for fila in matriz_distancias:
        print(fila)

    return matriz_distancias

# Levantar los datos de las ciudades
datos = levantarArchivosDataSet()

# Calcular la matriz de distancias entre las ciudades
matriz_distancia = calcularDistancias(datos)

# Algoritmo del viajante de comercio
def tsp_dynamic_programming(distances, start_city):
    n = len(distances)
    dp = [[math.inf] * n for _ in range(1 << n)]
    parent = [[None] * n for _ in range(1 << n)]
    dp[1 << start_city][start_city] = 0

    for mask in range(1 << n):
        for last in range(n):
            if not (mask & (1 << last)):
                continue
            for next in range(n):
                if mask & (1 << next):
                    continue
                new_mask = mask | (1 << next)
                new_dist = dp[mask][last] + distances[last][next]
                if new_dist < dp[new_mask][next]:
                    dp[new_mask][next] = new_dist
                    parent[new_mask][next] = last

    min_cost = math.inf
    end_city = None
    full_mask = (1 << n) - 1

    for last in range(n):
        cost = dp[full_mask][last] + distances[last][start_city]
        if cost < min_cost:
            min_cost = cost
            end_city = last

    tour = []
    mask = full_mask
    last = end_city
    while mask:
        tour.append(last)
        new_last = parent[mask][last]
        mask ^= (1 << last)
        last = new_last
    tour = tour[::-1]
    tour.append(start_city)

    return tour, min_cost

# Crear la ventana principal
root_tk = tkinter.Tk()
root_tk.geometry(f"{800}x{600}")
root_tk.title("Mapa de Ciudades")

# Crear el widget del mapa
map_widget = tkintermapview.TkinterMapView(root_tk, width=800, height=600, corner_radius=0)
map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

# Establecer la posición inicial y el nivel de zoom
map_widget.set_position(-32.5228, -55.7658)  # Centro aproximado de Uruguay
map_widget.set_zoom(7)

# Obtener el recorrido del algoritmo TSP
tour, min_cost = tsp_dynamic_programming(matriz_distancia, 0)

# Crear una lista de coordenadas según el recorrido (tour)
coordenadas_tour = [(datos[i][1], datos[i][2]) for i in tour]

# Crear una lista para almacenar los marcadores
markers = []

# Agregar marcadores de las ciudades
for ciudad in datos:
    nombre, lat, lon = ciudad
    marker = map_widget.set_marker(lat, lon, text=nombre)
    markers.append(marker)

# Función para dibujar las rutas secuencialmente
def mostrar_rutas_secuencialmente(i):
    if i < len(coordenadas_tour) - 1:
        lat1, lon1 = coordenadas_tour[i]
        lat2, lon2 = coordenadas_tour[i + 1]
        map_widget.set_path([(lat1, lon1), (lat2, lon2)], color="blue")
        root_tk.after(1000, mostrar_rutas_secuencialmente, i + 1)

# Iniciar la visualización secuencial
root_tk.after(1000, mostrar_rutas_secuencialmente, 0)
print("Costo óptimo:", min_cost, "Recorrido:", tour)

# Iniciar el bucle de eventos
root_tk.mainloop()
