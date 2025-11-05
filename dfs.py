# dfs.py
def dfs_recursive(graph, node, visited=None, order=None):
    if visited is None:
        visited = set(); order = []
    visited.add(node)
    order.append(node)
    for nbr in graph.get(node, []):
        if nbr not in visited:
            dfs_recursive(graph, nbr, visited, order)
    return order

def dfs_iterative(graph, start):
    visited = set(); stack = [start]; order = []
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            order.append(node)
            # push neighbors in reverse for same order as recursive
            for nbr in reversed(graph.get(node, [])):
                if nbr not in visited:
                    stack.append(nbr)
    return order

if __name__ == "__main__":
    g = {'A':['B','C'],'B':['D'],'C':['E'],'D':[],'E':[]}
    print("DFS recursive:", dfs_recursive(g,'A'))
    print("DFS iterative:", dfs_iterative(g,'A'))
