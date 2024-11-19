from haversine import haversine, Unit 

def levantarArchivosDataSet():
    ciudades = []
    with open('ciudades.txt', 'r') as fichero:
        linea = fichero.readline()
        linea = fichero.readline()
        while linea != '':
            datos = linea.split(",")
            linea = fichero.readline()
            ciudades.append([datos[0], datos[1], datos[2], datos[3], datos[4], datos[8], datos[9]])
    return ciudades


def calcularDistancias(ciudades):
    # Inicializar una matriz cuadrada de tamaño n x n (donde n es la cantidad de ciudades)
    n = len(ciudades)
    matriz_distancias = [[0 for _ in range(n)] for _ in range(n)]

    # Calcular las distancias entre todas las combinaciones de ciudades
    for i in range(n):
        for j in range(i + 1, n):
            puntoInicial = (float(ciudades[i][5]), float(ciudades[i][6]))
            puntoActual = (float(ciudades[j][5]), float(ciudades[j][6]))
            
            # Calcular la distancia usando Haversine
            distancia = haversine(puntoInicial, puntoActual, unit=Unit.KILOMETERS)

            # Asignar la distancia en ambas posiciones de la matriz (simétrica)
            matriz_distancias[i][j] = distancia
            matriz_distancias[j][i] = distancia

    # Imprimir la matriz de distancias
        """     
        for fila in matriz_distancias:
        print(fila)
        """
    return matriz_distancias

""" datos = levantarArchivosDataSet()



        

cities = [
    ["New York", 40.7128, -74.0060],
    ["Los Angeles", 34.0522, -118.2437],
    ["Chicago", 41.8781, -87.6298],
    ["Minneapolis", 44.9866, -93.2581],
    ["Denver", 39.7392, -104.9903],
    ["Dallas", 32.7767, -96.7970],
    ["Seattle", 47.6062, -122.3321],
    ["Boston", 42.3601, -71.0589],
    ["San Francisco", 37.7749, -122.4194],
    ["St. Louis", 38.6270, -90.1994],
    ["Houston", 29.7604, -95.3698],
    ["Phoenix", 33.4484, -112.0740],
    ["Salt Lake City", 40.7608, -111.8910],
]

calcularDistancias(datos)
 """
