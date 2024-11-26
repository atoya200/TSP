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


def ejecutar_tsp(datos, ciudad_inicio):
    
    # Se intrcambia latitud por longitud
    puntos = []
    
    # Puntos sin intercambiar
    puntos_sin_intercambiar = []

    for ciudad in datos:
       #puntos_sin_intercambiar.append([float(ciudad[5]), float(ciudad[6])])
       #puntos.append([float(ciudad[6]), float(ciudad[5])])
       puntos_sin_intercambiar.append([float(ciudad['latitude']), float(ciudad['longitud'])])
       puntos.append([float(ciudad['longitud']), float(ciudad['latitude'])])

    print(puntos)
    print("Ciudad inicio", ciudad_inicio)
    dist = obtener_matriz_distancias_y_tiempos(puntos)
    print(dist)

    # Prueba iniciando desde la ciudad 0
    tour, min_cost = tsp_dynamic_programming(dist, ciudad_inicio)
    
    tour_ciudades = []
    # Arma la lista de ciudades a visitar en el orden que debe visitarlas
    for i in tour: 
        tour_ciudades.append(datos[i])
        
    # Los datos quedaron reordenados para poder hacer el camino optimo
    return tour_ciudades

