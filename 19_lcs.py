import time


def lcs(X, Y):
    m, n = len(X), len(Y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    result = ""
    i, j = m, n
    while i > 0 and j > 0:
        if X[i - 1] == Y[j - 1]:
            result = X[i - 1] + result
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return dp, result


X = "AGGTAB"
Y = "GXTXAYB"

start = time.perf_counter()
dp, seq = lcs(X, Y)
print("Time:", round((time.perf_counter() - start) * 1000, 3), "ms")

print("DP table:")
print("   ", list("-" + Y))
for i in range(len(dp)):
    print(("-" + X)[i], " ", dp[i])

print("LCS length:", dp[len(X)][len(Y)])
print("LCS:", seq)
print("Time complexity: O(m * n), Space: O(m * n)")
