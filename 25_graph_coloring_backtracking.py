import time


def is_safe(graph, color, u, c):
    return all(color[v] != c for v in graph[u])


def solve(graph, m, color, u):
    if u == len(graph):
        return True
    for c in range(m):
        if is_safe(graph, color, u, c):
            color[u] = c
            if solve(graph, m, color, u + 1):
                return True
            color[u] = -1
    return False


def chromatic_number(graph):
    m = 1
    while True:
        color = [-1] * len(graph)
        if solve(graph, m, color, 0):
            return m, color
        m += 1


graph = [
    [1, 2, 3],
    [0, 2],
    [0, 1, 3],
    [0, 2, 4],
    [3]
]

start = time.perf_counter()
m, color = chromatic_number(graph)
print("Time:", round((time.perf_counter() - start) * 1000, 3), "ms")
print("Chromatic number:", m)
print("Colors:", color)
print("Valid:", all(color[u] != color[v] for u in range(len(graph)) for v in graph[u]))
print("Time complexity: O(m^V)")
