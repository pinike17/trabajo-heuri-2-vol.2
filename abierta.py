# abierta.py (CORREGIDO)

import heapq

class Abierta:
    """
    Implementación de la Lista Abierta usando una Cola de Prioridad (Min-Heap).
    Los elementos se almacenan como tuplas: (f_cost, node_id).
    """

    def __init__(self):
        # Lista usada como heap binario.
        self._heap = []
        # Diccionario para verificar la existencia y el mejor costo conocido.
        self._entry_finder = {} # {node_id: f_cost}
        # Contador de prioridad (para desempate)
        self._counter = 0

    def push(self, f_cost, node_id):
        """
        Añade un nodo o actualiza su prioridad si ya existe.
        """
        
        # Solo se inserta si es un camino de costo MEJOR.
        if node_id in self._entry_finder and f_cost >= self._entry_finder[node_id]:
            return

        entry = [f_cost, self._counter, node_id]
        heapq.heappush(self._heap, entry)
        self._entry_finder[node_id] = f_cost
        self._counter += 1

    def pop(self):
        """Extrae el nodo con el menor costo f(n), ignorando entradas obsoletas."""
        if not self._heap:
            raise IndexError("pop from empty heap")

        while self._heap:
            # Extrae el elemento de menor costo.
            f_cost, _, node_id = heapq.heappop(self._heap)
            
            # **CORRECCIÓN CLAVE:** # 1. Verificamos si el nodo existe en el entry_finder.
            # 2. Verificamos si el costo extraído coincide con el mejor costo conocido.
            if node_id in self._entry_finder and f_cost == self._entry_finder[node_id]:
                 # Es la entrada válida (la de menor costo). La eliminamos y retornamos.
                del self._entry_finder[node_id] 
                return node_id
            
            # Si llegamos aquí, la entrada es obsoleta (ya que la válida fue extraída
            # o se encontró un camino mejor), y la ignoramos (el loop continúa).
            
        raise IndexError("pop from empty heap") # Se lanza si el heap se vacía sin encontrar un nodo válido
        
    def is_empty(self):
        """Verifica si la lista abierta está vacía."""
        return not self._entry_finder