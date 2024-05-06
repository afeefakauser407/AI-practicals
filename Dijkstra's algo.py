import heapq

class Graph:
    def _init_(self):
        self.graph = {}

    def add_edge(self, u, v, weight):
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append((v, weight))

    def dijkstra(self, start):
        min_heap = [(0, start)]
        visited = set()

        while min_heap:
            dist, node = heapq.heappop(min_heap)
            if node not in visited:
                visited.add(node)
                print(node, end=' ')
                for neighbor, weight in self.graph.get(node, []):
                    if neighbor not in visited:
                        heapq.heappush(min_heap, (dist + weight, neighbor))

# Example usage:
g = Graph()
g.add_edge('A', 'B', 2)
g.add_edge('A', 'C', 4)
g.add_edge('B', 'C', 1)
g.add_edge('B', 'D', 7)
g.add_edge('C', 'D', 3)

print("Shortest path from node 'A' using Dijkstra's Algorithm:")
g.dijkstra('A')
