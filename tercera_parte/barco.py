"""
Clase Barco

Modela un barco en el juego de batalla naval.
El mismo cuenta con las posiciones que ocupa, su direccion y su identificador.
Ayuda fundamentalmente a verificar si:
- Esta superpuesto con otros barcos.
- Tiene adyacencia con otros barcos.
- Excede demanda en el juego.
"""
class Barco:
    def __init__(self, numero, posiciones, direccion):
        self.numero = numero
        self.posiciones = posiciones 
        self.direccion = direccion 

    def esta_superpuesto(self, otro_barco):
        return bool(self.posiciones & otro_barco.posiciones)
    
    def id(self):
        return self.numero
    
    def _posiciones_adyacentes(self, pos):
        fila, columna = pos
        return {
            (fila - 1, columna - 1), (fila - 1, columna), (fila - 1, columna + 1),
            (fila, columna - 1),                        (fila, columna + 1),
            (fila + 1, columna - 1), (fila + 1, columna), (fila + 1, columna + 1)
        }

    def esta_adyacente(self, otro_barco):
        adyacentes = set()
        for posicion in self.posiciones:
            adyacentes.update(self._posiciones_adyacentes(posicion))
        
        adyacentes -= self.posiciones

        return bool(adyacentes & otro_barco.posiciones)
    
    def mostrar(self):
        return f"{self.numero}: {' - '.join(map(str, sorted(self.posiciones)))}"
    
    def excede_demanda(self, filas, columnas, puestos):
        # Calculo demanda actual
        demanda_fila = [0] * len(filas) 
        demanda_columna = [0] * len(columnas) 
        for barco in puestos:
            for (fila, columna) in barco.posiciones:
                demanda_fila[fila] += 1
                demanda_columna[columna] += 1

        # Calcula la demanda por el barco
        filas_ocupadas = [0] * len(filas) 
        columnas_ocupadas = [0] * len(columnas) 
        for (fil, col) in self.posiciones:
            filas_ocupadas[fil] += 1
            columnas_ocupadas[col] += 1

        # Verifico que la demanda del barco no exceda a la demanda por cumplir
        for i in range(len(filas)):
            if filas[i] - demanda_fila[i] < filas_ocupadas[i]:
                return True  
        for j in range(len(columnas)):
            if columnas[j] - demanda_columna[j] < columnas_ocupadas[j]:
                return True  
        return False  