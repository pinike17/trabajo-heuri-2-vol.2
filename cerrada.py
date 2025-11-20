# cerrada.py

class Cerrada:
    """
    Implementación de la Lista Cerrada usando un diccionario (Hash Map).
    Almacena los nodos ya expandidos y el costo g(n) con el que se expandieron.
    """

    def __init__(self):
        # {node_id: g_cost}
        self.expanded_nodes = {}
        # {node_id: parent_node_id} para reconstruir el camino
        self.parents = {}

    def is_expanded(self, node_id):
        """Verifica si un nodo ha sido expandido."""
        return node_id in self.expanded_nodes

    def get_cost(self, node_id):
        """Retorna el costo g(n) con el que el nodo fue expandido."""
        return self.expanded_nodes.get(node_id)

    def add(self, node_id, g_cost, parent_id):
        """Añade o actualiza un nodo en la lista cerrada."""
        self.expanded_nodes[node_id] = g_cost
        self.parents[node_id] = parent_id
        
    def get_parent(self, node_id):
        """Retorna el padre de un nodo."""
        return self.parents.get(node_id)
        
    def __len__(self):
        """Retorna el número de nodos en la lista cerrada (nodos expandidos)."""
        return len(self.expanded_nodes)