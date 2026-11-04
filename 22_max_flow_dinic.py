import time
from collections import deque


def bfs(cap, s):
    n = len(cap)
    level = [-1] * n
    level[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()
        for v in range(n):
            if level[v] == -1 and cap[u][v] > 0:
                level[v] = level[u] + 1
                q.append(v)
    return level


def dfs(cap, u, t, flow, level):
    if u == t:
        return flow
    for v in range(len(cap)):
        if cap[u][v] > 0 and level[v] == level[u] + 1:
            pushed = dfs(cap, v, t, min(flow, cap[u][v]), level)
            if pushed > 0:
                cap[u][v] -= pushed
                cap[v][u] += pushed
                return pushed
    return 0


def dinic(graph, s, t):
    cap = [row[:] for row in graph]
    max_flow = 0
    while True:
        level = bfs(cap, s)
        if level[t] == -1:
            break
        while True:
            pushed = dfs(cap, s, t, float('inf'), level)
            if pushed == 0:
                break
            max_flow += pushed
    return max_flow


graph = [
    [0, 16, 13, 0, 0, 0],
    [0, 0, 0, 12, 0, 0],
    [0, 4, 0, 0, 14, 0],
    [0, 0, 9, 0, 0, 20],
    [0, 0, 0, 7, 0, 4],
    [0, 0, 0, 0, 0, 0]
]

start = time.perf_counter()
max_flow = dinic(graph, 0, 5)
print("Time:", round((time.perf_counter() - start) * 1000, 3), "ms")
print("Max flow:", max_flow)
print("Time complexity: O(V^2 * E)")
