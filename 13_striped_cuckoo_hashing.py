import threading
import time


class StripedCuckooHashSet:
    LIMIT = 10

    def __init__(self, capacity=8):
        self.capacity = capacity
        self.table = [[None] * capacity, [None] * capacity]
        self.locks = [[threading.Lock() for _ in range(capacity)] for _ in range(2)]

    def hash(self, i, key):
        return key if i == 0 else key // 10

    def slot(self, i, key):
        return self.hash(i, key) % self.capacity

    def acquire(self, key):
        L = len(self.locks[0])
        self.locks[0][self.hash(0, key) % L].acquire()
        self.locks[1][self.hash(1, key) % L].acquire()

    def release(self, key):
        L = len(self.locks[0])
        self.locks[1][self.hash(1, key) % L].release()
        self.locks[0][self.hash(0, key) % L].release()

    def acquire_all(self):
        for i in (0, 1):
            for lock in self.locks[i]:
                lock.acquire()

    def release_all(self):
        for i in (0, 1):
            for lock in self.locks[i]:
                lock.release()

    def _contains(self, key):
        return self.table[0][self.slot(0, key)] == key or self.table[1][self.slot(1, key)] == key

    def swap(self, i, key):
        s = self.slot(i, key)
        old = self.table[i][s]
        self.table[i][s] = key
        return old

    def _add(self, key):
        if self._contains(key):
            return False
        for _ in range(self.LIMIT):
            key = self.swap(0, key)
            if key is None:
                return True
            key = self.swap(1, key)
            if key is None:
                return True
        self.resize()
        return self._add(key)

    def resize(self):
        old_keys = [k for row in self.table for k in row if k is not None]
        self.capacity *= 2
        self.table = [[None] * self.capacity, [None] * self.capacity]
        for k in old_keys:
            self._add(k)

    def contains(self, key):
        self.acquire(key)
        result = self._contains(key)
        self.release(key)
        return result

    def remove(self, key):
        self.acquire(key)
        result = False
        for i in (0, 1):
            s = self.slot(i, key)
            if self.table[i][s] == key:
                self.table[i][s] = None
                result = True
                break
        self.release(key)
        return result

    def add(self, key):
        self.acquire(key)
        if self._contains(key):
            self.release(key)
            return False
        for i in (0, 1):
            s = self.slot(i, key)
            if self.table[i][s] is None:
                self.table[i][s] = key
                self.release(key)
                return True
        self.release(key)
        self.acquire_all()
        result = self._add(key)
        self.release_all()
        return result

    def items(self):
        return [k for row in self.table for k in row if k is not None]


def work(op, start):
    for k in range(start, start + 250):
        op(k)


def run(op):
    start = time.perf_counter()
    threads = [threading.Thread(target=work, args=(op, i * 250)) for i in range(4)]
    for t in threads: t.start()
    for t in threads: t.join()
    return round((time.perf_counter() - start) * 1000, 3)


s = StripedCuckooHashSet()
print("Insert:", run(s.add), "ms")
print("Size after insert:", len(s.items()))
print("Search:", run(s.contains), "ms")
print(s.contains(500), s.contains(5000))
print("Delete:", run(s.remove), "ms")
print("Size after delete:", len(s.items()))
print("Time complexity: contains, remove = O(1), add = O(1) expected, resize = O(n)")
