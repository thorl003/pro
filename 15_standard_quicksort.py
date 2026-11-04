import random
import time
import sys

sys.setrecursionlimit(10000)


def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quicksort(arr, low, high):
    if low < high:
        p = partition(arr, low, high)
        quicksort(arr, low, p - 1)
        quicksort(arr, p + 1, high)


def measure(arr):
    a = arr[:]
    start = time.perf_counter()
    quicksort(a, 0, len(a) - 1)
    return round((time.perf_counter() - start) * 1000, 3)


arr = [10, 7, 8, 9, 1, 5, 3]
quicksort(arr, 0, len(arr) - 1)
print(arr)

random.seed(1)
for n in [500, 1000, 2000]:
    random_arr = [random.randint(1, 10000) for _ in range(n)]
    sorted_arr = list(range(n))
    print("n =", n, "| random:", measure(random_arr), "ms | sorted:", measure(sorted_arr), "ms")

print("Time complexity: best/average = O(n log n), worst = O(n^2) on sorted input")
