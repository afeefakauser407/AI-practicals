import heapq

class Node:
    def _init_(self, state, parent=None, action=None, cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.heuristic = heuristic

    def _lt_(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

class GridPuzzle:
    def _init_(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state

    def search(self):
        open_list = []
        closed_list = set()
        heapq.heappush(open_list, Node(self.initial_state, heuristic=self.heuristic(self.initial_state)))

        while open_list:
            current_node = heapq.heappop(open_list)
            if current_node.state == self.goal_state:
                return self.construct_path(current_node)
            closed_list.add(current_node.state)
            for action, successor_state, step_cost in self.get_successors(current_node.state):
                if successor_state not in closed_list:
                    successor_node = Node(
                        state=successor_state,
                        parent=current_node,
                        action=action,
                        cost=current_node.cost + step_cost,
                        heuristic=self.heuristic(successor_state)
                    )
                    heapq.heappush(open_list, successor_node)
        return None

    def get_successors(self, state):
        successors = []
        n = len(state)  # Size of the grid
        empty_row, empty_col = self.find_empty_tile(state)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, Left, Down, Up
        for dx, dy in directions:
            new_row, new_col = empty_row + dx, empty_col + dy
            if 0 <= new_row < n and 0 <= new_col < n:
                new_state = [list(row) for row in state]
                new_state[empty_row][empty_col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[empty_row][empty_col]
                successors.append(('move', tuple(map(tuple, new_state)), 1))  # Step cost is 1 for each move
        return successors

    def find_empty_tile(self, state):
        for i, row in enumerate(state):
            for j, tile in enumerate(row):
                if tile == 0:  # Assuming 0 represents the empty tile
                    return i, j
        return -1, -1  # If no empty tile is found

    def heuristic(self, state):
        # Manhattan distance heuristic
        n = len(state)  # Size of the grid
        total_distance = 0
        for i in range(n):
            for j in range(n):
                tile = state[i][j]
                if tile != 0:
                    goal_row, goal_col = divmod(tile - 1, n)  # Goal position for the tile
                    total_distance += abs(i - goal_row) + abs(j - goal_col)
        return total_distance

    def construct_path(self, node):
        path = []
        while node:
            path.append((node.action, node.state))
            node = node.parent
        return path[::-1]

# Example usage:
initial_state = [
    [1, 2, 3],
    [4, 5, 6],
    [0, 7, 8]
]

goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

puzzle = GridPuzzle(initial_state, goal_state)
path = puzzle.search()

if path:
    print("Solution Path:")
    for action, state in path:
        print(f"{action} to {state}")
else:
    print("No solution found!")
