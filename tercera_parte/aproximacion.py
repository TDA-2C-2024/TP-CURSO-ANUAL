import sys
import time

from util import extraer_datos_archivo
from barco import Barco
from backtracking import demanda
from backtracking import colocar_barco
from backtracking import estan_superpuesto
from backtracking import estan_adyacentes

def mayores_demandas(filas, columnas):
    n, m = len(filas), len(columnas)

    demandas = {(i, j): filas[i] + columnas[j] for i in range(n) for j in range(m)}
    
    return dict(sorted(demandas.items(), key=lambda x: x[1], reverse=True))
            
# Devuelve si se pudo ubicar un barco
def se_puede_ubicar(puestos, filas, columnas, barcos, barco_act, direccion, pos_fil, pos_col, celdas):
    posiciones, se_pudo = colocar_barco(direccion, pos_fil, pos_col, filas, columnas, barcos[barco_act][1])
    if se_pudo:
        barco = Barco(barcos[barco_act][0], posiciones, direccion)
        # Verifico que no se superponga con los demas, o que sea adyacente, o que no exceda demanda
        if estan_superpuesto(puestos, barco) or estan_adyacentes(puestos, barco) or barco.excede_demanda(filas, columnas, puestos):
            return False
        puestos.add(barco)
        return True
    else:
        return False

def actualizar_demanda(puestos, filas, columnas):
    demanda_filas, demanda_columnas = Barco.calcular_demanda(puestos, filas, columnas)
    demanda_filas_actual = [a - b for a, b in zip(filas, demanda_filas)]
    demanda_columas_actual = [a - b for a, b in zip(columnas, demanda_columnas)]

    return mayores_demandas(demanda_filas_actual, demanda_columas_actual)


def aproximacion(filas, columnas, barcos):
    # Ordeno las celdas de mayor a menor demanda
    celdas = mayores_demandas(filas, columnas)

    # Ordeno los barcos de mayor a menor longitud
    tuplas = [(i, largo) for i, largo in enumerate(barcos)]
    barcos_ordenados = sorted(tuplas, key=lambda x: x[1], reverse=True)

    puestos = set()
    barco_act = 0
    demanda_total = sum(filas) + sum(columnas)

    while demanda(puestos, filas, columnas) != demanda_total and barco_act != len(barcos_ordenados):
        se_pudo_colocar = False
        for (i, j), _ in celdas.items(): 
            if se_puede_ubicar(puestos, filas, columnas, barcos_ordenados, barco_act, 'vertical', i, j, celdas):
                se_pudo_colocar = True
                break
            # Para barcos de largo 1, basta con colocarlo horizontal o vertical
            if not se_pudo_colocar and barcos_ordenados[barco_act][1] == 1:
                continue
            if se_puede_ubicar(puestos, filas, columnas, barcos_ordenados, barco_act, 'horizontal', i, j, celdas):
                se_pudo_colocar = True 
                break
        
        # Si no pude colocar un barco de cierta longitud, no voy a poder colocar el siguiente si tiene la misma longitud
        if not se_pudo_colocar and barco_act != len(barcos_ordenados)-1:
            barco_act += 1
            while barcos_ordenados[barco_act-1][1] == barcos_ordenados[barco_act][1]:
                barco_act += 1
                if barco_act == len(barcos_ordenados):
                    break
            barco_act -= 1
        else:
            celdas = actualizar_demanda(puestos, filas, columnas)

        barco_act += 1

    return list(puestos), demanda(puestos, filas, columnas)

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