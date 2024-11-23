from armarBase import levantarArchivosDataSet, calcularDistancias
from trazarEnMapa import trazaMapa
from calculoDistancia import obtener_matriz_distancias_y_tiempos
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


datos = levantarArchivosDataSet()
puntos = []
puntos_de_bien = []
nombresCiudades = []

for ciudad in datos:
    puntos_de_bien.append([float(ciudad[5]), float(ciudad[6])])
    puntos.append([float(ciudad[6]), float(ciudad[5])])
    nombreCiudad = ciudad[1].replace("\"", "")
    nombresCiudades.append(nombreCiudad)

#dist = calcularDistancias(datos)
dist = obtener_matriz_distancias_y_tiempos(puntos)
print(dist)

# Prueba iniciando desde la ciudad 0
tour, min_cost = tsp_dynamic_programming(dist, 0)
print(tour)
for i in tour: 
    print(puntos_de_bien[i], ",")
trazaMapa(tour, puntos_de_bien, 0, nombresCiudades, "mapaTest4")

