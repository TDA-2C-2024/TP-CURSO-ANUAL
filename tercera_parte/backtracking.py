import sys
import time

from barco import Barco
from util import extraer_datos_archivo

# Devuelve si el barco esta superpuesto con otros que esten puestos
def estan_superpuesto(puestos, barco):
    for otro_barco in puestos:
            if otro_barco != barco and barco.esta_superpuesto(otro_barco): 
                return True  
    return False
    
# Devuelve si el barco es adyacente a otros que esten puestos
def estan_adyacentes(puestos, barco):
    for otro_barco in puestos:
        if otro_barco != barco and barco.esta_adyacente(otro_barco):
            return True  
    return False

# Devuelve las posiciones del barco solo si las mismas no esten afuera del tablero
def colocar_barco(direccion, pos_fil, pos_col, filas, columnas, longitud_barco):
    (fila_act, columna_act) = (pos_fil, pos_col)
    posiciones_ocupadas = set()
    se_pudo = False

    # Caso borde, posicion invalida (no tendria que ocurrir... pero por las dudas)
    if fila_act >= len(filas) or columna_act >= len(columnas):
        return posiciones_ocupadas, se_pudo

    # Trato de colocarlo horizontal o verticalmente
    if direccion == 'horizontal':
        # Me fijo si el largo excede las filas
        if columna_act + (longitud_barco-1) < len(columnas):
            for m in range(columna_act, columna_act + longitud_barco):
                posiciones_ocupadas.add((fila_act, m))
            se_pudo = True
    else:
        # Idem arriba
        if fila_act + (longitud_barco-1) < len(filas):
            for n in range(fila_act, fila_act + longitud_barco):
                posiciones_ocupadas.add((n, columna_act))
            se_pudo = True

    return posiciones_ocupadas, se_pudo

# Devuelve si se pudo ubicar un barco
def tratar_de_ubicar_barco(puestos, filas, columnas, barcos, barco_act, direccion, pos_fil, pos_col, mejores_puestos):
    posiciones, se_pudo = colocar_barco(direccion, pos_fil, pos_col, filas, columnas, barcos[barco_act][1])
    if se_pudo:
        barco = Barco(barcos[barco_act][0], posiciones, direccion)
        # Verifico que no se superponga con los demas, o que sea adyacente, o que no exceda demanda
        if estan_superpuesto(puestos, barco) or estan_adyacentes(puestos, barco) or barco.excede_demanda(filas, columnas, puestos):
            return False
        puestos.add(barco)
        ubicaciones_barco(puestos, filas, columnas, barcos, barco_act+1, mejores_puestos)
        puestos.remove(barco)
    return True

# Devuelve cuanta demanda cubri actualmente para una fila

def demanda_por_fila(nro_fila, puestos):
    demanda_actual = 0
    for barco in puestos:
        for (fila, _) in barco.posiciones:
            if fila == nro_fila:
                demanda_actual += 1
    
    return demanda_actual

# Devuelve cuanta demanda cubri actualmente para una columna
def demanda_por_columna(nro_columna, puestos):
    demanda_actual = 0
    for barco in puestos:
        for (_, columna) in barco.posiciones:
            if columna == nro_columna:
                demanda_actual += 1
    
    return demanda_actual

# Devuelve la demanda de los barcos
def demanda(puestos, filas, columnas):
    filas_ocupadas = [0] * len(filas) 
    columnas_ocupadas = [0] * len(columnas) 

    for barco in puestos:
        for (fila, columna) in barco.posiciones:
            filas_ocupadas[fila] += 1
            columnas_ocupadas[columna] += 1
     
    return sum(filas_ocupadas) + sum(columnas_ocupadas)

# Calcula la demanda de los barcos a partir de barco_act
def demanda_barcos_faltantes(barcos, barco_act):
    demanda_faltante = 0
    for barco in barcos[barco_act:]:
        demanda_faltante += barco[1] * 2
    return demanda_faltante

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

        for nro_columna, _ in ((columnas)).items():
            if tratar_de_ubicar_barco(puestos, filas, columnas, barcos, barco_act, 'vertical', nro_fila, nro_columna, mejores_puestos):
                se_pudo_colocar = True
            if tratar_de_ubicar_barco(puestos, filas, columnas, barcos, barco_act, 'horizontal', nro_fila, nro_columna, mejores_puestos):
                se_pudo_colocar = True
    
    # Si no pude colocar un barco de cierta longitud, no voy a poder colocar el siguiente si tiene la misma longitud
    if barco_act > 0 and not se_pudo_colocar and barcos[barco_act-1][1] == barcos[barco_act][1]:
        while barcos[barco_act-1][1] == barcos[barco_act][1]:
            barco_act += 1
            if barco_act == len(barcos):
                # No hay mas barcos para poner
                return
            
    # No tengo en cuenta este barco (ya sea si lo pude colocar o n o), asi que sigo con el siguiente
    ubicaciones_barco(puestos, filas, columnas, barcos, barco_act+1, mejores_puestos)
    
def backtracking(filas, columnas, barcos):
    mejores_puestos = [Barco(-1, set(), True)]
    # Al final no mejora nada ordenando las filas por mayor demanda
    dict_filas = {i: demanda for i, demanda in enumerate(filas)}
    dict_filas_ordenado = dict(sorted(dict_filas.items(), key=lambda item: item[0], reverse=False))

    # Al final no mejora nada ordenando las columnas por mayor demanda
    dict_columnas = {i: demanda for i, demanda in enumerate(columnas)}
    dict_columnas_ordenado = dict(sorted(dict_columnas.items(), key=lambda item: item[0], reverse=False))

    # Ordeno los barcos de mayor a menor longitud
    tuplas = [(i, largo) for i, largo in enumerate(barcos)]
    barcos_ordenados = sorted(tuplas, key=lambda x: x[1], reverse=True)

    ubicaciones_barco(set(), dict_filas_ordenado, dict_columnas_ordenado, barcos_ordenados, 0, mejores_puestos)
    return mejores_puestos, demanda(mejores_puestos, filas, columnas)

# Para correr el codigo, se debe pasar por parametro un .txt 
# que tengo el mismo formato que los test de la catedra
# Ejemplo: python3 tercera_parte.py test_data/3_3_2.txt (u otro .txt)
#
# Para correr los test de la catedra:
# $ chmod +x run_test.sh
# $ ./run_test.sh

if __name__ == "__main__":
    argumentos = sys.argv
    if len(argumentos) != 2:
        raise AssertionError("Error: se esperaba solo 2 argumentos")

    filas, columnas, barcos = extraer_datos_archivo(argumentos[1])

    inicio = time.time() 
    barcos_puestos, demanda_cumplida = backtracking(filas, columnas, barcos)
    fin = time.time()  
    tiempo_ejecucion = f"Tiempo de ejecución: {fin - inicio:.6f} segundos"
    
    print(tiempo_ejecucion)
    print(argumentos[1].split("/")[-1])
    barcos_ordenados = sorted(barcos_puestos, key=lambda barco: barco.id())
    for barco in barcos_ordenados:
        print(barco.mostrar())
    
    print("Demanda cumplida: " + str(demanda_cumplida))
    print("Demanda total: " + str(sum(filas)+sum(columnas)))