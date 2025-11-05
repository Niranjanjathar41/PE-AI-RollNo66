# bfs.py
from collections import deque

def bfs(graph, start):
    visited = set()
    order = []
    q = deque([start])
    visited.add(start)
    while q:
        node = q.popleft()
        order.append(node)
        for nbr in graph.get(node, []):
            if nbr not in visited:
                visited.add(nbr)
                q.append(nbr)
    return order

if __name__ == "__main__":
    g = {
        'A': ['B','C'],
        'B': ['D','E'],
        'C': ['F'],
        'D': [], 'E': [], 'F': []
    }
    print("BFS order:", bfs(g, 'A'))
