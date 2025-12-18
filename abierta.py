import heapq

class Abierta:
    # Implements a priority queue for A* search algorithm.

    def __init__(self):
        # Heap to store the nodes based on their f(n) cost.
        self._heap = []
        # Dictionary to track the best f(n) cost for each node.
        self._entry_finder = {} # {node_id: f_cost}
        # Unique sequence count to break ties in heapq.
        self._counter = 0

    def push(self, f_cost, node_id):
        # Add a new node or update the f(n) cost of an existing node.
        
        # If the node is already in the open list with a lower f(n) cost, ignore this entry.
        if node_id in self._entry_finder and f_cost >= self._entry_finder[node_id]:
            return

        entry = [f_cost, self._counter, node_id]
        heapq.heappush(self._heap, entry)
        self._entry_finder[node_id] = f_cost
        self._counter += 1

    def pop(self):
        # Remove and return the node with the lowest f(n) cost.
        if not self._heap:
            raise IndexError("pop from empty heap")

        while self._heap:
            
            f_cost, _, node_id = heapq.heappop(self._heap)
            
            if node_id in self._entry_finder and f_cost == self._entry_finder[node_id]:
                del self._entry_finder[node_id] 
                return node_id
   
        raise IndexError("pop from empty heap") # In case all entries were outdated
        
    def is_empty(self):
        # Check if the open list is empty.
        return not self._entry_finder