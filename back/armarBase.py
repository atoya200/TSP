ciudades_data_set = []

def levantar_archivos_ciudades_data_set():
    ciudades = []
    with open('back/ciudades.txt', 'r',  encoding='utf-8') as fichero:
        linea = fichero.readline()
        linea = fichero.readline()
        while linea != '':
            datos = linea.split(",")
            linea = fichero.readline()

            # ['129886', 'San JosÃ©', '3212', 'SJ', '"San JosÃ©"', '-34.33750000', '-56.71361000']
            ciudades.append({"id": datos[0],
                            "state_name": datos[4],
                            "state_code": datos[2],
                            "abrev_state":  datos[3],
                            "city_name": datos[1], 
                            "latitude": datos[8],
                            "longitud": datos[9]})
    
    global ciudades_data_set
    ciudades_data_set = ciudades
    return True



def obtener_datos_punto(id_punto):
    global ciudades_data_set
    for l in ciudades_data_set:
        if l['id'] == f"{id_punto}":
            return l
    
    return None
      
def devolver_todas_las_ciudades(campos=None):
    global ciudades_data_set
    
    """
    Devuelve las ciudades con los campos especificados.
    :param campos: Lista de nombres de campos que se desean incluir.
    :return: Lista de diccionarios con los campos seleccionados.
    """
    # Si no se pasan campos, devolver todo el dataset
    if not campos:
        return ciudades_data_set

    # Filtrar las ciudades con los campos especificados
    resultado = []
    for ciudad in ciudades_data_set:
        ciudad_filtrada = {campo: ciudad[campo] for campo in campos if campo in ciudad}
        resultado.append(ciudad_filtrada)
    
    return resultado
