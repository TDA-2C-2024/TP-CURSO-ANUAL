import sys
import time

from barco import Barco
from util import extraer_datos_archivo
from backtracking import demanda
from backtracking import demanda_barcos_faltantes
from backtracking import demanda_por_fila
from backtracking import tratar_de_ubicar_barco


# Ubica a los barcos tratando de minimizar la demanda incumplida, obteniendo asi un optimo
def ubicaciones_barco(puestos, filas, columnas, barcos, barco_act, mejores_puestos):
    # La mejor solucion es usar todos los barcos, ya no sigo buscando
    if len(mejores_puestos) == len(barcos):
        return

    demanda_actual = demanda(puestos, filas, columnas)
    demanda_mejor = demanda(mejores_puestos, filas, columnas)
    demanda_faltante = demanda_barcos_faltantes(barcos, barco_act)

    # Si con los barcos que tengo puestos (y los que me faltan colocar)
    # no llego a cubrir la maxima demanda que obtuve, no sigo
    if demanda_actual + demanda_faltante <= demanda_mejor:
        return 
    
    # Llegue a una mejor solucion, es decir, tengo mayor demanda cumplida que antes 
    if demanda_actual > demanda_mejor:
        mejores_puestos[:] = puestos
    
    # Me fijo que no me exceda por las dudas
    if barco_act >= len(barcos):
        return

    se_pudo_colocar = False
    for nro_fila, demanda_fila in ((filas)).items():
        # Salteo las filas con demanda 0 o las que tengan su demanda al maximo
        if demanda_fila == 0 or demanda_por_fila(nro_fila, puestos) == demanda_fila:
            continue

        for nro_columna, demanda_columna in ((columnas)).items():
            while barcos[barco_act][1] > demanda_fila and barcos[barco_act][1] > demanda_columna:
                barco_act += 1
                if barco_act == len(barcos):
                    barco_act -= 1
                    return
            if tratar_de_ubicar_barco(puestos, filas, columnas, barcos, barco_act, 'vertical', nro_fila, nro_columna, mejores_puestos):
                se_pudo_colocar = True
            # Para barcos de largo 1, basta con colocarlo horizontal o vertical
            if barcos[barco_act][1] == 1:
                continue
            if tratar_de_ubicar_barco(puestos, filas, columnas, barcos, barco_act, 'horizontal', nro_fila, nro_columna, mejores_puestos):
                se_pudo_colocar = True
    
    # Si no pude colocar un barco de cierta longitud, no voy a poder colocar el siguiente si tiene la misma longitud
    if not se_pudo_colocar and barco_act != len(barcos)-1:
        barco_act += 1
        while barcos[barco_act-1][1] == barcos[barco_act][1]:
            barco_act += 1
            if barco_act == len(barcos):
                return
        barco_act -= 1
            
    # No tengo en cuenta este barco (ya sea si lo pude colocar o n o), asi que sigo con el siguiente
    ubicaciones_barco(puestos, filas, columnas, barcos, barco_act+1, mejores_puestos)

def aproximacion(filas, columnas, barcos):
    mejores_puestos = [Barco(-1, set(), True)]
    # Ordeno las filas por mayor demanda
    dict_filas = {i: demanda for i, demanda in enumerate(filas)}
    dict_filas_ordenado = dict(sorted(dict_filas.items(), key=lambda item: item[1], reverse=True))

    # Ordeno las columnas por mayor demanda
    dict_columnas = {i: demanda for i, demanda in enumerate(columnas)}
    dict_columnas_ordenado = dict(sorted(dict_columnas.items(), key=lambda item: item[1], reverse=True))

    # Ordeno los barcos de mayor a menor longitud
    tuplas = [(i, largo) for i, largo in enumerate(barcos)]
    barcos_ordenados = sorted(tuplas, key=lambda x: x[1], reverse=True)

    ubicaciones_barco(set(), dict_filas_ordenado, dict_columnas_ordenado, barcos_ordenados, 0, mejores_puestos)
    return mejores_puestos, demanda(mejores_puestos, filas, columnas)

# Para correr el codigo, se debe pasar por parametro un .txt 
# que tengo el mismo formato que los test de la catedra
# Ejemplo: python3 aproximacion.py test_data_aprox/3_3_2.txt (u otro .txt con el mismo formato)
#
# Para correr los test de la catedra:
# $ chmod +x run_test_aprox.sh
# $ ./run_test_aprox.sh
if __name__ == "__main__":
    argumentos = sys.argv
    if len(argumentos) != 2:
        raise AssertionError("Error: se esperaba solo 2 argumentos")

    filas, columnas, barcos = extraer_datos_archivo(argumentos[1])

    inicio = time.time() 
    barcos_puestos, demanda_cumplida = aproximacion(filas, columnas, barcos)
    fin = time.time()  
    tiempo_ejecucion = f"Tiempo de ejecución: {fin - inicio:.6f} segundos"
    
    print(tiempo_ejecucion)
    print(argumentos[1].split("/")[-1])
    barcos_ordenados = sorted(barcos_puestos, key=lambda barco: barco.id())
    for barco in barcos_ordenados:
        print(barco.mostrar())
    
    print("Demanda cumplida: " + str(demanda_cumplida))
    print("Demanda total: " + str(sum(filas)+sum(columnas)))