import time


def saturation(graph, color, v):
    return len({color[w] for w in graph[v] if color[w] != -1})


def dsatur(graph):
    n = len(graph)
    color = [-1] * n
    for _ in range(n):
        uncolored = [v for v in range(n) if color[v] == -1]
        u = max(uncolored, key=lambda v: (saturation(graph, color, v), len(graph[v])))
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
color = dsatur(graph)
print("Time:", round((time.perf_counter() - start) * 1000, 3), "ms")
print("Colors:", color)
print("Colors used:", max(color) + 1)
print("Valid:", all(color[u] != color[v] for u in range(len(graph)) for v in graph[u]))
print("Time complexity: O(V^2)")
