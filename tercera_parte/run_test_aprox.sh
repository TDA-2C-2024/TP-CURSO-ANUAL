#!/bin/bash

test_data="test_data_aprox"
output="results/results_${test_data}_aprox.txt"

> "$output"

ls -v "$test_data"/*.txt | while read archivo; do
    if [[ "$(basename "$archivo")" == "30_25_25.txt" ]]; then
        continue 
    fi
    python3 aproximacion.py "$archivo" >> "$output"
    echo "" >> "$output"
done

echo "Todos los resultados se han guardado en '$output'."
