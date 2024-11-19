def buscar_solucion(i, j, arr, optimos):
    #ganancia_parcial_sofia = []
    #ganancia_parcial_mateo = []

    #turnos = len(arr)
    #for i in range(turnos)

    # Caso base, no hay mas monedas para agarrar
    if i > j:
        return 0

    if len(arr) == 1:
        return arr[0]
    
    if len(arr) == 2:
        return max(arr[0], arr[1])
    
    if len(arr) == 3:
        return max(arr[0], arr[2])
    
    if optimos[i][j] != 0:
        return optimos[i][j]
    
    # Sofia toma la primer moneda arr[i], por lo que Mateo elige
    # la mayor entre la siguiente M[i+1] o la ultima M[j];
    if arr[i+1] > arr[j]:
        takeFirst = arr[i] + buscar_solucion(i+2, j, arr, optimos)
    else:
        takeFirst = arr[i] + buscar_solucion(i+1, j-1, arr, optimos)
    
    # Sofia toma la ultima moneda arr[j], por lo que Mateo elige
    # la mayor entre la primera M[i] o la anteúltima M[j-1]
    if arr[i] > arr[j-1]:
        takeLast = arr[j] + buscar_solucion(i+1, j-1, arr, optimos)
    else:
        takeLast = arr[j] + buscar_solucion(i, j-2, arr, optimos)

    # Guardo el maximo entre los 2 posibles valores
    optimos[i][j] = max(takeFirst, takeLast)
    return optimos[i][j]

    """
    # Sofia toma la primer moneda arr[i], por lo que Mateo elige
    # la mayor entre la siguiente M[i+1] o la ultima M[j];
    takeFirst = arr[i] + max(buscar_solucion(i+2, j, arr, optimos),
                            buscar_solucion(i+1, j-1, arr, optimos))


    # Sofia toma la ultima moneda arr[j], por lo que Mateo elige
    # la mayor entre la primera M[i] o la anteúltima M[j-1]
    takeLast = arr[j] + max(buscar_solucion(i+1, j-1, arr, optimos),
                            buscar_solucion(i, j-2, arr, optimos))

    """

def reconstruir_elecciones(arr, optimos):
    i = 0
    j = len(arr)-1
    monedas_sofia = []
    monedas_mateo = []

    while i<j:
        # Determinar si Sofía toma la primera o la última moneda
        if arr[i+1] > arr[j]:
            takeFirst = arr[i] + buscar_solucion(i+2, j, arr, optimos)
        else:
            takeFirst = arr[i] + buscar_solucion(i+1, j-1, arr, optimos)

        if arr[i] > arr[j-1]:
            takeLast = arr[j] + buscar_solucion(i+1, j-1, arr, optimos)
        else:
            takeLast = arr[j] + buscar_solucion(i, j-2, arr, optimos)

        if takeFirst >= takeLast:
            monedas_sofia.append(arr[i])
            # El adversario toma la mayor entre arr[i+1] y arr[j]
            if arr[i+1] >= arr[j]:
                monedas_mateo.append(arr[i + 1])
                i += 2  # Avanzar dos posiciones
            else:
                monedas_mateo.append(arr[j])
                i += 1
                j -= 1
        else:
            monedas_sofia.append(arr[j])
            # El adversario toma la mayor entre arr[i] y arr[j-1]
            if arr[i] >= arr[j-1]:
                monedas_mateo.append(arr[i])
                i += 1
                j -= 1
            else:
                monedas_mateo.append(arr[j-1])
                j -= 2  # Reducir dos posiciones
    return monedas_sofia, monedas_mateo
