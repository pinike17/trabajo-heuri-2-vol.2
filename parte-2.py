
import sys
import os
import time
from algoritmo import AStarSolver
from grafo import Grafo

def main():
    # --- 1. Lectura y Validación de Argumentos ---
    if len(sys.argv) != 5:
        print("Uso: ./parte-2.py <vertex-1> <vertex-2> <map-name> <output-file>", file=sys.stderr)
        sys.exit(1)

    try:
        start_id = int(sys.argv[1])
        goal_id = int(sys.argv[2])
    except ValueError:
        print("Error: Los IDs de los vértices deben ser números enteros.", file=sys.stderr)
        sys.exit(1)

    map_name = sys.argv[3]
    output_filepath = sys.argv[4]

    # --- 2. Carga del Grafo ---
    print(f"Cargando mapa: {map_name}...")
    try:
        grafo = Grafo()
        grafo.load(map_name)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error al cargar el grafo: {e}", file=sys.stderr)
        sys.exit(1)

    # --- 3. Ejecución del Algoritmo ---
    start_time = time.time()
    solver = AStarSolver(grafo)
    
    # Intenta resolver el problema
    optimal_cost, nodes_expanded = solver.solve(start_id, goal_id)
    end_time = time.time()
    
    execution_time = end_time - start_time
    
    # --- 4. Generación de la Salida de Pantalla (stdout) ---
    print(f"# vertices: {grafo.num_vertices}")
    print(f"# edges : {grafo.num_aristas}")
    
    if optimal_cost is not None:
        print(f"Optimal solution found with cost {int(optimal_cost)}")
    else:
        print("No se encontró solución (ruta no existe o error).")
        
    print(f"Execution time: {execution_time:.2f} seconds")
    
    # Cálculo de nodos/seg
    expansions_per_sec = nodes_expanded / execution_time if execution_time > 0 else 0
    print(f"# expansions: {nodes_expanded} ({expansions_per_sec:.2f} nodes/sec)")

    # --- 5. Generación del Archivo de Salida ---
    
    if optimal_cost is not None:
        path_output = solver.reconstruct_path(start_id, goal_id, optimal_cost)
        
        try:
            with open(output_filepath, 'w') as f:
                f.write(path_output + "\n")
            # print(f"Solución escrita en {output_filepath}")
        except Exception as e:
            print(f"Error al escribir en el archivo de salida {output_filepath}: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    # La especificación pide que los archivos .py estén en el mismo directorio.
    # Usamos un hack de Python para permitir que `algoritmo.py` importe las estructuras auxiliares
    # aunque no estén en un paquete formal.
    # Esto es necesario para ejecutar `parte-2.py` directamente.
    
    # Busca los módulos en el directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
        
    # El algoritmo utiliza referencias relativas, por lo que el `__init__` se asegura
    # de que la importación funcione.
    
    main()

