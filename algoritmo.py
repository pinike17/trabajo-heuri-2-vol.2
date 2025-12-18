from abierta import Abierta
from cerrada import Cerrada

class AStarSolver:
    # Implementation of the A* algorithm for pathfinding in a graph.

    def __init__(self, grafo):
        self.grafo = grafo
        self.closed = Cerrada()
        self.open = Abierta()
        self.g_costs = {}

    def _calculate_h(self, node_id, goal_id):
        # Compute the heuristic (h) using Haversine distance.
        return self.grafo.haversine_distance(node_id, goal_id)

    def solve(self, start_id, goal_id):
        # Execute the A* algorithm to find the shortest path from start_id to goal_id.
        
        # Vertex validation
        if start_id not in self.grafo.coords or goal_id not in self.grafo.coords:
            return 0, 0

        # Initialization
        self.g_costs[start_id] = 0
        h_start = self._calculate_h(start_id, goal_id)
        f_start = h_start
        
        self.open.push(f_start, start_id)
        self.closed.add(start_id, 0, None) 
        
        nodes_expanded = 0

        # Main loop
        while not self.open.is_empty():
            current_id = self.open.pop()

            if current_id == goal_id:
                return self.g_costs[goal_id], nodes_expanded
            
            nodes_expanded += 1
            
            current_g = self.g_costs[current_id]
            
            # Expand neighbors
            for neighbor_id, cost_to_neighbor in self.grafo.get_neighbors(current_id).items():
                
                new_g = current_g + cost_to_neighbor

                # If we have already found a better path to neighbor, skip it
                if neighbor_id in self.g_costs and new_g >= self.g_costs[neighbor_id]:
                    continue
                
                # A better path to neighbor found
                self.g_costs[neighbor_id] = new_g
                h_neighbor = self._calculate_h(neighbor_id, goal_id)
                f_neighbor = new_g + h_neighbor
                
                self.open.push(f_neighbor, neighbor_id)
                
                self.closed.add(neighbor_id, new_g, current_id)
                
        # No path found
        return None, nodes_expanded

    def reconstruct_path(self, start_id, goal_id, final_cost):
        # Reconstruct the path from start_id to goal_id using the closed set.
        path = []
        current = goal_id
        
        edge_costs = {} 
        
        while current is not None:
            parent = self.closed.get_parent(current)
            if parent is not None:
                cost = self.grafo.get_neighbors(parent).get(current, 0)
                edge_costs[parent] = cost
            path.append(current)
            current = parent

        path.reverse()
        
        if not path or path[0] != start_id:
            return "" # No path found
        
        output = []
        for i in range(len(path) - 1):
            source = path[i]
            target = path[i+1]
            cost = self.grafo.get_neighbors(source).get(target)
            
            if i == 0:
                output.append(str(source))
            
            output.append(f" - ({cost}) - {target}")
            
        return "".join(output)