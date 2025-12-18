import sys
import os
import time
from algoritmo import AStarSolver
from grafo import Grafo

def main():
    # Argument parsing
    if len(sys.argv) != 5:
        print("Usage: ./parte-2.py <vertex-1> <vertex-2> <map-name> <output-file>", file=sys.stderr)
        sys.exit(1)

    try:
        start_id = int(sys.argv[1])
        goal_id = int(sys.argv[2])
    except ValueError:
        print("Error: ", file=sys.stderr)
        sys.exit(1)

    map_name = sys.argv[3]
    output_filepath = sys.argv[4]

    # Loading the graph
    print(f"Loading map: {map_name}...")
    try:
        grafo = Grafo()
        grafo.load(map_name)
    except FileNotFoundError as e:
        print(f"Error: file not found. {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error while loading the graph: {e}", file=sys.stderr)
        sys.exit(1)

    # Algorithm execution
    start_time = time.time()
    solver = AStarSolver(grafo)
    
    # Try to solve the problem
    optimal_cost, nodes_expanded = solver.solve(start_id, goal_id)
    end_time = time.time()
    
    execution_time = end_time - start_time
    
    # Screen output
    print(f"# vertices: {grafo.num_vertices}")
    print(f"# edges : {grafo.num_aristas}")
    
    if optimal_cost is not None:
        print(f"Optimal solution found with cost {int(optimal_cost)}")
    else:
        print("Could not find a solution.")
        
    print(f"Execution time: {execution_time:.2f} seconds")
    
    # Calculate expansions per second
    expansions_per_sec = nodes_expanded / execution_time if execution_time > 0 else 0
    print(f"# expansions: {nodes_expanded} ({expansions_per_sec:.2f} nodes/sec)")

    # Output file writing
    
    if optimal_cost is not None:
        path_output = solver.reconstruct_path(start_id, goal_id, optimal_cost)
        
        try:
            with open(output_filepath, 'w') as f:
                f.write(path_output + "\n")
        except Exception as e:
            print(f"Error al escribir en el archivo de salida {output_filepath}: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    
    # Look for modules in the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    main()

