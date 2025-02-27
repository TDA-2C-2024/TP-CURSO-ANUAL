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
# python3 primera_parte.py test_data/20.txt (u otro txt con el mismo formato) 

# Para correr los test de la catedra:
# $ chmod +x run_test_greedy.sh
# $ ./run_test_greedy.sh
if __name__ == "__main__":

    argumentos = sys.argv
    if len(argumentos) != 2:
        raise AssertionError("Error: se esperaba solo 2 argumentos")

    monedas = deque(serializar_txt(argumentos[1]))
    copia_monedas = monedas.copy()
    resultados = algoritmo_greedy(monedas)
    ganancia_sophia = []
    ganancia_mateo = []
    for eleccion in resultados:
        if eleccion == primera_moneda_sophia:
            ganancia_sophia.append(copia_monedas.popleft())
        elif eleccion == ultima_moneda_sophia:
            ganancia_sophia.append(copia_monedas.pop())
        elif eleccion == primera_moneda_mateo:
            ganancia_mateo.append(copia_monedas.popleft())
        elif eleccion == ultima_moneda_mateo:
            ganancia_mateo.append(copia_monedas.pop())
    
    print(argumentos[1])
    print("; ".join(resultados))
    print("Ganancia de Sophia: " + str(sum(ganancia_sophia)))
    print("Ganancia de Mateo: " + str(sum(ganancia_mateo)))