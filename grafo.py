# grafo.py

import os
from math import radians, sin, cos, sqrt, atan2

class Grafo:
    """
    Define y carga el grafo y las coordenadas de los archivos .gr y .co.
    """
    
    # Radio de la Tierra en metros (para la fórmula de Haversine)
    R_TIERRA = 6371000  # metros

    def __init__(self):
        # {origen: {destino: costo_distancia}}
        self.adj = {}
        # {vertice: (latitud_en_radianes, longitud_en_radianes)}
        self.coords = {}
        self.num_vertices = 0
        self.num_aristas = 0

    def load(self, map_name):
        """Carga los archivos .gr y .co a partir del nombre del mapa."""
        
        # 1. Cargar coordenadas (.co)
        coord_file = f"{map_name}.co"
        self._load_coords(coord_file)
        
        # 2. Cargar aristas (.gr)
        graph_file = f"{map_name}.gr"
        self._load_graph(graph_file)

    def _load_coords(self, filepath):
        """Carga las coordenadas geográficas de los vértices."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Archivo de coordenadas no encontrado: {filepath}")
            
        with open(filepath, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 4 and parts[0] == 'v':
                    # v <id> <lon*10^6> <lat*10^6>
                    vertex_id = int(parts[1])
                    # La especificación invierte el orden: (lat, lon)
                    lon = int(parts[2]) / 10**6
                    lat = int(parts[3]) / 10**6
                    
                    # Almacenamos en radianes para usar directamente en Haversine
                    self.coords[vertex_id] = (radians(lat), radians(lon))
                    self.num_vertices += 1
        
        if self.num_vertices == 0:
             raise ValueError(f"No se pudieron cargar vértices del archivo {filepath}")
             

    def _load_graph(self, filepath):
        """Carga las aristas y sus costos de distancia."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Archivo de grafo no encontrado: {filepath}")
            
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
            raise ValueError(f"No se pudieron cargar aristas del archivo {filepath}")

    def get_neighbors(self, node_id):
        """Retorna los vecinos y sus costos para un nodo."""
        return self.adj.get(node_id, {})

    def haversine_distance(self, node_a_id, node_b_id):
        """Calcula la distancia en línea recta (Haversine) entre dos nodos en metros."""
        
        # Esta función es la heurística h(n), la distancia del gran círculo.
        if node_a_id not in self.coords or node_b_id not in self.coords:
            # Si faltan coordenadas, la distancia es infinita, pero para la heurística
            # se debe usar una distancia calculada, si no existe la coordenada, algo salió mal.
            return 0 
            
        lat1, lon1 = self.coords[node_a_id]
        lat2, lon2 = self.coords[node_b_id]

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = self.R_TIERRA * c
        return distance