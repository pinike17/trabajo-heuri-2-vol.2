# grafo.py

import os
from math import radians, sin, cos, sqrt, atan2

class Grafo:
    # This class represents a directed graph with geographic coordinates for each vertex.
    
    R_EARTH = 6371000  # meters

    def __init__(self):
        self.adj = {}
        self.coords = {}
        self.num_vertices = 0
        self.num_aristas = 0

    def load(self, map_name):
        # Load graph data from .co and .gr files. 
        
        coord_file = f"{map_name}.co"
        self._load_coords(coord_file)
        
        graph_file = f"{map_name}.gr"
        self._load_graph(graph_file)

    def _load_coords(self, filepath):
        # Load vertex coordinates from file.
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
            
        with open(filepath, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 4 and parts[0] == 'v':
                    # v <id> <lon*10^6> <lat*10^6>
                    vertex_id = int(parts[1])
                    # Convert to degrees
                    lon = int(parts[2]) / 10**6
                    lat = int(parts[3]) / 10**6

                    self.coords[vertex_id] = (radians(lat), radians(lon))
                    self.num_vertices += 1
        
        if self.num_vertices == 0:
             raise ValueError(f"Could not load vertex from file {filepath}")
             

    def _load_graph(self, filepath):
        # Load edges from file.
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
            
        with open(filepath, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 4 and parts[0] == 'a':
                    # a <from> <to> <cost>
                    source = int(parts[1])
                    target = int(parts[2])
                    cost = int(parts[3])
                    
                    if source not in self.adj:
                        self.adj[source] = {}
                    
                    self.adj[source][target] = cost
                    self.num_aristas += 1
                    
        if self.num_aristas == 0:
            raise ValueError(f"Could not load edges from file: {filepath}")

    def get_neighbors(self, node_id):
        # Return neighbors and costs for a given node.
        return self.adj.get(node_id, {})

    def haversine_distance(self, node_a_id, node_b_id):
        # Calculate the Haversine distance between two nodes.
        
        if node_a_id not in self.coords or node_b_id not in self.coords:
            return 0 
            
        lat1, lon1 = self.coords[node_a_id]
        lat2, lon2 = self.coords[node_b_id]

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = self.R_EARTH * c
        return distance