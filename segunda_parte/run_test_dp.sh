#!/bin/bash

test_data="test_data"
output="results/results_${test_data}.txt"

# Crear o vaciar el archivo de resultados
> "$output"

# Procesar cada archivo en el directorio test_data
ls -v "$test_data"/*.txt | while read archivo; do
    # Ejecutar el script de Python para la segunda parte
    python3 segunda_parte.py "$archivo" >> "$output"
    echo "" >> "$output"
done

echo "Todos los resultados de la parte 2 se han guardado en '$output'."
