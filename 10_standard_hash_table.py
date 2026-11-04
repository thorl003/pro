import time


class HashSet:
    THRESHOLD = 4

    def __init__(self, capacity=4):
        self.table = [[] for _ in range(capacity)]
        self.size = 0

    def bucket(self, key):
        return self.table[hash(key) % len(self.table)]

    def contains(self, key):
        return key in self.bucket(key)

    def add(self, key):
        b = self.bucket(key)
        if key in b:
            return False
        b.append(key)
        self.size += 1
        if self.size / len(self.table) > self.THRESHOLD:
            self.resize()
        return True

    def remove(self, key):
        b = self.bucket(key)
        if key not in b:
            return False
        b.remove(key)
        self.size -= 1
        return True

    def resize(self):
        new_table = [[] for _ in range(2 * len(self.table))]
        for b in self.table:
            for key in b:
                new_table[hash(key) % len(new_table)].append(key)
        self.table = new_table


def run(op):
    start = time.perf_counter()
    for k in range(1000):
        op(k)
    return round((time.perf_counter() - start) * 1000, 3)


s = HashSet()
print("Insert:", run(s.add), "ms")
print("Size after insert:", s.size)
print("Search:", run(s.contains), "ms")
print(s.contains(500), s.contains(5000))
print("Delete:", run(s.remove), "ms")
print("Size after delete:", s.size)
print("Time complexity: add, remove, contains = O(1) average, O(n) worst")
