import threading
import time


class StripedHashSet:
    THRESHOLD = 4

    def __init__(self, capacity=4):
        self.table = [[] for _ in range(capacity)]
        self.locks = [threading.Lock() for _ in range(capacity)]
        self.size = 0
        self.size_lock = threading.Lock()

    def lock_for(self, key):
        return self.locks[hash(key) % len(self.locks)]

    def bucket(self, key):
        return self.table[hash(key) % len(self.table)]

    def contains(self, key):
        with self.lock_for(key):
            return key in self.bucket(key)

    def add(self, key):
        with self.lock_for(key):
            b = self.bucket(key)
            if key in b:
                return False
            b.append(key)
            with self.size_lock:
                self.size += 1
        if self.size / len(self.table) > self.THRESHOLD:
            self.resize()
        return True

    def remove(self, key):
        with self.lock_for(key):
            b = self.bucket(key)
            if key not in b:
                return False
            b.remove(key)
            with self.size_lock:
                self.size -= 1
            return True

    def resize(self):
        old_capacity = len(self.table)
        for lock in self.locks:
            lock.acquire()
        if old_capacity == len(self.table):
            new_table = [[] for _ in range(2 * old_capacity)]
            for b in self.table:
                for key in b:
                    new_table[hash(key) % len(new_table)].append(key)
            self.table = new_table
        for lock in self.locks:
            lock.release()


def work(op, start):
    for k in range(start, start + 250):
        op(k)


def run(op):
    start = time.perf_counter()
    threads = [threading.Thread(target=work, args=(op, i * 250)) for i in range(4)]
    for t in threads: t.start()
    for t in threads: t.join()
    return round((time.perf_counter() - start) * 1000, 3)


s = StripedHashSet()
print("Insert:", run(s.add), "ms")
print("Size after insert:", s.size)
print("Search:", run(s.contains), "ms")
print(s.contains(500), s.contains(5000))
print("Delete:", run(s.remove), "ms")
print("Size after delete:", s.size)
print("Time complexity: add, remove, contains = O(1) average, resize = O(n)")
