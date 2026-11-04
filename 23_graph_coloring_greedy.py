import time


def greedy_coloring(graph):
    n = len(graph)
    color = [-1] * n
    order = sorted(range(n), key=lambda v: len(graph[v]), reverse=True)
    for u in order:
        used = {color[v] for v in graph[u]}
        c = 0
        while c in used:
            c += 1
        color[u] = c
    return color


graph = [
    [1, 2, 3],
    [0, 2],
    [0, 1, 3],
    [0, 2, 4],
    [3]
]

start = time.perf_counter()
color = greedy_coloring(graph)
print("Time:", round((time.perf_counter() - start) * 1000, 3), "ms")
print("Colors:", color)
print("Colors used:", max(color) + 1)
print("Valid:", all(color[u] != color[v] for u in range(len(graph)) for v in graph[u]))
print("Time complexity: O(V log V + E)")
