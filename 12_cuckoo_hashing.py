import time


class CuckooHashSet:
    LIMIT = 10

    def __init__(self, capacity=8):
        self.capacity = capacity
        self.table = [[None] * capacity, [None] * capacity]

    def slot(self, i, key):
        h = key if i == 0 else key // 10
        return h % self.capacity

    def contains(self, key):
        return self.table[0][self.slot(0, key)] == key or self.table[1][self.slot(1, key)] == key

    def remove(self, key):
        for i in (0, 1):
            s = self.slot(i, key)
            if self.table[i][s] == key:
                self.table[i][s] = None
                return True
        return False

    def swap(self, i, key):
        s = self.slot(i, key)
        old = self.table[i][s]
        self.table[i][s] = key
        return old

    def add(self, key):
        if self.contains(key):
            return False
        for _ in range(self.LIMIT):
            key = self.swap(0, key)
            if key is None:
                return True
            key = self.swap(1, key)
            if key is None:
                return True
        self.resize()
        return self.add(key)

    def resize(self):
        old_keys = [k for row in self.table for k in row if k is not None]
        self.capacity *= 2
        self.table = [[None] * self.capacity, [None] * self.capacity]
        for k in old_keys:
            self.add(k)

    def items(self):
        return [k for row in self.table for k in row if k is not None]


def run(op):
    start = time.perf_counter()
    for k in range(1000):
        op(k)
    return round((time.perf_counter() - start) * 1000, 3)


s = CuckooHashSet()
print("Insert:", run(s.add), "ms")
print("Size after insert:", len(s.items()))
print("Search:", run(s.contains), "ms")
print(s.contains(500), s.contains(5000))
print("Delete:", run(s.remove), "ms")
print("Size after delete:", len(s.items()))
print("Time complexity: contains, remove = O(1) worst, add = O(1) expected, resize = O(n)")
