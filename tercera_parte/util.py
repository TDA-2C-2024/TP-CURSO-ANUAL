def extraer_datos_archivo(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        lineas = archivo.readlines()
    
    lineas_limpias = [linea.strip() for linea in lineas if not linea.strip().startswith('#')]
    
    bloques = []
    bloque_actual = []
    for linea in lineas_limpias:
        if linea == '': 
            if bloque_actual:
                bloques.append(bloque_actual)
                bloque_actual = []
        else:
            bloque_actual.append(linea)

    if bloque_actual:
        bloques.append(bloque_actual)
    
    filas = list(map(int, bloques[0]))
    columnas = list(map(int, bloques[1]))
    barcos = list(map(int, bloques[2]))
    
    return filas, columnas, barcos
