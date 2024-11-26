from flask import Flask, request, jsonify
from armarBase import levantar_archivos_ciudades_data_set, obtener_datos_punto, devolver_todas_las_ciudades
from tsp import ejecutar_tsp
from flask_cors import CORS

app = Flask(__name__)

# Habilitar CORS para todas las rutas y orígenes
CORS(app)

@app.route('/ciudades_disponibles', methods=['GET'])
def devolver_ciudades_disponibles():
    try:
        return jsonify(devolver_todas_las_ciudades(["id", "city_name", "state_name"])), 200

    
    except Exception as e:
        # Capturar y mostrar el error completo en la consola para depuración
        import traceback
        error_trace = traceback.format_exc()
        print(error_trace)

        # Respuesta de error genérica para el cliente
        return jsonify({"error": str(e)}), 500
    
    
@app.route('/calcular_tsp', methods=['POST'])
def calcular_tsp():
    try:
        # Obtén los datos del cuerpo de la solicitud
        datos = request.get_json()
        
        print(datos)
        print(type(datos))

        # Validar parámetros requeridos
        if not datos or "puntos" not in datos or "punto_partida" not in datos:
            return jsonify({"error": "Los parámetros 'puntos' y 'punto_partida' son requeridos"}), 400

        # Validar que 'punto_partida' sea un entero
        if not isinstance(datos['punto_partida'], int):
            return jsonify({"error": "'punto_partida' debe ser un número entero"}), 400

        # Validar que 'puntos' sea una lista y tenga máximo 19 elementos
        if not isinstance(datos['puntos'], list) or len(datos['puntos']) > 19:
            return jsonify({"error": "'puntos' debe ser una lista con un máximo de 19 elementos"}), 400

        # Validar que todos los elementos de 'puntos' sean enteros
        if not all(isinstance(punto, int) for punto in datos['puntos']):
            return jsonify({"error": "Todos los elementos de 'puntos' deben ser números enteros"}), 400

        # Recuperar datos para las ciudades
        ciudades = [obtener_datos_punto(datos['punto_partida'])]
        for punto in datos['puntos']:
            ciudades.append(obtener_datos_punto(punto))

        # Calcular ruta utilizando TSP
        ruta = ejecutar_tsp(ciudades, 0)

        # Respuesta exitosa
        return jsonify(ruta), 200

    except Exception as e:
        # Capturar y mostrar el error completo en la consola para depuración
        import traceback
        error_trace = traceback.format_exc()
        print(error_trace)

        # Respuesta de error genérica para el cliente
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Inicializar datos
    levantar_archivos_ciudades_data_set()
    # Iniciar el servidor
    app.run(debug=True)
