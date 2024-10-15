import tkinter
import tkintermapview
import math
import csv
import matplotlib.pyplot as plt
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

    return matriz_distancias

# Levantar los datos de las ciudades
datos = levantarArchivosDataSet()

# Calcular la matriz de distancias entre las ciudades
matriz_distancia = calcularDistancias(datos)

#  ciudad de inicio
start_city = 0

print(matriz_distancia)

def tsp_backtracking_memo(distances, start_city):
    n = len(distances)
    memo = {}

    def visit(city, visited):
        if (city, visited) in memo:
            return memo[(city, visited)]

        # Si hemos visitado todas las ciudades, regresar a la ciudad de inicio
        if visited == (1 << n) - 1:
            return distances[city][start_city]

        min_cost = math.inf

        # Explorar todas las ciudades no visitadas
        for next_city in range(n):
            if not (visited & (1 << next_city)):  # Si la ciudad no ha sido visitada
                new_cost = distances[city][next_city] + visit(next_city, visited | (1 << next_city))
                min_cost = min(min_cost, new_cost)

        memo[(city, visited)] = min_cost
        return min_cost

    # Función para reconstruir el recorrido
    def build_tour(city, visited):
        if visited == (1 << n) - 1:
            return [city, start_city]

        next_city = None
        min_cost = math.inf

        for city_to_visit in range(n):
            if not (visited & (1 << city_to_visit)):
                cost = distances[city][city_to_visit] + visit(city_to_visit, visited | (1 << city_to_visit))
                if cost < min_cost:
                    min_cost = cost
                    next_city = city_to_visit

        return [city] + build_tour(next_city, visited | (1 << next_city))

    # Iniciar el recorrido desde la ciudad de inicio
    min_cost = visit(start_city, 1 << start_city)
    tour = build_tour(start_city, 1 << start_city)

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
tour, min_cost = tsp_backtracking_memo(matriz_distancia, start_city)

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

def mostrar_distancia_entre_ciudades(matriz_distancia, tour):
    for i in range(len(tour) - 1):  # Itera hasta el penúltimo índice
        ciudad_origen = tour[i]       # Ciudad en la posición i del tour
        ciudad_destino = tour[i + 1]  # Ciudad en la posición i+1 del tour
        distancia = matriz_distancia[ciudad_origen][ciudad_destino]  # Distancia en la matriz
        print(f"Distancia entre {ciudad_origen} y {ciudad_destino}: {distancia}")


# Iniciar la visualización secuencial
root_tk.after(1000, mostrar_rutas_secuencialmente, 0)
# ESTa funcion muestra las distancias entre cada par de ciudades
mostrar_distancia_entre_ciudades(matriz_distancia,tour)
# Iniciar el bucle de eventos
print("Costo óptimo:", min_cost, "Recorrido:", tour)
root_tk.mainloop()


