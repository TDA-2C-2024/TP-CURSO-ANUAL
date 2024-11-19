import sys
from collections import deque

primera_moneda_sophia ="Primera moneda para Sophia"
ultima_moneda_sophia = "Última moneda para Sophia"
primera_moneda_mateo = "Primera moneda para Mateo"
ultima_moneda_mateo = "Última moneda para Mateo"

def serializar_txt(nombre_txt):
    with open(nombre_txt, 'r') as archivo:
        lineas = archivo.readlines()
        segunda_linea = lineas[1].strip()
        valores = [int(valor) for valor in segunda_linea.split(';')]

    return valores

def agarrar_moneda(monedas, resultado, es_sophia):
    primera_moneda = monedas.popleft()
    ultima_moneda = monedas.pop()
    
    if es_sophia: # Turno de Sophia, elije siempre la mayor
        if primera_moneda > ultima_moneda:
            resultado.append(primera_moneda_sophia) 
            monedas.append(ultima_moneda)  
        else:
            resultado.append(ultima_moneda_sophia)
            monedas.appendleft(primera_moneda)
    else: # Turno de Mateo, elije siempre la menor
        if primera_moneda > ultima_moneda:
            resultado.append(ultima_moneda_mateo)
            monedas.appendleft(primera_moneda) 
        else:
            resultado.append(primera_moneda_mateo)
            monedas.append(ultima_moneda) 

def algoritmo_greedy(monedas):
    resultado = []
    es_turno_sophia = True
    while len(monedas) >= 2: 
        agarrar_moneda(monedas, resultado, es_turno_sophia)
        es_turno_sophia = not es_turno_sophia  # Cambio de turno
    
    # Ultimo turno
    if es_turno_sophia:
        resultado.append(ultima_moneda_sophia)
    else:
        resultado.append(ultima_moneda_mateo)
    
    return resultado

# Para ejecutar:
# python3 primera_parte.py datos_test/20.txt (u otro txt) 
if __name__ == "__main__":

    argumentos = sys.argv
    if len(argumentos) != 2:
        raise AssertionError("Error: se esperaba solo 2 argumentos")

    monedas = deque(serializar_txt(argumentos[1]))

    resultado = algoritmo_greedy(monedas)

    respuesta_final = ""
    for rta in resultado:
        respuesta_final += rta + "; "

    print(respuesta_final[:-2])
