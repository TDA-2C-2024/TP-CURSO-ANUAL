class Barco:
    def __init__(self, numero, posiciones, direccion):
        self.numero = numero
        self.posiciones = posiciones 
        self.direccion = direccion 

    def esta_superpuesto(self, otro_barco):
        return bool(self.posiciones & otro_barco.posiciones)

    def longitud(self):
        return len(self.posiciones)
    
    def esta_horizontal(self):
        return self.direccion == "horizontal"
    
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
        return f"{self.numero}: {sorted(self.posiciones)}"