import sys
from constraint import Problem, ExactSumConstraint, FunctionConstraint
import time

def read_input_board(filepath):
    # Reads the input file and returns a list of lists representing the board.
    board = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    board.append(list(line))
    except FileNotFoundError:
        print(f"Error: Input file not found at {filepath}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Basic validation
    if not board:
        print("Error: Input file is empty.", file=sys.stderr)
        sys.exit(1)
    
    n = len(board)
    for row in board:
        if len(row) != n:
            print("Error: Input board is not square.", file=sys.stderr)
            sys.exit(1)
        for cell in row:
            if cell not in ('.', 'X', 'O'):
                print(f"Error: Invalid character '{cell}' in input board.", file=sys.stderr)
                sys.exit(1)

    # BINAIRO puzzles must have an even dimension
    if n % 2 != 0:
        print(f"Error: Board dimension (n={n}) must be an even number.", file=sys.stderr)
        sys.exit(1)

    return board, n

def get_board_string(board_data, n):
    # Returns a string representation of the board in the required format.
    # Helper to get the character for a cell
    def get_char(i, j):
        if isinstance(board_data, dict):
            val = board_data.get((i, j))
            if val == 1:
                return 'X'
            elif val == 0:
                return 'O'
            else:
                return ' '  # Should not happen in a full solution
        else:
            # It's a list of lists: [['.', 'X'], ['O', '.']]
            val = board_data[i][j]
            return val if val != '.' else ' '

    border_line = "+---" * n + "+\n"
    output_str = border_line
    for i in range(n):
        output_str += "|"
        for j in range(n):
            output_str += f" {get_char(i, j)} |"
        output_str += "\n" + border_line
    return output_str

def solve_binairo(initial_board, n):
    """
    Models and solves the BINAIRO CSP.
    """
    problem = Problem()

    # One variable for each cell (i, j)
    # Domain is {0, 1} where 0 = 'O' (white) and 1 = 'X' (black)
    variables = [(i, j) for i in range(n) for j in range(n)]
    problem.addVariables(variables, [0, 1])
    
    # Constraint A: Initial State
    # Set the value for pre-filled cells
    for i in range(n):
        for j in range(n):
            cell = initial_board[i][j]
            if cell == 'X':
                problem.addConstraint(lambda var: var == 1, [(i, j)])
            elif cell == 'O':
                problem.addConstraint(lambda var: var == 0, [(i, j)])

    # Constraint B & C: Equal discs in each row and column
    # The sum of each row/col must be n/2
    half_n = n // 2
    for i in range(n):
        # Rows
        row_vars = [(i, j) for j in range(n)]
        problem.addConstraint(ExactSumConstraint(half_n), row_vars)
        
        # Columns
        col_vars = [(j, i) for j in range(n)]
        problem.addConstraint(ExactSumConstraint(half_n), col_vars)

    # Constraint D & E: No more than two consecutive
    # The sum of any 3 consecutive cells cannot be 0 (OOO) or 3 (XXX)
    def no_three_consecutive(a, b, c):
        s = a + b + c
        return s != 0 and s != 3

    for i in range(n):
        # Rows
        for j in range(n - 2):
            triplet = [(i, j), (i, j+1), (i, j+2)]
            problem.addConstraint(no_three_consecutive, triplet)
        
        # Columns
        for j in range(n - 2):
            triplet = [(j, i), (j+1, i), (j+2, i)]
            problem.addConstraint(no_three_consecutive, triplet)

    # Solve
    solutions = problem.getSolutions()
    return solutions

def main():
    # Handle Arguments
    if len(sys.argv) != 3:
        print("Usage: ./parte-1.py <input-file> <output-file>", file=sys.stderr)
        sys.exit(1)

    input_filepath = sys.argv[1]
    output_filepath = sys.argv[2]

    # Read Input
    initial_board, n = read_input_board(input_filepath)
    initial_board_str = get_board_string(initial_board, n)

    # Solve
    start_time = time.time()
    solutions = solve_binairo(initial_board, n)
    end_time = time.time()    # Stop the timer
    execution_time = end_time - start_time

    num_solutions = len(solutions)

    # Screen Output
    
    print(initial_board_str, end='')
    print(f"{num_solutions} solutions found")
    print(f"Execution time: {execution_time:.4f} seconds")

    # File Output
    
    try:
        with open(output_filepath, 'w') as f:
            # Write the instance
            f.write(initial_board_str)
            
            # Write one solution if found
            if num_solutions > 0:
                f.write("\n\n\n")
                first_solution = solutions[0]
                solution_str = get_board_string(first_solution, n)
                f.write(solution_str)
                
    except Exception as e:
        print(f"Error writing to output file {output_filepath}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()