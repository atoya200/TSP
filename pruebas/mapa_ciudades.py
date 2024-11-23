import tkinter
import tkintermapview
import math

def tsp_dynamic_programming(distances, start_city):
    n = len(distances)  # Número de ciudades
    dp = [[math.inf] * n for _ in range(1 << n)]
    parent = [[None] * n for _ in range(1 << n)]

    # Caso base: comenzando desde la ciudad start_city
    dp[1 << start_city][start_city] = 0

    # Llenar la tabla DP
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

    # Encontrar el tour óptimo y el costo mínimo
    min_cost = math.inf
    end_city = None
    full_mask = (1 << n) - 1

    for last in range(n):  # Considerar todas las ciudades
        cost = dp[full_mask][last] + distances[last][start_city]  # Volver a la ciudad de inicio
        if cost < min_cost:
            min_cost = cost
            end_city = last

    # Reconstruir el tour óptimo
    tour = []
    mask = full_mask
    last = end_city
    while mask:
        tour.append(last)
        new_last = parent[mask][last]
        mask ^= (1 << last)
        last = new_last
    tour = tour[::-1]
    tour.append(start_city)  # Agregar la ciudad de inicio al final para completar el ciclo

    return tour, min_cost

# Matriz de distancias
dist = [
    [0, 2451, 713, 1018, 1631, 1374, 2408, 213, 2571, 875, 1420, 2145, 1972],
    [2451, 0, 1745, 1524, 831, 1240, 959, 2596, 403, 1589, 1374, 357, 579],
    [713, 1745, 0, 355, 920, 803, 1737, 851, 1858, 262, 940, 1453, 1260],
    [1018, 1524, 355, 0, 700, 862, 1395, 1123, 1584, 466, 1056, 1280, 987],
    [1631, 831, 920, 700, 0, 663, 1021, 1769, 949, 796, 879, 586, 371],
    [1374, 1240, 803, 862, 663, 0, 1681, 1551, 1765, 547, 225, 887, 999],
    [2408, 959, 1737, 1395, 1021, 1681, 0, 2493, 678, 1724, 1891, 1114, 701],
    [213, 2596, 851, 1123, 1769, 1551, 2493, 0, 2699, 1038, 1605, 2300, 2099],
    [2571, 403, 1858, 1584, 949, 1765, 678, 2699, 0, 1744, 1645, 653, 600],
    [875, 1589, 262, 466, 796, 547, 1724, 1038, 1744, 0, 679, 1272, 1162],
    [1420, 1374, 940, 1056, 879, 225, 1891, 1605, 1645, 679, 0, 1017, 1200],
    [2145, 357, 1453, 1280, 586, 887, 1114, 2300, 653, 1272, 1017, 0, 504],
    [1972, 579, 1260, 987, 371, 999, 701, 2099, 600, 1162, 1200, 504, 0],
]

# Prueba iniciando desde la ciudad 0
tour, min_cost = tsp_dynamic_programming(dist, 5)

# Crear la ventana principal
root_tk = tkinter.Tk()
root_tk.geometry(f"{800}x{600}")
root_tk.title("Mapa de Ciudades")

# Crear el widget del mapa
map_widget = tkintermapview.TkinterMapView(root_tk, width=800, height=600, corner_radius=0)
map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

# Establecer la posición inicial y el nivel de zoom
map_widget.set_position(39.8283, -98.5795)  # Posición inicial en el centro de EE. UU.
map_widget.set_zoom(4)

# Lista de ciudades con sus coordenadas y un ID
cities = [
    ("New York", 40.7128, -74.0060),
    ("Los Angeles", 34.0522, -118.2437),
    ("Chicago", 41.8781, -87.6298),
    ("Minneapolis", 44.9866, -93.2581),
    ("Denver", 39.7392, -104.9903),
    ("Dallas", 32.7767, -96.7970),
    ("Seattle", 47.6062, -122.3321),
    ("Boston", 42.3601, -71.0589),
    ("San Francisco", 37.7749, -122.4194),
    ("St. Louis", 38.6270, -90.1994),
    ("Houston", 29.7604, -95.3698),
    ("Phoenix", 33.4484, -112.0740),
    ("Salt Lake City", 40.7608, -111.8910),
]

# Crear una lista de coordenadas según el recorrido (tour)
coordenadas_tour = [(cities[i][1], cities[i][2]) for i in tour]

# Crear una lista para almacenar los marcadores
markers = []

# Agregar marcadores y crear rutas entre ellos
for city, lat, lon in cities:
    marker = map_widget.set_marker(lat, lon, text=city)  # Agregar marcador
    markers.append(marker)  # Guardar el marcador en la lista

# Crear un path entre las ciudades según el tour
path_coordinates = [(lat, lon) for lat, lon in coordenadas_tour]
map_widget.set_path(path_coordinates, color="blue")  # Cambiar el color si deseas


print("lista de ciudades: ", tour)
# Iniciar el bucle de eventos
root_tk.mainloop()
