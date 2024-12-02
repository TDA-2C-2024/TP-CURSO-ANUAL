#!/bin/bash

test_data="test_data"
output="results/results_${test_data}.txt"

> "$output"

ls -v "$test_data"/*.txt | while read archivo; do

    python3 primera_parte.py "$archivo" >> "$output"
    echo "" >> "$output"
done

echo "Todos los resultados se han guardado en '$output'."
