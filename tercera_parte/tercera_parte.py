import sys

from barco import Barco
from util import extraer_datos_archivo

def estan_superpuesto(puestos, barco):
    for otro_barco in puestos:
            if barco.esta_superpuesto(otro_barco): 
                return True  
    return False
    
def estan_adyacentes(puestos, barco):
    for otro_barco in puestos:
        if barco.esta_adyacente(otro_barco):
            return True  
    return False

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

def tratar_de_ubicar_barco(demanda_total, puestos, filas, columnas, barcos, barco_act, direccion, pos_fil, pos_col, mejores_puestos):
    posiciones, se_pudo = colocar_barco(direccion, pos_fil, pos_col, filas, columnas, barcos[barco_act])

    if se_pudo:
        barco = Barco(barco_act, posiciones, direccion)
        # Checkeo que no se superponga con los demas, o que sea adyacente
        if estan_superpuesto(puestos, barco) or estan_adyacentes(puestos, barco):
            return
        
        puestos.add(barco)
        ubicaciones_barco(demanda_total, puestos, filas, columnas, barcos, barco_act + 1, mejores_puestos)
        puestos.remove(barco)

# Demanda cumplida
def demanda(puestos):
    filas_ocupadas = [0] * len(filas) 
    columnas_ocupadas = [0] * len(columnas) 

    for barco in puestos:
        for (fila, columna) in barco.posiciones:
            filas_ocupadas[fila] += 1
            columnas_ocupadas[columna] += 1
     
    return sum(filas_ocupadas) + sum(columnas_ocupadas)

def excede_demanda(filas, columnas, puestos):
    filas_ocupadas = [0] * len(filas) 
    columnas_ocupadas = [0] * len(columnas) 

    for barco in puestos:
        for (fila, columna) in barco.posiciones:
            filas_ocupadas[fila] += 1
            columnas_ocupadas[columna] += 1

    for i in range(len(filas)):
        if filas_ocupadas[i] > filas[i]:
            return True  
    for i in range(len(columnas)):
        if columnas_ocupadas[i] > columnas[i]:
            return True  

    return False  

def ubicaciones_barco(demanda_total, puestos, filas, columnas, barcos, barco_act, mejores_puestos):
    # Me fijo si no me excedi alguna demanda de la columna o fila
    if excede_demanda(filas, columnas, puestos):
        return
    
    # Me quedo con los barcos que tenga la menor demanda incumplida
    if demanda_total - demanda(puestos) <= demanda_total - demanda(mejores_puestos):
        # Con el igual, me queda una solucion muy parecida a la catedra
        mejores_puestos[:] = puestos

    if barco_act >= len(barcos):
        return
    
    for n in range(len(filas)):
        for m in range(len(columnas)):
            # Tarda mucho, ver porque
            #tratar_de_ubicar_barco(demanda_total, puestos, filas, columnas, barcos, barco_act, 'horizontal', n, m, mejores_puestos)
            tratar_de_ubicar_barco(demanda_total, puestos, filas, columnas, barcos, barco_act, 'vertical',  n, m, mejores_puestos)
                
    # No lo coloco directamente, asi que sigo con el siguiente
    ubicaciones_barco(demanda_total, puestos, filas, columnas, barcos, barco_act+1, mejores_puestos)
    
def backtracking(filas, columnas, barcos):
    mejores_puestos = [Barco(-1, set(), True)]
    demanda_total = sum(filas) + sum(columnas)
    ubicaciones_barco(demanda_total, set(), filas, columnas, barcos, 0, mejores_puestos)
    return mejores_puestos, demanda(mejores_puestos)

if __name__ == "__main__":
    argumentos = sys.argv
    if len(argumentos) != 2:
        raise AssertionError("Error: se esperaba solo 2 argumentos")

    filas, columnas, barcos = extraer_datos_archivo(argumentos[1])
    barcos_puestos, demanda_cumplida = backtracking(filas, columnas, barcos)

    for barco in barcos_puestos:
        print(barco.mostrar())
    
    print("Demanda cumplida: " + str(demanda_cumplida))
