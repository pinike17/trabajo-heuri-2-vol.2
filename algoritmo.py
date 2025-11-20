# algoritmo.py

from abierta import Abierta
from cerrada import Cerrada

class AStarSolver:
    """
    Implementación del algoritmo de búsqueda A* para encontrar el camino más corto.
    """

    def __init__(self, grafo):
        self.grafo = grafo
        self.closed = Cerrada()
        self.open = Abierta()
        self.g_costs = {} # {node_id: g_cost} - Mejor costo encontrado hasta ahora

    def _calculate_h(self, node_id, goal_id):
        """Calcula el costo heurístico (distancia Haversine)."""
        return self.grafo.haversine_distance(node_id, goal_id)

    def solve(self, start_id, goal_id):
        """
        Ejecuta el algoritmo A* desde start_id hasta goal_id.
        Retorna (costo_optimo, nodos_expandidos).
        """
        
        # Validación de vértices
        if start_id not in self.grafo.coords or goal_id not in self.grafo.coords:
            return 0, 0 # Error o ruta no válida

        # 1. Inicialización
        self.g_costs[start_id] = 0
        h_start = self._calculate_h(start_id, goal_id)
        f_start = h_start
        
        self.open.push(f_start, start_id)
        # Inicializamos el nodo de inicio en la lista cerrada (que también rastrea padres)
        # para que se pueda reconstruir el camino si la meta es el inicio.
        self.closed.add(start_id, 0, None) 
        
        nodes_expanded = 0

        # 2. Bucle principal de A*
        while not self.open.is_empty():
            current_id = self.open.pop()

            # El nodo actual ya fue expandido y movido al ClosedSet en un camino más corto
            # En nuestro caso, la lógica de Abierta previene esto, ya que pop solo retorna
            # la entrada con el menor f_cost.

            if current_id == goal_id:
                # ¡Meta alcanzada!
                return self.g_costs[goal_id], nodes_expanded
            
            nodes_expanded += 1
            
            current_g = self.g_costs[current_id]
            
            # 3. Expansión
            for neighbor_id, cost_to_neighbor in self.grafo.get_neighbors(current_id).items():
                
                new_g = current_g + cost_to_neighbor

                # Si ya hemos encontrado un camino a este vecino Y el nuevo camino NO es mejor,
                # lo ignoramos.
                if neighbor_id in self.g_costs and new_g >= self.g_costs[neighbor_id]:
                    continue
                
                # ¡Hemos encontrado un camino mejor!
                self.g_costs[neighbor_id] = new_g
                h_neighbor = self._calculate_h(neighbor_id, goal_id)
                f_neighbor = new_g + h_neighbor
                
                # Añadir/Actualizar a la Lista Abierta
                self.open.push(f_neighbor, neighbor_id)
                
                # Actualizar el padre en la Lista Cerrada
                self.closed.add(neighbor_id, new_g, current_id)
                
        # Si la lista abierta está vacía y la meta no se alcanzó
        return None, nodes_expanded

    def reconstruct_path(self, start_id, goal_id, final_cost):
        """Reconstruye el camino en el formato de salida requerido."""
        path = []
        current = goal_id
        
        # Mapeo: {nodo_previo: costo_arista}
        edge_costs = {} 
        
        # Caminamos hacia atrás
        while current is not None:
            parent = self.closed.get_parent(current)
            if parent is not None:
                # Obtenemos el costo de la arista del grafo original
                cost = self.grafo.get_neighbors(parent).get(current, 0)
                edge_costs[parent] = cost
            path.append(current)
            current = parent

        path.reverse()
        
        if not path or path[0] != start_id:
            return "" # No se encontró un camino válido
        
        # Formato de salida: 1 - (1498) - 308 - (8718) - 309
        output = []
        for i in range(len(path) - 1):
            source = path[i]
            target = path[i+1]
            cost = self.grafo.get_neighbors(source).get(target)
            
            if i == 0:
                output.append(str(source))
            
            output.append(f" - ({cost}) - {target}")
            
        return "".join(output)