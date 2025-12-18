class Cerrada:
    # Implements the closed list for A* search algorithm.

    def __init__(self):
        self.expanded_nodes = {}
        self.parents = {}

    def is_expanded(self, node_id):
        #verifies if a node has been expanded
        return node_id in self.expanded_nodes

    def get_cost(self, node_id):
        # Returns the g cost of a node if it has been expanded, otherwise None.
        return self.expanded_nodes.get(node_id)

    def add(self, node_id, g_cost, parent_id):
        # Adds a node to the closed list with its g cost and parent.
        self.expanded_nodes[node_id] = g_cost
        self.parents[node_id] = parent_id
        
    def get_parent(self, node_id):
        # Returns the parent of a node if it exists, otherwise None.
        return self.parents.get(node_id)
        
    def __len__(self):
        # Returns the number of expanded nodes.
        return len(self.expanded_nodes)