# best_first.py
import heapq

def best_first_search(start, goal_test, successors, heuristic):
    """Greedy best-first: prioritize state with lowest heuristic value"""
    heap = [(heuristic(start), start, None)]
    visited = set()
    parent = {start: None}
    while heap:
        h, node, _ = heapq.heappop(heap)
        if node in visited: continue
        visited.add(node)
        if goal_test(node):
            # reconstruct path
            path = []
            cur = node
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            return list(reversed(path))
        for nbr in successors(node):
            if nbr not in visited:
                parent[nbr] = node
                heapq.heappush(heap, (heuristic(nbr), nbr, node))
    return None

# Example: simple grid-like states with fake heuristic (Manhattan distance)
if __name__ == "__main__":
    start = (0,0)
    goal = (3,2)
    def goal_test(s): return s==goal
    def successors(s):
        x,y = s
        cand = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        return [c for c in cand if 0<=c[0]<=4 and 0<=c[1]<=4]
    def heuristic(s):
        return abs(s[0]-goal[0]) + abs(s[1]-goal[1])
    path = best_first_search(start, goal_test, successors, heuristic)
    print("Path:", path)
