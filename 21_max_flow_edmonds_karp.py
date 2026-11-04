import time
from collections import deque


def bfs(cap, s, parent):
    n = len(cap)
    visited = [False] * n
    visited[s] = True
    q = deque([s])
    while q:
        u = q.popleft()
        for v in range(n):
            if not visited[v] and cap[u][v] > 0:
                visited[v] = True
                parent[v] = u
                q.append(v)
    return visited


def edmonds_karp(graph, s, t):
    n = len(graph)
    cap = [row[:] for row in graph]
    parent = [-1] * n
    max_flow = 0
    while True:
        visited = bfs(cap, s, parent)
        if not visited[t]:
            break
        flow = float('inf')
        path = [t]
        v = t
        while v != s:
            u = parent[v]
            flow = min(flow, cap[u][v])
            path.append(u)
            v = u
        print("Augmenting path:", path[::-1], "bottleneck:", flow)
        v = t
        while v != s:
            u = parent[v]
            cap[u][v] -= flow
            cap[v][u] += flow
            v = u
        max_flow += flow
    cut = [(u, v) for u in range(n) for v in range(n) if visited[u] and not visited[v] and graph[u][v] > 0]
    return max_flow, cut


graph = [
    [0, 16, 13, 0, 0, 0],
    [0, 0, 0, 12, 0, 0],
    [0, 4, 0, 0, 14, 0],
    [0, 0, 9, 0, 0, 20],
    [0, 0, 0, 7, 0, 4],
    [0, 0, 0, 0, 0, 0]
]

start = time.perf_counter()
max_flow, cut = edmonds_karp(graph, 0, 5)
print("Time:", round((time.perf_counter() - start) * 1000, 3), "ms")
print("Max flow:", max_flow)
print("Min cut edges:", cut)
print("Time complexity: O(V * E^2)")
