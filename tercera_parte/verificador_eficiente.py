import math
import ast
import sys

def calcular_modulo(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def son_contiguas(posiciones):
    if len(posiciones) == 1:
        return True
    
    es_horizontal = False
    (x0, y0) = posiciones[0]
    (x1, y1) = posiciones[1]

    if x0 == x1 and y1 == y0 + 1:
        es_horizontal = True
    elif y0 == y1 and x1 == x0 + 1:
        es_horizontal = False
    else:
        return False

    for (x2, y2), (x3, y3) in zip(posiciones[1:], posiciones[2:]):
        if x2 == x3 and y3 == y2 + 1 and es_horizontal:
            continue
        elif y2 == y3 and x3 == x2 + 1 and not es_horizontal:
            continue
        else:
            return False
    return True

def validador_eficiente(filas, columnas, barcos, solucion):
    # Verifico que los barcos sean los mismos, su posicion se encuentren dentro del tablero
    # y que sean contiguos cada una de las posiciones de cada barco
    for nro_barco, posiciones in solucion.items():
        if nro_barco > len(barcos):
            return False
        if len(posiciones) != barcos[nro_barco]:
            return False
        if not son_contiguas(posiciones):
            return False
        for pos_fil, pos_col in posiciones:
            if (pos_fil > len(filas) and pos_fil >= 0) or (pos_col > len(columnas) and pos_col >= 0):
                return False

    # Verifico que cumpla con la demanda, para esto calcula la demanda de la solucion y comparo
    demanda_fila = [0] * len(filas)
    demanda_columna = [0] * len(columnas)
    for posiciones in solucion.values():
        for pos_fil, pos_col in posiciones:
            demanda_fila[pos_fil] += 1
            demanda_columna[pos_col] += 1
    
    for pos_fil in range(len(filas)):
        if filas[pos_fil] != demanda_fila[pos_fil]:
            return False
        for pos_col in range(len(columnas)):
            if columnas[pos_col] != demanda_columna[pos_col]:
                return False
    
    # Verifica las restricciones de adyacencia, y de paso si esta superpuesto con otro barco
    for nro_barco, posiciones in solucion.items():
        for nro_otro_barco, posiciones_otro_barco in solucion.items():
            if nro_barco == nro_otro_barco:
                continue
            for posicion in posiciones:
                for otra_posicion in posiciones_otro_barco:
                    if calcular_modulo(posicion, otra_posicion) <= math.sqrt(2):
                        return False
                
    return True

def leer_archivo(archivo):
    try:
        with open(archivo, 'r') as f:
            contenido = f.readlines()
 
        contenido = [linea.strip() for linea in contenido if linea.strip() and not linea.strip().startswith('#')]
    
        filas = ast.literal_eval(contenido[0].split('=')[1].strip())
        columnas = ast.literal_eval(contenido[1].split('=')[1].strip())
        barcos = ast.literal_eval(contenido[2].split('=')[1].strip())
        solucion = ast.literal_eval(contenido[3].split('=')[1].strip())
        
        return filas, columnas, barcos, solucion
    
    except Exception:
        raise Exception("Hubo un error al leer el archivo. Verifique su formato y contenido.")



if __name__ == "__main__":
    argumentos = sys.argv
    if len(argumentos) != 2:
        raise AssertionError("Error: se esperaba solo 2 argumentos")
    
    filas, columnas, barcos, solucion = leer_archivo(argumentos[1])
    
    es_valida = validador_eficiente(filas, columnas, barcos, solucion)
    
    if es_valida:
        print("La solución es válida.")
    else:
        print("La solución no es válida.")