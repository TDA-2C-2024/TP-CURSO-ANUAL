# Ejecución

## Con un archivo de texto

### Algoritmo de Backtracking
Para ejecutar el algoritmo backtracking con un archivo `.txt` que contenga las demandas de las filas y columnas, y los largos de los barcos, debe poner en la consola:

```bash
python3 backtracking.py <ruta_del_archivo_txt>
```

- **<ruta_del_archivo_txt>**: ruta del archivo .txt que contiene las variables del problema. El archivo debe estar en un formato igual a los ejemplos proporcionados por la cátedra.

#### Output

El resultado de la ejecucion se muestra por consola.

### Algoritmo de Aproximacion
De manera similar a la ejecucion del algoritmo de backtracking, debe poner en consola:

```bash
python3 aproximacion.py <ruta_del_archivo_txt>
```

### Verificador eficiente
De manera similar a la ejecucion de los anteriores algoritmos, debe poner en consola:

```bash
python3 verificador_eficiente.py <ruta_del_archivo_txt>
```

## Con los tests

### Algoritmo Backtracking
Para ejecutar los tests proporcionados por la cátedra, debe poner en la consola:

```bash
chmod +x run_test_bt.sh
./run_test_bt.sh
```

#### Output

Los resultados se guardaran (de forma predeterminada) en la carpeta `results` dentro del archivo `results_test_data_bt_bt.txt`. 

Esto lo podra cambiar a a eleccion dentro del script, modificando las variables `test_data` y `output`.

Aclaracion: no se ejecuta el test 30_25_25.txt debido a que tarda varios minutos.

### Algoritmo de Aproximacion
De manera similar a la ejecucion del algoritmo de backtracking, debe poner en consola:

```bash
chmod +x run_test_aprox.sh
./run_test_aprox.sh
```

