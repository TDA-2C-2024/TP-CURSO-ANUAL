#!/bin/bash

test_data="test_data_bt"
output="results/results_${test_data}_bt_probando.txt"

> "$output"

ls -v "$test_data"/*.txt | while read archivo; do
    if [[ "$(basename "$archivo")" == "30_25_25.txt" ]]; then
        continue 
    fi
    python3 backtracking.py "$archivo" >> "$output"
    echo "" >> "$output"
done

echo "Todos los resultados se han guardado en '$output'."
