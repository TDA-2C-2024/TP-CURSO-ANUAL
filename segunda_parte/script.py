import os
import re
import time
from segunda_parte import serializar_txt, obtener_cantidad_max
from collections import deque

if __name__ == "__main__":
    # Current Path
    cwd = os.getcwd()
    data_path = cwd + '/test_data'
    
    result = open(cwd + "/test_data/output_datos_test.txt", "a")
    performance = open(cwd + "/mediciones/output_tiempo_test_data.txt", "a")

    # Get all test cases
    for (root, dirs, file) in os.walk(data_path):
        for f in sorted(file, key=lambda x: len(x)):
            if re.search("[0-9]+.txt", f):
                monedas = (deque(serializar_txt(root+'/'+f)))
                
                start = time.time()
                monedas_sofia, monedas_mateo, resultado = obtener_cantidad_max(monedas)
                elapsed = time.time() - start
                
                result.write(f + '\n')
                result.write("; ".join(resultado) + '\n')
                result.write(f"Ganancias Sofia: {sum(monedas_sofia)}" + '\n')
                result.write(f"Ganancias Mateo: {sum(monedas_mateo)}" + '\n\n')
                
                performance.write(f + '\n')
                performance.write(str(elapsed) + '\n\n')

    result.close()
    performance.close()
    
    print("All test finished")
