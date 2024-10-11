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
    for c in ciudades:
        print(c)
    return ciudades


datos = levantarArchivosDataSet()


def calcularDistancias(start, datos):
    distancias = []

    for i in range (0, len(datos)):
        if(i == start):
            distancias.append(0)
            continue
        
        puntoInicial = datos[start]
        puntoActal = datos[i]

        """x2 = float(puntoInicial[6])
        x1 = float(puntoActal[6])

        y2 = float(puntoInicial[5])
        y1 = float(puntoActal[5]) """

        inicial = (float(puntoInicial[1]), float(puntoInicial[2])) 
        actual = (float(puntoActal[1]), float(puntoActal[2])) 


        # Convertir las latitudes y longitudes de grados a radianes
        distancia = haversine(inicial, actual, unit=Unit.KILOMETERS)

        distancias.append(distancia)

    print(distancias)
        

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

calcularDistancias(0, cities)