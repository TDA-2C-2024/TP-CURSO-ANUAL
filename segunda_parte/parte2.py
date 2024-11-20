import sys
from collections import deque

sys.setrecursionlimit(20000)

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

# Ec de recurrencia?: 
# Opt(i,j) = max( M[i]+max(Opt(i+2,j),Opt(i+1,j-1)) , M[j]+max(Opt(i+1,j-1), Opt(i,j-2)) )


def obtener_cantidad_max(arr):
    n = len(arr)
    optimos = [[0] * n for _ in range(n)] #Inicializo la matriz con 0's
    solucion = buscar_solucion_iterativa(arr, optimos)
    print("Solucion: ", solucion)
    for fila in optimos:
        print(fila)
    monedas_sofia, monedas_mateo = reconstruir_monedas(arr, optimos)
    print("Sofia:", monedas_sofia)
    print("Mateo:", monedas_mateo)
    print("Ganancias sofia: ", sum(monedas_sofia))
    print("Ganancias mateo: ", sum(monedas_mateo))


def reconstruir_monedas(arr, dp):
    n = len(arr)
    i, j = 0, n - 1
    camino_sofia = []
    camino_mateo = []

    while i <= j:
        # Opción 1: Sofía toma arr[i]
        if arr[i + 1] > arr[j]:
            take_first = arr[i] + (dp[i + 2][j] if i + 2 <= j else 0)  # Mateo toma arr[i + 1]
        else:
            take_first = arr[i] + (dp[i + 1][j - 1] if i + 1 <= j - 1 else 0)  # Mateo toma arr[j]

        # Opción 2: Sofía toma arr[j]
        if arr[i] > arr[j - 1]:
            take_last = arr[j] + (dp[i + 1][j - 1] if i + 1 <= j - 1 else 0)  # Mateo toma arr[i]
        else:
            take_last = arr[j] + (dp[i][j - 2] if i <= j - 2 else 0)  # Mateo toma arr[j - 1]

        # Sofía elige la mejor opción
        if dp[i][j] == take_first:
            camino_sofia.append(arr[i])  # Sofía toma la moneda de la izquierda
            if i + 1 <= j:  # Verificar si hay una elección válida para Mateo
                if arr[i + 1] > arr[j]:
                    camino_mateo.append(arr[i + 1])
                    i += 2  # Mateo toma arr[i + 1]
                else:
                    camino_mateo.append(arr[j])
                    i += 1  # Mateo toma arr[j]
                    j -= 1
            else:
                i += 1  # Sofía toma la última moneda
        else:
            camino_sofia.append(arr[j])  # Sofía toma la moneda de la derecha
            if i <= j - 1:  # Verificar si hay una elección válida para Mateo
                if arr[i] > arr[j - 1]:
                    camino_mateo.append(arr[i])
                    i += 1  # Mateo toma arr[i]
                    j -= 1
                else:
                    camino_mateo.append(arr[j - 1])
                    j -= 2  # Mateo toma arr[j - 1]
            else:
                j -= 1  # Sofía toma la última moneda

    return camino_sofia, camino_mateo


def buscar_solucion_iterativa(arr, dp):
    n = len(arr)
    # Crear la tabla dp
    #dp = [[0] * n for _ in range(n)]
    
    # Casos base
    for i in range(n):
        dp[i][i] = arr[i]  # Una sola moneda
    for i in range(n - 1):
        dp[i][i + 1] = max(arr[i], arr[i + 1])  # Dos monedas
    
    # Llenar la tabla para intervalos mayores
    for length in range(2, n):  # Longitud del intervalo
        for i in range(n - length):
            j = i + length
            # Calcular dp[i][j]
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



if __name__ == "__main__":

    argumentos = sys.argv
    if len(argumentos) != 2:
        raise AssertionError("Error: se esperaba solo 2 argumentos")

    monedas = deque(serializar_txt(argumentos[1]))
    #monedas = [1,10, 5]
    print("Monedas: ", monedas)

    resultado = obtener_cantidad_max(monedas)

    # respuesta_final = ""
    # for rta in resultado:
    #     respuesta_final += rta + "; "
