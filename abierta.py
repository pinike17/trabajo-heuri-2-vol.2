# abierta.py

import heapq

class Abierta:
    """
    Implementación de la Lista Abierta usando una Cola de Prioridad (Min-Heap).
    Los elementos se almacenan como tuplas: (f_cost, node_id).
    """

    def __init__(self):
        # Lista usada como heap binario.
        self._heap = []
        # Diccionario para verificar la existencia del nodo en O(1)
        # {node_id: f_cost}
        self._entry_finder = {}
        # Contador de prioridad (para desempate)
        self._counter = 0

    def push(self, f_cost, node_id):
        """
        Añade un nodo o actualiza su prioridad si ya existe.
        La actualización se hace añadiendo una nueva entrada al heap; la antigua se ignora.
        """
        
        # Si el nodo ya está en el entry_finder, significa que hay una entrada antigua
        # en el heap con un costo más alto. No necesitamos hacer nada.
        # En una implementación más robusta, se usa una técnica de "invalidación" para
        # no re-procesar las entradas antiguas, pero por simplicidad de A*,
        # simplemente dejamos que el nodo con menor costo sea extraído primero.
        
        if node_id in self._entry_finder and f_cost >= self._entry_finder[node_id]:
            return

        entry = [f_cost, self._counter, node_id]
        heapq.heappush(self._heap, entry)
        self._entry_finder[node_id] = f_cost
        self._counter += 1

    def pop(self):
        """Extrae el nodo con el menor costo f(n)."""
        if not self._heap:
            raise IndexError("pop from empty heap")

        while self._heap:
            # Extrae el elemento de menor costo.
            f_cost, _, node_id = heapq.heappop(self._heap)
            
            # Verificamos si este nodo ya ha sido extraído con un costo menor.
            # Solo extraemos si el costo coincide con el mejor costo conocido.
            if f_cost == self._entry_finder[node_id]:
                 # Elimina la entrada del entry_finder, indicando que ha sido expandido.
                del self._entry_finder[node_id] 
                return node_id
            
        raise IndexError("pop from empty heap")
        
    def is_empty(self):
        """Verifica si la lista abierta está vacía."""
        return not self._entry_finder # Mejor chequeo usando el entry_finder limpio