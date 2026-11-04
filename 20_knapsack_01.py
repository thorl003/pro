import time


def knapsack(weights, profits, W):
    n = len(weights)
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(W + 1):
            dp[i][w] = dp[i - 1][w]
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - weights[i - 1]] + profits[i - 1])

    items = []
    w = W
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            items.append(i - 1)
            w -= weights[i - 1]
    return dp, items[::-1]


weights = [5, 10, 15, 22, 25]
profits = [15, 25, 45, 55, 60]
W = 50

start = time.perf_counter()
dp, items = knapsack(weights, profits, W)
print("Time:", round((time.perf_counter() - start) * 1000, 3), "ms")

print("DP table (row i = first i items, column w = capacity 0 to", W, "):")
for i in range(len(dp)):
    print("Row", i, ":", dp[i])

print("Max profit:", dp[len(weights)][W])
print("Selected items (0-based):", items)
print("Selected weights:", [weights[i] for i in items], "total =", sum(weights[i] for i in items))
print("Selected profits:", [profits[i] for i in items], "total =", sum(profits[i] for i in items))
print("Time complexity: O(n * W), Space: O(n * W)")
