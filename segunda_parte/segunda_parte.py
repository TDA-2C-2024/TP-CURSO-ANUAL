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

primera_moneda_sophia = "Sophia debe agarrar la primera (%d)"
ultima_moneda_sophia = "Sophia debe agarrar la ultima (%d)"
primera_moneda_mateo = "Mateo agarra la primera (%d)"
ultima_moneda_mateo = "Mateo agarra la ultima (%d)"


def obtener_cantidad_max(arr):
    n = len(arr)
    optimos = [[0] * n for _ in range(n)]  # Inicializo la matriz con 0's
    solucion = buscar_solucion_iterativa(arr, optimos)
    return reconstruir_monedas(arr, optimos)


def reconstruir_monedas(arr, dp):
    n = len(arr)
    i, j = 0, n - 1
    camino_sofia = []
    camino_mateo = []
    resultado = []

    while i < j:
        # Opción 1: Sofía toma arr[i]
        if arr[i + 1] > arr[j]:
            # Mateo toma arr[i + 1]
            take_first = arr[i] + (dp[i + 2][j] if i + 2 <= j else 0)
        else:
            # Mateo toma arr[j]
            take_first = arr[i] + (dp[i + 1][j - 1] if i + 1 <= j - 1 else 0)

        # Opción 2: Sofía toma arr[j]
        if arr[i] > arr[j - 1]:
            take_last = arr[j] + (dp[i + 1][j - 1] if i +
                                  1 <= j - 1 else 0)  # Mateo toma arr[i]
        else:
            # Mateo toma arr[j - 1]
            take_last = arr[j] + (dp[i][j - 2] if i <= j - 2 else 0)

        # Sofía elige la mejor opción
        if dp[i][j] == take_first:
            moneda_s = arr[i]
            # Sofía toma la moneda de la izquierda
            camino_sofia.append(moneda_s)
            resultado.append(primera_moneda_sophia % (moneda_s))
            if i + 1 <= j:  # Verificar si hay una elección válida para Mateo
                if arr[i + 1] > arr[j]:
                    moneda_m = arr[i + 1]
                    camino_mateo.append(moneda_m)
                    resultado.append(primera_moneda_mateo % (moneda_m))
                    i += 2  # Mateo toma arr[i + 1]
                else:
                    moneda_m = arr[j]
                    camino_mateo.append(moneda_m)
                    resultado.append(ultima_moneda_mateo % (moneda_m))
                    i += 1  # Mateo toma arr[j]
                    j -= 1
            else:
                i += 1  # Sofía toma la última moneda
        else:
            moneda_s = arr[j]
            camino_sofia.append(moneda_s)  # Sofía toma la moneda de la derecha
            resultado.append(ultima_moneda_sophia % (moneda_s))
            if i <= j - 1:  # Verificar si hay una elección válida para Mateo
                if arr[i] > arr[j - 1]:
                    moneda_m = arr[i]
                    camino_mateo.append(moneda_m)
                    resultado.append(primera_moneda_mateo % (moneda_m))
                    i += 1  # Mateo toma arr[i]
                    j -= 1
                else:
                    moneda_m = arr[j - 1]
                    camino_mateo.append(moneda_m)
                    resultado.append(ultima_moneda_mateo % (moneda_m))
                    j -= 2  # Mateo toma arr[j - 1]
            else:
                j -= 1  # Sofía toma la última moneda
    if i == j:
        moneda_s = arr[i]
        camino_sofia.append(moneda_s)
        resultado.append(primera_moneda_sophia % (moneda_s))

    return camino_sofia, camino_mateo, resultado


def buscar_solucion_iterativa(arr, dp):
    n = len(arr)


    # Casos base
    for i in range(n):
        dp[i][i] = arr[i]  # Una sola moneda
    for i in range(n - 1):
        dp[i][i + 1] = max(arr[i], arr[i + 1])  # Dos monedas

    for length in range(2, n):  # Longitud del intervalo
        for i in range(n - length):
            j = i + length
            # Si Sofia toma la moneda arr[i]
            if arr[i + 1] > arr[j]:
                take_first = arr[i] + dp[i + 2][j]  # Mateo elige arr[i + 1]
            else:
                take_first = arr[i] + dp[i + 1][j - 1]  # Mateo elige arr[j]

            # Si Sofia toma la moneda arr[j]
            if arr[i] > arr[j - 1]:
                take_last = arr[j] + dp[i + 1][j - 1]  # Mateo elige arr[i]
            else:
                take_last = arr[j] + dp[i][j - 2]  # Mateo elige arr[j - 1]

            # Sofia maximiza su ganancia
            dp[i][j] = max(take_first, take_last)

    # El resultado está en dp[0][n-1]
    return dp[0][n - 1]


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
 
    print("Ganancias Sofia: ", sum(monedas_sofia))
    print("Ganancias Mateo: ", sum(monedas_mateo))
