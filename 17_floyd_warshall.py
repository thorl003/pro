import time

INF = float('inf')


def floyd_warshall(graph):
    n = len(graph)
    dist = [row[:] for row in graph]
    nxt = [[j if graph[i][j] != INF else None for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    nxt[i][j] = nxt[i][k]
    return dist, nxt


def path(nxt, i, j):
    if nxt[i][j] is None:
        return []
    route = [i]
    while i != j:
        i = nxt[i][j]
        route.append(i)
    return route


cities = ["Chennai", "Vellore", "Salem", "Madurai"]
graph = [
    [0, 3, INF, 5],
    [2, 0, INF, 4],
    [INF, 1, 0, INF],
    [INF, INF, 2, 0]
]

start = time.perf_counter()
dist, nxt = floyd_warshall(graph)
print("Time:", round((time.perf_counter() - start) * 1000, 3), "ms")

print("Initial distance matrix:")
for row in graph:
    print(row)

print("Shortest distance matrix:")
for row in dist:
    print(row)

for i in range(len(cities)):
    for j in range(len(cities)):
        if i != j:
            route = " -> ".join(cities[v] for v in path(nxt, i, j))
            print(cities[i], "to", cities[j], "=", dist[i][j], ":", route)

print("Time complexity: O(V^3), Space: O(V^2)")
