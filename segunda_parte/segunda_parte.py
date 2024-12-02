import sys
from collections import deque

sys.setrecursionlimit(20000)

primera_moneda_sophia = "Primera moneda para Sophia"
ultima_moneda_sophia = "Última moneda para Sophia"
primera_moneda_mateo = "Primera moneda para Mateo"
ultima_moneda_mateo = "Última moneda para Mateo"


def serializar_txt(nombre_txt):
    with open(nombre_txt, 'r') as archivo:
        lineas = archivo.readlines()
        segunda_linea = lineas[1].strip()
        valores = [int(valor) for valor in segunda_linea.split(';')]

    return valores

# Ec de recurrencia?:
# Opt(i,j) = max( M[i]+max(Opt(i+2,j),Opt(i+1,j-1)) , M[j]+max(Opt(i+1,j-1), Opt(i,j-2)) )


primera_moneda_sophia = "Sophia debe agarrar la primera (%d)"
ultima_moneda_sophia = "Sophia debe agarrar la ultima (%d)"
primera_moneda_mateo = "Mateo agarra la primera (%d)"
ultima_moneda_mateo = "Mateo agarra la ultima (%d)"


def obtener_cantidad_max(arr):
    n = len(arr)
    optimos = [[0] * n for _ in range(n)]  # Inicializo la matriz con 0's
    buscar_solucion_iterativa(arr, optimos)
    return reconstruir_monedas(arr, optimos)


def buscar_solucion_iterativa(arr, optimos):
    n = len(arr)

    # Llenar los casos base (intervalos de longitud 1)
    for i in range(n):
        optimos[i][i] = arr[i]

    # Llenar la matriz para intervalos de longitud creciente
    for longitud in range(2, n + 1):  # Longitud de los subarreglos
        for i in range(n - longitud + 1):
            j = i + longitud - 1

            # Si tomamos el primero o el último, minimizamos la ganancia del oponente
            tomar_primero = arr[i] + min(
                optimos[i + 2][j] if i + 2 <= j else 0,
                optimos[i + 1][j - 1] if i + 1 <= j - 1 else 0
            )
            tomar_ultimo = arr[j] + min(
                optimos[i + 1][j - 1] if i + 1 <= j - 1 else 0,
                optimos[i][j - 2] if i <= j - 2 else 0
            )

            # Almacenar el mejor resultado en optimos[i][j]
            optimos[i][j] = max(tomar_primero, tomar_ultimo)
    
    return optimos[0][n - 1]   


def reconstruir_monedas(arr, optimos):
    n = len(arr)
    camino_sophia = []  # Monedas seleccionadas por Sophia
    camino_mateo = []  # Monedas seleccionadas por Mateo
    resultado = []  # Lista para guardar los mensajes sobre las decisiones
    start, end = 0, n - 1
    turno_sophia = True  # Indica si es el turno de Sophia

    while start <= end:
        # Determinar si tomar el primer o último elemento
        tomar_primero = arr[start] + min(
            optimos[start + 2][end] if start + 2 <= end else 0,
            optimos[start + 1][end - 1] if start + 1 <= end - 1 else 0
        )
        tomar_ultimo = arr[end] + min(
            optimos[start + 1][end - 1] if start + 1 <= end - 1 else 0,
            optimos[start][end - 2] if start <= end - 2 else 0
        )

        # Comparar con el valor en optimos para decidir
        if optimos[start][end] == tomar_primero:
            if turno_sophia:
                camino_sophia.append(arr[start])
                resultado.append(primera_moneda_sophia % arr[start])
            else:
                camino_mateo.append(arr[start])
                resultado.append(primera_moneda_mateo % arr[start])
            start += 1
        else:
            if turno_sophia:
                camino_sophia.append(arr[end])
                resultado.append(ultima_moneda_sophia % arr[end])
            else:
                camino_mateo.append(arr[end])
                resultado.append(ultima_moneda_mateo % arr[end])
            end -= 1

        # Cambiar el turno
        turno_sophia = not turno_sophia

    return camino_sophia, camino_mateo, resultado



# Para ejecutar:
# python3 segunda_parte.py test_data/5.txt (u otro txt con el mismo formato)
if __name__ == "__main__":

    argumentos = sys.argv
    if len(argumentos) != 2:
        raise AssertionError("Error: se esperaba solo 2 argumentos")

    monedas = deque(serializar_txt(argumentos[1]))
    # print("Monedas: ", monedas)

    monedas_sofia, monedas_mateo, resultado = obtener_cantidad_max(monedas)
    print("; ".join(resultado))
    # print("Sofia:", monedas_sofia)
    # print("Mateo:", monedas_mateo)
    print("Ganancias Sofia: ", sum(monedas_sofia))
    print("Ganancias Mateo: ", sum(monedas_mateo))
