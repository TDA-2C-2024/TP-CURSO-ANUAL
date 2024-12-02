import math
import ast
import sys

def calcular_modulo(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def validador_eficiente(filas, columnas, barcos, solucion):
    # Verifico que los barcos sean los mismos, y su posicion se encuentren dentro del tablero
    for nro_barco, posiciones in solucion.items():
        if nro_barco > len(barcos):
            return False
        if len(posiciones) != barcos[nro_barco]:
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