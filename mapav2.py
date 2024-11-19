import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Lista de puntos intermedios como coordenadas geográficas (longitud, latitud)
puntos = [
    (-56.1645, -34.9011),  # Montevideo
    (-55.9034, -34.4811),  # Canelones
    (-54.9508, -34.8978),  # Rocha
    (-56.3124, -34.7815),  # San José
    (-54.9855, -32.3123),  # Rivera
]

# Cargamos el mapa del mundo y filtramos Uruguay
mundo = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
uruguay = mundo[mundo['name'] == 'Uruguay']

# Configuramos la figura
fig, ax = plt.subplots(figsize=(8, 8))
uruguay.plot(ax=ax, color='lightgray')  # Dibujamos el mapa de Uruguay
ax.set_title('Animación de puntos intermedios sobre Uruguay')

# Configuramos los límites del mapa alrededor de Uruguay
ax.set_xlim(-58, -53)  # Límites de longitud
ax.set_ylim(-35.5, -30)  # Límites de latitud

# Inicializamos la línea que se animará
linea, = ax.plot([], [], color='blue', marker='o', lw=2)

# Función de actualización para animar el trazado
def actualizar(frame):
    # Tomamos los puntos hasta el frame actual
    longitudes, latitudes = zip(*puntos[:frame])
    linea.set_data(longitudes, latitudes)
    return linea,

# Creamos la animación
anim = FuncAnimation(fig, actualizar, frames=len(puntos) + 1,
                     interval=800, repeat=False)

# Guardamos la animación como GIF (necesitas ImageMagick)
anim.save('trazado_uruguay.gif', writer='imagemagick')

plt.show()
